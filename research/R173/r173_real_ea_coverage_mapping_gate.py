"""R173 pre-score coverage and reciprocal mapping audit on verified original EA data.

This script deliberately calculates no cultural variable association.
Dependencies: standard Python library and the pinned-source R173 loader.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import json
import re
import sys
import unittest

from r173_original_dplace_source_audit import COMMIT, HERE, rows

OUT = HERE / "R173_REAL_EA005_EA006_COVERAGE_AND_RECIPROCAL_MAPPING.json"
VALID = {"EA005": set("0123456789"), "EA006": set("1234567")}
VARIABLES = tuple(VALID)
YEAR_RE = re.compile(r"^[12][0-9]{3}$")


def refs(text: str, source: str) -> list[str]:
    """Extract only explicitly bracketed IDs of the named external dataset."""
    if source not in ("EA", "SCCS"):
        raise ValueError("unrecognized source")
    pattern = rf"(?:^|;\s*){source}:\s*[^;\[\]]*\[([A-Za-z0-9]+)\]"
    return re.findall(pattern, text or "")


def mappings(ea_rows, sccs_rows, valid_ea):
    ea_ids = {row["id"] for row in ea_rows}
    sc_ids = {row["id"] for row in sccs_rows}
    ea_pairs = [(r["id"], sid) for r in ea_rows for sid in refs(r["related"], "SCCS")]
    sc_pairs = [(eid, r["id"]) for r in sccs_rows for eid in refs(r["related"], "EA")]
    ea_set, sc_set = set(ea_pairs), set(sc_pairs)
    agreed = ea_set & sc_set
    ecount, scount = Counter(a for a, _ in agreed), Counter(b for _, b in agreed)
    clean = sorted((a,b) for a,b in agreed if ecount[a] == 1 and scount[b] == 1
                   and a in valid_ea and a in ea_ids and b in sc_ids)
    return {
        "EA_forward_ref_rows": len(ea_pairs),
        "SCCS_reverse_ref_rows": len(sc_pairs),
        "EA_forward_unique_pairs": len(ea_set),
        "SCCS_reverse_unique_pairs": len(sc_set),
        "reciprocal_unique_pairs": len(agreed),
        "accepted_exact_reciprocal_bijective_pairs": len(clean),
        "reciprocal_EA_ids": len(set(a for a,_ in agreed)),
        "reciprocal_SCCS_ids": len(set(b for _,b in agreed)),
        "EA_only_pairs": sorted(ea_set - sc_set)[:25],
        "SCCS_only_pairs": sorted(sc_set - ea_set)[:25],
        "ambiguous_agreed_EA_ids": sorted(a for a,n in ecount.items() if n > 1)[:25],
        "ambiguous_agreed_SCCS_ids": sorted(s for s,n in scount.items() if n > 1)[:25],
        "missing_EA_society_ids": sorted(a for a,_ in ea_set | sc_set if a not in valid_ea)[:25],
        "accepted_pairs": [{"EA_id":a,"SCCS_id":b} for a,b in clean],
    }


def four_digit_year(s):
    s = (s or "").strip()
    return int(s) if YEAR_RE.fullmatch(s) else None


def coverage(observations, societies, ids):
    """Classify at the society-variable level; never select a favorable duplicate."""
    chosen = set(ids)
    grouped = defaultdict(list)
    for row in observations:
        if row.get("soc_id") in chosen and row.get("var_id") in VALID:
            grouped[(row["soc_id"],row["var_id"])].append(row)
    soc_by_id = {r["id"]: r for r in societies}
    per_variable = {}
    clean_by_var = {}
    for var in VARIABLES:
        c = Counter()
        good = set()
        seen_codes = Counter()
        yy = Counter()
        year_mismatch = Counter()
        duplicate_samples = []
        for society in sorted(chosen):
            rs = grouped.get((society,var),[])
            if not rs:
                c["no_source_row"] += 1
                continue
            c["source_rows"] += len(rs)
            if len(rs) != 1:
                c["multiple_source_rows"] += 1
                if len(duplicate_samples) < 10:
                    duplicate_samples.append({"society":society,"count":len(rs),
                                              "codes":sorted(set(r.get("code","") for r in rs))})
                continue
            row = rs[0]
            code = row.get("code","").strip()
            seen_codes[code or "<blank>"] += 1
            if code not in VALID[var]:
                c["single_row_missing_or_illegal_code"] += 1
                continue
            c["usable_unambiguous"] += 1
            good.add(society)
            obs_y = four_digit_year(row.get("year",""))
            focal_y = four_digit_year(soc_by_id.get(society,{}).get("main_focal_year",""))
            yy["observation_year_present" if obs_y is not None else "observation_year_missing"] += 1
            yy["focal_year_present" if focal_y is not None else "focal_year_missing"] += 1
            if obs_y is not None and focal_y is not None:
                year_mismatch["both_years"] += 1
                if abs(obs_y - focal_y) > 25:
                    year_mismatch["over_25_years_apart"] += 1
        assert sum(c[k] for k in ("no_source_row","multiple_source_rows",
                 "single_row_missing_or_illegal_code","usable_unambiguous")) == len(chosen)
        per_variable[var] = {
            "societies_considered":len(chosen),
            "classification":dict(sorted(c.items())),
            "single_row_code_frequency":dict(sorted(seen_codes.items())),
            "year_availability_for_usable_rows":dict(sorted(yy.items())),
            "focal_vs_observation_year_on_usable_rows":dict(sorted(year_mismatch.items())),
            "example_multirow_conflicts":duplicate_samples,
        }
        clean_by_var[var] = good
    joint = sorted(clean_by_var["EA005"] & clean_by_var["EA006"])
    geographic = Counter()
    family_proxy = Counter()
    year_summary = Counter()
    for sid in joint:
        soc = soc_by_id[sid]
        geographic["coordinate_pair_present" if soc.get("Lat","").strip() and
                   soc.get("Long","").strip() else "coordinate_missing"] += 1
        family_proxy["glottocode_present" if soc.get("glottocode","").strip()
                     else "glottocode_missing"] += 1
        year_summary["focal_year_present" if four_digit_year(soc.get("main_focal_year"))
                     else "focal_year_missing"] += 1
    return {
        "unique_societies_considered":len(chosen),
        "per_variable":per_variable,
        "joint_usable_EA005_EA006_societies":len(joint),
        "joint_available_metadata": {
            "coordinates":dict(sorted(geographic.items())),
            "glottocode_only_not_language_family":dict(sorted(family_proxy.items())),
            "main_focal_year":dict(sorted(year_summary.items())),
        },
        "join_is_descriptive_only":True,
    }


def audit():
    _, obs = rows("datasets/EA/data.csv")
    _, soc = rows("datasets/EA/societies.csv")
    _, e_map = rows("datasets/EA/societies_mapping.csv")
    _, sc_map = rows("datasets/SCCS/societies_mapping.csv")
    soc_ids = [r["id"] for r in soc]
    if len(soc_ids) != len(set(soc_ids)):
        raise ValueError("duplicate original EA society IDs")
    mapping = mappings(e_map,sc_map,set(soc_ids))
    sccs_ids = [r["EA_id"] for r in mapping["accepted_pairs"]]
    result = {
      "research_id":"R173",
      "stage":"PRE_SCORE_SOURCE_MAPPING_AND_MISSINGNESS_AUDIT",
      "pinned_repository":"D-PLACE/dplace-data",
      "pinned_commit":COMMIT,
      "source_rows":len(obs),
      "EA_social_units":len(soc),
      "mapping":mapping,
      "full_EA_coverage":coverage(obs,soc,soc_ids),
      "strict_reciprocal_SCCS_coverage":coverage(obs,soc,sccs_ids),
      "estimated_associations":0,
      "fitted_models":0,
      "independent_predictions":0,
      "new_E2":0,"new_E3":0,
      "cautions":[
        "No covariances, significance values, causal claims or fitted coefficients computed.",
        "EA005 is ordinal; EA006 is nominal and cannot be treated as ordered.",
        "Glottocode is a language identifier, not a valid language-family cluster without an audited classification.",
        "SCCS mapped societies cannot be assumed historically, phylogenetically or spatially independent.",
        "Year is a field in the data observations, and focal year is a potentially different field in the society table.",
        "Any duplicate society-variable row remains excluded from unique-row eligibility."
      ]
    }
    OUT.write_text(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    summary = {"mapping":{k:v for k,v in mapping.items() if not isinstance(v,list)},
               "EA_joint":result["full_EA_coverage"]["joint_usable_EA005_EA006_societies"],
               "SCCS_joint":result["strict_reciprocal_SCCS_coverage"]["joint_usable_EA005_EA006_societies"]}
    print("R173_PRESCORE_AUDIT",json.dumps(summary,sort_keys=True))
    return result


class TestSourceGate(unittest.TestCase):
    def test_ref_exact_type(self):
        self.assertEqual(refs("Binford: A [B72]; SCCS: Kung [SCCS2]","SCCS"),["SCCS2"])
        self.assertEqual(refs("EA: Kung (Aa1) [Aa1]; Binford: X [B72]","EA"),["Aa1"])
    def test_missing_and_similar_dataset(self):
        self.assertEqual(refs("SCCS: no bracket; EA: A [Aa1]","SCCS"),[])
        self.assertEqual(refs("OtherSCCS: fake [SCCS3]","SCCS"),[])
    def test_reject_unknown_reference_name(self):
        with self.assertRaises(ValueError):
            refs("","DPLACE")
    def test_bidirectional(self):
        m=mappings([{"id":"Aa1","related":"SCCS: A [SCCS2]"}],
                   [{"id":"SCCS2","related":"EA: A [Aa1]"}],{"Aa1"})
        self.assertEqual(m["accepted_exact_reciprocal_bijective_pairs"],1)
    def test_nonreciprocal(self):
        m=mappings([{"id":"Aa1","related":"SCCS: A [SCCS2]"}],
                   [{"id":"SCCS2","related":""}],{"Aa1"})
        self.assertEqual(m["accepted_exact_reciprocal_bijective_pairs"],0)
    def test_ambiguous(self):
        m=mappings([{"id":"Aa1","related":"SCCS: A [SCCS2]; SCCS: B [SCCS3]"}],
                   [{"id":"SCCS2","related":"EA: A [Aa1]"},{"id":"SCCS3","related":"EA: A [Aa1]"}],{"Aa1"})
        self.assertEqual(m["accepted_exact_reciprocal_bijective_pairs"],0)
    def test_year_strict(self):
        self.assertEqual(four_digit_year("1950"),1950)
        self.assertIsNone(four_digit_year("c. 1950"))
        self.assertIsNone(four_digit_year(""))
    def test_coverage_no_imputation_or_ranked_nominal(self):
        soc=[{"id":"Aa1","main_focal_year":"1950","Lat":"5","Long":"6","glottocode":"foo"}]
        obs=[{"soc_id":"Aa1","var_id":"EA005","code":"9","year":"1940"},
             {"soc_id":"Aa1","var_id":"EA006","code":"7","year":"1940"}]
        z=coverage(obs,soc,["Aa1"])
        self.assertEqual(z["joint_usable_EA005_EA006_societies"],1)
    def test_duplicate_blocks_eligibility(self):
        soc=[{"id":"Aa1","main_focal_year":"","Lat":"","Long":"","glottocode":""}]
        obs=[{"soc_id":"Aa1","var_id":"EA005","code":"1","year":""},
             {"soc_id":"Aa1","var_id":"EA005","code":"1","year":""},
             {"soc_id":"Aa1","var_id":"EA006","code":"NA","year":""}]
        z=coverage(obs,soc,["Aa1"])
        self.assertEqual(z["joint_usable_EA005_EA006_societies"],0)
        self.assertEqual(z["per_variable"]["EA005"]["classification"]["multiple_source_rows"],1)
    def test_wrong_variable_code(self):
        soc=[{"id":"Aa1","main_focal_year":"","Lat":"","Long":"","glottocode":""}]
        z=coverage([{"soc_id":"Aa1","var_id":"EA006","code":"8"}],soc,["Aa1"])
        self.assertEqual(z["per_variable"]["EA006"]["classification"]["single_row_missing_or_illegal_code"],1)


if __name__=="__main__":
    if sys.argv[1:]==["--audit"]: audit()
    elif sys.argv[1:]==["--self-test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    else: raise SystemExit("use --audit or --self-test")
