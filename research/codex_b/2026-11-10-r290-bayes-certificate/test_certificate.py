import csv
from fractions import Fraction as F
import io
import json
from pathlib import Path
import tempfile
import unittest
from certificate import loss_certificate,trained_mask,derive
from audit import audit

ROOT=Path(__file__).resolve().parents[3]
CSV_PATH=ROOT/"research/validation/R290_S86_ALL_1950_TRAINING_SOURCES.csv"
JSON_PATH=ROOT/"research/validation/R290_S86_EXACT_RESULTS.json"


def bad_cases():
    for name in ("false_optimality","zero_oracle","cutoff_corruption","baseline_corruption","missing_baselines","risk_zero","regret_negative","source_mass"):
        doc=json.loads(JSON_PATH.read_bytes());row=doc["results"][0];data=CSV_PATH.read_text()
        if name=="false_optimality":row["oracle_risk"]=row["expected_heldout_risk"];row["regret"]="0"
        elif name=="zero_oracle":row["oracle_risk"]="0";row["regret"]=row["expected_heldout_risk"]
        elif name=="cutoff_corruption":row["best_fixed_cutoff_risk"]="999";row["best_fixed_cutoff_t"]=99
        elif name=="baseline_corruption":row["fixed_t3_risk"]="999";row["best_constant_risk"]="999"
        elif name=="missing_baselines":
            for key in ("best_fixed_cutoff_risk","best_fixed_cutoff_t","fixed_t3_risk","best_constant_risk"):del row[key]
        elif name=="risk_zero":row["expected_heldout_risk"]="0"
        elif name=="regret_negative":row["regret"]="-1"
        else:
            rows=list(csv.reader(io.StringIO(data)));rows[1][4]="0";stream=io.StringIO();csv.writer(stream,lineterminator="\n").writerows(rows);data=stream.getvalue()
        yield name,data.encode(),(json.dumps(doc,indent=2)+"\n").encode()


class CertificateTests(unittest.TestCase):
    def test_first_world_minimum_and_witnesses(self):
        c=loss_certificate("MONOTONE",F(1,2),1,1)
        self.assertEqual(c["denominator"],42);self.assertEqual(c["minimum_numerator"],10)
        self.assertEqual(c["minimizing_masks"],[24,28]);self.assertEqual(c["best_cutoff_t"],2)
        self.assertEqual(len(c["loss_numerators"]),32)
    def test_identical_equiprobable_all_rules_optimal(self):
        c=loss_certificate("IDENTICAL",F(1,2),1,1)
        self.assertEqual(c["minimizing_masks"],list(range(32)))
        self.assertTrue(all(F(v,c["denominator"])==F(1,2) for v in c["loss_numerators"]))
        self.assertEqual(c["best_cutoff_t"],0)
    def test_cutoffs_and_constants_are_specific_masks(self):
        c=loss_certificate("CENTERED",F(1,2),1,1)
        self.assertEqual(c["cutoff_masks"],[31,30,28,24,16,0])
        self.assertEqual(c["cutoff_numerators"],[c["loss_numerators"][m] for m in c["cutoff_masks"]])
        self.assertEqual(c["best_constant_numerator"],min(c["loss_numerators"][0],c["loss_numerators"][31]))
    def test_training_ties_and_frozen_costs(self):
        self.assertEqual(trained_mask("0","0",F(1,2),1,1),0)
        self.assertEqual(trained_mask("0","4",F(1,2),1,1),16)
        self.assertEqual(trained_mask("00","44",F(3,4),1,3),31)
    def test_histograms_and_gap_identity(self):
        d=derive(CSV_PATH.read_bytes());self.assertEqual(len(d["rule_histograms"]),24)
        for h in d["rule_histograms"].values():
            self.assertEqual(len(h["weights"]),32);self.assertEqual(sum(h["weights"]),h["denominator"])
        for row in d["expected"]["results"]:
            self.assertEqual(F(row["expected_heldout_risk"])-F(row["oracle_risk"]),F(row["regret"]))
            self.assertGreaterEqual(F(row["regret"]),0)
    def test_true_regret_and_nonmonotone_anchor(self):
        rows=derive(CSV_PATH.read_bytes())["expected"]["results"];lookup={(r["world"],r["m"]):r for r in rows}
        a=lookup[("MONOTONE_PI1of2_FP1_FN1",1)]
        self.assertEqual((a["expected_heldout_risk"],a["oracle_risk"],a["regret"]),("188/441","5/21","83/441"))
        self.assertEqual(lookup[("IDENTICAL_PI1of2_FP1_FN3",2)]["expected_heldout_risk"],"20939/39366")
        self.assertEqual(lookup[("IDENTICAL_PI1of2_FP1_FN1",2)]["regret"],"0")
    def test_unfrozen_and_bool_parameters(self):
        for args in (("UNKNOWN",F(1,2),1,1),("MONOTONE",F(1,4),1,1),("MONOTONE",F(1,2),True,1),("MONOTONE",F(1,2),1,2)):
            with self.assertRaises(ValueError):loss_certificate(*args)
        for a,b in (("","0"),("5","0"),("0","00")):
            with self.assertRaises(ValueError):trained_mask(a,b,F(1,2),1,1)


class AuditTests(unittest.TestCase):
    def case(self,data=None,doc=None):
        with tempfile.TemporaryDirectory() as temporary:
            a,b=Path(temporary)/"source.csv",Path(temporary)/"result.json"
            a.write_bytes(data if data is not None else CSV_PATH.read_bytes());b.write_bytes(doc if doc is not None else JSON_PATH.read_bytes())
            return audit(a,b)
    def test_complete_archive(self):
        r=audit(CSV_PATH,JSON_PATH)
        self.assertEqual(r["status"],"PASS_COMPLETE_BAYES_AND_RULE_LAW_CERTIFICATE")
        self.assertEqual((r["result_leaf_checks"],r["scientific_fraction_fields"],r["source_rows"]),(273,144,1950))
    def test_bad_cases_rejected(self):
        for name,data,doc in bad_cases():
            with self.subTest(name=name),self.assertRaises(ValueError):self.case(data,doc)
    def test_all_baseline_fields_are_checked(self):
        original=json.loads(JSON_PATH.read_bytes())
        for i,row in enumerate(original["results"]):
            for field in ("oracle_risk","regret","best_fixed_cutoff_risk","best_fixed_cutoff_t","fixed_t3_risk","best_constant_risk"):
                obj=json.loads(JSON_PATH.read_bytes());obj["results"][i][field]=999 if type(row[field]) is int else "999"
                with self.subTest(i=i,field=field),self.assertRaises(ValueError):self.case(doc=json.dumps(obj).encode())
    def test_strict_worlds_and_types(self):
        for field in ("m","new_E2","world"):
            obj=json.loads(JSON_PATH.read_bytes())
            if field=="new_E2":obj[field]=False
            elif field=="m":obj["results"][0][field]=True
            else:obj["results"][0][field]="MONOTONE_PI1of4_FP1_FN1"
            with self.assertRaises(ValueError):self.case(doc=json.dumps(obj).encode())
    def test_duplicate_json_key(self):
        raw=JSON_PATH.read_text().rstrip();raw=raw[:-1]+',"new_E2":0}'
        with self.assertRaisesRegex(ValueError,"DUPLICATE_JSON_KEY"):self.case(doc=raw.encode())


if __name__=="__main__":unittest.main()
