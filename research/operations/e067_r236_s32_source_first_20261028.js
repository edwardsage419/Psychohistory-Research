// E067: source-first exact audit. Run with Node.js 18+ and two local input paths.
// Usage: node e067_r236_s32_source_first_20261028.js research/R236/R236_ALL_576_ORIGINAL_SURVEY_RESPONSE_SOURCES.csv research/validation/R236_S32_RESPONSE_RETENTION_54_CONDITION_RECEIPT_2026-10-28.json
"use strict";
const fs = require("node:fs");
function audit(csv,receipt){
  let checks=0,failures=[];
  function check(ok,msg){checks++;if(!ok&&failures.length<25)failures.push(msg);}
  function frac(s){let [a,b="1"]=String(s).split("/");return [BigInt(a),BigInt(b)];}
  function equal(a,b){let x=Array.isArray(a)?a:frac(a),y=Array.isArray(b)?b:frac(b);return x[0]*y[1]===y[0]*x[1];}
  const lines=csv.trim().split(/\r?\n/),headers=lines.shift().split(",");
  const rows=lines.map(line=>Object.fromEntries(line.split(",").map((v,i)=>[headers[i],v])));
  check(rows.length===576,"source row count");
  check(receipt.conditions.length===54,"receipt condition count");
  const fields=["oracle_original_T","oracle_original_S","oracle_original_U","oracle_original_R","oracle_proxy_ascertainment_E1","oracle_proxy_ascertainment_E2","observed_mode_R","observed_report_Y1","observed_report_Y2","oracle_B1_doR0","oracle_B1_doR1"];
  const worlds=new Map();
  for(let i=0;i<rows.length;i++){
    let row=rows[i];check(equal(row.original_probability,"1/64"),"p row "+i);
    for(const f of fields)check(row[f]==="0"||row[f]==="1",f+" row "+i);
    for(const f of ["observed_prior_proxy_P","observed_prior_proxy_Z"])check(["-1","0","1"].includes(row[f]),f+" row "+i);
    check(row.observed_mode_R===row.oracle_original_R,"random mode row "+i);
    if(!worlds.has(row.world))worlds.set(row.world,[]);
    worlds.get(row.world).push(row);
  }
  check(worlds.size===9,"nine worlds");
  const rules=["ALL","Y1_POS_HALF","Y1_NEG_HALF","R1_POS_HALF","R1_NEG_HALF","PROXY_P_MISSING_HALF"];
  const summaries=[];
  for(const [world,items] of worlds){
    check(items.length===64,world+" count");
    let oracle=items.reduce((s,r)=>s+BigInt(r.oracle_B1_doR1)-BigInt(r.oracle_B1_doR0),0n);
    let seen=new Set(items.map(r=>["oracle_original_T","oracle_original_S","oracle_original_U","oracle_original_R","oracle_proxy_ascertainment_E1","oracle_proxy_ascertainment_E2"].map(k=>r[k]).join("")));
    check(seen.size===64,world+" unique exogenous");
    let baseline=null;
    for(const rule of rules){
      const c=receipt.conditions.find(x=>x.world===world&&x.rule===rule);
      check(!!c,world+" "+rule+" exists");
      if(!c)continue;
      let total=0n,groups=[0n,0n],success=[0n,0n],joint=new Map();
      for(const r of items){
        const R=Number(r.observed_mode_R),Y=Number(r.observed_report_Y1),P=Number(r.observed_prior_proxy_P);
        const half=(rule==="Y1_POS_HALF"&&Y===1)||(rule==="Y1_NEG_HALF"&&Y===0)||(rule==="R1_POS_HALF"&&R===1&&Y===1)||(rule==="R1_NEG_HALF"&&R===1&&Y===0)||(rule==="PROXY_P_MISSING_HALF"&&P===-1);
        const w=half?1n:2n;
        total+=w;groups[R]+=w;if(Y===1)success[R]+=w;
        const key=["observed_mode_R","observed_prior_proxy_P","observed_prior_proxy_Z","observed_report_Y1","observed_report_Y2"].map(f=>r[f]).join(",");
        joint.set(key,(joint.get(key)||0n)+w);
      }
      let itt=[success[1]*groups[0]-success[0]*groups[1],groups[1]*groups[0]];
      if(rule==="ALL")baseline=itt;
      check(equal([total,128n],c.retention_probability),world+" "+rule+" retention");
      check(equal([groups[0],total],c.retained_mode_R0_probability),world+" "+rule+" R0");
      check(equal([groups[1],total],c.retained_mode_R1_probability),world+" "+rule+" R1");
      check(equal(itt,c.reported_ITT),world+" "+rule+" ITT");
      check(equal([oracle,64n],c.oracle_private_mode_effect),world+" "+rule+" oracle");
      check(equal(baseline,c.baseline_reported_ITT),world+" "+rule+" baseline");
      check(joint.size===c.observable_joint_support,world+" "+rule+" support");
      check(joint.size===Object.keys(c.observable_joint).length,world+" "+rule+" cells");
      for(const [k,v] of joint)check(equal([v,total],c.observable_joint[k]??"0"),world+" "+rule+" cell "+k);
      for(const k of Object.keys(c.observable_joint))check(joint.has(k),world+" "+rule+" unexpected "+k);
      if(rule==="R1_POS_HALF"||rule==="R1_NEG_HALF")summaries.push({world,rule,itt:c.reported_ITT});
    }
  }
  const clone=JSON.parse(JSON.stringify(receipt));
  clone.conditions.find(c=>c.world==="TRUTHFUL_STABLE"&&c.rule==="R1_POS_HALF").reported_ITT="999";
  check(!equal([-1n,6n],clone.conditions.find(c=>c.world==="TRUTHFUL_STABLE"&&c.rule==="R1_POS_HALF").reported_ITT),"mutation detection");
  return {checks,failures,worlds:worlds.size,source_rows:rows.length,conditions:receipt.conditions.length,representative:summaries.filter(x=>x.world==="TRUTHFUL_STABLE"||x.world==="SOCIAL_DESIRABILITY_U"),mutation_detected:true};
}
if (require.main === module) {
  if (process.argv.length !== 4) { console.error("Usage: node script.js SOURCE.csv RECEIPT.json"); process.exit(2); }
  const result = audit(fs.readFileSync(process.argv[2],"utf8"),JSON.parse(fs.readFileSync(process.argv[3],"utf8")));
  console.log(JSON.stringify(result,null,2));
  if (result.failures.length || result.checks !== 12364) process.exit(1);
}
