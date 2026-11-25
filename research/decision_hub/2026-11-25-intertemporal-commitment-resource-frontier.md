# 自主认知专项累计第97轮候选：跨期承诺、资源账本与多目标可达前沿

2026-11-25。RESEARCH_CANDIDATE / DETERMINISTIC_COMMITMENT_FRONTIER_EXECUTED / SYNTHETIC_FIXTURE / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线main ef2e5e3733583da44267c5a6e16c2560a7741c28。核对近20提交、13开放PR（#61待审）、v3.2首8行及此前全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、完整未截断仓库树相关文件名、第42轮robust-longitudinal-planning、第43轮partial-observation-robust-planning、第13轮adaptive-resource-allocation及第96轮报告首18行。已有第42/43轮鲁棒反馈与观察历史、第13轮学习资源分配，故不重复Bellman最坏效用或概率学习DP。本轮增量为确定性跨期承诺账本、前置顺序与持续义务、双资源约束及不加权多目标Pareto可达前沿，保留所有首行动身份。未调用原生模块或历史R模型。

## 合同
四期、每期至多一个动作（WAIT/EARN/START_A/FINISH_A/START_B/FINISH_B），现金与剩余总时间分别记账，不相加。两项目阶段0未启动、1未完成承诺、2完成，启动需各自现金成本及2小时，完成需1现金及1小时，必须先启动且不能重复。EARN耗1小时获3现金，WAIT无动作成本；每期先结算第1索引期收入（仅一次）、奇数索引期账单1、每未完成承诺1维持费，再检查现金储备底线，行动后再次检查储备及时间非负。禁止用本期后续收入回补已经违反的底线。终点要求至少一项目完成且没有未完成承诺，此为假设用户确认的硬条件，不是所有人生项目都必须完成；真实取消、违约及延长时域需单独建模。无借贷、贴现、随机性、真实个人参数。终端输出四维（完成A、完成B、现金、剩余时间），均假设越高越好；不加权、不选择单一人生总分。以分量不小且至少一项严格更大定义支配，保留全部不受支配输出及各输出所有可达首行动。首行动集合表示存在一条可行续策，非现实承诺、最优唯一动作或自动执行。没有真实原文解析、证据资格、用户授权或统计概率。

## 数学
充分状态为时间索引及(cash,hours,phaseA,phaseB)。每期同一状态的后继和终点输出相同；可以合并状态、累加路径数、按位并集首行动身份，归纳保持全部可达状态及路径数。终点先硬门后对四维输出进行Pareto过滤；相同输出合并路径及首动作。不对中间状态用现金/时间单独支配剪枝（承诺身份不可丢失）。时间为各期可达状态数×6次转移及终点两两支配比较，状态规模可能随预算、项目数、时间增长；未做生产复杂度或真实设备测量。预算计转移尝试，不含前沿比较、构图、实际内存或BigInt（此有限路径数在JS安全整数内）。超限整体不返回部分状态/前沿；覆盖缺失UNKNOWN_COVERAGE，封闭域无合格计划NO_FEASIBLE_PLAN；所有结果authority NONE。真实开放域覆盖由可信宿主另外核验。

## 实验
3现金×3小时×2收入×2储备×2项目A成本×2项目B成本=144场景；每场景直接枚举6^4条行动串并独立账本复算，对所有可达终端输出、路径计数、首动作位图、放宽终点条件的结果、前沿核验。参照同研究者编写，非独立验收。对照1仅放宽终端无未完成承诺，仍要求完成至少一个项目并维持所有阶段底线；统计其额外输出、前沿变化及假可行场景。对照2按当期两项目阶段进展之和、现金、时间及动作ID排序的短视策略（研究者选定弱基线，不是通用AI或现有系统），统计在有可行完整计划时失败或被前沿支配；不以其结果证明现实收益。immediateTrap指当前合法但没有任何合格终点续策的首动作，仅给定有限合同。重复路径和场景不是独立用户数据。144覆盖与预算边界、12专项控制。无新外部资料、训练、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。参数、目标方向、预算和时序由研究者选定。保留既有完整版本范围及正式验收门。

## 复算
```js
function experiment(){
 const ck=(v,m)=>{if(!v)throw Error(m)},H=4,actions=["WAIT","EARN","START_A","FINISH_A","START_B","FINISH_B"],key=s=>s.join(","),same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 // State [cash, remaining hours, project A phase, project B phase].
 // 0 not started, 1 outstanding commitment, 2 completed.
 function step(s,t,a,p){
  let [c,h,A,B]=s;c+=(t===1?p.income:0)-(t%2)-(A===1?1:0)-(B===1?1:0);
  if(c<p.reserve)return null;
  if(a===1){c+=3;h--}
  if(a===2){if(A!==0)return null;c-=p.ca;h-=2;A=1}
  if(a===3){if(A!==1)return null;c--;h--;A=2}
  if(a===4){if(B!==0)return null;c-=p.cb;h-=2;B=1}
  if(a===5){if(B!==1)return null;c--;h--;B=2}
  return c>=p.reserve&&h>=0?[c,h,A,B]:null;
 }
 const output=s=>[+(s[2]===2),+(s[3]===2),s[0],s[1]];
 const terminal=s=>s[2]!==1&&s[3]!==1&&(s[2]===2||s[3]===2);
 function add(m,k,n,bits){let a=m.get(k)||{n:0,bits:0};a.n+=n;a.bits|=bits;m.set(k,a)}
 function finish(m){return [...m.entries()].sort((a,b)=>a[0].localeCompare(b[0])).map(([k,v])=>[k,v.n,v.bits])}
 function frontier(m){let a=[...m].map(([k,v])=>[k.split(",").map(Number),v]);return a.filter(([x])=>!a.some(([y])=>y.every((v,i)=>v>=x[i])&&y.some((v,i)=>v>x[i]))).map(([x,v])=>[key(x),v.bits]).sort((a,b)=>a[0].localeCompare(b[0]))}
 function dp(p,closed=true,cap=100000){
  if(!closed)return {status:"UNKNOWN_COVERAGE",authority:"NONE"};
  let m=new Map([[key([p.cash,p.hours,0,0]),{n:1,bits:0}]]),used=0,peak=1,first=0;
  for(let t=0;t<H;t++){
   let next=new Map();
   for(let [k,v] of m)for(let a=0;a<6;a++){
    if(used>=cap)return {status:"LIMIT",authority:"NONE",used};used++;
    let s=step(k.split(",").map(Number),t,a,p);if(s){if(!t)first|=1<<a;add(next,key(s),v.n,t?v.bits:1<<a)}
   }m=next;peak=Math.max(peak,m.size)
  }
  let valid=new Map(),relaxed=new Map(),openPaths=0,allPaths=0;
  for(let [k,v] of m){let s=k.split(",").map(Number);allPaths+=v.n;if(s[2]===2||s[3]===2){add(relaxed,key(output(s)),v.n,v.bits);if(!terminal(s))openPaths+=v.n}if(terminal(s))add(valid,key(output(s)),v.n,v.bits)}
  return {status:valid.size?"EXACT_CONDITIONAL":"NO_FEASIBLE_PLAN",authority:"NONE",valid,relaxed,openPaths,allPaths,first,used,peak}
 }
 // Independent enumeration of all six-action strings and replay via direct
 // cash/hour accounting and phase preconditions, without DP state merging.
 function oracle(p){
  let valid=new Map(),relaxed=new Map(),allPaths=0,openPaths=0;
  for(let code=0;code<6**H;code++){
   let q=code,seq=[];for(let t=0;t<H;t++){seq.push(q%6);q=Math.floor(q/6)}
   let c=p.cash,h=p.hours,ph=[0,0],ok=true;
   for(let t=0;t<H;t++){
    c+=t===1?p.income:0;c-=t%2+ph.filter(x=>x===1).length;
    if(c<p.reserve){ok=false;break}
    let a=seq[t];
    if(a===1){c+=3;h-=1}
    if(a>=2){let j=a>=4?1:0,start=a%2===0;if(ph[j]!==+!start){ok=false;break}
     ph[j]++;c-=start?(j?p.cb:p.ca):1;h-=start?2:1}
    if(c<p.reserve||h<0){ok=false;break}
   }
   if(!ok)continue;allPaths++;
   if(!ph.includes(2))continue;
   let k=key([+(ph[0]===2),+(ph[1]===2),c,h]);add(relaxed,k,1,1<<seq[0]);
   if(ph.includes(1))openPaths++;else add(valid,k,1,1<<seq[0])
  }return {valid,relaxed,allPaths,openPaths}
 }
 // Myopic ordering: prefer immediate phase progress (including start), then
 // current cash, then hours. No lookahead. This is a stipulated weak baseline.
 function greedy(p){let s=[p.cash,p.hours,0,0],seq=[];for(let t=0;t<H;t++){let options=actions.map((_,a)=>({a,s:step(s,t,a,p)})).filter(x=>x.s);if(!options.length)return {valid:false,seq};options.sort((x,y)=>(y.s[2]+y.s[3])-(x.s[2]+x.s[3])||y.s[0]-x.s[0]||y.s[1]-x.s[1]||x.a-y.a);s=options[0].s;seq.push(options[0].a)}return {valid:terminal(s),seq,out:output(s)}}
 let o={scenarios:0,enumeratedSequences:0,allLegalSequences:0,validSequences:0,openCommitmentSequences:0,reachableOutputChecks:0,frontierPoints:0,frontierFirstActionChecks:0,feasibleScenarios:0,impossibleScenarios:0,relaxedFalseFeasible:0,relaxedExtraOutputs:0,relaxedExtraFrontierScenarios:0,immediateTrapScenarios:0,immediateTrapActions:0,greedyFailedFeasible:0,greedyDominatedFeasible:0,greedyEfficient:0,peakStates:0,maxWork:0,coverageChecks:0,budgetChecks:0,controls:0,witnesses:{}};
 for(let cash of [2,4,6])for(let hours of [3,5,7])for(let income of [0,2])for(let reserve of [0,2])for(let ca of [1,3])for(let cb of [1,3]){
  let p={cash,hours,income,reserve,ca,cb},v=dp(p),q=oracle(p);
  ck(same(finish(v.valid),finish(q.valid))&&same(finish(v.relaxed),finish(q.relaxed))&&v.allPaths===q.allPaths&&v.openPaths===q.openPaths,"oracle");
  let f=frontier(v.valid),g=frontier(q.valid),rel=frontier(v.relaxed);ck(same(f,g),"frontier");
  o.scenarios++;o.enumeratedSequences+=6**H;o.allLegalSequences+=v.allPaths;o.validSequences+=[...v.valid.values()].reduce((n,x)=>n+x.n,0);o.openCommitmentSequences+=v.openPaths;o.reachableOutputChecks+=v.valid.size;o.frontierPoints+=f.length;o.frontierFirstActionChecks+=f.length;o.peakStates=Math.max(o.peakStates,v.peak);o.maxWork=Math.max(o.maxWork,v.used);
  let bits=[...v.valid.values()].reduce((n,x)=>n|x.bits,0),trap=v.first&~bits;
  if(v.valid.size){o.feasibleScenarios++;if(trap){o.immediateTrapScenarios++;o.immediateTrapActions+=actions.filter((_,i)=>trap&(1<<i)).length;o.witnesses.trap??={p,immediate:actions.filter((_,i)=>v.first&(1<<i)),canComplete:actions.filter((_,i)=>bits&(1<<i)),frontier:f}}
   let z=greedy(p);if(!z.valid){o.greedyFailedFeasible++;o.witnesses.greedy??={p,greedy:z.seq.map(a=>actions[a]),frontier:f}}
   else if(!f.some(([k])=>k===key(z.out))){o.greedyDominatedFeasible++}else o.greedyEfficient++;
  }else{o.impossibleScenarios++;if(v.relaxed.size){o.relaxedFalseFeasible++;o.witnesses.relaxed??={p,relaxed:finish(v.relaxed),valid:finish(v.valid)}}}
  let extra=[...v.relaxed.keys()].filter(k=>!v.valid.has(k));o.relaxedExtraOutputs+=extra.length;if(!same(f.map(x=>x[0]),rel.map(x=>x[0]))){o.relaxedExtraFrontierScenarios++;o.witnesses.frontier??={p,exact:f,relaxed:rel}}
  ck(dp(p,false).status==="UNKNOWN_COVERAGE","coverage");o.coverageChecks++;let z=dp(p,true,v.used-1);ck(z.status==="LIMIT"&&!Object.hasOwn(z,"valid")&&same(finish(dp(p,true,v.used).valid),finish(v.valid)),"budget");o.budgetChecks++;
 }
 for(let [name,test] of [["scenarios",o.scenarios===144],["all sequence count",o.enumeratedSequences===144*1296],["feasible accounting",o.feasibleScenarios+o.impossibleScenarios===o.scenarios],["greedy accounting",o.greedyFailedFeasible+o.greedyDominatedFeasible+o.greedyEfficient===o.feasibleScenarios],["budget",o.budgetChecks===144],["coverage",o.coverageChecks===144],["traps",o.immediateTrapActions>0],["open obligations",o.openCommitmentSequences>0],["frontier",o.frontierPoints===o.frontierFirstActionChecks],["no state after bill",step([2,3,1,0],1,1,{income:0,reserve:2,ca:1,cb:1})===null],["no duplicate start",step([6,5,1,0],0,2,{income:0,reserve:0,ca:1,cb:1})===null],["not finished",!terminal([9,5,1,2])]]){ck(test,name);o.controls++}
 return o;
}
console.log(experiment())
```

## 实测
```json
{
  "scenarios": 144,
  "enumeratedSequences": 186624,
  "allLegalSequences": 10664,
  "validSequences": 2274,
  "openCommitmentSequences": 220,
  "reachableOutputChecks": 941,
  "frontierPoints": 397,
  "frontierFirstActionChecks": 397,
  "feasibleScenarios": 107,
  "impossibleScenarios": 37,
  "relaxedFalseFeasible": 0,
  "relaxedExtraOutputs": 126,
  "relaxedExtraFrontierScenarios": 0,
  "immediateTrapScenarios": 49,
  "immediateTrapActions": 63,
  "greedyFailedFeasible": 38,
  "greedyDominatedFeasible": 12,
  "greedyEfficient": 57,
  "peakStates": 86,
  "maxWork": 354,
  "coverageChecks": 144,
  "budgetChecks": 144,
  "controls": 12,
  "witnesses": {
    "trap": {
      "p": {
        "cash": 2,
        "hours": 5,
        "income": 0,
        "reserve": 0,
        "ca": 1,
        "cb": 1
      },
      "immediate": [
        "WAIT",
        "EARN",
        "START_A",
        "START_B"
      ],
      "canComplete": [
        "WAIT",
        "EARN"
      ],
      "frontier": [
        [
          "0,1,0,1",
          3
        ],
        [
          "0,1,3,0",
          2
        ],
        [
          "1,0,0,1",
          3
        ],
        [
          "1,0,3,0",
          2
        ]
      ]
    },
    "greedy": {
      "p": {
        "cash": 2,
        "hours": 5,
        "income": 0,
        "reserve": 0,
        "ca": 1,
        "cb": 1
      },
      "greedy": [
        "START_A"
      ],
      "frontier": [
        [
          "0,1,0,1",
          3
        ],
        [
          "0,1,3,0",
          2
        ],
        [
          "1,0,0,1",
          3
        ],
        [
          "1,0,3,0",
          2
        ]
      ]
    }
  }
}
```

## 下一步
优先把既有决策记录、资源身份、跨期承诺状态、取消/修改/履约证据接入同一可信账本合同；评估新增计划是否改变旧有目标可达前沿及代价，先解决实际语义义务映射再扩展动态不确定性。数据轨、独立验收轨、产品轨责任不变，正式工程及训练另获授权。
