from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.models.enums import ApprovalStatus

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=120)
    description: Optional[str] = None
    image_url: Optional[str] = None
    display_order: int = 0
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int
    product_count: Optional[int] = 0
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductImageOut(BaseModel):
    id: int
    image_url: str
    is_primary: bool

    model_config = ConfigDict(from_attributes=True)

class InventoryOut(BaseModel):
    stock: int
    low_stock_threshold: int

    model_config = ConfigDict(from_attributes=True)

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = None
    brand: Optional[str] = None
    price: Decimal = Field(..., ge=0)
    unit: str = Field(..., max_length=50) # 'bag', 'ton', 'sqft', 'piece', 'kg', 'liter'
    min_order_quantity: int = Field(default=1, ge=1)
    category_id: int

class ProductCreate(ProductBase):
    initial_stock: int = Field(default=100, ge=0)
    image_url: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[Decimal] = None
    unit: Optional[str] = None
    min_order_quantity: Optional[int] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None

class StockUpdate(BaseModel):
    stock: int = Field(..., ge=0)
    low_stock_threshold: Optional[int] = None

class ProductOut(ProductBase):
    id: int
    supplier_id: int
    slug: str
    is_approved: bool
    approval_status: ApprovalStatus
    is_active: bool
    rating: float
    total_reviews: int
    created_at: datetime
    images: List[ProductImageOut] = []
    inventory: Optional[InventoryOut] = None
    category: Optional[CategoryBase] = None
    supplier_name: Optional[str] = None
    supplier_city: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ProductListResponse(BaseModel):
    items: List[ProductOut]
    total: int
    page: int
    limit: int
    total_pages: int
