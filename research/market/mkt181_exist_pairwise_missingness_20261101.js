#!/usr/bin/env node
"use strict";
const result=(function(){
function correlation(pairs){
  const n=pairs.length;let sx=0,sy=0,sxx=0,syy=0,sxy=0;
  for(const [x,y] of pairs){sx+=x;sy+=y;sxx+=x*x;syy+=y*y;sxy+=x*y;}
  const covarianceNumerator=n*sxy-sx*sy,varianceX=n*sxx-sx*sx,varianceY=n*syy-sy*sy;
  if(varianceX<=0||varianceY<=0)throw Error("degenerate correlation");
  return {n,covarianceNumerator,varianceX,varianceY,r:covarianceNumerator/Math.sqrt(varianceX*varianceY)};
}
const days=Array.from({length:31},(_,i)=>({day:i+1,x:i+1,y:i<21?i+1:null}));
const complete=correlation(days.filter(z=>z.y!==null).map(z=>[z.x,z.y]));
const zeroFilled=correlation(days.map(z=>[z.x,z.y===null?0:z.y]));
const check=(v,msg)=>{if(!v)throw Error(msg);};
check(days.length===31,"31 days");
check(days.filter(z=>z.y!==null).length===21,"21 observed");
check(days.filter(z=>z.y===null).length===10,"10 missing");
check(complete.n===21&&complete.covarianceNumerator===16170,"complete covariance");
check(complete.r===1,"complete correlation");
check(zeroFilled.n===31&&zeroFilled.covarianceNumerator===-11935,"zero filled covariance");
check(zeroFilled.varianceX===76880&&zeroFilled.varianceY===49280,"zero filled variances");
check(zeroFilled.r<0&&Math.abs(zeroFilled.r+0.19390115071860714)<1e-12,"sign flip");
return {complete,zeroFilled,missingDays:10,assertions:8,synthetic:true};

})();
console.log(JSON.stringify(result,null,2));
