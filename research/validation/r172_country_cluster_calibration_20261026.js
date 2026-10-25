"use strict";
// R172 third method. Run: node r172_country_cluster_calibration_20261026.js R172_REAL_HELDOUT_PREDICTIONS.csv
// Input SHA1 Git blob: 00d0379d77ec8e776a00cbb9c6e9dd5a00958dce
function assert(ok,msg){if(!ok)throw new Error(msg);}
function analyze(csv){
 const lines=csv.trimEnd().split(/\r?\n/), headers=lines.shift().split(",");
 const fields=["episode_id","country_id","year","age_t","recorded_breakdown_event","M0_constant_exact","M1_duration_exact","M2_duration_baseline_exact"];
 for(const f of fields)assert(headers.includes(f),"missing "+f);
 function prob(s){const parts=s.split("/");const p=Number(parts[0])/Number(parts[1]||1);assert(Number.isFinite(p)&&p>0&&p<1,"invalid p "+s);return p;}
 const rows=lines.map((l,i)=>{const parts=l.split(",");assert(parts.length===headers.length,"CSV width "+i);const d=Object.fromEntries(headers.map((h,j)=>[h,parts[j]]));const y=Number(d.recorded_breakdown_event),year=Number(d.year);assert((y===0||y===1)&&year>=2000&&year<=2017,"bad event/year "+i);
 const ps=[d.M0_constant_exact,d.M1_duration_exact,d.M2_duration_baseline_exact].map(prob);
 const loss=ps.map(p=>y?-Math.log(p):-Math.log1p(-p)),brier=ps.map(p=>(p-y)**2);
 return {episode:d.episode_id,country:d.country_id,year,age:Number(d.age_t),y,ps,loss,brier};});
 assert(rows.length===319,"row count");const episodes=new Map(),countries=new Map(),seen=new Set();let eventCount=0;
 for(const r of rows){assert(r.episode&&r.country,"missing ID");const key=r.episode+"|"+r.year;assert(!seen.has(key),"duplicate episode-year");seen.add(key);if(!episodes.has(r.episode))episodes.set(r.episode,{country:r.country,events:0});assert(episodes.get(r.episode).country===r.country,"episode country inconsistent");episodes.get(r.episode).events+=r.y;assert(episodes.get(r.episode).events<=1,"repeat breakdown");eventCount+=r.y;
 if(!countries.has(r.country))countries.set(r.country,[]);countries.get(r.country).push(r);}
 assert(episodes.size===35&&countries.size===32&&eventCount===18,"source count");
 const modelNames=["M0","M1","M2"],bins=[[0,.02],[.02,.05],[.05,1]];
 const models=modelNames.map((name,m)=>{const totalLog=rows.reduce((a,r)=>a+r.loss[m],0),totalBrier=rows.reduce((a,r)=>a+r.brier[m],0),expected=rows.reduce((a,r)=>a+r.ps[m],0);
 const calibration=bins.map(([lo,hi])=>{const rr=rows.filter(r=>r.ps[m]>=lo&&r.ps[m]<(hi===1?1:hi));const events=rr.reduce((a,r)=>a+r.y,0),sumP=rr.reduce((a,r)=>a+r.ps[m],0);return {bin:[lo,hi],n:rr.length,observed:events,expected:sumP,observed_rate:rr.length?events/rr.length:null,mean_p:rr.length?sumP/rr.length:null};});
 return {name,mean_logloss:totalLog/rows.length,mean_brier:totalBrier/rows.length,expected_events:expected,observed_events:eventCount,expected_over_observed:expected/eventCount,calibration};});
 const prior=[[.235881126652,.054407113235],[.245235328446,.054667027894],[.234530415157,.054105271593]];
 for(let i=0;i<3;i++)for(let j=0;j<2;j++)assert(Math.abs((j?models[i].mean_brier:models[i].mean_logloss)-prior[i][j])<1e-10,"original score mismatch "+i+"/"+j);
 const countriesSorted=[...countries.keys()].sort();const perCountry=countriesSorted.map(c=>{const rr=countries.get(c);return {country:c,n:rr.length,episodes:new Set(rr.map(r=>r.episode)).size,events:rr.reduce((a,r)=>a+r.y,0),log_delta:[1,2].map(m=>rr.reduce((a,r)=>a+r.loss[m]-r.loss[0],0)),brier_delta:[1,2].map(m=>rr.reduce((a,r)=>a+r.brier[m]-r.brier[0],0))};});
 const total=(key,m)=>perCountry.reduce((a,g)=>a+g[key][m],0);
 const full={log_delta:[0,1].map(i=>total("log_delta",i)/rows.length),brier_delta:[0,1].map(i=>total("brier_delta",i)/rows.length)};
 const loco=perCountry.map(g=>({country:g.country,remaining_rows:rows.length-g.n,log_delta:[0,1].map(i=>(total("log_delta",i)-g.log_delta[i])/(rows.length-g.n)),brier_delta:[0,1].map(i=>(total("brier_delta",i)-g.brier_delta[i])/(rows.length-g.n))}));
 const influence=[0,1].map(i=>{const vals=loco.map(x=>x.log_delta[i]),base=full.log_delta[i];return {model:["M1","M2"][i],full:base,min:Math.min(...vals),max:Math.max(...vals),positive:vals.filter(x=>x>0).length,negative:vals.filter(x=>x<0).length,zero:vals.filter(x=>x===0).length,sign_change_country:loco.filter(x=>Math.sign(x.log_delta[i])!==Math.sign(base)).map(x=>x.country)};});
 let state=20261026>>>0;const draws={log_delta:[[],[]],brier_delta:[[],[]]};
 for(let b=0;b<1024;b++){let n=0,sl=[0,0],sb=[0,0];for(let j=0;j<perCountry.length;j++){state=(Math.imul(1664525,state)+1013904223)>>>0;const g=perCountry[Math.floor(perCountry.length*state/4294967296)];n+=g.n;for(let i=0;i<2;i++){sl[i]+=g.log_delta[i];sb[i]+=g.brier_delta[i];}}
 for(let i=0;i<2;i++){draws.log_delta[i].push(sl[i]/n);draws.brier_delta[i].push(sb[i]/n);}}
 const quant=(arr,q)=>{const s=arr.slice().sort((a,b)=>a-b),z=(s.length-1)*q,k=Math.floor(z);return s[k]+(s[Math.min(k+1,s.length-1)]-s[k])*(z-k);};
 const bootstrap={seed:20261026,replicates:1024,country_units:perCountry.length,log_delta:[0,1].map(i=>[quant(draws.log_delta[i],.025),quant(draws.log_delta[i],.975)]),brier_delta:[0,1].map(i=>[quant(draws.brier_delta[i],.025),quant(draws.brier_delta[i],.975)])};
 const r0=rows[0],flipped=1-r0.y;const flippedLog=flipped?-Math.log(r0.ps[0]):-Math.log1p(-r0.ps[0]);const replacedBrier=(.5-r0.y)**2;
 const controls={flip_first_event_changes_m0_logloss:Math.abs(flippedLog-r0.loss[0])>1e-12,replace_first_m2_p_changes_brier:Math.abs(replacedBrier-r0.brier[2])>1e-12};
 assert(Object.values(controls).every(Boolean),"negative controls failed");
 return {status:"PASS_INTERNAL_RETROSPECTIVE_COUNTRY_CLUSTER",input_blob:"00d0379d77ec8e776a00cbb9c6e9dd5a00958dce",rows:rows.length,episodes:episodes.size,countries:countries.size,events:eventCount,countries_with_multiple_episodes:perCountry.filter(g=>g.episodes>1),models,full,loco,influence,bootstrap,controls};
}
module.exports={analyze};
if(typeof require!=="undefined"&&require.main===module){const fs=require("fs");const p=process.argv[2]||"R172_REAL_HELDOUT_PREDICTIONS.csv";console.log(JSON.stringify(analyze(fs.readFileSync(p,"utf8")),null,2));}
