"use strict";
function gcd(a,b){while(b){const t=a%b;a=b;b=t;}return a<0n?-a:a;}
function frac(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
function plus(a,b){return frac(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function eq(a,b){return a[0]*b[1]===b[0]*a[1];}
function parse(s){const p=String(s).split("/");return frac(BigInt(p[0]),BigInt(p[1]||"1"));}
function audit(csv,R,B){
 let checks=0,pairs=0;const ok=(v,m)=>{checks++;if(!v)throw Error("AUDIT FAIL: "+m);};
 const rows=csv.trim().split(/\r?\n/),head=rows.shift().split(",");
 const at=n=>{const i=head.indexOf(n);if(i<0)throw Error("missing column "+n);return i;};
 const ix={world:at("world"),y1:at("observed_generation_size_Y1"),y2:at("observed_generation_size_Y2"),y3:at("observed_generation_size_Y3"),h3:at("oracle_true_hidden_generation_H3"),p:at("original_complete_source_probability"),bits:[at("oracle_hidden_environment_U"),...Array.from({length:7},(_,i)=>at("oracle_original_node_bit_B"+i))]};
 const worlds=new Map();
 for(const line of rows){const a=line.split(",");ok(a.length===head.length,"CSV column count");ok(a[ix.p]==="1/256","source weight");
   const w=a[ix.world];if(!worlds.has(w))worlds.set(w,[]);
   const bits=ix.bits.map(i=>a[i]).join("");ok(/^[01]{8}$/.test(bits),"bit signature");
   worlds.get(w).push({bits,y1:Number(a[ix.y1]),y2:Number(a[ix.y2]),y3:Number(a[ix.y3]),h3:Number(a[ix.h3])});
 }
 ok(rows.length===2304,"source total");ok(worlds.size===9,"world count");
 ok(R.evidence==="E1_SYNTHETIC"&&B.evidence==="E1_SYNTHETIC","evidence labels");
 ok(R.source_blob==="33c948db4a5c3b0104f233fd8e03daa79faebccf","R source identity");
 ok(B.source_blob==="42de5332f4aafae65487a71f03fc0dce5beb59df","B source identity");
 const results={},features=["F0","F1","F2","F12"];
 for(const [name,data] of worlds){
   ok(data.length===256,name+" source count");
   ok(new Set(data.map(x=>x.bits)).size===256,name+" unique 8bit source");
   if(name==="STATIC_HIDDEN_TREE_SENSOR_ALIAS")for(const x of data)ok(x.h3===0,"alias hidden H3");
   results[name]={};
   for(const f of features){
     const groups=new Map();
     for(const x of data){const key=f==="F0"?"all":f==="F1"?String(x.y1):f==="F2"?String(x.y2):x.y1+","+x.y2;if(!groups.has(key))groups.set(key,[]);groups.get(key).push(x);}
     let risk=frac(0n);
     for(const g of groups.values()){
       let discord=0n;
       for(let i=0;i<g.length;i++)for(let j=i+1;j<g.length;j++){pairs++;if((g[i].y3>0)!==(g[j].y3>0))discord++;}
       risk=plus(risk,frac(discord,BigInt(256*g.length)));
     }
     ok(eq(risk,parse(R.results[name][f].risk)),name+" "+f+" R risk");
     ok(eq(risk,parse(B.results[name][f].risk)),name+" "+f+" B risk");
     ok(groups.size===R.results[name][f].support,name+" "+f+" R support");
     ok(groups.size===B.results[name][f].support,name+" "+f+" B support");
     ok(risk[0]>=0n&&risk[0]*4n<=risk[1],name+" "+f+" range");
     results[name][f]={risk:risk[1]===1n?String(risk[0]):risk[0]+"/"+risk[1],support:groups.size};
   }
   const r=results[name];ok(eq(parse(r.F2.risk),parse(r.F12.risk)),name+" F2 F12 equality");
   ok(parse(r.F0.risk)[0]*parse(r.F1.risk)[1]>=parse(r.F1.risk)[0]*parse(r.F0.risk)[1],name+" F0 >= F1");
 }
 for(const f of features)ok(results.IID_FAIR_0_OR_2[f].risk===results.STATIC_HIDDEN_TREE_SENSOR_ALIAS[f].risk,"alias "+f);
 ok(R.external_replication===0&&B.external_replication===0,"external replication zero");
 return {checks,failures:0,source_rows:rows.length,worlds:worlds.size,pairs_examined:pairs,risks:36,supports:36,results};
}
if(typeof module!=="undefined"&&typeof require==="function"&&require.main===module){
 const fs=require("fs"),args=process.argv.slice(2);if(args.length!==3)throw Error("Usage: node script.js original.csv R_receipt.json B_receipt.json");
 console.log(JSON.stringify(audit(fs.readFileSync(args[0],"utf8"),JSON.parse(fs.readFileSync(args[1],"utf8")),JSON.parse(fs.readFileSync(args[2],"utf8"))),null,2));
}
if(typeof module!=="undefined")module.exports={audit};
