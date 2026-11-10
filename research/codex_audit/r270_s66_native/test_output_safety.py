import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import run_native

ROOT=Path(__file__).resolve().parents[3]
FIRST='r_original'


class OutputSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'source'
        self.out=Path(self.temp.name)/'out';self.out.mkdir()
        for path in run_native.PINS:
            target=self.root/path;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/path,target)
        self.note=self.root/'unlisted_source_note.txt'
        self.note.write_bytes(b'Preserve source-local notes outside the declared scientific input set.\n')

    def invoke(self):
        command=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
        command += [run_native.__file__,str(self.root),'--output',str(self.out)]
        return subprocess.run(command,capture_output=True,text=True,timeout=90)

    def alias(self,name,hard=False):
        path=self.out/name
        if hard:os.link(self.note,path)
        else:path.symlink_to(self.note)
        before=self.note.read_bytes();p=self.invoke()
        self.assertEqual(self.note.read_bytes(),before,'unlisted source file overwritten')
        self.assertNotEqual(p.returncode,0,'unsafe output accepted')
        self.assertTrue(path.exists(),'rejected alias was removed')
        self.assertIn('unsafe output',p.stderr)

    def test_stdout_symlink_preserves_unlisted_source(self):self.alias(FIRST+'.stdout')
    def test_stderr_symlink_preserves_unlisted_source(self):self.alias(FIRST+'.stderr')
    def test_stdout_hardlink_preserves_unlisted_source(self):self.alias(FIRST+'.stdout',True)
    def test_execution_alias_rejected_before_unlink(self):self.alias('execution.json')

    def test_dangling_log_alias_cannot_create_source_file(self):
        target=self.root/'must_not_be_created';path=self.out/(FIRST+'.stdout');path.symlink_to(target)
        p=self.invoke()
        self.assertFalse(target.exists());self.assertTrue(path.is_symlink())
        self.assertNotEqual(p.returncode,0);self.assertIn('unsafe output',p.stderr)

    def test_declared_input_protection_is_preserved(self):
        target=self.root/next(iter(run_native.PINS));raw=target.read_bytes()
        (self.out/(FIRST+'.stdout')).symlink_to(target)
        p=self.invoke()
        self.assertNotEqual(p.returncode,0);self.assertEqual(target.read_bytes(),raw)

    def test_full_replay_preserves_entire_source_snapshot(self):
        before={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        p=self.invoke();self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(json.loads((self.out/'execution.json').read_text())['status'],'COMPLETE')
        after={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before,after)

    def test_dp_output_alias_preserves_unlisted_source(self):self.alias('DP_full_receipt.json')


if __name__=='__main__':unittest.main()
