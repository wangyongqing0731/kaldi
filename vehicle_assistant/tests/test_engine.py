"""Tests for the vehicle assistant recommendation engine."""

from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parents[2]))

from vehicle_assistant import RecommendationEngine, RecommendationRule


@pytest.mark.parametrize(
    ("event_state", "expected"),
    [
        (
            {
                "gear": "p",
                "passenger_front_door": "opening",
                "environment_puddle_nearby": True,
            },
            "副驾下车请注意脚下积水, 下车时观察周围环境以确保安全。",
        ),
        (
            {
                "gear": "N",
                "driver_door": "open",
                "environment_vehicles_passing": True,
            },
            "下车前请确认后方是否有来车, 建议开启盲区提醒或后视摄像头。",
        ),
    ],
)
def test_default_rules_cover_multiple_event_variants(event_state, expected):
    """Ensure each built-in rule fires for representative event combinations."""

    engine = RecommendationEngine()

    assert engine.recommend(event_state) == [expected]


def test_default_rule_matches_puddle_scenario():
    engine = RecommendationEngine()

    recommendations = engine.recommend(
        {
            "gear": "P",
            "passenger_front_door": "open",
            "environment_puddle_nearby": True,
        }
    )

    assert any("积水" in item for item in recommendations)


def test_puddle_scenario_returns_expected_text():
    """The real-world puddle case from the product discussion should pass."""

    engine = RecommendationEngine()

    recommendations = engine.recommend(
        {
            "gear": "P",
            "passenger_front_door": "open",
            "environment_puddle_nearby": True,
            # Extra keys that may appear in the real event payload.
            "driver_presence": "present",
            "time_of_day": "night",
        }
    )

    assert recommendations == [
        "副驾下车请注意脚下积水, 下车时观察周围环境以确保安全。"
    ]


def test_no_recommendation_when_state_does_not_match():
    """An unrelated event should not trigger any default recommendations."""

    engine = RecommendationEngine()

    assert engine.recommend({"gear": "D", "driver_door": "closed"}) == []


def test_custom_rule_can_be_added():
    engine = RecommendationEngine(rules=[])
    rule = RecommendationRule(
        name="seatbelt_warning",
        required_state={"speed": lambda value: value and value > 20},
        recommendation="当前车速超过 20km/h, 请确认所有乘员系好安全带。",
    )

    engine.add_rule(rule)

    recommendations = engine.recommend({"speed": 30})

    assert recommendations == ["当前车速超过 20km/h, 请确认所有乘员系好安全带。"]


def test_callable_requirement_gracefully_handles_missing_value():
    """Callable expectations should cope with absent keys without crashing."""

    rule = RecommendationRule(
        name="check_speed_threshold",
        required_state={"speed": lambda value: value and value > 20},
        recommendation="placeholder",
    )

    assert not rule.matches({})
