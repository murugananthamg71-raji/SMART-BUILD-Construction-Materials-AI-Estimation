from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from decimal import Decimal
from app.database.session import get_db
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.user import User
from app.schemas.cart import CartItemAdd, CartItemUpdate, CartOut, CartItemOut
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["Shopping Cart"])

def get_or_create_cart(user: User, db: Session) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        cart = Cart(user_id=user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

def compute_cart_details(cart: Cart, db: Session) -> CartOut:
    items_out = []
    subtotal = Decimal("0.00")
    total_count = 0

    for item in cart.items:
        prod = item.product
        if not prod or not prod.is_active:
            continue

        stock = prod.inventory.stock if prod.inventory else 0
        img = prod.images[0].image_url if prod.images else None

        line_total = Decimal(str(item.unit_price)) * Decimal(str(item.quantity))
        subtotal += line_total
        total_count += item.quantity

        items_out.append(
            CartItemOut(
                id=item.id,
                product_id=prod.id,
                product_name=prod.name,
                product_brand=prod.brand,
                product_image=img,
                unit=prod.unit,
                unit_price=item.unit_price,
                quantity=item.quantity,
                total_price=line_total,
                available_stock=stock
            )
        )

    # 18% GST on building materials
    tax_amount = (subtotal * Decimal("0.18")).quantize(Decimal("0.01"))
    # Free delivery on bulk orders > Rs. 50,000, else standard logistics charge Rs. 500
    delivery_fee = Decimal("0.00") if subtotal > Decimal("50000.00") or subtotal == Decimal("0.00") else Decimal("500.00")
    grand_total = subtotal + tax_amount + delivery_fee

    return CartOut(
        id=cart.id,
        items=items_out,
        item_count=total_count,
        subtotal=subtotal.quantize(Decimal("0.01")),
        tax_amount=tax_amount,
        delivery_fee=delivery_fee,
        grand_total=grand_total.quantize(Decimal("0.01"))
    )

@router.get("", response_model=CartOut)
def get_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = get_or_create_cart(current_user, db)
    return compute_cart_details(cart, db)

@router.post("/items", response_model=CartOut)
def add_to_cart(
    item_in: CartItemAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == item_in.product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found or unavailable.")

    # Validate stock
    stock = product.inventory.stock if product.inventory else 0
    if stock < item_in.quantity:
        raise HTTPException(status_code=400, detail=f"Insufficient stock available. Only {stock} {product.unit} remaining.")

    cart = get_or_create_cart(current_user, db)

    # Check if item already exists in cart
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product.id
    ).first()

    if cart_item:
        new_quantity = cart_item.quantity + item_in.quantity
        if stock < new_quantity:
            raise HTTPException(status_code=400, detail=f"Cannot add more. Stock limit reached ({stock} available).")
        cart_item.quantity = new_quantity
        cart_item.unit_price = product.price
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=item_in.quantity,
            unit_price=product.price
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart)
    return compute_cart_details(cart, db)

@router.put("/items/{item_id}", response_model=CartOut)
def update_cart_item(
    item_id: int,
    item_in: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = get_or_create_cart(current_user, db)
    cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found.")

    stock = cart_item.product.inventory.stock if cart_item.product and cart_item.product.inventory else 0
    if stock < item_in.quantity:
        raise HTTPException(status_code=400, detail=f"Cannot update quantity. Only {stock} available.")

    cart_item.quantity = item_in.quantity
    cart_item.unit_price = cart_item.product.price
    db.commit()
    db.refresh(cart)
    return compute_cart_details(cart, db)

@router.delete("/items/{item_id}", response_model=CartOut)
def remove_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = get_or_create_cart(current_user, db)
    cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found.")

    db.delete(cart_item)
    db.commit()
    db.refresh(cart)
    return compute_cart_details(cart, db)

@router.delete("", response_model=CartOut)
def clear_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = get_or_create_cart(current_user, db)
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    db.refresh(cart)
    return compute_cart_details(cart, db)
