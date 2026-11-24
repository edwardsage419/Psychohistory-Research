# 第37轮：联合情景可行性与无概率条件决策的后悔值组合
2026-11-24。固定 main a6440d99b24a8b5972de8983959c4364cef4a411；PR #61 HEAD 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，open Draft。核对v3.1、AGENTS、同步规程、近期提交/开放PR、唯一产品交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第4/6/27/31/33/34/36轮。原生源码审阅：decision_feasibility.py 6181d6c578c7ef251e9708d0ffcf65e95d35f88f；decision_regret.py e56689a54897d95eaa126540c23fca51cc0eede7；decision_voi.py a69571fcf6df9a779ed317e76c5dcac6933d2728；decision_timing.py 4ed9fa430dcb993cc5005656c8b1744276fe7c33。现有regret、voi、timing使用ctx.feasible；VOI及timing已有信号行动范围及期望价值研究。本轮不重计矩形区间、概率VOI、单次追问或依赖门控，新增的是同一联合情景身份下的条件可行集、不可预知状态的策略、无概率最坏后悔值及其比较基准。非原生方法缺陷证明，C035/C036仍保持候选。
## 数学合同
有限、非空且用户/可信来源确认覆盖的联合世界集合W；行动A；每世界硬约束可行集F(w)，共同效用u(w,a)（只对可行动有决策意义）；观察将W分成非空互斥且穷尽的单元C。观察须在行动前可靠区分单元，不得区分单元内部真实世界。无现实概率假设。硬约束未知需保留UNKNOWN或用有资格的保守可行集；不得把未知当失败事实或用虚构世界替代无界未知。
每世界的全信息可行基准 b(w)=max_{a in F(w)} u(w,a)。固定行动须属于所有世界F的交集；条件策略pi(C)须属于该单元的交集 S(C)=intersection_{w in C} F(w)。若任何S为空，则不存在保证通过底线的该类策略，不能以不安全行动填空。若每F非空且每S非空，损失 r(w,a)=b(w)-u(w,a)，最坏后悔最优值 R(P)=max_{C in P} min_{a in S(C)} max_{w in C} r(w,a)。证明：任一合法策略在每单元的最坏损失至少为单元最小值；逐单元选择最小值的行动同时达到上界，故相等。必须保存所有最优集合；单元局部最小值策略是一个全局最优构造，但并非所有全局最优策略都逐单元最优。全局最优策略恰好各单元安全且其局部最大损失不超过R(P)。
相同世界、效用与行动时限下，细化观察分区只扩大可实施策略类，R不增。无成本全信息下R=0。即时策略为单单元。若调查有共同固定效用成本c且不改变世界/行动可行集、收益或期限，则以原始即时/全信息基准比较的最坏后悔改善为R(immediate)-R(P)-c；严格正才是该准则下的改善。延迟、状态依赖成本、观察误差、行为机会变化须另建联合世界和策略；不得调用概率信息价值模型冒充。限制基准为全局稳健可行动集会缩小机会损失，可能把有价值的信息显示为无价值；该基准也可用于其他明确问题，但不可混用。最坏后悔不是期望收益、成功概率或用户默认价值准则。若效用未确认只能展示条件可行性，不生成数值排序。
## 执行
本轮工具实际运行下列JS函数。3个世界、3行动（第0行动始终可行），6个可行位、9个二元效用位，所有64*512表，5种分区。未可行的效用仅为占位数，不计入安全基准或策略；错误的union对照故意允许这些占位数参与损失，属于明确的不安全基线。候选公式以逐单元交集计算，并逐个枚举3^k完整策略验证安全及最坏后悔，两条路径同一研究者设计、非独立验收。unionRisk统计至少一个单元局部最优候选不安全（包括并列）；unionForced统计至少一个单元所有局部最优候选均不安全。不是现有产品真实错误计数或概率。restrictedComparatorUnderstates为即时稳健基准比全信息可行基准少报最坏后悔的表数。局部最优代表策略仅供测试；产品不可擅自从并列选择替用户决定。全部公开虚构。
```js
function experiment(){
 const check=(x,m)=>{if(!x)throw Error(m)};
 const partitions=[[[0,1,2]],[[0],[1,2]],[[1],[0,2]],[[2],[0,1]],[[0],[1],[2]]];
 const A=[0,1,2],W=[0,1,2];
 function solve(u,f,part){
  const oracle=W.map(w=>Math.max(...A.filter(a=>f[w][a]).map(a=>u[w][a])));
  const cells=part.map(cell=>{
   const safe=A.filter(a=>cell.every(w=>f[w][a]));
   const union=A.filter(a=>cell.some(w=>f[w][a]));
   const loss=a=>Math.max(...cell.map(w=>oracle[w]-u[w][a]));
   const v=Math.min(...safe.map(loss)),vUnion=Math.min(...union.map(loss));
   return {safe,v,leaders:safe.filter(a=>loss(a)===v),unionLeaders:union.filter(a=>loss(a)===vUnion)};
  });
  const r=Math.max(...cells.map(c=>c.v));
  const safePolicy=part.map((_,i)=>cells[i].leaders[0]);
  // Independent brute force all 3^k policies, reject if any action violates a world.
  let exact=Infinity,valid=0;
  function enumP(p){
   if(p.length===part.length){
    let m=0;
    for(let j=0;j<part.length;j++)for(const w of part[j]){
     const a=p[j];if(!f[w][a])return;
     const best=A.reduce((b,k)=>f[w][k]?Math.max(b,u[w][k]):b,-Infinity);
     m=Math.max(m,best-u[w][a]);
    }
    valid++;exact=Math.min(exact,m);return;
   }
   for(const a of A)enumP([...p,a]);
  }enumP([]);
  check(r===exact,"brute force");
  const unsafeUnion=cells.some(c=>c.unionLeaders.some(a=>!c.safe.includes(a)));
  const allUnionUnsafe=cells.some(c=>c.unionLeaders.every(a=>!c.safe.includes(a)));
  return {r,valid,unsafeUnion,allUnionUnsafe,safePolicy};
 }
 let n=0,strict=0,unionRisk=0,unionForced=0,fullInfo=0,partialStrict=0,partialN=0,validPolicies=0,oracleGap=0;
 let witness=null,forcedWitness=null;
 // Action 0 is guaranteed feasible, other 6 feasibility bits arbitrary; 9 binary utilities.
 for(let mask=0;mask<64;mask++){
  const f=W.map(w=>[true,!!(mask&(1<<(2*w))),!!(mask&(1<<(2*w+1)))]);
  for(let bits=0;bits<512;bits++){
   const u=W.map(w=>A.map(a=>(bits>>(3*w+a))&1));
   const b=solve(u,f,partitions[0]).r;
   const robust=A.filter(a=>W.every(w=>f[w][a]));
   const restricted=Math.min(...robust.map(a=>Math.max(...W.map(w=>Math.max(...robust.map(k=>u[w][k]))-u[w][a]))));
   check(restricted<=b,"restricted comparator");
   if(restricted<b)oracleGap++;
   for(let i=0;i<partitions.length;i++){
    const s=solve(u,f,partitions[i]);n++;validPolicies+=s.valid;
    check(s.r<=b,"information monotonicity");
    if(s.r<b){strict++;if(i>0&&i<4){partialStrict++;if(!witness)witness={u,f,partition:partitions[i],immediate:b,conditional:s.r,policy:s.safePolicy};}}
    if(i>0&&i<4)partialN++;
    if(s.unsafeUnion)unionRisk++;
    if(s.allUnionUnsafe){unionForced++;if(!forcedWitness)forcedWitness={u,f,partition:partitions[i],safeRegret:s.r};}
    if(i===4){check(s.r===0,"perfect information");fullInfo++;}
   }
  }
 }
 // If an observation cell has empty safe intersection, no guaranteed feasible policy.
 const noFallback=[[true,false],[false,true]];
 const noSafe=[0,1].filter(a=>noFallback.every(w=>w[a]));
 check(noSafe.length===0,"no safe action");
 // Counterexample: action0 safe utility0; action1 available only w0, action2 only w1; each yields 1.
 const example={u:[[0,1,0],[0,0,1],[0,0,1]],f:[[true,true,false],[true,false,true],[true,false,true]]};
 const immediate=solve(example.u,example.f,partitions[0]);const informed=solve(example.u,example.f,partitions[1]);
 check(immediate.r===1&&informed.r===0,"example");
 return {worldTables:64*512,partitionCases:n,partialCases:partialN,strictReduction:strict,partialStrict,unionRisk,unionForced,fullInfoZero:fullInfo,validPolicies,restrictedComparatorUnderstates:oracleGap,noFallbackSafeActions:noSafe,example:{...example,immediate,observed:informed,partition:partitions[1]},witness,forcedWitness};
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实际结果
```json
{
  "worldTables": 32768,
  "partitionCases": 163840,
  "partialCases": 98304,
  "strictReduction": 35784,
  "partialStrict": 20598,
  "unionRisk": 68850,
  "unionForced": 22362,
  "fullInfoZero": 32768,
  "validPolicies": 598016,
  "restrictedComparatorUnderstates": 12960,
  "noFallbackSafeActions": [],
  "example": {
    "u": [
      [
        0,
        1,
        0
      ],
      [
        0,
        0,
        1
      ],
      [
        0,
        0,
        1
      ]
    ],
    "f": [
      [
        true,
        true,
        false
      ],
      [
        true,
        false,
        true
      ],
      [
        true,
        false,
        true
      ]
    ],
    "immediate": {
      "r": 1,
      "valid": 1,
      "unsafeUnion": true,
      "allUnionUnsafe": false,
      "safePolicy": [
        0
      ]
    },
    "observed": {
      "r": 0,
      "valid": 4,
      "unsafeUnion": false,
      "allUnionUnsafe": false,
      "safePolicy": [
        1,
        2
      ]
    },
    "partition": [
      [
        0
      ],
      [
        1,
        2
      ]
    ]
  },
  "witness": {
    "u": [
      [
        0,
        1,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        0,
        0
      ]
    ],
    "f": [
      [
        true,
        true,
        false
      ],
      [
        true,
        false,
        false
      ],
      [
        true,
        false,
        false
      ]
    ],
    "partition": [
      [
        0
      ],
      [
        1,
        2
      ]
    ],
    "immediate": 1,
    "conditional": 0,
    "policy": [
      1,
      0
    ]
  },
  "forcedWitness": {
    "u": [
      [
        0,
        1,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        0,
        0
      ]
    ],
    "f": [
      [
        true,
        true,
        false
      ],
      [
        true,
        false,
        false
      ],
      [
        true,
        false,
        false
      ]
    ],
    "partition": [
      [
        0,
        1,
        2
      ]
    ],
    "safeRegret": 1
  }
}
```
## 模型组合接口候选
1 语义/证据层给出同一联合域身份、世界及观察范围、单位、确认效用、风险、可行集及时间；缺乏完整域资格时不运行精确模式。
2 可行性方法输出每世界硬约束判定与来源；单元按交集构造安全行动，禁止按并集放行。候选研究需独立验收才能扩展现有全局gate，不能绕过它。
3 后悔值方法计算每世界全信息可行基准及各策略损失，另保留全局固定行动基准（不同合同）；观察分区方法检查不可预知状态与非空单元，并保存所有并列策略资格。
4 信息/时机层只在同效用尺度和观察成本、时限条件有证据时比较净改善；概率证据缺失仍可输出无概率最坏后悔值。用户未选择该准则时显示为条件比较，与期望价值、最大最小效用并列且不平均。
5 用户界面以“现有信息下能安全选择什么；核实哪项信息后可新增哪些安全选择；是否值得核实”展示，说明条件和可逆备选。所有输出绑定联合域版本、行动集、效用、可行性及观察身份；任一变更令相应结果失效。
下一责任：模型轨核查实际可行域、观察成本、延迟和鲁棒准则，独立轨冻结未见情节（含无安全备选、观察误判、并列全局最优、相关联合域与期限变化）；产品轨核查白话初答与清晰图文。本轮是B05/B06/B07/B10研究增量，纳入完整版本候选，不独立启动Codex，不准入新方法。无真实数据、概率、真实Qwen或iPhone、原生完整入口、独立科学验收、生产修改、CI、训练、合并、部署、冻结变更及新增费用。复算为同源合成实验。
