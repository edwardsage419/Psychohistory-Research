import csv
from fractions import Fraction as F
import io
import itertools
import json
from pathlib import Path
import tempfile
import unittest
from moments import STAYS,QUALITIES,probability,prediction,expected
from audit import audit

ROOT=Path(__file__).resolve().parents[3]
CSV_PATH=ROOT/"research/validation/R300_S96_ALL_288_MISSPECIFIED_HMM_PREFIX_SOURCES.csv"
JSON_PATH=ROOT/"research/validation/R300_S96_EXACT_MISSPECIFICATION_BRIER_RESULTS.json"


def bad_cases():
    for name in ("one_group_duplicate","all_groups_identical","antipersistent_true_label","R073_changed","duplicate_JSON_key","missing_group","source_mass","group_risk"):
        doc=json.loads(JSON_PATH.read_bytes());data=CSV_PATH.read_text()
        if name=="one_group_duplicate":doc["results"][1]=dict(doc["results"][0])
        elif name=="all_groups_identical":doc["results"]=[dict(doc["results"][0]) for _ in range(18)]
        elif name=="antipersistent_true_label":
            for row in doc["results"]:
                if row["true_stay"]=="3/4":row["true_stay"]="1/4"
        elif name=="R073_changed":doc["R073"]="MODIFIED"
        elif name=="missing_group":doc["results"].pop()
        elif name=="source_mass":
            rows=list(csv.reader(io.StringIO(data)));rows[1][6]="0";stream=io.StringIO();csv.writer(stream,lineterminator="\n").writerows(rows);data=stream.getvalue()
        elif name=="group_risk":doc["results"][0]["expected_brier"]="0"
        raw=json.dumps(doc,indent=2)+"\n"
        if name=="duplicate_JSON_key":raw=raw.rstrip()[:-1]+',"group_count":18}\n'
        yield name,data.encode(),raw.encode()


def paths(n):return [''.join(bits) for bits in itertools.product('01',repeat=n)]


class MomentTests(unittest.TestCase):
    def test_hand_anchors(self):
        self.assertEqual(probability(F(3,4),F(3,4),'11'),F(9,32))
        self.assertEqual(prediction(F(3,4),F(3,4),'0000'),(F(99,1024),F(9,22)))
    def test_uninformative_profiles(self):
        for a,q in ((a,F(1,2)) for a in STAYS):
            for bits in paths(4):self.assertEqual(prediction(a,q,bits),(F(1,16),F(1,2)))
        for q in QUALITIES:
            for bits in paths(4):self.assertEqual(prediction(F(1,2),q,bits),(F(1,16),F(1,2)))
    def test_normalization_and_partition(self):
        for a in STAYS:
            for q in QUALITIES:
                for n in (0,1,4,5):self.assertEqual(sum((probability(a,q,s) for s in paths(n)),F(0)),1)
                for s in paths(4):self.assertEqual(probability(a,q,s+'0')+probability(a,q,s+'1'),probability(a,q,s))
    def test_global_complement_symmetry(self):
        for a in STAYS:
            for q in QUALITIES:
                for s in paths(4):
                    rev=''.join('1' if x=='0' else '0' for x in s)
                    self.assertEqual(prediction(a,q,s)[0],prediction(a,q,rev)[0])
                    self.assertEqual(prediction(a,q,s)[1]+prediction(a,q,rev)[1],1)
    def test_against_independent_latent_path_sum(self):
        def joint(a,q,s):
            total=F(0)
            for hidden in paths(len(s)):
                mass=F(1,2)
                for i,bit in enumerate(hidden):
                    if i:mass*=a if bit==hidden[i-1] else 1-a
                    mass*=q if bit==s[i] else 1-q
                total+=mass
            return total
        for a in STAYS:
            for q in QUALITIES:
                for s in paths(4):
                    self.assertEqual(probability(a,q,s),joint(a,q,s))
                    self.assertEqual(probability(a,q,s+'1'),joint(a,q,s+'1'))
    def test_risk_anchors_and_proper_score(self):
        rows=expected()["document"]["results"];lookup={(r['true_stay'],r['candidate_stay'],r['candidate_emission']):r for r in rows}
        self.assertEqual(lookup['3/4','1/4','1']['expected_brier'],'11/32')
        self.assertEqual(lookup['3/4','3/4','3/4']['oracle_brier'],'105579273/430168816')
        for row in rows:
            self.assertEqual(F(row['expected_brier'])-F(row['oracle_brier']),F(row['excess_brier']))
            self.assertGreaterEqual(F(row['excess_brier']),0)
    def test_invalid_inputs(self):
        for a,q,s in ((F(0),F(3,4),'0000'),(F(1,2),True,'0000'),(F(1,2),F(3,4),'x'),(F(1,2),F(3,4),'000000')):
            with self.assertRaises(ValueError):probability(a,q,s)


class AuditTests(unittest.TestCase):
    def case(self,data=None,raw=None):
        with tempfile.TemporaryDirectory() as temporary:
            a,j=Path(temporary)/'source.csv',Path(temporary)/'result.json'
            a.write_bytes(CSV_PATH.read_bytes() if data is None else data);j.write_bytes(JSON_PATH.read_bytes() if raw is None else raw)
            return audit(a,j)
    def test_archive_complete(self):
        r=audit(CSV_PATH,JSON_PATH)
        self.assertEqual(r['status'],'PASS_WALSH_HMM_COMPLETE_GROUP_CONTRACT')
        self.assertEqual((r['source_rows'],r['source_fraction_checks'],r['unique_model_groups'],r['result_leaf_checks']),(288,2016,18,176))
    def test_bad_cases_rejected(self):
        for name,data,raw in bad_cases():
            with self.subTest(name=name),self.assertRaises(ValueError):self.case(data,raw)
    def test_independent_record_permutations(self):
        table=list(csv.reader(io.StringIO(CSV_PATH.read_text())));stream=io.StringIO();csv.writer(stream,lineterminator='\n').writerows([table[0],*reversed(table[1:])])
        self.assertEqual(self.case(data=stream.getvalue().encode())['unique_model_groups'],18)
        doc=json.loads(JSON_PATH.read_bytes());doc['results'].reverse()
        self.assertEqual(self.case(raw=json.dumps(doc).encode())['unique_model_groups'],18)
    def test_all_group_risk_fields_checked(self):
        for i in range(18):
            for field in ('expected_brier','oracle_brier','excess_brier','fixed_half_brier'):
                doc=json.loads(JSON_PATH.read_bytes());doc['results'][i][field]='999'
                with self.subTest(i=i,field=field),self.assertRaises(ValueError):self.case(raw=json.dumps(doc).encode())
    def test_duplicate_json_key(self):
        _,data,raw=next(c for c in bad_cases() if c[0]=='duplicate_JSON_key')
        with self.assertRaisesRegex(ValueError,'DUPLICATE_JSON_KEY'):self.case(data,raw)


if __name__=='__main__':unittest.main()
