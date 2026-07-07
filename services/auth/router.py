from fastapi import (
    APIRouter, Depends,
    HTTPException, status
)
from sqlalchemy.orm import Session
from schemas import (
    UserRegister, UserLogin,
    TokenResponse, UserResponse
)
from models import User, UserTier
from utils.hashing import hash_password, verify_password
from utils.jwt import create_access_token
from database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    payload: UserRegister,
    db: Session = Depends(get_db)
):
    existing = db.query(User).filter(
        User.email == payload.email
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        tier=UserTier.FREE
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    payload: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == payload.email
    ).first()
    if not user or not verify_password(
        payload.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    token = create_access_token({
        "sub": str(user.id),
        "tier": user.tier.value
    })
    return {"access_token": token}

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    db: Session = Depends(get_db)
):
    # Placeholder — expand with JWT middleware later
    pass