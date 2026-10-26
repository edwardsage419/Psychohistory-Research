"use strict";
// Run from repository root: node research/validation/r182_covariate_shift_960_20261026.js
const fs=require("node:fs");
function analyze(worlds){
 const F=v=>{let [a,b="1"]=String(v).split("/");a=BigInt(a);b=BigInt(b);let gcd=(x,y)=>y?gcd(y,x%y):(x<0n?-x:x);let g=gcd(a,b);if(b<0n)g=-g;return [a/g,b/g]};
 const add=(x,y)=>F((x[0]*y[1]+y[0]*x[1])+"/"+(x[1]*y[1]));
 const neg=x=>[-x[0],x[1]],sub=(x,y)=>add(x,neg(y));
 const mul=(x,y)=>F((x[0]*y[0])+"/"+(x[1]*y[1])),div=(x,y)=>F((x[0]*y[1])+"/"+(x[1]*y[0]));
 const str=x=>x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);
 const cmp=(x,y)=>x[0]*y[1]>y[0]*x[1]?1:x[0]*y[1]<y[0]*x[1]?-1:0;
 const ds=[["BALANCED",[2,2,2,2]],["POSITIVE",[4,2,2,4]],["NEGATIVE",[2,4,4,2]],["STRONG_POSITIVE",[6,2,2,6]]];
 let out=[],stats={worlds:worlds.length,comparisons:0,analytic_exact_checks:0,m1_exact_checks:0,m0_vs_m1:{positive:0,zero:0,negative:0},m0_vs_train:{increase:0,decrease:0,same:0},m1_vs_train:{increase:0,decrease:0,same:0},nonzero_shift_bias_terms:0,max_excess:null,fixed_example:[]};
 for(let [idx,w] of worlds.entries()){
  const a=F(w.true_a),b=F(w.true_x_slope_b),c=F(w.true_group_slope_c),e=F(w.residual_amplitude_e);
  const tr=w.cell_counts_in_00_01_10_11_order;
  const qtr=[F(tr[1]+"/"+(tr[0]+tr[1])),F(tr[3]+"/"+(tr[2]+tr[3]))];
  const int0=F(w.simple_intercept),beta0=F(w.simple_x_coefficient),int1=F(w.adjusted_intercept),beta1=F(w.adjusted_x_coefficient),gamma1=F(w.adjusted_z_coefficient);
  let worldRows=[];
  for(let [name,counts] of ds){
   const N=counts.reduce((x,y)=>x+y,0),qt=[F(counts[1]+"/"+(counts[0]+counts[1])),F(counts[3]+"/"+(counts[2]+counts[3]))];
   let ss0=F(0),ss1=F(0);
   for(let k=0;k<4;k++){let x=k>>1,z=k%2;
    for(let t=0;t<counts[k];t++){
     const eps=t<counts[k]/2?e:neg(e),y=add(add(add(a,mul(b,F(x))),mul(c,F(z))),eps);
     const p0=add(int0,mul(beta0,F(x))),p1=add(add(int1,mul(beta1,F(x))),mul(gamma1,F(z)));
     const d0=sub(y,p0),d1=sub(y,p1);ss0=add(ss0,mul(d0,d0));ss1=add(ss1,mul(d1,d1));
    }
   }
   const mse0=div(ss0,F(N)),mse1=div(ss1,F(N));
   let formula=mul(e,e),shift=F(0);
   for(let x=0;x<2;x++){
    const px=F((counts[2*x]+counts[2*x+1])+"/"+N),variance=mul(qt[x],sub(F(1),qt[x])),bias=mul(sub(qt[x],qtr[x]),sub(qt[x],qtr[x]));
    formula=add(formula,mul(mul(mul(c,c),px),add(variance,bias)));shift=add(shift,mul(px,bias));
   }
   if(cmp(mse0,formula)!==0)throw Error("analytic mismatch "+idx+" "+name);
   if(cmp(mse1,mul(e,e))!==0)throw Error("full mismatch "+idx+" "+name);
   stats.analytic_exact_checks++;stats.m1_exact_checks++;
   if(cmp(shift,F(0))>0)stats.nonzero_shift_bias_terms++;
   const excess=sub(mse0,mse1);
   const r={world_index:idx,train_design:w.design,target_design:name,mse_m0:str(mse0),mse_m1:str(mse1),m0_excess:str(excess),shift_bias_component:str(mul(mul(c,c),shift))};
   worldRows.push(r);out.push(r);stats.comparisons++;
   stats.m0_vs_m1[cmp(excess,F(0))>0?"positive":cmp(excess,F(0))<0?"negative":"zero"]++;
   if(stats.max_excess===null||cmp(excess,F(stats.max_excess.value))>0)stats.max_excess={value:str(excess),world_index:idx,train_design:w.design,target_design:name,c:str(c)};
   if(w.design==="STRONG_POSITIVE"&&str(a)==="0"&&str(b)==="1/4"&&str(c)==="-2"&&str(e)==="1/4")stats.fixed_example.push(r);
  }
  const base=worldRows.find(r=>r.target_design===w.design);
  for(let r of worldRows){
   const d0=cmp(F(r.mse_m0),F(base.mse_m0)),d1=cmp(F(r.mse_m1),F(base.mse_m1));
   stats.m0_vs_train[d0>0?"increase":d0<0?"decrease":"same"]++;
   stats.m1_vs_train[d1>0?"increase":d1<0?"decrease":"same"]++;
  }
 }
 if(stats.worlds!==240||stats.comparisons!==960)throw Error("grid incomplete");
 return {source_blob:"aded7e150ca4f4e2d464fd6dfc85f16bb7738984",protocol_commit:"b8c5e1f2b12099238c52a2681b3ffd26809474ad",evidence:"E1_ARTIFICIAL_POSTSCORE",stats,rows:out};
}
const data=JSON.parse(fs.readFileSync("research/R182/R182_EXACT_RESULTS.json","utf8"));
process.stdout.write(JSON.stringify(analyze(data.all_worlds),null,2)+"\n");
