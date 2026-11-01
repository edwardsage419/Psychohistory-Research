#!/usr/bin/env node
"use strict";
// R329 S125 finite constructed sensor fidelity extension. Standard Node.js only.
// The pure generate() function is also runnable without Node-specific globals.
function generate(){
  const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t}return a||1n};
  const F=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);let g=gcd(n,d);return [n/g,d/g]};
  const add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
  const mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]);
  const sub=(a,b)=>F(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
  const one=F(1),num=a=>Number(a[0])/Number(a[1]),str=a=>a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);
  const beliefs=[F(1,4),F(1,2),F(3,4)],prefs=[F(1,2),F(3,4)],qualities=[F(1,2),F(5,8),F(3,4),F(7,8),F(1)],costs=[F(0),F(1,8),F(1,4)];
  const fields=["belief","preference_one","sensor_accuracy","precise_cost","policy","hidden","observation","likelihood","joint_mass","observation_mass","expected_free_energy","selected_policy","evidence_grade"];
  const rows=[],worlds=[],series=[];
  const score=(b,c,q,k,policy)=>{
    let accuracy=policy==="PRECISE"?q:F(1,2),joint=[],marg=[F(0),F(0)],joints={};
    for(let s=0;s<2;s++)for(let o=0;o<2;o++){let prior=s?b:sub(one,b),lik=s===o?accuracy:sub(one,accuracy),j=mul(prior,lik);joint.push({s,o,lik,j});marg[o]=add(marg[o],j)}
    let info=0,extrinsic=0,risk=0,ambiguity=0;
    for(let o=0;o<2;o++){let p=num(marg[o]),cp=num(o?c:sub(one,c));extrinsic+=p*Math.log(cp);if(p>0)risk+=p*Math.log(p/cp)}
    for(let v of joint){let p=num(v.j),lik=num(v.lik),m=num(marg[v.o]);if(p>0){info+=p*Math.log(lik/m);ambiguity-=p*Math.log(lik)}}
    let cost=policy==="PRECISE"?num(k):0,g=-extrinsic-info+cost,alt=risk+ambiguity+cost;
    return {joint,marg,info,g,alt};
  };
  for(let b of beliefs)for(let c of prefs){
    let ss=[];
    for(let q of qualities){
      let base=score(b,c,q,F(0),"PRECISE"),noisy=score(b,c,q,F(0),"NOISY");
      let advantage=noisy.g-base.g;
      ss.push({sensor_accuracy:str(q),net_advantage_at_zero_cost:advantage.toFixed(9)});
      for(let k of costs){
        let p=score(b,c,q,k,"PRECISE"),n=score(b,c,q,k,"NOISY");
        let selected=p.g<n.g-1e-14?"PRECISE":"NOISY";
        let identity=Math.max(Math.abs(p.g-p.alt),Math.abs(n.g-n.alt));
        worlds.push({belief:str(b),preference_one:str(c),sensor_accuracy:str(q),precise_cost:str(k),chosen_policy:selected,precise_efe:p.g.toFixed(9),noisy_efe:n.g.toFixed(9),precise_information:p.info.toFixed(9),noisy_information:n.info.toFixed(9),net_advantage_at_zero_cost:advantage.toFixed(9),identity_error:identity.toFixed(12),evidence_grade:"E1_CONSTRUCTED_ONLY"});
        for(let [policy,v] of [["PRECISE",p],["NOISY",n]])for(let t of v.joint)rows.push([str(b),str(c),str(q),str(k),policy,String(t.s),String(t.o),str(t.lik),str(t.j),str(v.marg[t.o]),v.g.toFixed(9),selected,"E1_CONSTRUCTED_ONLY"]);
      }
    }
    let deltas=ss.slice(1).map((x,i)=>Number(x.net_advantage_at_zero_cost)-Number(ss[i].net_advantage_at_zero_cost));
    series.push({belief:str(b),preference_one:str(c),values:ss,nonmonotonic:deltas.some(x=>x>1e-10)&&deltas.some(x=>x< -1e-10)});
  }
  const csv=fields.join(",")+"\n"+rows.map(x=>x.join(",")).join("\n")+"\n";
  const data={model:"R329_S125_CONSTRUCTED_SENSOR_FIDELITY_EFE",protocol:"S125-v1",evidence_grade:"E1_CONSTRUCTED_ONLY",source_row_count:rows.length,world_count:worlds.length,series,worlds};
  const json=JSON.stringify(data,null,2)+"\n";
  return {csv,json,data};
}
if (typeof require !== "undefined" && require.main === module) {
 const fs=require("fs"),path=require("path"),assert=require("assert");
 const out=generate(),args=process.argv.slice(2);
 if(args.includes("--selftest")){
   assert.strictEqual(out.data.world_count,90);
   assert.strictEqual(out.data.source_row_count,720);
   assert.strictEqual(out.data.series.length,6);
   assert.strictEqual(out.data.worlds.filter(w=>w.sensor_accuracy==="3/4").length,18);
   for(const w of out.data.worlds)assert(Number(w.identity_error)<1e-12);
   const original=JSON.parse(fs.readFileSync(path.resolve(__dirname,"../R329/R329_EXACT_18_EFE_WORLDS.json"),"utf8"));
   for(const w of out.data.worlds.filter(w=>w.sensor_accuracy==="3/4")){
     const old=original.worlds.find(x=>x.belief===w.belief&&x.preference_one===w.preference_one&&x.precise_cost===w.precise_cost);
     assert(old,"missing original world");
     for(const key of ["chosen_policy","precise_efe","noisy_efe","precise_information","noisy_information"])assert.strictEqual(w[key],old[key]);
   }
   for(const w of out.data.worlds.filter(w=>w.sensor_accuracy==="1/2")){
     assert(Math.abs(Number(w.precise_efe)-Number(w.noisy_efe)-Number(w.precise_cost.split("/")[0])/(w.precise_cost.includes("/")?Number(w.precise_cost.split("/")[1]):1))<2e-9);
   }
   console.log("R329 S125 selftest PASS: 720 atoms, 90 worlds, 18 original worlds, zero-info limit");
 }
 if(args.includes("--audit")){
   assert.strictEqual(fs.readFileSync(path.resolve(__dirname,"R329_S125_ALL_720_JOINT_ATOMS.csv"),"utf8"),out.csv);
   assert.strictEqual(fs.readFileSync(path.resolve(__dirname,"R329_S125_EXACT_90_EFE_WORLDS.json"),"utf8"),out.json);
   console.log("R329 S125 archived byte replay PASS");
 }
 const ix=args.indexOf("--emit-dir");
 if(ix>=0){
   assert(args[ix+1],"--emit-dir needs directory");
   const dir=path.resolve(args[ix+1]);fs.mkdirSync(dir,{recursive:true});
   fs.writeFileSync(path.join(dir,"R329_S125_ALL_720_JOINT_ATOMS.csv"),out.csv);
   fs.writeFileSync(path.join(dir,"R329_S125_EXACT_90_EFE_WORLDS.json"),out.json);
   console.log("R329 S125 emitted to "+dir);
 }
 if(!args.length)console.log(JSON.stringify({worlds:out.data.world_count,atoms:out.data.source_row_count,nonmonotonic:out.data.series.filter(s=>s.nonmonotonic)}));
}
