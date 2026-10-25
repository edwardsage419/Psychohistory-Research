"use strict";
// Independent B audit: recover full 3x3 matrix from observable entries K00 and K21.
// No parameter (f,u,m) is consulted. Run with frozen R168_EXACT_RESULTS.json.
const fs=require("fs");
const gcd=(a,b)=>{a=a<0n?-a:a;while(b){[a,b]=[b,a%b]}return a};
const q=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d}if(!d)throw Error("zero");const g=gcd(n,d);return [n/g,d/g]};
const parse=x=>{const z=String(x).split("/");return q(z[0],z[1]||1)};
const str=x=>x[1]===1n?String(x[0]):x[0]+"/"+x[1];
const add=(x,y)=>q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
const mul=(x,y)=>q(x[0]*y[0],x[1]*y[1]);
const sub=(x,y)=>add(x,q(-y[0],y[1]));
const O=q(1),Z=q(0);
function check(K){
 const A=K[0][0],B=K[2][1],R=[[A,sub(O,A),Z],[mul(A,B),mul(A,sub(O,B)),sub(O,A)],[Z,B,sub(O,B)]];
 let mismatches=0;for(let i=0;i<3;i++)for(let j=0;j<3;j++)if(str(R[i][j])!==str(K[i][j]))mismatches++;
 return mismatches;
}
function main(doc){
 if(doc.kernels.length!==32)throw Error("kernel count");
 let verified=0,mutants=0,byObservation=new Map(),byFull=new Map();
 for(const k of doc.kernels){
  const K=k.kernel.map(r=>r.map(parse));
  if(check(K)!==0)throw Error("observable reconstruction failed");
  verified+=9;
  const obs=str(K[0][0])+"|"+str(K[2][1]),full=K.map(r=>r.map(str).join(",")).join(";");
  for(const [map,key] of [[byObservation,obs],[byFull,full]]){if(!map.has(key))map.set(key,0);map.set(key,map.get(key)+1)}
  const altered1=K.map(r=>r.slice());altered1[1][0]=add(altered1[1][0],q(1,100));if(check(altered1)<1)throw Error("row1 mutant undetected");mutants++;
  const altered2=K.map(r=>r.slice());altered2[2][1]=add(altered2[2][1],q(1,100));if(check(altered2)<1)throw Error("row2 mutant undetected");mutants++;
 }
 const sorted=m=>[...m.values()].sort((a,b)=>b-a);
 if(JSON.stringify(sorted(byObservation))!==JSON.stringify(sorted(byFull)))throw Error("partition mismatch");
 return {id:"B_R168_OBSERVABLE_KERNEL_RECONSTRUCTION",evidence:"E1_INTERNAL_DIFFERENT_METHOD",original_kernels:32,verified_cells:verified,unique_observable_pairs:byObservation.size,unique_full_kernels:byFull.size,class_sizes:sorted(byObservation),executed_negative_controls:mutants,negative_control_failures:0,external_independent_replications:0,E2:0,E3:0};
}
if(require.main===module){console.log(JSON.stringify(main(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2))}
module.exports={main};