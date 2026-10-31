#!/usr/bin/env node
'use strict';
const fs=require('node:fs');
const path=require('node:path');
const os=require('node:os');
const crypto=require('node:crypto');
const cp=require('node:child_process');
const assert=require('node:assert/strict');
const root=path.resolve(process.argv[2] || '.');
const rel={
  source:'research/validation/r324_s120_ordinal_observation.js',
  original:'research/R324/R324_ALL_64_ARTIFICIAL_RISK_STATES.csv',
  csv:'research/validation/R324_S120_64_ATOM_ORDINAL_OBSERVATIONS.csv',
  json:'research/validation/R324_S120_EXACT_OBSERVATION_RESULTS.json',
};
const expected={source:'3e2c099cb638277d55b2bb0aa20af044aa4628e2',original:'1b0062eeea020606a3d510d566da43db03ace8d9',csv:'eeef39b66165e2ec0a918ccedb4f038b078cd05b',json:'a95be44193a4a7890203049d5615b4f27c93453e'};
function gitBlob(data){return crypto.createHash('sha1').update('blob '+data.length+'\0').update(data).digest('hex');}
const paths=Object.fromEntries(Object.entries(rel).map(([k,p])=>[k,path.join(root,p)]));
for(const k of Object.keys(rel)) assert.equal(gitBlob(fs.readFileSync(paths[k])),expected[k],k+' source identity');
const run=(...args)=>cp.spawnSync(process.execPath,[paths.source,...args],{encoding:'utf8'});
const check=run('--check',path.dirname(paths.csv));
assert.equal(check.status,0,check.stderr);
const selftest=run('--selftest');
assert.notEqual(selftest.status,0,'expected original selftest failure');
assert.match(selftest.stderr,/mutation accepted/);
const source=fs.readFileSync(paths.source,'utf8');
const originalCsv=fs.readFileSync(paths.csv,'utf8');
const needle=',0,0,0,0\n';
assert(source.includes('.replace('),'source contains negative-control replacement');
assert.equal(originalCsv.includes(needle),false,'first synthetic mutation does not match any CSV row');
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'r324-s120-e154-'));
try{
  const emit=run('--emit',tmp); assert.equal(emit.status,0,emit.stderr);
  for(const k of ['csv','json']) assert.deepEqual(fs.readFileSync(path.join(tmp,path.basename(paths[k]))),fs.readFileSync(paths[k]),k+' emitted bytes');
  const mutated=fs.readFileSync(paths.csv,'utf8').replace('0,0000,0,0,0,0,-1,-1','0,0000,0,0,1,0,-1,-1');
  assert.notEqual(mutated,fs.readFileSync(paths.csv,'utf8'));
  fs.writeFileSync(path.join(tmp,path.basename(paths.csv)),mutated);
  const bad=run('--check',tmp);assert.notEqual(bad.status,0,'real CSV mutation should fail');
} finally {fs.rmSync(tmp,{recursive:true,force:true});}
console.log(JSON.stringify({status:'E154_NATIVE_CLI_AUDIT_PASS_WITH_ORIGINAL_SELFTEST_FAILURE',node:process.version,source_git_blob:expected.source,original_git_blob:expected.original,archived_csv_git_blob:expected.csv,archived_json_git_blob:expected.json,original_check:'PASS',original_emit:'BYTE_IDENTICAL',original_selftest:'FAIL_EXIT_NONZERO',reason:'first CSV replace needle absent; only JSON negative control is live',independent_csv_mutation:'REJECTED',science:'PARTIAL_E1_EXTENSION',E2:0,E3:0},null,2));
