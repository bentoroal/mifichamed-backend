from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user_profile import (
    UserProfileCreate,
    UserProfileOut,
    UserProfileUpdate,
)
from app.services.user_profile_service import (
    get_profile,
    create_profile,
    update_profile,
    delete_profile,
)
from app.db.session import get_db

router = APIRouter(prefix="/user-profile", tags=["UserProfile"])


@router.get("/", response_model=UserProfileOut)
def read_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = get_profile(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.post("/", response_model=UserProfileOut)
def create_profile_route(
    item: UserProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing = get_profile(db, current_user.id)
    if existing:
        raise HTTPException(status_code=409, detail="Profile already exists")
    return create_profile(
        db,
        current_user.id,
        item.full_name,
        item.birth_date,
        item.sex,
    )


@router.patch("/", response_model=UserProfileOut)
def update_profile_route(
    item: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = update_profile(db, current_user.id, item.model_dump(exclude_unset=True))
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.delete("/", response_model=UserProfileOut)
def delete_profile_route(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = delete_profile(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
