"use strict";
// R307 S103 independent nonblind exact audit, no R generator imports.
function f(a,b=1n){a=BigInt(a);b=BigInt(b);let x=a<0n?-a:a,y=b;while(y){let z=x%y;x=y;y=z;}return [a/x,b/x];}
function a(x,y){return f(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);}
function m(x,y){return f(x[0]*y[0],x[1]*y[1]);}
function s(x,y){return a(x,[-y[0],y[1]]);}
function d(x,y){return f(x[0]*y[1],x[1]*y[0]);}
function str(x){return x[1]===1n?String(x[0]):x[0]+"/"+x[1];}
function ok(x,e){if(!x)throw Error(e);}
const levels=[f(0),f(1,2),f(1)],names=["D0_T0_JOINT_M1","D1_PRIVATE_M1","D2_PUBLIC_M1","D3_PUBLIC_M1_M2","D4_JOINT_M1","D5_JOINT_M1_M2"];
function evalAlgebra(t,c,k,n,minority){
 let mass=f(1);for(let j=0;j<t;j++)mass=m(mass,a(f(1),m(c,k)));
 let belief=s(f(1),d(f(1),a(f(1),mass)));
 let pub=a(f(1,2),m(s(f(1),m(n,f(6-minority,6))),s(belief,f(1,2))));
 return [str(belief),str(pub)];
}
function audit(csv,j){
 const lines=csv.trimEnd().split("\n"),fields=lines.shift().split(",");
 ok(fields.join(",")==="t,c,k,n,private,public_m1,public_m2","header");
 const rows=lines.map(line=>Object.fromEntries(fields.map((k,i)=>[k,line.split(",")[i]])));
 ok(rows.length===81&&new Set(rows.map(x=>[x.t,x.c,x.k,x.n].join("|"))).size===81,"coverage");
 ok(j.evidence==="E1_ARTIFICIAL"&&j.real_human_E2===0&&j.historical_E3===0&&j.R073==="FROZEN"&&j.PESEN_v0_1==="FROZEN","scope");
 ok(j.prior==="1/2"&&j.world_count===81&&JSON.stringify(j.designs)===JSON.stringify(names),"metadata");
 let expected=[],parts=new Map();
 for(let t=1;t<=3;t++)for(let c of levels)for(let k of levels)for(let n of levels){
  let x=evalAlgebra(t,c,k,n,1),y=evalAlgebra(t,c,k,n,2),z=evalAlgebra(0,c,k,n,1);
  let key=[str(c),str(k),str(n)].join("|");
  expected.push({t:String(t),c:str(c),k:str(k),n:str(n),private:x[0],public_m1:x[1],public_m2:y[1]});
  [z,[x[0]],[x[1]],[x[1],y[1]],x,[x[0],x[1],y[0],y[1]]].forEach((sig,i)=>{
   let id=t+"|"+names[i],ss=JSON.stringify(sig);
   if(!parts.has(id))parts.set(id,new Map());
   if(!parts.get(id).has(ss))parts.get(id).set(ss,[]);
   parts.get(id).get(ss).push(key);
  });
 }
 for(let i=0;i<81;i++)ok(JSON.stringify(rows[i])===JSON.stringify(expected[i]),"row "+i);
 ok(j.results.length===18,"18 designs");
 let seen=new Set();
 for(const z of j.results){
  let id=z.t+"|"+z.design,g=parts.get(id);ok(g&&!seen.has(id),"design identity");seen.add(id);
  ok(z.classes===g.size&&z.uniform_prior_optimal_accuracy===str(f(g.size,27)),"class/accuracy");
  let hist={};for(const v of g.values())hist[v.length]=(hist[v.length]||0)+1;
  ok(JSON.stringify(z.class_size_histogram)===JSON.stringify(hist),"histogram");
  ok(z.singleton_worlds===[...g.values()].filter(v=>v.length===1).length,"singletons");
  ok(z.max_class_size===Math.max(...[...g.values()].map(v=>v.length)),"max class");
  ok(z.partitions.length===g.size,"partition count");
  for(const p of z.partitions){let key=JSON.stringify(p.signature);ok(g.has(key)&&JSON.stringify(p.triples)===JSON.stringify(g.get(key)),"partition identity");}
 }
 ok(seen.size===18,"missing design");
 return true;
}
function mutationTests(csv,doc){
 const mutations=[
 (c,j)=>c+c.trimEnd().split("\n")[1]+"\n",
 (c,j)=>c.trimEnd().split("\n").slice(0,-1).join("\n")+"\n",
 (c,j)=>{let x=c.trimEnd().split("\n"),p=x[1].split(",");p[4]="0";x[1]=p.join(",");return x.join("\n")+"\n";},
 (c,j)=>{j.results[0].partitions[0].triples=["fake"];return c;},
 (c,j)=>{j.results[0].uniform_prior_optimal_accuracy="1";return c;},
 (c,j)=>{j.results[0].design="WRONG";return c;},
 (c,j)=>{j.evidence="E2_HUMAN";return c;},
 (c,j)=>{j.prior="1/4";return c;}
 ];
 let caught=0;
 for(const edit of mutations){let j=JSON.parse(JSON.stringify(doc)),c=edit(csv,j);try{audit(c,j);}catch(e){caught++;continue;}throw Error("false acceptance at "+caught);}
 return caught;
}
if(typeof module!=="undefined"&&require.main===module){
 const fs=require("node:fs"),csv=fs.readFileSync(process.argv[2],"utf8"),doc=JSON.parse(fs.readFileSync(process.argv[3],"utf8"));
 audit(csv,doc);console.log(JSON.stringify({status:"PASS",nonblind_internal_E1:true,worlds:81,designs:18,mutations_rejected:mutationTests(csv,doc)}));
}
