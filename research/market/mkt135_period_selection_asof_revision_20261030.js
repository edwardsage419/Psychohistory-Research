"use strict";
// MKT135: exact artificial time-varying selection bounds and as-of label history.
// Run with Node.js. No dependencies, network access, personal data or paid services.
const gcd=(a,b)=>{a=a<0n?-a:a;while(b){[a,b]=[b,a%b]}return a};
const q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(!b)throw Error("denominator");if(b<0n){a=-a;b=-b}let g=gcd(a,b);return [a/g,b/g]};
const add=(a,b)=>q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const sub=(a,b)=>q(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
const mul=(a,b)=>q(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>q(a[0]*b[1],a[1]*b[0]);
const cmp=(a,b)=>a[0]*b[1]-b[0]*a[1];
const fmt=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1];
const O=q(1),Z=q(0);
function bounds(pos,neg,gamma){
  if(cmp(pos,Z)<0n||cmp(neg,Z)<0n||cmp(add(pos,neg),O)>0n||cmp(pos,Z)===0n||cmp(neg,Z)===0n||cmp(gamma,O)<0n)throw Error("invalid selection assumptions");
  let x=div(pos,add(pos,neg));
  let lo=div(x,add(mul(gamma,sub(O,x)),x));
  let hi=div(mul(gamma,x),add(sub(O,x),mul(gamma,x)));
  if(cmp(lo,pos)<0n)lo=pos;
  if(cmp(hi,sub(O,neg))>0n)hi=sub(O,neg);
  if(cmp(lo,hi)>0n)throw Error("infeasible");
  return {selected:fmt(x),lo,hi};
}
function aggregate(g1,g2){
  const a=bounds(q(1,16),q(3,16),q(g1)),b=bounds(q(3,16),q(1,16),q(g2));
  return {A:[fmt(a.lo),fmt(a.hi)],B:[fmt(b.lo),fmt(b.hi)],mean:[fmt(div(add(a.lo,b.lo),q(2))),fmt(div(add(a.hi,b.hi),q(2)))]};
}
const history=[
 {id:"X",f:q(1,4),forecast_at:0,event_at:1,versions:[[2,0],[4,1]]},
 {id:"Y",f:q(3,4),forecast_at:0,event_at:1,versions:[[2,1],[5,0]]},
 {id:"Z",f:q(1,2),forecast_at:2,event_at:3,versions:[[3,1]]}
];
function asOf(row,t){
  if(row.forecast_at>row.event_at)throw Error("future forecast");
  let prev=-1,y=null;
  for(let [time,value] of row.versions){
    if(!Number.isInteger(time)||time<=prev||time<row.event_at||(value!==0&&value!==1))throw Error("invalid label version");
    if(time<=t)y=value;
    prev=time;
  }
  return y;
}
function score(rows,t){
  let sum=Z,n=0;
  for(let row of rows){
    let y=asOf(row,t);
    if(row.forecast_at>t||row.event_at>t||y===null)continue;
    let e=sub(q(y),row.f);sum=add(sum,mul(e,e));n++;
  }
  return {n,brier:n?fmt(div(sum,q(n))):null};
}
function run(){
  let checks=0,invalid=0;
  const ok=(v,msg)=>{checks++;if(!v)throw Error("assert: "+msg)};
  const eq=(x,y)=>JSON.stringify(x)===JSON.stringify(y);
  const a=aggregate(2,2),b=aggregate(1,3),c=aggregate(3,1);
  ok(eq(a.mean,["13/35","22/35"]),"2,2 mean");
  ok(eq(b.mean,["3/8","23/40"]),"1,3 mean");
  ok(eq(c.mean,["17/40","5/8"]),"3,1 mean");
  ok(eq(a.A,["1/7","2/5"]),"2,2 A");
  ok(eq(a.B,["3/5","6/7"]),"2,2 B");
  ok(eq(b.A,["1/4","1/4"]),"1,3 A");
  ok(eq(b.B,["1/2","9/10"]),"1,3 B");
  ok(eq(c.A,["1/10","1/2"]),"3,1 A");
  ok(eq(c.B,["3/4","3/4"]),"3,1 B");
  const pooled=bounds(q(1,8),q(1,8),O);
  ok(fmt(pooled.lo)==="1/2"&&fmt(pooled.hi)==="1/2","pooled equality assumption");
  const t1=score(history,1),t3=score(history,3),t6=score(history,6);
  ok(t1.n===0&&t1.brier===null,"unavailable early");
  ok(t3.n===3&&t3.brier==="1/8","as-of score");
  ok(t6.n===3&&t6.brier==="11/24","revised score");
  ok(fmt(sub(q(11,24),q(1,8)))==="1/3","score shift");
  ok(asOf(history[0],3)===0&&asOf(history[0],6)===1,"X version");
  ok(asOf(history[1],3)===1&&asOf(history[1],6)===0,"Y version");
  ok(score([history[0]],3).brier==="1/16","old X");
  ok(score([history[0]],6).brier==="9/16","revised X");
  const reject=f=>{try{f()}catch(e){invalid++;return}throw Error("negative control accepted")};
  reject(()=>bounds(q(1,16),q(3,16),q(1,2)));
  reject(()=>bounds(Z,q(1,4),O));
  reject(()=>bounds(q(1,2),q(3,4),O));
  reject(()=>aggregate(0,1));
  reject(()=>score([{...history[0],forecast_at:2,event_at:1}],3));
  reject(()=>score([{...history[0],versions:[[2,0],[2,1]]}],3));
  reject(()=>score([{...history[0],versions:[[2,2]]}],3));
  ok(invalid===7,"all invalid rejected");
  return {id:"MKT135",scope:"synthetic E1 nonblind",gamma_2_2:a,gamma_1_3:b,gamma_3_1:c,pooled_gamma1:[fmt(pooled.lo),fmt(pooled.hi)],as_of_t1:t1,as_of_t3:t3,latest_t6:t6,score_shift:"1/3",assertions:checks,negative_controls:invalid,real_data:0};
}
if(typeof process!=="undefined"&&process.versions?.node)process.stdout.write(JSON.stringify(run(),null,2)+"\n");
