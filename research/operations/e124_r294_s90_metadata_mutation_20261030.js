#!/usr/bin/env node
"use strict";
// Offline Node reproduction on the main checkout. Original B module remains unchanged.
const fs=require("fs"),path=require("path"),assert=require("assert");
const base=path.resolve(__dirname,"..");
const {audit}=require(path.join(base,"evidence_audit/b_r294_s90_independent_direct_formula_20261030.js"));
const original=fs.readFileSync(path.join(base,"R294/R294_ALL_144_EXACT_INTERTEMPORAL_DECISION_SOURCES.csv"),"utf8");
const csv=fs.readFileSync(path.join(base,"validation/R294_S90_ALL_288_COMMITMENT_CELLS.csv"),"utf8");
const raw=fs.readFileSync(path.join(base,"validation/R294_S90_EXACT_RESULTS.json"),"utf8");
const baseline=audit(original,csv,raw);assert.strictEqual(baseline.status,"PASS");
const mutations={
 research_id:j=>j.research_id="R999",stage:j=>j.stage="S00",status:j=>j.status="ACCEPTED_EXTERNALLY",
 freeze_commit:j=>j.freeze_commit="0".repeat(40),original_source_blob:j=>j.original_source_blob="0".repeat(40),
 fees:j=>j.fees=["0","1/2"],original_reversals:j=>j.original_reversals.HYPERBOLIC=999,
 R073:j=>j.R073="UNFROZEN",PESEN_v0_1:j=>j.PESEN_v0_1="UNFROZEN"
};
let accepted=0;
for(const [name,fn] of Object.entries(mutations)){
 let j=JSON.parse(raw);fn(j);assert.strictEqual(audit(original,csv,JSON.stringify(j)).status,"PASS");accepted++;
 j=JSON.parse(raw);delete j[name];assert.strictEqual(audit(original,csv,JSON.stringify(j)).status,"PASS");accepted++;
}
let rejected=0;
for(const fn of [j=>j.evidence="E2_HUMAN",j=>j.new_E2=1,j=>j.summary[0].purchases=999]){
 const j=JSON.parse(raw);fn(j);assert.throws(()=>audit(original,csv,JSON.stringify(j)));rejected++;
}
console.log(JSON.stringify({status:"PASS",baseline,metadata_false_accepts:accepted,controls_rejected:rejected,fields:Object.keys(mutations)},null,2));
