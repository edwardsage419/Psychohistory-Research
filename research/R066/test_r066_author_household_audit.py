"""Author-derived household network construction on synthetic identities only."""
import unittest
from r066_author_household_audit import summarize_author_households
from r066_larson_lewis_join_gate import ITEMS,WAVES,NETWORKS

def fixture():
    villages={}
    for i in range(2125):
        v=str((i%16)+1)
        villages.setdefault(v,[]).append(i)
    rows=[]
    for i in range(2125):
        v=str(i%16+1)
        group=villages[v]
        j=group[(group.index(i)+1)%len(group)]
        row={"village_number":v,
             "ego":"individual"+str(i),"hhh":"househead"+str(i),
             "hhnum":str(i//16+1),
             "visit1":"househead"+str(j)}
        for n in range(1,12):
            row["hh"+str(n)]="."
        for columns in NETWORKS.values():
            for field in columns:
                row.setdefault(field,".")
        for suf in WAVES.values():
            for pre in ITEMS:
                row[pre+suf]="3"
        rows.append(row)
    return rows

class HouseholdProof(unittest.TestCase):
    def test_16_village_household_edges_exist(self):
        rows=fixture()
        r=summarize_author_households(rows)
        self.assertEqual(r["village_count"],16)
        self.assertEqual(r["all_types_union_unique_household_edges"],2125)
        self.assertEqual(r["author_algorithm_derived_household_networks"]["visit"]["nominations_converted_to_household_edges"],2125)
        self.assertEqual(r["union_household_nodes_without_edge"],0)
        self.assertFalse(r["real_model_fit_performed"])
        self.assertNotIn("individual0",str(r))
        self.assertNotIn("househead0",str(r))

    def test_other_village_member_alias_does_not_join(self):
        rows=fixture()
        rows[0]["visit1"]="househead1" # row1 is a different village
        r=summarize_author_households(rows)
        self.assertGreater(r["author_algorithm_derived_household_networks"]["visit"]["nominations_not_convertible"],0)

    def test_six_item_score_is_author_direct_sum(self):
        r=summarize_author_households(fixture())
        self.assertEqual(r["six_item_author_code_sum_6_to_30"]["candidate_baseline"]["index_min"],18)
        self.assertEqual(r["candidate_baseline_and_endline_complete"],2125)

    def test_missing_survey_item_reduces_complete(self):
        rows=fixture()
        rows[0]["fit_e"]="."
        r=summarize_author_households(rows)
        self.assertEqual(r["candidate_baseline_and_endline_complete"],2124)

    def test_source_universe_requires_2125(self):
        with self.assertRaises(ValueError):
            summarize_author_households(fixture()[:-1])

    def test_member_ambiguity_not_silently_assigned_to_one_house(self):
        rows=fixture()
        rows[0]["hh1"]=rows[16]["hhh"] # same-village household member in two rows
        r=summarize_author_households(rows)
        self.assertGreater(r["ambiguous_person_identifiers_shared_by_multiple_households"],0)


if __name__=="__main__":
    unittest.main()
