"use strict";
// Independent source-first pair-discordance check; Node.js >=18, no packages.
const audit=function eAudit(csv,receipt){
  const fail=m=>{throw Error("E080 "+m)}, check=(v,m)=>{if(!v)fail(m);count++};
  let count=0,raw=csv.trim().split(/\r?\n/),cols=raw.shift().split(",");
  check(raw.length===576,"row count");
  const data=raw.map(line=>{let a=line.split(",");check(a.length===cols.length,"width");return Object.fromEntries(cols.map((k,i)=>[k,a[i]]))});
  const out=JSON.parse(receipt), names=out.worlds.map(w=>w.world);
  check(names.length===9&&new Set(names).size===9,"world names");
  const rat=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);let x=a<0n?-a:a,y=b;while(y){let t=x%y;x=y;y=t}let g=x||1n;return [a/g,b/g]};
  const add=(x,y)=>rat(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
  const sub=(x,y)=>rat(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
  const str=x=>x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);
  function components(edge){
    const parent=[0,1,2],root=i=>{while(parent[i]!==i)i=parent[i];return i};
    [[0,1],[0,2],[1,2]].forEach(([a,b],i)=>{if(edge[i])parent[root(a)]=root(b)});
    return new Set([0,1,2].map(root)).size===1?3: (root(0)===root(1)||root(0)===root(2)?2:1);
  }
  function pairRisk(rows,features){
    let groups=new Map();
    for(let r of rows){let key=features.map(k=>r[k]).join("|");if(!groups.has(key))groups.set(key,[]);groups.get(key).push(Number(r.observed_root_component_size=== "3"));}
    let total=rat(0);
    for(let a of groups.values()){
      let discordant=0;
      for(let x of a)for(let y of a)if(x!==y)discordant++;
      total=add(total,rat(discordant,128*a.length));
    }
    return {risk:str(total),support:groups.size};
  }
  let totalPairs=0;
  for(let expected of out.worlds){
    let rows=data.filter(r=>r.world===expected.world);
    check(rows.length===64,"world rows "+expected.world);
    let keys=new Set(),tObs=0,tTrue=0;
    for(let r of rows){
      let bits=["01","02","12"].flatMap(k=>["a","b"].map(z=>Number(r["oracle_original_edge_R"+k+z])));
      check(bits.length===6&&bits.every(b=>b===0||b===1),"source bits");
      let key=bits.join("");check(!keys.has(key),"duplicate bits");keys.add(key);
      check(r.original_full_edge_source_probability==="1/64","weight");
      const pp=r.frozen_edge_open_probability.split("/");const p=pp.length===2?Number(pp[0])*4/Number(pp[1]):Number(pp[0])*4;
      check(Number.isInteger(p)&&p>=0&&p<=4,"p");
      let observed=["01","02","12"].map((k,i)=>{
        let value=Number(r["observed_reported_edge_Y"+k]);
        let predicted=(expected.world.startsWith("CHAIN")&&i===1)?0:Number(2*bits[2*i]+bits[2*i+1]<p);
        check(value===predicted,"reported edge");return value;
      });
      const hidden=["01","02","12"].map((k,i)=>{
        let value=Number(r["oracle_true_hidden_edge_H"+k]);
        check(value===(expected.world.endsWith("ALIAS")?0:observed[i]),"hidden edge");
        return value;
      });
      let co=components(observed),ct=components(hidden);
      check(co===Number(r.observed_root_component_size),"observed cluster");
      check(ct===Number(r.oracle_true_root_component_size),"true cluster");
      tObs+=Number(co===3);tTrue+=Number(ct===3);
    }
    check(keys.size===64,"complete universe");
    const f0=pairRisk(rows,[]),f01=pairRisk(rows,["observed_reported_edge_Y01"]),fall=pairRisk(rows,["observed_reported_edge_Y01","observed_reported_edge_Y02","observed_reported_edge_Y12"]);
    const pr=s=>{let [a,b]=s.split("/");return rat(a,b||1)};
    const gain=str(sub(pr(f0.risk),pr(f01.risk)));
    for(let [key,value] of Object.entries({f0:f0.risk,f01:f01.risk,fall:fall.risk,gain,remaining:f01.risk,target_rate:str(rat(tObs,64)),oracle_true_target_rate:str(rat(tTrue,64)),support_f0:f0.support,support_f01:f01.support,support_fall:fall.support})){
      check(String(expected[key])===String(value),expected.world+" "+key+" expected "+expected[key]+" got "+value);
    }
    check(fall.risk==="0","fall must zero");
    totalPairs+=rows.length*rows.length*(1+2+1); // pair comparisons of group arrays bounded above
  }
  const bad=JSON.parse(receipt);bad.worlds[0].gain="999";
  let rejected=false;try{
    const v=bad.worlds[0];const rows=data.filter(r=>r.world===v.world);
    const a=pairRisk(rows,[]),b=pairRisk(rows,["observed_reported_edge_Y01"]);
    const pp=s=>{let [a,b]=s.split("/");return rat(a,b||1)};
    if(str(sub(pp(a.risk),pp(b.risk)))!==v.gain)throw Error("tampered");
  }catch(e){rejected=true}
  check(rejected,"tamper negative");
  return {checks:count,worlds:out.worlds.length,source_rows:data.length,paired_comparisons_upper_bound:totalPairs,failed:0,tamper_rejected:rejected};
};
if(require.main===module){const fs=require("fs"),path=require("path");const base=path.resolve(__dirname,"..");const csv=process.argv[2]||path.join(base,"R250","R250_ALL_576_ORIGINAL_THREE_NODE_EDGE_SOURCE_ATOMS.csv");const receipt=process.argv[3]||path.join(base,"validation","R250_S46_PARTIAL_EDGE_BRIER_EXACT_RECEIPT_2026-10-29.json");console.log(JSON.stringify(audit(fs.readFileSync(csv,"utf8"),fs.readFileSync(receipt,"utf8")),null,2));}
module.exports={audit};
