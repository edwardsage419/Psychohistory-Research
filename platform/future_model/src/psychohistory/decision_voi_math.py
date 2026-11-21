"""Exact finite expectation and polytope operations for investigation models."""

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


def _normalized(plane: Plane) -> Plane:
    coefficients, rhs = plane
    divisor = next(abs(value) for value in coefficients if value)
    return tuple(value / divisor for value in coefficients), rhs / divisor


def _canonical(plane: Plane) -> Plane:
    coefficients, rhs = _normalized(plane)
    if next(value for value in coefficients if value) < 0:
        return tuple(-value for value in coefficients), -rhs
    return coefficients, rhs


def _eliminate(rows: tuple[Plane, ...], dimension: int) -> tuple[list[list[Q]], list[int]]:
    matrix = [list(coefficients) + [rhs] for coefficients, rhs in rows]
    pivots = []
    for column in range(dimension):
        index = next((i for i in range(len(pivots), len(matrix)) if matrix[i][column]), None)
        if index is None:
            continue
        row = len(pivots)
        matrix[row], matrix[index] = matrix[index], matrix[row]
        divisor = matrix[row][column]
        matrix[row] = [value / divisor for value in matrix[row]]
        for i, equation in enumerate(matrix):
            if i != row and equation[column]:
                scale = equation[column]
                matrix[i] = [a - scale * b for a, b in zip(equation, matrix[row], strict=True)]
        pivots.append(column)
    return matrix, pivots


def _dot(coef: Vector, values: Vector) -> Q:
    return sum((a * b for a, b in zip(coef, values, strict=True)), ZERO)


def _constraints(problem: Problem) -> tuple[tuple[Plane, ...], tuple[Plane, ...]]:
    states, signals = len(problem.states), len(problem.signals)
    coordinates = tuple(product(range(states), range(signals)))
    equality = [(tuple(ONE for _ in coordinates), ONE)]
    inequalities = []
    for s, (low, high) in enumerate(problem.prior):
        incidence = tuple(ONE if r == s else ZERO for r, _ in coordinates)
        if low == high:
            equality.append((incidence, low))
        else:
            inequalities.extend(((incidence, high), (tuple(-x for x in incidence), -low)))
        for z, (q_low, q_high) in enumerate(problem.likelihood[s]):
            upper = tuple((ONE if c == z else ZERO) - q_high if r == s else ZERO for r, c in coordinates)
            if q_low == q_high:
                equality.append((upper, ZERO))
            else:
                lower = tuple(q_low - (ONE if c == z else ZERO) if r == s else ZERO for r, c in coordinates)
                inequalities.extend(((upper, ZERO), (lower, ZERO)))
    return tuple(equality), tuple(inequalities)


def _switches(problem: Problem, *, adaptive_policy: bool) -> tuple[Plane, ...]:
    coordinates = tuple(product(range(len(problem.states)), range(len(problem.signals))))
    baselines = [(tuple(problem.utility[s][a] - problem.utility[s][b] for s, _ in coordinates), ZERO)
                 for a, b in combinations(range(len(problem.options)), 2)]
    if not adaptive_policy:
        return tuple(baselines)
    signal_planes = [(tuple(problem.utility[s][a] - problem.utility[s][b] if c == z else ZERO
                           for s, c in coordinates), ZERO)
                     for z, actions in enumerate(problem.actions) for a, b in combinations(actions, 2)]
    return tuple(baselines + signal_planes)


@dataclass(frozen=True)
class Arrangement:
    """Reduce exact equations first, then intersect faces and switch planes."""

    offset: Vector
    basis: tuple[Vector, ...]
    inequalities: tuple[Plane, ...]
    faces: tuple[Plane, ...]

    def vertices(self) -> tuple[Vector, ...]:
        dimension = len(self.basis)
        if not dimension:
            return (self.offset,)
        coordinates = set()
        for active in combinations(self.faces, dimension):
            matrix, pivots = _eliminate(active, dimension)
            if len(pivots) != dimension:
                continue
            point = tuple(row[-1] for row in matrix)
            if all(_dot(coef, point) <= rhs for coef, rhs in self.inequalities):
                coordinates.add(tuple(value + sum(vector[i] * q for vector, q in zip(self.basis, point, strict=True))
                                      for i, value in enumerate(self.offset)))
        return tuple(sorted(coordinates))


def arrangement(problem: Problem, *, adaptive_policy: bool) -> Arrangement:
    dimension = len(problem.states) * len(problem.signals)
    # Bound matrix construction and projection before allocating dense constraint
    # or pairwise switch equations. Each nonconstant probability row has one sum constraint.
    free_dimension = sum(max(0, sum(low != high for low, high in row) - 1)
                         for row in (problem.prior, *problem.likelihood))
    constraint_count = 1 + 2 * (len(problem.states) + dimension)
    switch_count = comb(len(problem.options), 2)
    if adaptive_policy:
        switch_count += sum(comb(len(row), 2) for row in problem.actions)
    preparation = dimension * (constraint_count * dimension + switch_count * max(1, free_dimension))
    if preparation > MAX_WORK * 8:
        raise ScopeLimit('精确分段求界超出本方法的计算范围。')

    equalities, inequalities = _constraints(problem)
    matrix, pivots = _eliminate(equalities, dimension)
    free = [column for column in range(dimension) if column not in pivots]
    offset = [ZERO] * dimension
    for row, pivot in enumerate(pivots):
        offset[pivot] = matrix[row][-1]
    basis = []
    for column in free:
        coefficients = [ZERO] * dimension
        coefficients[column] = ONE
        for row, pivot in enumerate(pivots):
            coefficients[pivot] = -matrix[row][column]
        basis.append(tuple(coefficients))

    def reduced(planes: tuple[Plane, ...]):
        for coef, rhs in planes:
            projected = tuple(_dot(coef, vector) for vector in basis)
            if any(projected):
                yield projected, rhs - _dot(coef, tuple(offset))

    inequalities = tuple(dict.fromkeys(_normalized(plane) for plane in reduced(inequalities)))
    faces = tuple(dict.fromkeys(_canonical(plane) for plane in (*inequalities, *reduced(
        _switches(problem, adaptive_policy=adaptive_policy),
    ))))
    intersections = comb(len(faces), len(free))
    if intersections > MAX_INTERSECTIONS or intersections * len(free) * (len(free) ** 2 + len(inequalities)) > MAX_WORK * 8:
        raise ScopeLimit('精确分段求界超出本方法的计算范围。')
    return Arrangement(tuple(offset), tuple(basis), inequalities, faces)


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
