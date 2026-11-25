# 自主认知专项累计第110轮候选：用途资格与稳健个人规划的分层连接
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / SYNTHETIC_DEVELOPMENT / NATIVE_PLATFORM_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main c19b8065a04cf7e742696a398db190d360976324。核对近12提交、13开放PR（#61待审）、v3.2前15行及历史全文、唯一交接前25行、R109前20行、R108前15行、R101全文、R100/R99源码及R18实际源码配置。增量为独立许可下可用的稳健规划与个性化附加比较；不重复R101完整时间账本实验、R108 SQLite或R109历史查看全掩码实验。
## 固定资产
research/decision_hub/2026-11-24-feedback-replay-and-rollback/probe.js c07a499cfc0d3ab274fcb0a6e16abe71fab1f3f6
research/decision_hub/2026-11-24-feedback-replay-and-rollback/config.json fb4ec1cee38443c41d9f3fb7e90f616dafe78832
research/decision_hub/2026-11-25-semantic-resource-ledger-temporal-bridge.md 65008b82d4720e931c99bd66ed03228b1f8ef69e
research/decision_hub/2026-11-25-complementarity-realization-timing.md a1ea992561b43252c99e882494640b290a8fa5a4
R101 907f12081ddce7bb752ae498bcf21f4b4b218a60；R108 75deb196da9b81a4d872ac29187101235194ac1c；R109 5d2695da1f5a380369714adb5dd6fe0a5cdaa8db；唯一交接 5e74f4f0b37141d631740e844ad8bbbfed232e07。
## 合同与边界
R108恢复资格仅通过人工可信锚点及可用ID掩码模拟，未执行其SQLite或SHA256核验器；真实版本必须绑定内容、修订、主体、用途、授权代次及可信防回滚锚点。宿主已明确当前日4、两个到期实际根的确切最新记录b/c、已确认范围及期初余额；无锚点/缺任一最新记录/重复记录，保留未知，不从旧a或预测f补足。只把b/c当前合格载荷交给R100 view；不重新执行其ingest或全版本链核验，假定当前根清单及原始载荷已获资格，未模拟伪造可信载荷。过滤之前的完整合成备份仍在内存，本实验不证明真实数据最小驻留、擦除或隐私安全。R99 dp固定两现金未来情景0/4、4期开放环共同路径；按独立oracle枚举256序列核验两个终点组。现有规划仅使用合格实际余额，未来情景不能计入当前现金。无概率也保持稳健计划；无真实资源、真实用户计划或原生App。
R18 apply构造两版本各8种三次二元反馈序列；R109用途思想简化为每个事件p/y作为不可拆分授权对。learn掩码允许本地学习，use掩码独立允许同一对数据用于当前规划。用原weights及brute从均匀权重重放选定事件，保留原接收顺序。若learn非空且所有被使用的反馈对同时具备规划用途资格，才允许附加个性化比较；否则只保留不依赖反馈的稳健组，不自动改变学习集合。不同用途可独立授权，无真实授权及跨代次事务。两个未来专家预测概率0.2/0.8为人工假定，明确代表同一个未来二元培训到账情景的高收益概率；其合法来源、迁移及校准完全未证，本实验不得将组合概率解释为真实事件概率。假定该未来专家向量及使用范围独立获准且不依赖旧个人数据，真实模型需完整依赖核验。附加比较只在两个情景共同可行的已培训终点组内，以该假定概率加权终点现金进行条件性最大化；不与无培训路径比较、不构造总体效用、不称最佳人生选择。终点组不是实际执行序列，未处理用户其他偏好。比较使用同一研究者编写的排序和浮点容差1e-10，两路径共享目标公式，非独立数学验收。无反馈时不自动采用无证据概率。重放不修改历史预测；原状态留存仅合成实验。未训练新模型、未测试真实个性化效果、性能或隐私。DP按两种合格余额缓存，仅两次实际DP与oracle，不能把重复请求数当成独立DP运行量。
## 实验
2版本×8结果组合×8学习掩码×8规划用途掩码×8到账记录掩码×2锚点状态×2期初余额=32768请求。掩码故意含大量拒绝情景；统计非实际发生率。naivePurposeViolations计非空学习状态却不满足规划用途的已知余额请求，即盲用学习状态的反例；并不代表实际平台泄露。原R18路径枚举与R99直接序列oracle核对，非独立留出。研究者选择了保守用途隔离及终点现金排序，尚未确定产品政策。合成材料为ChatGPT辅助研发原创开发夹具，非真人、训练或独立留出。无新增外部事实、费用、训练、Codex、CI、生产修改、PR合并、部署或冻结变更。
## 复算
将上述四份固定自有源码分别置于docs[i].content；仅加载已审查项目代码，禁止执行任意外部文档内容。Node标准JS。
```js
function loadFeedback(src){return Function(src.replace("const config=require('./config.json');","").split("console.log(JSON.stringify(run(config)")[0]+"\nreturn {initial,apply,weights,brute,canon};")()}
function loadReport(text,names){let src=text.split("```js\n")[1].split("\n```")[0].split(" let o={scenarios:")[0];return Function(src+"\nreturn {"+names+"};\n}\nreturn experiment();")()}
const R=loadFeedback(docs[0].content),cfg=JSON.parse(docs[1].content),L=loadReport(docs[2].content,"parse,ingest,view"),P=loadReport(docs[3].content,"dp,oracle,pack");
function experiment(R,cfg,L,P){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const ps=[[.8,.25],[.3,.75],[.65,.4]],future=[.2,.8];
 function original(version,bits){
  let s=R.initial(),t=0;
  function send(e,owner=false){let z=R.apply(s,{...e,generation:s.generation},++t,cfg,owner);ck(["GRANTED","ACCEPTED"].includes(z.code),"apply "+z.code);s=z.s}
  send({id:"grant",type:"grant"},true);send({id:"activate",type:"activate",version},true);
  for(let i=0;i<3;i++){let event="e"+i,due=t+2;
   send({id:"i"+i,type:"issue",epoch:s.epoch,scope:cfg.scope,event,due,p:ps[i]});
   send({id:"f"+i,type:"feedback",epoch:s.epoch,scope:cfg.scope,event,revision:1,priorRevision:0,observed:due,y:(bits>>i)&1});
  }return s
 }
 function replay(s,learn){
  let obs=s.observations.filter((_,i)=>learn&(1<<i)),ids=new Set(obs.map(x=>x.event));
  let x={...s,observations:obs,receipts:s.receipts.filter(f=>ids.has(f.event))};
  let w=R.weights(x,cfg),b=R.brute(x,cfg);return {w,b}
 }
 // Current trusted metadata declares exact latest record IDs. Never pass
 // withdrawn payloads, historical superseded values or forecasts to view.
 function ledger(backup,mask,anchor,opening){
  if(!anchor)return {status:"UNKNOWN_QUALIFICATION"};
  const required=["b","c"];
  const eligible=required.filter((_,i)=>mask&(1<<i));
  if(eligible.length!==required.length)return {status:"UNKNOWN_SOURCE"};
  const rows=backup.filter(e=>eligible.includes(e.id));
  if(rows.length!==2||!required.every(id=>rows.filter(e=>e.id===id).length===1))return {status:"UNKNOWN_SOURCE"};
  const v=L.view(rows,4,4,opening,new Set(eligible));
  return v
 }
 function ranking(groups,p){
  let a=groups.map(([key])=>{let x=key.split(",").map(Number);return {key,v:(1-p)*x[0]+p*x[4]}});
  let max=Math.max(...a.map(x=>x.v));return a.filter(x=>Math.abs(x.v-max)<1e-10).map(x=>x.key).sort()
 }
 let out={requests:0,known:0,unknownSource:0,unknownAnchor:0,robustGroups:0,oracleSequenceChecks:0,robustTrainingFeasible:0,robustOldFeasible:0,replayChecks:0,maxError:0,optionalRanked:0,optionalDenied:0,optionalNoFeasible:0,naivePurposeViolations:0,robustWithoutPersonalization:0,rankingChecks:0,controls:0,example:null};
 // cache deterministic planning only by eligible current realized balance.
 const cache=new Map();
 function plan(cash){
  if(cache.has(cash))return cache.get(cash);
  const p={cash,hours:4,income:0,reserve:0,finish:2,cost:1};
  const v=P.dp(p,[0,4]),q=P.oracle(p,[0,4]);ck(v.status==="CONDITIONAL","dp");
  const tr=P.pack(v.trained),old=P.pack(v.old),rt=P.pack(q.trained),ro=P.pack(q.old);
  ck(eq(tr,rt)&&eq(old,ro),"oracle");out.robustGroups+=2;out.oracleSequenceChecks+=256;
  let z={tr,old,rt,ro};cache.set(cash,z);return z
 }
 for(let version of Object.keys(cfg.versions))for(let bits=0;bits<8;bits++){
  let s=original(version,bits),old=R.canon(s);
  for(let learn=0;learn<8;learn++){
   let {w,b}=replay(s,learn),err=Math.max(...w.map((v,i)=>Math.abs(v-b[i])));ck(err<1e-12,"replay");out.replayChecks++;out.maxError=Math.max(out.maxError,err);
   let prob=w[0]*future[0]+w[1]*future[1],refProb=b[0]*future[0]+b[1]*future[1];
   for(let use=0;use<8;use++)for(let mask=0;mask<8;mask++)for(let anchor of [false,true])for(let opening of [0,2]){
    // Third mask bit concerns old actual a; it is never a substitute for c.
    let backup=[{id:"f",text:"预计R1第2日到账5美元",received:0},{id:"b",text:"实际R2第1日到账1美元",received:1},{id:"a",text:"实际R1第2日到账3美元",received:2},{id:"c",text:"更正实际R1第2日到账4美元，替代版本1",received:4}];
    let v=ledger(backup,mask,anchor,opening);out.requests++;
    if(!anchor){ck(v.status==="UNKNOWN_QUALIFICATION","anchor");out.unknownAnchor++;continue}
    if((mask&3)!==3){ck(v.status==="UNKNOWN_SOURCE","missing");out.unknownSource++;continue}
    ck(v.status==="CONDITIONAL"&&v.balance===opening+5&&eq(v.applied,["b","c"])&&!v.forecasts.length,"ledger");out.known++;
    let z=plan(v.balance);out.robustTrainingFeasible+=+!!z.tr.length;out.robustOldFeasible+=+!!z.old.length;
    let allowed=learn!==0&&(learn&use)===learn;
    // Rank only within robust feasible trained terminal groups, no utility
    // aggregation or preference between training and no training.
    if(!allowed){out.optionalDenied++;if(z.tr.length)out.robustWithoutPersonalization++;if(learn)out.naivePurposeViolations++;continue}
    if(!z.tr.length){out.optionalNoFeasible++;continue}
    let rank=ranking(z.tr,prob),expected=ranking(z.rt,refProb);ck(eq(rank,expected)&&rank.every(k=>z.tr.some(x=>x[0]===k)),"rank");
    out.optionalRanked++;out.rankingChecks++;
    if(!out.example&&learn===6&&use===6)out.example={version,bits,learn,use,mask,opening,cash:v.balance,prob,robustGroups:z.tr.length,rank}
   }
   ck(R.canon(s)===old,"history unchanged")
  }
 }
 let v=ledger([{id:"a",text:"实际R1第2日到账3美元",received:2}],7,true,0);ck(v.status==="UNKNOWN_SOURCE","no fallback");out.controls++;
 ck(ledger([],7,false,0).status==="UNKNOWN_QUALIFICATION","no anchor");out.controls++;
 ck(ledger([{id:"b",text:"实际R2第1日到账1美元",received:1},{id:"c",text:"更正实际R1第2日到账4美元，替代版本1",received:4},{id:"c",text:"更正实际R1第2日到账4美元，替代版本1",received:4}],7,true,0).status==="UNKNOWN_SOURCE","duplicate");out.controls++;
 ck(out.requests===32768&&out.known+out.unknownSource+out.unknownAnchor===out.requests,"coverage");out.controls++;
 ck(out.optionalRanked+out.optionalDenied+out.optionalNoFeasible===out.known,"partition");out.controls++;
 ck(out.replayChecks===128&&out.rankingChecks===out.optionalRanked,"counts");out.controls++;
 ck(out.robustWithoutPersonalization>0&&out.naivePurposeViolations>0,"separation");out.controls++;
 return out
}
console.log(JSON.stringify(experiment(R,cfg,L,P),null,2));
```
## 实测
```json
{
  "requests": 32768,
  "known": 4096,
  "unknownSource": 12288,
  "unknownAnchor": 16384,
  "robustGroups": 4,
  "oracleSequenceChecks": 512,
  "robustTrainingFeasible": 4096,
  "robustOldFeasible": 4096,
  "replayChecks": 128,
  "maxError": 2.220446049250313e-16,
  "optionalRanked": 1216,
  "optionalDenied": 2880,
  "optionalNoFeasible": 0,
  "naivePurposeViolations": 2368,
  "robustWithoutPersonalization": 2880,
  "rankingChecks": 1216,
  "controls": 7,
  "example": {
    "version": "v1",
    "bits": 0,
    "learn": 6,
    "use": 6,
    "mask": 3,
    "opening": 0,
    "cash": 5,
    "prob": 0.45038065522620907,
    "robustGroups": 3,
    "rank": [
      "2,0,1,2,6,0,1,2"
    ]
  }
}
```
后续：优先将目前真实研究代码接口集中形成跨模块候选合同、覆盖清单及独立验证边界；授权正式工程前不启动训练或版本开发。产品轨维护唯一交接。
