"""Module 4: Quiz Generator."""
import json
import re
from app.services import llm_service


def _fallback_questions(text: str, n: int = 5):
    """Rule-based fallback: turn the first N sentences into simple recall
    fill-in-the-blank-style questions so the endpoint always returns
    something useful even without an LLM key."""
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if len(s.strip()) > 25]
    questions = []
    for s in sentences[:n]:
        questions.append(
            {
                "question": f"Explain in your own words: \"{s[:120]}...\"" if len(s) > 120 else f"Explain in your own words: \"{s}\"",
                "options": [],
                "answer": s,
                "explanation": "Open-ended recall question generated from the lesson text.",
            }
        )
    if not questions:
        questions.append(
            {
                "question": "Summarize the main idea of this lesson.",
                "options": [],
                "answer": "See lesson summary.",
                "explanation": None,
            }
        )
    return questions


def generate_quiz(text: str, num_questions: int = 5):
    fallback_questions = _fallback_questions(text, num_questions)
    fallback_json = json.dumps(fallback_questions)

    prompt = (
        f"Create {num_questions} multiple-choice quiz questions from the lesson text below. "
        "Return ONLY valid JSON: a list of objects with keys "
        '"question", "options" (list of 4 strings), "answer" (must match one option exactly), '
        '"explanation" (one sentence). No markdown, no code fences, JSON only.\n\n'
        f"LESSON TEXT:\n{text[:8000]}"
    )
    raw = llm_service.generate(prompt, fallback_json)

    try:
        cleaned = re.sub(r"^```json|```$", "", raw.strip(), flags=re.MULTILINE).strip()
        questions = json.loads(cleaned)
        assert isinstance(questions, list) and len(questions) > 0
        return questions
    except Exception:
        return fallback_questions
