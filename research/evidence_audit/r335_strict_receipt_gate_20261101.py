"""Optimization-safe, independent finite E1 receipt verifier for frozen R335.

Requires the exact archived source and receipt blobs. Does not import the
original model and does not establish empirical groupthink mechanisms.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
from itertools import product
from pathlib import Path

SOURCE_BLOB = '9c005079716fe38eb4cb6d99730884a55e2795a3'
CSV_BLOB = 'f5987d4d9da8ef7532a3615b5f7fb6efbd4701cb'
JSON_BLOB = '4ab8f69cbd483099dd2a1be28cb052e1e3bdb279'
SOURCE_NAME = 'r335_groupthink.py'
CSV_NAME = 'R335_ALL_384_ARTIFICIAL_GROUP_ATOMS.csv'
JSON_NAME = 'R335_EXACT_128_CONDITIONS.json'
HEADER = ['policy','truth','s1','s2','s3','leader','pressure','audit',
          'public1','public2','public3','decision','correct']
FROZEN_CHECKS = {
    'rows':384, 'conditions':128, 'pressure_unanimous':64,
    'concealed_private_dissent':48, 'pressure0_matches_open':64,
    'pressure_overrides_majority':32, 'audit_changes_pressure':16,
    'correct_open':64, 'correct_pressure':64, 'correct_audit':80,
}


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def require(condition: bool, description: str) -> None:
    if not condition:
        raise ValueError(description)


def unique_keys(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: '+key)
        result[key] = value
    return result


def independent_oracle() -> tuple[list[list[str]], list[dict], dict]:
    """Enumerate public reports and outcomes using direct Boolean logic."""
    rows, worlds = [], []
    counts = {key:0 for key in FROZEN_CHECKS}
    for t,x,y,z,l,p,a in product(range(2), repeat=7):
        majority = int(x+y+z > 1)
        hidden = int(x==y==z)
        reports = (l,l,l) if p else (x,y,z)
        pressured = l if p else majority
        audited = t if p*a else pressured
        outcomes = (
            ('OPEN',(x,y,z),majority),
            ('PRESSURE',reports,pressured),
            ('AUDIT',reports,audited),
        )
        for name,public,decision in outcomes:
            rows.append([str(v) for v in (name,t,x,y,z,l,p,a,*public,decision,int(decision==t))])
        worlds.append({
            'truth':t,'s1':x,'s2':y,'s3':z,'leader':l,'pressure':p,'audit':a,
            'open_decision':majority,'pressure_decision':pressured,
            'audit_decision':audited,'open_correct':int(majority==t),
            'pressure_correct':int(pressured==t),'audit_correct':int(audited==t),
            'open_unanimous':hidden,'pressure_unanimous':int(bool(p) or bool(hidden)),
            'audit_unanimous':int(bool(p) or bool(hidden)),
        })
        counts['rows'] += 3
        counts['conditions'] += 1
        counts['pressure_unanimous'] += p
        counts['concealed_private_dissent'] += int(bool(p) and not hidden)
        counts['pressure0_matches_open'] += int(p==0)
        counts['pressure_overrides_majority'] += int(bool(p) and l!=majority)
        counts['audit_changes_pressure'] += int(audited!=pressured)
        counts['correct_open'] += int(majority==t)
        counts['correct_pressure'] += int(pressured==t)
        counts['correct_audit'] += int(audited==t)
    return rows, worlds, counts


def check(root: Path) -> dict:
    paths = [(root/SOURCE_NAME,SOURCE_BLOB), (root/CSV_NAME,CSV_BLOB),
             (root/JSON_NAME,JSON_BLOB)]
    for path, expected in paths:
        require(path.is_file(), 'missing '+path.name)
        require(git_blob(path.read_bytes()) == expected, 'Git blob mismatch: '+path.name)
    csv_bytes = paths[1][0].read_bytes()
    require(b'\r\n' in csv_bytes and csv_bytes.endswith(b'\r\n'), 'CSV line endings')
    parsed = list(csv.reader(io.StringIO(csv_bytes.decode('utf-8'),newline='')))
    require(len(parsed)==385 and parsed[0]==HEADER, 'CSV structure mismatch')
    expected_rows, expected_worlds, counts = independent_oracle()
    require(parsed[1:]==expected_rows, 'independent CSV state mismatch')
    require(counts==FROZEN_CHECKS, 'independent frozen summary mismatch')
    obj = json.loads(paths[2][0].read_text(encoding='utf-8'),object_pairs_hook=unique_keys)
    require(type(obj) is dict and set(obj)=={'schema','conditions','checks'}, 'JSON keys')
    require(obj['schema']=='R335_frozen_public_unanimity_v1', 'JSON schema')
    require(obj['conditions']==expected_worlds, 'independent JSON state mismatch')
    require(obj['checks']==FROZEN_CHECKS, 'JSON frozen summary mismatch')
    return {'status':'PASS_BOUNDED_E1_RECEIPT','worlds':128,'rows':384,
            'source_git_blob':SOURCE_BLOB,'csv_git_blob':CSV_BLOB,'json_git_blob':JSON_BLOB}


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]/'R335')
    args=parser.parse_args()
    try:
        print(json.dumps(check(args.root),sort_keys=True))
        return 0
    except (OSError,ValueError,UnicodeError,csv.Error) as exc:
        print('R335_STRICT_RECEIPT_FAIL: '+str(exc),file=sys.stderr)
        return 1


if __name__=='__main__':
    sys.exit(main())
