import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import replay

ROOT=Path(__file__).resolve().parents[3]
COMPOSITE='research/evidence_audit/r333_r340_composite_acceptance_20261101.py'
RECEIPT='research/R333/R333_MACHINE_RECEIPT.json'


class ReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(prefix='r333-source-tests-');cls.addClassCleanup(cls.temp.cleanup)
        cls.root=Path(cls.temp.name)/'repo'
        subprocess.run(['git','clone','--shared','--no-checkout',str(ROOT),str(cls.root)],check=True,capture_output=True)
        subprocess.run(['git','checkout','--detach',replay.BASE],cwd=cls.root,check=True,capture_output=True)

    def test_real_existing_composition_keeps_scientific_boundary(self):
        result=replay.verify(self.root)
        self.assertEqual(result['status'],'COMPLETE_AUTHENTICATED_LOCAL_COMPOSITION')
        self.assertEqual(result['composite_receipt']['math_child_checks_claimed'],32)
        self.assertIs(result['production_ready'],False)
        self.assertEqual(result['scientific_acceptance'],'NOT_RUN')
        self.assertEqual(len(result['sources']),56)

    def test_forged_composite_pass_is_rejected_before_execution(self):
        p=self.root/COMPOSITE;old=p.read_bytes()
        try:
            p.write_text('print("FORGED_SUCCESS_WITHOUT_GATE_EXECUTION")\n')
            with self.assertRaisesRegex(ValueError,'identity mismatch'):replay.capture(self.root)
        finally:p.write_bytes(old)

    def test_missing_claim_receipt_is_rejected(self):
        p=self.root/RECEIPT;old=p.read_bytes()
        try:
            p.unlink()
            with self.assertRaises((OSError,ValueError)):replay.capture(self.root)
        finally:p.write_bytes(old)

    def test_symlink_claim_is_not_accepted(self):
        p=self.root/RECEIPT;old=p.read_bytes();target=Path(self.temp.name)/'linked-claim.json';target.write_bytes(old)
        try:
            p.unlink();p.symlink_to(target)
            with self.assertRaisesRegex(ValueError,'LINKED_SOURCE'):replay.capture(self.root)
        finally:p.unlink();p.write_bytes(old)

    def test_current_git_tree_must_match_fixed_sources(self):
        p=self.root/COMPOSITE;old=p.read_bytes()
        base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=self.root).decode().strip()
        try:
            p.write_bytes(old+b'\n# disposable tree change\n')
            subprocess.run(['git','add',COMPOSITE],cwd=self.root,check=True,capture_output=True)
            subprocess.run(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','temporary source change'],cwd=self.root,check=True,capture_output=True)
            p.write_bytes(old)
            with self.assertRaisesRegex(ValueError,'CHECKOUT_IDENTITY'):replay.capture(self.root)
        finally:
            subprocess.run(['git','reset','--hard',base],cwd=self.root,check=True,capture_output=True)

    def test_git_replace_cannot_execute_substituted_helper(self):
        helper='research/codex_a/r257_s53_authenticated/authenticate.py'
        original=subprocess.check_output(['git','rev-parse',replay.BASE+':'+helper],cwd=self.root).decode().strip()
        raw=(self.root/helper).read_bytes()
        marker=Path(self.temp.name)/'untrusted-helper-executed'
        changed=raw+b'\nfrom pathlib import Path\n'+('Path('+repr(str(marker))+').write_text("UNTRUSTED")\n').encode()
        substituted=subprocess.check_output(['git','hash-object','-w','--stdin'],input=changed,cwd=self.root).decode().strip()
        subprocess.run(['git','replace',original,substituted],cwd=self.root,check=True,capture_output=True)
        try:
            try:replay.capture(self.root)
            except ValueError:pass
            self.assertFalse(marker.exists(),'Substituted helper executed before authentication')
        finally:subprocess.run(['git','replace','-d',original],cwd=self.root,check=True,capture_output=True)

    def test_inherited_git_directory_cannot_redirect_source_repository(self):
        error=None
        with patch.dict(os.environ,{'GIT_DIR':str(Path(self.temp.name)/'not-a-repository'),
                                    'GIT_WORK_TREE':str(Path(self.temp.name)/'not-the-requested-root')}):
            try:replay.capture(self.root)
            except ValueError as exc:error=str(exc)
        self.assertIsNone(error,'Inherited Git environment redirected source lookup: '+str(error))

    def test_child_failure_cannot_be_promoted_to_success(self):
        executable=Path(self.temp.name)/'reject-node';executable.write_text('#!/bin/sh\nexit 9\n');executable.chmod(0o755)
        with self.assertRaisesRegex(ValueError,'COMPOSITE_CHILD_EXIT'):replay.verify(self.root,node=str(executable))


if __name__=='__main__':unittest.main()
