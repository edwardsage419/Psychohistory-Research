#!/usr/bin/env python3
import csv,hashlib,io,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r096_phase_b_montero_author_git_tag_pinned_original_FP_SP_CSV_source import (
 AUTHOR,REPO,COMMIT,FILES,CAP,raw_url,validate_raw_url,
 git_blob,verify_author_blob,safe_original_csv_schema)
def fake(n=1001):
 s=io.StringIO();w=csv.writer(s);w.writerow(["session","person","round","action"])
 for t in range(n):w.writerow(["PRIVATE_SESSION","PRIVATE_ACTOR",t,"VERY_SECRET_CHOICE"])
 return s.getvalue().encode()
class AuthorTagSynthetic(unittest.TestCase):
 def test_author_fixed(self):self.assertEqual(AUTHOR,"eladiomontero")
 def test_commit_fixed(self):self.assertEqual(COMMIT,"4743f74d8a03a031b8f70aff64956f8ad5155182")
 def test_repository_name(self):self.assertEqual(REPO,"PairwiseStrategies")
 def test_fix_tree_sha(self):self.assertEqual(FILES["fix.csv"]["blob"],"3bf78bf85f6642afee18d6f1965dca7272582f40")
 def test_rand_tree_sha(self):self.assertEqual(FILES["rand.csv"]["blob"],"f5a86cd033b739da45d3fc7c5019068f612146a2")
 def test_url_valid(self):
  for k in FILES:self.assertTrue(validate_raw_url(raw_url(k),k))
 def test_url_wrong_tag_rejected(self):
  with self.assertRaises(ValueError):validate_raw_url(raw_url("fix.csv").replace(COMMIT,"main"),"fix.csv")
 def test_url_other_host_rejected(self):
  with self.assertRaises(ValueError):validate_raw_url(raw_url("fix.csv").replace("githubusercontent.com","githubusercontent.com.evil"),"fix.csv")
 def test_url_HTTP_rejected(self):
  with self.assertRaises(ValueError):validate_raw_url(raw_url("fix.csv").replace("https","http",1),"fix.csv")
 def test_unpinned_file_rejected(self):
  with self.assertRaises(ValueError):raw_url("other.csv")
 def test_git_blob_formula(self):
  b=b"1234";self.assertEqual(git_blob(b),hashlib.sha1(b"blob 4\0"+b).hexdigest())
 def test_length_mismatch_denied(self):
  with self.assertRaises(ValueError):verify_author_blob(fake(),"fix.csv")
 def test_csv_rows_count(self):
  v=safe_original_csv_schema(fake());self.assertEqual(v["original_author_source_actor_action_row_count_NOT_YET_VALIDATED"],1001)
 def test_column_names_only(self):
  v=safe_original_csv_schema(fake());self.assertEqual(v["original_author_published_CSV_safe_headers_only"],["session","person","round","action"])
 def test_no_human_value_printed(self):
  s=str(safe_original_csv_schema(fake()))
  for word in ("PRIVATE_SESSION","PRIVATE_ACTOR","VERY_SECRET_CHOICE"):self.assertNotIn(word,s)
 def test_not_read_action_flag(self):
  self.assertFalse(safe_original_csv_schema(fake())["original_human_action_values_or_round_person_session_values_ever_examined"])
 def test_bad_utf8(self):
  with self.assertRaises(ValueError):safe_original_csv_schema(b"\xff\x00")
 def test_unsafe_column(self):
  with self.assertRaises(ValueError):safe_original_csv_schema(fake().replace(b"person",b"actor@example.com",1))
 def test_duplicate_column(self):
  with self.assertRaises(ValueError):safe_original_csv_schema(fake().replace(b"person",b"session",1))
 def test_too_few_data_rows(self):
  with self.assertRaises(ValueError):safe_original_csv_schema(fake(3))
 def test_broken_rowwidth(self):
  with self.assertRaises(ValueError):safe_original_csv_schema(fake()+b"broken,row\n")
 def test_unnamed_pandas_export_first_column(self):
  b=fake().replace(b"session,person,round,action",b",session,person,round,action",1)
  # Keep the entire original source row width unchanged by adding empty index cell.
  rows=b.decode().splitlines()
  b=(rows[0]+"\n"+"\n".join(","+x for x in rows[1:])+"\n").encode()
  m=safe_original_csv_schema(b)
  self.assertEqual(m["unnamed_export_index_source_columns"],1)
  self.assertEqual(m["original_author_published_CSV_safe_headers_only"][0],"__UNNAMED_INDEX_0__")
 def test_author_export_unnamed_named_pandas_columns(self):
  b=fake().replace(b"session,person,round,action",b",Unnamed: 0,round,action",1)
  rows=b.decode().splitlines()
  b=(rows[0]+"\n"+"\n".join(","+x for x in rows[1:])+"\n").encode()
  m=safe_original_csv_schema(b)
  self.assertEqual(m["unnamed_export_index_source_columns"],1)
  self.assertIn("Unnamed: 0",m["original_author_published_CSV_safe_headers_only"])
 def test_duplicate_unnamed_pandas_index_still_distinct_safe_names(self):
  b=fake().replace(b"session,person,round,action",b",,round,action",1)
  m=safe_original_csv_schema(b)
  self.assertEqual(m["unnamed_export_index_source_columns"],2)
  self.assertNotEqual(m["original_author_published_CSV_safe_headers_only"][0],m["original_author_published_CSV_safe_headers_only"][1])
 def test_original_leading_blank_line_accepted(self):
  m=safe_original_csv_schema(b"\n"+fake())
  self.assertEqual(m["empty_csv_lines_before_header"],1)
 def test_original_many_leading_blank_lines_denied(self):
  with self.assertRaises(ValueError):safe_original_csv_schema(b"\n"*6+fake())
 def test_after_unnamed_schema_no_secret_source_actor_value_leaks(self):
  b=fake().replace(b"session,person,round,action",b",session,round,action",1)
  s=str(safe_original_csv_schema(b))
  self.assertNotIn("PRIVATE_ACTOR",s)
  self.assertNotIn("VERY_SECRET_CHOICE",s)
if __name__=="__main__":unittest.main()
