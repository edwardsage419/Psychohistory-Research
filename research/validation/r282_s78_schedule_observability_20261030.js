// R282 S78 complete source enumeration, zero dependencies, nonblind artificial E1.
function computeR(){
 const schedules=["SYNC","A_THEN_B","B_THEN_A"],regimes=["TERMINAL","TRACE","TRACE_E0","TRACE_EALL"];
 const groups=Object.fromEntries(regimes.map(x=>[x,new Map()]));const rows=[],paired={};
 function step(a,b,ea,eb,s){if(s==="SYNC")return [b^ea,a^eb];if(s==="A_THEN_B"){let x=b^ea;return [x,x^eb]}let y=a^eb;return [y^ea,y]}
 for(let si=0;si<3;si++){let s=schedules[si];for(let i=0;i<64;i++){
   let bits=i.toString(2).padStart(6,"0"),[a,b,ea0,eb0,ea1,eb1]=[...bits].map(Number);
   let t0=""+a+b;let [x,y]=step(a,b,ea0,eb0,s),t1=""+x+y;let [u,v]=step(x,y,ea1,eb1,s),t2=""+u+v;
   let obs={TERMINAL:t2,TRACE:t0+t1+t2,TRACE_E0:t0+t1+t2+ea0+eb0,TRACE_EALL:t0+t1+t2+ea0+eb0+ea1+eb1};
   rows.push({schedule:s,source_index:i,source_bits:bits,t0,t1,t2,eA0:ea0,eB0:eb0,eA1:ea1,eB1:eb1,...obs});
   for(let r of regimes){let g=groups[r],arr=g.get(obs[r])||[0,0,0];arr[si]++;g.set(obs[r],arr)}
 }}
 const result={study:"R282_S78",freeze_commit:"def580607b81df0873fd54cd73ceff991f19e863",evidence:"E1_INTERNAL_NONBLIND_ARTIFICIAL",schedules,source_cases:192,source_mass:"1/192",regimes:[]};
 const gcd=(a,b)=>b?gcd(b,a%b):a;const rat=(a,b)=>{let g=gcd(a,b);return (b/g===1)?String(a/g):a/g+"/"+b/g};
 for(let r of regimes){
  let g=groups[r],conf=Array.from({length:3},()=>[0,0,0]),wins=0,ties=0,tv=[];
  for(let [key,c] of g){let mx=Math.max(...c),pick=c.indexOf(mx);wins+=mx;if(c.filter(x=>x===mx).length>1)ties+=c.reduce((a,b)=>a+b,0);for(let i=0;i<3;i++)conf[i][pick]+=c[i]}
  for(let i=0;i<3;i++)for(let j=0;j<3;j++){let d=0;for(let c of g.values())d+=Math.abs(c[i]-c[j]);tv.push({from:schedules[i],to:schedules[j],distance:rat(d,128)})}
  result.regimes.push({name:r,observations:g.size,accuracy:rat(wins,192),correct_sources:wins,tie_mass:rat(ties,192),tie_sources:ties,confusion:conf,tv});
  for(let i=0;i<3;i++){let n=0;for(let c of g.values())n+=c[i];if(n!==64)throw Error("incomplete "+r+" "+i)}
 }
 const by=Object.fromEntries(schedules.map(s=>[s,rows.filter(x=>x.schedule===s)]));
 for(let s of schedules){let cnt=[0,0,0,0];for(let x of by[s])cnt[["00","01","10","11"].indexOf(x.t2)]++;if(cnt.some(n=>n!==16))throw Error("original R282 marginal failure")}
 for(let s of schedules.slice(1)){let t1=0,t2=0;for(let i=0;i<64;i++){t1+=(by[s][i].t1!==by.SYNC[i].t1);t2+=(by[s][i].t2!==by.SYNC[i].t2)}if(t1!==32||t2!==48)throw Error("original R282 paired mismatch");paired[s]=[t1,t2]}
 if(result.regimes.some((x,i)=>i>0&&Number(x.correct_sources)<Number(result.regimes[i-1].correct_sources)))throw Error("nonmonotone");
 result.original_R282_paired_counts=paired;result.R073="FROZEN";result.PESEN_v0_1="FROZEN";result.new_E2=0;result.new_E3=0;
 const fields=["schedule","source_index","source_bits","t0","t1","t2","eA0","eB0","eA1","eB1","TERMINAL","TRACE","TRACE_E0","TRACE_EALL"];
 const csv=fields.join(",")+"\n"+rows.map(x=>fields.map(f=>String(x[f])).join(",")).join("\n")+"\n";
 return {result,rows,csv};
}
if(typeof require!=="undefined" && require.main===module){const fs=require("fs"),path=require("path");const out=process.argv[2]||".";const x=computeR();fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,"R282_S78_ALL_192_SOURCE_OBSERVATIONS.csv"),x.csv);fs.writeFileSync(path.join(out,"R282_S78_EXACT_RESULTS.json"),JSON.stringify(x.result,null,2)+"\n");console.log(JSON.stringify(x.result.regimes.map(y=>({name:y.name,accuracy:y.accuracy,tie_mass:y.tie_mass}))))}
