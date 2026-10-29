"""Byte-identity gate for R170 historical sources and the full B receipt.

No model execution, scientific acceptance, or historical execution attestation.
python -B identity_gate.py REPO_ROOT B_FULL_RECEIPT --output /tmp/identity.json
Use a distinct output for concurrent runs; it must not alias an input or this script.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import tempfile

PINS={
 'research/validation/r170_observation_ladder_20261026.js':'3ea018c4a113d95836873fcfd687f9df292aa1b7',
 'research/evidence_audit/r170_b_edge_utterance_20261026.py':'f6bd8574d6730b9c26708adb9e38ef88562eafbe',
 'research/validation/R170_OBSERVATION_LADDER_EXACT_RECEIPT_2026-10-26.json':'0d5b10125475a66a243be1632e21bd269027a866',
 'research/evidence_audit/B_R170_INDEPENDENT_PYTHON_EXECUTION_SUMMARY_2026-10-26.json':'165f14511c7c7ee57b43a18851d2e65729c50044',
}
PY='research/evidence_audit/r170_b_edge_utterance_20261026.py'
SUMMARY='research/evidence_audit/B_R170_INDEPENDENT_PYTHON_EXECUTION_SUMMARY_2026-10-26.json'
PIN_COMMIT='e2614fec5027247de328a5aeef295c4ed3bc9338'

def require(ok,message):
    if not ok:raise ValueError(message)

def verify(root,receipt):
    root,receipt=Path(root),Path(receipt)
    raw_sources={};identities={}
    for path,expected in PINS.items():
        raw=(root/path).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        require(blob==expected,'source identity mismatch: '+path)
        raw_sources[path]=raw
        identities[path]={'git_blob':blob,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
    summary=json.loads(raw_sources[SUMMARY])
    raw=receipt.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    require(type(summary['full_local_receipt_bytes']) is int and len(raw)==summary['full_local_receipt_bytes'],'receipt length mismatch')
    require(digest==summary['full_local_receipt_sha256'],'receipt digest mismatch')
    require(identities[PY]['sha256']==summary['script_sha256_local'],'historical Python source digest mismatch')
    return {'status':'COMPLETE','scope':'BYTE_IDENTITY_ONLY_NONBLIND',
            'pinned_commit':PIN_COMMIT,'source_files_verified':len(PINS),'sources':identities,
            'B_receipt_bytes':len(raw),'B_receipt_sha256':digest,
            'historical_source_digest_matches':True,
            'full_frozen_extension_acceptance':'PARTIAL',
            'historical_execution_time_authenticated':'NOT_ESTABLISHED',
            'model_execution_this_gate':'NOT_RUN','external_team_replications':0,
            'new_E2':0,'new_E3':0}

def main():
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('receipt',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    root,receipt,out=a.root.resolve(),a.receipt.resolve(),a.output.resolve()
    try:
        inputs=[root/path for path in PINS]+[receipt,Path(__file__).resolve()]
        require(out not in [path.resolve() for path in inputs],'output overlaps protected input')
        require(not out.exists() or not any(path.exists() and os.path.samefile(out,path) for path in inputs),'output aliases protected input')
        out.unlink(missing_ok=True)
        result=verify(root,receipt)
        result.update(python=sys.version,platform=platform.platform(),command=sys.argv,
                      gate_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
        out.parent.mkdir(parents=True,exist_ok=True)
        staged=None
        try:
            with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=out.parent,delete=False) as f:
                staged=Path(f.name);f.write(json.dumps(result,indent=2)+'\n')
            staged.replace(out)
        finally:
            if staged is not None:staged.unlink(missing_ok=True)
        print(json.dumps(result));return 0
    except (ValueError,OSError,KeyError) as e:
        print(json.dumps({'status':'PARTIAL','error':str(e),'identity_gate':'BLOCKED'}));return 1
if __name__=='__main__':sys.exit(main())
