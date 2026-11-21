"""Version-pinned, explicitly registered personal decision methods."""
from collections.abc import Callable
from dataclasses import dataclass
import re
from typing import Any

from .decision_state import DecisionState, Option
from .plugins import Registry


@dataclass(frozen=True)
class Context:
    state: DecisionState
    feasible: tuple[Option, ...] = ()


@dataclass(frozen=True)
class Method:
    model_id: str
    version: str
    title: str
    applicability: str | tuple[str, ...]
    inputs: str | tuple[str, ...]
    outputs: str | tuple[str, ...]
    units: str | tuple[str, ...]
    assumptions: str | tuple[str, ...]
    uncertainty: str | tuple[str, ...]
    sources: str | tuple[str, ...]
    failure_conditions: str | tuple[str, ...]
    replay: str | tuple[str, ...]
    baseline: str | tuple[str, ...]
    validate: Callable[[Context], list[str]]
    execute: Callable[[Context], dict[str, Any]]

    def describe(self):
        return {
            "model_id": self.model_id,
            "version": self.version,
            "title": self.title,
            "applicability": self.applicability,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "units": self.units,
            "assumptions": self.assumptions,
            "uncertainty": self.uncertainty,
            "sources": self.sources,
            "failure_conditions": self.failure_conditions,
            "replay": self.replay,
            "baseline": self.baseline,
            "evidence": "SYNTHETIC_ENGINEERING_CANDIDATE",
            "permissions": "本地计算。链接为项目研究记录。",
            "source_baseline": "5909e1ae58dbfcb0d14d00c0561726ecb35e1028",
        }


class DecisionRegistry(Registry):
    def register(self, plugin):
        if not isinstance(plugin, Method):
            raise ValueError("需要版本化的决策方法契约")
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]{1,63}", plugin.model_id):
            raise ValueError("无效的方法标识")
        if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", plugin.version):
            raise ValueError("需要固定的方法版本")
        for key, value in plugin.describe().items():
            if not value or not all(isinstance(item, str) and item.strip()
                                    for item in ((value,) if isinstance(value, str) else value)):
                raise ValueError(f"方法缺少元数据 {key}")
        if not callable(plugin.validate) or not callable(plugin.execute):
            raise ValueError("方法需要验证及执行入口")
        super().register(plugin)

    def methods(self):
        return tuple(self._plugins.values())


def default_registry():
    from .decision_feasibility import METHOD
    from .decision_regret import METHODS as regret
    from .decision_scoring import METHODS as scoring

    registry = DecisionRegistry()
    for method in (METHOD, *scoring, *regret):
        registry.register(method)
    return registry
