"""Fault-injection controls for Issue #34. These add zero empirical evidence."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CHECKER=Path(__file__).with_name('r132_phase_b_ci_attest.py')
# Each child isolates intentional stubs from the genuine native regression run.
DRIVER=r'''
import importlib.util,json,sys,uuid
from pathlib import Path
p=Path(sys.argv[1]);out=Path(sys.argv[2]);case=sys.argv[3]
sys.path.insert(0,str(p.parent))
spec=importlib.util.spec_from_file_location('attester',p);a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
if hasattr(a,'_load_math'):a._load_math()
v={'exact_independent_fraction_fields':75,'source_eq3_eq4_valid_state_checks':69}
t={'trajectory_endpoint_independent_comparisons':216,'max_numerical_absolute_error':1e-10,'real_human_or_animal_time_series_used':0}
e={'project_Hawk_original_share':'1/2','project_Hawk_exact_continuous_initial_derivative':'-1/8','Euler_h4_one_step_share':'0','true_continuous_t4_share':.343202279538,'Euler_local_multiplier_h4_at_one_third':'-5/3'}
b={'same_continuous_payoff_differences':True,'original_p149_eq3_unshifted_at_half':'2/5','original_p149_eq3_add_three_to_all_payoffs_at_half':'8/17'}
changes={
'exact_zero':(v,'exact_independent_fraction_fields',0),'states_zero':(v,'source_eq3_eq4_valid_state_checks',0),
'paths_zero':(t,'trajectory_endpoint_independent_comparisons',0),'error_large':(t,'max_numerical_absolute_error',1e-2),
'error_nan':(t,'max_numerical_absolute_error',float('nan')),'error_negative':(t,'max_numerical_absolute_error',-1.),
'human_data':(t,'real_human_or_animal_time_series_used',1),'bool_count':(t,'real_human_or_animal_time_series_used',False),
'bad_share':(e,'project_Hawk_original_share','0'),'bad_derivative':(e,'project_Hawk_exact_continuous_initial_derivative','0'),
'bad_euler':(e,'Euler_h4_one_step_share','1'),'bad_continuous':(e,'true_continuous_t4_share',.2),
'bad_multiplier':(e,'Euler_local_multiplier_h4_at_one_third','0'),'false_payoffs':(b,'same_continuous_payoff_differences',False),
'string_bool':(b,'same_continuous_payoff_differences','False'),'bad_unshifted':(b,'original_p149_eq3_unshifted_at_half','0'),
'bad_shifted':(b,'original_p149_eq3_add_three_to_all_payoffs_at_half','0')}
if case in changes:d,k,x=changes[case];d[k]=x
# Retain the legacy reproduction seam for RED; repaired runner uses the private collector.
a.m.exhaustive_exact_field_and_discrete_audit=lambda:v
a.m.exhaustive_216_analytic_vs_RK4=lambda:t
a.m.project_euler_false_extinction_counterexample=lambda:e
a.m.source_discrete_baseline_counterexample=lambda:b
if hasattr(a,'_run_unit_tests'):
 def fake(root,run_id,hashes):
  r={'run_id':run_id,'tests_run':70,'failures':0,'errors':0,'skipped':0,'expected_failures':0,'unexpected_successes':0,'returncode':0,'successful':True,'sources_unchanged':True,'source_sha256':hashes,'optimization_level':sys.flags.optimize}
  if case=='missing_test_receipt':return None
  if case=='failed_test_receipt':r.update(failures=1,successful=False)
  if case=='mismatched_test_source':r['source_sha256']={}
  if case=='mismatched_run':r['run_id']='other-run'
  if case=='too_few_tests':r['tests_run']=69
  if case=='expected_failure':r['expected_failures']=1
  return r
 a._run_unit_tests=fake
 if case=='loaded_source_mismatch':a._LOADED_CORE_SHA256='0'*64
 a.attest(out)
else:
 # Execute the original program's actual main under injected dependencies, redirected to a temporary copy.
 for name in ['r132_taylor_jonker_1978_replicator_trajectories.py','test_r132_taylor_jonker_1978_replicator_trajectories.py','R132_TAYLOR_JONKER_1978_FULL_REPLICATOR_TRAJECTORIES_EULER_ARTIFACT_SCIENTIFIC_REPORT_2026-10-20.md']:
  (out.parent/name).write_bytes((p.parent/name).read_bytes())
 a.__file__=str(out.parent/p.name);a.main()
'''

class AttestationIntegrity(unittest.TestCase):
    def test_faults_fail_in_all_optimization_modes_without_success_receipt(self):
        cases=['exact_zero','states_zero','paths_zero','error_large','error_nan','error_negative','human_data','bool_count','bad_share','bad_derivative','bad_euler','bad_continuous','bad_multiplier','false_payoffs','string_bool','bad_unshifted','bad_shifted','missing_test_receipt','failed_test_receipt','mismatched_test_source','mismatched_run','too_few_tests','expected_failure','loaded_source_mismatch']
        for mode in ['normal','-O','env']:
            for case in cases:
                with self.subTest(mode=mode,case=case),tempfile.TemporaryDirectory() as tmp:
                    root=Path(tmp);out=root/'receipt.json'
                    # A previous managed success may not survive a failed new invocation.
                    out.write_text(json.dumps({'attestation_format_version':2,'research_id':'R132','phase':'B','receipt_kind':'ENGINEERING_REVALIDATION','status':'SUCCESS'}))
                    env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
                    if mode=='env':env['PYTHONOPTIMIZE']='1'
                    cmd=[sys.executable]+(['-O'] if mode=='-O' else [])+['-c',DRIVER,str(CHECKER),str(out),case]
                    run=subprocess.run(cmd,capture_output=True,text=True,env=env,timeout=20)
                    self.assertNotEqual(run.returncode,0,(mode,case,run.stdout,run.stderr))
                    self.assertFalse(out.exists(),(mode,case,'stale managed SUCCESS retained'))
                    legacy=root/'R132_PHASE_B_70_TEST_216_TRAJECTORIES_CI_ACCEPTANCE.json'
                    self.assertFalse(legacy.exists(),(mode,case,'legacy SUCCESS minted'))

    def test_missing_math_source_removes_stale_managed_receipt(self):
        from unittest.mock import patch
        import r132_phase_b_ci_attest as a
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'receipt.json'
            out.write_text(json.dumps({'attestation_format_version':2,'research_id':'R132','phase':'B','receipt_kind':'ENGINEERING_REVALIDATION','status':'SUCCESS'}))
            with patch.object(a,'ROOT',Path(tmp)),patch.object(a,'_LOADED_CORE_SHA256',None):
                with self.assertRaises(FileNotFoundError):a.attest(out)
            self.assertFalse(out.exists())

    def test_same_size_timestamp_pyc_cannot_replace_native_tests(self):
        import importlib.util
        import py_compile
        import r132_phase_b_ci_attest as a
        for mode in ['normal','-O','env']:
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp)
                for name in [*a.SOURCE_NAMES,a.HISTORICAL.name]:
                    (root/name).write_bytes((a.ROOT/name).read_bytes())
                test_path=root/'test_r132_taylor_jonker_1978_replicator_trajectories.py'
                genuine=test_path.read_bytes();stamp=test_path.stat().st_mtime_ns
                fake=b"import unittest\nclass CachedNoopTests(unittest.TestCase): pass\nfor i in range(70): setattr(CachedNoopTests, 'test_cached_%03d'%i, lambda self:None)\n"
                fake+=b'#'+b' '*(len(genuine)-len(fake)-1)
                test_path.write_bytes(fake);os.utime(test_path,ns=(stamp,stamp))
                optimize=0 if mode=='normal' else 1
                cache=importlib.util.cache_from_source(str(test_path),optimization='' if optimize==0 else '1')
                py_compile.compile(str(test_path),cfile=cache,doraise=True,optimize=optimize)
                test_path.write_bytes(genuine);os.utime(test_path,ns=(stamp,stamp))
                out=root/'result.json';env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
                if mode=='env':env['PYTHONOPTIMIZE']='1'
                cmd=[sys.executable]+(['-O'] if mode=='-O' else [])+[str(root/CHECKER.name),'--output',str(out)]
                run=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=120)
                self.assertEqual(run.returncode,0,run.stderr)
                receipt=json.loads(out.read_text())
                self.assertIn('Primary1978ReplicatorEquations',receipt['actual_native_test_run']['stderr'])
                self.assertNotIn('CachedNoopTests',receipt['actual_native_test_run']['stderr'])
                self.assertEqual(test_path.read_bytes(),genuine)

    def test_historical_receipt_is_immutable(self):
        import r132_phase_b_ci_attest as a
        before=a.HISTORICAL.read_bytes()
        with self.assertRaises(a.AttestationError):a.attest(a.HISTORICAL)
        self.assertEqual(before,a.HISTORICAL.read_bytes())

    def test_atomic_publication_failure_leaves_no_success_or_temp(self):
        from unittest.mock import patch
        import r132_phase_b_ci_attest as a
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'receipt.json'
            with patch.object(a.os,'replace',side_effect=OSError('injected atomic publication failure')):
                with self.assertRaises(OSError):a.attest(out)
            self.assertFalse(out.exists())
            self.assertEqual(list(Path(tmp).iterdir()),[])

if __name__=='__main__':unittest.main()
