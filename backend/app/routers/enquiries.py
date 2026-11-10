from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import datetime

from app.database.session import get_db
from app.models.enquiry import Enquiry
from app.schemas.enquiry import EnquiryCreate, EnquiryOut

router = APIRouter(prefix="/enquiries", tags=["Enquiries & Order Booking"])

@router.post("", response_model=EnquiryOut, status_code=status.HTTP_201_CREATED)
def create_enquiry(payload: EnquiryCreate, db: Session = Depends(get_db)):
    # Generate unique enquiry / booking reference number
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    random_suffix = uuid.uuid4().hex[:6].upper()
    enquiry_no = f"ENQ-{date_str}-{random_suffix}"

    enquiry = Enquiry(
        enquiry_number=enquiry_no,
        customer_name=payload.customer_name.strip(),
        customer_phone=payload.customer_phone.strip(),
        customer_email=payload.customer_email.strip() if payload.customer_email else None,
        delivery_city=payload.delivery_city.strip(),
        site_address=payload.site_address.strip() if payload.site_address else None,
        material_category=payload.material_category.strip(),
        quantity_description=payload.quantity_description.strip() if payload.quantity_description else None,
        urgency=payload.urgency or "immediate",
        status="pending",
        notes=payload.notes.strip() if payload.notes else None
    )
    db.add(enquiry)
    db.commit()
    db.refresh(enquiry)
    return enquiry

@router.get("", response_model=List[EnquiryOut])
def list_enquiries(
    status: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Enquiry)
    if status:
        query = query.filter(Enquiry.status == status)
    return query.order_by(Enquiry.id.desc()).limit(limit).all()

@router.get("/{enquiry_id}", response_model=EnquiryOut)
def get_enquiry(enquiry_id: int, db: Session = Depends(get_db)):
    enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    return enquiry
