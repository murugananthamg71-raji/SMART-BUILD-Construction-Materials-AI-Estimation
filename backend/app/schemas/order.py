from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from app.models.enums import OrderStatus, PaymentStatus, DeliveryStatus, AddressType

class AddressBase(BaseModel):
    title: str = "Home"
    recipient_name: str = Field(..., min_length=2, max_length=150)
    recipient_phone: str = Field(..., max_length=20)
    street_address: str = Field(..., min_length=5, max_length=255)
    landmark: Optional[str] = None
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    postal_code: str = Field(..., max_length=20)
    address_type: AddressType = AddressType.SHIPPING
    is_default: bool = False

class AddressCreate(AddressBase):
    pass

class AddressOut(AddressBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    unit: Optional[str] = None
    supplier_name: Optional[str] = None
    status: OrderStatus

    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    delivery_address_id: Optional[int] = None
    new_address: Optional[AddressCreate] = None
    payment_method: str = "cod"  # 'razorpay', 'cod', 'stripe'
    notes: Optional[str] = None

class DeliveryOut(BaseModel):
    id: int
    tracking_number: str
    status: DeliveryStatus
    pickup_time: Optional[datetime] = None
    estimated_delivery_time: Optional[datetime] = None
    actual_delivery_time: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class OrderOut(BaseModel):
    id: int
    order_number: str
    user_id: int
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    total_amount: Decimal
    tax_amount: Decimal
    delivery_fee: Decimal
    discount_amount: Decimal
    net_amount: Decimal
    status: OrderStatus
    payment_status: PaymentStatus
    payment_method: str
    notes: Optional[str] = None
    ordered_at: datetime
    delivery_address: Optional[AddressOut] = None
    items: List[OrderItemOut] = []
    delivery: Optional[DeliveryOut] = None

    model_config = ConfigDict(from_attributes=True)

class OrderStatusUpdate(BaseModel):
    status: OrderStatus
    notes: Optional[str] = None
