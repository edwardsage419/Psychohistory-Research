// R282 S78 independent strict persisted receipt gate. No import of R enumerator.
function inverseOracle(){
 const S=["SYNC","A_THEN_B","B_THEN_A"],regimes=["TERMINAL","TRACE","TRACE_E0","TRACE_EALL"],groups=Object.fromEntries(regimes.map(r=>[r,new Map()]));
 function inv(s,old,next){let a=+old[0],b=+old[1],x=+next[0],y=+next[1];if(s==="SYNC")return ""+(x^b)+(y^a);if(s==="A_THEN_B")return ""+(x^b)+(y^x);return ""+(x^y)+(y^a)}
 for(let si=0;si<3;si++)for(let i=0;i<4;i++)for(let j=0;j<4;j++)for(let k=0;k<4;k++){
  let t0=i.toString(2).padStart(2,"0"),t1=j.toString(2).padStart(2,"0"),t2=k.toString(2).padStart(2,"0"),s=S[si],e0=inv(s,t0,t1),e1=inv(s,t1,t2),obs={TERMINAL:t2,TRACE:t0+t1+t2,TRACE_E0:t0+t1+t2+e0,TRACE_EALL:t0+t1+t2+e0+e1};
  for(let r of regimes){let m=groups[r],a=m.get(obs[r])||[0,0,0];a[si]++;m.set(obs[r],a)}
 }
 const gcd=(a,b)=>b?gcd(b,a%b):a,rat=(a,b)=>{let g=gcd(a,b);return b/g===1?String(a/g):a/g+"/"+b/g};let results=[];
 for(let r of regimes){let m=groups[r],conf=[[0,0,0],[0,0,0],[0,0,0]],correct=0,ties=0,tv=[];
  for(let c of m.values()){let max=Math.max(...c),pick=c.indexOf(max);correct+=max;if(c.filter(n=>n===max).length>1)ties+=c.reduce((x,y)=>x+y,0);for(let i=0;i<3;i++)conf[i][pick]+=c[i]}
  for(let i=0;i<3;i++)for(let j=0;j<3;j++){let d=0;for(let c of m.values())d+=Math.abs(c[i]-c[j]);tv.push({from:S[i],to:S[j],distance:rat(d,128)})}
  results.push({name:r,observations:m.size,accuracy:rat(correct,192),correct_sources:correct,tie_mass:rat(ties,192),tie_sources:ties,confusion:conf,tv});
 }return results;
}
function strictGate(csv,json){
 const expectedHeader="schedule,source_index,source_bits,t0,t1,t2,eA0,eB0,eA1,eB1,TERMINAL,TRACE,TRACE_E0,TRACE_EALL";
 const lines=csv.trimEnd().split(/\r?\n/);if(lines.shift()!==expectedHeader)throw Error("HEADER");
 if(lines.length!==192)throw Error("ROW_UNIVERSE");
 const seen=new Set(),S=["SYNC","A_THEN_B","B_THEN_A"];
 for(let line of lines){
  let v=line.split(",");if(v.length!==14)throw Error("ROW_FIELDS");
  let [s,index,bits,t0,t1,t2,eA0,eB0,eA1,eB1,terminal,trace,traceE0,traceAll]=v;
  if(!S.includes(s)||!/^(0|[1-9][0-9]*)$/.test(index)||+index>63)throw Error("KEY");
  let key=s+":"+index;if(seen.has(key))throw Error("DUPLICATE");seen.add(key);
  if(bits!==Number(index).toString(2).padStart(6,"0")||!/^([01]{2})$/.test(t0)||!/^([01]{2})$/.test(t1)||!/^([01]{2})$/.test(t2)||t0!==bits.slice(0,2)||eA0+eB0+eA1+eB1!==bits.slice(2))throw Error("SOURCE");
  function invert(old,next){let a=+old[0],b=+old[1],x=+next[0],y=+next[1];if(s==="SYNC")return ""+(x^b)+(y^a);if(s==="A_THEN_B")return ""+(x^b)+(y^x);return ""+(x^y)+(y^a)}
  if(invert(t0,t1)!==eA0+eB0||invert(t1,t2)!==eA1+eB1)throw Error("INVERSE_TRANSITION");
  if(terminal!==t2||trace!==t0+t1+t2||traceE0!==trace+eA0+eB0||traceAll!==traceE0+eA1+eB1)throw Error("OBSERVATION");
 }
 for(let s of S)for(let i=0;i<64;i++)if(!seen.has(s+":"+i))throw Error("MISSING_SOURCE");
 const o=JSON.parse(json);if(o.study!=="R282_S78"||o.freeze_commit!=="def580607b81df0873fd54cd73ceff991f19e863"||o.evidence!=="E1_INTERNAL_NONBLIND_ARTIFICIAL"||o.source_cases!==192||o.source_mass!=="1/192"||o.R073!=="FROZEN"||o.PESEN_v0_1!=="FROZEN"||o.new_E2!==0||o.new_E3!==0)throw Error("METADATA");
 if(JSON.stringify(o.regimes)!==JSON.stringify(inverseOracle()))throw Error("INVERSE_ORACLE_MISMATCH");
 return {rows:lines.length,regimes:o.regimes.length,independent_schedule_state_triples:192,tv_cells:o.regimes.reduce((s,x)=>s+x.tv.length,0)};
}
if(typeof require!=="undefined"&&require.main===module){const fs=require("fs");if(process.argv.length<4)throw Error("CSV JSON paths required");console.log(JSON.stringify(strictGate(fs.readFileSync(process.argv[2],"utf8"),fs.readFileSync(process.argv[3],"utf8"))))}
