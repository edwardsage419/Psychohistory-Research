#!/usr/bin/env python3
"""R123 exact DeGroot (1974) consensus and Berger (1981) conceptual correction.

1974 original JASA 69:118-121 DOI 10.1080/01621459.1974.10480137.
1981 Berger JASA 76:415-418 necessary/sufficient correction.
No real person-level beliefs or prediction E2 results are used.

U = consensus for ALL initial opinions: one aperiodic closed recurrent class.
C = each individual's opinion converges (not necessarily consensus) for
    ALL initial opinions: every closed recurrent class is aperiodic.
S = one PARTICULAR initial vector yields common limit: can happen even if
    U fails. Here we construct counterexamples, not Berger's full F theorem.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd
import json


class DeGrootDesignError(ValueError):
    pass


def matrix(values):
    if type(values) not in (tuple,list) or not 1 <= len(values) <= 4:
        raise DeGrootDesignError("R123_EXPLICIT_SQUARE_MATRIX_N_1_TO_4")
    n=len(values)
    rows=[]
    for row in values:
        if type(row) not in (tuple,list) or len(row)!=n:
            raise DeGrootDesignError("R123_NOT_SQUARE_ROW")
        if any(type(x) is not F or not F(0)<=x<=F(1) for x in row):
            raise DeGrootDesignError("R123_ENTRIES_STRICT_FRACTION_ZERO_TO_ONE")
        if sum(row,F(0))!=1:
            raise DeGrootDesignError("R123_ROWS_EXACTLY_STOCHASTIC")
        rows.append(tuple(row))
    return tuple(rows)


def initial(values,n):
    if type(values) not in (tuple,list) or len(values)!=n:
        raise DeGrootDesignError("R123_INITIAL_OPINION_DIMENSION")
    if any(type(v) is not F for v in values):
        raise DeGrootDesignError("R123_INITIAL_OPINIONS_EXACT_FRACTIONS")
    return tuple(values)


def one_update(w,values):
    m=matrix(w)
    x=initial(values,len(m))
    return tuple(sum((weight*x[j] for j,weight in enumerate(row)),F(0)) for row in m)


def exact_trajectory(w, values, steps=5):
    m=matrix(w)
    x=initial(values,len(m))
    if type(steps) is not int or not 0<=steps<=80:
        raise DeGrootDesignError("R123_FINITE_NONNEGATIVE_STEPS_MAX_80")
    series=[x]
    for _ in range(steps):
        x=one_update(m,x)
        prior=series[-1]
        if min(x)<min(prior) or max(x)>max(prior):
            raise DeGrootDesignError("R123_CONVEX_HULL_VIOLATION")
        if max(x)-min(x)>max(prior)-min(prior):
            raise DeGrootDesignError("R123_OPINION_RANGE_INCREASED")
        series.append(x)
    return tuple(series)


def power_matrix(w, exponent):
    m=matrix(w)
    if type(exponent) is not int or not 0<=exponent<=32:
        raise DeGrootDesignError("R123_MATRIX_POWER_0_TO_32")
    n=len(m)
    accum=tuple(tuple(F(int(i==j)) for j in range(n)) for i in range(n))
    for _ in range(exponent):
        accum=tuple(tuple(sum((accum[i][k]*m[k][j] for k in range(n)),F(0))
                          for j in range(n)) for i in range(n))
    return accum


def support_structure(w):
    """Independent graph structural audit; no opinion simulation used."""
    m=matrix(w)
    n=len(m)
    adj=tuple(frozenset(j for j,p in enumerate(row) if p>0) for row in m)
    # Graph reachability by DFS, independently of numerical iterated powers.
    reachable=[]
    for source in range(n):
        visited={source}
        stack=[source]
        while stack:
            i=stack.pop()
            for j in adj[i]:
                if j not in visited:
                    visited.add(j)
                    stack.append(j)
        reachable.append(frozenset(visited))
    remaining=set(range(n))
    components=[]
    while remaining:
        root=min(remaining)
        cls=frozenset(i for i in remaining if root in reachable[i] and i in reachable[root])
        if not cls:
            raise DeGrootDesignError("R123_SCC_INVALID")
        components.append(tuple(sorted(cls)))
        remaining -= cls
    closed=[]
    periods=[]
    for cls_tuple in components:
        cls=frozenset(cls_tuple)
        if not all(adj[i]<=cls for i in cls):
            continue
        closed.append(cls_tuple)
        # Strongly connected closed SCC period gcd over directed edges.
        distances={cls_tuple[0]:0}
        queue=[cls_tuple[0]]
        for source in queue:
            for neighbor in adj[source]:
                if neighbor in cls and neighbor not in distances:
                    distances[neighbor]=distances[source]+1
                    queue.append(neighbor)
        if len(distances)!=len(cls):
            raise DeGrootDesignError("R123_CLOSED_CLASS_UNREACHABLE")
        period=0
        for i in cls:
            for j in adj[i]:
                if j in cls:
                    period=gcd(period,abs(distances[i]+1-distances[j]))
        if period <= 0:
            raise DeGrootDesignError("R123_PERIOD_MISSING")
        periods.append(period)
    if not closed:
        raise DeGrootDesignError("R123_FINITE_MARKOV_CHAIN_MUST_HAVE_CLOSED_CLASS")
    return {
        "communicating_classes":tuple(components),
        "closed_classes":tuple(closed),
        "closed_periods":tuple(periods),
        "all_initial_consensus_guaranteed":len(closed)==1 and periods[0]==1,
        "all_initial_each_opinion_convergent":all(period==1 for period in periods),
    }


def positive_column_power_certificate(w, max_exponent=12):
    """DeGroot 1974 Theorem1 sufficient positive-column power certificate.

    This bounded test does not prove nonconsensus from absence at general n.
    We crosscheck against graph criterion only for our n<=3 tiny domain.
    """
    m=matrix(w)
    if type(max_exponent) is not int or not 1<=max_exponent<=32:
        raise DeGrootDesignError("R123_CERTIFICATE_EXPONENT_1_TO_32")
    n=len(m)
    cur=tuple(tuple(i==j for j in range(n)) for i in range(n))
    graph=tuple(tuple(p>0 for p in row) for row in m)
    for t in range(1,max_exponent+1):
        cur=tuple(tuple(any(cur[i][k] and graph[k][j] for k in range(n))
                        for j in range(n)) for i in range(n))
        for col in range(n):
            if all(cur[row][col] for row in range(n)):
                return {"witness_exponent":t,"positive_column":col}
    return None


def gaussian_stationary_weights(w):
    """Exact solve left eigenvector pi W = pi, sum pi = 1 by Gauss-Jordan.

    Works for any unique stationary vector including periodic W, but we
    restrict use to certified universal consensus in the public interface.
    """
    m=matrix(w)
    n=len(m)
    if not support_structure(m)["all_initial_consensus_guaranteed"]:
        raise DeGrootDesignError("R123_UNIVERSAL_CONSENSUS_REQUIRED_FOR_WEIGHTS")
    augmented=[
        [m[j][i]-F(int(i==j)) for j in range(n)]+[F(0)]
        for i in range(n)
    ]+[[F(1)]*n+[F(1)]]
    row=0
    pivotcols=[]
    for col in range(n):
        pivot=next((r for r in range(row,len(augmented)) if augmented[r][col]!=0),None)
        if pivot is None:
            continue
        augmented[row],augmented[pivot]=augmented[pivot],augmented[row]
        denom=augmented[row][col]
        augmented[row]=[x/denom for x in augmented[row]]
        for k in range(len(augmented)):
            if k!=row:
                scale=augmented[k][col]
                if scale:
                    augmented[k]=[augmented[k][j]-scale*augmented[row][j] for j in range(n+1)]
        pivotcols.append(col)
        row+=1
    if len(pivotcols)!=n or any(all(v==0 for v in line[:n]) and line[n]!=0 for line in augmented):
        raise DeGrootDesignError("R123_STATIONARY_UNDERDETERMINED_OR_INCONSISTENT")
    out=[F(0)]*n
    for r,col in enumerate(pivotcols):
        out[col]=augmented[r][n]
    pi=tuple(out)
    _verify_weights(m,pi)
    return pi


def _verify_weights(m,pi):
    if not all(p>=0 for p in pi) or sum(pi,F(0))!=1:
        raise DeGrootDesignError("R123_STATIONARY_INVALID_PROBABILITIES")
    n=len(m)
    if any(sum((pi[i]*m[i][j] for i in range(n)),F(0))!=pi[j] for j in range(n)):
        raise DeGrootDesignError("R123_STATIONARITY_EQUATIONS_FAILED")


def independent_markov_in_trees(w):
    """Independent directed Markov tree theorem, no Gaussian solver invoked.

    For each root, enumerate parent choices i->parent[i] for each other i,
    accept if following all parent links reaches root without cycles. Product
    of transition weights gives rooted directed in-arborescence weight.
    """
    m=matrix(w)
    n=len(m)
    if not support_structure(m)["all_initial_consensus_guaranteed"]:
        raise DeGrootDesignError("R123_UNIVERSAL_CONSENSUS_REQUIRED_FOR_TREES")
    weighted=[]
    for root in range(n):
        nonroots=[i for i in range(n) if i!=root]
        choices=[tuple(j for j in range(n) if j!=i and m[i][j]>0) for i in nonroots]
        total=F(0)
        for parents in product(*choices):
            parent=dict(zip(nonroots,parents))
            valid=True
            for source in nonroots:
                visited=set()
                current=source
                while current!=root:
                    if current in visited or current not in parent:
                        valid=False
                        break
                    visited.add(current)
                    current=parent[current]
                if not valid:
                    break
            if valid:
                mass=F(1)
                for i,j in parent.items():
                    mass*=m[i][j]
                total+=mass
        weighted.append(total)
    z=sum(weighted,F(0))
    if z<=0:
        raise DeGrootDesignError("R123_NO_SPANNING_IN_TREE")
    pi=tuple(p/z for p in weighted)
    _verify_weights(m,pi)
    return pi


def exact_consensus_value(w,values):
    m=matrix(w)
    x=initial(values,len(m))
    p=gaussian_stationary_weights(m)
    tree=independent_markov_in_trees(m)
    if p!=tree:
        raise DeGrootDesignError("R123_INDEPENDENT_STATIONARY_METHODS_DISAGREE")
    return sum((p[i]*x[i] for i in range(len(m))),F(0))


def degroot_original_published_examples():
    """Numerical matrices in original JASA 1974 printed p120."""
    first=((F(1,2),F(1,2)),(F(1,4),F(3,4)))
    extended=((F(1,2),F(1,2),F(0)),
              (F(1,4),F(3,4),F(0)),
              (F(1,3),F(1,3),F(1,3)))
    return {
        "two_person_stationary":tuple(str(p) for p in gaussian_stationary_weights(first)),
        "two_person_consensus_x0_0_1":str(exact_consensus_value(first,(F(0),F(1)))),
        "two_person_simple_arithmetic_mean":"1/2",
        "three_person_stationary":tuple(str(p) for p in independent_markov_in_trees(extended)),
        "three_person_consensus_x0_0_1_9":str(exact_consensus_value(extended,(F(0),F(1),F(9)))),
        "third_person_longrun_weight_zero":True,
        "DeGroot_1974_p120_original_author_numeric_examples":True,
    }


def special_initial_opinion_counterexamples():
    swap=((F(0),F(1)),(F(1),F(0)))
    identity=((F(1),F(0)),(F(0),F(1)))
    leader=((F(1),F(0)),(F(1,2),F(1,2)))
    return {
        "swap_structure":support_structure(swap),
        "swap_opposed_first_five":tuple(tuple(str(v) for v in x) for x in
                                        exact_trajectory(swap,(F(0),F(1)),4)),
        "swap_equal_opinion_stays_equal":tuple(tuple(str(v) for v in x) for x in
                                             exact_trajectory(swap,(F(1,2),F(1,2)),2)),
        "identity_structure":support_structure(identity),
        "identity_disagreement_stays":tuple(str(v) for v in exact_trajectory(identity,(F(0),F(1)),3)[-1]),
        "identity_equal_opinion_stays_equal":tuple(str(v) for v in exact_trajectory(identity,(F(1,2),F(1,2)),2)[-1]),
        "leader_structure":support_structure(leader),
        "leader_pi":tuple(str(v) for v in independent_markov_in_trees(leader)),
        "leader_value_x0_0_1":str(exact_consensus_value(leader,(F(0),F(1)))),
        "berger_1981_corrects_1974_claim_of_necessity_for_one_particular_initial_F":True,
        "these_are_our_toy_constructions_not_1974_empirical_subject_trials":True,
    }


def tiny_226_row_stochastic_matrix_audit():
    counts={}
    counts_u={}
    counts_c={}
    for n in (1,2,3):
        rowset=[]
        for index in range(n):
            rowset.append(tuple(F(int(j==index)) for j in range(n)))
        for i,j in combinations(range(n),2):
            rowset.append(tuple(F(1,2) if k in (i,j) else F(0) for k in range(n)))
        expected=(n+ n*(n-1)//2)**n
        actual=0
        universals=0
        convergents=0
        for rows in product(rowset,repeat=n):
            info=support_structure(rows)
            witness=positive_column_power_certificate(rows,12)
            if info["all_initial_consensus_guaranteed"]:
                universals+=1
                if witness is None:
                    raise DeGrootDesignError("R123_UNIVERSAL_GRAPH_WITHOUT_POSITIVE_COLUMN_SMALL_CASE")
                p=gaussian_stationary_weights(rows)
                tree=independent_markov_in_trees(rows)
                if p!=tree:
                    raise DeGrootDesignError("R123_EXHAUSTIVE_TWO_PI_METHODS_DIFFER")
            elif witness is not None:
                raise DeGrootDesignError("R123_POSITIVE_COLUMN_WITHOUT_UNIVERSAL_CONSENSUS")
            if info["all_initial_each_opinion_convergent"]:
                convergents+=1
            actual+=1
        if actual!=expected:
            raise DeGrootDesignError("R123_MATRIX_ENUMERATION_UNEXPECTED_SIZE")
        counts[str(n)]=actual
        counts_u[str(n)]=universals
        counts_c[str(n)]=convergents
    if counts!={"1":1,"2":9,"3":216}:
        raise DeGrootDesignError("R123_EXHAUSTIVE_EXPECTED_226_CONFIGURATIONS")
    return {
        "tested_row_stochastic_matrices_by_n":counts,
        "universal_consensus_structures_by_n":counts_u,
        "all_opinions_individually_converge_by_n":counts_c,
        "total_synthetic_matrices":sum(counts.values()),
        "finite_positive_column_certificate_12_powers_checked":True,
        "gaussian_and_independent_in_trees_identical_for_each_universal":True,
    }


def research_receipt():
    return {
        "research_id":"R123","candidate":"04-009","phase":"A",
        "DeGroot_1974_original_DOI":"10.1080/01621459.1974.10480137",
        "Berger_1981_source":"JASA 76(374)415-418",
        "source_original_pages_read":[118,119,120,121],
        "source_1981_pages_read":[415,416,417],
        "primary_source_original_1974_examples":degroot_original_published_examples(),
        "Berger_1981_conceptual_correction_toys":special_initial_opinion_counterexamples(),
        "fully_exhaustive_small_matrix_structural_cases":tiny_226_row_stochastic_matrix_audit(),
        "full_Berger_1981_arbitrary_distribution_correction_reproduced":False,
        "real_human_original_microdata_E2_scores":0,
        "R073":"FROZEN","PESEN_v0_1":"FROZEN",
    }


if __name__=="__main__":
    print(json.dumps(research_receipt(),sort_keys=True,indent=2))
