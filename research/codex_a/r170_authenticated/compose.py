#!/usr/bin/env python3
"""Run pinned PR8 state comparison and mandatory PR9 identity gate on one snapshot.

Stdout-only bounded nonblind engineering receipt. No implicit network or source edits.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

SOURCES = {'research/validation/r170_observation_ladder_20261026.js': {'git_blob': '3ea018c4a113d95836873fcfd687f9df292aa1b7',
                                                             'sha256': '1752281be18d042558955162f9174a4879e880b989cc40c7bbe5a0c13f92bba7'},
 'research/evidence_audit/r170_b_edge_utterance_20261026.py': {'git_blob': 'f6bd8574d6730b9c26708adb9e38ef88562eafbe',
                                                               'sha256': '134cfee8510606fef8f94eb3d9975f1045006bf17360444aeaa1b588d0080423'},
 'research/validation/R170_OBSERVATION_LADDER_EXACT_RECEIPT_2026-10-26.json': {'git_blob': '0d5b10125475a66a243be1632e21bd269027a866',
                                                                               'sha256': 'b0ae731555373b0c58b5d26fa806c10f79e7ba8a39b882fd1a4f150c57687400'},
 'research/evidence_audit/B_R170_INDEPENDENT_PYTHON_EXECUTION_SUMMARY_2026-10-26.json': {'git_blob': '165f14511c7c7ee57b43a18851d2e65729c50044',
                                                                                         'sha256': '626b63a463581c1cb012edb6e8540ebdb56a51680dbe00c1a197506212caeaef'},
 'protocols/R170_OBSERVATION_LADDER_THIRD_METHOD_FREEZE_2026-10-26.md': {'git_blob': '3a85af7291f5c916d26734fd54773aa347a5e027',
                                                                         'sha256': '4d98db52333758b4775c371eb41e0388327febbeb16471dc67f06896b3d08e7d'}}
CODE = {'run_audit.py': {'git_blob': '2573ba5d823449dff43c038bce61754baeea8184',
                  'sha256': '58318bfe802d7e5b77fb5f75093398afe89cd9820c004bbacc7b3a8c835fab27'},
 'export_js_states.js': {'git_blob': '5e7c17c3a876811ceb1f3c09df93faacd9c99cc8',
                         'sha256': '0a728789f364fef631c11e0292fd6ae0745787eb9a212ba6e85cfd159a008227'},
 'export_python_states.py': {'git_blob': '5360fcaca008865a8148122684b8b28edcd94e6d',
                             'sha256': 'a88bed9ad5ffa0613b08126f15ad8a16e39b9f9eb972e0719c7c80d482414439'},
 'identity_gate.py': {'git_blob': '8e62bc3f227d61c57854b958b41c64cdc58c83b1',
                      'sha256': 'f27a6323d50f981f03eb38676e74f13df1e4861b98ffd14ee9458b6f9b57aaf2'}}
PR8_CODE_COMMIT = '1d8294ee81c7e23cb16bb8882ebc619089a35c65'
PR9_CODE_COMMIT = '89a64ecd2975a7fa0409f000cef45b1b2792a8b4'
COMPARE = {'snapshots':288, 'state_mass_comparisons':23328,
           'nonzero_entries_per_route':5099, 'exact_normalization_checks':576,
           'unreachable_zero_states_included':True}
PR8_SUMMARY = {'status':'COMPLETE', 'protocol_acceptance':'PARTIAL',
              'snapshots':288, 'state_mass_comparisons':23328, 'nonzero_entries':5099,
              'B_receipt_historical_hash_match':True, 'witness_order_match':False}
B_SHA256 = '8cdf817c0e32cd48ea1a70dd1f9d0c5fc55022c8d355981157d0181934ab2565'


def identity(raw):
    return {'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),
            'sha256':hashlib.sha256(raw).hexdigest()}


def authenticate(path, pin):
    raw=Path(path).read_bytes()
    if identity(raw)!=pin:raise ValueError('identity mismatch: '+str(path))
    return raw


def unique(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError('duplicate JSON key: '+key)
        result[key]=value
    return result


def parse(raw):
    return json.loads(raw,object_pairs_hook=unique)


def exact(actual, expected, label):
    if json.dumps(actual,sort_keys=True)!=json.dumps(expected,sort_keys=True):
        raise ValueError(label+' mismatch')


def fields(actual, expected, label):
    if type(actual) is not dict or not set(expected)<=set(actual):
        raise ValueError(label+' fields missing')
    exact({key:actual[key] for key in expected},expected,label)


def child(command):
    try:result=subprocess.run(command,capture_output=True,text=True,timeout=60)
    except subprocess.TimeoutExpired as exc:raise ValueError('child timeout') from exc
    if result.returncode!=0:
        raise ValueError('child exit '+str(result.returncode)+': '+result.stderr[:500])
    return parse(result.stdout)


def verify(root, pr8_dir, identity_gate):
    root,pr8_dir=Path(root),Path(pr8_dir)
    data={path:authenticate(root/path,pin) for path,pin in SOURCES.items()}
    code={name:authenticate(identity_gate if name=='identity_gate.py' else pr8_dir/name,pin)
          for name,pin in CODE.items()}
    identities={path:identity(raw) for path,raw in data.items()}
    identities.update({'tool/'+name:identity(raw) for name,raw in code.items()})
    python=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
    with tempfile.TemporaryDirectory(prefix='r170-authenticated-') as directory:
        work=Path(directory);inputs=work/'inputs';tools=work/'tools';output=work/'output'
        tools.mkdir()
        for path,raw in data.items():
            target=inputs/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
        for name,raw in code.items():(tools/name).write_bytes(raw)
        comparison_command=python+[str(tools/'run_audit.py'),str(inputs),'--output',str(output)]
        summary=child(comparison_command)
        exact(summary,PR8_SUMMARY,'comparison summary')
        execution=parse((output/'execution.json').read_bytes())
        fields(execution,{'status':'COMPLETE','full_frozen_extension_acceptance':'PARTIAL',
                         'full_state_comparison':COMPARE,
                         'B_complete_receipt_matches_historical_digest':True,
                         'B_complete_receipt_matches_historical_bytes':True,
                         'B_source_matches_historical_digest':True,
                         'historical_witness_matches_either_order':False,
                         'new_E2':0,'new_E3':0,'external_team_replications':0},'comparison execution')
        identity_command=python+[str(tools/'identity_gate.py'),str(inputs),
                                 str(output/'B_full_receipt.json'),'--output',str(work/'identity.json')]
        authenticated=child(identity_command)
        exact(parse((work/'identity.json').read_bytes()),authenticated,'identity stdout/file')
        fields(authenticated,{'status':'COMPLETE','scope':'BYTE_IDENTITY_ONLY_NONBLIND',
                              'source_files_verified':4,'B_receipt_bytes':23004,
                              'B_receipt_sha256':B_SHA256,'historical_source_digest_matches':True,
                              'full_frozen_extension_acceptance':'PARTIAL',
                              'historical_execution_time_authenticated':'NOT_ESTABLISHED',
                              'model_execution_this_gate':'NOT_RUN',
                              'new_E2':0,'new_E3':0,'external_team_replications':0},'identity result')
    return {'status':'COMPLETE_PINNED_R170_COMPOSITION',
            'scope':'NONBLIND_INTERNAL_ARTIFICIAL_E1_EXISTING_GATES',
            'pinned_pr8_commit':PR8_CODE_COMMIT,'pinned_pr9_commit':PR9_CODE_COMMIT,
            'full_state_comparison':execution['full_state_comparison'],
            'identity_gate':authenticated,'comparison_execution':execution,
            'commands':[comparison_command,identity_command],'identities':identities,
            'source_authentication':'PINNED_INPUT_AND_EXECUTABLE_BYTES_VERIFIED',
            'witness_order_compliance':'NOT_ESTABLISHED',
            'full_frozen_extension_acceptance':'PARTIAL',
            'historical_execution_time_authenticated':'NOT_ESTABLISHED',
            'new_E2':0,'new_E3':0,'external_team_replications':0}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',type=Path)
    parser.add_argument('--pr8-dir',type=Path,required=True)
    parser.add_argument('--identity-gate',type=Path,required=True)
    args=parser.parse_args()
    try:result=verify(args.root,args.pr8_dir,args.identity_gate)
    except (OSError,ValueError) as exc:
        print(json.dumps({'status':'BLOCKED','reason':str(exc)}));return 1
    print(json.dumps(result,indent=2));return 0


if __name__=='__main__':sys.exit(main())
