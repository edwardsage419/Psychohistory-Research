#!/usr/bin/env node
"use strict";
// R329 S125 nonblind independent no-import KL plus ambiguity auditor.
// Reconstructs rational atoms and computes scores without importing R code.
function audit(csvText,jsonText,originalText){
  const fail=(ok,msg)=>{if(!ok)throw Error(msg)};
  const parse=s=>{let [a,b="1"]=s.split("/");return [BigInt(a),BigInt(b)]};
  const gcd=(a,b)=>{while(b){let t=a%b;a=b;b=t}return a<0n?-a:a};
  const f=(a,b=1n)=>{let g=gcd(a,b);return [a/g,b/g]};
  const mul=(x,y)=>f(x[0]*y[0],x[1]*y[1]);
  const add=(x,y)=>f(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
  const sub=(x,y)=>f(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
  const num=x=>Number(x[0])/Number(x[1]),txt=x=>x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);
  const entropy=x=>{let p=num(x);return p===0||p===1?0: -p*Math.log(p)-(1-p)*Math.log(1-p)};
  const lines=csvText.trimEnd().split("\n"),header=lines.shift().split(","),rows=lines.map(l=>Object.fromEntries(l.split(",").map((x,i)=>[header[i],x])));
  const data=JSON.parse(jsonText),old=JSON.parse(originalText);
  fail(data.world_count===90&&data.source_row_count===720&&rows.length===720&&data.worlds.length===90,"world or row count");
  fail(data.evidence_grade==="E1_CONSTRUCTED_ONLY"&&data.protocol==="S125-v1","metadata");
  const beliefs=["1/4","1/2","3/4"],prefs=["1/2","3/4"],qualities=["1/2","5/8","3/4","7/8","1"],costs=["0","1/8","1/4"];
  const keys=new Set(),advantages={},tol=5.1e-10;
  let i=0,originalCount=0,zeroCount=0;
  for(let bStr of beliefs)for(let cStr of prefs)for(let qStr of qualities)for(let kStr of costs){
    let b=parse(bStr),c=parse(cStr),q=parse(qStr),k=parse(kStr),w=data.worlds[i/8],scores={};
    fail(w.belief===bStr&&w.preference_one===cStr&&w.sensor_accuracy===qStr&&w.precise_cost===kStr,"world key");
    fail(w.evidence_grade==="E1_CONSTRUCTED_ONLY","world evidence grade");
    for(let policy of ["PRECISE","NOISY"]){
      let a=policy==="PRECISE"?q:parse("1/2");
      let m1=add(mul(b,a),mul(sub(f(1n),b),sub(f(1n),a))),m0=sub(f(1n),m1);
      let risk=num(m0)*Math.log(num(m0)/num(sub(f(1n),c)))+num(m1)*Math.log(num(m1)/num(c));
      let amb=entropy(a),info=entropy(m1)-amb,score=risk+amb+(policy==="PRECISE"?num(k):0);
      scores[policy]={score,info};
      for(let s of [0,1])for(let o of [0,1]){
        let row=rows[i++],prior=s?b:sub(f(1n),b),lik=s===o?a:sub(f(1n),a),joint=mul(prior,lik),marg=o?m1:m0;
        const expected={belief:bStr,preference_one:cStr,sensor_accuracy:qStr,precise_cost:kStr,policy,hidden:String(s),observation:String(o),likelihood:txt(lik),joint_mass:txt(joint),observation_mass:txt(marg),evidence_grade:"E1_CONSTRUCTED_ONLY"};
        for(let [key,val] of Object.entries(expected))fail(row[key]===val,"row "+i+" "+key);
        fail(Math.abs(Number(row.expected_free_energy)-score)<tol,"row score "+i);
        let id=[bStr,cStr,qStr,kStr,policy,s,o].join("|");
        fail(!keys.has(id),"duplicate atom");keys.add(id);
        if(joint[0]===0n)zeroCount++;
      }
    }
    let chosen=scores.PRECISE.score<scores.NOISY.score-1e-14?"PRECISE":"NOISY";
    fail(w.chosen_policy===chosen,"chosen policy");
    for(let row of rows.slice(i-8,i))fail(row.selected_policy===chosen,"row chosen policy");
    for(let [policy,prefix] of [["PRECISE","precise"],["NOISY","noisy"]]){
      fail(Math.abs(Number(w[prefix+"_efe"])-scores[policy].score)<tol,"world EFE");
      fail(Math.abs(Number(w[prefix+"_information"])-scores[policy].info)<tol,"world information");
    }
    fail(Math.abs(Number(w.identity_error))<1e-12,"identity error");
    let adv=scores.NOISY.score-scores.PRECISE.score+num(k);
    fail(Math.abs(Number(w.net_advantage_at_zero_cost)-adv)<tol,"advantage");
    let key=[bStr,cStr,qStr].join("|");
    if(!(key in advantages))advantages[key]=adv;else fail(Math.abs(advantages[key]-adv)<1e-12,"cost independence");
    if(qStr==="3/4"){
      let orig=old.worlds.find(x=>x.belief===bStr&&x.preference_one===cStr&&x.precise_cost===kStr);
      fail(!!orig,"original absent");
      for(let field of ["chosen_policy","precise_efe","noisy_efe","precise_information","noisy_information"])fail(w[field]===orig[field],"original parity "+field);
      originalCount++;
    }
  }
  fail(i===720&&keys.size===720&&originalCount===18&&zeroCount===36,"coverage and original parity");
  fail(data.series.length===6,"series count");
  let nonmono=0;
  for(let [si,s] of data.series.entries()){
    let b=beliefs[Math.floor(si/2)],c=prefs[si%2];
    fail(s.belief===b&&s.preference_one===c&&s.values.length===5,"series identity");
    let v=s.values.map((x,j)=>{fail(x.sensor_accuracy===qualities[j],"series quality");let expected=advantages[[b,c,qualities[j]].join("|")];fail(Math.abs(Number(x.net_advantage_at_zero_cost)-expected)<tol,"series value");return expected});
    let d=v.slice(1).map((x,j)=>x-v[j]);
    let isNon=d.some(x=>x>1e-10)&&d.some(x=>x< -1e-10);
    fail(s.nonmonotonic===isNon,"nonmonotonic classification");
    if(isNon)nonmono++;
  }
  return {worlds:90,atoms:720,original_worlds:18,zero_mass_atoms:zeroCount,nonmonotonic_series:nonmono,precise_wins:data.worlds.filter(x=>x.chosen_policy==="PRECISE").length};
}
if(typeof require!=="undefined" && require.main===module){
 const fs=require("fs"),path=require("path");
 const base=path.resolve(__dirname,"../validation");
 const original=fs.readFileSync(path.resolve(__dirname,"../R329/R329_EXACT_18_EFE_WORLDS.json"),"utf8");
 const csv=fs.readFileSync(path.join(base,"R329_S125_ALL_720_JOINT_ATOMS.csv"),"utf8");
 const json=fs.readFileSync(path.join(base,"R329_S125_EXACT_90_EFE_WORLDS.json"),"utf8");
 const r=audit(csv,json,original);
 if(process.argv.includes("--selftest")){
  const mutated=[
   [csv.split("\n").slice(0,-2).join("\n")+"\n",json],
   [csv+csv.split("\n")[1]+"\n",json],
   [csv.replace(",9/16,",",8/16,"),json],
   [csv.replace(",1/2,3/8,",",3/4,3/8,"),json],
   [csv,JSON.stringify({...JSON.parse(json),evidence_grade:"E2_HUMAN"})],
   [csv,(()=>{let d=JSON.parse(json);d.worlds[0].chosen_policy="NOISY";return JSON.stringify(d)})()],
   [csv,(()=>{let d=JSON.parse(json);d.worlds[0].precise_efe="99.000000000";return JSON.stringify(d)})()],
   [csv,(()=>{let d=JSON.parse(json);d.series[0].values[0].net_advantage_at_zero_cost="0.123456789";return JSON.stringify(d)})()],
   [csv.replace(",0,",",1/9,"),json],
   [(()=>{let l=csv.trimEnd().split("\n");[l[1],l[2]]=[l[2],l[1]];return l.join("\n")+"\n"})(),json]
  ];
  for(const [c,j] of mutated){let rejected=false;try{audit(c,j,original)}catch(e){rejected=true}if(!rejected)throw Error("mutation accepted");}
  console.log("B R329 S125 10 negative controls rejected");
 }
 console.log("B R329 S125 no-import audit PASS "+JSON.stringify(r));
}
