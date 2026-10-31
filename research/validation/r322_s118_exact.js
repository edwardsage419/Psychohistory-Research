// R322 S118 exact finite observation/noise scorer, Node standard library only.
// Frozen original R322 CSV required; no empirical data.
function exact(csv){
 const headers=["world_id","policy","h","a","y","d","r","w","weight","output","correct","intervention"];
 const lines=csv.trimEnd().split(/\r?\n/);if(lines[0]!==headers.join(","))throw Error("header mismatch");
 const rows=lines.slice(1).map(line=>{let a=line.split(",");if(a.length!==12)throw Error("column count");return Object.fromEntries(headers.map((h,i)=>[h,a[i]]))});
 if(rows.length!==256)throw Error("row count");
 const policies=["default_only","gated_intervention","analytic_only","lookup_equivalent"],seen=new Set();
 for(const row of rows){
  let p=row.policy;if(!policies.includes(p)||row.world_id!==String(policies.indexOf(p)))throw Error("policy identity");
  let bits=["h","a","y","d","r","w"].map(k=>Number(row[k]));
  if(bits.some(x=>!Number.isInteger(x)||(x!==0&&x!==1)))throw Error("nonbinary");
  let key=p+"|"+bits.join("");if(seen.has(key))throw Error("duplicate");seen.add(key);
  let [h,a,y,d,r,w]=bits,gate=Number(h!==a&&d===1&&r===1&&w===1);
  let out=p==="default_only"?h:p==="analytic_only"?a:p==="gated_intervention"?(gate?a:h):(h^((h^a)&d&r&w));
  let label=p==="gated_intervention"?gate:p==="analytic_only"?1:0;
  if(row.weight!=="1/64"||row.output!==String(out)||row.correct!==String(Number(out===y))||row.intervention!==String(label))throw Error("truth table mismatch");
 }
 if(seen.size!==256)throw Error("source universe");
 const strata=["all","r0","r1","gate_all"],epss=[0,1,2],obs=["behavior_full","behavior_partial","behavior_only","label_only","label_full"];
 const gcd=(a,b)=>b?gcd(b,a%b):a;const frac=(n,d)=>{if(n===0)return"0";let g=gcd(n,d);return d/g===1?String(n/g):`${n/g}/${d/g}`};
 const eligible=(r,s)=>s==="all"||(s==="r0"&&r.r==="0")||(s==="r1"&&r.r==="1")||(s==="gate_all"&&r.d==="1"&&r.r==="1"&&r.w==="1");
 const key=(r,o,l)=>o==="behavior_full"?[r.h,r.a,r.d,r.r,r.w,r.output].join("|"):o==="behavior_partial"?[r.h,r.a,r.output].join("|"):o==="behavior_only"?r.output:o==="label_only"?[r.output,l].join("|"):[r.h,r.a,r.d,r.r,r.w,r.output,l].join("|");
 const mass=(p,o,k,s)=>{let a=rows.filter(r=>r.policy===p&&eligible(r,s)),m=new Map();let add=(key,n)=>m.set(key,(m.get(key)||0)+n);
  for(const r of a){if(o.startsWith("behavior_"))add(key(r,o,null),4);else{let l=Number(r.intervention);add(key(r,o,l),4-k);add(key(r,o,1-l),k)}}
  if([...m.values()].reduce((x,y)=>x+y,0)!==4*a.length)throw Error("mass");
  return [m,a.length];
 };
 let cells=[];
 for(let s of strata)for(let k of epss)for(let o of obs){
  let [a,n]=mass("gated_intervention",o,k,s),[b,n2]=mass("lookup_equivalent",o,k,s);if(n!==n2)throw Error("stratum mismatch");
  let keys=new Set([...a.keys(),...b.keys()]),dist=0;for(let x of keys)dist+=Math.abs((a.get(x)||0)-(b.get(x)||0));
  let tvn=dist,tvd=8*n;
  cells.push({stratum:s,noise_flip:frac(k,4),observation:o,total_variation:frac(tvn,tvd),bayes_accuracy:frac(tvd+tvn,2*tvd),support_gated:[...a.values()].filter(x=>x>0).length,support_lookup:[...b.values()].filter(x=>x>0).length});
 }
 if(cells.length!==60)throw Error("cells");
 if(cells.some(x=>(x.observation.startsWith("behavior_")||x.stratum==="r0"||x.noise_flip==="1/2")&&x.total_variation!=="0"))throw Error("negative controls");
 return {schema:"R322_S118_EXACT_OBSERVATION_LABEL_NOISE_E1_v1",frozen_original_source_blob:"0cd38ecc22adc5941832c2b00e6928d48be8d896",evidence:"E1_NONBLIND_INTERNAL_ONLY",source_rows:rows.length,cells};
}
if(typeof require!=="undefined" && require.main===module){
 const fs=require("fs"),crypto=require("crypto");
 const source=process.argv[2];if(!source)throw Error("usage: node r322_s118_exact.js path/to/original_256.csv");
 const b=fs.readFileSync(source),git=crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+b.length+"\\0"),b])).digest("hex");
 if(git!=="0cd38ecc22adc5941832c2b00e6928d48be8d896")throw Error("source blob mismatch: "+git);
 console.log(JSON.stringify(exact(b.toString("utf8")),null,2));
}
