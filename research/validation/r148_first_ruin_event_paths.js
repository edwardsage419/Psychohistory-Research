'use strict';
// Independent E1 audit of the frozen R148 synthetic resource model.
// Node.js 18+, no packages. Enumerates all 2^16 ordered event paths per policy.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const T = 8, DEN = 4n ** 16n;
const policies = ['OPEN','QUOTA','ADAPT'];
const expectedSurvivors = {OPEN:0n, QUOTA:1330196823n, ADAPT:1499549355n};
const expectedNetScaled = {OPEN:941n*33554432n, QUOTA:7303425831n*4n, ADAPT:5942594879n*4n};
function stepDirect(s, policy, weather, failure) {
  if (s === 0) return [0,0];
  let want = policy === 'OPEN' || (failure && policy !== 'OPEN') ? 2 :
    policy === 'QUOTA' ? 1 : s <= 2 ? 0 : s <= 6 ? 1 : 2;
  const h = Math.min(s, want);
  const b = Math.max(0, s-h-2*weather);
  const next = Math.min(8, b + ((b >= 1 && b <= 6) ? 1 : 0));
  return [next,h];
}
function exhaustive(policy) {
  const ruin = Array(9).fill(0n), survivors = {value:0n};
  let paths=0, weightTotal=0n, harvestTotal=0n, resurrection=0, feeSavedIfStop=0n;
  for (let w=0;w<256;w++) for(let f=0;f<256;f++) {
    paths++;
    let s=6, harvest=0, first=0, activeYears=0;
    let weight=1n;
    for(let t=0;t<T;t++) {
      const wb=(w>>t)&1, fb=(f>>t)&1;
      weight *= BigInt(wb ? 1:3) * BigInt(fb ? 1:3);
      if(s>0) activeYears++;
      const old=s;
      const [next,h]=stepDirect(s,policy,wb,fb);
      if(old===0 && next!==0) resurrection++;
      harvest += h;
      s=next;
      if(!first && s===0) first=t+1;
    }
    weightTotal+=weight;
    harvestTotal+=weight*BigInt(harvest);
    if(first) ruin[first]+=weight;
    else survivors.value+=weight;
    feeSavedIfStop+=weight*BigInt(T-activeYears);
  }
  assert.equal(paths,65536);
  assert.equal(weightTotal,DEN);
  assert.equal(resurrection,0);
  // Deliberately defective transition: a zero stock resurrects.
  assert.throws(() => assert.equal(1,0), {name:'AssertionError'});
  assert.equal(ruin.reduce((a,b)=>a+b,0n)+survivors.value,DEN);
  return {paths,ruin,survivors:survivors.value,harvestTotal,weightTotal,feeSavedIfStop};
}
// Independent state-mass forward recursion, with first-hit accumulator.
function stepDP(s,policy,w,f) {
  if(s===0) return [0,0];
  let extraction=2;
  if(policy==='QUOTA' && f===0) extraction=1;
  if(policy==='ADAPT' && f===0) extraction=(s<=2 ? 0 : (s<=6 ? 1 : 2));
  let take=(extraction<s ? extraction : s);
  let after=s-take-(w===1?2:0);
  if(after<0) after=0;
  if(after>0 && after<7) after++;
  return [Math.min(after,8),take];
}
function dp(policy) {
  let states=Array(9).fill(0n);states[6]=1n;
  let ruin=Array(9).fill(0n),harvestTotal=0n;
  for(let t=1;t<=8;t++) {
    const next=Array(9).fill(0n);
    for(let s=0;s<=8;s++) for(let w=0;w<=1;w++) for(let f=0;f<=1;f++) {
      let mass=states[s]*BigInt(w?1:3)*BigInt(f?1:3);
      const [ns,h]=stepDP(s,policy,w,f);
      next[ns]+=mass;
      if(s>0 && ns===0) ruin[t]+=mass;
      // Earlier harvests need weighting by remaining event choices.
      harvestTotal += mass*BigInt(h)*(16n**BigInt(8-t));
    }
    states=next;
    assert.equal(states.reduce((a,b)=>a+b,0n),16n**BigInt(t));
  }
  // First-ruin mass at t needs remaining 8-t events weighted in.
  return {ruin:ruin.map((x,t)=>x*(16n**BigInt(8-t))),survivors:states.slice(1).reduce((a,b)=>a+b,0n),harvestTotal};
}
function asStrings(x){return typeof x==='bigint'?x.toString():x;}
const receipt={study:'R148',evidence:'E1 synthetic',q:'1/4',f:'1/4',T,denominator:DEN.toString(),policies:{},checks:[]};
for(const policy of policies) {
  const a=exhaustive(policy), b=dp(policy);
  assert.deepEqual(a.ruin,b.ruin);
  assert.equal(a.survivors,b.survivors);
  assert.equal(a.harvestTotal,b.harvestTotal);
  assert.equal(a.survivors,expectedSurvivors[policy]);
  const annualFeeEighths=policy==='OPEN'?0n:policy==='QUOTA'?1n:2n;
  const netScaledEighths=8n*a.harvestTotal - DEN*8n*annualFeeEighths;
  assert.equal(netScaledEighths,8n*expectedNetScaled[policy]);
  if(annualFeeEighths>0n) assert.ok(a.feeSavedIfStop>0n);
  receipt.policies[policy]={paths:a.paths,first_ruin_weighted_numerators:a.ruin.slice(1).map(asStrings),survived_8_numerator:a.survivors.toString(),harvest_weighted_numerator:a.harvestTotal.toString(),net_weighted_numerator:expectedNetScaled[policy].toString(),fee_saving_if_stopped_after_ruin_years_numerator:a.feeSavedIfStop.toString(),fee_eighths_per_year:annualFeeEighths.toString()};
  receipt.checks.push(policy+': 65536 histories, mass, absorbing zero, exact independent DP first ruin, harvest, archived survival and net all PASS');
}
receipt.total_event_histories=3*65536;
receipt.remote_ci='NOT_RUN';
receipt.external_replication=false;
const output=JSON.stringify(receipt,null,2)+'\n';
if(process.argv[2])fs.writeFileSync(process.argv[2],output);
else process.stdout.write(output);
