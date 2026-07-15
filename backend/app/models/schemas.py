from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    role: str


class LessonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    teacher_id: Optional[int]
    title: str
    file_path: str
    content_text: Optional[str] = None
    summary: Optional[str] = None
    created_at: datetime


class StudentProfileIn(BaseModel):
    student_id: int
    language: str = "en"
    learning_style: str = "reading"
    accessibility_type: str = "none"
    difficulty: str = "beginner"


class StudentProfileOut(StudentProfileIn):
    model_config = ConfigDict(from_attributes=True)


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = []
    answer: str
    explanation: Optional[str] = None


class QuizOut(BaseModel):
    lesson_id: int
    questions: List[QuizQuestion]


class TranslateRequest(BaseModel):
    target_language: str
    use_summary: bool = True


class PersonalizeRequest(BaseModel):
    student_id: int


class PersonalizedLessonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    lesson_id: int
    student_id: int
    adapted_text: str
    language: str
    format_notes: str
    created_at: datetime


class TutorChatRequest(BaseModel):
    lesson_id: int
    student_id: int
    message: str


class TutorChatResponse(BaseModel):
    reply: str
    sources_used: List[str] = []


class ProgressIn(BaseModel):
    student_id: int
    lesson_id: int
    score: Optional[float] = None
    time_spent_seconds: int = 0


class ProgressOut(ProgressIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
