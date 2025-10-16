# Vehicle Assistant Recommendation Engine

本模块提供一个简单的基于规则的推理引擎, 用于根据车内外状态事件生成可推荐的功能或提示。当前实现旨在作为后续智能座舱功能推荐系统的初步雏形。

## 功能特性
- 使用 Python 实现的轻量级规则匹配。
- 支持将一组事件状态输入引擎, 输出匹配规则的推荐提示。
- 默认规则可以扩展, 也可以在初始化引擎时自定义。

## 快速开始
```python
from vehicle_assistant import RecommendationEngine

engine = RecommendationEngine()
recommendations = engine.recommend({
    "gear": "P",
    "passenger_front_door": "open",
    "environment_puddle_nearby": True,
})
for item in recommendations:
    print(item)
```

## 命令行使用

本项目内置了一个简单的 CLI, 便于在没有集成环境的情况下快速验证事件输入与推荐输出。安装依赖后可以直接运行:

```bash
python -m vehicle_assistant.cli --event gear=P passenger_front_door=open environment_puddle_nearby=true
```

或使用 JSON 字符串传入复杂事件:

```bash
python -m vehicle_assistant.cli --json '{"gear": "P", "passenger_front_door": "opening", "environment_puddle_nearby": true}'
```

当没有匹配到任何规则时, CLI 会输出 `暂无推荐。`。

## 目录结构
```
vehicle_assistant/
├── README.md              # 模块简介
├── __init__.py            # 包初始化, 暴露主要 API
├── engine.py              # 推荐引擎核心逻辑
├── rules.py               # 默认规则定义
└── tests/
    └── test_engine.py     # 针对推荐引擎的基础测试
```

## 开发计划
- 支持更复杂的事件条件组合(如范围、比较等)。
- 提供规则配置文件的加载与保存。
- 集成自然语言生成模块, 输出更加丰富的推荐描述。
```
