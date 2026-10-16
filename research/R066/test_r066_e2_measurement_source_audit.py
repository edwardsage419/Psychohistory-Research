"""R066 source/measurement screening tests use synthetic invented inputs ONLY."""
import bz2
import tempfile
import unittest
from pathlib import Path

from r066_e2_measurement_source_audit import (
    audit_reddit_file, audit_annotated_opinions, git_blob_sha1, verify_blob
)


class MeasurementAuditTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.p = Path(self.dir.name)

    def tearDown(self):
        self.dir.cleanup()

    def mk(self, name, content):
        dest=self.p/name
        dest.write_bytes(content)
        return dest, git_blob_sha1(content), len(content)

    def test_git_blob_has_exact_known_empty_sha(self):
        self.assertEqual(git_blob_sha1(b""),"e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")

    def test_tamper_reject(self):
        file,sha,n=self.mk("toy.txt",b"valid")
        file.write_bytes(b"alter")
        with self.assertRaises(ValueError):
            verify_blob(file,sha,n)

    def test_length_reject(self):
        file,sha,n=self.mk("toy.txt",b"valid")
        with self.assertRaises(ValueError):
            verify_blob(file,sha,n+1)

    def test_valid_reddit_edge_structure(self):
        raw=b"200801\tfakeA\tfakeB\t2\n200802\tfakeB\tfakeA\t3\n"
        file,sha,n=self.mk("edges.tsv.bz2",bz2.compress(raw))
        result=audit_reddit_file(file,sha,n,("yearmonth","parent","author","count"))
        self.assertEqual(result["rows"],2)
        self.assertEqual(result["distinct_months"],2)
        self.assertEqual(result["aggregate_edge_weight"],5)
        self.assertNotIn("fakeA",str(result))

    def test_valid_scores_header(self):
        raw=b"yearmonth\tuser\tscore\n200801\tfakeA\t10\n"
        file,sha,n=self.mk("score.tsv.bz2",bz2.compress(raw))
        result=audit_reddit_file(file,sha,n,None)
        self.assertEqual(result["columns"],["yearmonth","user","score"])
        self.assertTrue(result["header_exists"])

    def test_malformed_compressed_file_fails(self):
        file,sha,n=self.mk("invalid.bz2",b"not a bz2 stream")
        with self.assertRaises(OSError):
            audit_reddit_file(file,sha,n,("yearmonth","parent","author","count"))

    def test_reddit_bad_edge_fields_fails(self):
        raw=b"200801\tfakeA\tfakeB\t0\n"
        file,sha,n=self.mk("invalid.bz2",bz2.compress(raw))
        with self.assertRaises(ValueError):
            audit_reddit_file(file,sha,n,("yearmonth","parent","author","count"))

    def test_reddit_wrong_column_count_fails(self):
        raw=b"200801\tfakeA\t2\n"
        file,sha,n=self.mk("invalid.bz2",bz2.compress(raw))
        with self.assertRaises(ValueError):
            audit_reddit_file(file,sha,n,("yearmonth","parent","author","count"))

    def test_b_annotated_opinion_measurement_status(self):
        raw=(b"user_id\topinion\ttime\n"
             b"privateA\t1\t0\nprivateB\t0\t1\nprivateA\t0\t2\n")
        file,sha,n=self.mk("opinion.tsv",raw)
        result=audit_annotated_opinions(file,sha,n)
        self.assertEqual(result["rows"],3)
        self.assertEqual(result["distinct_users"],2)
        self.assertEqual(result["participants_with_two_or_more_distinct_times"],1)
        self.assertEqual(result["opinion_label_counts"],{"0.0":2,"1.0":1})
        self.assertNotIn("privateA",str(result))
        self.assertIn("BLOCKED",result["three_model_identification"])

    def test_annotated_missing_header_fail(self):
        raw=b"id\tlabel\tdate\n0\t1\t2\n"
        file,sha,n=self.mk("invalid.tsv",raw)
        with self.assertRaises(ValueError):
            audit_annotated_opinions(file,sha,n)

    def test_annotated_nonfinite_fail(self):
        raw=b"user_id\topinion\ttime\nX\tnan\t0\n"
        file,sha,n=self.mk("invalid.tsv",raw)
        with self.assertRaises(ValueError):
            audit_annotated_opinions(file,sha,n)

    def test_annotated_time_inversions_fail(self):
        raw=b"user_id\topinion\ttime\nX\t1\t2\nY\t1\t1\n"
        file,sha,n=self.mk("invalid.tsv",raw)
        with self.assertRaises(ValueError):
            audit_annotated_opinions(file,sha,n)

    def test_annotated_bad_column_count_fail(self):
        raw=b"user_id\topinion\ttime\nX\t1\t2\ttoo_many\n"
        file,sha,n=self.mk("invalid.tsv",raw)
        with self.assertRaises(ValueError):
            audit_annotated_opinions(file,sha,n)


if __name__=="__main__":
    unittest.main()
