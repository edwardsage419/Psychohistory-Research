'use strict';
const fs=require('fs');
const SRC='research/R239/R239_ALL_144_ORIGINAL_CONFIGURATION_CAUSAL_SOURCES.csv';
const BASE='research/R239/R239_EXACT_RESULTS.json';
function gcd(a,b){while(b)[a,b]=[b,a%b];return a||1}
function f(a,b){if(!b)return null;const d=gcd(a,b);return b===d?String(a/d):a/d+'/'+b/d}
function run(csv,baseline){
 const lines=csv.trim().split(/\r?\n/),h=lines.shift().split(',');
 const rows=lines.map((line,i)=>{const v=line.split(',');if(v.length!==h.length)throw Error('CSV width '+i);return Object.fromEntries(h.map((k,j)=>[k,v[j]]))});
 if(rows.length!==144)throw Error('Expected 144 source rows');
 const worlds={};for(const r of rows)(worlds[r.world]??=[]).push(r);
 const bm=Object.fromEntries(baseline.world_results.map(w=>[w.world,w]));
 const abc=r=>r.observed_A+r.observed_B+r.observed_C;
 const key=r=>[r.oracle_original_X,r.oracle_original_B,r.oracle_original_C,r.oracle_original_U].join('');
 const obs=r=>[r.observed_A,r.observed_B,r.observed_C,r.observed_case_selected,r.observed_selected_Y].join('');
 function calc(rr){
  const t=Object.fromEntries(Array.from({length:8},(_,i)=>[i.toString(2).padStart(3,'0'),{p:0,n:0}]));
  let selected=0,a1=0,a1y=0;const joint={};
  for(const r of rr){joint[obs(r)]=(joint[obs(r)]||0)+1;
   if(r.observed_case_selected!=='1')continue;
   selected++;const k=abc(r),y=r.observed_selected_Y;
   if(y==='1')t[k].p++;else if(y==='0')t[k].n++;else throw Error('selected missing');
   if(r.observed_A==='1'){a1++;if(y==='1')a1y++}
  }
  let positive=0,negative=0,contradictory=0,remainder=0;
  for(const v of Object.values(t)){if(!v.p&&!v.n)remainder++;else if(v.p&&v.n)contradictory++;else if(v.p)positive++;else negative++}
  return {selected,positive,negative,contradictory,remainder,sufficiency_A:f(a1y,a1),table:t,joint};
 }
 const result=[];
 for(const name of Object.keys(worlds).sort()){
  const w=worlds[name],b=bm[name];if(!b||w.length!==16)throw Error('bad world '+name);
  const orig=calc(w);
  for(const t of b.complete_truth_table){const a=orig.table[t.abc];if(a.p!==t.positive_original_atoms||a.n!==t.negative_original_atoms)throw Error('baseline table')}
  if(orig.sufficiency_A!==b.observational_sufficiency_A)throw Error('baseline suff');
  const single=w.map(r=>{const z=calc(w.filter(x=>x!==r));
   const fresh=Object.keys(z.table).filter(k=>z.table[k].p>0&&z.table[k].n===0&&orig.table[k].p>0&&orig.table[k].n>0);
   return {source_key:key(r),selected:r.observed_case_selected==='1',removed_abc:abc(r),removed_y:r.observed_selected_Y,
    selected_after:z.selected,positive:z.positive,negative:z.negative,contradictory:z.contradictory,remainder:z.remainder,
    sufficiency_A:z.sufficiency_A,new_perfect_from_contradictory:fresh,observed_joint:z.joint}
  });
  const configs=Object.keys(orig.table).sort().filter(k=>orig.table[k].p+orig.table[k].n>0).map(k=>{
   const z=calc(w.filter(r=>r.observed_case_selected!=='1'||abc(r)!==k));
   return {removed_abc:k,removed_selected:orig.table[k].p+orig.table[k].n,selected_after:z.selected,
    positive:z.positive,negative:z.negative,contradictory:z.contradictory,remainder:z.remainder,sufficiency_A:z.sufficiency_A}
  });
  result.push({world:name,original:{selected:orig.selected,positive:orig.positive,negative:orig.negative,contradictory:orig.contradictory,remainder:orig.remainder,sufficiency_A:orig.sufficiency_A},
   single_source:single,drop_supported_config:configs,oracle_doA_effect:b.oracle_doA1_minus_doA0_population_effect});
 }
 for(const [a,b] of [['ALIAS_A_CAUSAL','ALIAS_U_CONFOUNDED'],['LIMITED_A_AND_B','LIMITED_UNSEEN_BRANCH']]){
  const x=result.find(w=>w.world===a),y=result.find(w=>w.world===b);
  for(let i=0;i<16;i++)if(x.single_source[i].source_key!==y.single_source[i].source_key||JSON.stringify(x.single_source[i].observed_joint)!==JSON.stringify(y.single_source[i].observed_joint))throw Error('alias failure')
 }
 return {research_id:'R239_S35',evidence:'E1_ARTIFICIAL_ONLY',source_rows:rows.length,worlds:result.length,
  single_source_perturbations:result.reduce((n,w)=>n+w.single_source.length,0),
  configuration_perturbations:result.reduce((n,w)=>n+w.drop_supported_config.length,0),
  new_perfect_positive_config_events:result.reduce((n,w)=>n+w.single_source.reduce((m,x)=>m+x.new_perfect_from_contradictory.length,0),0),
  sufficiency_A_changed_single_source:result.reduce((n,w)=>n+w.single_source.filter(x=>x.sufficiency_A!==w.original.sufficiency_A).length,0),
  alias_pair_deletion_checks:32,results:result};
}
if(require.main===module)process.stdout.write(JSON.stringify(run(fs.readFileSync(SRC,'utf8'),JSON.parse(fs.readFileSync(BASE,'utf8'))),null,2)+'\n');
module.exports={run};
