"use strict";
// E066 independent source-level exact rational audit for R235 S31.
// Run: node research/operations/e066_r235_s31_source_first_20261028.js <source.csv> <receipt.json>
const fs = require("node:fs");
function audit(csvText, receipt) {
  const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a;};
  const f=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d;}if(!d)throw Error("zero denominator");const g=gcd(n,d);return [n/g,d/g];};
  const p=s=>{const a=String(s).split("/");return f(a[0],a[1]??"1");};
  const add=(a,b)=>f(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
  const mul=(a,b)=>f(a[0]*b[0],a[1]*b[1]);
  const div=(a,b)=>f(a[0]*b[1],a[1]*b[0]);
  const sub=(a,b)=>add(a,[-b[0],b[1]]);
  const str=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1];
  const eq=(a,b)=>str(a)===str(b);
  const lines=csvText.trim().split(/\r?\n/), header=lines.shift().split(",");
  const rows=lines.map(l=>Object.fromEntries(l.split(",").map((v,i)=>[header[i],v])));
  let checks=0;const errors=[];
  function ok(cond,msg){checks++;if(!cond)errors.push(msg);}
  ok(receipt.research_id==="R235","research id");
  ok(receipt.phase==="S31","phase");
  ok(receipt.freeze_commit==="c0c353ba1cd87674ad7d791370ac78df66311ccd","freeze id");
  ok(rows.length===432,"source count");
  ok(receipt.conditions_data.length===45,"condition count");
  const byWorld=new Map();
  for(const r of rows){
    if(!byWorld.has(r.world))byWorld.set(r.world,[]);
    byWorld.get(r.world).push(r);
    const prior=mul(mul(p(r.original_group_prior),p(r.original_conditional_ability_probability)),p(r.conditional_response_pattern_probability));
    ok(eq(prior,p(r.original_source_probability)),r.world+" factor");
    ok(+r.observed_anchor_score===+r.observed_Y1 + +r.observed_Y3,r.world+" anchor");
    ok(p(r.original_source_probability)[0]>0n,r.world+" positive");
  }
  ok(byWorld.size===9,"world count");
  const rules=["ALL","G1_SUCCESS_HALF","G1_FAILURE_HALF","CONCORDANT_HALF","DISCORDANT_HALF"];
  function weight(rule,g,y){
    return rule==="ALL"||
      rule==="G1_SUCCESS_HALF"&&!(g===1&&y===1)||
      rule==="G1_FAILURE_HALF"&&!(g===1&&y===0)||
      rule==="CONCORDANT_HALF"&&g!==y||
      rule==="DISCORDANT_HALF"&&g===y?f(1):f(1,2);
  }
  for(const [world,rr] of byWorld){
    ok(rr.length===48,world+" source count");
    let z=f(0);for(const r of rr)z=add(z,p(r.original_source_probability));
    ok(str(z)==="1",world+" source normalization");
  }
  for(const c of receipt.conditions_data){
    const wr=byWorld.get(c.world);
    ok(!!wr,c.world+" exists");ok(rules.includes(c.rule),c.rule+" known");
    const mass={};let Z=f(0);
    for(const r of wr){
      const g=+r.observed_group_G,y=+r.observed_Y2,key=""+g+r.observed_Y1+r.observed_Y2+r.observed_Y3;
      const w=mul(p(r.original_source_probability),weight(c.rule,g,y));
      mass[key]=add(mass[key]??f(0),w);Z=add(Z,w);
    }
    ok(eq(Z,p(c.retention_probability)),c.world+" "+c.rule+" retention");
    const q={};for(const k of Object.keys(mass))q[k]=div(mass[k],Z);
    ok(Object.keys(q).length===16,c.world+" "+c.rule+" support");
    for(const [k,v] of Object.entries(c.selected_joint))ok(eq(q[k],p(v)),c.world+" "+c.rule+" cell "+k);
    const gm=[f(0),f(0)],succ=[f(0),f(0)];
    const tab=Array.from({length:3},()=>Array.from({length:2},()=>[f(0),f(0)]));
    for(const [key,v] of Object.entries(q)){
      const [g,y1,y2,y3]=[...key].map(Number);
      gm[g]=add(gm[g],v);if(y2)succ[g]=add(succ[g],v);
      tab[y1+y3][g][y2]=add(tab[y1+y3][g][y2],v);
    }
    for(let g=0;g<2;g++){
      ok(eq(gm[g],p(c.group_masses[g])),c.world+" group mass");
      ok(eq(div(succ[g],gm[g]),p(c.focal_success_rates_by_group[g])),c.world+" focal rate");
    }
    let n=f(0),d=f(0);
    for(let s=0;s<3;s++){
      const a=tab[s][1][1],b=tab[s][1][0],cc=tab[s][0][1],dd=tab[s][0][0];
      const N=add(add(a,b),add(cc,dd));
      n=add(n,div(mul(a,dd),N));d=add(d,div(mul(b,cc),N));
      ok(eq(sub(div(a,add(a,b)),div(cc,add(cc,dd))),p(c.anchor_score_focal_differences[s])),c.world+" anchor stratum "+s);
    }
    ok(eq(div(n,d),p(c.mh_odds_ratio)),c.world+" MH");
  }
  const base=receipt.conditions_data.filter(c=>c.world==="BASE_NO_DIF");
  const alias=receipt.conditions_data.filter(c=>c.world==="GLOBAL_REANCHOR_ALIAS");
  for(let i=0;i<5;i++)for(const k of Object.keys(base[i].selected_joint))
    ok(base[i].selected_joint[k]===alias[i].selected_joint[k],"alias "+i+" "+k);
  return {checks,failed:errors.length,errors:errors.slice(0,20),source_rows:rows.length,worlds:byWorld.size,conditions:receipt.conditions_data.length};
}
if(require.main===module){
  if(process.argv.length!==4)throw Error("Usage: node <script> <source.csv> <receipt.json>");
  const result=audit(fs.readFileSync(process.argv[2],"utf8"),JSON.parse(fs.readFileSync(process.argv[3],"utf8")));
  console.log(JSON.stringify(result,null,2));if(result.failed)process.exitCode=1;
}
module.exports={audit};
