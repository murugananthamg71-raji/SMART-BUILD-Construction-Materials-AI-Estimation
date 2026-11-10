from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

class EstimationInput(BaseModel):
    building_length: float = Field(..., gt=0, description="Length in feet")
    building_width: float = Field(..., gt=0, description="Width in feet")
    no_of_floors: int = Field(default=1, ge=1, le=50)
    floor_height: float = Field(default=10.0, ge=8.0, le=25.0)
    construction_type: str = Field(default="Residential") # Residential, Commercial, Industrial
    building_type: str = Field(default="Individual House") # Individual House, Apartment, Office, Warehouse, Shop
    location: str = Field(default="Bangalore")
    quality_preference: str = Field(default="Standard") # Budget, Standard, Premium

class MaterialBreakdownItem(BaseModel):
    material: str
    quantity: float
    unit: str
    unit_price: float
    estimated_cost: float
    specification: str

class EstimationOutput(BaseModel):
    id: Optional[int] = None
    built_up_area_sqft: float
    cement_bags: int
    steel_kg: float
    bricks_count: int
    sand_ton: float
    gravel_ton: float
    tiles_sqft: float
    paint_liter: float
    estimated_total_budget: float
    breakdown: List[MaterialBreakdownItem]
    quality_tier: str
    construction_type: str
    building_type: str
    location: str
    disclaimer: str
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
