#!/usr/bin/env python3
"""R212: six finite causal DAGs; observational equivalence vs interventions.

Exact artificial SCM source enumeration, fixed independent discrete exogenous
noise. DAG d-separation enumerates open/blocked simple paths, including
collider descendants, for 3-4 node fixed graphs. NO human causal inference.

python r212_exact_causal_dags.py --test
python r212_exact_causal_dags.py --emit
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import unittest
from fractions import Fraction
from pathlib import Path

F=Fraction
Z=F(0)
O=F(1)
WORLDS=("CONFOUND","DIRECT","COMBINED","REVERSE_CAUSAL","COLLIDER","MEDIATOR")
EDGES={
    "CONFOUND":(("C","T"),("C","Y")),
    "DIRECT":(("C","T"),("T","Y")),
    "COMBINED":(("C","T"),("C","Y"),("T","Y")),
    "REVERSE_CAUSAL":(("T","Y"),),
    "COLLIDER":(("T","K"),("U","K"),("U","Y")),
    "MEDIATOR":(("T","M"),("M","Y")),
}
OUT=Path(__file__).resolve().parent


def graph_nodes(world):
    if world not in EDGES:
        raise ValueError("unknown artificial DAG")
    return tuple(sorted({n for edge in EDGES[world] for n in edge}))


def source_states(world):
    if world in ("CONFOUND","DIRECT","COMBINED"):
        return tuple({"C":c,"j":j,"N":int(j==0)}
                     for c,j in itertools.product((0,1),range(4)))
    if world in ("REVERSE_CAUSAL","MEDIATOR"):
        return tuple({"Troot":t,"j":j,"N":int(j==0)}
                     for t,j in itertools.product((0,1),range(4)))
    if world=="COLLIDER":
        return tuple({"Troot":t,"U":u}
                     for t,u in itertools.product((0,1),repeat=2))
    raise ValueError("world unknown")


def structural_equations(world,exogenous,do_T=None):
    if world not in WORLDS or do_T not in (None,0,1):
        raise ValueError("invalid SCM or intervention")
    x=exogenous
    if world in ("CONFOUND","DIRECT","COMBINED"):
        c=x["C"]
        t=(c ^ x["N"]) if do_T is None else do_T
        y=c if world=="CONFOUND" else (t if world=="DIRECT" else (t|c))
        return {"C":c,"T":t,"Y":y}
    if world=="REVERSE_CAUSAL":
        t=x["Troot"] if do_T is None else do_T
        return {"T":t,"Y":t ^ x["N"]}
    if world=="COLLIDER":
        t=x["Troot"] if do_T is None else do_T
        u=x["U"]
        return {"T":t,"U":u,"K":t|u,"Y":u}
    if world=="MEDIATOR":
        t=x["Troot"] if do_T is None else do_T
        m=t ^ x["N"]
        return {"T":t,"M":m,"Y":m}
    raise ValueError("unexpected SCM")


def all_nodes_acyclic(edges):
    nodes={n for a,b in edges for n in (a,b)}
    incoming={v:0 for v in nodes}
    for a,b in edges:
        incoming[b]+=1
    rest=set(nodes)
    while rest:
        ready=sorted(v for v in rest if incoming[v]==0)
        if not ready:
            return False
        for v in ready:
            rest.remove(v)
            for a,b in edges:
                if a==v:
                    incoming[b]-=1
    return True


def descendants(edges,node):
    frontier=[node]
    found=set()
    while frontier:
        v=frontier.pop()
        for a,b in edges:
            if a==v and b not in found:
                found.add(b)
                frontier.append(b)
    found.discard(node)
    return found


def undirected_simple_paths(edges,start,end):
    nodes={v for a,b in edges for v in (a,b)}
    if start not in nodes or end not in nodes:
        raise ValueError("endpoints missing")
    und={v:set() for v in nodes}
    for a,b in edges:
        und[a].add(b)
        und[b].add(a)
    found=[]
    def explore(path):
        current=path[-1]
        if current==end:
            found.append(path)
            return
        for nxt in sorted(und[current]):
            if nxt not in path:
                explore(path+(nxt,))
    explore((start,))
    return tuple(found)


def active_path(edges,path,conditioned=()):
    edges=set(edges)
    conditioned=set(conditioned)
    for i in range(1,len(path)-1):
        prev,mid,nxt=path[i-1],path[i],path[i+1]
        collider=((prev,mid) in edges and (nxt,mid) in edges)
        if collider:
            if mid not in conditioned and not (descendants(edges,mid)&conditioned):
                return False
        elif mid in conditioned:
            return False
    return True


def d_separated(edges,start,end,conditioned=()):
    nodes={n for a,b in edges for n in (a,b)}
    if start not in nodes or end not in nodes or not set(conditioned)<=nodes:
        raise ValueError("d-separation nodes invalid")
    if not all_nodes_acyclic(edges):
        raise ValueError("DAG cycles prohibited")
    return not any(active_path(edges,p,conditioned)
                   for p in undirected_simple_paths(edges,start,end))


def source_distributions(world):
    raw=[]
    sources=source_states(world)
    n=len(sources)
    if n not in (4,8):
        raise AssertionError("source count")
    for x in sources:
        obs=structural_equations(world,x,None)
        do0=structural_equations(world,x,0)
        do1=structural_equations(world,x,1)
        if not (set(obs)==set(do0)==set(do1)==set(graph_nodes(world))):
            raise AssertionError("world nodes mismatch")
        if (do0["T"],do1["T"])!=(0,1):
            raise AssertionError("do operation did not intervene")
        raw.append((x,obs,do0,do1,F(1,n)))
    return tuple(raw)


def joint_obs(raw,keys):
    out={}
    for vals in itertools.product((0,1),repeat=len(keys)):
        out["".join(map(str,vals))]=sum(
            (w for x,obs,d0,d1,w in raw if tuple(obs[v] for v in keys)==vals),Z)
    if sum(out.values(),Z)!=1:
        raise AssertionError("observational mass")
    return out


def conditional_obs(raw,node,value,given):
    """Exact weighted observational conditional mean, with positivity check."""
    if not given:
        denominator=sum((w for x,obs,d0,d1,w in raw),Z)
        return sum((w*obs[node] for x,obs,d0,d1,w in raw),Z)/denominator
    denom=sum((w for x,obs,d0,d1,w in raw
               if all(obs.get(k)==v for k,v in given.items())),Z)
    if denom==0:
        raise ValueError("no support for observational conditional")
    return sum((w*obs[node] for x,obs,d0,d1,w in raw
                if all(obs.get(k)==v for k,v in given.items())),Z)/denom


def interventional_effect(raw):
    effect=sum((w*(d1["Y"]-d0["Y"]) for x,obs,d0,d1,w in raw),Z)
    mean_do1=sum((w*d1["Y"] for x,obs,d0,d1,w in raw),Z)
    mean_do0=sum((w*d0["Y"] for x,obs,d0,d1,w in raw),Z)
    if effect != mean_do1-mean_do0:
        raise AssertionError("two independent intervention mean expressions differ")
    return effect,mean_do0,mean_do1


def naive_diff(raw):
    return conditional_obs(raw,"Y",1,{"T":1})-conditional_obs(raw,"Y",1,{"T":0})


def backdoor_adjust_C(raw):
    """Pre-treatment C only, with full positivity in three applicable worlds."""
    pc0=sum((w for x,obs,d0,d1,w in raw if obs.get("C")==0),Z)
    pc1=sum((w for x,obs,d0,d1,w in raw if obs.get("C")==1),Z)
    if pc0+pc1!=1 or pc0<=0 or pc1<=0:
        raise ValueError("observable pre-treatment C not present with full support")
    return sum((p*(conditional_obs(raw,"Y",1,{"T":1,"C":c})-
                   conditional_obs(raw,"Y",1,{"T":0,"C":c}))
                for c,p in ((0,pc0),(1,pc1))),Z)


def collider_selection_diff(raw):
    return (conditional_obs(raw,"Y",1,{"T":1,"K":1})-
            conditional_obs(raw,"Y",1,{"T":0,"K":1}))


def mediator_conditioned_diff(raw):
    # All T/M cells have positive support because the independent N has 1/4 flip.
    pm={m:sum((w for x,obs,d0,d1,w in raw if obs.get("M")==m),Z) for m in (0,1)}
    if sum(pm.values(),Z)!=1:
        raise AssertionError("mediator distribution")
    return sum((prob*(conditional_obs(raw,"Y",1,{"T":1,"M":m})-
                      conditional_obs(raw,"Y",1,{"T":0,"M":m}))
                for m,prob in pm.items()),Z)


def compute():
    rows=[]
    worlds=[]
    source_cache={}
    for world in WORLDS:
        dag=EDGES[world]
        if not all_nodes_acyclic(dag):
            raise AssertionError("not a DAG")
        raw=source_distributions(world)
        source_cache[world]=raw
        if sum((w for x,obs,d0,d1,w in raw),Z)!=O:
            raise AssertionError("source mass")
        doeffect,do0,do1=interventional_effect(raw)
        naive=naive_diff(raw)
        result={
            "world":world,
            "graph_directed_edges":["->".join(e) for e in dag],
            "observed_graph_nodes":list(graph_nodes(world)),
            "complete_exogenous_source_records":len(raw),
            "true_exogenous_source_probability_sum":"1",
            "true_do_T_0_mean_outcome_exact":str(do0),
            "true_do_T_1_mean_outcome_exact":str(do1),
            "true_average_causal_effect_exact":str(doeffect),
            "naive_observed_Y_mean_difference_T1_minus_T0_exact":str(naive),
            "observational_TY_2_by_2_distribution":
                {k:str(v) for k,v in joint_obs(raw,("T","Y")).items()},
            "DAG_all_edges_acyclic":True,
            "T_Y_d_separated_without_conditioning":
                d_separated(dag,"T","Y"),
        }
        if world in ("CONFOUND","DIRECT","COMBINED"):
            adjustment=backdoor_adjust_C(raw)
            if adjustment!=doeffect:
                raise AssertionError("valid baseline backdoor adjustment fails")
            result["valid_pre_treatment_C_backdoor_adjusted_total_effect"]=str(adjustment)
            result["T_Y_d_separated_after_condition_C"]=d_separated(dag,"T","Y",("C",))
        if world=="COLLIDER":
            collider=collider_selection_diff(raw)
            if collider!=F(-1,2):
                raise AssertionError("collider induced correlation counterexample wrong")
            result["conditioning_on_K1_creates_spurious_observed_difference_exact"]=str(collider)
            result["T_Y_d_separated_after_condition_K"]=d_separated(dag,"T","Y",("K",))
            result["T1_K0_conditioning_has_zero_observed_support"]=True
        if world=="MEDIATOR":
            mediated=mediator_conditioned_diff(raw)
            if mediated!=Z or doeffect!=F(1,2):
                raise AssertionError("conditioning on mediator masks total causal effect")
            result["incorrect_post_treatment_M_adjustment_for_total_effect_exact"]=str(mediated)
            result["T_Y_d_separated_after_condition_M"]=d_separated(dag,"T","Y",("M",))
        worlds.append(result)
        for x,obs,d0,d1,p in raw:
            rows.append({
                "world":world,
                "directed_DAG_edges":"|".join(">".join(e) for e in dag),
                "complete_original_exogenous_source":"|".join(f"{k}:{x[k]}" for k in sorted(x)),
                "original_source_probability_exact":str(p),
                "observed_all_nodes":"|".join(f"{k}:{obs[k]}" for k in sorted(obs)),
                "observed_actual_T":obs["T"],
                "observed_actual_Y":obs["Y"],
                "do_T0_all_nodes":"|".join(f"{k}:{d0[k]}" for k in sorted(d0)),
                "do_T1_all_nodes":"|".join(f"{k}:{d1[k]}" for k in sorted(d1)),
                "do_T0_Y":d0["Y"],
                "do_T1_Y":d1["Y"],
                "individual_source_total_effect_exact":str(F(d1["Y"]-d0["Y"])),
                "exogenous_source_known_to_audit_not_observed_estimator":True,
            })
    if len(rows)!=44 or len(worlds)!=6:
        raise AssertionError("six worlds and 44 exact original source records required")
    d={r["world"]:r for r in worlds}
    if d["CONFOUND"]["observational_TY_2_by_2_distribution"] != \
       d["REVERSE_CAUSAL"]["observational_TY_2_by_2_distribution"]:
        raise AssertionError("required equal observational TY distributions not observed")
    assert d["CONFOUND"]["true_average_causal_effect_exact"]=="0"
    assert d["REVERSE_CAUSAL"]["true_average_causal_effect_exact"]=="1/2"
    assert d["CONFOUND"]["T_Y_d_separated_after_condition_C"] is True
    assert d["COLLIDER"]["T_Y_d_separated_without_conditioning"] is True
    assert d["COLLIDER"]["T_Y_d_separated_after_condition_K"] is False
    assert d["MEDIATOR"]["T_Y_d_separated_after_condition_M"] is True
    return {
        "research_id":"R212",
        "catalogue_id":"09-003",
        "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "complete_artificial_structural_worlds":6,
        "full_original_exogenous_source_records":44,
        "complete_two_interventions_on_each_exogenous_source":88,
        "exogenous_source_probabilities_all_worlds_sum_one":True,
        "same_exogenous_values_held_fixed_under_two_do_interventions":True,
        "true_causal_effect_two_fraction_routes_consistent":True,
        "observationally_equal_TY_marginals_but_different_do_effect_worlds":
            ["CONFOUND","REVERSE_CAUSAL"],
        "equal_TY_marginal_distribution":
            d["CONFOUND"]["observational_TY_2_by_2_distribution"],
        "no_interference_or_hidden_real_population_claim":True,
        "worlds":worlds,
        "new_real_human_E2":0,
        "new_real_historical_E3":0,
        "limits":"Known finite artificial binary SCMs, not any real human or historical causal effect; d-separation audited only on six small fixed graphs.",
    },rows


def emit():
    result,rows=compute()
    paths={
        "results":OUT/"R212_EXACT_RESULTS.json",
        "sources":OUT/"R212_ALL_44_ORIGINAL_SCM_EXOGENOUS_SOURCES.csv",
    }
    paths["results"].write_text(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    with paths["sources"].open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    acceptance={
        "model_id":"R212",
        "actual_original_catalogue_id":"09-003",
        "six_DAG_worlds":6,
        "original_true_exogenous_sources":44,
        "total_pairwise_intervention_outcomes":88,
        "DAG_simple_path_dseparation_and_two_route_do_effect_checked":True,
        "observational_TY_equivalence_different_intervention_verified":True,
        "new_E2":0,
        "new_E3":0,
        **{k+"_sha256":hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()},
    }
    (OUT/"R212_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(acceptance,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(acceptance,indent=2))


class Tests(unittest.TestCase):
    def test_six_scm_worlds(self):
        self.assertEqual(len(WORLDS),6)
    def test_all_dag_acyclic(self):
        self.assertTrue(all(all_nodes_acyclic(EDGES[w]) for w in WORLDS))
    def test_graph_nodes_conf(self):
        self.assertEqual(graph_nodes("CONFOUND"),("C","T","Y"))
    def test_graph_nodes_collider(self):
        self.assertEqual(graph_nodes("COLLIDER"),("K","T","U","Y"))
    def test_known_exogenous_44_sources(self):
        self.assertEqual(sum(len(source_states(w)) for w in WORLDS),44)
    def test_8_sources_conf(self):
        self.assertEqual(len(source_states("CONFOUND")),8)
    def test_4_sources_collider(self):
        self.assertEqual(len(source_states("COLLIDER")),4)
    def test_noise_flip_one_of_four(self):
        s=source_states("REVERSE_CAUSAL")
        self.assertEqual(sum(x["N"]==1 for x in s),2)
    def test_all_source_prob_sum_one(self):
        for w in WORLDS:
            self.assertEqual(sum((x[-1] for x in source_distributions(w)),Z),O)
    def test_do_intervene_T_value(self):
        for w in WORLDS:
            for x in source_states(w):
                self.assertEqual(structural_equations(w,x,0)["T"],0)
                self.assertEqual(structural_equations(w,x,1)["T"],1)
    def test_do_conf_Y_independent(self):
        for x in source_states("CONFOUND"):
            self.assertEqual(structural_equations("CONFOUND",x,0)["Y"],
                             structural_equations("CONFOUND",x,1)["Y"])
    def test_do_direct_effect_one(self):
        a=source_distributions("DIRECT")
        self.assertEqual(interventional_effect(a)[0],O)
    def test_conf_true_do_effect_zero(self):
        self.assertEqual(interventional_effect(source_distributions("CONFOUND"))[0],Z)
    def test_conf_naive_diff_half(self):
        self.assertEqual(naive_diff(source_distributions("CONFOUND")),F(1,2))
    def test_conf_backdoor_corrects(self):
        self.assertEqual(backdoor_adjust_C(source_distributions("CONFOUND")),Z)
    def test_direct_naive_one(self):
        self.assertEqual(naive_diff(source_distributions("DIRECT")),O)
    def test_combined_naive_three_quarters(self):
        self.assertEqual(naive_diff(source_distributions("COMBINED")),F(3,4))
    def test_combined_do_half(self):
        self.assertEqual(interventional_effect(source_distributions("COMBINED"))[0],F(1,2))
    def test_combined_adjust_C_half(self):
        self.assertEqual(backdoor_adjust_C(source_distributions("COMBINED")),F(1,2))
    def test_equal_TY_marginals_conf_reverse(self):
        self.assertEqual(joint_obs(source_distributions("CONFOUND"),("T","Y")),
                         joint_obs(source_distributions("REVERSE_CAUSAL"),("T","Y")))
    def test_distinct_true_do_conf_reverse(self):
        self.assertNotEqual(interventional_effect(source_distributions("CONFOUND"))[0],
                            interventional_effect(source_distributions("REVERSE_CAUSAL"))[0])
    def test_conf_reverse_joint_entries(self):
        dist=joint_obs(source_distributions("CONFOUND"),("T","Y"))
        self.assertEqual(dist,{"00":F(3,8),"01":F(1,8),"10":F(1,8),"11":F(3,8)})
    def test_collider_T_Y_marginal_independent(self):
        self.assertEqual(naive_diff(source_distributions("COLLIDER")),Z)
    def test_collider_selection_spurious_half_negative(self):
        self.assertEqual(collider_selection_diff(source_distributions("COLLIDER")),F(-1,2))
    def test_collider_K0_T1_no_support(self):
        with self.assertRaises(ValueError):
            conditional_obs(source_distributions("COLLIDER"),"Y",1,{"T":1,"K":0})
    def test_mediator_total_effect_half(self):
        self.assertEqual(interventional_effect(source_distributions("MEDIATOR"))[0],F(1,2))
    def test_mediator_condition_M_zero(self):
        self.assertEqual(mediator_conditioned_diff(source_distributions("MEDIATOR")),Z)
    def test_conf_dsep_given_C(self):
        e=EDGES["CONFOUND"]
        self.assertFalse(d_separated(e,"T","Y"))
        self.assertTrue(d_separated(e,"T","Y",("C",)))
    def test_collider_dsep_open_on_K(self):
        e=EDGES["COLLIDER"]
        self.assertTrue(d_separated(e,"T","Y"))
        self.assertFalse(d_separated(e,"T","Y",("K",)))
    def test_mediator_dsep_by_M(self):
        e=EDGES["MEDIATOR"]
        self.assertFalse(d_separated(e,"T","Y"))
        self.assertTrue(d_separated(e,"T","Y",("M",)))
    def test_dsep_descendant_opens_collider(self):
        e=(("T","K"),("U","K"),("U","Y"),("K","S"))
        self.assertTrue(d_separated(e,"T","Y"))
        self.assertFalse(d_separated(e,"T","Y",("S",)))
    def test_direct_edge_remains_open_under_C(self):
        self.assertFalse(d_separated(EDGES["COMBINED"],"T","Y",("C",)))
    def test_cycle_detection(self):
        self.assertFalse(all_nodes_acyclic((("A","B"),("B","C"),("C","A"))))
    def test_invalid_dag_node_rejected(self):
        with self.assertRaises(ValueError):
            d_separated(EDGES["CONFOUND"],"T","Y",("NOTANODE",))
    def test_invalid_world_rejected(self):
        with self.assertRaises(ValueError):
            source_states("UNKNOWN")
    def test_invalid_do_rejected(self):
        with self.assertRaises(ValueError):
            structural_equations("CONFOUND",{"C":0,"N":0},2)
    def test_full_six_world_exact_result(self):
        r,rows=compute()
        self.assertEqual((len(r["worlds"]),len(rows)),(6,44))
        self.assertEqual(r["complete_two_interventions_on_each_exogenous_source"],88)
        self.assertEqual(r["new_real_human_E2"],0)
    def test_full_deterministic_replay(self):
        self.assertEqual(compute(),compute())

if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--test",action="store_true")
    a.add_argument("--emit",action="store_true")
    v=a.parse_args()
    if v.test:
        res=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if res.wasSuccessful() else 1)
    if v.emit:
        emit()
    if not v.test and not v.emit:
        a.print_help()
