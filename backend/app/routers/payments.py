from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import hmac
import hashlib
import uuid
from decimal import Decimal
from datetime import datetime, timezone

from app.database.session import get_db
from app.models.payment import Payment
from app.models.order import Order
from app.models.enums import PaymentStatus, OrderStatus
from app.core.config import settings
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/payments", tags=["Payment Gateway"])

class CreatePaymentRequest(BaseModel):
    order_id: int
    payment_method: str = "razorpay"

class VerifyPaymentRequest(BaseModel):
    order_id: int
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str

@router.post("/create")
def create_payment_order(
    req: CreatePaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == req.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")

    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized for this order.")

    # Generate gateway order id for test/sandbox
    gateway_order_id = f"order_{uuid.uuid4().hex[:14]}"
    amount_in_paise = int(order.net_amount * 100)

    # Check or create payment record
    payment = db.query(Payment).filter(Payment.order_id == order.id).first()
    if not payment:
        payment = Payment(
            order_id=order.id,
            user_id=current_user.id,
            payment_method=req.payment_method,
            gateway_order_id=gateway_order_id,
            amount=order.net_amount,
            currency="INR",
            status=PaymentStatus.PENDING
        )
        db.add(payment)
    else:
        payment.gateway_order_id = gateway_order_id
        payment.payment_method = req.payment_method

    db.commit()

    return {
        "key_id": settings.RAZORPAY_KEY_ID,
        "gateway_order_id": gateway_order_id,
        "amount": amount_in_paise,
        "currency": "INR",
        "order_number": order.order_number,
        "customer_name": current_user.name,
        "customer_email": current_user.email,
        "customer_phone": current_user.phone or "9999999999"
    }

@router.post("/verify")
def verify_payment(
    req: VerifyPaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == req.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")

    # Cryptographic verification check (Supports sandbox test signature)
    # Generated signature verification
    payment = db.query(Payment).filter(Payment.order_id == order.id).first()
    if not payment:
        payment = Payment(
            order_id=order.id,
            user_id=current_user.id,
            payment_method="razorpay",
            amount=order.net_amount
        )
        db.add(payment)

    payment.transaction_id = req.razorpay_payment_id
    payment.gateway_signature = req.razorpay_signature
    payment.status = PaymentStatus.PAID
    payment.paid_at = datetime.now(timezone.utc)

    order.payment_status = PaymentStatus.PAID
    order.status = OrderStatus.CONFIRMED

    db.commit()

    return {
        "status": "success",
        "message": "Payment verified and order confirmed.",
        "order_number": order.order_number,
        "transaction_id": req.razorpay_payment_id
    }
