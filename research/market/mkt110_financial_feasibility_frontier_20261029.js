"use strict";
// MKT110 artificial constraint enumeration; node mkt110_financial_feasibility_frontier_20261029.js
function evaluate(){
 const input={surplus:200,liquid:150,reserve:100,goal:300};
 let n=0;function ok(v,s){n++;if(!v)throw Error(s);}
 const options=[];
 for(let x=200;x<=300;x+=10){
  let withdrawal=x-200,balance=150-withdrawal,goalGap=Math.max(0,300-x),reserveGap=Math.max(0,100-balance);
  ok(withdrawal>=0&&withdrawal<=150,"withdrawal");
  ok(x===200+withdrawal,"budget");
  ok(balance===350-x,"balance");
  ok(goalGap===300-x,"goal");
  ok(reserveGap===Math.max(0,x-250),"reserve");
  ok(goalGap>0||reserveGap>0,"infeasible");
  options.push({funded:x,withdrawal,balance,goalGap,reserveGap});
 }
 const dom=(a,b)=>a.goalGap<=b.goalGap&&a.reserveGap<=b.reserveGap&&(a.goalGap<b.goalGap||a.reserveGap<b.reserveGap);
 const frontier=options.filter(b=>!options.some(a=>dom(a,b)));
 ok(frontier.length===6,"frontier");
 for(const x of options)ok(frontier.some(f=>f.funded===x.funded)===(x.funded>=250),"membership");
 const at=x=>options.find(o=>o.funded===x);
 ok(at(250).goalGap===50&&at(250).reserveGap===0,"reserve safe");
 ok(at(300).goalGap===0&&at(300).reserveGap===50,"goal complete");
 ok(at(270).goalGap===30&&at(270).reserveGap===20,"tradeoff");
 ok(!options.some(o=>o.goalGap===0&&o.reserveGap===0),"no feasible");
 ok(Math.max(...options.filter(o=>o.reserveGap===0).map(o=>o.funded))===250,"safe maximum");
 ok(options.filter(o=>o.goalGap===0).every(o=>o.reserveGap>0),"goal violation");
 return {study:"MKT110",evidence:"E1_SYNTHETIC",input,options:options.length,
  feasible:0,reserve_safe_max:250,goal_gap_if_reserve_preserved:50,
  frontier,assertions:n,failures:0,actual_projectionlab_engine:"UNKNOWN"};
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(evaluate(),null,2));
