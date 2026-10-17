#!/usr/bin/env python3
import csv,hashlib,io,sys,pathlib,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r095_schniter_shields_2020_original_session_roster_no_actions import (
 URL,REC,PUBLISHER_MD5,MAX_FILE,check_source_url,verify_source_bytes,decode_original_metadata)
HEADER=["ID","round","option","session","group","other_split","optionAfraid"]
def fixture(sessions=3,third=False):
 b=io.StringIO();w=csv.writer(b);w.writerow(HEADER)
 for ss in range(sessions):
  for group in range(2):
   for person in range(2):
    for t in ((1,2,3) if third and ss==1 else (1,2)):
     w.writerow([f"PRIVATE_SOURCE_PERSON_{ss}_{group}_{person}",t,
                 "SENSITIVE ORIGINAL CHOICE","TRUE_SESSION_"+str(ss),
                 str(group+1),"SENSITIVE OTHER CHOICE",99])
 return b.getvalue().encode()
class SourceAuthentication(unittest.TestCase):
 def test_record(self):self.assertEqual(REC,"4321821")
 def test_author_official_md5(self):self.assertEqual(PUBLISHER_MD5,"4c30ac1861e12f46e0b9847c9d1857a7")
 def test_url_good(self):self.assertTrue(check_source_url(URL))
 def test_url_bad_host(self):
  with self.assertRaises(ValueError):check_source_url(URL.replace("zenodo.org","zenodo.org.evil"))
 def test_url_bad_record(self):
  with self.assertRaises(ValueError):check_source_url(URL.replace(REC,"1"))
 def test_url_bad_file(self):
  with self.assertRaises(ValueError):check_source_url(URL.replace("Fields.csv","Media.csv"))
 def test_reject_empty(self):
  with self.assertRaises(ValueError):verify_source_bytes(b"",hashlib.md5(b"").hexdigest())
 def test_reject_bad_md5(self):
  with self.assertRaises(ValueError):verify_source_bytes(fixture())
 def test_strict_cap(self):
  b=b"b"*(MAX_FILE+1)
  with self.assertRaises(ValueError):verify_source_bytes(b,hashlib.md5(b).hexdigest())
 def test_whole_file_sha(self):
  b=fixture();v=verify_source_bytes(b,hashlib.md5(b).hexdigest())
  self.assertEqual(v["original_full_file_SHA256"],hashlib.sha256(b).hexdigest())
class ActualGroupUniverse(unittest.TestCase):
 def test_three_sessions(self):
  v=decode_original_metadata(fixture())
  self.assertEqual(v["source_distinct_explicit_true_session_IDs"],3)
 def test_12_people_24_rows(self):
  v=decode_original_metadata(fixture())
  self.assertEqual(v["source_unique_original_real_participants"],12)
  self.assertEqual(v["source_total_original_actor_round_records"],24)
 def test_fixed_matched_6_pairs(self):
  self.assertEqual(decode_original_metadata(fixture())["source_matched_original_two_person_pairs"],6)
 def test_round_three_all_two_person_complete(self):
  v=decode_original_metadata(fixture(third=True))
  self.assertEqual(v["anonymous_original_round_1_2_3_actor_record_counts"]["3"],4)
 def test_subject_private_no_output(self):
  z=str(decode_original_metadata(fixture()))
  for k in ("PRIVATE_SOURCE_PERSON","TRUE_SESSION","SENSITIVE","99"):
   self.assertNotIn(k,z)
 def test_any_original_human_option_not_inspected(self):
  self.assertTrue(decode_original_metadata(fixture())["no_original_actor_option_or_partner_action_values_inspected"])
 def test_session_fewer_than_3_denied(self):
  with self.assertRaises(ValueError):decode_original_metadata(fixture(sessions=2))
 def test_duplicate_actor_round_denied(self):
  v=list(csv.reader(io.StringIO(fixture().decode())))
  v[2][1]=v[1][1]
  b=io.StringIO();csv.writer(b).writerows(v)
  with self.assertRaises(ValueError):decode_original_metadata(b.getvalue().encode())
 def test_missing_two_round_denied(self):
  v=list(csv.reader(io.StringIO(fixture().decode())))
  del v[2]
  b=io.StringIO();csv.writer(b).writerows(v)
  with self.assertRaises(ValueError):decode_original_metadata(b.getvalue().encode())
 def test_invalid_round_denied(self):
  v=list(csv.reader(io.StringIO(fixture().decode())))
  v[1][1]="7"
  b=io.StringIO();csv.writer(b).writerows(v)
  with self.assertRaises(ValueError):decode_original_metadata(b.getvalue().encode())
 def test_partner_group_changes_denied(self):
  v=list(csv.reader(io.StringIO(fixture().decode())))
  v[2][4]="90"
  b=io.StringIO();csv.writer(b).writerows(v)
  with self.assertRaises(ValueError):decode_original_metadata(b.getvalue().encode())
 def test_session_identity_switch_denied(self):
  v=list(csv.reader(io.StringIO(fixture().decode())))
  v[2][3]="DIFFERENT"
  b=io.StringIO();csv.writer(b).writerows(v)
  with self.assertRaises(ValueError):decode_original_metadata(b.getvalue().encode())
 def test_incomplete_optional_third_round_denied(self):
  v=list(csv.reader(io.StringIO(fixture(third=True).decode())))
  ix=next(j for j in range(1,len(v)) if v[j][1]=="3")
  del v[ix]
  b=io.StringIO();csv.writer(b).writerows(v)
  with self.assertRaises(ValueError):decode_original_metadata(b.getvalue().encode())
 def test_source_invalid_header_denied(self):
  with self.assertRaises(ValueError):decode_original_metadata(fixture().replace(b"ID,round",b"PERSON,round",1))
 def test_unexpected_extra_tab_denied(self):
  with self.assertRaises(ValueError):decode_original_metadata(fixture()+b"junk\n")
if __name__=="__main__":unittest.main()
