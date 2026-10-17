"""R100 B1e synthetic AB key cardinality diagnostics; never use real data."""
import unittest
import r100_phase_b1e_original_AB_identity_code_cardinality_only as m

def toy_cohort(t):
    return [
      (t,1,["1",None,None,None],["A1","B1","B2","A1"]),
      (t,1,["2",None,None,None],["A2","B2","B1","A2"]),
      (t,2,["3",None,None,None],["A1","B1","B1","A2"]),
      (t,2,["4",None,None,None],["A2","B2","B2","A1"]),
    ]

def all_toy():
    return sum((toy_cohort(str(i)) for i in range(5)),[])

class PureSynthetic(unittest.TestCase):
    def test_reciprocal_graph_codes_can_be_unique(self):
        r=m.anonymous_ab_cardinality(all_toy())
        self.assertEqual(r["candidate_focus_record_total"],20)
        self.assertTrue(all(p["B_unique_person_code_sufficient_from_repeated_focal_position"] for p in r["anonymous_treatment_summaries"]))
    def test_constant_focal_code_disqualifies_unique_B(self):
        b=all_toy()
        for i,(t,role,a,codes) in enumerate(b):
            c=codes[:]
            if role==1:c[0]=c[3]="SHARED_FOCAL_ROLE1"
            else:c[1]=c[2]="SHARED_FOCAL_ROLE2"
            b[i]=(t,role,a,c)
        r=m.anonymous_ab_cardinality(b)
        self.assertTrue(all(not p["B_unique_person_code_sufficient_from_repeated_focal_position"] for p in r["anonymous_treatment_summaries"]))
    def test_two_role_sheet_A_overlap_detected(self):
        b=all_toy()
        b[2]=(b[2][0],b[2][1],["1",None,None,None],b[2][3])
        r=m.anonymous_ab_cardinality(b)
        self.assertEqual(r["anonymous_treatment_summaries"][0]["A_number_strings_shared_across_both_role_sheets"],1)
    def test_no_codes_in_public_output(self):
        self.assertNotIn("A1",repr(m.anonymous_ab_cardinality(all_toy())))
        self.assertNotIn("B2",repr(m.anonymous_ab_cardinality(all_toy())))
    def test_missing_a_rejects(self):
        b=all_toy()
        b[0]=(b[0][0],1,[None,None,None,None],b[0][3])
        with self.assertRaises(m.SourceError):m.anonymous_ab_cardinality(b)
    def test_missing_b_rejects(self):
        b=all_toy()
        codes=b[0][3][:]
        codes[1]=None
        b[0]=(b[0][0],1,b[0][2],codes)
        with self.assertRaises(m.SourceError):m.anonymous_ab_cardinality(b)
    def test_one_treatment_only_rejects(self):
        with self.assertRaises(m.SourceError):m.anonymous_ab_cardinality(toy_cohort("x"))
    def test_fake_original_rejected(self):
        with self.assertRaises(m.SourceError):m.source_check(b"FAKE")

if __name__=="__main__":
    unittest.main()
