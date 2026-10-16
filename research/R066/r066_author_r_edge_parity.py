#!/usr/bin/env python3
"""Compare entire author-R-derived household edge sets vs Python, no row output.

Only final aggregated counts and parity verdict are emitted; raw respondent
identifiers and per-village edges remain in CI runner temporary files.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from collections import Counter, defaultdict
from pathlib import Path

from r066_larson_lewis_public_schema import FILES
from r066_larson_lewis_semantic_mapping import PINNED_SHA256
from r066_larson_lewis_join_gate import NETWORKS, clean_id
from r066_author_household_audit import MEMBERS, sort_hhnum

NETWORK_TYPES = tuple(NETWORKS)
MAX_LINES = 100_000


def canonical(village: str, category: str, a: int, b: int):
    if category not in NETWORK_TYPES or not village or a == b or a < 1 or b < 1:
        raise ValueError("invalid canonical undirected household edge")
    return village, category, min(a,b), max(a,b)


def python_edge_sets(rows: list[dict], require_full=True):
    if require_full and len(rows) != 2125:
        raise ValueError("expected 2125 original household rows")
    by_village = defaultdict(list)
    for row in rows:
        village = clean_id(row["village_number"])
        if village is None:
            raise ValueError("missing village")
        by_village[village].append(row)
    if require_full and len(by_village) != 16:
        raise ValueError("expected 16 source villages")
    edges = set()
    for village, raw in by_village.items():
        records = sorted(raw, key=lambda x: sort_hhnum(x["hhnum"]))
        names_to_households = defaultdict(set)
        for position, row in enumerate(records, start=1):
            members = {clean_id(row.get(col,"")) for col in MEMBERS}
            members.discard(None)
            for member in members:
                names_to_households[member].add(position)
        for category, columns in NETWORKS.items():
            for row in records:
                people_from = names_to_households.get(clean_id(row["ego"]), ())
                for col in columns:
                    person_to = clean_id(row[col])
                    if person_to is None:
                        continue
                    people_to = names_to_households.get(person_to, ())
                    for from_position in people_from:
                        for to_position in people_to:
                            if from_position != to_position:
                                edges.add(canonical(village,category,from_position,to_position))
    return edges


def read_author_rows(source_dir: Path):
    data = {}
    for label,(filename,_,size) in FILES.items():
        raw=(source_dir/filename).read_bytes()
        if len(raw)!=size or hashlib.sha256(raw).hexdigest()!=PINNED_SHA256[label]:
            raise ValueError("original source SHA256/length mismatch: "+label)
        data[label] = raw
    source=data["script"].decode("utf-8-sig")
    for function in ("make_el <- function", "convert_to_hh <- function"):
        if source.count(function) != 1:
            raise ValueError("original R function missing or duplicated")
    rdr=csv.DictReader(io.StringIO(data["data"].decode("utf-8-sig"),newline=""),
                       delimiter="\t")
    if rdr.fieldnames is None or len(rdr.fieldnames) != 66:
        raise ValueError("source 66-column schema mismatch")
    rows=list(rdr)
    if len(rows)!=2125 or any(None in row or any(val is None for val in row.values()) for row in rows):
        raise ValueError("original 2125-row source schema mismatch")
    return rows


def export_canonical_edges(edges, output_path: Path):
    # Runner-temp only; never upload as artifact, never print edges.
    with output_path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.writer(f,delimiter="\t",lineterminator="\n")
        for edge in sorted(edges):
            writer.writerow(edge)


def parse_r_edge_file(path: Path):
    edges=set()
    with path.open(encoding="utf-8",newline="") as f:
        reader=csv.reader(f,delimiter="\t")
        for n,row in enumerate(reader,1):
            if n>MAX_LINES or len(row)!=4:
                raise ValueError("invalid or too large R edge universe")
            village,category,a,b=row
            if not a.isdecimal() or not b.isdecimal():
                raise ValueError("R edge household position invalid")
            edge=canonical(village,category,int(a),int(b))
            if edge in edges:
                raise ValueError("duplicate R canonical edge")
            edges.add(edge)
    if not edges:
        raise ValueError("R side had no household edges")
    return edges


def compare_edges(python_edges, r_edges):
    if not python_edges or not r_edges:
        raise ValueError("cannot compare empty household universes")
    only_python=python_edges-r_edges
    only_r=r_edges-python_edges
    counts_python=Counter(edge[1] for edge in python_edges)
    counts_r=Counter(edge[1] for edge in r_edges)
    return {
        "status":("AUTHOR_R_CORE_EDGE_PARITY_PASS" if not only_python and not only_r
                  else "AUTHOR_R_CORE_EDGE_PARITY_FAIL"),
        "source_category_counts_python":{n:counts_python[n] for n in NETWORK_TYPES},
        "source_category_counts_r":{n:counts_r[n] for n in NETWORK_TYPES},
        "python_edge_count":len(python_edges),
        "r_edge_count":len(r_edges),
        "only_python_edges":len(only_python),
        "only_r_edges":len(only_r),
        "edge_identity_assessment":"ENTIRE_IN_MEMORY_SET_EQUALITY_NOT_JUST_COUNTS",
        "complete_original_r_igraph_analysis_parity":"OPEN",
        "real_model_fitting":"NOT_PERFORMED",
        "individual_edges_emitted":False,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-dir",type=Path,required=True)
    ap.add_argument("--r-edge-file",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    try:
        rows=read_author_rows(args.source_dir)
        py_edges=python_edge_sets(rows)
        r_edges=parse_r_edge_file(args.r_edge_file)
        detail=compare_edges(py_edges,r_edges)
        result={
            "research":"R066",
            "stage":"E2_AUTHOR_R_CORE_HOUSEHOLD_EDGE_PARITY",
            "protocol":"protocols/R066_E2_AUTHOR_R_EDGE_PARITY_2026-10-16.md",
            "source":"doi:10.7910/DVN/RAHSVM",
            "version":"1.0",
            "source_sha256":PINNED_SHA256,
            **detail,
            "pesen_v01":"FROZEN",
        }
    except (ValueError,OSError,UnicodeError,csv.Error) as exc:
        result={"research":"R066","stage":"E2_AUTHOR_R_CORE_HOUSEHOLD_EDGE_PARITY",
                "status":"UNRESOLVED_SOURCE_OR_EXECUTION",
                "error_type":type(exc).__name__,
                "individual_edges_emitted":False,"pesen_v01":"FROZEN"}
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="AUTHOR_R_CORE_EDGE_PARITY_PASS":
        raise RuntimeError("source R vs Python full edge equality NOT established")


if __name__=="__main__":
    main()
