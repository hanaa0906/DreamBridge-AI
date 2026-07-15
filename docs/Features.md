# DreamBridge AI — Features by Module

| # | Module                | Description                                                        | Status (v1) |
|---|------------------------|----------------------------------------------------------------------|-------------|
| 1 | Lesson Upload          | Teacher uploads PDF/image; file stored, DB record created            | ✅ Implemented |
| 2 | Content Extraction     | OCR (Tesseract) for images/scanned PDFs, direct text pull for text PDFs (PyMuPDF) | ✅ Implemented |
| 3 | Summarizer             | LLM-based summary of extracted lesson text                           | ✅ Implemented (LLM-backed, rule-based fallback) |
| 4 | Quiz Generator         | Generates MCQ/short-answer quiz from lesson text                     | ✅ Implemented (LLM-backed, rule-based fallback) |
| 5 | Translator             | Translates lesson/summary into student's preferred language          | ✅ Implemented (LLM-backed, pass-through fallback) |
| 6 | Accessibility Adapter  | Produces simplified / dyslexia-friendly / audio-ready text variants per student profile | ✅ Implemented |
| 7 | AI Tutor               | Chat interface grounded in the lesson (RAG over lesson chunks)       | ✅ Implemented (embeddings + FAISS retrieval + LLM) |
| 8 | Teacher Dashboard      | View lessons, students, and generated content                        | 🟡 API implemented, frontend minimal |
| 9 | Progress Analytics     | Track quiz scores, time spent, mastery per student                   | ✅ Implemented (API + storage) |

## Cutting features for a hackathon demo
If time is short, cut in this order (last cut first, most valuable last):
1. Progress Analytics UI polish
2. Multi-language support (keep one extra language only)
3. AI Tutor voice mode
4. Teacher dashboard styling

Never cut: upload → extract → personalize → quiz. That's the core demo loop.
