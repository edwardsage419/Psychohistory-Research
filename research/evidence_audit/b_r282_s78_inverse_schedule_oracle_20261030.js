// Independent inverse-transition oracle for R282 S78. Does not import the enumerator.
function computeB(){
 const S=["SYNC","A_THEN_B","B_THEN_A"],regimes=["TERMINAL","TRACE","TRACE_E0","TRACE_EALL"];
 const groups=Object.fromEntries(regimes.map(r=>[r,new Map()]));
 function inv(s,old,next){let a=+old[0],b=+old[1],x=+next[0],y=+next[1];if(s==="SYNC")return ""+(x^b)+(y^a);if(s==="A_THEN_B")return ""+(x^b)+(y^x);return ""+(x^y)+(y^a)}
 for(let si=0;si<3;si++)for(let i=0;i<4;i++)for(let j=0;j<4;j++)for(let k=0;k<4;k++){
  let t0=i.toString(2).padStart(2,"0"),t1=j.toString(2).padStart(2,"0"),t2=k.toString(2).padStart(2,"0"),s=S[si],e0=inv(s,t0,t1),e1=inv(s,t1,t2);
  let obs={TERMINAL:t2,TRACE:t0+t1+t2,TRACE_E0:t0+t1+t2+e0,TRACE_EALL:t0+t1+t2+e0+e1};
  for(let r of regimes){let m=groups[r],a=m.get(obs[r])||[0,0,0];a[si]++;m.set(obs[r],a)}
 }
 const gcd=(a,b)=>b?gcd(b,a%b):a;const rat=(a,b)=>{let g=gcd(a,b);return (b/g===1)?String(a/g):a/g+"/"+b/g};
 let results=[];
 for(let r of regimes){let m=groups[r],conf=[[0,0,0],[0,0,0],[0,0,0]],correct=0,ties=0,tv=[];
  for(let c of m.values()){let max=Math.max(...c),pick=c.indexOf(max);correct+=max;if(c.filter(n=>n===max).length>1)ties+=c.reduce((x,y)=>x+y,0);for(let i=0;i<3;i++)conf[i][pick]+=c[i]}
  for(let i=0;i<3;i++)for(let j=0;j<3;j++){let d=0;for(let c of m.values())d+=Math.abs(c[i]-c[j]);tv.push({from:S[i],to:S[j],distance:rat(d,128)})}
  results.push({name:r,observations:m.size,accuracy:rat(correct,192),correct_sources:correct,tie_mass:rat(ties,192),tie_sources:ties,confusion:conf,tv});
 }
 return results;
}
if(typeof require!=="undefined" && require.main===module){const fs=require("fs");const p=process.argv[2];const result=computeB();if(p){const obj=JSON.parse(fs.readFileSync(p,"utf8"));if(JSON.stringify(obj.regimes)!==JSON.stringify(result))throw Error("B oracle discrepancy");}console.log(JSON.stringify(result.map(x=>({name:x.name,accuracy:x.accuracy,tie_mass:x.tie_mass}))))}
