from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.ethics.frameworks import build_system_prompt, build_user_prompt, lens_adherence_mismatch
from src.ethics.parser import parse_verdict
from src.llm.errors import NOT_CONFIGURED_MESSAGE, friendly_api_error
from src.llm.provider import MockProvider, ResilientProvider, get_provider, resolve_model_id
from src.models.schemas import LensMode, ModelRunResult


def run_single(
    dilemma_text: str,
    model_display: str,
    lens: LensMode = LensMode.NEUTRAL,
) -> ModelRunResult:
    provider = get_provider()
    model_id = resolve_model_id(model_display)
    system = build_system_prompt(lens)
    user = build_user_prompt(dilemma_text)

    start = time.perf_counter()
    source = "live"
    api_error: str | None = None
    raw = ""

    try:
        raw = provider.complete(
            system, user, model=model_id, lens=lens, dilemma_text=dilemma_text,
        )
        if isinstance(provider, MockProvider):
            source = "mock"
            api_error = NOT_CONFIGURED_MESSAGE
        elif isinstance(provider, ResilientProvider) and provider.last_fallback_reason:
            source = "mock"
            api_error = provider.last_fallback_reason
    except Exception as exc:
        elapsed = (time.perf_counter() - start) * 1000
        api_error = friendly_api_error(exc)
        try:
            raw = MockProvider().complete(
                system, user, model=model_id, lens=lens, dilemma_text=dilemma_text,
            )
            source = "mock"
        except Exception:
            return ModelRunResult(
                model_id=model_id,
                lens=lens,
                raw_response="",
                parse_error=None,
                latency_ms=elapsed,
                source="mock",
                api_error=api_error,
            )

    elapsed = (time.perf_counter() - start) * 1000
    verdict, error = parse_verdict(raw)
    mismatch = False
    if verdict and lens != LensMode.NEUTRAL:
        mismatch = lens_adherence_mismatch(lens, verdict.primary_framework.value)

    return ModelRunResult(
        model_id=model_id,
        lens=lens,
        verdict=verdict,
        raw_response=raw,
        parse_error=error,
        latency_ms=elapsed,
        source=source,
        api_error=api_error,
        lens_adherence_mismatch=mismatch,
    )


def run_parallel(
    dilemma_text: str,
    model_displays: list[str],
    lenses: list[LensMode] | None = None,
) -> list[ModelRunResult]:
    lenses = lenses or [LensMode.NEUTRAL]
    tasks = [(m, lens) for m in model_displays for lens in lenses]

    results: list[ModelRunResult] = []
    with ThreadPoolExecutor(max_workers=min(8, len(tasks) or 1)) as executor:
        futures = {
            executor.submit(run_single, dilemma_text, model, lens): (model, lens)
            for model, lens in tasks
        }
        for future in as_completed(futures):
            results.append(future.result())

    return results
