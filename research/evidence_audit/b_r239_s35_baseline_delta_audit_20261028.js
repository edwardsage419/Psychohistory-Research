'use strict';
// B R239 S35: independent count-updating audit against frozen eight-cell truth tables.
// Node.js standard library only, repository root: node research/evidence_audit/b_r239_s35_baseline_delta_audit_20261028.js
const fs=require('fs');
function gcd(a,b){while(b)[a,b]=[b,a%b];return a||1}
function fraction(a,b){if(!b)return null;const d=gcd(a,b);return b===d?String(a/d):a/d+'/'+b/d}
function count(s){const p=s.split('/').map(Number);return 16*p[0]/(p[1]||1)}
function audit(csv,baseline,receipt){
 const lines=csv.trim().split(/\r?\n/),head=lines.shift().split(',');
 const rows=lines.map(line=>Object.fromEntries(line.split(',').map((v,i)=>[head[i],v])));
 const bm=Object.fromEntries(baseline.world_results.map(w=>[w.world,w]));
 let checks=0;
 function ck(a,b,label){checks++;if(JSON.stringify(a)!==JSON.stringify(b))throw Error('B R239 S35 mismatch '+label+': '+JSON.stringify(a)+' vs '+JSON.stringify(b))}
 function summary(t){
  let positive=0,negative=0,contradictory=0,remainder=0,yes=0,den=0,selected=0;
  for(const [k,v] of Object.entries(t)){
   const p=v.p,n=v.n;selected+=p+n;
   if(p===0&&n===0)remainder++;else if(p&&n)contradictory++;else if(p)positive++;else negative++;
   if(k[0]==='1'){yes+=p;den+=p+n}
  }
  return {selected,positive,negative,contradictory,remainder,sufficiency_A:fraction(yes,den)}
 }
 for(const w of receipt.results){
  const b=bm[w.world],rs=rows.filter(x=>x.world===w.world);
  ck(rs.length,16,'world rows');
  const t0=Object.fromEntries(b.complete_truth_table.map(x=>[x.abc,{p:x.positive_original_atoms,n:x.negative_original_atoms}]));
  ck(summary(t0),w.original,'original '+w.world);
  const baseJoint=Object.fromEntries(Object.entries(b.full_observed_joint_with_explicit_selection_missingness).map(([k,v])=>[k,count(v)]));
  for(const x of w.single_source){
   const row=rs.find(r=>[r.oracle_original_X,r.oracle_original_B,r.oracle_original_C,r.oracle_original_U].join('')===x.source_key);
   if(!row)throw Error('source key absent');
   const t=Object.fromEntries(Object.entries(t0).map(([k,v])=>[k,{...v}]));
   if(row.observed_case_selected==='1'){
    const k=row.observed_A+row.observed_B+row.observed_C;
    if(row.observed_selected_Y==='1')t[k].p--;else t[k].n--;
   }
   const s=summary(t);
   for(const k of Object.keys(s))ck(s[k],k==='selected'?x.selected_after:x[k],w.world+' source '+x.source_key+' '+k);
   const fresh=Object.keys(t).filter(k=>t[k].p>0&&t[k].n===0&&t0[k].p>0&&t0[k].n>0);
   ck(fresh,x.new_perfect_from_contradictory,'new perfect');
   const j={...baseJoint},obs=[row.observed_A,row.observed_B,row.observed_C,row.observed_case_selected,row.observed_selected_Y].join('');
   j[obs]--;if(j[obs]===0)delete j[obs];
   ck(Object.entries(j).sort(),Object.entries(x.observed_joint).sort(),'joint');
  }
  for(const x of w.drop_supported_config){
   const t=Object.fromEntries(Object.entries(t0).map(([k,v])=>[k,{...v}]));
   const removed=t[x.removed_abc].p+t[x.removed_abc].n;
   ck(removed,x.removed_selected,'removed support');t[x.removed_abc]={p:0,n:0};
   const s=summary(t);
   for(const k of Object.keys(s))ck(s[k],k==='selected'?x.selected_after:x[k],w.world+' config '+x.removed_abc+' '+k);
  }
  ck(w.oracle_doA_effect,b.oracle_doA1_minus_doA0_population_effect,'oracle frozen');
 }
 ck(receipt.source_rows,144,'rows');ck(receipt.worlds,9,'worlds');
 ck(receipt.single_source_perturbations,144,'single');ck(receipt.configuration_perturbations,68,'configs');
 ck(receipt.new_perfect_positive_config_events,8,'new perfect');ck(receipt.sufficiency_A_changed_single_source,40,'suff shifts');
 ck(receipt.alias_pair_deletion_checks,32,'alias checks');
 return {status:'PASS',checks,worlds:receipt.results.length,single_source:144,configuration:68};
}
if(require.main===module){
 const c=fs.readFileSync('research/R239/R239_ALL_144_ORIGINAL_CONFIGURATION_CAUSAL_SOURCES.csv','utf8');
 const b=JSON.parse(fs.readFileSync('research/R239/R239_EXACT_RESULTS.json','utf8'));
 const r=JSON.parse(fs.readFileSync('research/validation/R239_S35_SINGLE_SOURCE_AND_CONFIG_DELETION_EXACT_RECEIPT_2026-10-28.json','utf8'));
 const ok=audit(c,b,r);
 const bad=JSON.parse(JSON.stringify(r));bad.results[0].single_source[0].selected_after+=1;
 let rejected=false;try{audit(c,b,bad)}catch(e){rejected=true}
 if(!rejected)throw Error('mutation test failed');
 console.log(JSON.stringify({...ok,mutation_rejected:true}));
}
module.exports={audit};
