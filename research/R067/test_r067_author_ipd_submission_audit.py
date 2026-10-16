"""Safe synthetic author-IPD source schema controls, never real participants."""
import csv,io,unittest
from unittest.mock import patch
import r067_author_ipd_submission_audit as s

def toy(action="C",duplicate=False):
    out=io.StringIO(newline="")
    cols=["round","player","action_player","opponent","action_opponent","payoff",
          "who_played","treatment","session"]
    wr=csv.DictWriter(out,fieldnames=cols);wr.writeheader()
    wr.writerow({"round":1,"player":"FAKE_1","action_player":action,
                 "opponent":"FAKE_2","action_opponent":"D","payoff":4,
                 "who_played":"user","treatment":"fix","session":"FAKE_S"})
    wr.writerow({"round":1 if duplicate else 2,"player":"FAKE_1",
                 "action_player":"D","opponent":"FAKE_2","action_opponent":"C",
                 "payoff":1,"who_played":"user","treatment":"fix","session":"FAKE_S"})
    return out.getvalue().encode()

def run(b):
    with patch.object(s,"FILES",{"fix.csv":(len(b),s.git_sha(b))}):
        return s.audit_csv_bytes("fix.csv",b)

class AuditTests(unittest.TestCase):
    def test_real_C_and_D_schema_counts(self):
        x=run(toy())
        self.assertEqual((x["actions_player_C"],x["actions_player_D"]),(1,1))
        self.assertEqual(x["session_player_round_repeat_rows"],0)
        self.assertNotIn("FAKE_1",str(x))

    def test_duplicate_player_round_detected_not_hidden(self):
        self.assertEqual(run(toy(duplicate=True))["session_player_round_repeat_rows"],1)

    def test_unknown_choice_not_recoded_as_D(self):
        x=run(toy(action="X"))
        self.assertEqual(x["actions_player_other_or_missing"],1)
        self.assertEqual(x["actions_player_D"],1)

    def test_source_tamper_hard_fails(self):
        b=toy()
        with patch.object(s,"FILES",{"fix.csv":(len(b),s.git_sha(b))}):
            with self.assertRaises(ValueError):
                s.audit_csv_bytes("fix.csv",b.replace(b"FAKE_1",b"FAKE_3",1))

    def test_missing_column_hard_fails(self):
        b=b"round,player,action_player\n1,x,C\n2,x,D\n"
        with patch.object(s,"FILES",{"fix.csv":(len(b),s.git_sha(b))}):
            with self.assertRaises(ValueError):
                s.audit_csv_bytes("fix.csv",b)

    def test_git_blob_empty_known(self):
        self.assertEqual(s.git_sha(b""),"e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")

    def test_nonnumeric_round_cannot_prove_clean_schema(self):
        b=toy().replace(b"\n1,FAKE_1",b"\nNaN,FAKE_1",1)
        self.assertEqual(run(b)["invalid_round_values"],1)

if __name__=="__main__":
    unittest.main()
