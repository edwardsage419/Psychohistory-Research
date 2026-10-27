"use strict";
/* R223 S19: exact scenario grid, no packages. node script.js R223_EXACT_RESULTS.json */
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;}
function Q(n,d=1n){if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
function parse(x){const z=String(x).split("/");return Q(BigInt(z[0]),BigInt(z[1]||1));}
function div(a,b){return Q(a[0]*b[1],a[1]*b[0]);}
function le(a,b){return a[0]*b[1]<=b[0]*a[1];}
function fmt(a){return a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);}
function main(source){
 if(source.research_id!=="R223"||source.worlds.length!==7||source.all_structural_atoms!==448)throw Error("wrong frozen source");
 const gammas=[1,2,3,5,7,15],rows=[],perWorld=[];
 for(const w of source.worlds){
  const observed=parse(w.observed_RR),truth=parse(w.true_causal_RR);
  let nullCompatible=0,covered=0;
  for(const e of gammas)for(const d of gammas){
   const B=Q(BigInt(e*d),BigInt(e+d-1)),lower=div(observed,B);
   const coveredOracle=w.oracle_sensitivity_RR_EU===null?null:(le(parse(w.oracle_sensitivity_RR_EU),Q(BigInt(e)))&&le(parse(w.oracle_sensitivity_RR_UD),Q(BigInt(d))));
   if(coveredOracle===true){covered++;if(!le(lower,truth))throw Error("oracle coverage contradiction "+w.world+" "+e+" "+d);}
   const nullOK=le(lower,Q(1n));if(nullOK)nullCompatible++;
   rows.push({world:w.world,Gamma_E:e,Gamma_D:d,assumed_B:fmt(B),RR_lower:fmt(lower),null_compatible:nullOK,oracle_parameter_covered:coveredOracle});
  }
  perWorld.push({world:w.world,observed_RR:w.observed_RR,true_RR:w.true_causal_RR,null_compatible_count:nullCompatible,oracle_covered_count:covered});
 }
 if(rows.length!==252)throw Error("wrong grid length");
 const a=rows.filter(x=>x.world==="NULL_CONFOUNDED"),b=rows.filter(x=>x.world==="CAUSAL_ALIAS");
 if(a.length!==36||b.length!==36||a.some((x,i)=>x.RR_lower!==b[i].RR_lower||x.null_compatible!==b[i].null_compatible))throw Error("alias mismatch");
 function get(e,d){return a.find(x=>x.Gamma_E===e&&x.Gamma_D===d);}
 if(get(3,5).RR_lower!=="77/75"||get(3,5).null_compatible||get(3,7).RR_lower!=="33/35"||!get(3,7).null_compatible)throw Error("prespecified counterexample failed");
 return {rows,summary:{research_id:"R223",supplement:"S19",evidence:"E1_SYNTHETIC",input_git_blob:"3a3f2143357832e25ddf483d7ebd4d66298c5dd1",source_structural_atoms:448,worlds:7,gamma_grid:[1,2,3,5,7,15],conditions:rows.length,oracle_covered_conditions:perWorld.reduce((a,x)=>a+x.oracle_covered_count,0),per_world:perWorld,R073:"FROZEN",PESEN_v0_1:"FROZEN",new_E2:0,new_E3:0,external_independent_reproductions:0}};
}
if(typeof require!=="undefined"&&require.main===module){const fs=require("fs");const s=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));process.stdout.write(JSON.stringify(main(s),null,2)+"\n");}
