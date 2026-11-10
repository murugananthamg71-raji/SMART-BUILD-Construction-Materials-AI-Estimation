from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)

class CartItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_brand: Optional[str] = None
    product_image: Optional[str] = None
    unit: str
    unit_price: Decimal
    quantity: int
    total_price: Decimal
    available_stock: int

    model_config = ConfigDict(from_attributes=True)

class CartOut(BaseModel):
    id: int
    items: List[CartItemOut] = []
    item_count: int = 0
    subtotal: Decimal = Decimal("0.00")
    tax_amount: Decimal = Decimal("0.00")
    delivery_fee: Decimal = Decimal("0.00")
    grand_total: Decimal = Decimal("0.00")
