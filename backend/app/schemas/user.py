from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.enums import UserRole, ApprovalStatus

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)

class UserRegister(UserBase):
    password: str = Field(..., min_length=6, max_length=100)
    role: UserRole = UserRole.CUSTOMER
    
    # Optional Supplier Information during registration
    company_name: Optional[str] = None
    business_license: Optional[str] = None
    tax_id: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6, max_length=100)

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    company_name: Optional[str] = None
    avatar_url: Optional[str] = None
    preferences: Optional[str] = None

class SupplierProfileOut(BaseModel):
    id: int
    company_name: str
    city: str
    state: str
    postal_code: str
    address: str
    approval_status: ApprovalStatus
    rating: float
    total_reviews: int

    model_config = ConfigDict(from_attributes=True)

class CustomerProfileOut(BaseModel):
    id: int
    company_name: Optional[str] = None
    gst_number: Optional[str] = None
    avatar_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserOut(UserBase):
    id: int
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    customer_profile: Optional[CustomerProfileOut] = None
    supplier_profile: Optional[SupplierProfileOut] = None

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
