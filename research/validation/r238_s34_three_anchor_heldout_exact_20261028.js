"use strict";
// R238 S34. Exact rational geometry. Run with Node standard library.
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b];}return a;};
function F(x){if(typeof x==="object"&&x.n!==undefined)return x;let [a,b="1"]=String(x).split("/");let n=BigInt(a),d=BigInt(b);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);return {n:n/g,d:d/g};}
function calc(a,b,o){a=F(a);b=F(b);let n,d;if(o==="+"){n=a.n*b.d+b.n*a.d;d=a.d*b.d;}else if(o==="-"){n=a.n*b.d-b.n*a.d;d=a.d*b.d;}else if(o==="*"){n=a.n*b.n;d=a.d*b.d;}else{n=a.n*b.d;d=a.d*b.n;}if(!d)throw Error("division by zero");return F(n+"/"+d);}
const add=(a,b)=>calc(a,b,"+"),sub=(a,b)=>calc(a,b,"-"),mul=(a,b)=>calc(a,b,"*"),div=(a,b)=>calc(a,b,"/"),txt=x=>{x=F(x);return x.d===1n?String(x.n):x.n+"/"+x.d;},z=F(0);
const minus=(a,b)=>[sub(a[0],b[0]),sub(a[1],b[1])],norm=v=>add(mul(v[0],v[0]),mul(v[1],v[1]));
const ok=(v,m)=>{if(!v)throw Error(m);};
function apply(H,v){return [add(mul(H[0][0],v[0]),mul(H[0][1],v[1])),add(mul(H[1][0],v[0]),mul(H[1][1],v[1]))];}
function inverse(X){let d=sub(mul(X[0][0],X[1][1]),mul(X[0][1],X[1][0]));ok(d.n!==0n,"singular anchor pair");return [[div(X[1][1],d),div(sub(z,X[0][1]),d)],[div(sub(z,X[1][0]),d),div(X[0][0],d)]];}
function product(X,Y){return [0,1].map(i=>[0,1].map(j=>add(mul(X[i][0],Y[0][j]),mul(X[i][1],Y[1][j]))));}
function run(csv,source){
 const lines=csv.trim().split(/\r?\n/),header=lines.shift().split(",");
 ok(lines.length===144,"144 original records");
 const groups={};let source_checks=0;
 for(const line of lines){
  const cells=line.split(",");ok(cells.length===header.length,"CSV width");
  const r=Object.fromEntries(header.map((k,i)=>[k,cells[i]]));
  const {world,time,word,oracle_sense}=r;
  ok(["0","1"].includes(time)&&["A","B","C","D"].includes(word)&&["0","1"].includes(oracle_sense),"source domain");
  groups[world]??={};groups[world][time]??={};groups[world][time][word]??={};
  ok(!groups[world][time][word][oracle_sense],"duplicate source");
  groups[world][time][word][oracle_sense]={v:[F(r.observed_embedding_x),F(r.observed_embedding_y)],p:F(r.original_structural_source_probability)};
  source_checks++;
 }
 ok(Object.keys(groups).length===9,"nine original worlds");
 const pairs=[["A","B","C"],["A","C","B"],["B","C","A"]],worlds=[];
 for(const old of source.world_results){
  const g=groups[old.world];ok(g,"missing world");
  const v={};
  for(const t of ["0","1"]){
   v[t]={};let total=z;
   for(const w of ["A","B","C","D"]){
    const x=g[t][w];ok(x&&x["0"]&&x["1"],"missing sense");
    ok(x["0"].v.every((n,k)=>txt(n)===txt(x["1"].v[k])),"sense observation mismatch");
    v[t][w]=x["0"].v;total=add(total,add(x["0"].p,x["1"].p));
    ok(v[t][w].every((n,k)=>txt(n)===old.observed_embeddings_by_time[t][w][k]),"source/reference mismatch");
    source_checks+=3;
   }
   ok(txt(total)==="1/2","period source mass");source_checks++;
  }
  const out=[];
  for(const [i,j,k] of pairs){
   const X1=[[v["1"][i][0],v["1"][j][0]],[v["1"][i][1],v["1"][j][1]]];
   const X0=[[v["0"][i][0],v["0"][j][0]],[v["0"][i][1],v["0"][j][1]]];
   const H=product(X0,inverse(X1));
   const hold=norm(minus(apply(H,v["1"][k]),v["0"][k]));
   const d=norm(minus(apply(H,v["1"].D),v["0"].D));
   ok(hold.n>=0n&&d.n>=0n,"negative squared norm");
   out.push({pair:i+j,heldout:k,heldout_residual_sq:txt(hold),target_D_aligned_displacement_sq:txt(d)});
  }
  worlds.push({world:old.world,anchor_consistency:out.every(x=>x.heldout_residual_sq==="0")?"ANCHOR_CONSISTENT":"ANCHOR_INCONSISTENT",pairs:out,oracle_target_D_semantic_change_sq:old.oracle_true_target_D_semantic_centroid_change_squared});
 }
 const by=Object.fromEntries(worlds.map(x=>[x.world,x]));
 ok(JSON.stringify(by.STABLE_BASE.pairs)===JSON.stringify(by.SENSE_RECONFIGURATION_ALIAS.pairs),"alias mismatch");
 for(const n of ["STABLE_BASE","GLOBAL_ROTATION","GLOBAL_SCALE_2","FREQUENCY_COMPOSITION_ONLY","TARGET_SEMANTIC_DRIFT","ROTATED_TARGET_DRIFT","FREQUENCY_PLUS_TARGET_DRIFT"])
  ok(by[n].anchor_consistency==="ANCHOR_CONSISTENT","anchor expected consistency "+n);
 ok(by.ANCHOR_DRIFT_FALSE_ALIGNMENT.anchor_consistency==="ANCHOR_INCONSISTENT","anchor contamination");
 for(const n of ["STABLE_BASE","GLOBAL_ROTATION","GLOBAL_SCALE_2","FREQUENCY_COMPOSITION_ONLY"])
  ok(by[n].pairs.every(x=>x.target_D_aligned_displacement_sq==="0"),"negative control");
 for(const n of ["TARGET_SEMANTIC_DRIFT","ROTATED_TARGET_DRIFT","FREQUENCY_PLUS_TARGET_DRIFT"])
  ok(by[n].pairs.every(x=>x.target_D_aligned_displacement_sq==="1"),"positive control");
 return {research_id:"R238_S34",evidence:"E1_ONLY",prescore_protocol_commit:"9cd6087d9e4f8e399eb05c02e66e9cb875af7f7a",source_csv_sha256_frozen:"a3939283f67d40fc74d289daecde449566870cdeb1943a8431ae6d27457feceb",original_source_records:lines.length,world_count:worlds.length,anchor_pair_conditions:worlds.length*3,source_checks,worlds,new_E2:0,new_E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN"};
}
if(typeof module!=="undefined")module.exports={run};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs");
 const csv=fs.readFileSync("research/R238/R238_ALL_144_ORIGINAL_HIDDEN_SENSE_AND_OBSERVED_EMBEDDING_SOURCES.csv","utf8");
 const source=JSON.parse(fs.readFileSync("research/R238/R238_EXACT_RESULTS.json","utf8"));
 console.log(JSON.stringify(run(csv,source),null,2));
}