'use strict';
const fs=require('fs');
function run(csv,baseline,receipt){
 let checks=0;
 const ok=(v,msg)=>{checks++;if(!v)throw Error(msg)};
 const lines=csv.trim().split(/\r?\n/),head=lines.shift().split(',');
 const rows=lines.map((line,i)=>{const cols=line.split(',');ok(cols.length===head.length,'CSV width '+i);return Object.fromEntries(head.map((k,j)=>[k,cols[j]]))});
 ok(rows.length===144,'144 source rows');
 const bm=new Map(baseline.world_results.map(x=>[x.world,x]));
 const rm=new Map(receipt.results.map(x=>[x.world,x]));
 const worldNames=[...new Set(rows.map(x=>x.world))].sort();
 ok(worldNames.length===9,'9 worlds');
 const key=x=>[x.oracle_original_X,x.oracle_original_B,x.oracle_original_C,x.oracle_original_U].join('');
 const abc=x=>x.observed_A+x.observed_B+x.observed_C;
 const obs=x=>[x.observed_A,x.observed_B,x.observed_C,x.observed_case_selected,x.observed_selected_Y].join('');
 function fraction(a,b){if(!b)return null;const gcd=(x,y)=>y?gcd(y,x%y):Math.abs(x);let d=gcd(a,b);return b/d===1?String(a/d):a/d+'/'+b/d}
 function stats(rr){
  const table=Object.fromEntries(Array.from({length:8},(_,i)=>[i.toString(2).padStart(3,'0'),{p:0,n:0}]));
  let selected=0,den=0,num=0;const joint={};
  for(const x of rr){
   const k=obs(x);joint[k]=(joint[k]||0)+1;
   if(x.observed_case_selected==='0')continue;
   selected++;
   const t=table[abc(x)];if(x.observed_selected_Y==='1')t.p++;else t.n++;
   if(x.observed_A==='1'){den++;if(x.observed_selected_Y==='1')num++}
  }
  const v=Object.values(table);
  return {selected,positive:v.filter(x=>x.p>0&&x.n===0).length,negative:v.filter(x=>x.n>0&&x.p===0).length,contradictory:v.filter(x=>x.p>0&&x.n>0).length,remainder:v.filter(x=>x.p+x.n===0).length,sufficiency_A:fraction(num,den),table,joint};
 }
 function compareStats(a,b,label){for(const k of ['selected','positive','negative','contradictory','remainder','sufficiency_A'])ok(a[k]===b[k],label+' '+k)}
 function compareJoint(a,b,label){const keys=[...new Set([...Object.keys(a),...Object.keys(b)])];for(const k of keys)ok((a[k]||0)===(b[k]||0),label+' joint '+k)}
 let single=0,configs=0,spurious=0,changed=0,aliasChecks=0,missing=0;
 const singles=new Map();
 for(const name of worldNames){
  const w=rows.filter(x=>x.world===name),b=bm.get(name),r=rm.get(name);
  ok(!!b&&!!r,'world present '+name);ok(w.length===16,'world 16 '+name);
  ok(new Set(w.map(key)).size===16,'source keys '+name);
  let effect=0;
  for(const x of w){
   ok(x.original_source_probability==='1/16','source weight '+name);
   ok(['0','1'].includes(x.observed_case_selected),'selection '+name);
   ok(x.observed_selected_Y===(x.observed_case_selected==='1'?x.oracle_actual_Y:'-1'),'observed missingness '+name);
   ok(x.oracle_actual_Y===x['oracle_doA'+x.observed_A+'_Y'],'factual consistency '+name);
   effect+=Number(x.oracle_doA1_Y)-Number(x.oracle_doA0_Y);
   if(x.observed_case_selected==='0')missing++;
  }
  ok(fraction(effect,16)===b.oracle_doA1_minus_doA0_population_effect,'frozen oracle '+name);
  ok(r.oracle_doA_effect===b.oracle_doA1_minus_doA0_population_effect,'receipt oracle '+name);
  const original=stats(w);compareStats(original,r.original,'original '+name);
  for(const t of b.complete_truth_table){ok(original.table[t.abc].p===t.positive_original_atoms,'baseline p '+name);ok(original.table[t.abc].n===t.negative_original_atoms,'baseline n '+name)}
  ok(original.sufficiency_A===b.observational_sufficiency_A,'baseline suff '+name);
  ok(r.single_source.length===16,'16 deletion cases '+name);
  const recByKey=new Map(r.single_source.map(x=>[x.source_key,x]));
  const current=new Map();
  for(const x of w){
   const k=key(x),z=stats(w.filter(y=>y!==x)),e=recByKey.get(k);
   ok(!!e,'single receipt '+name+' '+k);
   const fresh=Object.keys(z.table).filter(k=>z.table[k].p>0&&z.table[k].n===0&&original.table[k].p>0&&original.table[k].n>0).sort();
   ok(e.removed_abc===abc(x),'removed abc '+name+' '+k);
   ok(e.removed_y===x.observed_selected_Y,'removed y '+name+' '+k);
   ok(e.selected===(x.observed_case_selected==='1'),'selected flag '+name+' '+k);
   ok(e.selected_after===z.selected,'selected count '+name+' '+k);
   for(const field of ['positive','negative','contradictory','remainder','sufficiency_A'])ok(e[field]===z[field],field+' '+name+' '+k);
   ok(JSON.stringify([...e.new_perfect_from_contradictory].sort())===JSON.stringify(fresh),'spurious '+name+' '+k);
   compareJoint(z.joint,e.observed_joint,name+' '+k);
   spurious+=fresh.length;changed+=(z.sufficiency_A!==original.sufficiency_A)?1:0;single++;current.set(k,z.joint);
  }
  singles.set(name,current);
  const supported=Object.keys(original.table).filter(k=>original.table[k].p+original.table[k].n>0);
  ok(r.drop_supported_config.length===supported.length,'config count '+name);
  const configMap=new Map(r.drop_supported_config.map(x=>[x.removed_abc,x]));
  for(const k of supported){
   const z=stats(w.filter(x=>x.observed_case_selected==='0'||abc(x)!==k)),e=configMap.get(k);
   ok(!!e,'config '+name+' '+k);
   ok(e.removed_selected===original.table[k].p+original.table[k].n,'config removed count '+name+' '+k);
   ok(e.selected_after===z.selected,'config selected '+name+' '+k);
   for(const field of ['positive','negative','contradictory','remainder','sufficiency_A'])ok(e[field]===z[field],'config '+field+' '+name+' '+k);
   configs++;
  }
 }
 for(const [left,right] of [['ALIAS_A_CAUSAL','ALIAS_U_CONFOUNDED'],['LIMITED_A_AND_B','LIMITED_UNSEEN_BRANCH']]){
  const a=singles.get(left),b=singles.get(right);
  for(const [k,joint] of a){compareJoint(joint,b.get(k),left+' '+right+' '+k);aliasChecks++}
 }
 for(const [field,expected] of [['source_rows',144],['worlds',9],['single_source_perturbations',single],['configuration_perturbations',configs],['new_perfect_positive_config_events',spurious],['sufficiency_A_changed_single_source',changed],['alias_pair_deletion_checks',aliasChecks]])ok(receipt[field]===expected,'receipt total '+field);
 return {checks,failures:0,rows:rows.length,worlds:worldNames.length,missing,source_deletions:single,configuration_deletions:configs,spurious_perfect:spurious,sufficiency_changes:changed,alias_checks:aliasChecks};
}
if(require.main===module){
 const csv=fs.readFileSync('research/R239/R239_ALL_144_ORIGINAL_CONFIGURATION_CAUSAL_SOURCES.csv','utf8');
 const base=JSON.parse(fs.readFileSync('research/R239/R239_EXACT_RESULTS.json','utf8'));
 const receipt=JSON.parse(fs.readFileSync('research/validation/R239_S35_SINGLE_SOURCE_AND_CONFIG_DELETION_EXACT_RECEIPT_2026-10-28.json','utf8'));
 console.log(JSON.stringify(run(csv,base,receipt),null,2));
}
module.exports={run};
