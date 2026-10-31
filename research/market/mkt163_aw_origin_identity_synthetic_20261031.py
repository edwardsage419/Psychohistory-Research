#!/usr/bin/env python3
"""Synthetic model of pinned ActivityWatch aw-sync destination identity selection.
No real user data or Rust execution. Models selected code branches only.
"""
import json
import re

SUFFIX = '-synced-from-'

def sanitize(value):
    result = re.sub(r'[^a-z0-9_-]+', '_', value.strip().lower()).strip('_')
    return result or 'unknown'

def choose(source, existing):
    base = source['id'].split(SUFFIX, 1)[0]
    origin = source.get('origin', source['hostname'])
    raw = base + SUFFIX + origin
    if raw in {x['id'] for x in existing}:
        return 'reuse_raw', raw
    norm = sanitize(origin)
    normalized_id = base + SUFFIX + norm
    if sanitize(source['hostname']) == 'unknown' or norm == 'unknown':
        return 'reject_unknown', None
    if normalized_id != raw and normalized_id in {x['id'] for x in existing}:
        return 'reuse_sanitized', normalized_id
    candidates = [x for x in existing if x['id'].split(SUFFIX, 1)[0] == base
                  and isinstance(x.get('origin'), str)
                  and sanitize(x['origin']) == norm]
    if len(candidates) == 1:
        return 'reuse_legacy', candidates[0]['id']
    if len(candidates) > 1:
        return 'reject_ambiguous', None
    return 'create', normalized_id

def main():
    source = {'id':'aw-watcher-window','hostname':'poco_f8_ultra','device_id':'device_new'}
    old = {'id':'aw-watcher-window-synced-from-POCO F8 Ultra',
           'origin':'POCO F8 Ultra','device_id':'device_old'}
    cases = [
        ('new',[],('create','aw-watcher-window-synced-from-poco_f8_ultra')),
        ('raw',[{'id':'aw-watcher-window-synced-from-poco_f8_ultra'}],
         ('reuse_raw','aw-watcher-window-synced-from-poco_f8_ultra')),
        ('legacy_one',[old],('reuse_legacy',old['id'])),
        ('legacy_two',[old,{'id':'aw-watcher-window-synced-from-POCO.F8.Ultra',
                            'origin':'POCO.F8.Ultra','device_id':'other'}],
         ('reject_ambiguous',None)),
        ('wrong_base',[{'id':'aw-watcher-afk-synced-from-POCO F8 Ultra',
                        'origin':'POCO F8 Ultra'}],
         ('create','aw-watcher-window-synced-from-poco_f8_ultra')),
        ('no_metadata',[{'id':'aw-watcher-window-synced-from-POCO F8 Ultra'}],
         ('create','aw-watcher-window-synced-from-poco_f8_ultra')),
    ]
    results={}
    for name,dest,expected in cases:
        actual=choose(source,dest)
        assert actual==expected,(name,actual,expected)
        results[name]=actual[0]
    raw_source={**source,'hostname':'POCO F8 Ultra'}
    dest=[{'id':'aw-watcher-window-synced-from-POCO F8 Ultra'}]
    assert choose(raw_source,dest)[0]=='reuse_raw'
    results['raw_unsanitized']='reuse_raw'
    assert choose(raw_source,[{'id':'aw-watcher-window-synced-from-poco_f8_ultra'}])[0]=='reuse_sanitized'
    results['sanitized']='reuse_sanitized'
    assert choose({**source,'hostname':'???'},[])[0]=='reject_unknown'
    results['unknown']='reject_unknown'
    assert sanitize('POCO F8 Ultra')==sanitize('POCO.F8.Ultra')=='poco_f8_ultra'
    assert old['device_id'] != source['device_id']
    assert choose(source,[old])[0]=='reuse_legacy'
    results['cross_device_same_name']='reuse_legacy_in_synthetic_model'
    print(json.dumps({'tests':11,'results':results,
                      'scope':'synthetic model of fixed Rust branches, not native Rust or exploit validation'},indent=2))

if __name__=='__main__':main()
