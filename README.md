# DreamBridge AI

Teachers upload one lesson. DreamBridge AI extracts the content and generates
personalized, accessible versions for each student — adapted for language,
reading level, learning style, and accessibility needs — plus an AI tutor
chat and progress analytics.

```
Teacher Uploads Lesson
        |
        v
AI Extracts Content        (OCR / text extraction)
        |
        v
AI Accessibility Engine     (simplification, formatting, translation)
        |
        v
Student Profile
        |
        v
Personalized Lesson
        |
        v
AI Tutor                     (RAG chat grounded in the lesson)
        |
        v
Progress Analytics
```

See [`docs/Vision.md`](docs/Vision.md) for the full product rationale.

## Project structure

```
DreamBridge-AI/
├── backend/     FastAPI app: upload, extraction, summarization, quiz,
│                translation, accessibility, AI tutor, analytics
├── frontend/    React (Vite) app: teacher upload flow, lesson pipeline UI,
│                dashboard, tutor chat
├── database/    (empty — SQLite db file is generated at runtime in backend/database)
├── docs/        Vision, Features, Workflow, Database schema, API contract
├── models/      Placeholder for any locally-stored model artifacts
└── assets/      Placeholder for demo assets (screenshots, sample lessons, logo)
```

## Quickstart

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # optional: add GEMINI_API_KEY for real LLM output
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs for interactive Swagger API docs.

**Note:** every AI-backed endpoint (summarize, quiz, translate, personalize,
tutor chat) works out of the box with a rule-based fallback even without an
API key, so you can demo the full pipeline immediately. Add a `GEMINI_API_KEY`
to `.env` to get real LLM-generated output instead of the fallback.

OCR (for scanned PDFs/images) requires the Tesseract binary on your system:

```bash
# Debian/Ubuntu
sudo apt-get install tesseract-ocr
# macOS
brew install tesseract
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env             # points at the backend, defaults to localhost:8000
npm run dev
```

Open http://localhost:5173.

### Try the full pipeline via API (no frontend needed)

```bash
# 1. Create a teacher and a student
curl -X POST localhost:8000/api/users -H "Content-Type: application/json" \
  -d '{"name":"Ms. Rao","email":"rao@school.edu","role":"teacher"}'
curl -X POST localhost:8000/api/users -H "Content-Type: application/json" \
  -d '{"name":"Arjun","email":"arjun@school.edu","role":"student"}'

# 2. Give the student an accessibility profile
curl -X POST localhost:8000/api/students -H "Content-Type: application/json" \
  -d '{"student_id":2,"language":"ta","learning_style":"visual","accessibility_type":"dyslexia","difficulty":"beginner"}'

# 3. Upload a lesson
curl -X POST localhost:8000/api/upload -F "title=The Water Cycle" -F "teacher_id=1" -F "file=@lesson.pdf"

# 4. Run the pipeline (assuming the uploaded lesson got id=1)
curl -X POST localhost:8000/api/lessons/1/extract
curl -X POST localhost:8000/api/lessons/1/summarize
curl -X POST "localhost:8000/api/lessons/1/quiz?num_questions=5"
curl -X POST localhost:8000/api/lessons/1/personalize -H "Content-Type: application/json" -d '{"student_id":2}'
curl -X POST localhost:8000/api/tutor/chat -H "Content-Type: application/json" \
  -d '{"lesson_id":1,"student_id":2,"message":"What is condensation?"}'
```

## Testing

```bash
cd backend
pytest -v
```

## Docs

- [`docs/Vision.md`](docs/Vision.md) — problem, solution, success criteria
- [`docs/Features.md`](docs/Features.md) — module-by-module feature status
- [`docs/Workflow.md`](docs/Workflow.md) — build order, git discipline, testing
- [`docs/Database.md`](docs/Database.md) — schema
- [`docs/API.md`](docs/API.md) — endpoint contract

## License

MIT — see [LICENSE](LICENSE).
