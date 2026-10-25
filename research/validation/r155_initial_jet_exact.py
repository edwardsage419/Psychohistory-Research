"""R155: exact synthetic Bass initial-sales jet audit, standard library only."""
from fractions import Fraction as Q
from collections import defaultdict
import json

P = (Q(0), Q(1, 200), Q(1, 50), Q(2, 25), Q(1, 5))
R = (Q(0), Q(1, 50), Q(1, 10), Q(2, 5), Q(4, 5))
M = (100, 1000, 10000)

def s(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"

def run():
    groups2, groups3, rows = defaultdict(list), defaultdict(list), []
    for ip, p in enumerate(P):
        for iq, q in enumerate(R):
            for im, m in enumerate(M):
                name = f"p{ip}_q{iq}_m{im}"
                a = m * p
                b = a * (q - p)
                c = a * ((q - p)**2 - 2 * p * q)
                jet = (a, b, c)
                groups2[jet[:2]].append(name)
                groups3[jet].append(name)
                if p:
                    d, h = b/a, ((b/a)**2 - c/a)/2
                    assert d == q-p and h == p*q
                    assert p*(p+d) == h and p+d == q and a/p == m
                    assert p > 0 and q >= 0 and a/p > 0
                    assert (q == 0) == (h == 0)
                else:
                    assert jet == (0, 0, 0)
                rows.append({"id":name,"p":s(p),"q":s(q),"m":m,"S0":s(a),"S1":s(b),"S2":s(c),"invertible":bool(p)})
    zero = [r for r in rows if r["p"] == "0"]
    nonzero = [r for r in rows if r["p"] != "0"]
    assert len(rows)==75 and len(zero)==15 and len(nonzero)==60
    assert len(groups3)==61 and sorted(map(len, groups3.values()))==[1]*60+[15]
    assert groups3[(Q(0),Q(0),Q(0))] == [r["id"] for r in zero]
    assert all(len(groups3[(Q(r["S0"]),Q(r["S1"]),Q(r["S2"]))])==1 for r in nonzero)
    assert all(Q(r["S1"])/Q(r["S0"])==Q(r["q"])-Q(r["p"]) for r in nonzero)
    two_collisions = [sorted(v) for v in groups2.values() if len(v)>1]
    # Continuous parameter space permits an off-grid two-jet twin.
    t1 = (Q(1,50), Q(2,5), 1000)
    t2 = (Q(1,100), Q(39,100), 2000)
    def jet(p,q,m):
        return (m*p, m*p*(q-p), m*p*((q-p)**2-2*p*q))
    j1, j2 = jet(*t1), jet(*t2)
    assert j1[:2] == j2[:2] and j1[2] != j2[2]
    return {"offgrid_two_jet_twin": {"world1": [s(t1[0]),s(t1[1]),t1[2]], "world2": [s(t2[0]),s(t2[1]),t2[2]], "shared_S0_S1": [s(z) for z in j1[:2]], "distinct_S2": [s(j1[2]),s(j2[2])]}, "research_id":"R155", "method":"exact_fraction_initial_sales_jet", "evidence":"E1_SYNTHETIC_ONLY", "source_blob":"60a296dfdb870c2a49994217d155d0a0387e7e20", "worlds":75, "positive_p_worlds":60, "zero_p_worlds":15, "three_jet_equivalence_classes":len(groups3), "three_jet_collision_sizes":sorted([len(v) for v in groups3.values() if len(v)>1]), "two_jet_equivalence_classes":len(groups2), "two_jet_ambiguous_worlds":sum(len(v) for v in two_collisions), "two_jet_collision_classes":two_collisions, "positive_p_exact_inversions_passed":60, "zero_p_inversion_blocked":15, "rows":rows}

if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
