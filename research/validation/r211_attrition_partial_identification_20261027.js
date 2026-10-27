
"use strict";
const TYPES=[[0,0],[0,1],[1,0],[1,1]];
const PAIRS=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const POLICIES=["FULL","FIXED_02","ARM_FAVORABLE"];
function schedule(k){return [0,1,2,3].map(i=>TYPES[Math.floor(k/Math.pow(4,3-i))%4]);}
function ateQ(s){return s.reduce((a,v)=>a+v[1]-v[0],0);}
function fmtHalf(q){return q%2===0?String(q/2):String(q)+"/2";}
function run(){
 const lines=["source_schedule_index,source_four_types,treated_pair,assignment_z,response_policy,response_mask,visible_outcomes,missing_count,compatible_count,ate_lower_quarters,ate_upper_quarters,width_quarters,true_ate_quarters,covered,cc_diff_halves"];
 const sum={};for(const p of POLICIES)sum[p]={rows:0,missing_hist:{},width_quarters_sum:0,covered:0,cc_defined:0,cc_undefined:0,cc_diff_halves_sum:0,zero_ate_cc_positive:0,cc_equals_one:0,example_zero_ate_positive:null,worlds_cc_mean_differs_from_true:0};
 let exact_checks=0, records=0;
 for(let k=0;k<256;k++){
  const s=schedule(k),trueQ=ateQ(s);
  for(const p of POLICIES){
   let worldCcSum=0,worldCcCount=0;
   for(const pair of PAIRS){
    const z=[0,1,2,3].map(i=>pair.includes(i)?1:0),y=[0,1,2,3].map(i=>s[i][z[i]]);
    const r=[0,1,2,3].map(i=>p==="FULL"?1:p==="FIXED_02"?(i===0||i===2?1:0):(z[i]===1?y[i]:1-y[i]));
    const m=r.filter(x=>!x).length, visible=y.map((v,i)=>r[i]?String(v):"?").join("|");
    let lo=100,hi=-100,count=0;
    for(let j=0;j<256;j++){
      const t=schedule(j);
      if([0,1,2,3].every(i=>!r[i]||t[i][z[i]]===y[i])){const q=ateQ(t);if(q<lo)lo=q;if(q>hi)hi=q;count++;}
    }
    if(count!==Math.pow(2,4+m)||hi-lo!==4+m||lo>trueQ||hi<trueQ)throw Error("enumeration invariant failure "+k+" "+p+" "+pair);
    exact_checks+=4;
    const tr=[0,1,2,3].filter(i=>r[i]&&z[i]),co=[0,1,2,3].filter(i=>r[i]&&!z[i]);
    let cc="";
    if(tr.length&&co.length){
      const trsum=tr.reduce((a,i)=>a+y[i],0),cosum=co.reduce((a,i)=>a+y[i],0);
      const h=2*trsum/tr.length-2*cosum/co.length;
      if(!Number.isInteger(h))throw Error("half-integer CC invariant");
      cc=String(h);worldCcSum+=h;worldCcCount++;
    }
    const row=[k,s.map(t=>t.join("")).join("|"),pair.join("|"),z.join("|"),p,r.join("|"),visible,m,count,lo,hi,hi-lo,trueQ,lo<=trueQ&&trueQ<=hi?1:0,cc];
    lines.push(row.join(","));records++;
    const a=sum[p];a.rows++;a.missing_hist[m]=(a.missing_hist[m]||0)+1;a.width_quarters_sum+=hi-lo;a.covered++;
    if(cc===""){a.cc_undefined++;}else{
      const h=Number(cc);a.cc_defined++;a.cc_diff_halves_sum+=h;
      if(trueQ===0&&h>0){a.zero_ate_cc_positive++;if(a.example_zero_ate_positive===null)a.example_zero_ate_positive={schedule_index:k,schedule:s.map(t=>t.join("")).join("|"),treated:pair.join("|"),response_mask:r.join("|"),observed:visible,cc_diff_halves:h,true_ate_quarters:trueQ};}
      if(h===2)a.cc_equals_one++;
    }
   }
   if(worldCcCount&&worldCcSum*2!==trueQ*worldCcCount)sum[p].worlds_cc_mean_differs_from_true++;
  }
 }
 if(records!==4608||sum.FULL.width_quarters_sum!==1536*4||sum.FIXED_02.width_quarters_sum!==1536*6)throw Error("total invariant");
 if(sum.ARM_FAVORABLE.zero_ate_cc_positive<=0||sum.ARM_FAVORABLE.cc_equals_one!==sum.ARM_FAVORABLE.cc_defined)throw Error("selection diagnostic");
 const receipt={research:"R211",method:"outcome_dependent_attrition_partial_identification_third_method",date:"2026-10-27",evidence:"E1_ARTIFICIAL",source_schedules:256,randomizations_per_schedule:6,response_policies:POLICIES,total_source_policy_rows:records,enumeration_invariant_checks:exact_checks,policies:sum,information_permission:"Z,response_mask,observed Y only; true schedule audit-only; selection policy unknown to bound estimator",protocol:"protocols/R211_OUTCOME_DEPENDENT_ATTRITION_THIRD_METHOD_PRESCORE_FREEZE_2026-10-27.md",new_E2:0,new_E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN"};
 return {csv:lines.join("\n")+"\n",receipt};
}

if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path"),out=process.argv[2]||".";
 fs.mkdirSync(out,{recursive:true});
 const x=run();
 fs.writeFileSync(path.join(out,"R211_ATTRITION_4608_SOURCE_POLICY_ROWS_2026-10-27.csv"),x.csv);
 fs.writeFileSync(path.join(out,"R211_ATTRITION_THIRD_METHOD_EXACT_RECEIPT_2026-10-27.json"),JSON.stringify(x.receipt,null,2)+"\n");
 console.log(JSON.stringify({rows:x.receipt.total_source_policy_rows,checks:x.receipt.enumeration_invariant_checks}));
}
if(typeof module!=="undefined")module.exports={run};
