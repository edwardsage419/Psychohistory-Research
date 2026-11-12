# R134 | independent post-freeze coupling sensitivity audit

Date: 2026-11-12 Asia/Taipei  
Track: R-series manual scientific execution  
Status: COMPLETE for the bounded independent mathematical audit; archival commit verified separately  
Scope: New supplementary mathematical sensitivity, **not** a change to the 2026-10-20 frozen R134 protocol, original results, or scientific grade.

## Authenticated research starting point

Repository: `edwardsage419/Psychohistory-Research`  
Observed `main`: `d4740c2cd999b8da06a25b0ef407aeaf8a56ab6c`  
Original frozen protocol: `protocols/R134_TAYLOR_1979_MULTIPOP_ESS_REPLICATOR_EXACT_PRESCORE_FREEZE_2026-10-20.md`  
Original bounded acceptance: `research/R134/R134_FINAL_ACCEPTANCE_STATUS.json`  
Original 34992 source-vs-expansion checks and original 45-test CI remain historical, unaltered.

Primary source: Peter D. Taylor (1979), *Evolutionarily Stable Strategies with Two Types of Player*, *Journal of Applied Probability* 16(1):76–83, DOI: `10.2307/3213376`. Original page 77 Eq. (1), page 78 Eq. (2)–(5), checked by direct PDF page view on 2026-11-12:  
https://static1.squarespace.com/static/5dc9917c4cdb1467e1e54c4c/t/6526a06fa3fe7456d63dd68d/1697030256664/1979%2Bevolutionarily%2Bstable%2Bstrategies%2Bwith%2Btwo%2Btypes%2Bof%2Bplayer.pdf

## Explicit model scope and mechanism

This is a newly explored **artificial** one-parameter family under Taylor's original *linear* two-population fitness and simultaneous invasion definition. No observed data or author experimental parameters are inferred.

A = D = [[0, 1], [1, 0]], B = C = k I_2. The two-population resident is p=q=(1/2,1/2). A mutant changes the two population strategy-1 shares by (a,b), with |a|,|b| <= 1/2 and (a,b) != (0,0). The mutant mixture is p_e=(1-e)p+e r, q_e=(1-e)q+e s, as in original Eq. (1).

For this resident, the first-order fitness difference D0 vanishes. Independent expansion of the block quadratic gives

`Q(k,a,b) = -2(a²+b²) + 4kab`,

and the resident-minus-mutant total fitness advantage is **exactly**

`D(e) = -e Q(k,a,b)`.

A strict ESS requires Q<0 for every nonzero feasible direction. The quadratic form has eigenvalues `-2+2k` and `-2-2k`, so the following are **global, analytical results within this artificial family**:

* |k| < 1: Q strictly negative, so this interior resident is a strict ESS.
* |k| = 1: Q has a zero direction; strict inequality fails, so the resident is not a strict ESS.
* |k| > 1: some simultaneous mutant direction has Q positive and invades at all positive e; the resident is not an ESS.
* Single-population mutant directions (a,0) and (0,b) have Q<0 for every k when the nonzero displacement is feasible. Thus unilateral resistance alone does not certify joint ESS.

From Taylor's Eq. (5), the two shares obey

`dx/dt = x(1-x)[1-2x+k(2y-1)]`  
`dy/dt = y(1-y)[1-2y+k(2x-1)]`.

At (1/2,1/2), `J = [[-1/2,k/2],[k/2,-1/2]]`; eigenvalues `(-1+k)/2` and `(-1-k)/2`. Consequently |k|<1 yields local linear attraction, |k|>1 a saddle, and |k|=1 a zero eigenvalue. At critical |k|=1 the specific diagonal/anti-diagonal continuum of stationary points can be checked directly from the exact vector field. A zero linear eigenvalue alone is not a universal nonlinear-stability conclusion.

For original R134 k=2, this exact algebra reproduces Q(1/4,1/4)=1/4, D(1/4)=-1/16 and the Jacobian eigenvalues 1/2 and -3/2. New k-sensitivity is post-freeze; it does not retroactively extend the original accepted pre-score grid.

## Actually executed independent calculations

Python standard-library `fractions.Fraction`, Python 3.13.5. Seven k values `-2,-1,-1/2,0,1/2,1,2`. Each k used the 17×17 grid of a,b in {-8/16,...,8/16}, excluding (0,0), giving 288 feasible mutant directions. Each direction was evaluated at e = 1/8,1/4,1/2. The 6048 direct original-Eq.1 fitness differences exactly matched the separately implemented quadratic expansion in every case.

| k | Q<0 | Q=0 | Q>0 | Linear dynamics |
|---|---:|---:|---:|---|
| -2 | 184 | 0 | 104 | saddle |
| -1 | 272 | 16 | 0 | zero-eigenvalue |
| -1/2 | 288 | 0 | 0 | stable |
| 0 | 288 | 0 | 0 | stable |
| 1/2 | 288 | 0 | 0 | stable |
| 1 | 272 | 16 | 0 | zero-eigenvalue |
| 2 | 184 | 0 | 104 | saddle |

**Interpretation:** each table cell is a count of *artificial perturbation directions*, not participant observations, datasets, independent studies or forecast scores. The 104/288 positive-Q directions at k=±2 are specific to this fixed lattice; the analytical threshold itself is not a grid estimate. The primary k=2 study remains E1.

Additional direct checks: exact center Jacobian from two different finite central-difference grids with cubic-error Richardson elimination; exact eigenvectors and eigenvalues; original k=2 single/joint mutant numerical identities; the k=±1 zero-advantage mutants. Four distinct Python `unittest` methods completed with no failures.

## Self-corrected test-design issue in this new audit

The first local test run failed two checks because a single nonzero finite central-difference step was incorrectly treated as an exact derivative of a cubic replicator field. This was **a defect in this newly written diagnostic**, not an observed defect in original R134. A second independent central-difference step was used to eliminate the cubic truncation term algebraically via `(4 D(h/2)-D(h))/3`. The revised run passed 4/4 tests and all 6048 exact comparisons. The failed initial output was inspected and is described here; no historical R134 accepted artifact was modified.

## Reproducibility, evidence and limits

Executed source and numerical JSON are embedded in the appendices of this same self-contained supplementary archive. Local development copies are also available in the execution environment; historical R134 sources remain intact.

Local code SHA256: `0f298296f8a3f39753cf219b677d60225fa8e28af359edaa6ba05eb8a30a04dc`  
Local JSON SHA256: `0c3a3b1e804f3061d36025aa12d32c914be78a3631a7f3a70d8d3d2d0cd0c909`  

Executed commands:

```shell
python3 r134_independent_coupling_sensitivity_20261112.py --test
python3 r134_independent_coupling_sensitivity_20261112.py
```

R073 and PESEN v0.1 frozen state unchanged. New human/animal behavior E2 = 0, historical forecasting E3 = 0, outside-team reproduction = 0. Original paper's nonlinear parental-care model was not evaluated. Independent computational rederivation is same-team internal replication, not external independent replication. Do not treat a linearization as a claim about realistic social populations.

GitHub Actions: **NOT_RUN** (no new CI). No fees initiated. No changes to original artifacts, frozen protocol, workflow prompts, or Codex branches.

## Next scientific check

Within R134, a separate bounded extension could test unequal mutant invasion fractions or nonlinear fitness only after explicitly defining scope, while keeping the original Taylor Eq. (1) acceptance unchanged. Across the formal R sequence, prioritize a different pending item with a verified first-party source and no active competing PR.

## Appendix A: executable independent Python3 source

Save the exact fenced source as `r134_independent_coupling_sensitivity_20261112.py`.

```python
#!/usr/bin/env python3
"""R134 post-freeze, independent exact two-population sensitivity audit.

Standard-library only. No modification of the 2026-10-20 frozen protocol.
This explores a new artificial cross-population coupling parameter k.
"""
from fractions import Fraction as F
from itertools import product
import json
import unittest

HALF = F(1, 2)
K_VALUES = tuple(F(s) for s in ("-2", "-1", "-1/2", "0", "1/2", "1", "2"))
EPS_VALUES = (F(1, 8), F(1, 4), F(1, 2))
OFFSETS = tuple(F(i, 16) for i in range(-8, 9))
DIRECTIONS = tuple((a, b) for a, b in product(OFFSETS, repeat=2) if a or b)

def matrix_vec(mat, v):
    return tuple(sum((cell * z for cell, z in zip(row, v)), F(0)) for row in mat)

def dot(a, b):
    return sum((u * v for u, v in zip(a, b)), F(0))

def direct_resident_advantage(k, a, b, epsilon):
    """Independent literal Eq. 1 route: fitness evaluated at mutant mixture."""
    A = ((F(0), F(1)), (F(1), F(0)))
    D = A
    B = ((k, F(0)), (F(0), k))
    C = B
    p = q = (HALF, HALF)
    r, s = (HALF + a, HALF - a), (HALF + b, HALF - b)
    mixed_p = tuple((1 - epsilon) * u + epsilon * v for u, v in zip(p, r))
    mixed_q = tuple((1 - epsilon) * u + epsilon * v for u, v in zip(q, s))
    Ap, Bq = matrix_vec(A, mixed_p), matrix_vec(B, mixed_q)
    Cp, Dq = matrix_vec(C, mixed_p), matrix_vec(D, mixed_q)
    f = tuple(u + v for u, v in zip(Ap, Bq))
    g = tuple(u + v for u, v in zip(Cp, Dq))
    return dot(p, f) + dot(q, g) - dot(r, f) - dot(s, g)

def quadratic_Q(k, a, b):
    """Independently expanded Eq. 4 quadratic along simplex tangent."""
    return -2 * (a * a + b * b) + 4 * k * a * b

def dynamics(k, x, y):
    """One-dimensional simplification of Eq. 5, independently coded."""
    return (x * (1 - x) * (1 - 2*x + k*(2*y-1)),
            y * (1 - y) * (1 - 2*y + k*(2*x-1)))

def jacobian_at_center(k):
    """Exact center derivative from two central differences of the cubic vector field.

    Each central slope is J + c*h**2; Richardson cancels the cubic term.
    """
    def central_slopes(h):
        fp, fm = dynamics(k, HALF+h, HALF), dynamics(k, HALF-h, HALF)
        gp, gm = dynamics(k, HALF, HALF+h), dynamics(k, HALF, HALF-h)
        return (((fp[0]-fm[0])/(2*h), (gp[0]-gm[0])/(2*h)),
                ((fp[1]-fm[1])/(2*h), (gp[1]-gm[1])/(2*h)))
    d1, d2 = central_slopes(F(1, 16)), central_slopes(F(1, 32))
    return tuple(tuple((4*d2[i][j]-d1[i][j])/3 for j in range(2)) for i in range(2))

def run_exact_grid():
    rows = []
    n_checks = 0
    for k in K_VALUES:
        counts = {"Q_negative": 0, "Q_zero": 0, "Q_positive": 0}
        for a, b in DIRECTIONS:
            q = quadratic_Q(k, a, b)
            counts["Q_negative" if q < 0 else ("Q_positive" if q > 0 else "Q_zero")] += 1
            # Three truly independent direct evaluations of the source fitness.
            for epsilon in EPS_VALUES:
                observed = direct_resident_advantage(k, a, b, epsilon)
                expected = -epsilon * q
                if observed != expected:
                    raise AssertionError((k, a, b, epsilon, observed, expected))
                n_checks += 1
        if sum(counts.values()) != len(DIRECTIONS):
            raise AssertionError("grid count mismatch")
        j = jacobian_at_center(k)
        expected_j = ((-HALF, k/2), (k/2, -HALF))
        if j != expected_j:
            raise AssertionError(("Jacobian", k, j, expected_j))
        rows.append({
            "cross_coupling_k": str(k),
            **counts,
            "positive_linear_eigenvalue": str((-1 + abs(k))/2),
            "strict_interior_ESS": abs(k) < 1,
            "local_linear_type": "stable" if abs(k)<1 else ("zero-eigenvalue" if abs(k)==1 else "saddle")
        })
    return {
        "study": "R134 supplementary post-freeze sensitivity, no old-score replacement",
        "source": "Taylor 1979 DOI:10.2307/3213376 printed pp.77-78 Eq.1 and Eq.5",
        "evidence_class": "artificial exact mathematical E1, no observational E2/E3",
        "k_values": [str(k) for k in K_VALUES],
        "eps_values": [str(e) for e in EPS_VALUES],
        "offset_grid": "integer [-8,8]/16 per population, excluding a=b=0",
        "directions_per_k": len(DIRECTIONS),
        "exact_direct_vs_expanded_checks": n_checks,
        "checks_per_k": len(DIRECTIONS)*len(EPS_VALUES),
        "results": rows
    }

class Audits(unittest.TestCase):
    def test_all_direct_source_expansion_checks(self):
        self.assertEqual(run_exact_grid()["exact_direct_vs_expanded_checks"], 6048)

    def test_original_k_two_counterexamples(self):
        k = F(2)
        self.assertEqual(quadratic_Q(k, F(1,4), F(1,4)), F(1,4))
        self.assertEqual(direct_resident_advantage(k, F(1,4), F(1,4), F(1,4)), -F(1,16))
        self.assertEqual(quadratic_Q(k, F(1,4), F(0)), -F(1,8))

    def test_critical_k_one_non_strict(self):
        self.assertEqual(direct_resident_advantage(F(1), F(1,4), F(1,4), F(1,2)), F(0))
        self.assertEqual(direct_resident_advantage(F(-1), F(1,4), -F(1,4), F(1,2)), F(0))

    def test_jacobian_eigenspaces(self):
        for k in K_VALUES:
            J = jacobian_at_center(k)
            for (a,b), eigenvalue in (((F(1), F(1)),(k-1)/2),
                                      ((F(1),-F(1)),(-k-1)/2)):
                self.assertEqual(J[0][0]*a+J[0][1]*b, eigenvalue*a)
                self.assertEqual(J[1][0]*a+J[1][1]*b, eigenvalue*b)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        unittest.main(argv=sys.argv[:1], verbosity=2)
    else:
        print(json.dumps(run_exact_grid(), ensure_ascii=False, indent=2))
```

## Appendix B: exact machine-readable output

```json
{
  "study": "R134 supplementary post-freeze sensitivity, no old-score replacement",
  "source": "Taylor 1979 DOI:10.2307/3213376 printed pp.77-78 Eq.1 and Eq.5",
  "evidence_class": "artificial exact mathematical E1, no observational E2/E3",
  "k_values": [
    "-2",
    "-1",
    "-1/2",
    "0",
    "1/2",
    "1",
    "2"
  ],
  "eps_values": [
    "1/8",
    "1/4",
    "1/2"
  ],
  "offset_grid": "integer [-8,8]/16 per population, excluding a=b=0",
  "directions_per_k": 288,
  "exact_direct_vs_expanded_checks": 6048,
  "checks_per_k": 864,
  "results": [
    {
      "cross_coupling_k": "-2",
      "Q_negative": 184,
      "Q_zero": 0,
      "Q_positive": 104,
      "positive_linear_eigenvalue": "1/2",
      "strict_interior_ESS": false,
      "local_linear_type": "saddle"
    },
    {
      "cross_coupling_k": "-1",
      "Q_negative": 272,
      "Q_zero": 16,
      "Q_positive": 0,
      "positive_linear_eigenvalue": "0",
      "strict_interior_ESS": false,
      "local_linear_type": "zero-eigenvalue"
    },
    {
      "cross_coupling_k": "-1/2",
      "Q_negative": 288,
      "Q_zero": 0,
      "Q_positive": 0,
      "positive_linear_eigenvalue": "-1/4",
      "strict_interior_ESS": true,
      "local_linear_type": "stable"
    },
    {
      "cross_coupling_k": "0",
      "Q_negative": 288,
      "Q_zero": 0,
      "Q_positive": 0,
      "positive_linear_eigenvalue": "-1/2",
      "strict_interior_ESS": true,
      "local_linear_type": "stable"
    },
    {
      "cross_coupling_k": "1/2",
      "Q_negative": 288,
      "Q_zero": 0,
      "Q_positive": 0,
      "positive_linear_eigenvalue": "-1/4",
      "strict_interior_ESS": true,
      "local_linear_type": "stable"
    },
    {
      "cross_coupling_k": "1",
      "Q_negative": 272,
      "Q_zero": 16,
      "Q_positive": 0,
      "positive_linear_eigenvalue": "0",
      "strict_interior_ESS": false,
      "local_linear_type": "zero-eigenvalue"
    },
    {
      "cross_coupling_k": "2",
      "Q_negative": 184,
      "Q_zero": 0,
      "Q_positive": 104,
      "positive_linear_eigenvalue": "1/2",
      "strict_interior_ESS": false,
      "local_linear_type": "saddle"
    }
  ]
}
```