// R271 S67: complete artificial source generator. Node 18+; no dependencies.
// Exploratory, nonblind E1 only. Do not alter original R271.
"use strict";
function generate() {
  const designs=["IDENTICAL","ROLLING","DISJOINT"];
  const policies=["FROZEN_FIRST","FLEXIBLE_ANY","BONFERRONI_ANY"];
  const pv=["1","15/16","11/16","5/16","1/16"];
  const header="world,design,m,policy,bits,window_positions,success_counts,raw_p_values,selected_index,positive,source_mass\n";
  let csv=header, worlds=[], total=0;
  function gcd(a,b){while(b){let t=a%b;a=b;b=t;}return a;}
  function fraction(n,d){let g=gcd(n,d);n/=g;d/=g;return d===1?String(n):n+"/"+d;}
  function windows(d,m){
    return Array.from({length:m},(_,j)=>Array.from({length:4},(_,k)=>
      d==="IDENTICAL"?k:d==="ROLLING"?j+k:4*j+k));
  }
  for(let m=1;m<=3;m++) for(let d of designs) for(let p of policies){
    const ww=windows(d,m),L=Math.max(...ww.flat())+1, N=2**L;
    const wp=ww.map(w=>w.join(".")).join(";");
    const label=d+"_M"+m+"_"+p;
    let positiveCount=0;
    for(let z=0;z<N;z++){
      const bits=z.toString(2).padStart(L,"0");
      const counts=ww.map(w=>w.reduce((s,k)=>s+(bits[k]==="1"?1:0),0));
      const values=counts.map(k=>pv[k]);
      const indices=p==="FROZEN_FIRST"?[0]:Array.from({length:m},(_,i)=>i);
      const selected=indices.find(i=>counts[i]===4 && (p!=="BONFERRONI_ANY" || m<=2));
      const index=selected===undefined?-1:selected;
      const pos=index>=0?1:0;
      positiveCount+=pos;
      csv += [label,d,m,p,bits,wp,counts.join(";"),values.join(";"),index,pos,"1/"+N].join(",")+"\n";
    }
    total+=N;
    worlds.push({world:label,design:d,m,policy:p,source_count:N,
      exact_familywise_false_positive_risk:fraction(positiveCount,N)});
  }
  if(worlds.length!==27||total!==13584)throw Error("universe mismatch");
  const results={research_id:"R271_S67",original_model:"R271",
    evidence:"E1_EXPLORATORY_ARTIFICIAL_NONBLIND",strict_blind_prescore_freeze:false,
    real_human_E2:0,real_historical_E3:0,external_independent_replications:0,
    original_R271_acceptance_unchanged:true,R073:"FROZEN",PESEN_v0_1:"FROZEN",
    world_count:27,policy_labelled_source_count:total,worlds};
  return {csv,json:JSON.stringify(results,null,2)+"\n",results};
}
if(typeof require==="function" && typeof process!=="undefined" && require.main===module){
  const fs=require("fs"),path=require("path"),crypto=require("crypto");
  const dir=process.argv[2]||".",out=generate();
  fs.mkdirSync(dir,{recursive:true});
  const csvName="R271_S67_ALL_13584_OVERLAPPING_NULL_SOURCE_ROWS.csv";
  const jsonName="R271_S67_EXACT_FAMILYWISE_RISKS.json";
  fs.writeFileSync(path.join(dir,csvName),out.csv);
  fs.writeFileSync(path.join(dir,jsonName),out.json);
  const receipt={research_id:"R271_S67",evidence:"E1_EXPLORATORY_ARTIFICIAL_NONBLIND",
    source_rows:13584,world_count:27,
    source_sha256:crypto.createHash("sha256").update(out.csv).digest("hex"),
    results_sha256:crypto.createHash("sha256").update(out.json).digest("hex"),
    external_independent_replications:0,new_E2:0,new_E3:0};
  fs.writeFileSync(path.join(dir,"R271_S67_MACHINE_RECEIPT.json"),JSON.stringify(receipt,null,2)+"\n");
  process.stdout.write(JSON.stringify(receipt)+"\n");
}
