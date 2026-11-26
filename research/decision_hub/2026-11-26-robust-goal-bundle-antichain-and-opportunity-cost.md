# 长期个人决策：联合目标组合、最小让步集合与内生信息反例
2026-11-26。RESEARCH_CANDIDATE / PREDECESSOR_CODE_EXECUTED / SYNTHETIC_EXECUTED / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线与查重
起点main 3976eeaf2bae7e4864d8a53ed781d5461ac83e21。核对25近期提交、15开放PR，#63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍draft。读取v3.2、同步规程及唯一交接固定blob 5e74f4f0b37141d631740e844ad8bbbfed232e07（未核对最新路径），R97 fa8c878449a333ab9ebe787c015df43dbcd1ec9f、R98 db648df87860bcb00037c8dddb3a2bc85d8aee28、R99 a1ea992561b43252c99e882494640b290a8fa5a4和前轮实际进度3c86747e0617f2f131de0c47bde4000f7e177ff4相关合同。八关键词代码检索无结果，非全库查重。R97已做无加权多目标前沿、R98已做旧目标机会损失、R99已做互补收益；本轮新增对多个目标组合的非预知策略查询、在满足明确单调条件时用极大可行/极小不可行集合表示完整格，以及首次针对余额内生信息破坏目标单调性给出构造反例。不是新集合格理论或新DP。
固定输入：
research/decision_hub/2026-11-26-time-varying-task-cost-liquidity-dp.md 56f16ddab494b41aa07852045653fbdf20f28341
research/decision_hub/2026-11-26-observed-balance-policy-partition-and-replanning.md b5be4353d489e8b9ab09a39ac9e11f2929c2bd5a
实际提取并调用已审阅项目自有函数valid/actions及P.solve/oracle/unpack，生产不得执行任意外部文档。
## 合同和关键反例
3个可选目标均为固定需求的可拆分整数任务，三个期间、2个联合世界、成本非负、任务自身没有现金收入/互补/依赖/取消费用。任何移除目标仅为假设性分析，不允许解除真实硬约束或既有承诺。真实主体、任务、资源、未来域及资格由可信宿主另确认，全部只读authority NONE。以同一已确认起始状态、世界域、观察合同计算8种目标子集。若只有与行动独立的外生信号（本实验不观察余额），给定可行目标组合的策略删除其中某些任务的动作，保留相同外生信号历史及原策略作为内部模拟，成本及容量使用不增加，其他期限和储备仍满足；所以可行集合向下封闭。其极大可行与极小不可行集合分别支持向下/向上推理。空组合也可能因强制支出与底线不可行。完整有限域中按顺序查询未被证实的组合，保留这两个反链，逐项和穷举对照。若世界覆盖未核对，不能给现实全称；例中的8个覆盖控制只是输出合同夹具，不验证生产覆盖。
重要：一旦任务动作产生有信息的实际余额观察，删掉任务可能同时删掉观察，从而破坏向下封闭，即使任务仅消耗资源。构造例：A必须第0期完成，两个世界成本0/1；初始余额1；B在后两期中一个世界仅前期成本0、另一世界仅后期成本0，另一期成本4。完成A后余额区分世界，因此A+B存在共同非预知策略；单做B时无法区分，不能保证。故不能以较大组合可行直接推导较小组合可行，也不能用较小组合不可行排除大组合。对于余额可观测域，本实验逐组合实际求解，保留违反单调的随机案例或零计数，并固定构造反例。若新任务带来收入、技能、强制协同或信息效应，同样应重新审查单调性。仅根据目标名猜测禁止剪枝。
旧目标集合O={A,B}且已可行，拟新增C。最小让步集合D⊆O使(O\D)∪{C}可行，且任何真子集不够。仅在单调外生信号合同中使用极大可行集合计算，直接枚举核对所有最小D。不同让步集合保留，不假设A/B价值相等、互换或可依法取消；不存在D表示给定模型内新增目标不可行。真实取消资格、违约、退款或效用须另模型处理。单世界分别可行不能推出共享策略可行；世界计数非概率。
## 实验
1200合成图、每图2种观测合同×8组合=19200次实际策略及独立排程参照，核验见证；外生合同反链查询与逐项对照，旧目标机会成本的最小让步集合及逐世界诊断。固定4控制含内生信息反例和不可合并的让步选择，另8输出覆盖夹具。连接器标准JS两次完整执行一致。计数为有限合成结构及重复查询，非独立用户、现实成功概率、产品错误率或性能。
```json
{
  "graphs": 1200,
  "exactBundleChecks": 19200,
  "oracleChecks": 19200,
  "monotoneCalls": 5748,
  "monotoneInferred": 3852,
  "observedBalanceMonotoneViolations": 0,
  "informationEffectExamples": 0,
  "conditionalGoalConflict": 38,
  "allIndividualButNotJoint": 289,
  "existingBaseFeasible": 444,
  "newGoalCompatible": 205,
  "releaseNeeded": 184,
  "releaseImpossible": 55,
  "releaseSetsChecked": 444,
  "partialCoverageControls": 8,
  "controls": 4,
  "witnesses": {
    "release": {
      "b": 5,
      "d": [
        1,
        1,
        1
      ],
      "feasible": [
        0,
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "drop": [
        1,
        2
      ]
    }
  }
}
```
## 接入
GoalBundlePort应保存稳定目标ID、原始义务、是否允许假设移除、时限、资源/收入/信息依赖、共同世界及实际状态版本。目标单调性必须经适用合同证明后才开启反链剪枝；行动依赖观察的域逐项求解或使用另行证明的搜索方法。最小让步集合只显示假设条件，不写入长期记录。研究者选择有限任务、外生/内生观测、成本、基线及查询顺序；未修改生产、交接、冻结、证据等级、PR、训练、部署、主动CI、费用；原生、独立留出、真机、真人未运行。
## 复算
固定两份报告按顺序传入，连接器实际执行，Node包装未运行。
```js
const code=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8").split("\`\`\`js\n")[1].split("\n\`\`\`")[0]);
const make=Function(code[0].split(" const out={graphs:")[0]+"\nreturn {valid,actions,solve,verify,oracle};\n}\nreturn study();");
const make2=Function("make",code[1].slice(code[1].indexOf("function experiment(make){")).split(" const out={graphs:")[0]+"\nreturn {solve,oracle,unpack};\n}\nreturn experiment(make);");
function experiment(make,make2){
 const P=make2(make),ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 let seed=20261126;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 const sub=(a,b)=>(a&b)===a,pop=m=>[0,1,2].filter(i=>m&(1<<i)).length,all=Array.from({length:8},(_,i)=>i);
 const maximal=xs=>xs.filter(a=>!xs.some(b=>a!==b&&sub(a,b))).sort((a,b)=>a-b);
 const minimal=xs=>xs.filter(a=>!xs.some(b=>a!==b&&sub(b,a))).sort((a,b)=>a-b);
 // Test goal bundle under a fixed initial state, common nonanticipative strategy.
 // Monotonicity assumes optional work has only nonnegative costs and no benefit to
 // feasibility EXCEPT information. With observed balance, optional work can itself
 // reveal the world; removing it can destroy information and monotonicity!
 function evalBundle(ws,s,b,m,observe){
  const d=ws[0].d.map((n,i)=>m&(1<<i)?n:0),ps=ws.map(p=>({...p,d}));
  return {z:P.solve(ps,s,b,observe),ps};
 }
 function monotoneSearch(test,order){
  let yes=[],no=[],calls=0,inferred=0;
  for(let m of order){
   if(yes.some(k=>sub(m,k))||no.some(k=>sub(k,m))){inferred++;continue}
   if(test(m)){yes=maximal([...yes,m]);}else no=minimal([...no,m]);calls++;
  }
  return {yes,no,calls,inferred};
 }
 function releases(yes,old,requested){
  const drops=all.filter(m=>sub(m,old)&&yes.some(y=>sub((old&~m)|requested,y)));
  return minimal(drops);
 }
 const out={graphs:0,exactBundleChecks:0,oracleChecks:0,monotoneCalls:0,monotoneInferred:0,observedBalanceMonotoneViolations:0,informationEffectExamples:0,conditionalGoalConflict:0,allIndividualButNotJoint:0,existingBaseFeasible:0,newGoalCompatible:0,releaseNeeded:0,releaseImpossible:0,releaseSetsChecked:0,partialCoverageControls:0,controls:0,witnesses:{}};
 for(let g=0;g<1200;g++){
  let d=[1+rnd(2),1+rnd(2),1+rnd(2)],jobs=Array.from({length:3},()=>{let release=rnd(2),deadline=release+rnd(3-release);return {release,deadline}});
  const ws=Array.from({length:2},()=>({d,jobs:jobs.map(j=>({...j,cost:Array.from({length:3},()=>rnd(4))})),cap:Array.from({length:3},()=>1+rnd(3)),income:Array.from({length:3},()=>rnd(5)),mandatory:Array.from({length:3},()=>rnd(3)),reserve:Array.from({length:3},()=>rnd(3))}));
  const b=rnd(10),s=[[0,0,0],[0,rnd(2),rnd(2)]],truth=[[],[]];
  for(let obs=0;obs<2;obs++)for(let m of all){
   let {z,ps}=evalBundle(ws,s,b,m,!!obs);const o=P.oracle(ps,s,b,!!obs);ck(z.ok===o.ok,"oracle");
   if(z.ok){truth[obs].push(m);ck(P.unpack(z,ps,s,b,!!obs),"witness")}
   out.exactBundleChecks++;out.oracleChecks++;
  }
  // Exogenous signals: deleting optional work preserves the same observation groups.
  let f=truth[0],gmax=maximal(f),gmin=minimal(all.filter(m=>!f.includes(m)));
  for(let m of f)ck(all.filter(k=>sub(k,m)).every(k=>f.includes(k)),"downward closed");
  let z=monotoneSearch(m=>evalBundle(ws,s,b,m,false).z.ok,[7,0,3,5,6,1,2,4]);
  ck(eq(z.yes,gmax)&&eq(z.no,gmin),"antichains");out.monotoneCalls+=z.calls;out.monotoneInferred+=z.inferred;
  // Never infer on endogenous-information domain; explicitly count discovered violations.
  const v=truth[1].flatMap(m=>all.filter(k=>sub(k,m)&&!truth[1].includes(k)).map(k=>[k,m]));
  if(v.length){out.observedBalanceMonotoneViolations+=v.length;out.informationEffectExamples++;out.witnesses.observed??={ws,b,s,v}}
  if([1,2,4].every(m=>f.includes(m))&&!f.includes(7))out.allIndividualButNotJoint++;
  const old=3,req=4;
  if(f.includes(old)){
   out.existingBaseFeasible++;
   let r=releases(gmax,old,req),direct=minimal(all.filter(m=>sub(m,old)&&f.includes((old&~m)|req)));
   ck(eq(r,direct),"minimal old-goal release");out.releaseSetsChecked++;
   if(f.includes(7))out.newGoalCompatible++;else if(r.length){out.releaseNeeded++;out.witnesses.release??={b,d,feasible:f,drop:r}}else out.releaseImpossible++;
  }
  // Perfect-world feasibility is weaker than common-policy feasibility.
  const one=ws.every((p,i)=>evalBundle([p],[s[i]],b,7,false).z.ok);
  if(one&&!f.includes(7))out.conditionalGoalConflict++;
  out.graphs++;
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 // Construct endogenous information counterexample: optional A costs 0 vs 1 now,
 // and distinguishes worlds; B is cheap in opposite later periods.
 // When A is omitted there is no observation to distinguish the worlds.
 const jobs=[{release:0,deadline:0,cost:[0,0,0]},{release:1,deadline:2,cost:[0,0,4]},{release:0,deadline:2,cost:[0,0,0]}],p={d:[1,1,0],jobs,cap:[1,1,1],income:[0,0,0],mandatory:[0,0,0],reserve:[0,0,0]},q={...p,jobs:[{...jobs[0],cost:[1,0,0]},{...jobs[1],cost:[0,4,0]},jobs[2]]};
 ctl(evalBundle([p,q],[[0,0,0],[0,0,0]],1,3,true).z.ok&&!evalBundle([p,q],[[0,0,0],[0,0,0]],1,2,true).z.ok,"endogenous information breaks downward closure");
 ctl(!evalBundle([p,q],[[0,0,0],[0,0,0]],1,3,false).z.ok,"unobserved cost does not reveal");
 ctl(eq(releases([3,5,6],3,4),[1,2]),"two incomparable concessions");
 ctl(eq(releases([3],3,4),[]),"impossible requested goal");
 // Incomplete coverage: no full-domain conclusion, even with enumerated witnesses.
 for(let m of all){let port={bundle:m,coverage:false,status:"UNKNOWN_COVERAGE",authority:"NONE"};ck(port.status==="UNKNOWN_COVERAGE","coverage");out.partialCoverageControls++}
 return out;
}
console.log(JSON.stringify(experiment(make,make2),null,2));
```
