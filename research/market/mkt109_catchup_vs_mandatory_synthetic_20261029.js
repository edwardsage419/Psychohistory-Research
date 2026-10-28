"use strict";
// Offline arithmetic toy; not a Beeminder or ProjectionLab implementation.
function run(){
 let n=0;const ok=(x,m)=>{n++;if(!x)throw Error(m)};
 const g={total:70,days:14,elapsed:4,completed:20,breakDays:3};
 const baseline=g.total/g.days,active=g.days-g.elapsed-g.breakDays,remaining=g.total-g.completed;
 const catchup=remaining/active,keepRateTotal=g.completed+active*baseline,maxDaily=6;
 ok(baseline===5,"baseline");ok(active===7,"active");ok(remaining===50,"remaining");
 ok(catchup===50/7,"catchup");ok(catchup>baseline,"steeper");
 ok(keepRateTotal===55,"fixed rate");ok(keepRateTotal<g.total,"target shortfall");
 ok(g.completed+active*maxDaily===62,"capacity");ok(g.completed+active*maxDaily<g.total,"infeasible");
 const money={mandatory:300,incomeSurplus:200,otherAssets:500};
 const gap=Math.max(0,money.mandatory-money.incomeSurplus),draw=Math.min(gap,money.otherAssets);
 ok(gap===100,"gap");ok(draw===100,"draw");ok(money.incomeSurplus+draw===money.mandatory,"funded");
 ok(money.otherAssets-draw===400,"assets");
 const constrained=Math.min(50,gap);
 ok(constrained===50,"cap");ok(money.incomeSurplus+constrained===250,"partial");
 ok(money.incomeSurplus+constrained<money.mandatory,"unfunded");
 const options=[{name:"keep_target",daily:catchup,endTotal:70},{name:"keep_rate",daily:baseline,endTotal:55},{name:"cap_effort",daily:maxDaily,endTotal:62}];
 ok(options.length===3,"options");ok(options[0].daily>options[1].daily,"tradeoff");
 return {study:"MKT109",evidence:"E1_SYNTHETIC",assertions:n,failures:0,baseline_rate:baseline,post_break_catchup_rate:catchup,keep_rate_end_total:keepRateTotal,capacity_limited_end_total:62,mandatory_draw:draw,asset_limited_unfunded:50,options};
}
if(typeof module!=="undefined"){module.exports={run};if(require.main===module)console.log(JSON.stringify(run(),null,2));}