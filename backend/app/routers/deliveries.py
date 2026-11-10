from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel

from app.database.session import get_db
from app.models.delivery import Delivery
from app.models.order import Order
from app.models.profile import DeliveryPartnerProfile
from app.models.user import User
from app.models.enums import DeliveryStatus, OrderStatus, UserRole
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/deliveries", tags=["Delivery Logistics"])

class DeliveryStatusUpdate(BaseModel):
    status: DeliveryStatus
    notes: Optional[str] = None
    failure_reason: Optional[str] = None

@router.get("/assigned")
def get_assigned_deliveries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # If delivery partner, get their profile
    profile = db.query(DeliveryPartnerProfile).filter(DeliveryPartnerProfile.user_id == current_user.id).first()
    
    q = db.query(Delivery)
    if profile:
        q = q.filter((Delivery.delivery_partner_id == profile.id) | (Delivery.delivery_partner_id == None))
    elif current_user.role != UserRole.ADMIN:
        return []

    deliveries = q.order_by(Delivery.created_at.desc()).all()
    results = []
    for d in deliveries:
        order = d.order
        results.append({
            "id": d.id,
            "order_id": d.order_id,
            "order_number": order.order_number if order else "N/A",
            "customer_name": order.user.name if order and order.user else "N/A",
            "customer_phone": order.user.phone if order and order.user else "N/A",
            "address": order.delivery_address.street_address if order and order.delivery_address else d.address,
            "city": order.delivery_address.city if order and order.delivery_address else "",
            "postal_code": order.delivery_address.postal_code if order and order.delivery_address else "",
            "tracking_number": d.tracking_number,
            "status": d.status.value,
            "notes": d.notes,
            "created_at": d.created_at
        })
    return results

@router.put("/{delivery_id}/status")
def update_delivery_status(
    delivery_id: int,
    status_in: DeliveryStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery record not found.")

    delivery.status = status_in.status
    if status_in.notes:
        delivery.notes = status_in.notes
    if status_in.failure_reason:
        delivery.failure_reason = status_in.failure_reason

    now = datetime.now(timezone.utc)
    if status_in.status == DeliveryStatus.PICKED_UP:
        delivery.pickup_time = now
        if delivery.order:
            delivery.order.status = OrderStatus.SHIPPED
    elif status_in.status == DeliveryStatus.OUT_FOR_DELIVERY:
        if delivery.order:
            delivery.order.status = OrderStatus.OUT_FOR_DELIVERY
    elif status_in.status == DeliveryStatus.DELIVERED:
        delivery.actual_delivery_time = now
        delivery.delivered_at = now
        if delivery.order:
            delivery.order.status = OrderStatus.DELIVERED
    elif status_in.status == DeliveryStatus.FAILED:
        if delivery.order:
            delivery.order.status = OrderStatus.FAILED

    db.commit()
    db.refresh(delivery)
    return {
        "message": f"Delivery updated to {status_in.status.value}",
        "tracking_number": delivery.tracking_number,
        "status": delivery.status.value
    }
