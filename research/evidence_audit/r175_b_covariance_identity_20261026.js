"use strict";
const fs=require("fs");
function audit(data){
const gcd=(a,b)=>{a=a<0n?-a:a;while(b){let r=a%b;a=b;b=r;}return a;};
const F=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);let g=gcd(a,b);if(b<0n)g=-g;return {a:a/g,b:b/g};};
const Q=s=>{let v=String(s).split("/");return F(v[0],v[1]||1);};
const add=(x,y)=>F(x.a*y.b+y.a*x.b,x.b*y.b),neg=x=>F(-x.a,x.b),sub=(x,y)=>add(x,neg(y)),mul=(x,y)=>F(x.a*y.a,x.b*y.b),pow=(x,n)=>{let v=F(1);for(let k=0;k<n;k++)v=mul(v,x);return v;},str=x=>x.b===1n?String(x.a):x.a+"/"+x.b,eq=(x,y)=>x.a===y.a&&x.b===y.b;
const one=F(1),two=F(2),rows=data.matrices.filter(r=>r.rule==="posterior_sample");
let pairs=[],checks=0;
for(let p of ["1/4","1/2","3/4"])for(let e of ["1/4","1/3"]){
let pi=Q(p),eps=Q(e),gain=sub(one,mul(two,eps)),q=add(eps,mul(gain,pi)),v=mul(mul(mul(gain,gain),pi),sub(one,pi));
let lambdas=[1,3].map(n=>{let r=rows.find(x=>x.pi===p&&x.epsilon===e&&x.n===n);if(!r)throw Error("missing matrix");return sub(Q(r.T_old_to_new[1][1]),Q(r.T_old_to_new[0][1]));});
for(let lag=1;lag<=8;lag++){
let c=lambdas.map(l=>mul(v,pow(l,lag)));
let joints=c.map(cv=>[add(mul(sub(one,q),sub(one,q)),cv),sub(mul(q,sub(one,q)),cv),sub(mul(q,sub(one,q)),cv),add(mul(q,q),cv)]);
let d=sub(c[0],c[1]);if(d.a<0n)d=neg(d);let tv=mul(two,d);
for(let J of joints){if(!eq(add(add(J[0],J[1]),add(J[2],J[3])),one)||!eq(add(J[2],J[3]),q))throw Error("joint check");checks++;}
pairs.push({pi:p,epsilon:e,lag,one_time_marginal:str(q),n1_joint:joints[0].map(str),n3_joint:joints[1].map(str),TV:str(tv)});
}}
return {schema:"B_R175_covariance_identity_v1",method:"closed_form_eigenvalue_covariance_no_hidden_path_enumeration",pair_count:pairs.length,marginal_checks:checks,pairs};
}
if(require.main===module){let p=process.argv[2]||"research/R175/R175_EXACT_RESULTS.json";console.log(JSON.stringify(audit(JSON.parse(fs.readFileSync(p,"utf8"))),null,2));}
module.exports=audit;