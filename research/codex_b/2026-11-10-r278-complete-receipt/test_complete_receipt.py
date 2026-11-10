"""R278 S74 finite artificial receipt; no human records loaded."""
import copy
from fractions import Fraction as F
import json
from pathlib import Path
import tempfile
import unittest

import complete_receipt as gate

ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = ROOT/"research/validation/R278_S74_EXACT_RESULTS_2026-10-30.json"
CSV_PATH = ROOT/"research/validation/R278_S74_ALL_960_ARTIFICIAL_SOURCES_2026-10-30.csv"


def original(): return json.loads(JSON_PATH.read_text())


class CompleteReceiptTests(unittest.TestCase):
    def test_hand_k2_joint_product_and_covariance(self):
        row = gate.expected_receipt()["conditional_forecasts"][2]
        self.assertEqual(row["posterior_low"], F(1, 2))
        self.assertEqual(row["marginal_q"], F(1, 2))
        self.assertEqual(row["joint_Q"], {"00": F(5, 16), "01": F(3, 16), "10": F(3, 16), "11": F(5, 16)})
        self.assertEqual(set(row["product_Q"].values()), {F(1, 4)})
        self.assertEqual(row["joint_predictive_covariance"], F(1, 16))

    def test_all_conditional_marginals_and_covariance_identity(self):
        rows = gate.expected_receipt()["conditional_forecasts"]
        self.assertEqual(set(rows), {0, 1, 2, 3, 4})
        for k, row in rows.items():
            w, q = row["posterior_low"], row["marginal_q"]
            self.assertEqual(sum(row["joint_Q"].values()), F(1))
            self.assertEqual(sum(row["product_Q"].values()), F(1))
            for field in ("joint_Q", "product_Q"):
                self.assertEqual(row[field]["10"]+row[field]["11"], q)
                self.assertEqual(row[field]["01"]+row[field]["11"], q)
            self.assertEqual(row["joint_predictive_covariance"], row["joint_Q"]["11"]-q*q)
            self.assertEqual(row["joint_predictive_covariance"], w*(1-w)/4)

    def test_hand_central_comparison_and_risk(self):
        expected = gate.expected_receipt()
        self.assertEqual(expected["world_results"][("1/2", "BMA_JOINT")]["expected_joint_brier"], F(2206809, 2689600))
        self.assertEqual(expected["BMA_joint_minus_product"]["1/2"]["delta"], F(1204403217, 113030440000))

    def test_original_full_receipt_and_native_csv_pass(self):
        self.assertEqual(gate.validate_receipt(original()), 140)
        result = gate.check(CSV_PATH, JSON_PATH)
        self.assertEqual((result["receipt_leaves"], result["source_rows"], result["worlds"]), (140, 960, 15))

    def test_record_reordering_and_equivalent_fraction_are_valid(self):
        receipt = original()
        for key in ("world_results", "BMA_joint_minus_product", "conditional_forecasts"):
            receipt[key].reverse()
        receipt["conditional_forecasts"][2]["posterior_low"] = "2/4"
        self.assertEqual(gate.validate_receipt(receipt), 140)

    def test_missing_and_extra_fields_fail_closed(self):
        for key in ("conditional_forecasts", "BMA_joint_minus_product", "R073", "new_E2_predictions"):
            receipt = original(); del receipt[key]
            with self.assertRaises(ValueError): gate.validate_receipt(receipt)
        receipt = original(); receipt["extra"] = 0
        with self.assertRaises(ValueError): gate.validate_receipt(receipt)
        receipt = original(); del receipt["conditional_forecasts"][0]["joint_Q"]["11"]
        with self.assertRaises(ValueError): gate.validate_receipt(receipt)

    def test_covariance_and_delta_tampering_rejected(self):
        for key in ("covariance", "delta", "joint_probability"):
            receipt = original()
            if key == "covariance": receipt["conditional_forecasts"][2]["joint_predictive_covariance"] = "999"
            elif key == "delta": receipt["BMA_joint_minus_product"][0]["delta"] = "999"
            else: receipt["conditional_forecasts"][2]["joint_Q"]["11"] = "1/4"
            with self.assertRaisesRegex(ValueError, "RECEIPT_MISMATCH"):
                gate.validate_receipt(receipt)

    def test_duplicate_and_missing_identity_records_rejected(self):
        for field in ("world_results", "BMA_joint_minus_product", "conditional_forecasts"):
            receipt = original(); receipt[field][1] = copy.deepcopy(receipt[field][0])
            with self.assertRaises(ValueError): gate.validate_receipt(receipt)
            receipt = original(); receipt[field].pop()
            with self.assertRaises(ValueError): gate.validate_receipt(receipt)

    def test_numeric_bool_and_float_substitutions_rejected(self):
        for field, bad in (("new_E2_predictions", False), ("new_E3_predictions", False),
                           ("primitive_rows", 960.0), ("same_source_reused_across_policies", 1)):
            receipt = original(); receipt[field] = bad
            with self.assertRaises(ValueError): gate.validate_receipt(receipt)
        for bad in (False, 2.0):
            receipt = original(); receipt["conditional_forecasts"][2]["train_successes"] = bad
            with self.assertRaises(ValueError): gate.validate_receipt(receipt)

    def test_scope_and_nonfinite_or_wrong_fraction_types_rejected(self):
        receipt = original(); receipt["R073"] = "MODIFIED"
        with self.assertRaises(ValueError): gate.validate_receipt(receipt)
        for bad in ("NaN", "Infinity", "", 0.0625, True):
            receipt = original(); receipt["conditional_forecasts"][2]["joint_predictive_covariance"] = bad
            with self.assertRaises(ValueError): gate.validate_receipt(receipt)

    def test_duplicate_json_keys_and_nonstandard_constants_rejected(self):
        for raw in ('{"x":0,"x":1}', '{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}'):
            with self.assertRaises(ValueError): gate.loads_strict(raw)
        raw = JSON_PATH.read_text().replace('"R073": "FROZEN"', '"R073": "MODIFIED", "R073": "FROZEN"')
        with self.assertRaises(ValueError): gate.loads_strict(raw)

    def test_corrupt_csv_is_still_rejected_by_existing_source_route(self):
        with tempfile.TemporaryDirectory(prefix="s74-csv-negative-") as tmp:
            path = Path(tmp)/"bad.csv"
            lines = CSV_PATH.read_text().splitlines()
            row = lines[1].split(","); row[6] = "1"; lines[1] = ",".join(row)
            path.write_text("\n".join(lines)+"\n")
            with self.assertRaises(ValueError): gate.check(path, JSON_PATH)

    def test_ambiguous_csv_header_and_extra_cells_are_rejected(self):
        with tempfile.TemporaryDirectory(prefix="s74-csv-shape-negative-") as tmp:
            path = Path(tmp)/"ambiguous.csv"
            rows = [line.split(",") for line in CSV_PATH.read_text().splitlines()]
            duplicated = [row[:7]+(["source_probability"] if index == 0 else ["999"])+row[7:]
                          for index, row in enumerate(rows)]
            path.write_text("\n".join(",".join(row) for row in duplicated)+"\n")
            with self.assertRaisesRegex(ValueError, "CSV_HEADER_SCHEMA"): gate.check(path, JSON_PATH)
            rows[1].append("999")
            path.write_text("\n".join(",".join(row) for row in rows)+"\n")
            with self.assertRaisesRegex(ValueError, "CSV_ROW_SCHEMA"): gate.check(path, JSON_PATH)


if __name__ == "__main__": unittest.main()
