#!/usr/bin/env python3
"""Run existing B18 artificial diagnostic behind an explicit production veto.

No new probability/scoring mathematics. No human-data scoring, original-file
writes, network, Git mutations or silent promotion of a diagnostic PASS.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

SOURCE_COMMIT = '9de51508daa160d33d0d05b13ba1454f8333f21d'
OWN = 'research/codex_b/2026-11-10-r077-exact-paired-ties'
MANIFEST = OWN+'/evidence/py312/summary.json'
CANDIDATE_COMMIT = '02989a4944d0f100035927883762d83e4dba4925'
CANDIDATE_DIR = 'research/codex_b/2026-11-10-r077-exact-score-candidate'


def require(ok, reason):
    if not ok:raise ValueError(reason)


def load_json(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'DUPLICATE_JSON_KEY')
            result[key] = value
        return result
    def invalid(_):raise ValueError('NONFINITE_JSON_CONSTANT')
    return json.loads(raw, object_pairs_hook=unique, parse_constant=invalid)


def classify(data):
    require(type(data) is dict and set(data) == {'data_class', 'permutations',
            'original_vote_histogram', 'guard_rejections', 'exact_ties', 'integer_proofs'}, 'DIAGNOSTIC_SCHEMA')
    require(data['data_class'] == 'ARTIFICIAL_ONLY', 'ARTIFICIAL_SCOPE_REQUIRED')
    for key, expected in (('guard_rejections', 11), ('exact_ties', 35), ('integer_proofs', 35)):
        require(type(data[key]) is int and data[key] == expected, 'DIAGNOSTIC_COUNT:'+key)
    rows = data['permutations']
    require(type(rows) is list and len(rows) == 35, 'CASE_COVERAGE')
    seen, histogram, rejected = set(), Counter(), 0
    for row in rows:
        require(type(row) is dict and set(row) == {'positive_positions', 'original', 'exact',
                'integer_witness', 'original_rejected_by_exact_votes'}, 'CASE_SCHEMA')
        positions = row['positive_positions']
        require(type(positions) is list and len(positions) == 3 and
                all(type(i) is int and 0 <= i < 7 for i in positions) and
                positions == sorted(set(positions)), 'CASE_IDENTITY')
        key = tuple(positions)
        require(key not in seen, 'DUPLICATE_CASE')
        seen.add(key)
        original = row['original']
        require(type(original) is dict, 'ORIGINAL_PAIR_REQUIRED')
        votes = tuple(original.get(k) for k in ('sessions_better', 'sessions_equal', 'sessions_worse'))
        require(all(type(v) is int and 0 <= v <= 2 for v in votes) and sum(votes) == 2, 'VOTE_TYPE_OR_COUNT')
        flag = row['original_rejected_by_exact_votes']
        require(type(flag) is bool and flag == (votes != (0, 2, 0)), 'FLAG_VOTE_MISMATCH')
        histogram[str(votes)] += 1
        rejected += flag
    require(seen == set(combinations(range(7), 3)), 'CASE_UNIVERSE')
    reported = data['original_vote_histogram']
    require(type(reported) is dict and all(type(v) is int for v in reported.values()) and
            reported == dict(histogram) and rejected == data['guard_rejections'], 'HISTOGRAM_MISMATCH')
    return {'status': 'BLOCKED_ORIGINAL_R077_UNREPAIRED', 'exit_code': 2,
            'engineering_preflight': 'COMPLETE', 'production_ready': False,
            'original_failure_cases': rejected, 'artificial_cases': len(seen),
            'exact_supplement': 'EXISTING_B18_DIAGNOSTIC_MATCHED_NOT_A_PRODUCTION_REPAIR',
            'human_rescoring': 'NOT_RUN', 'scientific_reacceptance': 'NOT_RUN'}


def validate_shadow(data, original):
    require(type(data) is dict and set(data) == {'rows', 'tiny'}, 'SHADOW_SCHEMA')
    require(type(data['rows']) is list and len(data['rows']) == 35, 'SHADOW_COVERAGE')
    indexed = {tuple(row['positive_positions']): row for row in original['permutations']}
    seen = set()
    for row in data['rows']:
        require(type(row) is dict and set(row) == {'positive_positions', 'old_pair',
                'corrected_pair', 'exact_pair', 'integer_witness'}, 'SHADOW_CASE_SCHEMA')
        positions = row['positive_positions']
        require(type(positions) is list and all(type(i) is int for i in positions), 'SHADOW_CASE_ID')
        key = tuple(positions)
        require(key in indexed and key not in seen, 'SHADOW_CASE_UNIVERSE')
        seen.add(key)
        for field, source in (('old_pair', 'original'), ('integer_witness', 'integer_witness')):
            require(json.dumps(row[field], sort_keys=True) == json.dumps(indexed[key][source], sort_keys=True),
                    'SHADOW_ORIGINAL_BINDING')
        for field in ('corrected_pair', 'exact_pair'):
            pair = row[field]
            require(type(pair) is dict and type(pair.get('sessions')) is int and pair['sessions'] == 2,
                    'SHADOW_PAIR_SHAPE')
            for name, expected in (('sessions_better', 0), ('sessions_equal', 2), ('sessions_worse', 0)):
                require(type(pair.get(name)) is int and pair[name] == expected, 'SHADOW_TIE_VOTE')
        require(row['exact_pair'].get('Brier_delta_all_original_sessions_equal') == '0', 'SHADOW_EXACT_DELTA')
    require(seen == set(indexed), 'SHADOW_CASE_UNIVERSE')
    tiny = data['tiny']
    require(type(tiny) is dict and set(tiny) == {'original_equal_sessions', 'candidate_worse_sessions',
            'expected_delta', 'actual_delta'}, 'SHADOW_TINY_SCHEMA')
    require(type(tiny['original_equal_sessions']) is int and tiny['original_equal_sessions'] == 2 and
            type(tiny['candidate_worse_sessions']) is int and tiny['candidate_worse_sessions'] == 2 and
            type(tiny['actual_delta']) is str and tiny['actual_delta'] == tiny['expected_delta'] and
            tiny['actual_delta'] != '0', 'SHADOW_TINY_DIRECTION')
    return {'corrected_orders': len(seen), 'production_ready': False,
            'status': 'PASS_ARTIFICIAL_SHADOW_ONLY_PINNED_CANDIDATE', 'tiny': tiny}


def git(repo, *args):
    try:
        return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as exc:
        raise ValueError('GIT_SOURCE_UNAVAILABLE') from exc


def identity(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'git_blob': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}


def capture(repo, snapshot):
    head = git(repo, 'rev-parse', 'HEAD^{commit}').decode().strip()
    manifest_raw = git(repo, 'show', SOURCE_COMMIT+':'+MANIFEST)
    pins = load_json(manifest_raw)['sources']
    require(type(pins) is dict and len(pins) == 40, 'PINNED_SOURCE_COVERAGE')
    for name, expected in pins.items():
        path = PurePosixPath(name)
        require(not path.is_absolute() and '..' not in path.parts and str(path) == name, 'SOURCE_PATH')
        raw = git(repo, 'show', SOURCE_COMMIT+':'+name)
        require(identity(raw) == expected, 'FIXED_OBJECT_IDENTITY:'+name)
        require(identity((Path(repo)/name).read_bytes()) == expected, 'WORKTREE_IDENTITY:'+name)
        require(git(repo, 'rev-parse', head+':'+name).decode().strip() == expected['git_blob'], 'CHECKOUT_IDENTITY:'+name)
        target = snapshot/name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    return head, pins, identity(manifest_raw)


def candidate_shadow(repo, snapshot, head, original, python):
    manifest_raw = git(repo, 'show', CANDIDATE_COMMIT+':'+CANDIDATE_DIR+'/pins.json')
    pins = load_json(manifest_raw)
    sources = {}
    for name, blob in pins.items():
        raw = git(repo, 'show', CANDIDATE_COMMIT+':'+name)
        fp = identity(raw)
        require(fp['git_blob'] == blob and identity((Path(repo)/name).read_bytes()) == fp and
                git(repo, 'rev-parse', head+':'+name).decode().strip() == blob, 'CANDIDATE_INPUT_IDENTITY:'+name)
        target = snapshot/name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        sources[name] = fp
    for name in ('candidate.py', 'test_candidate.py', 'pins.json'):
        path = CANDIDATE_DIR+'/'+name
        raw = git(repo, 'show', CANDIDATE_COMMIT+':'+path)
        target = snapshot/path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        sources[path] = identity(raw)
    test_code = ('import sys,unittest;sys.path.insert(0,sys.argv[1]);'
                 'unittest.main(module="test_candidate",argv=["R077-shadow"],verbosity=2)')
    tests_command = python+['-c', test_code, str(snapshot/CANDIDATE_DIR)]
    tests = subprocess.run(tests_command, cwd=snapshot, capture_output=True, timeout=60)
    require(tests.returncode == 0 and not tests.stdout and
            re.findall(rb'(?m)^Ran ([0-9]+) tests? in', tests.stderr) == [b'12'] and
            tests.stderr.rstrip().endswith(b'\n\nOK'), 'CANDIDATE_TEST_FAILURE')
    code = '''import sys,json
sys.path.insert(0,sys.argv[1])
from candidate import score_exact_brier,original
from case import legacy_fit,target_cases,integer_witness
from test_candidate import tiny_case,PAIR
rows=[]
for positions,sessions in target_cases():
 old=original.score_with_frozen_source(legacy_fit(),sessions)['paired_differences'][PAIR]
 out=score_exact_brier(legacy_fit(),sessions)
 rows.append({'positive_positions':positions,'old_pair':old,
 'corrected_pair':out['scores']['paired_differences'][PAIR],
 'exact_pair':out['exact_Brier']['paired_differences'][PAIR],
 'integer_witness':integer_witness([e[4] for e in next(iter(sessions.values()))['events']])})
fit,sessions,delta=tiny_case();out=score_exact_brier(fit,sessions)
tiny={'original_equal_sessions':original.score_with_frozen_source(fit,sessions)['paired_differences'][PAIR]['sessions_equal'],
'candidate_worse_sessions':out['scores']['paired_differences'][PAIR]['sessions_worse'],
'expected_delta':str(delta),'actual_delta':out['exact_Brier']['paired_differences'][PAIR]['Brier_delta_all_original_sessions_equal']}
print(json.dumps({'rows':rows,'tiny':tiny},indent=2))
'''
    command = python+['-c', code, str(snapshot/CANDIDATE_DIR)]
    child = subprocess.run(command, cwd=snapshot, capture_output=True, timeout=60)
    require(child.returncode == 0 and not child.stderr, 'CANDIDATE_SHADOW_CHILD_FAILURE')
    data = load_json(child.stdout)
    result = validate_shadow(data, original)
    result.update(candidate_commit=CANDIDATE_COMMIT, sources=sources, data=data,
                  tests_command=tests_command, tests_exit=tests.returncode,
                  tests_stderr=tests.stderr.decode(), tests_stderr_sha256=hashlib.sha256(tests.stderr).hexdigest(),
                  command=command, child_exit=child.returncode,
                  stdout_sha256=hashlib.sha256(child.stdout).hexdigest(),
                  scientific_adoption='NOT_AUTHORIZED', original_scorer_hook='NOT_INSTALLED')
    return result


def verify(repo, shadow=False):
    own_raw = Path(__file__).read_bytes()
    with tempfile.TemporaryDirectory(prefix='r077-preflight-') as directory:
        snapshot = Path(directory)
        head, identities, manifest_identity = capture(repo, snapshot)
        # Reuse B's existing DIAGNOSTICS string unchanged, including its exact
        # kernel checks. No scoring implementation is recreated in Codex A.
        bootstrap = ('import runpy,sys;sys.path.insert(0,sys.argv[1]);'
                     'd=runpy.run_path(sys.argv[1]+"/replay.py",run_name="B18_PINNED_DIAGNOSTIC");'
                     'exec(d["DIAGNOSTICS"])')
        python = [sys.executable, '-I', '-B']+(['-O'] if sys.flags.optimize else [])
        command = python+['-c', bootstrap, str(snapshot/OWN)]
        child = subprocess.run(command, cwd=snapshot, capture_output=True, timeout=60)
        require(child.returncode == 0 and not child.stderr, 'PINNED_DIAGNOSTIC_CHILD_FAILURE')
        diagnostic = load_json(child.stdout)
        result = classify(diagnostic)
        if shadow:
            result['candidate_shadow'] = candidate_shadow(repo, snapshot, head, diagnostic, python)
    require(Path(__file__).read_bytes() == own_raw, 'PREFLIGHT_SOURCE_CHANGED_DURING_EXECUTION')
    result.update(tested_checkout_sha=head, source_commit=SOURCE_COMMIT, sources=identities,
                  manifest_identity=manifest_identity, adapter_identity=identity(own_raw),
                  python=sys.version, optimized=bool(sys.flags.optimize),
                  diagnostic_command=command, diagnostic_exit=child.returncode,
                  diagnostic_stdout_sha256=hashlib.sha256(child.stdout).hexdigest(),
                  diagnostic_stderr_sha256=hashlib.sha256(child.stderr).hexdigest(),
                  diagnostic=diagnostic, production_invocation='NEW_PREFLIGHT_ENTRY_ONLY_ORIGINAL_SCORER_UNCHANGED',
                  historical_results='UNCHANGED_NOT_REINTERPRETED', new_human_scores=0,
                  new_E2_E3=0, external_team_replications=0, CI='NOT_RUN',
                  R073='FROZEN_UNCHANGED', PESEN_v0_1='FROZEN_UNCHANGED')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo', type=Path)
    parser.add_argument('--artificial-preflight', action='store_true', required=True)
    parser.add_argument('--candidate-shadow', action='store_true', help='Opt in to pinned PR28 synthetic shadow; never enables production.')
    args = parser.parse_args()
    try:result = verify(args.repo, shadow=args.candidate_shadow)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(json.dumps({'status': 'BLOCKED_INVALID_PREFLIGHT', 'reason': str(exc)[:240]}))
        return 1
    print(json.dumps(result, indent=2))
    return result['exit_code']


if __name__ == '__main__':sys.exit(main())
