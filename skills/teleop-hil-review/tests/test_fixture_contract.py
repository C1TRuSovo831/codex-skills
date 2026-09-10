#!/usr/bin/env python3
"""Validate the forward-test fixture's schema and branch coverage."""

from __future__ import annotations

import json
from pathlib import Path


FIXTURE = Path(__file__).parent / "fixtures" / "scenarios.json"
REQUIRED_IDS = {
    "reviewer-static-only-hil-claim",
    "reviewer-fake-arm-chain",
    "reviewer-connected-hardware-user-report",
    "reviewer-scoped-real-hil",
    "planner-final-scope",
    "wrong-role",
}
ALLOWED_FIRST_LINES = {"PASS", "CHANGES_REQUIRED", "APPROVED", "NOT APPROVED", "NOT RUN"}


def main() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    invariants = payload["contract_invariants"]
    assert any("TASK_ID, ROUND, and HANDOFF_ID" in item for item in invariants)
    assert any("Planner alone" in item for item in invariants)
    cases = payload["cases"]
    assert {case["id"] for case in cases} == REQUIRED_IDS

    for case in cases:
        assert case["role"] in {"Planner", "Reviewer", "Coder"}
        assert case["available_evidence"]
        expected = case["expected"]
        assert expected["first_line"] in ALLOWED_FIRST_LINES
        assert isinstance(expected["supported_classes"], list)
        assert expected["must_preserve"]

    wrong_role = next(case for case in cases if case["id"] == "wrong-role")
    assert wrong_role["expected"]["first_line"] == "NOT RUN"
    assert any("$teleop-hil-review" in case["request"] for case in cases)
    assert any("$teleop-hil-review" not in case["request"] for case in cases)
    print(f"OK: {len(cases)} teleop-hil-review forward-test fixtures")


if __name__ == "__main__":
    main()
