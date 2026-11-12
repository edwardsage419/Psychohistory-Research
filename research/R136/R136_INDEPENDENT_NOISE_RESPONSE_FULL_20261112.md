# R136 | Independent post-freeze exact noise-response curve (2026-11-12)

## Research status and strict scope

**Status:** COMPLETE, bounded theoretical exact-computation addendum; NO E2/E3 scientific promotion; GitHub archival to be verified separately.  
**Track:** R-series manual scientific execution, no workstream/automation/Codex instructions changed.  
**Starting main:** `33872eb515661039b981e21cf8de501321cad2f3` (as obtained after independent R134 addendum).  
**Original historical R136:** already CLOSED_BOUNDED as of 2026-10-20, with GitHub Actions run `39380956698`, 43 tests per Python job. The original source, published conclusion, pre-score rules, and original test receipt are unchanged. This addendum is a strictly separate mathematical sensitivity analysis.

Original pre-score freeze: `protocols/R136_PRESS_DYSON_2012_MEMORY_ONE_ZD_EXACT_STATIONARY_PRESCORE_FREEZE_2026-10-20.md`.  
Original final report: `research/R136/R136_PRESS_DYSON_2012_DIRECT_RECIPROCITY_EXACT_SCIENTIFIC_REPORT_2026-10-20.md`.

**Primary original reference:** William H. Press and Freeman J. Dyson (2012), *Iterated Prisoner's Dilemma contains strategies that dominate any evolutionary opponent*, PNAS 109(26), 10409–10413, DOI `10.1073/pnas.1206569109`. Read its first-party full-text page at https://pmc.ncbi.nlm.nih.gov/articles/PMC3387070/ on 2026-11-12, especially memory-one Markov matrix and stationary-vector discussion, Eq. (3)–(7), and extortion-type ZD score restriction. We use the original R136 frozen numerical strategy; no author human dataset or author evolutionary program is involved.

## Fixed artificial game and distinct new question

In X's CC,CD,DC,DD state ordering, X's base memory-one cooperation probabilities are `p = (4/5, 7/20, 7/20, 0)`, with extortion factor `chi=3` and `phi=1/20`. Y plays an independent fair coin on each step, `q=(1/2,1/2,1/2,1/2)`. Payoff vectors are `SX=(3,0,5,1)` and `SY=(3,5,0,1)`. These are the exact frozen original R136 witness settings.

Post-freeze supplementary question: How does a *single-sided*, independent action reversal rate `eta` in `[0,1/2]` change the long-run extortion identity? X's implemented memory-one probabilities are `p_i(eta)=eta+(1-2eta)*p_i`. We keep Y fair and hold all payoffs fixed, and suppose the expected long-run stationary score exists uniquely. This is a **hypothetical execution-error channel**, not measured error behavior. No model refitting or new frozen scoring rule is performed.

Because Y's action at each step is independent fair Bernoulli, the steady-state fraction `c` of X cooperating satisfies

`c = eta + (1-2eta) * [ (c/2)(p1+p2) + ((1-c)/2)(p3+p4) ]`

and hence algebraically

`c(eta)=(7+26*eta)/(24+32*eta)`.

The exact expected scores under this fixed fair-coin Y are

`sX(eta)=3-(3/2)*c(eta)` and `sY(eta)=1/2+(7/2)*c(eta)`.

Therefore the originally imposed ZD score identity residual is

`R(eta)=sX(eta)-1-3*[sY(eta)-1]=-25*eta/(3+4*eta)`.

This is exact for every eta in `[0,1/2]` under these artificial assumptions, not an interpolation of simulated samples. Its derivative is `R'(eta)=-75/(3+4*eta)^2`, so the residual strictly decreases for eta>0 and its slope at 0 is `-25/3`.

At eta=0, the exact original R136 result is recovered `sX=41/16`, `sY=73/48`, residual 0. At eta=1/20, it reproduces the previous frozen witness `sX=1287/512`, `sY=837/512`, residual `-25/64`. These two points are **old accepted results independently recovered**, while the general exact eta-dependence is this addendum's separate increment.

## Actual independent calculation and machine data

The new Python 3.13.5 standard-library script solves the **four-state** stationary equations `vM=v`, `sum(v)=1` with a generic rational Gauss-Jordan elimination matrix. That code independently computes the four state transition rows using every X state-specific noisy p and Y's fair q. It never imports or calls the independent scalar derived formula for computing the four-state stationary distribution. It then independently compares the stationary marginal `vCC+vCD`, both expected scores, their ZD residual and the explicit closed-form residual.

Evaluated 51 exact eta values `0,1/100,...,50/100`, and all 51 full-state-versus-reduced comparisons matched as exact `fractions.Fraction`, with no floating-point tolerance. Four `unittest` methods were run in ordinary Python and again with `python -O`; each mode passed 4/4 tests. All 51 calculated rows were independently re-run under optimization and serialized results were **byte-identical**. Validators use explicit `raise` statements rather than `assert`, so Python optimization cannot remove their acceptance checks.

| eta | P(X cooperates) | sX | sY | score-identity residual |
|---:|---:|---:|---:|---:|
| 0 | 7/24 | 41/16 | 73/48 | 0 |
| 1/100 | 363/1216 | 6207/2432 | 3757/2432 | -25/304 |
| 1/50 | 47/154 | 783/308 | 69/44 | -25/154 |
| 1/20 | 83/256 | 1287/512 | 837/512 | -25/64 |
| 1/10 | 6/17 | 42/17 | 59/34 | -25/34 |
| 1/4 | 27/64 | 303/128 | 253/128 | -25/16 |
| 1/2 | 1/2 | 9/4 | 9/4 | -5/2 |

**Read these as exact mathematical checks, not 51 human participants, 51 datasets, or 51 independent studies.** All points share one analytical model and one script implementation. The independent reduction and four-state solve provide a same-team computational cross-check, not external research-group reproduction.

## Scientific limitations and diagnostic controls

1. Source mechanism is Press–Dyson (2012) memory-one stationary scores; this supplementary two-route calculation fixes a *single fair Y opponent*. It makes no general claim about every possible opponent strategy, opponent adaptation, initial transient period, discounted or finite-horizon gains, or higher memory.
2. At zero noise, the original extortion identity holds under the original assumptions. Under the *particular* reversal channel, the same previously fixed p loses that exact identity for every eta>0. A designer could potentially choose another p for a known eta, or use error-correcting mechanisms; the present experiment does not test re-design feasibility.
3. Reconstructed R136 original epsilon=1/20 point matches historical result, so this addendum adds an *exact sensitivity curve*, not a new validation of human reciprocity or a correction to accepted R136 artifacts.
4. New evidence remains internal exact artificial **E1**; observed individual or animal E2 = 0; history E3 = 0; original-paper author numerical evolutionary calculation = NOT_RUN; actual external-team replication = NOT_RUN.
5. R073 and PESEN v0.1 freeze unchanged; all prior R136 archives and scored numerical outputs remain immutable. No other automation, Codex work, or concurrent PR file is touched.

**Runtime environment:** Python 3.13.5, stdlib `fractions`, `json`, `unittest`; no network calls or third-party packages.

**Executed commands:**

```bash
python r136_independent_noise_response_20261112.py --test
python -O r136_independent_noise_response_20261112.py --test
python r136_independent_noise_response_20261112.py > R136_INDEPENDENT_NOISE_RESPONSE_20261112.json
python -O r136_independent_noise_response_20261112.py > /tmp/r136_optimized.json
cmp R136_INDEPENDENT_NOISE_RESPONSE_20261112.json /tmp/r136_optimized.json
```

New script SHA256 `49cf66d5487d0096a6e739121dd89d9694359d1ae0ff4085bc29cedd0576bcb6`.  
New JSON SHA256 `a95f720b48446d88e77074f6b733dc2109cae7b09e60178efb3da8dde4ea8c41`.

No GitHub Actions initiated. Additional charges: NONE. GitHub Actions billing/CI quota was not independently audited; consequently no CI was triggered. Archival commit status should be determined from the actual repo remote readback, and is not itself mathematical evidence.

## Appendix A: Full executable independent code

```python
#!/usr/bin/env python3
"""Post-freeze R136 exact sensitivity: memory-one extortion vs fair-coin Y.

Independent four-state stationary solution compared with a two-state reduction.
Uses Python standard library only; changes no R136 frozen protocol.
"""
from fractions import Fraction as F
import json
import unittest

ONE, HALF = F(1), F(1, 2)
BASE_P = (F(4, 5), F(7, 20), F(7, 20), F(0))
Q_FAIR = (HALF, HALF, HALF, HALF)
SX = (F(3), F(0), F(5), F(1))
SY = (F(3), F(5), F(0), F(1))

def noisy_strategy(eta):
    if not (F(0) <= eta <= HALF):
        raise ValueError('noise must be in [0,1/2]')
    return tuple(eta + (ONE-2*eta)*p for p in BASE_P)

def stationary_by_4state(eta):
    p = noisy_strategy(eta)
    # X perspective CC,CD,DC,DD. Y always cooperates with probability 1/2.
    rows = []
    for a in p:
        rows.append((a*HALF, a*HALF, (ONE-a)*HALF, (ONE-a)*HALF))
    # Matrix equations from v M = v; replace last equation by sum(v)=1.
    aug = [[rows[j][i]-int(i==j) for j in range(4)] + [F(0)] for i in range(3)]
    aug.append([ONE,ONE,ONE,ONE,ONE])
    # Exact rational Gauss-Jordan elimination, with pivot choice independent
    # of any formula for the marginal cooperation probability.
    for col in range(4):
        pivot = next((r for r in range(col,4) if aug[r][col]), None)
        if pivot is None:
            raise ArithmeticError('nonunique stationary measure')
        aug[col], aug[pivot] = aug[pivot], aug[col]
        pivot_value = aug[col][col]
        aug[col] = [z/pivot_value for z in aug[col]]
        for row in range(4):
            if row != col:
                factor = aug[row][col]
                aug[row] = [u-factor*v for u,v in zip(aug[row],aug[col])]
    v = tuple(aug[i][-1] for i in range(4))
    if not (all(z >= 0 for z in v) and sum(v)==ONE):
        raise ArithmeticError('invalid stationary distribution')
    return v, sum(a*b for a,b in zip(v,SX)), sum(a*b for a,b in zip(v,SY))

def independent_closed_form(eta):
    # The Y action is independent of contemporaneous X action. The
    # stationary X cooperation fraction c follows a scalar recurrence.
    c = (7+26*eta)/(24+32*eta)
    sx, sy = F(3)-F(3,2)*c, HALF+F(7,2)*c
    return c, sx, sy, sx-ONE-3*(sy-ONE)

def run():
    selected = {0,1,2,5,10,25,50}
    display = []
    for i in range(51):
        eta = F(i,100)
        v,sx,sy = stationary_by_4state(eta)
        c,x,y,resid = independent_closed_form(eta)
        if c != v[0]+v[1]:
            raise ArithmeticError('stationary marginal mismatch')
        if (sx,sy) != (x,y):
            raise ArithmeticError('stationary payoff mismatch')
        if resid != sx-ONE-3*(sy-ONE):
            raise ArithmeticError('ZD residual mismatch')
        if resid != -25*eta/(3+4*eta):
            raise ArithmeticError('closed-form residual mismatch')
        if i in selected:
            display.append({'eta':str(eta),'cooperation_share':str(c),
                'score_X':str(sx),'score_Y':str(sy),'ZD_residual':str(resid)})
    return {'scope':'Post-freeze artificial R136 eta sensitivity with fixed fair opponent',
            'source':'Press & Dyson 2012 DOI 10.1073/pnas.1206569109',
            'evidence':'same-team independent mathematics E1; E2=0 E3=0',
            'tested_noise_grid':'eta=i/100, i=0..50',
            'exact_full_vs_reduced_stationary_checks':51,
            'closed_form':'c=(7+26eta)/(24+32eta); residual=-25eta/(3+4eta)',
            'sensitivity_at_zero':'d(residual)/deta = -25/3',
            'sampled':display}

class TestNoiseResponse(unittest.TestCase):
    def test_full_vs_reduced_51(self):
        self.assertEqual(run()['exact_full_vs_reduced_stationary_checks'],51)
    def test_frozen_old_point(self):
        _,x0,y0 = stationary_by_4state(F(0))
        self.assertEqual((x0,y0),(F(41,16),F(73,48)))
        _,x,y=stationary_by_4state(F(1,20))
        self.assertEqual((x,y), (F(1287,512), F(837,512)))
        self.assertEqual(x-1-3*(y-1),-F(25,64))
    def test_limit_and_invariant(self):
        self.assertEqual(independent_closed_form(F(0))[-1],F(0))
        self.assertEqual(independent_closed_form(HALF)[-1],-F(5,2))
        for i in range(1,51):
            self.assertLess(independent_closed_form(F(i,100))[-1],F(0))
    def test_reject_invalid_eta(self):
        for eta in (F(-1,100), F(51,100)):
            with self.assertRaises(ValueError):
                noisy_strategy(eta)

if __name__=='__main__':
    import sys
    if len(sys.argv)>1 and sys.argv[1]=='--test':
        unittest.main(argv=sys.argv[:1],verbosity=2)
    else:
        print(json.dumps(run(),indent=2))
```

## Appendix B: Full deterministic machine result

```json
{
  "scope": "Post-freeze artificial R136 eta sensitivity with fixed fair opponent",
  "source": "Press & Dyson 2012 DOI 10.1073/pnas.1206569109",
  "evidence": "same-team independent mathematics E1; E2=0 E3=0",
  "tested_noise_grid": "eta=i/100, i=0..50",
  "exact_full_vs_reduced_stationary_checks": 51,
  "closed_form": "c=(7+26eta)/(24+32eta); residual=-25eta/(3+4eta)",
  "sensitivity_at_zero": "d(residual)/deta = -25/3",
  "sampled": [
    {
      "eta": "0",
      "cooperation_share": "7/24",
      "score_X": "41/16",
      "score_Y": "73/48",
      "ZD_residual": "0"
    },
    {
      "eta": "1/100",
      "cooperation_share": "363/1216",
      "score_X": "6207/2432",
      "score_Y": "3757/2432",
      "ZD_residual": "-25/304"
    },
    {
      "eta": "1/50",
      "cooperation_share": "47/154",
      "score_X": "783/308",
      "score_Y": "69/44",
      "ZD_residual": "-25/154"
    },
    {
      "eta": "1/20",
      "cooperation_share": "83/256",
      "score_X": "1287/512",
      "score_Y": "837/512",
      "ZD_residual": "-25/64"
    },
    {
      "eta": "1/10",
      "cooperation_share": "6/17",
      "score_X": "42/17",
      "score_Y": "59/34",
      "ZD_residual": "-25/34"
    },
    {
      "eta": "1/4",
      "cooperation_share": "27/64",
      "score_X": "303/128",
      "score_Y": "253/128",
      "ZD_residual": "-25/16"
    },
    {
      "eta": "1/2",
      "cooperation_share": "1/2",
      "score_X": "9/4",
      "score_Y": "9/4",
      "ZD_residual": "-5/2"
    }
  ]
}
```
