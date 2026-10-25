"use strict";
/* R150 third method. Frozen: protocols/R150_TERMINAL_VS_TRAJECTORY_IDENTIFIABILITY_THIRD_METHOD_FREEZE_2026-10-25.md
   Standalone Node.js, no dependencies, exact rational arithmetic. E1 artificial only. */
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const c=a%b;a=b;b=c;}return a;}
function q(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
function add(a,b){return q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function neg(a){return [-a[0],a[1]];}
function sub(a,b){return add(a,neg(b));}
function mul(a,b){return q(a[0]*b[0],a[1]*b[1]);}
function fmt(a){return a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);}
function history(td,tb,shock){
  let p=q(1000),h=[fmt(p)];
  for(let t=0;t<12;t++){
    const b=t<tb?q(1,5):q(1,20),d=t<td?q(1,5):q(1,20);
    let factor=sub(add(q(1),b),d);
    if(t===4&&shock==="PANDEMIC_YEAR4")factor=sub(factor,q(1,10));
    if(t===4&&shock==="INMIGRATION_YEAR4")factor=add(factor,q(1,10));
    p=mul(p,factor);h.push(fmt(p));
  }
  return h;
}
function groups(entries,field){
  const map=new Map();
  for(const e of entries){const k=field==="terminal"?e.history[12]:e.history.join("|");
    if(!map.has(k))map.set(k,[]);map.get(k).push([e.td,e.tb]);}
  const sizes={};let max=0;
  for(const a of map.values()){sizes[a.length]=(sizes[a.length]||0)+1;max=Math.max(max,a.length);}
  return {distinct:map.size,max_class:max,class_size_histogram:sizes,
    collision_example:[...map].find(([,v])=>v.length>1)?.[1]||[]};
}
function compute(){
 const out={research:"R150",evidence:"E1_ARTIFICIAL",prescore:"protocols/R150_TERMINAL_VS_TRAJECTORY_IDENTIFIABILITY_THIRD_METHOD_FREEZE_2026-10-25.md",scenarios:243,steps:12,results:{}};
 for(const shock of ["NONE","PANDEMIC_YEAR4","INMIGRATION_YEAR4"]){
   const entries=[];for(let td=0;td<9;td++)for(let tb=0;tb<9;tb++)entries.push({td,tb,history:history(td,tb,shock)});
   const terminal=groups(entries,"terminal"),trajectory=groups(entries,"trajectory");
   if(entries.length!==81||trajectory.distinct!==73||trajectory.max_class!==9)throw Error("unexpected trajectory classes");
   if(shock==="NONE"&&terminal.distinct!==17)throw Error("baseline endpoint classes");
   if(shock!=="NONE"&&terminal.distinct!==25)throw Error("shock endpoint classes");
   out.results[shock]={terminal,trajectory,terminal_p0_0:entries[0].history[12],example_td2_tb6:entries.find(e=>e.td===2&&e.tb===6).history[12]};
 }
 const delta=new Set();
 for(let td=0;td<9;td++)for(let tb=0;tb<9;tb++){
   const base=history(td,tb,"NONE")[12],s=history(td,tb,"PANDEMIC_YEAR4")[12];
   // Compare exact ratio by parsing canonical fractions.
   function parse(v){const a=v.split("/");return q(a[0],a[1]||1);}
   const b=parse(base),v=parse(s);delta.add(fmt(q(v[0]*b[1],v[1]*b[0])));
 }
 if(delta.size!==3)throw Error("negative control shock proportionality unexpectedly holds");
 out.mortality_shock_terminal_multipliers=[...delta].sort();
 out.negative_controls={terminal_not_injective:true,full_trajectory_simultaneous_not_injective:true,shock_multiplier_not_constant:true};
 out.checks={exact_scenario_count:243,annual_accounting_updates:2916,expected_distinct_classes_verified:6};
 return out;
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(compute(),null,2));
if(typeof module!=="undefined")module.exports={compute,history};