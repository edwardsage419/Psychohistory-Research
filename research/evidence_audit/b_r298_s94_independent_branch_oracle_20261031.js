"use strict";
// R298 S94 nonblind independent exact oracle; no R generator import.
const TYPES=["BASELINE","REWARD_SHIFT","TRANSITION_SWAP","BOTH"],ES=["0","1/4","1/2","3/4","1"],GS=["1/2","1"],CS=["MODEL_BASED_PLANNER","CACHED_VALUES"];
const FIELDS=["world","true_scenario","gamma","error_rate","controller","message_scenario","message_probability","action","actual_Q","predicted_Q","chosen_action","oracle_action","regret","wrong_choice"];
function assert(x,m){if(!x)throw Error("B S94 FAIL: "+m);}
function rat(s){let p=String(s).split("/");return [BigInt(p[0]),BigInt(p[1]||1)];}
function gcd(a,b){while(b){let z=a%b;a=b;b=z;}return a<0n?-a:a;}
function norm(a){let g=gcd(a[0],a[1]);return [a[0]/g,a[1]/g];}
function add(a,b){return norm([a[0]*b[1]+b[0]*a[1],a[1]*b[1]]);}
function mul(a,b){return norm([a[0]*b[0],a[1]*b[1]]);}
function sub(a,b){return norm([a[0]*b[1]-b[0]*a[1],a[1]*b[1]]);}
function same(a,b){return a[0]*b[1]===b[0]*a[1];}
function val(s,g){let k=s==="BASELINE"?[2,1]:s==="REWARD_SHIFT"?[0,3]:s==="TRANSITION_SWAP"?[1,2]:[3,0];return k.map(v=>mul(rat(g),rat(v)));}
function winner(s){return s==="REWARD_SHIFT"||s==="TRANSITION_SWAP"?"RIGHT":"LEFT";}
function parseCSV(s){let lines=s.trim().split(/\r?\n/),keys=lines.shift().split(",");assert(keys.join("|")===FIELDS.join("|"),"CSV header");return lines.map(l=>{let v=l.split(",");assert(v.length===keys.length,"CSV width");return Object.fromEntries(keys.map((k,i)=>[k,v[i]]));});}
function audit(csv,json,original){
 let rows=parseCSV(csv),doc=JSON.parse(json);
 assert(rows.length===640,"640 rows");assert(doc.worlds.length===80&&doc.summaries.length===20,"result coverage");
 assert(doc.evidence==="E1_SYNTHETIC_ONLY"&&doc.new_E2===0&&doc.new_E3===0&&doc.external_replication===false,"evidence boundary");
 assert(doc.freeze_commit==="479b96c37c53c4d5f62503f308ab2067daa26933","freeze identity");
 let byKey=new Map();
 for(let r of rows){let k=[r.true_scenario,r.gamma,r.error_rate,r.controller,r.message_scenario,r.action].join("|");assert(!byKey.has(k),"duplicate row");byKey.set(k,r);}
 let wmap=new Map(doc.worlds.map(w=>[w.world,w]));assert(wmap.size===80,"unique worlds");
 let checks=0;
 for(let t of TYPES)for(let g of GS)for(let e of ES)for(let c of CS){
  let world="true="+t+"|gamma="+g+"|e="+e+"|controller="+c,ww=wmap.get(world);
  assert(ww&&ww.messages.length===4,"world identity "+world);
  let total=rat(0),wrong=rat(0),mass=rat(0);
  for(let m of TYPES){
   let expectedP=m===t?sub(rat(1),rat(e)):mul(rat(e),rat("1/3"));
   let actual=val(t,g),belief=c===CS[0]?m:"BASELINE",pred=val(belief,g),chosen=winner(belief),oracle=winner(t),iswrong=chosen!==oracle;
   let regret=iswrong?sub(actual[oracle==="RIGHT"?1:0],actual[chosen==="RIGHT"?1:0]):rat(0);
   mass=add(mass,expectedP);total=add(total,mul(expectedP,regret));if(iswrong)wrong=add(wrong,expectedP);
   let mm=ww.messages.find(x=>x.message===m);
   assert(mm&&same(rat(mm.probability),expectedP)&&same(rat(mm.regret),regret)&&mm.chosen_action===chosen&&mm.oracle_action===oracle&&mm.wrong_choice===iswrong,"message receipt "+world+"/"+m);
   for(let ai=0;ai<2;ai++){
    let r=byKey.get([t,g,e,c,m,ai===0?"LEFT":"RIGHT"].join("|"));
    assert(r&&r.world===world&&r.true_scenario===t&&r.controller===c&&r.message_scenario===m,"source identity");
    assert(same(rat(r.message_probability),expectedP)&&same(rat(r.actual_Q),actual[ai])&&same(rat(r.predicted_Q),pred[ai]),"source Q/prob");
    assert(r.chosen_action===chosen&&r.oracle_action===oracle&&same(rat(r.regret),regret)&&r.wrong_choice===(iswrong?"1":"0"),"source decision");
    checks++;
   }
  }
  assert(same(mass,rat(1))&&same(rat(ww.expected_regret),total)&&same(rat(ww.wrong_choice_probability),wrong),"world weighted risk");
 }
 assert(byKey.size===640&&checks===640,"all source checks");
 for(let g of GS)for(let e of ES)for(let c of CS){
  let ss=doc.summaries.filter(s=>s.gamma===g&&s.error_rate===e&&s.controller===c);
  assert(ss.length===1,"unique summary");
  let expected=c===CS[0]?mul(mul(rat("4/3"),rat(e)),rat(g)):rat(g);
  let expectedWrong=c===CS[0]?mul(rat("2/3"),rat(e)):rat("1/2");
  assert(same(rat(ss[0].equal_scenario_mean_regret),expected)&&same(rat(ss[0].equal_scenario_wrong_probability),expectedWrong),"summary formula");
 }
 let originalChecks=0;
 if(original){
  let old=original.trim().split(/\r?\n/),head=old.shift().split(",");
  assert(old.length===64,"original R298 64");
  for(let l of old){
   let v=l.split(","),r=Object.fromEntries(head.map((k,i)=>[k,v[i]]));
   let actual=val(r.scenario,r.gamma),oracle=winner(r.scenario),chosen=r.controller===CS[0]&&r.notified==="1"?oracle:"LEFT";
   assert(r.chosen_action===chosen&&r.actual_optimal_action===oracle&&same(rat(r.actual_Q),actual[r.action==="LEFT"?0:1]),"original R298 parity");
   if(r.notified==="1"){
    let newRow=byKey.get([r.scenario,r.gamma,"0",r.controller,r.scenario,r.action].join("|"));
    assert(newRow&&newRow.chosen_action===r.chosen_action&&newRow.oracle_action===r.actual_optimal_action&&same(rat(newRow.actual_Q),rat(r.actual_Q)),"e0 original bridge");
   }
   originalChecks++;
  }
 }
 return {status:"PASS",nonblind:true,rows_checked:checks,worlds_checked:80,summaries_checked:20,original_rows_checked:originalChecks};
}
function mutationTests(csv,json,original){
 const base=JSON.parse(json),lines=csv.trimEnd().split("\n"),cases=[];
 function trial(label,c,j){let rejected=false;try{audit(c,j,original);}catch(e){rejected=true;}assert(rejected,"mutation escaped: "+label);cases.push(label);}
 trial("duplicate_source",csv+lines[1]+"\n",json);
 trial("omitted_source",lines.slice(0,-1).join("\n")+"\n",json);
 function editRow(label,key,value){let a=lines.slice(),v=a[1].split(",");v[FIELDS.indexOf(key)]=value;a[1]=v.join(",");trial(label,a.join("\n")+"\n",json);}
 editRow("actual_q_tamper","actual_Q","999");
 editRow("probability_tamper","message_probability","1/3");
 editRow("chosen_action_tamper","chosen_action","RIGHT");
 editRow("regret_tamper","regret","1");
 let j=JSON.parse(json);j.summaries[0].equal_scenario_mean_regret="999";trial("summary_tamper",csv,JSON.stringify(j));
 j=JSON.parse(json);j.evidence="E2_REAL_HUMAN";trial("evidence_upgrade",csv,JSON.stringify(j));
 return cases;
}
if(typeof module!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path");
 const dir=process.argv[2]||".";
 const c=fs.readFileSync(path.join(dir,"R298_S94_ALL_640_MESSAGE_ACTION_SOURCES.csv"),"utf8");
 const j=fs.readFileSync(path.join(dir,"R298_S94_EXACT_NOISY_NOTIFICATION_RESULTS.json"),"utf8");
 const o=fs.readFileSync(path.join(__dirname,"../R298/R298_ALL_64_ORIGINAL_REVALUATION_ACTION_SOURCES.csv"),"utf8");
 console.log(JSON.stringify({audit:audit(c,j,o),mutations:mutationTests(c,j,o)},null,2));
}