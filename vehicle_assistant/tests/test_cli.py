"""Tests for the CLI utilities of the vehicle assistant package."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import List

import pytest

sys.path.append(str(Path(__file__).resolve().parents[2]))

from vehicle_assistant.cli import _coerce_value, _parse_event_pairs, main


@pytest.mark.parametrize(
    "value,expected",
    [
        ("true", True),
        ("FALSE", False),
        ("10", 10),
        ("3.14", pytest.approx(3.14)),
        ("leading", "leading"),
    ],
)
def test_coerce_value(value: str, expected) -> None:
    assert _coerce_value(value) == expected


def test_parse_event_pairs_handles_multiple_values() -> None:
    pairs = [
        "gear=P",
        "passenger_front_door=open",
        "environment_puddle_nearby=true",
        "speed=12",
    ]

    event_state = _parse_event_pairs(pairs)

    assert event_state == {
        "gear": "P",
        "passenger_front_door": "open",
        "environment_puddle_nearby": True,
        "speed": 12,
    }


def test_parse_event_pairs_rejects_invalid_items() -> None:
    with pytest.raises(ValueError):
        _parse_event_pairs(["invalid"])


@pytest.mark.parametrize(
    "argv,expected_output",
    [
        (
            [
                "--event",
                "gear=P",
                "passenger_front_door=open",
                "environment_puddle_nearby=true",
            ],
            "- 副驾下车请注意脚下积水, 下车时观察周围环境以确保安全。\n",
        ),
        (
            [
                "--json",
                json.dumps(
                    {
                        "gear": "D",
                        "driver_door": "closed",
                    }
                ),
            ],
            "暂无推荐。\n",
        ),
    ],
)
def test_main_outputs_expected_recommendations(argv: List[str], expected_output: str, capsys):
    exit_code = main(argv)

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == expected_output


def test_main_handles_json_type_errors():
    with pytest.raises(SystemExit) as excinfo:
        main(["--json", "[]"])

    assert excinfo.value.code == 2
