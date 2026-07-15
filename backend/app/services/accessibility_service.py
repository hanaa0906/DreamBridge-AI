"""Module 6: Accessibility Adapter.

Combines translation + simplification + format guidance based on a
student's profile (learning_style, accessibility_type, difficulty).
"""
from app.services import llm_service, translation_service

DIFFICULTY_INSTRUCTIONS = {
    "beginner": "Use very simple vocabulary, short sentences, and concrete examples.",
    "intermediate": "Use grade-appropriate vocabulary with some technical terms explained.",
    "advanced": "Use precise, subject-appropriate vocabulary and assume prior knowledge.",
}

ACCESSIBILITY_INSTRUCTIONS = {
    "none": "No special adaptation needed beyond the difficulty level.",
    "dyslexia": "Use short paragraphs, bullet points, avoid dense blocks of text, "
                "define any jargon in-line, and prefer active voice.",
    "low_vision": "Structure text with clear headings and short lines so it reads well "
                  "at large font sizes and works well with text-to-speech.",
    "hearing_impaired": "Ensure all information is fully conveyed in text with no reliance "
                        "on implied audio/visual cues; add explicit descriptions where needed.",
}

LEARNING_STYLE_INSTRUCTIONS = {
    "visual": "Suggest where a diagram or image would help, described in words.",
    "auditory": "Write in a conversational, read-aloud-friendly style suited for text-to-speech.",
    "reading": "Write as clear structured prose with headings and bullet points.",
    "kinesthetic": "Include a short hands-on activity or thought experiment per section.",
}


def format_notes_for(profile) -> str:
    return (
        f"difficulty={profile.difficulty}; "
        f"accessibility={profile.accessibility_type}; "
        f"learning_style={profile.learning_style}"
    )


def personalize(lesson_text: str, profile) -> str:
    difficulty_instr = DIFFICULTY_INSTRUCTIONS.get(profile.difficulty, DIFFICULTY_INSTRUCTIONS["beginner"])
    access_instr = ACCESSIBILITY_INSTRUCTIONS.get(profile.accessibility_type, ACCESSIBILITY_INSTRUCTIONS["none"])
    style_instr = LEARNING_STYLE_INSTRUCTIONS.get(profile.learning_style, LEARNING_STYLE_INSTRUCTIONS["reading"])

    fallback = llm_service.naive_wrap(lesson_text)
    prompt = (
        "Rewrite the lesson text below for a specific student.\n"
        f"Difficulty guidance: {difficulty_instr}\n"
        f"Accessibility guidance: {access_instr}\n"
        f"Learning-style guidance: {style_instr}\n\n"
        f"LESSON TEXT:\n{lesson_text[:8000]}"
    )
    adapted = llm_service.generate(prompt, fallback)

    if profile.language and profile.language != "en":
        adapted = translation_service.translate(adapted, profile.language)

    return adapted
