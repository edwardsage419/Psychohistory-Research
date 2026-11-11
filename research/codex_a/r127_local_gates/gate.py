#!/usr/bin/env python3
"""Local R127 fail-closed replay and provenance sidecar, stdout only.

Reuses original program/tests and pinned historical receipt values. Does not
repair/publish the production workflow or authenticate historical CI execution.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
PIN_MANIFEST_SHA256 = '291c87fc9f9855df5687d8795b8189213ed2f510218132030cc9aac37feae0a8'
WORKFLOW = '.github/workflows/r127-van-huyck-1990-coordination-source-table-60-tests.yml'
MODULE = 'r127_van_huyck_1990_min_effort_coordination_selection_exact'
TEST_MODULE = 'test_'+MODULE
RECEIPT = 'research/R127/R127_PHASE_A_1990_ORIGINAL_MIN_EFFORT_60_TEST_75117_DEVIATIONS_1296_2X2_CI_ACCEPTANCE.json'
LINKS = {
    'original': 'published_source_A_treatment_seven_experiments_p1_p10_only',
    'equilibria': 'source_A_seven_strict_common_effort_Nash_security_and_payoff_rank',
    'payoff_table': 'original_source_A_payoff_table_rows',
    'audit': 'n2to4_original_source_payoff_complete_synthetic_profiles_and_deviations',
    'toy': 'two_player_symmetric_coordination_project_created_conflict_and_risk_tie',
    'grid': 'synthetic_all_six_level_symmetric_2x2_payoffs',
}
FUNCTIONS = ('published_1990_table2_verification', 'min_effort_security_and_payoff_rank',
             'original_payoff_table_A', 'exhaustive_original_min_effort_payoff_audit',
             'frozen_two_person_examples', 'exhaustive_two_player_symmetric_payoff_grid')


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def load_json(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'DUPLICATE_JSON_KEY:'+key)
            result[key] = value
        return result
    def invalid(value):raise ValueError('NONFINITE_JSON_CONSTANT:'+value)
    return json.loads(raw, object_pairs_hook=unique, parse_constant=invalid)


def identity(raw):
    # Same byte identity formula used by the adopted S53/R170 compositions.
    return {'git_blob': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),
            'sha256': hashlib.sha256(raw).hexdigest()}


def capture(root):
    root = Path(root)
    pin_bytes = (HERE/'pins.json').read_bytes()
    require(hashlib.sha256(pin_bytes).hexdigest() == PIN_MANIFEST_SHA256, 'PIN_MANIFEST_CHANGED')
    pins = load_json(pin_bytes)
    raw, identities = {}, {}
    try:
        head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD^{commit}'],
                                       text=True, stderr=subprocess.PIPE).strip()
        for name, pin in pins.items():
            data = (root/name).read_bytes()
            observed = identity(data)
            require(observed == pin, 'SOURCE_IDENTITY:'+name)
            tracked = subprocess.check_output(['git', '-C', str(root), 'rev-parse', head+':'+name],
                                              text=True, stderr=subprocess.PIPE).strip()
            require(tracked == pin['git_blob'], 'CHECKOUT_IDENTITY:'+name)
            raw[name], identities[name] = data, observed
    except subprocess.CalledProcessError as exc:
        raise ValueError('GIT_IDENTITY_UNAVAILABLE') from exc
    return raw, identities, head


def parse_test_log(raw, child_exit):
    require(type(raw) is bytes and type(child_exit) is int and child_exit == 0, 'TEST_CHILD_EXIT')
    text = raw.decode('utf-8')
    require(not re.search(r'(?m)^\s*(?:FAILED|ERROR|FAIL)(?:\s|\(|:|$)', text), 'FAILURE_MARKER')
    require(not re.search(r'\bskipped\b|expected failures|unexpected successes', text), 'NONPASSING_TESTS')
    counts = re.findall(r'(?m)^Ran ([0-9]+) tests? in [^\r\n]+\r?$', text)
    require(counts == ['60'], 'EXACTLY_ONE_60_TEST_SUMMARY')
    require(len(re.findall(r'(?m)^OK[ \t]*\r?$', text)) == 1, 'EXACTLY_ONE_OK')
    require(re.search(r'(?m)^Ran 60 tests in [^\r\n]+\r?\n\s*\r?\nOK[ \t]*\r?\n?\Z', text)
            is not None, 'FINAL_PLAIN_OK_SUMMARY')
    return {'tests': 60, 'failures': 0, 'skipped': 0, 'exit': child_exit,
            'log_sha256': hashlib.sha256(raw).hexdigest()}


def same(actual, expected, path='stage2'):
    require(type(actual) is type(expected), 'FIELD_TYPE:'+path)
    if type(expected) is dict:
        require(set(actual) == set(expected), 'FIELD_SCHEMA:'+path)
        return sum(same(actual[key], value, path+'.'+key) for key, value in expected.items())
    if type(expected) is list:
        require(len(actual) == len(expected), 'FIELD_LENGTH:'+path)
        return sum(same(a, b, path+'['+str(i)+']') for i, (a, b) in enumerate(zip(actual, expected)))
    require(actual == expected, 'FIELD_VALUE:'+path)
    return 1


def validate_stage2(observed, authenticated_receipt):
    """Compare full typed sections; the outer CLI authenticates the expectation."""
    expected = {key: authenticated_receipt[name] for key, name in LINKS.items()}
    count = same(observed, expected)
    e2 = observed['original']['new_real_human_E2_prediction_scores']
    require(type(e2) is int and e2 == 0 and
            type(authenticated_receipt['new_real_person_level_E2_prediction_scores']) is int and
            authenticated_receipt['new_real_person_level_E2_prediction_scores'] == e2, 'E2_RECEIPT_BINDING')
    return {'checked_leaf_fields': count, 'comparison': 'EXACT_TYPED_ARCHIVED_SECTIONS',
            'new_real_person_level_E2_prediction_scores': e2}


def run_child(command, cwd):
    child = subprocess.run(command, cwd=cwd, capture_output=True, timeout=120)
    streams = {name: {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw),
                      'text': raw.decode('utf-8')}
               for name, raw in (('stdout', child.stdout), ('stderr', child.stderr))}
    return child, {'command': list(map(str, command)), 'cwd': str(cwd),
                   'exit': child.returncode, 'streams': streams}


def verify(root):
    gate_raw = Path(__file__).read_bytes()
    raw, identities, checkout = capture(root)
    # Isolated Python excludes ambient PYTHONPATH/user-site; explicit -O follows
    # the parent mode. Original program and test bytes are never patched.
    python = [sys.executable, '-I', '-B']+(['-O'] if sys.flags.optimize else [])
    test_code = ('import sys,unittest;sys.path.insert(0,sys.argv[1]);'
                 'unittest.main(module=sys.argv[2],argv=["R127"],verbosity=2)')
    stage_code = ('import sys,json,importlib;sys.path.insert(0,sys.argv[1]);'
                  'm=importlib.import_module(sys.argv[2]);'
                  'print(json.dumps({k:getattr(m,f)() for k,f in '
                  'zip(json.loads(sys.argv[3]),json.loads(sys.argv[4]))}))')
    with tempfile.TemporaryDirectory(prefix='codex-a-r127-') as directory:
        snapshot = Path(directory)
        for name, data in raw.items():
            target = snapshot/name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        cwd = snapshot/'research/R127'
        tests, tests_record = run_child(python+['-c', test_code, str(cwd), TEST_MODULE], cwd)
        require(not tests.stdout, 'UNEXPECTED_TEST_STDOUT')
        test_result = parse_test_log(tests.stderr, tests.returncode)
        stage, stage_record = run_child(python+['-c', stage_code, str(cwd), MODULE,
                                              json.dumps(list(LINKS)), json.dumps(FUNCTIONS)], cwd)
        require(stage.returncode == 0 and not stage.stderr, 'STAGE2_CHILD_EXIT')
        checked = validate_stage2(load_json(stage.stdout), load_json(raw[RECEIPT]))
    require(Path(__file__).read_bytes() == gate_raw, 'GATE_SOURCE_CHANGED_DURING_REPLAY')
    return {'status': 'COMPLETE_LOCAL_R127_ENGINEERING_REPLAY',
            'scope': 'PINNED_ORIGINAL_TESTS_AND_ARCHIVED_STAGE2_REGRESSION_ONLY',
            'tested_checkout_sha': checkout, 'sources': identities,
            'gate_identity': identity(gate_raw),
            'pin_manifest_sha256': PIN_MANIFEST_SHA256,
            'workflow_git_blob': identities[WORKFLOW]['git_blob'],
            'unittest': test_result, 'stage2': checked,
            'commands': [tests_record, stage_record],
            'python': sys.version, 'optimized': bool(sys.flags.optimize),
            'new_real_person_level_E2_prediction_scores': checked['new_real_person_level_E2_prediction_scores'],
            'workflow_run_id': None, 'workflow_job_id': None,
            'historical_execution_time_authenticated': 'NOT_ESTABLISHED',
            'historical_run_source_identity': 'NOT_REAUTHENTICATED',
            'production_workflow_fix': 'NOT_APPLIED_MAINLINE_OWNED',
            'production_receipt_publish_or_rebase': 'NOT_RUN',
            'CI': 'NOT_RUN', 'formal_scientific_reacceptance': 'NOT_RUN',
            'original_catalogue_05_003_closure': 'NOT_RUN',
            'new_E2': 0, 'new_E3': 0, 'external_team_replications': 0,
            'R073': 'FROZEN_UNCHANGED', 'PESEN_v0_1': 'FROZEN_UNCHANGED'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    try:
        result = verify(args.root)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(json.dumps({'status': 'BLOCKED', 'reason': str(exc)[:300]}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':sys.exit(main())
