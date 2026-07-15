from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import orm, schemas

router = APIRouter(prefix="/teacher", tags=["teacher"])


@router.get("/lessons", response_model=list[schemas.LessonOut])
def list_lessons(teacher_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(orm.Lesson)
    if teacher_id is not None:
        q = q.filter(orm.Lesson.teacher_id == teacher_id)
    return q.order_by(orm.Lesson.created_at.desc()).all()


@router.get("/students", response_model=list[schemas.UserOut])
def list_students(db: Session = Depends(get_db)):
    return db.query(orm.User).filter(orm.User.role == "student").all()
