"""R103 B4 source ID syntax class synthetic tests without real person IDs."""
import csv
import hashlib
import io
import unittest
from unittest.mock import patch
import r103_phase_a_2016_drbrain_original_md5_header_only as a
import r103_phase_b4_original_ID_field_syntax_class_only as b

def fixture():
    o=io.StringIO(newline="")
    writer=csv.DictWriter(o,fieldnames=a.MANDATORY_FIELDS,lineterminator="\n")
    writer.writeheader()
    for opponent in ("10","0","-1","1.0","","NA","ABC123","β"):
        writer.writerow({"User_ID":"1","Experiment_number":"5",
            "Round_number":"1","S":"2","T":"4","Game":"PD",
            "Action":"PRIVATE_C","Opponent_ID":opponent,"Opponent_Action":"PRIVATE_D"})
    return o.getvalue().encode()

def audited(raw):
    with patch.object(a,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()), \
         patch.object(b,"PINNED_SHA",hashlib.sha256(raw).hexdigest()), \
         patch.object(b,"PINNED_N",raw.count(b"\n")-1):
        return b.original_id_syntax_only(raw)

class SyntaxOnly(unittest.TestCase):
    def test_positive(self):self.assertEqual(b.classify_id_syntax("12"),"ascii_positive_unsigned_int")
    def test_zero(self):self.assertEqual(b.classify_id_syntax("0"),"ascii_zero")
    def test_negative(self):self.assertEqual(b.classify_id_syntax("-1"),"ascii_signed_negative_int")
    def test_decimal(self):self.assertEqual(b.classify_id_syntax("1.0"),"ascii_finite_decimal_syntax")
    def test_null(self):self.assertEqual(b.classify_id_syntax("NA"),"blank_or_NA_literal")
    def test_blank(self):self.assertEqual(b.classify_id_syntax(""),"blank_or_NA_literal")
    def test_other_ascii(self):self.assertEqual(b.classify_id_syntax("ID12"),"other_printable_ascii_string")
    def test_nonascii(self):self.assertEqual(b.classify_id_syntax("β"),"nonascii_or_control")
    def test_actual_meta_aggregate_only(self):
        r=audited(fixture())
        self.assertEqual(r["original_source_rows"],8)
        d=r["source_four_ID_field_syntax_counts"]["Opponent_ID"]
        self.assertEqual(sum(d.values()),8)
        self.assertEqual(d["blank_or_NA_literal"],2)
        self.assertFalse(r["any_original_Action_or_Opponent_Action_values_accessed"])
        self.assertNotIn("PRIVATE_C",str(r))
        self.assertNotIn("PRIVATE_D",str(r))
    def test_source_invalid_MD5(self):
        self.assertRaises(a.SourceError,b.original_id_syntax_only,fixture())
    def test_uninspected_action_suffix_does_not_affect_ID_syntax(self):
        raw=fixture().replace(b"PRIVATE_D",b"PRIVATE_X")
        with patch.object(a,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()), \
             patch.object(b,"PINNED_SHA",hashlib.sha256(raw).hexdigest()), \
             patch.object(b,"PINNED_N",8):
            result=b.original_id_syntax_only(raw)
        self.assertEqual(result["original_source_rows"],8)
        self.assertFalse(result["any_original_Action_or_Opponent_Action_values_accessed"])

if __name__=="__main__":
    unittest.main()
