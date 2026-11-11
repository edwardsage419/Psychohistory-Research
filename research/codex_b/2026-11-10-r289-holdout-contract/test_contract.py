from collections import defaultdict
from fractions import Fraction as F
import csv
import io
import itertools
import json
from pathlib import Path
import tempfile
import unittest
from stopping import NAMES,joint_law,world,expected_tree,reward2
from audit import audit

ROOT=Path(__file__).resolve().parents[3]
CSV_PATH=ROOT/"research/validation/R289_S85_ALL_243_PAIRED_OFFERS.csv"
JSON_PATH=ROOT/"research/validation/R289_S85_EXACT_RESULTS.json"


class StoppingTests(unittest.TestCase):
    def test_hand_rewards(self):
        self.assertEqual(reward2("1111",3),-1)
        self.assertEqual(reward2("1351",3),5)
        self.assertEqual(reward2("1351",5),8)
    def test_law_mass_and_support(self):
        for name in NAMES:
            law=joint_law(name);self.assertEqual(sum(law.values(),F(0)),1)
            self.assertTrue(all(type(x) is F and x>0 for x in law.values()))
    def test_joint_law_against_independent_enumeration(self):
        weights=((1,1,1),(2,1,1),(1,1,2))
        for name,w in zip(NAMES,weights):
            expected=defaultdict(F)
            for offers in itertools.product((1,3,5),repeat=4):
                p=F(1);nets=[]
                for x in offers:p*=F(w[(x-1)//2],sum(w))
                for h in (3,5):
                    for i,x in enumerate(offers):
                        if x>=h or i==3:nets.append(2*x-i);break
                expected[tuple(nets)]+=p
            self.assertEqual(joint_law(name),dict(expected))
    def test_fresh_reward_hand(self):
        w=world("UNIFORM",1)
        self.assertEqual(w["probability_select_H5"],"25/81")
        self.assertEqual(w["independent_test_expected_net"],"8128/2187")
        clairvoyant=sum((p*F(max(pair),2) for pair,p in joint_law("UNIFORM").items()),F(0))
        self.assertEqual(clairvoyant,F(331,81))
        self.assertLess(F(w["independent_test_expected_net"]),F(67,18))
        self.assertGreater(clairvoyant,F(67,18))
    def test_all_means_and_fixed_oracle_bound(self):
        expected=(("67/18","100/27"),("27/8","197/64"),("133/32","35/8"))
        for name,means in zip(NAMES,expected):
            for m in (1,2):
                w=world(name,m);self.assertEqual((w["expected_H3"],w["expected_H5"]),means)
                self.assertGreater(F(w["regret_vs_best_fixed_threshold"]),0)
                self.assertGreater(F(w["gain_over_first_only"]),0)
    def test_ties_and_two_episode_anchor(self):
        w=world("UNIFORM",1);self.assertEqual(w["probability_training_tie"],"14/27")
        self.assertEqual(F(w["probability_select_H5"])+F(w["probability_training_tie"]),F(67,81))
        self.assertEqual(world("UNIFORM",2)["probability_select_H5"],"2819/6561")
    def test_unfrozen_input_rejected(self):
        for args in (("UNKNOWN",1),("UNIFORM",True),("UNIFORM",0),("UNIFORM",3)):
            with self.assertRaises(ValueError):world(*args)
        for source,h in (("111",3),("1112",3),("1111",4),("1111",True)):
            with self.assertRaises(ValueError):reward2(source,h)


class AuditTests(unittest.TestCase):
    def run_case(self,doc=None,text=None):
        with tempfile.TemporaryDirectory() as d:
            a,j=Path(d)/"sources.csv",Path(d)/"result.json"
            a.write_text(text if text is not None else CSV_PATH.read_text())
            j.write_text(json.dumps(doc) if doc is not None else JSON_PATH.read_text())
            return audit(a,j)
    def test_archive_and_complete_tree(self):
        result=audit(CSV_PATH,JSON_PATH)
        self.assertEqual(result["status"],"PASS_INDEPENDENT_STOPPING_HOLDOUT_CONTRACT")
        self.assertEqual(result["result_leaf_checks"],136)
        self.assertEqual(result["source_rows"],243)
    def test_hindsight_evaluation_rejected(self):
        doc=json.loads(JSON_PATH.read_text());doc["worlds"][0]["independent_test_expected_net"]="331/81"
        doc["worlds"][0]["regret_vs_best_fixed_threshold"]="-59/162"
        with self.assertRaises(ValueError):self.run_case(doc=doc)
    def test_tie_policy_and_historical_flags(self):
        for field in ("probability_select_H5","mutation_tests","new_E2"):
            with self.subTest(field=field):
                doc=json.loads(JSON_PATH.read_text())
                if field=="probability_select_H5":doc["worlds"][0][field]="67/81"
                elif field=="mutation_tests":doc[field][-1]["rejected"]=1
                else:doc[field]=False
                with self.assertRaises(ValueError):self.run_case(doc=doc)
    def test_ledger_missing_duplicate_mass_payoff(self):
        rows=list(csv.reader(io.StringIO(CSV_PATH.read_text())))
        variants=[rows[:-1],[*rows[:-1],rows[1]]]
        for column in (2,4):
            altered=[r[:] for r in rows];altered[1][column]="999";variants.append(altered)
        for changed in variants:
            stream=io.StringIO();csv.writer(stream,lineterminator="\n").writerows(changed)
            with self.assertRaises(ValueError):self.run_case(text=stream.getvalue())
    def test_all_world_fraction_fields_checked(self):
        original=json.loads(JSON_PATH.read_text())
        for i,row in enumerate(original["worlds"]):
            for key,value in row.items():
                if key in ("distribution","training_episodes","training_source_tuples","evidence"):continue
                doc=json.loads(JSON_PATH.read_text());doc["worlds"][i][key]="999"
                with self.subTest(i=i,key=key),self.assertRaises(ValueError):self.run_case(doc=doc)


if __name__=="__main__":unittest.main()
