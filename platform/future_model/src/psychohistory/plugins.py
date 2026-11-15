"""Explicitly allowlisted plugins; never import discovered research code."""
import hashlib
import inspect
import math
import json
from .contracts import canonical
from .contracts import uncertainty

class StateCapability:
    def inspect(self, state):
        return json.loads(canonical(state))
    def serialize_state(self, state):
        return canonical({'schema_version':'1.0.0','model_id':self.model_id,'model_version':self.version,'state':state})
    def restore_state(self, serialized):
        value=json.loads(serialized)
        if value.get('schema_version')!='1.0.0' or value.get('model_id')!=self.model_id or value.get('model_version')!=self.version:
            raise ValueError('Incompatible plugin state identity')
        return self.inspect(value['state'])

class Individual(StateCapability):
    model_id, version = 'individual','1.0.0'
    capabilities = ('describe','validate_input','simulate','advance_state','inspect','serialize_state','restore_state')

    def describe(self):
        return {'model_id':self.model_id,'version':self.version,'capabilities':list(self.capabilities),
                'source':'BUILTIN_SYNTHETIC','source_sha256':hashlib.sha256(inspect.getsource(type(self)).encode()).hexdigest(),
                'dependency_identity':'python-stdlib-random','assumptions':['Bernoulli innovations conditional on supplied exposure','No empirical calibration'],
                'scale':'individual / discrete tick','input':'binary states, exposure, intervention','output':'binary states and conditional probabilities',
                'parameters':{'base':0.08,'influence':0.5},'evidence':'SYNTHETIC_ONLY','permission':'SYNTHETIC_ONLY'}

    def validate_input(self, states, exposure, intervention):
        if not states or any(type(x)!=int or x not in (0,1) for x in states):
            raise ValueError('Binary nonmissing states required')
        if any(type(x) not in (float,int) or not math.isfinite(x) or not 0<=x<=1 for x in (exposure,intervention)):
            raise ValueError('Exposure and intervention must be in [0,1]')

    def simulate(self, states, exposure, intervention, seed):
        import random
        return self.advance_state(states,exposure,intervention,random.Random(seed))

    def advance_state(self, states, exposure, intervention, rng):
        self.validate_input(states, exposure, intervention)
        probabilities=[1.0 if s else min(1.0,0.08+0.5*exposure+intervention) for s in states]
        return [int(rng.random()<p) for p in probabilities], [uncertainty('DISCRETE',values=[0,1],probabilities=[1-p,p]) for p in probabilities]

class Group(StateCapability):
    model_id, version = 'group','1.0.0'
    capabilities = ('describe','validate_input','simulate','advance_state','inspect','serialize_state','restore_state')
    def describe(self):
        return {'model_id':self.model_id,'version':self.version,'capabilities':list(self.capabilities),
                'source':'BUILTIN_SYNTHETIC','source_sha256':hashlib.sha256(inspect.getsource(type(self)).encode()).hexdigest(),
                'dependency_identity':'python-stdlib','assumptions':['Complete synthetic population observed','Two-tick update; exposure held between updates'],
                'scale':'group / every two ticks','input':'population prevalence','output':'held group exposure',
                'parameters':{'period':2},'evidence':'SYNTHETIC_ONLY','permission':'SYNTHETIC_ONLY'}
    def validate_input(self, record):
        from .contracts import validate_record
        validate_record(record)
        if record['record_type']!='group.exposure' or record['units']!='proportion':
            raise ValueError('Group input incompatible')
        x=record['payload'].get('prevalence')
        if type(x) not in (float,int) or not 0<=x<=1:
            raise ValueError('Invalid prevalence')
        return float(x)
    def advance_state(self, record):
        return self.validate_input(record)
    def simulate(self, record):
        return self.advance_state(record)

class Registry:
    def __init__(self):
        self._plugins={}
    def register(self, plugin):
        key=(plugin.model_id,plugin.version)
        if key in self._plugins or plugin.version=='latest':
            raise ValueError('Duplicate or unpinned plugin')
        self._plugins[key]=plugin
    def get(self, model_id, version):
        try: return self._plugins[(model_id,version)]
        except KeyError: raise ValueError('Unknown exact model version') from None
    def describe(self):
        return [x.describe() for x in self._plugins.values()]

registry=Registry()
registry.register(Individual()); registry.register(Group())
