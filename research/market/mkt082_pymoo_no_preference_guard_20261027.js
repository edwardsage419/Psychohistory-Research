#!/usr/bin/env node
// MKT082 pinned source audit, Node >=18. No network calls.
const fs=require("fs"),crypto=require("crypto");
const sha=s=>crypto.createHash("sha1").update("blob "+Buffer.byteLength(s)+"\0"+s).digest("hex");
function audit(src,tests){
 let checks=0;const check=(v,m)=>{checks++;if(!v)throw Error(m);};
 check(/rank,\s*F\s*=\s*self\.pop\.get\("rank",\s*"F"\)/.test(src),"population rank origin");
 check(/if len\(set\(rank\)\) == 0:/.test(src),"no-preference guard");
 check(/dm_ranks\s*=\s*PINSGA2\._get_pairwise_ranks/.test(src),"pairwise path");
 check(/elif preference == "c":\s*\n\s*group\.append\(i\)/.test(src),"ties supported");
 check(/return np\.array\(ranks\) \+ 1/.test(src),"rank conversion");
 let populationVectors=0,allTieCases=0;
 for(let n=2;n<=6;n++){
  check(new Set(Array(n).fill(1)).size===1,"all tied ranks");allTieCases++;
  for(let code=0;code<3**n;code++){
   let k=code,rank=[];
   for(let i=0;i<n;i++){rank.push(k%3);k=Math.floor(k/3);}
   check(new Set(rank).size!==0,"unreachable guard "+n+":"+code);populationVectors++;
  }
 }
 return {checks,populationVectors,allTieCases,explicitAllTieInInspectedTest:/all.?tie|all.?equal|no.?preference/i.test(tests)};
}
if(require.main===module){
 if(process.argv.length!==4)throw Error("usage: node script.js pinned_pinsga2.py pinned_test.py");
 const src=fs.readFileSync(process.argv[2],"utf8"),tests=fs.readFileSync(process.argv[3],"utf8");
 if(sha(src)!=="207726ffba920eca75f739b2d0cccaf0c23d92b8")throw Error("source SHA mismatch");
 if(sha(tests)!=="5ad77aeb58797a8f72ab0bb3ff221bc14f19ac5a")throw Error("test SHA mismatch");
 console.log(JSON.stringify(audit(src,tests),null,2));
}
module.exports={audit};
