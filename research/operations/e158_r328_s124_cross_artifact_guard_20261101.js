"use strict";
// E158: cross-artifact schema, identity and receipt consistency. Node.js standard library.
const fs=require("node:fs"),assert=require("node:assert/strict");
const csvPath=process.argv[2]||"research/validation/R328_S124_ALL_480_STEP_SIZE_STATES.csv";
const jsonPath=process.argv[3]||"research/validation/R328_S124_EXACT_96_STABILITY_WORLDS.json";
const rows=fs.readFileSync(csvPath,"utf8").trim().split("\n").slice(1).map(x=>x.split(","));
const worlds=JSON.parse(fs.readFileSync(jsonPath,"utf8")).worlds;
function audit(rs,ws){
 assert.equal(rs.length,480);assert.equal(ws.length,96);
 const key=r=>r.slice(0,5).join("|"),worldKey=w=>[w.alpha,w.prior,w.target,w.prior_precision,w.sensory_precision].join("|");
 const map=new Map(),wm=new Map();let checks=0;
 for(const r of rs){assert.equal(r.length,13);const k=key(r);if(!map.has(k))map.set(k,[]);map.get(k).push(r);}
 assert.equal(map.size,96);
 for(const w of ws){const k=worldKey(w);assert.ok(!wm.has(k));wm.set(k,w);}
 assert.equal(wm.size,96);
 for(const [k,five] of map){const w=wm.get(k);assert.ok(w);assert.equal(five.length,5);
  assert.equal(five.map(r=>r[5]).join(","),"0,1,2,3,4");
  for(const [idx,val] of [[6,w.estimate_step4],[9,w.energy_step4],[10,w.analytic_optimum],[11,w.lambda]]){assert.equal(five[4][idx],val);checks++;}
  let inc=0;for(let i=1;i<5;i++){const frac=s=>{const [n,d="1"]=s.split("/");return [BigInt(n),BigInt(d)];};const [a,b]=frac(five[i][9]),[c,d]=frac(five[i-1][9]);if(a*d>c*b)inc++;}
  assert.equal(inc,w.strict_increase_steps);assert.equal(inc===0,w.energy_nonincreasing);checks+=2;
 }
 return checks;
}
const checks=audit(rows,worlds);let mutants=0;
for(const type of ["duplicate","drop","energy","summary","counter"]){
 const rr=rows.map(x=>x.slice()),ww=worlds.map(x=>({...x}));
 if(type==="duplicate")rr[1]=rr[0].slice();
 if(type==="drop")rr.pop();
 if(type==="energy")rr[4][9]="999";
 if(type==="summary")ww[0].energy_step4="99";
 if(type==="counter")ww[0].strict_increase_steps=1;
 try{audit(rr,ww);}catch{mutants++;}
}
assert.equal(mutants,5);
console.log(JSON.stringify({rows:rows.length,worlds:worlds.length,checks,mutants_rejected:mutants,scope:"cross-artifact E1 only; no independent closed-form recomputation"}));
