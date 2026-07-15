"""Module 3: Summarizer."""
from app.services import llm_service


def summarize(text: str) -> str:
    fallback = llm_service.naive_summary(text, max_sentences=5)
    prompt = (
        "Summarize the following lesson for a teacher's overview. "
        "Keep it to 4-6 sentences, plain language, no markdown headers.\n\n"
        f"LESSON TEXT:\n{text[:8000]}"
    )
    return llm_service.generate(prompt, fallback)
