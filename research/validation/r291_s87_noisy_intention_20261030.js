#!/usr/bin/env node
"use strict";
const fs=require("fs"),path=require("path");
const generate=function generate(){
 const F=(a,b=1n)=>{let n=BigInt(a),d=BigInt(b);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d}let x=n<0n?-n:n,y=d;while(y){let t=x%y;x=y;y=t}return [n/x,d/x]};
 const add=(x,y)=>F(x[0]*y[1]+y[0]*x[1],x[1]*y[1]), neg=x=>[-x[0],x[1]],sub=(x,y)=>add(x,neg(y)),mul=(x,y)=>F(x[0]*y[0],x[1]*y[1]),div=(x,y)=>F(x[0]*y[1],x[1]*y[0]),eq=(x,y)=>x[0]===y[0]&&x[1]===y[1],str=x=>x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);
 const Z=F(0),O=F(1),profiles=[["BALANCED",1,1],["ATTITUDE_HEAVY",2,1],["NORM_HEAVY",1,2],["NORM_NULL",2,0]],modes=[["MEDIATED",0],["DIRECT_NORM_STRESS",1]],errors=[F(0),F(1,4),F(1,2)];
 const keys=["FULL_ANJ","AJ","AN","A"],fields={FULL_ANJ:["A","N","J"],AJ:["A","J"],AN:["A","N"],A:["A"]};
 const id=(row,which)=>fields[which].map(k=>String(row[k])).join("|");
 const rows=[],results=[];
 function expected(profile,mode,e,A,N,I,B,J){
  const pI=add(F(1,2),F(profile[1]*A+profile[2]*N,8)),pB=add(add(F(1,4),F(I,2)),F(mode[1]*N,8)),pJ=I===J?sub(O,e):e;
  return mul(F(1,4),mul(I?pI:sub(O,pI),mul(B?pB:sub(O,pB),pJ)));
 }
 function verifyCells(xs,profile,mode,e){
  if(xs.length!==32)throw Error("source count");
  const seen=new Set();let mass=Z;
  for(const x of xs){
   const k=[x.A,x.N,x.I,x.B,x.J].join("|");if(seen.has(k))throw Error("duplicate");seen.add(k);
   if(![-1,1].includes(x.A)||![-1,1].includes(x.N)||![0,1].includes(x.I)||![0,1].includes(x.B)||![0,1].includes(x.J))throw Error("domain");
   if(!eq(x.p,expected(profile,mode,e,x.A,x.N,x.I,x.B,x.J)))throw Error("source mismatch");
   if(x.p[0]<0n)throw Error("negative mass");mass=add(mass,x.p);
  }
  if(seen.size!==32||!eq(mass,O))throw Error("coverage or mass");
 }
 for(const profile of profiles)for(const mode of modes)for(const e of errors){
  const world=profile[0]+"__"+mode[0],xs=[];
  for(const A of [-1,1])for(const N of [-1,1])for(const I of [0,1])for(const B of [0,1])for(const J of [0,1]){
   xs.push({world,profile:profile[0],mode:mode[0],error_rate:str(e),A,N,I,B,J,p:expected(profile,mode,e,A,N,I,B,J)});
  }
  verifyCells(xs,profile,mode,e);
  const tables={};for(const k of keys)tables[k]=new Map();
  for(const x of xs)for(const k of keys){const tag=id(x,k),t=tables[k].get(tag)||{mass:Z,positive:Z};t.mass=add(t.mass,x.p);if(x.B)t.positive=add(t.positive,x.p);tables[k].set(tag,t)}
  const risks={};for(const k of keys)risks[k]=Z;
  for(const x of xs){
   x.q={};
   for(const k of keys){
    const t=tables[k].get(id(x,k)),q=t.mass[0]===0n?null:div(t.positive,t.mass);
    x.q[k]=q;
    if(x.p[0]>0n&&q===null)throw Error("undefined forecast with positive mass");
    if(q!==null){if(q[0]<0n||q[0]>q[1])throw Error("bad q");risks[k]=add(risks[k],mul(x.p,mul(sub(F(x.B),q),sub(F(x.B),q))))}
   }
  }
  const gap=sub(risks.AJ,risks.FULL_ANJ);
  for(const k of ["AJ","AN","A"])if(sub(risks[k],risks.FULL_ANJ)[0]<0n)throw Error("negative omission gap");
  const n=profile[2],d=mode[1];
  if(e[0]===0n&&d===0&&!eq(gap,Z))throw Error("perfect intention mediation failed");
  if(eq(e,F(1,2))&&!eq(gap,F((n+2*d)**2,256)))throw Error("unmeasured intention limit failed");
  if(profile[0]==="NORM_NULL"&&d===0&&!eq(gap,Z))throw Error("null mediated gap failed");
  if(profile[0]==="NORM_NULL"&&d===1&&!eq(gap,F(1,64)))throw Error("null direct gap failed");
  if(profile[0]==="BALANCED"&&d===0&&eq(e,F(1,4))&&gap[0]<=0n)throw Error("positive gap expected");
  if(profile[0]==="BALANCED"&&d===0&&eq(e,F(1,4))){
    const mutated=xs.map(x=>({...x}));mutated[0]={...mutated[0],p:add(mutated[0].p,F(1,100))};
    for(const variant of [mutated,xs.slice(1),xs.concat(xs[0]),xs.map((x,i)=>i===0?{...x,B:1-x.B}:x)]){
     let rejected=false;try{verifyCells(variant,profile,mode,e)}catch{rejected=true}if(!rejected)throw Error("negative test accepted");
    }
  }
  for(const x of xs)rows.push(x);
  results.push({world,profile:profile[0],mode:mode[0],proxy_flip_rate:str(e),source_cells:32,zero_mass_cells:xs.filter(x=>x.p[0]===0n).length,source_mass:"1",risk_brier:Object.fromEntries(keys.map(k=>[k,str(risks[k])])),norm_omission_gap:str(gap),ignore_proxy_gap:str(sub(risks.AN,risks.FULL_ANJ)),ignore_proxy_and_norm_gap:str(sub(risks.A,risks.FULL_ANJ))});
 }
 if(rows.length!==768||results.length!==24)throw Error("global coverage");
 const cols=["world","profile","mode","error_rate","A","N","I","B","J","source_probability",...keys.map(k=>"forecast_"+k)];
 const lines=[cols.join(",")];for(const x of rows){lines.push([x.world,x.profile,x.mode,x.error_rate,x.A,x.N,x.I,x.B,x.J,str(x.p),...keys.map(k=>x.q[k]===null?"NA":str(x.q[k]))].join(","))}
 const output={research_id:"R291_S87",parent_R291_freeze:"161d40a01451f1e89be045910f95ec536768754c",S87_prescore_commit:"4f51f8119ab5faba95fcf4b7b44b63eb6bb3621b",scope:"INTERNAL_NONBLIND_E1_ARTIFICIAL",source_cells:768,worlds:24,new_human_E2:0,new_historical_E3:0,external_independent_replication:0,R073:"FROZEN",PESEN_v0_1:"FROZEN",results};
 return {csv:lines.join("\n")+"\n",json:JSON.stringify(output,null,2)+"\n",summary:results.map(x=>({world:x.world,e:x.proxy_flip_rate,gap:x.norm_omission_gap})),mutation_controls:4};
};
const args=process.argv.slice(2);
if(args.length!==1 && !(args.length===2 && args[0]==="--emit")){console.error("usage: node r291_s87_noisy_intention_20261030.js --test | --check | --emit DIRECTORY");process.exit(2)}
const out=generate();
const names=["R291_S87_ALL_768_PROXY_SOURCE_CELLS.csv","R291_S87_EXACT_RESULTS.json"];
if(args[0]==="--test"){console.log(JSON.stringify({status:"PASS",worlds:24,source_cells:768,mutation_controls:4}));}
else if(args[0]==="--check"){for(let i=0;i<2;i++){const actual=fs.readFileSync(path.join(__dirname,names[i]),"utf8");if(actual!==(i===0?out.csv:out.json))throw Error("archive mismatch: "+names[i]);}console.log("PASS: both persisted archives byte-identical to generated output");}
else if(args[0]==="--emit"){fs.mkdirSync(args[1],{recursive:true});for(let i=0;i<2;i++)fs.writeFileSync(path.join(args[1],names[i]),i===0?out.csv:out.json,"utf8");console.log("emitted",names.join(", "));}
else{process.exit(2)}
