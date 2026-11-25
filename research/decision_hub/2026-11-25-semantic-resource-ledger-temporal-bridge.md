# 自主认知专项累计第100轮候选：有限语言到账语义、双时间资源账本与硬约束输入

2026-11-25。RESEARCH_CANDIDATE / BOUNDED_LANGUAGE_LEDGER_EXECUTED / SYNTHETIC_FIXTURE / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线main 02924709750569cb941a74cc5a36a90db129f229。核对近20提交、13开放PR（#61待审）、v3.2首8行及历史全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、未截断仓库树相关文件、第99轮、反馈重放第18轮、语义修订第2轮、跨轮身份第64轮各首16行。增量为实际有限中文输入至到账事件、获知时点及发生时点的资源投影，再比较可支用现金硬门。已有预测评分反馈重放与约束修改不重复。未连接R97-99完整DP、C028或原生API。

## 合同
有限完整句式：预计/实际/更正实际+显式R1/R2+第1/2/3日+到账+0..999整数美元；更正必须携带替代版本1/2。原型只支持单一账户、美元正向到账（含0）、每根一次事件，预测与实际独立链；预测仅一版，不实现预测修改、多次分期到账、支出、承诺修改、跨主体或自然指代。使用显式ID及合格标记、接收日、期初余额、独立完整覆盖及有效来源集均由研究者可信夹具给定，未实现真实鉴权、确认、签名、证据核验、存储或授权。源撤回这里只模拟失去使用资格，非真实隐私删除、历史备份擦除或现金流冲销。历史查询的来源集由外部给定，未自动重建历史撤回时点；撤回后的最新实际版本无资格则相关现金未知，不回退旧金额。现金查询要求发生日不晚于获知截止日。实际发生日不能晚于接收日；预测仅允许未来日期。实际更正只改变金额、显式引用上一版本及原发生日；接收日单调，历史预测不被覆盖。相同请求ID且相同字段载荷幂等；不同载荷拒绝。代码以JSON字段顺序比较请求，非生产规范化或加密身份。根身份不凭词面推断；不同根可能实际同一现金流，仍需可信去重。原文只是有限规则解析，绝非开放白话理解。

## 双时间投影
截至获知日a，取接收日≤a的实际事件链的最新版本；对发生日≤d≤a的事件仅使用有效来源且合格的最新金额，余额=已确认初始余额+这些金额之和。真实遗漏事件、来源不明或不完整账本不能以0代替；本轮covered布尔由外部指定，人工夹具仅测试已记录事件及其更正。迟到到账在获知之前不可进入当时记录投影，不代表实际尚未到账。as-of余额只是已知且覆盖资格成立的条件值，非真实历史银行余额。预测单独列示，不参与实际现金余额；后续规划可用独立条件情景，不自动实现收益。缺来源/覆盖/时间资格、预算超限无余额输出；authority NONE。仅预算计记录扫描，不是完整请求资源。硬门示例为余额≥指定支出阈值（1/3/5/7）；非原生C028或实际支付权限。真实用户授权、数据撤回、存储加密、跨期义务与长期规划接入待完成。

## 实验
64个合成场景，每个四事件（预测、另一实际事件、迟到或准时实际、金额更正），对5个获知日、所有不晚于获知日的发生截止日及16种来源掩码核验15360次投影。直接由生成参数构造参照，不调用解析/版本遍历，同一研究者编写，非独立验收。只在全部来源有效的快照比较错误基线：使用最新更正倒灌历史、预测额直接加到现金、修订前后实际重复累计。支出阈值错误放行次数为快照×阈值计数，不是独立人次或真实产品错误率。所有数据为项目原创合成夹具，非真人、真实银行数据或训练集。无新增外部资料、训练、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。参数、时序、句式和资格策略由研究者选定。保留完整版本范围及正式验收门。

## 复算
```js
function experiment(){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 // Finite explicit language, full match; no inferred reference or identity.
 function parse(s){
  let m=/^(预计|实际|更正实际)(R[12])第([123])日到账([0-9]{1,3})美元(?:，替代版本([12]))?$/.exec(s);
  if(!m)return null;
  let [_,kind,root,day,amount,parent]=m;
  if((kind==="更正实际")!==Boolean(parent))return null;
  return {kind:kind==="预计"?"FORECAST":"ACTUAL",root,day:+day,amount:+amount,parent:parent?+parent:0}
 }
 // Host receipt qualification is a fixture, not real authorization.
 function ingest(log,e){
  let p=parse(e.text);if(!p||!e.qualified||!e.id||!Number.isInteger(e.received)||e.received<0)return "REJECT";
  let prior=log.find(x=>x.id===e.id);if(prior)return eq(prior,e)?"DUPLICATE":"REJECT";
  if(log.length&&e.received<log.at(-1).received)return "REJECT";
  if(p.kind==="ACTUAL"&&p.day>e.received)return "REJECT";
  let chain=log.map(x=>parse(x.text)).filter(x=>x.root===p.root&&x.kind===p.kind);
  if(p.kind==="FORECAST"&&chain.length)return "REJECT";
  if(p.kind==="ACTUAL"&&(p.parent!==chain.length||chain.length&&p.day!==chain[0].day))return "REJECT";
  if(p.kind==="FORECAST"&&p.day<=e.received)return "REJECT";
  log.push({...e});return "ACCEPT";
 }
 // Relevant source coverage and fixed opening balance are external fixture.
 // A withdrawn latest actual must not fall back to an earlier observation.
 function view(log,asOf,day,opening,active,covered=true,cap=1000){
  if(!covered)return {status:"UNKNOWN_COVERAGE",authority:"NONE"};
  if(day>asOf)return {status:"UNKNOWN_TIME",authority:"NONE"};
  let latest=new Map(),forecasts=[],used=0;
  for(let e of log){if(used>=cap)return {status:"LIMIT",authority:"NONE"};used++;
   if(e.received>asOf)continue;let p=parse(e.text);if(p.kind==="FORECAST"){if(active.has(e.id))forecasts.push({root:p.root,day:p.day,amount:p.amount});continue}
   latest.set(p.root,{...p,id:e.id});
  }
  let balance=opening,missing=[],applied=[];
  for(let p of latest.values())if(p.day<=day){if(!active.has(p.id)){missing.push(p.root);continue}balance+=p.amount;applied.push(p.id)}
  if(missing.length)return {status:"UNKNOWN_SOURCE",authority:"NONE",missing,forecasts};
  return {status:"CONDITIONAL",authority:"NONE",balance,applied,forecasts};
 }
 let o={scenarios:0,eventsAccepted:0,duplicateChecks:0,conflictChecks:0,snapshots:0,knownSnapshots:0,unknownSnapshots:0,forecastExcludedChecks:0,latestCorrectionChecks:0,retroactiveLeakCases:0,forecastAsCashCases:0,duplicateSumCases:0,falseFeasibleForecast:0,falseFeasibleLatest:0,coverageChecks:0,budgetChecks:0,controls:0,witnesses:{}};
 const event=(id,text,received,qualified=true)=>({id,text,received,qualified});
 for(let predicted of [2,5])for(let actual of [0,3])for(let revised of [0,4])for(let other of [1,4])for(let delay of [2,3])for(let opening of [0,2]){
  let log=[],es=[event("f",`预计R1第2日到账${predicted}美元`,0),event("b",`实际R2第1日到账${other}美元`,1),event("a",`实际R1第2日到账${actual}美元`,delay),event("c",`更正实际R1第2日到账${revised}美元，替代版本1`,4)];
  for(let e of es){ck(ingest(log,e)==="ACCEPT","accept");o.eventsAccepted++;let snap=JSON.stringify(log);ck(ingest(log,e)==="DUPLICATE"&&JSON.stringify(log)===snap,"dup");o.duplicateChecks++;ck(ingest(log,{...e,text:e.text.replace("美元","美元 ")})==="REJECT"&&JSON.stringify(log)===snap,"invalid");o.conflictChecks++}
  o.scenarios++;
  for(let asOf=0;asOf<=4;asOf++)for(let day=0;day<=asOf;day++)for(let mask=0;mask<16;mask++){
   let active=new Set(es.filter((_,i)=>mask&(1<<i)).map(e=>e.id)),v=view(log,asOf,day,opening,active),missing=[],balance=opening,ids=[];
   // Independent direct fixture oracle: no parser or version traversal.
   if(day>=1){if(active.has("b")){balance+=other;ids.push("b")}else missing.push("R2")}
   if(day>=2&&asOf>=delay){let id=asOf>=4?"c":"a";if(active.has(id)){balance+=asOf>=4?revised:actual;ids.push(id)}else missing.push("R1")}
   o.snapshots++;
   if(missing.length){ck(v.status==="UNKNOWN_SOURCE"&&!Object.hasOwn(v,"balance")&&eq(v.missing,missing),"missing");o.unknownSnapshots++;continue}
   ck(v.status==="CONDITIONAL"&&v.balance===balance&&eq(v.applied,ids),"balance");o.knownSnapshots++;
   // The forecast stream cannot change realized balance.
   let toggle=new Set(active);active.has("f")?toggle.delete("f"):toggle.add("f");
   ck(view(log,asOf,day,opening,toggle).balance===v.balance,"forecast separation");o.forecastExcludedChecks++;
   if(day>=2&&asOf>=4){ck(v.applied.includes("c")&&!v.applied.includes("a"),"latest");o.latestCorrectionChecks++}
   // Comparators limited to all-source-qualified snapshots.
   if(mask===15){
    let naiveLatest=opening+(day>=1?other:0)+(day>=2?revised:0),naiveForecast=balance+predicted,naiveDuplicate=balance+(day>=2&&asOf>=4?actual:0);
    if(naiveLatest!==balance){o.retroactiveLeakCases++;o.witnesses.leak??={p:{predicted,actual,revised,other,delay,opening},asOf,day,balance,naiveLatest}}
    if(naiveForecast!==balance)o.forecastAsCashCases++;
    if(naiveDuplicate!==balance)o.duplicateSumCases++;
    for(let need of [1,3,5,7]){if(balance<need&&naiveForecast>=need)o.falseFeasibleForecast++;if(balance<need&&naiveLatest>=need)o.falseFeasibleLatest++}
   }
  }
  let active=new Set(es.map(e=>e.id));ck(view(log,4,4,opening,active,false).status==="UNKNOWN_COVERAGE","coverage");o.coverageChecks++;
  ck(view(log,4,4,opening,active,true,3).status==="LIMIT"&&view(log,4,4,opening,active,true,4).status==="CONDITIONAL","budget");o.budgetChecks++;
 }
 let l=[];for(let [e,expect] of [[event("a","实际R1第2日到账3美元",1),"REJECT"],[event("a","实际R1第2日到账3美元",2,false),"REJECT"],[event("a","更正实际R1第2日到账3美元，替代版本1",2),"REJECT"],[event("a","实际R1第2日到账3美元",2),"ACCEPT"],[event("a","实际R1第2日到账4美元",2),"REJECT"],[event("b","更正实际R1第3日到账4美元，替代版本1",3),"REJECT"],[event("b","实际R1第2日到账4美元",3),"REJECT"],[event("b","更正实际R1第2日到账4美元，替代版本1",3),"ACCEPT"],[event("c","更正实际R1第2日到账5美元，替代版本1",4),"REJECT"],[event("c","预计R2第1日到账4美元",4),"REJECT"],[event("c","预计R2第3日到账4美元",1),"REJECT"]]){ck(ingest(l,e)===expect,"control event");o.controls++}
 ck(view(l,1,2,0,new Set(["a","b"])).status==="UNKNOWN_TIME","future");o.controls++;
 ck(o.scenarios===64&&o.snapshots===15360&&o.knownSnapshots+o.unknownSnapshots===o.snapshots,"accounting");o.controls++;
 return o;
}
console.log(experiment())
```

## 实测
```json
{
  "scenarios": 64,
  "eventsAccepted": 256,
  "duplicateChecks": 256,
  "conflictChecks": 256,
  "snapshots": 15360,
  "knownSnapshots": 8832,
  "unknownSnapshots": 6528,
  "forecastExcludedChecks": 8832,
  "latestCorrectionChecks": 768,
  "retroactiveLeakCases": 136,
  "forecastAsCashCases": 960,
  "duplicateSumCases": 96,
  "falseFeasibleForecast": 1352,
  "falseFeasibleLatest": 118,
  "coverageChecks": 64,
  "budgetChecks": 64,
  "controls": 13,
  "witnesses": {
    "leak": {
      "p": {
        "predicted": 2,
        "actual": 0,
        "revised": 4,
        "other": 1,
        "delay": 2,
        "opening": 0
      },
      "asOf": 2,
      "day": 2,
      "balance": 1,
      "naiveLatest": 5
    }
  }
}
```

## 后续
优先建立已有自主语言候选、真实义务确认、资源账本及数学方法的版本化接口与完整工程验收计划；避免把100轮研究计数当成训练或产品完成度。缺少开放语义、合法独立语料、实际学习、原生全链路与真机验证。数据、独立验收、产品轨职责不变，训练和正式工程另获授权。
