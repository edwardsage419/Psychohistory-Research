"""R153 bounded synthetic 2x2 spatial interaction experiment.

All real-valued 60 positive-support examples are synthetic E1 mathematical checks.
Only Python standard library required.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from typing import Sequence

ROW_PAIRS = ((3, 5), (4, 4), (6, 2))
COL_FIRST = (2, 3, 4, 5)
WEIGHTS = (
    ((1, 1), (1, 1)),
    ((2, 1), (1, 1)),
    ((1, 1), (1, 2)),
    ((2, 1), (1, 2)),
    ((1, 2), (2, 1)),
)
TOL = 1e-10


def _safe_number(z: object, label: str, allow_zero: bool = True) -> float:
    if isinstance(z, bool) or not isinstance(z, (int, float, Fraction)):
        raise ValueError(f"{label} must be numeric")
    v = float(z)
    if not math.isfinite(v) or v < 0 or (not allow_zero and v == 0):
        raise ValueError(f"{label} must be finite and {'nonnegative' if allow_zero else 'positive'}")
    return v


def _validated(rows: Sequence[object], cols: Sequence[object],
               weights: Sequence[Sequence[object]], positive: bool = True):
    if len(rows) != 2 or len(cols) != 2 or len(weights) != 2 or any(len(w) != 2 for w in weights):
        raise ValueError("all inputs must have exactly 2 rows/columns")
    r = tuple(_safe_number(x, "row", False) for x in rows)
    c = tuple(_safe_number(x, "column", False) for x in cols)
    w = tuple(tuple(_safe_number(x, "weight", not positive) for x in rr) for rr in weights)
    if abs(sum(r) - sum(c)) > 1e-12:
        raise ValueError("row and column totals must match")
    if not any(w[0]) or not any(w[1]) or not any(row[j] for row in w for j in [0]):
        raise ValueError("unsupported row/column")
    if w[0][1] == 0 and w[1][1] == 0:
        raise ValueError("unsupported row/column")
    return r, c, w


def origin_only(rows: Sequence[object], weights: Sequence[Sequence[object]]) -> tuple[tuple[float, ...], ...]:
    if len(rows) != 2 or len(weights) != 2 or any(len(v) != 2 for v in weights):
        raise ValueError("must be 2x2")
    r = tuple(_safe_number(z, "row", False) for z in rows)
    w = tuple(tuple(_safe_number(v, "weight") for v in z) for z in weights)
    if any(sum(q) <= 0 for q in w):
        raise ValueError("zero origin support")
    return tuple(tuple(r[i] * w[i][j] / sum(w[i]) for j in range(2)) for i in range(2))


def support_interval(rows: Sequence[object], cols: Sequence[object],
                     weights: Sequence[Sequence[object]]):
    """Exact support-constrained interval for x=T00, with Fraction budgets."""
    if len(rows) != 2 or len(cols) != 2 or len(weights) != 2 or any(len(w) != 2 for w in weights):
        raise ValueError("2x2 input required")
    if any(isinstance(v, bool) or not isinstance(v, (int, Fraction)) for v in (*rows, *cols)):
        raise ValueError("integer or Fraction budgets required for exact support")
    a, b = map(Fraction, rows)
    c, d = map(Fraction, cols)
    if min(a, b, c, d) < 0 or a + b != c + d:
        raise ValueError("invalid budgets")
    mask = tuple(tuple(_safe_number(v, "weight") > 0 for v in row) for row in weights)
    lo, hi = max(Fraction(0), c-b), min(a, c)
    # Each structural zero fixes x to an exact value.
    required = []
    if not mask[0][0]: required.append(Fraction(0))
    if not mask[0][1]: required.append(a)
    if not mask[1][0]: required.append(c)
    if not mask[1][1]: required.append(c-b)
    if required:
        if len(set(required)) > 1:
            raise ValueError("infeasible structural support")
        lo = max(lo, required[0]); hi = min(hi, required[0])
    if lo > hi:
        raise ValueError("infeasible marginal/support constraints")
    return lo, hi


def solve_scalar(rows: Sequence[object], cols: Sequence[object],
                 weights: Sequence[Sequence[object]]) -> tuple[tuple[float, ...], ...]:
    """Independent 2x2 cross-product solution via a monotone scalar root."""
    r, c, w = _validated(rows, cols, weights, positive=False)
    # Support admissibility uses the exact parameterization for positive integer budgets.
    a, b = r
    p, q = c
    lo, hi = max(0.0, p-b), min(a, p)
    forced = []
    if w[0][0] == 0: forced.append(0.0)
    if w[0][1] == 0: forced.append(a)
    if w[1][0] == 0: forced.append(p)
    if w[1][1] == 0: forced.append(p-b)
    if forced:
        if max(forced)-min(forced) > 1e-12 or not(lo-1e-12 <= forced[0] <= hi+1e-12):
            raise ValueError("infeasible structural support")
        x = forced[0]
    else:
        # Positive support: solve T00*T11*w01*w10 = T01*T10*w00*w11.
        def residual(x0: float) -> float:
            return x0*(b-p+x0)*w[0][1]*w[1][0] - (a-x0)*(p-x0)*w[0][0]*w[1][1]
        for _ in range(90):
            mid=(lo+hi)/2.0
            if residual(mid) > 0:
                hi=mid
            else:
                lo=mid
        x=(lo+hi)/2.0
    table=((x,a-x),(p-x,b-p+x))
    if min(v for row in table for v in row) < -1e-9:
        raise AssertionError("negative output from scalar method")
    return table


def solve_ipf(rows: Sequence[object], cols: Sequence[object],
              weights: Sequence[Sequence[object]], tol: float = TOL,
              max_iterations: int = 30000) -> tuple[tuple[float, ...], ...]:
    """Independent alternating row-column proportional fitting, full positive support."""
    r, c, w = _validated(rows, cols, weights, positive=True)
    t = [list(w[0]), list(w[1])]
    for _ in range(max_iterations):
        for i in range(2):
            m = r[i] / sum(t[i])
            for j in range(2): t[i][j] *= m
        for j in range(2):
            m = c[j] / (t[0][j]+t[1][j])
            for i in range(2): t[i][j] *= m
        if max(abs(sum(t[i])-r[i]) for i in range(2)) < tol:
            return tuple(tuple(v for v in row) for row in t)
    raise RuntimeError("IPF did not converge")


def _round_table(t):
    return [[round(float(v), 12) for v in row] for row in t]


def scenario_results():
    """Deterministic JSON-serializable full 60-case ledger."""
    outputs=[]
    for ri, rows in enumerate(ROW_PAIRS):
        for ci, first in enumerate(COL_FIRST):
            cols=(first,8-first)
            for wi, w in enumerate(WEIGHTS):
                scalar=solve_scalar(rows,cols,w)
                ipf=solve_ipf(rows,cols,w)
                origin=origin_only(rows,w)
                discrepancy=max(abs(scalar[i][j]-ipf[i][j]) for i in range(2) for j in range(2))
                if discrepancy >= 1e-9:
                    raise AssertionError("independent solvers disagree")
                row_errors=[abs(sum(ipf[i])-rows[i]) for i in range(2)]
                col_errors=[abs(sum(ipf[i][j] for i in range(2))-cols[j]) for j in range(2)]
                if max(row_errors+col_errors)>=1e-9:
                    raise AssertionError("marginals incorrect")
                outputs.append({
                    "case_id":f"r{ri}_c{ci}_w{wi}", "rows":list(rows),"columns":list(cols),
                    "weights":[list(rr) for rr in w],
                    "origin_only":_round_table(origin), "origin_only_columns":
                    [round(sum(origin[i][j] for i in range(2)), 12) for j in range(2)],
                    "doubly_constrained":_round_table(ipf),
                    "independent_scalar":_round_table(scalar),
                    "solver_max_abs_discrepancy":round(discrepancy,14),
                    "max_abs_margin_error":round(max(row_errors+col_errors),14),
                })
    if len(outputs)!=60 or len(set(t['case_id'] for t in outputs))!=60:
        raise AssertionError("scenario count")
    return {"project":"Psychohistory R153", "evidence_level":"E1_SYNTHETIC_ONLY",
            "frozen_scenarios":60,"results":outputs,
            "exact_uniform_benchmark":{"rows":[3,5],"columns":[2,6],
             "cells":[[str(Fraction(r*c,8)) for c in (2,6)] for r in (3,5)]},
            "structural_zero":{"rows":[3,5],"columns":[4,4],
             "weight_mask":[[0,1],[1,1]],"unique_feasible_matrix":[[0,3],[4,1]]}}


def main():
    print(json.dumps(scenario_results(),ensure_ascii=False,sort_keys=True,indent=2))


if __name__ == "__main__":
    main()
