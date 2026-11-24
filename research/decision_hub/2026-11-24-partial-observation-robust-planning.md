# 第43轮：部分观察下的长期可行性、历史信息集合与模型失效
2026-11-24。固定 main aeed46c4d0c743d59201d55e39cfca94dd792bae；PR #61 HEAD 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，open Draft。核对v3.1、AGENTS、同步规程、近期提交、开放PR及唯一产品交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第37/40/42轮。原生 decision_timing.py blob 4ed9fa430dcb993cc5005656c8b1744276fe7c33 已有调查/联合完成时间和行动比较。查重 partial observation/belief state/POMDP/set membership/hidden state/regime shift，发现历史R327提交62f73f8a3cddb86c7d838283cac35c105e60669d（实际查看结果JSON差异，18先验/准确率人工世界、72路径，单次sense与猜测价值），R198/R244相关提交（仅查到题名，未审原报告）；本轮不开展这些R项、不复验其冻结结果或改结论。与第42轮全观察、第37轮一次观察、第40轮固定世界问询区分：新增实际状态逐步变化、部分观察支持递推、多阶段路径硬门、可观察历史策略、支持扩大撤销证书。原创有限研究，无外部文献事实新增。
## 数学合同
有限充分真实状态X、行动a、非空后继支持T(x,a)、非空观察支持O(x')；行动先于新状态及信号实现。真实状态不可直接读取，只能读取已核验的历史行动和观察。初始非空信息集合B为有资格的可能状态。每期所有可能真实状态满足当前硬约束；未来状态支持 P=并集_{x∈B}T(x,a)，每个可能信号y的下一信息集合B_y={x'∈P:y∈O(x')}。观察不是概率；不同信号支持可重叠。若存在可能危险状态，不允许通过观察过滤来隐藏已经发生的违规；先检查P全体，再考虑后续观察。终端要求B包含于用户确认的目标集合G。定义D_0(B)=1当且仅当非空B包含于G；D_h(B)=1当且仅当B满足阶段底线且存在已确认对B全部状态可实施的行动，其全部后继满足下一阶段底线、对每个非空B_y均D_{h-1}(B_y)=1。递推保留全部合格首行动。空B代表当前合同与记录不一致，永远不能作为实际可行状态。不存在可能分支的信号可不进入预先策略；真实发生此信号必须触发异常处理。证明：给定符合Markov支持合同的真实状态及观察，归纳可知B恰为与完整历史相容的当前状态集合；同一B的剩余可行策略问题相同。每条合法观察历史策略的首行动须共同且每种可出现信号都有合法续策，反之按递推各分支拼接可行。仅针对保证满足硬约束及终端目标；一般累计效用存在未观察到的历史收益时，单纯B未必充分，须扩充状态或维护联合收益轨迹。固定潜在环境、相关冲击、观察误差相关或历史依赖也须入状态；不能自动独立组合。模型支持不足、用户拒绝提供信息、时间过期或观察错误保持UNKNOWN。
完整观察允许更多策略，故可行性是部分观察的上界。仅保留当前信号的策略及固定开环是完整历史策略子集；若重置时扩大信息集合，可能保守地丢失真实可行策略。真实新观察超出旧模型支持时，不能自动猜测一个新状态或任意扩大模型；先标MODEL_CONFLICT，撤销受影响的推荐资格，检查观察、时间及来源，只有独立获资格的新模型才能重新求解。旧结果保留事前身份。若转移支持扩大但状态/观察/目标/权限相同，旧策略的保证可能失效；新模型保证蕴含旧模型保证，因为旧路径是新路径子集。没有概率时不报告发生变化的概率。外部观察异常可能是测量错误、模型错设或环境变化，不能仅凭一次异常确定原因。
## 实验
2安全状态+1危险状态，每安全状态2行动，4种后继集合{0},{1},{0,1},{0,1,2}，4个状态行动对；2安全状态各3种非空二元信号支持，3种非空终端目标，3种非空初始安全信息集合，三阶段。共20736组。DP与128个完整二叉观察历史决策表逐真实状态路径重放对照，包含初始共同动作与后两期信号历史，核对所有首行动。32个仅当前信号+时间策略和8个固定开环表同样重放；完全观察上界与可能单路径另算。reset基线每次信号后丢弃历史和预测可达性，仅取全安全状态信号支持；若预测可进入危险状态，先失败。resetReject为精确可行而该保守基线不可行，并非真实错误事实。historyOnly为完整历史可行但不存在仅当前信号的保证策略；observationUseful为有完整历史策略但无保证开环；fullOnly为全观察可行但部分观察不可保证；possibleOnly为至少一个真实起点有成功路径而无保证策略。updates含不同状态/行动/信号及重复目标夹具的核查，不是独立用户样本。额外16确定转移表×16扩大遮罩×9观察×3目标×3初始域，检验扩大支持后保证不能增加（只扩大到含危险状态的全部3状态，此有限族不能证明所有变化实际适用）。withdrawals为旧保证在扩大域失效。异常观察示例旧模型保持状态0，观测1不可能；另立更宽支持后可得到状态1；不把后者自动采纳。两算法由同一研究者设计，非独立验收。
```js
function experiment(){
 const check=(v,m)=>{if(!v)throw Error(m)}, A=[0,1], states=[0,1,2], H=3;
 const members=m=>states.filter(s=>m&(1<<s));
 let cases=0,policyChecks=0,firstChecks=0,fullObsChecks=0,guaranteed=0,fullOnly=0,historyOnly=0,observationUseful=0,forgetUnsafe=0,resetReject=0,possibleOnly=0,updates=0,empty=0;
 let historyWitness=null,fullWitness=null,resetWitness=null;
 for(let code=0;code<256;code++){
  let z=code;const T=A.map(s=>A.map(a=>{const m=[1,2,3,7][z%4];z=Math.floor(z/4);return m;}));
  for(let o=0;o<9;o++){
   const O=[1+o%3,1+Math.floor(o/3),3]; // possible binary signals, including overlap
   const next=(b,a)=>members(b).reduce((m,s)=>m|(s===2?4:T[s][a]),0);
   const filter=(b,y)=>members(b).reduce((m,s)=>m|((O[s]&(1<<y))?(1<<s):0),0);
   const memo=new Map();
   for(let target=1;target<=3;target++){
    memo.clear();
    function dp(b,h){
     const k=b+8*h;
     if(memo.has(k))return memo.get(k);
     if(!b||(b&4)){return [];}
     if(!h)return (b&target)===b?[-1]:[];
     const good=A.filter(a=>{
      const p=next(b,a);
      if(p&4)return false;
      return A.every(y=>{const n=filter(p,y);return !n||dp(n,h-1).length>0;});
     });
     memo.set(k,good);return good;
    }
    function full(s,h){
     if(s===2)return false;if(!h)return !!(target&(1<<s));
     return A.some(a=>members(T[s][a]).every(n=>full(n,h-1)));
    }
    function possible(s,h){
     if(s===2)return false;if(!h)return !!(target&(1<<s));
     return A.some(a=>members(T[s][a]).some(n=>possible(n,h-1)));
    }
    // Oracle uses true-state trajectories, complete observable signal histories, not support DP.
    // Binary heap node indexes 0..6 give all 128 causal policies.
    function play(s,t,node,act){
     if(s===2)return false;if(t===H)return !!(target&(1<<s));
     const a=act(t,node);
     return members(T[s][a]).every(n=>A.filter(y=>O[n]&(1<<y)).every(y=>play(n,t+1,2*node+1+y,act)));
    }
    // Baseline that discards prior observations: current signal only, with time and root action.
    function memoryless(mask,t,node){const i=t===0?0:1+2*(t-1)+(node%2===0?1:0);return (mask>>i)&1;}
    function updateCheck(b,a,y){
     const p=next(b,a),n=filter(p,y);
     const direct=members(b).flatMap(s=>members(s===2?4:T[s][a])).filter(s=>O[s]&(1<<y)).reduce((m,s)=>m|(1<<s),0);
     check(n===direct,"update");updates++;if(!n)empty++;
    }
    for(let b=1;b<=3;b++){
     cases++;const d=dp(b,H),root=members(b);
     const good=[false,false];let any=false;
     for(let m=0;m<128;m++){
      const ok=root.every(s=>play(s,0,0,(t,n)=>(m>>n)&1));policyChecks++;
      if(ok){any=true;good[m&1]=true;}
     }
     check(any===(d.length>0)&&d.join()===A.filter(a=>good[a]).join(),"policy oracle");firstChecks++;
     const f=root.every(s=>full(s,H));fullObsChecks++;check(!any||f,"full information upper bound");
     if(any)guaranteed++;else if(root.some(s=>possible(s,H)))possibleOnly++;
     if(f&&!any){fullOnly++;if(!fullWitness)fullWitness={T,O,target,b};}
     let ml=false,open=false;
     for(let m=0;m<32;m++){if(root.every(s=>play(s,0,0,(t,n)=>memoryless(m,t,n))))ml=true;}
     for(let m=0;m<8;m++)if(root.every(s=>play(s,0,0,t=>(m>>t)&1)))open=true;
     check(!open||ml,"memoryless includes open");check(!ml||any,"history includes memoryless");
     if(any&&!ml){historyOnly++;if(!historyWitness)historyWitness={T,O,target,b,first:d};}
     if(any&&!open)observationUseful++;
     // Reset baseline treats every new signal as global current-state support, discards transition constraints.
     function reset(b,h){
      if(!b||(b&4))return false;if(!h)return (b&target)===b;
      return A.some(a=>{
       const p=next(b,a);if(p&4)return false;
       return A.every(y=>!filter(p,y)||reset(filter(3,y),h-1));
      });
     }
     const rr=reset(b,H);check(!rr||any,"reset conservative");
     if(any&&!rr){resetReject++;if(!resetWitness)resetWitness={T,O,target,b,first:d};}
     for(const a of A)for(const y of A)updateCheck(b,a,y);
    }
   }
  }
 }
 // Model invalidation: a perfectly persistent state 0 predicts only signal 0.
 // A new trusted observation of 1 has empty support; an independently authorized wider model admits 1.
 const update=(b,T,O,y)=>members(b).flatMap(s=>members(T[s])).filter(s=>O[s]&(1<<y)).reduce((m,s)=>m|(1<<s),0);
 const narrow=update(1,[1,2,4],[1,2,3],1),wide=update(1,[3,2,4],[1,2,3],1);
 check(narrow===0&&wide===2,"contradiction and separately qualified expansion");
 // Hard safety certificate monotonicity under support expansion: widening transition support cannot create a guarantee
 // with identical observation contract, state set, and target; checked on each of 16 narrow deterministic tables
 // vs all 256 wider tables containing them, all O and target and initial sets.
 let expansionChecks=0,withdrawals=0;
 function solve(T,O,b,target,h){
  if(!b||(b&4))return false;if(!h)return (b&target)===b;
  return A.some(a=>{const p=members(b).reduce((m,s)=>m|T[s][a],0);if(p&4)return false;return A.every(y=>{const n=members(p).filter(s=>O[s]&(1<<y)).reduce((m,s)=>m|(1<<s),0);return !n||solve(T,O,n,target,h-1);});});
 }
 for(let c=0;c<16;c++){
  const narrow=A.map(s=>A.map(a=>1<<((c>>(2*s+a))&1)));
  for(let e=0;e<16;e++){
   const wide=A.map(s=>A.map(a=>(e&(1<<(2*s+a)))?7:narrow[s][a]));
   for(let o=0;o<9;o++)for(let g=1;g<=3;g++)for(let b=1;b<=3;b++){
    const O=[1+o%3,1+Math.floor(o/3),3],x=solve(narrow,O,b,g,H),y=solve(wide,O,b,g,H);
    check(!y||x,"support expansion monotonicity");expansionChecks++;if(x&&!y)withdrawals++;
   }
  }
 }
 return {cases,policyChecks,firstChecks,fullObsChecks,guaranteed,fullOnly,historyOnly,observationUseful,resetReject,possibleOnly,updates,empty,expansionChecks,withdrawals,historyWitness,fullWitness,resetWitness,unexpectedObservation:{priorSupport:1,observedSignal:1,oldModelSupport:narrow,requalifiedWiderModelSupport:wide}};
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实际结果
```json
{
  "cases": 20736,
  "policyChecks": 2654208,
  "firstChecks": 20736,
  "fullObsChecks": 20736,
  "guaranteed": 10525,
  "fullOnly": 590,
  "historyOnly": 0,
  "observationUseful": 112,
  "resetReject": 3752,
  "possibleOnly": 9869,
  "updates": 82944,
  "empty": 13248,
  "expansionChecks": 20736,
  "withdrawals": 8442,
  "historyWitness": null,
  "fullWitness": {
    "T": [
      [
        1,
        2
      ],
      [
        2,
        1
      ]
    ],
    "O": [
      1,
      1,
      3
    ],
    "target": 1,
    "b": 3
  },
  "resetWitness": {
    "T": [
      [
        1,
        1
      ],
      [
        1,
        1
      ]
    ],
    "O": [
      1,
      1,
      3
    ],
    "target": 1,
    "b": 1,
    "first": [
      0,
      1
    ]
  },
  "unexpectedObservation": {
    "priorSupport": 1,
    "observedSignal": 1,
    "oldModelSupport": 0,
    "requalifiedWiderModelSupport": 2
  }
}
```
## 接入
B05/B06/B07/B08/B10候选。每次用户提供新事实或外部观察，检查身份、观测时期、行动记录、来源、模型版本与授权；在可信支持内更新可辨识状态，保留原事前预测及观察前后集合，重新计算后续可行策略。对模型冲突先暂停有依赖的建议；独立且有效的分析可继续。若证据更新使支持扩大，撤销旧保证并明确风险变化；新保证必须带当前版本/作用域/来源/观察历史依赖。拒绝提供隐私数据不视为世界状态被排除；新观察不可冒充用户的长期偏好。实际行动仍由用户确认。独立轨预留未见历史依赖、固定环境、模糊信号、空支持、危险状态被观察隐藏、过期和撤回、累计隐变量收益等案例；模型轨审查扩展状态和有概率的替代模型；产品轨验证现实解释与必要追问。当前实验只证明有限合成保证可行性；没有实际预测准确率、变化检测性能、真实模型更新、Qwen、设备或独立验收。不改生产、不启动Codex、CI、训练、合并、部署或冻结协议变更，零新增费用。
