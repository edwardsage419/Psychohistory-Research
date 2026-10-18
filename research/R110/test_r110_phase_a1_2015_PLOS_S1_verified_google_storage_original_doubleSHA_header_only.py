"""R110 A1 pure publisher source delivery one-hop SHA header-only synthetics."""
import unittest,urllib.request
import r110_phase_a1_2015_PLOS_S1_verified_google_storage_original_doubleSHA_header_only as a
from r110_phase_a0_2015_bone_UCL_PLOS_s1_original_CSV_delivery_no_body import URL,SourceError

def fixture(header="lab,actor,peer,period,choice"):
    return (header+"\n"+("PRIVATE_SESSION,PRIVATE_ACTOR,PRIVATE_PEER,PRIVATE_ROUND,PRIVATE_ACTION\n"*250)).encode("utf-8")
def redirected(destination):
    return a.SinglePublisherDelegation().redirect_request(
        urllib.request.Request(URL),None,302,"Found",{},destination)

class GenuinePublisherSourceGates(unittest.TestCase):
    def test_A0_verified_google_storage_exact(self):
        self.assertTrue(a.delegated_final("https://storage.googleapis.com/plos-journal/PRIVATE?Expires=1&Signature=PRIVATE"))
    def test_google_host_suffix_spoof_denied(self):
        self.assertRaises(SourceError,a.delegated_final,"https://storage.googleapis.com.bad.example/private")
    def test_unrelated_bucket_denied(self):
        self.assertRaises(SourceError,a.delegated_final,"https://untrusted-storage.com/other")
    def test_http_downgrade_denied(self):
        self.assertRaises(SourceError,a.delegated_final,"http://storage.googleapis.com/unsafe")
    def test_user_credentials_denied(self):
        self.assertRaises(SourceError,a.delegated_final,"https://p:q@storage.googleapis.com/private")
    def test_redirect_fragment_denied(self):
        self.assertRaises(SourceError,a.delegated_final,"https://storage.googleapis.com/a#token")
    def test_wrong_port_denied(self):
        self.assertRaises(SourceError,a.delegated_final,"https://storage.googleapis.com:404/object")
    def test_true_firstparty_only_single_redirect(self):
        r=redirected("https://storage.googleapis.com/official/object?PRIVATE_SIGNATURE=value")
        self.assertEqual(r.get_method(),"GET")
        self.assertRaises(SourceError,a.SinglePublisherDelegation().redirect_request,
            urllib.request.Request("https://storage.googleapis.com/first"),None,
            302,"Found",{},"https://storage.googleapis.com/second")
    def test_generated_realistic_csv_SHA_header_only(self):
        x=a.authenticate_header_and_whole_SHA(fixture())
        self.assertEqual(x["source_S1_first_CSV_header_column_count"],5)
        self.assertGreater(x["source_physical_CSV_data_lines_no_behavior_values_read"],0)
        self.assertFalse(x["original_CSV_actor_pair_action_or_round_value_accessed"])
        self.assertNotIn("PRIVATE_ACTOR",repr(x))
        self.assertFalse(x["publisher_MD5_independently_published_and_verified"])
    def test_two_realistic_bytes_original_replay(self):
        x=a.two_independent_full_sources(fixture(),fixture())
        self.assertTrue(x["two_separate_official_PLOS_S1_downloads_byte_identical"])
    def test_double_download_mismatch_fails(self):
        b=fixture();other=b.replace(b"PRIVATE_PEER",b"PRIVATE_PEEX")
        self.assertRaises(SourceError,a.two_independent_full_sources,b,other)
    def test_html_source_denied(self):
        self.assertRaises(SourceError,a.authenticate_header_and_whole_SHA,b"<html>Forbidden</html>\n"*1200)
    def test_original_source_oversize_denied(self):
        self.assertRaises(SourceError,a.authenticate_header_and_whole_SHA,b"x"*(a.CAP+1))
    def test_undersized_body_denied(self):
        self.assertRaises(SourceError,a.authenticate_header_and_whole_SHA,b"a,b\nx,y\n")
    def test_header_blank_and_duplicate_only_numbers(self):
        x=a.authenticate_header_and_whole_SHA(fixture("alpha,alpha,,c,d"))
        self.assertEqual(x["source_header_blank_column_count"],1)
        self.assertEqual(x["source_header_duplicate_column_count"],1)
        self.assertNotIn("PRIVATE_ACTION",str(x))
    def test_unicode_header_class_count(self):
        x=a.authenticate_header_and_whole_SHA(fixture("actör,actor,peer,round,choice"))
        self.assertEqual(x["source_header_nonASCII_or_control_name_count"],1)

if __name__=="__main__":unittest.main()
