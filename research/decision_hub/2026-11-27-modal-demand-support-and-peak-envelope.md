# 自主认知：可能性量词、联合需求支持与峰值资源边界
2026-11-27。RESEARCH_CANDIDATE / FINITE_SYNTHETIC_EXECUTED / CONNECTOR_JS_EXECUTED / MANUAL_RAW_SPAN_AUDIT / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。

## 基线与去重
起点main ab18e7a09bbe9001b644f4a5bac00b3ad0c9de1e。核对20近期提交、15开放PR、v3.2与同步规程全文、唯一产品交接前20行、decision_hub目录相关标题；#63 head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft，未重跑。读直接前序匿名群体资源界6bd4044bbddd9a05278a3f92f0d53f428a113cba、部分观察策略0eb4141f42b9e1607c8f4fe4122f6cc6cb699320、相关工时227daac97ef9bc28b62d0c5f3087602a05e0cb8b、主体容量bd75b981b35e3c63cbc5550b8ea690ddea2ed80f、条件封套6f3bf015c3a82faaf863c8cc38a14230e75e7fc0、数量语义296465980e23a1d8082f81a8181343668965328b、带符号世界推理bb5596aa97731c536ff0b6aa66045bb4311ec7f1、条件模型覆盖8fa6c050fd71d60823e4dc99d4f4f7310b579a0d前段。旧模型已经处理给定联合域、观察后策略、共享容量、条件守卫和证据推理；本轮增量为联合支持域本身未确定时，仅凭合格全称与存在量词精确约束其可能峰值。非新逻辑定理、非全库查重，不宣称原生语言解析。

## 数学合同与证明
给定有限、已资格化的非空候选世界全集W，每个世界具有固定非负整数同口径资源需求c(w)。真实可能世界支持S是未知的非空子集。每条全称约束U_i要求S⊆U_i，每条存在约束E_j要求S∩E_j≠∅。仅处理这些约束的合取，不处理嵌套模态、概率、必然发生的物理时间、因果、来源竞争、矛盾证据可信度或任意支持集合之间的相关限制。W和约束资格须由宿主确认；不能从“都可能”等词直接授予。候选域缺覆盖、资格未知返回UNKNOWN_COVERAGE/UNQUALIFIED。
令A=交集U_i（无约束时W）；R={A}并{A∩E_j}。S可存在当且仅当每个R元素非空。必要性显然；充分性由各R选一元素并集构造。若可存在，A本身就是合法支持，因此每个A内世界均在某合法S中。若每个合法S的峰值为M(S)=max_{w∈S}c(w)，则精确范围端点 L=max_{R_r∈R}min_{w∈R_r}c(w)，H=max_{w∈A}c(w)。每个S必须击中全部R，故M(S)≥L；每个R取最低成本世界并集即达到L；再加入A内最高成本世界得到H且不违反任何全称或存在约束。返回两端点支持见证，可直接核查。空域是有限约束矛盾而非真空保证。端点之间未必每个整数可达。
若资源容量C≥H，则所有合格支持内所有情景满足此单资源峰值约束；C<L则每个合格支持至少存在一个超过容量的情景，不意味着实际一定超额或每个情景都失败；L≤C<H则是否具有稳健容量保证取决于仍未解决的联合支持。没有现实概率。固定事前专用预留、不能调整、观察时间、部分共享、跨期累积、资源不可拆分、具体人员身份及其他硬约束不适用本峰值判断；应调用既有资格化模型另行分析。模型无行动或记账权限，auth NONE。
例如两处各可能需要7天，容量10天，若资源可按已知实际情景动态分配、需求同时适用且加和口径有资格，分别存在需求的陈述给出峰值7至14天；明确共同需求情景可能出现时峰值14天；明确二者互斥时峰值7天。若无法调整预留，需另求固定方案，不能依据7天峰值直接批准原L05。世界0为两处不需求、1仅第一、2仅第二、3共同。以上情景不是原文已经确认的完备世界，只有夹具资格下成立。
算法使用位掩码及每条存在条件最小成本见证，时间O((|U|+|E|+1)|W|)宽松界，空间O(|E|+|W|)，世界上限16；输入世界生成可能指数增长，此处不包含其成本。未验证真实设备或大规模资源防护。不枚举2^|W|种支持，但参照穷举支持；不声称总体产品加速。

## 实测
双事件：全部16种全称允许域×16种第一存在域×16种第二存在域×3组需求权重，12288个配置，包含重复/空约束。三事件：1200个固定seed高位缩放伪随机结构，0至2全称、0至4存在约束，1至4单位需求。不是现实抽样，可能重复。直接枚举所有非空支持，独立检查量词条件、峰值两端点、世界并集、见证及每个整数容量判断。参照与候选同一研究者，非独立验收。简化基线机械把全部需求同时发生且按和计量，针对已给定加和成本的峰值合同比较，非现有产品基线或真实AI能力评估。两次完整执行结果逐项一致。每个非空配置检查覆盖未知；12专项控制。结果如下：
```json
{
  "two": {
    "cases": 12288,
    "valid": 6387,
    "conflict": 5901,
    "interval": 3324,
    "thresholds": 27677,
    "pass": 10127,
    "necessaryOverload": 10482,
    "unknown": 7068,
    "collapseFalseCertainty": 7068,
    "collapseFalseOverload": 3740,
    "collapseFalsePass": 0,
    "maxSupports": 15,
    "supports": 21891
  },
  "three": {
    "cases": 1200,
    "valid": 973,
    "conflict": 227,
    "interval": 827,
    "thresholds": 8276,
    "pass": 1790,
    "necessaryOverload": 2367,
    "unknown": 4119,
    "collapseFalseCertainty": 4119,
    "collapseFalseOverload": 817,
    "collapseFalsePass": 0,
    "maxSupports": 255,
    "supports": 93792
  },
  "controls": 12,
  "examples": {
    "separate": [
      7,
      14
    ],
    "joint": [
      14,
      14
    ],
    "exclusive": [
      7,
      7
    ],
    "capacity10": [
      "UNRESOLVED_ROBUST",
      "EVERY_SUPPORT_HAS_OVERLOAD",
      "GUARANTEED_WITHIN"
    ]
  }
}
```
其中collapseFalseCertainty为真实稳健状态未决但基线给确定；collapseFalseOverload为真实全域容量充足但基线给每支持存在超额；collapseFalsePass为真实每支持存在超额但基线给全域充足。分别计不同容量阈值的重复诊断，不是独立人群错误率。机械总和是上界，故此特定合同中FalsePass预期为零，不能推广至一般语义或资源方法。

## 原文桥接及缺口
实际完整读取固定两套公开合成开发资产：
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
连接器返回blob，未独立重算Git原始字节。人工选12段原文，逐一核对唯一出现及Unicode标量坐标；kind为事后人工解释，不是自动识别。L05的“两个地方临时都可能需要七天”不能单凭词面判断共同需求支持，也不等于每处需求下限；L12确认两项分别至少六万与共同预算上限形成条件冲突；S02“任何一套”指候选方案分别约束，不将两套房的步行时间相加；S04两人能用厨房不是同时使用；S14保留两种方式不意味着同时执行。后续原文接口需要分别提交群体身份、需求谓词、模态位置、量词范围、时间及共现资格、来源和候选域覆盖。不得把有限模型的数学充分性当自然语言资格充分性。
```json
{
  "episodes": 32,
  "reviewedSpans": 12,
  "rows": [
    {
      "id": "L05",
      "t": 0,
      "span": "两家老人要照顾",
      "start": 0,
      "end": 7,
      "kind": "group_cardinality_candidate",
      "authority": "NONE"
    },
    {
      "id": "L05",
      "t": 0,
      "span": "只有十天假",
      "start": 12,
      "end": 17,
      "kind": "resource_cap",
      "authority": "NONE"
    },
    {
      "id": "L05",
      "t": 0,
      "span": "先各留五天",
      "start": 18,
      "end": 23,
      "kind": "proposed_distribution",
      "authority": "NONE"
    },
    {
      "id": "L05",
      "t": 1,
      "span": "一旦申请就不能调",
      "start": 3,
      "end": 11,
      "kind": "reported_no_recourse",
      "authority": "NONE"
    },
    {
      "id": "L05",
      "t": 1,
      "span": "两个地方临时都可能需要七天",
      "start": 12,
      "end": 25,
      "kind": "individual_possibility_joint_unresolved",
      "authority": "NONE"
    },
    {
      "id": "L12",
      "t": 0,
      "span": "两项加起来只能十万",
      "start": 18,
      "end": 27,
      "kind": "aggregate_cap",
      "authority": "NONE"
    },
    {
      "id": "L12",
      "t": 1,
      "span": "两个都必须至少六万",
      "start": 2,
      "end": 11,
      "kind": "universal_minimum",
      "authority": "NONE"
    },
    {
      "id": "L02",
      "t": 1,
      "span": "A一年最多一次",
      "start": 0,
      "end": 7,
      "kind": "reported_upper_bound",
      "authority": "NONE"
    },
    {
      "id": "L02",
      "t": 1,
      "span": "一次都不能有",
      "start": 15,
      "end": 21,
      "kind": "zero_tolerance",
      "authority": "NONE"
    },
    {
      "id": "S02",
      "t": 0,
      "span": "任何一套都必须离车站步行十五分钟以内",
      "start": 11,
      "end": 29,
      "kind": "per_option_constraint",
      "authority": "NONE"
    },
    {
      "id": "S04",
      "t": 0,
      "span": "我们两个人都得能用厨房",
      "start": 0,
      "end": 11,
      "kind": "access_not_concurrency",
      "authority": "NONE"
    },
    {
      "id": "S14",
      "t": 1,
      "span": "这两种方式都先留着",
      "start": 13,
      "end": 22,
      "kind": "retain_alternatives",
      "authority": "NONE"
    }
  ]
}
```

## 完整复算
标准JS，experiment()不依赖外部数据；audit(docs)输入上述固定JSON解析数组。本次实际执行函数如下。
```js
function experiment(){
 const check=(v,m)=>{if(!v)throw Error(m)};
 // A support is a nonempty subset of the explicitly qualified finite world domain.
 // universal clause = every world in the support belongs to mask;
 // existential clause = at least one world in the support belongs to mask.
 const bits=(mask,n)=>Array.from({length:n},(_,i)=>i).filter(i=>mask&(1<<i));
 const min=(xs)=>Math.min(...xs),max=(xs)=>Math.max(...xs);
 function solve(cost,U,E,{covered=true,qualified=true}={}){
  const auth="NONE";
  if(!Array.isArray(cost)||cost.length===0||cost.length>16||!cost.every(x=>Number.isSafeInteger(x)&&x>=0&&x<=1000000)||!Array.isArray(U)||!Array.isArray(E))return {status:"INVALID",auth};
  const n=cost.length,full=(1<<n)-1;
  if(![...U,...E].every(m=>Number.isSafeInteger(m)&&m>=0&&m<=full))return {status:"INVALID",auth};
  if(!qualified)return {status:"UNQUALIFIED",auth};
  if(!covered)return {status:"UNKNOWN_COVERAGE",auth};
  const A=U.reduce((a,m)=>a&m,full),R=[full,...E].map(m=>m&A);
  if(R.some(m=>!m))return {status:"CONFLICT_FINITE",auth};
  const picks=R.map(m=>bits(m,n).reduce((a,b)=>cost[a]<=cost[b]?a:b));
  const lowSupport=picks.reduce((m,i)=>m|(1<<i),0);
  const highWorld=bits(A,n).reduce((a,b)=>cost[a]>=cost[b]?a:b);
  const hiSupport=lowSupport|(1<<highWorld);
  return {status:"BOUNDED_FINITE",auth,A,lo:max(picks.map(i=>cost[i])),hi:cost[highWorld],lowSupport,hiSupport,obligations:R};
 }
 function oracle(cost,U,E){
  const n=cost.length,peaks=[],supports=[];
  for(let s=1;s<(1<<n);s++){
   const worlds=bits(s,n);
   if(!U.every(m=>worlds.every(i=>(m&(1<<i))!==0)))continue;
   if(!E.every(m=>worlds.some(i=>(m&(1<<i))!==0)))continue;
   supports.push(s);peaks.push(Math.max(...worlds.map(i=>cost[i])));
  }
  return supports.length?{lo:min(peaks),hi:max(peaks),supports,union:supports.reduce((a,b)=>a|b,0)}:null;
 }
 const status=(lo,hi,c)=>hi<=c?"GUARANTEED_WITHIN":lo>c?"EVERY_SUPPORT_HAS_OVERLOAD":"UNRESOLVED_ROBUST";
 const out={two:{cases:0,valid:0,conflict:0,interval:0,thresholds:0,pass:0,necessaryOverload:0,unknown:0,collapseFalseCertainty:0,collapseFalseOverload:0,collapseFalsePass:0,maxSupports:0,supports:0},three:{cases:0,valid:0,conflict:0,interval:0,thresholds:0,pass:0,necessaryOverload:0,unknown:0,collapseFalseCertainty:0,collapseFalseOverload:0,collapseFalsePass:0,maxSupports:0,supports:0},controls:0,examples:{}};
 function test(cost,U,E,which,collapsed){
  const o=out[which];o.cases++;
  const p=solve(cost,U,E),q=oracle(cost,U,E);
  check(p.auth==="NONE","auth");
  if(!q){o.conflict++;check(p.status==="CONFLICT_FINITE","conflict");return}
  o.valid++;o.supports+=q.supports.length;o.maxSupports=Math.max(o.maxSupports,q.supports.length);
  check(p.status==="BOUNDED_FINITE"&&p.lo===q.lo&&p.hi===q.hi&&p.A===q.union,"range");
  check(q.supports.includes(p.lowSupport)&&q.supports.includes(p.hiSupport),"witness");
  check(max(bits(p.lowSupport,cost.length).map(i=>cost[i]))===p.lo&&max(bits(p.hiSupport,cost.length).map(i=>cost[i]))===p.hi,"endpoint witness");
  o.interval+=Number(p.lo!==p.hi);
  for(let c=0;c<=max(cost);c++){
   o.thresholds++;
   const truth=status(p.lo,p.hi,c);
   const flags=q.supports.map(s=>bits(s,cost.length).every(i=>cost[i]<=c));
   check(truth===(flags.every(Boolean)?"GUARANTEED_WITHIN":flags.every(x=>!x)?"EVERY_SUPPORT_HAS_OVERLOAD":"UNRESOLVED_ROBUST"),"capacity");
   if(truth==="GUARANTEED_WITHIN")o.pass++;
   else if(truth==="EVERY_SUPPORT_HAS_OVERLOAD")o.necessaryOverload++;
   else o.unknown++;
   const base=collapsed<=c?"GUARANTEED_WITHIN":"EVERY_SUPPORT_HAS_OVERLOAD";
   if(base!==truth){o.collapseFalseCertainty+=Number(truth==="UNRESOLVED_ROBUST");o.collapseFalseOverload+=Number(truth==="GUARANTEED_WITHIN");o.collapseFalsePass+=Number(truth==="EVERY_SUPPORT_HAS_OVERLOAD")}
  }
  check(solve(cost,U,E,{covered:false}).status==="UNKNOWN_COVERAGE","coverage");
 }
 // Exhaustive two-event clauses. The full universe contains four activation patterns.
 // Include empty existential clauses and repeated/uninformative clauses.
 for(let allowed=0;allowed<16;allowed++)for(let e1=0;e1<16;e1++)for(let e2=0;e2<16;e2++)for(const w of [[1,1],[1,3],[3,1]]){
  test([0,w[0],w[1],w[0]+w[1]],[allowed],[e1,e2],"two",w[0]+w[1]);
 }
 // Three events. High-bit random extraction, fixed deterministic development sample.
 let seed=20261127;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed*n/4294967296)};
 for(let t=0;t<1200;t++){
  const w=[1+rand(4),1+rand(4),1+rand(4)],cost=Array.from({length:8},(_,m)=>w.reduce((s,x,i)=>s+((m>>i)&1)*x,0));
  const U=Array.from({length:rand(3)},()=>rand(256)),E=Array.from({length:rand(5)},()=>rand(256));
  test(cost,U,E,"three",w.reduce((a,b)=>a+b,0));
 }
 const c=(v,m)=>{check(v,m);out.controls++};
 const cost=[0,7,7,14],p=solve(cost,[],[10,12]),q=solve(cost,[],[8]),s=solve(cost,[7],[10,12]);
 c(p.lo===7&&p.hi===14,"separate possible");
 c(q.lo===14&&q.hi===14,"joint possible");
 c(s.lo===7&&s.hi===7,"exclusive");
 c(solve(cost,[7],[8]).status==="CONFLICT_FINITE","contradiction");
 c(solve(cost,[],[],{covered:false}).status==="UNKNOWN_COVERAGE","unknown");
 c(solve(cost,[],[],{qualified:false}).status==="UNQUALIFIED","qualification");
 c(solve(cost,[],[16]).status==="INVALID","mask outside");
 c(solve([],[],[]).status==="INVALID","empty domain");
 c(solve(cost,[0],[]).status==="CONFLICT_FINITE","no vacuity");
 c(solve(cost,[],[0]).status==="CONFLICT_FINITE","empty existential");
 c(solve(cost,[8],[]).lo===14,"all joint");
 c(solve(cost,[],[]).lo===0&&solve(cost,[],[]).hi===14,"unconstrained");
 out.examples={separate:[p.lo,p.hi],joint:[q.lo,q.hi],exclusive:[s.lo,s.hi],capacity10:[status(p.lo,p.hi,10),status(q.lo,q.hi,10),status(s.lo,s.hi,10)]};
 return out;
}

function audit(docs){
 const rows=[];
 // Manually selected literal spans: only verify location, role descriptions are post-inspection review.
 const cases=[
 ["L05",0,"两家老人要照顾","group_cardinality_candidate"],
 ["L05",0,"只有十天假","resource_cap"],
 ["L05",0,"先各留五天","proposed_distribution"],
 ["L05",1,"一旦申请就不能调","reported_no_recourse"],
 ["L05",1,"两个地方临时都可能需要七天","individual_possibility_joint_unresolved"],
 ["L12",0,"两项加起来只能十万","aggregate_cap"],
 ["L12",1,"两个都必须至少六万","universal_minimum"],
 ["L02",1,"A一年最多一次","reported_upper_bound"],
 ["L02",1,"一次都不能有","zero_tolerance"],
 ["S02",0,"任何一套都必须离车站步行十五分钟以内","per_option_constraint"],
 ["S04",0,"我们两个人都得能用厨房","access_not_concurrency"],
 ["S14",1,"这两种方式都先留着","retain_alternatives"]
 ];
 const all=docs.flatMap(d=>d.cases);
 for(const [id,t,span,kind] of cases){
  const ep=all.find(x=>x.id===id),raw=ep.turns[t].text,index=raw.indexOf(span);
  if(index<0||raw.indexOf(span,index+span.length)>=0)throw Error("anchor "+id);
  const start=Array.from(raw.slice(0,index)).length,end=start+Array.from(span).length;
  if(Array.from(raw).slice(start,end).join("")!==span)throw Error("unicode");
  rows.push({id,t,span,start,end,kind,authority:"NONE"});
 }
 return {episodes:all.length,reviewedSpans:rows.length,rows};
}
```

## 限制与治理
研究者自行选择有限支持语法、需求加和合同、人工标注、测试范围及基线，均非产品规范。未完成原文量词解析、未知成员身份绑定、真实来源、原生入口、独立留出、真人交互、设备性能、事务/持久化、安全权限。未修改生产代码、训练、合并PR、部署、主动CI或增加费用。冻结协议、历史证据等级和唯一交接保持原样。
