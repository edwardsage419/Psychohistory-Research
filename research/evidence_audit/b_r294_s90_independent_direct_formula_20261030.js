"use strict";
// Independent direct-formula R294 S90 audit. No import of the R generator.
const fs=require("fs"),path=require("path");
function audit(originalCsv,commitCsv,resultJson){
  const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t}return a||1n};
  const R=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("zero denominator");if(b<0n){a=-a;b=-b}const g=gcd(a,b);return [a/g,b/g]};
  const F=s=>{const z=String(s).split("/");return R(z[0],z[1]||"1")};
  const plus=(a,b)=>R(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
  const minus=(a,b)=>R(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
  const times=(a,b)=>R(a[0]*b[0],a[1]*b[1]);
  const over=(a,b)=>R(a[0]*b[1],a[1]*b[0]);
  const gt=(a,b)=>a[0]*b[1]>b[0]*a[1];
  const ge=(a,b)=>a[0]*b[1]>=b[0]*a[1];
  const eq=(a,b)=>a[0]*b[1]===b[0]*a[1];
  const fmt=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1];
  const parse=txt=>{const lines=txt.trimEnd().split(/\r?\n/);const header=lines.shift().split(",");return lines.map(l=>{const vals=l.split(",");if(vals.length!==header.length)throw Error("bad csv");return Object.fromEntries(header.map((h,i)=>[h,vals[i]]))})};
  const o=parse(originalCsv),c=parse(commitCsv),j=JSON.parse(resultJson);
  if(o.length!==144||c.length!==288||j.source_rows!==288||j.worlds!==72||j.evidence!=="E1_SYNTHETIC"||j.new_E2!==0||j.new_E3!==0)throw Error("coverage/grade");
  const groups=new Map();for(const r of o){if(!groups.has(r.world))groups.set(r.world,[]);groups.get(r.world).push(r)}
  if(groups.size!==72)throw Error("original coverage");
  const expect=new Map(),familyReversals={HYPERBOLIC:0,EXPONENTIAL:0,QUASI_HYPERBOLIC_BETA_DELTA:0};
  const fees=["0","1/4","1/2","1"],sum=new Map();
  for(const [id,pair] of groups){
    if(pair.length!==2||pair[0].decision_at!=="0"||pair[1].decision_at!=="1")throw Error("original pair");
    const [x,y]=pair,a=F(x.earlier_reward),b=F(x.later_reward),one=F("1"),zero=F("0");
    let ua0,ub0,ua1=a,ub1;
    if(x.family==="HYPERBOLIC"){
      const k=F(x.parameter_k);ua0=over(a,plus(one,k));ub0=over(b,plus(one,times(F("2"),k)));ub1=over(b,plus(one,k));
    }else if(x.family==="EXPONENTIAL"){
      const d=F(x.parameter_delta);ua0=times(a,d);ub0=times(b,times(d,d));ub1=times(b,d);
    }else if(x.family==="QUASI_HYPERBOLIC_BETA_DELTA"){
      const beta=F(x.parameter_beta),d=F(x.parameter_delta);ua0=times(a,times(beta,d));ub0=times(b,times(beta,times(d,d)));ub1=times(b,times(beta,d));
    }else throw Error("family");
    if(!eq(ua0,F(x.earlier_utility))||!eq(ub0,F(x.later_utility))||!eq(ua1,F(y.earlier_utility))||!eq(ub1,F(y.later_utility)))throw Error("original utility");
    const p0=ge(ua0,ub0)?"A":"B",p1=ge(ua1,ub1)?"A":"B";
    if(p0!==x.selected_option||p1!==y.selected_option||String(eq(ua0,ub0))!==x.exact_tie.toLowerCase()||String(eq(ua1,ub1))!==y.exact_tie.toLowerCase())throw Error("original choice/tie");
    const reversal=p0!==p1;
    if(p0==="A"&&p1==="B"||String(reversal)!==x.world_reversal.toLowerCase())throw Error("original reversal");
    if(reversal)familyReversals[x.family]++;
    const gain=reversal?minus(ub0,ua0):zero;
    for(const f of fees){
      const fee=F(f),purchase=gt(gain,fee),net=purchase?minus(gain,fee):zero;
      expect.set(id+"|"+f,{world:id,family:x.family,fee:f,gain:fmt(gain),purchase:String(purchase),implemented:purchase?p0:p1,net:fmt(net)});
      const k=x.family+"|"+f;if(!sum.has(k))sum.set(k,{worlds:0,purchases:0,net:zero});
      const z=sum.get(k);z.worlds++;z.purchases+=Number(purchase);z.net=plus(z.net,net);
    }
  }
  if(JSON.stringify(familyReversals)!==JSON.stringify({HYPERBOLIC:8,EXPONENTIAL:0,QUASI_HYPERBOLIC_BETA_DELTA:7}))throw Error("baseline family");
  const seen=new Set();
  for(const r of c){
    const key=r.world+"|"+r.fee_t0_utility;
    if(seen.has(key))throw Error("duplicate new cell");seen.add(key);
    const x=expect.get(key);
    if(!x||r.family!==x.family||r.gain_t0_utility!==x.gain||r.purchase!==x.purchase||r.implemented!==x.implemented||r.net_improvement_t0_utility!==x.net||r.evidence!=="E1_SYNTHETIC")throw Error("new cell mismatch "+key);
  }
  if(seen.size!==expect.size)throw Error("missing cells");
  if(j.summary.length!==12)throw Error("summary count");
  const summarySeen=new Set();
  for(const r of j.summary){
    const k=r.family+"|"+r.fee;if(summarySeen.has(k))throw Error("summary duplicate");summarySeen.add(k);
    const x=sum.get(k);if(!x||r.worlds!==x.worlds||r.purchases!==x.purchases||r.sum_net_improvement!==fmt(x.net)||r.mean_net_improvement!==fmt(over(x.net,F(String(x.worlds)))))throw Error("summary mismatch "+k);
  }
  if(summarySeen.size!==sum.size)throw Error("summary coverage");
  return {status:"PASS",original_rows:o.length,new_rows:c.length,worlds:groups.size,summary_cells:sum.size,baseline:familyReversals};
}
if(require.main===module){const base=path.resolve(__dirname,"..");const original=fs.readFileSync(path.join(base,"R294/R294_ALL_144_EXACT_INTERTEMPORAL_DECISION_SOURCES.csv"),"utf8");const csv=fs.readFileSync(path.join(base,"validation/R294_S90_ALL_288_COMMITMENT_CELLS.csv"),"utf8");const json=fs.readFileSync(path.join(base,"validation/R294_S90_EXACT_RESULTS.json"),"utf8");console.log(JSON.stringify(audit(original,csv,json),null,2));}
module.exports={audit};
