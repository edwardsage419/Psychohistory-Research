"use strict";
// Exact finite-time diagnostic; no floating-point thresholds.
const G=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t}return a||1n};
const Q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b}if(!b)throw Error("zero denominator");let g=G(a,b);return [a/g,b/g]};
const P=s=>{let x=String(s).split("/");return Q(x[0],x[1]||1)};
const A=(x,y)=>Q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
const N=x=>[-x[0],x[1]],S=(x,y)=>A(x,N(y)),M=(x,y)=>Q(x[0]*y[0],x[1]*y[1]);
const ABS=x=>[x[0]<0n?-x[0]:x[0],x[1]];
const C=(x,y)=>x[0]*y[1]<y[0]*x[1]?-1:x[0]*y[1]>y[0]*x[1]?1:0;
const T=x=>x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);
const roots={"AFFINE_CONTRACT_ZERO":"0","AFFINE_CONTRACT_ONE":"1","AFFINE_ALTERNATE_CONTRACT":"0","AFFINE_EXPAND_ZERO":"0","IDENTITY_EVERY_POINT_FIXED":"0","LOGISTIC_R2":"1/2","LOGISTIC_R3_BORDER":"2/3","LOGISTIC_R4_REPELLER":"3/4","CUBIC_NONHYPERBOLIC_ATTRACTOR":"0"};
const kinds={"AFFINE_CONTRACT_ZERO":"ATTRACTOR","AFFINE_CONTRACT_ONE":"ATTRACTOR","AFFINE_ALTERNATE_CONTRACT":"ATTRACTOR","AFFINE_EXPAND_ZERO":"REPELLER","IDENTITY_EVERY_POINT_FIXED":"NEUTRAL","LOGISTIC_R2":"ATTRACTOR","LOGISTIC_R3_BORDER":"ATTRACTOR","LOGISTIC_R4_REPELLER":"REPELLER","CUBIC_NONHYPERBOLIC_ATTRACTOR":"ATTRACTOR"};
const initials=["-1/2","-1/4","0","1/4","1/2","2/3","3/4","1","5/4"];
function map(w,x){let one=Q(1);if(w==="AFFINE_CONTRACT_ZERO")return M(x,P("1/2"));if(w==="AFFINE_CONTRACT_ONE")return M(A(x,one),P("1/2"));if(w==="AFFINE_ALTERNATE_CONTRACT")return N(M(x,P("1/2")));if(w==="AFFINE_EXPAND_ZERO")return M(x,Q(2));if(w==="IDENTITY_EVERY_POINT_FIXED")return x;if(w==="LOGISTIC_R2")return M(M(Q(2),x),S(one,x));if(w==="LOGISTIC_R3_BORDER")return M(M(Q(3),x),S(one,x));if(w==="LOGISTIC_R4_REPELLER")return M(M(Q(4),x),S(one,x));if(w==="CUBIC_NONHYPERBOLIC_ATTRACTOR")return S(x,M(M(x,x),x));throw Error("world");}
function run(csv){let lines=csv.trim().split(/\r?\n/),headers=lines.shift().split(","),group={},seen=new Set(),checks=0;
for(let line of lines){let v=line.split(","),r=Object.fromEntries(headers.map((k,i)=>[k,v[i]])),w=r.world,x=r.observed_initial_x0,n=Number(r.observed_time_step_n),key=w+"|"+x+"|"+n;
if(!(w in roots)||!initials.includes(x)||n<0||n>4||!Number.isInteger(n)||seen.has(key))throw Error("source key");seen.add(key);checks++;
if(C(P(r.original_cohort_time_source_probability),P("1/45"))!==0)throw Error("mass");checks++;
group[w]??={};group[w][x]??=[];group[w][x][n]=P(r.observed_state_xn);
}
if(lines.length!==405||Object.keys(group).length!==9)throw Error("source universe");checks+=2;
let rows=[],summary={},compared=0;
for(let w of Object.keys(roots)){let g=group[w],cnt={SHRINK:0,TIE:0,EXPAND:0,AT_FIXED_EXCLUDED:0},warnings=[];
if(Object.keys(g||{}).length!==9)throw Error("cohort count");checks++;
for(let x0 of initials){let xs=g[x0];if(!xs||xs.length!==5||xs.some(x=>!x))throw Error("time support");checks++;
let direct=P(x0),d=[];
for(let n=0;n<5;n++){if(C(xs[n],direct)!==0)throw Error("independent formula mismatch "+w+" "+x0+" "+n);checks++;compared++;d.push(ABS(S(xs[n],P(roots[w]))));if(n<4)direct=map(w,direct)}
let label=C(d[0],Q(0))===0?"AT_FIXED_EXCLUDED":C(d[4],d[0])<0?"SHRINK":C(d[4],d[0])===0?"TIE":"EXPAND";cnt[label]++;
let warning=(kinds[w]!=="ATTRACTOR"&&label==="SHRINK")||(kinds[w]==="ATTRACTOR"&&label==="EXPAND");if(warning)warnings.push(x0);
let hit=d.findIndex(z=>C(z,Q(0))===0);
rows.push({world:w,x0,root:roots[w],local_kind:kinds[w],distances:d.map(T),label,first_exact_hit:hit<0?null:hit,ratio:C(d[0],Q(0))===0?null:T(Q(d[4][0]*d[0][1],d[4][1]*d[0][0])),warning});
}
summary[w]={...cnt,warning_initials:warnings};
}
if(rows.length!==81||compared!==405)throw Error("universe");checks+=2;
let pick=(w,x)=>rows.find(z=>z.world===w&&z.x0===x);
if(pick("LOGISTIC_R4_REPELLER","1/4").label!=="SHRINK"||pick("LOGISTIC_R4_REPELLER","1/4").first_exact_hit!==1)throw Error("repeller control");
if(initials.filter(x=>x!=="0").some(x=>pick("IDENTITY_EVERY_POINT_FIXED",x).label!=="TIE"))throw Error("identity control");
if(initials.filter(x=>x!=="0").some(x=>pick("AFFINE_EXPAND_ZERO",x).label!=="EXPAND"))throw Error("expand control");
if(pick("LOGISTIC_R3_BORDER","3/4").label!=="SHRINK")throw Error("r3 control");checks+=4;
return {research_id:"R248_S44",evidence:"E1_SYNTHETIC",original_source_rows:405,trajectories:81,comparison_points:compared,assertions:checks,failures:0,summary,rows,new_E2:0,new_E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN"};
}
if(typeof module!=="undefined"){module.exports={run};if(require.main===module){let fs=require("fs");if(!process.argv[2])throw Error("usage: node script.js original_405.csv");process.stdout.write(JSON.stringify(run(fs.readFileSync(process.argv[2],"utf8")),null,2)+"\n");}}
