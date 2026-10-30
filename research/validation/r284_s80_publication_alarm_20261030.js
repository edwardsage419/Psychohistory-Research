"use strict";
const POLICIES=["COMPLETE_REGISTRY","POSITIVE_ONLY","POSITIVE_PREFERRED"];
const HEADER="policy,source8,Ybits,Rbits,included4,K,J,T,published_alarm,registry_alarm,mass,evidence";
function frac(a,b){function gcd(x,y){while(y){let z=x%y;x=y;y=z;}return x;}let g=gcd(a,b);return b/g===1?String(a/g):String(a/g)+"/"+String(b/g);}
function calculate(){
 let csv=[HEADER],worlds=[];
 for(const p of POLICIES){
  let c={eligible:0,alarm:0,registry:0,false_alarm:0,miss_alarm:0,none:0,cell00:0,cell01:0,cell10:0,cell11:0};
  for(let n=0;n<256;n++){
   let s=n.toString(2).padStart(8,"0"),Y=[0,2,4,6].map(i=>+s[i]),R=[1,3,5,7].map(i=>+s[i]);
   let flags=Y.map((y,i)=>p==="COMPLETE_REGISTRY"?1:p==="POSITIVE_ONLY"?y:+Boolean(y||R[i]));
   let K=flags.reduce((a,b)=>a+b,0),J=Y.reduce((a,y,i)=>a+y*flags[i],0),T=Y.reduce((a,b)=>a+b,0);
   let pa=+(K>=2&&4*J>=3*K),ra=+(T>=3);
   c.eligible+=+(K>=2);c.none+=+(K===0);c.alarm+=pa;c.registry+=ra;c.false_alarm+=pa*(1-ra);c.miss_alarm+=(1-pa)*ra;c["cell"+pa+ra]++;
   csv.push([p,s,Y.join(""),R.join(""),flags.join(""),K,J,T,pa,ra,"1/256","E1_ARTIFICIAL"].join(","));
  }
  if(c.cell00+c.cell01+c.cell10+c.cell11!==256)throw Error("mass failure");
  worlds.push({policy:p,original_source_types:256,counts:c,probabilities:{eligible:frac(c.eligible,256),published_alarm:frac(c.alarm,256),published_alarm_given_eligible:frac(c.alarm,c.eligible),registry_alarm:frac(c.registry,256),published_only_false_alarm:frac(c.false_alarm,256),registry_only_missed_alarm:frac(c.miss_alarm,256),no_publication:frac(c.none,256)}});
 }
 let result={research_id:"R284",extension:"S80-v1",original_catalogue_id:"12-014",protocol_freeze_commit:"dd478613b265823f620db2affb69ef94ffb7a955",evidence:"E1_ARTIFICIAL_NONBLIND",source_count:768,source_probability:"1/256",threshold:"3/4",min_published_count:2,policy_worlds:worlds,real_human_E2_prediction:0,real_historical_E3_prediction:0,external_team_replication:"NOT_RUN",R073:"FROZEN",PESEN_v0_1:"FROZEN"};
 return {csv:csv.join("\n")+"\n",json:JSON.stringify(result,null,2)+"\n",result};
}
if(typeof require!=="undefined"&&require.main===module){let fs=require("fs"),path=require("path"),o=calculate(),d=process.argv[2]||".";fs.mkdirSync(d,{recursive:true});fs.writeFileSync(path.join(d,"R284_S80_ALL_768_SOURCES.csv"),o.csv);fs.writeFileSync(path.join(d,"R284_S80_RESULTS.json"),o.json);console.log(JSON.stringify(o.result.policy_worlds.map(w=>({policy:w.policy,counts:w.counts}))));}
