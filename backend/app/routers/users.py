from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.core.database import get_db
from app.models import orm, schemas

router = APIRouter(prefix="/users", tags=["users"])


class UserIn(BaseModel):
    name: str
    email: EmailStr
    role: str = "student"  # teacher | student


@router.post("", response_model=schemas.UserOut)
def create_user(payload: UserIn, db: Session = Depends(get_db)):
    existing = db.query(orm.User).filter_by(email=payload.email).first()
    if existing:
        raise HTTPException(400, "A user with this email already exists")
    user = orm.User(**payload.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(orm.User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    return user
