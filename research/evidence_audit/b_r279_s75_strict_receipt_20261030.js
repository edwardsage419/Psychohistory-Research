"use strict";
// Independent persisted receipt audit, artificial E1, internal nonblind.
// node b_r279_s75_strict_receipt_20261030.js source.csv result.json
function audit(csvText,jsonText){
  const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;};
  const rat=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("denominator");if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];};
  const parse=x=>{if(typeof x!=="string")throw Error("fraction type");const p=x.split("/");if(p.length>2||p.some(z=>z.trim()===""||!Number.isFinite(Number(z))))throw Error("fraction");return rat(p[0],p.length===2?p[1]:1);};
  const add=(x,y)=>rat(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
  const sub=(x,y)=>rat(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
  const mul=(x,y)=>rat(x[0]*y[0],x[1]*y[1]);
  const div=(x,y)=>rat(x[0]*y[1],x[1]*y[0]);
  const square=x=>mul(x,x),equal=(x,y)=>x[0]===y[0]&&x[1]===y[1];
  const repr=x=>x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);
  const zero=rat(0),one=rat(1),half=rat(1,2),quarter=rat(1,4),three=rat(3,4);
  const truth={CALIBRATED_RATE:[quarter,three],DETERMINISTIC_GROUP:[zero,one],INVERTED_RATE:[three,quarter]};
  const forecast={ORIGINAL_BUCKETS:[quarter,three],FLAT_HALF:[half,half],REVERSED_BUCKETS:[three,quarter]};
  const names=["REL","RES","UNC","Brier"],j=JSON.parse(jsonText);
  if(j.research!=="R279_S75"||j.evidence!=="ARTIFICIAL_E1_INTERNAL_NONBLIND_EXPLORATORY"||j.E2!==0||j.E3!==0||j.R073!=="FROZEN"||j.PESEN_v0_1!=="FROZEN"||j.original_R279_unchanged!==true||j.source_atoms!==144||j.positive_source_atoms!==99)throw Error("metadata gate");
  if(!Array.isArray(j.results)||j.results.length!==9)throw Error("world count");
  const rows=csvText.trimEnd().split("\n");
  if(rows.shift()!=="regime,policy,bits,source_mass,empirical_REL,empirical_RES,empirical_UNC,sample_Brier"||rows.length!==144)throw Error("CSV coverage");
  const grouped=new Map();
  for(const row of rows){
    const c=row.split(",");if(c.length!==8)throw Error("row fields");
    const [regime,policy,bits]=c;
    if(!(regime in truth)||!(policy in forecast)||bits.length!==4||[...bits].some(b=>b!=="0"&&b!=="1"))throw Error("world or bits");
    const key=regime+"/"+policy;if(!grouped.has(key))grouped.set(key,new Map());
    const group=grouped.get(key);if(group.has(bits))throw Error("duplicate source");group.set(bits,c);
    const t=truth[regime],q=forecast[policy],k=[Number(bits[0])+Number(bits[1]),Number(bits[2])+Number(bits[3])];
    let mass=one;for(let i=0;i<4;i++)mass=mul(mass,bits[i]==="1"?t[Math.floor(i/2)]:sub(one,t[Math.floor(i/2)]));
    if(!equal(parse(c[3]),mass))throw Error("source mass");
    const overall=rat(k[0]+k[1],4);let rel=zero,res=zero;
    if(equal(q[0],q[1]))rel=square(sub(q[0],overall));
    else{const a=rat(k[0],2),b=rat(k[1],2);rel=div(add(square(sub(q[0],a)),square(sub(q[1],b))),rat(2));res=div(add(square(sub(a,overall)),square(sub(b,overall))),rat(2));}
    const unc=mul(overall,sub(one,overall));let brier=zero;
    for(let i=0;i<4;i++)brier=add(brier,square(sub(rat(Number(bits[i])),q[Math.floor(i/2)])));
    brier=div(brier,rat(4));
    if(!equal(brier,add(sub(rel,res),unc)))throw Error("Murphy identity");
    const v=[rel,res,unc,brier];for(let i=0;i<4;i++)if(!equal(parse(c[i+4]),v[i]))throw Error("primitive "+names[i]);
  }
  let positive=0;const seen=new Set();
  for(const e of j.results){
    const key=e.regime+"/"+e.policy;if(seen.has(key))throw Error("duplicate world");seen.add(key);
    const group=grouped.get(key);if(!group||group.size!==16||e.source_atoms!==16)throw Error("world coverage");
    const t=truth[e.regime],q=forecast[e.policy];let expected=[zero,zero,zero,zero],total=zero,pzero=zero,ple=zero,npositive=0;
    const base=div(add(t[0],t[1]),rat(2));
    const pr=equal(q[0],q[1])?square(sub(q[0],base)):div(add(square(sub(q[0],t[0])),square(sub(q[1],t[1]))),rat(2));
    const ps=equal(q[0],q[1])?zero:div(add(square(sub(t[0],base)),square(sub(t[1],base))),rat(2));
    const pu=mul(base,sub(one,base)),pop=[pr,ps,pu,add(sub(pr,ps),pu)];
    for(const c of group.values()){
      const m=parse(c[3]),r=parse(c[4]);total=add(total,m);if(m[0]!==0n)npositive++;
      for(let i=0;i<4;i++)expected[i]=add(expected[i],mul(m,parse(c[i+4])));
      if(r[0]===0n)pzero=add(pzero,m);
      if(r[0]*pr[1]<=pr[0]*r[1])ple=add(ple,m);
    }
    if(!equal(total,one)||e.positive_source_atoms!==npositive)throw Error("mass coverage");
    positive+=npositive;
    for(let i=0;i<4;i++){if(e.population[names[i]]!==repr(pop[i])||e.expected_empirical[names[i]]!==repr(expected[i])||e.empirical_minus_population[names[i]]!==repr(sub(expected[i],pop[i])))throw Error("summary "+names[i]);}
    if(e.P_empirical_REL_equals_zero!==repr(pzero)||e.P_empirical_REL_at_most_population_REL!==repr(ple)||e.count_oracle_equal!==true||e.variance_formula_equal!==true)throw Error("probability or flag");
  }
  if(seen.size!==9||grouped.size!==9||positive!==99)throw Error("global coverage");
  return {status:"PASS",rows:144,worlds:9,positive:99};
}
if(typeof module!=="undefined")module.exports={audit};
if(typeof require==="function"&&require.main===module){const fs=require("fs");if(process.argv.length!==4)throw Error("requires source.csv and result.json");console.log(JSON.stringify(audit(fs.readFileSync(process.argv[2],"utf8"),fs.readFileSync(process.argv[3],"utf8"))));}
