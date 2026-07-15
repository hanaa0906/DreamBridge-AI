"""Module 5: Translator.

Uses the configured LLM for translation (works well for major and most
Indic languages with Gemini). If no LLM key is configured, falls back
to returning the original text with a notice, so the pipeline never
breaks — swap in IndicTrans2 or Google Translate API here if you want
a dedicated translation model instead of the general LLM.
"""
from app.services import llm_service

LANGUAGE_NAMES = {
    "en": "English",
    "ta": "Tamil",
    "hi": "Hindi",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "bn": "Bengali",
    "mr": "Marathi",
    "es": "Spanish",
    "fr": "French",
}


def translate(text: str, target_language: str) -> str:
    lang_name = LANGUAGE_NAMES.get(target_language, target_language)
    fallback = f"[Translation unavailable without an LLM key — original text shown]\n\n{text}"
    prompt = (
        f"Translate the following lesson text into {lang_name}. "
        "Keep the meaning and tone faithful, use natural phrasing for students, "
        "and return only the translated text.\n\n"
        f"TEXT:\n{text[:8000]}"
    )
    return llm_service.generate(prompt, fallback)
