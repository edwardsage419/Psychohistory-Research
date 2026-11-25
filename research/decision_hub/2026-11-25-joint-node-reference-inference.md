# 自主认知专项累计第87轮候选：节点存在性与跨轮引用联合推理、全请求预算

2026-11-25。RESEARCH_CANDIDATE / JOINT_FINITE_GRAPH_EXECUTED / ORACLE_SPANS / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。main 08536062546de1f9653047e54f4aeba2c2712074。核查最近20提交、13开放PR（#61待审）、v3.2首8行及此前全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R86/R84/R76前14行。新增范围：将有限节点存在性与跨轮引用放进同一分区、加入当前相邻节点软交互并统一全请求子查询预算。借鉴R85/86文字及有方向节点/边分解、R84联合部分监督、R76域外候选；未直接调用历轮源码或完整特征字典、未运行原生系统。

## 固定输入
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
两固定完整JSON核对连接器blob。32情节64轮167个已有人工标注节点，12正引用，45无明确引用标签。原创公开合成开发资料（ChatGPT研发辅助），非真人、独立留出或训练。候选跨度由已有标注提供（oracle）；角色与属性未用于本轮评分；没有从开放文本提取节点、负例、实体、概念或条件。固定一元权重为1+码点长度mod3，边权为1+共享字符二元组数，均为研究者选定的任意正整数示例，当前相邻存在因子2也仅为夹具，非真实语义先验、学习权重或概率。引用候选全前轮节点，不根据标注筛选；已有ref仅用于监督掩码。前轮节点0/1存在性；当前节点状态ABSENT、NO_LINK、OUTSIDE或某一前轮节点的LINK。仅LINK需要目标节点存在，允许多个引用指向同一目标，不强制互斥。OUTSIDE表示有限候选之外的占位，不能估计真实域外概率，整个输出始终outside=true、authority=NONE。实际监督已标跨度为存在，12条引用固定目标；其余45条保留NO_LINK、OUTSIDE及所有合格前轮候选，不将null/缺失作为负例。假定每当前节点最多一条指向，尚不支持多目标、长对话、嵌套或真正语义义务。没有个人数据。

## 数学及预算
固定前轮存在掩码后，各当前节点可选域确定；沿当前序列对前一节点存在性两状态递推，加和合法当前选择，乘固定前轮一元权重；最后遍历前轮掩码求和。分配律保证对固定图的精确加权求和。边际分子通过额外固定单节点或选择后重算，完整与相容分区可供部分监督目标使用，不训练。独立参照直接递归完整赋值，使用BigInt逐项对照；同研究者编写，非独立验收。统一全请求预算：所有分区、边际子查询共享计数，计前轮掩码和当前选项循环，每次消耗前检查，任何超限整体返回LIMIT且清除部分结果；不代表真实时间、内存、BigInt位复杂度或构建成本预算。最大2,000,000研究计数及独立参照访问上限由研究者选定，非生产承诺。复杂度随前轮节点数指数增加；当前链每掩码O(m(n+3))，全边际重复子查询另计；没有复杂跨当前因子、真实多轮、候选全量或设备性能验证。相容分区仅有限已见标注，非事实概率；输出不触发数学方法或历史更正。无训练、CI、Codex、生产修改、PR合并、部署、费用或冻结协议变更。

## 复算代码
按L/S顺序载入完整JSON。
```js
function experiment(docs){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>a.length===b.length&&a.every((v,i)=>v===b[i]);
 const grams=q=>new Set([...q].slice(0,-1).map((c,i)=>c+[...q][i+1]));
 // Fixed illustrative weights. No training or annotation-derived semantic role in score.
 function build(d,e){
  let nodes=e.turns.map(t=>(d===0?t.claims:t.proposal.claims).map(c=>{let q=d===0?c.span:c.quote,i=t.text.indexOf(q);ck(i>=0&&i===t.text.lastIndexOf(q),"anchor");return {q,g:grams(q),u:BigInt(1+([...q].length%3))}}));
  let [a,b]=nodes, n=a.length,m=b.length, edges=b.map(v=>a.map(u=>1n+BigInt([...v.g].filter(g=>u.g.has(g)).length)));
  let aa=d===0?e.turns[0].claims:e.turns[0].proposal.claims,bb=d===0?e.turns[1].claims:e.turns[1].proposal.claims;
  let refs=bb.map(c=>{let s=d===0?c.supersedes:c.ref;if(typeof s!=="string")return -1;let i=d===0?aa.findIndex(x=>x.field===s.split(":").at(-1)):Number(s.split(".").at(-1))-1;ck(i>=0&&i<n,"ref");return i});
  return {n,m,a:a.map(x=>x.u),b:b.map(x=>x.u),edges,refs};
 }
 // Current choice 0=absent,1=present/no link,2=present/outside,3+i=present/link prior i.
 // Present prior weight; absent weight 1. Adjacent present current nodes have factor 2.
 // Condition on prior presence mask, then eliminate current chain.
 function partition(g,obs,extra,budget){
  let z=0n;const tick=()=>{if(budget.used>=budget.cap)throw Error("LIMIT");budget.used++};
  for(let mask=0;mask<2**g.n;mask++){
   tick();
   if(obs&&mask!==2**g.n-1)continue; // all observed prior spans positive in this corpus
   if(extra?.kind==="prior"&&!(mask&(1<<extra.i)))continue;
   let pw=1n;for(let i=0;i<g.n;i++)if(mask&(1<<i))pw*=g.a[i];
   let dp=[1n,0n];
   for(let j=0;j<g.m;j++){
    let next=[0n,0n];
    for(let c=0;c<g.n+3;c++){
     tick();
     if(c>=3&&!(mask&(1<<(c-3))))continue;
     if(obs&&(c===0||(g.refs[j]>=0&&c!==3+g.refs[j])))continue;
     if(extra?.kind==="choice"&&extra.i===j&&c!==extra.c)continue;
     let p=+(c!==0),w=c===0?1n:g.b[j]*(c>=3?g.edges[j][c-3]:1n);
     next[p]+=w*(dp[0]+dp[1]*(p?2n:1n));
    }dp=next;
   }z+=pw*(dp[0]+dp[1]);
  }return z;
 }
 // Independent recursive enumeration of all complete assignments, no DP.
 function oracle(g,obs){
  let z=0n,prior=Array(g.n).fill(0n),choices=Array.from({length:g.m},()=>Array(g.n+3).fill(0n)),visits=0,worlds=0;
  let a=[],b=[];
  function cur(j,w){
   if(++visits>2000000)throw Error("oracle cap");
   if(j===g.m){z+=w;worlds++;a.forEach((x,i)=>{if(x)prior[i]+=w});b.forEach((x,i)=>choices[i][x]+=w);return}
   for(let c=0;c<g.n+3;c++){
    if(c>=3&&!a[c-3])continue;
    if(obs&&(c===0||(g.refs[j]>=0&&c!==g.refs[j]+3)))continue;
    let v=c===0?1n:g.b[j]*(c>=3?g.edges[j][c-3]:1n);if(j&&b[j-1]&&c)v*=2n;
    b.push(c);cur(j+1,w*v);b.pop();
   }
  }
  function hist(i,w){if(i===g.n){cur(0,w);return}for(let v=obs?1:0;v<=1;v++){a.push(v);hist(i+1,w*(v?g.a[i]:1n));a.pop()}}
  hist(0,1n);return {z,prior,choices,visits,worlds};
 }
 function run(g,cap){
  let budget={cap,used:0};
  try{
   let out=[];for(let obs of [false,true]){
    let z=partition(g,obs,null,budget);
    if(!z)return {status:"INCOMPATIBLE",authority:"NONE",used:budget.used,results:null};
    let prior=g.a.map((_,i)=>partition(g,obs,{kind:"prior",i},budget));
    let choices=g.b.map((_,i)=>Array.from({length:g.n+3},(_,c)=>partition(g,obs,{kind:"choice",i,c},budget)));
    out.push({z,prior,choices});
   }
   return {status:"EXACT_FINITE",authority:"NONE",outside:true,used:budget.used,results:out};
  }catch(e){if(e.message!=="LIMIT")throw e;return {status:"LIMIT",authority:"NONE",outside:true,used:budget.used,results:null}}
 }
 let o={episodes:0,priorNodes:0,currentNodes:0,markedLinks:0,unmarkedLinks:0,partitionChecks:0,marginalChecks:0,oracleWorlds:0,oracleVisits:0,budgetChecks:0,maxBudget:0,maxOracleWorlds:0,unknownOutsidePositive:0,supervisedOutsideZero:0,fullAbsentPositive:0,observedAbsentZero:0,controls:0,records:[]};
 for(let d=0;d<docs.length;d++)for(let e of docs[d].cases){
  let g=build(d,e),v=run(g,2000000);ck(v.status==="EXACT_FINITE","run");o.episodes++;o.priorNodes+=g.n;o.currentNodes+=g.m;o.markedLinks+=g.refs.filter(x=>x>=0).length;o.unmarkedLinks+=g.refs.filter(x=>x<0).length;
  for(let k=0;k<2;k++){
   let a=v.results[k],b=oracle(g,!!k);ck(a.z===b.z,"partition");o.partitionChecks++;ck(eq(a.prior,b.prior),"prior");o.marginalChecks+=g.n;
   for(let j=0;j<g.m;j++){ck(eq(a.choices[j],b.choices[j])&&a.choices[j].reduce((s,x)=>s+x,0n)===a.z,"choice");o.marginalChecks+=g.n+3;
    if(k){if(g.refs[j]<0){ck(a.choices[j][2]>0n,"outside retained");o.unknownOutsidePositive++}else{ck(a.choices[j][2]===0n&&a.choices[j][g.refs[j]+3]===a.z,"positive link");o.supervisedOutsideZero++}ck(a.choices[j][0]===0n,"positive span");o.observedAbsentZero++}
    else{ck(a.choices[j][0]>0n,"full absent");o.fullAbsentPositive++}
   }
   o.oracleWorlds+=b.worlds;o.oracleVisits+=b.visits;o.maxOracleWorlds=Math.max(o.maxOracleWorlds,b.worlds)
  }
  ck(v.results[0].z>=v.results[1].z,"subset");
  let short=run(g,v.used-1),exact=run(g,v.used);ck(short.status==="LIMIT"&&short.results===null&&short.used===v.used-1&&exact.status==="EXACT_FINITE"&&exact.used===v.used,"aggregate budget");o.budgetChecks+=2;o.maxBudget=Math.max(o.maxBudget,v.used);
  o.records.push({id:e.id,n:g.n,m:g.m,used:v.used,fullZ:String(v.results[0].z),observedZ:String(v.results[1].z)});
 }
 for(let t of [()=>o.episodes===32,()=>o.priorNodes===110,()=>o.currentNodes===57,()=>o.markedLinks===12,()=>o.unmarkedLinks===45,()=>o.partitionChecks===64,()=>o.unknownOutsidePositive===45,()=>o.supervisedOutsideZero===12,()=>o.fullAbsentPositive===57,()=>o.observedAbsentZero===57,()=>o.budgetChecks===64,()=>run({n:1,m:1,a:[1n],b:[1n],edges:[[1n]],refs:[-1]},0).status==="LIMIT"]){ck(t(),"control");o.controls++}
 return o;
}
```

## 实际结果
```json
{
  "episodes": 32,
  "priorNodes": 110,
  "currentNodes": 57,
  "markedLinks": 12,
  "unmarkedLinks": 45,
  "partitionChecks": 64,
  "marginalChecks": 944,
  "oracleWorlds": 8840,
  "oracleVisits": 10974,
  "budgetChecks": 64,
  "maxBudget": 11744,
  "maxOracleWorlds": 1008,
  "unknownOutsidePositive": 45,
  "supervisedOutsideZero": 12,
  "fullAbsentPositive": 57,
  "observedAbsentZero": 57,
  "controls": 12,
  "records": [
    {
      "id": "L01",
      "n": 4,
      "m": 1,
      "used": 1588,
      "fullZ": "1424",
      "observedZ": "324"
    },
    {
      "id": "L02",
      "n": 4,
      "m": 2,
      "used": 4682,
      "fullZ": "16160",
      "observedZ": "5184"
    },
    {
      "id": "L03",
      "n": 4,
      "m": 1,
      "used": 1588,
      "fullZ": "1134",
      "observedZ": "48"
    },
    {
      "id": "L04",
      "n": 4,
      "m": 2,
      "used": 4682,
      "fullZ": "3344",
      "observedZ": "576"
    },
    {
      "id": "L05",
      "n": 3,
      "m": 2,
      "used": 1840,
      "fullZ": "13184",
      "observedZ": "6480"
    },
    {
      "id": "L06",
      "n": 3,
      "m": 2,
      "used": 1840,
      "fullZ": "3804",
      "observedZ": "1080"
    },
    {
      "id": "L07",
      "n": 3,
      "m": 2,
      "used": 1840,
      "fullZ": "5966",
      "observedZ": "2160"
    },
    {
      "id": "L08",
      "n": 3,
      "m": 2,
      "used": 1840,
      "fullZ": "5102",
      "observedZ": "360"
    },
    {
      "id": "L09",
      "n": 2,
      "m": 3,
      "used": 1434,
      "fullZ": "10679",
      "observedZ": "6144"
    },
    {
      "id": "L10",
      "n": 4,
      "m": 1,
      "used": 1588,
      "fullZ": "684",
      "observedZ": "108"
    },
    {
      "id": "L11",
      "n": 4,
      "m": 2,
      "used": 4682,
      "fullZ": "56061",
      "observedZ": "19008"
    },
    {
      "id": "L12",
      "n": 4,
      "m": 2,
      "used": 4682,
      "fullZ": "3480",
      "observedZ": "672"
    },
    {
      "id": "L13",
      "n": 4,
      "m": 2,
      "used": 4682,
      "fullZ": "8736",
      "observedZ": "1728"
    },
    {
      "id": "L14",
      "n": 3,
      "m": 2,
      "used": 1840,
      "fullZ": "2704",
      "observedZ": "900"
    },
    {
      "id": "L15",
      "n": 4,
      "m": 2,
      "used": 4682,
      "fullZ": "2432",
      "observedZ": "72"
    },
    {
      "id": "L16",
      "n": 4,
      "m": 2,
      "used": 4682,
      "fullZ": "8406",
      "observedZ": "2016"
    },
    {
      "id": "L17",
      "n": 3,
      "m": 3,
      "used": 3700,
      "fullZ": "23770",
      "observedZ": "10800"
    },
    {
      "id": "L18",
      "n": 2,
      "m": 3,
      "used": 1434,
      "fullZ": "19501",
      "observedZ": "12000"
    },
    {
      "id": "S01",
      "n": 4,
      "m": 2,
      "used": 4682,
      "fullZ": "99280",
      "observedZ": "19440"
    },
    {
      "id": "S02",
      "n": 3,
      "m": 1,
      "used": 628,
      "fullZ": "576",
      "observedZ": "108"
    },
    {
      "id": "S03",
      "n": 3,
      "m": 1,
      "used": 628,
      "fullZ": "168",
      "observedZ": "18"
    },
    {
      "id": "S04",
      "n": 4,
      "m": 1,
      "used": 1588,
      "fullZ": "912",
      "observedZ": "48"
    },
    {
      "id": "S05",
      "n": 3,
      "m": 1,
      "used": 628,
      "fullZ": "378",
      "observedZ": "144"
    },
    {
      "id": "S06",
      "n": 2,
      "m": 2,
      "used": 714,
      "fullZ": "170",
      "observedZ": "64"
    },
    {
      "id": "S07",
      "n": 3,
      "m": 2,
      "used": 1840,
      "fullZ": "12132",
      "observedZ": "5400"
    },
    {
      "id": "S08",
      "n": 3,
      "m": 1,
      "used": 628,
      "fullZ": "351",
      "observedZ": "64"
    },
    {
      "id": "S09",
      "n": 4,
      "m": 1,
      "used": 1588,
      "fullZ": "1377",
      "observedZ": "352"
    },
    {
      "id": "S10",
      "n": 4,
      "m": 2,
      "used": 4682,
      "fullZ": "35280",
      "observedZ": "1512"
    },
    {
      "id": "S11",
      "n": 3,
      "m": 2,
      "used": 1840,
      "fullZ": "778",
      "observedZ": "112"
    },
    {
      "id": "S12",
      "n": 5,
      "m": 2,
      "used": 11744,
      "fullZ": "161728",
      "observedZ": "6048"
    },
    {
      "id": "S13",
      "n": 3,
      "m": 2,
      "used": 1840,
      "fullZ": "13527",
      "observedZ": "2160"
    },
    {
      "id": "S14",
      "n": 4,
      "m": 1,
      "used": 1588,
      "fullZ": "540",
      "observedZ": "96"
    }
  ]
}
```

## 后续责任
继续研究真实原文候选覆盖与规模控制，先保证明确未知、可信义务与授权接口，再与数学引擎连接。当前实现仍是有限oracle跨度实验，不等于完整自主理解或正式产品。保留R50完整范围和验收门。数据轨、独立验收轨、产品轨责任不变；训练与工程版本另获授权。
