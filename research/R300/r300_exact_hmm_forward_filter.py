#!/usr/bin/env python3
"""R300 exact two-hidden-state HMM filter on all 128 complete labeled artificial sources."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="ef56b01c3c2b5da98e433f9d2fefdd61fd9028c3"
Z,O=F(0),F(1)
ACCURACY=F(3,4)
MODELS=("PERSISTENT_HMM","IID_HIDDEN_NEGATIVE_CONTROL")
STAY={"PERSISTENT_HMM":F(3,4),"IID_HIDDEN_NEGATIVE_CONTROL":F(1,2)}
OBSERVATIONS=tuple("".join(map(str,bits)) for bits in itertools.product((0,1),repeat=4))
TIMES=(1,2,3,4)
SOURCE_NAME="R300_ALL_128_ORIGINAL_HMM_PREFIX_SOURCES.csv"
RESULT_NAME="R300_EXACT_HMM_FORWARD_RESULTS.json"
RECEIPT_NAME="R300_MACHINE_RECEIPT.json"

def emission(y,h):
    if y not in (0,1) or h not in (0,1):raise ValueError("not binary")
    return ACCURACY if y==h else O-ACCURACY

@lru_cache(maxsize=300)
def filter_prefix(world,prefix):
    if world not in MODELS or not prefix or len(prefix)>4 or any(x not in "01" for x in prefix):
        raise ValueError("not frozen prefix")
    stay=STAY[world]
    weights=(F(1,2),F(1,2))
    for t,symbol in enumerate(prefix):
        y=int(symbol)
        if t==0:
            old=weights
        else:
            old=(weights[0]*stay+weights[1]*(O-stay),
                 weights[0]*(O-stay)+weights[1]*stay)
        weights=(old[0]*emission(y,0),old[1]*emission(y,1))
    evidence=sum(weights,Z)
    posterior=weights[1]/evidence
    next_state=posterior*stay+(O-posterior)*(O-stay)
    next_observation=next_state*ACCURACY+(O-next_state)*(O-ACCURACY)
    return {"alpha_hidden_0":weights[0],"alpha_hidden_1":weights[1],
       "prefix_evidence":evidence,"posterior_hidden_1":posterior,
       "predictive_next_hidden_1":next_state,"predictive_next_observed_1":next_observation}

def row(world,observation,t):
    if world not in MODELS or observation not in OBSERVATIONS or t not in TIMES:raise ValueError("not original cell")
    prefix=observation[:t]
    return {"world":world,"stay_probability":STAY[world],"emission_match_probability":ACCURACY,
            "full_observation_bits":observation,"prefix_bits":prefix,"prefix_length":t,
            **filter_prefix(world,prefix)}

def allrows():
    return tuple(row(world,ob,t) for world in MODELS for ob in OBSERVATIONS for t in TIMES)

def verify():
    assert len(OBSERVATIONS)==16 and len(allrows())==128
    assert len(set((r["world"],r["full_observation_bits"],r["prefix_length"]) for r in allrows()))==128
    for world in MODELS:
        for t in TIMES:
            distinct=["".join(b) for b in itertools.product("01",repeat=t)]
            assert sum((filter_prefix(world,p)["prefix_evidence"] for p in distinct),Z)==O
            assert sum((filter_prefix(world,p)["prefix_evidence"] for p in distinct if p[-1]=="1"),Z)==F(1,2)
        for ob in OBSERVATIONS:
            for t in TIMES:
                vals=filter_prefix(world,ob[:t])
                assert Z<vals["prefix_evidence"]<=O
                assert vals["alpha_hidden_0"]+vals["alpha_hidden_1"]==vals["prefix_evidence"]
                assert all(Z<=vals[k]<=O for k in ("posterior_hidden_1",
                   "predictive_next_hidden_1","predictive_next_observed_1"))
                if world=="IID_HIDDEN_NEGATIVE_CONTROL":
                    assert vals["posterior_hidden_1"]==(ACCURACY if ob[t-1]=="1" else O-ACCURACY)
                    assert vals["predictive_next_observed_1"]==F(1,2)
                    assert vals["prefix_evidence"]==F(1,2)**t
    a=filter_prefix("PERSISTENT_HMM","1110")
    b=filter_prefix("PERSISTENT_HMM","0000")
    assert a["posterior_hidden_1"]!=b["posterior_hidden_1"]
    assert a["predictive_next_observed_1"]!=b["predictive_next_observed_1"]
    assert filter_prefix("IID_HIDDEN_NEGATIVE_CONTROL","1110")["posterior_hidden_1"]==filter_prefix("IID_HIDDEN_NEGATIVE_CONTROL","0000")["posterior_hidden_1"]==F(1,4)
    return True

def emit():
    verify()
    cols=("world","stay_probability","emission_match_probability","full_observation_bits",
      "prefix_bits","prefix_length","alpha_hidden_0","alpha_hidden_1","prefix_evidence",
      "posterior_hidden_1","predictive_next_hidden_1","predictive_next_observed_1")
    csvpath=ROOT/SOURCE_NAME
    with csvpath.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n")
        w.writeheader()
        for r in allrows():w.writerow({k:str(r[k]) for k in cols})
    worlds=[]
    for world in MODELS:
        records=[]
        for observation in OBSERVATIONS:
            for t in TIMES:
                r=row(world,observation,t)
                records.append({k:str(r[k]) for k in cols if k not in ("world","stay_probability","emission_match_probability")})
        worlds.append({"world":world,"stay_probability":str(STAY[world]),"source_rows":64,
          "full_sequence_count":16,"complete_source_records":records,
          "evidence_sum_each_prefix_length":{str(t):"1" for t in TIMES}})
    p=filter_prefix("PERSISTENT_HMM","1110")
    q=filter_prefix("PERSISTENT_HMM","0000")
    out={"research_id":"R300","original_catalogue_id":"02-008","freeze_commit":FREEZE,
        "scope":"E1_FINITE_TWO_STATE_KNOWN_HMM_FILTERING_AND_IID_LATENT_NEGATIVE_CONTROL_NO_REAL_DATA",
        "complete_original_source_rows":128,"artificial_worlds":2,
        "original_observation_strings_per_world":16,"prefix_lengths_each":4,
        "history_effect_demo":{
          "persistent_1110_posterior_hidden1":str(p["posterior_hidden_1"]),
          "persistent_0000_posterior_hidden1":str(q["posterior_hidden_1"]),
          "persistent_1110_next_obs1":str(p["predictive_next_observed_1"]),
          "persistent_0000_next_obs1":str(q["predictive_next_observed_1"]),
          "iid_same_last_obs_posterior_hidden1":"1/4",
          "iid_next_observation1":"1/2"},
        "worlds":worlds,"real_human_E2_added":0,"real_animal_E2_added":0,
        "historical_E3_added":0,"parameters_learned_from_empirical_data":False,
        "viterbi_path_decoding_performed":False,"R073":"FROZEN","PESEN_v0_1":"FROZEN"}
    rp=ROOT/RESULT_NAME
    rp.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={"research_id":"R300","freeze_commit":FREEZE,"source_rows":128,
      "source_sha256":hashlib.sha256(csvpath.read_bytes()).hexdigest(),
      "results_sha256":hashlib.sha256(rp.read_bytes()).hexdigest(),
      "new_real_E2":0,"new_historical_E3":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_all(self):self.assertTrue(verify())
    def test_source_rows(self):self.assertEqual(len(allrows()),128)
    def test_worlds(self):self.assertEqual(len(MODELS),2)
    def test_iid_independent(self):self.assertEqual(filter_prefix("IID_HIDDEN_NEGATIVE_CONTROL","110")["predictive_next_observed_1"],F(1,2))
    def test_iid_posterior(self):self.assertEqual(filter_prefix("IID_HIDDEN_NEGATIVE_CONTROL","1110")["posterior_hidden_1"],F(1,4))
    def test_filter_first(self):self.assertEqual(filter_prefix("PERSISTENT_HMM","1")["posterior_hidden_1"],F(3,4))
    def test_past_influences(self):self.assertNotEqual(filter_prefix("PERSISTENT_HMM","1110")["posterior_hidden_1"],filter_prefix("PERSISTENT_HMM","0000")["posterior_hidden_1"])
    def test_bad_world(self):
        with self.assertRaises(ValueError):filter_prefix("MISSING","0")
    def test_bad_prefix(self):
        with self.assertRaises(ValueError):filter_prefix("PERSISTENT_HMM","2")
    def test_bad_t(self):
        with self.assertRaises(ValueError):row("PERSISTENT_HMM","0000",5)

def generated(world,obs,t,kind):
    def case(self):
        r=row(world,obs,t);v=filter_prefix(world,obs[:t])
        if kind=="source":self.assertEqual({k:r[k] for k in v},v)
        elif kind=="mass":self.assertEqual(r["alpha_hidden_0"]+r["alpha_hidden_1"],r["prefix_evidence"])
        elif kind=="predict":self.assertTrue(Z<=r["predictive_next_observed_1"]<=O)
        else:raise AssertionError(kind)
    return case
for world in MODELS:
    for obs in OBSERVATIONS:
        for t in TIMES:
            for kind in ("source","mass","predict"):
                setattr(Tests,f"test_{world.lower()}_{obs}_t{t}_{kind}",generated(world,obs,t,kind))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    m=p.add_mutually_exclusive_group(required=True)
    m.add_argument("--test",action="store_true")
    m.add_argument("--emit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R300"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
