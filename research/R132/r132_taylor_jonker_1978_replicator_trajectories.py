#!/usr/bin/env python3
"""R132: original Taylor/Jonker (1978) Eq2 versus Eq3 and full 2-type paths.

First-party original PDF, printed page149 Eq(2),(3),(4), page150 stability:
https://public.ek-cer.hu/~szabo/EGT20/library/taylor_mbs78.pdf
DOI 10.1016/0025-5564(78)90077-9.
Matrices HAWK/STAG/LOGISTIC are PROJECT-CHOSEN mathematical scenarios.
Numerical Euler is NOT the 1978 original discrete-generation Eq3.
Analytic/implicit original scalar ODE solutions independent from RK4.
No human or original animal time series is used; E2=0.
"""
from __future__ import annotations

from fractions import Fraction as F
from math import ceil, exp, isfinite, log
import json


class ReplicatorAuditError(ValueError):
    pass


PROJECT_GAMES={
    "Hawk-Dove":((F(-2),F(2)),(F(0),F(1))),
    "Stag-Hunt":((F(4),F(0)),(F(3),F(3))),
    "Logistic-control":((F(2),F(2)),(F(1),F(1))),
}
INITIALS=(F(1,10),F(1,4),F(2,5),F(3,5),F(4,5),F(9,10))
TIMES=(F(1,4),F(1,2),F(1),F(2),F(3),F(4),F(5),
       F(6),F(8),F(10),F(12),F(16))


def matrix_2x2(A):
    if type(A) not in (tuple,list) or len(A)!=2:
        raise ReplicatorAuditError("R132_EXPLICIT_TWO_BY_TWO_GAME_REQUIRED")
    if any(type(row) not in (tuple,list) or len(row)!=2
           or any(type(v) is not F for v in row) for row in A):
        raise ReplicatorAuditError("R132_PAYOFF_VALUES_EXACT_FRACTIONS_ONLY")
    return tuple(tuple(row) for row in A)


def share_fraction(x):
    if type(x) is not F or not F(0)<=x<=F(1):
        raise ReplicatorAuditError("R132_STRICT_FRACTION_SIMPLEX_0_TO1")
    return x


def scalar_payoffs(A,x):
    """Direct full 2x2 payoff summation, independently of cubic coefficients."""
    ((a,b),(c,d))=matrix_2x2(A)
    x=share_fraction(x)
    y=1-x
    return a*x+b*y,c*x+d*y


def cubic_coefficients(A):
    ((a,b),(c,d))=matrix_2x2(A)
    return a-b-c+d,b-d


def exact_continuous_original_eq2(A,x):
    """Direct F_A and Fbar of Taylor/Jonker p149 Eq2, exact Fraction."""
    x=share_fraction(x)
    FA,FB=scalar_payoffs(A,x)
    mean=x*FA+(1-x)*FB
    return x*(FA-mean),(1-x)*(FB-mean)


def independent_exact_cubic_field(A,x):
    """Separate algebraic implementation of x(1-x)[alpha*x+beta]."""
    x=share_fraction(x)
    alpha,beta=cubic_coefficients(A)
    f=x*(1-x)*(alpha*x+beta)
    return f,-f


def original_1978_discrete_generation(A,x):
    """EXACT Taylor/Jonker 1978 p149 Eq3, NOT Euler and NOT x*F/mean.

    Fail closed unless ALL potential types have nonnegative fertility
    multipliers 1+F_i, including currently absent strategies.
    """
    x=share_fraction(x)
    FA,FB=scalar_payoffs(A,x)
    wa,wb=1+FA,1+FB
    mean=wa*x+wb*(1-x)
    if wa<0 or wb<0 or mean<=0:
        raise ReplicatorAuditError("R132_ORIGINAL_DISCRETE_BIRTH_MULTIPLIER_NEGATIVE")
    return share_fraction(x*wa/mean)


def original_1978_eq4_increment_independent(A,x):
    """Compute original Eq4 directly, not from calling Eq3 and subtract."""
    x=share_fraction(x)
    FA,FB=scalar_payoffs(A,x)
    mean=x*FA+(1-x)*FB
    if 1+FA<0 or 1+FB<0 or 1+mean<=0:
        raise ReplicatorAuditError("R132_ORIGINAL_EQ4_FITNESS_DOMAIN")
    return x*(FA-mean)/(1+mean)


def shift_all_payoffs(A,amount):
    A=matrix_2x2(A)
    if type(amount) is not F:
        raise ReplicatorAuditError("R132_EXACT_COMMON_PAYOFF_BASELINE")
    return tuple(tuple(v+amount for v in row) for row in A)


def _numeric_share(x):
    if type(x) is not float or not isfinite(x) or not 0<=x<=1:
        raise ReplicatorAuditError("R132_FINITE_FLOAT_NUMERICAL_SHARE_REQUIRED")
    return x


def _numeric_time(t):
    if type(t) is not float or not isfinite(t) or t<0 or t>20:
        raise ReplicatorAuditError("R132_NUMERIC_TIME_FLOAT_0_TO20")
    return t


def numeric_cubic_f(x,alpha,beta):
    x=_numeric_share(x)
    return x*(1-x)*(alpha*x+beta)


def rk4_continuous_trajectory(A,x0,t,steps):
    """Independent direct explicit RK4 integration, no analytic solver used."""
    A=matrix_2x2(A)
    x=_numeric_share(x0)
    t=_numeric_time(t)
    if type(steps) is not int or not 1<=steps<=20000:
        raise ReplicatorAuditError("R132_RK4_STEPS_1_TO20000_INTEGER")
    h=t/steps
    if h>1/120+1e-14:
        raise ReplicatorAuditError("R132_RK4_CONVERGENCE_STEP_LIMIT")
    a,b=(float(z) for z in cubic_coefficients(A))
    for _ in range(steps):
        k1=numeric_cubic_f(x,a,b)
        k2=numeric_cubic_f(x+h*k1/2,a,b)
        k3=numeric_cubic_f(x+h*k2/2,a,b)
        k4=numeric_cubic_f(x+h*k3,a,b)
        x=_numeric_share(x+h*(k1+2*k2+2*k3+k4)/6)
    return x


def implicit_integral_primitive(x,alpha,beta):
    """Independently integrated separation dx/[x(1-x)(alpha*x+beta)].

    Uses logarithms: unlike the original Eq2 Fraction field it is numerical.
    """
    x=_numeric_share(x)
    if not 0<x<1 or beta==0 or alpha+beta==0 or alpha*x+beta==0:
        raise ReplicatorAuditError("R132_LOG_PRIMITIVE_SINGULAR")
    G=log(x)/beta-log1p_safe_minus_x(x)/(alpha+beta)
    if alpha!=0:
        G-=alpha/(beta*(alpha+beta))*log(abs(alpha*x+beta))
    return G


def log1p_safe_minus_x(x):
    from math import log1p
    return log1p(-x)


def analytical_continuous_value(A,x0,t):
    """Non-RK4 analytic scalar solution; exact logit for logistic case.

    In Hawk/Stag, monotonically invert the mathematically integrated
    implicit equation within the unique equilibrium-delimited basin.
    """
    A=matrix_2x2(A)
    x0=_numeric_share(x0)
    t=_numeric_time(t)
    if t==0 or x0 in (0.0,1.0):
        return x0
    aa,bb=(float(v) for v in cubic_coefficients(A))
    stationary=-bb/aa if aa else None
    if stationary is not None and abs(x0-stationary)<1e-15:
        return stationary
    if aa==0:
        if bb!=1.0:
            raise ReplicatorAuditError("R132_EXPLICIT_LOGISTIC_ONLY_BETA1")
        return 1/(1+((1-x0)/x0)*exp(-t))
    if bb==0 or aa+bb==0:
        raise ReplicatorAuditError("R132_SOURCE_BRANCH_LOG_REQUIRES_NONZERO_ENDPOINT_COEFFICIENTS")
    drift=numeric_cubic_f(x0,aa,bb)
    if drift==0:
        return x0
    roots=[0.0,1.0]
    if stationary is not None and 0<stationary<1:
        roots.append(stationary)
    roots.sort()
    if drift>0:
        limit=min(r for r in roots if r>x0)
        low=x0;high=limit
    else:
        limit=max(r for r in roots if r<x0)
        low=limit;high=x0
    initial_G=implicit_integral_primitive(x0,aa,bb)
    for _ in range(76):
        middle=(low+high)/2
        if middle==low or middle==high:
            break
        tau=implicit_integral_primitive(middle,aa,bb)-initial_G
        if drift>0:
            if tau<t: low=middle
            else: high=middle
        else:
            if tau<t: high=middle
            else: low=middle
    return (low+high)/2


def exact_euler_step(A,x,h):
    """Project-defined Euler, not original paper's discrete generations."""
    A=matrix_2x2(A);x=share_fraction(x)
    if type(h) is not F or h<0:
        raise ReplicatorAuditError("R132_EULER_NONNEGATIVE_EXACT_H")
    y=x+h*independent_exact_cubic_field(A,x)[0]
    if not 0<=y<=1:
        raise ReplicatorAuditError("R132_EULER_LEFT_SIMPLEX_NO_CLAMP_ALLOWED")
    return y


def euler_internal_linear_multiplier(A,x_star,h):
    A=matrix_2x2(A);x=share_fraction(x_star)
    if type(h) is not F or h<0:
        raise ReplicatorAuditError("R132_EULER_H_EXACT_NONNEGATIVE")
    aa,bb=cubic_coefficients(A)
    if x*(1-x)*(aa*x+bb)!=0:
        raise ReplicatorAuditError("R132_STABILITY_ONLY_AT_EXACT_FIXED_POINT")
    derivative=(1-2*x)*(aa*x+bb)+aa*x*(1-x)
    return F(1)+h*derivative


def source_discrete_baseline_counterexample():
    hawk=PROJECT_GAMES["Hawk-Dove"]
    x=F(1,2)
    k0=original_1978_discrete_generation(hawk,x)
    k3=original_1978_discrete_generation(shift_all_payoffs(hawk,F(3)),x)
    if (k0,k3)!=(F(2,5),F(8,17)):
        raise ReplicatorAuditError("R132_P149_DISCRETE_BASELINE_COUNTEREXAMPLE_WRONG")
    for y in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
        if exact_continuous_original_eq2(hawk,y)!=exact_continuous_original_eq2(shift_all_payoffs(hawk,F(3)),y):
            raise ReplicatorAuditError("R132_CONTINUOUS_PAYOFF_TRANSLATION_NOT_INVARIANT")
    return {
        "same_continuous_payoff_differences":True,
        "original_p149_eq3_unshifted_at_half":str(k0),
        "original_p149_eq3_add_three_to_all_payoffs_at_half":str(k3),
        "original_p149_eq3_not_Euler":True,
        "illegal_negative_birth_multipliers_rejected":True,
    }


def project_euler_false_extinction_counterexample():
    hawk=PROJECT_GAMES["Hawk-Dove"]
    x=F(1,2)
    f=independent_exact_cubic_field(hawk,x)[0]
    y=exact_euler_step(hawk,x,F(4))
    low=euler_internal_linear_multiplier(hawk,F(1,3),F(1))
    high=euler_internal_linear_multiplier(hawk,F(1,3),F(4))
    analytical=analytical_continuous_value(hawk,0.5,4.0)
    numerical=rk4_continuous_trajectory(hawk,0.5,4.0,480)
    if f!=F(-1,8) or y!=0 or low!=F(1,3) or high!=F(-5,3):
        raise ReplicatorAuditError("R132_EXACT_EULER_ARTIFACT_VALUES_DRIFTED")
    if not 1/3<analytical<0.5 or abs(numerical-analytical)>1e-6:
        raise ReplicatorAuditError("R132_TRUE_ODE_NOT_AN_INTERIOR_HAWK_TRAJECTORY")
    return {
        "project_Hawk_original_share":"1/2",
        "project_Hawk_exact_continuous_initial_derivative":"-1/8",
        "Euler_h4_one_step_share":"0",
        "true_continuous_t4_share":round(analytical,12),
        "true_continuous_t4_RK4_share":round(numerical,12),
        "Euler_local_multiplier_h1_at_one_third":"1/3",
        "Euler_local_multiplier_h4_at_one_third":"-5/3",
        "Euler_false_extinction_not_original_Taylor_Jonker_1978_Eq3":True,
    }


def exhaustive_exact_field_and_discrete_audit():
    verified=0
    discrete=0
    for A in PROJECT_GAMES.values():
        for k in range(25):
            x=F(k,24)
            direct=exact_continuous_original_eq2(A,x)
            algebraic=independent_exact_cubic_field(A,x)
            if direct!=algebraic or sum(direct,F(0))!=0:
                raise ReplicatorAuditError("R132_1978_EQ2_INDEPENDENT_2X2_FIELD_MISMATCH")
            verified+=1
            # Only legally reproducible states, do not secretly shift payoff.
            fA,fB=scalar_payoffs(A,x)
            if 1+fA>=0 and 1+fB>=0 and 1+x*fA+(1-x)*fB>0:
                xnew=original_1978_discrete_generation(A,x)
                inc=original_1978_eq4_increment_independent(A,x)
                if xnew-x!=inc:
                    raise ReplicatorAuditError("R132_ORIGINAL_1978_EQ3_EQ4_MISMATCH")
                discrete+=1
    if verified!=75:
        raise ReplicatorAuditError("R132_EXPECT_75_EXACT_VECTOR_FIELDS")
    return {"exact_independent_fraction_fields":verified,
            "source_eq3_eq4_valid_state_checks":discrete,
            "original_discrete_reproduction_invalid_states_explicitly_excluded":True}


def exhaustive_216_analytic_vs_RK4():
    checked=0
    worst=0.0
    detail={}
    for name,A in PROJECT_GAMES.items():
        for ini in INITIALS:
            for tF in TIMES:
                x0=float(ini);t=float(tF)
                steps=ceil(t*120)
                computed=rk4_continuous_trajectory(A,x0,t,steps)
                reference=analytical_continuous_value(A,x0,t)
                error=abs(computed-reference)
                if error>1e-6:
                    raise ReplicatorAuditError("R132_RK4_VS_INDEPENDENT_IMPLICIT_CONTINUOUS_MISMATCH")
                worst=max(error,worst)
                checked+=1
                if ini in (F(1,4),F(4,5)) and tF in (F(1),F(4),F(16)):
                    detail[name+":"+str(ini)+":"+str(tF)] = {
                        "rk4":round(computed,12),
                        "independent_analytic":round(reference,12),
                        "absolute_error":round(error,15)
                    }
    if checked!=216:
        raise ReplicatorAuditError("R132_NOT_ALL_216_CONTINUOUS_TRAJECTORY_END_POINTS")
    return {
        "source_continuous_replicator_eq2_with_three_project_payoffs":list(PROJECT_GAMES),
        "initials":[str(v) for v in INITIALS],
        "times":[str(v) for v in TIMES],
        "trajectory_endpoint_independent_comparisons":checked,
        "max_numerical_absolute_error":worst,
        "all_216_errors_less_than_1e_minus_6":True,
        "selected_endpoint_samples":detail,
        "real_human_or_animal_time_series_used":0,
    }


def phase_receipt():
    return {
        "study":"R132","catalogue":"05-008",
        "original_Taylor_Jonker_1978_equations":"p149 Eq2 continuous, Eq3 +1 fitness discrete, Eq4 relation",
        "exact_fraction_2type_field_audit":exhaustive_exact_field_and_discrete_audit(),
        "full_continuous_paths":exhaustive_216_analytic_vs_RK4(),
        "project_numeric_Euler_false_extinction":project_euler_false_extinction_counterexample(),
        "original_discrete_birth_baseline_noninvariance":source_discrete_baseline_counterexample(),
        "new_real_person_E2_prediction_scores":0,"R073":"FROZEN","PESEN_v0_1":"FROZEN",
    }


if __name__=="__main__":
    print(json.dumps(phase_receipt(),sort_keys=True,indent=2))
