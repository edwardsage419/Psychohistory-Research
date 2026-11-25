# 自主认知专项累计第122轮候选：有成本的信息获取与共享现金时间硬约束
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / BOUNDED_COSTED_INFORMATION / SYNTHETIC_FIXTURE / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 35e200a42cd947f14c929ea44c3a54707db63154。核对近12提交、13开放PR（#61待审）、v3.2前15行及历史全文、唯一交接前18行、R121前20行及实际代码、R40/R47前16行、R100前14行及实际代码。R40研究同尺度问询损失、R47计算预算、R121无成本观察、R100双时间现金；本轮新增真实占位的模拟调查成本与现金硬门的具体连接。没有把现金、工时或用户价值相加。
## 固定资产
research/decision_hub/2026-11-25-correlated-workload-observation-scheduling.md 227daac97ef9bc28b62d0c5f3087602a05e0cb8b
research/decision_hub/2026-11-25-contiguous-task-window-feasibility.md 089e7d446004f5303a26a6de25ff328fc857295e
research/decision_hub/2026-11-25-anchored-deadline-shared-time-feasibility.md e5a2b2921d9c810b82a1e449200b17caf987cf7d
research/decision_hub/2026-11-25-civil-temporal-anchor-version-replay.md cc9f6c6103e4ac863d2cdaa6961721149fd4189a
research/decision_hub/2026-11-25-temporal-quantity-candidate-separation.md 8a6b42f83b80283db6e215fe48f4fb2efbf8368c
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
research/decision_hub/2026-11-25-semantic-resource-ledger-temporal-bridge.md 65008b82d4720e931c99bd66ed03228b1f8ef69e
R40 56b1885f277b70797974ad48e80884a2d99dde81；R47 d99676bf1241e852a7c035fe092f1eabbf124c7e；唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07。所有为项目原创合成资料，无真实个人信息、交易、日历或新外部数据。
## 合同与算法
沿R121四日、两个布局、A连续确定、B连续及C可拆且相关工时支持。比较不调查（无观察）、免费即时完整信息（反事实诊断）、调查占用第1日或第2日最早可用一单位时段且在剩余第2日任务之前取得完整观察。若该日无可用时段则该调查方式不可实施；不假定可在其他时段完成，不处理调查失败、误差、延迟跨日、多次调查或真实信息来源。已知固定调查槽从位图删除，重算每日容量，复用R121 evaluate/reference及其下游R120求解器、R119日期投影、R118锚定；所有共同早期动作与观察分支须重新满足约束。缩减资源不可能改善免费信息可行域；成本后可能失去原有保证。调查时间是独立确定的工作量，不能自动与任务共享。没有额外现金成本的任务、跨期现金流支出账本或延期罚金；现金用于单次模拟调查费用，费用时点由外部固定为账本第1日（早于两种调查的剩余任务执行；抽象账本编号与日历日期未建立真实时区映射）。调用R100 ingest/view实际解析到账与未来预测，当前已知实际金额0/2/4美元、未来预测3美元、费用0/1/2美元、最低余额0/2美元。资格/覆盖和购买权限由研究者夹具提供，不是真实授权。现金不足或调查槽缺失不执行；未知资格/余额保持UNKNOWN。支付后余额只用于硬门，不写入真实支出；未来预测不得当作可支用现金。可行保证只针对已设有限合同。无概率、实际收益或完整用户价值排序；若不调查已保证，仍可因调查增加信息价值，但本轮不估计。全部authority NONE。预算沿固定小域，未做全请求资源或真机验证。
## 实验
复用R121的2880场景及原始免费信息结果；两个调查日期分别检查，存在调查时段则重算并与R121 reference对照；每个方案×3实际现金×3费用×2储备=103680个现金时间联合判断。独立现金参考为已知实际金额直接减费与底线比较；调度参照沿原R121共享最大需求定理及R120直接枚举，两路径同研究者，非独立验收。timeCostDestroysFreeGuarantee包含调查槽缺失，具体witness优先记录实际扣减槽导致失去保证的案例；baselineViablePaidFails仅在不调查且当前余额满足储备时计数。forecastFalseCashPass仅计真实现金不足但错误计入未来预测会通过现金门且调查时段策略保证的组合；非现实错误率。所有计数非独立人次、现实概率、经济效用或真实花费。13专项控制。研究者选择费用、工时、支持、观察和资源合同，未实现自动白话、真实证据资格、支付、原生C028、生产部署或设备。无训练、Codex、CI、PR合并、部署、费用或冻结变化。产品轨维护唯一交接。
## 复算
按上述七文件顺序置入docs[i].content，Node标准JS，仅执行审查过的项目自有源码。
```js
function load(docs){
 const code=i=>docs[i].content.split("```js\n")[1].split("\n```")[0],c=code(0);
 const {P,S}=Function(c.split("function experiment(P,S)")[0]+"\nreturn load;")()(docs.slice(1,6));
 const E=Function("P","S",c.slice(c.indexOf("function experiment(P,S)")).split(" let out={cases:")[0]+"\nreturn {evaluate,reference};\n}\nreturn experiment(P,S);")(P,S);
 const L=Function(code(6).split(" let o={scenarios:")[0]+"\nreturn {ingest,view};\n}\nreturn experiment();")();
 return {P,S,E,L}
}
function experiment(P,S,E,L){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),pop=x=>{let n=0;for(;x;x&=x-1)n++;return n};
 // Payment is required at time 1. Forecast is future, never spendable.
 function ledger(actual,predicted,active=true,covered=true){
  let log=[];for(let e of [{id:"f",text:`预计R1第2日到账${predicted}美元`,received:0,qualified:true},{id:"b",text:`实际R2第1日到账${actual}美元`,received:1,qualified:true}])ck(L.ingest(log,e)==="ACCEPT","ingest");
  return L.view(log,1,1,0,new Set(active?["f","b"]:["f"]),covered)
 }
 function reduce(req,available,spent){
  if((spent&available)!==spent)return null;
  let mask=available&~spent;
  return {req:{...req,capacity:Array.from({length:4},(_,i)=>pop((mask>>(3*i))&7))},mask}
 }
 const guaranteed=z=>z.status==="GUARANTEED_IN_DOMAIN";
 // Purchase choice: no investigation, free ideal information (diagnostic),
 // or one unit of day-1/day-2 capacity consumed before remaining day-2 work.
 // One fixed earliest available slot of the nominated day, not an arbitrary later slot.
 function costed(req,available,support,day){
  let availDay=(available>>(3*day))&7;
  if(!availDay)return {status:"NO_INVESTIGATION_SLOT",authority:"NONE"};
  let spent=(availDay&-availDay)<<(3*day),r=reduce(req,available,spent);
  let z=E.evaluate(r.req,r.mask,support,"full"),o=E.reference(r.req,r.mask,support,"full");
  ck(eq(z.safe.map(x=>x.day0).sort((a,b)=>a-b),o.safe)&&eq(z.possible.map(x=>x.ok),o.possible),"costed oracle");
  return {status:z.status,spent,remaining:r.mask,safe:z.safe,authority:"NONE"}
 }
 function qualify(z,v,fee,reserve,allowed){
  if(!allowed||v.status!=="CONDITIONAL"||!Number.isInteger(fee)||fee<0||!Number.isInteger(reserve)||reserve<0)return "UNKNOWN";
  if(v.balance-fee<reserve)return "CASH_BLOCKED";
  if(z.status==="NO_INVESTIGATION_SLOT")return "TIME_BLOCKED";
  if(z.status==="GUARANTEED_IN_DOMAIN")return "GUARANTEED_IN_DOMAIN";
  return "NOT_GUARANTEED";
 }
 const out={cases:0,scheduleChecks:0,investigationSlotAbsent:0,freeInfoGuaranteed:0,baselineGuaranteed:0,freeInfoRescue:0,timeCostDestroysFreeGuarantee:0,timeCostDestroysBaselineGuarantee:0,timeCostRescue:0,paidChecks:0,cashBlocked:0,timeBlocked:0,notGuaranteed:0,paidGuaranteed:0,unknown:0,forecastFalseCashPass:0,paidRescue:0,baselineViablePaidFails:0,controls:0,witnesses:{}};
 // Each paid comparison uses same underlying baseline with reserve applied.
 // Research-only finite fee/reserve variants, no actual financial transactions.
 for(let cap of P.caps)for(let frag of [false,true])for(let ha of [1,2])for(let ar of [0,1])for(let a of [P.ra,P.ra2]){
  let req={covered:true,capacity:cap,records:[P.record(a,ha,ar),P.record(P.rb2,1,1),P.record(P.rc,1,1)]},available=S.calendar(cap,frag);
  for(let m=1;m<16;m++){
   let support=[0,1,2,3].filter(i=>m&(1<<i)),base=E.evaluate(req,available,support,"none"),free=E.evaluate(req,available,support,"full");
   out.cases++;let b=guaranteed(base),f=guaranteed(free);out.baselineGuaranteed+=+b;out.freeInfoGuaranteed+=+f;out.freeInfoRescue+=+(!b&&f);
   for(let day of [0,1]){
    let z=costed(req,available,support,day),g=guaranteed(z);
    if(z.status==="NO_INVESTIGATION_SLOT")out.investigationSlotAbsent++;else out.scheduleChecks++;
    ck(!g||f,"resource monotonicity");
    if(f&&!g){out.timeCostDestroysFreeGuarantee++;if(z.spent)out.witnesses.timeCost??={cap,frag,ha,ar,deadline:a.receipt.value.date,support,day,spent:z.spent,base:base.status,free:free.status,costed:z.status}}
    if(b&&!g)out.timeCostDestroysBaselineGuarantee++;
    if(!b&&g){out.timeCostRescue++;out.witnesses.rescue??={cap,frag,ha,ar,deadline:a.receipt.value.date,support,day,spent:z.spent,base:base.status,costed:z.status}}
    for(let actual of [0,2,4])for(let fee of [0,1,2])for(let reserve of [0,2]){
     let v=ledger(actual,3),q=qualify(z,v,fee,reserve,true);
     ck(v.status==="CONDITIONAL"&&v.balance===actual,"actual cash");
     let expected=actual-fee<reserve?"CASH_BLOCKED":z.status==="NO_INVESTIGATION_SLOT"?"TIME_BLOCKED":g?"GUARANTEED_IN_DOMAIN":"NOT_GUARANTEED";
     ck(q===expected,"cash gate");out.paidChecks++;
     if(q==="CASH_BLOCKED"){out.cashBlocked++;if(actual+3-fee>=reserve&&g){out.forecastFalseCashPass++;out.witnesses.forecast??={actual,forecast:3,fee,reserve,schedule:z.status}}}
     else if(q==="TIME_BLOCKED")out.timeBlocked++;else if(q==="NOT_GUARANTEED")out.notGuaranteed++;else if(q==="GUARANTEED_IN_DOMAIN"){out.paidGuaranteed++;if(!b)out.paidRescue++}else out.unknown++;
     if(b&&actual>=reserve&&q!=="GUARANTEED_IN_DOMAIN")out.baselineViablePaidFails++;
    }
   }
  }
 }
 let z={status:"GUARANTEED_IN_DOMAIN"},v=ledger(4,3);
 for(let t of [()=>out.cases===2880,()=>out.paidChecks===103680,()=>out.scheduleChecks+out.investigationSlotAbsent===out.cases*2,()=>out.cashBlocked+out.timeBlocked+out.notGuaranteed+out.paidGuaranteed+out.unknown===out.paidChecks,()=>out.freeInfoRescue===32,()=>out.timeCostDestroysFreeGuarantee>0,()=>qualify(z,ledger(4,3,false),1,0,true)==="UNKNOWN",()=>qualify(z,ledger(4,3,true,false),1,0,true)==="UNKNOWN",()=>qualify(z,v,1,0,false)==="UNKNOWN",()=>qualify(z,v,-1,0,true)==="UNKNOWN",()=>qualify(z,v,3,2,true)==="CASH_BLOCKED",()=>qualify(z,v,2,2,true)==="GUARANTEED_IN_DOMAIN",()=>qualify({status:"NO_INVESTIGATION_SLOT"},v,1,0,true)==="TIME_BLOCKED"]){ck(t(),"control "+out.controls);out.controls++}
 return out
}
const {P,S,E,L}=load(docs);console.log(JSON.stringify(experiment(P,S,E,L),null,2));
```
## 实测
```json
{
  "cases": 2880,
  "scheduleChecks": 3600,
  "investigationSlotAbsent": 2160,
  "freeInfoGuaranteed": 281,
  "baselineGuaranteed": 249,
  "freeInfoRescue": 32,
  "timeCostDestroysFreeGuarantee": 402,
  "timeCostDestroysBaselineGuarantee": 342,
  "timeCostRescue": 4,
  "paidChecks": 103680,
  "cashBlocked": 40320,
  "timeBlocked": 23760,
  "notGuaranteed": 37840,
  "paidGuaranteed": 1760,
  "unknown": 0,
  "forecastFalseCashPass": 960,
  "paidRescue": 44,
  "baselineViablePaidFails": 5754,
  "controls": 13,
  "witnesses": {
    "forecast": {
      "actual": 0,
      "forecast": 3,
      "fee": 0,
      "reserve": 2,
      "schedule": "GUARANTEED_IN_DOMAIN"
    },
    "timeCost": {
      "cap": [
        1,
        1,
        1,
        1
      ],
      "frag": false,
      "ha": 1,
      "ar": 0,
      "deadline": "2026-11-25",
      "support": [
        1
      ],
      "day": 0,
      "spent": 1,
      "base": "GUARANTEED_IN_DOMAIN",
      "free": "GUARANTEED_IN_DOMAIN",
      "costed": "NO_FEASIBLE_WORLD"
    },
    "rescue": {
      "cap": [
        2,
        1,
        1,
        2
      ],
      "frag": false,
      "ha": 1,
      "ar": 1,
      "deadline": "2026-11-25",
      "support": [
        1,
        2
      ],
      "day": 0,
      "spent": 1,
      "base": "POSSIBLE_NOT_GUARANTEED",
      "costed": "GUARANTEED_IN_DOMAIN"
    }
  }
}
```
下一步：对真实信息资格、可延迟行动、失败信号、收益与多维成本进行独立研究，避免把无保证误当作必然失败。正式开发与训练另获授权。
