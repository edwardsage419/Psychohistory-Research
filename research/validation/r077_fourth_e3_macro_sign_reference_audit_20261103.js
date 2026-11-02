'use strict';
// Read-only audit of the exact archived R077 E3 macro receipt.
// Conditional sign tails are exploratory; session independence is unverified.
const PIN='13946754afc06e529f2d3a2072a7bae297453fa9';
const NAMES=['M0_TREATMENT_PREVALENCE','M1_OWN_LAST','M2_OPPONENT_LAST','M3_JOINT_LAST','M4_JOINT_TWO_LAGS','M5_TFT_NOISY','M6_WSLS_NOISY'];
const PAIRS=['M1_OWN_LAST_VS_M0_TREATMENT_PREVALENCE','M2_OPPONENT_LAST_VS_M0_TREATMENT_PREVALENCE','M3_JOINT_LAST_VS_M1_OWN_LAST','M4_JOINT_TWO_LAGS_VS_M3_JOINT_LAST','M5_TFT_NOISY_VS_M0_TREATMENT_PREVALENCE','M6_WSLS_NOISY_VS_M0_TREATMENT_PREVALENCE'];
function need(ok,msg){if(!ok)throw Error(msg);}
function keys(obj,arr,label){need(obj&&typeof obj==='object'&&Object.keys(obj).length===arr.length&&arr.every(k=>Object.hasOwn(obj,k)),label+' coverage');}
function comb(n,k){let a=1;for(let i=1;i<=k;i++)a=a*(n-i+1)/i;return Math.round(a);}
function tail(b,w){const n=b+w;need(Number.isInteger(n)&&n>0&&n<=15,'sign universe');let v=0;for(let i=0;i<=Math.min(b,w);i++)v+=comb(n,i);return Math.min(1,2*v/2**n);}
function audit(d){
 const r=d.results;need(r&&r.original_session_count===15&&r.scored_t3_human_events===1040,'source universe');
 need(d.source_universe&&d.source_universe.true_independent_original_sessions===15&&d.source_universe.treatment_session_counts['0']===7&&d.source_universe.treatment_session_counts['1']===8,'session strata');
 keys(r.models,NAMES,'model');keys(r.paired_differences,PAIRS,'pair');
 let count=0,max=0;
 function eq(x,y,why){need(typeof x==='number'&&typeof y==='number'&&Number.isFinite(x)&&Number.isFinite(y),why+' nonfinite');let e=Math.abs(x-y);max=Math.max(max,e);count++;need(e<=1e-12,why+' mismatch');}
 for(const name of NAMES){let m=r.models[name],t=m.per_treatment_original_session_equal;need(t&&t['0'].original_sessions===7&&t['1'].original_sessions===8,name+' strata');
  for(const metric of ['Brier','log_loss'])eq(m['all_original_sessions_equal_'+metric],(7*t['0'][metric]+8*t['1'][metric])/15,name+' '+metric);
 }
 const signs=[];
 for(const name of PAIRS){let [left,right]=name.split('_VS_'),p=r.paired_differences[name],a=r.models[left],b=r.models[right];
  need(p.sessions===15,name+' n');
  eq(p.Brier_delta_all_original_sessions_equal,a.all_original_sessions_equal_Brier-b.all_original_sessions_equal_Brier,name+' global');
  eq(p.sessions_better+p.sessions_equal+p.sessions_worse,15,name+' signs');
  let n=0,better=0,worse=0,equal=0;
  for(const t of ['0','1']){let row=p.per_treatment[t],nn=t==='0'?7:8;need(row&&row.sessions===nn,name+' group n');
   eq(row.Brier_delta,a.per_treatment_original_session_equal[t].Brier-b.per_treatment_original_session_equal[t].Brier,name+' group delta');
   eq(row.better+row.worse+row.equal,nn,name+' group signs');n+=row.sessions;better+=row.better;worse+=row.worse;equal+=row.equal;
  }
  eq(n,p.sessions,name+' n2');eq(better,p.sessions_better,name+' better');eq(worse,p.sessions_worse,name+' worse');eq(equal,p.sessions_equal,name+' equal');
  eq(p.Brier_delta_all_original_sessions_equal,(7*p.per_treatment['0'].Brier_delta+8*p.per_treatment['1'].Brier_delta)/15,name+' weighted');
  signs.push({contrast:name,better,worse,equal,p_two_sided_reference:tail(better,worse)});
 }
 signs.sort((a,b)=>a.p_two_sided_reference-b.p_two_sided_reference);
 let previous=0;for(let i=0;i<signs.length;i++){previous=Math.max(previous,Math.min(1,signs[i].p_two_sided_reference*(signs.length-i)));signs[i].holm_six_reference=previous;}
 need(count===80,'comparison count');
 return {status:'PASS',evidence:'INTERNAL_NONBLIND_ARCHIVED_E3_MACRO_ONLY',numeric_checks:count,max_absolute_difference:max,signs,independent_session_assumption_verified:false,original_individual_scores_recomputed:false,new_human_E3_scores:0};
}
function selftest(d){let good=audit(d);let mutants=[
 x=>x.results.models.M3_JOINT_LAST.all_original_sessions_equal_Brier+=0.01,
 x=>x.results.models.M3_JOINT_LAST.per_treatment_original_session_equal['0'].Brier+=0.01,
 x=>x.results.paired_differences.M3_JOINT_LAST_VS_M1_OWN_LAST.Brier_delta_all_original_sessions_equal+=0.01,
 x=>x.results.paired_differences.M3_JOINT_LAST_VS_M1_OWN_LAST.sessions_better=15,
 x=>x.results.models.M3_JOINT_LAST.per_treatment_original_session_equal['1'].original_sessions=9,
 x=>delete x.results.models.M4_JOINT_TWO_LAGS,
 x=>delete x.results.paired_differences.M2_OPPONENT_LAST_VS_M0_TREATMENT_PREVALENCE
 ];for(let i=0;i<mutants.length;i++){let m=JSON.parse(JSON.stringify(d));mutants[i](m);let rejected=false;try{audit(m);}catch(_){rejected=true;}need(rejected,'mutation '+i+' falsely accepted');}
 return {...good,mutations_rejected:mutants.length};
}
function main(){const fs=require('node:fs'),crypto=require('node:crypto');let arg=process.argv[2];need(arg&&process.argv.length===3,'supply R077 JSON path or --selftest');
 let path=arg==='--selftest'?'research/R077/R077_FOURTH_INDEPENDENT_HUMAN_SOURCE_ONLY_E3_RESULTS.json':arg;
 let raw=fs.readFileSync(path),sha=crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex');
 need(sha===PIN,'archived Git blob mismatch');let d=JSON.parse(raw.toString('utf8'));
 console.log(JSON.stringify(arg==='--selftest'?selftest(d):audit(d),null,2));
}
if(typeof require==='function'&&typeof module!=='undefined'&&require.main===module){try{main();}catch(e){console.error('FAIL: '+e.message);process.exitCode=1;}}
module.exports={audit,selftest,tail};
