from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database.session import get_db
from app.models.category import Category
from app.models.product import Product
from app.schemas.product import CategoryCreate, CategoryOut
from app.core.dependencies import require_admin

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).filter(Category.is_active == True).order_by(Category.display_order.asc(), Category.name.asc()).all()
    results = []
    for cat in categories:
        count = db.query(func.count(Product.id)).filter(Product.category_id == cat.id, Product.is_active == True).scalar()
        out = CategoryOut.model_validate(cat)
        out.product_count = count
        results.append(out)
    return results

@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    cat_in: CategoryCreate,
    db: Session = Depends(get_db),
    admin_user = Depends(require_admin)
):
    existing = db.query(Category).filter((Category.name == cat_in.name) | (Category.slug == cat_in.slug)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category with this name or slug already exists.")

    new_cat = Category(**cat_in.model_dump())
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    out = CategoryOut.model_validate(new_cat)
    out.product_count = 0
    return out

@router.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    cat_in: CategoryCreate,
    db: Session = Depends(get_db),
    admin_user = Depends(require_admin)
):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found.")

    for field, value in cat_in.model_dump(exclude_unset=True).items():
        setattr(cat, field, value)

    db.commit()
    db.refresh(cat)
    return CategoryOut.model_validate(cat)

@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin_user = Depends(require_admin)
):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found.")

    cat.is_active = False
    db.commit()
    return {"message": "Category deactivated successfully."}
