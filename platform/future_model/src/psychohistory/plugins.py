"""Explicitly allowlisted plugins; never import discovered research code."""
import hashlib
import inspect
import math
from .contracts import uncertainty

class Individual:
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

    def advance_state(self, states, exposure, intervention, rng):
        self.validate_input(states, exposure, intervention)
        probabilities=[1.0 if s else min(1.0,0.08+0.5*exposure+intervention) for s in states]
        return [int(rng.random()<p) for p in probabilities], [uncertainty('DISCRETE',values=[0,1],probabilities=[1-p,p]) for p in probabilities]

class Group:
    model_id, version = 'group','1.0.0'
    capabilities = ('describe','validate_input','simulate','advance_state','inspect','serialize_state','restore_state')
    def describe(self):
        return {'model_id':self.model_id,'version':self.version,'capabilities':list(self.capabilities),
                'source':'BUILTIN_SYNTHETIC','source_sha256':hashlib.sha256(inspect.getsource(type(self)).encode()).hexdigest(),
                'dependency_identity':'python-stdlib','assumptions':['Complete synthetic population observed','Two-tick update; exposure held between updates'],
                'scale':'group / every two ticks','input':'population prevalence','output':'held group exposure',
                'parameters':{'period':2},'evidence':'SYNTHETIC_ONLY','permission':'SYNTHETIC_ONLY'}
    def advance_state(self, record):
        from .contracts import validate_record
        validate_record(record)
        if record['record_type']!='group.exposure' or record['units']!='proportion':
            raise ValueError('Group input incompatible')
        x=record['payload'].get('prevalence')
        if type(x) not in (float,int) or not 0<=x<=1:
            raise ValueError('Invalid prevalence')
        return float(x)

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
