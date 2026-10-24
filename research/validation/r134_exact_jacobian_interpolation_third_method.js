(function () {
"use strict";
// R134 frozen third method, Node.js standard library only. Exact integer arithmetic.
const worldValues = [-1,0,1], residents = [1,2,3], mutants = [0,1,3,4];
const eps2 = [0,1,2];
const assert = (ok, msg) => { if (!ok) throw new Error(msg); };
const gcd = (x,y) => { x=Math.abs(x); y=Math.abs(y); while(y){const t=x%y;x=y;y=t;}return x||1; };
const frac = (n,d=1) => { assert(d!==0,"zero denominator"); if(d<0){n=-n;d=-d;}const g=gcd(n,d);return (d/g===1)?String(n/g):String(n/g)+"/"+String(d/g); };
// Direct source Eq.1: total resident-minus-mutant payoff at mixed population e/2.
// Frequencies are represented by integers in quarters; payoff numerator has denominator 32.
function directNumerator(a,b,c,d,x4,y4,r4,s4,e2) {
  const X=2*x4+e2*(r4-x4),Y=2*y4+e2*(s4-y4);
  const fDiff=a*(8-2*X)+2*b*(2*Y-8);
  const gDiff=2*c*(2*X-8)+d*(8-2*Y);
  return (x4-r4)*fDiff+(y4-s4)*gDiff;
}
// Independent quadratic-form expansion Q, denominator 16.
function qNumerator(a,b,c,d,x4,y4,r4,s4) {
  const dx=r4-x4,dy=s4-y4;
  return -2*a*dx*dx+4*(b+c)*dx*dy-2*d*dy*dy;
}
// Two-population replicator vector field, each component denominator 512.
// Coordinates use eighths. This function is algebraically separate from directNumerator.
function fieldNumerator(a,b,c,d,x8,y8) {
  return [
    x8*(8-x8)*(a*(8-2*x8)+2*b*(2*y8-8)),
    y8*(8-y8)*(2*c*(2*x8-8)+d*(8-2*y8))
  ];
}
// Four-point symmetric derivative stencil, h=1/8. Exact for cubic polynomials.
function stencil(a,b,c,d,component,axis) {
  const f=(t)=>axis===0?fieldNumerator(a,b,c,d,t,4)[component]:fieldNumerator(a,b,c,d,4,t)[component];
  return -f(6)+8*f(5)-8*f(3)+f(2); // result /768
}
function classify(trace2,det4) {
  if(det4<0)return "saddle";
  if(det4===0)return "nonhyperbolic";
  if(trace2<0)return "asymptotically_stable_linear";
  if(trace2>0)return "unstable_linear";
  return "linear_center_inconclusive";
}
const rows=[],counts={}, examples={};
let triples=0, directCalls=0, midpointChecks=0, qChecks=0, jacobianChecks=0;
for(const a of worldValues)for(const b of worldValues)for(const c of worldValues)for(const d of worldValues){
  const j00=stencil(a,b,c,d,0,0),j01=stencil(a,b,c,d,0,1);
  const j10=stencil(a,b,c,d,1,0),j11=stencil(a,b,c,d,1,1);
  assert(j00===-384*a && j01===768*b && j10===768*c && j11===-384*d,"Jacobian stencil mismatch");
  jacobianChecks+=4;
  const tr2=-(a+d), det4=a*d-4*b*c, discr4=(a-d)*(a-d)+16*b*c;
  const category=classify(tr2,det4);
  const unilateralStrict=(a>0&&d>0);
  const jointSaddle=unilateralStrict&&det4<0;
  counts[category]=(counts[category]||0)+1;
  if(jointSaddle)examples[[a,b,c,d].join(",")]=true;
  rows.push([a,b,c,d,frac(tr2,2),frac(det4,4),frac(discr4,4),category,
    unilateralStrict?"true":"false",jointSaddle?"true":"false",
    frac(j00,768),frac(j01,768),frac(j10,768),frac(j11,768)].join(","));
  for(const x4 of residents)for(const y4 of residents)for(const r4 of mutants)for(const s4 of mutants){
    const n0=directNumerator(a,b,c,d,x4,y4,r4,s4,0);
    const nh=directNumerator(a,b,c,d,x4,y4,r4,s4,1);
    const n1=directNumerator(a,b,c,d,x4,y4,r4,s4,2);
    directCalls+=3;triples++;
    assert(2*nh===n0+n1,"interpolation mismatch");
    midpointChecks++;
    const q=qNumerator(a,b,c,d,x4,y4,r4,s4);
    assert(n1-n0===-2*q,"quadratic form mismatch");
    qChecks++;
  }
}
assert(rows.length===81&&triples===11664&&directCalls===34992,"grid cardinality");
assert(jacobianChecks===324&&midpointChecks===11664&&qChecks===11664,"audit cardinality");
assert(classify(-2,4)==="asymptotically_stable_linear","positive control stable");
assert(classify(-2,-3)==="saddle","positive control saddle");
assert(classify(0,4)==="linear_center_inconclusive","positive control center");
const negativeJacobian = stencil(1,1,0,1,0,1)!==2*768;
const negativeQuadratic = (()=> {
  const a=1,b=1,c=0,d=1,x=1,y=1,r=3,s=3;
  const n0=directNumerator(a,b,c,d,x,y,r,s,0);
  const n1=directNumerator(a,b,c,d,x,y,r,s,2);
  const dx=r-x,dy=s-y;
  const wrongQ=-2*a*dx*dx-2*d*dy*dy;
  return n1-n0!==-2*wrongQ;
})();
assert(negativeJacobian&&negativeQuadratic,"negative control escaped");
const headers="a,b,c,d,trace,determinant,discriminant,linear_class,unilateral_strict_both,joint_saddle_despite_unilateral,j00,j01,j10,j11";
const csv=headers+"\n"+rows.join("\n")+"\n";
const receipt={
  research_id:"R134",date:"2026-10-25",source:"Taylor 1979 DOI 10.2307/3213376",
  prior_protocol:"research/validation/R134_THIRD_METHOD_EXACT_JACOBIAN_INTERPOLATION_PROTOCOL_FREEZE_2026-10-25.md",
  scope:"internal_exact_synthetic_E1",worlds:81,resident_mutant_combinations:11664,
  direct_source_evaluations:directCalls,midpoint_interpolation_exact_checks:midpointChecks,
  quadratic_form_exact_checks:qChecks,exact_jacobian_entry_checks:jacobianChecks,
  counts,unilateral_strict_worlds:rows.filter(x=>x.includes(",true,")).length,
  joint_saddle_worlds:Object.keys(examples).length,joint_saddle_parameters:Object.keys(examples),
  negative_controls:{wrong_cross_jacobian_rejected:negativeJacobian,omitted_cross_Q_rejected:negativeQuadratic},
  new_E2:0,new_E3:0,external_independent_replication:false,
  original_R134_zip_executed_this_run:false,CI_run_this_turn:false
};
if(typeof require!=="undefined" && typeof module!=="undefined" && require.main===module){
  const fs=require("fs");
  fs.writeFileSync("R134_THIRD_METHOD_81_EXACT_JACOBIANS_2026-10-25.csv",csv);
  fs.writeFileSync("R134_THIRD_METHOD_EXACT_AUDIT_RECEIPT_2026-10-25.json",JSON.stringify(receipt,null,2)+"\n");
  console.log(JSON.stringify(receipt,null,2));
}
return {csv,receipt};
})()
