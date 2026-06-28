"""Sample LLM JSON fixtures for smoke tests (no API calls)."""

TROLLEY_UTILITARIAN = """{
  "creative_alternatives": ["Warn workers if time permits."],
  "decision": "Pull the lever to divert the trolley onto the side track",
  "reasoning_steps": [
    "Five lives outweigh one on a consequentialist calculus.",
    "Diverting minimizes total harm."
  ],
  "primary_framework": "utilitarian",
  "stakeholders": ["five on main track", "one on side track"],
  "harms_identified": ["death of one person"],
  "uncertainties": ["whether active intervention changes moral weight"],
  "confidence": 0.8
}"""

TROLLEY_DEONTOLOGICAL = """{
  "creative_alternatives": [],
  "decision": "Do not pull the lever",
  "reasoning_steps": [
    "Actively redirecting the trolley uses a person as a means.",
    "A duty not to kill intentionally outweighs outcome calculations."
  ],
  "primary_framework": "deontological",
  "stakeholders": ["five on main track", "one on side track", "agent at lever"],
  "harms_identified": ["five deaths if no action", "moral complicity if lever pulled"],
  "uncertainties": ["distinction between killing and letting die"],
  "confidence": 0.75
}"""

AV_SWERVE_LLAMA = """{
  "decision": "swerve into a barrier killing its single passenger",
  "reasoning_steps": [
    "Three pedestrian deaths exceed one passenger death.",
    "Minimize total fatalities."
  ],
  "primary_framework": "utilitarian",
  "stakeholders": ["pedestrians", "passenger"],
  "harms_identified": ["single fatality", "three fatalities avoided"],
  "uncertainties": ["split-second perception"],
  "confidence": 0.8
}"""

AV_SWERVE_GPT = """{
  "decision": "Program the car to swerve into the barrier, sacrificing the single passenger to avoid hitting the three pedestrians.",
  "reasoning_steps": [
    "Identify stakeholders.",
    "Minimize total deaths.",
    "Swerve saves more lives."
  ],
  "primary_framework": "utilitarian",
  "stakeholders": ["passenger", "three pedestrians"],
  "harms_identified": ["death of passenger"],
  "uncertainties": ["legal liability", "public acceptance"],
  "confidence": 0.85
}"""
