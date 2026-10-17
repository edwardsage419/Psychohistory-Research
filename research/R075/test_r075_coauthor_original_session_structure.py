"""R075 source schema and session scope. Synthetic person codes only."""
import unittest
from r075_coauthor_original_session_structure import (
    EXPECTED_HEADERS,audit_source_text,ORIGINAL_SHA256,original_text_from_verified_zip
)

def fixture(people=(1,2), sessions=(1,2), rounds=(1,2,3)):
    lines=["\t".join(EXPECTED_HEADERS)]
    for sess in sessions:
        for person in people:
            for rnd in rounds:
                row={f:"0" for f in EXPECTED_HEADERS}
                row.update({"file":str(sess),"bc":"2","error":"0","subject":str(sess*100+person),
                            "interaction":"1","group":"1","period":str(rnd),
                            "decision":"1" if rnd%2 else "2",
                            "you_p_1":"0" if rnd==1 else "1",
                            "other_p_1":"0" if rnd==1 else "2"})
                lines.append("\t".join(row[f] for f in EXPECTED_HEADERS))
    return ("\n".join(lines)+"\n").encode()

class TestOriginalSessionSource(unittest.TestCase):
    def test_01_schema_24_fields(self):
        self.assertEqual(len(EXPECTED_HEADERS),24)
    def test_02_source_pin_sha64(self):
        self.assertEqual(len(ORIGINAL_SHA256),64)
    def test_03_two_sessions(self):
        s=audit_source_text(fixture(),False)
        self.assertEqual(s["distinct_original_file_session_ids"],2)
        self.assertEqual(s["text_rows"],12)
        self.assertEqual(s["person_session_slots"],4)
    def test_04_treatment_isolation(self):
        s=audit_source_text(fixture(),False)
        self.assertEqual(s["treatment_count"],1)
        self.assertEqual(s["treatments"][0]["sessions"],2)
    def test_05_pair_counting(self):
        s=audit_source_text(fixture(),False)
        self.assertEqual(s["pair_group_round_count_distribution"],{2:6})
    def test_06_no_individual_records(self):
        s=audit_source_text(fixture(),False)
        self.assertFalse(s["individual_human_records_exported"])
        self.assertNotIn("source_rows",s)
    def test_07_no_unauthorized_fit(self):
        self.assertFalse(audit_source_text(fixture(),False)["model_score_run"])
    def test_08_duplicate_detected(self):
        b=fixture().decode().splitlines()
        b.append(b[1])
        s=audit_source_text(("\n".join(b)+"\n").encode(),False)
        self.assertEqual(s["subject_interaction_round_duplicate_records"],1)
    def test_09_missing_key_blocked(self):
        b=fixture().decode().splitlines()
        b[1]=b[1].replace("\t1\t1\t1\t1\t", "\t1\t1\t\t1\t",1)
        # A fixture with missing any required field cannot pass.
        if b[1]==fixture().decode().splitlines()[1]:
            cells=b[1].split("\t");cells[0]="";b[1]="\t".join(cells)
        with self.assertRaises(ValueError):
            audit_source_text(("\n".join(b)+"\n").encode(),False)
    def test_10_invalid_round_blocked(self):
        b=fixture().decode().splitlines()
        cells=b[1].split("\t");cells[6]="round-one";b[1]="\t".join(cells)
        with self.assertRaisesRegex(ValueError,"TEXT_ROUND_MALFORMED"):
            audit_source_text(("\n".join(b)+"\n").encode(),False)
    def test_11_no_unpinned_zip_allowed(self):
        with self.assertRaisesRegex(ValueError,"SHA"):
            original_text_from_verified_zip(b"fabricated")
    def test_12_bad_dictionary_rejected(self):
        b=fixture().replace(b"file\tbc\terror",b"wrong\tbc\terror",1)
        with self.assertRaisesRegex(ValueError,"DICTIONARY_CHANGED"):
            audit_source_text(b,False)
if __name__=="__main__":unittest.main()
