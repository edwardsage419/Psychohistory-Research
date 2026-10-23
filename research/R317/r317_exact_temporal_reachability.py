#!/usr/bin/env python3
"""R317: exact strictly time respecting paths in a complete 3-contact micro-universe."""
from __future__ import annotations
import argparse
import csv
import json
import unittest
from pathlib import Path

DIR=Path(__file__).resolve().parent
SOURCE=DIR/"R317_ALL_81_ORIGINAL_TEMPORAL_CONTACT_SOURCE_ROWS.csv"
RESULT=DIR/"R317_ALL_81_ORIGIN_TEMPORAL_REACHABILITY_OUTCOMES.json"
CONTACTS=((0,1),(0,2),(1,2))
FIELDS=("schedule_id","schedule_code","time","contact_index","node_u","node_v")

def digits(schedule_id):
    assert 0<=schedule_id<27
    return (schedule_id//9,(schedule_id//3)%3,schedule_id%3)

def temporal_arrival(order,origin):
    a=[None,None,None]
    a[origin]=0
    for t,index in enumerate(order,1):
        u,v=CONTACTS[index]
        # Evaluate both directions against the same pre-event state.
        pre_u=a[u] is not None and a[u]<t
        pre_v=a[v] is not None and a[v]<t
        if pre_u and a[v] is None:a[v]=t
        if pre_v and a[u] is None:a[u]=t
    return a

def static_reachable(order,origin):
    links=[set() for _ in range(3)]
    for index in order:
        u,v=CONTACTS[index]
        links[u].add(v)
        links[v].add(u)
    seen={origin}
    queue=[origin]
    for node in queue:
        for nb in sorted(links[node]):
            if nb not in seen:
                seen.add(nb);queue.append(nb)
    return sorted(seen)

def generate():
    sources=[];outcomes=[];missed=0
    for schedule_id in range(27):
        order=digits(schedule_id)
        code="".join(map(str,order))
        for t,index in enumerate(order,1):
            u,v=CONTACTS[index]
            sources.append(dict(zip(FIELDS,map(str,(schedule_id,code,t,index,u,v)))))
        for origin in range(3):
            arr=temporal_arrival(order,origin)
            temp=[i for i,x in enumerate(arr) if x is not None]
            static=static_reachable(order,origin)
            assert set(temp).issubset(static)
            deficits=sorted(set(static)-set(temp))
            assert origin not in deficits
            missed+=len(deficits)
            outcomes.append({
                "schedule_id":schedule_id,"schedule_code":code,"origin":origin,
                "earliest_arrival":arr,"temporal_reachable":temp,
                "static_reachable":static,
                "static_overstatement_targets":deficits
            })
    return sources,{
        "schema":"r317_temporal_network_3_events_strict_time_paths_exact_e1",
        "catalogue_id":"04-022","grade":"FINITE_ARTIFICIAL_E1_ONLY",
        "source_rows":len(sources),"schedule_count":27,"origin_evaluations":len(outcomes),
        "ordered_static_overstatement_pairs":missed,
        "outcomes":outcomes
    }

def replay():
    with SOURCE.open(newline="",encoding="utf-8") as f:
        prev=list(csv.DictReader(f))
    src,result=generate()
    assert prev==src and len(src)==81
    assert json.loads(RESULT.read_text(encoding="utf-8"))==result
    assert len(result["outcomes"])==81

class TemporalTests(unittest.TestCase):
    def test_three_contacts(self):self.assertEqual(len(CONTACTS),3)
    def test_contact_nonloops(self):self.assertTrue(all(a<b for a,b in CONTACTS))
    def test_first_digits(self):self.assertEqual(digits(0),(0,0,0))
    def test_last_digits(self):self.assertEqual(digits(26),(2,2,2))
    def test_witness_digits(self):self.assertEqual(digits(18),(2,0,0))
    def test_codes_unique(self):self.assertEqual(len({digits(i) for i in range(27)}),27)
    def test_schedule_count(self):self.assertEqual(generate()[1]["schedule_count"],27)
    def test_source_count(self):self.assertEqual(generate()[1]["source_rows"],81)
    def test_origin_results(self):self.assertEqual(generate()[1]["origin_evaluations"],81)
    def test_origin_self_t0(self):
        for s in range(27):
            for o in range(3):self.assertEqual(temporal_arrival(digits(s),o)[o],0)
    def test_arrivals_within_time_window(self):
        for s in range(27):
            for o in range(3):
                self.assertTrue(all(t is None or t in (0,1,2,3) for t in temporal_arrival(digits(s),o)))
    def test_no_origin_other_when_unrelated(self):
        self.assertEqual(temporal_arrival((0,0,0),2),[None,None,0])
    def test_01_only_origin0(self):
        self.assertEqual(temporal_arrival((0,0,0),0),[0,1,None])
    def test_01_only_origin1(self):
        self.assertEqual(temporal_arrival((0,0,0),1),[1,0,None])
    def test_12_only_origin0(self):
        self.assertEqual(temporal_arrival((2,2,2),0),[0,None,None])
    def test_12_only_origin2(self):
        self.assertEqual(temporal_arrival((2,2,2),2),[None,1,0])
    def test_witness_origin0(self):
        self.assertEqual(temporal_arrival((2,0,0),0),[0,2,None])
    def test_witness_origin2(self):
        self.assertEqual(temporal_arrival((2,0,0),2),[2,1,0])
    def test_witness_static_origin0(self):
        self.assertEqual(static_reachable((2,0,0),0),[0,1,2])
    def test_witness_static_origin2(self):
        self.assertEqual(static_reachable((2,0,0),2),[0,1,2])
    def test_forward_order_origin0(self):
        self.assertEqual(temporal_arrival((0,2,0),0),[0,1,2])
    def test_reverse_order_origin0(self):
        self.assertEqual(temporal_arrival((2,0,0),0)[2],None)
    def test_forward_order_origin2(self):
        self.assertEqual(temporal_arrival((2,0,0),2)[0],2)
    def test_origin_static_self(self):
        for s in range(27):
            for o in range(3):self.assertIn(o,static_reachable(digits(s),o))
    def test_static_superset(self):
        for s in range(27):
            for o in range(3):
                a=temporal_arrival(digits(s),o)
                self.assertTrue({i for i,x in enumerate(a) if x is not None}.issubset(static_reachable(digits(s),o)))
    def test_all_time_increasing(self):
        for s in range(27):
            for o in range(3):
                a=temporal_arrival(digits(s),o)
                self.assertTrue(all(t is None or t>=0 for t in a))
    def test_all_27_present(self):
        x,_=generate()
        self.assertEqual(sorted(set(int(z["schedule_id"]) for z in x)),list(range(27)))
    def test_three_records_per_schedule(self):
        x,_=generate()
        for s in range(27):
            self.assertEqual(sum(int(r["schedule_id"])==s for r in x),3)
    def test_all_three_origins_per_schedule(self):
        _,out=generate()
        for s in range(27):
            self.assertEqual(sorted(z["origin"] for z in out["outcomes"] if z["schedule_id"]==s),[0,1,2])
    def test_any_static_overstatement_exists(self):
        self.assertGreater(generate()[1]["ordered_static_overstatement_pairs"],0)
    def test_no_negative_overstatement(self):
        self.assertLessEqual(generate()[1]["ordered_static_overstatement_pairs"],27*3*2)
    def test_archive(self):replay()

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--test",action="store_true");p.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:
        tests=unittest.defaultTestLoader.loadTestsFromTestCase(TemporalTests)
        result=unittest.TextTestRunner(verbosity=1).run(tests)
        if not result.wasSuccessful():raise SystemExit(1)
    elif args.audit:
        replay()
        print("PASS R317: all 81 original time-event rows and 81 origin reachability outcomes")
    else:
        print(json.dumps(generate()[1],indent=2))
