#!/usr/bin/env python3
"""Original239 v5.8 strict R340/R341 itemwise linkage and 3-item queue audit."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.7_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.8_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_3_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"

def raw(p):return (ROOT/p).read_bytes()
def blob(p):
    b=raw(p)
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def main():
    old,new=json.loads(raw(OLD)),json.loads(raw(NEW))
    assert blob(OLD)=="dddf026e63049254acfa350fb4cd8324bb9fc234"
    assert new["base_v5_7_git_blob_sha1"]==blob(OLD)
    assert len(old["rows"])==len(new["rows"])==239
    assert [x["catalogue_id"] for x in old["rows"]]==[x["catalogue_id"] for x in new["rows"]]
    assert len({x["catalogue_id"] for x in new["rows"]})==239
    targets={"04-007":("R340",40063363405,48,3,"c4b98ab32a221a1b8e549d6850f3d0e4d71a7015"),
             "04-020":("R341",40063471750,32,4,"0506e9a4fdcf5e13b02065df62c0c488bea2a604")}
    for before,after in zip(old["rows"],new["rows"]):
        id=before["catalogue_id"]
        if id not in targets:
            assert before==after,id
            continue
        rid,run,atoms,worlds,readme_sha=targets[id]
        assert before["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
        assert after["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
        assert after["proposed_primary_research_id"]==rid
        assert blob(after["readme_path"])==after["readme_git_blob_sha1"]==readme_sha
        assert after["method_specific_E1_acceptance"]==f"research/{rid}/{rid}_FINAL_ACCEPTANCE_STATUS.json"
        status=json.loads(raw(after["method_specific_E1_acceptance"]))
        receipt=json.loads(raw(f"research/{rid}/{rid}_MACHINE_RECEIPT.json"))
        assert status["status"].startswith("PASS_BOUNDED_E1_CONSTRUCTED_")
        assert status["CI_run_id"]==receipt["verification"]["run_id"]==run
        assert status["three_jobs_success"] and status["CI_conclusion"]=="success"
        assert status["artificial_original_source_rows"]==atoms and status["world_count"]==worlds
        assert status["real_human_E2"]==status["historical_E3"]=="NOT_ESTABLISHED"
        for path,sha in [
            (f"research/{rid}/{rid}_ALL_{atoms}_ARTIFICIAL_"+("GENERATOR_ATOMS.csv" if rid=="R340" else "GRAPH_ATOMS.csv"),receipt["artificial_source_blob_sha1"]),
            (f"research/{rid}/"+("R340_EXACT_3_GENERATORS.json" if rid=="R340" else "R341_EXACT_4_GRAPH_WORLDS.json"),receipt["results_blob_sha1"]),
            (f"research/{rid}/"+("r340_sis_generator.py" if rid=="R340" else "r341_exact_ergm.py"),receipt["production_python_blob_sha1"]),
            (f"research/catalogue_audit/independent_{rid.lower()}_"+("sis_audit.py" if rid=="R340" else "ergm_audit.py"),receipt["independent_auditor_blob_sha1"]),
        ]:
            assert blob(path)==sha,(path,blob(path))
    assert new["counts"]==dict(primary_R=233,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=3,pending_primary_R=3)
    counts=Counter(x["link_status"] for x in new["rows"])
    assert counts["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert counts["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==24
    assert counts["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==3
    assert dict(counts)=={k:v for k,v in new["status_counts"].items() if v>0}
    pending=[x["catalogue_id"] for x in new["rows"] if x["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    rows=list(csv.DictReader(raw(QUEUE).decode().splitlines()))
    assert [x["original_catalogue_id"] for x in rows]==pending==["04-021","04-023","04-024"]
    assert new["changed_original_IDs"][-2:]==["04-007","04-020"]
    assert new["E1_new_research"][-2:]==["R340","R341"]
    print("ORIGINAL239_V58_PASS 239 candidates 233 primary 3 shared 3 pending 173 provisional R340 R341 E1 only")

if __name__=="__main__":
    main()
