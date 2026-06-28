from __future__ import annotations

from unittest.mock import patch

import pytest

from src.ethics.parser import parse_verdict
from src.llm.mock_provider import build_mock_response
from src.llm.runner import run_single
from src.models.schemas import LensMode
from src.scenarios.loader import load_scenarios


@pytest.mark.parametrize("scenario_id", [s.id for s in load_scenarios()])
def test_mock_response_parses_for_every_scenario(scenario_id):
    from src.scenarios.loader import get_scenario_by_id

    scenario = get_scenario_by_id(scenario_id)
    assert scenario is not None

    for lens in (LensMode.NEUTRAL, LensMode.UTILITARIAN, LensMode.DEONTOLOGICAL, LensMode.CARE):
        raw = build_mock_response(scenario.dilemma_text, lens)
        verdict, err = parse_verdict(raw)
        assert err is None, f"{scenario_id}/{lens.value}: {err}"
        assert verdict is not None
        assert verdict.decision
        assert verdict.creative_alternatives is not None


@patch("src.llm.runner.get_provider")
def test_runner_uses_mock_when_no_api(mock_get_provider):
    from src.llm.provider import MockProvider

    mock_get_provider.return_value = MockProvider()
    scenario = load_scenarios()[0]

    result = run_single(scenario.dilemma_text, "Llama 3.1 8B (Groq)", LensMode.NEUTRAL)

    assert result.parse_error is None
    assert result.source == "mock"
    assert result.verdict is not None
    assert len(result.verdict.creative_alternatives) >= 0
