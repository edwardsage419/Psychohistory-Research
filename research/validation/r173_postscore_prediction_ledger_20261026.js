// R173 postscore supplementary diagnostic, fixed source CSV, no refitting.
// Usage: node <script.js> path/to/R173_REAL_EA_SCCS_LOSO_HELDOUT_PREDICTIONS.csv
// Node.js standard library only. Existing frozen M0/M1 probabilities remain unchanged.
const fs=require("fs"),crypto=require("crypto");
const path=process.argv[2];if(!path)throw Error("Provide CSV path");
const raw=fs.readFileSync(path);const digest=crypto.createHash("sha256").update(raw).digest("hex");
if(digest!=="f65271786d0a1c6f58fa43c316db62d60d8064f64356088cc163b549c6996b2e")throw Error("SHA256 source mismatch: "+digest);

function parseRows(csv){
  const lines=csv.trimEnd().split(/\r?\n/),hdr=lines.shift().split(",");
  if(hdr.length!==22)throw Error("column count "+hdr.length);
  const rows=lines.map((l,i)=>{
    const a=l.split(",");if(a.length!==22)throw Error("CSV fields row "+(i+2)+"="+a.length);
    const p0=a.slice(8,15).map(Number),p1=a.slice(15,22).map(Number);
    return {sample:a[0],id:a[1],x:Number(a[2]),y:Number(a[3]),years:Number(a[4]),sccs:Number(a[5]),loss0:Number(a[6]),loss1:Number(a[7]),p0,p1};
  });
  return rows;
}
function primary(rows){
 const expected={SCCS_186:186,EA_1271:1271,SCCS_COMPLETE_SOURCE_YEARS:183,EA_COMPLETE_SOURCE_YEARS:1259};
 const groups={};for(const row of rows)(groups[row.sample]??=[]).push(row);
 const res={input_rows:rows.length,groups:{},cross_sample:{},checks:{probability_max_error:0,logloss_max_error:0,invalid_rows:0}};
 if(rows.length!==2899)throw Error("rows mismatch");
 for(const [name,n] of Object.entries(expected)){
  const rs=groups[name]??[];if(rs.length!==n)throw Error("group "+name+" "+rs.length);
  if(new Set(rs.map(r=>r.id)).size!==n)throw Error("duplicate society "+name);
  let log0=0,log1=0,brier0=0,brier1=0;const byX={},byY={};
  const del=(key,group)=>{const arr=group[key]??(group[key]=[]);return arr};
  const influence=[];
  for(const r of rs){
    if(!Number.isInteger(r.x)||r.x<0||r.x>9||!Number.isInteger(r.y)||r.y<1||r.y>7)throw Error("bad codes "+r.id);
    for(const p of [r.p0,r.p1]){
      if(p.some(x=>!Number.isFinite(x)||x<=0||x>1))throw Error("invalid p "+r.id);
      const err=Math.abs(p.reduce((a,b)=>a+b,0)-1);
      res.checks.probability_max_error=Math.max(res.checks.probability_max_error,err);
      if(err>1e-12)throw Error("p not normalized "+r.id);
    }
    const l0=-Math.log(r.p0[r.y-1]),l1=-Math.log(r.p1[r.y-1]);
    const err=Math.max(Math.abs(l0-r.loss0),Math.abs(l1-r.loss1));
    res.checks.logloss_max_error=Math.max(res.checks.logloss_max_error,err);
    if(err>1e-12)throw Error("log loss mismatch "+r.id);
    const b0=r.p0.reduce((a,p,k)=>a+(p-(k===r.y-1?1:0))**2,0);
    const b1=r.p1.reduce((a,p,k)=>a+(p-(k===r.y-1?1:0))**2,0);
    log0+=l0;log1+=l1;brier0+=b0;brier1+=b1;
    const d=l0-l1;
    del(r.x,byX).push(d);del(r.y,byY).push(d);
    influence.push({society_id:r.id,x:r.x,y:r.y,delta:d});
  }
  const mean=(a)=>a.reduce((x,y)=>x+y,0)/a.length;
  const strata=(g,all)=>Object.fromEntries(all.map(k=>{const v=g[k]??[];return [k,{n:v.length,delta_sum:v.reduce((a,b)=>a+b,0),delta_mean:v.length?mean(v):null}]}));
  const groupLeave=(g,all)=>Object.fromEntries(all.map(k=>{const v=g[k]??[];return [k,v.length===n?null:{removed:v.length,remaining:n-v.length,delta_remaining:(log0-log1-v.reduce((a,b)=>a+b,0))/(n-v.length)}]}));
  influence.sort((a,b)=>Math.abs(b.delta)-Math.abs(a.delta)||a.society_id.localeCompare(b.society_id));
  res.groups[name]={n,mean_log_loss_M0:log0/n,mean_log_loss_M1:log1/n,delta_log_loss_M0_minus_M1:(log0-log1)/n,mean_brier_M0:brier0/n,mean_brier_M1:brier1/n,delta_brier_M0_minus_M1:(brier0-brier1)/n,by_agriculture:strata(byX,Array.from({length:10},(_,i)=>i)),by_marriage:strata(byY,[1,2,3,4,5,6,7]),drop_agriculture_stratum:groupLeave(byX,Array.from({length:10},(_,i)=>i)),drop_marriage_class:groupLeave(byY,[1,2,3,4,5,6,7]),top5_absolute_influence:influence.slice(0,5)};
 }
 const idx=(arr)=>new Map(arr.map(r=>[r.id,r]));
 for(const [a,b] of [["SCCS_186","EA_1271"],["SCCS_COMPLETE_SOURCE_YEARS","SCCS_186"],["EA_COMPLETE_SOURCE_YEARS","EA_1271"]]){
   const A=idx(groups[a]),B=idx(groups[b]);let overlap=0,labels=0,probDiff=0,maxProb=0;
   for(const [id,r] of A){if(!B.has(id))continue;overlap++;const q=B.get(id);if(r.x!==q.x||r.y!==q.y)labels++;const d=Math.max(...r.p0.map((v,i)=>Math.abs(v-q.p0[i])),...r.p1.map((v,i)=>Math.abs(v-q.p1[i])));if(d>1e-12)probDiff++;maxProb=Math.max(maxProb,d)}
   res.cross_sample[a+"_vs_"+b]={overlap,identity_label_conflicts:labels,probabilities_differ:probDiff,max_probability_difference:maxProb};
 }
 return res;
}
const rows=parseRows(raw.toString('utf8'));console.log(JSON.stringify(primary(rows),null,2));
