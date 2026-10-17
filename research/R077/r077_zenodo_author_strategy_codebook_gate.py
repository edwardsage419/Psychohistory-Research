#!/usr/bin/env python3
"""R077 author source Stata code semantics, no fourth-human model scores."""
from __future__ import annotations
import argparse,hashlib,io,json,re,pathlib
from urllib.request import Request,urlopen

PUBLISHER="https://zenodo.org/records/15462528/files/"
SCRIPTS={"number 1.do":"0ee6ace76d2ea9a8daf7ab1f7ef026e6",
         "number 2.do":"563263f55bb3a7a1910b3b38e85fe22c",
         "power.do":"3464cb2e28d3e05d6296d09f88b159cf"}
DTA="https://zenodo.org/records/15462528/files/cleandata.dta?download=1"
DTA_MD5="4cce04ea68b7a0492c242b206efebe53"
TOKEN_RE=re.compile(r"\b(?:session|subject|period|cooperat|collus|decision|partner|matched|group|choice|partici|strategy|game|treat|round|outcome|payoff|leader|left|defect|pair|client|B)\b",re.I)
def fetch(url,maxbytes=3_000_000):
    with urlopen(Request(url,headers={
        "User-Agent":"Psychohistory-R077-PearceDrouvelis-author-syntax-nonhuman/1.0"}),timeout=60) as r:
        b=r.read(maxbytes+1)
        if len(b)>maxbytes:raise ValueError("AUTHOR_DOWNLOAD_UNEXPECTEDLY_LARGE")
        return b

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--private-dir",type=pathlib.Path,required=True)
    p.add_argument("--output",type=pathlib.Path,required=True)
    a=p.parse_args()
    result={"stage":"R077_FOURTH_AUTHOR_CODE_AND_DICTIONARY_NO_OUTCOME_MODEL",
            "source":"Drouvelis Pearce 2025 original Zenodo v1",
            "script_snapshots":{},"stata_variable_labels":{},
            "treatment_grouping_condition_counts":{},
            "target_semantics_not_established":True,
            "human_model_scores":"NOT_RUN","individual_rows_emitted":False}
    for name,md5 in SCRIPTS.items():
        b=fetch(PUBLISHER+name.replace(" ","%20")+"?download=1",100_000)
        if hashlib.md5(b).hexdigest()!=md5:raise ValueError("AUTHOR_SCRIPT_MD5_FAIL:"+name)
        script=b.decode("utf-8-sig",errors="replace").splitlines()
        hits=[]
        for line_num,line in enumerate(script,1):
            s=line.strip()
            if len(s)>150 or "http" in s.lower() or ".dta" in s.lower() or "@ " in s:
                continue
            if not TOKEN_RE.search(s):continue
            if not re.match(r"^(?:gen|generate|replace|rename|drop|keep|by |bys|egen|xtset|sort|order|tab|table|preserve|assert|isid|label|merge|collapse|reshape|logit|probit|reg|regress|xtreg|xtlogit|gls|forval|foreach|egen|use|import|local|global|/\*|\*|//)",s,re.I):
                continue
            if re.search(r"(/[a-zA-Z]|[A-Z]:\\|[$][A-Z])",s):continue
            hits.append({"n":line_num,"line":s})
        result["script_snapshots"][name]={"md5":md5,"lines_total":len(script),
            "relevant_source_statements":hits[:50]}
    blob=fetch(DTA)
    if hashlib.md5(blob).hexdigest()!=DTA_MD5:raise ValueError("AUTHOR_DTA_MD5_FAIL")
    a.private_dir.mkdir(parents=True,exist_ok=True)
    f=a.private_dir/"author_data.dta"
    f.write_bytes(blob)
    import pandas as pd
    reader=pd.io.stata.StataReader(f)
    labels=reader.variable_labels()
    for name,label in labels.items():
        if name in ("Session","B","Period","Subject","ClientNumber","LastClientNumber",
            "Group","Participate","realperiod","game","treatment","ID","part",
            "e","g","x","y","s","t","counter","Profit","otherprofit","left","otherleft"):
            # author field descriptions, no raw person rows
            result["stata_variable_labels"][name]=str(label)[:110]
    data=reader.read(convert_categoricals=False)
    for name in ("B","Participate","Period","realperiod","realrounds","game","treatment","part","Session","Group","ClientNumber","Subject","e","g","x","y","s","t"):
        if name in data:
            v=data[name]
            result["treatment_grouping_condition_counts"][name]={
                "unique_values":int(v.nunique(dropna=True)),
                "missing":int(v.isna().sum())
            }
            # only publish small numeric binary/action/treatment domain counts, not actual IDs
            if name in ("B","Participate","treatment","part","e","g","s","t","realrounds"):
                counts=v.value_counts(dropna=False)
                if len(counts)<=8:
                    result["treatment_grouping_condition_counts"][name]["domain_counts"]={
                        str(k):int(x) for k,x in counts.items()}
    result["author_DTA_sha256"]=hashlib.sha256(blob).hexdigest()
    result["original_source_rows"]=len(data)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,sort_keys=True))
if __name__=="__main__":main()
