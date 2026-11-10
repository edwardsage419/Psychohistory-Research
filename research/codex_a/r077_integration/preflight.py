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
import subprocess
import sys
import tempfile

SOURCE_COMMIT = '9de51508daa160d33d0d05b13ba1454f8333f21d'
OWN = 'research/codex_b/2026-11-10-r077-exact-paired-ties'
MANIFEST = OWN+'/evidence/py312/summary.json'


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


def verify(repo):
    own_raw = Path(__file__).read_bytes()
    with tempfile.TemporaryDirectory(prefix='r077-preflight-') as directory:
        snapshot = Path(directory)
        head, identities, manifest_identity = capture(repo, snapshot)
        # Reuse B's existing DIAGNOSTICS string unchanged, including its exact
        # kernel checks. No scoring implementation is recreated in Codex A.
        bootstrap = ('import runpy,sys;sys.path.insert(0,sys.argv[1]);'
                     'd=runpy.run_path(sys.argv[1]+"/replay.py",run_name="B18_PINNED_DIAGNOSTIC");'
                     'exec(d["DIAGNOSTICS"])')
        command = [sys.executable, '-I', '-B']+(['-O'] if sys.flags.optimize else [])+[
            '-c', bootstrap, str(snapshot/OWN)]
        child = subprocess.run(command, cwd=snapshot, capture_output=True, timeout=60)
        require(child.returncode == 0 and not child.stderr, 'PINNED_DIAGNOSTIC_CHILD_FAILURE')
        diagnostic = load_json(child.stdout)
        result = classify(diagnostic)
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
    args = parser.parse_args()
    try:result = verify(args.repo)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(json.dumps({'status': 'BLOCKED_INVALID_PREFLIGHT', 'reason': str(exc)[:240]}))
        return 1
    print(json.dumps(result, indent=2))
    return result['exit_code']


if __name__ == '__main__':sys.exit(main())
