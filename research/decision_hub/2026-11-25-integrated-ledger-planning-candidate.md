# 自主认知专项累计第101轮候选：有限语言、双时间账本与既有长期规划真实代码整合

2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_INTEGRATION_EXECUTED / SYNTHETIC_FIXTURE / NATIVE_NOT_RUN / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线main 6d7786c5226f76875b93b6393527a8c200e69dfc。核对近20提交、13开放PR（#61待审）、v3.2首8行及此前全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、未截断Git树语言及数学文件名、第100/53/67/60轮相关前17行。实际加载第100及99轮完整报告中的既有JS原型，核对固定blob；从原始代码块截取experiment内函数定义并暴露接口，不重写其解析、到账投影或长期DP。新增接收账本投影的规划接口及当前收据验证，而非另一套孤立数学模型。无原生C028、registry、API或App执行。

## 固定资产
research/decision_hub/2026-11-25-semantic-resource-ledger-temporal-bridge.md 65008b82d4720e931c99bd66ed03228b1f8ef69e
research/decision_hub/2026-11-25-complementarity-realization-timing.md a1ea992561b43252c99e882494640b290a8fa5a4
第100轮：parse/ingest/view；第99轮：dp/oracle/pack。二者均为项目原创合成开发研究源码，非真实产品或第三方AI运行组件。第53/67轮已有方法义务及反向规划，第60轮历史迁移；此轮只接入一个长期规划研究方法，不宣称通用调度、知识引擎或第三方依赖迁移已经完成。

## 合同与增量
到账原文沿第100轮有限句式。新规划请求仅完全匹配“用当前余额完成旧计划并培训”；计划所需的剩余时间、成本、储备、未来情景均由人工宿主夹具提供，未从开放白话抽取。当前查询要求发生截止日=获知截止日=宿主当前日；禁止把历史快照作当前余额。单一账户、整数美元，固定两个现金流根的对账清单由可信夹具独立给定，不从预测自动生成事实义务。若到期清单对应实际事件尚未获知则UNKNOWN_RECONCILIATION，不把未知实际到账当作0；若最新到账来源失效则沿R100 UNKNOWN_SOURCE，不回退旧版本。清单覆盖、权限、代次、期初余额、来源有效性均外部假设，尚无真实证据资格、鉴权、隐私擦除或持久化。历史记录只读。实际现金输入R99的低/高收益共同开环规划；未来培训收益情景0/4由研究夹具另给，不使用到账预测生成或校准这些情景。旧项目成本等沿R99，终点不含未来未激活收益。仅确定两个固定情景的共同可行路径，非真实最优策略或支付/写入权限。全部authority NONE。

输出结构绑定请求、清单、设置、宿主、完整日志、有效来源及三个研究版本；当前复验重新计算并比较全部结果。该JSON字符串是保守结构快照，非签名、哈希或真实并发CAS，字段顺序依赖、对不影响计算的预测撤回也会失效，复验可能重复成本。未证明仅最小相关依赖失效。缺覆盖、未知语言、未对账、资格失效或规划预算不足无计划输出。预算只继承R99转移次数限制，不包含对账、序列化、前沿或实际设备资源，未实现全请求预算。源代码中仅调用既有可信研究函数，不执行网络内容；实际部署不得对任意外部文档执行代码。

## 实验
64个沿R100事件参数场景×5当前日×16来源掩码=5120请求。独立直接夹具余额公式及原R99直接行动序列参照核验所有合格请求的两个终点组、状态与路径计数。同一研究者设计/复用参照，非独立验收。预测当现金的错误基线仅在全源有效的合格快照加预测值重新计算同一DP；差异与额外可行仅是模型内反例。逐一更改来源、权限代次、资源设置、期初余额，复验旧收据拒绝；篡改余额拒绝，覆盖/预算边界另查。所有参数、句式及全日志绑定策略由研究者选定。未实现自主语义、真实账户对账、真实学习或设备测量。无新增外部数据、训练、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。保留正式版本范围与验收门。

## 复算
按上列顺序读取固定Markdown全文为字符串。仅对已审查的两个项目自有研究代码执行以下加载函数，绝不可扩展为执行任意网络文本。
```js
function load(text,names){let src=text.split("```js\n")[1].split("\n```")[0].split(" let o={scenarios:")[0];return Function(src+"\nreturn {"+names+"};\n}\nreturn experiment();")()}
function experiment(L,P){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),event=(id,text,received)=>({id,text,received,qualified:true});
 // Trusted fixture declares which actual settlement roots must be reconciled
 // as of a date. A forecast itself does not establish such an obligation.
 function bridge(log,req,active,manifest,settings,host,cap=100000){
  const unknown=status=>({status,authority:"NONE"});
  if(req.text!=="用当前余额完成旧计划并培训")return unknown("UNKNOWN_LANGUAGE");
  if(!host.qualified||!host.covered||host.generation!==req.generation)return unknown("UNKNOWN_QUALIFICATION");
  if(req.day!==req.asOf||req.asOf!==host.asOf)return unknown("UNKNOWN_TIME");
  let actual=log.filter(e=>e.received<=req.asOf).map(e=>L.parse(e.text)).filter(p=>p.kind==="ACTUAL");
  if(manifest.some(m=>m.day<=req.day&&!actual.some(p=>p.root===m.root&&p.day===m.day)))return unknown("UNKNOWN_RECONCILIATION");
  // Compare the latest receipt in the ledger, not an older receipt whose source remains active.
  let v=L.view(log,req.asOf,req.day,host.opening,active,true);
  if(v.status!=="CONDITIONAL")return unknown(v.status);
  let p={...settings,cash:v.balance},z=P.dp(p,[0,4],cap,true,false);
  if(z.status!=="CONDITIONAL")return unknown(z.status);
  // Full, conservative structural snapshot; not a signature or production authorization.
  let binding=JSON.stringify({req,manifest,settings,host,log,active:[...active].sort(),versions:["ledger100","planning99","bridge101"]});
  return {status:"CONDITIONAL",authority:"NONE",binding,balance:v.balance,trained:P.pack(z.trained),old:P.pack(z.old),used:z.used};
 }
 function valid(receipt,log,req,active,manifest,settings,host){
  let v=bridge(log,req,active,manifest,settings,host);
  return receipt.status==="CONDITIONAL"&&v.status==="CONDITIONAL"&&eq(receipt,v)
 }
 let o={scenarios:0,requests:0,eligible:0,unknownReconciliation:0,unknownSource:0,oracleGroupChecks:0,sequenceChecks:0,robustFeasible:0,baseFeasible:0,forecastInflatedPlan:0,forecastChangedPlanSet:0,staleRejectChecks:0,tamperRejectChecks:0,coverageChecks:0,budgetChecks:0,controls:0,witnesses:{}};
 for(let forecast of [2,5])for(let actual of [0,3])for(let revised of [0,4])for(let other of [1,4])for(let delay of [2,3])for(let opening of [0,2]){
  let log=[],ev=[event("f",`预计R1第2日到账${forecast}美元`,0),event("b",`实际R2第1日到账${other}美元`,1),event("a",`实际R1第2日到账${actual}美元`,delay),event("c",`更正实际R1第2日到账${revised}美元，替代版本1`,4)];
  for(let e of ev)ck(L.ingest(log,e)==="ACCEPT","ingest");
  let manifest=[{root:"R2",day:1},{root:"R1",day:2}],settings={hours:4,income:0,reserve:0,finish:2,cost:1};o.scenarios++;
  for(let asOf=0;asOf<=4;asOf++)for(let mask=0;mask<16;mask++){
   let active=new Set(ev.filter((_,i)=>mask&(1<<i)).map(e=>e.id)),host={qualified:true,covered:true,generation:1,asOf,opening},req={text:"用当前余额完成旧计划并培训",day:asOf,asOf,generation:1};
   let v=bridge(log,req,active,manifest,settings,host);o.requests++;
   // Separate direct expected ledger formula and original R99 direct sequence oracle.
   if(asOf>=2&&asOf<delay){ck(v.status==="UNKNOWN_RECONCILIATION"&&!Object.hasOwn(v,"trained"),"reconcile");o.unknownReconciliation++;continue}
   let missing=asOf>=1&&!active.has("b")||asOf>=delay&&!active.has(asOf>=4?"c":"a");
   if(missing){ck(v.status==="UNKNOWN_SOURCE"&&!Object.hasOwn(v,"trained"),"source");o.unknownSource++;continue}
   let balance=opening+(asOf>=1?other:0)+(asOf>=delay?(asOf>=4?revised:actual):0),q=P.oracle({...settings,cash:balance},[0,4],false);
   ck(v.status==="CONDITIONAL"&&v.balance===balance&&eq(v.trained,P.pack(q.trained))&&eq(v.old,P.pack(q.old)),"full chain");o.eligible++;o.oracleGroupChecks+=2;o.sequenceChecks+=256;o.robustFeasible+=+!!v.trained.length;o.baseFeasible+=+!!v.old.length;
   if(mask===15){
    let naive=P.dp({...settings,cash:balance+forecast},[0,4]);if(!v.trained.length&&naive.trained.size){o.forecastInflatedPlan++;o.witnesses.forecast??={asOf,opening,forecast,actual,revised,other,delay,balance,naiveBalance:balance+forecast}}
    if(!eq(v.trained,P.pack(naive.trained)))o.forecastChangedPlanSet++;
    // Same current scope but altered provenance/context, even where math is unchanged.
    let withoutForecast=new Set(active);withoutForecast.delete("f");
    for(let args of [[log,req,withoutForecast,manifest,settings,host],[log,{...req,generation:2},active,manifest,settings,{...host,generation:2}],[log,req,active,manifest,{...settings,hours:5},host],[log,req,active,manifest,settings,{...host,opening:opening+1}]]){
     ck(!valid(v,...args),"stale");o.staleRejectChecks++}
    ck(valid(v,log,req,active,manifest,settings,host),"valid");
    ck(!valid({...v,balance:v.balance+1},log,req,active,manifest,settings,host),"tampered");o.tamperRejectChecks++;
    ck(bridge(log,req,active,manifest,settings,{...host,covered:false}).status==="UNKNOWN_QUALIFICATION","coverage");o.coverageChecks++;
    ck(bridge(log,req,active,manifest,settings,host,v.used-1).status==="LIMIT","budget");o.budgetChecks++;
   }
  }
 }
 for(let t of [()=>o.scenarios===64,()=>o.requests===5120,()=>o.eligible+o.unknownReconciliation+o.unknownSource===o.requests,()=>o.oracleGroupChecks===2*o.eligible,()=>o.sequenceChecks===256*o.eligible,()=>o.unknownReconciliation===512,()=>o.forecastInflatedPlan>0,()=>o.staleRejectChecks===4*o.tamperRejectChecks,()=>o.coverageChecks===o.budgetChecks&&o.budgetChecks===o.tamperRejectChecks,()=>bridge([], {text:"随便说",day:0,asOf:0,generation:1},new Set(),[],{},{}).status==="UNKNOWN_LANGUAGE"]){ck(t(),"control");o.controls++}
 return o
}
// console.log(experiment(load(ledgerMarkdown,"parse,ingest,view"),load(planningMarkdown,"dp,oracle,pack")))
```

## 实测
```json
{
  "scenarios": 64,
  "requests": 5120,
  "eligible": 2176,
  "unknownReconciliation": 512,
  "unknownSource": 2432,
  "oracleGroupChecks": 4352,
  "sequenceChecks": 557056,
  "robustFeasible": 736,
  "baseFeasible": 1664,
  "forecastInflatedPlan": 102,
  "forecastChangedPlanSet": 254,
  "staleRejectChecks": 1152,
  "tamperRejectChecks": 288,
  "coverageChecks": 288,
  "budgetChecks": 288,
  "controls": 10,
  "witnesses": {
    "forecast": {
      "asOf": 0,
      "opening": 2,
      "forecast": 2,
      "actual": 0,
      "revised": 0,
      "other": 1,
      "delay": 2,
      "balance": 2,
      "naiveBalance": 4
    }
  }
}
```

## 后续
在授权完整工程前优先将现有研究接口统一为类型化、可版本化的原文义务、证据、数学调用、账本及结果收据；独立数据/评价不足仍是主阻塞。下一轮可从实际现有语义语料及自主候选接口连接，避免再造专用规则链。产品轨维护唯一交接，数据轨合法来源，独立轨未见评价；正式训练/版本另获授权。
