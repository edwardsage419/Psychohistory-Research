# 自主学习：选择情景的偏好识别边界、析取约束与撤回重放
2026-11-26。RESEARCH_CANDIDATE / PREDECESSOR_CODE_EXECUTED / SYNTHETIC_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线与查重
固定main 6e7a81af3653ed40efa0bf4eb2381ba49a2568a0，核对25近期提交、15开放PR、#63 head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft、v3.2与同步规程、唯一交接固定blob 5e74f4f0b37141d631740e844ad8bbbfed232e07前段（未核对最新路径）。实际读取固定前序 research/decision_hub/2026-11-26-partial-lexicographic-goal-order-witnesses.md blob 56ccc94a47a135670b670e26e65c99503740e7e5，执行其closure/orderOK/winner等；前序部分偏好选择、R109用途反馈5d2695da1f5a380369714adb5dd6fe0a5cdaa8db、R44配对政策93ba01e1fb71e32e0f7ed7e57c5acc76afb9b091、R18反馈f55a6fb6a801bb765b96530ce71b45e58d802852、缺失预测反馈799e4e0761a5544b1b6527ff69e594b51cbd369f、延迟序贯4168eb54e9c3421cb0e8aecad7d92f5ccadbaecb及退化监测c58ae4a613957a8ecb3ad3bfbae0b5f943d33f56相关段落。本轮新增选择上下文对词典序偏好假说的联合约束及明确偏好与选择推断的隔离，既有反馈评分、权重重放、直接偏好声明、因果政策评价不重复计。7关键词检索无返回，不构成全库查重。
## 合同与证明
六二元目标；已由用户明确接受词典序偏好作为此用途假设（不由一般“更重要”推断），同主体、上下文、偏好epoch及当前授权；每次选择有已知可行菜单K、可能可行菜单P，K⊆P，选中c∈K。菜单必须覆盖所有当时相关备选，选择为明确自愿且理由完整、同信息边界下依该模型作出；真实用户通常不满足这些强条件，任何不明均隔离，不能以日常行为、结果好坏、推荐接受、未选行动推断偏好。选择记录只形成只读模型诊断假说，不能自动新增/删除已确认的偏好边、底线或长期目标。
每个竞争组合r给出析取约束：在c与r不同的目标中，第一个出现者必须属于c\r（good），而非r\c（bad）。联合多次选择要求全部约束同时成立，不能逐个good×bad生成所有成对优先边。例如选择A+B超过C，只能推出A或B中至少一个先于C，而非两者都先于C。在偏序可用节点中任取不在任一未解除约束bad中的节点；若它属于good则解除相应约束。任一如此节点可移到任何成功剩余顺序的首位而不使原成功顺序失败，且无前置关系受破坏，因此贪心完整；无可选节点则不存在相容顺序。与前序单目标多竞争者证明同型，此处多次选择共享一套顺序。以K中的竞争者生成约束，代表存在一个菜单补全与选择相容；以P生成约束，代表对所有菜单补全均相容。在菜单独立补全合同内精确；菜单关联未知时是保守必要/充分诊断，不是实际偏好识别。不同上下文或时代不得混合。明确偏好循环与选择模型不一致分开，不自动修正用户价值。枚举有限全部允许顺序得到在相容模型下所有顺序都成立的候选比较，仅供确认；全为空不凭空推出任何比较。所有输出authority NONE。
最新选择记录版本按id及获知截点选择；撤回或资格失效不退回旧记录。版本即使同值也改变证据依赖；本实验假定版本/ID/时序由可信宿主生成，未验证冲突版本、真实身份、用途分离、签名、删除或恢复。旧快照历史仅在仍授权时供审计，原型内存历史不是真实擦除。用户主动更改偏好应开启明确的新范围，不将选择拟合当用户确认，不训练任何模型。
## 实验
1200随机合成偏序、每图3个选择菜单及有意不一致的选择；分别对K和P的联合贪心存在性与全部拓扑顺序枚举对照，检查具体顺序见证。故意错误对照以每个选择直接生成全部good×bad成对优先边，记录与相容顺序冲突或排除合法假说；不以全部可能菜单当已知菜单。每图一条撤回、同值版本更新及8项资格变更，核对候选扩张、旧截止重放与不回退旧记录。7控制包括析取、未知竞争、非自愿/理由不明、显式循环及相反选择。实际标准JS连接器两次执行一致。合成研究夹具由ChatGPT研发辅助生成，非独立数据、真实用户、模型训练或现实预测表现；计数非独立样本。
```json
{
  "graphs": 1200,
  "episodes": 3600,
  "compatibleTests": 2400,
  "orderEnumerationChecks": 397482,
  "possibleOrders": 85866,
  "robustOrders": 8460,
  "robustEmpty": 899,
  "allPotentialOverstatesConflict": 780,
  "naivePairwiseWrong": 316,
  "naivePairwiseExtra": 487,
  "retractionChecks": 1200,
  "sameValueRevisionChecks": 1200,
  "qualificationRejects": 9600,
  "controls": 7,
  "example": {
    "choice": 3,
    "rival": 4,
    "possible": 480,
    "explicitEdges": [],
    "impliedCandidatePairs": []
  }
}
```
## 接入与限制
PreferenceEvidencePort独立输出EXPLICIT_USER_STATE、CHOICE_HYPOTHESIS、OBSERVED_OUTCOME、MODEL_MISMATCH，不允许反馈自动写入明确偏好；偏好假说仅在真实资格、范围、选择时菜单和用户确认充分时显示。真实学习及更新授权仍独立，原生、真实数据、独立留出、设备性能未运行。研究者选定强词典序、菜单补全、六目标、版本与资格夹具及比较基线，不能视为正式产品默认。未修改生产、唯一交接、冻结、证据等级、PR、训练、部署、主动CI或新增费用。
## 复算
固定前序报告作为唯一参数，Node包装未执行；核心已在连接器实际运行。
```js
const code=require("node:fs").readFileSync(process.argv[2],"utf8").split("\`\`\`js\n")[1].split("\n\`\`\`")[0];
const make=Function(code.split(" const out={graphs:")[0]+"\nreturn {closure,orderOK,winner,greedy,enumerate};\n}\nreturn experiment();");
function study(make){
 const R=make(),ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),N=6,ALL=63;
 let seed=20261126;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 const bits=m=>Array.from({length:N},(_,i)=>i).filter(i=>m&(1<<i));
 const sort=a=>[...a].sort((x,y)=>x-y);
 // Every rival produces a disjunctive ordering constraint: the first
 // differing goal in the order must belong to the chosen bundle.
 function clauses(row,mode){
  const rivals=mode==="NECESSARY"?row.potential:row.known;
  return rivals.filter(r=>r!==row.chosen).map(r=>({good:row.chosen&~r,bad:r&~row.chosen}));
 }
 function allOrders(p){
  let out=[];
  function walk(used,order){
   if(used===ALL){out.push(order);return}
   for(let i=0;i<N;i++)if(!(used&(1<<i))&&!(p[i]&~used))walk(used|(1<<i),[...order,i]);
  }walk(0,[]);return out;
 }
 function solve(edges,rows,mode){
  const p=R.closure(edges);if(!p)return {status:"EXPLICIT_CONFLICT",order:null};
  const c=rows.flatMap(r=>clauses(r,mode)),order=[];let used=0,live=c.slice();
  while(used!==ALL){
   let i=bits(ALL&~used).find(j=>!(p[j]&~used)&&live.every(k=>!(k.bad&(1<<j))));
   if(i===undefined)return {status:"NO_COMPATIBLE_ORDER",order:null,blocked:live,used};
   order.push(i);used|=1<<i;live=live.filter(k=>!(k.good&(1<<i)));
  }
  ck(live.length===0&&R.orderOK(order,p),"witness");
  return {status:"COMPATIBLE",order};
 }
 function qualified(r,host){
  return r.subject===host.subject&&r.context===host.context&&r.epoch===host.epoch&&r.grant===host.grant&&r.allowed&&r.model==="EXPLICIT_LEXICOGRAPHIC"&&r.covered&&r.deliberate&&r.reasonsComplete&&r.known.includes(r.chosen)&&r.known.every(x=>r.potential.includes(x))&&r.potential.every(x=>Number.isInteger(x)&&x>=0&&x<=ALL);
 }
 function view(log,host,edges){
  if(!host.allowed||host.model!=="EXPLICIT_LEXICOGRAPHIC")return {status:"UNKNOWN_QUALIFICATION",authority:"NONE"};
  let by=new Map();
  for(const r of log.filter(r=>r.received<=host.asOf)){
   const old=by.get(r.id);if(!old||r.version>old.version)by.set(r.id,r);
  }
  const usable=[...by.values()].filter(r=>qualified(r,host));
  const p=R.closure(edges);
  if(!p)return {status:"EXPLICIT_CONFLICT",authority:"NONE"};
  const os=allOrders(p);
  const possible=os.filter(o=>usable.every(r=>R.winner(o,r.known)===r.chosen));
  const robust=os.filter(o=>usable.every(r=>R.winner(o,r.potential)===r.chosen));
  // Diagnostics only. The explicit user-confirmed edges do not change.
  const possiblePairs=[];
  for(let i=0;i<N;i++)for(let j=0;j<N;j++)if(i!==j&&possible.length&&possible.every(o=>o.indexOf(i)<o.indexOf(j))&&!(p[j]&(1<<i)))possiblePairs.push([i,j]);
  return {status:possible.length?"CONDITIONAL_HYPOTHESIS":"CHOICE_MODEL_MISMATCH",possible:possible.length,robust:robust.length,orders:possible,possiblePairs,dependencies:usable.map(r=>[r.id,r.version]),confirmed:edges,authority:"NONE"};
 }
 const host={subject:"self",context:"ctx",epoch:1,grant:1,allowed:true,model:"EXPLICIT_LEXICOGRAPHIC",asOf:3};
 function row(i,known,potential,chosen,extra={}){return {id:"e"+i,version:1,received:1,subject:"self",context:"ctx",epoch:1,grant:1,allowed:true,model:"EXPLICIT_LEXICOGRAPHIC",covered:true,deliberate:true,reasonsComplete:true,known,potential,chosen,...extra}}
 const out={graphs:0,episodes:0,compatibleTests:0,orderEnumerationChecks:0,possibleOrders:0,robustOrders:0,robustEmpty:0,allPotentialOverstatesConflict:0,naivePairwiseWrong:0,naivePairwiseExtra:0,retractionChecks:0,sameValueRevisionChecks:0,qualificationRejects:0,controls:0,example:null};
 for(let g=0;g<1200;g++){
  let porder=[0,1,2,3,4,5];for(let i=N-1;i>0;i--){let j=rnd(i+1);[porder[i],porder[j]]=[porder[j],porder[i]]}
  let edges=[];for(let i=0;i<N;i++)for(let j=i+1;j<N;j++)if(rnd(5)===0)edges.push([porder[i],porder[j]]);
  let logs=[];
  for(let i=0;i<3;i++){
   let potential=sort([...new Set(Array.from({length:2+rnd(6)},()=>rnd(64)))]),known=potential.filter(()=>rnd(2)===0);if(!known.length)known=[potential[0]];
   let c=R.winner(porder,known);if(rnd(7)===0)c=known[rnd(known.length)];
   logs.push(row(i,known,potential,c));out.episodes++;
  }
  let z=view(logs,host,edges),p=R.closure(edges),os=allOrders(p);
  for(let mode of ["POSSIBLE","NECESSARY"]){
   let a=solve(edges,logs,mode),ref=os.filter(o=>logs.every(r=>R.winner(o,mode==="NECESSARY"?r.potential:r.known)===r.chosen));
   ck((a.status==="COMPATIBLE")===!!ref.length,"existence parity");
   if(a.order)ck(ref.some(o=>eq(o,a.order)),"witness parity");
   ck(ref.length===(mode==="NECESSARY"?z.robust:z.possible),"view parity");out.compatibleTests++;out.orderEnumerationChecks+=os.length;
  }
  out.possibleOrders+=z.possible;out.robustOrders+=z.robust;out.robustEmpty+=+(z.robust===0);out.allPotentialOverstatesConflict+=+(z.possible>0&&z.robust===0);
  if(z.possible>0){
   let naive=[];for(let r of logs)for(let q of r.known)for(let i of bits(r.chosen&~q))for(let j of bits(q&~r.chosen))naive.push([i,j]);
   let np=R.closure([...edges,...naive]);if(!np)out.naivePairwiseWrong++;else if(z.orders.some(o=>!R.orderOK(o,np)))out.naivePairwiseExtra++;
  }
  let k=rnd(logs.length),r=logs[k],retracted=[...logs,{...r,version:2,received:2,allowed:false}],v=view(retracted,host,edges);
  ck(z.orders.every(o=>v.orders.some(q=>eq(o,q))),"withdraw expands");
  ck(eq(view(retracted,{...host,asOf:1},edges),z),"historical");
  ck(!v.dependencies.some(d=>d[0]===r.id),"no fallback");
  out.retractionChecks++;
  let same=view([...logs,{...r,version:2,received:2}],host,edges);
  ck(eq(same.orders,z.orders)&&!eq(same.dependencies,z.dependencies),"version only");out.sameValueRevisionChecks++;
  for(let patch of [{context:"other"},{subject:"other"},{epoch:0},{grant:0},{deliberate:false},{covered:false},{reasonsComplete:false},{model:"UNKNOWN"}]){
   let bad={...r,...patch,version:2,received:2},v=view([...logs,bad],host,edges);
   ck(!v.dependencies.some(d=>d[0]===r.id)&&eq(v.orders,view(logs.filter(x=>x.id!==r.id),host,edges).orders),"qualification and no fallback");out.qualificationRejects++;
  }
  out.graphs++;
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 const r=row(0,[3,4],[3,4],3);
 let z=view([r],host,[]);
 ctl(z.orders.some(o=>o.indexOf(2)<o.indexOf(0))&&z.orders.some(o=>o.indexOf(2)<o.indexOf(1)),"disjunction not both pairwise");
 ctl(!z.possiblePairs.some(e=>eq(e,[0,2])||eq(e,[1,2])),"no forced pair");
 const u=row(0,[1],[1,2],1);
 ctl(view([u],host,[[1,0]]).possible>0&&view([u],host,[[1,0]]).robust===0,"unknown rival");
 ctl(view([row(0,[1,2],[1,2],1,{deliberate:false})],host,[]).possible===720,"choice without confirmed reason");
 ctl(view([r],host,[[0,1],[1,0]]).status==="EXPLICIT_CONFLICT","explicit cycle");
 ctl(view([r],{...host,allowed:false},[]).status==="UNKNOWN_QUALIFICATION","withdraw");
 ctl(view([row(0,[1,2],[1,2],1),row(1,[1,2],[1,2],2)],host,[]).status==="CHOICE_MODEL_MISMATCH","inconsistent choice not automatic edit");
 out.example={choice:3,rival:4,possible:z.possible,explicitEdges:z.confirmed,impliedCandidatePairs:z.possiblePairs};
 return out;
}
console.log(JSON.stringify(study(make),null,2));
```
