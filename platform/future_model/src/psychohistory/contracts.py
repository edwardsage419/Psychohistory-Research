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
        if not isinstance(p,list) or not isinstance(values,list) or not p or len(p) != len(values) or any(type(x) not in (float,int) or not math.isfinite(x) or x < 0 or x > 1 for x in p) or not math.isclose(sum(p), 1, abs_tol=1e-12):
            raise ValueError('Invalid discrete probability mass')
        if len({canonical(x) for x in values}) != len(values):
            raise ValueError('Duplicate outcomes')
    if kind in {'UNKNOWN','UNIDENTIFIABLE'} and any(k in kwargs for k in ['value','values','probabilities','bounds','samples','distribution','models']):
        raise ValueError('Unknown uncertainty cannot carry quantified estimates')
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
    if not isinstance(record,dict) or not required<=record.keys() or record['schema_version']!=SCHEMA_VERSION:
        raise ValueError('Missing fields or incompatible contract version')
    try:canonical(record)
    except (ValueError,TypeError) as exc:raise ValueError('Record must be finite JSON') from exc
    for field in ['record_id','record_type','units']:
        if not isinstance(record[field],str) or not record[field].strip():raise ValueError('Nonempty scalar identity/type/unit required')
    for field in ['subject_ref','dependencies']:
        values=record[field]
        if not isinstance(values,list) or not values or not all(isinstance(x,str) and x.strip() for x in values) or len(values)!=len(set(values)):
            raise ValueError('Explicit nonempty unique identity/dependency list required')
    if not isinstance(record['payload'],dict) or not isinstance(record['provenance'],dict) or not isinstance(record['provenance'].get('source'),str) or not record['provenance']['source']:
        raise ValueError('Structured payload and provenance required')
    extensions=record.get('extensions',{})
    import re
    if not isinstance(extensions,dict) or any(not re.fullmatch(r'[a-z][a-z0-9_.-]+@[0-9]+\.[0-9]+\.[0-9]+',k) for k in extensions):raise ValueError('Extensions require namespace@version')
    if set(record)-required-{'extensions'}:raise ValueError('Undeclared record fields')
    t=record['time_context']
    if not isinstance(t,dict):raise ValueError('Structured time_context required')
    for k in ['simulation_time','round','event_time','observed_at','available_at','cutoff','target_time']:
        if type(t.get(k)) not in (int,float) or not math.isfinite(t[k]):raise ValueError('Explicit finite time semantics required')
    if not t['event_time']<=t['observed_at']<=t['available_at']<=t['cutoff']<t['target_time']:
        raise ValueError('Future information or inconsistent time order')
    if t['simulation_time']<0 or t['simulation_time']>t['cutoff'] or type(t['round'])!=int or t['round']<0:raise ValueError('Invalid discrete round or simulation time')
    if record['access_policy'] not in {'PUBLIC_SYNTHETIC','METADATA_ONLY','RESTRICTED'}:raise ValueError('Unknown access policy')
    u=record['uncertainty']
    metadata={'kind','conditions','target','units','method','dependencies','interpretation','source'}
    if not isinstance(u,dict) or not metadata<=u.keys():raise ValueError('Complete uncertainty interpretation required')
    if any(not isinstance(u[k],str) or not u[k].strip() for k in ['kind','target','units','method','interpretation','source']):raise ValueError('Invalid uncertainty metadata')
    if not isinstance(u['conditions'],list) or not all(isinstance(x,str) for x in u['conditions']):raise ValueError('Invalid uncertainty conditions')
    if u['units']!=record['units'] or u['target']!=record['record_type'] or u['dependencies']!=record['dependencies']:
        raise ValueError('Uncertainty target/unit/joint-dependency mismatch')
    uncertainty(u['kind'],**{k:v for k,v in u.items() if k!='kind'})
    return record
