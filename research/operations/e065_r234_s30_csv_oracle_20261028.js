"use strict";
const columns=["observed_X01","observed_X02","observed_X03","observed_X11","observed_X12","observed_X13"];
const tests=[
["ALL",x=>true],
["BASELINE_ITEM1_POS",x=>x[0]>0],
["FOLLOWUP_ITEM1_POS",x=>x[3]>0],
["FOLLOWUP_ITEM1_NONNEG",x=>x[3]>=0],
["FOLLOWUP_COMPOSITE_GAIN_POS",x=>x[3]+x[4]+x[5]>x[0]+x[1]+x[2]]
];
function frac(n,d){if(d===0)throw Error("empty");let a=Math.abs(n),b=d;while(b){let t=a%b;a=b;b=t;}let g=a||1;return d/g===1?String(n/g):n/g+"/"+d/g;}
function audit(csv,json){
const receipt=JSON.parse(json),lines=csv.trim().split(/\r?\n/),headers=lines.shift().split(","),ix=Object.fromEntries(headers.map((x,i)=>[x,i]));
let rows=lines.map(s=>s.split(",")),groups=new Map(),checks=0,byWorld={},failures=[];
function eq(a,b,context){checks++;if(JSON.stringify(a)!==JSON.stringify(b))failures.push({context,expected:b,actual:a});}
eq(rows.length,2304,"row_count");
for(const r of rows){let w=r[ix.world];if(!groups.has(w))groups.set(w,[]);groups.get(w).push(r);eq(r[ix.original_source_probability],"1/256","source_mass");for(let j=0;j<3;j++){eq(Number(r[ix["observed_X1"+(j+1)]])-Number(r[ix["observed_X0"+(j+1)]]),Number(r[ix["observed_paired_difference_item"+(j+1)]]),"row_delta");}}
eq(groups.size,9,"worlds");
for(const wr of receipt.world_results){
let rs=groups.get(wr.world)||[];eq(rs.length,256,"world_rows");byWorld[wr.world]={};
for(const [name,rule] of tests){
let subset=rs.filter(r=>rule(columns.map(c=>Number(r[ix[c]]))));
let n=subset.length,ref=wr.selection_results[name];eq(ref.status,n?"OK":"EMPTY_SUPPORT",wr.world+"/"+name+"/status");
if(!n)continue;
let sum=Array(6).fill(0),latent=0,keys=new Map();
for(const r of subset){let x=columns.map(c=>Number(r[ix[c]]));x.forEach((v,i)=>sum[i]+=v);latent+=Number(r[ix.oracle_true_individual_latent_change]);let key=x.join(",");keys.set(key,(keys.get(key)||0)+1);}
let means=sum.map(v=>frac(v,n)),change=[0,1,2].map(i=>frac(sum[i+3]-sum[i],n)),comp=frac(sum[3]+sum[4]+sum[5]-sum[0]-sum[1]-sum[2],3*n),oracle=frac(latent,n);
eq(n,ref.selected,wr.world+"/"+name+"/selected");eq(frac(n,256),ref.retention,wr.world+"/"+name+"/retention");eq(keys.size,ref.support,wr.world+"/"+name+"/support");for(let i=0;i<6;i++)eq(means[i],ref.observed_means[i],wr.world+"/"+name+"/mean"+i);for(let i=0;i<3;i++)eq(change[i],ref.observed_item_change[i],wr.world+"/"+name+"/delta"+i);eq(comp,ref.observed_composite_change,wr.world+"/"+name+"/composite");eq(oracle,ref.oracle_true_latent_change_mean,wr.world+"/"+name+"/oracle");
byWorld[wr.world][name]={n,keys:[...keys].sort((a,b)=>a[0].localeCompare(b[0]))};
}
}
for(const [a,b] of receipt.observational_alias_pairs)for(const [name] of tests)eq(byWorld[a][name].keys,byWorld[b][name].keys,"alias/"+a+"/"+b+"/"+name);
eq(byWorld.STABLE_BASE.FOLLOWUP_ITEM1_POS.n,64,"negative_control_selected");
return {checks,failures,worlds:groups.size,conditions:receipt.conditions,rows:rows.length,source:"CSV-first independent integer sums",note:"same frozen synthetic data; internal verification only"};
}
if(typeof require!=="undefined" && typeof module!=="undefined" && require.main===module){
const fs=require("fs"),path=require("path"),root=path.resolve(__dirname,"../..");
const csv=fs.readFileSync(path.join(root,"research/R234/R234_ALL_2304_ORIGINAL_TWO_WAVE_SOURCES.csv"),"utf8");
const json=fs.readFileSync(path.join(root,"research/validation/R234_S30_OBSERVED_ATTRITION_45_CONDITION_RECEIPT_2026-10-28.json"),"utf8");
const out=audit(csv,json);console.log(JSON.stringify({checks:out.checks,failures:out.failures,worlds:out.worlds,conditions:out.conditions,rows:out.rows},null,2));if(out.failures.length)process.exitCode=1;
}
if(typeof module!=="undefined")module.exports={audit};
