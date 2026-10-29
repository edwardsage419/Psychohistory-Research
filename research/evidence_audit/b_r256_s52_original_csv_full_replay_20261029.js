"use strict";
// R256 S52 full original CSV audit. Node.js standard library only.
// node research/evidence_audit/b_r256_s52_original_csv_full_replay_20261029.js
const WORLDS=[
["IDLE_NO_ARRIVALS",0,0.5,"SERVICE_FIRST"],["FAST_SERVICE_HALF_ARRIVAL",0.5,1,"SERVICE_FIRST"],
["BALANCED_INDEPENDENT_HALF_HALF",0.5,0.5,"SERVICE_FIRST"],
["DEMAND_ALWAYS_HALF_SERVICE",1,0.5,"SERVICE_FIRST"],
["NO_SERVICE_HALF_ARRIVAL",0.5,0,"SERVICE_FIRST"],
["DEMAND_ALWAYS_NO_SERVICE",1,0,"SERVICE_FIRST"],
["ARRIVAL_FIRST_BALANCED_HALF_HALF",0.5,0.5,"ARRIVAL_FIRST"],
["SHARED_DEMAND_ENV_HALF_HALF",0.5,0.5,"SERVICE_FIRST"],
["STATIC_EMPTY_TRUE_QUEUE_SENSOR_ALIAS",0.5,0.5,"SERVICE_FIRST"]];
const EXPECTED_SHA256="8be5360465497321c15bffc554c7088fad48bcef71847e43e2ee2f714ed5119b";
function verify(csv){
 if(!csv.endsWith("\n"))throw Error("missing final newline");
 const lines=csv.trimEnd().split("\n"),columns=lines[0].split(",");
 if(lines.length!==4609||columns.length!==44)throw Error("source dimensions");
 let checked=0,flow=0;
 for(let wi=0;wi<9;wi++){
  const [world,pa,ps,policy]=WORLDS[wi];
  for(let mask=0;mask<512;mask++){
   const bit=i=>(mask>>(8-i))&1,u=bit(0);
   let q=0,offered=0,admitted=0,servedTotal=0,rejectedTotal=0;
   const expected={world,oracle_original_shared_environment_U:u,frozen_event_order:policy};
   for(let t=1;t<=4;t++){
    const a0=bit(2*t-1),s0=bit(2*t);
    const a=world==="SHARED_DEMAND_ENV_HALF_HALF"?u:pa===0.5?a0:pa;
    const s=ps===0.5?s0:ps;
    let d,g,reject,qn;
    if(policy==="SERVICE_FIRST"){
     d=q>0&&s?1:0;g=a&&q-d<2?1:0;reject=a-g;qn=q-d+g;
    }else{
     g=a&&q<2?1:0;reject=a-g;d=q+g>0&&s?1:0;qn=q+g-d;
    }
    if(q+a!==qn+d+reject||qn<0||qn>2)throw Error("source flow");
    flow++;offered+=a;admitted+=g;servedTotal+=d;rejectedTotal+=reject;q=qn;
    Object.assign(expected,{
     ["oracle_original_arrival_bit_A"+t]:a0,["oracle_original_service_bit_S"+t]:s0,
     ["oracle_exogenous_realized_offered_arrival_a"+t]:a,
     ["oracle_exogenous_realized_available_service_s"+t]:s,
     ["observed_reported_queue_Q"+t]:q,["oracle_model_served_d"+t]:d,
     ["oracle_model_rejected_r"+t]:reject,["oracle_model_admitted_g"+t]:g,
     ["oracle_true_hidden_physical_queue_H"+t]:world==="STATIC_EMPTY_TRUE_QUEUE_SENSOR_ALIAS"?0:q
    });
   }
   Object.assign(expected,{oracle_total_offered:offered,oracle_total_admitted:admitted,oracle_total_served:servedTotal,oracle_total_rejected:rejectedTotal,original_complete_ninebit_source_probability:"1/512"});
   const actual=lines[1+wi*512+mask].split(",");
   if(actual.length!==44)throw Error("row columns");
   for(let j=0;j<44;j++){
    if(actual[j]!==String(expected[columns[j]]))throw Error("original source mismatch "+world+" "+mask+" "+columns[j]);
    checked++;
   }
  }
 }
 return {research_id:"R256_S52",original_csv_rows:4608,columns:44,compared_cells:checked,conservation_checks:flow,source_sha256_expected:EXPECTED_SHA256,original_csv_full_row_comparison:"PASS",evidence:"INTERNAL_E1"};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs"),crypto=require("crypto"),path=require("path");
 const file=path.join(__dirname,"..","R256","R256_ALL_4608_ORIGINAL_FOUR_SLOT_QUEUE_SOURCE_ATOMS.csv");
 const raw=fs.readFileSync(file);
 const sha=crypto.createHash("sha256").update(raw).digest("hex");
 if(sha!==EXPECTED_SHA256)throw Error("original source SHA256 mismatch");
 const out=verify(raw.toString("utf8"));out.actual_source_sha256=sha;
 console.log(JSON.stringify(out,null,2));
}
