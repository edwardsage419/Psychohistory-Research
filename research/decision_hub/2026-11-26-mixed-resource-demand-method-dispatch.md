# 自主数学调度：可拆分、不可拆分及未确认需求性质的混合资源分配
2026-11-26。RESEARCH_CANDIDATE / PREDECESSOR_CODE_EXECUTED / SYNTHETIC_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线与范围
同一手动轮第四阶段，起点main fabc2dbf68c1520b5eb73d06d715d30f87001b3e，沿用本轮已核对v3.2、同步规程、25近期提交、15开放PR、唯一交接及#63固定head 734686980b19da9291bdd08b67d4e2519c011acf。实际复用 research/decision_hub/2026-11-26-actor-scoped-resource-flow-and-common-plan.md blob bd75b981b35e3c63cbc5550b8ea690ddea2ed80f 的flow/verify/common；此前不可拆分研究blob 3ecd15ad1a91e31301d91c2abd1a89b01a9b1534，前两阶段研究预留身份及余量。此次增量为已确认混合任务及未知拆分性质的统一条件方法选择，非新流算法、开放白话分类、全库查重或生产修复。
## 合同与证明
沿用3个固定需求及3个池、同单位同窗口、需求1..3整数单位，明确拆分、不可拆分或未确认三态。若所有任务可拆分，调用前序整数流；若全部不可拆分，搜索所有资格允许的单池分配；混合时仅对不可拆分任务搜索，剩余可拆分需求在每个完成前缀调用整数流。任何真实可行混合分配的前缀剩余需求可作可拆分流，故流松弛不足可以安全剪枝；满流只在所有不可拆分任务已经分配后构成混合见证。所有非剪枝且合法的单池分配都进入有限搜索；未完成不能确证失败。共同方案仍使用固定需求及身份、各池最低容量和资格交集。
未知性质不默认为可拆分或不可拆分。分别构造放宽域（所有未知可拆分）与收紧域（所有未知不可拆分）。任何真实解释的可行分配集合在二者之间。放宽仍无解则所有解释无解；收紧有解且具体分配在所有类型解释有效则可证共同见证；否则UNKNOWN_TYPE_OR_BUDGET。这里允许明确区分可拆分是允许拆分但不强制拆分，故收紧解也是放宽解；若现实义务要求多主体协作或禁止集中，必须换合同，不能直接用此规则。节点预算在两次求解间共享扣减，不将每次单独满额重复计算；每节点含至多一次小流松弛，未测实际时间、内存或CPU上限。条件类型、世界覆盖、授权、时效、真实证据仍由可信宿主保证，本程序不自动验证；各结果研究用途无行动权，若域覆盖未确认只允许已知域的条件只读结果。没有真实持久收据或可独立验证的完整搜索树证明，有限域用逐分配复算。
## 实际实验
1800合成图、2..4世界、任务需求1..3、容量0..6、资格掩码0..7，任务性质独立选择三态。逐世界及共同方案对照逐任务枚举所有三池整数分配，并遍历所有未知类型补全，验证可行性和共同见证；检查预算0/1/2/4/8/16/32下不越额、不错误判定。统计把全部需求当可拆分或全部不可拆分的错误及未知类型强行取极端的风险。7个专项控制（混合、不可拆分、未知、放宽失败、收紧见证、零预算、非法类型）。连接器核心实际执行两次结果一致。均为重复合成结构，不是真实独立样本、原生错误率或产品性能。
```json
{
  "graphs": 1800,
  "worldPorts": 5401,
  "commonPorts": 1800,
  "knownTypeChecks": 2168,
  "unknownTypeChecks": 5033,
  "budgetChecks": 50407,
  "budgetUnknown": 11766,
  "unknownTypeAllYes": 1298,
  "unknownTypeAllNo": 3694,
  "unknownTypeMixed": 41,
  "unknownTypeOptimisticFalsePass": 41,
  "unknownTypePessimisticFalseReject": 41,
  "allSplitFalsePass": 14,
  "allIndivFalseReject": 24,
  "routeCounts": {
    "UNKNOWN_TYPE_SHARED_WITNESS": 1298,
    "UNKNOWN_TYPE_RELAXATION_FAILURE": 3694,
    "MIXED": 1565,
    "FLOW": 317,
    "TYPE_UNRESOLVED": 41,
    "INDIVISIBLE": 286
  },
  "nodes": {
    "UNKNOWN_TYPE_SHARED_WITNESS": 6657,
    "UNKNOWN_TYPE_RELAXATION_FAILURE": 3706,
    "MIXED": 2235,
    "FLOW": 317,
    "TYPE_UNRESOLVED": 165,
    "INDIVISIBLE": 503
  },
  "controls": 7
}
```
## 工程接入建议
资源身份与预留来源证据先经可信宿主校验，明确任务需求、是否允许拆分及使用资格。由此选择FLOW/INDIVISIBLE/MIXED研究方法；未知性质则在同一预算内尝试放宽不可行或收紧共同见证，仅当类型不确定性改变结果且仍需确定答案时提出澄清。当前不执行原生方法注册、用户授权、时间调度或真实长期写入；需与原生语义义务、时域、来源、版本和结果回退合同对接，独立轨验证未见输入。研究者选择有限类型合同、搜索顺序、预算及测试种子。未修改生产、交接、历史冻结、证据等级、PR、训练、部署、主动CI或费用。
## 复算
固定前序流报告为唯一参数，Node包装未执行；连接器核心已执行两次。
```js
const code=require("node:fs").readFileSync(process.argv[2],"utf8").split("\`\`\`js\n")[1].split("\n\`\`\`")[0];
const make=Function(code.split(" const out={singleCases:")[0]+"\nreturn {flow,verify,witness,common,ports,brute};\n}\nreturn experiment();");
function experiment(make){
 const {flow,verify,common}=make(),ck=(b,m)=>{if(!b)throw Error(m)},sum=a=>a.reduce((x,y)=>x+y,0),N=3,P=3;
 let seed=20261130;
 const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 function checkWitness(d,types,ws,x){
  return x.length===N&&x.every((r,i)=>r.length===P&&r.every(v=>Number.isInteger(v)&&v>=0)&&sum(r)===d[i]&&(types[i]===0||r.filter(v=>v>0).length===1))&&ws.every(w=>x.every((r,i)=>r.every((v,j)=>v===0||!!(w.e[i]&(1<<j))))&&w.c.every((v,j)=>sum(x.map(r=>r[j]))<=v));
 }
 function validate(d,t,w,budget){
  ck(d.length===N&&d.every(v=>Number.isSafeInteger(v)&&v>=1&&v<=3),"d");
  ck(t.length===N&&t.every(v=>[0,1,null].includes(v)),"type");
  ck(w.c.length===P&&w.c.every(v=>Number.isSafeInteger(v)&&v>=0&&v<=9)&&w.e.length===N&&w.e.every(v=>Number.isInteger(v)&&v>=0&&v<8),"world");
  ck(budget===Infinity||Number.isSafeInteger(budget)&&budget>=0,"budget");
 }
 function solve(d,t,w,budget=Infinity){
  validate(d,t,w,budget);
  const indiv=[0,1,2].filter(i=>t[i]===1).sort((i,j)=>d[j]-d[i]||i-j);
  // Unknown task semantics: optimistic relaxation may prove impossibility; pessimistic
  // all unknown indivisible may prove a witness valid under either interpretation.
  if(t.includes(null)){
   const opt=solve(d,t.map(v=>v===null?0:v),w,budget);
   if(opt.status==="INFEASIBLE")return {...opt,route:"UNKNOWN_TYPE_RELAXATION_FAILURE"};
   const remain=budget===Infinity?Infinity:budget-opt.nodes;
   const pess=solve(d,t.map(v=>v===null?1:v),w,remain);
   const nodes=opt.nodes+pess.nodes;
   if(pess.status==="FEASIBLE")return {...pess,nodes,route:"UNKNOWN_TYPE_SHARED_WITNESS"};
   return {status:"UNKNOWN_TYPE_OR_BUDGET",nodes,route:"TYPE_UNRESOLVED"};
  }
  const route=indiv.length===0?"FLOW":indiv.length===N?"INDIVISIBLE":"MIXED";
  let stack=[{k:0,c:w.c.slice(),x:Array.from({length:N},()=>Array(P).fill(0))}],nodes=0,cutPrunes=0;
  while(stack.length){
   if(nodes===budget)return {status:"UNKNOWN_BUDGET",route,nodes,cutPrunes};
   const p=stack.pop();nodes++;
   const assigned=new Set(indiv.slice(0,p.k)),rem=d.map((v,i)=>assigned.has(i)?0:v),e=w.e.map((v,i)=>assigned.has(i)?0:v);
   const z=flow(rem,{c:p.c,e});
   if(!verify(rem,{c:p.c,e},z)){cutPrunes++;continue}
   if(p.k===indiv.length){
    const x=p.x.map((r,i)=>assigned.has(i)?r:z.x[i]);
    ck(checkWitness(d,t,[w],x),"mixed witness");
    return {status:"FEASIBLE",route,nodes,cutPrunes,x};
   }
   const i=indiv[p.k];
   for(let j=P-1;j>=0;j--)if((w.e[i]&(1<<j))&&p.c[j]>=d[i]){
    const c=p.c.slice(),x=p.x.map(r=>r.slice());c[j]-=d[i];x[i][j]=d[i];stack.push({k:p.k+1,c,x});
   }
  }
  return {status:"INFEASIBLE",route,nodes,cutPrunes};
 }
 function oracle(d,t,ws){
  const options=d.map((v,i)=>{
   const out=[];
   for(let a=0;a<=v;a++)for(let b=0;b<=v-a;b++){
    const r=[a,b,v-a-b];
    if(t[i]===1&&r.filter(n=>n>0).length!==1)continue;
    if(ws.every(w=>r.every((n,j)=>n===0||!!(w.e[i]&(1<<j)))))out.push(r);
   }return out;
  });
  for(const a of options[0])for(const b of options[1])for(const c of options[2])
   if(checkWitness(d,t,ws,[a,b,c]))return true;
  return false;
 }
 function completions(t){
  if(!t.includes(null))return [t];
  const k=t.indexOf(null);return [0,1].flatMap(v=>completions(t.map((x,i)=>i===k?v:x)));
 }
 const out={graphs:0,worldPorts:0,commonPorts:0,knownTypeChecks:0,unknownTypeChecks:0,budgetChecks:0,budgetUnknown:0,unknownTypeAllYes:0,unknownTypeAllNo:0,unknownTypeMixed:0,unknownTypeOptimisticFalsePass:0,unknownTypePessimisticFalseReject:0,allSplitFalsePass:0,allIndivFalseReject:0,routeCounts:{},nodes:{},controls:0};
 function check(d,t,ws,isCommon){
  const w=isCommon?common(ws):ws[0],z=solve(d,t,w),variants=completions(t),truth=variants.map(v=>oracle(d,v,ws));
  const exp=truth.every(Boolean)?"FEASIBLE":truth.every(v=>!v)?"INFEASIBLE":"UNKNOWN_TYPE_OR_BUDGET";
  ck(z.status===exp,"complete parity");
  if(z.status==="FEASIBLE")ck(variants.every(v=>checkWitness(d,v,ws,z.x)),"all type witness");
  if(isCommon)out.commonPorts++;else out.worldPorts++;
  out.routeCounts[z.route]=(out.routeCounts[z.route]||0)+1;out.nodes[z.route]=(out.nodes[z.route]||0)+z.nodes;
  if(t.includes(null)){
   out.unknownTypeChecks++;
   if(exp==="FEASIBLE")out.unknownTypeAllYes++;
   else if(exp==="INFEASIBLE")out.unknownTypeAllNo++;
   else{out.unknownTypeMixed++;out.unknownTypeOptimisticFalsePass++;out.unknownTypePessimisticFalseReject++}
  }else{
   out.knownTypeChecks++;
   if(oracle(d,[0,0,0],ws)&&exp==="INFEASIBLE")out.allSplitFalsePass++;
   if(!oracle(d,[1,1,1],ws)&&exp==="FEASIBLE")out.allIndivFalseReject++;
  }
  for(const b of [0,1,2,4,8,16,32]){
   const q=solve(d,t,w,b);ck(q.nodes<=b,"budget cap");out.budgetChecks++;
   if(q.status==="FEASIBLE"||q.status==="INFEASIBLE"){
    ck(q.status===exp,"budget sound");
    if(q.status==="FEASIBLE")ck(variants.every(v=>checkWitness(d,v,ws,q.x)),"bounded witness");
   }else out.budgetUnknown++;
  }
 }
 for(let t=0;t<1800;t++){
  const d=Array.from({length:N},()=>1+rnd(3)),types=Array.from({length:N},()=>[0,1,null][rnd(3)]),W=2+rnd(3),ws=Array.from({length:W},()=>({c:Array.from({length:P},()=>rnd(7)),e:Array.from({length:N},()=>rnd(8))}));
  for(const w of ws)check(d,types,[w],false);check(d,types,ws,true);out.graphs++;
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 const d=[3,1,1],w={c:[2,2,2],e:[7,7,7]};
 ctl(solve(d,[0,1,1],w).status==="FEASIBLE","mixed split large demand");
 ctl(solve(d,[1,0,0],w).status==="INFEASIBLE","indiv large demand");
 ctl(solve(d,[null,1,1],w).status==="UNKNOWN_TYPE_OR_BUDGET","unknown not guessed");
 ctl(solve(d,[null,0,0],{c:[1,1,1],e:[7,7,7]}).status==="INFEASIBLE","optimistic failure");
 ctl(solve(d,[null,null,null],{c:[3,1,1],e:[1,2,4]}).status==="FEASIBLE","pessimistic witness");
 ctl(solve(d,[null,null,null],w,0).nodes===0,"zero budget");
 let bad=false;try{solve(d,[0,1,2],w)}catch{bad=true}ctl(bad,"invalid type");
 return out;
}
console.log(JSON.stringify(experiment(make),null,2));
```
