"""R155 Bass (1969) first-adoption diffusion: bounded synthetic E1 experiments.

This is model mathematics and original Table I published-coefficient arithmetic.
No original sales time series or empirical predictive evaluation is used.
"""
from __future__ import annotations

import json
import math

P_GRID = (0.0, 1/200, 1/50, 2/25, 1/5)
Q_GRID = (0.0, 1/50, 1/10, 2/5, 4/5)
MARKETS = (100, 1000, 10000)
TIMES = (0.0, 0.25, 1.0, 3.0, 5.0, 10.0)
STEPS_PER_UNIT = 2048

# Printed p, q and m (m column is in 1,000 units), original Bass 1969 p.218 Table I.
PUBLISHED_TABLE_I = (
    ("electric_refrigerators", 0.0026167, 0.21566, 40001),
    ("home_freezers", 0.018119, 0.17110, 21973),
    ("black_white_television", 0.027877, 0.25105, 96717),
)


def checked_number(value: object, label: str, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise ValueError(f"{label}: finite numeric argument required")
    v = float(value)
    if not math.isfinite(v) or v < 0 or (positive and v <= 0):
        raise ValueError(f"{label}: out of range")
    return v


def rates(p: float, q: float) -> tuple[float, float]:
    return checked_number(p, "p"), checked_number(q, "q")


def rhs(f: float, p: float, q: float) -> float:
    """Original continuous-time Bass model dF/dt."""
    return (p + q*f)*(1.0-f)


def cumulative(t: float, p: float, q: float) -> float:
    """Numerically stable closed-form F(t), zero initial adoption."""
    t = checked_number(t, "time")
    p, q = rates(p, q)
    if p == 0.0:
        return 0.0
    k = p + q
    e = math.exp(-k*t)
    return -math.expm1(-k*t)/(1.0 + (q/p)*e)


def adoption_density(t: float, p: float, q: float) -> float:
    f = cumulative(t, p, q)
    return rhs(f, p, q)


def interior_peak_time(p: float, q: float) -> float | None:
    """None means no unique finite maximizer (unseeded p=0)."""
    p, q = rates(p, q)
    if p == 0.0:
        return None
    if q <= p:
        return 0.0
    return math.log(q/p)/(p+q)


def rk4_at(t: float, p: float, q: float) -> float:
    """Independent integration uses only RHS and F(0)=0; no closed-form calls."""
    t = checked_number(t, "time")
    p, q = rates(p, q)
    n = max(1, math.ceil(t*STEPS_PER_UNIT))
    h = t/n
    f = 0.0
    for _ in range(n):
        k1 = rhs(f,p,q)
        k2 = rhs(f + 0.5*h*k1,p,q)
        k3 = rhs(f + 0.5*h*k2,p,q)
        k4 = rhs(f + h*k3,p,q)
        f += h*(k1+2*k2+2*k3+k4)/6.0
    return f


def rk4_grid(p: float, q: float) -> tuple[float, ...]:
    """One independent RK4 run, checkpointed exactly at six preregistered times."""
    p, q = rates(p, q)
    indices = {int(round(t*STEPS_PER_UNIT)):i for i,t in enumerate(TIMES)}
    result = [None]*len(TIMES)
    f = 0.0
    h = 1.0/STEPS_PER_UNIT
    for step in range(int(TIMES[-1]*STEPS_PER_UNIT)+1):
        if step in indices:
            result[indices[step]]=f
        if step == int(TIMES[-1]*STEPS_PER_UNIT):
            break
        k1=rhs(f,p,q)
        k2=rhs(f+0.5*h*k1,p,q)
        k3=rhs(f+0.5*h*k2,p,q)
        k4=rhs(f+h*k3,p,q)
        f += h*(k1+2*k2+2*k3+k4)/6.0
    assert all(z is not None for z in result)
    return tuple(result)


def euler_one_step(dt: float, p: float, q: float) -> float:
    """Unconstrained Euler negative control, starting at F=0."""
    dt=checked_number(dt,"dt")
    p,q=rates(p,q)
    return dt*rhs(0.0,p,q)


def published_table_arithmetic() -> list[dict]:
    """Arithmetic on 3 printed 1969 rounded coefficients, not sales-data refitting."""
    out=[]
    for name,p,q,m_thousands in PUBLISHED_TABLE_I:
        t=interior_peak_time(p,q)
        fstar=(q-p)/(2*q)
        peak=m_thousands*((p+q)**2)/(4*q)
        direct=m_thousands*adoption_density(t,p,q)
        if abs(peak-direct)>1e-7:
            raise AssertionError("Table I coefficient peak algebra error")
        out.append({
            "product":name,"source_printed_p":p,"source_printed_q":q,
            "source_printed_m_thousands":m_thousands,
            "source_derived_t_peak":round(t,12),
            "source_derived_peak_fraction":round(fstar,12),
            "source_derived_peak_sales_thousands_per_time":round(peak,9),
            "source_derived_initial_sales_thousands_per_time":round(m_thousands*p,9),
            "table_reproduction_scope":"published rounded coefficients arithmetic only",
        })
    return out


def result_document() -> dict:
    cases=[]
    errors=[]
    for pi,p in enumerate(P_GRID):
        for qi,q in enumerate(Q_GRID):
            numerical = rk4_grid(p,q)
            analytic = tuple(cumulative(t,p,q) for t in TIMES)
            err = max(abs(n-a) for n,a in zip(numerical,analytic))
            if err > 2e-11:
                raise AssertionError(f"RK4 mismatch p={p} q={q} err={err}")
            errors.append(err)
            peak_t=interior_peak_time(p,q)
            samples=[]
            for t,f,n in zip(TIMES,analytic,numerical):
                density=rhs(f,p,q)
                samples.append({
                    "t":t,
                    "F":round(f,14),
                    "RK4_F":round(n,14),
                    "f":round(density,14),
                    "first_adopters_m_fraction":round(1.0-f,14)
                })
            for mi,m in enumerate(MARKETS):
                cases.append({
                    "scenario_id":f"p{pi}_q{qi}_m{mi}",
                    "p":p,"q":q,"market":m,
                    "peak_t":None if peak_t is None else round(peak_t,12),
                    "samples":[{**s,"cumulative_count":round(s["F"]*m,10),
                        "adoption_rate_count":round(s["f"]*m,10)} for s in samples],
                    "max_abs_closed_form_vs_RK4":round(err,16),
                })
    assert len(cases)==75 and len({c["scenario_id"] for c in cases})==75
    return {
        "research_id":"R155",
        "evidence_level":"E1_ORIGINAL_EQUATION_AND_PRINTED_TABLE_ARITHMETIC",
        "original_author_data_refit":False,
        "historical_heldout_prediction":False,
        "scenario_count":75,"time_grid":list(TIMES),
        "integration_steps_per_unit":STEPS_PER_UNIT,
        "max_RK4_closed_form_error":round(max(errors),16),
        "cases":cases,
        "published_table_I_arithmetic":published_table_arithmetic(),
        "negative_controls":{
            "Euler_p_0_2_q_0_8_dt_10":euler_one_step(10.0,.2,.8),
            "exact_continuous_F_t10_p_0_2_q_0_8":round(cumulative(10.0,.2,.8),14),
            "p_zero_q_point_eight_F_t10":cumulative(10.0,0.0,.8),
            "same_initial_flow_first":1000*.02,
            "same_initial_flow_second":2000*.01,
            "different_future_F_t1_first":round(cumulative(1,.02,.4),14),
            "different_future_F_t1_second":round(cumulative(1,.01,.4),14),
        },
    }


def main():
    print(json.dumps(result_document(),sort_keys=True,indent=2,ensure_ascii=False))


if __name__ == "__main__":
    main()
