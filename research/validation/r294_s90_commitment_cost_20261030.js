"use strict";
// Exact rational R294 S90 replay. Uses only Node standard library. Does not overwrite original R294.
const fs=require("fs"),path=require("path");
function generate(input){
  const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t}return a||1n};
  const rat=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero denominator");if(b<0n){a=-a;b=-b}const g=gcd(a,b);return [a/g,b/g]};
  const f=s=>{if(s===""||s===null)throw Error("missing fraction");const x=String(s).split("/");return rat(x[0],x[1]||"1")};
  const add=(a,b)=>rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
  const neg=a=>[-a[0],a[1]];
  const sub=(a,b)=>add(a,neg(b));
  const mul=(a,b)=>rat(a[0]*b[0],a[1]*b[1]);
  const div=(a,b)=>rat(a[0]*b[1],a[1]*b[0]);
  const cmp=(a,b)=>a[0]*b[1]<b[0]*a[1]?-1:a[0]*b[1]>b[0]*a[1]?1:0;
  const str=a=>a[1]===1n?String(a[0]):`${a[0]}/${a[1]}`;
  const one=f("1"),zero=f("0");
  const lines=input.trimEnd().split(/\r?\n/);
  const cols=lines[0].split(",");
  const rows=lines.slice(1).map(line=>Object.fromEntries(line.split(",").map((v,i)=>[cols[i],v])));
  if(rows.length!==144)throw Error("original rows !=144");
  const groups=new Map();
  for(const r of rows){if(!groups.has(r.world))groups.set(r.world,[]);groups.get(r.world).push(r)}
  if(groups.size!==72)throw Error("original worlds !=72");
  const fees=["0","1/4","1/2","1"];
  const csvCols=["world","family","earlier_reward","later_reward","original_t0","original_t1","fee_t0_utility","gain_t0_utility","purchase","implemented","net_improvement_t0_utility","evidence"];
  const out=[csvCols.join(",")];
  const stats={};
  const baseline={HYPERBOLIC:0,EXPONENTIAL:0,QUASI_HYPERBOLIC_BETA_DELTA:0};
  for(const [world,pair] of groups){
    if(pair.length!==2||pair[0].decision_at!=="0"||pair[1].decision_at!=="1")throw Error("original pair identity");
    const [r0,r1]=pair;const family=r0.family;const a=f(r0.earlier_reward),b=f(r0.later_reward);
    if(!baseline.hasOwnProperty(family))throw Error("unknown family");
    const discount=(delay)=>{
      if(family==="HYPERBOLIC")return div(one,add(one,mul(f(r0.parameter_k),f(String(delay)))));
      if(family==="EXPONENTIAL"){let z=one;for(let j=0;j<delay;j++)z=mul(z,f(r0.parameter_delta));return z}
      if(family==="QUASI_HYPERBOLIC_BETA_DELTA"){let z=one;for(let j=0;j<delay;j++)z=mul(z,f(r0.parameter_delta));return delay?mul(f(r0.parameter_beta),z):one}
      throw Error("family");
    };
    const vals=[[mul(a,discount(1)),mul(b,discount(2))],[a,mul(b,discount(1))]];
    for(let t=0;t<2;t++){
      const row=pair[t];const [va,vb]=vals[t];
      if(str(va)!==row.earlier_utility||str(vb)!==row.later_utility)throw Error("original value mismatch "+world);
      const ch=cmp(va,vb)>=0?"A":"B";
      if(ch!==row.selected_option||String(cmp(va,vb)===0)!==(row.exact_tie.toLowerCase()))throw Error("original choice mismatch");
    }
    const t0=r0.selected_option,t1=r1.selected_option;
    if(t0==="A"&&t1==="B")throw Error("unanticipated reversal");
    const reversal=t0!==t1;
    if(String(reversal)!==r0.world_reversal.toLowerCase()||r0.world_reversal!==r1.world_reversal)throw Error("original reversal mismatch");
    if(reversal)baseline[family]++;
    const gain=reversal?sub(vals[0][1],vals[0][0]):zero;
    if(cmp(gain,zero)<0)throw Error("negative gain");
    for(const feeText of fees){
      const fee=f(feeText),purchase=cmp(gain,fee)>0;
      const improvement=purchase?sub(gain,fee):zero;
      const impl=purchase?t0:t1;
      const key=family+"|"+feeText;
      if(!stats[key])stats[key]={family,fee:feeText,worlds:0,purchases:0,sum:zero};
      stats[key].worlds++;if(purchase)stats[key].purchases++;stats[key].sum=add(stats[key].sum,improvement);
      const record=[world,family,r0.earlier_reward,r0.later_reward,t0,t1,feeText,str(gain),String(purchase),impl,str(improvement),"E1_SYNTHETIC"];
      out.push(record.join(","));
    }
  }
  if(out.length!==289)throw Error("288 source cells");
  if(JSON.stringify(baseline)!==JSON.stringify({HYPERBOLIC:8,EXPONENTIAL:0,QUASI_HYPERBOLIC_BETA_DELTA:7}))throw Error("baseline mismatch");
  const summary=Object.values(stats).map(s=>({family:s.family,fee:s.fee,worlds:s.worlds,purchases:s.purchases,sum_net_improvement:str(s.sum),mean_net_improvement:str(div(s.sum,f(s.worlds)))}));
  for(const family of Object.keys(baseline)){const x=summary.filter(s=>s.family===family);if(x.length!==4||x.some((s,i)=>i&&s.purchases>x[i-1].purchases))throw Error("nonmonotone");}
  const result={research_id:"R294",stage:"S90",status:"PARTIAL",evidence:"E1_SYNTHETIC",freeze_commit:"905467c19d04c01b4fea3f26592625fbc8229d13",original_source_blob:"098e45b9ba81de9bd7dc59c0a3466083b03e6ab4",worlds:72,source_rows:288,fees,original_reversals:baseline,summary,new_E2:0,new_E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN"};
  return {csv:out.join("\n")+"\n",json:JSON.stringify(result,null,2)+"\n",result};
}
if(require.main===module){const input=fs.readFileSync(path.resolve(__dirname,"../R294/R294_ALL_144_EXACT_INTERTEMPORAL_DECISION_SOURCES.csv"),"utf8");const out=generate(input);if(process.argv[2]==="--check"){process.stdout.write(JSON.stringify(out.result.summary)+"\n");}else if(process.argv[2]==="--emit"&&process.argv[3]){const dir=path.resolve(process.argv[3]);fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(path.join(dir,"R294_S90_ALL_288_COMMITMENT_CELLS.csv"),out.csv);fs.writeFileSync(path.join(dir,"R294_S90_EXACT_RESULTS.json"),out.json);process.stdout.write("R294 S90 emitted 288 cells\n");}else{process.stderr.write("Usage: node r294_s90_commitment_cost_20261030.js --check | --emit OUTPUT_DIR\n");process.exitCode=2;}}
module.exports={generate};
