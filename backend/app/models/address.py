from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.base import Base
from app.models.enums import AddressType

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(50), default="Home", nullable=False)  # Home, Site, Office
    recipient_name = Column(String(150), nullable=False)
    recipient_phone = Column(String(20), nullable=False)
    street_address = Column(String(255), nullable=False)
    landmark = Column(String(100), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    address_type = Column(SQLEnum(AddressType), default=AddressType.SHIPPING, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="delivery_address")
