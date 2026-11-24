/* Research prototype, Node.js >=18. Finite deterministic synthetic worlds. */
function experiment(){
 const worlds=Array.from({length:8},(_,i)=>[i&1,(i>>1)&1,(i>>2)&1]);
 const specs=[
  {id:"gate_then_rank",out:([a,b,c])=>!a?"B":b?"A":"B"},
  {id:"conditional_branch",out:([a,b,c])=>(a?b:c)?"A":"B"},
  {id:"two_feasible",out:([a,b,c])=>`${a?"A":""}${b?"B":""}|${a&&b?(c?"A":"B"):a?"A":b?"B":"NONE"}`},
  {id:"redundant_conditions",out:([a,b,c])=>((a&&b)||(a&&!b))?"A":"B"}
 ];
 const bits=m=>worlds.map((_,i)=>i).filter(i=>m&(1<<i));
 const masks=[0,1,2].map(q=>worlds.reduce((m,w,i)=>m|(w[q]?(1<<i):0),0));
 const split=(m,q)=>[m&(~masks[q]&255),m&masks[q]];
 const rows=[];let witness=null;
 for(const spec of specs){
  const labels=worlds.map(spec.out), distinct=m=>new Set(bits(m).map(i=>labels[i])).size;
  const conflicts=m=>{const xs=bits(m);let n=0;for(let i=0;i<xs.length;i++)for(let j=i+1;j<xs.length;j++)if(labels[xs[i]]!==labels[xs[j]])n++;return n};
  const possible=(m,allowed)=>[0,1,2].filter(q=>(allowed&(1<<q))&&split(m,q).every(Boolean));
  const memo=new Map();
  function optimal(m,allowed=7){
   if(!m)return {cost:Infinity,q:null,status:"CONFLICT"};
   if(distinct(m)===1)return {cost:0,q:null,status:"RESOLVED"};
   const key=m+":"+allowed;if(memo.has(key))return memo.get(key);
   let best={cost:Infinity,q:null,status:"UNRESOLVED"};
   for(const q of possible(m,allowed)){
    const cost=1+Math.max(...split(m,q).map(s=>optimal(s,allowed&~(1<<q)).cost));
    if(cost<best.cost)best={cost,q,status:"ASK"};
   }
   memo.set(key,best);return best;
  }
  function policy(m,mode,allowed=7){
   if(!m)return Infinity;
   if(distinct(m)===1)return 0;
   const qs=possible(m,allowed);if(!qs.length)return Infinity;
   if(mode==="greedy")qs.sort((a,b)=>Math.max(...split(m,a).map(conflicts))-Math.max(...split(m,b).map(conflicts))||a-b);
   const q=qs[0];
   return 1+Math.max(...split(m,q).map(s=>policy(s,mode,allowed&~(1<<q))));
  }
  // Independent exhaustive tree enumeration, no memo, retaining all attainable worst depths.
  function allDepths(m,allowed){
   if(distinct(m)===1)return [0];
   let depths=[];
   for(const q of possible(m,allowed)){
    const [x,y]=split(m,q);
    for(const a of allDepths(x,allowed&~(1<<q)))for(const b of allDepths(y,allowed&~(1<<q)))depths.push(1+Math.max(a,b));
   }
   return depths;
  }
  function replay(m,world,mode,allowed=7){
   if(distinct(m)===1)return {n:0,answer:labels[bits(m)[0]]};
   let qs=possible(m,allowed);
   if(mode==="greedy")qs.sort((a,b)=>Math.max(...split(m,a).map(conflicts))-Math.max(...split(m,b).map(conflicts))||a-b);
   const q=mode==="optimal"?optimal(m,allowed).q:qs[0];
   if(q===null||q===undefined)throw Error("no query");
   const child=split(m,q)[worlds[world][q]];
   const z=replay(child,world,mode,allowed&~(1<<q));return {n:z.n+1,answer:z.answer};
  }
  for(let m=1;m<256;m++){
   const opt=optimal(m),fixed=policy(m,"fixed"),greedy=policy(m,"greedy"),oracle=Math.min(...allDepths(m,7));
   if(opt.cost!==oracle||opt.cost>fixed||opt.cost>greedy)throw Error("optimality");
   let paths=0;
   for(const i of bits(m))for(const mode of ["fixed","greedy","optimal"]){
    const z=replay(m,i,mode);
    if(z.answer!==labels[i]||z.n>(mode==="fixed"?fixed:mode==="greedy"?greedy:opt.cost))throw Error("replay");
    paths++;
   }
   const row={spec:spec.id,mask:m,worlds:bits(m),fixed,greedy,optimal:opt.cost,first:opt.q,paths};
   rows.push(row);
   if(greedy>opt.cost&&!witness)witness={...row,labels:bits(m).map(i=>({world:worlds[i],label:labels[i]}))};
  }
 }
 // Partial user response: declined questions add no evidence. Missing allowed question can make resolution impossible.
 const controls=[];
 const g=(m,allowed)=>{if(!m)return "CONFLICT";const labels=bits(m).map(i=>worlds[i][0]);if(new Set(labels).size===1)return "RESOLVED";return allowed&1?"ASK":"UNRESOLVED"};
 for(const [m,allowed,expected] of [[0,7,"CONFLICT"],[255,7,"ASK"],[255,6,"UNRESOLVED"],[85,6,"RESOLVED"],[170,6,"RESOLVED"],[3,6,"UNRESOLVED"]]){
  const status=g(m,allowed);if(status!==expected)throw Error("control");controls.push({m,allowed,expected,status});
 }
 const total=k=>rows.reduce((s,x)=>s+x[k],0);
 return {summary:{cases:rows.length,paths:total("paths"),fixed_worst_sum:total("fixed"),greedy_worst_sum:total("greedy"),optimal_worst_sum:total("optimal"),improved_vs_fixed:rows.filter(x=>x.optimal<x.fixed).length,improved_vs_greedy:rows.filter(x=>x.optimal<x.greedy).length,zero_questions:rows.filter(x=>!x.optimal).length,controls:controls.length},witness,rows,controls};
}
console.log(JSON.stringify(experiment(),null,2));
