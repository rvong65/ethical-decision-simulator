from __future__ import annotations

import json
import re

from src.models.schemas import EthicalFramework, EthicalVerdict


def _extract_json(raw: str) -> str:
    text = raw.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence_match:
        return fence_match.group(1).strip()

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return text


def _normalize_framework(value: str) -> EthicalFramework:
    normalized = value.lower().strip()
    mapping = {
        "utilitarian": EthicalFramework.UTILITARIAN,
        "utilitarianism": EthicalFramework.UTILITARIAN,
        "deontological": EthicalFramework.DEONTOLOGICAL,
        "deontology": EthicalFramework.DEONTOLOGICAL,
        "virtue": EthicalFramework.VIRTUE,
        "virtue ethics": EthicalFramework.VIRTUE,
        "care": EthicalFramework.CARE,
        "care ethics": EthicalFramework.CARE,
        "mixed": EthicalFramework.MIXED,
    }
    return mapping.get(normalized, EthicalFramework.MIXED)


def _fill_missing_fields(payload: dict) -> dict:
    """Apply safe defaults when models omit optional schema fields."""
    filled = dict(payload)
    if "stakeholders" not in filled:
        filled["stakeholders"] = []
    if "harms_identified" not in filled:
        filled["harms_identified"] = []
    if "creative_alternatives" not in filled:
        filled["creative_alternatives"] = []
    if "primary_framework" not in filled:
        filled["primary_framework"] = "mixed"
    if "confidence" not in filled:
        filled["confidence"] = 0.5
    return filled


def parse_verdict(raw: str) -> tuple[EthicalVerdict | None, str | None]:
    if not raw.strip():
        return None, "Empty response from model"

    try:
        payload = json.loads(_extract_json(raw))
    except json.JSONDecodeError as exc:
        return None, f"JSON parse error: {exc}"

    if not isinstance(payload, dict):
        return None, "JSON root must be an object"

    payload = _fill_missing_fields(payload)

    if "primary_framework" in payload:
        payload["primary_framework"] = _normalize_framework(str(payload["primary_framework"]))

    try:
        return EthicalVerdict.model_validate(payload), None
    except Exception as exc:
        return None, f"Schema validation error: {exc}"
