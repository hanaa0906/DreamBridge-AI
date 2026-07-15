from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.models import orm  # noqa: F401 - ensures models are registered before create_all
from app.routers import lessons, students, tutor, progress, teacher, users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DreamBridge AI",
    description="Personalized, accessible lessons generated from one teacher upload.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api")
app.include_router(lessons.router, prefix="/api")
app.include_router(students.router, prefix="/api")
app.include_router(tutor.router, prefix="/api")
app.include_router(progress.router, prefix="/api")
app.include_router(teacher.router, prefix="/api")


@app.get("/")
def root():
    return {"status": "ok", "service": "DreamBridge AI backend", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}
