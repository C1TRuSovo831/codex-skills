#!/usr/bin/env python3
"""Validate the requirements-grill forward-test fixture contract."""

from __future__ import annotations

import json
from pathlib import Path


FIXTURE = Path(__file__).parent / "fixtures" / "scenarios.json"
REQUIRED_IDS = {
    "planner-vague-high-impact",
    "planner-discoverable-fact",
    "planner-complete-contract",
    "wrong-role",
}


def main() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    cases = payload["cases"]
    assert {case["id"] for case in cases} == REQUIRED_IDS
    for case in cases:
        assert case["role"] in {"Planner", "Coder"}
        assert case["request"]
        assert case["evidence"]
        assert case["expected"]
    wrong_role = next(case for case in cases if case["id"] == "wrong-role")
    assert "ROLE_MISMATCH" in wrong_role["expected"]
    print(f"OK: {len(cases)} herdr-requirements-grill forward-test fixtures")


if __name__ == "__main__":
    main()
