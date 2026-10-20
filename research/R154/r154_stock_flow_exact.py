"""R154: conserved two-stock feedback and explicit nonphysical artifact controls.

Synthetic E1 only, 100 exactly preregistered Fraction histories.
"""
from __future__ import annotations

import json
from fractions import Fraction as F
from typing import Sequence

SHARES = (F(0), F(1,4), F(1,2), F(3,4), F(1))
INITIAL_A = (0, 2, 6, 10)
TOTAL = F(10)
HORIZON = 12


def as_fraction(value, label: str) -> F:
    if isinstance(value, bool) or not isinstance(value, (F, int)):
        raise ValueError(f'{label} needs int or Fraction')
    return F(value)


def checked_stocks(a, b):
    a, b = as_fraction(a, 'stock A'), as_fraction(b, 'stock B')
    if a < 0 or b < 0:
        raise ValueError('stocks cannot be negative')
    return a, b


def checked_rates(p, q):
    p, q = as_fraction(p, 'flow share p'), as_fraction(q, 'flow share q')
    if not (0 <= p <= 1 and 0 <= q <= 1):
        raise ValueError('transfer shares must lie between zero and one')
    return p, q


def closed_step(a, b, p, q):
    """Simultaneous conserved flows. Return next stocks and both directed flows."""
    a, b = checked_stocks(a, b)
    p, q = checked_rates(p, q)
    ab, ba = p*a, q*b
    return (a-ab+ba, b+ab-ba), (ab, ba)


def direct_history(a0, p, q, horizon=HORIZON):
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 0:
        raise ValueError('horizon must be a nonnegative integer')
    a0 = as_fraction(a0, 'initial A')
    if not 0 <= a0 <= TOTAL:
        raise ValueError('initial A must lie within total stock 10')
    checked_rates(p, q)
    a, b = a0, TOTAL-a0
    history = [(a,b)]
    flows = []
    for _ in range(horizon):
        (a,b),(ab,ba) = closed_step(a,b,p,q)
        history.append((a,b)); flows.append((ab,ba))
    return history, flows


def analytical_history(a0, p, q, horizon=HORIZON):
    """Independent diagonalized two-stock recurrence, never calls direct_history."""
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 0:
        raise ValueError('horizon must be a nonnegative integer')
    a0 = as_fraction(a0, 'initial A')
    if not 0 <= a0 <= TOTAL:
        raise ValueError('initial A out of bounds')
    p, q = checked_rates(p,q)
    if p+q == 0:
        a_values = [a0 for _ in range(horizon+1)]
    else:
        star = TOTAL*q/(p+q)
        lam = 1-p-q
        a_values = [star + lam**t*(a0-star) for t in range(horizon+1)]
    return [(a,TOTAL-a) for a in a_values]


def forward_euler_step(a,b,rate_ab,rate_ba,dt):
    """Unconstrained explicit Euler for a continuous rate model, may go negative."""
    a,b=checked_stocks(a,b)
    u,v=as_fraction(rate_ab,'continuous rate'),as_fraction(rate_ba,'continuous rate')
    dt=as_fraction(dt,'dt')
    if min(u,v,dt)<0:
        raise ValueError('rates/dt cannot be negative')
    delta=dt*(v*b-u*a)
    return a+delta,b-delta


def delayed_withdrawal_step(current_a,current_b,lagged_a,transfer_share,strict=True):
    """Artificial one-period delayed A->B command, with optional physical guard."""
    a,b=checked_stocks(current_a,current_b)
    old=as_fraction(lagged_a,'lagged A')
    p=as_fraction(transfer_share,'share')
    if old<0 or not 0<=p<=1:
        raise ValueError('negative lagged stock or invalid share')
    amount=p*old
    if strict and amount>a:
        raise ValueError('delayed command exceeds currently available A stock')
    return a-amount,b+amount


def open_step(a,b,p,q,inflow_a,outflow_b):
    """Internal transfers then external influx to A and withdrawal from B."""
    flow_in=as_fraction(inflow_a,'external input')
    flow_out=as_fraction(outflow_b,'external output')
    if flow_in < 0 or flow_out < 0:
        raise ValueError('external flows must be nonnegative')
    (na,nb), pair = closed_step(a,b,p,q)
    if nb < flow_out:
        raise ValueError('external output exceeds stock B after internal flow')
    return (na+flow_in,nb-flow_out),pair


def result_document():
    cases=[]
    for ai,a0 in enumerate(INITIAL_A):
        for pi,p in enumerate(SHARES):
            for qi,q in enumerate(SHARES):
                direct,flows=direct_history(a0,p,q)
                analytic=analytical_history(a0,p,q)
                if direct != analytic or len(direct) != 13 or len(flows) != 12:
                    raise AssertionError('independent exact route mismatch')
                if any(a<0 or b<0 or a+b!=TOTAL for a,b in direct):
                    raise AssertionError('invalid physical stock')
                cases.append({
                    'id':f'a{ai}_p{pi}_q{qi}', 'initial_A':str(F(a0)),
                    'p':str(p),'q':str(q),'lambda':str(1-p-q),
                    'stocks':[[str(a),str(b)] for a,b in direct],
                    'opposed_transfers':[[str(ab),str(ba)] for ab,ba in flows],
                    'matches_independent_closed_form':True,
                })
    assert len(cases)==100 and len({x['id'] for x in cases})==100
    return {
        'research_id':'R154', 'evidence':'E1_SYNTHETIC_ONLY',
        'scenario_count':100,'observations_per_case':13,
        'transitions_per_case':12,'total_stock':'10',
        'cases':cases,
        'negative_controls':{
            'Euler_rate_three_quarters_dt2_initial_10_0':
                [str(x) for x in forward_euler_step(10,0,F(3,4),F(3,4),2)],
            'Euler_rate_three_quarters_dt1_initial_10_0':
                [str(x) for x in forward_euler_step(10,0,F(3,4),F(3,4),1)],
            'delayed_unbounded_second_step':
                [str(x) for x in delayed_withdrawal_step(0,10,10,1,strict=False)],
            'open_system_initial_5_5_in_2_out_1':
                [str(x) for x in open_step(5,5,F(1,2),F(1,2),2,1)[0]],
        },
    }


def main():
    print(json.dumps(result_document(), sort_keys=True, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
