"use strict";
// R247 S43 R route. Exact rational arithmetic on frozen observed joint PMFs.
const fs = typeof require==="function" ? require("fs") : null;
const PREFIXES=["F0","F1","F2","F12"];
function gcd(a,b){while(b){const t=a%b;a=b;b=t;}return a<0n?-a:a;}
function Q(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
function add(a,b){return Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function mul(a,b){return Q(a[0]*b[0],a[1]*b[1]);}
function sub(a,b){return add(a,[-b[0],b[1]]);}
function fmt(a){return a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);}
function parse(s){const a=String(s).split("/").map(BigInt);return Q(a[0],a[1]||1n);}
function eq(a,b){return a[0]*b[1]===b[0]*a[1];}
function k(y1,y2,f){return f==="F0"?"":f==="F1"?String(y1):f==="F2"?String(y2):y1+","+y2;}
function compute(doc){
  if(doc.research_id!=="R247"||doc.world_results.length!==9)throw Error("wrong frozen results");
  const output={research_id:"R247",study:"S43",evidence:"E1_SYNTHETIC",source_blob:"33c948db4a5c3b0104f233fd8e03daa79faebccf",results:{},checks:0};
  for(const world of doc.world_results){
    const entries=Object.entries(world.observed_full_four_generation_family_path_joint).map(([path,p])=>{
      const y=path.split(",").map(Number);if(y.length!==4||y[0]!==1)throw Error("path");return {y,w:parse(p),t:y[3]>0?1:0};
    });
    let mass=Q(0n);for(const e of entries)mass=add(mass,e.w);
    if(!eq(mass,Q(1n)))throw Error("world mass");output.checks++;
    const record={};
    for(const f of PREFIXES){
      const groups=new Map();
      for(const e of entries){const key=k(e.y[1],e.y[2],f);const z=groups.get(key)||{m:Q(0n),s:Q(0n)};z.m=add(z.m,e.w);if(e.t)z.s=add(z.s,e.w);groups.set(key,z);}
      let risk=Q(0n);
      for(const e of entries){const g=groups.get(k(e.y[1],e.y[2],f));const p=Q(g.s[0]*g.m[1],g.s[1]*g.m[0]);const err=sub(Q(e.t),p);risk=add(risk,mul(e.w,mul(err,err)));}
      if(risk[0]<0n||risk[0]*4n>risk[1])throw Error("Brier bounds");
      record[f]={risk:fmt(risk),support:groups.size};output.checks+=2;
    }
    for(const [less,more] of [["F0","F1"],["F0","F2"],["F1","F12"],["F2","F12"]]){
      const a=parse(record[less].risk),b=parse(record[more].risk);if(a[0]*b[1]<b[0]*a[1])throw Error("conditioning monotonicity");output.checks++;
    }
    output.results[world.world]=record;
  }
  if(JSON.stringify(output.results.IID_FAIR_0_OR_2)!==JSON.stringify(output.results.STATIC_HIDDEN_TREE_SENSOR_ALIAS))throw Error("observational alias");
  output.checks++;output.future_leakage_negative_control="TARGET_INCLUDED_RISK_ZERO_ILLEGAL";output.external_replication=0;return output;
}
if(typeof module!=="undefined")module.exports={compute};
if(typeof require==="function"&&require.main===module){
 const file=process.argv[2]||"research/R247/R247_EXACT_RESULTS.json";
 process.stdout.write(JSON.stringify(compute(JSON.parse(fs.readFileSync(file,"utf8"))),null,2)+"\n");
}
