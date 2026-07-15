from app.services.quiz_service import generate_quiz


def test_generate_quiz_fallback_no_llm_key():
    text = (
        "Photosynthesis is the process plants use to convert light into energy. "
        "It occurs mainly in the leaves, inside structures called chloroplasts. "
        "Water and carbon dioxide are combined using light energy to produce glucose and oxygen."
    )
    questions = generate_quiz(text, num_questions=2)
    assert isinstance(questions, list)
    assert len(questions) >= 1
    assert "question" in questions[0]
    assert "answer" in questions[0]
