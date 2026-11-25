# 自主认知专项累计第98轮候选：承诺变更的配对反事实与旧目标机会损失

2026-11-25。RESEARCH_CANDIDATE / PAIRED_COMMITMENT_FRONTIER_EXECUTED / SYNTHETIC_FIXTURE / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线main 9c32e8e20de270b00f366a3ff2dda5bf031b0fcc。核对近20提交、13开放PR（#61待审）、v3.2首8行及此前全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、未截断Git树相关文件名、第97轮报告首16行。第97轮从两个未启动项目计算共同前沿；本轮固定已经发生的旧承诺，从相同初始账本比较必须完成新目标、保留旧承诺、经资格确认取消等互斥合同。不重跑既有R42/43鲁棒规划、R97实验或原生平台。

## 合同
四期，每期一个行动，旧项目初始已启动，新项目未开始。现金与时间各自计量，不混合；保留旧项目需支付完成成本与1小时，新项目启动耗给定现金及2小时，完成耗1现金及1小时；赚取3现金耗1小时。每期先结算同一收入、账单、未完成项目维持费各1，再检查储备，行动后再检查储备及时间。旧项目已发生的沉没成本不可返还。取消仅在人工给定cancelQualified为真时允许，支付给定费用，不消耗时间但占一个决策期，旧目标标为取消而非完成；这不是实际用户授权或合同法律资格。四终点组：仅旧完成、旧新均完成、取消旧且新完成、仅取消旧。未完成承诺不可进入这些终点组。取消后不能重启，未模拟退款、延期、违约或新项目收益。所有组使用相同初始账本及时间窗，未将未执行反事实当观察。资源输出为现金和时间，均假设越多越好，目标完成身份独立列示，不将取消与履约混同或跨组直接排序。

## 数学及计算
复用R97充分状态思想但新增旧项目取消吸收状态。逐期合并完全相同状态并计数，分别计算四类终点集合及资源Pareto前沿。独立直接枚举6^4行动串，重复账本计算，逐组逐状态及路径计数对照。组内保留资源不受支配点。对旧完成且新未启动基线前沿点b，若旧新均完成组没有任一资源点a逐维>=b，则原资源组合不可在必须新增计划时保持；这称为条件性资源机会损失，不是福利损失或统一人生评分。仅在两组均非空时统计前沿点损失；无新增可行方案另计，避免重复。新项目在本夹具只有现金时间成本及维持费，替换其启动完成动作为等待保留旧行动时，现金与时间均不下降，因而新增组位于旧组下闭包内；真实项目可带来现金收益、互补、前置技能等，本结论不能推广。取消救援只指旧新均完成不可行而取消旧后新完成可行；旧目标损失另行显示，不认为自动值得取消。未将历史成本加入未来优化。authority NONE，覆盖缺失UNKNOWN，预算超限不返回任何组；计转移尝试，不计前沿、真实设备成本。不存在真实开放语言覆盖或资格证明。

## 实验与结果
4现金×3时间×2收入×2储备×2旧完成成本×2新启动成本×2取消费×2取消资格=768人工情景。每个穷举1296行动串，4组结果及前沿核验，同研究者参照非独立验收。取消资格不明的真实情景必须保留UNKNOWN，不能用布尔夹具替代授权。对照为同一模型中不同终点合同，非普通AI、真实人或预测准确率。参数、时序、范围、偏好方向、预算、取消条件均由研究者选定。无新外部数据、训练、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。保留完整版本范围和正式验收门。

## 复算
```js
function experiment(){
 const ck=(x,m)=>{if(!x)throw Error(m)}, H=4, A=["WAIT","EARN","FINISH_OLD","START_NEW","FINISH_NEW","CANCEL_OLD"],key=s=>s.join(","),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 // Old commitment already active at t=0. No refund for sunk cost.
 // old 1 active,2 fulfilled,3 cancelled; new 0 not started,1 active,2 fulfilled.
 function step(s,t,a,p){
  let [c,h,o,n]=s;c+=(t===1?p.income:0)-(t%2)-(o===1?1:0)-(n===1?1:0);
  if(c<p.reserve)return null;
  if(a===1){c+=3;h--}
  if(a===2){if(o!==1)return null;c-=p.finish;h--;o=2}
  if(a===3){if(n!==0)return null;c-=p.start;h-=2;n=1}
  if(a===4){if(n!==1)return null;c--;h--;n=2}
  if(a===5){if(o!==1||!p.cancelQualified)return null;c-=p.fee;o=3}
  return c>=p.reserve&&h>=0?[c,h,o,n]:null;
 }
 const out=s=>[s[0],s[1]],dom=(x,y)=>x.every((v,i)=>v>=y[i]);
 function frontier(rows){let v=[...new Set(rows.map(key))].map(k=>k.split(",").map(Number));return v.filter(x=>!v.some(y=>dom(y,x)&&key(y)!==key(x))).sort((a,b)=>a[0]-b[0]||a[1]-b[1])}
 function terminal(s){let o=s[2],n=s[3];if(o===2&&n===0)return 0;if(o===2&&n===2)return 1;if(o===3&&n===2)return 2;if(o===3&&n===0)return 3;return -1}
 function add(m,s,count){let k=key(s);m.set(k,(m.get(k)||0)+count)}
 function pack(m){return [...m].sort((a,b)=>a[0].localeCompare(b[0]))}
 function project(m){return [...m.keys()].map(k=>out(k.split(",").map(Number)))}
 function dp(p,qualified=true,cap=100000){
  if(!qualified)return {status:"UNKNOWN_COVERAGE",authority:"NONE"};
  let m=new Map([[key([p.cash,p.hours,1,0]),1]]),used=0;
  for(let t=0;t<H;t++){let next=new Map();for(let [k,count] of m)for(let a=0;a<A.length;a++){if(used>=cap)return {status:"LIMIT",authority:"NONE",used};used++;let s=step(k.split(",").map(Number),t,a,p);if(s)add(next,s,count)}m=next}
  let groups=Array.from({length:4},()=>new Map());for(let [k,count] of m){let s=k.split(",").map(Number),i=terminal(s);if(i>=0)add(groups[i],s,count)}
  return {status:"EXACT_CONDITIONAL",authority:"NONE",groups,used}
 }
 function oracle(p){
  let groups=Array.from({length:4},()=>new Map());
  for(let code=0;code<6**H;code++){let q=code,c=p.cash,h=p.hours,o=1,n=0,ok=true;
   for(let t=0;t<H;t++){let a=q%6;q=Math.floor(q/6);
    c-=t%2+ +(o===1)+ +(n===1);if(t===1)c+=p.income;
    if(c<p.reserve){ok=false;break}
    switch(a){
    case 0:break;
    case 1:c+=3;h--;break;
    case 2:if(o!==1)ok=false;else{o=2;c-=p.finish;h--}break;
    case 3:if(n!==0)ok=false;else{n=1;c-=p.start;h-=2}break;
    case 4:if(n!==1)ok=false;else{n=2;c--;h--}break;
    case 5:if(o!==1||!p.cancelQualified)ok=false;else{o=3;c-=p.fee}break;
    }
    if(!ok||c<p.reserve||h<0){ok=false;break}
   }
   if(!ok)continue;let i=o===2&&n===0?0:o===2&&n===2?1:o===3&&n===2?2:o===3&&n===0?3:-1;if(i>=0)add(groups[i],[c,h,o,n],1)
  }return groups
 }
 let o={scenarios:0,sequenceChecks:0,groupChecks:0,frontierChecks:0,baseFeasible:0,addFeasible:0,cancelNewFeasible:0,cancelOnlyFeasible:0,baseButAddImpossible:0,baseAndAddFeasible:0,allBaseFrontierLost:0,someBaseFrontierLost:0,baseFrontierPoints:0,baseFrontierLost:0,addOutsideBaseDownset:0,cancelNewRescue:0,cancelRescueWithOldLoss:0,unauthorizedCancellationExcluded:0,budgetChecks:0,coverageChecks:0,controls:0,witnesses:{}};
 for(let cash of [2,4,6,8])for(let hours of [2,4,6])for(let income of [0,2])for(let reserve of [0,2])for(let finish of [1,3])for(let start of [1,3])for(let fee of [0,2])for(let cancelQualified of [false,true]){
  let p={cash,hours,income,reserve,finish,start,fee,cancelQualified},v=dp(p),w=oracle(p),f=v.groups.map(g=>frontier(project(g))),g=w.map(z=>frontier(project(z)));
  ck(v.groups.every((z,i)=>eq(pack(z),pack(w[i]))),"groups");ck(eq(f,g),"frontier");
  o.scenarios++;o.sequenceChecks+=1296;o.groupChecks+=4;o.frontierChecks+=4;
  let [base,addf,cancel,only]=f;
  o.baseFeasible+=+!!base.length;o.addFeasible+=+!!addf.length;o.cancelNewFeasible+=+!!cancel.length;o.cancelOnlyFeasible+=+!!only.length;
  if(base.length&&!addf.length)o.baseButAddImpossible++;
  if(base.length&&addf.length){o.baseAndAddFeasible++;let lost=base.filter(x=>!addf.some(y=>dom(y,x)));o.baseFrontierPoints+=base.length;o.baseFrontierLost+=lost.length;o.someBaseFrontierLost+=+(lost.length>0);o.allBaseFrontierLost+=+(lost.length===base.length);if(lost.length)o.witnesses.loss??={p,base,add:addf,lost};}
  // The new project has only costs in this fixture. Replacing its actions with
  // WAIT yields an old-only feasible path with weakly greater resources.
  for(let x of addf)if(!base.some(y=>dom(y,x)))o.addOutsideBaseDownset++;
  if(!addf.length&&cancel.length){o.cancelNewRescue++;if(base.length){o.cancelRescueWithOldLoss++;o.witnesses.rescue??={p,base,add:addf,cancel}}}
  if(!cancelQualified){ck(!cancel.length&&!only.length,"authorization");o.unauthorizedCancellationExcluded++}
  ck(dp(p,false).status==="UNKNOWN_COVERAGE","coverage");o.coverageChecks++;
  let lim=dp(p,true,v.used-1);ck(lim.status==="LIMIT"&&!Object.hasOwn(lim,"groups")&&eq(dp(p,true,v.used).groups.map(pack),v.groups.map(pack)),"budget");o.budgetChecks++;
 }
 for(let t of [()=>o.scenarios===768,()=>o.groupChecks===3072,()=>o.frontierChecks===3072,()=>o.baseFeasible===o.baseButAddImpossible+o.baseAndAddFeasible,()=>o.addOutsideBaseDownset===0,()=>o.unauthorizedCancellationExcluded===384,()=>o.budgetChecks===768,()=>o.coverageChecks===768,()=>o.cancelNewRescue>0,()=>o.baseFrontierLost>0,()=>step([4,3,1,0],0,5,{income:0,reserve:0,fee:0,cancelQualified:false})===null,()=>step([4,3,1,0],0,5,{income:0,reserve:0,fee:2,cancelQualified:true})[0]===1]){ck(t(),"control");o.controls++}
 return o;
}
console.log(experiment())
```

## 实测
```json
{
  "scenarios": 768,
  "sequenceChecks": 995328,
  "groupChecks": 3072,
  "frontierChecks": 3072,
  "baseFeasible": 656,
  "addFeasible": 152,
  "cancelNewFeasible": 128,
  "cancelOnlyFeasible": 336,
  "baseButAddImpossible": 504,
  "baseAndAddFeasible": 152,
  "allBaseFrontierLost": 152,
  "someBaseFrontierLost": 152,
  "baseFrontierPoints": 608,
  "baseFrontierLost": 608,
  "addOutsideBaseDownset": 0,
  "cancelNewRescue": 60,
  "cancelRescueWithOldLoss": 60,
  "unauthorizedCancellationExcluded": 384,
  "budgetChecks": 768,
  "coverageChecks": 768,
  "controls": 12,
  "witnesses": {
    "rescue": {
      "p": {
        "cash": 2,
        "hours": 4,
        "income": 2,
        "reserve": 0,
        "finish": 1,
        "start": 1,
        "fee": 0,
        "cancelQualified": true
      },
      "base": [
        [
          0,
          3
        ],
        [
          3,
          2
        ],
        [
          6,
          1
        ],
        [
          9,
          0
        ]
      ],
      "add": [],
      "cancel": [
        [
          1,
          0
        ]
      ]
    },
    "loss": {
      "p": {
        "cash": 2,
        "hours": 6,
        "income": 2,
        "reserve": 0,
        "finish": 1,
        "start": 1,
        "fee": 0,
        "cancelQualified": false
      },
      "base": [
        [
          0,
          5
        ],
        [
          3,
          4
        ],
        [
          6,
          3
        ],
        [
          9,
          2
        ]
      ],
      "add": [
        [
          0,
          1
        ]
      ],
      "lost": [
        [
          0,
          5
        ],
        [
          3,
          4
        ],
        [
          6,
          3
        ],
        [
          9,
          2
        ]
      ]
    }
  }
}
```

## 后续
优先研究新增承诺带来的互补收益、延期及修改条件，随后接入经核验的跨决策原文义务、版本身份及证据；不将本轮确定性成本模型直接作为实际人生建议。数据、独立验收及产品轨职责不变，正式开发和训练另获授权。
