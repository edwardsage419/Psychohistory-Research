# 自主决策：不可拆分任务的容量分配、流松弛和有界可行性证书
2026-11-26。RESEARCH_CANDIDATE / PREDECESSOR_CODE_EXECUTED / SYNTHETIC_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线及范围
同一手动轮第三阶段，起点main cc62ebe5f0bc82e15b6f101e73501aa1182fd8f4，沿用前两阶段对v3.2、同步规程、25近期提交、15开放PR、固定交接及#63固定head 734686980b19da9291bdd08b67d4e2519c011acf 的核对；未重跑原生。本轮实际读取并复用 research/decision_hub/2026-11-26-actor-scoped-resource-flow-and-common-plan.md blob bd75b981b35e3c63cbc5550b8ea690ddea2ed80f 的flow/verify/common，前阶段已有可拆分资源分配和预留区间。已有有界搜索、动态计划、非预知政策及C035联合可行性不重复声称发明。本轮针对之前明确未支持的不可拆分需求，连接可拆分网络松弛和可复算分配见证；不是通用调度求解器或全库无重复证明。
## 合同与数学
固定3个任务、3个资源池、共同整数单位与时段，需求为1..3不可拆分单位，每任务须全部分配一个有资格的池；不同任务可使用同一池但总量不能超过容量。明确任务不可拆分及使用资格由可信宿主提供，不从自然语言自动判断；同一人在多项任务中的时间冲突若未包含在容量模型内仍需独立检查。无持续时间、顺序、旅行、技能异质性或多资源同步；不推广真实调度。给定固定任务/池身份、需求与联合世界，所有世界同一分配的充要条件仍为每池最低容量及资格交集。可拆分流是本模型的松弛：不可拆分分配可投影为合法流，故流不足严格证明无不可拆分分配；满流不证明不可拆分可行。反例：需求[3,1,1]，三池容量[2,2,2]且资格全开，满流存在但需求3没有任何单池可用。
DFS按需求降序分配，当前前缀扣减容量；剩余任务的可拆分流不足时以已核验割剪去其全部后继。其他分支只枚举资格与余量允许的单池；有完整见证时FEASIBLE，只有搜索栈耗尽才INFEASIBLE；预算耗尽未完成返回UNKNOWN_BUDGET。有限域证书不授权行为。核验器复算前缀容量、资格、割容量与剩余需求的严格差值或无单池的证书；在这个3x3域还直接枚举所有27个分配独立核对全局结果。未实现生产级可独立验证的完整搜索树覆盖收据，真实更大问题需要持久安全搜索状态、覆盖证明和资源界。节点预算按前缀检查计数，每节点至多一次小规模流松弛；不含输入、排序、序列化或实际CPU成本。由于求解前缀本身额外计算，节点下降不能直接解释为墙时提速。真实资格、来源、当前性、授权、世界覆盖由宿主确认；若缺失不得从本程序输出推导现实全称或建议。所有研究端口无授权能力。
## 实际实验
连接器标准JS实际运行两次结果一致。1600个固定种子图，每图2..5个联合世界，3任务、3池，需求1..3，容量0..6，资格掩码0..7；逐世界与共同方案分别核对独立27项分配穷举、无流松弛DFS及有松弛DFS；检查松弛假通过、完整及预算0/1/2/4/8/16/40前缀的状态单调、见证及割。专项控制3项（可拆分假通过、确定分配、零预算），另非法输入及每个存在共同方案的逐世界蕴涵控制，后者次数随图变化。计数为合成结构及重复预算，不是独立用户或原生错误率。未测设备性能。
```json
{
  "graphs": 1600,
  "worlds": 5623,
  "commonCases": 1600,
  "oracleChecks": 7223,
  "splitFalsePass": 126,
  "commonSplitFalsePass": 2,
  "everyWorldNoCommon": 76,
  "budgetChecks": 50561,
  "budgetUnknown": 11528,
  "budgetFeasible": 7813,
  "budgetInfeasible": 31220,
  "fullNodes": 13549,
  "plainNodes": 16827,
  "cutPrunes": 5355,
  "localPrunes": 71,
  "certChecks": 5426,
  "controls": 18
}
```
## 接入建议
ResourceDemand需由宿主明确splittable、固定需求、身份、窗口、资格与其他约束；不明确拆分时保留未知。可拆分时采用前阶段流方法，不可拆分且有限域支持时使用本研究候选，节点帽用尽保留未决。允许输出已证明不可行的瓶颈、具体条件性分配和进一步需要的信息，不能把松弛解当真实行动；如需更完整时序、多维资源或不可观测的未来调整，应进入独立方法资格审查。未修改生产、唯一交接、历史冻结、证据等级、PR、训练、部署、主动CI或费用。研究者选择有限规模、整数单位、搜索顺序和预算；原生、真机、独立留出及真实使用效果仍未执行。
## 复算
固定前一流报告作为唯一参数，Node包装未运行；连接器核心已运行两次。
```js
const code=require("node:fs").readFileSync(process.argv[2],"utf8").split("\`\`\`js\n")[1].split("\n\`\`\`")[0];
const make=Function(code.split(" const out={singleCases:")[0]+"\nreturn {flow,verify,witness,common,ports,brute};\n}\nreturn experiment();");
function experiment3(make){
 const {flow,verify,common}=make(),ck=(b,m)=>{if(!b)throw Error(m)},sum=a=>a.reduce((x,y)=>x+y,0);
 let seed=20261129;
 const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 const N=3,P=3;
 function valid(d,w){ck(d.length===3&&d.every(x=>Number.isInteger(x)&&x>=1&&x<=3)&&w.c.length===3&&w.c.every(x=>Number.isInteger(x)&&x>=0&&x<=9)&&w.e.length===3&&w.e.every(x=>Number.isInteger(x)&&x>=0&&x<=7),"bounded domain")}
 function witness(d,ws,x){
  return x.length===N&&x.every(j=>Number.isInteger(j)&&j>=0&&j<P)&&ws.every(w=>d.every((v,i)=>w.e[i]&(1<<x[i]))&&w.c.every((v,j)=>sum(d.filter((_,i)=>x[i]===j))<=v));
 }
 // Each DFS node reserves remaining capacities; residual split-flow failure safely prunes.
 // Node budget includes each inspected prefix and its one relaxation, excluding input setup.
 function solve(d,w,budget=Infinity,prune=true){
  valid(d,w);ck(budget===Infinity||Number.isSafeInteger(budget)&&budget>=0,"budget");
  const order=[0,1,2].sort((i,j)=>d[j]-d[i]||i-j);
  let stack=[{k:0,c:[...w.c],x:[-1,-1,-1]}],nodes=0,cutPrunes=0,localPrunes=0,cert=[];
  while(stack.length){
   if(nodes===budget)return {status:"UNKNOWN_BUDGET",nodes,cutPrunes,localPrunes,remaining:stack.length,cert};
   const p=stack.pop();nodes++;
   if(p.k===N){ck(witness(d,[w],p.x),"witness");return {status:"FEASIBLE",x:p.x,nodes,cutPrunes,localPrunes,remaining:stack.length,cert}}
   const rem=d.map((v,i)=>p.x[i]<0?v:0),e=w.e.map((m,i)=>p.x[i]<0?m:0);
   if(prune){
    const z=flow(rem,{c:p.c,e});
    if(!verify(rem,{c:p.c,e},z)){cutPrunes++;cert.push({prefix:[...p.x],cap:[...p.c],kind:"FLOW_CUT",f:z.f,cut:z.cut});continue}
   }
   const i=order[p.k];let children=0;
   for(let j=P-1;j>=0;j--)if((w.e[i]&(1<<j))&&p.c[j]>=d[i]){
    let c=[...p.c],x=[...p.x];c[j]-=d[i];x[i]=j;
    stack.push({k:p.k+1,c,x});children++;
   }
   if(!children){localPrunes++;cert.push({prefix:[...p.x],cap:[...p.c],kind:"NO_POOL",task:i})}
  }
  return {status:"INFEASIBLE",nodes,cutPrunes,localPrunes,remaining:0,cert};
 }
 function oracle(d,ws){
  let x=[];
  for(let a=0;a<P;a++)for(let b=0;b<P;b++)for(let c=0;c<P;c++){let p=[a,b,c];if(witness(d,ws,p))x.push(p)}
  return x;
 }
 function audit(d,w,z){
  for(const c of z.cert){
   // Check prefix capacities and eligibility independently.
   let left=w.c.map((v,j)=>v-sum(d.filter((_,i)=>c.prefix[i]===j)));
   ck(JSON.stringify(left)===JSON.stringify(c.cap)&&left.every(v=>v>=0),"prefix capacity");
   ck(c.prefix.every((j,i)=>j===-1||!!(w.e[i]&(1<<j))),"prefix eligibility");
   if(c.kind==="FLOW_CUT"){
    const rem=d.map((v,i)=>c.prefix[i]<0?v:0),e=w.e.map((m,i)=>c.prefix[i]<0?m:0),s=c.cut;
    ck(s[0]&&!s.at(-1),"cut terminals");
    let k=0;
    for(let i=0;i<N;i++){
     if(!s[i+1])k+=rem[i];
     for(let j=0;j<P;j++)if(s[i+1]&&!s[N+1+j]&&(e[i]&(1<<j)))k+=sum(rem)+1;
    }
    for(let j=0;j<P;j++)if(s[N+1+j])k+=left[j];
    ck(k===c.f&&k<sum(rem),"cut proof");
   }else{
    ck(c.kind==="NO_POOL"&&c.prefix[c.task]===-1&&left.every((v,j)=>!(w.e[c.task]&(1<<j))||v<d[c.task]),"local impossibility");
   }
  }
  if(z.status==="INFEASIBLE"){
   // Audit coverage of all 27 raw assignments: every otherwise admissible full assignment
   // would extend a rejected prefix, which is impossible. Oracle separately checks exact answer.
   ck(z.remaining===0,"complete");
   for(let a=0;a<P;a++)for(let b=0;b<P;b++)for(let c=0;c<P;c++){
    const x=[a,b,c];
    if(witness(d,[w],x))throw Error("false infeasible");
   }
  }
 }
 const out={graphs:0,worlds:0,commonCases:0,oracleChecks:0,splitFalsePass:0,commonSplitFalsePass:0,everyWorldNoCommon:0,budgetChecks:0,budgetUnknown:0,budgetFeasible:0,budgetInfeasible:0,fullNodes:0,plainNodes:0,cutPrunes:0,localPrunes:0,certChecks:0,controls:0};
 function check(d,w,expect,commonCase){
  const z=solve(d,w),plain=solve(d,w,Infinity,false),ok=z.status==="FEASIBLE";
  ck(ok===expect&&plain.status===z.status,"oracle and plain parity");
  if(ok)ck(witness(d,[w],z.x),"solution");
  audit(d,w,z);out.oracleChecks++;out.fullNodes+=z.nodes;out.plainNodes+=plain.nodes;out.cutPrunes+=z.cutPrunes;out.localPrunes+=z.localPrunes;out.certChecks+=z.cert.length;
  const split=verify(d,w,flow(d,w));
  ck(split||!ok,"relaxation");
  if(split&&!ok){if(commonCase)out.commonSplitFalsePass++;else out.splitFalsePass++}
  let fixed=null;
  for(const b of [0,1,2,4,8,16,40]){
   const p=solve(d,w,b);
   ck(p.nodes<=b,"budget");audit(d,w,p);
   if(p.status!=="UNKNOWN_BUDGET"){
    ck(p.status===z.status,"bounded soundness");if(fixed)ck(p.status===fixed,"monotone status");fixed=p.status;
    if(p.status==="FEASIBLE")out.budgetFeasible++;else out.budgetInfeasible++;
   }else {ck(fixed===null,"status regression");out.budgetUnknown++}
   out.budgetChecks++;
  }
  return ok;
 }
 // Split flow can use 2+1 quanta from two pools, but the indivisible task needs one pool of 3.
 const ctl=(b,m)=>{ck(b,m);out.controls++};
 let w={c:[2,2,2],e:[7,7,7]},d=[3,1,1];
 ctl(verify(d,w,flow(d,w))&&solve(d,w).status==="INFEASIBLE","split false pass");
 w={c:[3,2,1],e:[1,3,4]};ctl(solve([3,2,1],w).status==="FEASIBLE","exact assignment");
 ctl(solve([3,2,1],w,0).status==="UNKNOWN_BUDGET","zero budget");
 for(let t=0;t<1600;t++){
  let d=Array.from({length:3},()=>1+rnd(3)),W=2+rnd(4),ws=Array.from({length:W},()=>({c:Array.from({length:3},()=>rnd(7)),e:Array.from({length:3},()=>rnd(8))}));
  let each=ws.map(w=>check(d,w,oracle(d,[w]).length>0,false));out.worlds+=W;
  let c=common(ws),ok=check(d,c,oracle(d,ws).length>0,true);out.commonCases++;
  if(ok)ctl(each.every(Boolean),"common entails each");
  if(each.every(Boolean)&&!ok)out.everyWorldNoCommon++;
  out.graphs++;
 }
 let bad=false;try{solve([0,1,1],{c:[1,1,1],e:[7,7,7]})}catch{bad=true}ctl(bad,"invalid demand");
 return out;
}
console.log(JSON.stringify(experiment3(make),null,2));
```
