#!/usr/bin/env python3
"""R020, synthetic DESIGN CHECK only. This is not human-subject evidence.

Orthogonal randomized one-shot factors:
E factual evidence, N stated audience approval, V identifiable visibility,
C real uniform *posting* cost (NOT necessarily a normative sanction).

This model is an illustrative prospective DGP, NOT the R019 paper or PESEN.
Independent participants / fixed exogenous message cards / no interaction
until all outcome elicitation. For live network experiments switch to session-
level randomization and a cluster/interference-aware estimator.
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
import random
from dataclasses import dataclass, asdict
from pathlib import Path

FACTOR_NAMES = ("E", "N", "V", "C")
CELLS = tuple(itertools.product((0, 1), repeat=4))

@dataclass(frozen=True)
class SyntheticParameters:
    information: float = 0.045
    audience: float = 0.50
    posting_cost: float = 0.60
    private_noise: float = 0.16
    seed: int = 20261014


def logistic(z: float) -> float:
    return 1/(1+math.exp(-z)) if z >= 0 else math.exp(z)/(1+math.exp(z))


def validate(params: SyntheticParameters, per_cell: int) -> None:
    if per_cell < 2:
        raise ValueError('at least two participants in each factorial cell')
    if any(not math.isfinite(getattr(params,f)) for f in ('information','audience','posting_cost','private_noise')):
        raise ValueError('finite parameters required')
    if params.private_noise < 0:
        raise ValueError('negative noise impossible')


def generate(params: SyntheticParameters, per_cell: int, seed: int | None = None):
    """Return 16 independent randomized cells, participants repeated only pre/post."""
    validate(params,per_cell)
    rng = random.Random(params.seed if seed is None else seed)
    out = {}
    for E,N,V,C in CELLS:
        rs = []
        for _ in range(per_cell):
            b0 = 0.25 + 0.5*rng.random()
            b1 = min(1.0,max(0.0,b0 + params.information * (2*E-1) + rng.gauss(0,params.private_noise)))
            logit = -.15 + 2.5*(b1-.5) + params.audience*V*(2*N-1) - params.posting_cost*C + .10*V
            y = int(rng.random() < logistic(logit))
            rs.append({'b0':b0,'b1':b1,'delta_private':b1-b0,'public_endorse':y})
        out[(E,N,V,C)] = rs
    return out


def contrast_weights(name: str):
    """Factorial ATE estimands: exact equal-weight cell contrasts."""
    w={}
    for E,N,V,C in CELLS:
        if name == 'evidence_to_private':w[(E,N,V,C)]=(2*E-1)/8
        elif name == 'cost_to_public':w[(E,N,V,C)]=(2*C-1)/8
        elif name == 'approval_x_visibility_on_public':w[(E,N,V,C)]=(2*N-1)*(2*V-1)/4
        else:raise ValueError(name)
    return w


def estimate(cells, name: str):
    """Cell-mean contrast and heteroskedastic plug-in SE, individual independence only."""
    w=contrast_weights(name)
    measure = 'delta_private' if name == 'evidence_to_private' else 'public_endorse'
    effect=0.0; var=0.0
    for key in CELLS:
        a=[r[measure] for r in cells[key]]
        n=len(a)
        if n<2:raise ValueError('undersized cell')
        mean=sum(a)/n
        sample_var=sum((x-mean)**2 for x in a)/(n-1)
        effect+=w[key]*mean
        var+=w[key]**2*sample_var/n
    se=math.sqrt(var)
    return {'estimate':effect,'se':se,'z':effect/se if se else 0.0,
            'interval_95_normal':[effect-1.96*se,effect+1.96*se]}


def gaussian_rank(matrix,tol=1e-10):
    """Check factorial design rank; pivoted Gauss-Jordan on column design matrix."""
    a=[list(map(float,row)) for row in matrix]
    n=len(a);p=len(a[0]);rank=0
    for col in range(p):
        pivot=max(range(rank,n), key=lambda r:abs(a[r][col]))
        if abs(a[pivot][col])<tol:continue
        a[rank],a[pivot]=a[pivot],a[rank]
        z=a[rank][col]
        a[rank]=[x/z for x in a[rank]]
        for j in range(n):
            if j!=rank:
                factor=a[j][col]
                a[j]=[x-factor*y for x,y in zip(a[j],a[rank])]
        rank+=1
        if rank==n:break
    return rank


def design_rank():
    return gaussian_rank([[1,E,N,V,C,N*V] for E,N,V,C in CELLS])


def audience_only_can_mimic(s_target: float,b:float=0.0,peer:float=1.0):
    """A free audience weight d fits any public s between b and peer.
    Since s=(b+d*peer)/(1+d), solve d=(s-b)/(peer-s).
    This is non-identification when D may change with treatment.
    """
    if not (b <= s_target < peer):raise ValueError('target outside demonstration domain')
    return (s_target-b)/(peer-s_target)


def monte_carlo(per_cell=64,replications=350,seed=20261014):
    """Indicative operating characteristics under ASSUMED effects, not empirical power."""
    if replications<1:raise ValueError('replications must be positive')
    cfgs={'null':SyntheticParameters(0,0,0,seed=seed),
          'fixed_audience_no_cost':SyntheticParameters(.045,.5,0,seed=seed),
          'audience_plus_posting_cost':SyntheticParameters(.045,.5,.6,seed=seed)}
    names=('evidence_to_private','cost_to_public','approval_x_visibility_on_public')
    critical_z = 2.39398  # two-sided Bonferroni alpha=0.05/3, normal approximation
    out={}
    for k,p in cfgs.items():
        rejects={name:0 for name in names};means={name:0.0 for name in names}
        for i in range(replications):
            cells=generate(p,per_cell,seed=seed+17_981*i+sum(map(ord,k)))
            for name in names:
                est=estimate(cells,name)
                rejects[name]+=abs(est['z'])>critical_z
                means[name]+=est['estimate']
        out[k]={'rejection_rate_bonferroni':{n:rejects[n]/replications for n in names},
                'mean_estimates':{n:means[n]/replications for n in names}}
    return {'status':'EX_ANTE_SYNTHETIC_OPERATING_CHARACTERISTICS_NOT_HUMAN_DATA',
            'per_cell':per_cell,'total_participants':16*per_cell,
            'replications_per_DGP':replications,'seed':seed,'design_matrix_rank':design_rank(),
            'multiplicity':'three primary contrasts, Bonferroni two-sided alpha=0.05/3',
            'critical_z':critical_z,
            'parameters':{k:asdict(v) for k,v in cfgs.items()},'results':out,
            'caveat':'Normal-z demonstration assumes no interaction/spillovers, fixed random messages, and iid subjects; effect sizes chosen, NOT estimated. Not a recruitment recommendation.'}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--per-cell',type=int,default=64)
    ap.add_argument('--replications',type=int,default=350)
    ap.add_argument('--output',type=Path,default=Path('results/synthetic_design_check.json'))
    args=ap.parse_args()
    out=monte_carlo(args.per_cell,args.replications)
    out['audience_network_observational_equivalence_example']={
       'b':0,'peer_statement':1,
       's_cost0':0.5,'s_cost1':0.4,
       'D_cost0':audience_only_can_mimic(0.5),
       'D_cost1':audience_only_can_mimic(0.4),
       'interpretation':'Same decline in s can arise from D(C), even when no direct sanction term exists. A price effect only rejects FIXED-D baseline under appropriate exclusion assumptions.'}
    args.output.parent.mkdir(exist_ok=True,parents=True)
    args.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'n_per_cell':args.per_cell,'rank':design_rank(),'results':out['results']},ensure_ascii=False))
if __name__=='__main__':main()