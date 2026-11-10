from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from decimal import Decimal
import uuid
import datetime
from typing import List, Optional

from app.database.session import get_db
from app.models.order import Order, OrderItem
from app.models.cart import Cart, CartItem
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.address import Address
from app.models.delivery import Delivery
from app.models.payment import Payment
from app.models.profile import SupplierProfile
from app.models.user import User
from app.models.enums import OrderStatus, PaymentStatus, DeliveryStatus, UserRole
from app.schemas.order import OrderCreate, OrderOut, OrderStatusUpdate, AddressCreate, AddressOut
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders & Checkout"])

def generate_order_number() -> str:
    now = datetime.datetime.now()
    unique_suffix = uuid.uuid4().hex[:6].upper()
    return f"SB-{now.strftime('%Y%m%d')}-{unique_suffix}"

def generate_tracking_number() -> str:
    return f"TRK-{uuid.uuid4().hex[:10].upper()}"

def enrich_order_out(order: Order) -> OrderOut:
    items_out = []
    for item in order.items:
        items_out.append({
            "id": item.id,
            "product_id": item.product_id,
            "product_name": item.product.name if item.product else "Material",
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "total_price": item.total_price,
            "unit": item.product.unit if item.product else None,
            "supplier_name": item.supplier.company_name if item.supplier else None,
            "status": item.status
        })

    delivery_data = None
    if order.deliveries:
        deliv = order.deliveries[0] if isinstance(order.deliveries, list) else order.deliveries
        delivery_data = {
            "id": deliv.id,
            "tracking_number": deliv.tracking_number,
            "status": deliv.status,
            "pickup_time": deliv.pickup_time,
            "estimated_delivery_time": deliv.estimated_delivery_time,
            "actual_delivery_time": deliv.actual_delivery_time
        }

    return OrderOut(
        id=order.id,
        order_number=order.order_number,
        user_id=order.user_id,
        customer_name=order.user.name if order.user else None,
        customer_email=order.user.email if order.user else None,
        total_amount=order.total_amount,
        tax_amount=order.tax_amount,
        delivery_fee=order.delivery_fee,
        discount_amount=order.discount_amount,
        net_amount=order.net_amount,
        status=order.status,
        payment_status=order.payment_status,
        payment_method=order.payment_method,
        notes=order.notes,
        ordered_at=order.ordered_at,
        delivery_address=order.delivery_address,
        items=items_out,
        delivery=delivery_data
    )

@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Fetch user's cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Shopping cart is empty. Add materials before checkout.")

    # 2. Resolve delivery address
    address_id = order_in.delivery_address_id
    if not address_id and order_in.new_address:
        new_addr = Address(
            user_id=current_user.id,
            **order_in.new_address.model_dump()
        )
        db.add(new_addr)
        db.flush()
        address_id = new_addr.id

    if not address_id:
        # Check if user has an existing default address
        default_addr = db.query(Address).filter(Address.user_id == current_user.id, Address.is_default == True).first()
        if not default_addr:
            default_addr = db.query(Address).filter(Address.user_id == current_user.id).first()
        if default_addr:
            address_id = default_addr.id
        else:
            # Create a fallback placeholder delivery address
            fallback_addr = Address(
                user_id=current_user.id,
                title="Site Delivery",
                recipient_name=current_user.name,
                recipient_phone=current_user.phone or "+91 9999999999",
                street_address="Construction Project Site",
                city="Bangalore",
                state="Karnataka",
                postal_code="560001",
                is_default=True
            )
            db.add(fallback_addr)
            db.flush()
            address_id = fallback_addr.id

    # 3. Validate stock & calculate totals server-side
    subtotal = Decimal("0.00")
    order_items_data = []

    for ci in cart.items:
        product = db.query(Product).filter(Product.id == ci.product_id).with_for_update().first()
        if not product or not product.is_active:
            raise HTTPException(status_code=400, detail=f"Product {ci.product.name} is no longer available.")

        inventory = product.inventory
        if not inventory or inventory.stock < ci.quantity:
            avail = inventory.stock if inventory else 0
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for '{product.name}'. Requested: {ci.quantity}, Available: {avail}."
            )

        # Deduct stock safely
        inventory.stock -= ci.quantity

        item_total = (product.price * ci.quantity).quantize(Decimal("0.01"))
        subtotal += item_total

        order_items_data.append({
            "product_id": product.id,
            "supplier_id": product.supplier_id,
            "quantity": ci.quantity,
            "unit_price": product.price,
            "total_price": item_total,
            "status": OrderStatus.PENDING
        })

    # Calculations
    tax_amount = (subtotal * Decimal("0.18")).quantize(Decimal("0.01"))
    delivery_fee = Decimal("0.00") if subtotal > Decimal("50000.00") else Decimal("500.00")
    discount_amount = Decimal("0.00")
    net_amount = subtotal + tax_amount + delivery_fee - discount_amount

    # 4. Create Order master record
    new_order = Order(
        order_number=generate_order_number(),
        user_id=current_user.id,
        delivery_address_id=address_id,
        total_amount=subtotal,
        tax_amount=tax_amount,
        delivery_fee=delivery_fee,
        discount_amount=discount_amount,
        net_amount=net_amount,
        status=OrderStatus.CONFIRMED,
        payment_status=PaymentStatus.PENDING if order_in.payment_method == "cod" else PaymentStatus.PAID,
        payment_method=order_in.payment_method,
        notes=order_in.notes
    )
    db.add(new_order)
    db.flush()

    # 5. Create Order Items
    for oid in order_items_data:
        item = OrderItem(order_id=new_order.id, **oid)
        db.add(item)

    # 6. Create Delivery Record
    deliv = Delivery(
        order_id=new_order.id,
        tracking_number=generate_tracking_number(),
        address=f"Delivery to address ID #{address_id}",
        status=DeliveryStatus.ASSIGNED
    )
    db.add(deliv)

    # 7. Create Payment Record
    pay = Payment(
        order_id=new_order.id,
        user_id=current_user.id,
        payment_method=order_in.payment_method,
        transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
        amount=net_amount,
        status=PaymentStatus.PENDING if order_in.payment_method == "cod" else PaymentStatus.PAID
    )
    db.add(pay)

    # 8. Clear Cart
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()

    db.commit()
    db.refresh(new_order)

    return enrich_order_out(new_order)

@router.get("", response_model=List[OrderOut])
def list_orders(
    status_filter: Optional[OrderStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Order).options(
        joinedload(Order.user),
        joinedload(Order.delivery_address),
        joinedload(Order.items).joinedload(OrderItem.product),
        joinedload(Order.items).joinedload(OrderItem.supplier),
        joinedload(Order.deliveries)
    )

    if current_user.role == UserRole.CUSTOMER:
        query = query.filter(Order.user_id == current_user.id)
    elif current_user.role == UserRole.SUPPLIER:
        # Show orders that contain items from this supplier
        supplier = db.query(SupplierProfile).filter(SupplierProfile.user_id == current_user.id).first()
        if supplier:
            query = query.join(Order.items).filter(OrderItem.supplier_id == supplier.id)
    # Admin sees all orders

    if status_filter:
        query = query.filter(Order.status == status_filter)

    orders = query.order_by(Order.ordered_at.desc()).all()
    return [enrich_order_out(o) for o in orders]

@router.get("/{order_id}", response_model=OrderOut)
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).options(
        joinedload(Order.user),
        joinedload(Order.delivery_address),
        joinedload(Order.items).joinedload(OrderItem.product),
        joinedload(Order.items).joinedload(OrderItem.supplier),
        joinedload(Order.deliveries)
    ).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")

    # Permissions check
    if current_user.role == UserRole.CUSTOMER and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this order.")

    return enrich_order_out(order)

@router.put("/{order_id}/status", response_model=OrderOut)
def update_order_status(
    order_id: int,
    status_in: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")

    if current_user.role not in [UserRole.ADMIN, UserRole.SUPPLIER]:
        raise HTTPException(status_code=403, detail="Not authorized to update order status.")

    order.status = status_in.status
    if status_in.notes:
        order.notes = status_in.notes

    # Sync with delivery status if applicable
    if order.deliveries:
        deliv = order.deliveries[0] if isinstance(order.deliveries, list) else order.deliveries
        if status_in.status == OrderStatus.SHIPPED:
            deliv.status = DeliveryStatus.PICKED_UP
        elif status_in.status == OrderStatus.OUT_FOR_DELIVERY:
            deliv.status = DeliveryStatus.OUT_FOR_DELIVERY
        elif status_in.status == OrderStatus.DELIVERED:
            deliv.status = DeliveryStatus.DELIVERED
            deliv.delivered_at = datetime.datetime.now(datetime.timezone.utc)
            order.payment_status = PaymentStatus.PAID

    db.commit()
    db.refresh(order)
    return enrich_order_out(order)
