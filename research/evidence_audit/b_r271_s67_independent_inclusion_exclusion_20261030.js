// R271 S67 B route: nonblind independent inclusion-exclusion and persisted source gate.
// Node 18+, no external dependencies. Does not import R generator.
"use strict";
function audit(csv,json,receipt) {
  const D=["IDENTICAL","ROLLING","DISJOINT"], P=["FROZEN_FIRST","FLEXIBLE_ANY","BONFERRONI_ANY"];
  const check=(x,m)=>{if(!x)throw Error(m);};
  const f=(n,d)=>{function gcd(a,b){while(b){[a,b]=[b,a%b]}return a;}let g=gcd(n,d);return d/g===1?String(n/g):n/g+"/"+d/g;};
  const W=(design,m)=>Array.from({length:m},(_,i)=>Array.from({length:4},(_,j)=>design==="IDENTICAL"?j:design==="ROLLING"?i+j:4*i+j));
  function union(design,m) {
    const w=W(design,m);let numerator=0;
    for(let mask=1;mask<(1<<m);mask++){
      let set=new Set(),bits=0;
      for(let i=0;i<m;i++)if(mask&(1<<i)){bits++;for(let j of w[i])set.add(j);}
      numerator+=(bits%2?1:-1)*2**(12-set.size);
    }
    return f(numerator,4096);
  }
  check(typeof json==="string"&&typeof csv==="string","input type");
  const obj=JSON.parse(json),r=JSON.parse(receipt);
  check(obj.evidence==="E1_EXPLORATORY_ARTIFICIAL_NONBLIND"&&obj.strict_blind_prescore_freeze===false,"evidence scope");
  check([obj.real_human_E2,obj.real_historical_E3,obj.external_independent_replications].every(v=>Number.isInteger(v)&&v===0),"E2 E3 external scope");
  check(Number.isInteger(obj.world_count)&&obj.world_count===27&&obj.policy_labelled_source_count===13584,"world count");
  check(Array.isArray(obj.worlds)&&obj.worlds.length===27,"world list");
  let expected=new Map();
  for(let m=1;m<=3;m++)for(let d of D)for(let p of P){
    const key=d+"_M"+m+"_"+p;
    expected.set(key,p==="FROZEN_FIRST"?"1/16":p==="BONFERRONI_ANY"&&m===3?"0":union(d,m));
  }
  let seen=new Set();
  for(let w of obj.worlds){
    check(w&&typeof w==="object"&&expected.has(w.world)&&!seen.has(w.world),"duplicate or unknown world");
    seen.add(w.world);
    check(w.world===w.design+"_M"+w.m+"_"+w.policy,"world key");
    check(typeof w.exact_familywise_false_positive_risk==="string"&&w.exact_familywise_false_positive_risk===expected.get(w.world),"independent exact risk");
    const len=Math.max(...W(w.design,w.m).flat())+1;
    check(Number.isInteger(w.source_count)&&w.source_count===2**len,"world source count");
  }
  check(seen.size===27,"missing world");
  check(r.research_id==="R271_S67"&&r.evidence==="E1_EXPLORATORY_ARTIFICIAL_NONBLIND"&&r.source_rows===13584&&r.world_count===27,"receipt identity");
  check([r.new_E2,r.new_E3,r.external_independent_replications].every(v=>Number.isInteger(v)&&v===0),"receipt evidence");
  const lines=csv.trimEnd().split("\n");
  check(lines.length===13585,"CSV row count");
  check(lines[0]==="world,design,m,policy,bits,window_positions,success_counts,raw_p_values,selected_index,positive,source_mass","CSV schema");
  let groups=new Map();
  const pvals=["1","15/16","11/16","5/16","1/16"];
  for(let j=1;j<lines.length;j++){
    const cols=lines[j].split(",");
    check(cols.length===11,"CSV fields");
    const [key,d,mstr,p,bits,wp,counts,raw,index,positive,mass]=cols;
    check(expected.has(key),"CSV unknown world");
    const m=Number(mstr),w=W(d,m),L=Math.max(...w.flat())+1;
    check(key===d+"_M"+m+"_"+p&&bits.length===L&&/^[01]+$/.test(bits),"CSV identity");
    check(wp===w.map(v=>v.join(".")).join(";"),"CSV window");
    const cnt=w.map(indices=>indices.reduce((s,i)=>s+(bits[i]==="1"?1:0),0));
    check(counts===cnt.join(";")&&raw===cnt.map(v=>pvals[v]).join(";"),"CSV p values");
    const choices=p==="FROZEN_FIRST"?[0]:Array.from({length:m},(_,i)=>i);
    const idx=choices.find(i=>cnt[i]===4&&(p!=="BONFERRONI_ANY"||m<=2));
    const sel=idx===undefined?-1:idx;
    check(index===String(sel)&&positive===String(Number(sel>=0)),"CSV decision");
    check(mass==="1/"+(2**L),"CSV mass");
    if(!groups.has(key))groups.set(key,{seen:new Set(),pos:0,count:0});
    let g=groups.get(key);check(!g.seen.has(bits),"duplicate primitive");g.seen.add(bits);g.pos+=Number(positive);g.count++;
  }
  for(let [key,g] of groups){
    const w=obj.worlds.find(v=>v.world===key);
    check(g.count===w.source_count,"missing primitive");
    check(f(g.pos,g.count)===expected.get(key),"CSV vs exact risk");
  }
  check(groups.size===27,"CSV missing world");
  return {status:"PASS",worlds:27,source_rows:13584,route:"independent_inclusion_exclusion_and_full_CSV",evidence:"NONBLIND_INTERNAL_E1"};
}
function mutationTests(csv,json,receipt) {
  const base=JSON.parse(json),test=(mutateCsv,mutateObj)=>{
    let c=mutateCsv?mutateCsv(csv):csv, o=JSON.parse(json);
    if(mutateObj)mutateObj(o);
    try{audit(c,JSON.stringify(o),receipt);return false}catch(e){return true}
  };
  const checks=[
    test(null,o=>{o.worlds[1]=JSON.parse(JSON.stringify(o.worlds[0]));}),
    test(null,o=>{o.worlds.pop();}),
    test(null,o=>{o.worlds[0].exact_familywise_false_positive_risk="999";}),
    test(null,o=>{o.real_human_E2=1;}),
    test(null,o=>{o.world_count=true;}),
    test(c=>{let lines=c.split("\n");lines.splice(2,1);return lines.join("\n");},null)
  ];
  if(!checks.every(Boolean))throw Error("mutation test false acceptance");
  return checks.length;
}
if(typeof require==="function"&&typeof process!=="undefined"&&require.main===module){
  const fs=require("fs"),path=require("path"),crypto=require("crypto"),dir=process.argv[2]||".";
  const csv=fs.readFileSync(path.join(dir,"R271_S67_ALL_13584_OVERLAPPING_NULL_SOURCE_ROWS.csv"),"utf8");
  const json=fs.readFileSync(path.join(dir,"R271_S67_EXACT_FAMILYWISE_RISKS.json"),"utf8");
  const receipt=fs.readFileSync(path.join(dir,"R271_S67_MACHINE_RECEIPT.json"),"utf8");
  const r=JSON.parse(receipt);
  if(crypto.createHash("sha256").update(csv).digest("hex")!==r.source_sha256||
     crypto.createHash("sha256").update(json).digest("hex")!==r.results_sha256)throw Error("checksum mismatch");
  const result=audit(csv,json,receipt);
  result.mutations_rejected=mutationTests(csv,json,receipt);
  process.stdout.write(JSON.stringify(result)+"\n");
}
