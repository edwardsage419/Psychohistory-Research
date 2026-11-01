#!/usr/bin/env node
'use strict';
// R257 S53: independent nonblind E1 projection oracle. Standard library only.
// Enumerates exact minima on the three triangle faces and the feasible interior.
// It imports neither the archived Python optimizer nor Codex PR #3.
const fs=require('node:fs'),crypto=require('node:crypto');
const RECEIPT_BLOB='37f33083b45435e18c66641ef693c6f0c779a680';
const P={
INTERIOR_OFF_GRID:['1','3/5','1/5'],BINDING_SUM_BOTH:['1','3/4','3/4'],
LOWER_X_ACTIVE:['1','-1/2','1/2'],LOWER_Y_ACTIVE:['1','1/2','-1/2'],
VERTEX_ORIGIN:['1','-1/2','-1/2'],VERTEX_RIGHT:['1','2','1/4'],
VERTEX_UPPER:['1','1/4','2'],CAPACITY_TWO_SLACK:['2','3/4','3/4']};
function need(ok,s){if(!ok)throw Error(s)}
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t}return a}
function q(a,b=1n){a=BigInt(a);b=BigInt(b);need(b!==0n,'zero denominator');if(b<0n){a=-a;b=-b}let d=gcd(a,b);return [a/d,b/d]}
function parse(s){need(typeof s==='string'&&/^-?\d+(?:\/[1-9]\d*)?$/.test(s),'rational format');let a=s.split('/');return q(a[0],a[1]||1)}
function add(a,b){return q(a[0]*b[1]+b[0]*a[1],a[1]*b[1])}
function neg(a){return [-a[0],a[1]]}
function sub(a,b){return add(a,neg(b))}
function mul(a,b){return q(a[0]*b[0],a[1]*b[1])}
function div(a,b){return q(a[0]*b[1],a[1]*b[0])}
function cmp(a,b){let z=a[0]*b[1]-b[0]*a[1];return z<0n?-1:z>0n?1:0}
function eq(a,b){return cmp(a,b)===0}
const Z=q(0),TWO=q(2);
function clamp(a,lo,hi){return cmp(a,lo)<0?lo:cmp(a,hi)>0?hi:a}
function sq(a){return mul(a,a)}
function value(x,y,a,b){return add(sq(sub(x,a)),sq(sub(y,b)))}
function opt(C,a,b){
need(cmp(C,Z)>0,'positive capacity');
let candidates=[[Z,clamp(b,Z,C)],[clamp(a,Z,C),Z]];
let x=clamp(div(add(sub(C,b),a),TWO),Z,C);
candidates.push([x,sub(C,x)]);
if(cmp(a,Z)>=0&&cmp(b,Z)>=0&&cmp(add(a,b),C)<=0)candidates.push([a,b]);
let best=null;
for(let [xx,yy] of candidates){
let v=value(xx,yy,a,b);
if(!best||cmp(v,best.v)<0)best={x:xx,y:yy,v};
}
return best;
}
function ratKey(s){let v=parse(s);return v[0]+'/'+v[1]}
function uniq(rows,field,expected){
need(Array.isArray(rows)&&rows.length===expected.length,'coverage '+field);
let m=new Map();
for(let r of rows){
need(r&&typeof r==='object'&&Object.hasOwn(r,field),'missing '+field);
let k=field==='world'?r[field]:ratKey(r[field]);
need(!m.has(k),'duplicate '+field);m.set(k,r);
}
need(expected.every(k=>m.has(k)),'universe '+field);
return m;
}
function verify(d){
need(d.research_id==='R257_S53'&&d.evidence==='E1','grade');
need(d.capacity_evaluations===40&&d.one_sided_secants===32&&d.baseline_lambdas===8,'counts');
need(d.new_human_E2===0&&d.new_history_E3===0,'E2/E3');
need(d.nonconvex_negative_control==='KKT_stationary_0_vs_feasible_-1/4','control');
let wm=uniq(d.worlds,'world',Object.keys(P));
let checks=0,secants=0,lamchecks=0;
for(let [name,params] of Object.entries(P)){
let w=wm.get(name),[C0,a,b]=params.map(parse);
need(eq(parse(w.baseline_capacity),C0),'baseline C '+name);
let ds=['-1/4','-1/16','0','1/16','1/4'];
let dm=uniq(w.perturbations,'delta',ds.map(ratKey));
let vals=new Map(),opts=new Map();
for(let s of ds){
let delta=parse(s),row=dm.get(ratKey(s)),C=add(C0,delta);
need(eq(parse(row.capacity),C),'capacity '+name+' '+s);
let out=opt(C,a,b);
need(Array.isArray(row.point)&&row.point.length===2,'point shape');
need(eq(parse(row.point[0]),out.x)&&eq(parse(row.point[1]),out.y),'projection '+name+' '+s);
need(eq(parse(row.minimum),out.v),'objective '+name+' '+s);
vals.set(ratKey(s),out.v);opts.set(ratKey(s),out);checks++;
}
let zero=opts.get(ratKey('0')),lambda;
if(cmp(add(zero.x,zero.y),C0)<0)lambda=Z;
else lambda=cmp(zero.x,Z)>0?mul(TWO,sub(a,zero.x)):mul(TWO,sub(b,zero.y));
need(cmp(lambda,Z)>=0,'dual '+name);
need(eq(parse(w.baseline_minimum),zero.v)&&eq(parse(w.baseline_lambda),lambda),'baseline '+name);
need(eq(parse(w.local_derivative),neg(lambda)),'derivative '+name);lamchecks++;
let sm=uniq(w.secants,'step',['1/4','1/16'].map(ratKey));
for(let h of ['1/4','1/16']){
let H=parse(h),s=sm.get(ratKey(h)),v0=zero.v;
let left=div(sub(v0,vals.get(ratKey('-'+h))),H);
let right=div(sub(vals.get(ratKey(h)),v0),H);
need(eq(parse(s.left_secant),left)&&eq(parse(s.right_secant),right),'secant '+name+' '+h);
need(cmp(left,neg(lambda))<=0&&cmp(neg(lambda),right)<=0&&cmp(right,Z)<=0,'convex bound '+name);secants+=2;
}
for(let s of ds){
let delta=parse(s);
need(cmp(vals.get(ratKey(s)),sub(zero.v,mul(lambda,delta)))>=0,'support '+name);
}
}
return {status:'PASS_BOUNDED_NONBLIND_E1_FACE_PROJECTION',worlds:wm.size,exact_capacity_points:checks,secant_values:secants,baseline_lambdas:lamchecks,new_E2:0,new_E3:0,external_replication:'NOT_RUN'};
}
function selftest(d){
let cases=[
['objective',x=>x.worlds[0].perturbations[0].minimum='0'],
['point',x=>x.worlds[0].perturbations[0].point[0]='0'],
['duplicate_delta',x=>x.worlds[0].perturbations[1].delta='-1/4'],
['lambda',x=>x.worlds[1].baseline_lambda='0'],
['secant',x=>x.worlds[1].secants[0].right_secant='0'],
['shrink',x=>x.worlds.pop()],
['grade',x=>x.evidence='E2'],
['duplicate_world',x=>x.worlds[0].world=x.worlds[1].world]];
for(let [name,mutate] of cases){
let copy=JSON.parse(JSON.stringify(d));mutate(copy);let rejected=false;
try{verify(copy)}catch(e){rejected=true}
need(rejected,'FALSE_ACCEPT '+name);
}
return cases.length;
}
function main(){
try{
let args=process.argv.slice(2);
need(args.length===1||(args.length===2&&args[1]==='--selftest'),'usage: node script RECEIPT.json [--selftest]');
let raw=fs.readFileSync(args[0]);
let blob=crypto.createHash('sha1').update(Buffer.from('blob '+raw.length+'\0')).update(raw).digest('hex');
need(blob===RECEIPT_BLOB,'receipt blob mismatch');
let d=JSON.parse(raw.toString('utf8'));
let out=verify(d);
out.mutation_controls=args.length===2?selftest(d):'NOT_RUN';
out.receipt_blob=blob;
console.log(JSON.stringify(out));
}catch(e){console.error('INDEPENDENT_FACE_PROJECTION_FAIL: '+e.message);process.exitCode=1}
}
if(require.main===module)main();
module.exports={verify,opt,selftest};
