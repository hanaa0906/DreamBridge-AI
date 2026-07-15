import os
import uuid
import json

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models import orm, schemas
from app.services import (
    extraction_service,
    summarizer_service,
    quiz_service,
    translation_service,
    accessibility_service,
)

router = APIRouter(tags=["lessons"])


@router.post("/upload", response_model=schemas.LessonOut)
def upload_lesson(
    title: str = Form(...),
    teacher_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Module 1: Lesson Upload."""
    ext = os.path.splitext(file.filename)[1]
    stored_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(settings.upload_dir, stored_name)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    lesson = orm.Lesson(teacher_id=teacher_id, title=title, file_path=file_path)
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.post("/lessons/{lesson_id}/extract", response_model=schemas.LessonOut)
def extract_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """Module 2: Content Extraction."""
    lesson = _get_lesson_or_404(db, lesson_id)
    text = extraction_service.extract_text(lesson.file_path)
    lesson.content_text = text
    db.commit()
    db.refresh(lesson)
    return lesson


@router.post("/lessons/{lesson_id}/summarize", response_model=schemas.LessonOut)
def summarize_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """Module 3: Summarizer."""
    lesson = _get_lesson_or_404(db, lesson_id)
    if not lesson.content_text:
        raise HTTPException(400, "Run /extract before /summarize")
    lesson.summary = summarizer_service.summarize(lesson.content_text)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.post("/lessons/{lesson_id}/quiz", response_model=schemas.QuizOut)
def quiz_lesson(lesson_id: int, num_questions: int = 5, db: Session = Depends(get_db)):
    """Module 4: Quiz Generator."""
    lesson = _get_lesson_or_404(db, lesson_id)
    source_text = lesson.content_text or lesson.summary
    if not source_text:
        raise HTTPException(400, "Run /extract before /quiz")

    questions = quiz_service.generate_quiz(source_text, num_questions)
    quiz = orm.Quiz(lesson_id=lesson_id, questions_json=json.dumps(questions))
    db.add(quiz)
    db.commit()
    return schemas.QuizOut(lesson_id=lesson_id, questions=questions)


@router.post("/lessons/{lesson_id}/translate")
def translate_lesson(lesson_id: int, req: schemas.TranslateRequest, db: Session = Depends(get_db)):
    """Module 5: Translator."""
    lesson = _get_lesson_or_404(db, lesson_id)
    source_text = lesson.summary if req.use_summary and lesson.summary else lesson.content_text
    if not source_text:
        raise HTTPException(400, "Run /extract (and optionally /summarize) before /translate")

    translated = translation_service.translate(source_text, req.target_language)
    return {"lesson_id": lesson_id, "language": req.target_language, "translated_text": translated}


@router.post("/lessons/{lesson_id}/personalize", response_model=schemas.PersonalizedLessonOut)
def personalize_lesson(lesson_id: int, req: schemas.PersonalizeRequest, db: Session = Depends(get_db)):
    """Module 6: Accessibility Adapter — the core value proposition."""
    lesson = _get_lesson_or_404(db, lesson_id)
    if not lesson.content_text:
        raise HTTPException(400, "Run /extract before /personalize")

    profile = db.query(orm.StudentProfile).filter_by(student_id=req.student_id).first()
    if not profile:
        raise HTTPException(404, "Student profile not found. Create one via POST /api/students first.")

    adapted_text = accessibility_service.personalize(lesson.content_text, profile)
    format_notes = accessibility_service.format_notes_for(profile)

    record = orm.PersonalizedLesson(
        lesson_id=lesson_id,
        student_id=req.student_id,
        adapted_text=adapted_text,
        language=profile.language,
        format_notes=format_notes,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/lessons/{lesson_id}", response_model=schemas.LessonOut)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    return _get_lesson_or_404(db, lesson_id)


def _get_lesson_or_404(db: Session, lesson_id: int) -> orm.Lesson:
    lesson = db.query(orm.Lesson).filter(orm.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    return lesson
