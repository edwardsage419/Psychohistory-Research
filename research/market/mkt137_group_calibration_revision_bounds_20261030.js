"use strict";
const STAGES = [
 {cutoff:4,A:[0,1],B:[1,1],expected:{ece:[-1,2],brier:[-1,3],counts:[8,6,2]}},
 {cutoff:8,A:[1,1],B:[1,1],expected:{ece:[0,3],brier:[0,4],counts:[14,2,0]}},
 {cutoff:10,A:[1,1],B:[0,1],expected:{ece:[-1,3],brier:[-1,3],counts:[11,4,1]}}
];
function ensure(cond,msg){if(!cond)throw Error(msg)}
function evaluate(stage){
 ensure(Number.isInteger(stage.cutoff)&&stage.cutoff>=0,"invalid cutoff");
 for(const key of ["A","B"]){ensure(Array.isArray(stage[key])&&stage[key].length===2&&stage[key].every(v=>v===0||v===1),"invalid labels");}
 const ece=[],brier=[];let counts=[0,0,0];
 for(let mask=0;mask<16;mask++){
   const bits=[0,1,2,3].map(k=>(mask>>k)&1);
   const a=stage.A[0]+stage.A[1]+bits[0]+bits[1];
   const b=stage.B[0]+stage.B[1]+bits[2]+bits[3];
   const eceGapQuarters=Math.abs(a-1)-Math.abs(b-3);
   const brierGapEighths=a+b-4;
   ece.push(eceGapQuarters);brier.push(brierGapEighths);
   counts[eceGapQuarters>0?0:eceGapQuarters===0?1:2]++;
 }
 return {cutoff:stage.cutoff,possibleCompletions:16,eceGapQuarters:[Math.min(...ece),Math.max(...ece)],brierGapEighths:[Math.min(...brier),Math.max(...brier)],eceRankingCounts:counts};
}
function main(){
 const results=STAGES.map(evaluate);
 results.forEach((r,i)=>{
   const e=STAGES[i].expected;
   ensure(JSON.stringify(r.eceGapQuarters)===JSON.stringify(e.ece),"ECE mismatch");
   ensure(JSON.stringify(r.brierGapEighths)===JSON.stringify(e.brier),"Brier mismatch");
   ensure(JSON.stringify(r.eceRankingCounts)===JSON.stringify(e.counts),"ranking mismatch");
 });
 let rejected=0;
 for(const bad of [{cutoff:-1,A:[0,1],B:[1,1]},{cutoff:1,A:[0,2],B:[1,1]},{cutoff:1,A:[0],B:[1,1]},{cutoff:1,A:[0,1],B:[null,1]}]){
  try{evaluate(bad)}catch(e){rejected++}
 }
 ensure(rejected===4,"invalid-input controls");
 return {status:"PASS",positiveChecks:9,rejectedInvalidInputs:rejected,results};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(main(),null,2));
