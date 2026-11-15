"""Two synthetic mechanisms, explicit delayed coupling, paired scenario branches."""
import hashlib
import json
import math
import platform
import random
from pathlib import Path
from .contracts import canonical, uncertainty, SCHEMA_VERSION
from .plugins import registry
from .adapters import PopulationAdapter
from .state import Snapshot
from .relations import validate_schedule, validate_relations


def code_identity():
    h=hashlib.sha256()
    for path in sorted(Path(__file__).parent.glob('*.py')):
        h.update(path.name.encode());h.update(path.read_bytes())
    return h.hexdigest()


def run_experiment(seed=7, rounds=8, population=24, intervention=0.2):
    if type(seed)!=int or not 0<=seed<2**32 or type(rounds)!=int or not 1<=rounds<=100 or type(population)!=int or not 1<=population<=1000:
        raise ValueError('Seed/round/population outside bounded synthetic budget')
    if type(intervention) not in (int,float) or not math.isfinite(intervention) or not 0<=intervention<=1:
        raise ValueError('Intervention must be finite [0,1]')
    validate_schedule([('individual','group',0),('group','individual',1)])
    individual,group=registry.get('individual','1.0.0'),registry.get('group','1.0.0')
    env={'python':platform.python_version(),'platform_version':'0.1.0','core_code_sha256':code_identity()}
    rng=random.Random(seed)
    root=Snapshot.create('coupled-synthetic','1.0.0',{'states':[0]*population,'exposure':0},'root',None,[],env,rng.getstate())
    result={'schema_version':SCHEMA_VERSION,'scientific_status':'SYNTHETIC_ONLY',
            'versions':{'platform':'0.1.0','contract':SCHEMA_VERSION,'individual':'1.0.0','group':'1.0.0','adapter':'1.0.0','protocol':'synthetic-paired-1.0.0','dataset':'generated-1.0.0'},
            'input':{'seed':seed,'rounds':rounds,'population':population,'intervention':intervention},'environment':env,
            'models':registry.describe(),'root_snapshot':root.to_dict(),'branches':{},
            'uncertainty':uncertainty('UNKNOWN',target='real-world validity'),'logs':[],
            'mechanism_relations':validate_relations([
                {'kind':'CANDIDATE_CAUSAL','from':'individual','to':'group','source':'SYNTHETIC','assumptions':['Complete constructed population'],'time_semantics':'individual before group','verification':'SYNTHETIC_ONLY','limitations':['No empirical identification']},
                {'kind':'DYNAMIC_FEEDBACK','from':'group','to':'individual','source':'SYNTHETIC','assumptions':['Held exposure between group updates'],'time_semantics':'one tick delayed; group period 2','verification':'SYNTHETIC_ONLY','limitations':['Synthetic illustrative mechanism only']}
            ])}
    for name,delta in [('baseline',0.0),('scenario',intervention)]:
        snap=root.fork(name);initial_snapshot=snap.to_dict();states=snap.restore()['state']['states'];exposure=0;history=[];rng=random.Random(seed)
        for tick in range(1,rounds+1):
            used=exposure
            states,dist=individual.advance_state(states,used,delta,rng)
            message={'schema_version':SCHEMA_VERSION,'record_id':f'{name}:{tick}','record_type':'individual.states',
                'subject_ref':[f'person-{i}' for i in range(population)],
                'time_context':{'simulation_time':tick,'round':tick,'event_time':tick,'observed_at':tick,'available_at':tick,'cutoff':tick,'target_time':tick+1},
                'payload':{'states':states},'units':'binary','uncertainty':uncertainty('UNKNOWN',units='binary',target='individual.states'),
                'provenance':{'source':'SYNTHETIC','seed':seed},'access_policy':'PUBLIC_SYNTHETIC','dependencies':['joint-population-state']}
            adapted=PopulationAdapter().adapt(message)
            if tick%2==0:exposure=group.advance_state(adapted)
            event={'event_id':f'{name}:{tick}','model_time':tick,'occurred_at':tick,'observed_at':tick,'available_at':tick,
                   'order_rule':'individual_then_group_every_2_ticks_then_next_tick_feedback'}
            snap=Snapshot.create('coupled-synthetic','1.0.0',{'states':states,'exposure':exposure},name,snap.content_hash,[event],env,rng.getstate())
            history.append({'tick':tick,'prevalence':sum(states)/population,'exposure_used':used,'group_updated':tick%2==0,
                            'snapshot_hash':snap.content_hash,'snapshot':snap.to_dict(),'probability_output':dist[0],'exchange':adapted})
            result['logs'].append(f'{event["event_id"]}: individual advanced; group {"updated" if tick%2==0 else "held"}; snapshot {snap.content_hash}')
        result['branches'][name]={'parent_hash':root.content_hash,'initial_snapshot':initial_snapshot,'history':history,'final_snapshot':snap.to_dict()}
    result['comparison']={'scenario_minus_baseline':result['branches']['scenario']['history'][-1]['prevalence']-result['branches']['baseline']['history'][-1]['prevalence'],
                          'interpretation':'SYNTHETIC_SCENARIO_DIFFERENCE_NOT_CAUSAL','paired_seed':seed}
    return json.loads(canonical(result))
