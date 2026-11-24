# 第41轮：有资格的候选行动生成、前缀资源与行动范围更新
2026-11-24。固定 main 1507376849edac68a46f352063a814b0434fd81a；PR #61 HEAD 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，open Draft。核对v3.1、AGENTS、同步规程、近期提交、开放PR、唯一产品交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第2/37/40轮及本会话前轮第39轮。原生源码：main decision_state.py 0840855431fbc88fe212785584277aa01be74d93，options最大24；PR61 decision_language.py fff9d6c8e20c6a57c4ae9756bf5d6fe0e81f61b4、decision_local_ai.py 726b7a2e0da64af7037d892ac8bf508412deb5d6（prompt明确原文逐字候选）、decision_conversation.py f505aeab2d9e5e0a9c8957ce6e039dea174918a7（confirm/select/plan入口）。审查仅这些固定文本锚点，未运行原生入口；不将生成新行动与原文提取混为一谈，不断言产品无任何其他建议能力。查询alternative generation/candidate generation/option expansion/action synthesis/branch and bound提交关键词无结果，非全库无重复证明。新增从已确认行动原语合成方案、阶段资源可行性、未知资格保留、候选范围修订后的后悔基准。纯原创有限模型和公开虚构数据，不新增外部来源事实。
## 数学合同
有限行动原语a，每项最多执行一次，固定现金增量d(a)，前置集合P(a)，单位步时，明确资格 yes/no/unknown；同一预算币种及时域。现金起点C>=0，最多h步，禁止任何前缀现金为负。模型不允许隐性借款、透支或收入提前兑现。状态为已完成动作集合S；现金C+sum_{a in S}d(a)、时间|S|、终端共同效用U(S)均由集合决定；只有动作a未执行、已获资格、P(a)⊆S、下一状态现金非负且时间不超限时可扩展。开始空状态仅为搜索根；实验假定停止/维持现状也是合法备选，现实无此保证需另验。只要这些充分状态假设成立，同一S的任意合法到达序列对未来可行性和终值等价，故每S记录一条见证并穷举可达集合足够；对路径深度归纳，任一合法序列的前缀状态均会被访问，每个扩展又是合法序列。若收益、现金流时点、疲劳、次序、不可逆副作用、时窗或历史依赖未入状态，合并状态不合法。每个状态的见证不是全部可行顺序，也不能替用户选定行动。
资格不确定时，先以yes集合生成已确认域，再以yes+unknown生成明确标记的条件域。本轮假定未知资格可独立取真或假、固定且执行时不改变，其他量和关系固定；全部补全的交集等于只用yes的可达终态，全部补全的并集等于yes+unknown的可达终态。原因是动作许可单调扩大，不会删除旧路径，而且最小和最大补全均存在。联合资格互斥时，最大补全可能不存在，后一结论失效；应使用真实联合域或保守外界，不得把条件生成的计划推荐为已可行。新增方案的现实存在性、作用、可用时间、资格和收益均需独立确认，禁止LLM编造承诺或收益。生成范围有界，只能声明所列原语、规则、步数内穷尽；超时/截断/未知原语均明确未穷尽。
终端总现金非负和前置集合最终包含只是必要条件，不能替代各阶段可行性。若前置行动先耗尽现金且后续行动才回款，终端余额可能合格却无法实施。候选集合扩大时，固定同目标/效用/可行性下最大效用不下降；但最小最大后悔的每情景最优参照随候选集变化，旧行动的相对排序可以反转。因此必须区分原始范围的历史收据与新范围计算，不直接比较不同基准下的后悔值，更新可行性、排序、信息价值、解释、图表和确认快照。不能把用户否决的行动再次加入活动范围，除非用户重新授权。
## 实际执行
3个原语，27种现金增量(-1/0/1)，8种有向无环前置图（0->1、0->2、1->2可选），27种资格三值组合，3个起始余额，3个时间上限；每行动固定正效用1/2/4，集合加和。共52488组；逐状态生成与完整16个无重复序列（含空序列）在每个资格补全上逐步重放对照。两路径同一研究者设计，非独立验收。safe/poss各保留一个见证，核对前缀。confirmedPlans/possiblePlans含空状态，跨情景重复不表示独立现实方案；possibleOnly是条件域差集。improved是生成复合行动后最优效用严格超过仅已可行单动作/空行动的有限例数；noSingle是单动作无正效用时仍获得复合正效用，理论上在本实验正效用及前缀可行规则下应为0（任何合法复合计划首步可行），不冒称发现无中生有。aggregateFalse是终态筛查误放行的状态数，aggregateCases为含至少一误放行状态的例数。没有真实效用、现实成功率、实际自然语言或自主候选发现率。
```js
function experiment(){
 const check=(v,m)=>{if(!v)throw Error(m)};
 const A=[0,1,2],pop=m=>A.filter(a=>m&(1<<a)).length;
 const bits=m=>A.filter(a=>m&(1<<a));
 const subsets=Array.from({length:8},(_,i)=>i);
 const sum=(m,values)=>bits(m).reduce((s,a)=>s+values[a],0);
 const utility=m=>sum(m,[1,2,4]);
 function discover(delta,pre,allow,cash,h){
  const found=new Map([[0,[]]]),queue=[0];
  for(let i=0;i<queue.length;i++){
   const m=queue[i];if(pop(m)>=h)continue;
   for(const a of A){
    const b=1<<a,n=m|b;
    if((m&b)||!(allow&b)||(m&pre[a])!==pre[a]||cash+sum(n,delta)<0)continue;
    if(!found.has(n)){found.set(n,[...found.get(m),a]);queue.push(n);}
   }
  }return found;
 }
 // Independent brute force actual ordered actions, replay step by step.
 const orders=[[]];
 function gen(p){for(const a of A)if(!p.includes(a)){const n=[...p,a];orders.push(n);gen(n);}}gen([]);
 function replay(p,delta,pre,allow,cash,h){
  if(p.length>h)return null;
  let balance=cash,m=0;
  for(const a of p){const b=1<<a;if(!(allow&b)||m&b||(m&pre[a])!==pre[a])return null;
   balance+=delta[a];if(balance<0)return null;m|=b;
  }return m;
 }
 const eq=(a,b)=>a.length===b.length&&a.every(v=>b.includes(v));
 let cases=0,oracleChecks=0,witnessChecks=0,completionChecks=0,improved=0,noSingle=0,unknownCases=0,aggregateFalse=0,aggregateCases=0,possibleOnly=0,confirmedPlans=0,possiblePlans=0,earlyImprovement=null,unsafeWitness=null,unknownWitness=null;
 for(let code=0;code<27;code++){
  let t=code;const delta=A.map(()=>{const v=t%3-1;t=Math.floor(t/3);return v;});
  for(let graph=0;graph<8;graph++){
   const pre=[0,graph&1?1:0,(graph&2?1:0)|(graph&4?2:0)];
   for(let qual=0;qual<27;qual++){
    let z=qual,yes=0,maybe=0;const state=A.map(a=>{const v=z%3;z=Math.floor(z/3);if(v===2)yes|=1<<a;if(v!==0)maybe|=1<<a;return v;});
    const completions=subsets.filter(m=>(m&yes)===yes&&(m&maybe)===m);
    for(let cash=0;cash<=2;cash++)for(let h=1;h<=3;h++){
     cases++;
     const safe=discover(delta,pre,yes,cash,h),poss=discover(delta,pre,maybe,cash,h);
     const ss=[...safe.keys()],ps=[...poss.keys()];
     confirmedPlans+=ss.length;possiblePlans+=ps.length;
     const allSets=completions.map(m=>{const p=orders.map(o=>replay(o,delta,pre,m,cash,h)).filter(v=>v!==null);oracleChecks+=orders.length;completionChecks++;return [...new Set(p)];});
     const intersection=subsets.filter(m=>allSets.every(s=>s.includes(m)));
     const union=subsets.filter(m=>allSets.some(s=>s.includes(m)));
     check(eq(ss,intersection)&&eq(ps,union),"scope oracle");
     for(const [m,p] of safe){check(replay(p,delta,pre,yes,cash,h)===m,"safe witness");witnessChecks++;}
     for(const [m,p] of poss){check(replay(p,delta,pre,maybe,cash,h)===m,"conditional witness");witnessChecks++;}
     const only=ps.filter(m=>!safe.has(m));possibleOnly+=only.length;
     if(only.length){unknownCases++;if(!unknownWitness)unknownWitness={delta,pre,state,cash,h,confirmed:ss,conditional:only};}
     const one=Math.max(...ss.filter(m=>pop(m)<=1).map(utility)),best=Math.max(...ss.map(utility));
     if(best>one){improved++;if(one===0)noSingle++;if(!earlyImprovement)earlyImprovement={delta,pre,state,cash,h,one,best,plan:safe.get(ss.find(m=>utility(m)===best))};}
     // Incorrect aggregate-only baseline: all terminal resources and prerequisite inclusion, no sequence check.
     const aggregate=subsets.filter(m=>(m&yes)===m&&pop(m)<=h&&cash+sum(m,delta)>=0&&bits(m).every(a=>(m&pre[a])===pre[a]));
     check(ss.every(m=>aggregate.includes(m)),"aggregate outer");
     const falsePlans=aggregate.filter(m=>!safe.has(m));aggregateFalse+=falsePlans.length;
     if(falsePlans.length){aggregateCases++;if(!unsafeWitness)unsafeWitness={delta,pre,state,cash,h,aggregate,falsePlans};}
    }
   }
  }
 }
 // For same scope, adding actions cannot lower best utility; changing regret benchmark can reverse old rankings.
 function regret(u){const b=[0,1].map(w=>Math.max(...u.map(a=>a[w])));return u.map(a=>Math.max(...a.map((v,w)=>b[w]-v)));}
 const old=[[3,0],[1,2]],expanded=[...old,[0,6]];
 const oldR=regret(old),newR=regret(expanded);
 check(oldR[0]===2&&oldR[1]===2,"old tie"); // separate strict reversal below
 const reversal={old:[[4,0],[1,2]],new:[[4,0],[1,2],[0,7]]};
 reversal.oldR=regret(reversal.old);reversal.newR=regret(reversal.new);
 // old A:2 B:3; expanded A:7 B:5 C:4.
 check(reversal.oldR[0]<reversal.oldR[1]&&reversal.newR[0]>reversal.newR[1],"old pair regret reversal");
 // Truncating expansion cannot certify exhaustion.
 check(orders.length===16&&aggregateCases>0&&improved>0&&unknownCases>0,"coverage");
 return {cases,oracleChecks,completionChecks,witnessChecks,confirmedPlans,possiblePlans,possibleOnly,unknownCases,improved,noSingle,aggregateCases,aggregateFalse,earlyImprovement,unsafeWitness,unknownWitness,reversal};
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实际结果
```json
{
  "cases": 52488,
  "oracleChecks": 1990656,
  "completionChecks": 124416,
  "witnessChecks": 219555,
  "confirmedPlans": 85883,
  "possiblePlans": 133672,
  "possibleOnly": 47789,
  "unknownCases": 25928,
  "improved": 4909,
  "noSingle": 0,
  "aggregateCases": 133,
  "aggregateFalse": 145,
  "earlyImprovement": {
    "delta": [
      -1,
      -1,
      -1
    ],
    "pre": [
      0,
      0,
      0
    ],
    "state": [
      2,
      2,
      0
    ],
    "cash": 2,
    "h": 2,
    "one": 2,
    "best": 3,
    "plan": [
      0,
      1
    ]
  },
  "unsafeWitness": {
    "delta": [
      -1,
      1,
      -1
    ],
    "pre": [
      0,
      1,
      0
    ],
    "state": [
      2,
      2,
      0
    ],
    "cash": 0,
    "h": 2,
    "aggregate": [
      0,
      3
    ],
    "falsePlans": [
      3
    ]
  },
  "unknownWitness": {
    "delta": [
      -1,
      -1,
      -1
    ],
    "pre": [
      0,
      0,
      0
    ],
    "state": [
      1,
      0,
      0
    ],
    "cash": 1,
    "h": 1,
    "confirmed": [
      0
    ],
    "conditional": [
      1
    ]
  },
  "reversal": {
    "old": [
      [
        4,
        0
      ],
      [
        1,
        2
      ]
    ],
    "new": [
      [
        4,
        0
      ],
      [
        1,
        2
      ],
      [
        0,
        7
      ]
    ],
    "oldR": [
      2,
      3
    ],
    "newR": [
      7,
      5,
      4
    ]
  }
}
```
## 接入
B02/B05/B06/B07/B08/B10候选增量。自然语言中枢应明确区分用户原始选项、外部证据发现的可能机会、系统组合推导和纯假设提议。按目标主动考虑维持现状、分阶段、缩小规模、先验证、替代资源及合法混合行动；这些只是搜索方向，不能自动生成事实或改变底线。每条新方案记录原语、来源、资格、前置、资源时间、风险、路径见证、生成规则及范围版本。先筛查真实可行性，再展示具有实质增量的少量备选并允许用户拒绝或扩展；无共同效用时不作总排序，用户未确认的新方案不进入最终行动建议。选择、授权和实际执行分离。状态合并需要充分性证书，预算不足仅输出部分候选及未穷尽。独立轨冻结未见资源跨期、不同顺序结果、互斥资格、未知收益、重复生成、范围更正、所有选择不可行及拒绝案例；产品轨评估是否减少遗漏及操作负担；模型轨审阅非加性、多资源和状态依赖扩展。未运行正式原生方法、Qwen、真实数据、Mac/iPhone、独立验收或完整端到端。无生产修改、Codex、CI、训练、PR合并、部署、冻结协议变更及新增费用。
