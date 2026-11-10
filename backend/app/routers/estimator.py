from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json
from typing import List, Optional
from decimal import Decimal

from app.database.session import get_db
from app.ai.estimator import calculate_material_estimates
from app.models.estimator import AIEstimation
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.estimator import EstimationInput, EstimationOutput
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token

router = APIRouter(prefix="/estimator", tags=["AI Material Estimator"])

oauth2_optional = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

def get_optional_user(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(oauth2_optional)
) -> Optional[User]:
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    return db.query(User).filter(User.id == int(user_id)).first()

@router.post("/calculate", response_model=EstimationOutput)
def calculate_estimate(
    calc_in: EstimationInput,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    result = calculate_material_estimates(
        length=calc_in.building_length,
        width=calc_in.building_width,
        floors=calc_in.no_of_floors,
        floor_height=calc_in.floor_height,
        construction_type=calc_in.construction_type,
        building_type=calc_in.building_type,
        location=calc_in.location,
        quality=calc_in.quality_preference
    )

    # Persist in database
    estimation_rec = AIEstimation(
        user_id=current_user.id if current_user else None,
        building_length=calc_in.building_length,
        building_width=calc_in.building_width,
        no_of_floors=calc_in.no_of_floors,
        floor_height=calc_in.floor_height,
        construction_type=calc_in.construction_type,
        building_type=calc_in.building_type,
        location=calc_in.location,
        quality_preference=calc_in.quality_preference,
        built_up_area_sqft=result["built_up_area_sqft"],
        estimated_cement_bags=result["cement_bags"],
        estimated_steel_kg=result["steel_kg"],
        estimated_bricks_count=result["bricks_count"],
        estimated_sand_ton=result["sand_ton"],
        estimated_gravel_ton=result["gravel_ton"],
        estimated_tiles_sqft=result["tiles_sqft"],
        estimated_paint_liter=result["paint_liter"],
        estimated_total_budget=Decimal(str(result["estimated_total_budget"])),
        detailed_breakdown_json=json.dumps(result["breakdown"])
    )
    db.add(estimation_rec)
    db.commit()
    db.refresh(estimation_rec)

    result["id"] = estimation_rec.id
    result["created_at"] = estimation_rec.created_at
    return result

@router.get("/history", response_model=List[EstimationOutput])
def get_user_estimation_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_optional_user)
):
    if not current_user:
        return []

    records = db.query(AIEstimation).filter(
        AIEstimation.user_id == current_user.id
    ).order_by(AIEstimation.created_at.desc()).limit(20).all()

    output = []
    for r in records:
        breakdown_items = json.loads(r.detailed_breakdown_json) if r.detailed_breakdown_json else []
        output.append({
            "id": r.id,
            "built_up_area_sqft": r.built_up_area_sqft,
            "cement_bags": r.estimated_cement_bags,
            "steel_kg": r.estimated_steel_kg,
            "bricks_count": r.estimated_bricks_count,
            "sand_ton": r.estimated_sand_ton,
            "gravel_ton": r.estimated_gravel_ton,
            "tiles_sqft": r.estimated_tiles_sqft,
            "paint_liter": r.estimated_paint_liter,
            "estimated_total_budget": float(r.estimated_total_budget),
            "breakdown": breakdown_items,
            "quality_tier": r.quality_preference,
            "construction_type": r.construction_type,
            "building_type": r.building_type,
            "location": r.location,
            "disclaimer": "Preliminary rule-based civil engineering estimates.",
            "created_at": r.created_at
        })
    return output

@router.get("/{estimation_id}", response_model=EstimationOutput)
def get_single_estimate(
    estimation_id: int,
    db: Session = Depends(get_db)
):
    r = db.query(AIEstimation).filter(AIEstimation.id == estimation_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Estimation not found.")

    breakdown_items = json.loads(r.detailed_breakdown_json) if r.detailed_breakdown_json else []
    return {
        "id": r.id,
        "built_up_area_sqft": r.built_up_area_sqft,
        "cement_bags": r.estimated_cement_bags,
        "steel_kg": r.estimated_steel_kg,
        "bricks_count": r.estimated_bricks_count,
        "sand_ton": r.estimated_sand_ton,
        "gravel_ton": r.estimated_gravel_ton,
        "tiles_sqft": r.estimated_tiles_sqft,
        "paint_liter": r.estimated_paint_liter,
        "estimated_total_budget": float(r.estimated_total_budget),
        "breakdown": breakdown_items,
        "quality_tier": r.quality_preference,
        "construction_type": r.construction_type,
        "building_type": r.building_type,
        "location": r.location,
        "disclaimer": "Preliminary rule-based civil engineering estimates.",
        "created_at": r.created_at
    }
