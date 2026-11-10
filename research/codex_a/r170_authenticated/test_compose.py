import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import compose as gate

ROOT = Path(__file__).resolve().parents[3]
P8 = '1d8294ee81c7e23cb16bb8882ebc619089a35c65'
P9 = '89a64ecd2975a7fa0409f000cef45b1b2792a8b4'


class CompositionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.root = self.work / 'root'
        self.pr8 = self.work / 'pr8'
        self.pr8.mkdir()
        self.identity = self.work / 'identity_gate.py'
        for path in gate.SOURCES:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, target)
        for name in gate.CODE:
            commit, path = ((P9, 'research/codex_audit/r170_identity_gate/'+name) if name == 'identity_gate.py'
                            else (P8, 'research/codex_audit/r170_full_state/'+name))
            target = self.identity if name == 'identity_gate.py' else self.pr8 / name
            target.write_bytes(subprocess.check_output(['git','-C',str(ROOT),'show',commit+':'+path]))

    def verify(self):
        return gate.verify(self.root,self.pr8,self.identity)

    def test_real_composition_and_source_stability(self):
        files = [self.root/p for p in gate.SOURCES]+list(self.pr8.iterdir())+[self.identity]
        before = {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
        result = self.verify()
        self.assertEqual(result['status'],'COMPLETE_PINNED_R170_COMPOSITION')
        self.assertEqual(result['pinned_pr8_commit'],P8)
        self.assertEqual(result['pinned_pr9_commit'],P9)
        self.assertEqual(result['full_state_comparison']['state_mass_comparisons'],23328)
        self.assertEqual(result['identity_gate']['B_receipt_bytes'],23004)
        self.assertEqual(result['full_frozen_extension_acceptance'],'PARTIAL')
        self.assertEqual(result['witness_order_compliance'],'NOT_ESTABLISHED')
        self.assertEqual(before,{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})

    def test_each_source_change_blocks(self):
        for path in gate.SOURCES:
            with self.subTest(path=path):
                p=self.root/path;raw=p.read_bytes();p.write_bytes(raw+b'\n')
                with self.assertRaisesRegex(ValueError,'identity mismatch'):self.verify()
                p.write_bytes(raw)

    def test_each_executable_change_blocks_before_execution(self):
        for name in gate.CODE:
            with self.subTest(name=name):
                p=self.identity if name=='identity_gate.py' else self.pr8/name
                raw=p.read_bytes();p.write_bytes(raw+b'\n')
                with patch.object(gate.subprocess,'run') as child:
                    with self.assertRaisesRegex(ValueError,'identity mismatch'):self.verify()
                    child.assert_not_called()
                p.write_bytes(raw)

    def test_old_runner_is_not_silently_accepted_after_pin_upgrade(self):
        raw=subprocess.check_output(['git','-C',str(ROOT),'show',
            'fd0d2c65084d1ef99b6040ce0464b237c38431b5:research/codex_audit/r170_full_state/run_audit.py'])
        (self.pr8/'run_audit.py').write_bytes(raw)
        with self.assertRaisesRegex(ValueError,'identity mismatch'):self.verify()

    def test_missing_dependency_blocks(self):
        self.identity.unlink()
        with self.assertRaises(OSError):self.verify()

    def test_child_failure_blocks(self):
        fake=subprocess.CompletedProcess([],1,'{}','failure')
        with patch.object(gate.subprocess,'run',return_value=fake):
            with self.assertRaisesRegex(ValueError,'child exit'):self.verify()

    def test_forged_child_success_blocks(self):
        fake=subprocess.CompletedProcess([],0,'{"status":"COMPLETE"}','')
        with patch.object(gate.subprocess,'run',return_value=fake):
            with self.assertRaisesRegex(ValueError,'summary mismatch'):self.verify()

    def test_duplicate_summary_key_blocks(self):
        fake=subprocess.CompletedProcess([],0,'{"status":"FAILED","status":"COMPLETE"}','')
        with patch.object(gate.subprocess,'run',return_value=fake):
            with self.assertRaisesRegex(ValueError,'duplicate JSON key'):self.verify()

    def test_identity_failure_after_successful_comparison_blocks(self):
        original=gate.subprocess.run
        def fail_identity(command, **kwargs):
            if any(str(p).endswith('/identity_gate.py') for p in command):
                return subprocess.CompletedProcess(command,1,'{}','identity rejected')
            return original(command,**kwargs)
        with patch.object(gate.subprocess,'run',side_effect=fail_identity):
            with self.assertRaisesRegex(ValueError,'child exit'):self.verify()

    def test_false_identity_boolean_in_execution_blocks(self):
        original=gate.subprocess.run
        def corrupt_execution(command, **kwargs):
            result=original(command,**kwargs)
            if any(str(p).endswith('/run_audit.py') for p in command):
                output=Path(command[command.index('--output')+1])/'execution.json'
                data=json.loads(output.read_bytes())
                data['B_complete_receipt_matches_historical_bytes']=False
                output.write_text(json.dumps(data))
            return result
        with patch.object(gate.subprocess,'run',side_effect=corrupt_execution):
            with self.assertRaisesRegex(ValueError,'comparison execution mismatch'):self.verify()

    def test_float_count_in_identity_result_blocks(self):
        original=gate.subprocess.run
        def corrupt_identity(command, **kwargs):
            result=original(command,**kwargs)
            if any(str(p).endswith('/identity_gate.py') for p in command):
                data=json.loads(result.stdout);data['B_receipt_bytes']=23004.0
                output=Path(command[command.index('--output')+1])
                output.write_text(json.dumps(data));result.stdout=json.dumps(data)
            return result
        with patch.object(gate.subprocess,'run',side_effect=corrupt_identity):
            with self.assertRaisesRegex(ValueError,'identity result mismatch'):self.verify()

    def test_cli_missing_dependency_returns_blocked(self):
        self.identity.unlink()
        command=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
        command += [str(Path(gate.__file__)),str(self.root),'--pr8-dir',str(self.pr8),'--identity-gate',str(self.identity)]
        p=subprocess.run(command,capture_output=True,text=True)
        self.assertNotEqual(p.returncode,0)
        self.assertEqual(json.loads(p.stdout)['status'],'BLOCKED')


if __name__=='__main__':unittest.main()
