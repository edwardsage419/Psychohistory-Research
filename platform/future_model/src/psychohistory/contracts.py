"""Versioned exchange contracts. Pure stdlib; no assumptions about joint independence."""
import json
import math

SCHEMA_VERSION = '1.0.0'
KINDS = {'POINT','DISCRETE','DISTRIBUTION','PREDICTION_INTERVAL','CONFIDENCE_INTERVAL',
         'CREDIBLE_INTERVAL','POSTERIOR_SAMPLES','PARTIAL_IDENTIFICATION','MODEL_SET','UNKNOWN','UNIDENTIFIABLE'}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)


def uncertainty(kind, **kwargs):
    if kind not in KINDS:
        raise ValueError('Unsupported uncertainty kind')
    result = {'kind':kind, 'conditions':[], 'target':'synthetic state', 'units':'dimensionless',
              'method':'declared', 'dependencies':['joint-population-state'],
              'interpretation':'No empirical claim', 'source':'SYNTHETIC', **kwargs}
    canonical(result)
    if kind == 'DISCRETE':
        p, values = kwargs.get('probabilities', []), kwargs.get('values', [])
        if not p or len(p) != len(values) or any(type(x) not in (float,int) or not math.isfinite(x) or x < 0 or x > 1 for x in p) or not math.isclose(sum(p), 1, abs_tol=1e-12):
            raise ValueError('Invalid discrete probability mass')
        if len({canonical(x) for x in values}) != len(values):
            raise ValueError('Duplicate outcomes')
    if kind.endswith('INTERVAL'):
        bounds=kwargs.get('bounds')
        if not bounds or len(bounds)!=2 or any(type(x) not in (int,float) or not math.isfinite(x) for x in bounds) or bounds[0]>bounds[1]:
            raise ValueError('Invalid interval')
    return result


def convert_uncertainty(value, target):
    if value.get('kind') != target:
        raise ValueError('Unjustified uncertainty conversion forbidden')
    return json.loads(canonical(uncertainty(target, **{k:v for k,v in value.items() if k!='kind'})))


def validate_record(record):
    required={'schema_version','record_id','record_type','subject_ref','time_context','payload','units','uncertainty','provenance','access_policy','dependencies'}
    if not required <= record.keys() or record['schema_version'] != SCHEMA_VERSION:
        raise ValueError('Missing fields or incompatible contract version')
    canonical(record)
    subjects=record['subject_ref']
    if not subjects or not all(isinstance(x,str) and x for x in subjects) or len(subjects)!=len(set(subjects)):
        raise ValueError('Missing or ambiguous subject identity')
    if not record['dependencies'] or not record['units'] or not record['provenance'].get('source'):
        raise ValueError('Units, joint dependence and provenance required')
    t=record['time_context']
    for k in ['simulation_time','round','event_time','observed_at','available_at','cutoff','target_time']:
        if type(t.get(k)) not in (int,float) or not math.isfinite(t[k]):
            raise ValueError('Explicit finite time semantics required')
    if not t['event_time'] <= t['observed_at'] <= t['available_at'] <= t['cutoff'] < t['target_time']:
        raise ValueError('Future information or inconsistent time order')
    if t['simulation_time'] > t['cutoff'] or t['round'] < 0:
        raise ValueError('Invalid simulation time')
    if record['access_policy'] not in {'PUBLIC_SYNTHETIC','METADATA_ONLY','RESTRICTED'}:
        raise ValueError('Unknown access policy')
    u=record['uncertainty']
    uncertainty(u['kind'], **{k:v for k,v in u.items() if k!='kind'})
    return record
