"""Pure-synthetic R100 B1b source A/B reciprocal match and graph tests."""
import io
import unittest
import zipfile
import r100_phase_b1b_original_AB_role_partner_reciprocal_graph as m

def cohort(t="T"):
    return [
        (t,1,["1",None,None,None],["A1","B1","B2","A1"]),
        (t,1,["2",None,None,None],["A2","B2","B1","A2"]),
        (t,2,["3",None,None,None],["A1","B1","B1","A2"]),
        (t,2,["4",None,None,None],["A2","B2","B2","A1"]),
    ]

def five():
    return sum((cohort("T"+str(i)) for i in range(5)),[])

class SyntheticB1b(unittest.TestCase):
    def test_five_cohorts_perfect_reciprocity(self):
        r=m.assess_blocks(five(),expected_sizes=[4]*5)
        self.assertEqual(r["status"],"B1B_STRICT_SOURCE_PAIR_RECIPROCITY_PASS")
        self.assertEqual(r["verified_distinct_source_people"],20)
        self.assertTrue(r["source_pair_full_reciprocity"])
        for t in r["anonymous_treatment_summaries"]:
            self.assertEqual(t["stage1_undirected_pair_candidates"],2)
            self.assertEqual(t["stage2_undirected_pair_candidates"],2)
            self.assertEqual(t["person_graph_connected_components"],1)
    def test_stable_partner_not_allowed(self):
        x=five()
        x[0]=(x[0][0],x[0][1],x[0][2],["A1","B1","B1","A1"])
        r=m.assess_blocks(x,expected_sizes=[4]*5)
        self.assertEqual(r["status"],"B1B_BLOCKED_BOUNDED")
        self.assertGreater(r["anonymous_treatment_summaries"][0]["violations"]["same_opponent_two_sessions"],0)
    def test_wrong_role_repetition_blocked(self):
        x=five()
        x[0]=(x[0][0],x[0][1],x[0][2],["A1","B1","A1","B2"])
        r=m.assess_blocks(x,expected_sizes=[4]*5)
        self.assertGreater(r["anonymous_treatment_summaries"][0]["violations"]["focal_repeated_position_mismatch"],0)
    def test_duplicate_A_source_ID_blocked(self):
        x=five()
        x[1]=(x[1][0],x[1][1],["1",None,None,None],x[1][3])
        r=m.assess_blocks(x,expected_sizes=[4]*5)
        self.assertIn("duplicated_source_A_identifier",r["anonymous_treatment_summaries"][0]["violations"])
    def test_duplicate_self_code_blocked(self):
        x=five()
        x[1]=(x[1][0],x[1][1],x[1][2],["A1","B2","B1","A1"])
        r=m.assess_blocks(x,expected_sizes=[4]*5)
        self.assertIn("duplicated_B_focal_identifier",r["anonymous_treatment_summaries"][0]["violations"])
    def test_unmatched_peer_code_blocked(self):
        x=five()
        x[0]=(x[0][0],x[0][1],x[0][2],["A1","GHOST","B2","A1"])
        r=m.assess_blocks(x,expected_sizes=[4]*5)
        self.assertGreater(r["anonymous_treatment_summaries"][0]["violations"]["unmatched_B_partner_code"],0)
    def test_nonreciprocal_peer_code_blocked(self):
        x=five()
        x[0]=(x[0][0],x[0][1],x[0][2],["A1","B2","B2","A1"])
        r=m.assess_blocks(x,expected_sizes=[4]*5)
        self.assertIn("nonreciprocal_partner",r["anonymous_treatment_summaries"][0]["violations"])
    def test_same_role_pair_blocked(self):
        x=five()
        x[0]=(x[0][0],x[0][1],x[0][2],["A1","A2","B2","A1"])
        r=m.assess_blocks(x,expected_sizes=[4]*5)
        self.assertIn("same_role_within_pair",r["anonymous_treatment_summaries"][0]["violations"])
    def test_missing_A_on_first_row_blocked(self):
        x=five()
        x[0]=(x[0][0],x[0][1],[None,"1",None,None],x[0][3])
        r=m.assess_blocks(x,expected_sizes=[4]*5)
        self.assertIn("A_not_one_code_on_first_row",r["anonymous_treatment_summaries"][0]["violations"])
    def test_treatment_size_mismatch_blocked(self):
        r=m.assess_blocks(five(),expected_sizes=[4,4,4,4,6])
        self.assertEqual(r["status"],"B1B_BLOCKED_BOUNDED")
        self.assertFalse(r["five_original_treatments_expected_sizes_match"])
    def test_single_cohort_cannot_masquerade_as_five(self):
        with self.assertRaises(m.SourceError):m.assess_blocks(cohort())
    def test_no_original_code_publication(self):
        r=m.assess_blocks(five(),expected_sizes=[4]*5)
        self.assertNotIn("A1",str(r))
        self.assertNotIn("GHOST",str(r))
        self.assertFalse(r["original_person_pair_ids_exported"])
        self.assertEqual(r["C_to_Z_cell_values_dereferenced"],0)
    def test_components_two_unconnected_pairs(self):
        graph={"x":{"y"},"y":{"x"},"a":{"b"},"b":{"a"}}
        self.assertEqual(m.count_components(graph),(2,2,2))
    def test_missing_workbook_rels_rejected(self):
        o=io.BytesIO()
        with zipfile.ZipFile(o,"w") as z:z.writestr("xl/workbook.xml","<x/>")
        with zipfile.ZipFile(io.BytesIO(o.getvalue())) as z:
            self.assertRaises(m.SourceError,m.approved_workbook_sheet_map,z)

if __name__=="__main__":
    unittest.main()
