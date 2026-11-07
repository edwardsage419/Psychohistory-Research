import copy
from fractions import Fraction as F
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import run_audit

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
JS='research/validation/r170_observation_ladder_20261026.js'
PY='research/evidence_audit/r170_b_edge_utterance_20261026.py'
J='research/validation/R170_OBSERVATION_LADDER_EXACT_RECEIPT_2026-10-26.json'
SUMMARY='research/evidence_audit/B_R170_INDEPENDENT_PYTHON_EXECUTION_SUMMARY_2026-10-26.json'


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.js=json.loads(subprocess.check_output(['node',str(HERE/'export_js_states.js'),str(ROOT/JS)],text=True))
        cls.py=json.loads(subprocess.check_output([sys.executable,'-B',str(HERE/'export_python_states.py'),str(ROOT/PY)],text=True))

    def test_real_288_laws_and_81_state_universe(self):
        r=run_audit.compare_states(self.js,self.py)
        self.assertEqual(r['snapshots'],288)
        self.assertEqual(r['state_mass_comparisons'],23328)
        self.assertEqual(r['nonzero_entries_per_route'],5099)

    def test_duplicate_snapshot_rejected(self):
        d=copy.deepcopy(self.py);d['records'][1]=copy.deepcopy(d['records'][0])
        with self.assertRaises(ValueError):run_audit.compare_states(self.js,d)

    def test_missing_snapshot_rejected(self):
        d=copy.deepcopy(self.py);d['records'].pop()
        with self.assertRaises(ValueError):run_audit.compare_states(self.js,d)

    def test_normalized_but_different_law_rejected(self):
        d=copy.deepcopy(self.py);row=next(x for x in d['records'] if len(x['law'])>=2)
        a,b=list(row['law'])[:2]
        row['law'][a]=str(F(row['law'][a])+F(1,10000))
        row['law'][b]=str(F(row['law'][b])-F(1,10000))
        with self.assertRaisesRegex(ValueError,'state mass'):run_audit.compare_states(self.js,d)

    def test_invalid_inventory_state_rejected(self):
        d=copy.deepcopy(self.py);law=d['records'][0]['law'];law['0000']=law.pop(next(iter(law)))
        with self.assertRaises(ValueError):run_audit.compare_states(self.js,d)

    def test_boolean_time_rejected(self):
        d=copy.deepcopy(self.py);d['records'][0]['t']=False
        with self.assertRaises(ValueError):run_audit.compare_states(self.js,d)

    def test_float_probability_rejected(self):
        d=copy.deepcopy(self.py);law=d['records'][0]['law'];law[next(iter(law))]=1.0
        with self.assertRaises(ValueError):run_audit.compare_states(self.js,d)

    def test_explicit_lexical_conventions_both_start_complete_alternate(self):
        literal=run_audit.lex_witness(self.js)
        numeric=run_audit.lex_witness(self.js,numeric=True)
        for r in (literal,numeric):
            self.assertEqual((r['graph'],r['initial'],r['t']),('complete','alternate',1))
        self.assertEqual(literal['control_a'],['1/2','both_confirm'])
        self.assertEqual(numeric['control_a'],['1/4','both_confirm'])
        self.assertEqual((literal['tv_O1'],literal['tv_O4']),('0','1/3'))
        self.assertEqual((numeric['tv_O1'],numeric['tv_O4']),('0','1/6'))

    def test_failed_rerun_clears_old_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'out';out.mkdir();receipt=out/'execution.json';receipt.write_text('{"status":"COMPLETE"}')
            p=subprocess.run([sys.executable,'-B',run_audit.__file__,str(Path(tmp)/'missing'),'--output',str(out)],capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0)
            self.assertFalse(receipt.exists())

    def test_complete_audit_source_tree_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'source'
            for path in (JS,PY,J,SUMMARY):
                dest=root/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/path,dest)
            before={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
            out=Path(tmp)/'out'
            p=subprocess.run([sys.executable,'-B',run_audit.__file__,str(root),'--output',str(out)],capture_output=True,text=True,timeout=60)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertTrue((out/'execution.json').exists())
            after={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
            self.assertEqual(before,after)


if __name__=='__main__':unittest.main()
