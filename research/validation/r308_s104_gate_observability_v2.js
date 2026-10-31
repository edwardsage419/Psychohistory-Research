"use strict";
// R308 S104 v2. Correct newline serialization; original v1 kept as failure evidence.
function computeS104(){
 const patterns={
  NONE:[0,0,0],LOW_UNIFORM:[1,1,1],HIGH_UNIFORM:[2,2,2],
  ONE_STRONG_TWO_ZERO:[2,0,0],ONE_WEAK_LINK:[2,2,0],
  SAME_MEAN_NO_ZERO:[2,1,1],HETEROGENEOUS:[2,1,0],HALF_HALF_ZERO:[1,1,0]};
 const aggregations=["MEAN","BOTTLENECK_MIN"],schemes=["S0","S1","S2","S3"];
 const rows=[],groups=[];
 for(const [pattern,beliefs] of Object.entries(patterns))for(const aggregation of aggregations){
  const b=aggregation==="MEAN"?beliefs.reduce((a,v)=>a+v,0):3*Math.min(...beliefs);
  const buckets=schemes.map(()=>new Map());
  for(let c=0;c<=2;c++)for(let w=0;w<=2;w++)for(let r=0;r<=2;r++){
   const A=b*c*w*r,Ac=b*2*w*r,Aw=b*c*2*r,Ar=b*c*w*2,
    Acw=b*4*r,Acr=b*4*w,Awr=b*4*c;
   const v=[[A],[A,Ac,Aw,Ar],[A,Acw,Acr,Awr],[A,Ac,Aw,Ar,Acw,Acr,Awr]];
   const row={pattern,aggregation,B_num6:b,c_half:c,w_half:w,r_half:r,
    S0_A_num48:A,S1_Ac_num48:Ac,S1_Aw_num48:Aw,S1_Ar_num48:Ar,
    S2_Acw_num48:Acw,S2_Acr_num48:Acr,S2_Awr_num48:Awr};
   rows.push(row);
   v.forEach((signature,i)=>{const key=signature.join("|");buckets[i].set(key,(buckets[i].get(key)||0)+1)});
  }
  groups.push({pattern,aggregation,B_num6:b,
   classes:buckets.map(m=>m.size),
   singleton_worlds:buckets.map(m=>[...m.values()].filter(v=>v===1).length),
   largest_class:buckets.map(m=>Math.max(...m.values()))});
 }
 const sum=(field,i)=>groups.reduce((a,g)=>a+g[field][i],0);
 const summary={worlds:rows.length,belief_groups:groups.length,gate_worlds_per_group:27,
  zero_B_groups:groups.filter(g=>g.B_num6===0).length,
  total_classes:schemes.map((_,i)=>sum("classes",i)),
  singleton_worlds:schemes.map((_,i)=>sum("singleton_worlds",i)),
  group_mean_classes:schemes.map((_,i)=>sum("classes",i)/groups.length),
  no_real_human_E2:0,no_historical_E3:0};
 if(rows.length!==432||groups.length!==16||summary.zero_B_groups!==6)throw Error("universe failure");
 for(const g of groups)if(g.B_num6>0 && (g.classes[2]!==27||g.classes[3]!==27))throw Error("S2 injectivity failure");
 for(const g of groups)if(g.B_num6===0 && g.classes.some(v=>v!==1))throw Error("B0 negative control failure");
 return {schema:"R308_S104_E1_exact_integer_gate_observability_v1",freeze_path:"research/validation/R308_S104_GATE_OBSERVABILITY_PRESCORE_FREEZE_2026-10-31.md",
  freeze_commit:"e3d2b690a794d4fd3e748b43a59e71d56eda09cf",
  original_R308_unchanged:true,scale:"B_num6 / 6, all A numerators / 48, gates_half / 2",
  schemes,summary,groups,rows};
}
const fs=require("fs"),path=require("path");
const result=computeS104();
const csvColumns=["pattern","aggregation","B_num6","c_half","w_half","r_half","S0_A_num48","S1_Ac_num48","S1_Aw_num48","S1_Ar_num48","S2_Acw_num48","S2_Acr_num48","S2_Awr_num48"];
const csv=csvColumns.join(",")+"\n"+result.rows.map(r=>csvColumns.map(k=>r[k]).join(",")).join("\n")+"\n";
const json=JSON.stringify(result,null,2)+"\n";
if(process.argv[2]==="--selftest"){
 if(result.summary.total_classes.join(",")!=="56,186,276,276")throw Error("unexpected classes");
 if(result.summary.singleton_worlds.join(",")!=="20,140,270,270")throw Error("unexpected singletons");
 console.log("PASS R308 S104 432 worlds, 16 groups, 4 schemes");
}else if(process.argv[2]==="--emit"){
 const dest=process.argv[3];if(!dest)throw Error("usage: node r308_s104_gate_observability.js --emit OUT_DIR");
 fs.mkdirSync(dest,{recursive:true});
 fs.writeFileSync(path.join(dest,"R308_S104_ALL_432_GATE_WORLDS.csv"),csv);
 fs.writeFileSync(path.join(dest,"R308_S104_EXACT_OBSERVABILITY_RESULTS.json"),json);
 console.log("WROTE",dest);
}else{console.log(JSON.stringify(result.summary,null,2));}
