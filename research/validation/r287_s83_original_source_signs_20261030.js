#!/usr/bin/env node
"use strict";
// R287 S83. Read the unchanged original R287 2304-row CSV and emit derived E1 receipts.
// Usage: node r287_s83_original_source_signs_20261030.js ORIGINAL.csv OUTPUT_DIRECTORY
const fs=require("fs"),path=require("path");
const compute=(raw)=>{
 const profiles={LINEAR:[8,-10],SQRT_ON_SQUARES:[4,-2],SATURATING:[3,-1]};
 const gcd=(a,b)=>b?gcd(b,a%b):a;
 const frac=(a,b)=>{let d=gcd(Math.abs(a),b);return b/d===1?String(a/d):`${a/d}/${b/d}`};
 const parse=(s)=>{const a=s.split("/").map(Number);return [a[0],a[1]||1]};
 const lambdaNum=(s)=>s==="1/2"?2:Number(s[0]);
 const lines=raw.trim().split(/\r?\n/);
 const header="world,utility_profile,lambda_common,full_ordered_M1X1_M2X2_M3X3_M4X4,source_probability,actual_payoffs_A,actual_payoffs_B,realized_mean_utility_A,realized_mean_utility_B,realized_mean_difference_A_minus_B";
 if(lines[0]!==header||lines.length!==2305)throw Error("original header/length");
 const derived=["profile,lambda_common,original_source,original_probability,realized_mean_difference_A_minus_B,sign_category"];
 const seen=new Set(),groups=new Map();
 for(let i=1;i<lines.length;i++){
  const c=lines[i].split(",");if(c.length!==10)throw Error("columns");
  const [world,p,l,s,prob]=c, originalD=c[9];
  if(world!==p+"_"+l||!(p in profiles)||!["1/4","1/2","3/4"].includes(l)||!/^[01]{8}$/.test(s))throw Error("identity");
  const key=world+"|"+s;if(seen.has(key))throw Error("duplicate");seen.add(key);
  const m=[0,2,4,6].filter(j=>s[j]==="1").length;
  const ln=lambdaNum(l),n=ln**m*(4-ln)**(4-m);
  const [pn,pd]=parse(prob);if(pn*4096!==pd*n)throw Error("source mass");
  let diff2=0;
  for(let j=0;j<8;j+=2)if(s[j]==="0")diff2+=s[j+1]==="0"?profiles[p][0]:profiles[p][1];
  const [dn,dd]=parse(originalD);if(dn*8!==dd*diff2)throw Error("original source difference");
  const truth=profiles[p][0]+profiles[p][1]>0?1:-1;
  const category=diff2===0?"TIE":diff2*truth>0?"CORRECT":"WRONG";
  const k=p+"|"+l;
  if(!groups.has(k))groups.set(k,{profile:p,lambda_common:l,mass:{CORRECT:0,WRONG:0,TIE:0},source_count:0});
  const g=groups.get(k);g.mass[category]+=n;g.source_count++;
  derived.push([p,l,s,frac(n,4096),frac(diff2,8),category].join(","));
 }
 if(seen.size!==2304||groups.size!==9)throw Error("coverage");
 const results=[];
 for(const g of groups.values()){
  const {CORRECT,WRONG,TIE}=g.mass;
  if(g.source_count!==256||CORRECT+WRONG+TIE!==4096||CORRECT+WRONG===0)throw Error("mass partition");
  const ln=lambdaNum(g.lambda_common);
  results.push({profile:g.profile,lambda_common:g.lambda_common,original_sources:256,probability_correct:frac(CORRECT,4096),probability_wrong:frac(WRONG,4096),probability_tie:frac(TIE,4096),wrong_given_non_tie:frac(WRONG,CORRECT+WRONG),probability_all_common:frac(ln**4,256),affine_3u_plus_7_sign_invariant:true});
 }
 const check=(text)=>{
  const rows=text.trim().split(/\r?\n/);if(rows.length!==2305||rows[0]!==derived[0])throw Error("derived length/header");
  const ids=new Set(),mass={};
  for(const line of rows.slice(1)){
   const c=line.split(",");if(c.length!==6)throw Error("derived columns");
   const [p,l,s,prob,d,cat]=c;if(!(p in profiles)||!["1/4","1/2","3/4"].includes(l)||!/^[01]{8}$/.test(s))throw Error("derived identity");
   const id=p+"|"+l+"|"+s;if(ids.has(id))throw Error("derived duplicate");ids.add(id);
   const m=[0,2,4,6].filter(j=>s[j]==="1").length,ln=lambdaNum(l),n=ln**m*(4-ln)**(4-m);
   let diff2=0;for(let j=0;j<8;j+=2)if(s[j]==="0")diff2+=s[j+1]==="0"?profiles[p][0]:profiles[p][1];
   const truth=profiles[p][0]+profiles[p][1]>0?1:-1;
   const exp=diff2===0?"TIE":diff2*truth>0?"CORRECT":"WRONG";
   if(prob!==frac(n,4096)||d!==frac(diff2,8)||cat!==exp)throw Error("derived wrong value");
   const k=p+"|"+l;mass[k]=(mass[k]||0)+n;
  }
  if(ids.size!==2304||Object.keys(mass).length!==9||Object.values(mass).some(v=>v!==4096))throw Error("derived coverage");
  return true;
 };
 const csv=derived.join("\n")+"\n";check(csv);
 const mutants=[
  ["duplicate",()=>{let a=[...derived];a[2]=a[1];return a.join("\n")+"\n"}],
  ["missing",()=>derived.slice(0,-1).join("\n")+"\n"],
  ["mass",()=>{let a=[...derived];let c=a[1].split(",");c[3]="1/999";a[1]=c.join(",");return a.join("\n")+"\n"}],
  ["category",()=>{let a=[...derived];let c=a[1].split(",");c[5]=c[5]==="WRONG"?"CORRECT":"WRONG";a[1]=c.join(",");return a.join("\n")+"\n"}]
 ];
 const negative_controls=mutants.map(([name,mut])=>{let rejected=false;try{check(mut())}catch(e){rejected=true}return {name,rejected}});
 if(negative_controls.some(x=>!x.rejected))throw Error("negative control false pass");
 return {csv,results,negative_controls,original_rows:2304};
};
if(require.main===module){
 if(process.argv.length!==4)throw Error("Usage: node script.js ORIGINAL.csv OUTPUT_DIRECTORY");
 const output=compute(fs.readFileSync(process.argv[2],"utf8"));
 fs.mkdirSync(process.argv[3],{recursive:true});
 fs.writeFileSync(path.join(process.argv[3],"R287_S83_ALL_2304_SIGN_RECEIPTS.csv"),output.csv);
 fs.writeFileSync(path.join(process.argv[3],"R287_S83_EXACT_RESULTS.json"),JSON.stringify({research_id:"R287",substudy:"S83",evidence:"E1_ARTIFICIAL_INTERNAL_NONBLIND",original_csv_blob:"ddf3ae0b924016a3a8aac7253a1a6a9b44d864d1",prescore_freeze_commit:"254b5f73c86a18d55a11c68118bd1d0fc77ce80c",results:output.results,negative_controls:output.negative_controls,R073:"FROZEN",PESEN_v0_1:"FROZEN",new_E2:0,new_E3:0},null,2)+"\n");
 console.log(JSON.stringify({original_rows:output.original_rows,worlds:output.results.length,negative_controls:output.negative_controls}));
}
module.exports={compute};
