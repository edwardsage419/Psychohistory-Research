"""MKT161 bounded synthetic manifest replay. Python 3.11+ stdlib only.
The model is not the ActivityWatch Rust implementation or a deployed exploit.
"""
import hashlib
import json

checks = 0

def require(condition, label):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(label)

def digest(payload):
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()

def manifest(epoch, payload):
    return {'format_v': 1, 'epoch': epoch, 'segment': 'sealed.jsonl.zst',
            'sha256': digest(payload), 'sealed': True}

def local_integrity(m, payload):
    return m['format_v'] == 1 and m['sealed'] and m['sha256'] == digest(payload)

def anchored_integrity(m, payload, trusted_epoch):
    return local_integrity(m, payload) and m['epoch'] >= trusted_epoch

old = '{"event":"A","state":"present"}'
current = '{"event":"A","state":"deleted"}'
m2 = manifest(2, old)
m3 = manifest(3, current)
require(local_integrity(m3, current), 'current digest')
require(anchored_integrity(m3, current, 3), 'current anchored')
require(not local_integrity(m2, current), 'manifest-only replay fails digest')
require(local_integrity(m2, old), 'coordinated replay passes local digest')
require(not anchored_integrity(m2, old, 3), 'trusted high-water rejects rollback')
require(anchored_integrity(m2, old, 2), 'stale anchor cannot detect rollback')
require(m2['sha256'] != m3['sha256'], 'distinct payload hashes')
require(m2['format_v'] == m3['format_v'], 'format version is not history epoch')
require(m2['sealed'] and m3['sealed'], 'both segments sealed')
require('A' in old and 'deleted' in current, 'synthetic event change')
print(json.dumps({'assertions': checks, 'local_integrity_old_pair': True,
                  'external_epoch_rejects_old_pair': True,
                  'scope': 'synthetic E1; no native Rust or real sync'}))
