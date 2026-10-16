"""Only invented sample rows; test forbidden inter-village joins and wave completeness."""
import copy
import unittest
from r066_larson_lewis_join_gate import (
    ITEMS,NETWORKS,WAVES,SCHEMA_ROWS,SCHEMA_COLS,analyze_rows,parse_response,
)


def dummy():
    base=["village_number","ego","trt","in_el","treatment_type"]
    items=[prefix+suffix for suffix in WAVES.values() for prefix in ITEMS]
    net=[x for g in NETWORKS.values() for x in g]
    header=base+items+net
    header+=["dummy"+str(i) for i in range(SCHEMA_COLS-len(header))]
    assert len(header)==SCHEMA_COLS
    rows=[]
    for i in range(SCHEMA_ROWS):
        rec=dict.fromkeys(header,".")
        rec.update({"village_number":"1","ego":str(i+1),"trt":"1",
                    "in_el":"1","treatment_type":"1",
                    "visit1":str((i+1)%SCHEMA_ROWS+1)})
        for col in items:
            rec[col]="3"
        rows.append(rec)
    return header,rows


class NetworkAndWaveGateTests(unittest.TestCase):
    def test_full_source_candidate_links(self):
        headers,rows=dummy()
        x=analyze_rows(headers,rows)
        self.assertEqual(x["distinct_villages"],1)
        self.assertEqual(x["complete_candidate_baseline_and_endline_rows"],SCHEMA_ROWS)
        self.assertEqual(x["network_nomination_summaries"]["visit"]["within_village_exact_ego_matches"],SCHEMA_ROWS)
        self.assertEqual(x["join_candidate_status"],"JOIN_CANDIDATE_SUPPORTED")
        self.assertTrue(x["all_source_respondent_rows_kept_private"])
        self.assertNotIn('"ego":',str(x))

    def test_baseline_missing_reduces_complete_pair(self):
        h,r=dummy()
        r[0]["noprob1"]="."
        q=analyze_rows(h,r)
        self.assertEqual(q["complete_candidate_baseline_and_endline_rows"],SCHEMA_ROWS-1)

    def test_intervillage_nomination_not_joined(self):
        h,r=dummy()
        r[0]["village_number"]="2"
        r[0]["visit1"]="2"  # exists only in village 1
        q=analyze_rows(h,r)
        self.assertGreater(q["network_nomination_summaries"]["visit"]["unmatched_or_outside_village"],0)

    def test_duplicate_ego_key_blocks_join(self):
        h,r=dummy()
        r[0]["ego"]=r[1]["ego"]
        q=analyze_rows(h,r)
        self.assertEqual(q["join_candidate_status"],"JOIN_CANDIDATE_BLOCKED")
        self.assertEqual(q["duplicate_within_village_ego_keys"],1)

    def test_all_unmatched_nominations_block_join(self):
        h,r=dummy()
        for row in r:
            row["visit1"]="NO_MATCH"
        q=analyze_rows(h,r)
        self.assertEqual(q["join_candidate_status"],"JOIN_CANDIDATE_BLOCKED")

    def test_nonfinite_opinion_not_complete(self):
        self.assertEqual(parse_response("NaN"),("missing",None))
        self.assertEqual(parse_response("inf"),("non_numeric",None))
        self.assertEqual(parse_response("6"),("outside_1_5",6.0))

    def test_bad_schema_universe_blocked(self):
        h,r=dummy()
        with self.assertRaises(ValueError):
            analyze_rows(h,r[:15])

    def test_omitted_wave_column_rejected(self):
        h,r=dummy()
        h.remove("values_e")
        with self.assertRaises(ValueError):
            analyze_rows(h,r)

    def test_public_results_do_not_prove_model_fit(self):
        h,r=dummy()
        q=analyze_rows(h,r)
        self.assertFalse(q["real_model_fit_performed"])
        self.assertEqual(q["model_identification_ready"],"OPEN")
        self.assertFalse(q["scoring_direction_confirmed"])


if __name__=="__main__":
    unittest.main()
