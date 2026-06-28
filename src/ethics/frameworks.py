from __future__ import annotations

import json
import re

from src.models.schemas import LensMode

FRAMEWORK_DESCRIPTIONS = {
    "utilitarian": {
        "name": "Utilitarianism",
        "summary": "Judges actions by their consequences — maximizing overall well-being or minimizing total harm.",
        "key_question": "Which option produces the greatest good for the greatest number?",
    },
    "deontological": {
        "name": "Deontological Ethics",
        "summary": "Focuses on duties, rules, and rights. Some actions are wrong regardless of outcomes.",
        "key_question": "What moral duties or principles apply, even if the outcome is worse?",
    },
    "virtue": {
        "name": "Virtue Ethics",
        "summary": "Asks what a person of good character would do, emphasizing integrity, courage, and wisdom.",
        "key_question": "What would a virtuous agent do in this situation?",
    },
    "care": {
        "name": "Care Ethics",
        "summary": "Prioritizes relationships, empathy, and responsiveness to those who are vulnerable.",
        "key_question": "Who is most vulnerable, and how do we honor our obligations to them?",
    },
    "mixed": {
        "name": "Mixed Framework",
        "summary": "The model drew on multiple ethical lenses without committing to one dominant framework.",
        "key_question": "Which frameworks are in tension, and how were they balanced?",
    },
}

LENS_FRAMEWORK = {
    LensMode.NEUTRAL: None,
    LensMode.UTILITARIAN: "utilitarian",
    LensMode.DEONTOLOGICAL: "deontological",
    LensMode.CARE: "care",
}

LENS_INSTRUCTIONS = {
    LensMode.NEUTRAL: (
        "Reason through the dilemma honestly. Identify which ethical framework best "
        "describes your reasoning, even if multiple frameworks are in tension."
    ),
    LensMode.UTILITARIAN: (
        "You MUST reason strictly as a utilitarian. Maximize overall well-being and "
        "minimize total harm. Consequentialist outcomes override rules. "
        "Do NOT cite duties, rights, or non-consequentialist principles as decisive. "
        "Set primary_framework to \"utilitarian\"."
    ),
    LensMode.DEONTOLOGICAL: (
        "You MUST reason strictly as a deontologist. Honor duties, rights, and "
        "universalizable rules even when outcomes would be worse. "
        "Do NOT justify the decision primarily by counting lives saved or total harm "
        "minimized — that is utilitarian reasoning. "
        "If you would pull a lever or sacrifice one to save many, explain why duty "
        "permits or forbids it without appeal to aggregate welfare. "
        "Set primary_framework to \"deontological\"."
    ),
    LensMode.CARE: (
        "You MUST reason from a care ethics perspective. Prioritize relationships, "
        "empathy, and protecting the most vulnerable parties. "
        "Set primary_framework to \"care\"."
    ),
}

JSON_SCHEMA_HINT = """\
Respond with ONLY valid JSON matching this schema:
{
  "creative_alternatives": ["ways to reduce harm or avoid the forced tradeoff, if any"],
  "decision": "string — chosen action in one sentence (given the dilemma as stated)",
  "reasoning_steps": ["ordered list of reasoning steps"],
  "primary_framework": "utilitarian | deontological | virtue | care | mixed",
  "stakeholders": ["parties affected"],
  "harms_identified": ["potential harms"],
  "uncertainties": ["where judgment is ambiguous"],
  "confidence": 0.0 to 1.0
}"""


def build_system_prompt(lens: LensMode) -> str:
    instruction = LENS_INSTRUCTIONS[lens]
    return f"""You are an ethical reasoning analyst. {instruction}

Be transparent and auditable. Acknowledge trade-offs and uncertainty where they exist.
Do not claim moral authority — explain your reasoning clearly.

{JSON_SCHEMA_HINT}"""


def build_user_prompt(dilemma_text: str) -> str:
    return f"""Analyze this moral dilemma and return structured JSON.

Step 1 — Before choosing between the stated options, list any creative_alternatives
(realistic ways to reduce harm or avoid the forced tradeoff). Use an empty list if
none exist within the scenario constraints.

Step 2 — Analyze the dilemma AS STATED and give your decision and reasoning.

---
{dilemma_text}
---"""


def lens_adherence_mismatch(lens: LensMode, detected_framework: str) -> bool:
    required = LENS_FRAMEWORK.get(lens)
    if required is None:
        return False
    return detected_framework != required
