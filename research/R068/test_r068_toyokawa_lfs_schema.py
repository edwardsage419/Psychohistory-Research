"""Synthetic-only pinned LFS pointers and human-table privacy/structural gates."""
import hashlib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import r068_toyokawa_lfs_schema as m


def fake_payload(name="choice"):
    return f"participant,{name},social_frequency\nSECRET_A,A,0.75\nSECRET_B,B,0.25\n".encode()


class LFSContracts(unittest.TestCase):
    def test_exact_pointer_contract(self):
        raw=b"version https://git-lfs.github.com/spec/v1\noid sha256:abc\nsize 10\n"
        self.assertTrue(m.pointer_contract(raw,"abc",10))
        self.assertFalse(m.pointer_contract(raw,"abc",11))

    def test_git_blob_hash_empty_known(self):
        self.assertEqual(m.git_blob_sha(b""),"e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")

    def test_safe_columns_no_rows(self):
        result=m.audit_csv(fake_payload())
        self.assertEqual(result["data_rows"],2)
        self.assertIn("social_frequency",result["candidate_measurement_field_names"])
        self.assertNotIn("SECRET_A",str(result))
        self.assertFalse(result["per_person_values_exported"])

    def test_original_lfs_pointer_rejected_as_data(self):
        with self.assertRaisesRegex(ValueError,"LFS_POINTER"):
            m.audit_csv(b"version https://git-lfs.github.com/spec/v1\noid sha256:x\nsize 100\n")

    def test_duplicate_columns_rejected(self):
        with self.assertRaisesRegex(ValueError,"DUPLICATE"):
            m.audit_csv(b"choice,choice\nA,B\nB,A\n")

    def test_ragged_rows_rejected(self):
        with self.assertRaisesRegex(ValueError,"RAGGED"):
            m.audit_csv(b"choice,other\nA\nB,x\n")

    def test_non_utf8_rejected(self):
        with self.assertRaises(UnicodeDecodeError):
            m.audit_csv(b"choice\n\xff\nA\n")

    def test_file_length_rejected(self):
        with patch.object(m,"MAX_BYTES",2):
            with self.assertRaisesRegex(ValueError,"FILE_TOO_LARGE"):
                m.audit_csv(fake_payload())

    def test_short_file_rejected(self):
        with self.assertRaisesRegex(ValueError,"NO_BEHAVIORAL"):
            m.audit_csv(b"a,b\n1,2\n")

    def test_header_redacted(self):
        res=m.audit_csv(b"person@example.com,choice\nA,1\nB,0\n")
        self.assertEqual(res["safe_field_names"][0],"[NONSTANDARD_HEADER_REDACTED]")

    def test_source_payload_mismatch_not_claimed(self):
        a=fake_payload()
        fake_spec={"dummy.csv":{"size":len(a),"sha256":hashlib.sha256(a).hexdigest(),
                                "pointer_blob":"notmatch"}}
        with TemporaryDirectory() as d,patch.object(m,"FILE_SPEC",fake_spec):
            (Path(d)/"dummy.csv").write_bytes(a+b"corrupted")
            with self.assertRaisesRegex(ValueError,"PAYLOAD_SHA"):
                m.audit_pinned_source(Path(d))

    def test_source_pointer_bitflip_detected(self):
        raw=fake_payload()
        oid=hashlib.sha256(raw).hexdigest()
        ptr=f"version https://git-lfs.github.com/spec/v1\noid sha256:{oid}\nsize {len(raw)}\n".encode()
        spec={"dummy.csv":{"size":len(raw),"sha256":oid,"pointer_blob":m.git_blob_sha(ptr)}}
        with TemporaryDirectory() as d,TemporaryDirectory() as p,patch.object(m,"FILE_SPEC",spec):
            (Path(d)/"dummy.csv").write_bytes(raw)
            (Path(p)/"dummy.csv").write_bytes(ptr[:-1]+b"X")
            with self.assertRaisesRegex(ValueError,"POINTER_OID_OR_BLOB"):
                m.audit_pinned_source(Path(d),Path(p))

    def test_positive_complete_synthetic_source(self):
        raw=fake_payload()
        oid=hashlib.sha256(raw).hexdigest()
        ptr=f"version https://git-lfs.github.com/spec/v1\noid sha256:{oid}\nsize {len(raw)}\n".encode()
        spec={"dummy.csv":{"size":len(raw),"sha256":oid,"pointer_blob":m.git_blob_sha(ptr)}}
        with TemporaryDirectory() as d,TemporaryDirectory() as p,patch.object(m,"FILE_SPEC",spec):
            (Path(d)/"dummy.csv").write_bytes(raw)
            (Path(p)/"dummy.csv").write_bytes(ptr)
            out=m.audit_pinned_source(Path(d),Path(p))
        self.assertEqual(out["status"],"SOURCE_SHA_AND_SCHEMA_PASS")
        self.assertFalse(out["actual_demonstrator_payoff_per_trial_verified"])
        self.assertEqual(out["e2_exact_three_demonstrator_majority_model_identification"],"OPEN")


if __name__=="__main__":
    unittest.main()
