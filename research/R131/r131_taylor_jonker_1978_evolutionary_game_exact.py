#!/usr/bin/env python3
"""R131 Taylor & Jonker 1978 exact finite matrix-game stability audit.

Original *Evolutionarily Stable Strategies and Game Dynamics*,
Mathematical Biosciences 40:145–156, DOI 10.1016/0025-5564(78)90077-9.
FULL ORIGINAL PDF linked FROM original author Peter Taylor publication page:
https://sites.google.com/view/peter-taylor/biology/publications
p147 Eq1 ESS invasion; p149 Eq2 (continuous) Eq3 (discrete, fitness+1);
p150 epsilon cyclic matrix ESS/continuous stable/discrete unstable;
p151 alpha-game continuous stable but NOT ESS.
PROJECT FINITE MORAN drift appendix is NOT from Taylor-Jonker 1978.
No real animal/human observations, no E2 and no R132 trajectory study.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import json


class EvolutionaryAuditError(ValueError):
    pass


def _matrix(matrix):
    if type(matrix) not in (tuple,list) or len(matrix)!=3:
        raise EvolutionaryAuditError("R131_EXPLICIT_THREE_BY_THREE_MATRIX")
    rows=[]
    for row in matrix:
        if type(row) not in (tuple,list) or len(row)!=3 or any(type(v) is not F for v in row):
            raise EvolutionaryAuditError("R131_THREE_BY_THREE_EXACT_FRACTION_PAYOFFS")
        rows.append(tuple(row))
    return tuple(rows)


def _simplex(v):
    if type(v) not in (tuple,list) or len(v)!=3 or any(type(x) is not F or x<0 for x in v):
        raise EvolutionaryAuditError("R131_THREE_SIMPLEX_EXACT_NONNEGATIVE_FRACTIONS")
    if sum(v,F(0))!=1:
        raise EvolutionaryAuditError("R131_SIMPLEX_PROBABILITIES_MUST_SUM_TO_ONE")
    return tuple(v)


def _fraction_probability(eps, strict_positive=False):
    if type(eps) is not F or not F(0)<=eps<=F(1) or (strict_positive and eps==0):
        raise EvolutionaryAuditError("R131_MUTANT_SHARE_EXACT_FRACTION_ZERO_TO_ONE")
    return eps


def dot(x,y):
    return sum((a*b for a,b in zip(x,y)),F(0))


def source_1978_cyclic_matrix(epsilon):
    """Source p150 cyclic 3x3, epsilon >0 <=1 chosen for safe discrete."""
    if type(epsilon) is not F or not F(0)<epsilon<=F(1):
        raise EvolutionaryAuditError("R131_SOURCE_EPSILON_STRICT_POSITIVE_LE_ONE")
    return ((-epsilon,F(1),F(-1)),
            (F(-1),-epsilon,F(1)),
            (F(1),F(-1),-epsilon))


def source_1978_alpha_matrix(alpha):
    """Exact original p151 payoff matrix for its α example."""
    if type(alpha) is not F:
        raise EvolutionaryAuditError("R131_SOURCE_ALPHA_EXACT_FRACTION")
    return ((F(2),F(1),F(5)),
            (F(5),alpha,F(0)),
            (F(1),F(4),F(3)))


def alpha_interior_equilibrium(alpha):
    """Algebraic equality A*p = constant * 1; original -8<α<17/2."""
    if type(alpha) is not F or not F(-8)<alpha<F(17,2):
        raise EvolutionaryAuditError("R131_SOURCE_ALPHA_INTERIOR_EQ_RANGE")
    den=F(36)-alpha
    return _simplex(((F(17)-2*alpha)/den,F(11)/den,(alpha+8)/den))


def payoff_each(matrix,p):
    m=_matrix(matrix);p=_simplex(p)
    return tuple(dot(row,p) for row in m)


def population_mean_payoff(matrix,p):
    """Direct average of all 9 ordered pair types, not dot(payoff_each)."""
    m=_matrix(matrix);p=_simplex(p)
    return sum((p[i]*m[i][j]*p[j] for i in range(3) for j in range(3)),F(0))


def mix_population(p,q,mu):
    x=_simplex(p);y=_simplex(q);u=_fraction_probability(mu)
    return tuple((1-u)*x[i]+u*y[i] for i in range(3))


def invasion_advantage_direct(matrix,p,q,mu):
    """Original definition F(q|mixed)-F(p|mixed)."""
    m=_matrix(matrix);p=_simplex(p);q=_simplex(q)
    mixed=mix_population(p,q,mu)
    val=lambda action:sum((action[i]*m[i][j]*mixed[j]
                           for i in range(3) for j in range(3)),F(0))
    return val(q)-val(p)


def invasion_advantage_independent_expansion(matrix,p,q,mu):
    """Original p147 Eq1 exact for linear games; not calling direct routine."""
    m=_matrix(matrix);p=_simplex(p);q=_simplex(q);u=_fraction_probability(mu)
    diff=tuple(q[i]-p[i] for i in range(3))
    base=sum((diff[i]*m[i][j]*p[j] for i in range(3) for j in range(3)),F(0))
    quadratic=sum((diff[i]*m[i][j]*diff[j] for i in range(3) for j in range(3)),F(0))
    return base+u*quadratic


def continuous_original_eq2_field(matrix,p):
    """1978 p149 Eq2; finite algebraic field evaluation ONLY, no trajectories."""
    m=_matrix(matrix);p=_simplex(p)
    f=payoff_each(m,p)
    avg=population_mean_payoff(m,p)
    result=tuple(p[i]*(f[i]-avg) for i in range(3))
    if sum(result,F(0))!=0:
        raise EvolutionaryAuditError("R131_CONTINUOUS_SIMPLEX_MASS_NOT_CONSERVED")
    return result


def discrete_original_eq3_one_generation(matrix,p):
    """Original p149 Eq3: s_i*(1+F_i)/(1+Fbar); never F_i/Fbar."""
    m=_matrix(matrix);p=_simplex(p)
    f=payoff_each(m,p)
    base=tuple(F(1)+y for y in f)
    meanbase=F(1)+population_mean_payoff(m,p)
    if meanbase<=0 or any(y<0 for y in base):
        raise EvolutionaryAuditError("R131_DISCRETE_SOURCE_NEGATIVE_REPRODUCTION_MULTIPLIER")
    return _simplex(tuple(p[i]*base[i]/meanbase for i in range(3)))


def _simplex_2d(u,v):
    if type(u) is not F or type(v) is not F:
        raise EvolutionaryAuditError("R131_SIMPLEX_TANGENT_EXACT_FRACTIONS")
    return _simplex((u,v,F(1)-u-v))


def tangent_analytic_continuous_jacobian(matrix,p):
    """Exact differentiating x_i[(A*x)_i - x^T A x], i=0,1 on simplex."""
    A=_matrix(matrix);p=_simplex(p)
    f=payoff_each(A,p)
    avg=population_mean_payoff(A,p)
    out=[]
    for i in (0,1):
        row=[]
        for j in (0,1):
            df=A[i][j]-A[i][2]
            dbar=f[j]-f[2]+sum((p[k]*(A[k][j]-A[k][2]) for k in range(3)),F(0))
            row.append((f[i]-avg if i==j else F(0))+p[i]*(df-dbar))
        out.append(tuple(row))
    return tuple(out)


def tangent_independent_exact_polynomial_jacobian(matrix,p):
    """Richardson center differences EXACT for cubic vector field.

    For polynomial degree<=3, [4D(h/2)-D(h)]/3 removes all h^2 terms.
    Independent from symbolic Jacobian formula, not float approximation.
    """
    A=_matrix(matrix);p=_simplex(p)
    h=F(1,100)
    jac=[[F(0),F(0)] for _ in range(2)]
    for j in range(2):
        def d(stepsize):
            plus=[p[0],p[1]]
            minus=[p[0],p[1]]
            plus[j]+=stepsize
            minus[j]-=stepsize
            pos=continuous_original_eq2_field(A,_simplex_2d(*plus))
            neg=continuous_original_eq2_field(A,_simplex_2d(*minus))
            return tuple((pos[i]-neg[i])/(2*stepsize) for i in range(2))
        large=d(h);small=d(h/2)
        for i in range(2):
            jac[i][j]=(4*small[i]-large[i])/3
    return tuple(tuple(row) for row in jac)


def trace_and_det_two_by_two(J):
    return {"trace":J[0][0]+J[1][1],
            "determinant":J[0][0]*J[1][1]-J[0][1]*J[1][0]}


def discrete_tangent_linearization_from_original_eq3(matrix,p):
    """At exact internal fixed point: D_discrete=I+J_cont/(1+mean F).

    Only valid at fixed point with all existing supports and multiplier>0.
    """
    A=_matrix(matrix);p=_simplex(p)
    if any(x==0 for x in p):
        raise EvolutionaryAuditError("R131_TANGENT_FULL_SUPPORT_ONLY")
    if continuous_original_eq2_field(A,p)!=(F(0),)*3:
        raise EvolutionaryAuditError("R131_JACOBIAN_SPECIAL_FORM_REQUIRES_EQ_POINT")
    mean_base=1+population_mean_payoff(A,p)
    if mean_base<=0:
        raise EvolutionaryAuditError("R131_ORIGINAL_DISCRETE_FITNESS_BASE_NONPOSITIVE")
    J=tangent_analytic_continuous_jacobian(A,p)
    return tuple(tuple((F(1) if i==j else F(0))+J[i][j]/mean_base
                       for j in (0,1)) for i in (0,1))


def original_cyclic_counterexample_audit():
    epsilon=F(1,2)
    A=source_1978_cyclic_matrix(epsilon)
    p=(F(1,3),)*3
    if payoff_each(A,p)!=(F(-1,6),)*3:
        raise EvolutionaryAuditError("R131_ORIGINAL_CYCLIC_EQ_PAYOFF_NOT_SOURCE")
    if discrete_original_eq3_one_generation(A,p)!=p:
        raise EvolutionaryAuditError("R131_ORIGINAL_CYCLIC_DISCRETE_FIXED_POINT_FAILED")
    if continuous_original_eq2_field(A,p)!=(F(0),)*3:
        raise EvolutionaryAuditError("R131_ORIGINAL_CYCLIC_CONTINUOUS_FIXED_POINT_FAILED")
    jac=tangent_analytic_continuous_jacobian(A,p)
    cross=tangent_independent_exact_polynomial_jacobian(A,p)
    if jac!=cross:
        raise EvolutionaryAuditError("R131_ORIGINAL_CYCLIC_JACOBIAN_INDEPENDENT_DERIVATIVES_DISAGREE")
    tr=trace_and_det_two_by_two(jac)
    disc=discrete_tangent_linearization_from_original_eq3(A,p)
    dr=trace_and_det_two_by_two(disc)
    if tr["trace"]!=F(-1,3) or tr["determinant"]!=F(13,36):
        raise EvolutionaryAuditError("R131_CYCLIC_CONTINUOUS_SOURCE_LINEARIZATION_INCORRECT")
    if dr["trace"]!=F(8,5) or dr["determinant"]!=F(28,25):
        raise EvolutionaryAuditError("R131_CYCLIC_DISCRETE_OVERSHOOT_INCORRECT")
    if tr["trace"]>=0 or tr["determinant"]<=0 or dr["determinant"]<=1:
        raise EvolutionaryAuditError("R131_CYCLIC_STABILITY_DIRECTION_WRONG")
    # ESS for every q≠p: (q-p)^T A(q-p)=−epsilon||q-p||^2.
    # Check one rational witness independently, keep analytic universal proof.
    q=(F(1),F(0),F(0))
    mu=F(1,10)
    gap=invasion_advantage_direct(A,p,q,mu)
    algebra=invasion_advantage_independent_expansion(A,p,q,mu)
    if gap!=algebra or gap>=0:
        raise EvolutionaryAuditError("R131_CYCLIC_INVADER_ADVANTAGE_SIGN")
    return {
        "primary_original_source":"Taylor and Jonker 1978 p150 3x3 cyclic game",
        "matrix_parameter_epsilon":"1/2",
        "primary_exact_payoff_matrix":[[str(v) for v in row] for row in A],
        "equilibrium_p":["1/3","1/3","1/3"],
        "mean_fitness":str(population_mean_payoff(A,p)),
        "universal_linear_game_ESS_proof":"for any q!=p, (q-p)A(q-p)=-(1/2)*sum((q_i-1/3)^2)<0; at p all payoffs tie",
        "continuous_local_jacobian":[[str(v) for v in row] for row in jac],
        "continuous_trace":str(tr["trace"]),
        "continuous_determinant":str(tr["determinant"]),
        "continuous_locally_strictly_stable":True,
        "discrete_local_jacobian":[[str(v) for v in row] for row in disc],
        "discrete_trace":str(dr["trace"]),
        "discrete_determinant":str(dr["determinant"]),
        "discrete_eigen_modulus_squared_if_conjugate":"28/25",
        "discrete_locally_unstable":True,
        "mutant_e0_at_share_one_tenth_advantage":str(gap),
    }


def original_alpha_counterexample_audit():
    alpha=F(1)
    A=source_1978_alpha_matrix(alpha)
    p=alpha_interior_equilibrium(alpha)
    expected=(F(15,35),F(11,35),F(9,35))
    if p!=expected or payoff_each(A,p)!=(F(86,35),)*3:
        raise EvolutionaryAuditError("R131_ORIGINAL_ALPHA1_SOURCE_EQ_WRONG")
    jac=tangent_analytic_continuous_jacobian(A,p)
    other=tangent_independent_exact_polynomial_jacobian(A,p)
    expected_jac=((F(-291,245),F(-60,49)),(F(2013,1225),F(33,49)))
    if jac!=expected_jac or other!=jac:
        raise EvolutionaryAuditError("R131_ALPHA1_CONTINUOUS_JACOBIAN_WRONG")
    t=trace_and_det_two_by_two(jac)
    if t!={"trace":F(-18,35),"determinant":F(297,245)}:
        raise EvolutionaryAuditError("R131_ALPHA1_SOURCE_STABILITY_TR_DET_WRONG")
    q=(F(0),F(0),F(1))
    mu=F(1,10)
    exact=invasion_advantage_direct(A,p,q,mu)
    expansion=invasion_advantage_independent_expansion(A,p,q,mu)
    if exact!=F(3,350) or expansion!=exact:
        raise EvolutionaryAuditError("R131_ALPHA1_MUTANT_E3_EARNINGS_WITNESS_WRONG")
    return {
        "primary_original_source":"Taylor and Jonker 1978 p151 A(alpha) α=1",
        "primary_exact_payoff_matrix":[[str(v) for v in row] for row in A],
        "alpha":"1",
        "full_support_exact_equilibrium_p":[str(y) for y in p],
        "each_present_pure_type_fitness":"86/35",
        "continuous_local_jacobian":[[str(v) for v in row] for row in jac],
        "continuous_trace":"-18/35",
        "continuous_determinant":"297/245",
        "continuous_locally_strictly_stable":True,
        "exact_invader_e3":[str(z) for z in q],
        "mutant_e3_at_share_one_tenth_advantage":"3/350",
        "general_exact_mutant_e3_advantage_for_share_mu":"3*mu/35, positive for every mu>0",
        "evolutionarily_stable_strategy":False,
    }


def original_p147_invasion_grid():
    """21 simplex points for each p/q and 3 mu? Use exactly 28 p and 3 q."""
    probs=[]
    for i in range(7):
        for j in range(7-i):
            probs.append((F(i,6),F(j,6),F(6-i-j,6)))
    if len(probs)!=28:
        raise EvolutionaryAuditError("R131_THREE_STRATEGY_GRID_NOT_28")
    cases=((source_1978_cyclic_matrix(F(1,2)),(F(1,3),)*3),
           (source_1978_alpha_matrix(F(1)),alpha_interior_equilibrium(F(1))))
    checked=0
    for A,_anchor in cases:
        for p in probs:
            for q in ((F(1),F(0),F(0)),(F(0),F(1),F(0)),(F(0),F(0),F(1))):
                for mu in (F(1,10),F(1,4),F(1,2)):
                    direct=invasion_advantage_direct(A,p,q,mu)
                    expansion=invasion_advantage_independent_expansion(A,p,q,mu)
                    if direct!=expansion:
                        raise EvolutionaryAuditError("R131_SOURCE_P147_EQ1_GRID_DISAGREEMENT")
                    checked+=1
    if checked!=504:
        raise EvolutionaryAuditError("R131_GRID_504_CASES_NOT_COMPLETE")
    return {"simplex_states_1_over_6_lattice":28,
            "mutant_pure_types_each":3,"mutant_invasion_shares_each":["1/10","1/4","1/2"],
            "original_matrix_examples":2,"exact_direct_vs_expansion_comparisons":checked}


def finite_project_moran_transitions(N,i,fitness_A,fitness_B):
    """PROJECT Moran birth-death, not 1978 authors' discrete large-N Eq3."""
    if type(N) is not int or not 2<=N<=8 or type(i) is not int or not 0<=i<=N:
        raise EvolutionaryAuditError("R131_MORAN_N_2TO8_I_0TON_REQUIRED")
    if type(fitness_A) is not F or type(fitness_B) is not F or fitness_A<=0 or fitness_B<=0:
        raise EvolutionaryAuditError("R131_MORAN_POSITIVE_EXACT_FITNESS_REQUIRED")
    if i in (0,N):
        return (F(0),F(0),F(1))
    base=i*fitness_B+(N-i)*fitness_A
    up=F(i)*fitness_B/base*F(N-i,N)
    down=F(N-i)*fitness_A/base*F(i,N)
    stay=F(1)-up-down
    if min(up,down,stay)<0 or up+down+stay!=1:
        raise EvolutionaryAuditError("R131_PROJECT_MORAN_NOT_STOCHASTIC")
    return (up,down,stay)


def exact_project_moran_fixation_probability(N,fitness_A,fitness_B):
    """Absorbing birth-death chain solve by successive forward differences.

    If Delta_i = u_i-u_(i-1), Delta_(i+1) = (down_i/up_i)*Delta_i.
    With u0=0 and uN=1, u1 = 1 / [1+sum_{k=1}^{N-1}product(down_j/up_j)].
    """
    if type(N) is not int or not 2<=N<=8:
        raise EvolutionaryAuditError("R131_MORAN_N_OUT_OF_SCOPE")
    cumulative=F(1);total=F(1)
    for i in range(1,N):
        up,down,_=finite_project_moran_transitions(N,i,fitness_A,fitness_B)
        cumulative*=down/up
        total+=cumulative
    return F(1)/total


def project_finite_stochastic_drift_counterexample():
    N=5
    resident_fitness=F(3)
    mutant_fitness=F(2)
    selected_against=exact_project_moran_fixation_probability(N,resident_fitness,mutant_fitness)
    neutral=exact_project_moran_fixation_probability(N,F(1),F(1))
    if selected_against!=F(16,211) or neutral!=F(1,5):
        raise EvolutionaryAuditError("R131_PROJECT_FINITE_ABSORPTION_EXACT_FRACTION_WRONG")
    if not F(0)<selected_against<neutral:
        raise EvolutionaryAuditError("R131_DISADVANTAGED_MUTANT_STILL_CAN_FIX")
    sweep=0
    for n in range(2,9):
        if exact_project_moran_fixation_probability(n,F(1),F(1))!=F(1,n):
            raise EvolutionaryAuditError("R131_NEUTRAL_FIXATION_NOT_1_OVER_N")
        disadvantage=exact_project_moran_fixation_probability(n,F(3),F(2))
        if not F(0)<disadvantage<F(1,n):
            raise EvolutionaryAuditError("R131_FINITE_DISADVANTAGE_OUTCOME_NOT_BOUNDED")
        sweep+=1
    return {
        "project_created_not_a_1978_source_theorem_or_simulation":True,
        "population_N":N,
        "incumbent_A_vs_any_action_payoff":"2",
        "mutant_B_vs_any_action_payoff":"1",
        "project_baseline_fitness_formula":"fitness=1+stage_payoff",
        "incumbent_fitness":"3","mutant_fitness":"2",
        "incumbent_strict_pure_ESS_in_infinite_symmetric_matrix":True,
        "project_single_mutant_risk_of_eventual_fixation":"16/211",
        "project_neutral_single_mutant_fixation":"1/5",
        "N2_to_8_neutral_and_disadvantaged_selection_checks":sweep,
        "selection_disadvantage_does_not_imply_zero_finite_fixation":True,
        "real_population_size_or_behavior_frequency_estimated":False,
    }


def stage_receipt():
    return {
        "study":"R131","catalogue":"05-007",
        "original_1978_regular_ESS_continuous_stable_discrete_unstable":original_cyclic_counterexample_audit(),
        "original_1978_strict_continuous_stability_without_ESS":original_alpha_counterexample_audit(),
        "original_1978_invasion_expansion_exact_grid":original_p147_invasion_grid(),
        "project_finite_population_random_drift_extra":project_finite_stochastic_drift_counterexample(),
        "new_real_human_E2_prediction_scores":0,
        "original_1978_numeric_population_trajectories_all_reconstructed":False,
        "R073":"FROZEN","PESEN_v0_1":"FROZEN",
    }


if __name__=="__main__":
    print(json.dumps(stage_receipt(),indent=2,sort_keys=True))
