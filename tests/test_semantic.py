from __future__ import annotations

import pytest

from src.analysis.semantic import decisions_semantically_match, semantic_decision_agreement


class TestSemanticAgreement:
    def test_whistleblowing_demo5_wording(self):
        a = "Report the toxic waste dumping to protect the environment and public health"
        b = "Report the illegal dumping to protect the river and downstream communities."
        assert decisions_semantically_match(a, b)

    def test_av_demo3_wording(self):
        a = "swerve into a barrier killing its single passenger"
        b = "Program the car to swerve into the barrier, sacrificing the single passenger to avoid hitting the three pedestrians."
        assert decisions_semantically_match(a, b)

    def test_opposite_decisions_do_not_match(self):
        assert not decisions_semantically_match(
            "Pull the lever to divert the trolley",
            "Do not pull the lever",
        )

    def test_agreement_score_for_demo5_pair(self):
        decisions = [
            "Report the toxic waste dumping to protect the environment and public health",
            "Report the illegal dumping to protect the river and downstream communities.",
        ]
        assert semantic_decision_agreement(decisions) == 1.0
