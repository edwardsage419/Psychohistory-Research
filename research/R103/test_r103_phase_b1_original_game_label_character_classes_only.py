"""R103 B1 Game-only anonymized char class synthetic tests."""
import csv
import hashlib
import io
import unittest
from unittest.mock import patch
import r103_phase_a_2016_drbrain_original_md5_header_only as a
import r103_phase_b_2016_original_dyadic_actor_opponent_reciprocity_only as b
import r103_phase_b1_original_game_label_character_classes_only as c

def toy(games=("Prisoner's Dilemma","Hawk-Dove","Stag Hunt")):
    out=io.StringIO(newline="")
    writer=csv.DictWriter(out,fieldnames=a.MANDATORY_FIELDS,lineterminator="\n")
    writer.writeheader()
    for i,g in enumerate(games):
        writer.writerow(dict(User_ID=str(i+1),Experiment_number="1",
           Round_number="1",S="1",T="3",Game=g,Action="PRIVATE_ACTION",
           Opponent_ID="8",Opponent_Action="PRIVATE_PEER_ACTION"))
    return out.getvalue().encode()

def audited(x):
    with patch.object(a,"OFFICIAL_MD5",hashlib.md5(x).hexdigest()), \
         patch.object(b,"PINNED_SOURCE_SHA",hashlib.sha256(x).hexdigest()), \
         patch.object(b,"PINNED_LINES",x.count(b"\n")-1), \
         patch.object(c,"PINNED_SOURCE_SHA",hashlib.sha256(x).hexdigest()), \
         patch.object(c,"PINNED_LINES",x.count(b"\n")-1):
        return c.label_format_only(x)

class B1(unittest.TestCase):
    def test_exact_safe_meta(self):
        x=audited(toy())
        self.assertEqual(x["distinct_original_game_labels_count"],3)
        self.assertEqual(x["original_source_rows"],3)
        self.assertIn(ord("'"),x["ascii_punctuation_unicode_decimal_codepoints_only"])
        self.assertFalse(x["any_original_Action_or_Opponent_Action_values_accessed"])
    def test_no_literal_game_or_decision_leak(self):
        r=audited(toy())
        self.assertNotIn("Prisoner",str(r))
        self.assertNotIn("PRIVATE_ACTION",str(r))
        self.assertFalse(r["any_original_Game_text_exported"])
    def test_game_punctuation_class(self):
        self.assertEqual(c.classify_label("'"),"ascii_punctuation")
    def test_ascii_whitespace_class(self):
        self.assertEqual(c.classify_label(" "),"ascii_whitespace")
    def test_unicode_class_nonascii(self):
        self.assertEqual(c.classify_label("β"),"nonascii_or_control")
    def test_original_bad_md5_refused(self):
        self.assertRaises(a.SourceError,c.label_format_only,toy())
    def test_oversize_label_rejected(self):
        self.assertRaises(c.SourceError,audited,toy(games=("x"*101,)))
    def test_label_unicode_counts_anonymous(self):
        r=audited(toy(games=("β",)))
        self.assertEqual(r["anonymous_game_label_character_class_count"]["nonascii_or_control"],1)
        self.assertNotIn("β",str(r))

if __name__=="__main__":
    unittest.main()
