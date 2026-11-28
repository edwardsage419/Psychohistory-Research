"""Version-pinned, explicitly registered personal decision methods."""
from collections.abc import Callable
from dataclasses import dataclass, field
import re
from typing import Any

from .decision_state import DecisionState, Option
from .plugins import Registry


@dataclass(frozen=True)
class Context:
    state: DecisionState
    feasible: tuple[Option, ...] = ()
    results: dict[str, dict[str, Any]] = field(default_factory=dict)


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

    depends_on: tuple[str, ...] = ()
    candidate_scope: str = "current"
    source_baseline: str = "5909e1ae58dbfcb0d14d00c0561726ecb35e1028"

    @property
    def key(self):
        return f"{self.model_id}@{self.version}"

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
            "source_baseline": self.source_baseline,
            **({"depends_on": self.depends_on} if self.depends_on else {}),
            **({"candidate_scope": self.candidate_scope} if self.candidate_scope != "current" else {}),
        }


class DecisionRegistry(Registry):
    def __init__(self):
        super().__init__()
        self._sealed = False

    def register(self, plugin):
        if self._sealed:
            raise ValueError("Active method releases are immutable")
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
        if plugin.candidate_scope not in {"current", "structural"}:
            raise ValueError("未知的候选方案范围")
        if not callable(plugin.validate) or not callable(plugin.execute):
            raise ValueError("方法需要验证及执行入口")
        if not re.fullmatch(r"[0-9a-f]{40}", plugin.source_baseline):
            raise ValueError("方法来源需要固定的提交身份")
        if len(set(plugin.depends_on)) != len(plugin.depends_on) or any(
            not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]{1,63}@[0-9]+\.[0-9]+\.[0-9]+", key)
            for key in plugin.depends_on
        ):
            raise ValueError("方法依赖需要唯一且固定的身份")
        super().register(plugin)

    def methods(self):
        return tuple(self._plugins.values())

    def for_release(self, manifest):
        """Select one reviewed exact version per family in a separate snapshot.

        Source pins identify the reviewed method. The caller must build the
        manifest from its trusted release configuration, never from a request.
        """
        from .decision_feasibility import GATE_ID

        selected = DecisionRegistry()
        families = set()
        for model_id, version, source in manifest:
            if model_id in families:
                raise ValueError("Only one active version per method family")
            method = self.get(model_id, version)
            if method.source_baseline != source:
                raise ValueError("Active method source differs from release manifest")
            selected.register(method)
            families.add(model_id)
        if (GATE_ID, "1.0.0") not in selected._plugins:
            raise ValueError("Active manifest must select the supported hard gate")
        selected.execution_order()
        selected._sealed = True
        return selected

    def execution_order(self):
        methods = {method.key: method for method in self.methods()}
        ordered, visiting, visited = [], set(), set()

        def visit(key):
            if key in visiting:
                raise ValueError("方法执行依赖存在循环")
            if key in visited or key not in methods:
                return
            visiting.add(key)
            method = methods[key]
            for dependency in method.depends_on:
                visit(dependency)
            visiting.remove(key)
            visited.add(key)
            ordered.append(method)

        for key in methods:
            visit(key)
        return ordered


def default_registry():
    from .decision_feasibility import METHOD
    from .decision_regret import METHODS as regret
    from .decision_scoring import METHODS as scoring

    registry = DecisionRegistry()
    for method in (METHOD, *scoring, *regret):
        registry.register(method)
    return registry
