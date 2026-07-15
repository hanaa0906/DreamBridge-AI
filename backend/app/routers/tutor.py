from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import orm, schemas
from app.services import tutor_service

router = APIRouter(prefix="/tutor", tags=["tutor"])


@router.post("/chat", response_model=schemas.TutorChatResponse)
def chat(req: schemas.TutorChatRequest, db: Session = Depends(get_db)):
    lesson = db.query(orm.Lesson).filter(orm.Lesson.id == req.lesson_id).first()
    if not lesson or not lesson.content_text:
        raise HTTPException(400, "Lesson not found or not yet extracted. Run /extract first.")

    db.add(orm.ChatMessage(lesson_id=req.lesson_id, student_id=req.student_id, role="user", content=req.message))

    reply = tutor_service.answer(req.lesson_id, lesson.content_text, req.message)

    db.add(orm.ChatMessage(lesson_id=req.lesson_id, student_id=req.student_id, role="assistant", content=reply))
    db.commit()

    return schemas.TutorChatResponse(reply=reply, sources_used=[f"lesson:{req.lesson_id}"])
