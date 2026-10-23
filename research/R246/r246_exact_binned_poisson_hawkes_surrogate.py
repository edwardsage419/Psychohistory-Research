#!/usr/bin/env python3
"""R246 finite four-bin Bernoulli self-excitation, NOT actual Poisson or Hawkes.

Four observed bins, each at most one event; conditional probability from
2-bit discrete thresholds. This cannot represent continuous-time Poisson's
nonzero multiple-event-per-bin probability or continuous Hawkes intensity.
Nine complete 9-bit exogenous source worlds (512 each; 4608 total).
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from functools import lru_cache
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="7e3c7efff3da87d3e1cde8cc5db813c1c8650707"
ONE=F(1);ZERO=F(0)
BITS=(0,1)
STEPS=(1,2,3,4)
EXOG=tuple(itertools.product(BITS,repeat=9))
PATHS=tuple(itertools.product(BITS,repeat=4))
WORLDS=(
 "IID_LOW","IID_HIGH","SELF_EXCITING_LAG1","REFRACTORY_LAG1",
 "STATIC_LATENT_RATE_MIXTURE","ALTERNATING_EXOGENOUS_RATE",
 "COMMON_SHOCK_ALL_BINS","STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS",
 "SELF_EXCITING_TWO_LAG"
)

def verify_world(world):
    if world not in WORLDS:raise ValueError("not pre-frozen finite event world")

def hazard(world,k,history,u):
    verify_world(world)
    if k not in STEPS or len(history)!=k-1 or u not in BITS:
        raise ValueError("invalid bin/index or latent source")
    last=history[-1] if history else 0
    two=history[-2] if len(history)>=2 else 0
    if world=="IID_LOW":return F(1,4)
    if world=="IID_HIGH":return F(3,4)
    if world in ("SELF_EXCITING_LAG1","STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS"):
        return F(1,4)+F(last,2)
    if world=="REFRACTORY_LAG1":return F(1,2)-F(last,4)
    if world=="STATIC_LATENT_RATE_MIXTURE":return F(3,4) if u==0 else F(1,4)
    if world=="ALTERNATING_EXOGENOUS_RATE":return F(1,4) if k%2 else F(3,4)
    if world=="COMMON_SHOCK_ALL_BINS":return F(1,2) if k==1 else F(history[0])
    if world=="SELF_EXCITING_TWO_LAG":return F(1,4)+F(last+two,4)
    raise AssertionError("unsupported artificial event mechanism")

def simulate(world,bits):
    verify_world(world)
    if len(bits)!=9 or any(z not in BITS for z in bits):
        raise ValueError("complete original nine-bit source required")
    u=bits[0]
    path=[];rates=[]
    for k in STEPS:
        p=hazard(world,k,path,u)
        if p*4 not in (0,1,2,3,4):raise AssertionError("hazard not quantized exactly")
        if world=="COMMON_SHOCK_ALL_BINS":
            r=2*bits[1]+bits[2]
        else:
            r=2*bits[2*k-1]+bits[2*k]
        path.append(int(r<4*p))
        rates.append(p)
    obs=tuple(path)
    hidden=(0,0,0,0) if world=="STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS" else obs
    return obs,hidden,tuple(rates)

def source_atom(world,bits):
    obs,hidden,rates=simulate(world,bits)
    out={"world":world,"oracle_hidden_U":bits[0]}
    for k in STEPS:
        out["oracle_exogenous_R"+str(k)+"1"]=bits[2*k-1]
        out["oracle_exogenous_R"+str(k)+"2"]=bits[2*k]
        out["observed_event_Y"+str(k)]=obs[k-1]
        out["observed_accumulated_count_N"+str(k)]=sum(obs[:k])
        out["oracle_generator_hazard_p"+str(k)]=rates[k-1]
        out["oracle_hidden_true_event_H"+str(k)]=hidden[k-1]
    out["original_exogenous_source_probability"]=F(1,512)
    return out

@lru_cache(maxsize=None)
def sources(world):
    verify_world(world)
    rows=tuple(source_atom(world,b) for b in EXOG)
    if len(rows)!=512 or sum((r["original_exogenous_source_probability"] for r in rows),ZERO)!=ONE:
        raise AssertionError("incomplete original 9-bit finite event source universe")
    return rows

@lru_cache(maxsize=None)
def observed_joint(world):
    d=defaultdict(F)
    for r in sources(world):
        path=tuple(r["observed_event_Y"+str(k)] for k in STEPS)
        d[path]+=r["original_exogenous_source_probability"]
    return dict(sorted(d.items()))

def independent_hazard(world,k,history,u):
    """Independent conditional Bernoulli formula, not calling source simulator."""
    if world=="IID_LOW":return F(1,4)
    if world=="IID_HIGH":return F(3,4)
    if world in ("SELF_EXCITING_LAG1","STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS"):
        return F(1,4)+(F(1,2)*history[-1] if history else ZERO)
    if world=="REFRACTORY_LAG1":return F(1,2)-(F(1,4)*history[-1] if history else ZERO)
    if world=="STATIC_LATENT_RATE_MIXTURE":return F(3,4) if u==0 else F(1,4)
    if world=="ALTERNATING_EXOGENOUS_RATE":return F(1,4) if k in (1,3) else F(3,4)
    if world=="SELF_EXCITING_TWO_LAG":
        return F(1,4)+sum((F(history[-j],4) for j in (1,2) if j<=len(history)),ZERO)
    raise AssertionError("no independent probability product")

def independent_probability(world,path):
    verify_world(world)
    if path not in PATHS:raise ValueError("not finite four-bin event path")
    if world=="COMMON_SHOCK_ALL_BINS":
        return F(1,2) if path in ((0,0,0,0),(1,1,1,1)) else ZERO
    def product(u):
        p=ONE
        for k in STEPS:
            cond=independent_hazard(world,k,path[:k-1],u)
            p*=cond if path[k-1] else ONE-cond
        return p
    if world=="STATIC_LATENT_RATE_MIXTURE":
        return (product(0)+product(1))/2
    return product(0)

def independent_joint(world):
    return {path:independent_probability(world,path) for path in PATHS
            if independent_probability(world,path)>0}

def prob_event(world,k):
    if k not in STEPS:raise ValueError("outside horizon")
    return sum((p*path[k-1] for path,p in observed_joint(world).items()),ZERO)

def expected_count(world,k):
    return sum((prob_event(world,j) for j in STEPS if j<=k),ZERO)

def adjacent_covariance(world):
    p12=sum((p*path[0]*path[1] for path,p in observed_joint(world).items()),ZERO)
    return p12-prob_event(world,1)*prob_event(world,2)

def conditional_event(world,k,history):
    if k not in STEPS or len(history)!=k-1 or any(x not in BITS for x in history):
        raise ValueError("unsupported observed event history")
    j=observed_joint(world)
    mass=sum((p for path,p in j.items() if path[:k-1]==history),ZERO)
    if mass==ZERO:return None
    positive=sum((p for path,p in j.items() if path[:k-1]==history and path[k-1]==1),ZERO)
    return positive/mass

def conditioned_second(world,first):
    return conditional_event(world,2,(first,))

def observation_aliases_and_frozen_claims():
    base="SELF_EXCITING_LAG1";alias="STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS"
    if observed_joint(base)!=observed_joint(alias):
        raise AssertionError("artificial self-excitation sourcewise report alias broken")
    for bits in EXOG:
        aa=simulate(base,bits)
        bb=simulate(alias,bits)
        if aa[0]!=bb[0] or any(bb[1]):
            raise AssertionError("same source observations vs stationary true events invalid")
    cov={
      "IID_LOW":ZERO,
      "IID_HIGH":ZERO,
      "SELF_EXCITING_LAG1":F(3,32),
      "REFRACTORY_LAG1":F(-1,16),
      "STATIC_LATENT_RATE_MIXTURE":F(1,16),
      "ALTERNATING_EXOGENOUS_RATE":ZERO,
      "COMMON_SHOCK_ALL_BINS":F(1,4),
      "STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS":F(3,32)
    }
    for w,x in cov.items():
        if adjacent_covariance(w)!=x:
            raise AssertionError("frozen first two bin covariance formula failed")
    assert prob_event(base,1)==F(1,4)
    assert prob_event(base,2)==F(3,8)
    assert conditioned_second(base,1)==F(3,4)
    assert conditioned_second(base,0)==F(1,4)
    mix="STATIC_LATENT_RATE_MIXTURE"
    assert prob_event(mix,1)==prob_event(mix,2)==F(1,2)
    assert conditioned_second(mix,1)==F(5,8)
    assert conditioned_second(mix,0)==F(3,8)
    two="SELF_EXCITING_TWO_LAG"
    assert conditional_event(two,3,(1,0))==F(1,2)
    assert conditional_event(two,3,(0,0))==F(1,4)
    return True

def result_for_world(world):
    obs=observed_joint(world)
    if obs!=independent_joint(world):
        raise AssertionError("complete observed path violates independent event product law")
    means=[prob_event(world,k) for k in STEPS]
    cumul=[expected_count(world,k) for k in STEPS]
    cov=adjacent_covariance(world)
    return dict(
       world=world,complete_original_nine_bit_source_atoms=512,
       observed_full_four_bin_path_support_size=len(obs),
       observed_event_probability_by_bin=[str(x) for x in means],
       observed_expected_cumulative_events_by_bin=[str(x) for x in cumul],
       observed_first_second_bin_covariance=str(cov),
       observed_p_bin2_event_given_bin1_event=str(conditioned_second(world,1)) if conditioned_second(world,1) is not None else None,
       observed_p_bin2_event_given_bin1_no_event=str(conditioned_second(world,0)) if conditioned_second(world,0) is not None else None,
       observed_p_bin3_event_given_bin2zero_bin1one=(
           str(conditional_event(world,3,(1,0))) if conditional_event(world,3,(1,0)) is not None else None),
       observed_p_bin3_event_given_bin2zero_bin1zero=(
           str(conditional_event(world,3,(0,0))) if conditional_event(world,3,(0,0)) is not None else None),
       complete_observed_four_bin_event_joint={
           "".join(map(str,k)):str(v) for k,v in obs.items()},
       oracle_true_hidden_events_sourcewise=[
           "".join(str(r["oracle_hidden_true_event_H"+str(k)]) for k in STEPS)
           for r in sources(world)],
       independent_conditional_Bernoulli_path_product_parity=True
    )

def generate():
    observation_aliases_and_frozen_claims()
    j=dict(
       research_id="R246",original_catalogue_id="11-006",
       prescore_freeze_commit=FREEZE,
       scientific_scope="FINITE_ARTIFICIAL_E1_BERNOULLI_EVENT_SURROGATE_NOT_CONTINUOUS_POISSON_HAWKES",
       frozen_worlds=9,original_nine_bit_event_source_atoms=4608,
       true_continuous_Poisson_Hawkes_reproduction=False,
       only_zero_or_one_event_per_bin=True,
       true_Poisson_multiple_events_per_bin_probability_for_positive_intensity="strictly_positive_unmodeled",
       sourcewise_observation_alias=["SELF_EXCITING_LAG1","STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS"],
       all_path_probabilities_independent_closed_hazard_product=True,
       new_real_human_E2=0,new_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[result_for_world(w) for w in WORLDS]
    )
    p=HERE/"R246_ALL_4608_ORIGINAL_BINNED_EVENT_SOURCES.csv"
    fields=list(sources("IID_LOW")[0])
    with p.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");wr.writeheader()
        for w in WORLDS:
            for row in sources(w):
                wr.writerow({k:str(row[k]) for k in fields})
    out=HERE/"R246_EXACT_RESULTS.json"
    out.write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    rec=dict(research_id="R246",original_catalogue_id="11-006",
        frozen_worlds=9,complete_original_nine_bit_atoms=4608,
        distinct_from_true_Poisson_Hawkes_processes=True,
        independent_conditional_Bernoulli_full_path_probability=True,
        latent_heterogeneity_vs_self_excitation_disambiguated=True,
        source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
        new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R246_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
    return rec

class Tests(unittest.TestCase):
    def test_nine_frozen(self):self.assertEqual(len(WORLDS),9)
    def test_all_4608_complete(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),4608)
    def test_covariances_and_sensor_alias(self):self.assertTrue(observation_aliases_and_frozen_claims())
    def test_sourcewise_hidden_static(self):
        self.assertTrue(all(all(r["oracle_hidden_true_event_H"+str(k)]==0 for k in STEPS)
                            for r in sources("STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS")))
    def test_negative_covariance(self):
        self.assertEqual(adjacent_covariance("REFRACTORY_LAG1"),F(-1,16))
    def test_positive_covariance_noncausal(self):
        self.assertEqual(adjacent_covariance("STATIC_LATENT_RATE_MIXTURE"),F(1,16))
    def test_excitation(self):
        self.assertEqual(conditioned_second("SELF_EXCITING_LAG1",1),F(3,4))
        self.assertEqual(conditioned_second("SELF_EXCITING_LAG1",0),F(1,4))
    def test_latent_conditional(self):
        self.assertEqual(conditioned_second("STATIC_LATENT_RATE_MIXTURE",1),F(5,8))
    def test_two_lag(self):
        self.assertEqual(conditional_event("SELF_EXCITING_TWO_LAG",3,(1,0)),F(1,2))
        self.assertEqual(conditional_event("SELF_EXCITING_TWO_LAG",3,(0,0)),F(1,4))
    def test_common_shock(self):
        self.assertEqual(set(observed_joint("COMMON_SHOCK_ALL_BINS")), {(0,0,0,0),(1,1,1,1)})
    def test_positive_support(self):
        self.assertTrue(all(v>0 for v in observed_joint("IID_LOW").values()))
    def test_unknown(self):
        with self.assertRaises(ValueError):sources("NOT_IN_FROZEN_WORLD_LIST")

def _case(world,kind):
    def t(self):
        rows=sources(world)
        if kind=="mass":
            self.assertEqual(sum((r["original_exogenous_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="unique":
            keys=("oracle_hidden_U",)+tuple("oracle_exogenous_R"+str(k)+s for k in STEPS for s in ("1","2"))
            self.assertEqual(len({tuple(r[k] for k in keys) for r in rows}),512)
        elif kind=="positive":
            self.assertTrue(all(r["original_exogenous_source_probability"]>0 for r in rows))
        elif kind=="joint":
            self.assertEqual(observed_joint(world),independent_joint(world))
        elif kind=="joint_mass":
            self.assertEqual(sum(observed_joint(world).values(),ZERO),ONE)
        elif kind=="expected_count":
            self.assertEqual(expected_count(world,4),sum((prob_event(world,k) for k in STEPS),ZERO))
        elif kind=="increment_sums":
            for r in rows:
                for k in STEPS:
                    self.assertEqual(r["observed_accumulated_count_N"+str(k)],
                                     sum(r["observed_event_Y"+str(j)] for j in STEPS if j<=k))
        elif kind=="result":
            self.assertEqual(result_for_world(world)["complete_original_nine_bit_source_atoms"],512)
        else:raise AssertionError("unfrozen test")
    return t

for _w in WORLDS:
    for _kind in ("mass","unique","positive","joint","joint_mass","expected_count","increment_sums","result"):
        setattr(Tests,"test_"+_w.lower()+"_"+_kind,_case(_w,_kind))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["r246"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
