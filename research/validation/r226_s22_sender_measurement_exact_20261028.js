#!/usr/bin/env node
"use strict";
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
function compute(csv){
const W=["PEER_COPY","SHARED_LATENT_SHOCK","HOMOPHILY_ONLY","HOMOPHILY_WITH_COPY","RANDOMIZED_PEER_COPY","RANDOMIZED_NO_COPY","RANDOMIZED_SIGNAL_ON_HOMOPHILY_NETWORK","ANTI_PEER_COPY"];
const random=new Set(["RANDOMIZED_PEER_COPY","RANDOMIZED_NO_COPY","RANDOMIZED_SIGNAL_ON_HOMOPHILY_NETWORK"]);
const check=(v,s)=>{if(!v)throw Error(s)};
const gcd=(a,b)=>{a=Math.abs(a);b=Math.abs(b);while(b){[a,b]=[b,a%b]}return a||1};
const f=(n,d=1)=>{check(Number.isSafeInteger(n)&&Number.isSafeInteger(d)&&d!==0,"bad rational");if(d<0){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g]};
const fmt=(x)=>x===null?null:x[1]===1?String(x[0]):x[0]+"/"+x[1];
const parse=(s)=>{let x=s.split("/").map(Number);return f(x[0],x[1]||1)};
const add=(a,b)=>f(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const sub=(a,b)=>add(a,[-b[0],b[1]]);
const mul=(a,b)=>f(a[0]*b[0],a[1]*b[1]);
const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const header="world,oracle_U,oracle_V,external_random_R,independent_background_Q,observed_edge_E,observed_sender_A0,observed_receiver_B0,observed_receiver_B1,oracle_B1_doA0,oracle_B1_doA1,original_probability".split(",");
const lines=csv.trimEnd().split(/\r?\n/);check(lines.shift()===header.join(","),"source header");
const rows=lines.map(line=>{let a=line.split(",");check(a.length===12,"source columns");return Object.fromEntries(header.map((h,i)=>[h,a[i]]))});
check(rows.length===128,"source rows");
const group=new Map(W.map(w=>[w,[]]));
for(const r of rows){check(group.has(r.world)&&r.original_probability==="1/16","source identity or probability");for(const h of header.slice(1,11))check(r[h]==="0"||r[h]==="1","binary source");group.get(r.world).push(r)}
let assertions=0;const a=(x,s)=>{assertions++;check(x,s)};
const out=[];
for(const w of W){
const src=group.get(w);a(src.length===16,"world rows");
a(new Set(src.map(r=>["oracle_U","oracle_V","external_random_R","independent_background_Q"].map(h=>r[h]).join(""))).size===16,"world unique sources");
for(let k=0;k<=4;k++){
let total=0,edge=0,discord=0,oraclePop=0,oracleEdge=0;
const an=[0,0],ad=[0,0],rn=[0,0],rd=[0,0],joint=new Map();
for(const r of src){
const e=+r.observed_edge_E,x=+r.observed_sender_A0,b0=+r.observed_receiver_B0,b1=+r.observed_receiver_B1,R=+r.external_random_R;
const effect=+r.oracle_B1_doA1-(+r.oracle_B1_doA0);
a(b1===+(x?r.oracle_B1_doA1:r.oracle_B1_doA0),"source consistency");
for(let t=0;t<2;t++){
const mass=t?k:8-k,A=x^t,key=""+e+A+b0+b1;
joint.set(key,(joint.get(key)||0)+mass);
total+=mass;oraclePop+=mass*effect;
if(e){edge+=mass;oracleEdge+=mass*effect;if(A!==b0)discord+=mass;ad[A]+=mass;an[A]+=mass*b1;if(random.has(w)){rd[R]+=mass;rn[R]+=mass*b1}}
}}
a(total===128&&[...joint.values()].reduce((x,y)=>x+y,0)===128,"mass");
a(edge>0&&ad[0]>0&&ad[1]>0,"sender support");
const obs=sub(f(an[1],ad[1]),f(an[0],ad[0])),truth=f(oracleEdge,edge),population=f(oraclePop,total);
const itt=random.has(w)?sub(f(rn[1],rd[1]),f(rn[0],rd[0])):null;
out.push({world:w,p:fmt(f(k,8)),source_slots:32,connected_probability:fmt(f(edge,128)),observed_discordance_given_edge:fmt(f(discord,edge)),observed_peer_contrast:fmt(obs),true_connected_doA_effect:fmt(truth),true_population_doA_effect:fmt(population),observed_minus_true_connected:fmt(sub(obs,truth)),randomized_assignment_contrast:fmt(itt),observation_signature:Object.fromEntries([...joint].filter(x=>x[1]>0).sort((x,y)=>x[0].localeCompare(y[0])).map(([key,n])=>[key,fmt(f(n,128))]))});
}}
for(const w of W){
const rr=out.filter(x=>x.world===w),base=rr[0];
for(let k=0;k<=4;k++){
const r=rr[k];
a(eq(parse(r.observed_peer_contrast),mul(parse(base.observed_peer_contrast),f(4-k,4))),"attenuation "+w+"/"+k);
const d=parse(base.observed_discordance_given_edge);
a(eq(parse(r.observed_discordance_given_edge),add(d,mul(f(k,8),sub(f(1),mul(f(2),d))))),"discordance "+w+"/"+k);
a(r.true_connected_doA_effect===base.true_connected_doA_effect,"oracle stability");
a(random.has(w)?r.randomized_assignment_contrast===base.randomized_assignment_contrast:r.randomized_assignment_contrast===null,"randomization gate");
}}
for(let k=0;k<=4;k++){
const pick=w=>out.find(r=>r.world===w&&r.p===fmt(f(k,8)));
a(JSON.stringify(pick(W[0]).observation_signature)===JSON.stringify(pick(W[1]).observation_signature),"alias common");
a(JSON.stringify(pick(W[2]).observation_signature)===JSON.stringify(pick(W[3]).observation_signature),"alias homophily");
}
for(const r of out.filter(r=>r.p==="1/2"))a(r.observed_peer_contrast==="0","full erasure");
a(out.length===40,"condition count");
return {study:"R226_S22",scope:"FINITE_ARTIFICIAL_E1_ONLY",protocol_path:"protocols/R226_S22_SENDER_MISCLASSIFICATION_PRESCORE_FREEZE_2026-10-28.md",original_source_path:"research/R226/R226_ALL_128_ORIGINAL_SELECTION_INFLUENCE_ATOMS.csv",original_source_sha256:"f5f012fa36b31ee71b8e5f409585a5ddf4d3146a61f5c54ad6f67a6cb05cd572",worlds:8,misclassification_levels:5,source_slots:1280,conditions:40,internal_assertions:assertions,R073:"FROZEN",PESEN_v0_1:"FROZEN",new_human_E2:0,new_historical_E3:0,rows:out};
}
const SOURCE=path.join(__dirname,"..","R226","R226_ALL_128_ORIGINAL_SELECTION_INFLUENCE_ATOMS.csv");
const RECEIPT=path.join(__dirname,"R226_S22_40_CONDITION_EXACT_RECEIPT_2026-10-28.json");
function main(){const csv=fs.readFileSync(SOURCE,"utf8");const sha=crypto.createHash("sha256").update(Buffer.from(csv,"utf8")).digest("hex");if(sha!=="f5f012fa36b31ee71b8e5f409585a5ddf4d3146a61f5c54ad6f67a6cb05cd572")throw Error("original source sha256 changed");const r=compute(csv);if(process.argv.includes("--emit"))fs.writeFileSync(RECEIPT,JSON.stringify(r,null,2)+"\n");else if(process.argv.includes("--check")){if(JSON.stringify(JSON.parse(fs.readFileSync(RECEIPT,"utf8")))!==JSON.stringify(r))throw Error("receipt mismatch");}else throw Error("use --emit or --check");process.stdout.write(JSON.stringify({conditions:r.conditions,source_slots:r.source_slots,assertions:r.internal_assertions,sha256:sha})+"\n");}
if(require.main===module)main();module.exports={compute};
