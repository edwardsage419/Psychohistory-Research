"""R106 C2 pure synthetic 26 recruited source sessions and two-person pairing."""
from __future__ import annotations
import hashlib
import io
import unittest
from unittest.mock import patch
import pandas as pd
from pandas.io.stata import StataReader

import r106_phase_a_2025_drouvelis_pearce_zenodo_original_dta_md5_only as a
import r106_phase_b_2025_publisher_dta_header_variables_nobs_only as b
import r106_phase_c2_2025_original_sessionid_global_ID_person_partner_roster as c


def artificial(edit=None):
    rows=[]
    for sess in range(1,27):
        for period in range(1,3):
            for subject in range(1,11):
                d=dict(
                    sessionid=sess, ID=(sess-1)*10+subject,
                    Subject=subject,Group=(subject-1)//2+1,
                    Period=period,part=2,game=1,practiceperiod=period,
                    Session=str((sess-1)%15+1),
                    left=0,otherleft=1,p2otherleft=0,
                )
                if edit:edit(d,sess,period,subject)
                rows.append(d)
    o=io.BytesIO()
    pd.DataFrame(rows).to_stata(o,version=118,write_index=False)
    return o.getvalue(),len(rows),len(rows[0])


def audited(raw,n,nvars):
    sha=hashlib.sha256(raw).hexdigest()
    with patch.object(a,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()), \
         patch.object(b,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()), \
         patch.object(b,"PINNED_SHA256",sha), \
         patch.object(b,"PINNED_BYTES",len(raw)), \
         patch.object(c,"PINNED_SHA256",sha), \
         patch.object(c,"NROWS",n), \
         patch.object(c,"NVARS",nvars):
        return c.source_true_roster(raw)

class True2025SourcePersonAndDyadSynthetic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source,cls.n,cls.k=artificial()
    def test_actual_26_by10_distinct_cohort_candidate(self):
        x=audited(self.source,self.n,self.k)
        self.assertEqual(x["status"],"R106_C2_GENUINE_2025_RECRUITED_26SESSION_260_ID_SOURCE_DYADS_ELIGIBLE")
        self.assertEqual(x["original_sessions_by_numeric_sessionid"],26)
        self.assertEqual(x["original_unique_global_ID_people"],260)
        self.assertEqual(x["source_session_persons_count_histogram"],{"10":26})
        self.assertTrue(x["source_identity_and_candidate_pair_gate_passed"])
    def test_exact_260_two_actor_group_period_keys(self):
        x=audited(self.source,self.n,self.k)
        self.assertEqual(x["candidate_true_two_distinct_person_group_period_events"],260)
        self.assertEqual(x["source_part2_actor_rows_in_true_candidate_pairs"],520)
        self.assertEqual(x["candidate_source_part2_row_pair_coverage"],1)
    def test_session_alias_duplicates_dont_conflate_26_true_sessions(self):
        x=audited(self.source,self.n,self.k)
        self.assertEqual(x["source_Session_string_aliases_shared_across_different_real_sessionid_count"],11)
        self.assertEqual(x["original_sessions_by_numeric_sessionid"],26)
    def test_privacy_and_zero_behavior_read(self):
        x=audited(self.source,self.n,self.k)
        self.assertFalse(x["original_human_source_action_columns_application_accessed"])
        self.assertFalse(x["raw_person_session_pair_ID_values_exported"])
        self.assertEqual(x["real_human_model_scores"],0)
    def test_stata_reader_never_selects_action_columns(self):
        original=StataReader.read
        def wrapped(self,*args,**kwargs):
            assert set(kwargs["columns"])==set(c.FIELDS)
            assert {"left","otherleft","p2otherleft"}.isdisjoint(kwargs["columns"])
            return original(self,*args,**kwargs)
        with patch.object(StataReader,"read",wrapped):
            audited(self.source,self.n,self.k)
    def test_reused_global_actor_ID_across_sessions_detected(self):
        def edit(x,s,t,p):
            if s==2 and p==1:x["ID"]=1
        raw,n,k=artificial(edit)
        r=audited(raw,n,k)
        self.assertFalse(r["source_identity_and_candidate_pair_gate_passed"])
        self.assertGreater(r["source_global_ID_codes_reused_between_sessions"],0)
    def test_missing_paired_subject_classified(self):
        def edit(x,s,t,p):
            if s==1 and t==1 and p==1:x["Group"]=2
        raw,n,k=artificial(edit)
        r=audited(raw,n,k)
        self.assertEqual(r["source_group_period_row_size_histogram"]["3"],1)
        self.assertEqual(r["source_group_period_row_size_histogram"]["1"],1)
        self.assertLess(r["candidate_source_part2_row_pair_coverage"],1)
    def test_duplicate_subject_ID_in_same_session_period_detected(self):
        def edit(x,s,t,p):
            if s==1 and t==1 and p==2:x["ID"]=1
        raw,n,k=artificial(edit)
        r=audited(raw,n,k)
        self.assertGreater(r["original_person_period_key_duplicate_record_count"],0)
        self.assertFalse(r["source_identity_and_candidate_pair_gate_passed"])
    def test_identity_positivity_and_string_alias_policy(self):
        self.assertIsNone(c.pos_int(-1))
        self.assertIsNone(c.pos_int(float("nan")))
        self.assertEqual(c.pos_int(100),100)
        self.assertIsNone(c.session_alias("UNKNOWN"))
        self.assertEqual(c.session_alias("1234"),"1234")
    def test_wrong_original_md5_fails_before_row_loading(self):
        with self.assertRaises(a.SourceError):
            c.source_true_roster(self.source)
    def test_missing_alias_diagnostic_without_export(self):
        def edit(x,s,t,p):
            if s==1 and t==1 and p==1:x["Session"]="INVALID_ALIAS"
        raw,n,k=artificial(edit)
        r=audited(raw,n,k)
        self.assertEqual(r["source_Session_string_alias_missing_or_unrecognized_rows"],1)
        self.assertNotIn("INVALID_ALIAS",str(r))
    def test_nonzero_part3_original_rows_preserved_and_excluded_from_pairing(self):
        def edit(x,s,t,p):
            if s==1 and t==1 and p==1:x["part"]=3
        raw,n,k=artificial(edit)
        r=audited(raw,n,k)
        self.assertEqual(r["source_part_task_record_counts"]["3"],1)
        self.assertEqual(r["source_part2_all_actor_rows"],519)
        self.assertFalse(r["source_identity_and_candidate_pair_gate_passed"] is None)

if __name__=="__main__":
    unittest.main()
