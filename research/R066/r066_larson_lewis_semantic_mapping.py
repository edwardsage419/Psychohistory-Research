#!/usr/bin/env python3
"""R066 schema-to-codebook/source-script evidence index, no individual data output."""
from __future__ import annotations
import argparse,csv,hashlib,io,json,re,zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET
from r066_larson_lewis_public_schema import FILES,scan_tabular,safe_header

PINNED_SHA256 = {
    "data":"10b3e31a6d160e003ff9edf96fc1f6e1a8549ea547b8b8b08aadab1f52b40cae",
    "script":"2e7b7b22887c69c057a6f2fa1a1ff393566826fdb19e6aad6360393ea9f86ff2",
    "codebook":"48741e3447d27fbf57bb54c995ff68c45ade21592c89e2454e71ab840fc8d161",
}
MISSING = frozenset(("", "NA", "NaN", "\\N", "."))
WORD = re.compile(r"\b(attitude|baseline|endline|neighbor|network|treatment|village|refugee|respondent)\b",re.I)
R_NETWORK_FNS = ("graph_from_data_frame","graph_from_edgelist",
                 "graph_from_adjacency_matrix","as_adjacency_matrix",
                 "graph_from_incidence_matrix","graph_from_graphnel",
                 "graph_from_literal","igraph","neighbors","degree",
                 "shortest_paths","distances","graph_from_atlas")


def exact_token_count(text:str, token:str)->int:
    return len(re.findall(r"(?<![A-Za-z0-9_])"+re.escape(token)+r"(?![A-Za-z0-9_])",text,re.I))


def docx_paragraphs(raw:bytes):
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            if z.testzip() is not None:
                raise ValueError("bad ZIP member")
            xml=z.read("word/document.xml")
    except (zipfile.BadZipFile,KeyError):
        raise ValueError("invalid codebook package") from None
    root=ET.fromstring(xml)
    ns="{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    return [" ".join((t.text or "") for t in p.findall(".//"+ns+"t")).strip()
            for p in root.findall(".//"+ns+"p")]


def audit_mapping(raw_data:bytes, raw_script:bytes, raw_codebook:bytes, *,pins=PINNED_SHA256):
    originals={"data":raw_data,"script":raw_script,"codebook":raw_codebook}
    for label,raw in originals.items():
        if hashlib.sha256(raw).hexdigest()!=pins[label] or len(raw)!=FILES[label][2]:
            raise ValueError("PINNED_SOURCE_SHA_OR_SIZE_MISMATCH: "+label)
    shape=scan_tabular(raw_data)
    if (shape["rows"],shape["columns"])!=(2125,66):
        raise ValueError("source universe must remain 2125x66")
    script=raw_script.decode("utf-8-sig")
    paragraphs=docx_paragraphs(raw_codebook)
    reader=csv.reader(io.StringIO(raw_data.decode("utf-8-sig"),newline=""),delimiter="\t")
    headers=next(reader)
    counts=Counter({k:0 for k in headers})
    for row in reader:
        if len(row)!=len(headers):
            raise ValueError("ragged row")
        for i,val in enumerate(row):
            if val in MISSING:
                counts[headers[i]]+=1
    dictionary=[]
    for h in headers:
        npara=[p for p in paragraphs if exact_token_count(p,h)>0]
        matched_topics=sorted(set(term.lower() for p in npara for term in WORD.findall(p)))
        dictionary.append({
            "source_column":safe_header(h),
            "missing_token_count":counts[h],
            "nonmissing_by_literal_token_rule":2125-counts[h],
            "codebook_paragraph_matches":len(npara),
            "codebook_context_topics":matched_topics,
            "r_script_exact_identifier_occurrences":exact_token_count(script,h),
        })
    funcs={name:exact_token_count(script,name) for name in R_NETWORK_FNS}
    return {
        "stage":"R066_E2_LARSON_LEWIS_SEMANTIC_MAPPING",
        "source":"doi:10.7910/DVN/RAHSVM", "version":"1.0",
        "pinned_sha256":pins, "rows":2125,"columns":66,
        "variable_index":dictionary,
        "r_script_network_token_counts":funcs,
        "codebook_nonempty_paragraphs":sum(bool(p) for p in paragraphs),
        "all_original_content_private_to_runner":True,
        "identity_linkage_contract":"NOT_ESTABLISHED_BY_STATIC_MAPPING",
        "attitude_measurement_mapping":"NOT_ESTABLISHED_BY_STATIC_MAPPING",
        "network_adjacency_join":"NOT_ESTABLISHED_BY_STATIC_MAPPING",
        "model_identification_ready":"OPEN",
        "real_fit_performed":False,
        "pesen_v01":"FROZEN",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-dir",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    try:
        data={key:(args.source_dir/name).read_bytes()
              for key,(name,_,_) in FILES.items()}
        out=audit_mapping(data["data"],data["script"],data["codebook"])
    except (ValueError,OSError,UnicodeError,csv.Error,ET.ParseError) as e:
        out={"stage":"R066_E2_LARSON_LEWIS_SEMANTIC_MAPPING",
             "status":"FAIL_CLOSED",
             "reason_type":type(e).__name__,
             "model_identification_ready":"OPEN",
             "real_fit_performed":False,"pesen_v01":"FROZEN"}
    else:
        out["status"]="VARIABLE_INDEX_COMPUTED"
    args.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":out["status"],"cols":out.get("columns"),
                      "columns":[x["source_column"] for x in out.get("variable_index",[])],
                      "codebook_matches":sum(x["codebook_paragraph_matches"] for x in out.get("variable_index",[])),
                      "network_function_tokens":out.get("r_script_network_token_counts")},
                     sort_keys=True))
    if out["status"]!="VARIABLE_INDEX_COMPUTED":
        raise RuntimeError("source mapping failed; no empirical model claim")


if __name__=="__main__":
    main()
