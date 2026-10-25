"use strict";
// R153 third method. Node.js standard library only; no network or paid services.
const fs=require("node:fs"),crypto=require("node:crypto"),path=require("node:path");
function r153Main(data){
  const U=10n**28n,Q=10n**24n,coords={near:[0,1,4],far:[0,2,6]},attrs={flat:[1,1,1],column_bonus:[1,2,3]};
  const abs=x=>x<0n?-x:x;
  const parse=x=>{if(typeof x!=="string"||!/^\d+\.\d{28}$/.test(x))throw Error("noncanonical decimal "+x);const [a,b]=x.split(".");return BigInt(a)*U+BigInt(b)};
  const pairs=[[0,1],[0,2],[1,2]],cases=new Map(),summaries=[];
  if(data.scenarios.length!==24)throw Error("scenario count");
  let initialMarginPass=0,initialMarginFail=0,amendedMarginPass=0,amendedMarginFail=0,cyclesPass=0,cyclesFail=0,attractionPass=0,attractionFail=0;
  let worst={n:0n,d:1n,key:""},maxMargin=0n;
  function cycle(T,x,alpha){
    let ok=0,bad=0;
    for(const [i,k] of pairs)for(const [j,l] of pairs){
      const d=(a,b)=>BigInt(1+Math.abs(x[a]-x[b]));
      const lhs=T[i][j]*T[k][l]*(d(i,j)*d(k,l))**BigInt(alpha);
      const rhs=T[i][l]*T[k][j]*(d(i,l)*d(k,j))**BigInt(alpha);
      const n=abs(lhs-rhs),den=lhs>rhs?lhs:rhs;
      if(n*Q<=den)ok++;else bad++;
      if(n*worst.d>worst.n*den)worst={n,d:den,key:`${i}${k}:${j}${l}`};
    }
    return{ok,bad};
  }
  for(const s of data.scenarios){
    const key=[s.layout,s.exponent,s.attraction,s.margin].join("|");
    if(cases.has(key)||!(s.layout in coords)||!(s.attraction in attrs)||![0,1,2].includes(s.exponent)||!["m0","m1"].includes(s.margin))throw Error("bad key");
    const R=s.margin==="m0"?[10,20,30]:[20,20,20],C=s.margin==="m0"?[15,25,20]:[10,30,20];
    if(JSON.stringify(R)!==JSON.stringify(s.origin_budgets)||JSON.stringify(C)!==JSON.stringify(s.destination_budgets))throw Error("margins inconsistent");
    const T=s.balanced_flow_28dp.map(r=>r.map(parse));
    for(const r of T)for(const t of r)if(t<=0n)throw Error("nonpositive");
    let initialPass=0,initialFail=0,amendedPass=0,amendedFail=0,caseMax=0n;
    for(let z=0;z<6;z++){
      const e=z<3?abs(T[z].reduce((a,b)=>a+b,0n)-BigInt(R[z])*U):abs(T.reduce((a,r)=>a+r[z-3],0n)-BigInt(C[z-3])*U);
      if(e<=3n)initialPass++;else initialFail++;
      if(e<=1000n)amendedPass++;else amendedFail++;
      if(e>caseMax)caseMax=e;
    }
    if(caseMax>maxMargin)maxMargin=caseMax;
    const c=cycle(T,coords[s.layout],s.exponent);
    initialMarginPass+=initialPass;initialMarginFail+=initialFail;amendedMarginPass+=amendedPass;amendedMarginFail+=amendedFail;cyclesPass+=c.ok;cyclesFail+=c.bad;
    cases.set(key,T);
    summaries.push({key,cycles_pass:c.ok,cycles_fail:c.bad,initial_margins_pass:initialPass,initial_margins_fail:initialFail,amended_margins_pass:amendedPass,amended_margins_fail:amendedFail,max_margin_error_1e28_units:caseMax.toString()});
  }
  for(const layout of Object.keys(coords))for(const alpha of [0,1,2])for(const margin of ["m0","m1"]){
    const a=cases.get([layout,alpha,"flat",margin].join("|")),b=cases.get([layout,alpha,"column_bonus",margin].join("|"));
    if(!a||!b)throw Error("missing attraction pair");
    for(let i=0;i<3;i++)for(let j=0;j<3;j++){if(abs(a[i][j]-b[i][j])<=10000n)attractionPass++;else attractionFail++}
  }
  const orig=cases.get("near|2|flat|m0"),mutant=orig.map(row=>row.slice()),delta=10n**26n;
  mutant[0][0]+=delta;mutant[0][1]-=delta;mutant[1][0]-=delta;mutant[1][1]+=delta;
  const n1=cycle(mutant,coords.near,2),n2=cycle(orig,coords.near,1);
  const out={research_id:"R153",evidence:"E1_INTERNAL_BOUNDED_WITH_DISCLOSED_AMENDMENT",input_blob_sha:"6491aaa9b05571fbae7dee243906144a6f1a916d",scenario_count:cases.size,cycles_pass:cyclesPass,cycles_fail:cyclesFail,initial_margins_pass:initialMarginPass,initial_margins_fail:initialMarginFail,amended_margins_pass:amendedMarginPass,amended_margins_fail:amendedMarginFail,attraction_cells_pass:attractionPass,attraction_cells_fail:attractionFail,negative_control_cycle_mutant_detected:n1.bad>0,negative_control_wrong_exponent_detected:n2.bad>0,max_margin_error_1e28_units:maxMargin.toString(),cycle_worst_relative_numerator:worst.n.toString(),cycle_worst_relative_denominator:worst.d.toString(),scenarios:summaries};
  if(cases.size!==24||cyclesPass!==216||cyclesFail||initialMarginFail!==48||amendedMarginPass!==144||amendedMarginFail||attractionPass!==108||attractionFail||!out.negative_control_cycle_mutant_detected||!out.negative_control_wrong_exponent_detected)throw Error("frozen coverage or amended gate failure");
  return out;
}
const inputPath=process.argv[2]||path.join(__dirname,"../R153/R153_WILSON_SINKHORN_24_CASES_EXACT_RESULTS.json");
const bytes=fs.readFileSync(inputPath);
const blob=crypto.createHash("sha1").update("blob "+bytes.length+"\0").update(bytes).digest("hex");
if(blob!=="6491aaa9b05571fbae7dee243906144a6f1a916d")throw Error("frozen input Git blob mismatch: "+blob);
process.stdout.write(JSON.stringify(r153Main(JSON.parse(bytes.toString("utf8"))),null,2)+"\n");
