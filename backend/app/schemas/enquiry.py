from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class EnquiryCreate(BaseModel):
    customer_name: str
    customer_phone: str
    customer_email: Optional[str] = None
    delivery_city: str
    site_address: Optional[str] = None
    material_category: str
    quantity_description: Optional[str] = None
    urgency: Optional[str] = "immediate"
    notes: Optional[str] = None

class EnquiryOut(BaseModel):
    id: int
    enquiry_number: str
    customer_name: str
    customer_phone: str
    customer_email: Optional[str] = None
    delivery_city: str
    site_address: Optional[str] = None
    material_category: str
    quantity_description: Optional[str] = None
    urgency: str
    status: str
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
