from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.database.base import Base

class Enquiry(Base):
    __tablename__ = "enquiries"

    id = Column(Integer, primary_key=True, index=True)
    enquiry_number = Column(String(50), unique=True, index=True, nullable=False)
    customer_name = Column(String(150), nullable=False)
    customer_phone = Column(String(30), nullable=False, index=True)
    customer_email = Column(String(150), nullable=True)
    delivery_city = Column(String(100), nullable=False)
    site_address = Column(String(255), nullable=True)
    material_category = Column(String(100), nullable=False)
    quantity_description = Column(String(255), nullable=True)
    urgency = Column(String(50), default="immediate")
    status = Column(String(50), default="pending", index=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
