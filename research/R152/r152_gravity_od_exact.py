"""R152: EXACT project-created migration gravity and 3-city OD marginal examples.

Provenance: original journal issue records Zipf 1946, Stouffer 1940, Wilson
1967, not authors' original empirical data or full-text reproductions.
All populations, distances, parameters, tables are synthetic E1 only.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from math import lcm
import json

POPULATIONS = (2, 3, 5, 7)
LAYOUTS = {"near":(0,1,3,6),"far":(0,1,3,9)}
ATTRACTIONS = {"flat":(1,1,1,1),"mid_bonus":(1,1,2,1),
               "last_bonus":(1,1,1,2)}
BUDGETS = ("pop_10","pop_5","half")
EXPONENTS = (0,1,2)
N = len(POPULATIONS)

def integer(x):
    if type(x) is not int:
        raise TypeError("integer required; floats and bool are forbidden")
    return x

def population_vector(pop):
    if not isinstance(pop,(tuple,list)) or len(pop)!=4:
        raise ValueError("four population entries required")
    values = tuple(integer(v) for v in pop)
    if any(v<=0 for v in values):
        raise ValueError("population entries must be strictly positive")
    return values

def positions(coords):
    if not isinstance(coords,(tuple,list)) or len(coords)!=4:
        raise ValueError("four positions required")
    values=tuple(integer(v) for v in coords)
    if len(set(values))!=4:
        raise ValueError("all four positions must be distinct")
    return values

def attraction_vector(v):
    if not isinstance(v,(tuple,list)) or len(v)!=4:
        raise ValueError("four attraction weights required")
    values=tuple(integer(x) for x in v)
    if any(z<=0 for z in values):
        raise ValueError("attraction weights must be positive")
    return values

def exponent(alpha):
    alpha=integer(alpha)
    if alpha not in EXPONENTS:
        raise ValueError("alpha must be 0, 1 or 2")
    return alpha

def outflows(pop, mode):
    pop=population_vector(pop)
    if mode == "pop_10":
        return tuple(F(p,10) for p in pop)
    if mode == "pop_5":
        return tuple(F(p,5) for p in pop)
    if mode == "half":
        return tuple(F(1,2) for _ in pop)
    raise ValueError("unknown outflow budget")

def distance(coords,i,j):
    p=positions(coords)
    i,j=integer(i),integer(j)
    if not 0<=i<4 or not 0<=j<4:
        raise ValueError("city index out of range")
    if i==j:
        raise ValueError("no self migration distances")
    return abs(p[i]-p[j])

def raw_gravity(pop,coords,alpha):
    pop,coords,alpha=population_vector(pop),positions(coords),exponent(alpha)
    return tuple(tuple(F(0) if i==j else F(pop[i]*pop[j],abs(coords[i]-coords[j])**alpha)
                       for j in range(4)) for i in range(4))

def flows_direct(pop,coords,attraction,alpha,budget):
    """Direct Fraction weight normalization for each fixed origin budget."""
    pop,coords,attraction,alpha=(population_vector(pop),positions(coords),
                                 attraction_vector(attraction),exponent(alpha))
    allocated=outflows(pop,budget)
    lines=[]
    for i in range(4):
        weights=[F(0) if j==i else F(pop[j]*attraction[j],abs(coords[i]-coords[j])**alpha)
                 for j in range(4)]
        normalizer=sum(weights,F(0))
        assert normalizer>0
        lines.append(tuple(allocated[i]*weight/normalizer for weight in weights))
    return tuple(lines)

def flows_integer_route(pop,coords,attraction,alpha,budget):
    """Independent integer common-denominator route, no call to flows_direct."""
    pop=population_vector(pop)
    coords=positions(coords)
    attraction=attraction_vector(attraction)
    alpha=exponent(alpha)
    quotas=outflows(pop,budget)
    rows=[]
    for i in range(4):
        ds=[abs(coords[j]-coords[i])**alpha for j in range(4) if j!=i]
        common=lcm(*ds)
        weights=[0 if j==i else pop[j]*attraction[j]*(common//(abs(coords[j]-coords[i])**alpha))
                 for j in range(4)]
        denom=sum(weights)
        assert denom>0
        rows.append(tuple(quotas[i]*F(n,denom) for n in weights))
    return tuple(rows)

def ordered_scenarios():
    for layout,alpha,attract,budget in product(LAYOUTS,EXPONENTS,ATTRACTIONS,BUDGETS):
        yield (layout,alpha,attract,budget)

def matrix_metrics(matrix,coords,quotas):
    coords=positions(coords)
    origin_totals=tuple(sum(row,F(0)) for row in matrix)
    destination_totals=tuple(sum((matrix[i][j] for i in range(4)),F(0)) for j in range(4))
    for i in range(4):
        assert origin_totals[i]==quotas[i]
        assert matrix[i][i]==0
    total=sum(quotas,F(0))
    assert total==sum(destination_totals,F(0))
    weighted_distance=sum((matrix[i][j]*abs(coords[i]-coords[j])
                            for i in range(4) for j in range(4) if i!=j),F(0))/total
    return {
        "row_outflow":[str(x) for x in origin_totals],
        "destination_inflow":[str(x) for x in destination_totals],
        "all_outflow":str(total),
        "mean_distance_weighted_by_flow":str(weighted_distance),
        "route_probabilities":[[str(matrix[i][j]/quotas[i]) for j in range(4)]
                              for i in range(4)],
    }

def scenario(layout,alpha,attraction,budget):
    if layout not in LAYOUTS or attraction not in ATTRACTIONS:
        raise ValueError("unknown layout or attraction mode")
    pop=POPULATIONS
    x=LAYOUTS[layout]
    a=ATTRACTIONS[attraction]
    d=flows_direct(pop,x,a,alpha,budget)
    alt=flows_integer_route(pop,x,a,alpha,budget)
    assert d==alt
    q=outflows(pop,budget)
    metrics=matrix_metrics(d,x,q)
    k=raw_gravity(pop,x,alpha)
    return {
        "layout":layout,"alpha":alpha,"attraction":attraction,
        "budget":budget,"positions":list(x),"populations":list(pop),
        "unconstrained_zipf_like_kernel":[[str(v) for v in row] for row in k],
        "flow_matrix":[[str(v) for v in row] for row in d],
        "two_separate_fraction_algorithms_agree":True,
        **metrics,
    }

def od_exact_tables_enumeration(margins=(2,3,4)):
    """Six independent integer route counts, all complete tables enumerated."""
    if not isinstance(margins,(tuple,list)) or len(margins)!=3:
        raise ValueError("three margins required")
    a,b,c=(integer(v) for v in margins)
    if min(a,b,c)<0:
        raise ValueError("negative margin")
    ans=[]
    for u01,u02,u10,u12,u20,u21 in product(range(a+1),range(a+1),
                                               range(b+1),range(b+1),
                                               range(c+1),range(c+1)):
        t=((0,u01,u02),(u10,0,u12),(u20,u21,0))
        if (all(sum(t[i])==margins[i] for i in range(3))
                and all(sum(t[i][j] for i in range(3))==margins[j] for j in range(3))):
            ans.append(t)
    return tuple(sorted(ans))

def od_exact_tables_symbolic(margins=(2,3,4)):
    """A separate symbolic-parametric reconstruction, not 6-nested enumeration."""
    if not isinstance(margins,(tuple,list)) or len(margins)!=3:
        raise ValueError("three margins required")
    a,b,c=tuple(integer(v) for v in margins)
    if min(a,b,c)<0:
        raise ValueError("negative margin")
    rows=[]
    for t in range(a+1):
        vals=((0,t,a-t),(a+b-c-t,0,c-a+t),(c-b+t,b-t,0))
        if all(v>=0 for r in vals for v in r):
            if all(sum(r)==m for r,m in zip(vals,(a,b,c))) and \
               all(sum(vals[i][j] for i in range(3))==m for j,m in enumerate((a,b,c))):
                rows.append(vals)
    return tuple(sorted(rows))

def od_score(table,alpha,coords=(0,1,3),pop=(2,3,4)):
    alpha=exponent(alpha)
    if not isinstance(table,(tuple,list)) or len(table)!=3:
        raise ValueError("3×3 directed table needed")
    if len(set(coords))!=3 or len(coords)!=3 or len(pop)!=3:
        raise ValueError("three distinct positions and populations needed")
    score=F(1)
    for i in range(3):
        if len(table[i])!=3:
            raise ValueError("3×3 directed table needed")
        for j in range(3):
            count=integer(table[i][j])
            if count<0 or (i==j and count!=0):
                raise ValueError("OD table cannot have negative or self traffic")
            if i!=j:
                score*=F(pop[i]*pop[j],abs(coords[i]-coords[j])**alpha)**count
    return score

def od_direction_reward(table):
    return 2**sum(table[i][j] for i in range(3) for j in range(i+1,3))

def od_undirected_pair_totals(table):
    return tuple(table[i][j]+table[j][i] for i in range(3) for j in range(i+1,3))

def output():
    all_cases=[scenario(*x) for x in ordered_scenarios()]
    assert len(all_cases)==54
    od=od_exact_tables_enumeration()
    assert od==od_exact_tables_symbolic()
    assert len(od)>=2
    scores={str(alpha):[str(od_score(t,alpha)) for t in od] for alpha in EXPONENTS}
    return {
        "id":"R152","all_project_synthetic":True,"historical_migration_data_replayed":False,
        "original_zipf_full_article_read":False,
        "original_stouffer_full_article_read":False,
        "original_wilson_full_article_read":False,
        "new_E2":0,"new_E3":0,
        "four_city_population":list(POPULATIONS),
        "scenarios_count":len(all_cases),"scenarios":all_cases,
        "three_city_margins":[2,3,4],
        "three_city_integer_od_count":len(od),
        "three_city_od_tables":[[list(row) for row in t] for t in od],
        "three_city_gravity_scores":scores,
        "od_undirected_pair_counts":[list(od_undirected_pair_totals(t)) for t in od],
        "od_direction_reward":[str(od_direction_reward(t)) for t in od],
        "all_od_analytical_and_bruteforce_agree":True,
        "all_scenario_direct_and_integer_algorithms_agree":True,
        "caveat_od_gravity_score_not_full_individual_likelihood":True,
    }

def canonical_json():
    return json.dumps(output(),sort_keys=True,ensure_ascii=False,separators=(",",":"))+"\n"

if __name__=="__main__":
    print(canonical_json(),end="")
