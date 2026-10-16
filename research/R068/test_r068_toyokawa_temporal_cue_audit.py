"""Synthetic prior-round social cue accounting. No real participant records."""
import hashlib,unittest
from unittest.mock import patch
import r068_toyokawa_temporal_cue_audit as m
from r068_toyokawa_lfs_schema import FILE_SPEC


def row(person,room,rd,choice,cues,task="11"):
    return {"amazonID":person,"room":room,"round":str(rd),
            "riskDistributionId":task,"choice_num":str(choice),
            "payoff":"150",
            **dict(zip(m.CUES,map(str,cues)))}


def fixed_rows():
    # The original source frequency at t=2 INCLUDES the learner's t=1
    # choice 0. With the subtraction, there is just one peer choosing 1.
    return [
        row("PERSON_A","ROOM_A",1,0,[0,0,0,0]),
        row("PERSON_A","ROOM_A",2,1,[1,1,0,0]),
        row("PERSON_B","ROOM_A",1,1,[0,0,0,0]),
        row("PERSON_B","ROOM_A",2,0,[1,1,0,0]),
    ]

class TemporalRules(unittest.TestCase):
    def test_exact_previous_round_self_exclusion(self):
        q=m.audit_semantics(fixed_rows(),[])
        x=q["temporal_source_check_counts"]
        self.assertEqual(x["valid_author_self_excluded_nonnegative_frequencies"],2)
        self.assertEqual(x["at_least_one_observed_peer_choice"],2)
        self.assertEqual(q["semantic_gate"],"FOUR_CHOICE_PREVIOUS_TRIAL_CUES_RECOVERABLE")
        self.assertNotIn("PERSON_A",str(q))

    def test_negative_after_self_exclusion_detected(self):
        rows=fixed_rows()
        rows[1]["socialFreq_safe1"]="0"
        q=m.audit_semantics(rows,[])
        self.assertEqual(q["temporal_source_check_counts"]["negative_after_self_exclusion"],1)

    def test_missing_prior_does_not_fabricate_social_exposure(self):
        rows=fixed_rows()[1:]
        q=m.audit_semantics(rows,[])
        self.assertEqual(q["temporal_source_check_counts"]["missing_same_room_prior_self_choice"],1)

    def test_duplicate_person_round_blocks_semantic_gate(self):
        rows=fixed_rows()+[fixed_rows()[0]]
        q=m.audit_semantics(rows,[])
        self.assertEqual(q["duplicate_group_person_round_key_rows"],1)
        self.assertEqual(q["semantic_gate"],"SOURCE_TEMPORAL_MAPPING_BLOCKED")

    def test_cross_room_person_blocks_semantic_gate(self):
        rows=fixed_rows()
        rows[1]["room"]="ROOM_B"
        q=m.audit_semantics(rows,[])
        self.assertEqual(q["group_people_in_multiple_rooms"],1)
        self.assertEqual(q["semantic_gate"],"SOURCE_TEMPORAL_MAPPING_BLOCKED")

    def test_mixed_task_group_reported_but_not_silently_dropped(self):
        rows=fixed_rows()
        rows[2]["riskDistributionId"]="12"
        q=m.audit_semantics(rows,[])
        self.assertEqual(q["group_rooms_with_multiple_risk_distribution_codes"],1)
        self.assertEqual(q["group_rows_in_mixed_task_rooms"],4)

    def test_no_peer_exposure_not_fabricated_as_copy(self):
        rows=fixed_rows()
        rows[1]["socialFreq_safe2"]="0"   # all current peers absent
        q=m.audit_semantics(rows,[])
        x=q["temporal_source_check_counts"]
        self.assertEqual(x["zero_observed_peers"],1)

    def test_invalid_current_choice_is_not_rescored(self):
        rows=fixed_rows()
        rows[1]["choice_num"]="-1"
        q=m.audit_semantics(rows,[])
        self.assertEqual(q["temporal_source_check_counts"]["previous_or_current_choice_invalid"],1)

    def test_unparseable_frequency_never_zero_imputed(self):
        rows=fixed_rows()
        rows[1]["socialFreq_safe2"]="NA"
        q=m.audit_semantics(rows,[])
        self.assertEqual(q["temporal_source_check_counts"]["noninteger_or_missing_social_freq"],1)

    def test_numeric_normalization_strict(self):
        self.assertIsNone(m.maybe_int("1.5"))
        self.assertEqual(m.maybe_int("1.0"),1)
        self.assertIsNone(m.maybe_int("inf"))

    def test_full_source_hash_must_match(self):
        data=b"amazonID,room,round\nSECRET_A,1,1\n"
        spec={"size":len(data),"sha256":hashlib.sha256(data).hexdigest()}
        with patch.object(m,"FILE_SPEC",{"toy.csv":spec}):
            with self.assertRaises(ValueError):
                m.parse_source("toy.csv",data+b"bad")

    def test_individual_data_never_interpreted_as_peer_network(self):
        rows=fixed_rows()
        indiv=[row("PRIVATE_X","ROOM_C",1,0,[0,0,0,0])]
        q=m.audit_semantics(rows,indiv)
        self.assertEqual(q["individual_distinct_anonymous_people"],1)
        self.assertNotIn("PRIVATE_X",str(q))
        self.assertFalse(q["trial_level_observed_demonstrator_payoffs_provided_to_learners"])

if __name__=="__main__":
    unittest.main()
