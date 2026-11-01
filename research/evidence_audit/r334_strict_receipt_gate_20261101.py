"""No-import, optimization-safe E1 receipt gate for frozen R334.

This checks the exact archived source and receipts plus independently reconstructed
finite arithmetic. It does not identify a real psychological mechanism.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import sys
from fractions import Fraction
from pathlib import Path

SOURCE_SHA = '7d232a07d9d2979c2fcc8a407dd8bda18cd8ab93'
CSV_SHA = '6e3bdcc5ca07d1321a651c29b899798a32f7fb72'
JSON_SHA = '02883b6b9cfc22b3b855d8a7cbaa5e5ddf6bd86c'
HEADER = ['model','a','b','j','c','m','latent_strain','post_attitude']
MODELS = ['DISSONANCE','RESPONSE_DEMAND','INCENTIVE']
CHECKS = {'rows':48,'conditions':16,'unchanged_conditions':12,
          'identical_reports':16,'latent_strain_disagreements':4,
          'low_justification_larger_dissonance_shifts':2,
          'high_justification_larger_incentive_shifts':2}

def blob_sha(b: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def require(cond: bool, message: str) -> None:
    if not cond:
        raise ValueError(message)

def reject_duplicate_keys(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, 'duplicate JSON key: '+key)
        out[key] = value
    return out

def check(root: Path) -> dict:
    files = [(root/'r334_dissonance.py',SOURCE_SHA),
             (root/'R334_ALL_48_ARTIFICIAL_CONTRAST_ATOMS.csv',CSV_SHA),
             (root/'R334_EXACT_16_CONDITIONS.json',JSON_SHA)]
    for path, expected in files:
        require(path.is_file(), 'missing file: '+path.name)
        require(blob_sha(path.read_bytes())==expected, 'Git blob mismatch: '+path.name)
    raw_csv=files[1][0].read_bytes()
    require(b'\r\n' in raw_csv and raw_csv.endswith(b'\r\n'), 'noncanonical CSV line endings')
    parsed=list(csv.reader(io.StringIO(raw_csv.decode('utf-8'), newline='')))
    require(parsed[0]==HEADER, 'CSV header mismatch')
    require(len(parsed)==49, 'CSV row count mismatch')
    expected_rows=[]
    expected_conditions=[]
    for a in (-1,1):
        for b in (-1,1):
            for j in (1,3):
                for c in (0,1):
                    mismatch=int(a!=b)
                    fraction=Fraction(c*mismatch,1+j)
                    y=Fraction(a)+(b-a)*fraction
                    yi=Fraction(a)+(b-a)*Fraction(c*mismatch*j,1+j)
                    for model in MODELS:
                        expected_rows.append([model,str(a),str(b),str(j),str(c),str(mismatch),
                            str(fraction if model=='DISSONANCE' else Fraction(0)),
                            str(yi if model=='INCENTIVE' else y)])
                    expected_conditions.append({'a':a,'b':b,'j':j,'c':c,
                        'post_dissonance':str(y),'post_response_demand':str(y),
                        'post_incentive':str(yi),'strain_dissonance':str(fraction),
                        'strain_response_demand':'0','strain_incentive':'0'})
    require(parsed[1:]==expected_rows,'independent row arithmetic mismatch')
    data=json.loads(files[2][0].read_text(encoding='utf-8'),object_pairs_hook=reject_duplicate_keys)
    require(type(data) is dict and set(data)=={'schema','conditions','checks'},'JSON top-level schema mismatch')
    require(data['schema']=='R334_frozen_induced_compliance_v1','JSON schema identity mismatch')
    require(data['conditions']==expected_conditions,'independent JSON condition arithmetic mismatch')
    require(data['checks']==CHECKS,'frozen falsifier summary mismatch')
    return {'source_git_blob':SOURCE_SHA,'csv_git_blob':CSV_SHA,'json_git_blob':JSON_SHA,
            'rows':len(expected_rows),'conditions':len(expected_conditions),'status':'PASS_BOUNDED_E1_RECEIPT'}

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]/'R334')
    args=p.parse_args()
    try:
        print(json.dumps(check(args.root),sort_keys=True))
        return 0
    except (ValueError,OSError,UnicodeError,json.JSONDecodeError,csv.Error) as exc:
        print('R334_STRICT_RECEIPT_FAIL: '+str(exc),file=sys.stderr)
        return 1

if __name__=='__main__':
    sys.exit(main())
