from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.profile import CustomerProfile, SupplierProfile, DeliveryPartnerProfile
from app.models.cart import Cart
from app.models.wishlist import Wishlist
from app.models.enums import UserRole, ApprovalStatus
from app.schemas.user import UserRegister, UserLogin, UserOut, TokenResponse, ProfileUpdate, PasswordChange

router = APIRouter(prefix="/auth", tags=["Authentication & Profiles"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    # Check if user already exists
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )

    # Disallow self-registration as admin
    role = user_in.role
    if role == UserRole.ADMIN:
        role = UserRole.CUSTOMER

    # Create base user
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        phone=user_in.phone,
        role=role,
        is_active=True,
        is_verified=True if role == UserRole.CUSTOMER else False
    )
    db.add(new_user)
    db.flush()

    # Create role-specific profiles & entities
    if role == UserRole.CUSTOMER:
        profile = CustomerProfile(user_id=new_user.id, company_name=user_in.company_name)
        cart = Cart(user_id=new_user.id)
        wishlist = Wishlist(user_id=new_user.id)
        db.add_all([profile, cart, wishlist])
    elif role == UserRole.SUPPLIER:
        supplier_profile = SupplierProfile(
            user_id=new_user.id,
            company_name=user_in.company_name or f"{user_in.name}'s Materials",
            business_license=user_in.business_license,
            tax_id=user_in.tax_id,
            address=user_in.address or "Address not specified",
            city=user_in.city or "Bangalore",
            state=user_in.state or "Karnataka",
            postal_code=user_in.postal_code or "560001",
            approval_status=ApprovalStatus.PENDING
        )
        db.add(supplier_profile)
    elif role == UserRole.DELIVERY_PARTNER:
        delivery_profile = DeliveryPartnerProfile(
            user_id=new_user.id,
            vehicle_type="Truck",
            vehicle_number="KA-01-XX-0000",
            license_number="DL-PENDING-VERIFICATION",
            is_available=True
        )
        db.add(delivery_profile)

    db.commit()
    db.refresh(new_user)

    token = create_access_token(subject=new_user.id, role=new_user.role.value)
    return TokenResponse(access_token=token, token_type="bearer", user=new_user)

@router.post("/login", response_model=TokenResponse)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_in.email).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Please contact support."
        )

    token = create_access_token(subject=user.id, role=user.role.value)
    return TokenResponse(access_token=token, token_type="bearer", user=user)

@router.get("/me", response_model=UserOut)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/profile", response_model=UserOut)
def update_profile(
    profile_in: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if profile_in.name:
        current_user.name = profile_in.name
    if profile_in.phone:
        current_user.phone = profile_in.phone

    if current_user.role == UserRole.CUSTOMER and current_user.customer_profile:
        if profile_in.company_name:
            current_user.customer_profile.company_name = profile_in.company_name
        if profile_in.avatar_url:
            current_user.customer_profile.avatar_url = profile_in.avatar_url
        if profile_in.preferences:
            current_user.customer_profile.preferences = profile_in.preferences
    elif current_user.role == UserRole.SUPPLIER and current_user.supplier_profile:
        if profile_in.company_name:
            current_user.supplier_profile.company_name = profile_in.company_name

    db.commit()
    db.refresh(current_user)
    return current_user

@router.put("/password")
def change_password(
    pwd_in: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(pwd_in.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password does not match"
        )
    current_user.hashed_password = get_password_hash(pwd_in.new_password)
    db.commit()
    return {"message": "Password updated successfully"}
