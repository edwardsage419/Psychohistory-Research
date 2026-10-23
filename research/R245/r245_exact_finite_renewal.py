#!/usr/bin/env python3
"""R245 exact finite renewal/counting processes: 9 worlds, 4608 complete atoms.

128? No: U plus 4 independent 2-bit gap draws = 2^9 = 512 source
types per artificial world. Full observed N(0..4) is distinguished from
oracle true hidden events and from the four latent generator intervals.
Independent 16-gap-vector product-law and renewal-equation checks.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="80160fbbe01d801fe27cc020bf59a63c7b503759"
ZERO=F(0);ONE=F(1)
BITS=(0,1)
GAP_VALUES=(1,2)
TIMES=(0,1,2,3,4)
GAP_VECTORS=tuple(itertools.product(GAP_VALUES,repeat=4))
EXOGENOUS=tuple(itertools.product(BITS,repeat=9))
WORLDS=(
    "IID_FAIR","IID_SHORT_3OF4","IID_LONG_1OF4",
    "DETERMINISTIC_UNIT","DETERMINISTIC_TWO",
    "LATENT_RATE_MIXTURE","ALTERNATING_RATE",
    "COMMON_GAP_SHOCK","STATIC_HIDDEN_EVENT_SENSOR_ALIAS"
)
IID_OBS=("IID_FAIR","IID_SHORT_3OF4","IID_LONG_1OF4",
         "DETERMINISTIC_UNIT","DETERMINISTIC_TWO",
         "STATIC_HIDDEN_EVENT_SENSOR_ALIAS")
NON_IID=("LATENT_RATE_MIXTURE","ALTERNATING_RATE","COMMON_GAP_SHOCK")

def require(world):
    if world not in WORLDS:raise ValueError("not frozen renewal world")

def threshold(world,index,u):
    require(world)
    if index not in (1,2,3,4) or u not in BITS:raise ValueError("invalid source")
    if world in ("IID_FAIR","STATIC_HIDDEN_EVENT_SENSOR_ALIAS","COMMON_GAP_SHOCK"):
        return 2
    if world=="IID_SHORT_3OF4":return 3
    if world=="IID_LONG_1OF4":return 1
    if world=="DETERMINISTIC_UNIT":return 4
    if world=="DETERMINISTIC_TWO":return 0
    if world=="LATENT_RATE_MIXTURE":return 3 if u==0 else 1
    if world=="ALTERNATING_RATE":return 3 if index%2==1 else 1
    raise AssertionError("unknown frozen threshold")

def draw_gaps(world,bits):
    require(world)
    if len(bits)!=9 or any(x not in BITS for x in bits):
        raise ValueError("expected nine binary exogenous source atoms")
    u=bits[0]
    r=tuple(2*bits[2*j-1]+bits[2*j] for j in (1,2,3,4))
    return tuple(
        1 if (r[0] if world=="COMMON_GAP_SHOCK" else r[j-1])<
                threshold(world,j,u) else 2
        for j in (1,2,3,4))

def cumulative_arrivals(gaps):
    if len(gaps)!=4 or any(g not in GAP_VALUES for g in gaps):
        raise ValueError("not positive frozen interarrival")
    out=[]
    s=0
    for g in gaps:
        s+=g;out.append(s)
    return tuple(out)

def observed_counts_from_gaps(gaps):
    arr=cumulative_arrivals(gaps)
    return tuple(sum(a<=t for a in arr) for t in TIMES)

def source_atom(world,bits):
    gaps=draw_gaps(world,bits)
    arr=cumulative_arrivals(gaps)
    observed=observed_counts_from_gaps(gaps)
    true=observed if world!="STATIC_HIDDEN_EVENT_SENSOR_ALIAS" else (0,0,0,0,0)
    row={"world":world,"oracle_exogenous_U":bits[0]}
    for j in (1,2,3,4):
        row["oracle_original_R"+str(j)+"1"]=bits[2*j-1]
        row["oracle_original_R"+str(j)+"2"]=bits[2*j]
        row["oracle_generator_gap_W"+str(j)]=gaps[j-1]
        row["oracle_generator_arrival_S"+str(j)]=arr[j-1]
    for t in TIMES:
        row["observed_reported_count_Y"+str(t)]=observed[t]
        row["oracle_true_event_count_H"+str(t)]=true[t]
    row["original_source_probability"]=F(1,512)
    return row

@lru_cache(maxsize=None)
def sources(world):
    require(world)
    rows=tuple(source_atom(world,bits) for bits in EXOGENOUS)
    if len(rows)!=512 or sum((r["original_source_probability"] for r in rows),ZERO)!=ONE:
        raise AssertionError("incomplete 512-source exogenous universe")
    if any(r["original_source_probability"]<=0 for r in rows):
        raise AssertionError("unexpected structural zero")
    return rows

@lru_cache(maxsize=None)
def observed_path_joint(world):
    out=defaultdict(F)
    for row in sources(world):
        path=tuple(row["observed_reported_count_Y"+str(t)] for t in TIMES)
        out[path]+=row["original_source_probability"]
    return dict(sorted(out.items()))

def independent_gap_vector_probability(world,gaps):
    """Product-law / mixture closed formula; reads no 9-bit source rows."""
    require(world)
    if gaps not in GAP_VECTORS:raise ValueError("not frozen positive gap vector")
    if world=="COMMON_GAP_SHOCK":
        return F(1,2) if gaps in ((1,1,1,1),(2,2,2,2)) else ZERO
    def product(u):
        prob=ONE
        for j,g in enumerate(gaps,1):
            p=F(threshold(world,j,u),4)
            prob*=p if g==1 else ONE-p
        return prob
    if world=="LATENT_RATE_MIXTURE":return (product(0)+product(1))/2
    return product(0)

def independent_observed_joint(world):
    result=defaultdict(F)
    for gaps in GAP_VECTORS:
        p=independent_gap_vector_probability(world,gaps)
        if p:result[observed_counts_from_gaps(gaps)]+=p
    return dict(sorted(result.items()))

def source_first_gap_short(world):
    return sum((r["original_source_probability"]*
                int(r["oracle_generator_gap_W1"]==1) for r in sources(world)),ZERO)

def observed_mean_count(world,t):
    if t not in TIMES:raise ValueError("outside finite renewal horizon")
    return sum((p*path[t] for path,p in observed_path_joint(world).items()),ZERO)

def false_iid_renewal_equation(world):
    """For NON-IID worlds this is intentionally a MIS-SPECIFIED counterfactual."""
    p1=source_first_gap_short(world)
    p2=ONE-p1
    pmf={1:p1,2:p2}
    m={0:ZERO}
    for t in TIMES[1:]:
        F_t=sum((p for s,p in pmf.items() if s<=t),ZERO)
        m[t]=F_t+sum((p*m[t-s] for s,p in pmf.items() if s<=t),ZERO)
    return tuple(m[t] for t in TIMES)

def independent_mean_from_gap_vectors(world,t):
    """Third expectation path: 16 exhaustive four-gap products, no source CSV."""
    return sum((independent_gap_vector_probability(world,gaps)*
                observed_counts_from_gaps(gaps)[t] for gaps in GAP_VECTORS),ZERO)

def source_second_gap_condition(world,first):
    if first not in GAP_VALUES:raise ValueError("invalid interval")
    rows=sources(world)
    mass=sum((r["original_source_probability"] for r in rows
              if r["oracle_generator_gap_W1"]==first),ZERO)
    if mass==0:return None
    good=sum((r["original_source_probability"] for r in rows
              if r["oracle_generator_gap_W1"]==first and
                 r["oracle_generator_gap_W2"]==1),ZERO)
    return good/mass

def independently_second_gap_condition(world,first):
    den=sum((independent_gap_vector_probability(world,gaps) for gaps in GAP_VECTORS
             if gaps[0]==first),ZERO)
    if not den:return None
    good=sum((independent_gap_vector_probability(world,gaps) for gaps in GAP_VECTORS
              if gaps[0]==first and gaps[1]==1),ZERO)
    return good/den

def exact_alias_and_mixture_claims():
    a="IID_FAIR";b="STATIC_HIDDEN_EVENT_SENSOR_ALIAS"
    if observed_path_joint(a)!=observed_path_joint(b):
        raise AssertionError("full reported counting joint not identical")
    for bits in EXOGENOUS:
        ra=source_atom(a,bits);rb=source_atom(b,bits)
        for t in TIMES:
            if ra["observed_reported_count_Y"+str(t)]!=rb["observed_reported_count_Y"+str(t)]:
                raise AssertionError("sourcewise counting sensor alias broken")
            if rb["oracle_true_event_count_H"+str(t)]!=0:
                raise AssertionError("static true events must remain zero")
    assert observed_mean_count("IID_FAIR",1)==F(1,2)
    assert observed_mean_count("IID_FAIR",2)==F(5,4)
    assert observed_mean_count("LATENT_RATE_MIXTURE",2)==F(21,16)
    assert observed_mean_count("ALTERNATING_RATE",2)==F(19,16)
    assert observed_mean_count("COMMON_GAP_SHOCK",2)==F(3,2)
    assert source_second_gap_condition("LATENT_RATE_MIXTURE",1)==F(5,8)
    assert source_second_gap_condition("LATENT_RATE_MIXTURE",2)==F(3,8)
    assert source_second_gap_condition("COMMON_GAP_SHOCK",1)==ONE
    assert source_second_gap_condition("COMMON_GAP_SHOCK",2)==ZERO
    assert observed_mean_count("DETERMINISTIC_UNIT",4)==F(4)
    assert observed_mean_count("DETERMINISTIC_TWO",4)==F(2)
    for w in IID_OBS:
        if tuple(observed_mean_count(w,t) for t in TIMES)!=false_iid_renewal_equation(w):
            raise AssertionError("IID renewal equation violated on full horizon")
    for w in NON_IID:
        if tuple(observed_mean_count(w,t) for t in TIMES)==false_iid_renewal_equation(w):
            raise AssertionError("non-IID renewal equation incorrectly claimed exact")
    return True

def world_result(world):
    src=sources(world)
    obs=observed_path_joint(world)
    independent=independent_observed_joint(world)
    if obs!=independent:
        raise AssertionError("full observation path distribution differs from independent 16-gap route")
    for first in GAP_VALUES:
        if source_second_gap_condition(world,first)!=independently_second_gap_condition(world,first):
            raise AssertionError("source/analytic conditional second gap differ")
    mean=tuple(observed_mean_count(world,t) for t in TIMES)
    for t in TIMES:
        if mean[t]!=independent_mean_from_gap_vectors(world,t):
            raise AssertionError("analytic and source expected count differ")
    incorrect=false_iid_renewal_equation(world)
    gapdiff=tuple(mean[t]-incorrect[t] for t in TIMES)
    if world in IID_OBS and any(gapdiff):
        raise AssertionError("independent renewal equation must hold on observed count")
    if world in NON_IID and not any(gapdiff):
        raise AssertionError("non-IID mis-specification should differ on finite support")
    return dict(
        world=world,
        complete_nine_bit_original_sources=512,
        independent_complete_four_gap_joint_normalized=str(sum(
            (independent_gap_vector_probability(world,gaps) for gaps in GAP_VECTORS),ZERO)),
        source_first_gap_short_probability=str(source_first_gap_short(world)),
        observed_mean_count_by_time=[str(v) for v in mean],
        putative_iid_renewal_equation_mean_by_time=[str(v) for v in incorrect],
        observed_minus_putative_iid_renewal_mean_by_time=[str(v) for v in gapdiff],
        oracle_generator_p_W2short_given_W1short=(str(source_second_gap_condition(world,1)) if source_second_gap_condition(world,1) is not None else None),
        oracle_generator_p_W2short_given_W1long=(str(source_second_gap_condition(world,2)) if source_second_gap_condition(world,2) is not None else None),
        observed_five_time_count_path_joint={
            ",".join(map(str,k)):str(v) for k,v in obs.items()},
        true_hidden_count_at_time4_sourcewise=[
            r["oracle_true_event_count_H4"] for r in src],
        independent_gap_vector_full_observation_probability_parity=True
    )

def generate():
    exact_alias_and_mixture_claims()
    results=dict(
       research_id="R245",original_catalogue_id="11-005",
       prescore_freeze_commit=FREEZE,
       scientific_scope="FINITE_ARTIFICIAL_E1_DISCRETE_RENEWAL_GAPS_AND_NONIID_COUNTEREXAMPLES",
       frozen_worlds=9,complete_original_nine_bit_sources=4608,
       gap_support=[1,2],time_support=list(TIMES),
       full_observed_count_path_sourcewise_alias=[
           "IID_FAIR","STATIC_HIDDEN_EVENT_SENSOR_ALIAS"],
       iid_renewal_equation_only_on_iid_observed_counting_processes=True,
       independent_four_gap_product_mixture_reference=True,
       new_real_human_E2=0,new_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[world_result(w) for w in WORLDS]
    )
    out=HERE/"R245_ALL_4608_ORIGINAL_RENEWAL_GAP_SOURCES.csv"
    fields=list(sources("IID_FAIR")[0])
    with out.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");wr.writeheader()
        for w in WORLDS:
            for row in sources(w):
                wr.writerow({k:str(row[k]) for k in fields})
    jfile=HERE/"R245_EXACT_RESULTS.json"
    jfile.write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    machine=dict(
       research_id="R245",original_catalogue_id="11-005",
       frozen_worlds=9,original_complete_source_atoms=4608,
       exact_iid_renewal_equation_true_and_non_iid_counterexamples=True,
       independent_gap_product_full_path_joint_parity=True,
       hidden_static_sensor_observational_alias=True,
       source_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(jfile.read_bytes()).hexdigest(),
       new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R245_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(machine,indent=2)+"\n",encoding="utf-8")
    return machine

class Tests(unittest.TestCase):
    def test_nine_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_full_4608_atoms(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),4608)
    def test_all_mixture_and_sensor_frozen_claims(self):self.assertTrue(exact_alias_and_mixture_claims())
    def test_fair_counts(self):
        self.assertEqual(observed_mean_count("IID_FAIR",2),F(5,4))
    def test_latent_mixture_count(self):
        self.assertEqual(observed_mean_count("LATENT_RATE_MIXTURE",2),F(21,16))
    def test_mixture_conditional_gap(self):
        self.assertEqual(source_second_gap_condition("LATENT_RATE_MIXTURE",1),F(5,8))
        self.assertEqual(source_second_gap_condition("LATENT_RATE_MIXTURE",2),F(3,8))
    def test_alternating_mean(self):self.assertEqual(observed_mean_count("ALTERNATING_RATE",2),F(19,16))
    def test_shared_gap_mean(self):self.assertEqual(observed_mean_count("COMMON_GAP_SHOCK",2),F(3,2))
    def test_static_real_count(self):
        self.assertTrue(all(r["oracle_true_event_count_H4"]==0 for r in sources("STATIC_HIDDEN_EVENT_SENSOR_ALIAS")))
    def test_deterministic_unit(self):self.assertEqual(observed_mean_count("DETERMINISTIC_UNIT",4),F(4))
    def test_deterministic_two(self):self.assertEqual(observed_mean_count("DETERMINISTIC_TWO",4),F(2))
    def test_unsupported_gap_condition_is_json_null(self):
        self.assertIsNone(world_result("DETERMINISTIC_UNIT")["oracle_generator_p_W2short_given_W1long"])
        self.assertIsNone(world_result("DETERMINISTIC_TWO")["oracle_generator_p_W2short_given_W1short"])
    def test_invalid(self):
        with self.assertRaises(ValueError):sources("UNFROZEN")

def _case(world,kind):
    def t(self):
        rows=sources(world)
        if kind=="source_mass":
            self.assertEqual(sum((r["original_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="source_unique":
            keys=("oracle_exogenous_U",)+tuple("oracle_original_R"+str(j)+i
                          for j in (1,2,3,4) for i in ("1","2"))
            self.assertEqual(len({tuple(r[k] for k in keys) for r in rows}),512)
        elif kind=="source_positive":
            self.assertTrue(all(r["original_source_probability"]>0 for r in rows))
        elif kind=="four_gap_product":
            self.assertEqual(sum((independent_gap_vector_probability(world,g) for g in GAP_VECTORS),ZERO),ONE)
        elif kind=="full_joint":
            self.assertEqual(observed_path_joint(world),independent_observed_joint(world))
        elif kind=="expected_count":
            for at in TIMES:
                self.assertEqual(observed_mean_count(world,at),independent_mean_from_gap_vectors(world,at))
        elif kind=="conditional":
            for first in GAP_VALUES:
                self.assertEqual(source_second_gap_condition(world,first),
                                 independently_second_gap_condition(world,first))
        elif kind=="summary":
            self.assertEqual(world_result(world)["complete_nine_bit_original_sources"],512)
        else:raise AssertionError("not frozen")
    return t
for _w in WORLDS:
    for _kind in ("source_mass","source_unique","source_positive","four_gap_product",
                  "full_joint","expected_count","conditional","summary"):
        setattr(Tests,"test_"+_w.lower()+"_"+_kind,_case(_w,_kind))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r245"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
