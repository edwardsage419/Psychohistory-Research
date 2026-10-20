#!/usr/bin/env python3
"""R132 Taylor & Jonker (1978) p149 Eq2/3/4: source-exact replicator.

Author-hosted original PDF:
https://static1.squarespace.com/static/5dc9917c4cdb1467e1e54c4c/t/6526a5647942e33b89ab7af1/1697031525653/1978%2Bevolutionarily%2Bstable%2Bstrategies%2Band%2Bgame%2Bdynamics.pdf

Primary source: Mathematical Biosciences 40 (1978) 145–156,
DOI 10.1016/0025-5564(78)90077-9, Eq2 continuous flow,
Eq3 discrete REPRODUCTION update with baseline +1, Eq4 increment.

Stag/Hare two-type game from Skyrms 2004 / R128, Chicken from R129,
zero-sum RPS and logistic constant advantage are PROJECT math examples.
Euler and RK4 are NUMERICAL approximations, NOT source discrete Eq3.
No trajectory observations from humans / animals, new real-human E2 = 0.
"""
from __future__ import annotations

from fractions import Fraction as F
from math import exp, isfinite, prod
import json


class ReplicatorDomainError(ValueError):
    pass


def _matrix(A):
    if type(A) not in (list, tuple) or len(A) not in (2,3):
        raise ReplicatorDomainError("R132_REQUIRE_EXPLICIT_2_OR_3_BY_2_OR_3_PAYOFFS")
    n=len(A)
    if any(type(r) not in (list,tuple) or len(r)!=n or any(type(v) is not F for v in r)
           for r in A):
        raise ReplicatorDomainError("R132_ALL_PAYOFFS_EXACT_FRACTION")
    return tuple(tuple(row) for row in A)


def _simplex(x,n):
    if type(x) not in (list,tuple) or len(x)!=n or any(type(v) is not F or v<0 for v in x):
        raise ReplicatorDomainError("R132_EXACT_NONNEGATIVE_N_SIMPLEX")
    if sum(x,F(0))!=1:
        raise ReplicatorDomainError("R132_EXACT_SIMPLEX_NORMALIZATION")
    return tuple(x)


def source_cyclic_1978(eps=F(1,2)):
    if type(eps) is not F or eps<=0 or eps>1:
        raise ReplicatorDomainError("R132_ORIGINAL_EPS_POSITIVE_UP_TO_ONE")
    return ((-eps,F(1),F(-1)),(F(-1),-eps,F(1)),(F(1),F(-1),-eps))


def source_alpha_1978(alpha=F(1)):
    if type(alpha) is not F:
        raise ReplicatorDomainError("R132_ALPHA_MUST_BE_FRACTION")
    return ((F(2),F(1),F(5)),(F(5),alpha,F(0)),(F(1),F(4),F(3)))


def constant_advantage_project():
    return ((F(2),F(2)),(F(1),F(1)))


def skyrms_stag_project_flow():
    return ((F(4),F(0)),(F(3),F(3)))


def chicken_project_flow():
    return ((F(-2),F(2)),(F(0),F(1)))


def zero_sum_rps_project():
    return ((F(0),F(-1),F(1)),(F(1),F(0),F(-1)),(F(-1),F(1),F(0)))


def exact_payoff_each(A,x):
    matrix=_matrix(A);point=_simplex(x,len(matrix))
    return tuple(sum((matrix[i][j]*point[j] for j in range(len(matrix))),F(0))
                 for i in range(len(matrix)))


def source_original_eq2_exact_field(A,x):
    """Original 1978 p149: xdot_i=x_i(F_i-Fbar), exact rational."""
    matrix=_matrix(A);point=_simplex(x,len(matrix))
    fitness=exact_payoff_each(matrix,point)
    mean=sum((a*b for a,b in zip(point,fitness)),F(0))
    deriv=tuple(point[i]*(fitness[i]-mean) for i in range(len(point)))
    if sum(deriv,F(0))!=0:
        raise ReplicatorDomainError("R132_PRIMARY_CONTINUOUS_MASS_CONSERVATION_BROKEN")
    return deriv


def exact_eq2_independent_pairwise_field(A,x):
    """Independent exact unordered payoff differences, no source Eq2 call.

    xdot_i=x_i * sum_j x_j * (F_i-F_j), constructed from matrix double sums.
    """
    matrix=_matrix(A);point=_simplex(x,len(matrix))
    n=len(point)
    derivative=tuple(
        point[i]*sum((
            point[j]*sum(((matrix[i][k]-matrix[j][k])*point[k]
                          for k in range(n)),F(0))
            for j in range(n)),F(0))
        for i in range(n))
    if sum(derivative,F(0))!=0:
        raise ReplicatorDomainError("R132_INDEPENDENT_PAIRWISE_MASS_INVARIANT_BROKEN")
    return derivative


def source_original_eq3_exact_generation(A,x):
    """NOT forward Euler. Original p149 reproduction baseline 1+fitness."""
    matrix=_matrix(A);point=_simplex(x,len(matrix))
    fitness=exact_payoff_each(matrix,point)
    base=tuple(F(1)+f for f in fitness)
    average=sum((point[i]*base[i] for i in range(len(point))),F(0))
    if average<=0 or any(z<0 for z in base):
        raise ReplicatorDomainError("R132_SOURCE_DISCRETE_NEGATIVE_REPRODUCTION_WEIGHT")
    out=tuple(point[i]*base[i]/average for i in range(len(point)))
    return _simplex(out,len(matrix))


def source_original_eq4_exact_increment(A,x):
    """Separate Taylor–Jonker p149 delta Eq4; return xnext-x, exact."""
    matrix=_matrix(A);point=_simplex(x,len(matrix))
    fitness=exact_payoff_each(matrix,point)
    mean=sum((point[i]*fitness[i] for i in range(len(point))),F(0))
    if F(1)+mean<=0 or any(F(1)+v<0 for v in fitness):
        raise ReplicatorDomainError("R132_EQ4_REPRODUCTION_DENOMINATOR_OR_MULTIPLIER_INVALID")
    return tuple(point[i]*(fitness[i]-mean)/(F(1)+mean) for i in range(len(point)))


def exact_two_type_scalar_derivative(A,x):
    """Independent reduction: x'(t)=x(1-x)*(fitness_0-fitness_1)."""
    matrix=_matrix(A)
    if len(matrix)!=2 or type(x) is not F or not F(0)<=x<=F(1):
        raise ReplicatorDomainError("R132_TWO_TYPE_EXACT_SCALAR_SHARE")
    other=1-x
    advantage=x*(matrix[0][0]-matrix[1][0])+other*(matrix[0][1]-matrix[1][1])
    return x*other*advantage


def exact_two_type_equilibria_and_direction(A):
    """Frozen exact sign witnesses; not deducing global dynamics from samples."""
    matrix=_matrix(A)
    if len(matrix)!=2:
        raise ReplicatorDomainError("R132_TWO_TYPE_ONLY")
    # Δf(x) = u + v*x. Fixed endpoints x=0,1, and optional interior root.
    u=matrix[0][1]-matrix[1][1]
    v=(matrix[0][0]-matrix[1][0])-u
    interior=-u/v if v else None
    if interior is not None and not F(0)<interior<F(1):
        interior=None
    return {
        "payoff_difference_constant":u,
        "payoff_difference_linear":v,
        "interior_fixed_point":interior,
        "at_quarter":exact_two_type_scalar_derivative(matrix,F(1,4)),
        "at_half":exact_two_type_scalar_derivative(matrix,F(1,2)),
        "at_four_fifths":exact_two_type_scalar_derivative(matrix,F(4,5)),
    }


def exact_replicator_invariant_grid():
    """28 3-simplex rational states per matrix, three matrices = 84."""
    matrices=(source_cyclic_1978(),source_alpha_1978(),zero_sum_rps_project())
    count=0
    shift_checks=0
    scale_checks=0
    zero_support_checks=0
    original_discrete_agreement_checks=0
    for A in matrices:
        for i in range(7):
            for j in range(7-i):
                p=(F(i,6),F(j,6),F(6-i-j,6))
                xdot=source_original_eq2_exact_field(A,p)
                other=exact_eq2_independent_pairwise_field(A,p)
                if xdot!=other:
                    raise ReplicatorDomainError("R132_TWO_INDEPENDENT_EQ2_IMPLEMENTATIONS_DISAGREE")
                if any(xdot[k]!=0 for k in range(3) if p[k]==0):
                    raise ReplicatorDomainError("R132_ABSENT_TYPE_SPONTANEOUSLY_CREATED")
                zero_support_checks+=1
                orig_next=source_original_eq3_exact_generation(A,p)
                orig_incr=source_original_eq4_exact_increment(A,p)
                if tuple(p[k]+orig_incr[k] for k in range(3))!=orig_next:
                    raise ReplicatorDomainError("R132_ORIGINAL_DISCRETE_EQ3_EQ4_DIVERGE")
                original_discrete_agreement_checks+=1
                for c in (F(-1),F(0),F(2)):
                    shifted=tuple(tuple(v+c for v in row) for row in A)
                    if source_original_eq2_exact_field(shifted,p)!=xdot:
                        raise ReplicatorDomainError("R132_CONSTANT_PAYOFF_SHIFT_CHANGED_EQ2")
                    shift_checks+=1
                for scale in (F(1,2),F(2),F(3)):
                    scaled=tuple(tuple(scale*v for v in row) for row in A)
                    if source_original_eq2_exact_field(scaled,p)!=tuple(scale*v for v in xdot):
                        raise ReplicatorDomainError("R132_PAYOFF_SCALE_TIME_RESCALE_FAILED")
                    scale_checks+=1
                count+=1
    if (count,shift_checks,scale_checks)!=(84,252,252):
        raise ReplicatorDomainError("R132_INVARIANT_GRID_COVERAGE_DRIFT")
    return {
        "three_strategy_simplex_states_per_matrix":28,
        "payoff_matrices_checked":3,
        "exact_field_vs_independent_pairwise_comparisons":count,
        "source_1978_original_eq3_vs_eq4_increment_checks":original_discrete_agreement_checks,
        "absence_boundary_preservation_checks":zero_support_checks,
        "constant_payoff_shift_invariance_checks":shift_checks,
        "positive_payoff_time_scale_checks":scale_checks
    }


def logistic_constant_advantage_closed(x0,t):
    """Project exact solution for dx/dt=x(1-x); float only for exp."""
    if type(x0) is not float or not isfinite(x0) or not 0<=x0<=1:
        raise ReplicatorDomainError("R132_LOGISTIC_INITIAL_SHARE_FLOAT")
    if type(t) not in (float,int) or not isfinite(t) or t<0 or t>20:
        raise ReplicatorDomainError("R132_LOGISTIC_TIME_NONNEGATIVE")
    if x0 in (0.0,1.0):
        return x0
    return 1.0/(1.0+(1.0-x0)/x0*exp(-t))


def _numeric_initial(A,x0,time,steps,method):
    matrix=_matrix(A)
    if type(x0) not in (tuple,list) or len(x0)!=len(matrix):
        raise ReplicatorDomainError("R132_NUMERIC_INITIAL_SIMPLEX_SHAPE")
    if any(type(v) is not float or not isfinite(v) or not 0<=v<=1 for v in x0):
        raise ReplicatorDomainError("R132_NUMERIC_EXPLICIT_FINITE_FLOAT_SHARES")
    if abs(sum(x0)-1.0)>1e-12:
        raise ReplicatorDomainError("R132_NUMERIC_SIMPLEX_NOT_NORMALIZED")
    if type(time) is not float or not isfinite(time) or time<=0 or time>20:
        raise ReplicatorDomainError("R132_NUMERIC_TIME_POSITIVE_FLOAT")
    if type(steps) is not int or not 1<=steps<=4096 or time/steps>0.5:
        raise ReplicatorDomainError("R132_NUMERIC_STEPS_POSITIVE_AND_DT_LE_HALF")
    if method not in ("euler","rk4") or type(method) is not str:
        raise ReplicatorDomainError("R132_NUMERIC_METHOD_EULER_OR_RK4")
    return tuple(tuple(float(v) for v in row) for row in matrix)


def _field_float(A,x):
    n=len(x)
    f=[sum(A[i][j]*x[j] for j in range(n)) for i in range(n)]
    avg=sum(x[i]*f[i] for i in range(n))
    return tuple(x[i]*(f[i]-avg) for i in range(n))


def _numeric_single_step(A,x,h,method):
    f=lambda xx:_field_float(A,xx)
    k1=f(x)
    if method=="euler":
        return tuple(x[i]+h*k1[i] for i in range(len(x)))
    xx2=tuple(x[i]+h*k1[i]/2 for i in range(len(x)))
    k2=f(xx2)
    xx3=tuple(x[i]+h*k2[i]/2 for i in range(len(x)))
    k3=f(xx3)
    xx4=tuple(x[i]+h*k3[i] for i in range(len(x)))
    k4=f(xx4)
    return tuple(x[i]+h*(k1[i]+2*k2[i]+2*k3[i]+k4[i])/6 for i in range(len(x)))


def numerical_trajectory(A,x0,time,steps,method,record=False):
    """Numerical approximate integrators are NOT author original Eq3/4."""
    a=_numeric_initial(A,x0,time,steps,method)
    x=tuple(x0);dt=time/steps;path=[x] if record else None
    for k in range(steps):
        x=_numeric_single_step(a,x,dt,method)
        if any(not isfinite(v) or v < -1e-8 or v>1+1e-8 for v in x):
            raise ReplicatorDomainError("R132_NUMERIC_INTEGRATOR_LEFT_SIMPLEX")
        if abs(sum(x)-1.0)>1e-9:
            raise ReplicatorDomainError("R132_NUMERIC_INTEGRATOR_MASS_DRIFT")
        if record:
            path.append(x)
    return tuple(path) if record else x


def exact_two_type_source_based_sign_audit():
    expected={
        "constant_advantage":{
            "interior":None,"at_quarter":F(3,16),
            "at_half":F(1,4),"at_four_fifths":F(4,25)
        },
        "stag_hare":{
            "interior":F(3,4),"at_quarter":F(-3,8),
            "at_half":F(-1,4),"at_four_fifths":F(4,125)
        },
        "chicken":{
            "interior":F(1,3),"at_quarter":F(3,64),
            "at_half":F(-1,8),"at_four_fifths":F(-28,125)
        }
    }
    models={"constant_advantage":constant_advantage_project(),
            "stag_hare":skyrms_stag_project_flow(),
            "chicken":chicken_project_flow()}
    out={}
    for name,A in models.items():
        y=exact_two_type_equilibria_and_direction(A)
        want=expected[name]
        if y["interior_fixed_point"]!=want["interior"]:
            raise ReplicatorDomainError("R132_TWO_TYPE_INTERIOR_FIXED_POINT_NOT_MATCHING")
        for key in ("at_quarter","at_half","at_four_fifths"):
            if y[key]!=want[key]:
                raise ReplicatorDomainError("R132_TWO_TYPE_EXACT_VECTOR_FIELD_WRONG")
        # All 13 rational x on grid: independent full-2D original Eq2 and scalar
        for k in range(13):
            x=F(k,12)
            direct=source_original_eq2_exact_field(A,(x,1-x))
            reduced=exact_two_type_scalar_derivative(A,x)
            if direct!=(reduced,-reduced):
                raise ReplicatorDomainError("R132_TWO_TYPE_REDUCTION_NOT_INDEPENDENT")
        out[name]={
            "exact_interior_fixed_point":None if y["interior_fixed_point"] is None else str(y["interior_fixed_point"]),
            "quarter_derivative":str(y["at_quarter"]),
            "half_derivative":str(y["at_half"]),
            "four_fifths_derivative":str(y["at_four_fifths"])
        }
    return {"two_type_models":out,"two_type_13_grid_cross_checks":39}


def numerical_replicator_audit():
    constant=constant_advantage_project()
    true=logistic_constant_advantage_closed(0.25,2.0)
    euler_errors=[]
    rk4_errors=[]
    for n in (40,80,160,320):
        euler=numerical_trajectory(constant,(0.25,0.75),2.0,n,"euler")[0]
        rk4=numerical_trajectory(constant,(0.25,0.75),2.0,n,"rk4")[0]
        euler_errors.append(abs(euler-true))
        rk4_errors.append(abs(rk4-true))
    if not all(euler_errors[i+1]<euler_errors[i] for i in range(3)):
        raise ReplicatorDomainError("R132_EULER_LOGISTIC_NOT_CONVERGING")
    if not all(rk4_errors[i+1]<rk4_errors[i] for i in range(3)):
        raise ReplicatorDomainError("R132_RK4_LOGISTIC_NOT_CONVERGING")
    if rk4_errors[-1]>=1e-11 or euler_errors[-1]<=rk4_errors[-1]*100:
        raise ReplicatorDomainError("R132_INDEPENDENT_LOGISTIC_SOLUTION_RK4_ACCURACY")

    stag=skyrms_stag_project_flow()
    chicken=chicken_project_flow()
    stag_lo=numerical_trajectory(stag,(0.5,0.5),8.0,320,"rk4")[0]
    stag_hi=numerical_trajectory(stag,(0.8,0.2),8.0,320,"rk4")[0]
    chicken_lo=numerical_trajectory(chicken,(0.1,0.9),8.0,320,"rk4")[0]
    chicken_hi=numerical_trajectory(chicken,(0.8,0.2),8.0,320,"rk4")[0]
    if not (0<stag_lo<0.5 and 0.8<stag_hi<1):
        raise ReplicatorDomainError("R132_STAG_BASIN_DIRECTION_INVALID")
    if not (0.1<chicken_lo<F(1,3) and F(1,3)<chicken_hi<0.8):
        raise ReplicatorDomainError("R132_CHICKEN_MIXED_BASIN_DIRECTION_INVALID")

    rps=zero_sum_rps_project()
    initial=(0.5,0.3,0.2)
    p0=prod(initial)
    if abs(p0-0.03)>1e-15:
        raise ReplicatorDomainError("R132_RPS_INITIAL_PRODUCT")
    rps_comparison={}
    for n in (40,80,160,320):
        eu=numerical_trajectory(rps,initial,12.0,n,"euler")
        rk=numerical_trajectory(rps,initial,12.0,n,"rk4")
        de=prod(eu)-p0;dr=prod(rk)-p0
        if not (de<0 and abs(dr)<abs(de)):
            raise ReplicatorDomainError("R132_EULER_SPURIOUS_SPIRAL_NOT_VISIBLE")
        rps_comparison[str(n)]={
            "euler_final_product":prod(eu),
            "rk4_final_product":prod(rk),
            "euler_product_error":de,
            "rk4_product_error":dr,
        }
    if abs(rps_comparison["320"]["rk4_product_error"])>=1e-9:
        raise ReplicatorDomainError("R132_RK4_RPS_CONSERVATION_INSUFFICIENT")
    if not abs(rps_comparison["320"]["euler_product_error"])>1e-4:
        raise ReplicatorDomainError("R132_EULER_RPS_ARTIFICIAL_INVARIANT_CHANGE_NOT_EXPOSED")
    return {
        "constant_advantage_exact_logistic_t2":true,
        "logistic_euler_absolute_errors":euler_errors,
        "logistic_RK4_absolute_errors":rk4_errors,
        "stag_hare_t8_initial_half_final":stag_lo,
        "stag_hare_t8_initial_four_fifths_final":stag_hi,
        "chicken_t8_initial_one_tenth_final":chicken_lo,
        "chicken_t8_initial_four_fifths_final":chicken_hi,
        "project_zero_sum_RPS_initial_product":p0,
        "project_RPS_exact_continuous_product_invariant":"3/100",
        "numeric_T12_RPS_comparison":rps_comparison,
        "this_numerical_drift_is_not_original_Taylor_Jonker_discrete_Eq3":True,
    }


def phase_receipt():
    return {
        "research_id":"R132","catalogue_id":"05-008",
        "original_source_1978_84_three_strategy_exact_audits":exact_replicator_invariant_grid(),
        "two_strategy_exact_field_and_basin_signs":exact_two_type_source_based_sign_audit(),
        "complete_finite_trajectories_with_independent_logistic_and_RPS_checks":numerical_replicator_audit(),
        "original_1978_full_population_nonlinear_phase_portraits_recreated":False,
        "real_animal_or_human_time_series_fitted":False,
        "new_real_human_E2_prediction_scores":0,
        "R073":"FROZEN","PESEN_v0_1":"FROZEN",
    }


if __name__=="__main__":
    print(json.dumps(phase_receipt(),sort_keys=True,indent=2))
