"""Core recommendation engine for vehicle assistant."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class RecommendationRule:
    """A rule that turns a matching event state into a recommendation."""

    name: str
    required_state: Dict[str, object]
    recommendation: str
    tags: List[str] = field(default_factory=list)

    def matches(self, event_state: Dict[str, object]) -> bool:
        """Return True if the event_state satisfies the rule's requirements."""
        for key, expected_value in self.required_state.items():
            if callable(expected_value):
                if not expected_value(event_state.get(key)):
                    return False
            elif isinstance(expected_value, Iterable) and not isinstance(expected_value, (str, bytes)):
                if event_state.get(key) not in expected_value:
                    return False
            else:
                if event_state.get(key) != expected_value:
                    return False
        return True


class RecommendationEngine:
    """Simple rule-based recommendation engine for in-vehicle events."""

    def __init__(self, rules: Optional[Iterable[RecommendationRule]] = None):
        self._rules: List[RecommendationRule] = list(rules) if rules is not None else []
        if rules is None:
            self._load_default_rules()

    def _load_default_rules(self) -> None:
        """Populate engine with baseline rules that demonstrate the concept."""
        from .rules import DEFAULT_RULES

        self._rules.extend(DEFAULT_RULES)

    @property
    def rules(self) -> List[RecommendationRule]:
        """Return a copy of the currently configured rules."""
        return list(self._rules)

    def add_rule(self, rule: RecommendationRule) -> None:
        """Add a new rule to the engine."""
        self._rules.append(rule)

    def recommend(self, event_state: Dict[str, object]) -> List[str]:
        """Return recommendations for a given event_state."""
        recommendations: List[str] = []
        for rule in self._rules:
            if rule.matches(event_state):
                recommendations.append(rule.recommendation)
        return recommendations
