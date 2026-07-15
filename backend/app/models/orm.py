from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(String, nullable=False, default="student")  # teacher | student

    lessons = relationship("Lesson", back_populates="teacher")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    content_text = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    teacher = relationship("User", back_populates="lessons")


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    student_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    language = Column(String, default="en")
    learning_style = Column(String, default="reading")
    accessibility_type = Column(String, default="none")
    difficulty = Column(String, default="beginner")


class PersonalizedLesson(Base):
    __tablename__ = "personalized_lessons"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    adapted_text = Column(Text)
    language = Column(String)
    format_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    questions_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    score = Column(Float, nullable=True)
    time_spent_seconds = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String)  # user | assistant
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
