"use strict";
function check(v,m){if(!v)throw Error(m);}
function guard(csv,j){
check(j.research_id==="R307","research_id");check(j.extension==="S103","extension");
check(JSON.stringify(j.confirmatory_t)==="[1,2,3]","confirmatory_t");check(j.candidate_triples_per_t===27,"candidate_triples_per_t");
check(j.prior==="1/2"&&j.world_count===81,"universe");
check(j.evidence==="E1_ARTIFICIAL"&&j.real_human_E2===0&&j.historical_E3===0,"scope");
check(j.R073==="FROZEN"&&j.PESEN_v0_1==="FROZEN","freeze");
const rows=csv.trimEnd().split("\n");
check(rows[0]==="t,c,k,n,private,public_m1,public_m2"&&rows.length===82,"CSV rows");
check(new Set(rows.slice(1).map(x=>x.split(",").slice(0,4).join("|"))).size===81,"world keys");
const names=["D0_T0_JOINT_M1","D1_PRIVATE_M1","D2_PUBLIC_M1","D3_PUBLIC_M1_M2","D4_JOINT_M1","D5_JOINT_M1_M2"];
check(JSON.stringify(j.designs)===JSON.stringify(names),"designs");
check(j.results.length===18,"result count");
const ids=new Set(j.results.map(x=>x.t+"|"+x.design));check(ids.size===18,"unique designs");
for(const t of [1,2,3])for(const name of names)check(ids.has(t+"|"+name),"missing design");
return true;
}
function run(csv,j){
check(guard(csv,j),"baseline");
const mutations=[
["research_id",x=>x.research_id="R999"],["extension",x=>delete x.extension],
["confirmatory_t",x=>x.confirmatory_t=[3,2,1]],["candidate_triples_per_t",x=>x.candidate_triples_per_t=999],
["evidence",x=>x.evidence="E2_HUMAN"],["duplicate_result",x=>x.results.push(JSON.parse(JSON.stringify(x.results[0])))]];
let rejected=0;for(const [name,edit] of mutations){let x=JSON.parse(JSON.stringify(j));edit(x);try{guard(csv,x);}catch(e){rejected++;continue;}throw Error("false acceptance "+name);}
return {baseline:"PASS",mutations_rejected:rejected,scope:"supplemental identity gate, not original algebra replacement"};
}
if(typeof module!=="undefined"&&require.main===module){
const fs=require("node:fs"),csv=fs.readFileSync(process.argv[2],"utf8"),j=JSON.parse(fs.readFileSync(process.argv[3],"utf8"));
console.log(JSON.stringify(run(csv,j)));
}