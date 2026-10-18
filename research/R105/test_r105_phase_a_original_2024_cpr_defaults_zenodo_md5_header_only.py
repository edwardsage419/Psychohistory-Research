"""R105 A synthetic-only source URL / full published MD5 / CSV header tests."""
import hashlib
import unittest
from unittest.mock import patch
import r105_phase_a_original_2024_cpr_defaults_zenodo_md5_header_only as s

def simulated_source(lines=50, ending=True, header="participant_id,group,round_number,extraction"):
    raw=(header+"\n")+("SYNTHETIC_FAKE_ID,SYNTHETIC_FAKE_GROUP,1,20\n"*lines)
    return (raw if ending else raw[:-1]).encode("utf-8")
def audited(raw):
    with patch.object(s,"PUBLISHED_MD5",hashlib.md5(raw).hexdigest()):
        return s.source_header_only(raw)

class OriginalMD5HeaderTests(unittest.TestCase):
    def test_exact_author_zenodo_url(self):s.validate_url(s.SOURCE_URL)
    def test_fake_record_rejected(self):
        self.assertRaises(s.SourceGateError,s.validate_url,s.SOURCE_URL.replace("10818840","10228658"))
    def test_evil_host_rejected(self):
        self.assertRaises(s.SourceGateError,s.validate_url,s.SOURCE_URL.replace("zenodo.org","files.example"))
    def test_query_extra_rejected(self):
        self.assertRaises(s.SourceGateError,s.validate_url,s.SOURCE_URL+"&token=secrets")
    def test_unauthentic_md5_blocked(self):
        self.assertRaises(s.SourceGateError,s.source_header_only,simulated_source())
    def test_only_header_interpreted(self):
        result=audited(simulated_source())
        self.assertEqual(result["physical_original_data_row_lines_unparsed"],50)
        self.assertEqual(result["original_csv_header_field_count"],4)
        self.assertFalse(result["any_original_human_choice_value_read"])
        self.assertFalse(result["any_original_person_or_group_identifier_cell_read"])
        self.assertEqual(result["actual_human_predictions_scored"],0)
        self.assertNotIn("SYNTHETIC_FAKE_ID",str(result))
    def test_unterminated_final_row_counts(self):
        result=audited(simulated_source(ending=False))
        self.assertEqual(result["physical_original_data_row_lines_unparsed"],50)
    def test_duplicate_header_refused(self):
        self.assertRaises(s.SourceGateError,audited,simulated_source(header="id,id,round,contrib"))
    def test_malicious_header_refused(self):
        self.assertRaises(s.SourceGateError,audited,simulated_source(header="participant,../../etc,round,contrib"))
    def test_binary_refused(self):
        self.assertRaises(s.SourceGateError,audited,simulated_source()+b"\x00")
    def test_html_refused(self):
        bad=(b"<html><body>server refused</body></html>"*10)
        self.assertRaises(s.SourceGateError,audited,bad)
    def test_oversized_source_refused(self):
        self.assertRaises(s.SourceGateError,s.source_header_only,b"X"*(s.CAP+1))

if __name__=="__main__":
    unittest.main()
