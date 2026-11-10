"""Independent integer/rational finite-design checks; no human scoring."""
from fractions import Fraction as F
import copy
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest

import certificate as m
import audit as a

ROOT = Path(__file__).resolve().parents[3]
CSV_PATH = ROOT/"research/R268/R268_ALL_3312_BERNOULLI_ORDERED_SOURCE_TYPES.csv"
CORE_PATH = ROOT/"research/R268/R268_EXACT_RESULTS.json"
S64_PATH = ROOT/"research/validation/R268_S64_ONE_STEP_BRIER_EXACT_RECEIPT_2026-10-29.json"


def write_case(folder, rows=None, core=None, s64=None):
    csv_path, core_path, s64_path = (Path(folder)/name for name in ("source.csv", "core.json", "s64.json"))
    if rows is None: csv_path.write_bytes(CSV_PATH.read_bytes())
    else:
        with csv_path.open("w", newline="") as stream: csv.writer(stream, lineterminator="\n").writerows(rows)
    core_path.write_text(json.dumps(core if core is not None else json.loads(CORE_PATH.read_text())))
    s64_path.write_text(json.dumps(s64 if s64 is not None else json.loads(S64_PATH.read_text())))
    return csv_path, core_path, s64_path


def coordinated_mutation():
    """Deliberately wrong shared labels with recomputed dependent summaries."""
    rows = list(csv.reader(io.StringIO(CSV_PATH.read_text())))
    fields = {name: i for i, name in enumerate(rows[0])}
    for row in rows[1:]:
        if row[fields["n"]] == "4" and row[fields["original_success_count"]] == "0":
            row[fields["AIC_selected"]] = "M1_FITTED"
            row[fields["criteria_disagree"]] = "0"
    core, s64 = json.loads(CORE_PATH.read_text()), json.loads(S64_PATH.read_text())
    for world in core["worlds"]:
        if world["n"] != 4: continue
        p = F(world["true_p"]); weight = (1-p)**4
        world["frozen_per_K_decisions"]["0"]["AIC"] = "M1_FITTED"
        world["source_weighted_probability_AIC_selects_M1"] = str(F(world["source_weighted_probability_AIC_selects_M1"])+weight)
        world["source_weighted_probability_AIC_BIC_disagree"] = str(F(world["source_weighted_probability_AIC_BIC_disagree"])-weight)
    for world in s64["results"]:
        if world["n"] != 4: continue
        p = F(world["true_p"]); change = (1-p)**4*(F(2, 5)*p-F(1, 25))
        for field in ("risk", "excess"):
            world[field]["AIC_SELECTED"] = str(F(world[field]["AIC_SELECTED"])+change)
        world["AIC_minus_BIC"] = str(F(world["AIC_minus_BIC"])+change)
    return rows, core, s64


class CertificateTests(unittest.TestCase):
    def test_exponential_series_bounds_have_hand_values(self):
        self.assertEqual(m.e2_bounds(3), (F(19, 3), F(67, 9)))
        low, high = m.e2_bounds(4)
        self.assertGreater(low, F(19, 3)); self.assertLess(high, F(67, 9))

    def test_likelihood_ratio_endpoints_and_hand_interior(self):
        self.assertEqual(m.likelihood_ratio_squared(4, 0), F(390625, 65536))
        self.assertEqual(m.likelihood_ratio_squared(4, 2), F(390625, 65536))
        self.assertEqual(m.likelihood_ratio_squared(10, 4), F(531441, 65536))
        self.assertEqual(m.likelihood_ratio_squared(4, 4), F(390625))

    def test_hand_reversed_penalty_decisions(self):
        a = m.certify(4, 0); b = m.certify(10, 4)
        self.assertEqual((a["AIC"], a["BIC"]), ("M0_FIXED", "M1_FITTED"))
        self.assertEqual((b["AIC"], b["BIC"]), ("M1_FITTED", "M0_FIXED"))

    def test_all23_states_are_strictly_certified(self):
        rows = [m.certify(n, k) for n in (4, 6, 10) for k in range(n+1)]
        self.assertEqual(len(rows), 23)
        self.assertEqual(min(r["AIC_margin_lower_bound"] for r in rows), F(73309, 1245184))
        self.assertEqual(min(r["BIC_margin_lower_bound"] for r in rows), F(123919, 655360))
        self.assertTrue(all(r["AIC_margin_lower_bound"] > F(1, 10**12) and
                            r["BIC_margin_lower_bound"] > F(1, 10**12) for r in rows))

    def test_exact_decision_sequences_match_hand_frozen_grid(self):
        expected = {4: ("00011", "10111"), 6: ("1001111", "1001111"),
                    10: ("10001111111", "10000111111")}
        for n, labels in expected.items():
            got = tuple("".join(str(int(m.certify(n, k)[criterion] == "M1_FITTED")) for k in range(n+1))
                        for criterion in ("AIC", "BIC"))
            self.assertEqual(got, labels)

    def test_polynomial_count_distribution_hand_binomial(self):
        self.assertEqual(m.count_distribution(F(1, 2), 4), [F(v, 16) for v in (1, 4, 6, 4, 1)])
        for p in (F(1, 5), F(1, 2), F(4, 5)):
            for n in (4, 6, 10): self.assertEqual(sum(m.count_distribution(p, n)), F(1))

    def test_hand_selection_probabilities(self):
        result = m.world_metrics(F(1, 2), 4)
        self.assertEqual(result["selection"], {"AIC": F(5, 16), "BIC": F(3, 4), "disagree": F(7, 16)})
        self.assertEqual(m.world_metrics(F(1, 5), 6)["selection"]["disagree"], F(0))

    def test_hand_independent_future_risk(self):
        result = m.world_metrics(F(1, 5), 4)
        self.assertEqual(result["risk"], {"M0_FIXED": F(4, 25), "M1_MLE": F(1, 5),
                                          "AIC_SELECTED": F(2637, 15625), "BIC_SELECTED": F(3109, 15625)})
        self.assertEqual(result["AIC_minus_BIC"], F(-472, 15625))

    def test_future_risk_identity_and_range(self):
        for p in (F(1, 5), F(1, 2), F(4, 5)):
            for n in (4, 6, 10):
                result = m.world_metrics(p, n)
                self.assertTrue(all(F(0) <= v <= F(1) for v in result["risk"].values()))
                self.assertEqual(result["risk"]["M1_MLE"], p*(1-p)*(1+F(1, n)))
                self.assertEqual(result["AIC_minus_BIC"], result["risk"]["AIC_SELECTED"]-result["risk"]["BIC_SELECTED"])

    def test_invalid_state_types_and_worlds_fail_closed(self):
        for n, k in ((True, 0), (4, False), (4, 2.0), (4, -1), (4, 5), (5, 2)):
            with self.assertRaises(ValueError): m.certify(n, k)
        for p in (.5, True, F(1, 3)):
            with self.assertRaises(ValueError): m.count_distribution(p, 4)
        for bad in (0, True, 2.0):
            with self.assertRaises(ValueError): m.e2_bounds(bad)

    def test_insufficient_proof_precision_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "UNRESOLVED_AIC_BOUND"):
            m.certify(4, 0, order=1)

    def test_actual_sources_and_receipts_agree_with_independent_certificate(self):
        result = a.audit(CSV_PATH, CORE_PATH, S64_PATH)
        self.assertEqual({key: result[key] for key in ("states", "source_rows", "core_decision_records", "selection_probabilities", "S64_fraction_checks")},
                         {"states": 23, "source_rows": 3312, "core_decision_records": 69, "selection_probabilities": 27, "S64_fraction_checks": 81})

    def test_coordinated_shared_labels_and_summaries_cannot_replace_proof(self):
        rows, core, s64 = coordinated_mutation()
        with tempfile.TemporaryDirectory(prefix="r268-shared-label-control-") as tmp:
            args = write_case(tmp, rows, core, s64)
            with self.assertRaisesRegex(ValueError, "CSV_DECISION_CERTIFICATE"):
                a.audit(*args)

    def test_bad_source_probability_coverage_and_risk_are_rejected(self):
        source = list(csv.reader(io.StringIO(CSV_PATH.read_text())))
        for kind in ("missing", "duplicate", "mass", "NaN_log", "risk", "E2_bool"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory(prefix="r268-numeric-negative-") as tmp:
                rows = copy.deepcopy(source); core = json.loads(CORE_PATH.read_text()); s64 = json.loads(S64_PATH.read_text())
                if kind == "missing": rows.pop()
                elif kind == "duplicate": rows[-1] = list(rows[1])
                elif kind == "mass": rows[1][5] = "1"
                elif kind == "NaN_log": rows[1][7] = "NaN"
                elif kind == "risk": s64["results"][0]["risk"]["AIC_SELECTED"] = "999"
                else: core["new_real_human_E2"] = False
                with self.assertRaises(ValueError): a.audit(*write_case(tmp, rows, core, s64))


if __name__ == "__main__": unittest.main()
