from sqlalchemy import Column, Integer, String, Text, Float, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.base import Base

class AIEstimation(Base):
    __tablename__ = "ai_estimations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Inputs
    building_length = Column(Float, nullable=False)  # in feet
    building_width = Column(Float, nullable=False)   # in feet
    no_of_floors = Column(Integer, default=1, nullable=False)
    floor_height = Column(Float, default=10.0, nullable=False)  # in feet
    construction_type = Column(String(50), nullable=False)  # Residential, Commercial, Industrial
    building_type = Column(String(50), nullable=False)      # Individual House, Apartment, Office, etc.
    location = Column(String(100), nullable=False)
    quality_preference = Column(String(50), default="Standard", nullable=False)  # Budget, Standard, Premium
    
    # Computed Outputs
    built_up_area_sqft = Column(Float, nullable=False)
    estimated_cement_bags = Column(Integer, nullable=False)
    estimated_steel_kg = Column(Float, nullable=False)
    estimated_bricks_count = Column(Integer, nullable=False)
    estimated_sand_ton = Column(Float, nullable=False)
    estimated_gravel_ton = Column(Float, nullable=False)
    estimated_tiles_sqft = Column(Float, nullable=False)
    estimated_paint_liter = Column(Float, nullable=False)
    estimated_total_budget = Column(Numeric(14, 2), nullable=False)
    detailed_breakdown_json = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="ai_estimations")

class AIPrediction(Base):
    __tablename__ = "ai_predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=True, index=True)
    prediction_type = Column(String(50), nullable=False)  # price_trend, demand_forecast, stock_depletion
    predicted_value = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
