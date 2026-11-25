# 自主认知专项累计第123轮候选：延迟与失败调查的条件排程及备用策略
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / BOUNDED_OBSERVATION_FAILURE_POLICY / SYNTHETIC_FIXTURE / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main cbd64c9380f8bbb47cde43a1273e7fa07dfdc108。核对近12提交、13开放PR（#61待审）、v3.2前15行及历史全文、唯一交接前18行、R122前20行及实际代码、R40/R43前12行。R40有拒答成本但行动窗口不变，R43有一般部分观察，R122只假定按时完整信息；本轮实际复用其调查成本、现金门及R121/R120调度，增加固定延迟、失败、等待或备用共同预约，不重做一般DP。
## 固定资产
research/decision_hub/2026-11-25-costed-information-time-cash-feasibility.md e828e2cb88fcc9d1fc4825908f27b7684fdb31b1
research/decision_hub/2026-11-25-correlated-workload-observation-scheduling.md 227daac97ef9bc28b62d0c5f3087602a05e0cb8b
research/decision_hub/2026-11-25-contiguous-task-window-feasibility.md 089e7d446004f5303a26a6de25ff328fc857295e
research/decision_hub/2026-11-25-anchored-deadline-shared-time-feasibility.md e5a2b2921d9c810b82a1e449200b17caf987cf7d
research/decision_hub/2026-11-25-civil-temporal-anchor-version-replay.md cc9f6c6103e4ac863d2cdaa6961721149fd4189a
research/decision_hub/2026-11-25-temporal-quantity-candidate-separation.md 8a6b42f83b80283db6e215fe48f4fb2efbf8368c
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
research/decision_hub/2026-11-25-semantic-resource-ledger-temporal-bridge.md 65008b82d4720e931c99bd66ed03228b1f8ef69e
R40 56b1885f277b70797974ad48e80884a2d99dde81；R43 0eb4141f42b9e1607c8f4fe4122f6cc6cb699320；唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07。全为项目原创合成数据，非真人、独立留出或训练数据。
## 合同
沿R122四日、调查占第1或2日最早可用一小时、已锚定A确定连续任务、B连续C可拆及四种工时世界非空支持。调查现金模拟费用1美元、最低储备2美元，实际0/2/4，未来预测3不当现金。调查费用在结果揭晓前支付，不因失败返还；不真实支付。每种观察模式须含按时完整结果（第2日调查后剩余任务开始前），late额外允许已确定第3日开始获得完整结果；failure额外允许第2日已知失败（无信息）；pending额外允许第2日已知待定，第三日可能完整结果也可能失败；all允许全部。所有工时世界均可能出现相应结果，失败或待定不缩小支持；无概率。已知延迟保证成功只是合成条件，真实没有证据不能当保证。所有共同第1日行动先于信号，只允许完成A整个块或空闲。按时分支可分别为精确世界预约。第2日已知失败，必须对全部支持共同预约剩余时间；待定或已知延迟可选择立即按全部支持预约、忽略之后信息，或在第2日只完成确定A或空闲，第三日起按实际可观察的结果预约。如果待定后失败，第三日仍须对全部支持共同预约；相同第2日行动不得依赖未来结果。此为有限保守策略族，不包含在等待期间提前执行B/C、动态调整已预留空余、再次调查、其他时刻或真实环境变化；无策略只表示本合同族未找到保证，不能断言所有现实策略不可行。
## 算法
实际复用R122 costed/reduce/qualify/ledger及R119 project，固定调查占位扣除；每个共同早期动作按允许观察分支构造预约。共同预约用R121已证明的逐任务最大需求，完整信号分世界；较短任务使用预留子集。R120 solve验证全部分支，成功排程经validate复核；参考路径直接枚举A块并调用R120 oracle逐时段分配，比较全部合格早期块。两路径共享有限合同及最大需求定理，同研究者非独立验收。按时模式还与实际R122 costed的完整安全早期块集合核对。保留等待与备用的候选标记及具体见证，不生成可执行真实政策或自动授权。缺覆盖/支持为UNKNOWN，所有authority NONE。没有真实身份、授权、来源准入、时区、持久化、真实日程或预算保护；R120固定小域不代表设备性能。
## 实验
2880基础情景×两调查日期=5760个选择，存在调查槽则5模式逐一对照；计数按选择非独立人次或概率。立即调查与延迟/失败追加分支的保证收缩，记录等待与备用各自可提供续策的选择（可重叠，并非独占改善）。现金门固定费用与储备，三种实际余额；比较直接算术。14专项控制。参数、观察条件、受限策略族及费用由研究者选择；非真实用户规则。无训练、Codex、CI、原生执行、独立验收、PR合并、部署、费用或冻结变化。产品轨维护唯一交接。
## 复算
按上述八文件顺序置入docs[i].content，Node标准JS，仅执行已审查项目自有源码。
```js
function load(docs){
 const c=docs[0].content.split("```js\n")[1].split("\n```")[0];
 const A=Function(c.split("function experiment(P,S,E,L)")[0]+"\nreturn load;")()(docs.slice(1));
 const C=Function("P","S","E","L",c.slice(c.indexOf("function experiment(P,S,E,L)")).split(" const out={cases:")[0]+"\nreturn {ledger,reduce,costed,qualify};\n}\nreturn experiment(P,S,E,L);")(A.P,A.S,A.E,A.L);
 return {...A,C}
}
function experiment(P,S,E,C){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),pop=m=>{let n=0;for(;m;m&=m-1)n++;return n};
 const W=[[1,1],[1,2],[2,1],[2,2]],modes=["timely","late","failure","pending","all"];
 // "late" means a known guarantee of a complete signal on day 2 (zero-index);
 // "pending" means it may still fail then. All worlds can have any admitted outcome.
 function policy(req,available,support,reference=false){
  if(!Array.isArray(support)||!support.length||new Set(support).size!==support.length||support.some(i=>!Number.isInteger(i)||i<0||i>3))return {status:"UNKNOWN",authority:"NONE"};
  const plain=P.project(req,P.sources,P.anchors);if(!plain||plain.length!==3||plain[1].r<1||plain[2].r<1||plain[0].h<1)return {status:"UNKNOWN",authority:"NONE"};
  const jobs=plain.map((x,i)=>({...x,block:i!==2}));
  const blocks=(j,day,mask,h)=>{
   if(!h||day<j.r||day>j.d)return [0];
   if(!reference)return [0,...S.placements({...j,h},mask).filter(m=>m&&((m>>(3*day))&7)===popMask(m,day)) .filter(m=>(m&~(7<<(3*day)))===0)];
   let out=[0];for(let h0=0;h0+h<=3;h0++){let m=((1<<h)-1)<<(day*3+h0);if((m&mask)===m)out.push(m)}return out
  };
  // helper isolates the day; the final filter enforces no other occupied days.
  function popMask(m,day){return (m>>(3*day))&7}
  const demand=ws=>[Math.max(...ws.map(i=>W[i][0])),Math.max(...ws.map(i=>W[i][1]))];
  function finish(h,from,ws,mask){
   let [b,c]=demand(ws),j=jobs.map((x,i)=>({...x,r:Math.max(x.r,from),h:[h,b,c][i]}));
   const avail=mask&~((1<<(3*from))-1);
   if(reference)return S.oracle(j,avail)?{ok:true}:null;
   let z=S.solve(j,avail);ck(z.status!=="LIMIT","solver limit");
   if(z.status!=="FEASIBLE")return null;
   ck(S.validate(z,j,avail),"schedule certificate");return {ok:true,schedule:z.schedule}
  }
  function branch(h,from,ws,mask,exact){
   const groups=exact?ws.map(i=>[i]):[ws],result=[];
   for(let g of groups){let z=finish(h,from,g,mask);if(!z)return null;result.push({worlds:g,...z})}return result
  }
  const result=Object.fromEntries(modes.map(m=>[m,[]])),details=[];
  for(let early of blocks(jobs[0],0,available,jobs[0].h)){
   let left=early?0:jobs[0].h,now=branch(left,1,support,available,true),fallback=branch(left,1,support,available,false);
   let waitLate=[],waitPending=[];
   for(let mid of blocks(jobs[0],1,available,left)){
    let rest=mid?0:left,late=branch(rest,2,support,available,true),failLate=branch(rest,2,support,available,false);
    if(late)waitLate.push({day1:mid,late});
    if(late&&failLate)waitPending.push({day1:mid,late,failLate})
   }
   const lateOK=!!fallback||waitLate.length>0,pendingOK=!!fallback||waitPending.length>0;
   if(now)result.timely.push(early);
   if(now&&lateOK)result.late.push(early);
   if(now&&fallback)result.failure.push(early);
   if(now&&pendingOK)result.pending.push(early);
   if(now&&lateOK&&fallback&&pendingOK)result.all.push(early);
   details.push({early,timely:!!now,fallback:!!fallback,waitLate:waitLate.length,waitPending:waitPending.length,lateOK,pendingOK});
  }
  for(let m of modes)result[m].sort((a,b)=>a-b);
  return {status:"EVALUATED",safe:result,details,authority:"NONE"}
 }
 const out={cases:0,investigationChoices:0,slotAbsent:0,policyChecks:0,modeChecks:0,immediateGuaranteed:0,lateGuaranteed:0,failureGuaranteed:0,pendingGuaranteed:0,allGuaranteed:0,lateLoss:0,failureLoss:0,pendingLoss:0,waitingRescuesLate:0,fallbackRescuesLate:0,waitingRescuesPending:0,paidChecks:0,cashBlocked:0,timeBlocked:0,paidAllGuaranteed:0,paidNotGuaranteed:0,paidUnknown:0,controls:0,witnesses:{}};
 const cash=[0,2,4].map(x=>({x,v:C.ledger(x,3)}));
 for(let cap of P.caps)for(let frag of [false,true])for(let ha of [1,2])for(let ar of [0,1])for(let a of [P.ra,P.ra2]){
  let req={covered:true,capacity:cap,records:[P.record(a,ha,ar),P.record(P.rb2,1,1),P.record(P.rc,1,1)]},available=S.calendar(cap,frag);
  for(let m=1;m<16;m++){
   let support=[0,1,2,3].filter(i=>m&(1<<i));out.cases++;
   for(let day of [0,1]){
    out.investigationChoices++;
    let c=C.costed(req,available,support,day),q=null;
    if(c.status==="NO_INVESTIGATION_SLOT")out.slotAbsent++;
    else{
     let r=C.reduce(req,available,c.spent),z=policy(r.req,r.mask,support),o=policy(r.req,r.mask,support,true);
     ck(z.status==="EVALUATED"&&eq(z.safe,o.safe),"reference");
     ck(eq(z.safe.timely,c.safe.map(x=>x.day0).sort((a,b)=>a-b)),"R122 timely");
     out.policyChecks++;out.modeChecks+=5;
     const g=Object.fromEntries(modes.map(k=>[k,z.safe[k].length>0]));
     ck((!g.all||g.pending)&&(!g.pending||g.late)&&(!g.late||g.timely)&&(!g.failure||g.timely),"nesting");
     out.immediateGuaranteed+=+g.timely;out.lateGuaranteed+=+g.late;out.failureGuaranteed+=+g.failure;out.pendingGuaranteed+=+g.pending;out.allGuaranteed+=+g.all;
     out.lateLoss+=+(g.timely&&!g.late);out.failureLoss+=+(g.timely&&!g.failure);out.pendingLoss+=+(g.timely&&!g.pending);
     const ctx={cap,frag,ha,ar,deadline:a.receipt.value.date,support:support.map(i=>W[i]),investigationDay:day+1,spent:c.spent,details:z.details};
     if(g.timely&&!g.late)out.witnesses.lateLoss??=ctx;
     if(g.timely&&!g.failure)out.witnesses.failureLoss??=ctx;
     if(g.late&&z.details.some(x=>x.timely&&!x.fallback&&x.waitLate)){out.waitingRescuesLate++;out.witnesses.wait??=ctx}
     if(g.late&&z.details.some(x=>x.timely&&x.fallback&&!x.waitLate)){out.fallbackRescuesLate++;out.witnesses.fallback??=ctx}
     if(g.pending&&z.details.some(x=>x.timely&&!x.fallback&&x.waitPending))out.waitingRescuesPending++;
     q={status:g.all?"GUARANTEED_IN_DOMAIN":"POSSIBLE_NOT_GUARANTEED"};
    }
    for(let {x,v} of cash){let s=C.qualify(q??c,v,1,2,true);out.paidChecks++;
     let expected=x<3?"CASH_BLOCKED":q===null?"TIME_BLOCKED":q.status==="GUARANTEED_IN_DOMAIN"?"GUARANTEED_IN_DOMAIN":"NOT_GUARANTEED";ck(s===expected,"cash");
     if(s==="CASH_BLOCKED")out.cashBlocked++;else if(s==="TIME_BLOCKED")out.timeBlocked++;else if(s==="GUARANTEED_IN_DOMAIN")out.paidAllGuaranteed++;else if(s==="NOT_GUARANTEED")out.paidNotGuaranteed++;else out.paidUnknown++;
    }
   }
  }
 }
 const req={covered:true,capacity:[2,2,2,2],records:[P.record(P.ra,1,0),P.record(P.rb2,1,1),P.record(P.rc,1,1)]},avail=S.calendar(req.capacity,false);
 for(let t of [()=>out.cases===2880,()=>out.policyChecks===3600,()=>out.modeChecks===18000,()=>out.investigationChoices===5760,()=>out.paidChecks===17280,()=>out.cashBlocked+out.timeBlocked+out.paidAllGuaranteed+out.paidNotGuaranteed+out.paidUnknown===out.paidChecks,()=>out.immediateGuaranteed===160,()=>out.allGuaranteed<=out.lateGuaranteed&&out.allGuaranteed<=out.failureGuaranteed,()=>policy(req,avail,[]).status==="UNKNOWN",()=>policy(req,avail,[0,0]).status==="UNKNOWN",()=>policy(req,avail,[4]).status==="UNKNOWN",()=>policy({...req,covered:false},avail,[0]).status==="UNKNOWN",()=>C.qualify({status:"GUARANTEED_IN_DOMAIN"},C.ledger(4,3,false),1,2,true)==="UNKNOWN",()=>policy(req,avail,[1,2]).authority==="NONE"]){ck(t(),"control "+out.controls);out.controls++}
 return out
}
const {P,S,E,C}=load(docs);console.log(JSON.stringify(experiment(P,S,E,C),null,2));
```
## 实测
```json
{
  "cases": 2880,
  "investigationChoices": 5760,
  "slotAbsent": 2160,
  "policyChecks": 3600,
  "modeChecks": 18000,
  "immediateGuaranteed": 160,
  "lateGuaranteed": 160,
  "failureGuaranteed": 148,
  "pendingGuaranteed": 148,
  "allGuaranteed": 148,
  "lateLoss": 0,
  "failureLoss": 12,
  "pendingLoss": 12,
  "waitingRescuesLate": 16,
  "fallbackRescuesLate": 34,
  "waitingRescuesPending": 0,
  "paidChecks": 17280,
  "cashBlocked": 11520,
  "timeBlocked": 2160,
  "paidAllGuaranteed": 148,
  "paidNotGuaranteed": 3452,
  "paidUnknown": 0,
  "controls": 14,
  "witnesses": {
    "fallback": {
      "cap": [
        2,
        2,
        0,
        0
      ],
      "frag": false,
      "ha": 1,
      "ar": 0,
      "deadline": "2026-11-25",
      "support": [
        [
          1,
          1
        ]
      ],
      "investigationDay": 1,
      "spent": 1,
      "details": [
        {
          "early": 0,
          "timely": false,
          "fallback": false,
          "waitLate": 0,
          "waitPending": 0,
          "lateOK": false,
          "pendingOK": false
        },
        {
          "early": 2,
          "timely": true,
          "fallback": true,
          "waitLate": 0,
          "waitPending": 0,
          "lateOK": true,
          "pendingOK": true
        }
      ]
    },
    "wait": {
      "cap": [
        2,
        1,
        1,
        2
      ],
      "frag": false,
      "ha": 1,
      "ar": 0,
      "deadline": "2026-11-25",
      "support": [
        [
          1,
          2
        ],
        [
          2,
          1
        ]
      ],
      "investigationDay": 1,
      "spent": 1,
      "details": [
        {
          "early": 0,
          "timely": true,
          "fallback": false,
          "waitLate": 1,
          "waitPending": 0,
          "lateOK": true,
          "pendingOK": false
        },
        {
          "early": 2,
          "timely": true,
          "fallback": true,
          "waitLate": 1,
          "waitPending": 0,
          "lateOK": true,
          "pendingOK": true
        }
      ]
    },
    "failureLoss": {
      "cap": [
        2,
        1,
        1,
        2
      ],
      "frag": false,
      "ha": 1,
      "ar": 0,
      "deadline": "2026-11-25",
      "support": [
        [
          1,
          2
        ],
        [
          2,
          1
        ]
      ],
      "investigationDay": 2,
      "spent": 8,
      "details": [
        {
          "early": 0,
          "timely": false,
          "fallback": false,
          "waitLate": 0,
          "waitPending": 0,
          "lateOK": false,
          "pendingOK": false
        },
        {
          "early": 1,
          "timely": true,
          "fallback": false,
          "waitLate": 1,
          "waitPending": 0,
          "lateOK": true,
          "pendingOK": false
        },
        {
          "early": 2,
          "timely": true,
          "fallback": false,
          "waitLate": 1,
          "waitPending": 0,
          "lateOK": true,
          "pendingOK": false
        }
      ]
    }
  }
}
```
下一步：研究已发生支出与后续增量选择的正确分离、信息来源时效与观测资格，以及真实语义到策略合同连接。正式开发和训练另获授权。
