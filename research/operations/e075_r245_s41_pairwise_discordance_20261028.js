#!/usr/bin/env node
'use strict';
// E075: independent pairwise discordance oracle for R245 S41. Requires only Node.js standard library.
const fs=require('node:fs'),path=require('node:path');
function verify(csv, receipt){
  let checks=0;function assert(b,m){checks++;if(!b)throw Error(m)}
  const lines=csv.trim().split(/\r?\n/), cols=lines.shift().split(",");
  const idx=Object.fromEntries(cols.map((c,i)=>[c,i]));
  const required=["world","oracle_exogenous_U","original_source_probability",...Array.from({length:5},(_,i)=>"observed_reported_count_Y"+i)];
  for(const k of required)assert(Number.isInteger(idx[k]),"missing "+k);
  const groups=new Map(), ids=new Map(), full=new Map();
  for(const line of lines){
    const a=line.split(",");assert(a.length===cols.length,"bad CSV width");
    const w=a[idx.world];if(!groups.has(w)){groups.set(w,[]);ids.set(w,new Set());full.set(w,new Map())}
    const bits=a[idx.oracle_exogenous_U]+[1,2,3,4].map(i=>a[idx["oracle_original_R"+i+"1"]]+a[idx["oracle_original_R"+i+"2"]]).join("");
    assert(/^[01]{9}$/.test(bits),"invalid exogenous bits");
    assert(!ids.get(w).has(bits),"duplicate source");ids.get(w).add(bits);
    assert(a[idx.original_source_probability]==="1/512","source probability");
    const y=[0,1,2,3,4].map(i=>Number(a[idx["observed_reported_count_Y"+i]]));
    assert(y[0]===0&&y.every((v,i)=>Number.isInteger(v)&&(i===0||v-y[i-1]===0||v-y[i-1]===1)),"observed path");
    const key=y.join(",");full.get(w).set(key,(full.get(w).get(key)||0)+1);
    groups.get(w).push({y,z:y[4]-y[3]});
  }
  assert(lines.length===4608,"source universe");
  assert(groups.size===9,"world count");
  function gcd(a,b){while(b!==0n){[a,b]=[b,a%b]}return a<0n?-a:a}
  function rat(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<=0n)throw Error("denom");const g=gcd(a,b);return [a/g,b/g]}
  function plus(x,y){return rat(x[0]*y[1]+y[0]*x[1],x[1]*y[1])}
  function minus(x,y){return rat(x[0]*y[1]-y[0]*x[1],x[1]*y[1])}
  function cmp(x,y){const v=x[0]*y[1]-y[0]*x[1];return v<0n?-1:v>0n?1:0}
  function fmt(x){return x[1]===1n?String(x[0]):x[0]+"/"+x[1]}
  const fields=["F0","F3","F23","F123"], results=[], byWorld=new Map(receipt.results.map(x=>[x.world,x]));
  let inspectedPairs=0;
  for(const [w,rs] of groups){
    assert(rs.length===512,"world source count");
    assert(ids.get(w).size===512,"source identity count");
    const risks={};
    for(const f of fields){
      const strata=new Map();
      for(const x of rs){
        const k=f==="F0"?"":f==="F3"?String(x.y[3]):f==="F23"?x.y.slice(2,4).join(","):x.y.slice(1,4).join(",");
        if(!strata.has(k))strata.set(k,[]);
        strata.get(k).push(x.z);
      }
      let risk=rat(0n);
      for(const arr of strata.values()){
        let discordant=0n;
        for(let i=0;i<arr.length;i++)for(let j=i+1;j<arr.length;j++){inspectedPairs++;if(arr[i]!==arr[j])discordant++}
        risk=plus(risk,rat(discordant,512n*BigInt(arr.length)));
        assert(discordant>=0n&&discordant<=BigInt(arr.length*(arr.length-1)/2),"pair bound");
      }
      risks[f]=risk;
      assert(cmp(risk,rat(0n))>=0&&cmp(risk,rat(1n,4n))<=0,"risk range");
      assert(fmt(risk)===byWorld.get(w)?.risks[f],"receipt risk "+w+" "+f);
    }
    for(let i=1;i<fields.length;i++)assert(cmp(risks[fields[i-1]],risks[fields[i]])>=0,"nested info monotonicity");
    assert(cmp(risks.F23,risks.F123)===0,"f23 f123 equality");
    const successes=rs.reduce((n,x)=>n+x.z,0);
    assert(cmp(risks.F0,rat(BigInt(successes*(512-successes)),512n*512n))===0,"F0 Bernoulli");
    const gain0=fmt(minus(risks.F0,risks.F123)),gain3=fmt(minus(risks.F3,risks.F123));
    assert(gain0===byWorld.get(w).gain_F0_F123,"gain0");
    assert(gain3===byWorld.get(w).gain_F3_F123,"gain3");
    results.push({world:w,risks:Object.fromEntries(fields.map(f=>[f,fmt(risks[f])])),gain_F0_F123:gain0,gain_F3_F123:gain3});
  }
  const a=full.get("IID_FAIR"),b=full.get("STATIC_HIDDEN_EVENT_SENSOR_ALIAS");
  assert(a?.size===b?.size,"alias support");
  for(const [k,v] of a)assert(v===b.get(k),"alias mass "+k);
  const mutant=JSON.parse(JSON.stringify(receipt));mutant.results.find(x=>x.world==="IID_FAIR").risks.F0="999";
  assert(results.find(x=>x.world==="IID_FAIR").risks.F0!==mutant.results.find(x=>x.world==="IID_FAIR").risks.F0,"mutation rejected");
  return {source_rows:lines.length,worlds:groups.size,conditions:36,checks,inspected_pairs:inspectedPairs,failures:0,results};
}
const root=path.resolve(__dirname,'..');
const csv=fs.readFileSync(path.join(root,'R245/R245_ALL_4608_ORIGINAL_RENEWAL_GAP_SOURCES.csv'),'utf8');
const receipt=JSON.parse(fs.readFileSync(path.join(root,'evidence_audit/B_R245_S41_EXACT_RISK_CROSSROUTE_RECEIPT_2026-10-28.json'),'utf8'));
console.log(JSON.stringify(verify(csv,receipt),null,2));
