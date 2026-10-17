"""R074 source audit contracts, all identities and rows synthetic."""
import unittest
from r074_dalbo_author_source_gate import audit

HEADER = """* Dictionary *
match: match #
round: round #
date: session date
r: payoff
delta: continuation probability
coop: cooperate or defect
group: pair identifier
id: subject identity within session
**************
match round date r delta coop group id
"""

def make_blob(sessions=("111.1","222.1"), games=2, rounds=3):
    rows=[]
    for d in sessions:
        for game in range(1,games+1):
            for p in (1,2):
                for t in range(1,rounds+1):
                    rows.append(f"{game} {t} {d} 32 .5 {(t+p)%2} {game} {p}")
    return (HEADER+"\n".join(rows)+"\n").encode()

class OriginalSourceGateTests(unittest.TestCase):
    def test_source_structure_two_sessions(self):
        x=audit(make_blob())
        self.assertEqual(x["distinct_sessions"],2)
        self.assertEqual(x["human_match_series"],8)
        self.assertEqual(x["source_rows"],24)
        self.assertEqual(x["candidate_t3_plus_actions"],8)
        self.assertEqual(x["treatments"][0]["session_count"],2)
        self.assertTrue(x["treatments"][0]["other_same_treatment_session_trainable"])
        self.assertFalse(x["scoring_models_executed"])

    def test_binary_rejected(self):
        blob=make_blob().replace(b" 32 .5 0 ",b" 32 .5 2 ",1)
        with self.assertRaisesRegex(ValueError,"COOP_NOT_BINARY"):audit(blob)

    def test_non_pair_rejected(self):
        s=make_blob().decode()
        line=next(ln for ln in s.splitlines() if ln.startswith("1 1 111.1"))
        s=s.replace(line+"\n","",1)
        with self.assertRaisesRegex(ValueError,"EXACTLY_TWO"):audit(s.encode())

    def test_repeated_record_rejected(self):
        s=make_blob().decode()
        line=next(ln for ln in s.splitlines() if ln.startswith("1 1 111.1"))
        with self.assertRaisesRegex(ValueError,"DUPLICATE"):audit((s+line+"\n").encode())

    def test_gap_in_round_rejected(self):
        s=make_blob().decode().replace("1 2 111.1","1 4 111.1")
        with self.assertRaises(ValueError):audit(s.encode())

    def test_no_cross_match_memory(self):
        x=audit(make_blob(rounds=2,games=5))
        self.assertEqual(x["candidate_t3_plus_actions"],0)

    def test_fail_on_treatment_switch_in_one_date(self):
        s=make_blob().decode().replace("1 1 111.1 32 .5","1 1 111.1 40 .5")
        with self.assertRaisesRegex(ValueError,"SESSION_MULTIPLE_TREATMENTS"):audit(s.encode())

    def test_same_day_decimal_sessions_distinct(self):
        x=audit(make_blob(sessions=("111.1","111.2")))
        self.assertEqual(x["distinct_sessions"],2)

    def test_no_ids_or_action_trajectories_exported(self):
        x=audit(make_blob())
        self.assertNotIn("individual_records",x)
        self.assertNotIn("session_identifiers",x)

if __name__=="__main__":
    unittest.main()
