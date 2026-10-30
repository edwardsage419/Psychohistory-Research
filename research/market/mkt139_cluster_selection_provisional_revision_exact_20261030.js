"use strict";
const G=[[1,0,3,4],[2,1,1,2],[3,0,1,2],[4,1,1,4]];
function gcd(a,b){while(b){let t=a%b;a=b;b=t;}return a<0n?-a:a;}
function f(a,b=1n){a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}let d=gcd(a,b);return[a/d,b/d];}
function add(a,b){return f(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function neg(a){return f(-a[0],a[1]);}
function sub(a,b){return add(a,neg(b));}
function mul(a,b){return f(a[0]*b[0],a[1]*b[1]);}
function div(a,b){if(!b[0])throw Error("zero divisor");return f(a[0]*b[1],a[1]*b[0]);}
function eq(a,b){return a[0]===b[0]&&a[1]===b[1];}
function fmt(a){return a.join("/");}
function pattern(mask){
 if(!Number.isInteger(mask)||mask<0||mask>15)throw Error("bad mask");
 let pr=f(1),den=0,num=0,ht=f(0);
 G.forEach(([n,y,p,q],i)=>{let yes=!!(mask&(1<<i)),pi=f(p,q);pr=mul(pr,yes?pi:sub(f(1),pi));if(yes){den+=n;num+=n*y;ht=add(ht,div(f(n*y,10),pi));}});
 return {mask,pr,naive:den?f(num,den):null,ht};
}
function bounds(mask,t){
 if(!Number.isInteger(t)||t<1||t>3)throw Error("bad cutoff");
 let low=0,unknown=0;
 G.forEach(([n,y],i)=>{let seen=!!(mask&(1<<i))&&!(i===3&&t===1);if(!seen){unknown+=n;return;}low+=n*(i===3&&t===2?0:y);});
 return {t,lo:f(low,10),hi:f(low+unknown,10),unknown};
}
function run(){
 let P=Array.from({length:16},(_,i)=>pattern(i)),truth=f(3,5);
 let sum=(items,fn)=>items.reduce((a,x)=>add(a,fn(x)),f(0));
 let empty=sum(P.filter(x=>!x.naive),x=>x.pr);
 let naive=div(sum(P.filter(x=>x.naive),x=>mul(x.pr,x.naive)),sub(f(1),empty));
 let ht=sum(P,x=>mul(x.pr,x.ht));
 let variance=sum(P,x=>{let d=sub(x.ht,truth);return mul(x.pr,mul(d,d));});
 let noPositive=sum(P.filter(x=>!(x.mask&2)&&!(x.mask&8)),x=>x.pr);
 let cuts=[1,2,3].map(t=>bounds(11,t)),checks=0;
 const check=(v,msg)=>{if(!v)throw Error(msg);checks++;};
 check(eq(sum(P,x=>x.pr),f(1)),"mass");
 check(eq(truth,f(3,5)),"truth");
 check(eq(empty,f(3,64)),"empty");
 check(eq(noPositive,f(3,8)),"no-positive");
 check(eq(naive,f(5189,12810)),"naive");
 check(eq(ht,truth),"HT unbiased");
 check(eq(variance,f(13,25)),"variance");
 check(eq(P[11].pr,f(3,64)),"scenario");
 check(eq(cuts[0].lo,f(1,5)),"early low");
 check(eq(cuts[0].hi,f(9,10)),"early high");
 check(eq(cuts[1].lo,f(1,5))&&eq(cuts[1].hi,f(1,2)),"provisional");
 check(eq(cuts[2].lo,f(3,5))&&eq(cuts[2].hi,f(9,10)),"revised");
 check(eq(sub(cuts[2].lo,cuts[1].lo),f(2,5)),"revision");
 check(cuts[1].hi[0]*5n<cuts[1].hi[1]*3n,"provisional falsely excludes truth");
 let rejected=0;
 for(const fn of [()=>pattern(-1),()=>pattern(16),()=>pattern(1.5),()=>bounds(1,0),()=>bounds(1,4),()=>div(f(1),f(0))])try{fn();}catch(e){rejected++;}
 check(rejected===6,"negative controls");
 return {patterns:P.length,checks,rejected,truth:fmt(truth),empty:fmt(empty),noPositive:fmt(noPositive),naiveConditional:fmt(naive),htMean:fmt(ht),htVariance:fmt(variance),scenarioProbability:fmt(P[11].pr),bounds:cuts.map(x=>({time:x.t,low:fmt(x.lo),high:fmt(x.hi),unknown:x.unknown}))};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
