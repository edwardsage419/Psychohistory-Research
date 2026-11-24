# 第47轮：有限计算资源的依赖闭包、共享产出及预算规划
2026-11-24。固定 main 39354c9b7151ca3fb1aa17b76f81751e00ead6c2；PR #61 HEAD 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，open Draft。核对v3.1、AGENTS、同步规程、近期提交、开放PR、唯一协调交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第4/27/40/45/46轮。原生 decision_hub.py a97de30f5241063862dbc0ce797c214cbc4d405f、decision_registry.py 8046de09674af850a456bbccc534e5f6c2511497、decision_planner.py f2d3d21b853afe9dc757a33e83cd3d6160f8dd7b 已有依赖顺序、适用性检查、异常隔离和信息优先级；未运行原生入口。关键词 budgeted scheduling/resource allocation/knapsack/anytime/computation cost/budgeted analysis 查重发现R332历史资源分配提交7a164a941b9fda3c529be37a5fa0bf80a8661f7d（仅题名），未开展R项或复验其冻结结果。区别于第4轮按需依赖闭包、第27轮局部出口、第40轮追问成本和第45轮类别模型选择，本轮新增固定预算下的唯一工作节点、共享前置任务、唯一产出覆盖、上界成本以及必需检查优先。原创有限计算，不新增外部来源事实。
## 数学合同
有限有向无环工作图，节点为有资格且获授权的具体计算或检索实例，身份绑定输入、作用域、版本、授权、依赖及结果类型。边表示必须先完成且具备合格结果的依赖；只有计划执行并不等于获得结果。每项工作有已核实的非负资源上界c_i、固定预算B；本实验串行、单资源、确定工作范围、无额外并行、启动、重试或缓存开销。真实成本未知不应以任意点值冒充上界。工作集合S须对依赖闭合、全体有资格，且sum c_i<=B；同一个有效依赖只执行一次。已完成且仍合格的共享结果可另设已完成状态，不能跨版本/授权擅自复用。每项产出有唯一语义身份，只有明确可替代的同一输出才去重；不同方法的独立复核、互补信息和竞争解释不得作为重复项删除。设O_i为可交付的唯一产出集合，v_j>=0为经确认的分析任务价值（本实验为合成覆盖权重，非用户人生效用），V(S)=sum_{j in union O_i}v_j。
必需检查M的依赖闭包优先；若不具资格或预算不足，则完整建议出口受阻，仍可运行具有独立合法依赖的描述性输出。本实验M仅节点0，存在可负担M则所有候选集合必须包含M；否则只比较可独立执行集合。真实系统还应强制所有必要风险、隐私、硬约束及证据核查，不得仅因覆盖权重低跳过；M完成后仍须检查实际结果、关键必需端口及授权。最大化V(S)，并列时最小化资源上界，保留全部并列。没有共同分析价值权重时展示覆盖与成本偏序，不强制单一总分。实际有失败或新观察时重新规划；无真实成功率假设，计划价值为条件性覆盖，不是保证现实决策收益。
通过从空集逐次加入资格满足且所有前置已完成的节点，记录可达集合。非负成本保证合法最终集合的所有前缀不超预算；任何闭合合法集合均存在拓扑序，故可被访问，所有访问集合也合法。给定有限图可穷尽并给出最优证书；超出规模或时限只能报告已找到合法下界、剩余松弛上界（例如所有尚可能产出总和）和未完成事项，不得宣称最优。本轮未实现截断搜索或动态失败重规划。
## 实验
5节点：0必需约束核查；1共享证据；2、3模型共同依赖0和1；4独立描述；产出位掩码分别0,0,1,6,2（3、4有同一可替代产出）。32种成本上界(1/2)，32种资格掩码，27种三个产出权重(0/1/2)，9个预算0..8，共248832组。逐步合法可达集合与直接32个子集穷举核对全部合法域、最大覆盖及全部成本最小并列。mandatory可行仅指能安排必需检查，绝非检查通过或最终建议许可。对照一：先保留必需节点后，按新增唯一产出价值/新增闭包成本贪婪选择；对照二：用1作为所有成本的乐观下端点，选择同样目标，检查上界总成本超预算（nominalOverrun仅存在上界情景超支，不是实际超支）；对照三：错误把重复产出逐节点加分。sharedSavings为存在最优计划同时运行2/3且共享闭包比分别计费节省的案例数，不是实际时间测量。partialValue为无法安排必需检查但仍可完成正权重局部描述的案例。gateControls为人工布尔结果门控制，非真实鉴权。两种计算路径同一研究者设计，非独立验收。没有真实费用、耗时、任务权重或产品使用效果。
```js
function experiment(){
 const check=(x,m)=>{if(!x)throw Error(m)};
 const N=[0,1,2,3,4],bits=m=>N.filter(i=>m&(1<<i));
 // 0 mandatory constraint check; 1 shared evidence; 2,3 optional models; 4 independent descriptive analysis.
 const dep=[0,0,3,3,0],out=[0,0,1,6,2]; // outputs 0,1,2; models 3 and 4 overlap on output 1.
 const masks=Array.from({length:32},(_,i)=>i);
 const union=(m,vs)=>bits(m).reduce((v,i)=>v|vs[i],0);
 const closure=m=>{let prev;do{prev=m;m|=union(m,dep);}while(prev!==m);return m;};
 const closed=m=>closure(m)===m;
 const sum=(m,vs)=>bits(m).reduce((v,i)=>v+vs[i],0);
 const valid=(m,allowed)=>closed(m)&&(m&allowed)===m;
 let cases=0,oracleChecks=0,full=0,partial=0,greedyGap=0,nominalOverrun=0,duplicateScoreGap=0,sharedSavings=0,gateBlocked=0,gateControls=0,statesVisited=0,strictGainSum=0,baselineSum=0,partialValue=0;
 let witness=null,overrunWitness=null;
 for(let c=0;c<32;c++){
  const hi=N.map(i=>1+((c>>i)&1)),lo=N.map(()=>1);
  for(let qual=0;qual<32;qual++){
   for(let w=0;w<27;w++){
    let k=w;const weight=[0,1,2].map(()=>{const v=k%3;k=Math.floor(k/3);return v;});
    const value=m=>[0,1,2].reduce((s,i)=>s+((union(m,out)&(1<<i))?weight[i]:0),0);
    for(let budget=0;budget<=8;budget++){
     cases++;
     // Reachable completed sets via legal topological additions, reserve upper cost.
     const seen=new Set([0]),queue=[0];
     for(let q=0;q<queue.length;q++){
      const m=queue[q];
      for(const i of N){const b=1<<i,n=m|b;if((m&b)||!(qual&b)||(m&dep[i])!==dep[i]||sum(n,hi)>budget)continue;
       if(!seen.has(n)){seen.add(n);queue.push(n);}
      }
     }statesVisited+=seen.size;
     const hasGate=[...seen].some(m=>m&1);
     const pool=[...seen].filter(m=>!hasGate||m&1);
     const best=Math.max(...pool.map(value));
     // Choose minimum resource among value ties, keep all remaining ties.
     const cheapest=Math.min(...pool.filter(m=>value(m)===best).map(m=>sum(m,hi)));
     const leaders=pool.filter(m=>value(m)===best&&sum(m,hi)===cheapest).sort((a,b)=>a-b);
     // Reference direct subset enumeration.
     const all=masks.filter(m=>valid(m,qual)&&sum(m,hi)<=budget);oracleChecks+=32;
     check(all.length===seen.size&&all.every(m=>seen.has(m)),"reachable sets");
     const gated=all.some(m=>m&1);check(gated===hasGate,"mandatory");
     const ref=all.filter(m=>!gated||m&1).sort((a,b)=>value(b)-value(a)||sum(a,hi)-sum(b,hi)||a-b);
     check(best===value(ref[0])&&leaders.join()===ref.filter(m=>value(m)===best&&sum(m,hi)===cheapest).sort((a,b)=>a-b).join(),"optimal subset");
     if(hasGate)full++;else {partial++;gateBlocked++;if(best>0)partialValue++;}
     // Package greedy based on marginal unique coverage per incremental upper cost, after mandatory reservation.
     let g=hasGate?1:0;
     while(true){
      let pick=-1,gn=0,gc=1;
      for(const i of N){const n=closure(g|(1<<i));if(n===g||!valid(n,qual)||sum(n,hi)>budget)continue;
       const dv=value(n)-value(g),dc=sum(n,hi)-sum(g,hi);
       if(dv>0&&dv*gc>gn*dc){pick=n;gn=dv;gc=dc;}
      }if(pick<0)break;g=pick;
     }
     const gv=value(g);check(gv<=best,"greedy");
     baselineSum+=gv;strictGainSum+=best-gv;
     if(gv<best){greedyGap++;if(!witness)witness={hi,qual,weight,budget,greedy:g,greedyValue:gv,leaders,best};}
     // Point-cost planning with the lower duration, same gate rule, then check high-cost overrun.
     const nominal=masks.filter(m=>valid(m,qual)&&sum(m,lo)<=budget);
     const ng=nominal.some(m=>m&1);
     const chosen=nominal.filter(m=>!ng||m&1).sort((a,b)=>value(b)-value(a)||sum(a,lo)-sum(b,lo)||a-b)[0];
     if(sum(chosen,hi)>budget){nominalOverrun++;if(!overrunWitness)overrunWitness={hi,qual,weight,budget,nominal:chosen,upperCost:sum(chosen,hi)};}
     // Wrong additive output scoring counts repeated output separately.
     const double=m=>bits(m).reduce((s,i)=>s+[0,1,2].reduce((v,j)=>v+((out[i]&(1<<j))?weight[j]:0),0),0);
     const duplicated=pool.slice().sort((a,b)=>double(b)-double(a)||sum(a,hi)-sum(b,hi)||a-b)[0];
     if(value(duplicated)<best)duplicateScoreGap++;
     if(leaders.some(m=>(m&12)===12&&sum(closure(4),hi)+sum(closure(8),hi)>sum(closure(12),hi)))sharedSavings++;
    }
   }
  }
 }
 // Scheduling planned completion does not grant result authorization.
 const authorize=x=>x.gateDone&&x.gatePass&&x.requiredPorts&&x.current&&x.permission;
 const x={gateDone:true,gatePass:true,requiredPorts:true,current:true,permission:true};
 check(authorize(x),"authorized gate");gateControls++;
 for(const k of Object.keys(x)){check(!authorize({...x,[k]:false}),"deny "+k);gateControls++;}
 check(greedyGap>0&&nominalOverrun>0&&duplicateScoreGap>0&&partialValue>0,"coverage");
 return {cases,oracleChecks,statesVisited,full,partial,partialValue,greedyGap,nominalOverrun,duplicateScoreGap,sharedSavings,gateBlocked,gateControls,strictGainSum,baselineSum,witness,overrunWitness};
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实际结果
```json
{
  "cases": 248832,
  "oracleChecks": 7962624,
  "statesVisited": 747819,
  "full": 103680,
  "partial": 145152,
  "partialValue": 35712,
  "greedyGap": 462,
  "nominalOverrun": 21344,
  "duplicateScoreGap": 165,
  "sharedSavings": 2992,
  "gateBlocked": 145152,
  "gateControls": 6,
  "strictGainSum": 566,
  "baselineSum": 130810,
  "witness": {
    "hi": [
      1,
      1,
      1,
      1,
      1
    ],
    "qual": 27,
    "weight": [
      0,
      2,
      1
    ],
    "budget": 3,
    "greedy": 17,
    "greedyValue": 2,
    "leaders": [
      11
    ],
    "best": 3
  },
  "overrunWitness": {
    "hi": [
      2,
      1,
      1,
      1,
      1
    ],
    "qual": 1,
    "weight": [
      0,
      0,
      0
    ],
    "budget": 1,
    "nominal": 1,
    "upperCost": 2
  }
}
```
## 接入
B04/B06/B07/B08/B09/B10/B11候选增量。根据确认目标生成必需及可选工作图，先检查硬门及授权，采用实际任务上界预算、共享有效依赖和版本绑定去重。对必需工作不足明确限制完整建议，允许独立合格输出；执行后核实证据与计算收据才发布。实时展示已完成、未执行、受阻、失效及剩余预算；用户修改目标、撤回授权、来源/结果变化则重新求解。不为节省资源删除竞争模型或必要风险核查；零新增费用硬约束始终优先。独立轨预留未见循环、缺依赖、失效缓存、共享但不同身份、预算变化、结果失败、并发/取消、成本未界定及关键检查未通过；模型轨研究多资源、并发、随机成本、输出交互及截断证书；产品轨评估真实首答延迟及解释。未运行生产、Qwen、Mac/iPhone、真实数据、独立验收或实际资源测量；无生产修改、Codex、CI、训练、合并、部署、冻结协议变更，零新增费用。
