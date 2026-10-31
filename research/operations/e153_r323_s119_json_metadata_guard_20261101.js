"use strict";
// Independent strict metadata/summary gate for archived R323 S119 JSON.
// Nonblind E1. Does not replace the B-track 256-row CSV oracle.
const POL=["vbn_cascade","direct_product","unconstrained_norm","value_feasible"];
const SRC="1b92efb314aae036e773be92e28793f8fcd60809";
function act(w,V,T,R,E,C,n){return [n*C,V*T*R*E*C,n,V*C][w];}
function frac(a,b){function gcd(x,y){while(y){const t=x%y;x=y;y=t;}return x;}const g=gcd(a,b);return b/g===1?String(a/g):a/g+"/"+b/g;}
function exact(x,keys){return JSON.stringify(Object.keys(x))===JSON.stringify(keys);}
function validate(x) {
  const ok=(v,m)=>{if(!v)throw Error(m);};
  ok(exact(x,["schema","source_blob","evidence","rows","worlds","pairwise_action_disagreements","cascade_vs_direct","real_human_E2","historical_E3","external_independent_replication"]),"top-level shape");
  ok(x.schema==="r323_s119_structural_do_norm_e1_v1"&&x.source_blob===SRC&&x.evidence==="E1_ARTIFICIAL_ONLY"&&x.rows===256,"source/evidence");
  ok(x.real_human_E2==="NOT_ESTABLISHED"&&x.historical_E3==="NOT_ESTABLISHED"&&x.external_independent_replication==="NOT_RUN","claim boundary");
  ok(Array.isArray(x.worlds)&&x.worlds.length===4,"world coverage");
  const states=[];for(let v=0;v<2;v++)for(let t=0;t<2;t++)for(let r=0;r<2;r++)for(let e=0;e<2;e++)for(let c=0;c<2;c++)states.push([v,t,r,e,c]);
  for(let w=0;w<4;w++){
    const item=x.worlds[w], c0=states.reduce((n,s)=>n+act(w,...s,0),0),c1=states.reduce((n,s)=>n+act(w,...s,1),0);
    ok(exact(item,["world_id","policy","rows","do0_action_positive","do1_action_positive","average_intervention_effect"]),"world shape");
    ok(item.world_id===w&&item.policy===POL[w]&&item.rows===64&&item.do0_action_positive===c0&&item.do1_action_positive===c1&&item.average_intervention_effect===frac(c1-c0,32),"world values");
  }
  const pairs={};
  for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)pairs[POL[a]+"|"+POL[b]]=states.reduce((n,s)=>n+Number(act(a,...s,0)!==act(b,...s,0))+Number(act(a,...s,1)!==act(b,...s,1)),0);
  ok(JSON.stringify(x.pairwise_action_disagreements)===JSON.stringify(pairs),"pairs");
  const d0=states.reduce((n,s)=>n+Number(act(0,...s,0)!==act(1,...s,0)),0),d1=states.reduce((n,s)=>n+Number(act(0,...s,1)!==act(1,...s,1)),0);
  const summary={observational_disagreements:0,do0_disagreements:d0,do1_disagreements:d1,total_disagreements:d0+d1,tv:frac(d0+d1,64),equal_prior_accuracy:frac(64+d0+d1,128),do0_tv:frac(d0,32),do1_tv:frac(d1,32),do0_accuracy:frac(32+d0,64),do1_accuracy:frac(32+d1,64)};
  ok(JSON.stringify(x.cascade_vs_direct)===JSON.stringify(summary),"summary");
  return {worlds:4,rows:256,pairs:6,summary};
}
function testMutations(original){
  const cases=[
    x=>{x.source_blob="wrong";},x=>{x.evidence="E2";},x=>{x.rows=255;},
    x=>{x.worlds.pop();},x=>{[x.worlds[0],x.worlds[1]]=[x.worlds[1],x.worlds[0]];},
    x=>{x.worlds[0].do1_action_positive++;},x=>{delete x.pairwise_action_disagreements["vbn_cascade|direct_product"];},
    x=>{x.cascade_vs_direct.tv="0";},x=>{x.historical_E3="ESTABLISHED";},
    x=>{x.external_independent_replication="COMPLETE";}
  ];
  validate(original);
  let rejected=0;for(const mutate of cases){const x=JSON.parse(JSON.stringify(original));mutate(x);try{validate(x);}catch(e){rejected++;}}
  if(rejected!==cases.length)throw Error("mutation false acceptance "+(cases.length-rejected));
  return {baseline:"PASS",mutations_rejected:rejected,mutations_total:cases.length};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
  const fs=require("fs");const input=process.argv[2];if(!input)throw Error("usage: node e153...js <R323_S119_EXACT_RESULTS.json>");
  console.log(JSON.stringify(testMutations(JSON.parse(fs.readFileSync(input,"utf8"))),null,2));
}
