"""R106 C1 pure synthetic seven source ID format classes; never human decisions."""
import hashlib
import io
import unittest
from unittest.mock import patch

import pandas as pd
from pandas.io.stata import StataReader

import r106_phase_a_2025_drouvelis_pearce_zenodo_original_dta_md5_only as a
import r106_phase_b_2025_publisher_dta_header_variables_nobs_only as b
import r106_phase_c1_2025_source_seven_identity_field_syntax_anonymous_only as d

def synthetic():
    df=pd.DataFrame({
        "Session":[1,1,2,2,3,3],
        "Subject":[1,2,1,2,1,2],
        "Group":[0,0,1,1,float("nan"),1],
        "Period":[1,2,3,4,5,6],
        "ID":[10,11,12,13,14,15],
        "sessionid":[100,100,101,101,102,102],
        "ClientNumber":[1,2,1,2,1,2],
        "left":[1,0,1,0,1,0],
        "otherleft":[0,1,0,1,0,1],
        "p2otherleft":[0,1,0,1,0,1],
        "secret":["PERSON123"]*6
    })
    o=io.BytesIO()
    df.to_stata(o,write_index=False,version=118)
    return o.getvalue(),len(df.columns),len(df)

def audited(raw,numvars,n):
    digest=hashlib.sha256(raw).hexdigest()
    with patch.object(a,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()), \
         patch.object(b,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()), \
         patch.object(b,"PINNED_BYTES",len(raw)), \
         patch.object(b,"PINNED_SHA256",digest), \
         patch.object(d,"PINNED_SHA256",digest), \
         patch.object(d,"SOURCE_VARS",numvars), \
         patch.object(d,"SOURCE_ROWS",n):
        return d.anonymous_id_types_only(raw)

class OriginalSevenIDTypesSynthetic(unittest.TestCase):
    def test_positive(self):self.assertEqual(d.class_only(8),"numeric_positive_integer_bounded")
    def test_zero(self):self.assertEqual(d.class_only(0),"numeric_zero")
    def test_negative(self):self.assertEqual(d.class_only(-8),"numeric_negative_integer")
    def test_large_integer(self):self.assertEqual(d.class_only(1000000001),"numeric_positive_integer_above_original_1e9_ceiling")
    def test_fractional(self):self.assertEqual(d.class_only(2.5),"numeric_fractional")
    def test_missing(self):self.assertEqual(d.class_only(float("nan")),"missing_nan_or_blank")
    def test_numeric_string(self):self.assertEqual(d.class_only("1.0"),"ascii_numeric_string")
    def test_nonnumeric_string(self):self.assertEqual(d.class_only("A-1"),"ascii_nonnumeric_string")
    def test_unicode(self):self.assertEqual(d.class_only("β"),"unicode_string")
    def test_six_fake_original_rows_without_any_action_column(self):
        raw,k,n=synthetic()
        result=audited(raw,k,n)
        self.assertEqual(result["original_source_row_count"],6)
        self.assertEqual(result["anonymous_seven_ID_source_field_type_classes"]["Group"]["missing_nan_or_blank"],1)
        self.assertEqual(result["anonymous_source_ID_field_distinct_nonmissing_counts"]["Session"],3)
        self.assertFalse(result["original_left_otherleft_p2otherleft_application_accessed"])
        self.assertNotIn("PERSON123",str(result))
        self.assertEqual(result["original_human_behavior_scores"],0)
    def test_selected_column_security(self):
        raw,k,n=synthetic()
        original=StataReader.read
        def read_guard(self,*args,**kwargs):
            assert set(kwargs["columns"])==set(d.COLUMNS)
            assert {"left","otherleft","p2otherleft","secret"}.isdisjoint(kwargs["columns"])
            return original(self,*args,**kwargs)
        with patch.object(StataReader,"read",read_guard):
            audited(raw,k,n)
    def test_MD5_failure_before_ID_cells(self):
        raw,k,n=synthetic()
        with self.assertRaises(a.SourceError):
            d.anonymous_id_types_only(raw)
    def test_bad_original_SHA_not_accepted(self):
        raw,k,n=synthetic()
        with patch.object(a,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()):
            self.assertRaises(a.SourceError,d.anonymous_id_types_only,raw)

if __name__=="__main__":
    unittest.main()
