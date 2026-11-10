from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.base import Base
from app.models.enums import DeliveryStatus

class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    delivery_partner_id = Column(Integer, ForeignKey("delivery_partner_profiles.id", ondelete="SET NULL"), nullable=True, index=True)
    tracking_number = Column(String(100), unique=True, index=True, nullable=False)
    address = Column(String(500), nullable=False)
    status = Column(SQLEnum(DeliveryStatus), default=DeliveryStatus.ASSIGNED, nullable=False, index=True)
    pickup_time = Column(DateTime, nullable=True)
    estimated_delivery_time = Column(DateTime, nullable=True)
    actual_delivery_time = Column(DateTime, nullable=True)
    failure_reason = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    order = relationship("Order", back_populates="deliveries")
    delivery_partner = relationship("DeliveryPartnerProfile", back_populates="deliveries")
