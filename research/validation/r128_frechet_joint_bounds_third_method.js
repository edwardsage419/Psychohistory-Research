#!/usr/bin/env node
"use strict";
/* R128 independent exact finite joint-belief audit. Frozen protocol:
   R128_THIRD_METHOD_FRECHET_JOINT_BOUNDS_PROTOCOL_FREEZE_2026-10-24.md
   Constructed E1 only. No external packages or original R128 helpers. */
function runAudit() {
  const grid = [[0,1],[1,4],[1,2],[3,4],[4,5],[1,1]];
  const cases = [];
  function action(success, atoms) {
    return 4 * success > 3 * atoms ? "S" :
           4 * success < 3 * atoms ? "H" : "TIE";
  }
  function compute(n, num, D) {
    const k = n - 1, F = D - num;
    const lower = Array.from({length:k}, (_,j) => {
      const fail = new Set();
      for (let t=0;t<F;t++) fail.add((j*F+t)%D);
      return Array.from({length:D}, (_,a) => !fail.has(a));
    });
    const upper = Array.from({length:k}, () =>
      Array.from({length:D}, (_,a) => a<num));
    const countAll = x => Array.from({length:D}, (_,a) =>
      x.every(v => v[a])).filter(Boolean).length;
    const marginals = x => x.map(v => v.filter(Boolean).length);
    const L = Math.max(0, D-k*F), U = num;
    const actualL = countAll(lower), actualU = countAll(upper);
    const lm = marginals(lower), um = marginals(upper);
    if (actualL!==L || actualU!==U ||
        lm.some(v=>v!==num) || um.some(v=>v!==num))
      throw new Error("FRECHET_CONSTRUCTION_MISMATCH");
    const iidNum = num**k, iidDen = D**k;
    if (iidNum*D<L*iidDen || iidNum*D>U*iidDen)
      throw new Error("IID_OUTSIDE_SHARP_BOUNDS");
    const lowAction = action(actualL,D), highAction = action(actualU,D);
    const identification = lowAction===highAction ? lowAction : "AMBIGUOUS";
    return {n,k,num,D,L,U,actualL,actualU,lm,um,
            lowAction,highAction,identification,iidNum,iidDen};
  }
  function validate(c) {
    if (c.actualL!==c.L || c.actualU!==c.U ||
        c.lm.some(v=>v!==c.num) || c.um.some(v=>v!==c.num))
      throw new Error("TAMPER_OR_INVARIANT_FAILURE");
  }
  for (let n=2;n<=8;n++)
    for (const [num,D] of grid) {
      const c=compute(n,num,D);
      validate(c);
      cases.push(c);
    }
  if (cases.length!==42) throw new Error("WRONG_CASE_COUNT");
  const pick=(n,num,D)=>cases.find(c=>c.n===n&&c.num===num&&c.D===D);
  const c34=pick(3,4,5), c24=pick(2,4,5), c33=pick(3,3,4);
  if (!(c34.L===3&&c34.U===4&&c34.lowAction==="H"&&c34.highAction==="S" &&
        c24.L===4&&c24.U===4&&c24.identification==="S" &&
        c33.L===2&&c33.U===3&&c33.lowAction==="H"&&c33.highAction==="TIE"))
    throw new Error("FROZEN_DIAGNOSTIC_FAILED");
  let negative=0;
  for (const mutation of [
    c=>({...c,actualU:c.actualU-1}),
    c=>({...c,lm:[c.lm[0]-1,...c.lm.slice(1)]})
  ]) {
    try { validate(mutation(c34)); } catch(e) { negative++; }
  }
  if (negative!==2) throw new Error("TAMPER_NOT_REJECTED");
  const header="n,k,p_num,p_den,atoms,lower_joint_atoms,upper_joint_atoms,lower_action,upper_action,identification,iid_num,iid_den";
  const csv=[header,...cases.map(c=>[
    c.n,c.k,c.num,c.D,c.D,c.L,c.U,c.lowAction,c.highAction,
    c.identification,c.iidNum,c.iidDen].join(","))].join("\n")+"\n";
  const summary={
    research_id:"R128", evidence:"E1_CONSTRUCTED_INTERNAL",
    protocol:"FROZEN_BEFORE_COMPUTATION",cases:cases.length,
    sharp_lower_constructions:cases.length,sharp_upper_constructions:cases.length,
    exact_marginal_checks:cases.reduce((s,c)=>s+2*c.k,0),
    ambiguous:cases.filter(c=>c.identification==="AMBIGUOUS").length,
    identified_S:cases.filter(c=>c.identification==="S").length,
    identified_H:cases.filter(c=>c.identification==="H").length,
    identified_TIE:cases.filter(c=>c.identification==="TIE").length,
    negative_controls:negative,failures:0,
    result:"PASS_BOUNDED_INTERNAL_EXACT_FRECHET_CONSTRUCTION_E1"
  };
  return {csv,summary,cases};
}
if (typeof module!=="undefined") {
  module.exports=runAudit;
  if (require.main===module) {
    const r=runAudit();
    if (process.argv.includes("--csv")) process.stdout.write(r.csv);
    else console.log(JSON.stringify(r.summary,null,2));
  }
}
