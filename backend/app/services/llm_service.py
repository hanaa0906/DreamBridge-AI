"""
Thin wrapper around the LLM provider.

Uses Gemini by default. If no API key is configured, falls back to a
deterministic rule-based response so every endpoint stays demoable
without any external credentials. Swap `_call_gemini` for another
provider's SDK if you prefer (OpenAI, Anthropic, etc.) — everything
else in the app talks to this module only, not the provider directly.
"""
import textwrap
from app.core.config import settings

_configured = False


def _ensure_configured():
    global _configured
    if _configured or not settings.gemini_api_key:
        return
    import google.generativeai as genai
    genai.configure(api_key=settings.gemini_api_key)
    _configured = True


def is_llm_available() -> bool:
    return bool(settings.gemini_api_key)


def _call_gemini(prompt: str) -> str:
    import google.generativeai as genai
    _ensure_configured()
    model = genai.GenerativeModel(settings.llm_model)
    response = model.generate_content(prompt)
    return response.text


def generate(prompt: str, fallback: str) -> str:
    """Call the LLM if configured, otherwise return the given fallback."""
    if not is_llm_available():
        return fallback
    try:
        return _call_gemini(prompt)
    except Exception as exc:  # noqa: BLE001 - surface a usable fallback either way
        return f"{fallback}\n\n[LLM call failed, showing rule-based fallback: {exc}]"


def naive_summary(text: str, max_sentences: int = 5) -> str:
    """Very simple extractive fallback summary: first N sentences."""
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    return ". ".join(sentences[:max_sentences]) + ("." if sentences else "")


def naive_wrap(text: str, width: int = 100) -> str:
    return "\n".join(textwrap.wrap(text, width=width))
