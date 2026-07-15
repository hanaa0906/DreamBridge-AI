# DreamBridge AI — Engineering Workflow

## Build order (matches backend/app/routers)

1. **Upload** — `POST /api/upload` — store file, create Lesson row
2. **Extract** — `POST /api/lessons/{id}/extract` — OCR/text extraction, store `content_text`
3. **Summarize** — `POST /api/lessons/{id}/summarize` — LLM summary, store `summary`
4. **Quiz** — `POST /api/lessons/{id}/quiz` — generate quiz JSON
5. **Translate** — `POST /api/lessons/{id}/translate` — translate summary/content
6. **Accessibility** — `POST /api/lessons/{id}/personalize` — combine translation +
   simplification + formatting based on a `StudentProfile`
7. **Tutor** — `POST /api/tutor/chat` — RAG chat grounded in lesson chunks
8. **Dashboard** — `GET /api/teacher/lessons`, `GET /api/teacher/students`
9. **Analytics** — `POST /api/progress`, `GET /api/progress/{student_id}`

## Local dev loop

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your LLM API key
uvicorn app.main:app --reload
# Swagger UI: http://localhost:8000/docs
```

Test each endpoint in Swagger before touching the frontend.

## Git discipline

Commit after every module works end-to-end, e.g.:

```
feat: project scaffold + docs
feat: upload endpoint + Lesson model
feat: OCR/text extraction module
feat: LLM summarizer with rule-based fallback
feat: quiz generator
feat: translation module
feat: accessibility adapter + student profiles
feat: AI tutor (RAG chat)
feat: teacher dashboard endpoints
feat: progress analytics
```

## Testing

Each service in `backend/app/services/` has a matching test in `backend/tests/`.
Run with:

```bash
cd backend
pytest -v
```
