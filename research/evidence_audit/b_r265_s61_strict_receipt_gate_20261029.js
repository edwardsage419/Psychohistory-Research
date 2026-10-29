"use strict";
// Strict persisted receipt gate. Uses separately archived B covariance oracle.
// CLI: node b_r265_s61_strict_receipt_gate_20261029.js RECEIPT.json B_ORACLE.js
function verify(receipt,oracle){
if(!receipt||!Array.isArray(receipt.rows)||receipt.rows.length!==18)throw Error("coverage:18");
if(receipt.protocol!=="R265_S61_DEPENDENT_INPUT_CONDITIONAL_VARIANCE"||
 receipt.route!=="R_CONDITIONAL_PROJECTION"||
 receipt.evidence!=="E1_SYNTHETIC_NONBLIND"||
 receipt.new_real_human_E2!==0||receipt.new_real_historical_E3!==0||
 receipt.R073!=="FROZEN"||receipt.PESEN_v0_1!=="FROZEN"||
 receipt.prescore_freeze_commit!=="13f61626eba9d33fe0174d43b482b7f8fe4ec5e0")throw Error("metadata");
const ref=new Map(oracle.rows.map(r=>[r.world+"|"+r.design,r]));
if(ref.size!==18)throw Error("oracle coverage");
const seen=new Set();let comparisons=0;
for(const row of receipt.rows){
if(!row||typeof row.world!=="string"||typeof row.design!=="string")throw Error("key type");
const key=row.world+"|"+row.design;
if(seen.has(key)||!ref.has(key))throw Error("duplicate or unexpected key "+key);
seen.add(key);const base=ref.get(key);
for(const field of ["world","design","mean","variance","residual"]){
if(typeof row[field]!=="string"||row[field]!==base[field])throw Error("field "+key+" "+field);comparisons++;
}
for(const field of ["first","remaining"]){
if(!Array.isArray(row[field])||row[field].length!==4)throw Error("array "+field);
for(let k=0;k<4;k++){
if(typeof row[field][k]!=="string"||row[field][k]!==base[field][k])throw Error("numeric "+key+" "+field+" "+k);comparisons++;
}}
}
if(seen.size!==18)throw Error("incomplete coverage");
return {status:"PASS",rows:18,field_comparisons:comparisons};
}
if(typeof module!=="undefined"&&require.main===module){
const fs=require("fs"),path=require("path");
if(process.argv.length!==4)throw Error("usage receipt.json B_oracle.js");
const receipt=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
const oracle=require(path.resolve(process.argv[3]));
console.log(JSON.stringify(verify(receipt,oracle.compute())));
}
if(typeof module!=="undefined")module.exports={verify};
