from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, desc, asc
import math
import re
from typing import Optional, List
from decimal import Decimal

from app.database.session import get_db
from app.models.product import Product, ProductImage, PriceHistory
from app.models.inventory import Inventory
from app.models.category import Category
from app.models.profile import SupplierProfile
from app.models.user import User
from app.models.enums import UserRole, ApprovalStatus
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductOut, ProductListResponse, StockUpdate
)
from app.core.dependencies import get_current_user, require_supplier, require_admin

router = APIRouter(prefix="/products", tags=["Products & Catalog"])

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text

def enrich_product_out(p: Product) -> ProductOut:
    out = ProductOut.model_validate(p)
    if p.supplier:
        out.supplier_name = p.supplier.company_name
        out.supplier_city = p.supplier.city
    return out

@router.get("", response_model=ProductListResponse)
def list_products(
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    supplier_id: Optional[int] = None,
    brand: Optional[str] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    in_stock: Optional[bool] = None,
    sort_by: Optional[str] = "latest",  # latest, price_asc, price_desc, rating
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db)
):
    query = db.query(Product).options(
        joinedload(Product.supplier),
        joinedload(Product.category),
        joinedload(Product.images),
        joinedload(Product.inventory)
    ).filter(Product.is_active == True)

    # By default in marketplace, show approved products
    query = query.filter(Product.is_approved == True)

    if search:
        search_filter = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_filter),
                Product.brand.ilike(search_filter),
                Product.description.ilike(search_filter)
            )
        )

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if supplier_id:
        query = query.filter(Product.supplier_id == supplier_id)

    if brand:
        query = query.filter(Product.brand.ilike(f"%{brand}%"))

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if in_stock is True:
        query = query.join(Product.inventory).filter(Inventory.stock > 0)

    # Sorting
    if sort_by == "price_asc":
        query = query.order_by(asc(Product.price))
    elif sort_by == "price_desc":
        query = query.order_by(desc(Product.price))
    elif sort_by == "rating":
        query = query.order_by(desc(Product.rating))
    else:
        query = query.order_by(desc(Product.created_at))

    total = query.count()
    offset = (page - 1) * limit
    products = query.offset(offset).limit(limit).all()

    items = [enrich_product_out(p) for p in products]
    total_pages = math.ceil(total / limit) if total > 0 else 1

    return ProductListResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages
    )

@router.get("/{product_id}", response_model=ProductOut)
def get_product_details(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).options(
        joinedload(Product.supplier),
        joinedload(Product.category),
        joinedload(Product.images),
        joinedload(Product.inventory)
    ).filter(Product.id == product_id, Product.is_active == True).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    return enrich_product_out(product)

@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    prod_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supplier)
):
    supplier = db.query(SupplierProfile).filter(SupplierProfile.user_id == current_user.id).first()
    if not supplier and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=400, detail="Supplier profile required to add products.")

    supplier_id = supplier.id if supplier else 1

    # Check category
    category = db.query(Category).filter(Category.id == prod_in.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category ID.")

    slug = f"{slugify(prod_in.name)}-{int(prod_in.price)}"

    # Auto-approve for demo convenience or default to approved if supplier is approved
    is_approved = True if (supplier and supplier.approval_status == ApprovalStatus.APPROVED) or current_user.role == UserRole.ADMIN else True

    new_prod = Product(
        supplier_id=supplier_id,
        category_id=prod_in.category_id,
        name=prod_in.name,
        slug=slug,
        description=prod_in.description,
        brand=prod_in.brand,
        price=prod_in.price,
        unit=prod_in.unit,
        min_order_quantity=prod_in.min_order_quantity,
        is_approved=is_approved,
        approval_status=ApprovalStatus.APPROVED if is_approved else ApprovalStatus.PENDING,
        is_active=True
    )
    db.add(new_prod)
    db.flush()

    # Create inventory
    inv = Inventory(
        product_id=new_prod.id,
        stock=prod_in.initial_stock,
        low_stock_threshold=10
    )
    db.add(inv)

    # Add image if provided
    if prod_in.image_url:
        img = ProductImage(
            product_id=new_prod.id,
            image_url=prod_in.image_url,
            is_primary=True,
            display_order=1
        )
        db.add(img)

    db.commit()
    db.refresh(new_prod)
    return enrich_product_out(new_prod)

@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    prod_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supplier)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    # Only owner supplier or admin can edit
    if current_user.role != UserRole.ADMIN and product.supplier.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this product.")

    # Price history tracking
    if prod_in.price is not None and prod_in.price != product.price:
        history = PriceHistory(
            product_id=product.id,
            old_price=product.price,
            new_price=prod_in.price,
            changed_by_user_id=current_user.id,
            change_reason="Supplier updated price"
        )
        db.add(history)

    for field, val in prod_in.model_dump(exclude_unset=True).items():
        setattr(product, field, val)

    db.commit()
    db.refresh(product)
    return enrich_product_out(product)

@router.put("/{product_id}/stock", response_model=ProductOut)
def update_stock(
    product_id: int,
    stock_in: StockUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supplier)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    if current_user.role != UserRole.ADMIN and product.supplier.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update stock for this product.")

    if not product.inventory:
        product.inventory = Inventory(product_id=product.id, stock=stock_in.stock)
        db.add(product.inventory)
    else:
        product.inventory.stock = stock_in.stock
        if stock_in.low_stock_threshold is not None:
            product.inventory.low_stock_threshold = stock_in.low_stock_threshold

    db.commit()
    db.refresh(product)
    return enrich_product_out(product)

@router.put("/{product_id}/approve")
def approve_product(
    product_id: int,
    status_choice: ApprovalStatus,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    product.approval_status = status_choice
    product.is_approved = (status_choice == ApprovalStatus.APPROVED)
    db.commit()
    return {"message": f"Product approval status updated to {status_choice.value}."}

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supplier)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    if current_user.role != UserRole.ADMIN and product.supplier.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this product.")

    product.is_active = False
    db.commit()
    return {"message": "Product deactivated successfully."}
