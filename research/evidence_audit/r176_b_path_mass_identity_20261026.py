"""Independent closed-form path mass check for R176 institutional observation audit.
Reads only R third-method receipt; reconstructs t2 and t3 differences algebraically.
"""
from fractions import Fraction as Q
from math import comb
import json
from pathlib import Path
from collections import defaultdict

RECEIPT=str(Path(__file__).resolve().parent.parent / 'validation' / 'r176_institution_observability_receipt_20261026.json')

def count_transition(k,j,mu,beta,gamma,d):
    a=1-(1-mu)*(1-beta)**k*(1-gamma)**j
    r=1-d/Q(1+j)
    out=defaultdict(Q)
    for b in range(k+1):
        for c in range(5-k):
            out[b+c]+=comb(k,b)*r**b*(1-r)**(k-b)*comb(4-k,c)*a**c*(1-a)**(4-k-c)
    assert sum(out.values())==1
    return dict(out)

def check(record):
    mu,beta,gamma,d=map(Q,[record['mu'],record['beta'],record['gamma'],record['dropout']])
    k0=record['initial_k']
    p1=count_transition(k0,0,mu,beta,gamma,d)
    # J1=1 iff k1>=3 for both rules, because J0=0.
    mass=sum((p1.get(k,Q(0))*count_transition(k,1,mu,beta,gamma,d).get(2,Q(0))
              for k in (3,4)),Q(0))
    # Only k2=2, J2=1 vs J2=0 differs at t2.
    observed_t2=Q(record['joint_tv'][2])
    assert mass==observed_t2,(record,mass,observed_t2)
    # At t3, the k marginal difference equals that displaced mass times
    # the total-variation distance of the two conditional count kernels.
    a=count_transition(2,0,mu,beta,gamma,d)
    b=count_transition(2,1,mu,beta,gamma,d)
    kernel_tv=sum(abs(a.get(k,Q(0))-b.get(k,Q(0))) for k in range(5))/2
    expected_t3=mass*kernel_tv
    observed_t3=Q(record['count_tv'][3])
    assert expected_t3==observed_t3,(record,expected_t3,observed_t3)
    return mass,kernel_tv

def main():
    data=json.load(open(RECEIPT))
    rows=data['rows']
    results=[check(row) for row in rows]
    assert len(results)==48
    assert sum(m>0 for m,tv in results)==24
    assert sum(m==0 for m,tv in results)==24
    # Mutant: forced reset at k2=2 would set the path mass to zero,
    # contradicting the 24 positive original observations.
    assert sum(m>0 for m,tv in results)>0
    out={'pairs_checked':48,'exact_t2_joint_path_mass_matches':48,
         'exact_t3_count_path_mass_times_kernel_tv_matches':48,
         'positive_path_mass_pairs':24,'zero_path_mass_pairs':24,
         'mutant_forced_reset_detected':True,
         'method':'independent two-step event factorization; no Markov trajectory propagation',
         'external_replication':False,'evidence':'E1_SYNTHETIC'}
    with open(str(Path(__file__).resolve().with_name('r176_b_path_mass_receipt_20261026.json')),'w') as f:json.dump(out,f,indent=2,sort_keys=True)
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
