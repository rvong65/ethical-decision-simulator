from __future__ import annotations

from collections import Counter

from src.analysis.semantic import semantic_decision_agreement
from src.models.schemas import ComparisonResult, ModelRunResult


def _normalize_decision(text: str) -> str:
    return " ".join(text.lower().split())


def decision_agreement_lexical(runs: list[ModelRunResult]) -> float:
    verdicts = [r for r in runs if r.verdict and r.lens.value == "neutral"]
    if len(verdicts) < 2:
        return 1.0 if verdicts else 0.0

    decisions = [_normalize_decision(r.verdict.decision) for r in verdicts]
    most_common = Counter(decisions).most_common(1)[0][1]
    return most_common / len(decisions)


def decision_agreement(runs: list[ModelRunResult]) -> float:
    verdicts = [r for r in runs if r.verdict and r.lens.value == "neutral"]
    if len(verdicts) < 2:
        return 1.0 if verdicts else 0.0

    decisions = [r.verdict.decision for r in verdicts]
    return semantic_decision_agreement(decisions)


def framework_agreement(runs: list[ModelRunResult]) -> float:
    verdicts = [r for r in runs if r.verdict and r.lens.value == "neutral"]
    if len(verdicts) < 2:
        return 1.0 if verdicts else 0.0

    frameworks = [r.verdict.primary_framework.value for r in verdicts]
    most_common = Counter(frameworks).most_common(1)[0][1]
    return most_common / len(frameworks)


def avg_uncertainty_count(runs: list[ModelRunResult]) -> float:
    verdicts = [r for r in runs if r.verdict]
    if not verdicts:
        return 0.0
    return sum(len(r.verdict.uncertainties) for r in verdicts) / len(verdicts)


def build_comparison(
    dilemma_text: str,
    runs: list[ModelRunResult],
    consistency_score: float | None = None,
) -> ComparisonResult:
    return ComparisonResult(
        dilemma_text=dilemma_text,
        runs=runs,
        decision_agreement=decision_agreement(runs),
        decision_agreement_lexical=decision_agreement_lexical(runs),
        framework_agreement=framework_agreement(runs),
        consistency_score=consistency_score,
        avg_uncertainty_count=avg_uncertainty_count(runs),
    )
