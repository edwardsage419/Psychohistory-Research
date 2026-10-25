"use strict";
// Independent R153 convex entropy audit. Does not import IPF or BigInt cycle program.
const fs=require("node:fs"),crypto=require("node:crypto"),path=require("node:path");
function r153IndependentEntropyAudit(data){
  const layouts={near:[0,1,4],far:[0,2,6]},att={flat:[1,1,1],column_bonus:[1,2,3]};
  const pairs=[[0,1],[0,2],[1,2]];
  let entropyPass=0,entropyFail=0,logPass=0,logFail=0,negativeMarginDetected=false;
  let minGap=Infinity,maxLogResidual=0,minCell=Infinity;
  const failures=[];
  if(data.scenarios.length!==24)throw Error("unexpected scenario count");
  for(const s of data.scenarios){
    const x=layouts[s.layout],a=att[s.attraction],alpha=s.exponent;
    if(!x||!a)throw Error("unknown case");
    const T=s.balanced_flow_28dp.map(row=>row.map(Number));
    const K=x.map((xi,i)=>x.map((xj,j)=>a[j]/Math.pow(1+Math.abs(xi-xj),alpha)));
    const objective=M=>M.reduce((acc,row,i)=>acc+row.reduce((t,v,j)=>t+v*Math.log(v/K[i][j]),0),0);
    const f0=objective(T);
    for(const [i,k] of pairs)for(const [j,l] of pairs){
      const e=Math.abs(Math.log(T[i][j])+Math.log(T[k][l])-Math.log(T[i][l])-Math.log(T[k][j])-
        (Math.log(K[i][j])+Math.log(K[k][l])-Math.log(K[i][l])-Math.log(K[k][j])));
      if(e>maxLogResidual)maxLogResidual=e;
      if(e<=1e-12)logPass++;else{logFail++;failures.push({case:s.layout+"|"+alpha+"|"+s.attraction+"|"+s.margin,logResidual:e})}
    }
    for(const [[i,k],[j,l]] of [[[0,1],[0,1]],[[1,2],[1,2]]])for(const sign of [-1,1]){
      const m=T.map(row=>row.slice()),eps=sign*0.01;
      m[i][j]+=eps;m[k][l]+=eps;m[i][l]-=eps;m[k][j]-=eps;
      if(!m.every(row=>row.every(v=>v>0)))throw Error("nonpositive perturbed flow");
      for(let p=0;p<3;p++)if(Math.abs(m[p].reduce((a,b)=>a+b,0)-T[p].reduce((a,b)=>a+b,0))>1e-9)throw Error("row broken");
      for(let q=0;q<3;q++)if(Math.abs(m.reduce((a,row)=>a+row[q],0)-T.reduce((a,row)=>a+row[q],0))>1e-9)throw Error("column broken");
      const gap=objective(m)-f0;
      if(gap<minGap)minGap=gap;
      if(gap>1e-9)entropyPass++;else{entropyFail++;failures.push({case:s.layout+"|"+alpha+"|"+s.attraction+"|"+s.margin,gap})}
    }
    const mutant=T.map(row=>row.slice());mutant[0][0]+=0.01;
    if(Math.abs(mutant[0].reduce((a,b)=>a+b,0)-T[0].reduce((a,b)=>a+b,0))>1e-9)negativeMarginDetected=true;
    for(const row of T)for(const v of row)if(v<minCell)minCell=v;
  }
  const out={research_id:"R153",evidence:"E1_INTERNAL_INDEPENDENT_NUMERIC_AUDIT",input_blob_sha:"6491aaa9b05571fbae7dee243906144a6f1a916d",scenarios:data.scenarios.length,entropy_perturbations_pass:entropyPass,entropy_perturbations_fail:entropyFail,log_cycle_pass:logPass,log_cycle_fail:logFail,min_entropy_objective_increase:minGap,max_abs_log_cycle_residual:maxLogResidual,negative_single_cell_margin_detected:negativeMarginDetected,min_flow_cell:minCell,failures};
  if(entropyPass!==96||entropyFail||logPass!==216||logFail||!negativeMarginDetected||minGap<=1e-9)throw Error("independent audit failure");
  return out;
}
const inputPath=process.argv[2]||path.join(__dirname,"../R153/R153_WILSON_SINKHORN_24_CASES_EXACT_RESULTS.json");
const bytes=fs.readFileSync(inputPath);
const blob=crypto.createHash("sha1").update("blob "+bytes.length+"\0").update(bytes).digest("hex");
if(blob!=="6491aaa9b05571fbae7dee243906144a6f1a916d")throw Error("frozen input Git blob mismatch");
process.stdout.write(JSON.stringify(r153IndependentEntropyAudit(JSON.parse(bytes.toString("utf8"))),null,2)+"\n");
