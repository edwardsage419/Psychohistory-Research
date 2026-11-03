#!/usr/bin/env python3
"""Independent local counterexample for R272's unisolated Python import path.

Creates only temporary synthetic files. It does not run CI or modify a repo.
Run: /usr/bin/python3 -I -S r272_shadow_import_audit_20261103.py
Optional: --source /path/to/authentic/r272_single_entrypoint_failclosed_20261102.py
"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import sys
import tempfile

# These imports reproduce the candidate's actual import block, in source order.
PREFIX = '''from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile
'''


def check(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def run(argv: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=cwd, text=True, capture_output=True,
                          timeout=15, check=False)


def audit(source: Path | None) -> None:
    check('json' not in sys.modules, 'audit interpreter already loaded json; use -I -S')
    with tempfile.TemporaryDirectory(prefix='r272_shadow_import_') as tmp:
        root = Path(tmp)
        directory = root / 'research' / 'validation'
        directory.mkdir(parents=True)
        entry = directory / 'r272_single_entrypoint_failclosed_20261102.py'
        if source is None:
            entry.write_text(PREFIX + "\nraise SystemExit(17)\n", encoding='utf-8')
            mode = 'SOURCE_PREFIX_MIRROR'
        else:
            raw = source.read_text(encoding='utf-8')
            check(PREFIX in raw, 'actual candidate no longer contains audited import block')
            entry.write_text(raw, encoding='utf-8')
            mode = 'ACTUAL_CANDIDATE_SOURCE'
        # This file is NOT among the candidate's pinned input identities.
        (directory / 'json.py').write_text(
            "print('FORGED_R272_PASS_FROM_UNPINNED_JSON_MODULE')\n"
            "raise SystemExit(0)\n", encoding='utf-8')
        clean = run([sys.executable, '-I', '-S', str(entry), '--root', str(root)], cwd=root)
        check(clean.returncode != 0 and 'FORGED_R272_PASS' not in clean.stdout,
              'isolated negative control unexpectedly passed')
        for flags in ([], ['-O'], ['-OO']):
            result = run([sys.executable, *flags, str(entry), '--root', str(root)], cwd=root)
            check(result.returncode == 0 and
                  result.stdout.strip() == 'FORGED_R272_PASS_FROM_UNPINNED_JSON_MODULE',
                  'expected shadow import bypass not reproduced: ' + str(flags)
                  + ' exit=' + str(result.returncode) + ' err=' + result.stderr[-300:])
        print('status=PASS')
        print('test_mode=' + mode)
        print('unisolated_modes_falsely_accepted=3/3')
        print('isolated_negative_control_rejected=1/1')
        print('trusted_original_or_archive_files_used=0')
        print('production_workflow_executed=false')
        print('scope=PYTHON_IMPORT_PATH_SYNTHETIC_E1')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path)
    args = parser.parse_args()
    audit(args.source)


if __name__ == '__main__':
    main()
