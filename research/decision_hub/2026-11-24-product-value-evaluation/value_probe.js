/* Node.js >=18. Synthetic development pilot; not an LLM, product, or user study. */
function experiment(){
 // Narrow artificial purchase decisions, same explicit budget and preferences across strategies.
 // Integer prices, two alternatives; no probability distribution assigned to possible worlds.
 const costs=[[1,1],[1,2],[1,3],[2,2],[2,3],[3,3]];
 const rows=[];
 for(const a of costs)for(const b of costs)for(const limit of [1,2,3])for(const utility of [[1,2],[2,1],[1,1]]){
   const opts=[{id:"A",cost:a,u:utility[0]},{id:"B",cost:b,u:utility[1]}];
   const leaders=xs=>xs.length?xs.filter(x=>x.u===Math.max(...xs.map(o=>o.u))).map(x=>x.id).sort():[];
   const worlds=[];
   for(let x=a[0];x<=a[1];x++)for(let y=b[0];y<=b[1];y++){
     const fs=opts.filter((o,i)=>[x,y][i]<=limit);
     worlds.push({x,y,feasible:fs.map(o=>o.id),leaders:leaders(fs)});
   }
   const oracle={certain:opts.filter(o=>worlds.every(w=>w.feasible.includes(o.id))).map(o=>o.id),possible:opts.filter(o=>worlds.some(w=>w.feasible.includes(o.id))).map(o=>o.id),uniqueStable:new Set(worlds.map(w=>JSON.stringify(w.leaders))).size===1?worlds[0].leaders:null};
   // Baseline 1: score alone. Baseline 2: check midpoint estimate. Baseline 3: robust upper bound and possible competitors.
   const naive=leaders(opts);
   const midpoint=leaders(opts.filter(o=>(o.cost[0]+o.cost[1])/2<=limit));
   const upper=opts.filter(o=>o.cost[1]<=limit), possible=opts.filter(o=>o.cost[0]<=limit);
   const best=leaders(upper);
   const robust=possible.every(o=>upper.includes(o)||best.length&&o.u<Math.max(...upper.map(o=>o.u)))?best:null;
   if(JSON.stringify(robust)!==JSON.stringify(oracle.uniqueStable))throw Error("oracle mismatch");
   function assess(pred){
     if(pred===null)return {status:"ABSTAIN",unsafe:false,correct:oracle.uniqueStable===null,actionable:false,missedStable:oracle.uniqueStable!==null};
     const unsafe=pred.some(id=>!oracle.certain.includes(id));
     const correct=oracle.uniqueStable!==null&&JSON.stringify(pred)===JSON.stringify(oracle.uniqueStable);
     return {status:pred.length?"RECOMMEND":"NO_FEASIBLE",unsafe,correct,actionable:pred.length>0&&correct,missedStable:false};
   }
   rows.push({a,b,limit,utility,oracle,naive:assess(naive),midpoint:assess(midpoint),robust:assess(robust)});
 }
 const stats=Object.fromEntries(["naive","midpoint","robust"].map(k=>[k,{cases:rows.length,unsafe:rows.filter(x=>x[k].unsafe).length,correct:rows.filter(x=>x[k].correct).length,abstain:rows.filter(x=>x[k].status==="ABSTAIN").length,actionable:rows.filter(x=>x[k].actionable).length,false_no_feasible:rows.filter(x=>x[k].status==="NO_FEASIBLE"&&x.oracle.possible.length).length,missed_stable:rows.filter(x=>x[k].missedStable).length}]));
 // Scoring policy tested with deliberately constructed responses, never claimed as model outputs.
 const oracle={required:["budget","period"],allowed:["B"],unknown:["probability"],revision:2,critical:["budget"],numeric:{cost:2900},expectedSet:["B"],requiredEvidence:["user:cost"]};
 const base={fields:["budget","period"],recommend:["B"],invented:[],revision:2,numeric:{cost:2900},answerSet:["B"],evidence:["user:cost"],graphRevision:2,questions:1,mandatoryForms:0};
 function score(o,x){
   const fail=[];
   if(o.critical.some(k=>!x.fields.includes(k)))fail.push("OMITTED_HARD_CONSTRAINT");
   if(x.recommend.some(k=>!o.allowed.includes(k)))fail.push("UNSAFE_RECOMMENDATION");
   if(x.invented.some(k=>o.unknown.includes(k)))fail.push("FABRICATED_EVIDENCE");
   if(x.revision!==o.revision||x.graphRevision!==o.revision)fail.push("STALE_OUTPUT");
   const num=Object.entries(o.numeric).every(([k,v])=>x.numeric[k]===v);
   const covered=o.required.every(k=>x.fields.includes(k));
   const eq=JSON.stringify([...x.answerSet].sort())===JSON.stringify([...o.expectedSet].sort());
   const provenance=o.requiredEvidence.every(k=>x.evidence.includes(k));
   return {critical:fail,pass:fail.length===0&&num&&covered&&eq&&provenance,numeric:num,semantic:covered,conclusion:eq,provenance,questions:x.questions,mandatoryForms:x.mandatoryForms};
 }
 const fixtures=[
 ["good",{},true,[]],
 ["omitted",{fields:["period"]},false,["OMITTED_HARD_CONSTRAINT"]],
 ["unsafe",{recommend:["A"]},false,["UNSAFE_RECOMMENDATION"]],
 ["probability",{invented:["probability"]},false,["FABRICATED_EVIDENCE"]],
 ["old",{revision:1},false,["STALE_OUTPUT"]],
 ["chart_old",{graphRevision:1},false,["STALE_OUTPUT"]],
 ["numeric",{numeric:{cost:3000}},false,[]],
 ["silent_abstain",{recommend:[],answerSet:[]},false,[]],
 ["no_source",{evidence:[]},false,[]],
 ["extra_question",{questions:5},true,[]],
 ["manual_forms",{mandatoryForms:7},true,[]],
 ["combined",{fields:[],recommend:["A"],revision:1,invented:["probability"]},false,["OMITTED_HARD_CONSTRAINT","UNSAFE_RECOMMENDATION","FABRICATED_EVIDENCE","STALE_OUTPUT"]]
 ].map(([id,change,pass,critical])=>{const actual=score(oracle,{...base,...change});if(actual.pass!==pass||JSON.stringify(actual.critical)!==JSON.stringify(critical))throw Error(id);return {id,pass,critical,actual}});
 // Exact paired sign test power planning, conditional on discordant pairs, no claims of efficacy.
 const binom=(n,k)=>{let a=1;for(let i=1;i<=k;i++)a*=((n-i+1)/i);return a};
 const tail=(n,k,p)=>{let s=0;for(let i=k;i<=n;i++)s+=binom(n,i)*p**i*(1-p)**(n-i);return s};
 const planning=[10,20,30,40,60,80].map(n=>{let k=0;while(k<=n&&Math.min(1,2*tail(n,k,.5))>.05)k++;return {discordant:n,minimumWins:k<=n?k:null,twoSidedP:k<=n?2*tail(n,k,.5):null,powerIfWinProbabilityPoint75:k<=n?tail(n,k,.75)+tail(n,n-k,.25):0}});
 return {summary:{syntheticCases:rows.length,worlds:rows.reduce((s,x)=>s+(x.a[1]-x.a[0]+1)*(x.b[1]-x.b[0]+1),0),stable:rows.filter(x=>x.oracle.uniqueStable!==null).length,stats,scoringControls:fixtures.length},rows,fixtures,planning};
}
console.log(JSON.stringify(experiment(),null,2));
