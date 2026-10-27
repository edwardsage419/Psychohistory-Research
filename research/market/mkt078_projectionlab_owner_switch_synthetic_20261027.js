'use strict';
// Synthetic ProjectionLab documentation contract, not vendor execution.
// Node.js 18+; no external packages or personal financial data.
function run() {
  let checks = 0;
  function ok(condition, name) { checks++; if (!condition) throw Error(name); }
  const accounts = [
    {id:'self', owner:'self', balance:80000},
    {id:'partner', owner:'partner', balance:50000},
    {id:'joint', owner:'joint', balance:100000}
  ];
  const incomes = [
    {id:'salary', owner:'partner', annual:60000},
    {id:'social_security', owner:'partner', annual:24000},
    {id:'self_income', owner:'self', annual:30000}
  ];
  const costs = [{id:'partner_medicare', owner:'partner', annual:6000}];
  const original = JSON.stringify({accounts,incomes,costs});
  const sum = xs => xs.reduce((s,x)=>s+(x.balance||0),0);
  const sumIncome = xs => xs.reduce((s,x)=>s+x.annual,0);
  ok(sum(accounts)===230000,'starting net worth');
  ok(sumIncome(incomes)===114000,'starting income');
  ok(costs.length===1,'partner Medicare present');
  const planningMode = 'individual';
  const afterAccounts = accounts.map(a => ({
    ...a, owner: (a.owner==='partner'||a.owner==='joint') ? null : a.owner
  }));
  const afterIncomes = incomes.map(i=>({...i}));
  const afterCosts = costs.filter(c=>c.id!=='partner_medicare');
  ok(planningMode==='individual','mode changed');
  ok(afterAccounts.length===3,'accounts retained');
  ok(sum(afterAccounts)===230000,'net worth unchanged');
  ok(afterAccounts.find(a=>a.id==='self').owner==='self','self owner retained');
  ok(afterAccounts.find(a=>a.id==='partner').owner===null,'partner owner cleared');
  ok(afterAccounts.find(a=>a.id==='joint').owner===null,'joint owner cleared');
  ok(afterAccounts.find(a=>a.id==='partner').balance===50000,'partner balance retained');
  ok(afterAccounts.find(a=>a.id==='joint').balance===100000,'joint balance retained');
  ok(afterIncomes.length===3,'income streams retained');
  ok(sumIncome(afterIncomes)===114000,'income unchanged');
  ok(afterIncomes.find(i=>i.id==='salary').annual===60000,'partner salary retained');
  ok(afterIncomes.find(i=>i.id==='social_security').annual===24000,'partner benefit retained');
  ok(afterCosts.length===0,'partner Medicare removed');
  const intendedSelfAssets=sum(afterAccounts.filter(a=>a.owner==='self'));
  const retainedUnattributed=sum(afterAccounts.filter(a=>a.owner===null));
  ok(intendedSelfAssets===80000,'self assets');
  ok(retainedUnattributed===150000,'unattributed assets');
  ok(sum(afterAccounts)-intendedSelfAssets===150000,'asset overcount example');
  const retainedPartnerIncome=sumIncome(afterIncomes.filter(i=>i.owner==='partner'));
  ok(retainedPartnerIncome===84000,'partner income still present');
  ok(sumIncome(afterIncomes)-retainedPartnerIncome===30000,'self income');
  const standardPlan={kind:'standard',startBalance:sum(afterAccounts)};
  const customPlan={kind:'custom',startBalance:170000};
  ok(standardPlan.startBalance===230000,'standard inherits current');
  ok(customPlan.startBalance===170000,'custom independent start');
  const withoutJoint=afterAccounts.filter(a=>a.id!=='joint');
  ok(sum(withoutJoint)===130000,'delete current account');
  ok(sum(withoutJoint)!==standardPlan.startBalance,'standard plan changes on delete');
  ok(customPlan.startBalance===170000,'custom plan does not sync');
  const unresolved=afterAccounts.filter(a=>a.owner===null).map(a=>a.id);
  ok(unresolved.length===2,'two accounts require review');
  ok(unresolved.includes('partner'),'partner review');
  ok(unresolved.includes('joint'),'joint review');
  const unresolvedIncomes=afterIncomes.filter(i=>i.owner==='partner').map(i=>i.id);
  ok(unresolvedIncomes.length===2,'two income streams require review');
  ok(unresolvedIncomes.includes('salary'),'salary review');
  ok(unresolvedIncomes.includes('social_security'),'benefit review');
  ok(JSON.stringify({accounts,incomes,costs})===original,'source records unchanged');
  return {checks,failures:0,account_total_after_switch:sum(afterAccounts),
    self_only_assets:intendedSelfAssets,unattributed_assets:retainedUnattributed,
    partner_income_still_present:retainedPartnerIncome,custom_start:customPlan.startBalance};
}
if (typeof module!=='undefined') module.exports={run};
if (typeof require!=='undefined' && typeof module!=='undefined' && require.main===module) {
  console.log(JSON.stringify(run(),null,2));
}
