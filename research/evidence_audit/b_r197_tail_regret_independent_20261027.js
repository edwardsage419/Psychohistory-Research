// B R197 independent candidate-risk audit, Node.js >=18.
const fs=require("fs"),path=require("path");
function verify(csv,receipt){
 const frac=x=>{let t=String(x).split("/"),n=BigInt(t[0]),d=t[1]===undefined?1n:BigInt(t[1]);if(d<0n){n=-n;d=-d}let a=n<0n?-n:n,b=d;while(b){let q=a%b;a=b;b=q}a=a||1n;return [n/a,d/a]};
 const plus=(a,b)=>frac((a[0]*b[1]+b[0]*a[1])+"/"+(a[1]*b[1]));
 const minus=(a,b)=>frac((a[0]*b[1]-b[0]*a[1])+"/"+(a[1]*b[1]));
 const mul=(a,b)=>frac((a[0]*b[0])+"/"+(a[1]*b[1]));
 const div=(a,b)=>frac((a[0]*b[1])+"/"+(a[1]*b[0]));
 const cmp=(a,b)=>a[0]*b[1]-b[0]*a[1];
 const Z=frac(0),O=frac(1),Q=frac("1/4");
 const fields=s=>{let a=[],v="",quoted=false;for(let i=0;i<s.length;i++){let c=s[i];if(c==='"'){if(quoted&&s[i+1]==='"'){v+='"';i++}else quoted=!quoted}else if(c===","&&!quoted){a.push(v);v=""}else v+=c}a.push(v);return a};
 const lines=csv.trim().split(/\r?\n/),header=fields(lines.shift()),main=JSON.parse(receipt);
 const sources=["WHITE","AR1","RW","DRIFT","DIFF_AR1","DIFF_MA1"],groups=new Map();let identity=0,hindsight=0;
 for(const line of lines){let a=fields(line),r=Object.fromEntries(header.map((k,i)=>[k,a[i]]));if(a.length!==header.length)throw Error("width");
  const k=r.source+"|"+r.training_time_steps_T+"|"+r.future_horizon_h;
  if(!groups.has(k))groups.set(k,{mass:Z,q:Z,rw:Z,d:Z,t25:Z,t1:Z,worse:Z,better:Z,tie:Z,model:Object.fromEntries(sources.map(s=>[s,{mass:Z,q:Z,d:Z}]))});
  let w=groups.get(k),p=frac(r.true_original_training_mass),v=frac(r.true_conditional_test_variance_oracle);
  let selected=frac(r["candidate_"+r.selected_prequential_model+"_true_independent_future_MSE"]),rw=frac(r.candidate_RW_true_independent_future_MSE);
  if(cmp(selected,frac(r.fitted_model_true_independent_future_MSE))!==0n)throw Error("candidate selected mismatch");
  let q=minus(selected,v),qrw=minus(rw,v),d=minus(selected,rw);if(cmp(q,Z)<0n||cmp(qrw,Z)<0n)throw Error("negative risk");identity+=3;
  let best=selected;for(const s of sources){let t=frac(r["candidate_"+s+"_true_independent_future_MSE"]);if(cmp(t,best)<0n)best=t}if(cmp(best,selected)<0n)hindsight++;
  w.mass=plus(w.mass,p);w.q=plus(w.q,mul(p,q));w.rw=plus(w.rw,mul(p,qrw));w.d=plus(w.d,mul(p,d));
  if(cmp(q,Q)>0n)w.t25=plus(w.t25,p);if(cmp(q,O)>0n)w.t1=plus(w.t1,p);
  if(cmp(d,Z)>0n)w.worse=plus(w.worse,p);else if(cmp(d,Z)<0n)w.better=plus(w.better,p);else w.tie=plus(w.tie,p);
  let m=w.model[r.selected_prequential_model];m.mass=plus(m.mass,p);m.q=plus(m.q,mul(p,q));m.d=plus(m.d,mul(p,d));
 }
 if(lines.length!==3888||groups.size!==24||hindsight===0)throw Error("counts");
 let checks=0,nonzero=0;
 for(let r of main.worlds){let w=groups.get(r.source+"|"+r.T+"|"+r.h);if(!w)throw Error("missing");
  for(const [a,b] of [[w.mass,r.probability_mass],[w.q,r.selected_excess],[w.rw,r.RW_excess],[w.d,r.selected_minus_RW],[w.t25,r.P_excess_gt_quarter],[w.t1,r.P_excess_gt_one],[w.worse,r.P_worse_than_RW],[w.better,r.P_better_than_RW],[w.tie,r.P_equal_RW]]){if(cmp(a,frac(b))!==0n)throw Error("world mismatch");checks++}
  for(const s of sources){let a=w.model[s],b=r.by_selected_model[s];if(cmp(a.mass,frac(b.probability))!==0n)throw Error("model mass");checks++;if(a.mass[0]===0n){if(b.conditional_excess!==null||b.conditional_vs_RW!==null)throw Error("null mismatch")}else{nonzero++;if(cmp(div(a.q,a.mass),frac(b.conditional_excess))!==0n||cmp(div(a.d,a.mass),frac(b.conditional_vs_RW))!==0n)throw Error("conditional mismatch");checks+=2}}
 }
 const first=Object.fromEntries(header.map((k,i)=>[k,fields(lines[0])[i]]));
 if(cmp(plus(frac(first.fitted_model_true_independent_future_MSE),O),frac(first["candidate_"+first.selected_prequential_model+"_true_independent_future_MSE"]))===0n)throw Error("mutation missed");
 return {schema:"B_R197_independent_exact_v1",rows:lines.length,worlds:groups.size,field_identity_checks:identity,exact_main_comparisons:checks,nonzero_selected_model_cells:nonzero,corrupt_risk_negative_control:"DETECTED",hindsight_future_best_strictly_better_paths:hindsight,mismatches:0,evidence:"INTERNAL_E1_ONLY"};
}
if(require.main===module){const root=process.argv[2]||path.resolve(__dirname,"../..");const a=fs.readFileSync(path.join(root,"research/R197/R197_ALL_3888_INDEPENDENT_HELDOUT_RISK_PROFILES.csv"),"utf8");const b=fs.readFileSync(path.join(root,"research/validation/R197_SELECTION_TAIL_REGRET_24_EXACT_RECEIPT_2026-10-27.json"),"utf8");process.stdout.write(JSON.stringify(verify(a,b),null,2)+"\n")}
module.exports={verify};
