from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.base import Base
from app.models.enums import OrderStatus, PaymentStatus

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    delivery_address_id = Column(Integer, ForeignKey("addresses.id", ondelete="RESTRICT"), nullable=True)
    
    total_amount = Column(Numeric(12, 2), nullable=False)
    tax_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    delivery_fee = Column(Numeric(10, 2), default=0.00, nullable=False)
    discount_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    net_amount = Column(Numeric(12, 2), nullable=False)
    
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False, index=True)
    payment_status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False, index=True)
    payment_method = Column(String(50), default="cod", nullable=False)  # 'razorpay', 'cod', 'stripe'
    notes = Column(Text, nullable=True)
    
    ordered_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    user = relationship("User", back_populates="orders", foreign_keys=[user_id])
    delivery_address = relationship("Address", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")
    deliveries = relationship("Delivery", back_populates="order", cascade="all, delete-orphan")
    complaints = relationship("Complaint", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="RESTRICT"), nullable=False, index=True)
    supplier_id = Column(Integer, ForeignKey("supplier_profiles.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    supplier = relationship("SupplierProfile")
