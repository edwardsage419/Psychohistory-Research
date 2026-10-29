#!/usr/bin/env node
"use strict";
// Usage: node r261_s57_prefix_brier_20261029.js <original_R261_CSV> [output_JSON]
// Requires Node.js built-in fs only. All losses use exact integer arithmetic.
const fs=require("fs");
function calculate(csv){
  "use strict";
  const S=1024;
  const WORLDS=["FINITE_NEUTRAL_IDIOSYNCRATIC","FINITE_CONVEX_SQUARE","FINITE_CONCAVE_CONFORMITY","FINITE_CONTRARIAN","INDEPENDENT_HALF","UNANIMOUS_ONLY","MAJORITY_TIE_UP","COMMON_NOISE_NEUTRAL","OBSERVED_COMMON_NOISE_TRUE_INDEPENDENT_SENSOR"];
  const shared=new Set(WORLDS.slice(7));
  const gcd=(a,b)=>{a=BigInt(a);b=BigInt(b);while(b){const t=a%b;a=b;b=t}return a<0n?-a:a};
  function frac(a,b=1n){a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("zero denominator");if(b<0n){a=-a;b=-b}const d=gcd(a,b);return (b/d===1n?String(a/d):String(a/d)+"/"+String(b/d))}
  function rationalToScale(x){const parts=x.split("/").map(Number);const d=parts[1]||1;if(!Number.isInteger(parts[0]*S/d))throw Error("unrepresentable probability "+x);return parts[0]*S/d}
  function q(w,m){if(!Number.isInteger(m)||m<0||m>S)throw Error("invalid mean");if(w===WORLDS[0]||shared.has(w))return m;if(w===WORLDS[1])return m*m/S;if(w===WORLDS[2])return 2*m-m*m/S;if(w===WORLDS[3])return S-m;if(w===WORLDS[4])return S/2;if(w===WORLDS[5])return m===S?S:0;if(w===WORLDS[6])return m>=S/2?S:0;throw Error("unknown world")}
  const lines=csv.trimEnd().split(/\r?\n/),heads=lines[0].split(","),rows=lines.slice(1);
  if(rows.length!==9216)throw Error("source count mismatch "+rows.length);
  const ix=Object.fromEntries(heads.map((h,i)=>[h,i]));
  const required=["world","original_complete_tenbit_source_probability","observed_initial_count_K0","oracle_public_generator_q_t0","oracle_public_generator_q_t1","observed_reported_count_K1","observed_reported_count_K2","observed_reported_agent0_state_t1","observed_reported_agent1_state_t1","observed_reported_agent0_state_t2","observed_reported_agent1_state_t2"];
  for(const h of required)if(ix[h]===undefined)throw Error("missing "+h);
  const bitCols=["oracle_original_initial_agent_bit_0","oracle_original_initial_agent_bit_1"];
  for(let t=0;t<2;t++)for(let i=0;i<2;i++)for(const b of ["a","b"])bitCols.push("oracle_original_step"+t+"_agent"+i+"_R_"+b);
  for(const h of bitCols)if(ix[h]===undefined)throw Error("missing source bit "+h);
  const groups=new Map(),unique=new Map();
  for(const line of rows){
    const v=line.split(",");if(v.length!==heads.length)throw Error("CSV column count mismatch");
    const w=v[ix.world],k=Number(v[ix.observed_initial_count_K0]);if(!WORLDS.includes(w)||![0,1,2].includes(k))throw Error("world/K0 mismatch");
    if(v[ix.original_complete_tenbit_source_probability]!=="1/1024")throw Error("wrong source mass");
    const bits=bitCols.map(h=>Number(v[ix[h]]));if(bits.some(x=>x!==0&&x!==1))throw Error("invalid bit");
    if(bits[0]+bits[1]!==k)throw Error("initial count inconsistent");
    const key=w+"|"+bits.join("");if(unique.has(key))throw Error("duplicate original tenbit source");unique.set(key,true);
    const k1=Number(v[ix.observed_reported_count_K1]),k2=Number(v[ix.observed_reported_count_K2]);
    const y1a=Number(v[ix.observed_reported_agent0_state_t1]),y1b=Number(v[ix.observed_reported_agent1_state_t1]);
    const y2a=Number(v[ix.observed_reported_agent0_state_t2]),y2b=Number(v[ix.observed_reported_agent1_state_t2]);
    if([y1a,y1b,y2a,y2b].some(x=>x!==0&&x!==1)||k1!==y1a+y1b||k2!==y2a+y2b)throw Error("reported count inconsistent");
    const q0=q(w,k*S/2),q1=q(w,k1*S/2);
    if(rationalToScale(v[ix.oracle_public_generator_q_t0])!==q0||rationalToScale(v[ix.oracle_public_generator_q_t1])!==q1)throw Error("q/source inconsistency");
    // Reconstruct both observed transitions from the frozen ten raw bits.
    for(let t=0;t<2;t++){
      const threshold=t===0?q0:q1,off=2+4*t;
      const draw0=2*bits[off]+bits[off+1],draw1=2*bits[off+2]+bits[off+3];
      const expected0=Number(draw0*S<4*threshold),expected1=Number((shared.has(w)?draw0:draw1)*S<4*threshold);
      const observed0=t===0?y1a:y2a,observed1=t===0?y1b:y2b;
      if(expected0!==observed0||expected1!==observed1)throw Error("raw bit transition mismatch");
    }
    const gkey=w+"|"+k;
    if(!groups.has(gkey))groups.set(gkey,[]);
    groups.get(gkey).push({k,k1,y:y2a,j1:Number(y1a===1&&y1b===1),q0,q1,bits:bits.join("")});
  }
  if(unique.size!==9216||groups.size!==27)throw Error("source uniqueness/coverage failed");
  const result=[];
  for(const w of WORLDS)for(let k=0;k<=2;k++){
    const a=groups.get(w+"|"+k),n=a.length,expected=k===1?512:256;
    if(n!==expected)throw Error("conditional cohort count mismatch");
    const hits=a.reduce((s,x)=>s+x.y,0),p0=hits*S/n;
    if(!Number.isInteger(p0))throw Error("prior probability not exactly scaled");
    const q0=q(w,k*S/2),mf=q(w,q0);
    const brier=(f,target)=>frac(a.reduce((s,x)=>{const d=BigInt(f(x)-(target==="y"?x.y:x.j1)*S);return s+d*d},0n),BigInt(n)*BigInt(S)*BigInt(S));
    const b0=brier(()=>p0,"y"),b1=brier(x=>x.q1,"y"),bm=brier(()=>mf,"y");
    const f0num=BigInt(hits)*BigInt(n-hits),f0den=BigInt(n)*BigInt(n);
    if(b0!==frac(f0num,f0den))throw Error("Brier baseline oracle mismatch");
    const correctJoint=shared.has(w)?q0:q0*q0/S,naiveJoint=q0*q0/S;
    const pj=a.reduce((s,x)=>s+x.j1,0)*S/n;
    if(pj!==correctJoint)throw Error("joint observed event vs frozen kernel mismatch");
    const bj=brier(()=>correctJoint,"j1"),bn=brier(()=>naiveJoint,"j1");
    const score0=a.reduce((s,x)=>s+BigInt(p0-x.y*S)**2n,0n);
    const score1=a.reduce((s,x)=>s+BigInt(x.q1-x.y*S)**2n,0n);
    const scorem=a.reduce((s,x)=>s+BigInt(mf-x.y*S)**2n,0n);
    if(score1>score0||score0>scorem)throw Error("proper score monotonicity violated");
    const delta=(x,y)=>frac(x-y,BigInt(n)*BigInt(S)*BigInt(S));
    const jointDelta=frac(BigInt(n)*(BigInt(naiveJoint-correctJoint)**2n),BigInt(n)*BigInt(S)*BigInt(S));
    if(delta(scorem,score0)!==frac(BigInt(mf-p0)**2n,BigInt(S)*BigInt(S)))throw Error("MF excess identity");
    if(delta(score0,score1)!==frac(a.reduce((s,x)=>s+BigInt(x.q1-p0)**2n,0n),BigInt(n)*BigInt(S)*BigInt(S)))throw Error("prefix value identity");
    if(bn===bj&&naiveJoint!==correctJoint)throw Error("joint score expected difference");
    result.push({world:w,initial_count_K0:k,source_rows:n,
      y2_probability_given_K0:frac(p0,S),prefix_mean_field_q0:frac(q0,S),deterministic_MF_y2_probability:frac(mf,S),
      y2_Brier_K0_oracle:b0,y2_Brier_K0_K1_prefix:b1,y2_Brier_deterministic_MF:bm,
      y2_prefix_information_gain:delta(score0,score1),y2_MF_excess_risk:delta(scorem,score0),
      j1_true_joint_probability:frac(pj,S),j1_independent_naive_probability:frac(naiveJoint,S),
      j1_Brier_correct:bj,j1_Brier_naive_independence:bn,
      j1_naive_excess_risk:jointDelta});
  }
  const by=(w,k)=>result.find(r=>r.world===w&&r.initial_count_K0===k);
  if(by(WORLDS[1],1).y2_MF_excess_risk!=="9/1024")throw Error("convex Jensen excess regression");
  if(by(WORLDS[0],1).y2_prefix_information_gain!=="1/8")throw Error("independent neutral prefix regression");
  if(by(WORLDS[7],1).y2_prefix_information_gain!=="1/4")throw Error("shared neutral prefix regression");
  if(by(WORLDS[7],1).j1_naive_excess_risk!=="1/16")throw Error("shared joint regression");
  if(by(WORLDS[8],1).j1_naive_excess_risk!=="1/16")throw Error("sensor observed joint regression");
  for(let k=0;k<=2;k++){const a=by(WORLDS[7],k),b=by(WORLDS[8],k);for(const key of Object.keys(a))if(key!=="world"&&a[key]!==b[key])throw Error("observed alias score mismatch "+key)}
  return {research_id:"R261",stage:"S57",prescore_protocol_path:"protocols/R261_S57_PREFIX_BRIER_AND_SHARED_SHOCK_PRESCORE_FREEZE_2026-10-29.md",
    original_source_git_blob:"7aec6fe1bbce064b985168f72a3b9adbcb6ca521",evidence_class:"E1_ARTIFICIAL",all_original_source_rows:9216,
    nine_worlds:9,conditional_initial_groups:27,forecast_target_y2:"observed_reported_agent0_state_t2",joint_target_j1:"both observed_reported agents state_t1 equal 1",
    oracle_prior_is_not_out_of_sample:true,new_human_E2:0,new_historical_E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN",
    exact_rows:result};
}
if(require.main===module){
  if(process.argv.length<3||process.argv.length>4){console.error("Usage: node script.js original.csv [output.json]");process.exit(2)}
  const result=calculate(fs.readFileSync(process.argv[2],"utf8"));
  const content=JSON.stringify(result,null,2)+"\n";
  if(process.argv[3])fs.writeFileSync(process.argv[3],content,"utf8");
  else process.stdout.write(content);
}
module.exports={calculate};
