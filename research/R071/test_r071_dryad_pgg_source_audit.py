"""Synthetic-only Dryad CSV safe source structure and inference limits."""
import unittest
from r071_dryad_pgg_source_audit import audit_bytes

class DryadSourceGates(unittest.TestCase):
    def test_public_header_stats_without_subject_rows(self):
        data=b"player_id,group,round,contribution,punishment,noise\n7,5,1,10,0,low\n8,5,1,9,1,low\n"
        x=audit_bytes(data)
        self.assertEqual(x["parsed_data_rows"],2)
        self.assertEqual(x["parsed_header_column_count"],6)
        self.assertEqual(x["candidate_semantic_field_names_only"]["cooperation"],["contribution"])
        self.assertTrue(x["no_participant_or_group_identifiers_exported"])
        self.assertNotIn("\n7,5",str(x))
        self.assertEqual(x["E2_full_human_model_fit"],"BLOCKED_MODEL_CONTRACT")

    def test_casefold_duplicate_header_rejected(self):
        with self.assertRaisesRegex(ValueError,"HEADER"):
            audit_bytes(b"User,user\n2,3\n")

    def test_empty_header_rejected(self):
        with self.assertRaisesRegex(ValueError,"HEADER"):
            audit_bytes(b"player,,round\n1,2,3\n")

    def test_empty_data_rejected(self):
        with self.assertRaisesRegex(ValueError,"ROWS_MISSING"):
            audit_bytes(b"player,round\n")

    def test_RTF_and_HTML_not_pass_csv(self):
        for raw in (b"<html><body>Access denied</body></html>",
                    b"<!DOCTYPE html><title>Forbidden</title>"):
            with self.assertRaises(ValueError):
                audit_bytes(raw)

    def test_pdf_not_pass_csv(self):
        with self.assertRaisesRegex(ValueError,"NOT_A_CSV"):
            audit_bytes(b"%PDF-1.4 pretend")

    def test_row_shape_drift_rejected(self):
        with self.assertRaisesRegex(ValueError,"ROW_LENGTH"):
            audit_bytes(b"a,b\n1,2\n3\n")

    def test_source_over_budget_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"BYTE_BUDGET"):
            audit_bytes(b"a\n"+b"x"*(4_000_000+1))

    def test_utf8_invalid_rejected(self):
        with self.assertRaisesRegex(ValueError,"ENCODING"):
            audit_bytes(b"person,x\n1,\xff\n")

    def test_no_fake_group_identity_or_known_ids(self):
        x=audit_bytes(b"person_id,treatment\n998877,control\n")
        self.assertNotIn("998877",str(x))
        self.assertFalse(x["causal_norm_or_punishment_model_fitted"])

    def test_semantic_column_candidate_not_assume_correctness(self):
        x=audit_bytes(b"cooperation_rate,round,subject_code\n.75,2,A\n")
        self.assertEqual(x["measurement_status"],
                         "CANDIDATE_HEADER_ONLY_NO_VALUE_SEMANTICS_OR_REGIME_PARITY")

if __name__=="__main__":
    unittest.main()
