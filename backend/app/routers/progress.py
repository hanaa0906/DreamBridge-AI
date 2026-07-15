from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import orm, schemas

router = APIRouter(prefix="/progress", tags=["progress"])


@router.post("", response_model=schemas.ProgressOut)
def log_progress(payload: schemas.ProgressIn, db: Session = Depends(get_db)):
    record = orm.Progress(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/{student_id}", response_model=list[schemas.ProgressOut])
def get_progress(student_id: int, db: Session = Depends(get_db)):
    return db.query(orm.Progress).filter_by(student_id=student_id).order_by(orm.Progress.created_at.desc()).all()
