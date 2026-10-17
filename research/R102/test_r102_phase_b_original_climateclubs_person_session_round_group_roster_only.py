"""R102 B synthetic 2700 source person/session/group/round rows, no human actions."""
import csv
import hashlib
import io
import unittest
from unittest.mock import patch
import r102_phase_b_original_climateclubs_person_session_round_group_roster_only as b
import r102_2025_original_climateclubs_zenodo_publisher_md5_header_only as a

def fake_csv(corrupt=None):
    o=io.StringIO(newline="")
    writer=csv.DictWriter(o,fieldnames=a.EXPECTED_HEADER,lineterminator="\n")
    writer.writeheader()
    record=0
    # Two synthetic independently recruited sessions, 90 subjects x 15 rounds.
    for session,tr in (("S1","T1"),("S2","T2")):
        for round_number in range(1,16):
            for person in range(1,91):
                record+=1
                index_group=(person-1)//6+1
                item={k:"NA" for k in a.EXPECTED_HEADER}
                item.update({
                    "session.code":session,
                    "participant.code":f"{session}person{person}",
                    "participant.id_in_session":str(person),
                    "participant._round_number":str(round_number),
                    "subsession.round_number":str(round_number),
                    "group.id_in_subsession":str(index_group),
                    "group":f"{index_group}A",
                    "player.id_in_group":str((person-1)%6+1),
                    "treatment":tr,
                })
                if corrupt is not None:
                    corrupt(item,record)
                writer.writerow(item)
    return o.getvalue().rstrip("\n").encode()

def audit(raw):
    with patch.object(a,"PUBLISHER_MD5",hashlib.md5(raw).hexdigest()), \
         patch.object(b,"PINNED_SHA256",hashlib.sha256(raw).hexdigest()):
        return b.parse_nonbehavior_roster(raw)

class RosterOnlySynthetic(unittest.TestCase):
    def test_complete_two_sessions(self):
        x=audit(fake_csv())
        self.assertEqual(x["original_actual_person_round_rows"],2700)
        self.assertEqual(x["original_session_count"],2)
        self.assertEqual(x["anonymous_source_person_per_session_count"],180)
        self.assertEqual(x["original_group_size_histogram"],{6:450})
        self.assertEqual(x["original_participant_codes_reused_across_sessions_count"],0)
        self.assertEqual(x["actual_human_model_scores"],0)
        self.assertEqual(x["real_human_contribution_values_dereferenced"],0)
    def test_source_ids_never_public(self):
        x=audit(fake_csv())
        self.assertNotIn("S1person1",repr(x))
        self.assertNotIn("1A",repr(x))
        self.assertFalse(x["raw_person_group_session_IDs_exported"])
    def test_duplicate_round_fails(self):
        def corrupt(item,i):
            if i==2:item["participant.code"]="S1person1";item["participant.id_in_session"]="1"
        self.assertRaises(b.SourceError,audit,fake_csv(corrupt))
    def test_participant_technical_round_mismatch_counted(self):
        def corrupt(item,i):
            if i==1:item["participant._round_number"]="2"
        x=audit(fake_csv(corrupt))
        self.assertEqual(x["technical_participant_round_disagrees_with_actual_subsession_round_rows"],1)
        self.assertEqual(x["actual_human_model_scores"],0)
    def test_invalid_participant_technical_round_still_rejected(self):
        def corrupt(item,i):
            if i==1:item["participant._round_number"]="BAD"
        self.assertRaises(b.SourceError,audit,fake_csv(corrupt))
    def test_position_reused_fails(self):
        def corrupt(item,i):
            if i==2:item["player.id_in_group"]="1"
        self.assertRaises(b.SourceError,audit,fake_csv(corrupt))
    def test_session_mixed_treatment_fails(self):
        def corrupt(item,i):
            if i==2:item["treatment"]="T2"
        self.assertRaises(b.SourceError,audit,fake_csv(corrupt))
    def test_missing_tag_fails(self):
        def corrupt(item,i):
            if i==1:item["session.code"]=""
        self.assertRaises(b.SourceError,audit,fake_csv(corrupt))
    def test_source_integer_not_numeric_fails(self):
        self.assertRaises(b.SourceError,b.natural_int,"NOTANINT")
    def test_untrusted_synthetic_unpinned_MD5_fails(self):
        self.assertRaises(a.SourceError,b.parse_nonbehavior_roster,fake_csv())
    def test_abandoned_source_person_identifier_count(self):
        # A person's session numeric ID must be stable through all rounds.
        def corrupt(item,i):
            if i==91:item["participant.id_in_session"]="999"
        self.assertRaises(b.SourceError,audit,fake_csv(corrupt))

if __name__=="__main__":
    unittest.main()
