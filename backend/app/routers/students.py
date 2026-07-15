from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import orm, schemas

router = APIRouter(prefix="/students", tags=["students"])


@router.post("", response_model=schemas.StudentProfileOut)
def upsert_student_profile(payload: schemas.StudentProfileIn, db: Session = Depends(get_db)):
    profile = db.query(orm.StudentProfile).filter_by(student_id=payload.student_id).first()
    if profile:
        for field, value in payload.model_dump().items():
            setattr(profile, field, value)
    else:
        profile = orm.StudentProfile(**payload.model_dump())
        db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/{student_id}", response_model=schemas.StudentProfileOut)
def get_student_profile(student_id: int, db: Session = Depends(get_db)):
    profile = db.query(orm.StudentProfile).filter_by(student_id=student_id).first()
    if not profile:
        raise HTTPException(404, "Student profile not found")
    return profile
