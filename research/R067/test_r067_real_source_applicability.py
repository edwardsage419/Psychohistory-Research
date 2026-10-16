"""Synthetic-only R047 source integrity, nonbinary rejection and Dryad metadata gates."""
import csv
import hashlib
import io
import json
import unittest
from unittest.mock import patch

import r067_real_source_applicability as audit

THEORY=b"surplus_value = 6*surplus - 0.025*surplus^2\npayoff = private + surplus_share*surplus_value\n"


def sample_source():
    out=io.StringIO(newline="")
    fields=["ProfileID","GameID","RoundID","Token","Invest","Session","FF","Homo"]
    writer=csv.DictWriter(out,fieldnames=fields)
    writer.writeheader()
    for session in range(1,9):
        for game in range(1,5):
            for person in range(1,5):
                for rd in range(1,17):
                    homo=1 if session%2 else 0
                    token=50 if homo else 40 if person%2 else 60
                    writer.writerow({"ProfileID":f"FAKE_{session}_{game}_{person}",
                                     "GameID":game,"RoundID":rd,"Token":token,
                                     "Invest":10+(rd%7),"Session":session,
                                     "FF":0 if session<5 else 1,"Homo":homo})
    return out.getvalue().encode()


def parse_mock(raw,theory=THEORY):
    with patch.object(audit,"EXPECTED_BYTES",len(raw)),\
         patch.object(audit,"SOURCE_BLOB",audit.git_sha(raw)),\
         patch.object(audit,"THEORY_BLOB",audit.git_sha(theory)):
        return audit.parse_original_r047(raw,theory)


class ApplicabilityTests(unittest.TestCase):
    def test_git_blob_sha_empty(self):
        self.assertEqual(audit.git_sha(b""),"e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")

    def test_synthetic_2048_real_source_universe(self):
        data=parse_mock(sample_source())
        self.assertEqual(data["raw_experimental_rows"],2048)
        self.assertEqual(data["post_practice_rows"],1920)
        self.assertEqual(data["distinct_participants"],128)
        self.assertEqual(data["distinct_four_person_groups"],32)
        self.assertEqual(data["groups_with_three_or_more_distinct_postpractice_extractions"],32)
        self.assertEqual(data["fixed_R067_PD_e2_fit"],"BLOCKED_MODEL_MISMATCH")
        self.assertFalse(data["binary_recoding_undertaken"])
        self.assertNotIn("FAKE_1_1_1",str(data))

    def test_modified_source_hash_fails(self):
        original=sample_source()
        with patch.object(audit,"EXPECTED_BYTES",len(original)),\
             patch.object(audit,"SOURCE_BLOB",audit.git_sha(original)),\
             patch.object(audit,"THEORY_BLOB",audit.git_sha(THEORY)):
            with self.assertRaises(ValueError):
                audit.parse_original_r047(original.replace(b",10,",b",11,",1),THEORY)

    def test_source_nonblank_tail_fails(self):
        data=sample_source()+b"FAKE_NEW,1,1,40,20,1,0,0\n"
        with self.assertRaises(ValueError):
            parse_mock(data)

    def test_invalid_group_round_fails(self):
        raw=sample_source().replace(b",1,40,11,",b",17,40,11,",1)
        with self.assertRaises(ValueError):
            parse_mock(raw)

    def test_invalid_extraction_endowment_fails(self):
        raw=sample_source().replace(b",40,11,",b",40,99,",1)
        with self.assertRaises(ValueError):
            parse_mock(raw)

    def test_author_theory_code_changed_fails(self):
        with self.assertRaises(ValueError):
            parse_mock(sample_source(),b"# payoff model unavailable\n")

    def test_no_human_record_logging(self):
        result=parse_mock(sample_source())
        self.assertNotIn("ProfileID",str(result))
        self.assertEqual(result["source_mechanism"],
                         "CONTINUOUS_OR_MULTILEVEL_COMMON_POOL_EXTRACTION_WITH_NONLINEAR_SURPLUS_AND_SANCTION_CONDITIONS")

    def test_known_metadata_identity(self):
        class FakeResp:
            status=200
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def read(self,n):return json.dumps({"identifier":"doi:10.5061/dryad.37pvmcvmk",
                "versionNumber":1,"license":"CC0"}).encode()
        res=audit.dryad_catalog_probe(opener=lambda *args,**kwargs:FakeResp())
        self.assertEqual(res["catalog_status"],"PUBLIC_METADATA_MATCHES_DOI")
        self.assertFalse(res["raw_participant_files_read"])

    def test_unrelated_doi_cannot_be_assumed(self):
        class Resp:
            status=200
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def read(self,n):return b'{"identifier":"doi:10.0000/fake"}'
        self.assertEqual(audit.dryad_catalog_probe(opener=lambda *a,**kw:Resp())["catalog_status"],
                         "IDENTITY_UNRESOLVED")


if __name__=="__main__":
    unittest.main()
