# 第40轮：带成本、含糊回答与拒答分支的有限自主追问
2026-11-24。固定 main 245689c996c0edd79508d57de2e3375e9cd8ae9b；PR #61 HEAD 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，open Draft。已核对v3.1、AGENTS、同步规程、近期提交、开放PR、唯一协调交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第5/27/37/38/39轮。原生decision_planner.py blob f2d3d21b853afe9dc757a33e83cd3d6160f8dd7b已有规则优先级、信息模型补证顺序与行动窗口核查。第5轮最坏追问深度假设确定回答、单位成本、完整签名识别；拒答未纳入其最优保证。第27轮局部分析和第37轮一次确定观察的条件策略均保留。新增有限预算内可停止的多次追问、不同成本、含糊回答的重叠支持、拒答分支和残余决策损失。提交关键词查重未发现相同专项，非全库无重复证明。非现有产品漏洞证明。
## 第39轮来源记录补充
第39轮报告声称当轮实际查看出版商摘要；该轮可核验工具记录未显示实际网络检索，不能据此确认当轮审阅。2026-11-24本轮实际检索出版商公开摘要 https://www.sciencedirect.com/science/article/abs/pii/0004370291900066 ，核对 Dechter, Meiri & Pearl (1991), DOI https://doi.org/10.1016/0004-3702(91)90006-6 ，摘要确认连续变量及单一成对区间的简单时间问题。未阅读全文，不追认历史来源审阅或独立验收。第39轮数学计算记录与原文件保留。
## 数学合同
有限非空联合世界S，固定行动与每世界可信硬约束、共同效用、全信息基准b(w)。终止损失 L(S)=min_{a in intersection F(w)} max_{w in S}[b(w)-u(w,a)]，若无保证可行行动则无穷或独立的安全暂缓出口（若真实存在并有损失依据才纳入）。无论损失多小，必需的底线、授权及重大风险核查仍先于优化。可选问题q的可能回答集合A_q(w)须有语义及证据资格；不同回答可对应重叠的世界集合 S_y={w in S:y in A_q(w)}，不能强制分割或将模糊回答当精确事实。拒答不提供新事实，S保持原样；问题不再自动重复。拒绝整个交互立即停止问询，明确条件/未知，不能替用户授权。用户拒绝隐私采集等重要授权不可视作普通可重复调查。
在非负且同效用单位的确定提问成本c(q)、剩余问题Q、最多剩余h次、响应限制r下，V(S,Q,h,r)=min{L(S), min_q[c(q)+max_y V(S_y,Q\{q},h-1,r_y)]}，h=0时V=L。所有分支均保留；最大化包含所有允许的回答，包括无信息拒答。归纳：任一策略根为停止或一个允许问题，各分支最优余损失由更短树递推，且分支策略可分别选取，故公式最优。前提是响应模型的跨历史限制完整进入状态、成本相加、行动机会和效用不随时间改变、无隐藏状态变化。若允许任意连续拒答，则始终存在完全无信息路径，非负成本下V=L；正成本时停止严格优于追问。这仅意味着没有保证的最坏情景净收益，并不说明自愿回答的条件价值或具有可靠概率时的期望价值为零。不能未经证据假定用户最多拒绝一次；有限拒答为显式假设。没有真实成本/效用尺度时展示多维成本与潜在决策改善或条件阈值，不自动设定偏好。延迟会改变行动集时须另建时序模型。未知世界域不能宣称完整最优树。
## 实验
4个世界（两个二元属性）、安全备选效用4、另一行动每世界效用0/4/8及任意可行位，16*81=1296表。三个问题：两个精确属性、一个含糊奇偶问题（世界3两种答案均允许）；三种成本组，三种拒答条件（无、至多一次、无限制），最多两次问题。DP与独立的整数损失预算可满足性递归核对最优值及其减一的不可满足性。两算法共享人工回答集合与损失定义，非独立验收。myopic基线仅在当下单问严格降低净损失时追问；depthGain为两次上限优于一次上限；ambiguityGap为忽略重叠回答使单次调查成本加残余损失严格低估的表数（1296为分母）；unlimited为任意拒答条件下验证停止；firstCounts只统计严格优于停止时所有并列首问，计数可重叠。合成频数及效用单位非现实概率、真实损失或问询效果。以下原函数本轮实际执行：
```js
function experiment(){
 const check=(v,m)=>{if(!v)throw Error(m)};
 const W=[0,1,2,3],Q=[0,1,2],all=15;
 const worlds=m=>W.filter(w=>m&(1<<w));
 // Third question has overlapping answer support at world 3.
 const replies=[[1,2,1,2],[1,1,2,2],[1,2,2,3]];
 function branches(m,q,r){
  const bs=[];
  for(let a=0;a<2;a++){const n=worlds(m).filter(w=>replies[q][w]&(1<<a)).reduce((s,w)=>s|(1<<w),0);if(n)bs.push([n,r]);}
  if(r!==0)bs.push([m,r===-1?-1:r-1]);
  return bs;
 }
 let cases=0,oracle=0,gains=0,vsMyopic=0,unlimited=0,finiteRefusal=0,ambiguityGap=0,depthGain=0,stops=0,firstCounts=[0,0,0],valueSum=0,baseSum=0,witness=null,refusalWitness=null;
 const costsets=[[1,1,3],[1,2,1],[2,1,2]];
 for(let f=0;f<16;f++)for(let b=0;b<81;b++){
  let z=b;const u=W.map(w=>{const v=(z%3)*4;z=Math.floor(z/3);return v;});
  const best=W.map(w=>Math.max(4,f&(1<<w)?u[w]:-Infinity));
  const loss=(w,a)=>best[w]-(a===0?4:u[w]);
  function terminal(m){return Math.min(...[0,1].filter(a=>a===0||(m&f)===m).map(a=>Math.max(...worlds(m).map(w=>loss(w,a)))));}
  for(const cost of costsets)for(const refusal of [0,1,-1]){
   const memo=new Map();
   function dp(m,qs,h,r){
    const key=[m,qs,h,r].join(",");if(memo.has(key))return memo.get(key);
    let v=terminal(m),first=[];
    if(h)for(const q of Q)if(qs&(1<<q)){
     const t=cost[q]+Math.max(...branches(m,q,r).map(([n,k])=>dp(n,qs^(1<<q),h-1,k).v));
     if(t<v){v=t;first=[q];}else if(t===v)first.push(q);
    }
    const out={v,first,stop:v===terminal(m)};memo.set(key,out);return out;
   }
   // Independent feasibility-of-loss-budget recursion, enumerating terminal actions and possible questions.
   function possible(m,qs,h,r,t){
    for(const a of [0,1])if(worlds(m).every(w=>(a===0||!!(f&(1<<w)))&&loss(w,a)<=t))return true;
    if(h===0)return false;
    return Q.some(q=>(qs&(1<<q))&&t>=cost[q]&&branches(m,q,r).every(([n,k])=>possible(n,qs^(1<<q),h-1,k,t-cost[q])));
   }
   const d=dp(all,7,2,refusal),one=dp(all,7,1,refusal),start=terminal(all);
   check(possible(all,7,2,refusal,d.v)&&!possible(all,7,2,refusal,d.v-1),"exact threshold");oracle+=2;cases++;
   check(d.v<=one.v&&one.v<=start,"optional questions");
   if(d.v<start){gains++;if(refusal===1)finiteRefusal++;}
   if(d.v<one.v){depthGain++;if(!witness&&refusal===0)witness={f,u,cost,start,one,two:d};}
   // Myopic asks only when a single question strictly improves terminal loss, then repeats.
   function greedy(m,qs,h,r){
    let q0=-1,v=terminal(m);if(!h)return v;
    for(const q of Q)if(qs&(1<<q)){
     const t=cost[q]+Math.max(...branches(m,q,r).map(([n])=>terminal(n)));
     if(t<v){v=t;q0=q;}
    }
    return q0<0?terminal(m):cost[q0]+Math.max(...branches(m,q0,r).map(([n,k])=>greedy(n,qs^(1<<q0),h-1,k)));
   }
   const g=greedy(all,7,2,refusal);check(d.v<=g,"greedy bound");
   if(d.v<g)vsMyopic++;
   if(refusal===-1){check(d.v===start&&d.stop&&d.first.length===0,"unlimited refusal");unlimited++;}
   if(refusal===1&&d.v<start&&!refusalWitness)refusalWitness={f,u,cost,start,d};
   if(d.stop)stops++;else for(const q of d.first)firstCounts[q]++;
   valueSum+=d.v;baseSum+=start;
  }
  // False perfect observation assumption for q2 alone; cost 1.
  const trueValue=1+Math.max(...branches(all,2,0).map(([m])=>terminal(m)));
  const perfect=[6,9].map(m=>terminal(m)); // parity 1 worlds 1,2; parity 0 worlds 0,3
  const falseValue=1+Math.max(...perfect);
  check(falseValue<=trueValue,"overlapping response bound");if(falseValue<trueValue)ambiguityGap++;
 }
 // Joint complement: no single bit resolves XOR, two do; third question ambiguous.
 const comp={f:15,u:[0,8,8,0],cost:[1,1,3]};
 // In this case direct robust stop 4; one question cannot improve; two clean bits cost 2.
 check(witness!==null&&vsMyopic>0&&ambiguityGap>0,"nontrivial cases");
 return {cases,oracle,gains,vsMyopic,unlimited,finiteRefusal,ambiguityGap,depthGain,stops,firstCounts,valueSum,baseSum,witness,refusalWitness,complementExample:comp};
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实际结果
```json
{
  "cases": 11664,
  "oracle": 23328,
  "gains": 2040,
  "vsMyopic": 1184,
  "unlimited": 3888,
  "finiteRefusal": 72,
  "ambiguityGap": 108,
  "depthGain": 1184,
  "stops": 9624,
  "firstCounts": [
    1624,
    1428,
    528
  ],
  "valueSum": 19568,
  "baseSum": 23616,
  "witness": {
    "f": 1,
    "u": [
      8,
      0,
      0,
      0
    ],
    "cost": [
      1,
      1,
      3
    ],
    "start": 4,
    "one": {
      "v": 4,
      "first": [],
      "stop": true
    },
    "two": {
      "v": 2,
      "first": [
        0,
        1
      ],
      "stop": false
    }
  },
  "refusalWitness": {
    "f": 7,
    "u": [
      8,
      4,
      4,
      0
    ],
    "cost": [
      1,
      1,
      3
    ],
    "start": 4,
    "d": {
      "v": 2,
      "first": [
        0,
        1
      ],
      "stop": false
    }
  },
  "complementExample": {
    "f": 15,
    "u": [
      0,
      8,
      8,
      0
    ],
    "cost": [
      1,
      1,
      3
    ]
  }
}
```
## 接入和验收
B02/B05/B06/B07/B08/B10候选增量。先由可信中枢检查必要底线、风险、授权、问题是否可答及现有证据可否自行推导；可选问询只在可支持的响应与成本合同下优化。禁止为用户设置强制回答、隐私交换或未确认成本权重。默认允许跳过/不知道/含糊回答，保留原域，重算条件建议，用户明确拒绝继续即停止。先给已有的有用分析；通常只展示一个关键问题，若存在多问互补且用户愿意，说明可能需要下一项核实；达到预算、时间、权限或安全边界即终止。没有回答可靠性证据时展示条件价值，不将“最多一次拒答”当默认现实行为。问题、成本、候选行动、用户确认、响应支持、证据版本及剩余预算绑定收据；修改后重算。重大风险确认不能由低效用成本覆盖。独立轨使用未见多步互补、拒答、模糊回答、错误回答、完全无安全备选、授权撤回、窗口到期与单位不明案例；产品轨测真实用户答题负担及初答价值；模型轨审视联合响应、时间和非同单位成本。未执行原生planner、自然语言、真实Qwen、设备、用户效果或独立验收。无生产修改、CI、Codex、训练、合并、部署、冻结协议变更及新增费用。
