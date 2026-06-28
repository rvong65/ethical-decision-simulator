from __future__ import annotations

from collections import Counter

from src.llm.runner import run_single
from src.models.schemas import LensMode, ModelRunResult


def _normalize_decision(text: str) -> str:
    return " ".join(text.lower().split())


def consistency_score(
    baseline: ModelRunResult,
    variant_results: list[ModelRunResult],
) -> float:
    if not baseline.verdict:
        return 0.0

    base_decision = _normalize_decision(baseline.verdict.decision)
    comparable = [r for r in variant_results if r.verdict]
    if not comparable:
        return 0.0

    matches = sum(
        1 for r in comparable if _normalize_decision(r.verdict.decision) == base_decision
    )
    return matches / len(comparable)


def run_consistency_test(
    dilemma_text: str,
    rephrase_variants: list[str],
    model_display: str,
) -> tuple[ModelRunResult, list[ModelRunResult], float]:
    baseline = run_single(dilemma_text, model_display, LensMode.NEUTRAL)
    variants = [run_single(text, model_display, LensMode.NEUTRAL) for text in rephrase_variants]
    score = consistency_score(baseline, variants)
    return baseline, variants, score
