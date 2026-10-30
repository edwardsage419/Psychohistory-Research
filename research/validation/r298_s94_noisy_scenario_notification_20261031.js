"use strict";
// R298 S94 E1 exact rational notification-channel model; native Node CLI --test/--emit/--check.
const SC=["BASELINE","REWARD_SHIFT","TRANSITION_SWAP","BOTH"],G=["1/2","1"],E=["0","1/4","1/2","3/4","1"],C=["MODEL_BASED_PLANNER","CACHED_VALUES"],A=["LEFT","RIGHT"];
const FREEZE="479b96c37c53c4d5f62503f308ab2067daa26933",ORIG_SHA="10e78b17e24296703b3379997edfb3384991b95e316eaac7fe3c1f557322c326";
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n;}
function F(x,y=1n){x=BigInt(x);y=BigInt(y);if(y===0n)throw Error("zero denom");if(y<0n){x=-x;y=-y;}let z=gcd(x,y);return [x/z,y/z];}
function P(s){let v=s.split("/");return F(v[0],v[1]||1);}
function S(a){return a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);}
function add(a,b){return F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function mul(a,b){return F(a[0]*b[0],a[1]*b[1]);}
function sub(a,b){return F(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);}
function eq(a,b){return a[0]===b[0]&&a[1]===b[1];}
function check(ok,label){if(!ok)throw Error("S94 check failed: "+label);}
function Q(t,g){let v=t==="BASELINE"?[2,1]:t==="REWARD_SHIFT"?[0,3]:t==="TRANSITION_SWAP"?[1,2]:[3,0];return v.map(x=>mul(P(g),F(x)));}
function choice(q){return q[1][0]*q[0][1]>q[0][0]*q[1][1]?"RIGHT":"LEFT";}
function build(){
 let rows=[],worlds=[],summaries=[],fields=["world","true_scenario","gamma","error_rate","controller","message_scenario","message_probability","action","actual_Q","predicted_Q","chosen_action","oracle_action","regret","wrong_choice"];
 for(let t of SC)for(let g of G)for(let e of E)for(let c of C){
  let world="true="+t+"|gamma="+g+"|e="+e+"|controller="+c,loss=F(0),wrong=F(0),mass=F(0),messages=[];
  for(let m of SC){
   let prob=t===m?sub(F(1),P(e)):mul(P(e),F(1,3)),real=Q(t,g),pred=Q(c===C[0]?m:"BASELINE",g),chosen=choice(pred),oracle=choice(real),bad=chosen!==oracle;
   let regret=bad?sub(real[A.indexOf(oracle)],real[A.indexOf(chosen)]):F(0);
   mass=add(mass,prob);loss=add(loss,mul(prob,regret));if(bad)wrong=add(wrong,prob);
   messages.push({message:m,probability:S(prob),chosen_action:chosen,oracle_action:oracle,regret:S(regret),wrong_choice:bad});
   for(let i=0;i<2;i++)rows.push({world,true_scenario:t,gamma:g,error_rate:e,controller:c,message_scenario:m,message_probability:S(prob),action:A[i],actual_Q:S(real[i]),predicted_Q:S(pred[i]),chosen_action:chosen,oracle_action:oracle,regret:S(regret),wrong_choice:bad?1:0});
  }
  check(eq(mass,F(1)),world+" mass");
  let gap=mul(P(g),F(t==="BASELINE"||t==="TRANSITION_SWAP"?1:3)),wrongExpected=c===C[0]?mul(F(2,3),P(e)):F(t==="BASELINE"||t==="BOTH"?0:1);
  check(eq(wrong,wrongExpected)&&eq(loss,mul(gap,wrongExpected)),world+" exact oracle");
  worlds.push({world,true_scenario:t,gamma:g,error_rate:e,controller:c,expected_regret:S(loss),wrong_choice_probability:S(wrong),messages});
 }
 check(worlds.length===80&&rows.length===640,"counts");
 check(new Set(rows.map(r=>r.world+"|"+r.message_scenario+"|"+r.action)).size===640,"unique keys");
 for(let g of G)for(let e of E)for(let c of C){
  let chosen=worlds.filter(w=>w.gamma===g&&w.error_rate===e&&w.controller===c),loss=F(0),wrong=F(0);
  check(chosen.length===4,"scenario coverage");
  for(let w of chosen){loss=add(loss,P(w.expected_regret));wrong=add(wrong,P(w.wrong_choice_probability));}
  loss=mul(loss,F(1,4));wrong=mul(wrong,F(1,4));
  let target=c===C[0]?mul(mul(F(4,3),P(e)),P(g)):P(g),wrongTarget=c===C[0]?mul(F(2,3),P(e)):F(1,2);
  check(eq(loss,target)&&eq(wrong,wrongTarget),"mean "+g+"/"+e+"/"+c);
  summaries.push({gamma:g,error_rate:e,controller:c,equal_scenario_mean_regret:S(loss),equal_scenario_wrong_probability:S(wrong)});
 }
 const result={research_id:"R298",extension:"S94",freeze_commit:FREEZE,original_source_sha256:ORIG_SHA,evidence:"E1_SYNTHETIC_ONLY",new_E2:0,new_E3:0,external_replication:false,world_count:80,message_branches:320,action_rows:640,worlds,summaries};
 const csv=fields.join(",")+"\n"+rows.map(r=>fields.map(k=>r[k]).join(",")).join("\n")+"\n";
 return {rows,worlds,summaries,csv,json:JSON.stringify(result,null,2)+"\n"};
}
if(typeof module!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path"),crypto=require("crypto"),v=build(),dir=process.argv[3]||".",mode=process.argv[2];
 const original=fs.readFileSync(path.join(__dirname,"../R298/R298_ALL_64_ORIGINAL_REVALUATION_ACTION_SOURCES.csv"));
 check(crypto.createHash("sha256").update(original).digest("hex")===ORIG_SHA,"original sha");
 check(original.toString("utf8").trim().split(/\r?\n/).length===65,"original rows");
 const p=path.join(dir,"R298_S94_ALL_640_MESSAGE_ACTION_SOURCES.csv"),j=path.join(dir,"R298_S94_EXACT_NOISY_NOTIFICATION_RESULTS.json");
 if(mode==="--test")console.log("PASS 80 worlds 320 messages 640 rows original sha verified");
 else if(mode==="--emit"){fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(p,v.csv);fs.writeFileSync(j,v.json);console.log("EMITTED");}
 else if(mode==="--check"){check(fs.readFileSync(p,"utf8")===v.csv,"CSV bytes");check(fs.readFileSync(j,"utf8")===v.json,"JSON bytes");console.log("PASS archived bytes");}
 else throw Error("Usage: --test | --emit DIR | --check DIR");
}