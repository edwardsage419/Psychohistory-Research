"""R156 96 constructed AK versus diminishing-return growth histories.

Research scope is E1 mathematics. No Romer/Rebelo full equilibrium reconstruction
or historical macroeconomic calibration is asserted.
"""
from __future__ import annotations

import json
import math

ALPHAS = (1.0, 0.5)
INITIAL_STOCKS = (1.0, 4.0, 9.0)
SAVINGS = (0.1, 0.2, 0.4, 0.6)
DEPRECIATIONS = (0.0, 0.1, 0.2, 0.4)
TIMES = (0.0, 1.0, 5.0, 10.0)
STEPS_PER_UNIT = 1024


def checked(value, name: str, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value,(float,int)):
        raise ValueError(f"{name} must be numeric")
    result=float(value)
    if not math.isfinite(result) or result<0 or (positive and result<=0):
        raise ValueError(f"{name} must be finite and {'positive' if positive else 'nonnegative'}")
    return result


def inputs(k0, alpha, s, delta):
    k0=checked(k0,"initial capital",positive=True)
    alpha=checked(alpha,"alpha",positive=True)
    s=checked(s,"saving rate")
    delta=checked(delta,"depreciation")
    if alpha not in ALPHAS or s>1:
        raise ValueError("only frozen model exponents and valid saving shares accepted")
    return k0,alpha,s,delta


def flow_rhs(k,alpha,s,delta):
    return s*k**alpha-delta*k


def analytic_k(t,k0,alpha,s,delta):
    t=checked(t,"time")
    k0,alpha,s,delta=inputs(k0,alpha,s,delta)
    if alpha==1.0:
        return k0*math.exp((s-delta)*t)
    x0=math.sqrt(k0)
    if delta==0:
        x=x0+s*t/2
    else:
        xstar=s/delta
        x=xstar+(x0-xstar)*math.exp(-delta*t/2)
    return x*x


def rk4_grid(k0,alpha,s,delta):
    """Integrate the physical stock k directly; do not integrate the transformed x."""
    k,alpha,s,delta=inputs(k0,alpha,s,delta)
    limit=int(round(TIMES[-1]*STEPS_PER_UNIT))
    points={int(round(t*STEPS_PER_UNIT)):i for i,t in enumerate(TIMES)}
    out=[None]*len(TIMES)
    h=1/STEPS_PER_UNIT
    for step in range(limit+1):
        if step in points:
            out[points[step]]=k
        if step==limit:
            break
        a=flow_rhs(k,alpha,s,delta)
        b=flow_rhs(k+h*a/2,alpha,s,delta)
        c=flow_rhs(k+h*b/2,alpha,s,delta)
        d=flow_rhs(k+h*c,alpha,s,delta)
        k=k+h*(a+2*b+2*c+d)/6
        if not math.isfinite(k) or k<=0:
            raise AssertionError("physical positive stock violated by RK4")
    return tuple(out)


def rk4_at(t,k0,alpha,s,delta):
    """Independent optional arbitrary-time RK4, fixed maximum step."""
    t=checked(t,"time")
    k,alpha,s,delta=inputs(k0,alpha,s,delta)
    n=max(1,math.ceil(t*STEPS_PER_UNIT))
    h=t/n
    for _ in range(n):
        a=flow_rhs(k,alpha,s,delta)
        b=flow_rhs(k+h*a/2,alpha,s,delta)
        c=flow_rhs(k+h*b/2,alpha,s,delta)
        d=flow_rhs(k+h*c,alpha,s,delta)
        k+=h*(a+2*b+2*c+d)/6
    return k


def euler_step(k0,alpha,s,delta,dt):
    dt=checked(dt,"dt")
    k0,alpha,s,delta=inputs(k0,alpha,s,delta)
    return k0+dt*flow_rhs(k0,alpha,s,delta)


def result_document():
    worlds=[]
    worst=0.0
    for ai,alpha in enumerate(ALPHAS):
        for ki,k0 in enumerate(INITIAL_STOCKS):
            for si,s in enumerate(SAVINGS):
                for di,delta in enumerate(DEPRECIATIONS):
                    numerical=rk4_grid(k0,alpha,s,delta)
                    analytical=[analytic_k(t,k0,alpha,s,delta) for t in TIMES]
                    err=max(abs(x-y) for x,y in zip(numerical,analytical))
                    if err>=1e-7:
                        raise AssertionError(f"model integration disagreement: {ai},{ki},{si},{di},err={err}")
                    worst=max(err,worst)
                    points=[{
                        "t":t,
                        "closed_stock":round(a,12),
                        "rk4_stock":round(b,12),
                        "output_at_closed_stock":round(a**alpha,12),
                        "flow_at_closed_stock":round(flow_rhs(a,alpha,s,delta),12)
                    } for t,a,b in zip(TIMES,analytical,numerical)]
                    worlds.append({
                        "scenario_id":f"a{ai}_k{ki}_s{si}_d{di}",
                        "alpha":alpha,"k0":k0,"s":s,"delta":delta,
                        "points":points,"max_abs_closed_vs_RK4":round(err,15),
                        "AK_implied_growth":round(s-delta,12) if alpha==1.0 else None,
                        "concave_steady_state":round((s/delta)**2,12) if alpha==.5 and delta>0 else None,
                    })
    if len(worlds)!=96 or len(set(w["scenario_id"] for w in worlds))!=96:
        raise AssertionError("frozen world count mismatch")
    return {
        "research_id":"R156","evidence_level":"E1_REDUCED_FORM_ARTIFICIAL",
        "author_original_full_model_reproduction":False,
        "historical_data_forecasting":False,
        "scenario_count":96,"time_grid":list(TIMES),
        "independent_RK4_steps_per_time_unit":STEPS_PER_UNIT,
        "max_absolute_RK4_error":round(worst,15),
        "worlds":worlds,
        "mechanism_controls":{
            "AK_same_growth_path_a":[round(analytic_k(t,1,1,.2,.1),12) for t in TIMES],
            "AK_same_growth_path_b":[round(analytic_k(t,1,1,.4,.3),12) for t in TIMES],
            "concave_initial_slope_same":round(flow_rhs(1,.5,.2,.1),12),
            "concave_future_path_a":round(analytic_k(5,1,.5,.2,.1),12),
            "concave_future_path_b":round(analytic_k(5,1,.5,.4,.3),12),
            "Euler_large_step_negative":euler_step(1,1,.1,.4,20),
            "AK_exact_large_time_positive":round(analytic_k(20,1,1,.1,.4),15),
        }
    }


def main():
    print(json.dumps(result_document(),indent=2,sort_keys=True,ensure_ascii=False))


if __name__=="__main__":
    main()
