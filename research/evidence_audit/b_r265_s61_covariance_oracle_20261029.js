"use strict";
// B route: independent exact covariance and conditional residual oracle.
// Frozen before R S61 output; nonblind to the historical R265 nine functions.
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a||1n;};
const q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];};
const add=(a,b)=>q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const neg=a=>[-a[0],a[1]];
const sub=(a,b)=>add(a,neg(b));
const mul=(a,b)=>q(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>q(a[0]*b[1],a[1]*b[0]);
const sq=a=>mul(a,a);
const str=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1];
const ZERO=q(0),ONE=q(1);
const names=["ADDITIVE_WEIGHTED_123","ADDITIVE_EQUAL_FOUR","PURE_PAIR_PARITY","PURE_TRIPLE_PARITY","PURE_FOUR_PARITY","AND_PAIR","AND_FOUR","SHIFT_SCALED_PAIR_PARITY","INTERACTION_PLUS_ADDITIVE"];
function output(w,x){const [a,b,c,d]=x;
switch(w){
case names[0]:return a+2*b+3*c;
case names[1]:return a+b+c+d;
case names[2]:return a^b;
case names[3]:return a^b^c;
case names[4]:return a^b^c^d;
case names[5]:return a*b;
case names[6]:return a*b*c*d;
case names[7]:return 7+3*(a^b);
case names[8]:return (a^b)+c+2*d;
default:throw Error("world");}}
function compute(){
const rows=[];
for(const w of names)for(const design of ["P0_INDEPENDENT","P1_CORRELATED"]){
const atoms=[];for(let i=0;i<16;i++){
const x=[(i>>3)&1,(i>>2)&1,(i>>1)&1,i&1];
const numerator=design==="P0_INDEPENDENT"?2:(x[0]===x[1]?3:1);
atoms.push({x,y:q(output(w,x)),p:q(numerator,32)});
}
const mass=atoms.reduce((a,z)=>add(a,z.p),ZERO);
if(str(mass)!=="1")throw Error("mass");
const mu=atoms.reduce((a,z)=>add(a,mul(z.p,z.y)),ZERO);
const ey2=atoms.reduce((a,z)=>add(a,mul(z.p,sq(z.y))),ZERO);
const V=sub(ey2,sq(mu));if(V[0]<=0n)throw Error("nonpositive variance");
const first=[],remaining=[];
for(let k=0;k<4;k++){
const ex=atoms.reduce((a,z)=>add(a,mul(z.p,q(z.x[k]))),ZERO);
const eyx=atoms.reduce((a,z)=>add(a,mul(z.p,mul(z.y,q(z.x[k])))),ZERO);
const vx=sub(ex,sq(ex));const cov=sub(eyx,mul(mu,ex));
first.push(div(sq(cov),mul(vx,V)));
const groups=new Map();
for(const z of atoms){
const key=z.x.filter((_,j)=>j!==k).join("");
const old=groups.get(key)||{p:ZERO,py:ZERO};
old.p=add(old.p,z.p);old.py=add(old.py,mul(z.p,z.y));groups.set(key,old);
}
let projected=ZERO;
for(const v of groups.values())projected=add(projected,div(sq(v.py),v.p));
const W=sub(projected,sq(mu));
remaining.push(sub(ONE,div(W,V)));
}
const sumFirst=first.reduce(add,ZERO);
rows.push({world:w,design,mean:str(mu),variance:str(V),first:first.map(str),remaining:remaining.map(str),residual:str(sub(ONE,sumFirst))});
}
return {protocol:"R265_S61_DEPENDENT_INPUT_CONDITIONAL_VARIANCE",route:"B_COVARIANCE_AND_COMPLEMENT",evidence:"E1_SYNTHETIC_NONBLIND",rows};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(compute(),null,2));
