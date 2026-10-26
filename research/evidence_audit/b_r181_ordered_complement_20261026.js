"use strict";
// node research/evidence_audit/b_r181_ordered_complement_20261026.js from repository root
const fs=require("node:fs");
function independent(worlds,r){
 const gcd=(a,b)=>b?gcd(b,a%b):a<0n?-a:a;
 const F=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);let g=gcd(a,b);return [a/g,b/g]};
 const sum=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]);
 const read=s=>{let [a,b="1"]=s.split("/");return F(a,b)},str=x=>x[1]===1n?String(x[0]):x[0]+"/"+x[1];
 let masks=[];for(let m=0;m<64;m++){let bits=0;for(let j=0;j<6;j++)bits+=(m>>j)&1;if(bits===3&&m<(m^63))masks.push(m);}
 if(masks.length!==10)throw Error("bad masks");
 const condition={};let badTie=0;
 for(const row of r.rows){let k=row.k.split("").map(Number),S=k.reduce((a,b)=>a+b,0),v=masks.map(m=>{let t=0;for(let i=0;i<6;i++)if(m&(1<<i))t+=k[i];return Math.abs(2*t-S)});
 let maximum=Math.max(...v),n=v.filter(x=>x===maximum).length,expected=n===1?2:0;
 if(row.min_p!==str(F(n,10))||row.reject10!==expected||row.reject05!==0)throw Error("profile mismatch");
 condition[row.k]=expected;badTie+=v.filter(x=>x>maximum).length===0?1:0;
 }
 const out=[];for(const w of worlds){let pmf=w.source_count_pmf.map(read),mass=F(0),rate=F(0),n=0;
 for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++)for(let d=0;d<5;d++)for(let e=0;e<5;e++)for(let f=0;f<5;f++){
 let v=[a,b,c,d,e,f],key=[...v].sort((x,y)=>x-y).join(""),p=F(1);for(let x of v)p=mul(p,pmf[x]);
 mass=sum(mass,p);if(condition[key]===2)rate=sum(rate,mul(p,F(1,10)));n++;
 }
 let x=r.worlds.find(x=>x.p===w.true_p&&x.source===w.source);if(str(mass)!=="1"||str(rate)!==x.alpha10)throw Error("ordered mismatch");
 out.push({p:w.true_p,source:w.source,ordered_profiles:n,alpha10:str(rate),pass:true});
 }
 return {method:"10 complementary masks + 5^6 ordered profiles per source",profiles_checked:r.rows.length,ordered_profiles_checked:out.reduce((s,x)=>s+x.ordered_profiles,0),negative_control_tie_omission_detected_profiles:badTie,worlds:out,external_replication:false};
}
const w=JSON.parse(fs.readFileSync("research/R181/R181_EXACT_RESULTS.json","utf8")).all_source_worlds;
const r=JSON.parse(fs.readFileSync("research/validation/R181_PVALUE_RESOLUTION_THIRD_METHOD_EXACT_RECEIPT_2026-10-26.json","utf8"));
process.stdout.write(JSON.stringify(independent(w,r),null,2)+"\n");
