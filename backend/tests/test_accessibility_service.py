from types import SimpleNamespace
from app.services.accessibility_service import personalize, format_notes_for


def test_personalize_no_llm_key_returns_wrapped_text():
    profile = SimpleNamespace(
        language="en", learning_style="reading", accessibility_type="dyslexia", difficulty="beginner"
    )
    text = "This is a lesson about the water cycle and how rain forms from evaporated water."
    result = personalize(text, profile)
    assert isinstance(result, str)
    assert len(result) > 0


def test_format_notes_for():
    profile = SimpleNamespace(
        language="ta", learning_style="visual", accessibility_type="low_vision", difficulty="advanced"
    )
    notes = format_notes_for(profile)
    assert "advanced" in notes
    assert "low_vision" in notes
    assert "visual" in notes
