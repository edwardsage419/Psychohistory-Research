# 第42轮：长期路径的鲁棒可行域、动态反馈与未来选择空间
2026-11-24。固定 main dc71c5e3fa814d70f0f74e6cf6fdb22e82fec9ef；PR #61 HEAD 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，open Draft。核对v3.1、AGENTS、同步规程、近期提交/开放PR、唯一产品交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第33/37/40/41轮。原生 decision_timing.py blob 4ed9fa430dcb993cc5005656c8b1744276fe7c33 已有立即、等待、现状、调查时机、可逆性和行动到期；不宣称原生完全无时序分析。查重发现历史R258正式报告（固定提交30a6e4c47eb0d93b88302e2cd217a1f0e4efb0f1）已有三阶段随机有限状态控制、期望成本Bellman与开环/反馈穷举；C009（固定提交829c49c43a5b48060aeb05dbc8591b6c437fe453）已有等待信息价值、可逆性与跨期偏好。仅阅读两份历史报告用于去重，不开展或改写R258、不复验其冻结结果或重新计为成果。第41轮是确定性原语合成，第37/40轮是固定世界的观察与追问。此轮新增无概率的逐阶段扰动集合、路径与终端硬约束、保证可行的反馈策略及完整首行动集合，保留相关轨迹反例。原创新有限模型，无外部文献新增主张。
## 数学合同
有限时域H，有限且当期可观察的充分状态s，阶段硬约束K_t与终端目标集合G⊆K_H；当前行动A_t(s)已确认可实施，随后环境在非空集合T_t(s,a)内实现下一状态，决策者不能预见本期尚未实现的扰动。非空集合必须有来源/适用期及联合支持依据。阶段效用r_t(s,a)与终端效用g(s)在同一用户确认尺度；本实验无折现且终端效用0，终端目标是硬条件。未知效用可只算可行域，不作排序。无概率、无因果估计、无真实人生成功率。关键假设：条件于充分状态的所有允许扰动可在每一阶段发生，未来支持不依赖遗漏的历史；即这里的逐阶段组合域，不自动适用于固定潜在情景或相关冲击。
定义可生存集合K*_H=G，K*_t={s∈K_t:存在a∈A_t(s), T_t(s,a)⊆K*_{t+1}}。只要状态属于该集合，存在满足所有路径及最终底线的反馈策略；证明由终端条件和逆向归纳。最优价值V_H=g于G，域外为负无穷；V_t(s)=max_a[r_t(s,a)+min_{s'∈T_t(s,a)} V_{t+1}(s')]（s∈K_t且有行动），其余负无穷。负无穷表示无保证合格策略，不是现实效用为负无穷。每一步在所有合法行动之间比较，环境选最不利的后续状态，保留全部并列首行动；归纳证明这是给定逐阶段组合域和完整观察下的最优最坏累计效用。安全门先于优化，不把不可行当有限惩罚。若存在可能路径而无保证策略，标明条件性、缺口及可能的安全替代；不能将保证失败解释为一定失败。开放式人生不存在默认终点，H、底线、阶段效用、终端目标和折现需用户确认；延长时域或修改目标需要重新计算，不自动声称最优人生。
当前行动可通过下一阶段安全门却失去更远期目标，需报告不可逆机会损失。预先固定开环计划是反馈策略的子集；反馈允许未来只依据当时已观察状态调整，故最坏最优值不低于开环，未必严格优于。选择空间大小不是福利，只有结合用户目标、可行性和成本才能定价值。若未来状态不能观察，须将可辨识信息集及其联合支持加入状态，不能使用本轮全观察反馈结果。
## 实验
3状态（0、1安全，2违反底线），每安全状态2行动，4种非空转移支持{0},{1},{0,1},{0,1,2}各自赋予4个状态行动对；16种阶段效用表（0/2），3种非空终端安全目标集合，两种初始状态，固定三阶段，共24576例。逐阶段递推与独立穷举64个确定性反馈表（2^(2*3)，危险状态不继续）、逐路径验证全部允许结果与累计收益；8个固定开环表同样回放；同时比较只看下一期安全与当前最高效用的基线（并列取低ID，无立即安全行动时标失败或执行其失败路径）。firstChecks检查所有最优首行动，不以单一代表代替并列。terminalVisits为所有策略（含开环和贪心）的终端调用数，排除提前进入危险状态的调用，可能含终端目标不达；并非独立实际人生轨迹。feedbackOnly为存在保证反馈但无保证开环；feedbackBetter为两者均保证而反馈严格优于；myopicUnsafe是可保证问题上该固定贪心策略未能保证完成路径/终端底线（含目标未达到）；myopicWorse为同样合格但价值较低；immediateTrap是下一期安全的首行动中存在无保证全程完成的动作。possibleNotGuaranteed仅为存在一条合法成功路径、但无保证反馈策略。计算两路径由同一研究者设计，非独立验收。
固定潜在情景反例：两期收益路径只有(0,2)或(2,0)，真实限定域累计下界2；如果无依据独立组合每期支持，会加入(0,0)，下界变0。不得将外界保守值称为可达真实最坏值；状态充分性及共同历史支持须另验。额外虚构两阶段例用于展示当前奖励6但终端不可行、投资当前奖励2且后续5或8时保证总值7的条件逻辑，非生产求解器输出。
```js
function experiment(){
 const check=(v,m)=>{if(!v)throw Error(m)};
 const safe=[0,1],actions=[0,1],out=m=>[0,1,2].filter(s=>m&(1<<s)),N=-Infinity,H=3;
 let cases=0,policies=0,paths=0,viable=0,noGuarantee=0,possibleNotGuaranteed=0,feedbackOnly=0,feedbackBetter=0,myopicUnsafe=0,myopicWorse=0,strictValue=0,immediateTrap=0,firstChecks=0;
 let witness=null,trap=null;
 for(let code=0;code<256;code++){
  let z=code;const trans=safe.map(()=>actions.map(()=>{const v=[1,2,3,7][z%4];z=Math.floor(z/4);return out(v)}));
  for(let r=0;r<16;r++){
   const reward=safe.map(s=>actions.map(a=>2*((r>>(2*s+a))&1)));
   for(let target=1;target<=3;target++){
    const goal=s=>s<2&&!!(target&(1<<s));
    const dp=[[goal(0)?0:N,goal(1)?0:N,N]],leaders=[[]];
    for(let h=1;h<=H;h++){
     const row=safe.map(s=>actions.map(a=>reward[s][a]+Math.min(...trans[s][a].map(n=>dp[h-1][n]))));
     dp.push([...row.map(x=>Math.max(...x)),N]);
     leaders.push(row.map(x=>Math.max(...x)===N?[]:actions.filter(a=>x[a]===Math.max(...x))));
    }
    // Independent exhaustive enumeration of full feedback tables and terminal outcomes.
    function evaluate(policy,s,t,total=0){
     if(s===2)return N;
     if(t===H){paths++;return goal(s)?total:N;}
     const a=policy(t,s);
     return Math.min(...trans[s][a].map(n=>evaluate(policy,n,t+1,total+reward[s][a])));
    }
    function exists(s,t){return s!==2&&(t===H?goal(s):actions.some(a=>trans[s][a].some(n=>exists(n,t+1))));}
    for(const s of safe){
     cases++;
     let best=N,bestFirst=[N,N];
     for(let mask=0;mask<64;mask++){
      const policy=(t,x)=>(mask>>(2*t+x))&1;
      const v=evaluate(policy,s,0);policies++;
      best=Math.max(best,v);const a=policy(0,s);bestFirst[a]=Math.max(bestFirst[a],v);
     }
     check(dp[H][s]===best,"feedback value");
     check(leaders[H][s].join()===actions.filter(a=>best!==N&&bestFirst[a]===best).join(),"all first leaders");firstChecks++;
     let open=N;
     for(let mask=0;mask<8;mask++)open=Math.max(open,evaluate((t)=>((mask>>t)&1),s,0));
     check(best>=open,"open-loop subset");
     if(best===N){noGuarantee++;if(exists(s,0))possibleNotGuaranteed++;continue;}
     viable++;
     if(open===N){feedbackOnly++;if(!witness)witness={trans,reward,target,start:s,feedback:best,open:"NO_GUARANTEE",first:leaders[H][s]};}
     else if(best>open)feedbackBetter++;
     // Myopic baseline: max immediate reward among actions with next-state safety; tie lower ID.
     const greedy=(t,x)=>{const a=actions.filter(a=>trans[x][a].every(n=>n<2));return a.length?a.reduce((b,k)=>reward[x][k]>reward[x][b]?k:b):0};
     const g=evaluate(greedy,s,0);check(best>=g,"greedy subset");
     if(g===N)myopicUnsafe++;else if(g<best)myopicWorse++;
     if(g<best)strictValue++;
     const lost=actions.filter(a=>trans[s][a].every(n=>n<2)&&bestFirst[a]===N);
     if(lost.length){immediateTrap++;if(!trap)trap={trans,reward,target,start:s,viableFirst:leaders[H][s],traps:lost};}
    }
   }
  }
 }
 // Explicit two-period life-path illustration, common score and hard terminal reserve.
 // Initial choices: spend reserve now for reward 6, or invest for reward 2.
 // Invest leaves a choice between later reward 5 (low state) or 8 (high state).
 const example={immediateCommit:{reward:6,terminalFeasible:false},invest:{reward:2,continuations:[5,8],guaranteedTotal:7}};
 check(example.invest.guaranteedTotal===2+Math.min(...example.invest.continuations),"example");
 // Fixed hidden regime has anticorrelated payoffs; rectangularization adds impossible low-low trajectory.
 const correlated=[[0,2],[2,0]],rectangle=[[0,0],[0,2],[2,0],[2,2]];
 const lower=x=>Math.min(...x.map(v=>v[0]+v[1]));
 check(lower(correlated)===2&&lower(rectangle)===0,"joint trajectory counterexample");
 return {cases,policies,terminalVisits:paths,firstChecks,viable,noGuarantee,possibleNotGuaranteed,feedbackOnly,feedbackBetter,myopicUnsafe,myopicWorse,strictValue,immediateTrap,witness,trap,example,correlation:{fixedRegimeLower:2,rectangularLower:0}};
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实际输出
```json
{
  "cases": 24576,
  "policies": 1572864,
  "terminalVisits": 6474880,
  "firstChecks": 24576,
  "viable": 14272,
  "noGuarantee": 10304,
  "possibleNotGuaranteed": 9728,
  "feedbackOnly": 256,
  "feedbackBetter": 524,
  "myopicUnsafe": 2752,
  "myopicWorse": 468,
  "strictValue": 3220,
  "immediateTrap": 1856,
  "witness": {
    "trans": [
      [
        [
          0,
          1
        ],
        [
          0,
          1,
          2
        ]
      ],
      [
        [
          0,
          1,
          2
        ],
        [
          0
        ]
      ]
    ],
    "reward": [
      [
        0,
        0
      ],
      [
        0,
        0
      ]
    ],
    "target": 3,
    "start": 0,
    "feedback": 0,
    "open": "NO_GUARANTEE",
    "first": [
      0
    ]
  },
  "trap": {
    "trans": [
      [
        [
          0,
          1
        ],
        [
          1
        ]
      ],
      [
        [
          0
        ],
        [
          0
        ]
      ]
    ],
    "reward": [
      [
        0,
        0
      ],
      [
        0,
        0
      ]
    ],
    "target": 2,
    "start": 0,
    "viableFirst": [
      1
    ],
    "traps": [
      0
    ]
  },
  "example": {
    "immediateCommit": {
      "reward": 6,
      "terminalFeasible": false
    },
    "invest": {
      "reward": 2,
      "continuations": [
        5,
        8
      ],
      "guaranteedTotal": 7
    }
  },
  "correlation": {
    "fixedRegimeLower": 2,
    "rectangularLower": 0
  }
}
```
## 接入
B05/B06/B07/B08/B10研究增量。自然语言先识别时间范围、各阶段可观测状态、资源/义务、不可逆条件与用户终端目标；证据层验证转移支持和状态充分性，缺失保持UNKNOWN。模型层先计算可保证的路径与首行动集合，后按用户确认准则计算价值；风险层单列可能成功但无法保证、早期安全却失去终端选择、固定计划与动态修订、相关轨迹和有限时域边界。显示当前建议、分支触发条件、下一回顾节点、退出要求及各阶段底线，不自动承诺未来行动，不擅自固定人生终端目标。每次新观察、目标/价值或证据修订、行动范围改变后更新收据；保持原事前分析，未选路径不记实际结果。独立轨预留未见部分可观察、相关冲击、状态混叠、全无保证、时间改变、并列与退出代价；模型轨研究真实联合轨迹及多目标；产品轨验证可理解性和实际负担。此轮状态转移/效用由人工设定，未运行真实自然语言、生产模型、Qwen、Mac/iPhone、真人/历史验证或独立验收；不准入方法，不改生产，不启动Codex、CI、训练、合并、部署或冻结协议变更，零新增费用。
