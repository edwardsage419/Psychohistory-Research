/* R170 third-method observation ladder. Node.js 18+, no dependencies.
 * Frozen protocol: protocols/R170_OBSERVATION_LADDER_THIRD_METHOD_FREEZE_2026-10-26.md
 * Main route: directed contact and conditional delivered-token mixture.
 * Secondary route: undirected edge, orientation, utterance and flip branches.
 * E1 finite artificial process only.
 */
"use strict";
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const r=a%b;a=b;b=r;}return a;}
class Q{
 constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);this.n=n/g;this.d=d/g;}
 add(b){return new Q(this.n*b.d+b.n*this.d,this.d*b.d);}
 sub(b){return new Q(this.n*b.d-b.n*this.d,this.d*b.d);}
 mul(b){return new Q(this.n*b.n,this.d*b.d);}
 div(b){return new Q(this.n*b.d,this.d*b.n);}
 abs(){return new Q(this.n<0n?-this.n:this.n,this.d);}
 toString(){return this.d===1n?String(this.n):this.n+"/"+this.d;}
}
const Z=new Q(0),ONE=new Q(1),HALF=new Q(1,2);
const graphs=[
 ["path",[[0,1],[1,2],[2,3]]],
 ["star",[[0,1],[0,2],[0,3]]],
 ["cycle",[[0,1],[0,3],[1,2],[2,3]]],
 ["complete",[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]]
];
const starts=[["split","1122"],["alternate","1212"],["bilingual","1323"]];
const noises=[Z,new Q(1,4),HALF],modes=["both_confirm","listener_only"],levels=["O1","O2","O3","O4"];
function plus(m,k,v){m.set(k,(m.get(k)||Z).add(v));}
function update(inv,s,h,w,mode){const a=inv.split("").map(Number);if((a[h]&w)!==0){a[h]=w;if(mode==="both_confirm")a[s]=w;}else a[h]|=w;return a.join("");}
function mainKernel(edges,inv,nu,mode){
 const out=new Map(),directed=edges.flatMap(([u,v])=>[[u,v],[v,u]]);
 for(const [s,h] of directed){
  const mask=Number(inv[s]),pA=mask===1?ONE.sub(nu):mask===2?nu:HALF;
  for(const [w,p] of [[1,pA],[2,ONE.sub(pA)]])if(p.n!==0n)plus(out,update(inv,s,h,w,mode),p.div(new Q(directed.length)));
 }
 return out;
}
function secondaryKernel(edges,inv,nu,mode){
 const out=new Map();
 for(const [u,v] of edges)for(const [s,h] of [[u,v],[v,u]]){
  const words=[1,2].filter(w=>(Number(inv[s])&w)!==0);
  for(const spoken of words)for(const [w,p] of [[spoken,ONE.sub(nu)],[3-spoken,nu]]){
   if(p.n===0n)continue;
   plus(out,update(inv,s,h,w,mode),p.div(new Q(2*edges.length*words.length)));
  }
 }
 return out;
}
function path(edges,start,nu,mode,kernel){
 let dist=new Map([[start,ONE]]),out=[dist];
 for(let t=1;t<=3;t++){
  const next=new Map();
  for(const [inv,mass] of dist)for(const [later,p] of kernel(edges,inv,nu,mode))plus(next,later,mass.mul(p));
  dist=next;out.push(dist);
 }
 return out;
}
function signature(m){return [...m].sort((a,b)=>a[0].localeCompare(b[0])).map(([k,v])=>k+":"+v).join(";");}
function normalized(m){let s=Z;for(const [k,p] of m){s=s.add(p);if(p.n<0n||!/^[123]{4}$/.test(k))throw Error("invalid state");}if(s.toString()!=="1")throw Error("non-normalized");}
function projection(inv,edges,level){
 if(level==="O4")return inv;
 const h=[1,2,3].map(k=>[...inv].filter(x=>Number(x)===k).length);
 if(level==="O1")return String(h[2]);
 if(level==="O2")return h.join(",");
 const disjoint=edges.filter(([u,v])=>(Number(inv[u])&Number(inv[v]))===0).length;
 return h.join(",")+"|"+disjoint;
}
function law(dist,edges,level){const out=new Map();for(const [inv,p] of dist)plus(out,projection(inv,edges,level),p);return out;}
function tv(a,b){let s=Z;for(const k of new Set([...a.keys(),...b.keys()]))s=s.add((a.get(k)||Z).sub(b.get(k)||Z).abs());return s.div(new Q(2));}
function classesFor(six,laws){
 const groups=new Map();
 for(let i=0;i<six.length;i++){const s=signature(laws[i]);if(!groups.has(s))groups.set(s,[]);groups.get(s).push(i);}
 const sizes=[...groups.values()].map(x=>x.length),unique=sizes.filter(x=>x===1).length;
 return {classes:groups.size,unique,ambiguous:6-unique,distinguishable_pairs:15-sizes.reduce((s,n)=>s+n*(n-1)/2,0)};
}
function run(){
 const aggregate={},strata=[];let equalSnapshots=0,normalizedSnapshots=0,mono=0,witness=null;
 for(const [graph,edges] of graphs)for(const [initial,start] of starts){
  const six=noises.flatMap(nu=>modes.map(mode=>({nu,mode}))),paths=[];
  for(const {nu,mode} of six){
   const a=path(edges,start,nu,mode,mainKernel),b=path(edges,start,nu,mode,secondaryKernel);
   for(let t=0;t<=3;t++){normalized(a[t]);normalized(b[t]);if(signature(a[t])!==signature(b[t]))throw Error("kernel route mismatch "+graph+initial+nu+mode+t);equalSnapshots++;normalizedSnapshots++;}
   paths.push(a);
  }
  if(initial!=="bilingual"&&signature(paths[0][1])===signature(paths[1][1]))mono++;
  else if(initial!=="bilingual")throw Error("noiseless monolingual first-step mismatch");
  for(let t=1;t<=3;t++){
   const rec={graph,initial,t};const byLevel={};
   for(const level of levels){
    const laws=paths.map(p=>law(p[t],edges,level));
    byLevel[level]=laws;
    rec[level]=classesFor(six,laws);
    const key="t"+t+"_"+level,old=aggregate[key]||{classes:0,unique:0,ambiguous:0,distinguishable_pairs:0};
    for(const k of Object.keys(old))old[k]+=rec[level][k];
    aggregate[key]=old;
   }
   for(let j=1;j<4;j++)if(rec[levels[j]].classes<rec[levels[j-1]].classes)throw Error("observation refinement violation");
   strata.push(rec);
   if(!witness)for(let i=0;i<6&&!witness;i++)for(let j=i+1;j<6&&!witness;j++){
    const d1=tv(byLevel.O1[i],byLevel.O1[j]),d4=tv(byLevel.O4[i],byLevel.O4[j]);
    if(d1.n===0n&&d4.n>0n)witness={graph,initial,t,control_a:[six[i].nu.toString(),six[i].mode],control_b:[six[j].nu.toString(),six[j].mode],tv_O1:d1.toString(),tv_O4:d4.toString()};
   }
  }
 }
 const edges=graphs[0][1],base=path(edges,starts[2][1],new Q(1,4),"both_confirm",mainKernel)[1];
 const mutated=path(edges,starts[2][1],new Q(1,3),"both_confirm",mainKernel)[1];
 const mutation=tv(base,mutated).toString();if(mutation==="0")throw Error("mutation undetected");
 if(strata.length!==36||equalSnapshots!==288||mono!==8)throw Error("unexpected experiment size");
 return {schema:"r170_observation_ladder_exact_v1",date:"2026-10-26",evidence:"E1_INTERNAL_FINITE_ONLY",worlds:72,strata_count:12,within_stratum_pairs:180,full_state_snapshot_route_equalities:equalSnapshots,normalized_snapshots:normalizedSnapshots,monolingual_nu0_first_step_equal_strata:mono,mutation_t1_full_TV:mutation,first_witness:witness,aggregate,strata,real_E2_scored:0,historical_E3_scored:0,external_replications:0};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
