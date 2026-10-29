"use strict";
// R265 S61 R route: direct conditional expectation grouping with exact fractions.
// All nine original R265 functions unchanged; P0 and P1 distributions frozen in protocol.
function F(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero divisor");if(d<0n){n=-n;d=-d;}let a=n<0n?-n:n,b=d;while(b){const c=a%b;a=b;b=c;}return {n:n/a,d:d/a};}
function plus(a,b){return F(a.n*b.d+b.n*a.d,a.d*b.d)}
function minus(a,b){return F(a.n*b.d-b.n*a.d,a.d*b.d)}
function times(a,b){return F(a.n*b.n,a.d*b.d)}
function over(a,b){return F(a.n*b.d,a.d*b.n)}
function fmt(a){return a.d===1n?""+a.n:a.n+"/"+a.d}
const NAMES=["ADDITIVE_WEIGHTED_123","ADDITIVE_EQUAL_FOUR","PURE_PAIR_PARITY","PURE_TRIPLE_PARITY","PURE_FOUR_PARITY","AND_PAIR","AND_FOUR","SHIFT_SCALED_PAIR_PARITY","INTERACTION_PLUS_ADDITIVE"];
function yvalue(w,v){let [a,b,c,d]=v;
if(w===NAMES[0])return a+2*b+3*c;
if(w===NAMES[1])return a+b+c+d;
if(w===NAMES[2])return (a+b)%2;
if(w===NAMES[3])return (a+b+c)%2;
if(w===NAMES[4])return (a+b+c+d)%2;
if(w===NAMES[5])return a*b;
if(w===NAMES[6])return a*b*c*d;
if(w===NAMES[7])return 7+3*((a+b)%2);
if(w===NAMES[8])return ((a+b)%2)+c+2*d;
throw Error("world");}
function projection(atoms,mask,mu){
const groups=new Map();
for(const atom of atoms){
const key=atom.x.filter((_,i)=>mask&(1<<i)).join("");
const g=groups.get(key)||{m:F(0),s:F(0)};
g.m=plus(g.m,atom.p);g.s=plus(g.s,times(atom.p,atom.y));groups.set(key,g);
}
let out=F(0);
for(const g of groups.values()){
const cond=over(g.s,g.m),delta=minus(cond,mu);
out=plus(out,times(g.m,times(delta,delta)));
}
return out;
}
function compute(){
const rows=[];
for(const w of NAMES)for(const design of ["P0_INDEPENDENT","P1_CORRELATED"]){
const atoms=[];
for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++)for(let d=0;d<2;d++){
const p=F(design==="P0_INDEPENDENT"?2:(a===b?3:1),32);
atoms.push({x:[a,b,c,d],p,y:F(yvalue(w,[a,b,c,d]))});
}
const mass=atoms.reduce((s,z)=>plus(s,z.p),F(0));if(fmt(mass)!=="1")throw Error("mass");
const mu=atoms.reduce((s,z)=>plus(s,times(z.p,z.y)),F(0));
const V=atoms.reduce((s,z)=>{const delta=minus(z.y,mu);return plus(s,times(z.p,times(delta,delta)))},F(0));
if(V.n<=0n)throw Error("nonpositive variance");
const first=[],remaining=[];
for(let k=0;k<4;k++){
first.push(over(projection(atoms,1<<k,mu),V));
remaining.push(minus(F(1),over(projection(atoms,15^(1<<k),mu),V)));
}
const sum=first.reduce(plus,F(0));
rows.push({world:w,design,mean:fmt(mu),variance:fmt(V),first:first.map(fmt),remaining:remaining.map(fmt),residual:fmt(minus(F(1),sum))});
}
return {protocol:"R265_S61_DEPENDENT_INPUT_CONDITIONAL_VARIANCE",route:"R_CONDITIONAL_PROJECTION",evidence:"E1_SYNTHETIC_NONBLIND",rows};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(compute(),null,2));
