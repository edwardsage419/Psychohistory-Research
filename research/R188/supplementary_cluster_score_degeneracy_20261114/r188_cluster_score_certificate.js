#!/usr/bin/env node
"use strict";
/*
 * Independent analytic certificate for R188 postscore cluster-score degeneracy.
 * Run from repository root:
 *   node research/R188/supplementary_cluster_score_degeneracy_20261114/r188_cluster_score_certificate.js
 * Uses Node standard library only. It verifies the exact Git blob of frozen R188 data.
 * The companion downloadable Python experiment also independently rebuilds every row.
 */
const fs=require("fs"), crypto=require("crypto");
const sourcePath="research/R188/R188_EXACT_RESULTS.json";
const raw=fs.readFileSync(sourcePath);
const h=crypto.createHash("sha1").update(Buffer.from("blob "+raw.length+"\0")).update(raw).digest("hex");
if(h!=="9d57c24f6327f1e0ce5c83cba4d55174bded1292")
  throw Error("R188 source Git blob mismatch: fail closed");
const source=JSON.parse(raw.toString("utf8"));
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b];}return a;}
function q(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);return [n/g,d/g];}
function from(s){s=String(s);const a=s.split("/");return q(a[0],a[1]??1);}
function mul(a,b){return q(a[0]*b[0],a[1]*b[1]);}
function add(a,b){return q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function sub(a,b){return q(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);}
function div(a,b){return q(a[0]*b[1],a[1]*b[0]);}
function sq(a){return mul(a,a);}
function same(a,b){return a[0]===b[0]&&a[1]===b[1];}
function st(a){return a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);}
function sum(v){return v.reduce((a,b)=>add(a,b),q(0));}
function ensure(x,m){if(!x)throw Error(m);}
const rows=[];
const delta=q(1,16);
for(const w of source.all_worlds){
  const k=w.group_exposure_count_k;
  ensure(k.length===6&&k.every(v=>[2,4,6].includes(v)),"bad group design");
  const Sg=k.map(v=>q(v*(8-v),8));
  const S=sum(Sg), e=from(w.original_error_magnitude), b=from(w.true_within_b);
  const sse=mul(q(48),sq(e));
  ensure(same(sse,from(w.residual_SSE_exact)),"R188 residual identity mismatch");
  ensure(same(b,from(w.within_FE_x_slope)),"R188 FE source mismatch");
  const hc0=div(sq(e),S);
  const homo=div(sse,mul(q(41),S));
  const firstWithin=sub(q(0),q(k[0],8));
  const dBeta=div(mul(delta,firstWithin),S);
  const scores=Sg.map((sg,i)=>sub(i===0?mul(delta,firstWithin):q(0),mul(dBeta,sg)));
  const CRperturbed=div(sum(scores.map(sq)),sq(S));
  ensure(CRperturbed[0]>0n&&dBeta[0]!==0n,"perturbation did not break degeneracy");
  rows.push({
    design:w.design,a:w.true_a,b:w.true_within_b,c:w.true_context_c,
    e:w.original_error_magnitude,Sxx:st(S),SSE:st(sse),
    FE_beta:w.within_FE_x_slope,FE_cluster_scores:["0","0","0","0","0","0"],
    CR0_variance:"0",HC0_variance:st(hc0),FE_homoskedastic_variance:st(homo),
    perturbed_delta_beta:st(dBeta),perturbed_beta:st(add(b,dBeta)),
    perturbed_CR0_variance:st(CRperturbed)
  });
}
ensure(rows.length===180,"not 180 frozen worlds");
const pos=rows.filter(w=>w.HC0_variance!=="0").length;
ensure(pos===120,"positive HC0 world count mismatch");
const example=rows.find(w=>w.design==="STRONG_BETWEEN"&&w.a==="0"&&w.b==="1/4"&&w.c==="-4"&&w.e==="1/4");
ensure(example&&example.Sxx==="9"&&example.HC0_variance==="1/144"&&example.FE_homoskedastic_variance==="1/123"&&example.perturbed_beta==="143/576"&&example.perturbed_CR0_variance==="5/1990656","fixed source example mismatch");
console.log(JSON.stringify({
  study:"R188_SOURCE_PINNED_CLUSTER_SCORE_ANALYTIC_CERTIFICATE",
  frozen_R188_results_git_blob:h,worlds:180,clusters_per_world:6,rows_per_cluster:8,
  source_rows:8640,CR0_zero_count:180,HC0_positive_count:pos,
  perturbed_CR0_positive_count:180,example,rows,
  evidence_grade:"ARTIFICIAL_E1_POSTSCORE",new_E2:0,new_E3:0
},null,2));
