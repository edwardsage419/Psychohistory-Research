"use strict";
// MKT116: synthetic pairwise preference, abstention, conflicting votes, withdrawal.
// Run: node research/market/mkt116_pairwise_abstention_synthetic_20261029.js
function runMkt116() {
  let checks=0;
  function ok(x,msg){checks++;if(!x)throw new Error("CHECK_"+checks+": "+msg);}
  function close(a,b,t=1e-12){return Math.abs(a-b)<t;}
  const choices={A:{cost:0,delay:8},B:{cost:40,delay:4},C:{cost:100,delay:0}};
  const hypotheses=[0.2,0.5,0.8],names=Object.keys(choices);
  function utility(name,w){const x=choices[name];return -(w*x.cost/100+(1-w)*x.delay/8);}
  function logistic(x){return 1/(1+Math.exp(-x));}
  function prob(pref,other,w){return logistic(12*(utility(pref,w)-utility(other,w)));}
  function posterior(events){
    const active=events.filter(e=>e.kind==="VOTE"&&!events.some(r=>r.kind==="RETRACT"&&r.target===e.id));
    const logp=hypotheses.map(w=>active.reduce((s,e)=>s+Math.log(prob(e.winner,e.loser,w)),Math.log(1/3)));
    const shift=Math.max(...logp),ex=logp.map(x=>Math.exp(x-shift)),z=ex.reduce((a,b)=>a+b,0);
    return ex.map(x=>x/z);
  }
  function entropy(p){return -p.reduce((s,x)=>s+(x>0?x*Math.log2(x):0),0);}
  function infoGain(pair,p){
    const [a,b]=pair,like=hypotheses.map(w=>prob(a,b,w));
    const pA=like.reduce((s,x,i)=>s+x*p[i],0);
    const postA=p.map((x,i)=>x*like[i]/pA);
    const postB=p.map((x,i)=>x*(1-like[i])/(1-pA));
    return entropy(p)-pA*entropy(postA)-(1-pA)*entropy(postB);
  }
  const prior=posterior([]),H0=entropy(prior);
  ok(close(prior.reduce((a,b)=>a+b,0),1),"prior mass");
  ok(prior.every(x=>close(x,1/3)),"prior uniform");
  ok(names.length===3,"three candidates");
  for(const w of hypotheses){
    ok(names.every(n=>Number.isFinite(utility(n,w))),"finite utility");
    for(const a of names)for(const b of names)ok(close(prob(a,b,w)+prob(b,a,w),1),"symmetry");
  }
  const pairs=[["A","B"],["A","C"],["B","C"]];
  const ig=pairs.map(pair=>({pair:pair.join(":"),bits:infoGain(pair,prior)}));
  ok(ig.every(x=>x.bits>=-1e-12&&x.bits<=H0),"bounded information");
  const best=ig.reduce((a,b)=>b.bits>a.bits?b:a);
  ok(best.bits>0,"positive information");
  const events=[];
  function vote(id,winner,loser){
    ok(!events.some(e=>e.id===id),"unique vote id");
    ok(names.includes(winner)&&names.includes(loser)&&winner!==loser,"valid pair");
    events.push({kind:"VOTE",id,winner,loser});
  }
  function retract(id,target){ok(events.some(e=>e.kind==="VOTE"&&e.id===target),"existing target");events.push({kind:"RETRACT",id,target});}
  const pBefore=posterior(events);
  events.push({kind:"ABSTAIN",id:"a1",pair:"A:C"});
  const pAbstain=posterior(events);
  ok(pAbstain.every((x,i)=>close(x,pBefore[i])),"abstain leaves posterior unchanged");
  vote("v1","C","A");
  const pOne=posterior(events);
  ok(pOne.some((x,i)=>!close(x,prior[i])),"vote changes posterior");
  ok(close(pOne.reduce((a,b)=>a+b,0),1),"updated mass");
  vote("v2","A","C");
  const pContradiction=posterior(events);
  ok(pContradiction[1]>.99,"opposite votes spuriously concentrate neutral hypothesis");
  ok(!pContradiction.every((x,i)=>close(x,prior[i])),"conflicting votes are not missing votes");
  retract("r2","v2");
  const pAfterRetract=posterior(events);
  ok(pAfterRetract.every((x,i)=>close(x,pOne[i])),"retract second vote restores first posterior");
  retract("r1","v1");
  const pAllRetracted=posterior(events);
  ok(pAllRetracted.every((x,i)=>close(x,prior[i])),"all retracted restore prior");
  const preferenceEvents=[{kind:"APPROVE",id:"approval1",candidate:"B"},{kind:"REVOKE",id:"revoke1",target:"approval1"}];
  function activeApproval(history){
    const approvals=history.filter(e=>e.kind==="APPROVE"&&!history.some(r=>r.kind==="REVOKE"&&r.target===e.id));
    return approvals.length?approvals[approvals.length-1].candidate:null;
  }
  ok(activeApproval(preferenceEvents)===null,"revoked approval never auto-restored");
  ok(activeApproval([])===null,"no approval");
  ok(activeApproval([{kind:"APPROVE",id:"ok",candidate:"A"}])==="A","explicit approval");
  return {checks,failures:0,prior_entropy_bits:H0,query_information_bits:ig,best_query:best,
    posterior_after_vote:pOne,posterior_after_opposing_vote:pContradiction,
    posterior_after_retraction:pAfterRetract,posterior_after_all_retracted:pAllRetracted,
    abstain_no_update:true,consent_state:"NO_ACTIVE_PREFERENCE",
    decision:"ABSTAIN_REQUIRES_USER",model:"THREE_HYPOTHESIS_LOGISTIC_TOY_NOT_BOTORCH"};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(runMkt116(),null,2));
