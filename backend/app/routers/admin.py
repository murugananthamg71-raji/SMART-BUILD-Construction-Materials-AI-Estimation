from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from decimal import Decimal

from app.database.session import get_db
from app.models.user import User
from app.models.profile import SupplierProfile, CustomerProfile
from app.models.product import Product
from app.models.order import Order
from app.models.inventory import Inventory
from app.models.enums import UserRole, ApprovalStatus, OrderStatus
from app.core.dependencies import require_admin

router = APIRouter(prefix="/admin", tags=["Admin Portal"])

@router.get("/dashboard")
def get_admin_dashboard_metrics(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    total_users = db.query(func.count(User.id)).scalar() or 0
    total_customers = db.query(func.count(User.id)).filter(User.role == UserRole.CUSTOMER).scalar() or 0
    total_suppliers = db.query(func.count(SupplierProfile.id)).scalar() or 0
    total_products = db.query(func.count(Product.id)).filter(Product.is_active == True).scalar() or 0
    total_orders = db.query(func.count(Order.id)).scalar() or 0

    total_revenue_result = db.query(func.sum(Order.net_amount)).filter(Order.status != OrderStatus.CANCELLED).scalar()
    total_revenue = float(total_revenue_result) if total_revenue_result else 0.0

    pending_suppliers = db.query(func.count(SupplierProfile.id)).filter(SupplierProfile.approval_status == ApprovalStatus.PENDING).scalar() or 0
    pending_products = db.query(func.count(Product.id)).filter(Product.approval_status == ApprovalStatus.PENDING).scalar() or 0

    # Low stock count
    low_stock_count = db.query(func.count(Inventory.id)).filter(Inventory.stock <= Inventory.low_stock_threshold).scalar() or 0

    # Order status distribution
    status_counts = db.query(Order.status, func.count(Order.id)).group_by(Order.status).all()
    order_status_distribution = {status.value if hasattr(status, 'value') else str(status): count for status, count in status_counts}

    # Recent orders
    recent_orders = db.query(Order).order_by(Order.ordered_at.desc()).limit(5).all()
    recent_orders_data = [
        {
            "id": o.id,
            "order_number": o.order_number,
            "customer_name": o.user.name if o.user else "Customer",
            "net_amount": float(o.net_amount),
            "status": o.status.value,
            "ordered_at": o.ordered_at
        }
        for o in recent_orders
    ]

    return {
        "total_users": total_users,
        "total_customers": total_customers,
        "total_suppliers": total_suppliers,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "pending_suppliers": pending_suppliers,
        "pending_products": pending_products,
        "low_stock_count": low_stock_count,
        "order_status_distribution": order_status_distribution,
        "recent_orders": recent_orders_data
    }

@router.get("/users")
def list_all_users(
    role: Optional[UserRole] = None,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    q = db.query(User)
    if role:
        q = q.filter(User.role == role)
    users = q.order_by(User.created_at.desc()).all()
    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "phone": u.phone,
            "role": u.role.value,
            "is_active": u.is_active,
            "is_verified": u.is_verified,
            "created_at": u.created_at
        }
        for u in users
    ]

@router.get("/suppliers")
def list_suppliers(
    status_filter: Optional[ApprovalStatus] = None,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    q = db.query(SupplierProfile)
    if status_filter:
        q = q.filter(SupplierProfile.approval_status == status_filter)
    suppliers = q.order_by(SupplierProfile.created_at.desc()).all()
    return [
        {
            "id": s.id,
            "user_id": s.user_id,
            "company_name": s.company_name,
            "contact_person": s.user.name if s.user else "",
            "email": s.user.email if s.user else "",
            "phone": s.user.phone if s.user else "",
            "city": s.city,
            "state": s.state,
            "approval_status": s.approval_status.value,
            "rating": s.rating,
            "created_at": s.created_at
        }
        for s in suppliers
    ]

@router.put("/suppliers/{supplier_id}/approve")
def update_supplier_approval(
    supplier_id: int,
    status_choice: ApprovalStatus,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    supplier = db.query(SupplierProfile).filter(SupplierProfile.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found.")

    supplier.approval_status = status_choice
    if supplier.user:
        supplier.user.is_verified = (status_choice == ApprovalStatus.APPROVED)
    db.commit()
    return {"message": f"Supplier status updated to {status_choice.value}."}
