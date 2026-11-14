import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import prepare
import run_workflow as runner

ROOT = Path(__file__).resolve().parents[3]


class BoundaryTests(unittest.TestCase):
    def test_context_preserves_claims_without_attestation(self):
        found = runner.context('101', '2', 'firstparty-r127', 'local')
        self.assertEqual(found['run_id'], '101')
        self.assertEqual(found['job_key'], 'firstparty-r127')
        self.assertIsNone(found['numeric_job_id'])
        self.assertIs(found['externally_attested'], False)

    def test_invalid_context_cannot_control_output_paths(self):
        for run, attempt, job in [('0','1','job'),('1','0','job'),('1','1','../job'),('1','1','x/y')]:
            with self.subTest(args=(run,attempt,job)), self.assertRaises(ValueError):
                runner.context(run, attempt, job, 'local')

    def test_immutable_write_and_identical_noop(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); ctx = runner.context('101','1','job','local')
            path, state = runner.store(root, ctx, b'{"valid":true}\n')
            self.assertEqual(state, 'CREATED')
            self.assertEqual(runner.store(root, ctx, path.read_bytes())[1], 'UNCHANGED')
            with self.assertRaises(ValueError):runner.store(root, ctx, b'changed')
            self.assertEqual(path.read_bytes(), b'{"valid":true}\n')

    def test_symlink_and_hardlink_outputs_rejected(self):
        for kind in ('symlink','hardlink'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                root = Path(directory);ctx = runner.context('1','1','job','local')
                path = root/runner.receipt_name(ctx);path.parent.mkdir(parents=True)
                original = root/'unchanged';original.write_bytes(b'preserve')
                if kind == 'symlink':path.symlink_to(original)
                else:
                    import os
                    os.link(original, path)
                with self.assertRaises(ValueError):runner.store(root, ctx, b'changed')
                self.assertEqual(original.read_bytes(), b'preserve')

    def test_symlink_output_parent_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory);ctx = runner.context('1','1','job','local')
            target = root/'protected';target.mkdir()
            parent = root/runner.OWN/'receipts';parent.parent.mkdir(parents=True)
            parent.symlink_to(target, target_is_directory=True)
            with self.assertRaises(ValueError):runner.store(root, ctx, b'changed')
            self.assertFalse(list(target.iterdir()))


class PatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='r127-patch-fixture-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.repo = Path(cls.temp.name)/'repo'
        subprocess.run(['git','clone','--shared','--no-checkout',str(ROOT),str(cls.repo)],check=True,capture_output=True)
        subprocess.run(['git','checkout','--detach',prepare.BASE],cwd=cls.repo,check=True,capture_output=True)

    def test_patch_applies_and_second_preparation_is_noop(self):
        patch, manifest = prepare.build(self.repo)
        self.assertEqual(manifest['state'], 'BASE_MATCHES')
        self.assertEqual(set(manifest['targets']), {prepare.WORKFLOW,prepare.GATE,prepare.PINS})
        subprocess.run(['git','apply','--check','-'],input=patch.encode(),cwd=self.repo,check=True,capture_output=True)
        subprocess.run(['git','apply','-'],input=patch.encode(),cwd=self.repo,check=True,capture_output=True)
        try:
            second, state = prepare.build(self.repo)
            self.assertEqual(second, '')
            self.assertEqual(state['state'], 'ALREADY_APPLIED')
        finally:
            subprocess.run(['git','restore','--',prepare.WORKFLOW,prepare.GATE,prepare.PINS],cwd=self.repo,check=True,capture_output=True)

    def test_changed_workflow_refuses_patch(self):
        path = self.repo/prepare.WORKFLOW;raw = path.read_bytes()
        try:
            path.write_bytes(raw+b'\n# concurrent owner change\n')
            with self.assertRaisesRegex(ValueError, 'STALE_OR_PARTIAL'):prepare.build(self.repo)
        finally:path.write_bytes(raw)


if __name__ == '__main__':unittest.main()
