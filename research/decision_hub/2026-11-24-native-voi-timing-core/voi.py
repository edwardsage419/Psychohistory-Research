from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from math import comb, prod


type Q = Fraction
type Vector = tuple[Q, ...]
type Bounds = tuple[Q, Q]
type Plane = tuple[Vector, Q]
type Policy = tuple[int, ...]

ZERO = Fraction(0)
ONE = Fraction(1)
MAX_INTERSECTIONS = 100_000
MAX_POLICIES = 4_096
MAX_WORK = 400_000


class ScopeLimit(ValueError):
    """The exact finite problem is larger than the supported search scope."""


@dataclass(frozen=True)
class Problem:
    states: tuple[str, ...]
    signals: tuple[str, ...]
    options: tuple[str, ...]
    prior: tuple[Bounds, ...]
    likelihood: tuple[tuple[Bounds, ...], ...]
    utility: tuple[Vector, ...]
    actions: tuple[tuple[int, ...], ...]
    cost: Q

    @property
    def point(self) -> bool:
        return all(low == high for low, high in self.prior) and all(
            low == high for row in self.likelihood for low, high in row
        )

    @property
    def unrestricted(self) -> bool:
        return all(not row or len(row) == len(self.options) for row in self.actions)


@dataclass(frozen=True)
class Payoffs:
    mass: Vector
    baseline: Vector
    signals: tuple[Vector, ...]
    probability: Vector


def joint(prior: Vector, likelihood: tuple[Vector, ...]) -> Vector:
    return tuple(p * q for p, row in zip(prior, likelihood, strict=True) for q in row)


def payoffs(problem: Problem, mass: Vector) -> Payoffs:
    rows = tuple(zip(*(iter(mass),) * len(problem.signals), strict=True))
    signal = tuple(tuple(sum(m * utility[a] for m, utility in zip(column, problem.utility, strict=True))
                         for a in range(len(problem.options))) for column in zip(*rows, strict=True))
    return Payoffs(mass, tuple(map(sum, zip(*signal, strict=True))), signal,
                   tuple(map(sum, zip(*rows, strict=True))))


def winners(values: Vector, choices: tuple[int, ...]) -> tuple[int, ...]:
    best = max(values[index] for index in choices)
    return tuple(index for index in choices if values[index] == best)


def adaptive(problem: Problem, values: Payoffs) -> Q:
    return sum((max(row[index] for index in choices) for row, choices, probability in
                zip(values.signals, problem.actions, values.probability, strict=True) if probability), ZERO)


def policy_value(values: Payoffs, policy: Policy) -> Q:
    return sum((row[index] for row, index in zip(values.signals, policy, strict=True) if index >= 0), ZERO)


def net(problem: Problem, values: Payoffs, policy: Policy | None = None) -> Q:
    value = adaptive(problem, values) if policy is None else policy_value(values, policy)
    return value - problem.cost - max(values.baseline)


def point_world(problem: Problem) -> Vector:
    return joint(tuple(low for low, _ in problem.prior),
                 tuple(tuple(low for low, _ in row) for row in problem.likelihood))


def _row_vertices(bounds: tuple[Bounds, ...]) -> tuple[Vector, ...]:
    fixed = tuple(low for low, _ in bounds)
    changing = [i for i, (low, high) in enumerate(bounds) if low != high]
    if not changing:
        return (fixed,)
    if len(changing) * 2 ** (len(changing) - 1) > MAX_INTERSECTIONS:
        raise ScopeLimit('概率单纯形的端点枚举超出本方法的计算范围。')
    vertices = set()
    for free in changing:
        rest = [i for i in changing if i != free]
        for endpoint in product(*(bounds[i] for i in rest)):
            values = list(fixed)
            for i, value in zip(rest, endpoint, strict=True):
                values[i] = value
            values[free] = ONE - (sum(values) - values[free])
            if bounds[free][0] <= values[free] <= bounds[free][1]:
                vertices.add(tuple(values))
    return tuple(sorted(vertices))


def parameter_vertices(problem: Problem) -> tuple[tuple[Vector, ...], ...]:
    return (_row_vertices(problem.prior), *(_row_vertices(row) for row in problem.likelihood))


def fixed_search(problem: Problem) -> tuple[tuple[Vector, ...], ...]:
    policy_count = prod(len(row) or 1 for row in problem.actions)
    if policy_count > MAX_POLICIES:
        raise ScopeLimit('固定策略枚举超出本方法的计算范围。')
    vertices = parameter_vertices(problem)
    count = prod(map(len, vertices))
    if count * max(len(problem.states) * len(problem.signals) * len(problem.options), policy_count) > MAX_WORK:
        raise ScopeLimit('固定策略或联合参数端点枚举超出本方法的计算范围。')
    return vertices


def fixed_worlds(problem: Problem) -> tuple[Vector, ...]:
    vertices = fixed_search(problem)
    return tuple(dict.fromkeys(joint(prior, tuple(rows)) for prior, *rows in product(*vertices)))


def policies(problem: Problem) -> tuple[Policy, ...]:
    return tuple(product(*(row or (-1,) for row in problem.actions)))
