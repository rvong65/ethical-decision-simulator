from __future__ import annotations

from src.ui.crisis import is_crisis_dilemma


def test_detects_self_harm_custom_dilemma():
    text = "Your AI chatbot learns a user is planning self-harm. What do you do?"
    assert is_crisis_dilemma(text)


def test_trolley_not_crisis():
    assert not is_crisis_dilemma("A runaway trolley is heading toward five people.")


def test_suicide_keyword():
    assert is_crisis_dilemma("A user says they want to die tonight.")


def test_distress_phrases():
    assert is_crisis_dilemma("I feel like I am better off dead.")
    assert is_crisis_dilemma("They said life is not worth living anymore.")


def test_philosophy_question_not_crisis():
    assert not is_crisis_dilemma("Is life worth living?")
