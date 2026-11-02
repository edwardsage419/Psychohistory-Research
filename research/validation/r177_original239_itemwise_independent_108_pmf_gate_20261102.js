#!/usr/bin/env node
"use strict";
// R177 original239 08-001 independent exact PMF oracle. Node standard library.
const PIN="57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535";
function ok(x,s){if(!x)throw Error(s);}
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a;}
function q(a,b=1n){a=BigInt(a);b=BigInt(b);ok(b!==0n,"zero denominator");if(b<0n){a=-a;b=-b;}let g=gcd(a,b);return [a/g,b/g];}
function p(s){ok(typeof s==="string"&&/^-?\d+(\/[1-9]\d*)?$/.test(s),"bad rational");let z=s.split("/");return q(z[0],z[1]||1);}
function a(x,y){return q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);}
function m(x,y){return q(x[0]*y[0],x[1]*y[1]);}
function d(x,y){return q(x[0]*y[1],x[1]*y[0]);}
function sub(x,y){return a(x,[-y[0],y[1]]);}
function eq(x,y){return x[0]===y[0]&&x[1]===y[1];}
function pw(x,n){let z=q(1);for(let i=0;i<n;i++)z=m(z,x);return z;}
function c(n,k){if(k<0||k>n)return 0n;let z=1n;for(let i=1;i<=Math.min(k,n-k);i++)z=z*BigInt(n-i+1)/BigInt(i);return z;}
function rising(x,n){let z=q(1);for(let i=0;i<n;i++)z=m(z,a(x,q(i)));return z;}
const O=q(1),Z=q(0),cs=[2,4,8],Ns=[24,48,72],zs=["1/8","1/4","1/3"];
function bin(n,p,k){return m(q(c(n,k)),m(pw(p,k),pw(sub(O,p),n-k)));}
function pmf(f,n,p,r,k){
 if(f==="BIN")return bin(n,p,k);
 if(f==="BB"){let C=q(cs[r]);return m(q(c(n,k)),d(m(rising(m(p,C),k),rising(m(sub(O,p),C),n-k)),rising(C,n)));}
 if(f==="HG"){let N=Ns[r],K=Number(d(m(p,q(N)),O)[0]);return q(c(K,k)*c(N-K,n-k),c(N,n));}
 if(f==="ZIB"){let z=pRat(zs[r]),v=d(p,sub(O,z));return a(k===0?z:Z,m(sub(O,z),bin(n,v,k)));}
 throw Error("family");
}
function pRat(s){return p(s);}
function audit(x){
 ok(x.research_id==="R177"&&x.worlds===108&&x.full_PMF_probability_cells===972,"summary");
 ok(x.new_E2===0&&x.new_E3===0&&x.real_social_events_or_historical_data===false,"grade");
 ok(Array.isArray(x.world_data)&&x.world_data.length===108,"world count");
 let seen=new Set(),cells=0,groups=new Map();
 for(const w of x.world_data){
  ok(["BIN","BB","HG","ZIB"].includes(w.family)&&[4,8,12].includes(w.n)&&["1/8","1/4","1/2"].includes(w.p)&&[0,1,2].includes(w.regime),"world identity");
  let key=[w.family,w.n,w.p,w.regime].join("|");ok(!seen.has(key),"duplicate "+key);seen.add(key);
  let ex=w.family==="BB"?{concentration:String(cs[w.regime])}:w.family==="HG"?{population:String(Ns[w.regime])}:w.family==="ZIB"?{structural_zero:zs[w.regime]}:{};
  ok(JSON.stringify(w.extra)===JSON.stringify(ex),"extra "+key);
  let P=p(w.p),mass=Z,mean=Z,second=Z;
  ok(w.full_PMF.length===w.n+1&&w.count_support.length===w.n+1,"support");
  for(let k=0;k<=w.n;k++){
   ok(w.count_support[k]===k,"support order");let v=pmf(w.family,w.n,P,w.regime,k);
   ok(eq(v,p(w.full_PMF[k])),"PMF "+key+" k"+k);
   mass=a(mass,v);mean=a(mean,m(q(k),v));second=a(second,m(q(k*k),v));cells++;
  }
  ok(eq(mass,O)&&eq(mean,m(q(w.n),P)),"mass mean "+key);
  let variance=sub(second,pw(mean,2));
  ok(eq(variance,p(w.variance))&&eq(mean,p(w.mean))&&eq(p(w.p_zero),pmf(w.family,w.n,P,w.regime,0)),"moments "+key);
  let g=[w.n,w.p,w.regime].join("|");if(!groups.has(g))groups.set(g,{});
  groups.get(g)[w.family]={variance,zero:pmf(w.family,w.n,P,w.regime,0)};
 }
 ok(seen.size===108&&cells===972&&groups.size===27&&x.distinct_parameter_worlds===90,"universe");
 for(let [key,g] of groups){
  ok(Object.keys(g).length===4,"family group "+key);
  ok(sub(g.BIN.variance,g.HG.variance)[0]>0n&&sub(g.BB.variance,g.BIN.variance)[0]>0n&&sub(g.ZIB.variance,g.BIN.variance)[0]>0n,"variance order");
  ok(sub(g.BIN.zero,g.HG.zero)[0]>0n&&sub(g.BB.zero,g.BIN.zero)[0]>0n&&sub(g.ZIB.zero,g.BIN.zero)[0]>0n,"zero order");
 }
 let alias=x.two_different_mechanisms_identical_full_count_PMF;
 for(let k=0;k<3;k++){
  let bb=m(q(c(2,k)),d(m(rising(q(1),k),rising(q(1),2-k)),rising(q(2),2)));
  let zib=a(k===0?q(1,4):Z,m(q(3,4),bin(2,q(2,3),k)));
  ok(eq(bb,q(1,3))&&eq(zib,bb)&&eq(p(alias.BB_c2_alpha1_beta1_pmf[k]),bb)&&eq(p(alias.ZIB_z_quarter_q_two_thirds_pmf[k]),zib),"alias");
 }
 return {status:"PASS",worlds:seen.size,cells,groups:groups.size,unique_parameters:90,alias:"THREE_EXACT_THIRDS",grade:"INTERNAL_NONBLIND_ARTIFICIAL_E1",new_E2:0,new_E3:0};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs"),crypto=require("crypto");
 ok(process.argv[2],"usage: node audit.js R177_EXACT_RESULTS.json");
 const bytes=fs.readFileSync(process.argv[2]);
 ok(crypto.createHash("sha256").update(bytes).digest("hex")===PIN,"archive SHA256");
 console.log(JSON.stringify(audit(JSON.parse(bytes.toString("utf8")))));
}
