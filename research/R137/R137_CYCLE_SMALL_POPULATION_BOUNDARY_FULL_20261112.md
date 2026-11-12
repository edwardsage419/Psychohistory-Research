# R137 | Post-freeze exact small-cycle boundary audit: C3 and C4

Research date: 2026-11-12, Asia/Taipei.  
Status: **COMPLETE as a bounded new exact-mathematics E1 addendum**. Repository commit status to be verified independently.  
Research track: manual R-series scientific execution. No modification of existing freezes, authorship, source licenses, automated workflows, Codex A/B, or ongoing PR branches.

## Source provenance and immutable research baseline

Repository `edwardsage419/Psychohistory-Research`, observed `main` at the start of this independent audit: `f3313ab8ae8276491c67e114e5a2bc1d18e64da7`.

Historical R137 freeze: `protocols/R137_OHTSUKI_2006_FINITE_WEAK_SELECTION_GRAPH_FIXATION_PROTOCOL_2026-10-20.md`, as accepted 2026-10-20. Prior accepted graph family C5, C6, C7, C8, C9 and complete graph K4. Original exact 40-unit-test code and CI evidence are preserved and have NOT been changed. Historical R137 E2/E3 remain zero.

Original first-party theory: H. Ohtsuki, C. Hauert, E. Lieberman, M. A. Nowak (2006), *A simple rule for the evolution of cooperation on graphs and social networks*, Nature 441, 502–505, DOI 10.1038/nature04605; full original author manuscript directly read 2026-11-12: https://pmc.ncbi.nlm.nih.gov/articles/PMC2430087/ . Specifically original player payoff per cooperating neighbor, cost paid per neighbor, uniform-death then fitness-proportional local reproduction, neutrality 1/N, and source's warning that the simple `b/c > k` rule assumes N large relative to k.

Extended finite-graph primary theory: Y.-T. Chen, A. McAvoy, M. A. Nowak (2016), *Fixation Probabilities for Any Configuration of Two Strategies on Regular Graphs*, Scientific Reports 6:39181, DOI 10.1038/srep39181; original open text directly read 2026-11-12: https://pmc.ncbi.nlm.nih.gov/articles/PMC5177945/. Its finite homogeneous graph discussions motivate checking the N>2k boundary. Do not apply the finite threshold `k(N-2)/(N-2k)` algebraically to N<=2k as if it were a valid positive threshold.

## New scientific question and fixed mechanism

The original R137 checked C5 through C9 for degree k=2, obtaining the exact finite-cycle threshold `2(N−2)/(N−4)` for N>4. This new supplementary calculation asks: what actually happens at the **N=2k (C4)** equality and the **N<2k (C3)** case, where the previously quoted threshold becomes undefined or invalid?

The C3 graph is the simple three-vertex cycle, graph-theoretically K3. C4 is the four-vertex cycle. Both have degree k=2. There is no mutation, no population-size change, no tie-breaking by floating point, and one initial cooperator located uniformly among vertices.

For each binary configuration `s`, with number of cooperating vertices `m(s)`, each cooperator has `pi_i=b*number_of_cooperating_neighbors−c*2`, and each defector `pi_i=b*number_of_cooperating_neighbors`; as in the historical R137 freeze, implemented fitness `f_i=1+w*pi_i`. Source Ohtsuki 2006 also writes a normalization `1−w+w*pi_i`, which has the **same first derivative at w=0** under fitness-proportional replacement because the common additive first-order shift cancels. Its finite nonzero-w numerical values need not equal the archived `1+w*pi_i` convention.

Per update, choose the dead vertex uniformly; then one of its two existing neighbors reproduces with probability proportional to its **pre-event** fitness. Replaced vertex copies the parent strategy. The two absorbing configurations are all defect and all cooperate. Let `rho_C(w)` be the probability of absorption at all cooperators from a uniformly random single-cooperator start. The neutral probability is exactly 1/N.

All 2^N configurations were generated without orbit aggregation or dependencies on prior R137 code. Constructed exact `P0` and `P1=dP/dw at w=0`, with all row sums respectively 1 and 0. Fixed transient neutral probabilities `rho0(s)=m(s)/N`. Exact state-by-state first derivative follows the full transient linear system:

`(I-Q0) rho_prime = P1 rho0`.

To calculate the linear coefficient in benefit and cost, the entire system is separately solved with `(b=1,c=0)` and `(b=0,c=1)` using exact rational Gauss-Jordan elimination. A second independent direct-code path constructs transition probabilities at `w=1/10000` from actual positive fitness, solves the full absorbing chain **without invoking P0, P1 or gradient routines**, and compares the signs of the first-order predictions outside zero-derivative cases.

## New exact findings

| Graph | coefficient of b | coefficient of c | Positive b/c threshold | Neutral ρ_C |
|---|---:|---:|---|---:|
| C3 | -1/6 | -1/3 | no_finite_positive_threshold | 1/3 |
| C4 | 0 | -1/2 | no_finite_positive_threshold | 1/4 |
| C5 | 1/10 | -3/5 | 6 | 1/5 |

Therefore, with the per-neighbor cost c>0:

* C3: `d rho_C / dw at 0 = -b/6 - c/3`. For nonnegative benefit b, a single cooperator has **negative** first-order selective advantage. Its k=2 large-population condition cannot be transplanted to N=3.
* C4: `d rho_C / dw at 0 = -c/2`. The positive benefit b cancels **at first order**; no finite positive b/c can make the one-mutant *weak-selection derivative* positive while c>0. This is the mathematical N=2k critical boundary that the historical C5–C9 grid did not include.
* C5: `d rho_C / dw at 0 = (b-6c)/10`. The implied `b/c>6` strictly reproduces the previously accepted R137 C5 threshold. C5 values are **historical-claim recovery**, while C3 and C4 constitute this addendum's genuinely newly computed coverage.

For each C3/C4/C5 and b∈{0,2,6,10} with c=1, actual fixed positive strength `w=1/10000` was solved by an independent direct absorbing Markov system, **12 exact finite-strength probability calculations**. Sign agreement with the weak-selection derivative occurred whenever the derivative was nonzero. For C5 b=6, the first derivative is exactly zero and the finite-strength score is slightly negative: **a zero derivative alone is insufficient to infer a sign at w>0**. At C4, different b may change higher-order outcomes despite all having the same first-order gradient -c/2.

This model is mathematical, with 8, 16 and 32 artificial configurations in C3/C4/C5. They are not empirical persons or sessions. No humans/animals or historical processes were measured and no causal social-network claim follows.

## Tests, reproducibility, caveats

Python 3.13.5 standard library only. Exact Fraction arithmetic for every Markov entry and linear solve. Four real `unittest` methods passed under standard and optimized (`python -O`) execution independently; both modes produced byte-identical complete machine-readable JSON. No errors in accepted tests. The positive-fitness secondary path is intentionally confined to chosen finite w and parameters; it is a sensitivity validation, not a full proof of signs for every finite w.

Executed commands:

```bash
python r137_cycle_small_population_boundary_20261112.py --test
python -O r137_cycle_small_population_boundary_20261112.py --test
python r137_cycle_small_population_boundary_20261112.py > R137_CYCLE_SMALL_POPULATION_BOUNDARY_20261112.json
python -O r137_cycle_small_population_boundary_20261112.py > /tmp/r137_optimized.json
cmp R137_CYCLE_SMALL_POPULATION_BOUNDARY_20261112.json /tmp/r137_optimized.json
```

Stand-alone Python script SHA256 `03deb51fb3167045095fcc8b94a2148381565f504206f522f4156d88ad436cba`; complete JSON SHA256 `e44c79ee3c5fbd1d277c7fff8c3b07c4686e8b3125f69f08f02eef1de12a7dc5`.

**Evidence level:** independent **same-team** exact mathematical E1 addendum to already accepted model. Not an independent external group reproduction. Original Ohtsuki numerical simulations, 2016 full analytical formula and real animal or human behavior were not independently rerun. New E2 scores 0; E3 scores 0; frozen R073 and PESEN v0.1 unchanged. No paid APIs, packages, clouds or CI initiated. The actual GitHub CI state should be checked separately; commit archival is not a new CI result.

## Appendix A. Complete independently executable Python source

```python
#!/usr/bin/env python3
"""R137 post-freeze exact C3/C4 boundary audit, with frozen C5 check.

Different implementation: full 2**N configurations, uncompressed state-wise
transitions and differentiation through an exact absorbing Markov system.
No prior R137 implementation imported. No external packages.
"""
from fractions import Fraction as F
import unittest
import json

ZERO=F(0)
ONE=F(1)

def graph_cycle(n):
    if n < 3:
        raise ValueError('a simple cycle has at least three vertices')
    return tuple(tuple(sorted({(i-1)%n, (i+1)%n})) for i in range(n))

def num_coop(state):
    return state.bit_count()

def payoffs(state, adj, b, c):
    n=len(adj)
    return tuple(b*sum((state>>j)&1 for j in adj[i]) - (c*len(adj[i]) if (state>>i)&1 else ZERO) for i in range(n))

def transition_and_gradient(n, b, c):
    adj=graph_cycle(n)
    tot=2**n
    trans=[{} for _ in range(tot)]
    gradient=[{} for _ in range(tot)]
    for state in range(tot):
        pi=payoffs(state, adj, b, c)
        for dying in range(n):
            friends=adj[dying]
            k=len(friends)
            sum_pi=sum((pi[j] for j in friends),ZERO)
            for parent in friends:
                newstate = (state | (1<<dying)) if ((state>>parent)&1) else (state & ~(1<<dying))
                p=F(1,n*k)
                dp=F(1,n)*(F(k)*pi[parent]-sum_pi)/F(k*k)
                trans[state][newstate]=trans[state].get(newstate,ZERO)+p
                gradient[state][newstate]=gradient[state].get(newstate,ZERO)+dp
        if sum(trans[state].values(),ZERO)!=ONE or sum(gradient[state].values(),ZERO)!=ZERO:
            raise ArithmeticError('non-stochastic exact transition or derivative')
    return trans,gradient

def exact_solve(matrix,rhs):
    """Generic independent exact linear solver with strict rank checks."""
    n=len(rhs)
    mat=[[F(z) for z in row]+[F(y)] for row,y in zip(matrix,rhs)]
    for col in range(n):
        pivot=next((k for k in range(col,n) if mat[k][col]),None)
        if pivot is None:
            raise ArithmeticError('singular transient system')
        mat[col],mat[pivot]=mat[pivot],mat[col]
        den=mat[col][col]
        mat[col]=[u/den for u in mat[col]]
        for i in range(n):
            if i!=col and mat[i][col]:
                scale=mat[i][col]
                mat[i]=[u-scale*v for u,v in zip(mat[i],mat[col])]
    return [row[-1] for row in mat]

def fixation_derivative_cycle(n,b,c):
    """Solve (I-Q0)*rho_prime = P1*rho0 on all transient states."""
    trans,grad=transition_and_gradient(n,b,c)
    states=range(1,(2**n)-1)
    Q=[]
    rhs=[]
    for state in states:
        Q.append([F(int(state==j)) - trans[state].get(j,ZERO) for j in states])
        rhs.append(sum((weight*F(num_coop(nextstate),n) for nextstate,weight in grad[state].items()),ZERO))
    derivative=exact_solve(Q,rhs)
    return sum((derivative[(1<<i)-1] for i in range(n)),ZERO)/n

def direct_transition_cycle(n,b,c,w):
    adj=graph_cycle(n)
    trans=[{} for _ in range(2**n)]
    for state in range(2**n):
        pi=payoffs(state,adj,b,c)
        fitness=tuple(ONE+w*z for z in pi)
        if min(fitness)<=ZERO:
            raise ValueError('nonpositive fitness')
        for dying in range(n):
            denom=sum((fitness[z] for z in adj[dying]),ZERO)
            for parent in adj[dying]:
                newstate = (state | (1<<dying)) if ((state>>parent)&1) else (state & ~(1<<dying))
                probability=F(1,n)*fitness[parent]/denom
                trans[state][newstate]=trans[state].get(newstate,ZERO)+probability
        if sum(trans[state].values(),ZERO)!=ONE:
            raise ArithmeticError('transition not stochastic')
    return trans

def direct_fixation(n,b,c,w):
    """No derivative code called here: directly solve full positive-fitness chain."""
    mat=direct_transition_cycle(n,b,c,w)
    states=range(1,2**n-1)
    a=[[F(int(s==t))-mat[s].get(t,ZERO) for t in states] for s in states]
    rhs=[mat[s].get(2**n-1,ZERO) for s in states]
    x=exact_solve(a,rhs)
    return sum((x[(1<<i)-1] for i in range(n)),ZERO)/n

def run():
    out=[]
    for n in (3,4,5):
        alpha=fixation_derivative_cycle(n,F(1),ZERO)
        beta=fixation_derivative_cycle(n,ZERO,F(1))
        intercept={'n':n,'graph':f'C{n}','degree':2,'benefit_slope':str(alpha),
                   'cost_slope':str(beta),
                   'weak_selection_threshold_b_over_c':str(-beta/alpha) if alpha>0 else 'no_finite_positive_threshold',
                   'neutral_fixation':str(F(1,n))}
        if not (beta<0):
            raise ArithmeticError('expected cost gradient sign not found')
        if n==5 and -beta/alpha != F(6):
            raise ArithmeticError('C5 original R137 finite-cycle threshold disagrees')
        values=[]
        for benefit in (F(0),F(2),F(6),F(10)):
            predicted=benefit*alpha+beta
            val=direct_fixation(n,benefit,F(1),F(1,10000))
            actual=val-F(1,n)
            if (predicted>0) != (actual>0) or (predicted<0)!=(actual<0):
                # When derivative zero higher order may matter. Do not over-interpret.
                if predicted!=0:
                    raise ArithmeticError(('exact-finite-vs-weak-sign',n,benefit,predicted,actual))
            values.append({'benefit':str(benefit),'weak_gradient':str(predicted),'exact_rho_minus_neutral_w_1e-4':str(actual)})
        intercept['finite_strength_cases']=values
        out.append(intercept)
    return {'study':'R137 supplemental C3/C4 boundary source-equation exact audit',
       'evidence':'synthetic exact Markov systems E1 only; new E2/E3 0',
       'n_states_examined':{'C3':8,'C4':16,'C5':32},
       'update_rule':'death-birth (uniform death, pre-event neighbor fitness proportional replacement)',
       'payoff':'benefit per cooperating neighbor; cost per neighbor paid by each cooperator; F=1+w*payoff',
       'small_w':'1/10000',
       'results':out}

class Tests(unittest.TestCase):
    def test_neutral_transition(self):
        for n in (3,4,5):
            trans,p1=transition_and_gradient(n,F(4),F(1))
            self.assertEqual(len(trans),2**n)
            for s in range(2**n):
                self.assertEqual(sum(trans[s].values(),ZERO),ONE)
                self.assertEqual(sum(p1[s].values(),ZERO),ZERO)
    def test_benefit_cost_derivatives(self):
        result=run()
        self.assertEqual(len(result['results']),3)
    def test_original_c5_identity(self):
        a=fixation_derivative_cycle(5,ONE,ZERO)
        c=fixation_derivative_cycle(5,ZERO,ONE)
        self.assertEqual(-c/a,F(6))
    def test_reject_invalid_cycle(self):
        with self.assertRaises(ValueError):
            graph_cycle(2)

if __name__=='__main__':
    import sys
    if len(sys.argv)>1 and sys.argv[1]=='--test':
        unittest.main(argv=sys.argv[:1],verbosity=2)
    else:
        print(json.dumps(run(),ensure_ascii=False,indent=2))
```

## Appendix B. Complete deterministic machine results

```json
{
  "study": "R137 supplemental C3/C4 boundary source-equation exact audit",
  "evidence": "synthetic exact Markov systems E1 only; new E2/E3 0",
  "n_states_examined": {
    "C3": 8,
    "C4": 16,
    "C5": 32
  },
  "update_rule": "death-birth (uniform death, pre-event neighbor fitness proportional replacement)",
  "payoff": "benefit per cooperating neighbor; cost per neighbor paid by each cooperator; F=1+w*payoff",
  "small_w": "1/10000",
  "results": [
    {
      "n": 3,
      "graph": "C3",
      "degree": 2,
      "benefit_slope": "-1/6",
      "cost_slope": "-1/3",
      "weak_selection_threshold_b_over_c": "no_finite_positive_threshold",
      "neutral_fixation": "1/3",
      "finite_strength_cases": [
        {
          "benefit": "0",
          "weak_gradient": "-1/3",
          "exact_rho_minus_neutral_w_1e-4": "-1/29997"
        },
        {
          "benefit": "2",
          "weak_gradient": "-2/3",
          "exact_rho_minus_neutral_w_1e-4": "-15002/225044997"
        },
        {
          "benefit": "6",
          "weak_gradient": "-4/3",
          "exact_rho_minus_neutral_w_1e-4": "-5003/37537503"
        },
        {
          "benefit": "10",
          "weak_gradient": "-2",
          "exact_rho_minus_neutral_w_1e-4": "-15016/75135027"
        }
      ]
    },
    {
      "n": 4,
      "graph": "C4",
      "degree": 2,
      "benefit_slope": "0",
      "cost_slope": "-1/2",
      "weak_selection_threshold_b_over_c": "no_finite_positive_threshold",
      "neutral_fixation": "1/4",
      "finite_strength_cases": [
        {
          "benefit": "0",
          "weak_gradient": "-1/2",
          "exact_rho_minus_neutral_w_1e-4": "-39995/799840012"
        },
        {
          "benefit": "2",
          "weak_gradient": "-1/2",
          "exact_rho_minus_neutral_w_1e-4": "-400089993/8002399879972"
        },
        {
          "benefit": "6",
          "weak_gradient": "-1/2",
          "exact_rho_minus_neutral_w_1e-4": "-133483347/2670667639820"
        },
        {
          "benefit": "10",
          "weak_gradient": "-1/2",
          "exact_rho_minus_neutral_w_1e-4": "-44534465/891290119812"
        }
      ]
    },
    {
      "n": 5,
      "graph": "C5",
      "degree": 2,
      "benefit_slope": "1/10",
      "cost_slope": "-3/5",
      "weak_selection_threshold_b_over_c": "6",
      "neutral_fixation": "1/5",
      "finite_strength_cases": [
        {
          "benefit": "0",
          "weak_gradient": "-3/5",
          "exact_rho_minus_neutral_w_1e-4": "-374905007/6248125274985"
        },
        {
          "benefit": "2",
          "weak_gradient": "-2/5",
          "exact_rho_minus_neutral_w_1e-4": "-5001600019993/125050001749349965"
        },
        {
          "benefit": "6",
          "weak_gradient": "0",
          "exact_rho_minus_neutral_w_1e-4": "-247670533988637/38696115108190136819185"
        },
        {
          "benefit": "10",
          "weak_gradient": "2/5",
          "exact_rho_minus_neutral_w_1e-4": "6974206456988240507/174550518116433052744265"
        }
      ]
    }
  ]
}
```
