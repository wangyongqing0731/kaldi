"""Command-line interface for the vehicle assistant recommendation engine."""

from __future__ import annotations

import argparse
import json
from typing import Dict, Iterable, List

from .engine import RecommendationEngine


def _coerce_value(value: str) -> object:
    """Convert string inputs into Python primitives when possible."""

    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False

    try:
        if value.startswith("0") and value != "0":
            raise ValueError
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        return value


def _parse_event_pairs(pairs: Iterable[str]) -> Dict[str, object]:
    """Turn key=value CLI arguments into an event state dictionary."""

    event_state: Dict[str, object] = {}
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"事件参数需要使用 key=value 形式, 当前输入: '{pair}'")
        key, value = pair.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"事件键名不能为空: '{pair}'")
        event_state[key] = _coerce_value(value.strip())
    return event_state


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="车辆场景推荐引擎 CLI")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--json",
        help="使用 JSON 字符串传入事件状态, 例如 '{\"gear\": \"P\"}'",
    )
    group.add_argument(
        "--event",
        nargs="+",
        metavar="KEY=VALUE",
        help="使用若干 key=value 对描述事件状态",
    )
    return parser


def _load_event_state(args: argparse.Namespace) -> Dict[str, object]:
    if getattr(args, "json", None):
        try:
            event_state = json.loads(args.json)
        except json.JSONDecodeError as exc:
            raise ValueError(f"无法解析 JSON: {exc.msg}") from exc
        if not isinstance(event_state, dict):
            raise ValueError("JSON 输入必须是对象类型, 例如 {'gear': 'P'}。")
        return event_state

    try:
        return _parse_event_pairs(args.event or [])
    except ValueError as exc:
        raise ValueError(str(exc)) from exc


def main(argv: List[str] | None = None) -> int:
    """Entrypoint used by ``python -m vehicle_assistant.cli``."""

    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        event_state = _load_event_state(args)
    except ValueError as exc:
        parser.error(str(exc))

    engine = RecommendationEngine()
    recommendations = engine.recommend(event_state)

    if not recommendations:
        print("暂无推荐。")
        return 0

    for item in recommendations:
        print(f"- {item}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
