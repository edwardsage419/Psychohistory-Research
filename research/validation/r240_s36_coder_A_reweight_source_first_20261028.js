#!/usr/bin/env node
"use strict";
// R240 S36 source-first exact observed-only reweighting. No oracle fields are read.
const fs=require("fs"),crypto=require("crypto"),path=require("path");
const FROZEN_BLOB="ef6b1382c80d9fe2e3a13054e31a7195786c4c7a";
const FREEZE_COMMIT="6c3ec37fd867cf223ccb2709ea49d99ca6a8159d";
function runR(csv){
 const worlds=["PERFECT_TRUTHFUL","PERFECT_SYSTEMATICALLY_WRONG","SHARED_SYSTEMATIC_ERROR","INDEPENDENT_QUARTER_ERRORS","BALANCED_INDEPENDENT_RANDOM","RARE_POSITIVE_INDEPENDENT_RANDOM","ASYMMETRIC_FALSE_POSITIVE","SELECTIVE_MISSING_DISAGREEMENTS","OPPOSING_CODERS"];
 const lines=csv.trimEnd().split(/\r?\n/),header=lines.shift().split(","),at=Object.fromEntries(header.map((h,i)=>[h,i]));
 const fields=["world","observed_pair_available","observed_coder_A","observed_coder_B","original_structural_source_probability"];
 for(const f of fields)if(at[f]===undefined)throw Error("missing "+f);
 const data=Object.fromEntries(worlds.map(w=>[w,[]]));
 for(const line of lines){const v=line.split(","),w=v[at.world];if(!data[w])throw Error("unknown world");if(v[at.original_structural_source_probability]!=="1/256")throw Error("source probability");data[w].push(v)}
 if(lines.length!==2304||worlds.some(w=>data[w].length!==256))throw Error("source universe mismatch");
 function gcd(a,b){while(b){let t=a%b;a=b;b=t}return a}
 function frac(n,d){if(d===0)throw Error("zero denominator");if(d<0){n=-n;d=-d}const g=gcd(Math.abs(n),d);return d/g===1?String(n/g):`${n/g}/${d/g}`}
 const results=[];
 for(const world of worlds){const rows=data[world],n=rows.filter(v=>v[at.observed_pair_available]==="1").length;
  for(const weight of [1,2,4,8]){
   const c=[0,0,0,0];for(const v of rows){const s=Number(v[at.observed_pair_available]),a=Number(v[at.observed_coder_A]),b=Number(v[at.observed_coder_B]);if(s===0){if(a!==-1||b!==-1)throw Error("missing row reveals code");continue}if(![0,1].includes(a)||![0,1].includes(b))throw Error("invalid observed code");c[a*2+b]+=a?weight:1}
   const W=c.reduce((a,b)=>a+b,0),pNum=c[0]+c[3],a0=c[0]+c[1],a1=c[2]+c[3],b0=c[0]+c[2],b1=c[1]+c[3],peNum=a0*b0+a1*b1;
   const kNum=pNum*W-peNum,kDen=W*W-peNum;
   results.push({world,weight_A1:weight,unweighted_complete_pair_source_types:n,weighted_table_00_01_10_11:c,weighted_mass:W,observed_agreement:frac(pNum,W),independent_marginal_chance_agreement:frac(peNum,W*W),cohens_kappa:kDen?frac(kNum,kDen):"UNDEFINED"});
  }
 }
 const by=(w,k)=>results.find(x=>x.world===w&&x.weight_A1===k);
 for(const k of [1,2,4,8]){
  const tri=["PERFECT_TRUTHFUL","PERFECT_SYSTEMATICALLY_WRONG","SHARED_SYSTEMATIC_ERROR"].map(w=>JSON.stringify({...by(w,k),world:null}));if(new Set(tri).size!==1)throw Error("alias mismatch");
  for(const w of ["BALANCED_INDEPENDENT_RANDOM","RARE_POSITIVE_INDEPENDENT_RANDOM"])if(by(w,k).cohens_kappa!=="0")throw Error("independent kappa nonzero");
  if(by("OPPOSING_CODERS",k).observed_agreement!=="0")throw Error("opposing Po");
  if(by("SELECTIVE_MISSING_DISAGREEMENTS",k).unweighted_complete_pair_source_types!==192)throw Error("missingness changed");
 }
 return {study:"R240_S36",evidence:"E1_FINITE_ARTIFICIAL",original_R240_source_blob:"ef6b1382c80d9fe2e3a13054e31a7195786c4c7a",freeze_commit:FREEZE_COMMIT,worlds:9,original_source_rows:2304,conditions:results.length,weight_A0:1,weight_A1_values:[1,2,4,8],hidden_oracle_used:false,results,new_E2:0,new_E3:0};
}
function main(){
 const file=process.argv[2]||path.join(__dirname,"../R240/R240_ALL_2304_ORIGINAL_TWO_CODER_ANNOTATION_ATOMS.csv");
 const bytes=fs.readFileSync(file);
 const blob=crypto.createHash("sha1").update(Buffer.from("blob "+bytes.length+"\0")).update(bytes).digest("hex");
 if(blob!==FROZEN_BLOB)throw Error("frozen source Git blob mismatch: "+blob);
 const result=runR(bytes.toString("utf8"));
 process.stdout.write(JSON.stringify(result,null,2)+"\n");
}
if(require.main===module)main();
module.exports={runR};
