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
function independent(rows){
 const groups={};for(const r of rows)(groups[r.sample]??=[]).push(r);
 const out={checked_rows:0,checked_probabilities:0,max_abs_probability_error:0,max_abs_brier_difference:0,failed_rows:0};
 for(const rs of Object.values(groups)){
  const n=rs.length;
  const cntY=Array(7).fill(0),cntX=Array(10).fill(0),cntXY=Array.from({length:10},()=>Array(7).fill(0));
  for(const r of rs){cntY[r.y-1]++;cntX[r.x]++;cntXY[r.x][r.y-1]++}
  for(const r of rs){
    const p0=Array.from({length:7},(_,k)=>(cntY[k]-(r.y-1===k?1:0)+1)/(n-1+7));
    const p1=Array.from({length:7},(_,k)=>(cntXY[r.x][k]-(r.y-1===k?1:0)+10*p0[k])/(cntX[r.x]-1+10));
    const err=Math.max(...p0.map((v,k)=>Math.abs(v-r.p0[k])),...p1.map((v,k)=>Math.abs(v-r.p1[k])));
    out.max_abs_probability_error=Math.max(out.max_abs_probability_error,err);out.checked_probabilities+=14;
    const alt=(p)=>1-2*p[r.y-1]+p.reduce((s,x)=>s+x*x,0);
    const dir=(p)=>p.reduce((s,x,k)=>s+(x-(k===r.y-1?1:0))**2,0);
    out.max_abs_brier_difference=Math.max(out.max_abs_brier_difference,Math.abs(alt(r.p0)-dir(r.p0)),Math.abs(alt(r.p1)-dir(r.p1)));
    if(err>1e-12)out.failed_rows++;out.checked_rows++;
  }
 }
 if(out.checked_rows!==2899||out.failed_rows)throw Error("INDEPENDENT_FAIL "+JSON.stringify(out));
 return out;
}
const rows=parseRows(raw.toString('utf8'));console.log(JSON.stringify(independent(rows),null,2));
