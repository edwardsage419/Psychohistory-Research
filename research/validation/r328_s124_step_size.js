"use strict";
/* R328 S124 exact finite E1 step-size stability, standard Node.js only.
 * Usage: node research/validation/r328_s124_step_size.js --emit /tmp/r328_s124
 *        node research/validation/r328_s124_step_size.js --check /tmp/r328_s124
 */
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;}
function Q(a,b=1n){a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return {n:a/g,d:b/g};}
const plus=(a,b)=>Q(a.n*b.d+b.n*a.d,a.d*b.d);
const neg=a=>Q(-a.n,a.d);
const minus=(a,b)=>plus(a,neg(b));
const times=(a,b)=>Q(a.n*b.n,a.d*b.d);
const divide=(a,b)=>Q(a.n*b.d,a.d*b.n);
const square=a=>times(a,a);
const str=a=>a.d===1n?String(a.n):String(a.n)+"/"+String(a.d);
const eq=(a,b)=>a.n===b.n&&a.d===b.d;
const cmp=(a,b)=>{const v=a.n*b.d-b.n*a.d;return v<0n?-1:v>0n?1:0;};
const abs=a=>Q(a.n<0n?-a.n:a.n,a.d);
const ZERO=Q(0),ONE=Q(1),TWO=Q(2);
const FIELDS=["alpha","prior","target","prior_precision","sensory_precision","step","estimate","sensory_error","prior_error","energy","analytic_optimum","lambda","energy_gap"];
function energy(x,m,y,r,p){return divide(plus(times(r,square(minus(x,m))),times(p,square(minus(y,x)))),TWO);}
function generate(){
  const rows=[],worlds=[];
  for(const alpha of [Q(1,4),Q(1,2),Q(3,4),ONE])
  for(const m of [ZERO,ONE])
  for(const y of [ZERO,ONE,TWO])
  for(const r of [ONE,TWO])
  for(const p of [ONE,TWO]){
    const optimum=divide(plus(times(r,m),times(p,y)),plus(r,p));
    const lambda=minus(ONE,times(alpha,plus(r,p)));
    const flat=eq(m,y);
    const category=flat?"FLAT_ZERO_RESIDUAL":cmp(abs(lambda),ONE)<0?"CONTRACTIVE":cmp(abs(lambda),ONE)===0?"NEUTRAL":"EXPANSIVE";
    let x=m,prev=null,nonincreasing=true,increasing=0;
    const optimumEnergy=energy(optimum,m,y,r,p);
    for(let t=0;t<=4;t++){
      const e=energy(x,m,y,r,p),gap=minus(e,optimumEnergy);
      if(cmp(gap,ZERO)<0)throw Error("negative energy gap");
      if(prev!==null){if(cmp(e,prev)>0){nonincreasing=false;increasing++;}}
      rows.push([str(alpha),str(m),str(y),str(r),str(p),String(t),str(x),str(minus(y,x)),str(minus(m,x)),str(e),str(optimum),str(lambda),str(gap)]);
      prev=e;
      if(t<4)x=plus(x,times(alpha,plus(times(p,minus(y,x)),times(r,minus(m,x)))));
    }
    worlds.push({alpha:str(alpha),prior:str(m),target:str(y),prior_precision:str(r),sensory_precision:str(p),lambda:str(lambda),analytic_optimum:str(optimum),estimate_step4:str(x),energy_step4:str(prev),category,energy_nonincreasing:nonincreasing,strict_increase_steps:increasing});
  }
  const csv=FIELDS.join(",")+"\n"+rows.map(r=>r.join(",")).join("\n")+"\n";
  const result={model:"R328_S124_FINITE_STEP_SIZE_STABILITY_E1",source_row_count:rows.length,world_count:worlds.length,worlds};
  const json=JSON.stringify(result,null,2)+"\n";
  return {rows,worlds,csv,json};
}
function verify(g){
  if(g.rows.length!==480||g.worlds.length!==96)throw Error("coverage");
  const seen=new Set();
  for(const r of g.rows){const k=r.slice(0,6).join("|");if(seen.has(k))throw Error("duplicate row");seen.add(k);}
  for(const a of ["1/4","1/2","3/4","1"])if(g.worlds.filter(w=>w.alpha===a).length!==24)throw Error("alpha coverage");
  const categories={};for(const w of g.worlds)categories[w.category]=(categories[w.category]||0)+1;
  const witnesses=g.worlds.filter(w=>w.prior==="0"&&w.target==="2"&&w.prior_precision==="2"&&w.sensory_precision==="2");
  if(witnesses.length!==4)throw Error("witness coverage");
  const get=a=>witnesses.find(w=>w.alpha===a);
  if(get("1/4").estimate_step4!=="1"||get("1/2").estimate_step4!=="0"||get("1/2").category!=="NEUTRAL"||get("3/4").category!=="EXPANSIVE")throw Error("witness failure");
  return categories;
}
if(typeof module!=="undefined"&&typeof require==="function"&&require.main===module){
  const fs=require("node:fs"),path=require("node:path");
  const mode=process.argv[2],dir=process.argv[3];if(!["--emit","--check"].includes(mode)||!dir)throw Error("usage: --emit|--check DIR");
  const g=generate();const categories=verify(g);
  const csvPath=path.join(dir,"R328_S124_ALL_480_STEP_SIZE_STATES.csv"),jsonPath=path.join(dir,"R328_S124_EXACT_96_STABILITY_WORLDS.json");
  if(mode==="--emit"){fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(csvPath,g.csv);fs.writeFileSync(jsonPath,g.json);}
  else if(fs.readFileSync(csvPath,"utf8")!==g.csv||fs.readFileSync(jsonPath,"utf8")!==g.json)throw Error("archived receipt mismatch");
  console.log(JSON.stringify({status:"PASS_INTERNAL_E1",rows:g.rows.length,worlds:g.worlds.length,categories}));
}
