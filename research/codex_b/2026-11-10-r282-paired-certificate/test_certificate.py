import copy
import csv
import io
import itertools
import json
from pathlib import Path
import tempfile
import unittest

from algebra import SCHEDULES, rank, linear_states, evaluate, certificates, paired_counts
from audit import audit

ROOT = Path(__file__).resolve().parents[3]
CSV_PATH = ROOT/"research/validation/R282_S78_ALL_192_SOURCE_OBSERVATIONS.csv"
JSON_PATH = ROOT/"research/validation/R282_S78_EXACT_RESULTS.json"


def bad_cases():
    original = json.loads(JSON_PATH.read_bytes()); csv_text = CSV_PATH.read_text()
    for name in ("paired_zero", "paired_missing", "paired_999", "paired_bool", "paired_stages",
                 "paired_schedule_missing", "schedule_reversed", "duplicate_paired_key", "CSV_transition", "TV_corruption"):
        doc = copy.deepcopy(original); data = csv_text
        if name == "paired_zero": doc["original_R282_paired_counts"] = {s: [0,0] for s in SCHEDULES[1:]}
        elif name == "paired_missing": del doc["original_R282_paired_counts"]
        elif name == "paired_999": doc["original_R282_paired_counts"]["A_THEN_B"][0] = 999
        elif name == "paired_bool": doc["original_R282_paired_counts"]["A_THEN_B"][0] = False
        elif name == "paired_stages": doc["original_R282_paired_counts"] = {s: [48,32] for s in SCHEDULES[1:]}
        elif name == "paired_schedule_missing": del doc["original_R282_paired_counts"]["A_THEN_B"]
        elif name == "schedule_reversed": doc["schedules"].reverse()
        elif name == "CSV_transition":
            rows = list(csv.reader(io.StringIO(data))); rows[1][4] = "11"
            stream = io.StringIO(newline="");csv.writer(stream,lineterminator="\n").writerows(rows);data=stream.getvalue()
        elif name == "TV_corruption": doc["regimes"][0]["tv"][0]["distance"] = "1"
        raw = json.dumps(doc, indent=2)+"\n"
        if name == "duplicate_paired_key": raw = raw.rstrip()[:-1]+',"original_R282_paired_counts":{"A_THEN_B":[0,0],"B_THEN_A":[0,0]}}\n'
        yield name, data.encode(), raw.encode()


def write_case(folder, data, raw):
    a,b=folder/"sources.csv",folder/"receipt.json";a.write_bytes(data);b.write_bytes(raw);return a,b


class AlgebraTests(unittest.TestCase):
    def test_rank_hand(self):
        for rows, expected in (([],0),([0,0],0),([7,7],1),([7,24],2),([1,2,4,8,16,32],6)):
            self.assertEqual(rank(rows),expected)
    def test_rank_row_operations(self):
        self.assertEqual(rank([1,2,3]),rank([3,2,1,0,3]))
        self.assertEqual(rank([7,24]),rank([31,24]))
        self.assertEqual(rank([7,24]),2)
    def test_hand_transforms(self):
        expected={"SYNC":((1,2),(6,9),(25,38)),"A_THEN_B":((1,2),(6,14),(30,62)),"B_THEN_A":((1,2),(13,9),(61,45))}
        for s in SCHEDULES:self.assertEqual(linear_states(s),expected[s])
    def test_named_source_witness(self):
        for s, expected in (("SYNC",("10","01","10")),("A_THEN_B",("10","00","00")),("B_THEN_A",("10","11","11"))):
            self.assertEqual(tuple(''.join(str(evaluate(mask,"100000")) for mask in state) for state in linear_states(s)),expected)
    def test_exact_count_formula(self):
        self.assertEqual(paired_counts(),{s:[32,48] for s in SCHEDULES[1:]})
        self.assertEqual([c["rank"] for c in certificates()],[1,2,1,2])
        self.assertTrue(all(c["equal_count"]+c["disagreement_count"]==64 for c in certificates()))
    def test_rank_against_exhaustive_kernel(self):
        for rows in ([0,0],[7,7],[7,24],[36,11],[1,2,4,8,16,32]):
            zero=sum(all((row & value).bit_count()%2==0 for row in rows) for value in range(64))
            self.assertEqual(zero,64>>rank(rows))
    def test_invalid_inputs(self):
        for value in ([True],[-1],[64],[1.0],"1"):
            with self.subTest(value=value),self.assertRaises(ValueError):rank(value)
        with self.assertRaises(ValueError):linear_states("UNKNOWN")
        for mask,bits in ((False,"000000"),(64,"000000"),(0,"00000x"),(0,"00000")):
            with self.assertRaises(ValueError):evaluate(mask,bits)


class AuditTests(unittest.TestCase):
    def test_archive(self):
        result=audit(CSV_PATH,JSON_PATH)
        self.assertEqual(result["status"],"PASS_PAIRED_GF2_SUPPLEMENT")
        self.assertEqual(result["source_rows"],192)
        self.assertEqual(result["symbolic_output_bit_checks"],768)
        self.assertEqual(result["paired_integer_fields"],4)
    def test_paired_bad_controls(self):
        for name,data,raw in bad_cases():
            if name.startswith("paired_"):
                with self.subTest(name=name),tempfile.TemporaryDirectory() as d:
                    with self.assertRaises(ValueError):audit(*write_case(Path(d),data,raw))
    def test_schedule_declaration(self):
        _,data,raw=next(c for c in bad_cases() if c[0]=="schedule_reversed")
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):audit(*write_case(Path(d),data,raw))
    def test_duplicate_paired_key(self):
        _,data,raw=next(c for c in bad_cases() if c[0]=="duplicate_paired_key")
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,"DUPLICATE_JSON_KEY"):audit(*write_case(Path(d),data,raw))
    def test_source_and_summary_controls(self):
        for name,data,raw in bad_cases():
            if name in ("CSV_transition","TV_corruption"):
                with self.subTest(name=name),tempfile.TemporaryDirectory() as d:
                    with self.assertRaises(ValueError):audit(*write_case(Path(d),data,raw))


if __name__=="__main__":unittest.main()
