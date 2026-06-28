from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class EthicalFramework(str, Enum):
    UTILITARIAN = "utilitarian"
    DEONTOLOGICAL = "deontological"
    VIRTUE = "virtue"
    CARE = "care"
    MIXED = "mixed"


class LensMode(str, Enum):
    NEUTRAL = "neutral"
    UTILITARIAN = "utilitarian"
    DEONTOLOGICAL = "deontological"
    CARE = "care"


class EthicalVerdict(BaseModel):
    decision: str = Field(description="Chosen action in one sentence")
    reasoning_steps: list[str] = Field(min_length=1)
    primary_framework: EthicalFramework
    creative_alternatives: list[str] = Field(default_factory=list)
    stakeholders: list[str] = Field(default_factory=list)
    harms_identified: list[str] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)


class ModelRunResult(BaseModel):
    model_id: str
    lens: LensMode
    verdict: EthicalVerdict | None = None
    raw_response: str = ""
    parse_error: str | None = None
    latency_ms: float = 0.0
    source: str = "live"  # live | mock
    api_error: str | None = None
    lens_adherence_mismatch: bool = False


class ComparisonResult(BaseModel):
    dilemma_text: str
    runs: list[ModelRunResult]
    decision_agreement: float
    decision_agreement_lexical: float
    framework_agreement: float
    consistency_score: float | None = None
    avg_uncertainty_count: float


class Scenario(BaseModel):
    id: str
    title: str
    category: str
    dilemma_text: str
    stakes: list[str]
    framework_tension: str
    rephrase_variants: list[str] = Field(default_factory=list)


def verdict_to_dict(verdict: EthicalVerdict) -> dict[str, Any]:
    return verdict.model_dump(mode="json")
