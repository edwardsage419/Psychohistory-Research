# 账本至收益门槛与预算续算的研究链集成及v0.7接口缺口
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_INTEGRATION_EXECUTED / SYNTHETIC_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。起始main 25ef47505e8b172fb8e3925fd85da94cdb7c17fe；Draft #62固定候选 e61bbad10932edabc9a87483e5407fdae6c751cc。核对近期12提交、14开放PR、v3.2/同步规程/唯一产品交接前22行（交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07）；检索integration/envelope/bridge/end-to-end/native method，审阅R34 4b3205e91e627819782e2d1fda50f2de16f0e608及R101 4dc2396abfe47ebc95327b3da715462455ca5a5a合同前段；进一步历史commit读取遇连接器RemoteProtocolError，未完成该项复审。R101已把有限到账语义接入旧R99 DP，本轮只新增实际连接近期收益阈值、情景连接及续算接口，沿用R101对账原则，不重复其DP、不声称全库无重叠。
## 固定资产
research/decision_hub/2026-11-25-resumable-budgeted-world-join.md @ 25ef47505e8b172fb8e3925fd85da94cdb7c17fe @ d4a85f1e92744d1179f76a47cf56926d17b18cf3
research/decision_hub/2026-11-25-world-bound-multistage-result-join.md @ 879ef117e9c6978482784eb81006bdc1468b5298 @ af4daae1aaeee5a36a140d8a0f272a48c064368b
research/decision_hub/2026-11-25-recurring-benefit-feasibility-threshold.md @ 45934aedcc37ad2bae1c56cee4dce4959befeccc @ 9c27c104e3be8f18eebc18f5ad8a0e10e2940fcf
research/decision_hub/2026-11-25-semantic-resource-ledger-temporal-bridge.md @ 6d7786c5226f76875b93b6393527a8c200e69dfc @ 65008b82d4720e931c99bd66ed03228b1f8ef69e
四份报告连接器blob核对一致，实际提取原研究函数，非原生产品入口。v0.7源码已读取decision_candidates.py a697b9f4dbdde12267f883df29de65e4a2d56723、decision_resources.py 53708241b09e03d1bef7beed17cb304db508bf3c、decision_conversation.py ed1c5aa8407f53ef3dfc1484ba1a18ef1edabcad、decision_planner.py f2d3d21b853afe9dc757a33e83cd3d6160f8dd7b、decision_language.py 4e6733499f74db505e2cedaff84cf8c5eae207d1；核查符号及候选登记正文前段；V07_RESEARCH_INTEGRATION.md 05508e59216294b0ff312df78c14adedf7cb6520，V07_INDEPENDENT_HANDOFF.md a6af56d5741f137433b081452cf0acd116dbf217。非完整源审计或重新验收。
## 连接合同
固定R100有限中文到账句式、单账户整数美元、独立应对账R2第1日/R1第2日（不是由预测推定），查询发生和获知时点等于可信当前日。计划参数由合成宿主指定，当前日结束后进入新的四期相对规划时间，不自动从开放语言取得计划目标或时间锚。当前余额来自实际最新有效到账；应到期但未获知阻塞，最新更正来源失效阻塞，不回退。预测到账独立列示，不进入实际余额、收益情景或用户授权。将现金送入原threshold，未来费用/滞后/收益8个情景由夹具提供，固定储备1、基础净收入0、两旧目标各一工作槽且成本1、新计划第1期。计算实际可行谓词，再送入原group/prepare/advance。全域与有限关联域两种，收益来源覆盖全量/掩码85两种。局部计划始终authority NONE；逐情景存在日程不意味着不观察未来就有共同可实施策略。没有模型预测或长期效用排序。所有身份及epoch为可信夹具，真实变更时必须由宿主提升代次并作原子校验，实验只验证给不同epoch时旧状态拒绝，不实现真实撤回/存储/并发或签名。预算仅针对组对续算，前置计算不受其限制。未知真实计划参数须阻断，不能以合成值补齐。
## 实验
沿R100 64记录组合×4当前日×16来源掩码×2联合域×2收益端口覆盖，共16384请求。直接按生成参数对账、用原feasible行动枚举对照全组，逐次执行0/1预算，核对终点及局部，预测资格切换不得改变计算状态。错误基线将历史预测金额额外加到现金后计算，统计存在错误放行情景次数（已获账本资格的请求×已知情景，重复非独立）。12控制，含撤回、更正、时间、资格及旧epoch。两路径同一研究者、共享合同，不是独立验收。无真人、个人数据、真实训练、原生API、设备测量、CI请求、PR合并、部署、费用或冻结变化。
## v0.7接口差距与候选对接（不授权开发）
1. decision_language.interpret、ConversationHub.confirm/_project：保留真实原文义务与确认；R100规则只可作为研究适配或有限用例，不能替换开放语义。知识检索的候选、事实资格和方法准备仍须分层；本轮未连接原生检索或开放语义。
2. decision_resources.ResourceState/evaluate_resources与decision_records保存复用：实际余额来源、日期及授权；近期现金义务并集、期限延展和持续收益门槛均需明确规范身份、时域及共同日程假设。不能以独立方案资源检查充当跨计划联合可行。
3. decision_candidates.CandidateRegistry/ResearchCandidate：可承载固定研究源、公式、适用性、反例、基线、复算及missing_admission；describe固定NOT_ADMITTED/NONE。近期数学研究先登记为隔离候选，经独立验证后才讨论原生方法端口。真实科研许可仍需核验。
4. decision_conversation._compute/_view/result_receipt与decision_planner.plan：需独立局部结果、条件情景覆盖、续算进度和当前性，不能将研究正状态升级为ANALYZED/可选择。会话实例身份问题及结果权威隔离已有专项审计，须纳入真实入口回归。
5. 连续残差修正与跨域迁移：须由真实同口径结果记录、独立目标支持、用途许可与后续评价门控制；本轮不将修正值当作收益支持。共享信息成本前沿及竞争假设覆盖属于尚未接入的独立候选。统一接口必须保留各自合同和证据级别，不机械合成。
6. 产品轨仍维护唯一交接；独立轨负责未见原文、全部硬约束、跨轮更新、候选隔离、真实回退、真机及竞争效果。先审#62与最新main差异，后续完整版本由所有者另行授权；不启动零碎Codex任务，不合并或部署。
## 可复算代码
按四份固定资产顺序置入docs全文，Node标准JS，只加载已审查项目自有代码。
```js
function load(docs){
 const code=d=>d.split("```js\n")[1].split("\n```")[0];
 const s=code(docs[0]),A=Function(s.split("function experiment({P,J})")[0]+"\nreturn load;")()(docs.slice(1,3));
 const B=Function("A",s.slice(s.indexOf("function experiment({P,J})")).split(" let o={settings:")[0]+"\nreturn {prepare,advance};\n}\nreturn experiment(A);")(A);
 const L=Function(code(docs[3]).split(" let o={scenarios:")[0]+"\nreturn {parse,ingest,view};\n}\nreturn experiment();")();
 return {...A,B,L}
}
function experiment({P,J,B,L}){
 const ck=(v,m)=>{if(!v)throw Error(m)},W=[0,1,2,3,4,5,6,7],INF="NO_FINITE_THRESHOLD",all=255;
 const event=(id,text,received)=>({id,text,received,qualified:true});
 // Dates 1,2 are expected actual settlement roots, not inferred from forecasts.
 // On missing or withdrawn actual cash, refuse to manufacture a plan.
 function prepare(log,day,opening,active,host,scope,gainMask,fee){
  const fail=status=>({status,authority:"NONE"});
  if(!host.covered||!host.allowed)return fail("UNKNOWN_QUALIFICATION");
  if(host.day!==day)return fail("UNKNOWN_TIME");
  let actual=log.filter(e=>e.received<=day).map(e=>L.parse(e.text)).filter(p=>p&&p.kind==="ACTUAL");
  for(let [root,d] of [["R2",1],["R1",2]])if(day>=d&&!actual.some(p=>p.root===root&&p.day===d))return fail("UNKNOWN_RECONCILIATION");
  let v=L.view(log,day,day,opening,active,true);
  if(v.status!=="CONDITIONAL")return fail(v.status);
  const params=W.map(w=>({cash:v.balance,reserve:1,income:0,ca:1,cb:1,fee:fee+(w&1),busy:1,da:2,db:4,lag:(w&2)?2:1}));
  const gain=W.map(w=>(w&4)?2:0);
  const t=params.map(p=>{let v=P.threshold(p);return v.status==="CONDITIONAL"?v.minimum:INF});
  const state=B.prepare(J.group(t,scope),J.group(gain,scope&gainMask),scope,host.epoch);
  return {status:"PREPARED_RESEARCH",authority:"NONE",balance:v.balance,applied:v.applied,state};
 }
 const o={ledgers:0,requests:0,ready:0,blocked:{},worldChecks:0,initialChecks:0,resumed:0,finalChecks:0,partialGain:0,forecastToggle:0,naiveForecastFalsePass:0,staleChecks:0,controls:0,witness:null};
 for(let predicted of [2,5])for(let actual of [0,3])for(let revised of [0,4])for(let other of [1,4])for(let delay of [2,3])for(let opening of [0,2]){
  let log=[],es=[event("f",`预计R1第2日到账${predicted}美元`,0),event("b",`实际R2第1日到账${other}美元`,1),event("a",`实际R1第2日到账${actual}美元`,delay),event("c",`更正实际R1第2日到账${revised}美元，替代版本1`,4)];
  for(let e of es)ck(L.ingest(log,e)==="ACCEPT","ingest");o.ledgers++;
  for(let day=1;day<=4;day++)for(let mask=0;mask<16;mask++)for(let scope of [255,65])for(let gainMask of [255,85]){
   let active=new Set(es.filter((e,i)=>mask&(1<<i)).map(e=>e.id)),host={covered:true,allowed:true,day,epoch:day},fee=1;
   let s=prepare(log,day,opening,active,host,scope,gainMask,fee);o.requests++;
   let status=day>=2&&day<delay?"UNKNOWN_RECONCILIATION":!active.has("b")||day>=2&&!active.has(day===4?"c":"a")?"UNKNOWN_SOURCE":"PREPARED_RESEARCH";
   ck(s.status===status,"ledger qualification");
   if(status!=="PREPARED_RESEARCH"){ck(!Object.hasOwn(s,"state")&&!Object.hasOwn(s,"balance"),"no unsafe state");o.blocked[status]=(o.blocked[status]||0)+1;continue}
   o.ready++;let balance=opening+other+(day>=2?(day===4?revised:actual):0);ck(s.balance===balance,"balance");
   let toggle=new Set(active);active.has("f")?toggle.delete("f"):toggle.add("f");
   let alt=prepare(log,day,opening,toggle,host,scope,gainMask,fee);
   ck(JSON.stringify(s.state)===JSON.stringify(alt.state),"forecast separation");o.forecastToggle++;
   let pass=0,fail=0,missing=scope&~gainMask;
   for(let w of W)if(scope&gainMask&(1<<w)){
    let p={cash:balance,reserve:1,income:0,ca:1,cb:1,fee:fee+(w&1),busy:1,da:2,db:4,lag:(w&2)?2:1},gain=(w&4)?2:0;
    let v=P.feasible(p,gain);if(v)pass|=1<<w;else fail|=1<<w;
    let naive=P.feasible({...p,cash:balance+predicted},gain);if(naive&&!v){o.naiveForecastFalsePass++;o.witness??={day,balance,predicted,w,gain,p}}
    o.worldChecks++;
   }
   let q=B.advance(s.state,0,host.epoch);ck(q.pending===(scope&gainMask)&&q.missing===missing&&q.conclusion==="UNKNOWN_GLOBAL","zero budget");o.initialChecks++;
   while(q.pending){
    q=B.advance(s.state,1,host.epoch);ck((q.pass&pass)===q.pass&&(q.fail&fail)===q.fail,"partial");o.resumed++;
   }
   ck(q.pass===pass&&q.fail===fail&&q.missing===missing,"final oracle");o.finalChecks++;o.partialGain+=+(missing!==0);
   let cursor=s.state.cursor;ck(B.advance(s.state,1,host.epoch+1).status==="STALE_OR_INVALID"&&s.state.cursor===cursor,"stale");o.staleChecks++;
  }
 }
 let log=[];for(let e of [event("b","实际R2第1日到账1美元",1),event("a","实际R1第2日到账3美元",2),event("c","更正实际R1第2日到账0美元，替代版本1",4)])ck(L.ingest(log,e)==="ACCEPT","control ingest");
 let h={day:4,epoch:4,allowed:true,covered:true},act=new Set(["a","b","c"]),s=prepare(log,4,0,act,h,all,all,1);
 for(let v of [o.ledgers===64,o.requests===16384,o.ready+Object.values(o.blocked).reduce((a,b)=>a+b,0)===o.requests,o.ready===o.finalChecks,o.naiveForecastFalsePass>0,s.balance===1,prepare(log,4,0,new Set(["a","b"]),h,all,all,1).status==="UNKNOWN_SOURCE",prepare(log,4,0,act,{...h,allowed:false},all,all,1).status==="UNKNOWN_QUALIFICATION",prepare(log,4,0,act,{...h,covered:false},all,all,1).status==="UNKNOWN_QUALIFICATION",prepare(log,3,0,act,h,all,all,1).status==="UNKNOWN_TIME",B.advance(s.state,1,5).status==="STALE_OR_INVALID",s.state.cursor===0]){ck(v,"control "+o.controls);o.controls++}
 return o;
}
console.log(JSON.stringify(experiment(load(docs)),null,2));
```
## 实测
```json
{
  "ledgers": 64,
  "requests": 16384,
  "ready": 4608,
  "blocked": {
    "UNKNOWN_SOURCE": 9728,
    "UNKNOWN_RECONCILIATION": 2048
  },
  "worldChecks": 18432,
  "initialChecks": 4608,
  "resumed": 10144,
  "finalChecks": 4608,
  "partialGain": 1152,
  "forecastToggle": 4608,
  "naiveForecastFalsePass": 4776,
  "staleChecks": 4608,
  "controls": 12,
  "witness": {
    "day": 1,
    "balance": 1,
    "predicted": 2,
    "w": 4,
    "gain": 2,
    "p": {
      "cash": 1,
      "reserve": 1,
      "income": 0,
      "ca": 1,
      "cb": 1,
      "fee": 1,
      "busy": 1,
      "da": 2,
      "db": 4,
      "lag": 1
    }
  }
}
```
