#!/usr/bin/env python3
"""R132 Phase-B integrity v2: explicit gates + same-invocation native tests.

Historical CI receipts are immutable. This entry point emits a new, versioned
LOCAL engineering revalidation, never claims a new CI run or empirical evidence.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import uuid
import types

ROOT=Path(__file__).resolve().parent
# Bind the actual parent-side math code to the exact bytes that were compiled,
# rather than fingerprinting a path after Python may already have imported it.
_CORE_NAME='r132_taylor_jonker_1978_replicator_trajectories.py'
_LOADED_CORE_SHA256=None
m=types.ModuleType('_r132_phase_b_authenticated_math')

def _load_math():
    global _LOADED_CORE_SHA256
    if _LOADED_CORE_SHA256 is None:
        raw=(ROOT/_CORE_NAME).read_bytes()
        m.__file__=str(ROOT/_CORE_NAME)
        exec(compile(raw,m.__file__,'exec'),m.__dict__)
        _LOADED_CORE_SHA256=hashlib.sha256(raw).hexdigest()

HISTORICAL=ROOT/'R132_PHASE_B_70_TEST_216_TRAJECTORIES_CI_ACCEPTANCE.json'
DEFAULT_OUTPUT=ROOT/'R132_PHASE_B_ATTESTATION_V2_LOCAL_ENGINEERING_RECEIPT.json'
SOURCE_NAMES=(
    'r132_taylor_jonker_1978_replicator_trajectories.py',
    'test_r132_taylor_jonker_1978_replicator_trajectories.py',
    'R132_TAYLOR_JONKER_1978_FULL_REPLICATOR_TRAJECTORIES_EULER_ARTIFACT_SCIENTIFIC_REPORT_2026-10-20.md',
    'r132_phase_b_ci_attest.py',
)

class AttestationError(ValueError):
    """Acceptance failed. No new successful receipt is permitted."""


def require(condition,message):
    if condition is not True:raise AttestationError(message)


def _source_hashes(root):
    return {name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in SOURCE_NAMES}


def validate_science(vector,paths,euler,birth):
    """The original 13 conditions, with explicit types and finite error semantics."""
    def integer(data,key):
        value=data[key];require(type(value) is int,f'{key}: integer required');return value
    require(integer(vector,'exact_independent_fraction_fields')==75,'exact Fraction field count != 75')
    require(integer(vector,'source_eq3_eq4_valid_state_checks')>40,'source Eq3/Eq4 checks must exceed 40')
    require(integer(paths,'trajectory_endpoint_independent_comparisons')==216,'independent trajectory count != 216')
    error=paths['max_numerical_absolute_error']
    require(type(error) in (int,float) and math.isfinite(error) and 0<=error<1e-6,'numerical absolute error must be finite, nonnegative and <1e-6')
    require(integer(paths,'real_human_or_animal_time_series_used')==0,'human/animal time series forbidden')
    require(euler['project_Hawk_original_share']=='1/2','Hawk original share != 1/2')
    require(euler['project_Hawk_exact_continuous_initial_derivative']=='-1/8','initial derivative != -1/8')
    require(euler['Euler_h4_one_step_share']=='0','Euler h4 share != 0')
    try:continuous=F(str(euler['true_continuous_t4_share']))
    except (ValueError,TypeError,ZeroDivisionError) as exc:raise AttestationError('invalid continuous t4 share') from exc
    require(continuous>F(1,3),'true continuous t4 share must exceed 1/3')
    require(euler['Euler_local_multiplier_h4_at_one_third']=='-5/3','Euler multiplier != -5/3')
    require(birth['same_continuous_payoff_differences'] is True,'payoff-difference equality must be boolean True')
    require(birth['original_p149_eq3_unshifted_at_half']=='2/5','original Eq3 unshifted share != 2/5')
    require(birth['original_p149_eq3_add_three_to_all_payoffs_at_half']=='8/17','original Eq3 shifted share != 8/17')


TEST_HARNESS=r'''
import hashlib,json,pathlib,sys,types,unittest
root=pathlib.Path(sys.argv[1]);run_id=sys.argv[2];names=json.loads(sys.argv[3])
sys.path.insert(0,str(root))
def hashes():return {n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names}
snapshots={n:(root/n).read_bytes() for n in names}
before={n:hashlib.sha256(raw).hexdigest() for n,raw in snapshots.items()}
# Do not trust timestamp/size .pyc caches for source-qualified math or tests.
for filename in ['r132_taylor_jonker_1978_replicator_trajectories.py','test_r132_taylor_jonker_1978_replicator_trajectories.py']:
    name=pathlib.Path(filename).stem
    module=types.ModuleType(name);module.__file__=str(root/filename)
    sys.modules[name]=module
    exec(compile(snapshots[filename],module.__file__,'exec'),module.__dict__)
suite=unittest.defaultTestLoader.loadTestsFromModule(module)
result=unittest.TextTestRunner(stream=sys.stderr,verbosity=2).run(suite)
after=hashes()
print(json.dumps({'run_id':run_id,'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'expected_failures':len(result.expectedFailures),'unexpected_successes':len(result.unexpectedSuccesses),'successful':result.wasSuccessful(),'source_sha256':after,'sources_unchanged':before==after,'optimization_level':sys.flags.optimize},sort_keys=True))
sys.exit(0 if result.wasSuccessful() and before==after else 1)
'''


def _run_unit_tests(root,run_id,hashes):
    env=os.environ.copy();env['PYTHONOPTIMIZE']=str(sys.flags.optimize)
    command=[sys.executable,'-c',TEST_HARNESS,str(root),run_id,json.dumps(list(hashes))]
    run=subprocess.run(command,cwd=root,env=env,capture_output=True,text=True,timeout=120)
    try:record=json.loads(run.stdout)
    except ValueError as exc:raise AttestationError('missing/malformed actual unittest result') from exc
    require(isinstance(record,dict),'test result must be an object')
    record.update(returncode=run.returncode,stderr=run.stderr,command_kind='same-invocation native unittest subprocess')
    return record


def _validate_test_result(record,run_id,hashes):
    require(isinstance(record,dict),'actual native test receipt required')
    require(record.get('run_id')==run_id,'test run identity mismatch')
    require(record.get('source_sha256')==hashes,'test source SHA mismatch')
    require(record.get('sources_unchanged',False) is True,'sources changed during native tests')
    for name,expected in [('tests_run',70),('failures',0),('errors',0),('skipped',0),('expected_failures',0),('unexpected_successes',0),('returncode',0),('optimization_level',sys.flags.optimize)]:
        require(type(record.get(name)) is int and record[name]==expected,f'actual test {name} != {expected}')
    require(record.get('successful') is True,'native tests failed')


def _prepare_output(output):
    output=Path(output).absolute()
    require(not any(p.is_symlink() for p in [output,*output.parents]),'symlink output forbidden')
    # Any preexisting unowned/historical file is immutable to this checker.
    require(output!=HISTORICAL,'historical Phase B receipt is immutable')
    if output.exists():
        try:previous=json.loads(output.read_text(encoding='utf-8'))
        except (ValueError,UnicodeError) as exc:raise AttestationError('refusing to replace unowned output') from exc
        require(isinstance(previous,dict) and previous.get('attestation_format_version')==2 and previous.get('research_id')=='R132' and previous.get('phase')=='B' and previous.get('receipt_kind')=='ENGINEERING_REVALIDATION','refusing to replace unowned/historical receipt')
        output.unlink()  # A failed new attempt cannot leave a stale managed SUCCESS.
    return output


def attest(output=DEFAULT_OUTPUT):
    output=_prepare_output(output)
    _load_math()
    run_id=uuid.uuid4().hex;hashes=_source_hashes(ROOT)
    require(hashes[_CORE_NAME]==_LOADED_CORE_SHA256,'loaded mathematical source identity mismatch')
    test_run=_run_unit_tests(ROOT,run_id,hashes)
    _validate_test_result(test_run,run_id,hashes)
    vector=m.exhaustive_exact_field_and_discrete_audit()
    paths=m.exhaustive_216_analytic_vs_RK4()
    euler=m.project_euler_false_extinction_counterexample()
    birth=m.source_discrete_baseline_counterexample()
    validate_science(vector,paths,euler,birth)
    require(_source_hashes(ROOT)==hashes,'source identity changed during scientific revalidation')
    receipt={
        'attestation_format_version':2,'research_id':'R132','phase':'B','receipt_kind':'ENGINEERING_REVALIDATION',
        'status':'R132_PHASE_B_LOCAL_ENGINEERING_VALIDATION_SUCCESS_V2','run_id':run_id,
        'execution_backend':'LOCAL_CODEX_CLOUD_NOT_GITHUB_ACTIONS','optimization_level':sys.flags.optimize,
        'original_model':'Taylor Jonker 1978 Eq2 continuous Eq3 birth-generation',
        'historical_phase_b_receipt':HISTORICAL.name,'historical_receipt_sha256':hashlib.sha256(HISTORICAL.read_bytes()).hexdigest(),
        'original_13_scientific_conditions_preserved':True,'actual_native_test_run':test_run,
        'exact_source_vector_and_discrete_fraction_rechecks':vector,
        'full_216_ODE_RK4_vs_separate_implicit_integral_rechecks':paths,
        'project_Euler_false_extinction_not_original_discrete_rule':euler,
        'source_1978_discrete_generation_baseline_dependency':birth,
        'source_sha256':hashes,'new_real_human_E2_prediction_scores':0,'new_real_historical_E3_prediction_scores':0,
        'evidence_grade_unchanged':True,'R073':'FROZEN','PESEN_v0_1':'FROZEN',
    }
    raw=(json.dumps(receipt,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    output.parent.mkdir(parents=True,exist_ok=True)
    temp=None
    try:
        with tempfile.NamedTemporaryFile(prefix='.'+output.name+'.',suffix='.tmp',dir=output.parent,delete=False) as f:
            temp=Path(f.name);f.write(raw);f.flush();os.fsync(f.fileno())
        os.replace(temp,output)
    finally:
        if temp is not None:temp.unlink(missing_ok=True)
    print('R132_PHASE_B_V2_LOCAL_RECEIPT_SHA256',hashlib.sha256(raw).hexdigest())
    return receipt


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=DEFAULT_OUTPUT)
    args=parser.parse_args()
    attest(args.output)

if __name__=='__main__':main()
