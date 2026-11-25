# 自主认知专项累计第125轮候选：增量再规划的分层依赖与选择性失效
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / SELECTIVE_REPLANNING_DEPENDENCIES / SYNTHETIC_FIXTURE / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 8e9b08365e93dfa2883c29d3af1e68d6598bdbc5。核对近12提交、13开放PR（#61待审）、v3.2前15行及历史全文、唯一交接前18行、R124前20行与实际源码、R107/R108/R111前段。R107已有发布事务代次、R108真实SQLite恢复实验、R111分支信封，本轮不重做事务或恢复，新增实际R124再规划函数四出口的细粒度依赖、复用及当前资格。未接入原生系统。
## 固定资产
research/decision_hub/2026-11-25-realized-cost-incremental-replanning.md 43edd309981f55ff110de8fb57be0248f9a075df
research/decision_hub/2026-11-25-costed-information-time-cash-feasibility.md e828e2cb88fcc9d1fc4825908f27b7684fdb31b1
research/decision_hub/2026-11-25-correlated-workload-observation-scheduling.md 227daac97ef9bc28b62d0c5f3087602a05e0cb8b
research/decision_hub/2026-11-25-contiguous-task-window-feasibility.md 089e7d446004f5303a26a6de25ff328fc857295e
research/decision_hub/2026-11-25-anchored-deadline-shared-time-feasibility.md e5a2b2921d9c810b82a1e449200b17caf987cf7d
research/decision_hub/2026-11-25-civil-temporal-anchor-version-replay.md cc9f6c6103e4ac863d2cdaa6961721149fd4189a
research/decision_hub/2026-11-25-temporal-quantity-candidate-separation.md 8a6b42f83b80283db6e215fe48f4fb2efbf8368c
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
research/decision_hub/2026-11-25-semantic-resource-ledger-temporal-bridge.md 65008b82d4720e931c99bd66ed03228b1f8ef69e
R107 36b1d776ec4d71ad7f28d27c68feae438a8acb07；R108 75deb196da9b81a4d872ac29187101235194ac1c；R111 177574fed228e81752863c7993527aa2118aeee5；唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07。
## 合同
同一固定虚构主体、目的、模型、原始日期锚点及任务身份，四出口为现金条件余额、时间可行性、无需再调查的联合可行性、再调查成功条件/失败亦可保证的联合可行性。实际R124 snapshot/future/choose、R122 ledger、R119/R118日期校验与R120调度。现金仅使用总到账及已支付，固定无退款夹具；预测到账变化不进入任何数学出口，原始预测记录仍可独立显示，但本轮不输出预测。时间依赖容量、任务完成、期限、联合支持及时间资格；无需再调查依赖现金、时间、储备；再调查另依赖未来费用及其资格。三类单调代次使付款/现金资格、进度/期限/支持/时间资格、费用/费用资格分别失效；任何相关代次变化即拒绝旧出口，即使数值或许可恢复。仅允许可信进程内缓存复用，外部收据须按当前独立输入全量重算，不能凭自报key或JSON认证。缺失来源维持UNKNOWN，独立出口仍可保留，联合出口不得将未知替零。全部authority NONE。研究者选定保守分层，时间出口含有再调查的时间可行性，因此时间更新同时使两个联合出口失效，可能过度重算；无真实用户资格、跨主体隔离、持久化、撤回删除、签名、真实CAS、并发或恢复，R107/R108历史边界不变。时间与现金资格为模拟布尔，完成状态切换是人工更正不是自动任务执行，固定两个容量下已完成A均存在调查后第一日合法块。未定义可执行建议、概率、效用或完整开放语义。
## 实验
两个初始合成状态，9种事件全部长度4序列及共享前缀，逐前缀用缓存候选与独立从头复算核对四出口。参考现金直接减已支付，时间实际R124 reference调用R120逐时段枚举，联合条件直接算术；同研究者且共享模型合同，不是独立验收。缓存命中仅计出口次数，不是运行速度或设备性能；候选原始key依赖固定字段序列，非规范化或认证。naiveStalePayloads计不更新旧出口时内容确实不同的前缀出口，代次变化但结果值相同不计该项；不是产品错误率。7项ABA、11专项控制。费用、资金、时间、支持、代次规则及变更范围为研究者选择，均原创合成资料，非真实个人数据/真人/训练/独立留出。无训练、Codex、CI、原生、PR合并、部署、费用及冻结变化。产品轨维护唯一交接。
## 复算
按上述八文件顺序置入docs[i].content，Node标准JS，仅执行已审查的项目自有源码。
```js
function load(docs){
 const c=docs[0].content.split("```js\n")[1].split("\n```")[0];
 const A=Function(c.split("function experiment(P,S,C)")[0]+"\nreturn load;")()(docs.slice(1));
 const R=Function("P","S","C",c.slice(c.indexOf("function experiment(P,S,C)")).split(" let out={timeCases:")[0]+"\nreturn {snapshot,future,choose};\n}\nreturn experiment(P,S,C);")(A.P,A.S,A.C);
 return {...A,R}
}
function experiment(P,S,C,R){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),copy=x=>JSON.parse(JSON.stringify(x));
 const actions=["PAYMENT","CASH_SOURCE","PROGRESS","DEADLINE","TIME_SOURCE","FEE","FORECAST","SUPPORT","FEE_SOURCE"];
 const initial=(k)=>({cap:k===0?[2,2,2,2]:[2,1,1,2],gross:k===0?4:3,paid:1,forecast:3,completed:false,extended:false,support:[1,2],fee:1,reserve:2,cashOK:true,timeOK:true,feeOK:true,gen:[0,0,0]});
 function transition(s,a){
  let z=copy(s),g=null;
  switch(a){
   case "PAYMENT":z.paid=3-z.paid;g=0;break;
   case "CASH_SOURCE":z.cashOK=!z.cashOK;g=0;break;
   case "PROGRESS":z.completed=!z.completed;g=1;break;
   case "DEADLINE":z.extended=!z.extended;g=1;break;
   case "TIME_SOURCE":z.timeOK=!z.timeOK;g=1;break;
   case "SUPPORT":z.support=z.support.length===2?[0]:[1,2];g=1;break;
   case "FEE":z.fee=2-z.fee; // use two distinct future costs
    if(z.fee===s.fee)z.fee=0;
    g=2;break;
   case "FEE_SOURCE":z.feeOK=!z.feeOK;g=2;break;
   case "FORECAST":z.forecast=z.forecast===3?6:3;break;
  }
  if(g!==null)z.gen[g]++;return z
 }
 const req=s=>({covered:true,capacity:s.cap,records:[P.record(s.extended?P.ra2:P.ra,1,0),P.record(P.rb2,1,1),P.record(P.rc,1,1)]});
 const avail=s=>S.calendar(s.cap,false);
 // Keys bind exact relevant inputs, current scope and relevant generation.
 const key=(s,l)=>JSON.stringify(l==="cash"?[l,s.gen[0],s.gross,s.paid,s.cashOK]:l==="time"?[l,s.gen[1],s.cap,s.completed,s.extended,s.support,s.timeOK]:l==="base"?[l,key(s,"cash"),key(s,"time"),s.reserve]:[l,key(s,"cash"),key(s,"time"),s.gen[2],s.fee,s.reserve,s.feeOK]);
 const lanes=["cash","time","base","retry"];
 function payload(s,l,parents){
  if(l==="cash"){let v=R.snapshot(C.ledger(s.gross,s.forecast,s.cashOK),[{id:"pay",kind:"PAID",amount:s.paid,qualified:true}],new Set(["pay"]));return v?{status:"CONDITIONAL",balance:v.balance}:{status:"UNKNOWN"}}
  if(l==="time"){let f=s.timeOK?R.future(req(s),avail(s),s.support,s.completed):null;return f?{status:"CONDITIONAL",f}:{status:"UNKNOWN"}}
  const c=parents.cash.payload,t=parents.time.payload;
  if(c.status!=="CONDITIONAL"||t.status!=="CONDITIONAL"||(l==="retry"&&!s.feeOK))return {status:"UNKNOWN"};
  const q=R.choose(t.f,{balance:c.balance},l==="base"?0:s.fee,s.reserve);
  return l==="base"?{status:"CONDITIONAL",feasible:q.noRetry}:{status:"CONDITIONAL",ifSuccess:q.retrySuccess,guaranteed:q.retryRobust};
 }
 function render(s,prev={}){
  let result={},reused=[];
  for(let l of lanes){
   const k=key(s,l);
   if(prev[l]?.key===k){result[l]=prev[l];reused.push(l)}
   else result[l]={lane:l,key:k,payload:payload(s,l,result),authority:"NONE"};
  }
  return {result,reused}
 }
 // Oracle evaluates current snapshot from scratch using direct arithmetic and
 // R124 reference search, not cache or dependency keys.
 function oracle(s){
  const cash=s.cashOK?{status:"CONDITIONAL",balance:s.gross-s.paid}:{status:"UNKNOWN"},f=s.timeOK?R.future(req(s),avail(s),s.support,s.completed,true):null;
  const time=f?{status:"CONDITIONAL",f}:{status:"UNKNOWN"};
  const ok=cash.status==="CONDITIONAL"&&time.status==="CONDITIONAL";
  return {cash,time,base:ok?{status:"CONDITIONAL",feasible:cash.balance>=s.reserve&&f.base}:{status:"UNKNOWN"},retry:ok&&s.feeOK?{status:"CONDITIONAL",ifSuccess:cash.balance-s.fee>=s.reserve&&f.success,guaranteed:cash.balance-s.fee>=s.reserve&&f.robust}:{status:"UNKNOWN"}}
 }
 const out={prefixes:0,laneChecks:0,reused:0,recomputed:0,reuseByLane:{cash:0,time:0,base:0,retry:0},sourceUnknown:0,partialKnown:0,staleRejections:0,forecastPreserved:0,feeOnlyPreserved:0,naiveStalePayloads:0,abaControls:0,controls:0,witness:null};
 // Key equality is only for trusted in-memory results. External receipts must
 // be independently recomputed and match expected lane, key and full payload.
 function verify(s,l,r){
  if(!r||r.lane!==l||r.authority!=="NONE"||r.key!==key(s,l))return false;
  return eq(r,render(s).result[l])
 }
 function walk(s,prev,depth){
  if(!depth)return;
  for(let a of actions){
   let z=transition(s,a),r=render(z,prev),o=oracle(z);out.prefixes++;
   for(let l of lanes){
    ck(eq(r.result[l].payload,o[l]),"oracle "+l);out.laneChecks++;
    if(r.reused.includes(l)){out.reused++;out.reuseByLane[l]++}
    else {out.recomputed++;ck(prev[l].key!==r.result[l].key&&!verify(z,l,prev[l]),"stale");out.staleRejections++}
    if(!eq(prev[l].payload,o[l]))out.naiveStalePayloads++;
    if(o[l].status==="UNKNOWN")out.sourceUnknown++;
   }
   if(r.reused.length===4&&a==="FORECAST")out.forecastPreserved++;
   if(["FEE","FEE_SOURCE"].includes(a)){ck(eq(r.reused,["cash","time","base"]),"fee independence");out.feeOnlyPreserved++}
   if((o.cash.status==="CONDITIONAL")!==(o.time.status==="CONDITIONAL")){out.partialKnown++;out.witness??={event:a,state:z,outputs:o}}
   walk(z,r.result,depth-1)
  }
 }
 for(let k=0;k<2;k++){let s=initial(k);walk(s,render(s).result,4)}
 let s=initial(0),old=render(s).result;
 for(let [a,l] of [["CASH_SOURCE","cash"],["TIME_SOURCE","time"],["FEE_SOURCE","retry"],["PAYMENT","cash"],["PROGRESS","time"],["DEADLINE","time"],["SUPPORT","time"]]){
  let z=transition(transition(s,a),a);ck(eq(oracle(z)[l],old[l].payload)&&!verify(z,l,old[l]),"ABA");out.abaControls++;
 }
 for(let t of [()=>out.prefixes===14760,()=>out.laneChecks===59040,()=>out.reused+out.recomputed===out.laneChecks,()=>out.staleRejections===out.recomputed,()=>out.forecastPreserved===1640,()=>out.feeOnlyPreserved===3280,()=>verify(s,"cash",old.cash),()=>!verify(s,"cash",{...old.cash,payload:{status:"CONDITIONAL",balance:999}}),()=>!verify(s,"time",old.cash),()=>!verify(s,"cash",{...old.cash,authority:"EXECUTE"}),()=>out.partialKnown>0]){ck(t(),"control "+out.controls);out.controls++}
 return out
}
const {P,S,C,R}=load(docs);console.log(JSON.stringify(experiment(P,S,C,R),null,2));
```
## 实测
```json
{
  "prefixes": 14760,
  "laneChecks": 59040,
  "reused": 26240,
  "recomputed": 32800,
  "reuseByLane": {
    "cash": 11480,
    "time": 8200,
    "base": 4920,
    "retry": 1640
  },
  "sourceUnknown": 27240,
  "partialKnown": 6600,
  "staleRejections": 32800,
  "forecastPreserved": 1640,
  "feeOnlyPreserved": 3280,
  "naiveStalePayloads": 11991,
  "abaControls": 7,
  "controls": 11,
  "witness": {
    "event": "CASH_SOURCE",
    "state": {
      "cap": [
        2,
        2,
        2,
        2
      ],
      "gross": 4,
      "paid": 2,
      "forecast": 3,
      "completed": false,
      "extended": false,
      "support": [
        1,
        2
      ],
      "fee": 1,
      "reserve": 2,
      "cashOK": false,
      "timeOK": true,
      "feeOK": true,
      "gen": [
        4,
        0,
        0
      ]
    },
    "outputs": {
      "cash": {
        "status": "UNKNOWN"
      },
      "time": {
        "status": "CONDITIONAL",
        "f": {
          "base": true,
          "success": true,
          "failure": true,
          "robust": true,
          "spent": 8,
          "authority": "NONE"
        }
      },
      "base": {
        "status": "UNKNOWN"
      },
      "retry": {
        "status": "UNKNOWN"
      }
    }
  }
}
```
下一步：统一原始语义字段到可信状态增量的候选接口，重点研究真实数据与授权确认，避免将已完成数学研究误作开放语义成果。正式开发和训练另获授权。
