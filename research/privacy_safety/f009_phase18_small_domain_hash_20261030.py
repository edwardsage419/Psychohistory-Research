#!/usr/bin/env python3
"""Synthetic low-cardinality audit metadata hash enumeration; no personal data."""
import hashlib
import hmac
import json

STATES = ('OPEN', 'PENDING', 'REVIEW', 'CLOSED')
DAYS = (0, 1, 2, 3)
DOMAIN = [f'{s}:{d}' for s in STATES for d in DAYS]
PUBLIC_SALT = 'public-demo-v1:'
DEMO_SECRET = b'demo-only-secret-never-deploy'


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def keyed(text, key):
    return hmac.new(key, text.encode('utf-8'), hashlib.sha256).hexdigest()


plain = {sha(x): x for x in DOMAIN}
salted = {sha(PUBLIC_SALT + x): x for x in DOMAIN}
receipts = [(x, sha(x), sha(PUBLIC_SALT + x), keyed(x, DEMO_SECRET)) for x in DOMAIN]
assert len(plain) == len(salted) == len(receipts) == 16
assert all(plain[a] == x and salted[b] == x for x, a, b, _ in receipts)
assert all(keyed(x, b'wrong-key') != digest for x, _, _, digest in receipts)
assert len({d for _, _, _, d in receipts}) == 16
assert all(len(a) == len(b) == len(d) == 64 for _, a, b, d in receipts)
assert len({a for _, a, _, _ in receipts}) == 16
assert len({b for _, _, b, _ in receipts}) == 16
assert all(a != b for _, a, b, _ in receipts)
print(json.dumps({'synthetic_domain_size':len(DOMAIN),'unsalted_dictionary_recovered':16,
 'public_salt_dictionary_recovered':16,'wrong_hmac_key_matches':0,
 'assertions':8,'real_personal_data':False,
 'limitation':'offline finite dictionary only; no cryptographic break; no legal anonymization determination'},indent=2))
