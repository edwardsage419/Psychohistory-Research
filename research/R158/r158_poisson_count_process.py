"""R158 controlled synthetic Poisson conditional count model.

This is a discrete one-lag event count analogue, not Hawkes' continuous
point process, not a conflict dataset, and no actual forecast/causality claim.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction as F

MU_GRID=(F(1,2), F(1), F(2))
ALPHA_GRID=(F(0), F(1,4), F(1,2), F(3,4), F(1))
ARTIFICIAL_HISTORIES=(
    (0,0,0,0,0,0,0,0),
    (1,0,2,0,3,0,2,1),
    (0,1,3,2,0,1,4,0),
    (4,4,0,0,0,0,1,0),
)
EXPECTATION_HORIZON=12


def fraction_arg(x, name, strictly_positive=False):
    if isinstance(x,bool) or not isinstance(x,(int,F)):
        raise ValueError(f"{name} must be integer or Fraction")
    value=F(x)
    if value<0 or (strictly_positive and value==0):
        raise ValueError(f"{name} must be nonnegative/positive")
    return value


def params(mu,alpha):
    mu=fraction_arg(mu,"baseline mu",strictly_positive=True)
    alpha=fraction_arg(alpha,"feedback alpha")
    if alpha>1:
        raise ValueError("alpha outside the frozen stability/critical range [0,1]")
    return mu,alpha


def valid_counts(counts):
    if isinstance(counts,(str,bytes)) or not isinstance(counts,(tuple,list)):
        raise ValueError("history must be a list or tuple of nonnegative integer counts")
    out=[]
    for n in counts:
        if isinstance(n,bool) or not isinstance(n,int) or n<0:
            raise ValueError("invalid event count")
        out.append(n)
    return tuple(out)


def intensities(history, mu, alpha):
    hist=valid_counts(history)
    mu,alpha=params(mu,alpha)
    previous=0
    out=[]
    for observed in hist:
        out.append(mu+alpha*previous)
        previous=observed
    return tuple(out)


def log_score_gamma(history,mu,alpha):
    """Conditional Poisson log likelihood using lgamma for log(n!)."""
    history=valid_counts(history)
    lam=intensities(history,mu,alpha)
    terms=tuple(n*math.log(float(v))-float(v)-math.lgamma(n+1)
                for n,v in zip(history,lam))
    return sum(terms),terms


def log_score_factorial(history,mu,alpha):
    """Independent factorial arithmetic route, never calls log_score_gamma."""
    history=valid_counts(history)
    lam=intensities(history,mu,alpha)
    terms=[]
    for n,v in zip(history,lam):
        factorial=math.factorial(n)
        terms.append(n*math.log(float(v))-float(v)-math.log(factorial))
    return sum(terms),tuple(terms)


def expectation_recurrence(mu,alpha,horizon=EXPECTATION_HORIZON):
    """Expected counts under the hypothetical feedback model, no observations."""
    mu,alpha=params(mu,alpha)
    if isinstance(horizon,bool) or not isinstance(horizon,int) or horizon<0:
        raise ValueError("horizon must be nonnegative integer")
    previous=F(0)
    output=[]
    for _ in range(horizon+1):
        previous=mu+alpha*previous
        output.append(previous)
    return tuple(output)


def expectation_geometric(mu,alpha,horizon=EXPECTATION_HORIZON):
    """Independent exact finite sum that never calls the recurrence solver."""
    mu,alpha=params(mu,alpha)
    if isinstance(horizon,bool) or not isinstance(horizon,int) or horizon<0:
        raise ValueError("horizon must be nonnegative integer")
    return tuple(mu*sum((alpha**k for k in range(t+1)),F(0))
                 for t in range(horizon+1))


def stationary_mean(mu,alpha):
    mu,alpha=params(mu,alpha)
    return None if alpha==1 else mu/(1-alpha)


def full_result():
    worlds=[]
    for hi,history in enumerate(ARTIFICIAL_HISTORIES):
        for mi,mu in enumerate(MU_GRID):
            for ai,alpha in enumerate(ALPHA_GRID):
                intensity=intensities(history,mu,alpha)
                score,parts=log_score_gamma(history,mu,alpha)
                independent,iparts=log_score_factorial(history,mu,alpha)
                if abs(score-independent)>=1e-12:
                    raise AssertionError("two independent Poisson log scores disagree")
                if any(abs(x-y)>=1e-12 for x,y in zip(parts,iparts)):
                    raise AssertionError("per-step score mismatch")
                worlds.append({
                    "case_id":f"h{hi}_m{mi}_a{ai}",
                    "history_id":hi,
                    "observed_artificial_counts":list(history),
                    "mu":str(mu),"alpha":str(alpha),
                    "conditional_lambdas":[str(v) for v in intensity],
                    "log_score_terms":[round(x,12) for x in parts],
                    "total_log_score":round(score,12),
                    "factorial_score_matches_gamma":True
                })
    if len(worlds)!=60 or len({w["case_id"] for w in worlds})!=60:
        raise AssertionError("frozen scenarios not exhaustive")
    exp=[]
    for mu in MU_GRID:
        for alpha in ALPHA_GRID:
            direct=expectation_recurrence(mu,alpha)
            geom=expectation_geometric(mu,alpha)
            if direct!=geom:
                raise AssertionError("expected count closed-form exact mismatch")
            exp.append({"mu":str(mu),"alpha":str(alpha),
                        "mean_by_t0_to_t12":[str(x) for x in direct],
                        "stationary_mean":None if alpha==1 else str(mu/(1-alpha))})
    return {
        "research_id":"R158",
        "evidence":"E1_SYNTHETIC_POISSON_COUNT_MATH",
        "not_exact_hawkes_or_original_INGARCH":True,
        "historical_conflict_data_used":False,
        "real_event_predictive_accuracy_tested":False,
        "causal_self_excitation_established":False,
        "world_count":60,"forecast_periods_per_world":8,
        "hypothetical_conditional_model":"Poisson(mu + alpha * previous_period_count), prev(-1)=0",
        "worlds":worlds,
        "independent_expectation_paths":exp,
        "negative_controls":{
            "all_zero_history_is_alpha_independent":all(
                log_score_gamma(ARTIFICIAL_HISTORIES[0],F(1),x)[0]==
                log_score_gamma(ARTIFICIAL_HISTORIES[0],F(1),F(0))[0] for x in ALPHA_GRID),
            "history_H1_mu1_feedback_point5_log_score_difference":
                round(log_score_gamma(ARTIFICIAL_HISTORIES[1],1,F(1,2))[0]-
                      log_score_gamma(ARTIFICIAL_HISTORIES[1],1,0)[0],12),
            "history_H2_mu_point5_feedback_point5_log_score_difference":
                round(log_score_gamma(ARTIFICIAL_HISTORIES[2],F(1,2),F(1,2))[0]-
                      log_score_gamma(ARTIFICIAL_HISTORIES[2],F(1,2),0)[0],12),
            "alpha_one_mu1_t12_mean":str(expectation_geometric(1,1)[-1]),
            "alpha_three_quarters_mu1_stationary_mean":str(stationary_mean(1,F(3,4)))
        }
    }


def main():
    print(json.dumps(full_result(),indent=2,sort_keys=True,ensure_ascii=False))


if __name__=="__main__":
    main()
