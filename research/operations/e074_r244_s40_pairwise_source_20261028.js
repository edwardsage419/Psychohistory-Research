"use strict";
// E074: third route from original R244 artificial source rows.
// Uses unordered discordant observation pairs within each conditioning bin.
const fs = require("fs");
const path = require("path");
const features = {F0:[0], F1:[1], F2:[2], F12:[1,2], LEAK:[3]};
function gcd(a,b){while(b!==0n){[a,b]=[b,a%b]}return a;}
function format(n,d){let g=gcd(n,d);n/=g;d/=g;return d===1n?String(n):String(n)+"/"+String(d);}
function audit(csv,receipt){
  const lines=csv.trim().split(/\r?\n/),header=lines.shift().split(",");
  const col=Object.fromEntries(header.map((x,i)=>[x,i]));
  const required=["world","original_source_probability",...Array.from({length:4},(_,i)=>"observed_y"+i),
    "oracle_source_U",...["R11","R12","R21","R22","R31","R32"].map(x=>"oracle_original_"+x)];
  if(required.some(k=>col[k]===undefined))throw Error("missing original source column");
  let checks=0;const test=(ok,why)=>{checks++;if(!ok)throw Error("E074 mismatch: "+why);};
  const rows=lines.map(line=>line.split(",")),worlds=new Map();
  for(const row of rows){
    const name=row[col.world],obs=Array.from({length:4},(_,i)=>row[col["observed_y"+i]]);
    const source=[col.oracle_source_U,...["R11","R12","R21","R22","R31","R32"].map(x=>col["oracle_original_"+x])].map(i=>row[i]).join("");
    test(row[col.original_source_probability]==="1/128","source mass "+name);
    test(obs.every(x=>x==="0"||x==="1")&&obs[0]==="0","observed bits "+name);
    test(/^[01]{7}$/.test(source),"source bits "+name);
    if(!worlds.has(name))worlds.set(name,[]);
    worlds.get(name).push({source,obs});
  }
  test(rows.length===1152,"source row count");
  test(worlds.size===9,"world count");
  const output=[];
  for(const [name,group] of worlds){
    test(group.length===128,"per world source count "+name);
    test(new Set(group.map(x=>x.source)).size===128,"seven-bit source uniqueness "+name);
    const risks={},support={};
    for(const [feature,indices] of Object.entries(features)){
      const bins=new Map();
      for(const row of group){
        const key=indices.map(i=>row.obs[i]).join("");
        if(!bins.has(key))bins.set(key,[]);
        bins.get(key).push(row.obs[3]);
      }
      let numerator=0n,denominator=1n;
      for(const bin of bins.values()){
        let discordant=0n;
        // Count every unordered pair directly, rather than using a precomputed
        // PMF, a Bernoulli variance formula, or the R/B research functions.
        for(let i=0;i<bin.length;i++)
          for(let j=i+1;j<bin.length;j++)
            if(bin[i]!==bin[j])discordant++;
        const d=128n*BigInt(bin.length);
        numerator=numerator*d+discordant*denominator;
        denominator*=d;
        const g=gcd(numerator,denominator);
        numerator/=g;denominator/=g;
      }
      risks[feature]=format(numerator,denominator);
      support[feature]=bins.size;
    }
    const expected=receipt.worlds.find(x=>x.world===name);
    test(!!expected,"receipt world "+name);
    for(const feature of Object.keys(features)){
      test(risks[feature]===expected.risks[feature],"risk "+name+" "+feature);
      test(support[feature]===expected.support[feature],"support "+name+" "+feature);
    }
    test(risks.LEAK==="0","leak must be zero "+name);
    output.push({world:name,risks,support});
  }
  return {study:"R244_S40",source_rows:rows.length,worlds:worlds.size,checks,failures:0,route:"source_unordered_discordant_pairs",risks:output};
}
if(require.main===module){
  const csv=fs.readFileSync(path.join(__dirname,"../R244/R244_ALL_1152_ORIGINAL_BINARY_MARKOV_SOURCE_PATHS.csv"),"utf8");
  const receipt=JSON.parse(fs.readFileSync(path.join(__dirname,"../validation/R244_S40_HISTORY_BRIER_RECEIPT_2026-10-28.json"),"utf8"));
  const result=audit(csv,receipt);
  const mutant=JSON.parse(JSON.stringify(receipt));
  mutant.worlds[0].risks.F2="999";
  let mutationRejected=false;
  try{audit(csv,mutant)}catch(_){mutationRejected=true;}
  if(!mutationRejected)throw Error("mutation test failed");
  console.log(JSON.stringify({study:result.study,source_rows:result.source_rows,worlds:result.worlds,checks:result.checks,failures:0,mutation_rejected:mutationRejected},null,2));
}
module.exports={audit};
