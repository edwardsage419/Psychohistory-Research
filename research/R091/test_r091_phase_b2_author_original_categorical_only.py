import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r091_phase_b2_author_original_categorical_only import category_label,metadata_codes
class SafeSourceLabels(unittest.TestCase):
 def test_control(self):self.assertEqual(category_label("Control"),"Control")
 def test_sweden(self):self.assertEqual(category_label("Sweden"),"Sweden")
 def test_probabilistic_treatment(self):self.assertEqual(category_label("40P"),"40P")
 def test_mixed_case(self):self.assertEqual(category_label("philippines"),"philippines")
 def test_safe_numeric_code(self):self.assertEqual(category_label("1"),"1")
 def test_missing(self):self.assertEqual(category_label(None),"MISSING_LABEL")
 def test_email_private_redacted(self):self.assertEqual(category_label("person@example.com"),"REDACTED_UNRECOGNIZED_LABEL")
 def test_backslash_private_redacted(self):self.assertEqual(category_label("C:\\\\actor"),"REDACTED_UNRECOGNIZED_LABEL")
 def test_newline_private_redacted(self):self.assertEqual(category_label("private\nactor"),"REDACTED_UNRECOGNIZED_LABEL")
 def test_nonascii_private_redacted(self):self.assertEqual(category_label("私人资料"),"REDACTED_UNRECOGNIZED_LABEL")
 def test_excessively_long_redacted(self):self.assertEqual(category_label("A"*60),"REDACTED_UNRECOGNIZED_LABEL")
 def test_two_original_fields(self):
  r=metadata_codes([("Sweden","Control")]*3,3)
  self.assertEqual(r["original_main_actor_round_rows"],3)
  self.assertEqual(r["Country_safe_original_metadata_label_frequency"]["Sweden"],3)
 def test_real_15200_denominator_default_required(self):
  with self.assertRaises(ValueError):metadata_codes([("Sweden","Control")]*3)
 def test_malformed_columns_denied(self):
  with self.assertRaises(ValueError):metadata_codes([("Sweden","Control","PERSONID")],1)
 def test_categories_do_not_echo_private(self):
  r=metadata_codes([("PRIVATE-very-long-person-actor-ID-999999999999","CONTROL")],1)
  self.assertNotIn("999999",str(r))
if __name__=="__main__":unittest.main()
