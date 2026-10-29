#!/usr/bin/env node
"use strict";
// E089 source-first integer lattice receipt audit, nonblind internal E1.
function audit(csv, receipt) {
  let checks=0;
  const check=(v,m)=>{checks++;if(!v)throw Error(m);};
  const gcd=(a,b)=>{a=Math.abs(a);b=Math.abs(b);while(b){let t=a%b;a=b;b=t;}return a;};
  const fmt=n=>{let g=gcd(n,16);return 16/g===1?String(n/g):(n/g)+"/"+(16/g);};
  const scale=s=>{let p=s.split("/").map(Number),n=p[0],d=p[1]||1;
    check(Number.isInteger(n)&&Number.isInteger(d)&&d>0&&(4*n)%d===0,"quarter-grid");return 4*n/d;};
  const ws=["0","1/4","1/2","3/4","1"],ls="ABCDE".split("");
  const lines=csv.trimEnd().split(/\r?\n/),head=lines.shift().split(",");
  check(head.length===10&&head[0]==="world"&&head[5]==="original_weighted_objective_score","header");
  check(lines.length===225&&receipt.original_rows===225,"225 rows");
  const worlds=new Map(),seen=new Set();
  for(const line of lines){
    const v=line.split(","),[world,label,w,f1,f2,score,pareto,supported,win,mass]=v;
    check(v.length===10&&ls.includes(label)&&ws.includes(w),"identity");
    const key=[world,label,w].join("|");
    check(!seen.has(key),"duplicate key");seen.add(key);
    const x=scale(f1),y=scale(f2),k=ws.indexOf(w);
    check(fmt(k*x+(4-k)*y)===score,"source score");
    check(mass==="1/25"&&[pareto,supported,win].every(z=>z==="0"||z==="1"),"flags");
    if(!worlds.has(world))worlds.set(world,new Map());
    const acts=worlds.get(world);
    if(!acts.has(label))acts.set(label,{x,y,pareto,supported,weights:new Set()});
    const old=acts.get(label);
    check(old.x===x&&old.y===y&&old.pareto===pareto&&old.supported===supported,"cost identity");
    check(!old.weights.has(w),"weight duplicate");old.weights.add(w);
  }
  check(worlds.size===9&&receipt.world_results.length===9,"world coverage");
  check(receipt.original_source_blob==="58ff66fab67a65fb0bd0f53ec141f77735d46a3d","blob identity");
  check(receipt.prescore_freeze_commit==="b11c8185a107decbc4c9a2d5c805215ddf71e99b","freeze");
  let combos=0,unsupported=0;
  for(const wr of receipt.world_results){
    check(worlds.has(wr.world),"world match");
    const acts=worlds.get(wr.world);
    check(acts.size===5,"five actions");
    for(const label of ls)check(acts.has(label)&&acts.get(label).weights.size===5,"weights");
    check(JSON.stringify(ls.filter(x=>acts.get(x).pareto==="1"))===JSON.stringify(wr.pareto_labels),"pareto");
    check(JSON.stringify(ls.filter(x=>acts.get(x).supported==="1"))===JSON.stringify(wr.continuously_supported_labels),"support");
    check(wr.intervals.length===2,"interval coverage");
    for(const ir of wr.intervals){
      const ks=ir.interval==="FULL"?[0,4]:ir.interval==="CENTRAL"?[1,3]:null;
      check(ks!==null,"interval");
      check(JSON.stringify(ir.lambda_bounds)===JSON.stringify(ks.map(k=>ws[k])),"bounds");
      const scores=ks.map(k=>ls.map(label=>{let x=acts.get(label);return k*x.x+(4-k)*x.y;}));
      const mins=scores.map(s=>Math.min(...s));
      let minR=Infinity,minW=Infinity,rw=[],ww=[];
      for(let i=0;i<5;i++){
        const regret=scores.map((s,j)=>s[i]-mins[j]);
        const r=Math.max(...regret),w=Math.max(...scores.map(s=>s[i]));
        const obj=ir.all_actions[ls[i]];
        check(obj.worst_regret===fmt(r),"receipt regret");
        check(obj.worst_weighted_loss===fmt(w),"receipt loss");
        check(JSON.stringify(obj.regret_at_endpoints)===JSON.stringify(regret.map(fmt)),"endpoints");
        if(r<minR){minR=r;rw=[ls[i]];}else if(r===minR)rw.push(ls[i]);
        if(w<minW){minW=w;ww=[ls[i]];}else if(w===minW)ww.push(ls[i]);
        combos++;
      }
      check(ir.minimax_regret_value===fmt(minR),"minimax regret");
      check(ir.minimax_worst_weighted_loss_value===fmt(minW),"minimax loss");
      check(JSON.stringify(ir.minimax_regret_winners)===JSON.stringify(rw),"regret winners");
      check(JSON.stringify(ir.minimax_worst_weighted_loss_winners)===JSON.stringify(ww),"loss winners");
      const nominal=ls.map(label=>{let x=acts.get(label);return 2*x.x+2*x.y;});
      check(JSON.stringify(ir.nominal_half_weight_winners)===
        JSON.stringify(ls.filter((_,i)=>nominal[i]===Math.min(...nominal))),"nominal");
      const unsupportedWinners=rw.filter(x=>acts.get(x).pareto==="1"&&acts.get(x).supported==="0");
      check(JSON.stringify(ir.unsupported_pareto_minimax_regret_winners)===
        JSON.stringify(unsupportedWinners),"unsupported labels");
      unsupported+=unsupportedWinners.length;
    }
  }
  check(combos===90&&receipt.action_interval_combinations===90,"90 action intervals");
  check(unsupported===4&&receipt.unsupported_pareto_minimax_regret_winner_occurrences===4,"unsupported count");
  check(receipt.scope==="E1_FINITE_ARTIFICIAL"&&receipt.new_E2===0&&receipt.new_E3===0,"evidence grade");
  return {checks,failures:0,source_rows:225,worlds:9,action_intervals:combos,
    unsupported_winner_occurrences:unsupported,evidence:"nonblind_internal_E1"};
}
if(typeof module!=="undefined"&&require.main===module){
  const fs=require("fs");
  if(process.argv.length!==4)throw Error("Usage: node audit.js source.csv receipt.json");
  console.log(JSON.stringify(audit(fs.readFileSync(process.argv[2],"utf8"),
    JSON.parse(fs.readFileSync(process.argv[3],"utf8"))),null,2));
}
