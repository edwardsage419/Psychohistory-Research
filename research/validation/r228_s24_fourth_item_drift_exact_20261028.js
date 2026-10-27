#!/usr/bin/env node
"use strict";
/* R228 S24. Frozen original 384 artificial atoms. Exact BigInt rational arithmetic.
   Run: node research/validation/r228_s24_fourth_item_drift_exact_20261028.js */
function main(csvText, originalText) {
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;};
 const f=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];};
 const P=x=>{const z=String(x).split("/");return f(z[0],z[1]||1);};
 const add=(a,b)=>f(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
 const neg=a=>[-a[0],a[1]],sub=(a,b)=>add(a,neg(b));
 const mul=(a,b)=>f(a[0]*b[0],a[1]*b[1]);
 const div=(a,b)=>f(a[0]*b[1],a[1]*b[0]);
 const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
 const str=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1];
 const zero=f(0),one=f(1),two=f(2),square=x=>mul(x,x);
 const pow2=k=>k>=0?f(2n**BigInt(k)):f(1,2n**BigInt(-k));
 const q=k=>{const z=pow2(k);return div(z,add(one,z));};
 const assert=(ok,msg)=>{if(!ok)throw Error(msg);};
 const raw=csvText.trim().split(/\r?\n/),cols=raw.shift().split(",");
 assert(raw.length===384,"original 384 source rows changed");
 const rows=raw.map(line=>{const a=line.split(",");assert(a.length===cols.length,"CSV schema changed");const r=Object.fromEntries(cols.map((k,i)=>[k,a[i]]));return {w:r.world,g:+r.observed_group_G,k:+r.latent_index_k,y:r.observed_Y1+r.observed_Y2+r.observed_Y3,s:+r.observed_total_score,p:P(r.source_probability)};});
 const worlds=[...new Set(rows.map(r=>r.w))],original=JSON.parse(originalText);
 assert(worlds.length===8,"world count");assert(original.world_results.length===8,"original results missing");
 const cases=[["STABLE",0,0],["GLOBAL_MINUS2",-2,-2],["GLOBAL_MINUS1",-1,-1],["GLOBAL_PLUS1",1,1],["GLOBAL_PLUS2",2,2],["GROUP1_MINUS1",0,-1],["GROUP1_PLUS1",0,1]];
 const rasch=new Set(["BASE_RASCH","LOCATION_SHIFT_ALIAS","DIF_SECOND_ITEM","EQUAL_ITEM_DIFFICULTY","SCALE_HIGH_DISCRIM","SCALE_LOW_DISCRIM_ALIAS"]);
 const result=[];let tests=0,positive=0;
 for(const w of worlds){
  const wr=rows.filter(r=>r.w===w);assert(wr.length===48,"48 per world");
  const total=wr.reduce((a,r)=>add(a,r.p),zero);assert(eq(total,one),"world probability");tests++;
  for(const [label,d0,d1] of cases){
   const groups={full:new Map(),score:new Map()};
   const key=(r,kind)=>r.g+":"+(kind==="full"?r.y:r.s);
   for(const kind of ["full","score"])for(const r of wr){
    const k=key(r,kind),t=groups[kind].get(k)||{mass:zero,old:zero,now:zero};
    t.mass=add(t.mass,r.p);t.old=add(t.old,mul(r.p,q(r.k)));t.now=add(t.now,mul(r.p,q(r.k-(r.g?d1:d0))));groups[kind].set(k,t);
   }
   const risks={old_full:zero,new_full:zero,old_score:zero,new_score:zero},extra={full:zero,score:zero},bias={full:zero,score:zero};
   let supported=0;
   for(const r of wr){if(eq(r.p,zero))continue;supported++;
    const qr=q(r.k-(r.g?d1:d0));
    for(const kind of ["full","score"]){
     const t=groups[kind].get(key(r,kind)),po=div(t.old,t.mass),pn=div(t.now,t.mass);
     for(const [version,pred] of [["old",po],["new",pn]]){
      const risk=add(mul(qr,square(sub(one,pred))),mul(sub(one,qr),square(pred)));
      const alt=add(mul(qr,sub(one,qr)),square(sub(qr,pred)));
      assert(eq(risk,alt),"Brier two point identity");tests++;
      const name=version+"_"+kind;risks[name]=add(risks[name],mul(r.p,risk));
     }
     extra[kind]=add(extra[kind],mul(r.p,square(sub(po,pn))));
     bias[kind]=add(bias[kind],mul(r.p,sub(qr,po)));
    }
   }
   positive+=supported;
   for(const kind of ["full","score"]){assert(eq(sub(risks["old_"+kind],risks["new_"+kind]),extra[kind]),"Bayes excess square identity");tests++;}
   assert(sub(risks.new_score,risks.new_full)[0]>=0n,"full information should not hurt");tests++;
   if(rasch.has(w)){assert(eq(risks.new_score,risks.new_full),"Rasch total sufficient");tests++;}
   if(label==="STABLE"){
    assert(eq(risks.old_full,risks.new_full)&&eq(risks.old_score,risks.new_score),"stable drift");
    const ref=original.world_results.find(x=>x.world===w);
    assert(eq(risks.old_full,P(ref.independent_fourth_item_full_pattern_brier))&&eq(risks.old_score,P(ref.independent_fourth_item_total_score_brier)),"R228 original risk regression");tests+=2;
   }
   result.push({world:w,scenario:label,d0,d1,structural_atoms:48,positive_atoms:supported,
    old_full_brier:str(risks.old_full),new_full_brier:str(risks.new_full),
    old_score_brier:str(risks.old_score),new_score_brier:str(risks.new_score),
    full_drift_excess:str(extra.full),score_drift_excess:str(extra.score),
    old_full_calibration_bias:str(bias.full),old_score_calibration_bias:str(bias.score),
    new_score_minus_full:str(sub(risks.new_score,risks.new_full))});
  }
 }
 assert(result.length===56&&positive===2520,"56 conditions 2520 positive source slots");
 for(const [a,b] of [["BASE_RASCH","LOCATION_SHIFT_ALIAS"],["SCALE_HIGH_DISCRIM","SCALE_LOW_DISCRIM_ALIAS"]]){
  for(const label of cases.map(c=>c[0])){
   const x=result.find(z=>z.world===a&&z.scenario===label),y=result.find(z=>z.world===b&&z.scenario===label);
   for(const key of ["old_full_brier","new_full_brier","old_score_brier","new_score_brier","full_drift_excess","old_full_calibration_bias"]){assert(x[key]===y[key],"alias mismatch");tests++;}
  }
 }
 return {study:"R228_S24",evidence:"E1_FINITE_ARTIFICIAL_ONLY",freeze_commit:"1e7936b9b78a61f2f4c8a508b4d239e193986375",
  source_blob:"bd980c55fb3c45b0f31a6e290afed1e01d471fd4",original_results_blob:"52065f07eecfea52cce42c1c48c7f024e619e0e9",
  worlds:8,scenarios:7,conditions:56,structural_source_slots:2688,positive_source_slots:positive,
  exact_internal_assertions:tests,external_human_E2:0,external_history_E3:0,rows:result};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path"),root=path.resolve(__dirname,"../..");
 const out=main(fs.readFileSync(path.join(root,"research/R228/R228_ALL_384_ORIGINAL_IRT_RESPONSE_ATOMS.csv"),"utf8"),
                fs.readFileSync(path.join(root,"research/R228/R228_EXACT_RESULTS.json"),"utf8"));
 process.stdout.write(JSON.stringify(out,null,2)+"\n");
}
