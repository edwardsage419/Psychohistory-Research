"use strict";
// Run: node research/market/mkt071_beeminder_sqrt_synthetic_20261027.js

function audit(){
let n=0;const ck=(x,msg)=>{if(!x)throw Error(msg);n++},eq=(a,b)=>Math.abs(a-b)<1e-10;
const sum=a=>a.reduce((x,y)=>x+y,0),root=a=>Math.sqrt(sum(a)),binary=a=>a.length?1:0;
ck(eq(root([0]),0),"zero");ck(eq(root([1]),1),"one");ck(eq(root([4]),2),"four");
ck(eq(root([100]),10),"100");ck(eq(root([400]),20),"400");
ck(eq(root([200]),Math.sqrt(200)),"200");
ck(eq(root([30,70]),root([100])),"within day split");
ck(eq(sum([30,70]),100),"raw sum");ck(binary([30,70])===1,"binary");
ck(eq(root([100])+root([100]),20),"balanced two");
ck(eq(root([200])+root([0]),Math.sqrt(200)),"concentrated");
ck(eq(sum([100,100]),sum([200,0])),"same total");
ck(root([100])+root([100])>root([200])+root([0]),"regularity");
ck(eq(root([400])+root([0]),20),"400 double");
ck(eq(sum([400,0]),400),"sum contrast");
ck(root([200])-root([100])<10,"diminishing");
ck(root([100])-root([0])>root([200])-root([100]),"marginal");
ck(eq(root([100])*3,30),"three balanced");
ck(root([100])*3>root([300]),"three concentrated");
ck(eq(root([100])+root([0]),10),"retro edit new");
ck(eq(root([100])+root([100]),20),"retro edit old");
ck(sum([100,100])>root([100])+root([100]),"mode switch");
ck(eq(root([25,75]),10),"within day 2");
ck(eq(root([0,0]),0),"zeroes");
return {syntheticAssertions:n,failed:0,balancedTwoDayCredit:20,concentratedTwoDayCredit:Math.sqrt(200),oneDay400Credit:20};
}
console.log(JSON.stringify(audit(),null,2));
