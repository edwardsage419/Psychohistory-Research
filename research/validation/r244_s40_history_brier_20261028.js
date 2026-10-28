"use strict";
const fs=require("fs"),path=require("path");
const gcd=(a,b)=>b===0n?(a<0n?-a:a):gcd(b,a%b);
function q(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d}let g=gcd(n,d);return [n/g,d/g]}
function from(s){let [n,d="1"]=String(s).split("/");return q(n,d)}
const add=(x,y)=>q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
const sub=(x,y)=>q(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
const mul=(x,y)=>q(x[0]*y[0],x[1]*y[1]);
const div=(x,y)=>q(x[0]*y[1],x[1]*y[0]);
const str=x=>x[1]===1n?String(x[0]):x.join("/");
const features={F0:[0],F1:[1],F2:[2],F12:[1,2],LEAK:[3]};
function risk(joint,indices){let groups=new Map;
 for(let [key,p] of Object.entries(joint)){if(!/^[01]{4}$/.test(key)||key[0]!=="0")throw Error("bad observed path");let mass=from(p),id=indices.map(i=>key[i]).join(""),g=groups.get(id)||{t:q(0),n:q(0)};g.t=add(g.t,mass);if(key[3]==="1")g.n=add(g.n,mass);groups.set(id,g)}
 let total=q(0),result=q(0);for(let g of groups.values()){total=add(total,g.t);if(g.t[0]===0n)continue;result=add(result,div(mul(g.n,sub(g.t,g.n)),g.t))}
 if(str(total)!=="1")throw Error("probability mass not one");return {value:str(result),support:groups.size}}
function compute(doc){if(doc.research_id!=="R244"||doc.world_results.length!==9)throw Error("wrong frozen research");let out=[];
 for(let w of doc.world_results){let risks={},support={};for(let [name,idx] of Object.entries(features)){let x=risk(w.complete_observed_four_time_state_joint,idx);risks[name]=x.value;support[name]=x.support}
 let gain=str(sub(from(risks.F2),from(risks.F12)));if(from(gain)[0]<0n||risks.LEAK!=="0")throw Error("risk invariant failed");
 out.push({world:w.world,risks,history_gain:gain,support,original_markov_defect:w.observed_time3_conditional_markov_defect})}
 if(out.filter(x=>x.history_gain!=="0").map(x=>x.world).join(",")!=="LATENT_RATE_MIXTURE,FIXED_SWITCH_POLICY")throw Error("unexpected positive gain worlds");
 let aliases=out.filter(x=>["PERSISTENT_3OF4","STATIC_HIDDEN_SENSOR_ALIAS","COMPLEMENT_HIDDEN_COORDINATE_ALIAS"].includes(x.world));
 if(aliases.some(x=>JSON.stringify(x.risks)!==JSON.stringify(aliases[0].risks)))throw Error("observation alias risk mismatch");
 return {study:"R244_S40",evidence:"E1_SYNTHETIC",source_blob:"081f173f39686235940c6327b375561093ed965b",worlds:out,new_E2:0,new_E3:0,external_replications:0,CI:"NOT_RUN"}}
if(require.main===module){let input=JSON.parse(fs.readFileSync(path.join(__dirname,"../R244/R244_EXACT_RESULTS.json"),"utf8"));console.log(JSON.stringify(compute(input),null,2))}
module.exports={compute};
