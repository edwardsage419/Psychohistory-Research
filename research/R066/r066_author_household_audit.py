#!/usr/bin/env python3
"""R066: post-failure author-algorithm-derived household network source audit.

The program builds in-memory household edges but emits ONLY aggregated counts.
It does not claim exact parity with author's igraph network or fit any model.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math
from collections import Counter,defaultdict
from pathlib import Path
from r066_larson_lewis_semantic_mapping import PINNED_SHA256
from r066_larson_lewis_public_schema import FILES
from r066_larson_lewis_join_gate import ITEMS,WAVES,NETWORKS,MISSING,clean_id,parse_response

MEMBERS=("ego","hhh")+tuple("hh"+str(i) for i in range(1,12))
LIMIT_EDGES=500_000


def sort_hhnum(value: str):
    try:
        return (0,float(value))
    except (TypeError,ValueError):
        return (1,str(value))


def summarize_author_households(rows: list[dict]):
    if len(rows)!=2125:
        raise ValueError("source universe mismatch")
    by_village=defaultdict(list)
    for row in rows:
        village=clean_id(row["village_number"])
        if village is None:
            raise ValueError("missing village")
        by_village[village].append(row)
    if len(by_village)!=16:
        raise ValueError("village universe mismatch")
    network_counts={name:Counter() for name in NETWORKS}
    node_sets={name:set() for name in NETWORKS}
    merged_edges=set()
    shared_member_ids=0
    repeated_hhnums=0
    # Nodes are indexed by the row's position *within a sorted village*.
    for village,records in by_village.items():
        records=sorted(records,key=lambda d:sort_hhnum(d["hhnum"]))
        hhnums=[r["hhnum"] for r in records]
        repeated_hhnums+=len(hhnums)-len(set(hhnums))
        household_aliases=defaultdict(set)
        for i,row in enumerate(records):
            members={clean_id(row[k]) for k in MEMBERS}
            members.discard(None)
            if not members:
                raise ValueError("empty household")
            for alias in members:
                household_aliases[alias].add(i)
        shared_member_ids+=sum(len(nodes)>1 for nodes in household_aliases.values())
        for network,cols in NETWORKS.items():
            local_edges=set()
            counter=network_counts[network]
            for row in records:
                ego=clean_id(row["ego"])
                for col in cols:
                    alter=clean_id(row[col])
                    if alter is None:
                        continue
                    counter["nonmissing_nomination_slots"]+=1
                    src=household_aliases.get(ego,set())
                    dst=household_aliases.get(alter,set())
                    if not src:
                        counter["nominations_without_ego_household"]+=1
                    if not dst:
                        counter["nominations_without_alter_household"]+=1
                    if not src or not dst:
                        counter["unconverted_nominations"]+=1
                        continue
                    counter["nominations_with_both_households"]+=1
                    for u in src:
                        for v in dst:
                            counter["expanded_household_pairs"]+=1
                            if u==v:
                                counter["self_pairs_removed"]+=1
                                continue
                            link=(u,v) if u<v else (v,u)
                            local_edges.add(link)
                            if len(local_edges)>LIMIT_EDGES:
                                raise ValueError("expanded source household edges exceed cap")
            counter["unique_undirected_household_edges"]+=len(local_edges)
            nodes=set()
            for u,v in local_edges:
                nodes.update((u,v))
                merged_edges.add((village,u,v))
            counter["household_nodes_with_edge"]+=len(nodes)
            node_sets[network].update((village,x) for x in nodes)
    all_nodes_count=2125
    union_nodes=set()
    for category in node_sets:
        union_nodes|=node_sets[category]
    out={}
    for name in NETWORKS:
        cnt=network_counts[name]
        total=cnt["nonmissing_nomination_slots"]
        out[name]={
            "nonmissing_nomination_slots":total,
            "nominations_converted_to_household_edges":cnt["nominations_with_both_households"],
            "nominations_not_convertible":cnt["unconverted_nominations"],
            "expanded_household_pairs":cnt["expanded_household_pairs"],
            "self_pairs_removed":cnt["self_pairs_removed"],
            "unique_undirected_household_edges":cnt["unique_undirected_household_edges"],
            "household_nodes_with_at_least_one_edge":cnt["household_nodes_with_edge"],
            "conversion_fraction":cnt["nominations_with_both_households"]/total if total else None
        }
    scores={}
    full_at_both=set()
    by_wave={}
    for phase,suffix in WAVES.items():
        arr=[]
        indices=set()
        for i,row in enumerate(rows):
            values=[parse_response(row[k+suffix]) for k in ITEMS]
            if all(status=="within_1_5" for status,_ in values):
                scoresum=math.fsum(val for _,val in values)
                if not 6<=scoresum<=30:
                    raise ValueError("six item sum outside codebook 6-30 scale")
                arr.append(scoresum)
                indices.add(i)
        by_wave[phase]=indices
        scores[phase]={"complete_items":len(arr),"index_min":min(arr) if arr else None,
                       "index_max":max(arr) if arr else None}
    return {
        "village_count":len(by_village),
        "record_count":len(rows),
        "ambiguous_person_identifiers_shared_by_multiple_households":shared_member_ids,
        "repeated_hhnum_within_village":repeated_hhnums,
        "author_algorithm_derived_household_networks":out,
        "all_types_union_unique_household_edges":len(merged_edges),
        "union_household_nodes_with_edge":len(union_nodes),
        "union_household_nodes_without_edge":all_nodes_count-len(union_nodes),
        "six_item_author_code_sum_6_to_30":scores,
        "candidate_baseline_and_endline_complete":len(
            by_wave["candidate_baseline"] & by_wave["candidate_endline"]),
        "status":"AUTHOR_ALGORITHM_DERIVED_HOUSEHOLD_GRAPH_AGGREGATE",
        "original_R_igraph_exact_edge_parity":"NOT_TESTED",
        "real_model_fit_performed":False,
        "source_person_ids_and_edges_emitted":False,
    }


def audit_files(folder:Path):
    data={}
    for label,(name,_,size) in FILES.items():
        raw=(folder/name).read_bytes()
        if len(raw)!=size or hashlib.sha256(raw).hexdigest()!=PINNED_SHA256[label]:
            raise ValueError("source SHA/size mismatch "+label)
        data[label]=raw
    reader=csv.DictReader(io.StringIO(data["data"].decode("utf-8-sig"),newline=""),delimiter="\t")
    if reader.fieldnames is None or len(reader.fieldnames)!=66:
        raise ValueError("expected 66 fields")
    rows=list(reader)
    if any(None in row or any(v is None for v in row.values()) for row in rows):
        raise ValueError("bad tabular row")
    out=summarize_author_households(rows)
    return {"study":"R066","stage":"E2_ORIGINAL_AUTHOR_HOUSEHOLD_NETWORK_AUDIT",
            "doi":"doi:10.7910/DVN/RAHSVM","version":"1.0",
            "pinned_sha256":PINNED_SHA256,
            "scope":"POST_FAILURE_SOURCE_DEFINED_HOUSEHOLD_NETWORK_RECONSTRUCTION",
            "source_integrity":"PASS",
            "anonymous_aggregate":out,
            "empirical_model_validation":"OPEN",
            "pesen_v01":"FROZEN"}


def main():
    a=argparse.ArgumentParser()
    a.add_argument("--source-dir",type=Path,required=True)
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args()
    try:
        x=audit_files(args.source_dir)
    except (ValueError,OSError,UnicodeError,csv.Error) as e:
        x={"study":"R066","stage":"E2_ORIGINAL_AUTHOR_HOUSEHOLD_NETWORK_AUDIT",
           "source_integrity":"FAIL_CLOSED","reason_type":type(e).__name__,
           "reason":str(e)[:220],"pesen_v01":"FROZEN"}
    args.output.write_text(json.dumps(x,indent=2)+"\n",encoding="utf-8")
    r=x.get("anonymous_aggregate",{})
    print(json.dumps({"stage":x["stage"],"status":x["source_integrity"],
                      "village_count":r.get("village_count"),
                      "original_ego_duplicates_explained_by_household_alias_mapping":r.get("ambiguous_person_identifiers_shared_by_multiple_households"),
                      "union_unique_household_edges":r.get("all_types_union_unique_household_edges"),
                      "six_item_complete_pairs":r.get("candidate_baseline_and_endline_complete"),
                      "edge_counts":{k:v["unique_undirected_household_edges"]
                                    for k,v in r.get("author_algorithm_derived_household_networks",{}).items()}},
                     sort_keys=True))
    if x["source_integrity"]!="PASS":
        raise RuntimeError("failed author-equivalent household network audit")


if __name__=="__main__":
    main()
