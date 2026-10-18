"""R106 C pure synthetic fake Stata cohort, only nonbehavior original session-pair roster."""
from __future__ import annotations
import hashlib
import io
import unittest
from unittest.mock import patch

import pandas as pd
from pandas.io.stata import StataReader
import r106_phase_a_2025_drouvelis_pearce_zenodo_original_dta_md5_only as a
import r106_phase_b_2025_publisher_dta_header_variables_nobs_only as b
import r106_phase_c_2025_original_26session_dyadic_nonbehavior_roster_census as c

def synthetic(extra=None):
    rows=[]
    for s in (1,2):
        for t in (1,2):
            for person in (1,2):
                rows.append({
                    "Session":s,"Subject":person,"ID":10*s+person,"sessionid":s,
                    "Group":1,"Period":t,"part":2,"game":1,
                    "practiceperiod":t,"realround":t,
                    "realperiod":t,"practiceround":t,
                    "left":0,"otherleft":1,"p2otherleft":0,
                    "PRIVATE_DECISION":"DO_NOT_REVEAL",
                })
    if extra:
        extra(rows)
    out=io.BytesIO()
    pd.DataFrame(rows).to_stata(out,write_index=False,version=118)
    return out.getvalue(),len(rows),len(rows[0])

def audited(raw,n,nvar):
    digest=hashlib.sha256(raw).hexdigest()
    with patch.object(a,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()), \
         patch.object(b,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()), \
         patch.object(b,"PINNED_BYTES",len(raw)), \
         patch.object(b,"PINNED_SHA256",digest), \
         patch.object(c,"PINNED_SHA256",digest), \
         patch.object(c,"EXPECTED_NOBS",n), \
         patch.object(c,"EXPECTED_VARS",nvar):
        return c.source_roster_only(raw)

class R106TrueCohortSynthetic(unittest.TestCase):
    def test_eight_fake_source_actor_rounds_four_valid_pair_keys(self):
        raw,n,v=synthetic()
        x=audited(raw,n,v)
        self.assertEqual(x["original_data_frame_rows_header_verified"],8)
        self.assertEqual(x["original_source_distinct_session_labels"],2)
        self.assertEqual(x["original_distinct_source_session_subject_pairs"],4)
        self.assertEqual(x["all_part_source_pair_coverage"]["exact_two_distinct_person_pair_keys"],4)
        self.assertEqual(x["part2_original_source_pair_eligible_actor_fraction"],1)
        self.assertEqual(x["original_human_model_scores"],0)
    def test_true_data_cell_strings_never_published(self):
        raw,n,v=synthetic()
        x=audited(raw,n,v)
        self.assertNotIn("DO_NOT_REVEAL",str(x))
        self.assertTrue(x["Stata_library_internally_decodes_rows_but_application_retrieves_only_whitelisted_nonbehavior_fields"])
        self.assertFalse(x["original_choice_own_partner_or_prior_partner_columns_application_accessed"])
        self.assertFalse(x["source_raw_person_session_group_identifiers_exported"])
    def test_pandas_gets_only_12_source_nonbehavior_column_names(self):
        original=StataReader.read
        def spy(self,*args,**kwargs):
            cols=kwargs.get("columns")
            assert cols is not None and set(cols)==set(c.WHITELIST)
            assert {"left","otherleft","p2otherleft","PRIVATE_DECISION"}.isdisjoint(cols)
            return original(self,*args,**kwargs)
        raw,n,v=synthetic()
        with patch.object(StataReader,"read",spy):
            x=audited(raw,n,v)
        self.assertEqual(x["original_human_model_scores"],0)
    def test_technical_part3_is_not_mistaken_for_true_PD(self):
        def edit(rows):
            rows[-1]["part"]=3
        raw,n,v=synthetic(edit)
        x=audited(raw,n,v)
        self.assertEqual(x["source_part_category_row_counts"]["3"],1)
        self.assertEqual(x["part2_source_actor_rows"],7)
        self.assertEqual(x["part2_only_source_pair_coverage"]["source_actor_rows_in_exact_two_person_pairs"],6)
    def test_missing_pair_group_classified(self):
        def edit(rows):
            rows[0]["Group"]=float("nan")
        raw,n,v=synthetic(edit)
        x=audited(raw,n,v)
        self.assertEqual(x["source_rows_not_eligible_for_group_period_pair_key"],1)
        self.assertEqual(x["all_part_source_pair_coverage"]["source_actor_rows_in_exact_two_person_pairs"],6)
    def test_wrong_pair_group_overfull_fails_eligibility(self):
        def edit(rows):
            rows.append(dict(rows[0],Subject=3,ID=13))
        raw,n,v=synthetic(edit)
        x=audited(raw,n,v)
        self.assertEqual(x["all_part_source_pair_coverage"]["group_record_count_histogram"]["3"],1)
        self.assertEqual(x["part2_only_source_pair_coverage"]["source_actor_rows_in_exact_two_person_pairs"],6)
    def test_id_reuse_across_sessions_is_reported_anonymously(self):
        def edit(rows):
            for r in rows:
                r["ID"]=r["Subject"]
        raw,n,v=synthetic(edit)
        x=audited(raw,n,v)
        self.assertEqual(x["source_ID_codes_reused_across_source_sessions"],2)
        self.assertNotIn("Session: 1",str(x))
    def test_invalid_source_md5_rejected_before_row_decoding(self):
        raw,n,v=synthetic()
        with self.assertRaises(a.SourceError):
            c.source_roster_only(raw)
    def test_bad_original_source_sha_does_not_get_to_rows(self):
        raw,n,v=synthetic()
        with patch.object(a,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()):
            self.assertRaises(a.SourceError,c.source_roster_only,raw)
    def test_bad_missing_session_classified_not_imputed(self):
        def edit(rows):rows[0]["Session"]=float("nan")
        raw,n,v=synthetic(edit)
        x=audited(raw,n,v)
        self.assertEqual(x["source_missing_session_or_subject_source_rows"],1)
    def test_noninteger_period_not_false_pair(self):
        def edit(rows):rows[0]["Period"]=1.5
        raw,n,v=synthetic(edit)
        x=audited(raw,n,v)
        self.assertEqual(x["source_rows_not_eligible_for_group_period_pair_key"],1)
    def test_direct_id_value_validation(self):
        self.assertIsNone(c.as_id(float("nan")))
        self.assertIsNone(c.as_id(-1))
        self.assertEqual(c.as_id(3),3)

if __name__=="__main__":
    unittest.main()
