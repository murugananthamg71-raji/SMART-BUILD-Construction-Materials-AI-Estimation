from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal
from typing import List

from app.database.session import get_db
from app.models.user import User
from app.models.profile import SupplierProfile
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.models.inventory import Inventory
from app.models.enums import OrderStatus
from app.core.dependencies import require_supplier

router = APIRouter(prefix="/supplier", tags=["Supplier Portal"])

@router.get("/dashboard")
def get_supplier_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supplier)
):
    supplier = db.query(SupplierProfile).filter(SupplierProfile.user_id == current_user.id).first()
    if not supplier:
        return {
            "total_products": 0,
            "active_products": 0,
            "low_stock_products": 0,
            "total_orders": 0,
            "total_revenue": 0.0,
            "approval_status": "pending",
            "recent_orders": []
        }

    total_products = db.query(func.count(Product.id)).filter(Product.supplier_id == supplier.id).scalar() or 0
    active_products = db.query(func.count(Product.id)).filter(Product.supplier_id == supplier.id, Product.is_active == True).scalar() or 0

    low_stock = db.query(func.count(Inventory.id)).join(Product).filter(
        Product.supplier_id == supplier.id,
        Inventory.stock <= Inventory.low_stock_threshold
    ).scalar() or 0

    # Orders containing this supplier's products
    supplier_items = db.query(OrderItem).filter(OrderItem.supplier_id == supplier.id).all()
    order_ids = list(set([item.order_id for item in supplier_items]))
    total_orders = len(order_ids)

    revenue_sum = db.query(func.sum(OrderItem.total_price)).filter(OrderItem.supplier_id == supplier.id).scalar()
    total_revenue = float(revenue_sum) if revenue_sum else 0.0

    recent_orders = []
    if order_ids:
        orders = db.query(Order).filter(Order.id.in_(order_ids[:5])).order_by(Order.ordered_at.desc()).all()
        recent_orders = [
            {
                "id": o.id,
                "order_number": o.order_number,
                "customer_name": o.user.name if o.user else "Customer",
                "net_amount": float(o.net_amount),
                "status": o.status.value,
                "ordered_at": o.ordered_at
            }
            for o in orders
        ]

    return {
        "company_name": supplier.company_name,
        "approval_status": supplier.approval_status.value,
        "rating": supplier.rating,
        "total_products": total_products,
        "active_products": active_products,
        "low_stock_products": low_stock,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "recent_orders": recent_orders
    }
