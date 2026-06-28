from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from src.models.schemas import Scenario

LIBRARY_PATH = Path(__file__).parent / "library.json"


@lru_cache(maxsize=1)
def load_scenarios() -> list[Scenario]:
    with LIBRARY_PATH.open(encoding="utf-8") as f:
        data = json.load(f)
    return [Scenario.model_validate(item) for item in data]


def get_scenario_by_id(scenario_id: str) -> Scenario | None:
    for scenario in load_scenarios():
        if scenario.id == scenario_id:
            return scenario
    return None


def scenario_options() -> dict[str, str]:
    return {s.title: s.id for s in load_scenarios()}
