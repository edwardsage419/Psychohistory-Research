# 长期个人决策：未完成可行性计算与部分偏好的联合候选证书
2026-11-26。RESEARCH_CANDIDATE / PREDECESSOR_CODE_EXECUTED / SYNTHETIC_EXECUTED / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线
同一手动轮第三阶段，起点main ebb909a63fb7916a6d1a5e72d1840f51b4794b80。沿用本轮已核对v3.2、同步规程、25近期提交、15开放PR、固定交接及#63固定head 734686980b19da9291bdd08b67d4e2519c011acf。实际加载以下三份固定自有研究源码：
research/decision_hub/2026-11-26-time-varying-task-cost-liquidity-dp.md 56f16ddab494b41aa07852045653fbdf20f28341
research/decision_hub/2026-11-26-observed-balance-policy-partition-and-replanning.md b5be4353d489e8b9ab09a39ac9e11f2929c2bd5a
research/decision_hub/2026-11-26-partial-lexicographic-goal-order-witnesses.md 56ccc94a47a135670b670e26e65c99503740e7e5
前两阶段目标组合与不完整词典序，既有anytime decision ports、联合覆盖、优先澄清不重复发明。本轮专门连接真实研究规划函数与已知可行/已知不可行/尚未计算的组合分类，在两类不确定性同时存在时给出精确有限包络。查重有限。
## 合同与证明
目标组合全集U必须为可信宿主确认的完整有限域；所有硬义务保留，不允许将必须履约的事项随意放入可释放软目标。F为已证可行，I为已证不可行，R=U\(F∪I)为尚未确定。真实可行集合B满足F⊆B⊆F∪R。除该包含关系外本模型不使用未知组合间约束；若真实存在关联则本包络仍为保守外界，不声称尖锐。已经确认采用强词典序二元目标偏好且偏序无环，目标完成身份独立，所有可能线性扩展保留；不假设一般用户接受这一偏好或无差异不存在。未确认覆盖/偏好模型返回UNKNOWN_QUALIFICATION；冲突单列。所有输出authority NONE。
某组合t在至少一个可行性补全及优先顺序中能胜，当且仅当t∈F∪R且在F∪{t}中有可胜顺序。必要性因任何真实补全必须包含F和t，删除其他竞争者不损害t获胜；充分性由允许取最小补全F∪{t}直接得到。因此只需在最小竞争集合调用前阶段可胜算法。若F空，允许全部未知均不可行的补全；不能凭候选非空证明存在可行方案。所有补全及顺序共同获胜的组合t必须已知可行且在最大补全F∪R中为唯一可能胜者；充分性由删除其他竞争者仍获胜，必要性由最小补全和最大补全均在域内。完整已计算时还原普通部分偏好问题。随着确定的可行性结论增加，所有补全集合缩小，可能获胜集合不能扩张，已证共同获胜不能被随后合格计算推翻（若输入修订则非同一合同，必须重新计算）。不使用单调目标反链，故适用于上一阶段内生信息反例。单轮计算只控制完成组合的个数，不是实际设备CPU、内存预算或可安全续算的持久检查点。
## 实际执行
600个任意有限分区夹具，最多8组合，对每个未知可行性补全实际枚举，并调用前轮独立拓扑排列参照，核对完整可能集合、必要胜者及空可行域可能性。800个真实研究函数驱动的合成规划图，2世界、3期、3目标，每图全部8组合实际调用P.solve、P.oracle及成功树验算，观察余额可开关。然后以随机计算顺序逐项揭示结果，检查0..8已计算前缀，包络覆盖完整结果、可能集合单调缩小、已确认胜者稳定、完整时精确、偏好撤回后可能集合扩张；错误对照把未计算当不可行，在仅F上给出唯一胜者但不同于完整域的共同胜者（含完整域偏好未定）。6专项控制。实际复用研究源码和标准JS，两次完整结果一致。计数为有限合成结构/重复计算，不是独立人次、实际产品错误率或真实性能。
```json
{
  "arbitraryStates": 600,
  "completionChecks": 2441,
  "planningGraphs": 800,
  "actualBundleChecks": 6400,
  "progressPrefixes": 7200,
  "earlyNecessary": 256,
  "completeNecessary": 500,
  "earlyNoFeasible": 0,
  "unknownAsInfeasibleFalseWinner": 1504,
  "unknownExistencePrefixes": 2386,
  "possibleShrinks": 4341,
  "unresolvedFeasibility": 3292,
  "preferenceRevisionChecks": 570,
  "controls": 6,
  "example": {
    "yes": [
      0
    ],
    "no": [],
    "truth": [
      3,
      5,
      6
    ],
    "naive": 0,
    "possible": [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7
    ]
  }
}
```
## 接入
GoalBundlePort逐项提供状态和当前范围见证；PreferenceOrderPort提供明确用户偏好模型及版本；联合出口同时显示已证可行候选、可能最优集合、仍未知是否可行和共同最优证书。不能把未计算/无证据/输入不合格标为已证不可行，不能提前强制排序或要求用户回答不影响输出的偏好问题。真实证书还需原生方法科学资格、身份/时间/证据/授权/方法版本、持久预算及原子发布。研究者选择有限模型、词典序、组合顺序及独立未知补全包络；未运行完整原生、独立留出、真实用户、真机、真实资源预算。未修改生产、唯一交接、冻结、证据等级、PR、训练、部署、主动CI或费用。
## 复算
固定三份报告按上列顺序输入，Node包装未运行，连接器核心实际执行。
```js
const code=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8").split("\`\`\`js\n")[1].split("\n\`\`\`")[0]);
const make=Function(code[0].split(" const out={graphs:")[0]+"\nreturn {valid,actions,solve,verify,oracle};\n}\nreturn study();");
const make2=Function("make",code[1].slice(code[1].indexOf("function experiment(make){")).split(" const out={graphs:")[0]+"\nreturn {solve,oracle,unpack};\n}\nreturn experiment(make);");
const make3=Function(code[2].split(" const out={graphs:")[0]+"\nreturn {closure,possible,greedy,enumerate,orderOK,winner};\n}\nreturn experiment();");
function experiment(make,make2,make3){
 const P=make2(make),R=make3(),ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),all=Array.from({length:8},(_,i)=>i),sort=x=>[...x].sort((a,b)=>a-b);
 let seed=20261205;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 function port(yes,no,universe,edges,covered,semantics){
  if(!covered||semantics!=="EXPLICIT_LEXICOGRAPHIC")return {status:"UNKNOWN_QUALIFICATION",authority:"NONE"};
  const p=R.closure(edges);if(!p)return {status:"PREFERENCE_CONFLICT",authority:"NONE"};
  ck(new Set(universe).size===universe.length&&yes.every(v=>universe.includes(v)&&!no.includes(v))&&no.every(v=>universe.includes(v))&&new Set(yes).size===yes.length&&new Set(no).size===no.length,"partition");
  const unknown=universe.filter(v=>!yes.includes(v)&&!no.includes(v)),potential=universe.filter(v=>!no.includes(v));
  const possible=potential.filter(t=>R.possible(t,yes.includes(t)?yes:[...yes,t],p).ok);
  // No actual feasibility completion can introduce an alternative outside possible.
  // Necessary t must be already known feasible and win even when every unknown is feasible.
  const n=potential.length?R.greedy(potential,p).necessary:null;
  const necessary=n!==null&&yes.includes(n)?n:null;
  const status=!potential.length?"NO_FEASIBLE_BUNDLE":necessary!==null?"CONDITIONAL_COMMON_WINNER":!yes.length?"UNKNOWN_EXISTENCE":unknown.length?"UNRESOLVED_FEASIBILITY_OR_PREFERENCE":"UNRESOLVED_PREFERENCE";
  return {status,possible:sort(possible),necessary,unknown,emptyPossible:yes.length===0,authority:"NONE"};
 }
 // Exhaust all completions of unknown feasibility, using independent topology enumeration
 // from the previous study, not the greedy winner oracle.
 function ref(yes,no,universe,edges){
  let u=universe.filter(v=>!yes.includes(v)&&!no.includes(v)),p=R.closure(edges),out=new Set(),empty=false,sets=0;
  for(let mask=0;mask<1<<u.length;mask++){
   let b=[...yes,...u.filter((_,i)=>mask&(1<<i))];sets++;
   if(!b.length){empty=true;continue}
   for(let v of R.enumerate(b,p).possible)out.add(v);
  }
  const possible=sort(out);
  return {possible,necessary:!empty&&possible.length===1?possible[0]:null,empty,sets};
 }
 const out={arbitraryStates:0,completionChecks:0,planningGraphs:0,actualBundleChecks:0,progressPrefixes:0,earlyNecessary:0,completeNecessary:0,earlyNoFeasible:0,unknownAsInfeasibleFalseWinner:0,unknownExistencePrefixes:0,possibleShrinks:0,unresolvedFeasibility:0,preferenceRevisionChecks:0,controls:0,example:null};
 for(let g=0;g<600;g++){
  const universe=Array.from({length:1+rnd(8)},(_,i)=>i),yes=[],no=[];
  for(let v of universe){let k=rnd(3);if(k===0)yes.push(v);if(k===1)no.push(v)}
  let edges=[];for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(rnd(3)===0)edges.push([i,j]);
  const z=port(yes,no,universe,edges,true,"EXPLICIT_LEXICOGRAPHIC"),o=ref(yes,no,universe,edges);
  ck(eq(z.possible,o.possible)&&z.necessary===o.necessary&&z.emptyPossible===o.empty,"all completion parity");out.arbitraryStates++;out.completionChecks+=o.sets;
 }
 for(let g=0;g<800;g++){
  const d=[1+rnd(2),1+rnd(2),1+rnd(2)],jobs=Array.from({length:3},()=>{let release=rnd(2);return {release,deadline:release+rnd(3-release)}});
  const ws=Array.from({length:2},()=>({d,jobs:jobs.map(j=>({...j,cost:Array.from({length:3},()=>rnd(4))})),cap:Array.from({length:3},()=>1+rnd(3)),income:Array.from({length:3},()=>rnd(5)),mandatory:Array.from({length:3},()=>rnd(3)),reserve:Array.from({length:3},()=>rnd(3))}));
  let b=rnd(10),obs=!!rnd(2),s=[[0,0,0],[0,rnd(2),rnd(2)]],edges=[];
  for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(rnd(3)===0)edges.push([i,j]);
  let feasible=[];
  for(let m of all){
   let demand=d.map((n,i)=>m&(1<<i)?n:0),ps=ws.map(p=>({...p,d:demand}));
   const z=P.solve(ps,s,b,obs),o=P.oracle(ps,s,b,obs);ck(z.ok===o.ok,"actual planner parity");
   if(z.ok){feasible.push(m);ck(P.unpack(z,ps,s,b,obs),"witness")}
   out.actualBundleChecks++;
  }
  const p=R.closure(edges),truth=feasible.length?R.enumerate(feasible,p).possible:[],necessary=truth.length===1?truth[0]:null;
  let order=all.slice();for(let i=7;i>0;i--){let j=rnd(i+1);[order[i],order[j]]=[order[j],order[i]]}
  let yes=[],no=[],prev=null,early=false,earlyNo=false;
  for(let k=0;k<=8;k++){
   const z=port(yes,no,all,edges,true,"EXPLICIT_LEXICOGRAPHIC");
   ck(truth.every(v=>z.possible.includes(v)),"upper candidate containment");
   if(z.necessary!==null)ck(z.necessary===necessary,"sound early necessary");
   if(prev){ck(z.possible.every(v=>prev.possible.includes(v)),"possible monotonicity");if(z.possible.length<prev.possible.length)out.possibleShrinks++;
    if(prev.necessary!==null)ck(z.necessary===prev.necessary,"necessary stable");
   }
   if(k===8){ck(eq(z.possible,truth)&&z.necessary===necessary,"complete parity");if(necessary!==null)out.completeNecessary++}
   if(k<8&&z.necessary!==null)early=true;
   if(k<8&&z.status==="NO_FEASIBLE_BUNDLE")earlyNo=true;
   if(z.status==="UNKNOWN_EXISTENCE")out.unknownExistencePrefixes++;
   if(z.status==="UNRESOLVED_FEASIBILITY_OR_PREFERENCE")out.unresolvedFeasibility++;
   if(yes.length&&k<8){
    const naive=R.greedy(yes,p).necessary;
    if(naive!==null&&naive!==necessary){out.unknownAsInfeasibleFalseWinner++;out.example??={yes:[...yes],no:[...no],truth,naive,possible:z.possible}}
   }
   prev=z;out.progressPrefixes++;
   if(k<8){let m=order[k];(feasible.includes(m)?yes:no).push(m)}
  }
  if(early)out.earlyNecessary++;if(earlyNo)out.earlyNoFeasible++;
  if(edges.length){
   const old=port(yes,no,all,edges,true,"EXPLICIT_LEXICOGRAPHIC"),next=port(yes,no,all,edges.slice(1),true,"EXPLICIT_LEXICOGRAPHIC");
   ck(old.possible.every(v=>next.possible.includes(v)),"preference revision");out.preferenceRevisionChecks++;
  }
  out.planningGraphs++;
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 ctl(port([1],[],[1,2],[],true,"EXPLICIT_LEXICOGRAPHIC").necessary===null,"unknown alternative");
 ctl(port([3],[],[1,2,3],[],true,"EXPLICIT_LEXICOGRAPHIC").necessary===3,"known dominates all unknown");
 ctl(port([],[],[1],[],true,"EXPLICIT_LEXICOGRAPHIC").status==="UNKNOWN_EXISTENCE","existence uncertain");
 ctl(port([],[1],[1],[],true,"EXPLICIT_LEXICOGRAPHIC").status==="NO_FEASIBLE_BUNDLE","complete negative");
 ctl(port([1],[],[1],[],false,"EXPLICIT_LEXICOGRAPHIC").status==="UNKNOWN_QUALIFICATION","coverage");
 ctl(port([1],[],[1],[],true,"UNCONFIRMED").status==="UNKNOWN_QUALIFICATION","no preference model");
 return out;
}
console.log(JSON.stringify(experiment(make,make2,make3),null,2));
```
