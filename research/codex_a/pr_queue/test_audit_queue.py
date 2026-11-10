import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import audit_queue as audit


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo=Path(self.temp.name)
        self.git('init','-q')
        self.git('config','user.name','Queue fixture')
        self.git('config','user.email','fixture@example.invalid')
        (self.repo/'x.txt').write_text('base\n')
        self.git('add','x.txt');self.git('commit','-qm','base')
        self.git('branch','-M','main')
        self.git('update-ref','refs/remotes/origin/main','HEAD')
        self.rows=[]
        for number,value in [(1,'left'),(2,'right')]:
            self.git('switch','-qc','pr'+str(number),'main')
            (self.repo/'x.txt').write_text(value+'\n')
            self.git('commit','-qam',value)
            head=self.git('rev-parse','HEAD').strip()
            self.git('update-ref',f'refs/remotes/pr/{number}',head)
            self.rows.append({'number':number,'headRefOid':head,'baseRefName':'main',
                              'title':value,'url':f'https://example.invalid/{number}',
                              'isDraft':True,'statusCheckRollup':[]})
        self.git('switch','-q','main')

    def git(self,*args):
        return subprocess.check_output(['git','-C',str(self.repo),*args],text=True,stderr=subprocess.PIPE)

    def test_real_conflict_and_unchanged_checkout(self):
        head=self.git('rev-parse','HEAD')
        result=audit.audit(self.repo,self.rows)
        self.assertEqual(len(result['prs']),2)
        self.assertTrue(all(p['merge_with_main']['exit']==0 for p in result['prs']))
        self.assertEqual(result['pairs'][0]['exit'],1)
        self.assertTrue(result['conflicts_present'])
        self.assertEqual(self.git('rev-parse','HEAD'),head)
        self.assertEqual(self.git('status','--short'),'')

    def test_deleted_code_is_recorded_without_reading_missing_blob(self):
        (self.repo/'old.py').write_text('x=1\n')
        self.git('add','old.py');self.git('commit','-qm','add old code')
        self.git('update-ref','refs/remotes/origin/main','HEAD')
        self.git('switch','-qc','deleted')
        self.git('rm','-q','old.py');self.git('commit','-qm','delete old code')
        head=self.git('rev-parse','HEAD').strip()
        self.git('update-ref','refs/remotes/pr/3',head)
        row=dict(self.rows[0],number=3,headRefOid=head)
        result=audit.audit(self.repo,[row])
        self.assertEqual(result['prs'][0]['code_identity'],[
            {'path':'old.py','change':'D','git_blob':None,'sha256':None}])

    def test_duplicate_pr_rejected(self):
        with self.assertRaisesRegex(ValueError,'duplicate'):audit.audit(self.repo,[self.rows[0],self.rows[0]])

    def test_boolean_pr_number_rejected(self):
        rows=copy.deepcopy(self.rows);rows[0]['number']=True
        with self.assertRaises(ValueError):audit.audit(self.repo,rows)

    def test_snapshot_head_mismatch_rejected(self):
        rows=copy.deepcopy(self.rows);rows[0]['headRefOid']='0'*40
        with self.assertRaisesRegex(ValueError,'head mismatch'):audit.audit(self.repo,rows)

    def test_missing_field_rejected(self):
        rows=copy.deepcopy(self.rows);del rows[0]['headRefOid']
        with self.assertRaises(ValueError):audit.audit(self.repo,rows)

    def test_empty_snapshot_rejected(self):
        with self.assertRaises(ValueError):audit.audit(self.repo,[])

    def test_other_base_requires_explicit_handling(self):
        rows=copy.deepcopy(self.rows);rows[0]['baseRefName']='other'
        with self.assertRaisesRegex(ValueError,'base'):audit.audit(self.repo,rows)

    def test_missing_ref_rejected(self):
        self.git('update-ref','-d','refs/remotes/pr/2')
        with self.assertRaises(ValueError):audit.audit(self.repo,self.rows)

    def test_cli_duplicate_json_key_rejected(self):
        snap=self.repo/'snapshot.json'
        raw=json.dumps(self.rows).replace('"number": 1','"number": 99, "number": 1')
        snap.write_text(raw)
        command=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
        command += [str(Path(audit.__file__)),str(self.repo),str(snap)]
        p=subprocess.run(command,capture_output=True,text=True)
        self.assertNotEqual(p.returncode,0)
        self.assertEqual(json.loads(p.stdout)['status'],'BLOCKED')


if __name__=='__main__':unittest.main()
