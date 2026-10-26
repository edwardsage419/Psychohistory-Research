"use strict";
const fs=require("fs");
function compute(data){
const gcd=(a,b)=>{a=a<0n?-a:a;while(b){let t=a%b;a=b;b=t;}return a;};
const f=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}let g=gcd(a,b);return [a/g,b/g];};
const q=s=>{let p=String(s).split("/");return f(p[0],p[1]||1);};
const add=(x,y)=>f(x[0]*y[1]+y[0]*x[1],x[1]*y[1]),sub=(x,y)=>f(x[0]*y[1]-y[0]*x[1],x[1]*y[1]),mul=(x,y)=>f(x[0]*y[0],x[1]*y[1]),div=(x,y)=>f(x[0]*y[1],x[1]*y[0]),abs=x=>f(x[0]<0n?-x[0]:x[0],x[1]),s=x=>x[1]===1n?String(x[0]):x[0]+"/"+x[1],eq=(x,y)=>x[0]===y[0]&&x[1]===y[1];
const z=f(0),one=f(1),two=f(2),half=f(1,2),M=A=>A.map(r=>r.map(q));
const mm=(A,B)=>[0,1].map(i=>[0,1].map(j=>add(mul(A[i][0],B[0][j]),mul(A[i][1],B[1][j]))));
const power=(A,n)=>{let X=[[one,z],[z,one]];for(let k=0;k<n;k++)X=mm(X,A);return X;};
const obs=(h,v,e)=>h===v?sub(one,e):e;
const joint=(T,pi,e,lag)=>{let P=power(T,lag),J=[z,z,z,z];for(let h=0;h<2;h++)for(let k=0;k<2;k++)for(let x=0;x<2;x++)for(let y=0;y<2;y++)J[2*x+y]=add(J[2*x+y],mul(mul(mul(h?pi:sub(one,pi),P[h][k]),obs(h,x,e)),obs(k,y,e)));return J;};
const TV=(A,B)=>div(A.reduce((a,v,i)=>add(a,abs(sub(v,B[i]))),z),two);
let rows=data.matrices.filter(r=>r.rule==="posterior_sample");if(rows.length!==12)throw Error("wrong matrix count");
let pairs=[],pos=0,min=null,max=null,self0=0,blind0=0;
for(let p of ["1/4","1/2","3/4"])for(let e of ["1/4","1/3"]){
let r=rows.filter(x=>x.pi===p&&x.epsilon===e);if(r.length!==2)throw Error("missing group");
let A=M(r.find(x=>x.n===1).T_old_to_new),B=M(r.find(x=>x.n===3).T_old_to_new),pi=q(p),eps=q(e);
for(let T of [A,B])if(!eq(add(mul(sub(one,pi),T[0][1]),mul(pi,T[1][1])),pi))throw Error("prior not invariant");
for(let lag=1;lag<=8;lag++){
let X=joint(A,pi,eps,lag),Y=joint(B,pi,eps,lag),d=TV(X,Y);
for(let J of [X,Y]){if(!eq(J.reduce(add,z),one))throw Error("normalization");for(let v of J)if(v[0]<0n||v[0]>v[1])throw Error("invalid probability");if(!eq(add(J[2],J[3]),add(J[1],J[3])))throw Error("nonstationary report");}
if(!eq(add(X[2],X[3]),add(Y[2],Y[3])))throw Error("different one-time marginal");
if(d[0]>0n)pos++;if(min===null||min[0]*d[1]>d[0]*min[1])min=d;if(max===null||max[0]*d[1]<d[0]*max[1])max=d;
if(eq(TV(X,X),z))self0++;if(eq(TV(joint(A,pi,half,lag),joint(B,pi,half,lag)),z))blind0++;
pairs.push({pi:p,epsilon:e,lag,one_time_marginal:s(add(X[2],X[3])),n1_joint:X.map(s),n3_joint:Y.map(s),TV:s(d),equal_prior_Bayes_error:s(div(sub(one,d),two))});
}}
if(pairs.length!==48||self0!==48||blind0!==48)throw Error("negative controls failed");
return {schema:"R175_noisy_two_time_joint_v1",source_blob:"98da532e3656ff86caf5238d5174d211e3ca28d3",protocol:"protocols/R175_NOISY_TWO_TIME_OBSERVABILITY_THIRD_METHOD_FREEZE_2026-10-26.md",method:"exact_16_hidden_observed_combinations",pair_count:48,full_joint_probability_cells:384,positive_TV_count:pos,min_TV:s(min),max_TV:s(max),self_TV_zero_count:self0,blind_observation_TV_zero_count:blind0,pairs};
}
if(require.main===module){let p=process.argv[2]||"research/R175/R175_EXACT_RESULTS.json";console.log(JSON.stringify(compute(JSON.parse(fs.readFileSync(p,"utf8"))),null,2));}
module.exports=compute;