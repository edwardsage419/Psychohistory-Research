"use strict";
// Read-only exact third route. Usage: node e078.js original_405.csv R_S44_receipt.json
function run(csv,receipt){
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t}return a||1n};
 const q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero denominator");if(b<0n){a=-a;b=-b}let d=gcd(a,b);return [a/d,b/d]};
 const p=s=>{let [a,b="1"]=String(s).split("/");return q(a,b)};
 const add=(x,y)=>q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
 const sub=(x,y)=>q(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
 const mul=(x,y)=>q(x[0]*y[0],x[1]*y[1]);
 const cmp=(x,y)=>x[0]*y[1]<y[0]*x[1]?-1:x[0]*y[1]>y[0]*x[1]?1:0;
 const abs=x=>q(x[0]<0n?-x[0]:x[0],x[1]);
 const roots={AFFINE_CONTRACT_ZERO:"0",AFFINE_CONTRACT_ONE:"1",AFFINE_ALTERNATE_CONTRACT:"0",AFFINE_EXPAND_ZERO:"0",IDENTITY_EVERY_POINT_FIXED:"0",LOGISTIC_R2:"1/2",LOGISTIC_R3_BORDER:"2/3",LOGISTIC_R4_REPELLER:"3/4",CUBIC_NONHYPERBOLIC_ATTRACTOR:"0"};
 const kinds={AFFINE_CONTRACT_ZERO:"ATTRACTOR",AFFINE_CONTRACT_ONE:"ATTRACTOR",AFFINE_ALTERNATE_CONTRACT:"ATTRACTOR",AFFINE_EXPAND_ZERO:"REPELLER",IDENTITY_EVERY_POINT_FIXED:"NEUTRAL",LOGISTIC_R2:"ATTRACTOR",LOGISTIC_R3_BORDER:"ATTRACTOR",LOGISTIC_R4_REPELLER:"REPELLER",CUBIC_NONHYPERBOLIC_ATTRACTOR:"ATTRACTOR"};
 const initials=["-1/2","-1/4","0","1/4","1/2","2/3","3/4","1","5/4"];
 const step=(w,x)=>{let one=q(1);if(w==="AFFINE_CONTRACT_ZERO")return mul(x,p("1/2"));if(w==="AFFINE_CONTRACT_ONE")return mul(add(x,one),p("1/2"));if(w==="AFFINE_ALTERNATE_CONTRACT")return mul(q(-1),mul(x,p("1/2")));if(w==="AFFINE_EXPAND_ZERO")return mul(x,q(2));if(w==="IDENTITY_EVERY_POINT_FIXED")return x;if(w.startsWith("LOGISTIC_R"))return mul(mul(q(Number(w.match(/R(\d)/)[1])),x),sub(one,x));if(w==="CUBIC_NONHYPERBOLIC_ATTRACTOR")return sub(x,mul(mul(x,x),x));throw Error("world")};
 let checks=0;const ok=(v,m)=>{checks++;if(!v)throw Error(m)};
 let lines=csv.trim().split(/\r?\n/),head=lines.shift().split(","),source=new Map();
 for(const line of lines){
  let values=line.split(","),r=Object.fromEntries(head.map((h,i)=>[h,values[i]]));
  let k=[r.world,r.observed_initial_x0,r.observed_time_step_n].join("|");
  ok(Object.hasOwn(roots,r.world)&&initials.includes(r.observed_initial_x0),"source identity");
  ok(!source.has(k),"duplicate source");source.set(k,r);
  ok(cmp(p(r.original_cohort_time_source_probability),p("1/45"))===0,"source mass");
 }
 ok(source.size===405,"source rows");ok(receipt.rows.length===81,"receipt rows");
 let summary={},warns={},seen=new Set(),total=0;
 for(const row of receipt.rows){
  let w=row.world,x0=row.x0,k=w+"|"+x0,root=p(roots[w]),x=p(x0),ds=[];
  ok(!seen.has(k),"duplicate receipt");seen.add(k);
  for(let t=0;t<5;t++){
   let src=source.get([w,x0,t].join("|"));
   ok(!!src,"missing source");ok(cmp(p(src.observed_state_xn),x)===0,"formula state");
   let d=abs(sub(x,root));ds.push(d);ok(cmp(d,p(row.distances[t]))===0,"receipt distance");
   total++;if(t<4)x=step(w,x);
  }
  let label=cmp(ds[0],q(0))===0?"AT_FIXED_EXCLUDED":cmp(ds[4],ds[0])<0?"SHRINK":cmp(ds[4],ds[0])===0?"TIE":"EXPAND";
  ok(row.label===label,"receipt label");
  let first=ds.findIndex(z=>cmp(z,q(0))===0);ok(row.first_exact_hit===(first<0?null:first),"first hit");
  let ratio=cmp(ds[0],q(0))===0?null:q(ds[4][0]*ds[0][1],ds[4][1]*ds[0][0]);
  ok(ratio===null?row.ratio===null:cmp(ratio,p(row.ratio))===0,"ratio");
  let warning=(kinds[w]!=="ATTRACTOR"&&label==="SHRINK")||(kinds[w]==="ATTRACTOR"&&label==="EXPAND");
  ok(row.warning===warning,"warning");
  summary[w]??={SHRINK:0,TIE:0,EXPAND:0,AT_FIXED_EXCLUDED:0};summary[w][label]++;
  if(warning)(warns[w]??=[]).push(x0);
 }
 ok(seen.size===81&&total===405,"universe");
 for(const w of Object.keys(roots)){
  for(const label of ["SHRINK","TIE","EXPAND","AT_FIXED_EXCLUDED"])ok(summary[w][label]===receipt.summary[w][label],"summary");
  ok((warns[w]||[]).slice().sort().join(",")===receipt.summary[w].warning_initials.slice().sort().join(","),"warning set");
 }
 ok(summary.LOGISTIC_R4_REPELLER.SHRINK===1,"repeller false positive");
 ok(summary.LOGISTIC_R2.EXPAND===3,"r2 local/global scope");
 ok(summary.LOGISTIC_R3_BORDER.EXPAND===4,"r3 local/global scope");
 return {study:"E078_R248_S44",evidence:"E1_SYNTHETIC",source_rows:source.size,trajectories:seen.size,points:total,assertions:checks,failures:0,summary,new_E2:0,new_E3:0};
}
if(typeof module!=="undefined"){module.exports={run};if(require.main===module){let fs=require("fs");if(process.argv.length!==4)throw Error("usage: node e078.js original.csv receipt.json");console.log(JSON.stringify(run(fs.readFileSync(process.argv[2],"utf8"),JSON.parse(fs.readFileSync(process.argv[3],"utf8"))),null,2));}}