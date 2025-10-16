"""Default rules for the vehicle assistant recommendation engine."""

from __future__ import annotations

from typing import List

from .engine import RecommendationRule

DEFAULT_RULES: List[RecommendationRule] = [
    RecommendationRule(
        name="park_with_puddle",
        required_state={
            "gear": {"P", "p"},
            "passenger_front_door": {"open", "opening"},
            "environment_puddle_nearby": True,
        },
        recommendation="副驾下车请注意脚下积水, 下车时观察周围环境以确保安全。",
        tags=["safety", "environment"],
    ),
    RecommendationRule(
        name="park_with_traffic",
        required_state={
            "gear": {"P", "N"},
            "driver_door": {"open", "opening"},
            "environment_vehicles_passing": True,
        },
        recommendation="下车前请确认后方是否有来车, 建议开启盲区提醒或后视摄像头。",
        tags=["safety", "traffic"],
    ),
]
"""List of baseline rules used by :class:`vehicle_assistant.engine.RecommendationEngine`."""
