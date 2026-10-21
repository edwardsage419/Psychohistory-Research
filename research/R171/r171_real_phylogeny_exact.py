"""R171 auditable exact distances of a *previously published* linguistic tree.

Input: exact original Phlorest Gray et al. 2009 (Science) CLDF artifacts.
Derived source dataset CC BY 4.0, cite Gray et al. 2009 AND Phlorest.
This is a descriptive audit of authors' inferred tree, not independent
historical phylogeny inference or a demographic migration prediction.
"""
from __future__ import annotations

from collections import Counter
from decimal import Decimal, getcontext
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import csv
import hashlib
import io
import json
import re
import sys

getcontext().prec=50
ORIGINAL_REPO="phlorest/gray_et_al2009"
SOURCE_COMMIT="a2e535f07c05d214fe7d36fe03747f4cfd5f9ca5"
ORIGINAL_DOI="10.1126/science.1166858"
BLOB_SHA1={
    "summary.trees":"89139751991c9f5753d249baeb9230061db93a4d",
    "languages.csv":"3e48ef314a10d9684af6a47279e7a8df54b45f5a",
    "trees.csv":"b4626d14b127b8197fb68c569016f53d033969e3",
    "Generic-metadata.json":"4be59bc5d99841796c04ba20bc98538d9c8e06f4",
}
EXPECTED_BYTES={"summary.trees":10954,"languages.csv":23461,
                "trees.csv":65932,"Generic-metadata.json":15415}
SOURCE=Path(__file__).resolve().parent/"source"
PAIRS=(
    ("SquliqAtayal","CiuliAtayal"),
    ("SquliqAtayal","Sediq"),
    ("Saisiat","Pazeh"),
    ("Pazeh","Thao"),
    ("Bali","Sasak"),
    ("MalayBahasaIndonesia","Melayu"),
    ("Kanakanabu","Saaroa"),
    ("Rukai","Tsou"),
    ("OldChinese","Buyang"),
)


def git_blob_id(raw:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest()


def verify_input(filename,raw):
    if filename not in BLOB_SHA1 or not isinstance(raw,bytes):
        raise ValueError("unregistered source or non-byte source")
    actual=git_blob_id(raw)
    if actual!=BLOB_SHA1[filename] or len(raw)!=EXPECTED_BYTES[filename]:
        raise ValueError(f"Original {filename} differs from pinned Git blob and size: {actual}, {len(raw)}")
    return {"git_blob_sha1":actual,"sha256":hashlib.sha256(raw).hexdigest(),
            "bytes":len(raw),"original_path":"cldf/"+filename}


def fetch_sources():
    SOURCE.mkdir(parents=True,exist_ok=True)
    for name in BLOB_SHA1:
        url=f"https://raw.githubusercontent.com/{ORIGINAL_REPO}/{SOURCE_COMMIT}/cldf/{name}"
        request=Request(url,headers={"User-Agent":"Psychohistory-R171-original-source-audit/1.0"})
        with urlopen(request,timeout=45) as response:
            resolved=response.geturl()
            if urlparse(resolved).hostname!="raw.githubusercontent.com":
                raise ValueError("source redirect outside approved raw.githubusercontent.com")
            raw=response.read(EXPECTED_BYTES[name]+1)
        identity=verify_input(name,raw)
        (SOURCE/name).write_bytes(raw)
        print("PINNED_ORIGINAL_SOURCE_VERIFIED",name,json.dumps(identity,sort_keys=True))


def read_sources():
    output={}
    for name in BLOB_SHA1:
        raw=(SOURCE/name).read_bytes()
        output[name]=raw
        verify_input(name,raw)
    return output


def newick_from_nexus(raw):
    source=raw.decode("utf-8-sig")
    lines=[s.strip() for s in source.splitlines() if s.strip()]
    if len(lines)!=4 or lines[0].upper()!="#NEXUS" or lines[1].upper()!="BEGIN TREES;" or lines[-1].upper()!="END;":
        raise ValueError("source NEXUS does not have exact expected header, tree statement and end")
    match=re.fullmatch(r"tree\s+summary\s*=\s*\[&R\]\s*(.+);",lines[2],re.I|re.S)
    if not match:raise ValueError("rooted NEXUS summary declaration absent or malformed")
    newick=match.group(1).strip()+";"
    if "[" in newick or "]" in newick:raise ValueError("unsupported hidden tree annotations")
    return newick


def length_exact(token):
    if not isinstance(token,str) or not token:
        raise ValueError("missing branch length")
    try:length=Decimal(token)
    except Exception as exc:raise ValueError("malformed decimal branch length") from exc
    if not length.is_finite() or length<0:raise ValueError("branch length must be finite nonnegative")
    return length


def parse_recursive(newick):
    """Oracle 1: punctuation tokenized recursive-descent parse, no tree library."""
    chunks=re.findall(r"\s*([(),:;]|[^\s(),:;]+)",newick)
    if "".join(chunks)!=re.sub(r"\s+","",newick):
        raise ValueError("unexpected tree lexical characters")
    index=0

    def node():
        nonlocal index
        if index>=len(chunks):raise ValueError("truncated tree")
        children=[]
        label=None
        if chunks[index]=="(":
            index+=1
            children.append(node())
            while index<len(chunks) and chunks[index]==",":
                index+=1
                children.append(node())
            if index>=len(chunks) or chunks[index]!=")":
                raise ValueError("unbalanced parenthesis")
            index+=1
            if len(children)<2:raise ValueError("internal split needs at least two children")
        elif chunks[index] in (")",",",":",";"):
            raise ValueError("empty or punctuation-only taxon label")
        if index<len(chunks) and chunks[index] not in ("(",")",",",":",";"):
            label=chunks[index]
            index+=1
        if not children and not label:raise ValueError("missing terminal name")
        length=None
        if index<len(chunks) and chunks[index]==":":
            index+=1
            if index>=len(chunks):raise ValueError("missing length token")
            length=length_exact(chunks[index])
            index+=1
        return (label,length,tuple(children))

    root=node()
    if index!=len(chunks)-1 or chunks[index]!=";":
        raise ValueError("trailing nodes or missing semicolon")
    return root


def parse_iterative(newick):
    """Oracle 2: separate character scanner and iterative stack reduction.

    Neither calls parse_recursive nor uses its punctuation-tokenization logic.
    """
    toks=[]
    i=0
    specials="(),:;"
    while i<len(newick):
        ch=newick[i]
        if ch.isspace():i+=1;continue
        if ch in specials:toks.append(ch);i+=1;continue
        if ch=="'":
            i+=1;start=i
            while i<len(newick) and newick[i]!="'":i+=1
            if i>=len(newick):raise ValueError("unterminated quoted label")
            toks.append(newick[start:i]);i+=1;continue
        start=i
        while i<len(newick) and newick[i] not in specials and not newick[i].isspace():
            i+=1
        toks.append(newick[start:i])
    stack=[]
    cursor=0
    def suffix(pos):
        label=None
        if pos<len(toks) and toks[pos] not in specials:
            label=toks[pos];pos+=1
        length=None
        if pos<len(toks) and toks[pos]==":":
            if pos+1>=len(toks):raise ValueError("missing length")
            length=length_exact(toks[pos+1]);pos+=2
        return label,length,pos

    while cursor<len(toks):
        token=toks[cursor]
        if token=="(":
            stack.append("(");cursor+=1
        elif token==",":
            if not stack or stack[-1]=="(":raise ValueError("empty internal child")
            cursor+=1
        elif token==")":
            rev=[]
            while stack and stack[-1]!="(":
                rev.append(stack.pop())
            if not stack or len(rev)<2:raise ValueError("unbalanced/reduced internals")
            stack.pop()
            label,length,cursor=suffix(cursor+1)
            stack.append((label,length,tuple(reversed(rev))))
        elif token==";":
            if cursor!=len(toks)-1 or len(stack)!=1 or stack[0]=="(":
                raise ValueError("bad root termination")
            return stack[0]
        elif token==":":
            raise ValueError("orphan branch punctuation")
        else:
            label,length,cursor=suffix(cursor)
            if not label:raise ValueError("terminal name expected")
            stack.append((label,length,()))
    raise ValueError("missing end-of-tree semicolon")


def flatten(root):
    """Create indexed source trees, parent pointers, unique leaf names."""
    nodes=[];parent=[];length=[];children=[];names={}
    def visit(t,p):
        label,edge,kids=t
        idx=len(nodes)
        nodes.append(label)
        parent.append(p)
        length.append(edge)
        children.append([])
        if p is not None:
            if edge is None:raise ValueError("every non-root edge must be explicitly dated")
            children[p].append(idx)
        elif edge is not None:
            raise ValueError("root branch length is not meaningful in this audit")
        if not kids:
            if not label or label in names:raise ValueError("duplicate or empty tip label")
            names[label]=idx
        elif len(kids)<2:
            raise ValueError("internal unary degree invalid")
        for k in kids:visit(k,idx)
    visit(root,None)
    return {"node_labels":nodes,"parent":parent,"length":length,
            "children":children,"tips":names}


def root_depths(flat):
    depth=[Decimal(0)]*len(flat["parent"])
    for i in range(1,len(depth)):
        depth[i]=depth[flat["parent"][i]]+flat["length"][i]
    return depth


def lca_distance(flat,depth,tip_a,tip_b):
    nodes=flat["tips"];parent=flat["parent"]
    if tip_a not in nodes or tip_b not in nodes:raise ValueError("unknown taxon")
    i=nodes[tip_a];j=nodes[tip_b]
    ancestors=set()
    current=i
    while current is not None:
        ancestors.add(current)
        current=parent[current]
    common=j
    while common not in ancestors:
        common=parent[common]
        if common is None:raise AssertionError("disconnected rooted tree")
    return depth[i]+depth[j]-2*depth[common]


def independent_undirected_paths(flat,origin):
    """Oracle 2 for distances: independently traverse undirected link graph."""
    if origin not in flat["tips"]:raise ValueError("missing origin")
    p=flat["parent"];edge=flat["length"]
    adjacency=[[] for _ in p]
    for j in range(1,len(p)):
        i=p[j]
        adjacency[i].append((j,edge[j]))
        adjacency[j].append((i,edge[j]))
    source=flat["tips"][origin]
    seen={}
    stack=[(source,Decimal(0))]
    while stack:
        at,d=stack.pop()
        if at in seen:raise ValueError("tree graph contains a cycle")
        seen[at]=d
        for to,weight in adjacency[at]:
            if to not in seen:stack.append((to,d+weight))
    if len(seen)!=len(p):raise ValueError("incomplete tree graph")
    return {label:seen[idx] for label,idx in flat["tips"].items()}


def taxon_crosswalk(language_bytes,tree_tip_ids):
    text=language_bytes.decode("utf-8-sig")
    reader=csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or "ID" not in reader.fieldnames:
        raise ValueError("missing CLDF language ID")
    rows=list(reader)
    ids=[r["ID"] for r in rows]
    if any(not x for x in ids) or len(ids)!=len(set(ids)):
        raise ValueError("empty or duplicate CLDF IDs")
    tree_set=set(tree_tip_ids)
    table_set=set(ids)
    shared=tree_set&table_set
    return {"language_rows":len(rows),"tree_tips":len(tree_set),
            "common_taxon_ids":len(shared),
            "tree_only_ids":sorted(tree_set-table_set),
            "language_table_only_ids":sorted(table_set-tree_set),
            "tree_tip_coverage_fraction":str(Decimal(len(shared))/Decimal(len(tree_set))),
            "language_row_coverage_fraction":str(Decimal(len(shared))/Decimal(len(table_set)))}


def source_metadata_check(sources):
    tree_rows=list(csv.DictReader(io.StringIO(sources["trees.csv"].decode("utf-8-sig"))))
    summary=[row for row in tree_rows if row.get("ID")=="summary"]
    if len(summary)!=1:raise ValueError("missing unique CLDF summary tree")
    row=summary[0]
    if row.get("Tree_Branch_Length_Unit")!="millennia" or row.get("Media_ID")!="summary":
        raise ValueError("unexpected original CLDF tree-unit or media")
    meta=json.loads(sources["Generic-metadata.json"].decode("utf-8-sig"))
    tables={entry["url"] for entry in meta.get("tables",[])}
    if "languages.csv" not in tables or "trees.csv" not in tables:
        raise ValueError("missing CLDF reference table declaration")
    return {"rooted_NEXUS_marker":"[&R]","CLDF_rooted_field":row.get("Tree_Is_Rooted",""),
            "CLDF_branch_length_unit":row["Tree_Branch_Length_Unit"],
            "CLDF_media_ID":row["Media_ID"],
            "CLDF_source_ID":row.get("Source"),
            "CLDF_tables_present":sorted(tables)}


def save_and_document():
    raw=read_sources()
    newick=newick_from_nexus(raw["summary.trees"])
    recursive=parse_recursive(newick)
    iterative=parse_iterative(newick)
    if recursive!=iterative:raise AssertionError("independent parse topology/length mismatch")
    flat=flatten(recursive)
    tip_names=sorted(flat["tips"])
    cross=taxon_crosswalk(raw["languages.csv"],tip_names)
    info=source_metadata_check(raw)
    depth=root_depths(flat)
    tip_heights=sorted(depth[flat["tips"][x]] for x in tip_names)
    lengths=[v for v in flat["length"] if v is not None]
    polytomy_sizes=[len(x) for x in flat["children"] if len(x)>2]
    all_pair_count=0
    minimum=None;maximum=None;sum_dist=Decimal(0);maximum_pair=None
    by_pair={}
    out=io.StringIO()
    writer=csv.writer(out,lineterminator="\n")
    writer.writerow(["taxon_A","taxon_B","patristic_distance_millennia"])
    for i,source in enumerate(tip_names):
        via_graph=independent_undirected_paths(flat,source)
        if via_graph[source]!=0:raise AssertionError("nonzero diagonal")
        for target in tip_names[i+1:]:
            d=lca_distance(flat,depth,source,target)
            if d!=via_graph[target] or d<0:
                raise AssertionError(f"patristic oracle mismatch: {source},{target}")
            writer.writerow([source,target,str(d)])
            all_pair_count+=1
            sum_dist+=d
            if minimum is None or d<minimum:minimum=d
            if maximum is None or d>maximum:
                maximum=d
                maximum_pair=[source,target]
            if (source,target) in PAIRS:by_pair[(source,target)]=str(d)
            if (target,source) in PAIRS:by_pair[(target,source)]=str(d)
    full_matrix=out.getvalue().encode("utf-8")
    matrix_path=Path(__file__).with_name("R171_ALL_PAIR_PATRISTIC_DISTANCES.csv")
    matrix_path.write_bytes(full_matrix)
    selected=[{"taxon_A":a,"taxon_B":b,
               "distance_millennia":by_pair.get((a,b)),
               "tip_pair_found":(a,b) in by_pair}
              for a,b in PAIRS]
    if all_pair_count!=len(tip_names)*(len(tip_names)-1)//2:
        raise AssertionError("missing pairwise distances")
    return {
        "research_id":"R171",
        "scientific_status":"E1_SOURCE_DESCRIPTIVE_REAL_PUBLISHED_TREE_NOT_HISTORICAL_PREDICTION",
        "source_paper_DOI":ORIGINAL_DOI,
        "source_GitHub_commit":SOURCE_COMMIT,
        "Phlorest_repository":ORIGINAL_REPO,
        "license":"CC-BY-4.0, cite original and derived dataset",
        "source_identities":{name:verify_input(name,contents) for name,contents in raw.items()},
        "metadata_audit":info,
        "crosswalk":cross,
        "tree_summary":{
            "tree_labels_are_observed_source":True,
            "independent_parsers_exact_same_full_tree":True,
            "branch_length_units":"millennia",
            "leaf_count":len(tip_names),
            "total_nodes":len(flat["parent"]),
            "internal_nodes":len(flat["parent"])-len(tip_names),
            "branch_count":len(lengths),
            "root_outdegree":len(flat["children"][0]),
            "polytomy_count":len(polytomy_sizes),
            "max_polytomy_children":max(polytomy_sizes,default=0),
            "zero_length_branch_count":sum(v==0 for v in lengths),
            "total_branch_length":str(sum(lengths,Decimal(0))),
            "minimum_tip_root_height":str(tip_heights[0]),
            "median_tip_root_height":str(
                (tip_heights[(len(tip_heights)-1)//2]+tip_heights[len(tip_heights)//2])/2),
            "maximum_tip_root_height":str(tip_heights[-1])
        },
        "complete_pairwise_distances":{
            "number_of_unordered_pairs":all_pair_count,
            "independent_all_pairs_ancestry_and_graph_walk_equal":True,
            "original_full_matrix_csv_file":matrix_path.name,
            "original_full_matrix_csv_bytes":len(full_matrix),
            "original_full_matrix_csv_sha256":hashlib.sha256(full_matrix).hexdigest(),
            "minimum_distance":str(minimum),
            "mean_distance":str(sum_dist/Decimal(all_pair_count)),
            "maximum_distance":str(maximum),
            "one_farthest_pair":maximum_pair
        },
        "preregistered_original_language_tip_pairs":selected,
        "original_Bayesian_posterior_inference_reproduced":False,
        "original_population_migration_hypotheses_tested":False,
        "new_human_independent_predictions":0,
        "new_external_historical_predictions":0,
        "R073":"FROZEN","PESEN_v0_1":"FROZEN"
    }


def main():
    if len(sys.argv)==2 and sys.argv[1]=="--fetch-sources":
        fetch_sources()
        return
    if len(sys.argv)!=1:raise SystemExit("usage: python r171_real_phylogeny_exact.py [--fetch-sources]")
    print(json.dumps(save_and_document(),ensure_ascii=False,sort_keys=True,indent=2))


if __name__=="__main__":
    main()
