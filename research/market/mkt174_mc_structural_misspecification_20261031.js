"use strict";
/* MKT174: finite synthetic calibration example. No product code or personal data. */
function requireTrue(ok, label) { if (!ok) throw new Error(label); }
function draw(seed, n, joint) {
  let x = seed >>> 0, fail = 0;
  function next() { x ^= x << 13; x ^= x >>> 17; x ^= x << 5; return x >>> 0; }
  for (let i = 0; i < n; i++) {
    const u = next();
    const a = (u >>> 16) & 1;
    const b = joint === "independent" ? ((u >>> 24) & 1) : a;
    if (a === 0 && b === 0) fail++;
  }
  return fail;
}
function main() {
  const independent = [[0,0],[0,1],[1,0],[1,1]];
  const common = [[0,0],[1,1]];
  const probability = (rows) => rows.filter(([a,b]) => a === 0 && b === 0).length / rows.length;
  const marginals = rows => [0,1].map(k => rows.filter(row => row[k] === 0).length / rows.length);
  requireTrue(JSON.stringify(marginals(independent)) === JSON.stringify([.5,.5]), "independent marginals");
  requireTrue(JSON.stringify(marginals(common)) === JSON.stringify([.5,.5]), "common marginals");
  const q = probability(independent), p = probability(common);
  requireTrue(q === .25 && p === .5, "exact probabilities");
  const brierWrong = p * (1-q)**2 + (1-p)*q**2;
  const brierOracle = p*(1-p)**2+(1-p)*p**2;
  requireTrue(brierWrong === 5/16 && brierOracle === 1/4, "expected Brier");
  const trials = [20,200,2000,20000].map(n => ({n, model_fail:draw(174,n,"independent"), truth_fail:draw(174,n,"common")}));
  const ciHalfWidth = 1.96*Math.sqrt(q*(1-q)/2000);
  requireTrue(q+ciHalfWidth < p, "MC interval vs structural misspecification");
  requireTrue(Math.abs(trials[3].model_fail/20000-q) < .025, "sample sanity");
  return {worlds_independent:4,worlds_common:2,marginal_down_probability:.5,assumed_joint_failure:q,true_joint_failure:p,structural_gap:p-q,expected_brier_wrong:brierWrong,expected_brier_oracle:brierOracle,brier_excess:brierWrong-brierOracle,conditional_model_95pct_interval_n2000:[q-ciHalfWidth,q+ciHalfWidth],trials};
}
if (typeof module !== "undefined" && require.main === module) console.log(JSON.stringify(main(),null,2));
