import argparse
from contextlib import contextmanager
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import socket
import subprocess
import time
from urllib.request import urlopen

parser = argparse.ArgumentParser()
parser.add_argument('sha')
parser.add_argument('destination', type=Path)
options = parser.parse_args()
out = options.destination.resolve()
out.mkdir(parents=True, exist_ok=False)
checkout = out / 'checkout'
project = checkout / 'platform/future_model'
venv = project / '.venv/bin/python'
repo_url = 'https://github.com/edwardsage419/Psychohistory-Research.git'
branch = 'feat/psychohistory-platform-v0.2'
candidate = 'd80739906b7d0134634eafa2f3362e93150f2ec3'
base = '7ea6eab94433e3669b6f492d802bb35316dc90d6'
records = []
env = dict(os.environ)
env.pop('PH_VENV', None)
env.pop('PYTHONOPTIMIZE', None)
env.pop('PYTHONPATH', None)
env.update(PIP_CACHE_DIR='/tmp/psychohistory-pip-cache', npm_config_cache='/tmp/psychohistory-npm-cache')
summary = {'status': 'FAIL', 'tested_commit': options.sha, 'platform': platform.platform(), 'commands': records}

def call(name, args, *, cwd=project, extra=None, timeout=160):
    argv = list(map(str, args))
    selected = extra or {}
    completed = subprocess.run(argv, cwd=cwd, env={**env, **selected}, capture_output=True, timeout=timeout)
    row = {'name': name, 'argv': argv, 'cwd': str(cwd), 'extra_environment': selected, 'exit_code': completed.returncode}
    for key in ('stdout', 'stderr'):
        raw = getattr(completed, key)
        filename = f'{name}.{key}'
        (out / filename).write_bytes(raw)
        row[key] = {'file': filename, 'sha256': sha256(raw).hexdigest()}
    records.append(row)
    print(name, completed.returncode, flush=True)
    if completed.returncode:
        raise RuntimeError(f'{name}: {completed.stderr[-600:].decode(errors="replace")}')
    return completed.stdout.decode()

@contextmanager
def server(data, name):
    with socket.socket() as address:
        address.bind(('127.0.0.1', 0))
        port = address.getsockname()[1]
    url = f'http://127.0.0.1:{port}'
    argv = [str(venv), '-m', 'psychohistory.cli', '--repo', str(checkout), '--data', str(data),
            'serve', '--port', str(port)]
    with (out / f'{name}.log').open('wb') as log:
        p = subprocess.Popen(argv, cwd=project, env={**env, 'PYTHONPATH': str(project / 'src')},
                             stdout=log, stderr=log)
        try:
            for _ in range(100):
                try:
                    with urlopen(url + '/api/v1/health', timeout=.5) as response:
                        if response.status == 200:
                            break
                except OSError:
                    pass
                if p.poll() is not None:
                    raise RuntimeError('Loopback server failed')
                time.sleep(.05)
            else:
                raise RuntimeError('Loopback server did not become ready')
            yield url
        finally:
            p.terminate()
            code = p.wait(timeout=10)
            records.append({'name': name, 'argv': argv, 'exit_code': code, 'shutdown': 'SIGTERM',
                            'log': f'{name}.log', 'log_sha256': sha256((out / f'{name}.log').read_bytes()).hexdigest()})

try:
    call('clone', ['git', 'clone', '--single-branch', '--branch', branch, '--no-tags',
                   repo_url, checkout], cwd=out)
    actual = call('head', ['git', 'rev-parse', 'HEAD'], cwd=checkout).strip()
    if actual != options.sha:
        raise ValueError('Remote checkout identity mismatch')
    call('fetch-references', ['git', 'fetch', 'origin', 'refs/heads/main:refs/remotes/origin/main',
                               'refs/pull/44/head:refs/remotes/origin/v02-candidate-44'], cwd=checkout)
    call('install', ['bash', 'scripts/install.sh'])
    call('verify', ['bash', 'scripts/verify.sh'])
    call('browser-deps', [venv, '-m', 'pip', 'install', '--disable-pip-version-check',
                          '--index-url', 'https://pypi.org/simple', '--only-binary=:all:', '-r',
                          'requirements-browser.lock'])
    call('python-version', [venv, '-c', 'import sys,sqlite3;print(sys.version);print(sqlite3.sqlite_version)'])
    call('node-version', ['node', '--version'])
    call('chromium-version', ['chromium', '--version'])
    for mode, flags, extra in [('normal', [], {}), ('flag', ['-O'], {}),
                               ('env', [], {'PYTHONOPTIMIZE': '1'})]:
        call('guards-' + mode, [venv, *flags, '-S', 'scripts/verify_v02_optimized.py'],
             extra={**extra, 'PYTHONPATH': 'src'})
    call('cli', [venv, 'scripts/verify_v02_cli.py', '--repo', checkout,
                 '--report', out / 'cli.json'])
    call('cli-optimize', [venv, 'scripts/verify_v02_cli.py', '--repo', checkout,
                          '--report', out / 'cli-optimize.json'], extra={'PYTHONOPTIMIZE': '1'})
    first = json.loads((out / 'cli.json').read_text())
    second = json.loads((out / 'cli-optimize.json').read_text())
    if first['artifact_sha256'] != second['artifact_sha256']:
        raise ValueError('Independent normal and optimized artifact hashes differ')
    summary['reproducible_artifact_sha256'] = first['artifact_sha256']
    call('old-backup', [venv, 'scripts/verify_v02_legacy.py', '--repo', checkout,
                         '--baseline', base, '--report', out / 'old-backup.json'])
    data = out / 'browser-data'
    with server(data, 'browser-server') as url:
        call('browser-v02', [venv, 'scripts/browser_v02.py'],
             extra={'PH_TEST_URL': url, 'PH_TEST_DATA': str(data), 'PH_TEST_CANDIDATE_ID': 'R123',
                    'PH_TEST_CANDIDATE_COMMIT': candidate, 'PH_BROWSER_REPORT': str(out / 'browser-v02.json')})
        call('browser-v01', [venv, 'scripts/browser_check.py'],
             extra={'PH_TEST_URL': url, 'PH_TEST_DATA': str(data),
                    'PH_BROWSER_REPORT': str(out / 'browser-v01.json')})
    history = out / 'history-data'
    call('prepare-history', [venv, 'scripts/browser_history_check.py', '--prepare', '--data', history],
         extra={'PYTHONPATH': 'src'})
    with server(history, 'history-server') as url:
        call('browser-history', [venv, 'scripts/browser_history_check.py', '--data', history,
                                 '--url', url, '--report', out / 'browser-history.json'])
    dirty = call('status', ['git', 'status', '--porcelain'], cwd=checkout)
    if dirty:
        raise ValueError(f'Checkout changed during verification: {dirty}')
    summary['status'] = 'PASS'
finally:
    (out / 'execution.json').write_text(json.dumps(summary, indent=2) + '\n')
