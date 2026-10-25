"use strict";
// R147 positive-overlap observational twins. Standard JavaScript, no dependencies.
function main() {
  const cells = Array(8).fill(0);
  const encode = (a,b,c) => 4*a+2*b+c;
  const draw = (coin,u) => Number(coin < (u===1?3:1));
  // Model S: 128 equiprobable elementary worlds.
  for (let u=0;u<2;u++) for(let ac=0;ac<4;ac++)
    for(let bc=0;bc<4;bc++) for(let cc=0;cc<4;cc++)
      cells[encode(draw(ac,u),draw(bc,u),draw(cc,u))]++;
  const symbolic=Array(8).fill(0);
  for(let a=0;a<2;a++) for(let b=0;b<2;b++) for(let c=0;c<2;c++)
    for(let u=0;u<2;u++) {
      const wt=(x)=>x===u?3:1;
      symbolic[encode(a,b,c)]+=wt(a)*wt(b)*wt(c);
    }
  const sTotal=cells.reduce((a,b)=>a+b,0);
  const byA=[cells.slice(0,4).reduce((a,b)=>a+b,0),cells.slice(4).reduce((a,b)=>a+b,0)];
  // Model D: A depends on U, then B,C use a separate joint exogenous W.
  const dCells=Array(8).fill(0);
  function bcFromW(a,w) {
    for(let j=0;j<4;j++){if(w<cells[4*a+j])return [Math.floor(j/2),j%2];w-=cells[4*a+j];}
    throw Error("joint CDF exhausted");
  }
  for(let u=0;u<2;u++) for(let ac=0;ac<4;ac++) for(let w=0;w<64;w++){
    const a=draw(ac,u),[b,c]=bcFromW(a,w);dCells[encode(a,b,c)]++;
  }
  function b1Observed(a) {return cells[4*a+2]+cells[4*a+3];}
  const obsRiskNumerator=b1Observed(1)-b1Observed(0); // denominator 64
  // Surgical do: in S A has no children; in D B,C depend on assigned A.
  const sDoB1=[0,0],dDoB1=[0,0];
  for(let a=0;a<2;a++){
    for(let u=0;u<2;u++) for(let bc=0;bc<4;bc++) for(let cc=0;cc<4;cc++)
      if(draw(bc,u)===1)sDoB1[a]++; // out of 32
    for(let u=0;u<2;u++) for(let w=0;w<64;w++)
      if(bcFromW(a,w)[0]===1)dDoB1[a]++; // out of 128
  }
  const allObservedMatch=cells.every((v,i)=>4*v===dCells[i]&&v===symbolic[i]);
  const positivity=[1,3,3,1].every(x=>x>0&&x<4) && cells.every(x=>x>0);
  const dEffectNumerator=dDoB1[1]-dDoB1[0]; // /128
  const sEffectNumerator=sDoB1[1]-sDoB1[0]; // /32
  // Conditional residual covariance: P(11|A=1) - P(B=1|A=1)P(C=1|A=1).
  const p11Numerator=cells[7], b1=b1Observed(1), c1=cells[5]+cells[7];
  const covNumerator=64*p11Numerator-b1*c1; // denominator 4096
  const wrongIndependentNumerator=b1*c1; // denominator 4096
  const correctJointNumerator=64*p11Numerator; // denominator 4096
  const checks={
    s_128_worlds:sTotal===128,
    symbolic_eight_cells:cells.every((x,i)=>x===symbolic[i]),
    observed_eight_cells_equal:allObservedMatch,
    d_512_worlds:dCells.reduce((a,b)=>a+b,0)===512,
    positivity:positivity&&byA[0]===64&&byA[1]===64,
    observational_risk_diff_quarter:obsRiskNumerator===16,
    diffusion_do_effect_quarter:dEffectNumerator===32,
    shock_do_effect_zero:sEffectNumerator===0,
    residual_joint_seven_sixteenths:p11Numerator===28,
    residual_covariance_three_sixtyfourths:covNumerator===192,
    negative_control_independent_BC_rejected:wrongIndependentNumerator!==correctJointNumerator,
    negative_control_conditioning_as_do_rejected:obsRiskNumerator!==0&&sEffectNumerator===0
  };
  if(Object.values(checks).some(x=>x!==true))throw Error("Frozen protocol FAIL: "+JSON.stringify(checks));
  return {
    protocol:"R147_POSITIVE_OVERLAP_CAUSAL_TWIN_PROTOCOL_FREEZE_2026-10-25.md",
    evidence:"E1_SYNTHETIC_EXACT_ONLY",
    elementary_worlds_S:128, elementary_worlds_D:512,
    cell_order:"000,001,010,011,100,101,110,111",
    S_cell_numerators_over_128:cells,
    D_cell_numerators_over_512:dCells,
    symbolic_cell_numerators_over_128:symbolic,
    A_assignment_given_U_0:["3/4","1/4"],
    A_assignment_given_U_1:["1/4","3/4"],
    observed_B_risk_difference:"1/4",
    do_A_effect_on_B_S:"0",
    do_A_effect_on_B_D:"1/4",
    P_B1_C1_given_A1:"7/16",
    conditional_BC_covariance_given_A1:"3/64",
    wrong_independent_BC_P11_given_A1:"25/64",
    check_count:Object.keys(checks).length,
    checks,
    new_E2:0,new_E3:0,external_replication:0
  };
}
if (typeof require!=="undefined" && typeof module!=="undefined" && require.main===module)
  console.log(JSON.stringify(main(),null,2));
