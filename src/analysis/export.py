from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from src.models.schemas import ComparisonResult, ModelRunResult


def _serialize_run(run: ModelRunResult) -> dict[str, Any]:
    return {
        "model_id": run.model_id,
        "lens": run.lens.value,
        "latency_ms": run.latency_ms,
        "source": run.source,
        "api_error": run.api_error,
        "lens_adherence_mismatch": run.lens_adherence_mismatch,
        "parse_error": run.parse_error,
        "verdict": run.verdict.model_dump(mode="json") if run.verdict else None,
    }


def export_comparison_json(
    comparison: ComparisonResult,
    *,
    scenario_id: str | None = None,
    framework_stress: bool = False,
    consistency_test: bool = False,
    consistency_runs: list[ModelRunResult] | None = None,
) -> str:
    payload: dict[str, Any] = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "dilemma": comparison.dilemma_text,
        "scenario_id": scenario_id,
        "options": {
            "framework_stress": framework_stress,
            "consistency_test": consistency_test,
        },
        "metrics": {
            "decision_agreement": comparison.decision_agreement,
            "decision_agreement_lexical": comparison.decision_agreement_lexical,
            "framework_agreement": comparison.framework_agreement,
            "avg_uncertainty_count": comparison.avg_uncertainty_count,
            "consistency_score": comparison.consistency_score,
            "decision_agreement_note": (
                "decision_agreement uses semantic matching; "
                "decision_agreement_lexical is exact text match."
            ),
        },
        "runs": [_serialize_run(r) for r in comparison.runs],
    }
    if consistency_runs:
        payload["consistency_runs"] = [_serialize_run(r) for r in consistency_runs]
    return json.dumps(payload, indent=2)
