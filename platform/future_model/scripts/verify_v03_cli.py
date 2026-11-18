"""Execute installed CLI commands, restore original archives, and verify stable v0.3 identities."""
import argparse
from hashlib import sha256
import io
import json
import os
from pathlib import Path
import platform
import sqlite3
import subprocess
import sys
import tarfile
import tempfile

from psychohistory.contracts import canonical


V01 = '7ea6eab94433e3669b6f492d802bb35316dc90d6'
V02 = 'dd05f32f79efc2f4f4f37117cc039dca1008ed76'
LOGISTIC = {'initial': ['1/4', '3/4'], 'payoff': [['2', '2'], ['1', '1']],
            'method': 'rk4', 'steps': 40, 'step_size': '1/20'}
HAWK = {'initial': ['1/2', '1/2'], 'payoff': [['-2', '2'], ['0', '1']],
        'method': 'euler', 'steps': 1, 'step_size': '4'}
DEGROOT = {'opinions': ['0', '1'], 'weights': [['1/2', '1/2'], ['1/4', '3/4']], 'steps': 32}
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'src'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(repo, receipt):
    report = {'status': 'FAIL', 'commands': [], 'python': platform.python_version(),
              'optimization': sys.flags.optimize, 'sqlite': sqlite3.sqlite_version,
              'platform': platform.platform()}

    def command(argv, source=SOURCE, expected=0):
        argv = list(map(str, argv))
        env = {**os.environ, 'PYTHONPATH': str(source)}
        result = subprocess.run(argv, env=env, cwd=repo, capture_output=True, timeout=90)
        report['commands'].append({'argv': argv, 'source': str(source), 'exit_code': result.returncode,
                                   'stderr': result.stderr.decode(errors='replace'),
                                   'stdout_sha256': sha256(result.stdout).hexdigest()})
        require(result.returncode == expected,
                f'{argv[4:]}: expected exit {expected}, actual {result.returncode}: {result.stderr[-600:]}')
        return result.stdout

    def cli(root, *args, source=SOURCE, expected=0):
        data = command([sys.executable, *('-O' for _ in range(sys.flags.optimize)),
                        '-m', 'psychohistory.cli', '--repo', repo, '--data', root, *args],
                       source=source, expected=expected)
        return json.loads(data) if expected == 0 else None

    try:
        report['head'] = command(['git', 'rev-parse', 'HEAD']).decode().strip()
        with tempfile.TemporaryDirectory(prefix='ph-v03-acceptance-') as temp:
            home = Path(temp)
            root = home / 'v03'
            ids = {r: cli(root, 'research', 'register', r)['source_id'] for r in ('R123', 'R132')}

            def trajectory(research, spec, name, branch=None):
                kind = {'R123': 'r123-degroot', 'R132': 'r132-replicator'}[research]
                extra = ['--branch-from', branch] if branch else []
                run = cli(root, 'mechanism', 'submit', kind, '1.0.0', ids[research],
                          '--parameters', json.dumps(spec), *extra)
                identity = run['id']
                require(run['status'] == 'PENDING', 'Approval was not required')
                cli(root, 'mechanism', 'result', identity, expected=1)
                done = cli(root, 'mechanism', 'approve', identity)
                artifact = cli(root, 'mechanism', 'result', identity)
                value = artifact['result']
                require(done['status'] == 'COMPLETED' and done['result_hash'] == artifact['artifact_sha256'],
                        'Artifact does not match the completed run')
                require(sha256(canonical(value).encode()).hexdigest() == artifact['artifact_sha256'],
                        'Artifact canonical identity mismatch')
                report.setdefault('trajectories', {})[name] = {
                    'run_id': identity, 'artifact_sha256': artifact['artifact_sha256'],
                    'snapshot_sha256': value['snapshot']['content_hash'], 'source_id': ids[research],
                    'code_sha256': done['code_sha256'], 'limits': done['limits'],
                    'diagnostics': value['diagnostics'],
                    'trajectory_sha256': sha256(canonical(value['trajectory']).encode()).hexdigest(),
                }
                return identity, artifact

            left, logistic = trajectory('R132', LOGISTIC, 'logistic_rk4')
            right, _ = trajectory('R132', {**LOGISTIC, 'method': 'euler'}, 'logistic_euler')
            other, degroot = trajectory('R123', DEGROOT, 'degroot')
            hawk, _ = trajectory('R132', HAWK, 'hawk_large_euler')
            _, _ = trajectory('R132', {k: v for k, v in {**HAWK, 'method': 'eq3'}.items()
                                       if k != 'step_size'}, 'hawk_eq3')
            _, resumed = trajectory('R132', {**LOGISTIC, 'steps': 4}, 'continued', left)
            require(resumed['result']['trajectory'][0] == logistic['result']['trajectory'][-1],
                    'Resumed trajectory loses the final saved state')
            comparison = cli(root, 'mechanism', 'compare', left, right)
            require(comparison['max_abs_difference'] > 0 and comparison['samples'] == 41,
                    'Euler and RK4 did not produce a bounded independent comparison')
            report['comparison'] = comparison
            cli(root, 'mechanism', 'compare', left, right, '--metric', 'brier', expected=1)
            cli(root, 'mechanism', 'compare', left, other, expected=1)
            cli(root, 'mechanism', 'compare', left, hawk, expected=1)
            cli(root, 'result', other, expected=1)
            cli(root, 'research', 'result', other, expected=1)
            cli(root, 'mechanism', 'submit', 'r132-replicator', '1.0.0', ids['R132'],
                '--parameters', json.dumps({**HAWK, 'step_size': '5'}), expected=1)

            backup, restored = home/'v03-backup', home/'v03-restored'
            manifest = cli(root, 'backup', backup)
            cli(restored, 'restore', backup)
            require(cli(restored, 'mechanism', 'result', other) == degroot,
                    'Restored v0.3 artifact changed')
            report['v03_restore'] = {'artifact_sha256': degroot['artifact_sha256'],
                                     'backup_manifest_sha256': sha256(canonical(manifest).encode()).hexdigest()}

            for name, version in [('v01', V01), ('v02', V02)]:
                archive_dir = home / f'{name}-code'
                archive = command(['git', 'archive', version, 'platform/future_model/src'])
                with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
                    stream.extractall(archive_dir, filter='data')
                old_source = archive_dir/'platform/future_model/src'
                old, backup, restored = (home/f'{name}-{suffix}' for suffix in ('data', 'backup', 'restored'))
                if name == 'v01':
                    original = cli(old, 'demo', '--rounds', 4, '--population', 8, source=old_source)
                    identity = original['run']['id']
                    lookup = ('result', identity)
                    expected = original['result']
                    artifact_hash = original['run']['result_hash']
                else:
                    source = cli(old, 'research', 'register', 'R123', source=old_source)
                    protocol = cli(old, 'research', 'protocol', source['source_id'],
                                   '--seed', 829, source=old_source)['protocol_id']
                    cli(old, 'research', 'approve-protocol', protocol, source=old_source)
                    item = cli(old, 'research', 'submit', protocol, source=old_source)
                    identity = item['id']
                    cli(old, 'research', 'approve', identity, source=old_source)
                    lookup = ('research', 'result', identity)
                    expected = cli(old, *lookup, source=old_source)
                    artifact_hash = expected['artifact_sha256']
                    old_status = cli(old, 'research', 'status', identity, source=old_source)
                manifest = cli(old, 'backup', backup, source=old_source)
                cli(restored, 'restore', backup)
                require(cli(restored, *lookup) == expected, f'{name} artifact changed after restore')
                if name == 'v02':
                    current = cli(restored, 'research', 'status', identity)
                    require(current['holdout_started_at'] == old_status['holdout_started_at']
                            and current['holdout_started_at'] is not None,
                            'Restored v0.2 holdout reservation changed')
                    cli(restored, 'research', 'submit', protocol, expected=1)
                    require(cli(restored, 'research', 'status', identity) == current,
                            'Restored v0.2 holdout was altered by submit')
                report[f'{name}_restore'] = {
                    'source_commit': version, 'artifact_sha256': artifact_hash,
                    'backup_manifest_sha256': sha256(canonical(manifest).encode()).hexdigest(),
                }
        report['status'] = 'PASS'
    finally:
        receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: report[key] for key in ('status', 'head', 'v01_restore', 'v02_restore', 'v03_restore')}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    verify(args.repo.resolve(), args.report)
