# 自主认知专项累计第124轮候选：已实现成本与未来增量再规划
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / REALIZED_COST_REPLANNING / SYNTHETIC_FIXTURE / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 15e1e1409464183290fa57b296ae453d8f13a741。核对近12提交、13开放PR（#61待审）、v3.2前15行及历史全文、唯一交接前18行、R123前20行、R98前16行、R100前14行。R98已有旧承诺取消及前沿；R100只有到账，R122/R123有调查前费用及失败；本轮新增调查后已实现付款/退款与剩余资源状态、历史不同但当前状态相同的配对不变性及后续再调查边界。实际复用R122现金账本及R120/R119/R118调度，未调用R123 policy函数或重做R98取消DP。
## 固定资产
research/decision_hub/2026-11-25-costed-information-time-cash-feasibility.md e828e2cb88fcc9d1fc4825908f27b7684fdb31b1
research/decision_hub/2026-11-25-correlated-workload-observation-scheduling.md 227daac97ef9bc28b62d0c5f3087602a05e0cb8b
research/decision_hub/2026-11-25-contiguous-task-window-feasibility.md 089e7d446004f5303a26a6de25ff328fc857295e
research/decision_hub/2026-11-25-anchored-deadline-shared-time-feasibility.md e5a2b2921d9c810b82a1e449200b17caf987cf7d
research/decision_hub/2026-11-25-civil-temporal-anchor-version-replay.md cc9f6c6103e4ac863d2cdaa6961721149fd4189a
research/decision_hub/2026-11-25-temporal-quantity-candidate-separation.md 8a6b42f83b80283db6e215fe48f4fb2efbf8368c
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
research/decision_hub/2026-11-25-semantic-resource-ledger-temporal-bridge.md 65008b82d4720e931c99bd66ed03228b1f8ef69e
R123 a5c9bd9dcfd5955d7487ab60e928d7626273b415；R98 db648df87860bcb00037c8dddb3a2bc85d8aee28；唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07。均为原创合成开发资料，无真实日程、交易或个人信息。
## 合同
第一日已完成一小时调查并支付费用，第二日开始观察到失败，所有世界仍可能。先前调查占第一日最早可用槽；A若已完成，必须存在与调查不重叠的合法连续块且已释放，完成与否为宿主给定的合成实际状态；不从可行性推断实际完成。所有第一日时段均已过去，不得重用。第二日至第四日A剩余确定、B/C不确定且同原支持；继续原任务、不再调查，或第二日占最早可用一小时再调查且支付未来费用。再调查按时返回完整结果为条件分支，失败仍需共同预约；全保证要求两个分支均可行。无真实概率、延迟再调查、多次重试、任务取消/退款请求、放弃强制义务或价值排序。停止调查仍保留所有必需任务。若真实计划取消带来未来赔偿/实际退款或效用，须单独建模，不将历史成本本身作为续投理由。
R100到账只支持正向到账；本轮另建有限已结算支出/退款投影，不修改其历史合同。R122 ledger实际得到模拟总到账（不含调查退款），独立支付记录及实际退款记录净额一次，当前余额=总到账-已支付+已到账退款；再比较当前余额-未来费与储备。两记录固定身份pay/refund及资格/覆盖为人工夹具，费用不含未来义务，假定退款不超过已支付且支付时资金已到账；未实现完整双时间支出事件、实际签名、退款链、真实授权、账本去重跨系统、实际支付或持久化。预测退款及撤回/缺失记录不得当零或继续使用。当前余额、剩余时间、任务进度与未来资格固定时，不同历史费用或退款不改变当前条件性可行结论；若历史造成当前余额或义务差异，该差异必须保留。所有authority NONE。
## 算法及实验
实际R119 project验证锚定日期；R120 placements确认第一日完成状态有可行见证，R120 solve与validate求未来共同最大需求或逐世界预约；直接R120 oracle复算。二者同研究者且共享R121最大需求定理，非独立验收。未来失败分支消耗时间且没有信息，因资源减少，保证再调查蕴含不调查有保证；合成合同中不应存在仅通过可失败再调查恢复保证的情景；不推广到有其他收益的调查。每个时间场景对当前余额1..4、历史付款1/2、实际退款0/1构造16历史（总到账相应调整以固定余额），未来费0/1/2、储备0/2，按同余额比较三个条件决策输出。错误基线分别再次扣已付金额、恢复未退回历史费用、使用已过去的第一日全部时间。错误次数按重复情景组合计，非实际概率或产品错误率。独立现金参照为当前已指定余额减未来费，非真实用户账本。6历史资格负控、11其他控制。研究者指定日网格、支持、费用、退款、任务范围及权限，非产品政策。未做完整预算、设备、真实语言/效果、原生调用或独立验收。无训练、Codex、CI、PR合并、部署、费用或冻结变更。产品轨维护唯一交接。
## 复算
按上述七文件顺序置入docs[i].content，Node标准JS，仅执行已审查自有源码。
```js
function load(docs){
 const c=docs[0].content.split("```js\n")[1].split("\n```")[0];
 const A=Function(c.split("function experiment(P,S,E,L)")[0]+"\nreturn load;")()(docs.slice(1));
 const C=Function("P","S","E","L",c.slice(c.indexOf("function experiment(P,S,E,L)")).split(" const out={cases:")[0]+"\nreturn {ledger,reduce,qualify};\n}\nreturn experiment(P,S,E,L);")(A.P,A.S,A.E,A.L);
 return {...A,C}
}
function experiment(P,S,C){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),W=[[1,1],[1,2],[2,1],[2,2]];
 // Research-only historical cash reconciliation. The income ledger is gross,
 // the separate complete paid/refund record is netted exactly once.
 function snapshot(gross,events,active,covered=true){
  if(!covered||gross.status!=="CONDITIONAL"||!Array.isArray(events)||events.length<1||events.length>2||new Set(events.map(x=>x.id)).size!==events.length)return null;
  let paid=events.find(x=>x.id==="pay"),refund=events.find(x=>x.id==="refund");
  if(!paid||paid.kind!=="PAID"||!Number.isInteger(paid.amount)||paid.amount<0||paid.amount>gross.balance||!paid.qualified||!active.has("pay"))return null;
  if(events.length===2&&!refund)return null;
  if(refund&&(refund.kind!=="ACTUAL_REFUND"||!Number.isInteger(refund.amount)||refund.amount<0||refund.amount>paid.amount||!refund.qualified||!active.has("refund")))return null;
  return {balance:gross.balance-paid.amount+(refund?.amount??0),paid:paid.amount,refund:refund?.amount??0,authority:"NONE"}
 }
 function future(req,available,support,completed,reference=false){
  let plain=P.project(req,P.sources,P.anchors);
  if(!plain||plain.length!==3||!Array.isArray(support)||!support.length||support.some(i=>!Number.isInteger(i)||i<0||i>3)||new Set(support).size!==support.length)return null;
  // All elapsed day 0 capacity is unavailable, regardless of whether used.
  let mask=available&~7;
  const make=ws=>plain.map((j,i)=>({...j,r:Math.max(1,j.r),h:i===0?(completed?0:j.h):Math.max(...ws.map(w=>W[w][i-1])),block:i!==2}));
  function feasible(ws,avail){
   let jobs=make(ws);
   // R120 placements handles zero jobs; all positive windows are in range.
   if(reference)return S.oracle(jobs,avail);
   let z=S.solve(jobs,avail);ck(z.status!=="LIMIT","limit");
   if(z.status==="FEASIBLE")ck(S.validate(z,jobs,avail),"certificate");
   return z.status==="FEASIBLE"
  }
  const base=feasible(support,mask),day=(mask>>3)&7,spent=day?(day&-day)<<3:0;
  const retryMask=mask&~spent;
  const success=!!spent&&support.every(w=>feasible([w],retryMask)),failure=!!spent&&feasible(support,retryMask);
  return {base,success,failure,robust:success&&failure,spent,authority:"NONE"}
 }
 function choose(f,v,fee,reserve,allowed=true){
  if(!f||!v||!allowed||!Number.isInteger(fee)||fee<0||!Number.isInteger(reserve)||reserve<0)return {status:"UNKNOWN",authority:"NONE"};
  const baseCash=v.balance>=reserve,retryCash=v.balance-fee>=reserve;
  return {status:"EVALUATED",noRetry:baseCash&&f.base,retrySuccess:retryCash&&f.success,retryRobust:retryCash&&f.robust,baseCash,retryCash,authority:"NONE"}
 }
 let out={timeCases:0,historyVariants:0,pairedComparisons:0,futureChecks:0,cashChecks:0,noRetry:0,retrySuccess:0,retryRobust:0,conditionalRescue:0,robustRescue:0,doubleChargeFalseReject:0,restoredSunkFalsePass:0,elapsedTimeFalsePass:0,unknownHistoryChecks:0,controls:0,witnesses:{}};
 const active=new Set(["pay","refund"]);
 const histories=[];for(let balance of [1,2,3,4])for(let paid of [1,2])for(let refund of [0,1]){
  let gross=C.ledger(balance+paid-refund,3),events=[{id:"pay",kind:"PAID",amount:paid,qualified:true},...(refund?[{id:"refund",kind:"ACTUAL_REFUND",amount:refund,qualified:true}]:[])],v=snapshot(gross,events,active);
  ck(v&&v.balance===balance,"net");
  histories.push({balance,paid,refund,gross,events,v});
 }
 for(let cap of P.caps)for(let frag of [false,true])for(let ha of [1,2])for(let ar of [0,1])for(let a of [P.ra,P.ra2]){
  let req={covered:true,capacity:cap,records:[P.record(a,ha,ar),P.record(P.rb2,1,1),P.record(P.rc,1,1)]},avail=S.calendar(cap,frag),first=avail&7;
  if(!first)continue;let spent=first&-first,remaining0=first&~spent;
  let plain=P.project(req,P.sources,P.anchors),canComplete=ar===0&&S.placements({...plain[0],block:true},remaining0).some(m=>m!==0);
  for(let completed of canComplete?[false,true]:[false])for(let m=1;m<16;m++){
   let support=[0,1,2,3].filter(i=>m&(1<<i)),f=future(req,avail,support,completed),r=future(req,avail,support,completed,true);
   ck(eq(f,r),"direct reference");out.timeCases++;out.futureChecks++;
   ck(!f.robust||f.base,"failure branch monotonicity");
   // An incorrect plan can use old idle/consumed hours again, only compare
   // cases where the old A was not completed and the real future is infeasible.
   if(!completed&&!f.base){
    let jobs=plain.map((j,i)=>({...j,h:i===0?j.h:Math.max(...support.map(w=>W[w][i-1])),block:i!==2}));
    if(S.solve(jobs,avail).status==="FEASIBLE"){out.elapsedTimeFalsePass++;out.witnesses.elapsed??={cap,frag,ha,ar,support,deadline:a.receipt.value.date}}
   }
   for(let fee of [0,1,2])for(let reserve of [0,2]){
    let seen=new Map();
    for(let h of histories){
     const q=choose(f,h.v,fee,reserve);
     ck(q.noRetry===(h.balance>=reserve&&f.base)&&q.retrySuccess===(h.balance-fee>=reserve&&f.success)&&q.retryRobust===(h.balance-fee>=reserve&&f.robust),"direct cash");
     out.historyVariants++;out.cashChecks++;
     if(seen.has(h.balance)){ck(eq(q,seen.get(h.balance)),"sunk invariance");out.pairedComparisons++}else seen.set(h.balance,q);
     out.noRetry+=+q.noRetry;out.retrySuccess+=+q.retrySuccess;out.retryRobust+=+q.retryRobust;out.conditionalRescue+=+(!q.noRetry&&q.retrySuccess);out.robustRescue+=+(!q.noRetry&&q.retryRobust);
     if(q.retrySuccess&&h.balance-h.paid-fee<reserve){out.doubleChargeFalseReject++;out.witnesses.double??={balance:h.balance,paid:h.paid,refund:h.refund,fee,reserve,future:f}}
     if(!q.retrySuccess&&f.success&&h.balance-fee<reserve&&h.balance+h.paid-h.refund-fee>=reserve){out.restoredSunkFalsePass++;out.witnesses.restore??={balance:h.balance,paid:h.paid,refund:h.refund,fee,reserve,future:f}}
    }
   }
  }
 }
 const h=histories.find(x=>x.refund===1),z={base:true,success:true,robust:true};
 for(let v of [snapshot(h.gross,h.events,new Set(["refund"])),snapshot(h.gross,h.events,new Set(["pay"])),snapshot(h.gross,h.events,active,false),snapshot(h.gross,[h.events[0],h.events[0]],active),snapshot(h.gross,[h.events[0],{...h.events[1],kind:"FORECAST_REFUND"}],active),snapshot(C.ledger(4,3,false),h.events,active)]){
  ck(v===null&&choose(z,v,1,2).status==="UNKNOWN","unknown history");out.unknownHistoryChecks++
 }
 for(let t of [()=>out.timeCases>0,()=>out.pairedComparisons===out.timeCases*6*12,()=>out.cashChecks===out.timeCases*6*16,()=>out.robustRescue===0,()=>out.doubleChargeFalseReject>0,()=>out.restoredSunkFalsePass>0,()=>out.elapsedTimeFalsePass>0,()=>choose(z,h.v,1,2,false).status==="UNKNOWN",()=>choose(z,h.v,-1,2).status==="UNKNOWN",()=>choose(z,h.v,1,-1).status==="UNKNOWN",()=>out.unknownHistoryChecks===6]){ck(t(),"control "+out.controls);out.controls++}
 return out
}
const {P,S,C}=load(docs);console.log(JSON.stringify(experiment(P,S,C),null,2));
```
## 实测
```json
{
  "timeCases": 2160,
  "historyVariants": 207360,
  "pairedComparisons": 155520,
  "futureChecks": 2160,
  "cashChecks": 207360,
  "noRetry": 9576,
  "retrySuccess": 1904,
  "retryRobust": 1632,
  "conditionalRescue": 0,
  "robustRescue": 0,
  "doubleChargeFalseReject": 840,
  "restoredSunkFalsePass": 392,
  "elapsedTimeFalsePass": 111,
  "unknownHistoryChecks": 6,
  "controls": 11,
  "witnesses": {
    "elapsed": {
      "cap": [
        1,
        1,
        1,
        1
      ],
      "frag": false,
      "ha": 1,
      "ar": 0,
      "support": [
        1
      ],
      "deadline": "2026-11-25"
    },
    "double": {
      "balance": 1,
      "paid": 2,
      "refund": 0,
      "fee": 0,
      "reserve": 0,
      "future": {
        "base": true,
        "success": true,
        "failure": true,
        "robust": true,
        "spent": 8,
        "authority": "NONE"
      }
    },
    "restore": {
      "balance": 1,
      "paid": 1,
      "refund": 0,
      "fee": 0,
      "reserve": 2,
      "future": {
        "base": true,
        "success": true,
        "failure": true,
        "robust": true,
        "spent": 8,
        "authority": "NONE"
      }
    }
  }
}
```
下一步：结合实际来源资格与反馈，建立跨决策状态的统一增量修订接口，并审查真实语料中的成本、承诺及已实现结果。正式开发、训练另获授权。
