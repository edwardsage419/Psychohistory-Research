import copy
import json
import pytest


def test_engine_reproducibility_branches_and_time():
    from psychohistory.engine import run_experiment
    a = run_experiment(seed=12, rounds=6, population=20, intervention=0.4)
    assert a == run_experiment(seed=12, rounds=6, population=20, intervention=0.4)
    assert a['scientific_status'] == 'SYNTHETIC_ONLY'
    assert a['versions']['individual'] == '1.0.0'
    assert len(a['branches']) == 2
    base, changed = a['branches']['baseline'], a['branches']['scenario']
    assert base['parent_hash'] == changed['parent_hash']
    assert base['history'][0]['snapshot_hash'] != changed['history'][0]['snapshot_hash']
    assert len(base['history']) == 6
    assert base['history'][0]['exposure_used'] == 0
    assert base['history'][1]['group_updated'] is True
    assert base['history'][2]['exposure_used'] == base['history'][1]['prevalence']
    assert a['comparison']['interpretation'] == 'SYNTHETIC_SCENARIO_DIFFERENCE_NOT_CAUSAL'
    for branch in a['branches'].values():
        assert all(0 <= x['prevalence'] <= 1 for x in branch['history'])
        assert len(branch['final_snapshot']['content_hash']) == 64


def test_uncertainty_and_refusal():
    from psychohistory.contracts import uncertainty, convert_uncertainty
    assert uncertainty('UNKNOWN')['kind'] == 'UNKNOWN'
    assert uncertainty('DISCRETE', values=[0,1], probabilities=[.3,.7])['probabilities'] == [.3,.7]
    for probabilities in [[.5,.4],[-.1,1.1],[float('nan'),0]]:
        with pytest.raises(ValueError): uncertainty('DISCRETE', values=[0,1], probabilities=probabilities)
    with pytest.raises(ValueError): convert_uncertainty(uncertainty('UNKNOWN'), 'DISCRETE')
    with pytest.raises(ValueError): convert_uncertainty(uncertainty('CONFIDENCE_INTERVAL', bounds=[0,1]), 'CREDIBLE_INTERVAL')


def record():
    return {'schema_version':'1.0.0','record_id':'input-1','record_type':'individual.states',
      'subject_ref':['person-0','person-1'],'time_context':{'simulation_time':0,'round':0,'event_time':0,'observed_at':0,'available_at':0,'cutoff':0,'target_time':1},
      'payload':{'states':[0,1]},'units':'binary','uncertainty':{'kind':'UNKNOWN'},
      'provenance':{'source':'SYNTHETIC','seed':1},'access_policy':'PUBLIC_SYNTHETIC','dependencies':['joint-population-state']}


def test_adapter_contracts_reject_future_identity_unit_version():
    from psychohistory.adapters import PopulationAdapter
    from psychohistory.contracts import validate_record
    a=PopulationAdapter()
    assert a.adapt(record())['payload']['prevalence'] == .5
    for mutate in [lambda r:r.update(units='kg'),lambda r:r.update(schema_version='2.0.0'),
                   lambda r:r['time_context'].update(available_at=2),lambda r:r.update(subject_ref=['same','same']),
                   lambda r:r.update(dependencies=[]),lambda r:r['payload'].update(states=[None,1])]:
        r=record();mutate(r)
        with pytest.raises(ValueError):a.adapt(r)
    r=record();r['time_context']['target_time']=-1
    with pytest.raises(ValueError):validate_record(r)


def test_registry_snapshots_and_cycles():
    from psychohistory.plugins import registry
    from psychohistory.state import Snapshot
    from psychohistory.relations import validate_relations, validate_schedule
    assert len(registry.describe()) == 2
    with pytest.raises(ValueError):registry.get('individual','latest')
    original={'states':[0,1]}; s=Snapshot.create('individual','1.0.0',original,'root',None,[],{'python':'3.12'})
    original['states'][0]=1
    assert s.restore()['state']['states']==[0,1]
    x=s.restore();x['state']['states'][0]=1
    assert s.restore()['state']['states']==[0,1]
    assert s.fork('branch-a').content_hash != s.fork('branch-b').content_hash
    dumped=s.to_dict();dumped['content_hash']='0'*64
    with pytest.raises(ValueError):Snapshot.from_dict(dumped)
    with pytest.raises(ValueError):validate_schedule([('a','b',0),('b','a',0)])
    validate_schedule([('a','b',1),('b','a',1)])
    with pytest.raises(ValueError):validate_relations([{'kind':'IDENTIFIED_CAUSAL','source':'simulation','verified':False}])


@pytest.mark.parametrize('args',[{'rounds':0},{'population':100001},{'seed':-1},{'intervention':float('nan')}])
def test_bounded_engine(args):
    from psychohistory.engine import run_experiment
    with pytest.raises(ValueError):run_experiment(**args)


def test_plugin_capabilities_are_real_and_state_is_restorable():
    from psychohistory.plugins import registry
    for model in registry.describe():
        plugin=registry.get(model['model_id'],model['version'])
        for capability in model['capabilities']:
            assert callable(getattr(plugin,capability,None)),(model['model_id'],capability)


def test_unknown_payload_fields_do_not_smuggle_future_information():
    from psychohistory.adapters import PopulationAdapter
    r=record();r['payload']['tomorrow_states']=[1,1]
    with pytest.raises(ValueError):PopulationAdapter().adapt(r)
