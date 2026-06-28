from __future__ import annotations

import json

from src.models.schemas import LensMode


def _framework_for_lens(lens: LensMode) -> str:
    mapping = {
        LensMode.UTILITARIAN: "utilitarian",
        LensMode.DEONTOLOGICAL: "deontological",
        LensMode.CARE: "care",
        LensMode.NEUTRAL: "mixed",
    }
    return mapping[lens]


def _decision_for_dilemma(dilemma: str, lens: LensMode) -> tuple[str, list[str], list[str]]:
    d = dilemma.lower()
    alternatives: list[str] = []

    if "trolley" in d or "lever" in d:
        alternatives = [
            "Sound an alarm to warn track workers if time permits.",
            "Attempt to derail the trolley without hitting a person (if physically possible).",
        ]
        if lens == LensMode.DEONTOLOGICAL:
            return (
                "Do not pull the lever — do not use a person as a means to an end.",
                alternatives,
                ["Duty forbids actively redirecting lethal force onto an innocent."],
            )
        return (
            "Pull the lever to divert the trolley onto the side track.",
            alternatives,
            ["Minimizing total loss of life supports diverting."] ,
        )

    if "ventilator" in d or "triage" in d:
        alternatives = [
            "Share the ventilator in shifts if clinically viable.",
            "Transfer one patient to another facility.",
        ]
        if lens == LensMode.CARE:
            return (
                "Allocate the ventilator to the 70-year-old patient with chronic illness.",
                alternatives,
                ["Prioritize the patient with greater immediate vulnerability."] ,
            )
        return (
            "Allocate the ventilator to the 25-year-old teacher.",
            alternatives,
            ["Greater life-years saved favors the younger patient."] ,
        )

    if "toxic waste" in d or "whistleblow" in d or "dumping" in d:
        alternatives = [
            "Report internally first while documenting evidence.",
            "Seek remediation before public disclosure to save jobs if harm can be stopped.",
        ]
        return (
            "Report the illegal dumping to protect the environment and public health.",
            alternatives,
            ["Long-term public health outweighs short-term job loss."] ,
        )

    if "self-driving" in d or "pedestrian" in d and "passenger" in d:
        alternatives = [
            "Design systems to prevent brake failure and avoid forced binary choices.",
            "Deploy geofencing and speed limits to reduce crash severity.",
        ]
        return (
            "Program the car to swerve into the barrier, sacrificing the passenger to avoid hitting pedestrians.",
            alternatives,
            ["Minimize total fatalities when a crash is unavoidable."] ,
        )

    if "self-harm" in d or "confidentiality" in d:
        alternatives = [
            "Provide in-app crisis resources and encourage voluntary help-seeking.",
            "Use a trained human moderator escalation path.",
        ]
        return (
            "Report the user to appropriate emergency services while documenting the minimum necessary information.",
            alternatives,
            ["Imminent risk to life may override strict confidentiality."] ,
        )

    alternatives = ["Seek mediation or a third option not presented in the scenario."]
    return (
        "Proceed with the option that minimizes foreseeable harm to the most vulnerable parties.",
        alternatives,
        ["Scenario requires judgment under constrained options."] ,
    )


def build_mock_response(dilemma: str, lens: LensMode) -> str:
    decision, alternatives, reasoning = _decision_for_dilemma(dilemma, lens)
    framework = _framework_for_lens(lens)
    payload = {
        "creative_alternatives": alternatives,
        "decision": decision,
        "reasoning_steps": reasoning + ["Simulated response — live API was unavailable."],
        "primary_framework": framework,
        "stakeholders": ["affected parties"],
        "harms_identified": ["harm under each available option"],
        "uncertainties": ["This is a simulated fallback response, not live model output."],
        "confidence": 0.6,
    }
    return json.dumps(payload)
