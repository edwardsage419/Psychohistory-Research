"""R106 B synthetic Stata 117/118 header tests. No original human records."""
from __future__ import annotations
import hashlib
import io
import unittest
from unittest.mock import patch

import pandas as pd
from pandas.io.stata import StataReader

import r106_phase_a_2025_drouvelis_pearce_zenodo_original_dta_md5_only as a
import r106_phase_b_2025_publisher_dta_header_variables_nobs_only as b


def fake_stata(version=118, n=12):
    o=io.BytesIO()
    pd.DataFrame({
        "source_session":[1]*n,
        "source_actor":list(range(n)),
        "source_period":[1]*n,
        "source_action":[0]*n,
        "private_code":["DO_NOT_EXPORT"]*n,
    }).to_stata(o,version=version,write_index=False)
    return o.getvalue()


def audit_fake(raw):
    with patch.object(a,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()), \
         patch.object(b,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()), \
         patch.object(b,"PINNED_SHA256",hashlib.sha256(raw).hexdigest()), \
         patch.object(b,"PINNED_BYTES",len(raw)):
        return b.metadata_only(raw)


class R106HeaderOnly(unittest.TestCase):
    def test_realistic_stata118_names_types_and_N(self):
        out=audit_fake(fake_stata())
        self.assertEqual(out["Stata_header_observation_count_unverified_human_rows"],12)
        self.assertEqual(out["Stata_header_variable_count"],5)
        self.assertEqual(out["Stata_header_type_family_counts"]["numeric_integer"],4)
        self.assertEqual(out["Stata_header_type_family_counts"]["string"],1)
        self.assertEqual(out["actual_original_human_record_cells_read"],0)
        self.assertEqual(out["actual_human_model_scores"],0)
    def test_117_metadata_supported(self):
        out=audit_fake(fake_stata(version=117))
        self.assertEqual(out["Stata_header_variable_count"],5)
        self.assertEqual(out["Stata_header_observation_count_unverified_human_rows"],12)
    def test_no_record_read_even_if_stata_reader_read_is_forbidden(self):
        raw=fake_stata()
        with patch.object(StataReader,"read",side_effect=AssertionError("row read forbidden")), \
             patch.object(StataReader,"get_chunk",side_effect=AssertionError("chunk read forbidden")):
            out=audit_fake(raw)
        self.assertEqual(out["actual_original_human_record_cells_read"],0)
    def test_no_real_actions_or_private_cells_released(self):
        out=audit_fake(fake_stata())
        self.assertNotIn("DO_NOT_EXPORT",repr(out))
        self.assertFalse(out["actual_dataset_contains_260_new_humans_verified"])
        self.assertFalse(out["original_paired_opponent_identity_verified"])
    def test_original_md5_still_rejects(self):
        with self.assertRaises(a.SourceError):
            b.metadata_only(fake_stata())
    def test_wrong_pinned_source_hash_rejected(self):
        raw=fake_stata()
        with patch.object(a,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()):
            self.assertRaises(a.SourceError,b.metadata_only,raw)
    def test_bad_short_bytes_rejected(self):
        with self.assertRaises(a.SourceError):
            b.metadata_only(b"")
    def test_stata_integer_types_classified(self):
        self.assertEqual(b.type_class("l"),"numeric_integer")
        self.assertEqual(b.type_class("h"),"numeric_integer")
        self.assertEqual(b.type_class("b"),"numeric_integer")
    def test_stata_float_types_classified(self):
        self.assertEqual(b.type_class("d"),"numeric_float")
        self.assertEqual(b.type_class("f"),"numeric_float")
    def test_stata_str_width_classified(self):
        self.assertEqual(b.type_class(100),"string")
        self.assertEqual(b.type_class("Q"),"string")
    def test_invalid_external_column_name_not_exported(self):
        raw=fake_stata()
        with patch.object(a,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()), \
             patch.object(b,"PINNED_SHA256",hashlib.sha256(raw).hexdigest()), \
             patch.object(b,"PINNED_BYTES",len(raw)), \
             patch.object(StataReader,"_get_varlist",return_value=["Private/Actor","good","other","four","five"]):
            self.assertRaises(b.SourceError,b.metadata_only,raw)
    def test_original_source_URL_pinned(self):
        a.validate_url(a.URL)
        self.assertRaises(a.SourceError,a.validate_url,a.URL.replace("zenodo.org","hostile.example"))


if __name__=="__main__":
    unittest.main()
