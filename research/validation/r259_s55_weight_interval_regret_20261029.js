"use strict";
const SOURCE_BLOB="58ff66fab67a65fb0bd0f53ec141f77735d46a3d";
const FREEZE_COMMIT="b11c8185a107decbc4c9a2d5c805215ddf71e99b";
const LABELS=["A","B","C","D","E"], GRID=["0","1/4","1/2","3/4","1"];
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n;}
function q(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);return [n/g,d/g];}
function f(s){let z=String(s).split("/");if(z.length>2)throw Error("invalid rational");return q(BigInt(z[0]),z[1]===undefined?1n:BigInt(z[1]));}
function add(a,b){return q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function neg(a){return [-a[0],a[1]];}
function sub(a,b){return add(a,neg(b));}
function mul(a,b){return q(a[0]*b[0],a[1]*b[1]);}
function div(a,b){return q(a[0]*b[1],a[1]*b[0]);}
function cmp(a,b){let z=a[0]*b[1]-b[0]*a[1];return z<0n?-1:z>0n?1:0;}
function lo(a,b){return cmp(a,b)<=0?a:b;}
function hi(a,b){return cmp(a,b)>=0?a:b;}
function s(a){return a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);}
const ZERO=f("0"), ONE=f("1");
function weighted(cost,lambda){return add(mul(lambda,cost[0]),mul(sub(ONE,lambda),cost[1]));}
function validate(csv){
  const lines=csv.trimEnd().split(/\r?\n/);
  const header="world,original_decision_label,original_scalar_weight_lambda,original_objective_f1,original_objective_f2,original_weighted_objective_score,original_decision_is_Pareto,original_decision_supported_any_continuous_weight,original_decision_wins_this_weight,original_uniform_decision_weight_design_mass";
  if(lines[0]!==header)throw Error("CSV header changed");
  const keys=new Set(),worlds=new Map();
  for(const line of lines.slice(1)){
    let c=line.split(",");if(c.length!==10)throw Error("field count");
    let [w,d,lam,ca,cb,score,p,sup,win,mass]=c;
    if(!LABELS.includes(d)||!GRID.includes(lam))throw Error("invalid key");
    let key=[w,d,lam].join("|");if(keys.has(key))throw Error("duplicate key");keys.add(key);
    if(s(f(mass))!=="1/25")throw Error("design mass");
    if(!["0","1"].includes(p)||!["0","1"].includes(sup)||!["0","1"].includes(win))throw Error("binary flags");
    if(!worlds.has(w))worlds.set(w,{cost:{},rows:[]});
    let o=worlds.get(w),v=[f(ca),f(cb)];
    if(o.cost[d]&&(cmp(o.cost[d][0],v[0])!==0||cmp(o.cost[d][1],v[1])!==0))throw Error("cost changed across weights");
    o.cost[d]=v;o.rows.push({d,lam,score,p,sup,win});
    if(cmp(weighted(v,f(lam)),f(score))!==0)throw Error("weighted score mismatch");
  }
  if(keys.size!==225||worlds.size!==9)throw Error("source coverage");
  for(const [w,o] of worlds){
    if(o.rows.length!==25||LABELS.some(d=>!o.cost[d]))throw Error("world coverage");
    const pareto={},supported={};
    for(const d of LABELS){
      let [a,b]=o.cost[d];
      pareto[d]=!LABELS.some(e=>e!==d&&cmp(o.cost[e][0],a)<=0&&cmp(o.cost[e][1],b)<=0&&(cmp(o.cost[e][0],a)<0||cmp(o.cost[e][1],b)<0));
      let low=ZERO,high=ONE,possible=true;
      for(const e of LABELS){
        if(e===d)continue;
        let [c,dd]=o.cost[e],slope=sub(sub(a,c),sub(b,dd)),intercept=sub(b,dd);
        if(cmp(slope,ZERO)===0){if(cmp(intercept,ZERO)>0){possible=false;break;}}
        else {let cut=div(neg(intercept),slope);if(cmp(slope,ZERO)>0)high=lo(high,cut);else low=hi(low,cut);}
        if(cmp(low,high)>0){possible=false;break;}
      }
      supported[d]=possible;
    }
    for(const r of o.rows){
      let values=LABELS.map(d=>weighted(o.cost[d],f(r.lam)));
      let best=values.reduce(lo);
      let winner=cmp(weighted(o.cost[r.d],f(r.lam)),best)===0;
      if(Number(pareto[r.d])!==Number(r.p)||Number(supported[r.d])!==Number(r.sup)||Number(winner)!==Number(r.win))throw Error("frozen flags mismatch "+w+" "+r.d);
    }
    o.pareto=pareto;o.supported=supported;
  }
  return worlds;
}
function analyze(csv){
  const worlds=validate(csv), intervals=[["FULL","0","1"],["CENTRAL","1/4","3/4"]],out=[];
  let unsupportedWins=0,comparisons=0;
  for(const [w,o] of worlds){
    const nominal=LABELS.map(d=>weighted(o.cost[d],f("1/2"))),nomMin=nominal.reduce(lo);
    const nominalWinners=LABELS.filter((d,i)=>cmp(nominal[i],nomMin)===0);
    const groups=[];
    for(const [id,low,high] of intervals){
      const endpoints=[f(low),f(high)],byAction={};
      for(const d of LABELS){
        const losses=endpoints.map(l=>weighted(o.cost[d],l));
        const regrets=endpoints.map((l,i)=>sub(losses[i],LABELS.map(e=>weighted(o.cost[e],l)).reduce(lo)));
        byAction[d]={worst_regret:s(regrets.reduce(hi)),worst_weighted_loss:s(losses.reduce(hi)),regret_at_endpoints:regrets.map(s)};
        comparisons+=4;
      }
      const bestR=LABELS.map(d=>f(byAction[d].worst_regret)).reduce(lo);
      const bestW=LABELS.map(d=>f(byAction[d].worst_weighted_loss)).reduce(lo);
      const rWinners=LABELS.filter(d=>cmp(f(byAction[d].worst_regret),bestR)===0);
      const wWinners=LABELS.filter(d=>cmp(f(byAction[d].worst_weighted_loss),bestW)===0);
      const unsupported=rWinners.filter(d=>!o.supported[d]&&o.pareto[d]);
      unsupportedWins+=unsupported.length;
      groups.push({interval:id,lambda_bounds:[low,high],minimax_regret_value:s(bestR),minimax_regret_winners:rWinners,minimax_worst_weighted_loss_value:s(bestW),minimax_worst_weighted_loss_winners:wWinners,nominal_half_weight_winners:nominalWinners,unsupported_pareto_minimax_regret_winners:unsupported,all_actions:byAction});
    }
    for(const d of LABELS){
      if(cmp(f(groups[0].all_actions[d].worst_regret),f(groups[1].all_actions[d].worst_regret))<0)throw Error("regret set monotonicity");
      if(cmp(f(groups[0].all_actions[d].worst_weighted_loss),f(groups[1].all_actions[d].worst_weighted_loss))<0)throw Error("cost set monotonicity");
    }
    out.push({world:w,pareto_labels:LABELS.filter(d=>o.pareto[d]),continuously_supported_labels:LABELS.filter(d=>o.supported[d]),intervals:groups});
  }
  return {research_id:"R259_S55",scope:"E1_FINITE_ARTIFICIAL",original_source_blob:SOURCE_BLOB,prescore_freeze_commit:FREEZE_COMMIT,original_rows:225,worlds:9,action_interval_combinations:90,endpoint_score_checks:comparisons,unsupported_pareto_minimax_regret_winner_occurrences:unsupportedWins,new_E2:0,new_E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN",world_results:out};
}
function negativeTests(csv){
  validate(csv);
  let lines=csv.trimEnd().split(/\r?\n/),cases=[];
  let duplicated=lines.concat([lines[1]]).join("\n")+"\n";
  let score=lines.slice(),cells=score[1].split(",");cells[5]="999";score[1]=cells.join(",");
  let cost=lines.slice(),c2=cost[2].split(",");c2[3]="999";cost[2]=c2.join(",");
  for(const [name,bad] of [["duplicate_key",duplicated],["wrong_weighted_score",score.join("\n")+"\n"],["inconsistent_action_cost",cost.join("\n")+"\n"]]){
    let rejected=false;try{validate(bad)}catch(e){rejected=true;}
    if(!rejected)throw Error("negative injection accepted "+name);cases.push(name);
  }
  return cases;
}
if(typeof require!=="undefined"&&require.main===module){
  const fs=require("fs"),path=process.argv[2];
  if(!path)throw Error("usage: node r259_s55_weight_interval_regret_20261029.js original.csv [--test]");
  const csv=fs.readFileSync(path,"utf8");
  if(process.argv.includes("--test"))process.stdout.write(JSON.stringify({negative_tests:negativeTests(csv)},null,2)+"\n");
  else process.stdout.write(JSON.stringify(analyze(csv),null,2)+"\n");
}
