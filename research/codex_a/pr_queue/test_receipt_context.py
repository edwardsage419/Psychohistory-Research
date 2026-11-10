import copy
import hashlib
import unittest
import receipt_context as gate


class ReceiptContextTests(unittest.TestCase):
    def setUp(self):
        self.main='a'*40;self.head='b'*40
        self.logs={'tests/normal.log':b'Ran 2 tests in 0.001s\n\nOK\n','tests/optimized.log':b'Ran 2 tests in 0.001s\n\nOK\n'}
        rows=[dict(pr=1,scope='research/codex_a/example',optimized=opt,exit=0,status='PASS',tests=2,
                   log='tests/'+name+'.log',sha256=hashlib.sha256(self.logs['tests/'+name+'.log']).hexdigest())
              for opt,name in [(False,'normal'),(True,'optimized')]]
        self.old=dict(main=self.main,prs=[dict(number=1,head=self.head)])
        self.current=copy.deepcopy(self.old)
        self.matrix=dict(main=self.main,candidate_head_after=self.main,tracked_main_diff_exit=0,
                         failed_scopes=[],positive_executions=4,scopes=rows)

    def verify(self):return gate.verify(self.old,self.matrix,self.current,self.logs.__getitem__)

    def test_same_source_is_not_a_claim_of_new_execution(self):
        r=self.verify();self.assertEqual(r['status'],'SOURCE_CONTEXT_MATCHES')
        self.assertEqual(r['verified_prior_method_executions'],4)
        self.assertEqual(r['new_test_executions'],0)

    def test_changed_main_requires_rerun(self):
        self.current['main']='c'*40
        self.assertEqual(self.verify()['status'],'RERUN_REQUIRED')

    def test_changed_pr_requires_rerun(self):
        self.current['prs'][0]['head']='c'*40
        self.assertEqual(self.verify()['changed_prs'],[1])

    def test_new_pr_requires_rerun(self):
        self.current['prs'].append(dict(number=2,head='c'*40))
        self.assertEqual(self.verify()['new_prs'],[2])

    def test_corrupt_log_rejected(self):
        self.logs['tests/normal.log']+=b'changed'
        with self.assertRaisesRegex(ValueError,'log hash'):self.verify()

    def test_forged_aggregate_rejected(self):
        self.matrix['positive_executions']=99
        with self.assertRaisesRegex(ValueError,'aggregate'):self.verify()

    def test_duplicate_scope_mode_rejected(self):
        self.matrix['scopes'].append(copy.deepcopy(self.matrix['scopes'][0]))
        with self.assertRaisesRegex(ValueError,'duplicate'):self.verify()

    def test_boolean_count_rejected(self):
        self.matrix['scopes'][0]['tests']=True
        with self.assertRaises(ValueError):self.verify()

    def test_zero_tests_rejected(self):
        self.matrix['scopes'][0]['tests']=0
        with self.assertRaises(ValueError):self.verify()

    def test_missing_hash_rejected(self):
        del self.matrix['scopes'][0]['sha256']
        with self.assertRaises(ValueError):self.verify()

    def test_missing_mode_rejected(self):
        self.matrix['scopes'].pop();self.matrix['positive_executions']=2
        with self.assertRaisesRegex(ValueError,'both modes'):self.verify()

    def test_failed_log_with_coherent_hash_rejected(self):
        raw=b'Ran 2 tests in 0.001s\n\nFAILED (failures=1)\n'
        self.logs['tests/normal.log']=raw
        self.matrix['scopes'][0]['sha256']=hashlib.sha256(raw).hexdigest()
        with self.assertRaisesRegex(ValueError,'log outcome'):self.verify()

    def test_traversal_log_path_rejected(self):
        self.matrix['scopes'][0]['log']='../secret'
        with self.assertRaises(ValueError):self.verify()

    def test_one_log_cannot_claim_two_modes(self):
        self.matrix['scopes'][1]['log']='tests/normal.log'
        with self.assertRaisesRegex(ValueError,'log receipt reused'):self.verify()

    def test_log_path_alias_spelling_is_rejected(self):
        self.logs['tests/./normal.log']=self.logs['tests/normal.log']
        self.matrix['scopes'][1]['log']='tests/./normal.log'
        with self.assertRaises(ValueError):self.verify()

    def test_inner_summary_cannot_inflate_outer_test_count(self):
        raw=b'Ran 99 tests in 0.001s\n\nOK\n\nRan 2 tests in 0.001s\n\nOK\n'
        self.logs['tests/normal.log']=raw
        self.matrix['scopes'][0].update(tests=99,sha256=hashlib.sha256(raw).hexdigest())
        self.matrix['positive_executions']=101
        with self.assertRaisesRegex(ValueError,'log count mismatch'):self.verify()

    def test_duplicate_pr_number_rejected(self):
        self.current['prs'].append(copy.deepcopy(self.current['prs'][0]))
        with self.assertRaises(ValueError):self.verify()


if __name__=='__main__':unittest.main()
