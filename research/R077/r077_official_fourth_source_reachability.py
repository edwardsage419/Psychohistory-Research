#!/usr/bin/env python3
"""R077 fourth-human-experiment official archive reachability only.

Runs before any fourth-study actual human probability score. Does not inspect,
fit, or retain participants. Outputs anonymous HTTP/archive provenance only.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"R075"))
from r075_first_party_archive_probe import probe_one

SOURCES=(
  ("HUMAN_VS_AGENT_2026_OSF","https://osf.io/4htq3/"),
  ("HUMAN_VS_AGENT_2026_OSF_API","https://api.osf.io/v2/nodes/4htq3/files/"),
  ("ALGORITHMIC_COOPERATION_2026_PREREG","https://osf.io/zcv6x/"),
  ("ALGORITHMIC_COOPERATION_2026_OSF_API","https://api.osf.io/v2/nodes/zcv6x/files/"),
  ("PURE_MIXED_PD_2019_OSF","https://osf.io/p4dgz/"),
  ("PURE_MIXED_PD_2019_OSF_API","https://api.osf.io/v2/nodes/p4dgz/files/"),
)

def audit():
    result=[]
    for label,url in SOURCES:
        item=probe_one(label,url)
        # Exclude any unsafe metadata accidentally added by a webpage.
        allowed=("candidate","url","source_kind","status","http_status",
                 "content_type","response_bytes","sha256","redirect_final_host",
                 "archive","error_type")
        result.append({k:v for k,v in item.items() if k in allowed})
    return {
        "research_id":"R077",
        "status":"FOURTH_AUTHOR_SOURCE_ENDPOINT_ACCESS_AUDITED_ONLY",
        "source_gate":"protocols/R077_FOURTH_INDEPENDENT_HUMAN_DATA_SOURCE_AND_BLIND_SCORE_GATE_2026-10-17.md",
        "observations":result,
        "candidate_count":3,
        "candidate_target_study_score_computed":False,
        "fourth_original_session_field_verified":False,
        "source_model_frozen":"R073 Git blob c8a0b47fd27bf05e7be5b87419a0824355fc911a",
        "participant_rows_or_identifiers_exported":False,
        "R077_E3":"OPEN",
        "PESEN_v0.1":"FROZEN"
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=audit()
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps(result,sort_keys=True))

if __name__=="__main__":main()
