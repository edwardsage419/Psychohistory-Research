# 长期个人决策：精确多候选终止证书与自适应计算顺序
2026-11-26。RESEARCH_CANDIDATE / PREDECESSOR_CODE_EXECUTED / SYNTHETIC_EXECUTED / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线
同一手动轮第四阶段，起点main d774c52aa15a96c7b4f26c9725de66c890889ec0；沿用本轮已核对v3.2、同步规程、25近期提交、15开放PR、固定交接及#63固定head 734686980b19da9291bdd08b67d4e2519c011acf。上阶段部分可行与偏好联合出口blob a1414d2385bb2c756b1a0f5cb311919551d5fb25，已有任时计算、决策出口证书与预算研究，本轮新增非唯一最优集合的精确上下界一致终止，以及独立可行性补全合同下求最坏查询次数最小的顺序。不是一般动态规划、任时算法发明或全库去重。
固定输入并实际调用已审阅自有源码：
research/decision_hub/2026-11-26-time-varying-task-cost-liquidity-dp.md 56f16ddab494b41aa07852045653fbdf20f28341
research/decision_hub/2026-11-26-observed-balance-policy-partition-and-replanning.md b5be4353d489e8b9ab09a39ac9e11f2929c2bd5a
research/decision_hub/2026-11-26-partial-lexicographic-goal-order-witnesses.md 56ccc94a47a135670b670e26e65c99503740e7e5
## 合同与证明
三个有效软目标，8二元组合（上一阶段6目标接口其余位为常零），全集覆盖及明确词典序偏好由可信宿主给定；所有硬义务已在前置过滤保留。已证可行集合F、已证不可行I、未确定R，任一补全B满足F⊆B⊆F∪R；不假设目标单调或未确定项独立概率。W(B)是所有允许优先顺序的词典序胜者集合，空B对应空集合。上界U为所有补全W的并集，沿上阶段对t在F∪{t}可胜判定。下界L是所有补全W的交集，精确等于F∩W(F∪R)：任何属于所有补全的胜者必须在最小补全可用，且在最大补全可胜；反过来，最大补全中使已知可行t获胜的排序在删去其他竞争者后仍获胜，所以t属于每个补全的可能胜者集合。注意L的各成员只分别在某个允许偏好下可胜，不表示所有偏好均获胜。若L=U，则完整的可能胜者集合已确定；可含多个候选、单一或空，不需为了唯一答案继续计算。未分类项t∉U表示每条允许排序均有已知可行竞争者严格优先于t（因为在F∪{t}不可胜）。无论其可行性如何，该项不能改变任何补全的胜者集合，因此可省略单独查询，仍不能把它标为不可行。L≠U时至少一个未分类项属于U，否则已知F决定整个集合。
对状态(F,I)计算D=0若L=U；否则D=1+min_{t∈R∩U}max(D(F∪{t},I),D(F,I∪{t}))。有限查询成本各1、只需确定W、无概率、无实际偏好询问、无并行或各次实际CPU成本差异。忽略无关查询不会改变任务输出或帮助减少最坏次数，因它的两个结果对任何其他未知补全相同。该递推最小化抽象合同中最坏额外可行性求解次数，不保证每个真实情景最少调用或更快；状态空间最坏3^|U|，不得在开放大域无预算使用。若真实补全存在关联，仍是保守证书，最坏次数不声称现实最优；所有输出只读authority NONE，覆盖未核对、词典序未确认、真实身份/证据/授权/方法版本须由宿主阻断。
## 实际执行
80个随机三态分区，在一个固定优先偏序中，将上下界与独立枚举每个可行性补全和拓扑优先顺序核对；最坏查询递推与允许查询所有未分类项的独立递推核对。700个实际研究规划函数驱动的合成图，全部8组合预先实际调用原P.solve及独立P.oracle，作为真值表；然后用不同查询顺序逐项揭示同一表结果，比较自适应最坏策略、优先目标数较多的候选、按编号选择候选，三者均使用相同上下界停止合同及无关项过滤。提前结束计数是模拟减少的未来规划调用，实验为对照已运行全部组合，未实测节省设备时间。5控制，包含多个已证可行且剩余未计算被支配的精确歧义集合。标准JS核心实际执行两次一致，非独立验收、真人、现实产品准确率或计算性能。
```json
{
  "graphs": 700,
  "actualBundleChecks": 5600,
  "exactStops": 291,
  "ambiguousEarlyStops": 65,
  "policyCalls": {
    "adaptive": 4990,
    "descending": 3349,
    "ascending": 4990,
    "full": 5600
  },
  "maxCalls": {
    "adaptive": 8,
    "descending": 8,
    "ascending": 8
  },
  "fullTruth": {
    "unique": 423,
    "ambiguous": 146,
    "empty": 131
  },
  "partialReferenceChecks": 80,
  "optimalPolicyChecks": 80,
  "abstractWorstCase": {
    "[]": 8,
    "[[0,2],[1,2]]": 8,
    "[[0,2]]": 8,
    "[[0,1]]": 8,
    "[[1,2]]": 8,
    "[[0,1],[1,2]]": 8,
    "[[0,1],[0,2]]": 8,
    "[[0,1],[0,2],[1,2]]": 8
  },
  "zeroCandidateSkipChecks": 610,
  "controls": 5,
  "example": {
    "feasible": [
      0,
      1,
      2,
      3,
      4,
      5,
      6
    ],
    "edges": [
      [
        0,
        1
      ]
    ],
    "winners": [
      3,
      5
    ],
    "calls": 6,
    "unqueried": [
      2,
      6
    ]
  }
}
```
## 接入边界
当前候选模块提供PossibleWinnerLower/Upper及已证明完整集合状态。已知候选集合有多个时保留真实偏好取舍，不迫使用户回答无意义问题；如果覆盖、模型假设或证据仍未知，不能凭本研究完成标志发布正式结论。预算分配可先比较仍影响候选的任务，复杂域需启发式和实际性能验收，持久执行权及版本更新另由原生事务负责。研究者选择二元目标、等成本查询及有限独立补全，不属于用户确认的正式价值模型。未修改生产、交接、冻结、证据等级、PR、训练、部署、主动CI或费用；原生、独立留出、真机及真人未运行。
## 复算
固定三份报告按上列顺序输入，Node包装未执行，连接器核心已运行。
```js
const code=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8").split("\`\`\`js\n")[1].split("\n\`\`\`")[0]);
const make=Function(code[0].split(" const out={graphs:")[0]+"\nreturn {valid,actions,solve,verify,oracle};\n}\nreturn study();");
const make2=Function("make",code[1].slice(code[1].indexOf("function experiment(make){")).split(" const out={graphs:")[0]+"\nreturn {solve,oracle,unpack};\n}\nreturn experiment(make);");
const make3=Function(code[2].split(" const out={graphs:")[0]+"\nreturn {closure,possible,greedy,enumerate,orderOK,winner};\n}\nreturn experiment();");
function experiment(make,make2,make3){
 const P=make2(make),R=make3(),ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),all=Array.from({length:8},(_,i)=>i),ALL=255;
 let seed=20261206;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 const set=m=>all.filter(i=>m&(1<<i)),mask=a=>a.reduce((m,i)=>m|(1<<i),0),pop=m=>set(m).length;
 function policy(edges){
  const p=R.closure(edges);ck(p!==null,"acyclic");
  const winnerCache=new Map(),boundsCache=new Map(),dpCache=new Map();
  const winners=m=>{
   if(!winnerCache.has(m))winnerCache.set(m,m?mask(R.greedy(set(m),p).possible):0);
   return winnerCache.get(m);
  };
  function bounds(y,n){
   ck(!(y&n),"partition");
   const k=y+256*n;if(boundsCache.has(k))return boundsCache.get(k);
   const u=ALL&~(y|n),pot=y|u;
   let upper=0;
   for(let i of set(pot))if(winners(y|(1<<i))&(1<<i))upper|=1<<i;
   const lower=winners(pot)&y;
   const done=lower===upper;
   const v={lower,upper,done,emptyPossible:y===0,unknown:u,actionable:upper&u};
   boundsCache.set(k,v);return v;
  }
  // Exact worst-case number of extra feasibility queries in the abstract
  // independent-completion contract; no use of probabilities or assumed monotonicity.
  function dp(y,n){
   const k=y+256*n;if(dpCache.has(k))return dpCache.get(k);
   let z=bounds(y,n);
   if(z.done)return {cost:0,next:null};
   let best={cost:Infinity,next:null};
   for(let i of set(z.actionable)){
    let c=1+Math.max(dp(y|(1<<i),n).cost,dp(y,n|(1<<i)).cost);
    if(c<best.cost)best={cost:c,next:i};
   }
   ck(best.next!==null,"unresolved has actionable query");dpCache.set(k,best);return best;
  }
  // Independent exact reference for the query policy over all unclassified
  // bundles (including irrelevant ones). Terminal predicate is computed by
  // complete feasibility-completion enumeration, not candidate bounds.
  const refMemo=new Map(),refBounds=new Map();
  function ref(y,n){
   const k=y+256*n;if(refBounds.has(k))return refBounds.get(k);
   let unknown=set(ALL&~(y|n)),u=0,l=ALL;
   for(let m=0;m<1<<unknown.length;m++){
    let f=y|mask(unknown.filter((_,i)=>m&(1<<i))),w=f?mask(R.enumerate(set(f),p).possible):0;
    u|=w;l&=w;
   }
   const z={lower:l,upper:u};refBounds.set(k,z);return z;
  }
  function dpAll(y,n){
   const k=y+256*n;if(refMemo.has(k))return refMemo.get(k);
   let r=ref(y,n);if(r.lower===r.upper)return 0;
   let best=Infinity;
   for(let i of set(ALL&~(y|n)))best=Math.min(best,1+Math.max(dpAll(y|(1<<i),n),dpAll(y,n|(1<<i))));
   refMemo.set(k,best);return best;
  }
  return {bounds,dp,ref,dpAll,winners,p,stats:()=>({bounds:boundsCache.size,dp:dpCache.size,ref:refBounds.size})};
 }
 const out={graphs:0,actualBundleChecks:0,exactStops:0,ambiguousEarlyStops:0,policyCalls:{adaptive:0,descending:0,ascending:0,full:0},maxCalls:{adaptive:0,descending:0,ascending:0},fullTruth:{unique:0,ambiguous:0,empty:0},partialReferenceChecks:0,optimalPolicyChecks:0,abstractWorstCase:{},zeroCandidateSkipChecks:0,controls:0,example:null};
 const models=new Map();
 function get(edges){let k=JSON.stringify(edges);if(!models.has(k))models.set(k,policy(edges));return models.get(k)}
 // Exhaust all abstract ternary partitions for one representative preference
 // domain with three active goals. Use independent topological enumeration only
 // for selected partitions; the full independent policy DP below caches winners
 // implicitly via its reference table.
 const fixed=get([[0,1],[1,2]]);
 for(let g=0;g<80;g++){
  let y=0,n=0;for(let i of all){let v=rnd(3);if(v===0)y|=1<<i;if(v===1)n|=1<<i;}
  let r=fixed.bounds(y,n),o=fixed.ref(y,n);ck(r.lower===o.lower&&r.upper===o.upper,"completion reference");
  ck(fixed.dp(y,n).cost===fixed.dpAll(y,n),"all-query optimality");out.partialReferenceChecks++;out.optimalPolicyChecks++;
 }
 function run(m,truth,mode){
  let y=0,n=0,calls=0;
  while(true){
   let z=m.bounds(y,n);
   if(z.done){ck(z.lower===m.winners(truth),"exact early set");return {calls,winners:z.lower,remaining:z.unknown}}
   let next=mode==="adaptive"?m.dp(y,n).next:mode==="descending"?set(z.actionable).sort((a,b)=>pop(b)-pop(a)||a-b)[0]:set(z.actionable)[0];
   ck(z.actionable&(1<<next),"query relevance");
   if(truth&(1<<next))y|=1<<next;else n|=1<<next;calls++;
   ck(calls<=8,"finite");
  }
 }
 for(let g=0;g<700;g++){
  const d=[1+rnd(2),1+rnd(2),1+rnd(2)],jobs=Array.from({length:3},()=>{let release=rnd(2);return {release,deadline:release+rnd(3-release)}});
  const ws=Array.from({length:2},()=>({d,jobs:jobs.map(j=>({...j,cost:Array.from({length:3},()=>rnd(4))})),cap:Array.from({length:3},()=>1+rnd(3)),income:Array.from({length:3},()=>rnd(5)),mandatory:Array.from({length:3},()=>rnd(3)),reserve:Array.from({length:3},()=>rnd(3))}));
  let b=rnd(10),obs=!!rnd(2),s=[[0,0,0],[0,rnd(2),rnd(2)]],edges=[];
  for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(rnd(3)===0)edges.push([i,j]);
  let truth=0;
  for(let k of all){let demand=d.map((n,i)=>k&(1<<i)?n:0),ps=ws.map(p=>({...p,d:demand}));let z=P.solve(ps,s,b,obs),r=P.oracle(ps,s,b,obs);ck(z.ok===r.ok,"planner parity");if(z.ok)truth|=1<<k;out.actualBundleChecks++}
  const m=get(edges),actual=m.winners(truth),wc=m.dp(0,0).cost;out.abstractWorstCase[JSON.stringify(edges)]=wc;
  for(let mode of ["adaptive","descending","ascending"]){
   let r=run(m,truth,mode);out.policyCalls[mode]+=r.calls;out.maxCalls[mode]=Math.max(out.maxCalls[mode],r.calls);
   if(mode==="adaptive"){ck(r.calls<=wc,"worst case");out.exactStops+=+(r.calls<8);out.ambiguousEarlyStops+=+(r.calls<8&&pop(r.winners)>1);out.zeroCandidateSkipChecks+=pop(r.remaining);
    if(r.calls<8&&pop(r.winners)>1)out.example??={feasible:set(truth),edges,winners:set(actual),calls:r.calls,unqueried:set(r.remaining)}
   }
  }
  out.policyCalls.full+=8;out.fullTruth[actual?(pop(actual)===1?"unique":"ambiguous"):"empty"]++;out.graphs++;
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 const m=get([]);
 let z=m.bounds(mask([1,2]),mask([3,5,6,7,4]));
 ctl(z.done&&eq(set(z.lower),[1,2])&&eq(set(z.unknown),[0]),"ambiguous exact without evaluating dominated empty");
 ctl(m.bounds(mask([7]),0).done,"top bundle enough");
 ctl(!m.bounds(0,0).done,"unknown all");
 ctl(m.bounds(0,ALL).done&&m.bounds(0,ALL).upper===0,"known none");
 ctl(m.bounds(mask([1]),0).lower===0,"known only not guaranteed candidate");
 return out;
}
console.log(JSON.stringify(experiment(make,make2,make3),null,2));
```
