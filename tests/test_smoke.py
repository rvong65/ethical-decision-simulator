from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from src.analysis.compare import build_comparison, decision_agreement, decision_agreement_lexical, framework_agreement
from src.analysis.consistency import consistency_score, run_consistency_test
from src.analysis.export import export_comparison_json
from src.analysis.semantic import decisions_semantically_match, semantic_decision_agreement
from src.ethics.frameworks import build_system_prompt, build_user_prompt
from src.ethics.parser import parse_verdict
from src.llm.runner import run_parallel, run_single
from src.models.schemas import EthicalFramework, LensMode, ModelRunResult
from src.scenarios.loader import get_scenario_by_id, load_scenarios
from tests.fixtures.mock_responses import (
    AV_SWERVE_GPT,
    AV_SWERVE_LLAMA,
    TROLLEY_DEONTOLOGICAL,
    TROLLEY_UTILITARIAN,
)


class TestParser:
    def test_parses_valid_json(self):
        verdict, err = parse_verdict(TROLLEY_UTILITARIAN)
        assert err is None
        assert verdict is not None
        assert verdict.primary_framework == EthicalFramework.UTILITARIAN
        assert verdict.confidence == 0.8

    def test_parses_json_inside_code_fence(self):
        wrapped = f"```json\n{TROLLEY_UTILITARIAN}\n```"
        verdict, err = parse_verdict(wrapped)
        assert err is None
        assert verdict is not None

    def test_normalizes_framework_aliases(self):
        raw = TROLLEY_UTILITARIAN.replace('"utilitarian"', '"utilitarianism"')
        verdict, err = parse_verdict(raw)
        assert err is None
        assert verdict.primary_framework == EthicalFramework.UTILITARIAN

    def test_rejects_empty_response(self):
        verdict, err = parse_verdict("")
        assert verdict is None
        assert err is not None

    def test_rejects_invalid_json(self):
        verdict, err = parse_verdict("not json at all")
        assert verdict is None
        assert "JSON" in err

    def test_fills_missing_framework_and_confidence(self):
        partial = """{
          "decision": "Report the illegal dumping",
          "reasoning_steps": ["Duty to prevent harm outweighs job loss."]
        }"""
        verdict, err = parse_verdict(partial)
        assert err is None
        assert verdict is not None
        assert verdict.primary_framework == EthicalFramework.MIXED
        assert verdict.confidence == 0.5


class TestScenarios:
    def test_library_loads(self):
        assert len(load_scenarios()) >= 12

    def test_trolley_scenario_has_rephrase_variants(self):
        scenario = get_scenario_by_id("trolley_classic")
        assert scenario is not None
        assert len(scenario.rephrase_variants) >= 2

    def test_whistleblowing_scenario_exists(self):
        scenario = get_scenario_by_id("whistleblowing")
        assert scenario is not None
        assert "report" in scenario.dilemma_text.lower() or "dumping" in scenario.dilemma_text.lower()


class TestPrompts:
    def test_deontological_lens_differs_from_neutral(self):
        assert build_system_prompt(LensMode.NEUTRAL) != build_system_prompt(LensMode.DEONTOLOGICAL)
        assert "deontologist" in build_system_prompt(LensMode.DEONTOLOGICAL).lower()

    def test_user_prompt_includes_dilemma_and_alternatives(self):
        text = "A unique dilemma string for testing."
        prompt = build_user_prompt(text)
        assert text in prompt
        assert "creative_alternatives" in prompt


class TestAnalysis:
    def _result(self, model_id: str, raw: str, lens: LensMode = LensMode.NEUTRAL) -> ModelRunResult:
        verdict, err = parse_verdict(raw)
        return ModelRunResult(
            model_id=model_id,
            lens=lens,
            verdict=verdict,
            raw_response=raw,
            parse_error=err,
            latency_ms=100.0,
        )

    def test_framework_agreement_when_both_utilitarian(self):
        runs = [self._result("a", AV_SWERVE_LLAMA), self._result("b", AV_SWERVE_GPT)]
        assert framework_agreement(runs) == 1.0

    def test_decision_agreement_semantic_vs_lexical(self):
        runs = [
            self._result("llama-3.1-8b-instant", AV_SWERVE_LLAMA),
            self._result("openai/gpt-oss-20b", AV_SWERVE_GPT),
        ]
        assert decision_agreement(runs) == 1.0
        assert decision_agreement_lexical(runs) == 0.5

    def test_whistleblowing_semantic_agreement(self):
        a = "Report the toxic waste dumping to protect the environment"
        b = "Report the illegal dumping to protect the river and downstream communities."
        assert decisions_semantically_match(a, b)
        assert semantic_decision_agreement([a, b]) == 1.0

    def test_consistency_score_all_match(self):
        baseline = self._result("m", TROLLEY_UTILITARIAN)
        variants = [self._result("m", TROLLEY_UTILITARIAN), self._result("m", TROLLEY_UTILITARIAN)]
        assert consistency_score(baseline, variants) == 1.0

    def test_consistency_score_flip_detected(self):
        baseline = self._result("m", TROLLEY_UTILITARIAN)
        variants = [self._result("m", TROLLEY_DEONTOLOGICAL)]
        assert consistency_score(baseline, variants) == 0.0


class TestExportFormat:
    def test_export_includes_metrics(self):
        runs = [
            ModelRunResult(
                model_id="a",
                lens=LensMode.NEUTRAL,
                verdict=parse_verdict(AV_SWERVE_LLAMA)[0],
                raw_response="",
                parse_error=None,
                latency_ms=100,
            ),
            ModelRunResult(
                model_id="b",
                lens=LensMode.NEUTRAL,
                verdict=parse_verdict(AV_SWERVE_GPT)[0],
                raw_response="",
                parse_error=None,
                latency_ms=100,
            ),
        ]
        comparison = build_comparison("test dilemma", runs, consistency_score=0.5)
        payload = json.loads(
            export_comparison_json(
                comparison,
                scenario_id="whistleblowing",
                framework_stress=False,
                consistency_test=True,
            )
        )
        assert payload["metrics"]["decision_agreement"] == 1.0
        assert payload["metrics"]["decision_agreement_lexical"] == 0.5
        assert payload["metrics"]["consistency_score"] == 0.5
        assert payload["scenario_id"] == "whistleblowing"


class TestPipelineSmoke:
    @patch("src.llm.runner.get_provider")
    def test_run_single_mocked(self, mock_get_provider):
        mock_provider = MagicMock()
        mock_provider.complete.return_value = TROLLEY_UTILITARIAN
        mock_get_provider.return_value = mock_provider

        result = run_single("Pull the lever?", "Llama 3.1 8B (Groq)", LensMode.NEUTRAL)

        assert result.parse_error is None
        assert result.verdict is not None
        mock_provider.complete.assert_called_once()

    @patch("src.llm.runner.get_provider")
    def test_run_parallel_mocked(self, mock_get_provider):
        def side_effect(system, user, model=None, json_mode=True, lens=None, dilemma_text=""):
            if "gpt-oss" in (model or ""):
                return AV_SWERVE_GPT
            return AV_SWERVE_LLAMA

        mock_provider = MagicMock()
        mock_provider.complete.side_effect = side_effect
        mock_provider.last_fallback_reason = None
        mock_get_provider.return_value = mock_provider

        results = run_parallel(
            "AV dilemma",
            ["Llama 3.1 8B (Groq)", "GPT-OSS 20B (Groq)"],
            [LensMode.NEUTRAL],
        )

        assert len(results) == 2
        assert all(r.verdict is not None for r in results)

    @patch("src.analysis.consistency.run_single")
    def test_consistency_test_smoke(self, mock_run_single):
        mock_run_single.side_effect = [
            ModelRunResult(
                model_id="llama-3.1-8b-instant",
                lens=LensMode.NEUTRAL,
                verdict=parse_verdict(TROLLEY_UTILITARIAN)[0],
                raw_response=TROLLEY_UTILITARIAN,
                parse_error=None,
                latency_ms=100,
            ),
            ModelRunResult(
                model_id="llama-3.1-8b-instant",
                lens=LensMode.NEUTRAL,
                verdict=parse_verdict(TROLLEY_UTILITARIAN)[0],
                raw_response=TROLLEY_UTILITARIAN,
                parse_error=None,
                latency_ms=100,
            ),
            ModelRunResult(
                model_id="llama-3.1-8b-instant",
                lens=LensMode.NEUTRAL,
                verdict=parse_verdict(TROLLEY_DEONTOLOGICAL)[0],
                raw_response=TROLLEY_DEONTOLOGICAL,
                parse_error=None,
                latency_ms=100,
            ),
        ]

        _, variants, score = run_consistency_test(
            "trolley",
            ["rephrase A", "rephrase B"],
            "Llama 3.1 8B (Groq)",
        )

        assert len(variants) == 2
        assert score == 0.5
