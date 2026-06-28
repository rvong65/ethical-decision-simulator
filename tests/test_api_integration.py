from __future__ import annotations

import os

import pytest

from src.config import groq_configured
from src.llm.runner import run_single
from src.models.schemas import LensMode
from src.scenarios.loader import get_scenario_by_id


def _api_available() -> bool:
    if os.environ.get("LLM_PROVIDER", "groq").lower() == "ollama":
        return False
    return groq_configured()


pytestmark = pytest.mark.skipif(
    not _api_available(),
    reason="Set GROQ_API_KEY to run live API integration tests",
)


@pytest.mark.api
def test_api_run_single_trolley_parses():
    scenario = get_scenario_by_id("trolley_classic")
    assert scenario is not None

    result = run_single(
        scenario.dilemma_text,
        "Llama 3.1 8B (Groq)",
        LensMode.NEUTRAL,
    )

    assert result.parse_error is None, result.parse_error
    assert result.verdict is not None
    assert result.verdict.decision
    assert len(result.verdict.reasoning_steps) >= 1
    assert 0.0 <= result.verdict.confidence <= 1.0


@pytest.mark.api
def test_api_run_single_forced_lens_parses():
    scenario = get_scenario_by_id("trolley_classic")
    assert scenario is not None

    result = run_single(
        scenario.dilemma_text,
        "GPT-OSS 20B (Groq)",
        LensMode.UTILITARIAN,
    )

    assert result.parse_error is None, result.raw_response or result.parse_error
    assert result.verdict is not None
    assert "lever" in result.verdict.decision.lower() or "divert" in result.verdict.decision.lower()


@pytest.mark.api
def test_api_whistleblowing_both_models_parse():
    """Two Groq models on whistleblowing scenario return structured verdicts."""
    from src.llm.runner import run_parallel

    scenario = get_scenario_by_id("whistleblowing")
    assert scenario is not None

    results = run_parallel(
        scenario.dilemma_text,
        ["Llama 3.1 8B (Groq)", "GPT-OSS 20B (Groq)"],
        [LensMode.NEUTRAL],
    )

    assert len(results) == 2
    for result in results:
        assert result.parse_error is None, (
            f"{result.model_id}: {result.parse_error}\n{result.raw_response[:500]}"
        )
        assert result.verdict is not None
        assert "report" in result.verdict.decision.lower()
