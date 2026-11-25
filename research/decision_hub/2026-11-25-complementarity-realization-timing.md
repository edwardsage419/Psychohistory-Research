# 自主认知专项累计第99轮候选：跨计划互补收益、到账时序及共同可行行动

2026-11-25。RESEARCH_CANDIDATE / COMPLEMENTARITY_TIMING_EXECUTED / SYNTHETIC_FIXTURE / NATIVE_NOT_RUN / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线main f8a16f272ec27d0d95fe90d7f323c8969b6c2978。核对近20提交、13开放PR（#61待审）、v3.2首8行及此前全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、未截断Git树相关文件名、第98轮首16行。继承第97/98轮资源账本，新增培训完成后下一期收益及旧任务成本减免、同一行动序列在两个固定情景下的可行性、未来收益提前入账反例。不重做既有第42/43轮反馈规划或学习资源分配，不运行原生模块。

## 合同
四期，一个旧承诺初始未完成。WAIT、EARN（3现金、1小时）、TRAIN（给定现金成本、2小时）、FINISH_OLD（给定现金及1小时）。培训一次，下一期开始激活；在高收益情景b=4领取一次现金，旧任务若在激活后完成减免1现金；低情景b=0无收益无减免。两情景在事前固定，非每期自由组合、非概率或真实因果。期初先结算到期收益、收入、账单及旧任务维持费，检查储备，然后行动再次检查储备及时间；末期培训尚未激活不计完成。人工夹具高收益已假设在到期时实现，不能作为现实已观察收入。旧承诺终点必须完成；基线培训未发生，新增组培训已激活。资金时间各自比较，不加权。提前入账对照故意把同一高情景收益在培训动作扣成本前记入现金，后续不重复领取，成本减免时点不变；只比较由此新增路径与前沿，不称为实际软件错误。

## 数学
每期相同现金、时间、旧任务状态、培训阶段可合并，保留完整终点状态与路径计数。对两个固定收益情景构造配对状态，两个世界必须采取同一预先固定动作且各自满足硬约束；其可行序列恰为两情景可行序列交集。此为开环保证，不是允许观察后调整的鲁棒最优政策；低情景在本夹具弱支配高情景的资源过程，因此共同可行序列等于低情景可行序列，不推断一般相关扰动。各单情景资源Pareto前沿以现金和剩余时间不小且至少一个严格更大过滤。highBeyondBase仅在基线和高收益组均有可行解时统计高收益前沿存在基线不能弱支配的资源点；不等于全部资源改善或现实收益。highPreservesAllBase检查基线每个前沿点均有一个高收益组点弱支配，不要求同一个点支配全部。未对跨情景收益做概率加权。缺覆盖UNKNOWN，预算耗尽无部分集合，authority NONE；仅计转移尝试，未计终点前沿、设备时间内存。真实到账、减免资格、主体、时限、来源及因果证据须由可信宿主另验；不以预测转为已入账事实。

## 实验
3现金×3时间×2收入×2储备×2旧完成成本×2培训成本=144场景。四种计算模式：低收益、高收益、低高共同开环、提前高收益。每模式独立枚举4^4序列直接重放，与DP全部终点状态路径计数对照；单情景前沿也核验。比较共同序列交集、时序误差、收益互补与可行性；同研究者参照，非独立验收或真人效果。全部参数、收益合同、成本减免及预算由研究者选定。12专项控制、144覆盖及144预算检查。无外部数据、训练、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。保留既有完整版本范围及验收门。

## 复算
```js
function experiment(){
 const ck=(v,m)=>{if(!v)throw Error(m)},H=4,A=["WAIT","EARN","TRAIN","FINISH_OLD"],key=s=>s.join(","),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 // c,h,old completed, training phase: 0 absent,1 pending,2 activated.
 // The only extra cash is a stipulated scenario-specific receipt at next
 // period opening. A discount applies only after activation.
 function step(s,t,a,p,b,early=false){
  let [c,h,o,k]=s;if(k===1){if(!early)c+=b;k=2}
  c+=(t===1?p.income:0)-(t%2)-(!o?1:0);if(c<p.reserve)return null;
  if(a===1){c+=3;h--}
  if(a===2){if(k!==0)return null;if(early)c+=b;c-=p.cost;h-=2;k=1}
  if(a===3){if(o)return null;c-=Math.max(0,p.finish-(k===2&&b>0?1:0));h--;o=1}
  return c>=p.reserve&&h>=0?[c,h,o,k]:null;
 }
 function add(m,s,n){let k=key(s);m.set(k,(m.get(k)||0)+n)}
 function pack(m){return [...m].sort((a,b)=>a[0].localeCompare(b[0]))}
 function front(rows){let a=[...new Set(rows.map(key))].map(x=>x.split(",").map(Number));return a.filter(x=>!a.some(y=>y.every((v,i)=>v>=x[i])&&y.some((v,i)=>v>x[i]))).sort((a,b)=>a[0]-b[0]||a[1]-b[1])}
 const out=s=>s.slice(0,2),dom=(x,y)=>x.every((v,i)=>v>=y[i]),terminal=s=>s[2]===1&&s[3]===2,base=s=>s[2]===1&&s[3]===0;
 function dp(p,worlds,cap=100000,covered=true,early=false){
  if(!covered)return {status:"UNKNOWN_COVERAGE",authority:"NONE"};
  let start=worlds.flatMap(()=>[p.cash,p.hours,0,0]),m=new Map([[key(start),1]]),used=0;
  for(let t=0;t<H;t++){let next=new Map();for(let [k,n] of m)for(let a=0;a<4;a++){
   if(used>=cap)return {status:"LIMIT",authority:"NONE",used};used++;
   let x=k.split(",").map(Number),y=worlds.map((b,i)=>step(x.slice(i*4,i*4+4),t,a,p,b,early));if(y.every(Boolean))add(next,y.flat(),n)
  }m=next}
  let trained=new Map(),old=new Map();for(let [k,n] of m){let x=k.split(",").map(Number),s=worlds.map((_,i)=>x.slice(4*i,4*i+4));if(s.every(terminal))add(trained,x,n);if(s.every(base))add(old,x,n)}
  return {status:"CONDITIONAL",authority:"NONE",trained,old,used};
 }
 // Independent direct replay of a fixed sequence, no state merging.
 function replay(seq,p,b,early=false){
  let c=p.cash,h=p.hours,done=false,k=0;
  for(let t=0;t<H;t++){
   if(k===1){k=2;if(!early)c+=b}
   if(t===1)c+=p.income;c-=t%2+ +!done;
   if(c<p.reserve)return null;
   switch(seq[t]){
    case 1:c+=3;h-=1;break;
    case 2:if(k)return null;c-=p.cost;h-=2;if(early)c+=b;k=1;break;
    case 3:if(done)return null;c-=p.finish;if(k===2&&b>0)c+=1;h-=1;done=true;break;
   }
   if(c<p.reserve||h<0)return null;
  }return [c,h,+done,k]
 }
 function oracle(p,worlds,early=false){let trained=new Map(),old=new Map(),seqs=[];
  for(let code=0;code<4**H;code++){let q=code,seq=[];for(let t=0;t<H;t++){seq.push(q%4);q=Math.floor(q/4)}
   let x=worlds.map(b=>replay(seq,p,b,early));if(x.every(v=>v&&terminal(v))){add(trained,x.flat(),1);seqs.push(code)}
   if(x.every(v=>v&&base(v)))add(old,x.flat(),1)
  }return {trained,old,seqs}
 }
 const resource=m=>[...m.keys()].map(k=>out(k.split(",").map(Number)));
 let o={scenarios:0,sequenceChecks:0,groupChecks:0,frontierChecks:0,baseFeasible:0,lowFeasible:0,highFeasible:0,robustFeasible:0,highOnly:0,earlyFalseFeasible:0,earlyExtraSequences:0,earlyExtraFrontier:0,highBeyondBase:0,highPreservesAllBase:0,lowBeyondBase:0,highAddsFeasibility:0,coverageChecks:0,budgetChecks:0,controls:0,witnesses:{}};
 for(let cash of [2,4,6])for(let hours of [2,4,6])for(let income of [0,2])for(let reserve of [0,1])for(let finish of [2,4])for(let cost of [1,3]){
  let p={cash,hours,income,reserve,finish,cost},modes=[[[0],false],[[4],false],[[0,4],false],[[4],true]],v=[],q=[];
  for(let [ws,early] of modes){let a=dp(p,ws,100000,true,early),b=oracle(p,ws,early);ck(eq(pack(a.trained),pack(b.trained))&&eq(pack(a.old),pack(b.old)),"oracle");v.push(a);q.push(b);o.groupChecks+=2;o.sequenceChecks+=256;
   if(ws.length===1){ck(eq(front(resource(a.trained)),front(resource(b.trained)))&&eq(front(resource(a.old)),front(resource(b.old))),"front");o.frontierChecks+=2}
  }
  let [l,h,z,e]=v,basef=front(resource(l.old)),lf=front(resource(l.trained)),hf=front(resource(h.trained)),ef=front(resource(e.trained));
  ck(eq(pack(l.old),pack(h.old))&&eq(pack(h.old),pack(e.old)),"common base");
  ck(q[2].seqs.every(i=>q[0].seqs.includes(i)&&q[1].seqs.includes(i))&&q[2].seqs.length===q[0].seqs.filter(i=>q[1].seqs.includes(i)).length,"intersection");
  ck(q[0].seqs.every(i=>q[1].seqs.includes(i))&&q[1].seqs.every(i=>q[3].seqs.includes(i)),"monotonic fixture");
  o.scenarios++;o.baseFeasible+=+!!basef.length;o.lowFeasible+=+!!lf.length;o.highFeasible+=+!!hf.length;o.robustFeasible+=+!!z.trained.size;
  if(hf.length&&!lf.length){o.highOnly++;o.witnesses.highOnly??={p,base:basef,low:lf,high:hf}}
  if(hf.length&&!basef.length)o.highAddsFeasibility++;
  if(ef.length&&!hf.length){o.earlyFalseFeasible++;o.witnesses.early??={p,correct:hf,premature:ef}}
  o.earlyExtraSequences+=q[3].seqs.filter(i=>!q[1].seqs.includes(i)).length;
  if(!eq(ef,hf))o.earlyExtraFrontier++;
  if(basef.length&&hf.length&&hf.some(x=>!basef.some(y=>dom(y,x)))){o.highBeyondBase++;o.witnesses.complement??={p,base:basef,high:hf}}
  if(basef.length&&hf.length&&basef.every(x=>hf.some(y=>dom(y,x))))o.highPreservesAllBase++;
  if(basef.length&&lf.some(x=>!basef.some(y=>dom(y,x))))o.lowBeyondBase++;
  ck(dp(p,[0,4],100000,false).status==="UNKNOWN_COVERAGE","coverage");o.coverageChecks++;
  let lim=dp(p,[0,4],z.used-1);ck(lim.status==="LIMIT"&&!Object.hasOwn(lim,"trained")&&eq(pack(dp(p,[0,4],z.used).trained),pack(z.trained)),"budget");o.budgetChecks++;
 }
 for(let t of [()=>o.scenarios===144,()=>o.sequenceChecks===147456,()=>o.groupChecks===1152,()=>o.frontierChecks===864,()=>o.robustFeasible===o.lowFeasible,()=>o.highOnly===o.highFeasible-o.lowFeasible,()=>o.lowBeyondBase===0,()=>o.earlyExtraSequences>0,()=>o.highBeyondBase>0,()=>o.budgetChecks===144&&o.coverageChecks===144,()=>step([2,3,0,0],0,2,{income:0,reserve:0,cost:3,finish:2},4)===null,()=>step([2,3,0,0],0,2,{income:0,reserve:0,cost:3,finish:2},4,true)!==null]){ck(t(),"control");o.controls++}
 return o;
}
console.log(experiment())
```

## 实测
```json
{
  "scenarios": 144,
  "sequenceChecks": 147456,
  "groupChecks": 1152,
  "frontierChecks": 864,
  "baseFeasible": 128,
  "lowFeasible": 44,
  "highFeasible": 88,
  "robustFeasible": 44,
  "highOnly": 44,
  "earlyFalseFeasible": 1,
  "earlyExtraSequences": 376,
  "earlyExtraFrontier": 18,
  "highBeyondBase": 13,
  "highPreservesAllBase": 0,
  "lowBeyondBase": 0,
  "highAddsFeasibility": 0,
  "coverageChecks": 144,
  "budgetChecks": 144,
  "controls": 12,
  "witnesses": {
    "highOnly": {
      "p": {
        "cash": 2,
        "hours": 4,
        "income": 0,
        "reserve": 0,
        "finish": 2,
        "cost": 1
      },
      "base": [
        [
          2,
          1
        ],
        [
          5,
          0
        ]
      ],
      "low": [],
      "high": [
        [
          0,
          1
        ],
        [
          3,
          0
        ]
      ]
    },
    "early": {
      "p": {
        "cash": 2,
        "hours": 4,
        "income": 0,
        "reserve": 0,
        "finish": 2,
        "cost": 3
      },
      "correct": [],
      "premature": [
        [
          0,
          0
        ]
      ]
    },
    "complement": {
      "p": {
        "cash": 2,
        "hours": 6,
        "income": 0,
        "reserve": 0,
        "finish": 2,
        "cost": 1
      },
      "base": [
        [
          2,
          3
        ],
        [
          5,
          2
        ]
      ],
      "high": [
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
        ]
      ]
    }
  }
}
```

## 后续
优先连接真实原文中的预计收入、确定入账、到账时间、条件、证据及已履约状态，建立不可混淆的长期账本接口，避免继续仅扩展人工场景。独立轨负责未见评价，数据轨负责合法真实来源，产品轨维护唯一交接。正式版本及训练另获授权。
