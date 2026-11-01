#!/usr/bin/env node
'use strict';
// Synthetic test fixtures, independent of original research implementations.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {verify, blob, PINS} = require('./r333_r340_claim_receipt_gate_20261101.js');
function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'claim-gate-'));
  const pins = {};
  for (const [model, values] of Object.entries(PINS)) {
    const [, , run, source, protocol] = values;
    const dir = path.join(root, 'research', model);
    fs.mkdirSync(dir, {recursive:true});
    const machine = {research_id:model, catalogue_id:'X', protocol_commit:protocol, source_commit:source,
      verification:{CI_run_id:run, conclusion:'success'}, scientific_grade:'PASS_BOUNDED_E1_SYNTHETIC_ONLY',
      human_E2:'NOT_ESTABLISHED', historical_E3:'NOT_ESTABLISHED'};
    const final = {research_id:model, original_catalogue_id:'X', protocol_commit:protocol, source_commit:source,
      CI_run_id:run, CI_conclusion:'success', three_jobs_success:true, status:'PASS_BOUNDED_E1_SYNTHETIC_ONLY',
      real_human_E2:'NOT_ESTABLISHED', historical_E3:'NOT_ESTABLISHED', original_empirical_replication:'NOT_ESTABLISHED',
      machine_receipt:'research/'+model+'/'+model+'_MACHINE_RECEIPT.json'};
    const mb=Buffer.from(JSON.stringify(machine)), fb=Buffer.from(JSON.stringify(final));
    fs.writeFileSync(path.join(dir, model+'_MACHINE_RECEIPT.json'), mb);
    fs.writeFileSync(path.join(dir, model+'_FINAL_ACCEPTANCE_STATUS.json'), fb);
    pins[model]=[blob(mb),blob(fb),run,source,protocol];
  }
  return {root,pins};
}
let checks=0;
function trial(name, mutation, expected) {
  const f=fixture();
  try {
    if(mutation) mutation(f);
    let failed=false;
    try {verify(f.root,f.pins);} catch(e) {failed=true;}
    assert.equal(failed, expected, name);
    checks++;
  } finally {fs.rmSync(f.root,{recursive:true,force:true});}
}
function change(f, model, suffix, fn, rePin=false) {
  const file=path.join(f.root,'research',model,model+'_'+suffix+'.json');
  const obj=JSON.parse(fs.readFileSync(file)); fn(obj);
  const bytes=Buffer.from(JSON.stringify(obj)); fs.writeFileSync(file,bytes);
  if(rePin) f.pins[model][suffix==='MACHINE_RECEIPT'?0:1]=blob(bytes);
}
trial('valid all 16',null,false);
trial('machine CI tamper',f=>change(f,'R333','MACHINE_RECEIPT',x=>x.verification.conclusion='failure'),true);
trial('final E2 elevation',f=>change(f,'R334','FINAL_ACCEPTANCE_STATUS',x=>x.real_human_E2='PASS'),true);
trial('machine deletion',f=>fs.unlinkSync(path.join(f.root,'research/R335/R335_MACHINE_RECEIPT.json')),true);
trial('final deletion',f=>fs.unlinkSync(path.join(f.root,'research/R336/R336_FINAL_ACCEPTANCE_STATUS.json')),true);
trial('final changed with re-pin but false CI',f=>change(f,'R337','FINAL_ACCEPTANCE_STATUS',x=>x.CI_conclusion='failure',true),true);
trial('wrong source with re-pin',f=>change(f,'R338','MACHINE_RECEIPT',x=>x.source_commit='wrong',true),true);
trial('wrong protocol with re-pin',f=>change(f,'R339','FINAL_ACCEPTANCE_STATUS',x=>x.protocol_commit='wrong',true),true);
trial('evidence grade upgrade with re-pin',f=>change(f,'R340','FINAL_ACCEPTANCE_STATUS',x=>x.status='PASS_E2',true),true);
trial('missing model universe',f=>delete f.pins.R340,true);
trial('extra model universe',f=>f.pins.R341=f.pins.R340,true);
trial('symlink receipt',f=>{const p=path.join(f.root,'research/R333/R333_MACHINE_RECEIPT.json');fs.renameSync(p,p+'.old');fs.symlinkSync(p+'.old',p)},true);
trial('wrong receipt path with re-pin',f=>change(f,'R333','FINAL_ACCEPTANCE_STATUS',x=>x.machine_receipt='research/R334/R334_MACHINE_RECEIPT.json',true),true);
console.log(JSON.stringify({status:'PASS',synthetic_trials:checks,positive:1,negative:checks-1,real_archive_native:'NOT_RUN'}));
