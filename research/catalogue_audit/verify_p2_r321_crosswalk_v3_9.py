#!/usr/bin/env python3
"""Independent original239 v3.9 invariants; Git blob source identities; no empirical overclaim."""
import csv,hashlib,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(p):return (ROOT/p).read_bytes()
def blob(p):
    b=read(p);return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def run():
    base_path="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.8_2026-10-24.json"
    new_path="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.9_2026-10-24.json"
    old=json.loads(read(base_path));new=json.loads(read(new_path))
    assert blob(base_path)=="2ff10773da2157eb94fb887f0c80ec09aff7f7b3"
    assert new["base_v3_8_git_blob_sha1"]==blob(base_path)
    assert len(old["rows"])==len(new["rows"])==239
    a={r["catalogue_id"]:r for r in old["rows"]}
    b={r["catalogue_id"]:r for r in new["rows"]}
    assert list(a)==list(b) and len(a)==239
    assert all(a[k]==b[k] for k in a if k!="01-010")
    target=b["01-010"]
    assert target["catalogue_name_en"]=="Sequential Sampling Models"
    assert target["proposed_primary_research_id"]=="R321"
    assert target["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
    assert target["original_priority"]=="P2"
    assert blob(target["readme_path"])==target["readme_git_blob_sha1"]=="30982398e04229176d1b3d80f1b083f88e44ee77"
    assert new["counts"]["primary_R"]==213
    assert new["counts"]["shared_bounded_math"]==3
    assert new["counts"]["pending_primary_R"]==new["counts"]["no_link_in_checked_sets"]==23
    counts=Counter(x["link_status"] for x in new["rows"])
    assert sum(counts.values())==239
    assert counts["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==23
    assert counts["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==4
    assert counts["PROVISIONAL_PRIMARY_README_LINK"]==173
    for status,count in counts.items():assert new["status_counts"][status]==count
    pending=list(csv.DictReader(read("docs/ORIGINAL_239_PENDING_23_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv").decode().splitlines()))
    assert len(pending)==23 and pending[0]["original_catalogue_id"]=="01-012"
    assert [x["original_catalogue_id"] for x in pending]==[x["catalogue_id"] for x in new["rows"] if x["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    for path,sha in (
        ("protocols/R321_WALD_FINITE_BERNOULLI_SPRT_1024_PATHS_PRESCORE_FREEZE_2026-10-24.md","211fc14095398194849995d2795a5e12c2feba69"),
        ("research/R321/r321_finite_sprt.py","4a52be69239780492faf90aae79ab3fb5c1d0c7a"),
        ("research/R321/R321_ALL_1024_ORIGINAL_SEVEN_BIT_PATHS.csv","d5e5e183a786e199fbf792589ed68735f30ca1b3"),
        ("research/R321/R321_EXACT_8_WORLDS.json","5d8a6e807a099ab8b3e653c519a198497335fded"),
        ("research/catalogue_audit/independent_r321_sprt_audit.py","75f5f6014aa24efcc465bb7ec33439be7effe71d")):
        assert blob(path)==sha,(path,blob(path))
    receipt=json.loads(read("research/R321/R321_MACHINE_RECEIPT.json"))
    acceptance=json.loads(read("research/R321/R321_FINAL_ACCEPTANCE_STATUS.json"))
    assert receipt["protocol_commit"]=="f889554205b5339f1c52faa4c25d36dc270edb1f"
    assert receipt["original_source_commit"]=="1da4a0dfaad4494dd11ce35d128f5a2f05d78007"
    assert receipt["verification"]["CI_run_id"]==40013917870
    assert all(x["conclusion"]=="success" for x in receipt["verification"]["jobs"])
    assert acceptance["status"]=="PASS_BOUNDED_E1_FINITE_WALD_INSPIRED_ONLY"
    assert acceptance["real_human_E2"]=="NOT_ESTABLISHED" and acceptance["historical_E3"]=="NOT_ESTABLISHED"
    assert "R321" in new["E1_new_research"] and new["changed_original_IDs"][-1]=="01-010"
    print("ORIGINAL239_V39_PASS 239 identity rows 213 primary 3 shared 23 pending 173 provisional 1024 E1 paths")
if __name__=="__main__":run()
