#!/usr/bin/env python3
"""R256 finite discrete-time capacity-2 queue with full nine-bit source laws.

Four bins, at most one arrival and one service per bin, nine frozen worlds.
Not a continuous-time M/M/1 model: no Poisson arrivals, no exponential
service times, no infinite waiting room and no actual customer data.
Independent conditional Markov transition path products audit every source.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent
FREEZE="d16f5d3c5cecade05e43c583573b34d0571801bb"
ZERO=F(0);ONE=F(1)
BITS=(0,1)
EXOG=tuple(itertools.product(BITS,repeat=9))
CAPACITY=2
TIME_STEPS=(1,2,3,4)
BASE="BALANCED_INDEPENDENT_HALF_HALF"
SENSOR="STATIC_EMPTY_TRUE_QUEUE_SENSOR_ALIAS"
SHARED="SHARED_DEMAND_ENV_HALF_HALF"
AFIRST="ARRIVAL_FIRST_BALANCED_HALF_HALF"
CONFIG={
 "IDLE_NO_ARRIVALS":(ZERO,F(1,2),"SERVICE_FIRST"),
 "FAST_SERVICE_HALF_ARRIVAL":(F(1,2),ONE,"SERVICE_FIRST"),
 BASE:(F(1,2),F(1,2),"SERVICE_FIRST"),
 "DEMAND_ALWAYS_HALF_SERVICE":(ONE,F(1,2),"SERVICE_FIRST"),
 "NO_SERVICE_HALF_ARRIVAL":(F(1,2),ZERO,"SERVICE_FIRST"),
 "DEMAND_ALWAYS_NO_SERVICE":(ONE,ZERO,"SERVICE_FIRST"),
 AFIRST:(F(1,2),F(1,2),"ARRIVAL_FIRST"),
 SHARED:(F(1,2),F(1,2),"SERVICE_FIRST"),
 SENSOR:(F(1,2),F(1,2),"SERVICE_FIRST")
}
WORLDS=tuple(CONFIG)
def check(w):
    if w not in CONFIG:raise ValueError("unfrozen queue world")
def realized_requests(w,bits):
    check(w)
    if len(bits)!=9 or any(x not in BITS for x in bits):
        raise ValueError("nine exogenous fair bits required")
    u=bits[0]
    rate_a,rate_s,order=CONFIG[w]
    arr=[];serv=[]
    for k in range(4):
        original_a=bits[1+2*k]
        original_s=bits[2+2*k]
        a=u if w==SHARED else (original_a if rate_a==F(1,2) else int(rate_a==ONE))
        s=original_s if rate_s==F(1,2) else int(rate_s==ONE)
        arr.append(a);serv.append(s)
    return tuple(arr),tuple(serv)
def direct_queue_step(q,a,s,policy):
    """Procedural source generator with admissions, departures and rejection."""
    if q not in (0,1,2) or a not in BITS or s not in BITS:
        raise ValueError("invalid finite queue state or request")
    if policy=="SERVICE_FIRST":
        served=int(q>0 and s==1)
        after=q-served
        admitted=int(a==1 and after<CAPACITY)
        rejected=a-admitted
        next_q=after+admitted
    elif policy=="ARRIVAL_FIRST":
        admitted=int(a==1 and q<CAPACITY)
        rejected=a-admitted
        after=q+admitted
        served=int(s==1 and after>0)
        next_q=after-served
    else:raise ValueError("unfrozen timing policy")
    assert next_q==q+a-served-rejected and 0<=next_q<=CAPACITY
    return next_q,served,rejected,admitted
def source_atom(w,bits):
    arr,svc=realized_requests(w,bits)
    _,_,order=CONFIG[w]
    q=0
    states=[];served=[];rejected=[];admitted=[]
    for a,s in zip(arr,svc):
        q,d,r,accept=direct_queue_step(q,a,s,order)
        states.append(q);served.append(d);rejected.append(r);admitted.append(accept)
    if q!=sum(arr)-sum(served)-sum(rejected):
        raise AssertionError("four-step queue flow conservation failed")
    out={"world":w,"oracle_original_shared_environment_U":bits[0],
         "frozen_event_order":order}
    for k in range(4):
        out["oracle_original_arrival_bit_A"+str(k+1)]=bits[1+2*k]
        out["oracle_original_service_bit_S"+str(k+1)]=bits[2+2*k]
        out["oracle_exogenous_realized_offered_arrival_a"+str(k+1)]=arr[k]
        out["oracle_exogenous_realized_available_service_s"+str(k+1)]=svc[k]
        out["observed_reported_queue_Q"+str(k+1)]=states[k]
        out["oracle_model_served_d"+str(k+1)]=served[k]
        out["oracle_model_rejected_r"+str(k+1)]=rejected[k]
        out["oracle_model_admitted_g"+str(k+1)]=admitted[k]
        out["oracle_true_hidden_physical_queue_H"+str(k+1)]=0 if w==SENSOR else states[k]
    out["oracle_total_offered"]=sum(arr)
    out["oracle_total_admitted"]=sum(admitted)
    out["oracle_total_served"]=sum(served)
    out["oracle_total_rejected"]=sum(rejected)
    out["original_complete_ninebit_source_probability"]=F(1,512)
    return out
@lru_cache(None)
def sources(w):
    check(w)
    rows=tuple(source_atom(w,b) for b in EXOG)
    assert len(rows)==512 and sum((z["original_complete_ninebit_source_probability"] for z in rows),ZERO)==ONE
    return rows
@lru_cache(None)
def original_queue_path_joint(w):
    d=defaultdict(F)
    for z in sources(w):
        path=tuple(z["observed_reported_queue_Q"+str(k)] for k in TIME_STEPS)
        d[path]+=z["original_complete_ninebit_source_probability"]
    return dict(sorted(d.items()))
def independent_closed_next_state(q,a,s,order):
    """Algebraic state map; does NOT call source direct_queue_step."""
    if order=="SERVICE_FIRST":
        residual=max(q-s,0)
        return residual+(a if residual<2 else 0)
    if order=="ARRIVAL_FIRST":
        take=min(a,2-q)
        return max(q+take-s,0)
    raise ValueError("invalid independent Markov policy")
def independent_kernel(arrival_probability,service_probability,policy):
    """Analytic 3x3 transition from all four independent Bernoulli event cases."""
    kernel={}
    for q in range(3):
        row=defaultdict(F)
        for a,s in itertools.product(BITS,repeat=2):
            mass=(arrival_probability if a else ONE-arrival_probability)*(
                 service_probability if s else ONE-service_probability)
            new=independent_closed_next_state(q,a,s,policy)
            assert 0<=new<=2
            row[new]+=mass
        assert sum(row.values(),ZERO)==ONE
        kernel[q]=dict(row)
    return kernel
def independent_path_joint(w):
    """Full Q1..4 conditional Markov product with shared-U mixing, no original bit paths."""
    check(w)
    pa,ps,order=CONFIG[w]
    conditions=((ZERO,F(1,2)),(ONE,F(1,2))) if w==SHARED else ((pa,ONE),)
    joint=defaultdict(F)
    for qpath in itertools.product((0,1,2),repeat=4):
        mass=ZERO
        for ar,environment_mass in conditions:
            T=independent_kernel(ar,ps,order)
            qold=0;likelihood=ONE
            for qnew in qpath:
                likelihood*=T[qold].get(qnew,ZERO)
                qold=qnew
            mass+=environment_mass*likelihood
        if mass:joint[qpath]+=mass
    assert sum(joint.values(),ZERO)==ONE
    return dict(sorted(joint.items()))
def source_statistics(w):
    rows=sources(w)
    stats={
      "mean_reported_Q_by_time":[sum((F(z["observed_reported_queue_Q"+str(k)],512) for z in rows),ZERO) for k in TIME_STEPS],
      "mean_total_offered":sum((F(z["oracle_total_offered"],512) for z in rows),ZERO),
      "mean_total_served":sum((F(z["oracle_total_served"],512) for z in rows),ZERO),
      "mean_total_rejected":sum((F(z["oracle_total_rejected"],512) for z in rows),ZERO)
    }
    assert stats["mean_total_offered"]==stats["mean_total_served"]+stats["mean_total_rejected"]+stats["mean_reported_Q_by_time"][-1]
    return stats
def frozen_claims():
    for w in WORLDS:
        actual=original_queue_path_joint(w)
        independent=independent_path_joint(w)
        if actual!=independent:
            raise AssertionError(f"{w} ninebit source path PMF does not match independent conditional Markov likelihood")
    assert original_queue_path_joint("IDLE_NO_ARRIVALS")=={(0,0,0,0):ONE}
    assert original_queue_path_joint("DEMAND_ALWAYS_NO_SERVICE")=={(1,2,2,2):ONE}
    assert source_statistics("DEMAND_ALWAYS_NO_SERVICE")["mean_total_rejected"]==F(2)
    assert source_statistics("DEMAND_ALWAYS_NO_SERVICE")["mean_total_served"]==ZERO
    def p_first_is_one(w):
        return sum((mass for path,mass in original_queue_path_joint(w).items() if path[0]==1),ZERO)
    assert p_first_is_one(BASE)==F(1,2)
    assert p_first_is_one(AFIRST)==F(1,4)
    def p_0then1(w):
        return sum((mass for path,mass in original_queue_path_joint(w).items() if path[0]==0 and path[1]==1),ZERO)
    assert p_0then1(BASE)==F(1,4)
    assert p_0then1(SHARED)==ZERO
    assert original_queue_path_joint(BASE)==original_queue_path_joint(SENSOR)
    for bits in EXOG:
        a=source_atom(BASE,bits)
        b=source_atom(SENSOR,bits)
        assert all(a["observed_reported_queue_Q"+str(k)]==
                   b["observed_reported_queue_Q"+str(k)] for k in TIME_STEPS)
        assert all(b["oracle_true_hidden_physical_queue_H"+str(k)]==0 for k in TIME_STEPS)
    return True
def world_result(w):
    joint=original_queue_path_joint(w)
    if joint!=independent_path_joint(w):raise AssertionError("full path law not independently verified")
    stats=source_statistics(w)
    return dict(world=w,frozen_source_arrival_probability=str(CONFIG[w][0]),
        frozen_source_service_probability=str(CONFIG[w][1]),
        frozen_event_order=CONFIG[w][2],
        full_original_ninebit_source_atoms=512,
        exact_observed_queue_path_joint={"".join(map(str(k))):str(v) for k,v in joint.items()},
        observed_queue_path_support_size=len(joint),
        exact_reported_expected_Q_each_bin=[str(x) for x in stats["mean_reported_Q_by_time"]],
        oracle_expected_total_offered=str(stats["mean_total_offered"]),
        oracle_expected_total_served=str(stats["mean_total_served"]),
        oracle_expected_total_rejected=str(stats["mean_total_rejected"]),
        full_four_slot_source_conservation=True,
        independent_conditional_markov_path_likelihood_verified=True,
        true_hidden_queue_always_empty_if_sensor_alias=(w==SENSOR))
def emit():
    frozen_claims()
    data=dict(research_id="R256",original_catalogue_id="11-016",
        prescore_freeze_commit=FREEZE,
        scientific_scope="FINITE_ARTIFICIAL_E1_FOUR_SLOT_CAPACITY_TWO_DISCRETE_QUEUE_NOT_MM1",
        frozen_worlds=9,full_original_ninebit_source_atoms=4608,
        maximum_queue_capacity_including_service=2,
        independent_full_Q1_Q2_Q3_Q4_path_laws=True,
        not_continuous_time_M_M_1_reproduction=True,
        demand_always_no_service_path="1222",
        balanced_service_first_P_Q1_one="1/2",
        balanced_arrival_first_P_Q1_one="1/4",
        independent_balanced_P_Q1_zero_Q2_one="1/4",
        shared_demand_environment_P_Q1_zero_Q2_one="0",
        sensor_report_full_sourcewise_alias=[BASE,SENSOR],
        new_real_human_E2=0,new_real_historical_E3=0,
        R073="FROZEN",PESEN_v0_1="FROZEN",
        world_results=[world_result(w) for w in WORLDS])
    out=HERE/"R256_ALL_4608_ORIGINAL_FOUR_SLOT_QUEUE_SOURCE_ATOMS.csv"
    keys=list(sources(WORLDS[0])[0])
    with out.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=keys,lineterminator="\n");wr.writeheader()
        for w in WORLDS:
            for z in sources(w):wr.writerow({k:str(z[k]) for k in keys})
    res=HERE/"R256_EXACT_RESULTS.json"
    res.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R256",original_catalogue_id="11-016",
        frozen_worlds=9,all_original_ninebit_sources=4608,
        independent_conditional_Markov_path_probabilities=True,
        each_source_inventory_flow_conservation=True,
        nonexchangeable_arrival_service_order_verified=True,
        sourcewise_report_alias_vs_true_empty_queue=True,
        source_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(res.read_bytes()).hexdigest(),
        new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R256_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt
class Tests(unittest.TestCase):
    def test_nine(self):self.assertEqual(len(WORLDS),9)
    def test_4608(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),4608)
    def test_frozen(self):self.assertTrue(frozen_claims())
    def test_idle(self):self.assertEqual(original_queue_path_joint("IDLE_NO_ARRIVALS"),{(0,0,0,0):ONE})
    def test_demand_always_no_service(self):
        self.assertEqual(original_queue_path_joint("DEMAND_ALWAYS_NO_SERVICE"),{(1,2,2,2):ONE})
    def test_policy_first_slot(self):
        self.assertEqual(sum((v for k,v in original_queue_path_joint(BASE).items() if k[0]==1),ZERO),F(1,2))
        self.assertEqual(sum((v for k,v in original_queue_path_joint(AFIRST).items() if k[0]==1),ZERO),F(1,4))
    def test_shared_demand_0then1_impossible(self):
        self.assertEqual(sum((v for k,v in original_queue_path_joint(SHARED).items() if k[0]==0 and k[1]==1),ZERO),ZERO)
    def test_sensor_alias(self):self.assertEqual(original_queue_path_joint(BASE),original_queue_path_joint(SENSOR))
    def test_full_conservation(self):
        self.assertEqual(source_statistics(BASE)["mean_total_offered"],
          source_statistics(BASE)["mean_total_served"]+source_statistics(BASE)["mean_total_rejected"]+
          source_statistics(BASE)["mean_reported_Q_by_time"][-1])
    def test_unfrozen(self):
        with self.assertRaises(ValueError):sources("UNKNOWN_QUEUE")
def _case(w,k):
    def test(self):
        rows=sources(w)
        if k=="mass":self.assertEqual(sum((z["original_complete_ninebit_source_probability"] for z in rows),ZERO),ONE)
        elif k=="unique":
            cols=["oracle_original_shared_environment_U"]+[f"oracle_original_{typ}_bit_{typ[:1]}{i}" for i in () for typ in ()]
            cols=["oracle_original_shared_environment_U"]+[f"oracle_original_{typ}_bit_{tag}{i}" for i in TIME_STEPS for typ,tag in (("arrival","A"),("service","S"))]
            self.assertEqual(len({tuple(z[c] for c in cols) for z in rows}),512)
        elif k=="positive":self.assertTrue(all(z["original_complete_ninebit_source_probability"]==F(1,512) for z in rows))
        elif k=="joint":self.assertEqual(original_queue_path_joint(w),independent_path_joint(w))
        elif k=="capacity":self.assertTrue(all(all(z["observed_reported_queue_Q"+str(i)] in (0,1,2) for i in TIME_STEPS) for z in rows))
        elif k=="conservation":
            for z in rows:
                self.assertEqual(z["oracle_total_offered"],z["oracle_total_served"]+z["oracle_total_rejected"]+z["observed_reported_queue_Q4"])
        elif k=="expectations":self.assertEqual(source_statistics(w)["mean_total_offered"],source_statistics(w)["mean_total_served"]+source_statistics(w)["mean_total_rejected"]+source_statistics(w)["mean_reported_Q_by_time"][-1])
        elif k=="summary":self.assertEqual(world_result(w)["full_original_ninebit_source_atoms"],512)
        else:raise AssertionError("not frozen test")
    return test
for w in WORLDS:
    for k in ("mass","unique","positive","joint","capacity","conservation","expectations","summary"):
        setattr(Tests,"test_"+w.lower()+"_"+k,_case(w,k))
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r256"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
