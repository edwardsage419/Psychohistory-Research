#!/usr/bin/env python3
"""Artificial issuer authorization and outcome truth separation. No real credentials."""
import hashlib
import hmac
import json
from copy import deepcopy
KEYS = {'SELF': b'local-artificial-key-a', 'REVIEWER': b'local-artificial-key-b'}
PERMISSIONS = {'SELF': {'self_report'}, 'REVIEWER': {'outcome_review'}}
def canon(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def issue(issuer, subject, kind, outcome, evidence, revision=1):
    payload = {'issuer': issuer, 'subject': subject, 'kind': kind,
               'outcome': outcome, 'evidence': evidence, 'revision': revision}
    return {'payload': payload, 'tag': hmac.new(KEYS[issuer], canon(payload), hashlib.sha256).hexdigest()}
def verify(record, expected_subject, evidence_ok, current_revision=1):
    p = record['payload']
    issuer = p.get('issuer')
    if issuer not in KEYS or not hmac.compare_digest(
        hmac.new(KEYS[issuer], canon(p), hashlib.sha256).hexdigest(), record['tag']
    ):
        return 'BAD_AUTHENTICITY'
    if p.get('subject') != expected_subject:
        return 'WRONG_SUBJECT'
    if p.get('revision') != current_revision:
        return 'STALE_STATUS'
    if p.get('kind') not in PERMISSIONS[issuer]:
        return 'UNAUTHORIZED_CLAIM'
    if p.get('kind') == 'self_report':
        return 'SELF_REPORTED_ONLY'
    if not evidence_ok:
        return 'EVIDENCE_UNKNOWN'
    return 'REVIEW_ELIGIBLE'
def run():
    tests = 0
    def check(condition, msg):
        nonlocal tests
        assert condition, msg
        tests += 1
    self_claim = issue('SELF', 'D1', 'self_report', 'SUCCESS', 'unverified')
    check(verify(self_claim, 'D1', True) == 'SELF_REPORTED_ONLY', 'self report')
    forged_authority = issue('SELF', 'D1', 'outcome_review', 'SUCCESS', 'claimed-review')
    check(verify(forged_authority, 'D1', True) == 'UNAUTHORIZED_CLAIM', 'issuer scope')
    reviewed = issue('REVIEWER', 'D1', 'outcome_review', 'FAILURE', 'synthetic-ledger-1')
    check(verify(reviewed, 'D1', True) == 'REVIEW_ELIGIBLE', 'review')
    check(verify(reviewed, 'D1', False) == 'EVIDENCE_UNKNOWN', 'evidence unknown')
    check(verify(reviewed, 'D2', True) == 'WRONG_SUBJECT', 'subject')
    check(verify(reviewed, 'D1', True, 2) == 'STALE_STATUS', 'revision')
    tampered = deepcopy(reviewed); tampered['payload']['outcome'] = 'SUCCESS'
    check(verify(tampered, 'D1', True) == 'BAD_AUTHENTICITY', 'tamper')
    relabel = deepcopy(reviewed); relabel['payload']['issuer'] = 'SELF'
    check(verify(relabel, 'D1', True) == 'BAD_AUTHENTICITY', 'relabel')
    fake_truth = issue('REVIEWER', 'D1', 'outcome_review', 'SUCCESS', 'synthetic-ledger-1')
    check(verify(fake_truth, 'D1', True) == 'REVIEW_ELIGIBLE', 'authentic claim can be false')
    check(fake_truth['payload']['outcome'] != reviewed['payload']['outcome'], 'conflicting claims')
    check(fake_truth['tag'] != reviewed['tag'], 'different authenticated bytes')
    check(len(canon(reviewed['payload'])) > 0, 'serialization')
    print(json.dumps({'status':'PASS_SYNTHETIC_E1','assertions':tests,
        'key_finding':'authenticated authorized claim may contradict another authenticated claim; truth unresolved',
        'not_w3c_vc_crypto':True}, sort_keys=True))
if __name__ == '__main__':
    run()
