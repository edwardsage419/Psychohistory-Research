"""R102 C pure synthetic all-source replay for frozen 8-session LOSO M0/M1/M2/M3.

All human-style records are generated in memory. No original participant data.
"""
from __future__ import annotations
import csv
import hashlib
import io
import unittest
from unittest.mock import patch

import r102_2025_original_climateclubs_zenodo_publisher_md5_header_only as a
import r102_phase_b_original_climateclubs_person_session_round_group_roster_only as b
import r102_phase_c_2025_original_8sessions_2520_own_peers_M0123_LOSO as c


SESSIONS=(24,24,24,24,24,24,18,18)


def fixture(*, peer_rule=False, auto_rule=False, edit=None):
    """Eight real-style sessions, 180 fake people, 450 six-person groups, 15 rounds."""
    output=io.StringIO(newline="")
    writer=csv.DictWriter(output,fieldnames=a.EXPECTED_HEADER,lineterminator="\n")
    writer.writeheader()
    n=0
    for si,count in enumerate(SESSIONS,1):
        session=f"S{si}"
        treatment=f"T{(si+1)//2}"
        previous={}
        for rnd in range(1,16):
            current={}
            for pid in range(1,count+1):
                if not peer_rule:
                    # Stable private type: own history is exactly predictive.
                    share=(pid%5)/10.0
                elif rnd==1:
                    share=(pid%5)/10.0
                else:
                    group_start=((pid-1)//6)*6+1
                    fellows=[p for p in range(group_start,group_start+6) if p!=pid]
                    share=sum(previous[p] for p in fellows)/5.0
                current[pid]=share
                val={key:"NA" for key in a.EXPECTED_HEADER}
                val.update({
                    "session.code":session,
                    "treatment":treatment,
                    "participant.code":f"{session}Person{pid}",
                    "participant.id_in_session":str(pid),
                    "participant._round_number":"15",
                    "subsession.round_number":str(rnd),
                    "group.id_in_subsession":str((pid-1)//6+1),
                    "group":f"G{(pid-1)//6+1}",
                    "player.id_in_group":str((pid-1)%6+1),
                    "player.endowment":"10",
                    "player.contribution":format(share*10,".14g"),
                    "player.automatic_decision":("1" if auto_rule and si==1 and rnd==2 and pid==1 else "0"),
                })
                n+=1
                if edit is not None:
                    edit(val,n,si,rnd,pid)
                writer.writerow(val)
            previous=current
    return output.getvalue().rstrip("\n").encode("utf-8")


def audited(blob):
    """Temporarily substitute checksum anchors for synthetic source only."""
    digest=hashlib.sha256(blob).hexdigest()
    with patch.object(a,"PUBLISHER_MD5",hashlib.md5(blob).hexdigest()), \
         patch.object(b,"PINNED_SHA256",digest), \
         patch.object(c,"PINNED_SHA256",digest):
        return c.real_source_score(blob)


class R102FrozenCModelsSynthetic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.constant=fixture()

    def test_source_8sessions_2520_same_targets(self):
        output=audited(self.constant)
        self.assertEqual(output["status"],"R102_REAL_ORIGINAL_8SESSION_2520_HELDOUT_M0_M1_M2_M3_E2")
        self.assertEqual(output["actual_original_person_round_rows"],2700)
        self.assertEqual(output["actual_same_target_original_next_actor_rounds"],2520)
        self.assertEqual(output["verified_true_original_sessions"],8)
        self.assertEqual(output["verified_source_people"],180)
        self.assertEqual(len(output["anonymous_original_session_results"]),8)
        self.assertEqual(output["all_recorded"]["target_count"],2520)
        self.assertEqual(output["PESEN_v0_1"],"FROZEN")

    def test_exclusively_self_predictive_fixture_retains_peer_negative(self):
        output=audited(self.constant)
        self.assertAlmostEqual(output["all_recorded"]["MSE"]["M1"],0,places=22)
        self.assertGreater(output["all_recorded"]["MSE"]["M3"],0)
        self.assertLess(output["all_recorded"]["gains"]["M3_vs_M1"],0)
        self.assertEqual(output["session_effect_direction_counts"]["M3_vs_M1"]["negative_sessions"],8)

    def test_peer_generating_fixture_recovered_by_peer_only(self):
        output=audited(fixture(peer_rule=True))
        self.assertLess(output["all_recorded"]["MSE"]["M2"],1e-20)
        self.assertGreater(output["all_recorded"]["gains"]["M3_vs_M1"],0)
        self.assertEqual(output["session_effect_direction_counts"]["M3_vs_M1"]["positive_sessions"],8)

    def test_four_models_use_identical_frozen_2520_targets(self):
        output=audited(self.constant)
        self.assertEqual(set(output["all_recorded"]["MSE"]),{"M0","M1","M2","M3"})
        self.assertEqual(set(output["all_recorded"]["gains"]),
                         {"M1_vs_M0","M2_vs_M0","M3_vs_M1","M3_vs_M0"})
        self.assertEqual(sum(s["all_recorded"]["target_count"] for s in output["anonymous_original_session_results"]),2520)
        self.assertEqual(output["early_t2_to_t5"]["target_count"],180*4)
        self.assertEqual(output["later_t6_to_t15"]["target_count"],180*10)

    def test_automatic_target_subgroup_only_same_predictions(self):
        output=audited(fixture(auto_rule=True))
        self.assertEqual(output["original_automatic_target_count"],1)
        self.assertEqual(output["manual_target_only"]["target_count"],2519)
        self.assertEqual(output["all_recorded"]["target_count"],2520)

    def test_original_human_identity_not_republished(self):
        output=audited(self.constant)
        printed=repr(output)
        self.assertNotIn("S1Person1",printed)
        self.assertNotIn("S8Person18",printed)
        self.assertNotIn("G1",printed)
        self.assertTrue(output["original_human_ID_or_action_rows_exported"] is False)
        self.assertTrue(output["not_R073_exact_dyadic_opponent_contract"])

    def test_zero_endowment_fails(self):
        def edit(row,n,si,t,p):
            if n==1:
                row["player.endowment"]="0"
        with self.assertRaises(c.SourceError):
            audited(fixture(edit=edit))

    def test_contribution_over_endowment_fails(self):
        def edit(row,n,si,t,p):
            if n==1:
                row["player.contribution"]="11"
        with self.assertRaises(c.SourceError):
            audited(fixture(edit=edit))

    def test_nonfinite_contribution_fails(self):
        def edit(row,n,si,t,p):
            if n==1:
                row["player.contribution"]="NaN"
        with self.assertRaises(c.SourceError):
            audited(fixture(edit=edit))

    def test_invalid_automatic_code_fails(self):
        def edit(row,n,si,t,p):
            if n==1:
                row["player.automatic_decision"]="NA"
        with self.assertRaises(c.SourceError):
            audited(fixture(edit=edit))

    def test_missing_complete_six_person_previous_group_fails(self):
        def edit(row,n,si,t,p):
            if si==1 and t==1 and p==1:
                row["group.id_in_subsession"]="2"
                row["group"]="G2"
        with self.assertRaises(c.SourceError):
            audited(fixture(edit=edit))

    def test_source_original_md5_not_synthetic_rejected(self):
        with self.assertRaises(c.SourceError):
            c.real_source_score(self.constant)

    def test_person_round_duplicate_fails_in_roster(self):
        def edit(row,n,si,t,p):
            if si==1 and t==1 and p==2:
                row["participant.code"]="S1Person1"
                row["participant.id_in_session"]="1"
        with self.assertRaises(c.SourceError):
            audited(fixture(edit=edit))


if __name__=="__main__":
    unittest.main()
