# v3.2 自主认知专项第8轮（累计第67轮）：真实方法契约与反向知识需求规划

2026-11-25。RESEARCH_CANDIDATE。main 89da2969792d09fa4ba8e41325b0ff4e36251fe5；PR #61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，13开放Draft PR。核查最近8提交、v3.2 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（前部及历史全文）、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（相关标题及历史读取，非本轮全文审计）、第6轮9f3294756c22b012a53863df47984043065f4de7、第29轮method_contracts 4ff1666907c362066dcef697d955bc6fb689b75c、第53轮06744930cb28c581f036fd047168cf4dc71fafc7、第66轮1a7a8560ff3349635966857a07a4e71b1680f7f6。前序检索、依赖拓扑、概率支持补证和正向知识推理不重复执行；本轮增量为从有限明确决策目标反向生成当前可执行的补证前沿，区分证据获取、用户价值确认、原生计算准备及科学来源复审。旧Qwen安排已被v3.2替代。

## 实际源码及来源
从固定main实际读取5模块，blob与历史契约一致：decision_feasibility.py 6181d6c578c7ef251e9708d0ffcf65e95d35f88f evaluate及METHOD；decision_scoring.py 7832116703246bafc98831a6039d14c0d691cdd1 _basic_errors/_score_gap/_weight_sensitivity_errors；decision_regret.py e56689a54897d95eaa126540c23fca51cc0eede7 _validate/_validate_points；decision_timing.py 4ed9fa430dcb993cc5005656c8b1744276fe7c33 _common_errors/_option_values；decision_hub.py a97de30f5241063862dbc0ce797c214cbc4d405f validate_gate/run_method。仅静态阅读，没有执行原生Python、完整权重validator、全注册表或实际App。

5个真实方法契约：c028_interval_feasibility@1.0.0、pareto@1.0.0、weight_sensitivity@1.0.0、C029@1.0.0、timing_actions@1.0.0。7份不同知识档案当前blob实际核对（8条方法来源关联，其中C004关联两方法；7条匹配、1条历史变更）：
- C028_INTERVAL_HARD_CONSTRAINT_FEASIBILITY_2026-11-20.md 7cb8d5e3631dd17c0650cec06139d88b5bfcc700
- C004_DYNAMIC_UTILITY_MULTI_OBJECTIVE_ROBUST_2026-10-27.md 0d04c633a26437ad6017946cd528c4dc68db3d83
- C029_SCENARIO_MINIMAX_REGRET_INFORMATION_BOUNDARY_2026-11-20.md a2588cfdd47e547a46a7ee8cde2644caf81198d9
- C009_OPTION_VALUE_INFORMATION_REVERSIBILITY_2026-11-01.md 5048081b0a277f4bc511aff2293020268fd5c57c
- BUEHLER_GRIFFIN_ROSS_1994_PERSONAL_COMPLETION_TIME_FORECAST_BOUNDARY_2026-11-21.md e7e1002f00aab5bf782a5f2845fbfac2cb80969b（历史baseline b611c66afbdeb862353dbad7330916afc57ac45e，CHANGED）
- SAMUELSON_ZECKHAUSER_1988_STATUS_QUO_FRAMING_AUDIT_2026-11-20.md 60ea84e4074a7f78644f3d70f0cbd2822d84374b
- TVERSKY_SHAFIR_1992_CONFLICT_DEFERRAL_OPTION_SET_BOUNDARY_2026-11-21.md b03cdbe2165dd0543fff20cbeaefd6afacf718c4
以上为连接器报告blob及档案前段阅读，非独立原始字节哈希、原论文重审、外部数据复现或新科学准入。C028/C029档案标注合成分析候选，C004为有限方法笔记，不能当成已证个人效果。timing_actions仍需整方法来源复审，不因其他三份匹配而放行。

## 候选合同
限定5条明确中文目标短语（人工词典，非开放语言理解）。发现方法与计算准入分离；goalConfirmed、source identity、gateSourceOK、已核事实和gateReceipt由可信宿主夹具给定，不从用户或检索文本自报。固定候选范围内至少有方案，所有事实状态为同一主体、版本、时域、权限及口径的合格聚合标记；真实字段、完整覆盖、风险、权限和数值合法性仍需独立确认。C028的完整筛查准备要求底线清单已确认，非空时具有合格测量；原生validator仅检查constraints_confirmed，可能在缺测量时合法运行并返回UNRESOLVED，本候选准备度更严格，不作为原生validator的等价替代。明确空清单不需要测量；未知清单必须先核对，不能选择成本较低的空清单假设。下游需要当前有效原生gate结果，且此前置必须仍满足；未得到收据先走内部gate任务，不能因有收据字样就放行。Pareto、weight要求至少两个已接受方案；C029原生允许至少一个，不证明单方案有实质比较价值。方案不足保留复核行动范围，不自动扩大用户范围。Pareto的完整比较准备要求合格得分，原生_basic_errors允许缺单元并保留缺口；不阻断独立描述性局部分析的正式出口。本轮没有实现该局部出口。weight额外需要点值得分、共同效用尺度及权重；C029需要情景、独立共同情景效用合同及点值效用，不依赖weight权重、也不需要虚构概率。情景共同效用不从多目标得分自动推导。timing方法只返回研究复审任务，尚无完整时机补证图。任务仅分类为用户确认、合格证据获取、情景定义/证据、内部gate、研究复审、行动范围复核；不自动联网、不读取个人数据、不代用户确认、无执行权限。

每个节点若前置未完成，返回其最早未完成节点集合；全部完成才检查自身。独立前置并行合并；同一范围的同一任务ID去重；不同主体/时间/权限实际应有不同稳定身份，本轮固定单一共同范围。由有限无环依赖图归纳，前沿只含在当前合同内没有未完成前置的待补节点，且每个未完成叶均由上游返回；已确认不满足方案数为阻塞，不把复核行动当已完成。非最优问询树、无成本最优证明、无自动资料获取。源或状态变化必须重新计算，现有代码未实现持久收据鉴权、版本事务和真实权限。PREPARED_FOR_NATIVE_REVIEW仅研究准备度，非原生适用性通过、科学准入、执行成功或最终建议。

## 实验
3种清单状态×1024个合格字段遮罩×3个已接受数量=9216个合成快照，每个5个方法请求，46080次前沿核验。用直接条件参照独立于递归前沿构造，并核对4个目标联合前沿的同范围任务去重；同一研究者定义合同和夹具，非独立验收。遮罩包含故意不完整及旧收据状态，不能解释为自然出现频率。sourceReview统计时机方法的每次复审返回；unqualifiedReceiptIgnored统计存在收据标记但缺底线前置的下游方法，不能以此推断原生产品漏洞。sharedTasksDeduplicated是前沿任务ID重复项数，不是真实省下的追问数。20项专项控制。开发文本及数值为ChatGPT研发辅助生成的项目原创合成材料，非真人、训练或独立留出。无新外部文献或数据、真实语言覆盖、实际知识获取、真实原生执行、设备资源或用户效果。不是第66轮正向知识证明完整接入；实际结合仍待研究。

## 实际代码和结果
以下JS在连接器计算环境实际执行，Node无需第三方包或网络可复跑。
```js
const probe = function(){
 const ck=(x,m)=>{if(!x)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),uniq=a=>[...new Set(a)].sort();
 const facts=["measurements","gateReceipt","objectives","scores","pointScores","scale","weights","scenarios","regretBasis","utilities"];
 const ids=["c028_interval_feasibility@1.0.0","pareto@1.0.0","weight_sensitivity@1.0.0","C029@1.0.0","timing_actions@1.0.0"];
 const phrases=["判断方案是否违反底线","比较各目标的优势","判断权重改变是否影响选择","比较最坏情景的后悔值","比较现在行动和等待"];
 const methods=Object.fromEntries(phrases.map((p,i)=>[p,ids[i]]));
 const tasks={confirmConstraints:"USER_CONFIRM",measurements:"QUALIFIED_EVIDENCE",gateReceipt:"INTERNAL_NATIVE_GATE",objectives:"USER_CONFIRM",scores:"QUALIFIED_EVIDENCE",pointScores:"QUALIFIED_EVIDENCE",scale:"USER_CONFIRM",weights:"USER_CONFIRM",scenarios:"SCENARIO_DEFINITION_AND_EVIDENCE",regretBasis:"USER_CONFIRM",utilities:"QUALIFIED_EVIDENCE",reviewSources:"RESEARCH_REVIEW",reviewGateSource:"RESEARCH_REVIEW",reviewMethodSource:"RESEARCH_REVIEW",scope:"USER_CONFIRM",addFeasibleOptions:"REVIEW_ACTION_SCOPE"};
 function combine(nodes){return {frontier:uniq(nodes.flatMap(x=>x.frontier)),blocked:uniq(nodes.flatMap(x=>x.blocked))}}
 const done=()=>({frontier:[],blocked:[]}),need=x=>({frontier:[x],blocked:[]}),block=x=>({frontier:[],blocked:[x]});
 const ready=n=>!n.frontier.length&&!n.blocked.length;
 // Only a trusted snapshot supplies facts. This is a planning contract for a
 // complete bounded result, stricter than some native validators.
 function plan(s,request,identity=true,goalConfirmed=true){
  const id=methods[request];if(!id)return {status:"OUT_OF_SCOPE",method:null,frontier:[],blocked:[],authority:"NONE"};
  if(!goalConfirmed)return {status:"NEEDS_SCOPE",method:id,frontier:["scope"],blocked:[],authority:"NONE"};
  const has=x=>s.facts.includes(x);
  const gateInput=()=>{
   if(!s.gateSourceOK)return need("reviewGateSource");
   if(s.inventory==="unknown")return need("confirmConstraints");
   if(s.inventory==="nonempty"&&!has("measurements"))return need("measurements");
   return done();
  };
  function feasible(min){
   const g=gateInput();if(!ready(g))return g;
   if(!has("gateReceipt"))return need("gateReceipt");
   return s.accepted>=min?done():block("addFeasibleOptions");
  }
  const leaf=x=>has(x)?done():need(x);
  function after(deps,x){let n=combine(deps);return ready(n)?leaf(x):n}
  let n;
  if(!identity)n=need("reviewMethodSource");
  else if(id===ids[4])n=need("reviewSources"); // one historical source is CHANGED
  else if(id===ids[0])n=gateInput();
  else if(id===ids[1])n=after([feasible(2),leaf("objectives")],"scores");
  else if(id===ids[2]){
   const score=after([feasible(2),leaf("objectives")],"scores");
   const points=after([score],"pointScores");
   const scale=after([leaf("objectives")],"scale");
   const weights=after([scale],"weights");
   n=combine([points,weights]);
  }else if(id===ids[3])n=after([feasible(1),leaf("scenarios"),leaf("regretBasis")],"utilities");
  return {status:ready(n)?"PREPARED_FOR_NATIVE_REVIEW":n.blocked.length?"BLOCKED":"NEEDS_INPUT",method:id,frontier:n.frontier,blocked:n.blocked,authority:"NONE"};
 }
 // Independent direct reference using sets of earliest outstanding prerequisites.
 // No recursive candidate planner or candidate functions.
 function reference(s,i){
  let fs=new Set(s.facts),f=new Set(),b=new Set();
  let g=!s.gateSourceOK?"reviewGateSource":s.inventory==="unknown"?"confirmConstraints":s.inventory==="nonempty"&&!fs.has("measurements")?"measurements":null;
  if(i===4)return {frontier:["reviewSources"],blocked:[]};
  if(i===0)return {frontier:g?[g]:[],blocked:[]};
  let gg=g||(!fs.has("gateReceipt")?"gateReceipt":null);
  let tooFew=!gg&&s.accepted<(i===3?1:2);
  if(gg)f.add(gg);if(tooFew)b.add("addFeasibleOptions");
  if(i===1||i===2){
   if(!fs.has("objectives"))f.add("objectives");
   if(!gg&&!tooFew&&fs.has("objectives")){
    if(!fs.has("scores"))f.add("scores");else if(i===2&&!fs.has("pointScores"))f.add("pointScores");
   }
   if(i===2&&fs.has("objectives")){if(!fs.has("scale"))f.add("scale");else if(!fs.has("weights"))f.add("weights")}
  }else{
   for(const x of ["scenarios","regretBasis"])if(!fs.has(x))f.add(x);
   if(!gg&&!tooFew&&fs.has("scenarios")&&fs.has("regretBasis")&&!fs.has("utilities"))f.add("utilities");
  }
  return {frontier:uniq([...f]),blocked:uniq([...b])};
 }
 let out={snapshots:0,methodChecks:0,frontierMatches:0,prepared:0,needsInput:0,blocked:0,sourceReview:0,combinedRequests:0,sharedTasksDeduplicated:0,unqualifiedReceiptIgnored:0,controls:0,byMethod:{}};let witnesses={};
 for(const id of ids)out.byMethod[id]={prepared:0,needsInput:0,blocked:0};
 for(const inventory of ["unknown","empty","nonempty"])for(let mask=0;mask<1024;mask++)for(const accepted of [0,1,2]){
  const s={inventory,accepted,gateSourceOK:true,facts:facts.filter((_,i)=>mask&(1<<i))};out.snapshots++;
  const results=phrases.map((p,i)=>{
   const r=plan(s,p),e=reference(s,i);ck(eq(r.frontier,e.frontier)&&eq(r.blocked,e.blocked),"frontier "+JSON.stringify({s,i,r,e}));
   ck(r.authority==="NONE","authority");out.methodChecks++;out.frontierMatches++;
   let k=r.status==="PREPARED_FOR_NATIVE_REVIEW"?"prepared":r.status==="BLOCKED"?"blocked":"needsInput";out[k]++;out.byMethod[ids[i]][k]++;
   if(i===4)out.sourceReview++;
   if(i!==0&&i!==4&&s.facts.includes("gateReceipt")&&(inventory==="unknown"||inventory==="nonempty"&&!s.facts.includes("measurements"))){ck(r.status!=="PREPARED_FOR_NATIVE_REVIEW","unqualified receipt");out.unqualifiedReceiptIgnored++}
   return r;
  });
  // All requested purposes remain separate; deduplicate only identical prerequisite task IDs
  // within this single fully shared synthetic scope.
  const group=results.slice(0,4),merged=uniq(group.flatMap(x=>x.frontier));
  const expected=uniq([0,1,2,3].flatMap(i=>reference(s,i).frontier));
  ck(eq(merged,expected),"multi-goal");out.combinedRequests++;out.sharedTasksDeduplicated+=group.reduce((n,r)=>n+r.frontier.length,0)-merged.length;
  if(!witnesses.shared&&group.reduce((n,r)=>n+r.frontier.length,0)>merged.length&&inventory==="unknown")witnesses.shared={s,frontier:merged,byMethod:group.map(r=>({method:r.method,frontier:r.frontier}))};
 }
 const full={inventory:"nonempty",accepted:2,gateSourceOK:true,facts:facts.slice()};
 for(const [s,i,identity,confirmed,want] of [
  [full,0,true,true,"PREPARED_FOR_NATIVE_REVIEW"],
  [full,1,true,true,"PREPARED_FOR_NATIVE_REVIEW"],
  [full,2,true,true,"PREPARED_FOR_NATIVE_REVIEW"],
  [full,3,true,true,"PREPARED_FOR_NATIVE_REVIEW"],
  [full,4,true,true,"NEEDS_INPUT"],
  [full,3,false,true,"NEEDS_INPUT"],
  [full,3,true,false,"NEEDS_SCOPE"],
  [{...full,gateSourceOK:false},3,true,true,"NEEDS_INPUT"],
  [{...full,accepted:1},1,true,true,"BLOCKED"],
  [{...full,accepted:1},3,true,true,"PREPARED_FOR_NATIVE_REVIEW"],
  [{...full,accepted:0},3,true,true,"BLOCKED"],
  [{...full,facts:full.facts.filter(x=>x!=="pointScores")},2,true,true,"NEEDS_INPUT"],
  [{...full,facts:full.facts.filter(x=>x!=="weights")},1,true,true,"PREPARED_FOR_NATIVE_REVIEW"],
  [{...full,facts:full.facts.filter(x=>x!=="weights")},3,true,true,"PREPARED_FOR_NATIVE_REVIEW"],
  [{...full,inventory:"unknown"},3,true,true,"NEEDS_INPUT"]
 ]){ck(plan(s,phrases[i],identity,confirmed).status===want,"control");out.controls++}
 ck(plan(full,"预测我的整个人生").status==="OUT_OF_SCOPE","unknown goal");out.controls++;
 ck(eq(plan({...full,inventory:"empty",facts:full.facts.filter(x=>x!=="measurements")},phrases[0]).frontier,[]),"empty confirmed");out.controls++;
 ck(eq(plan({...full,facts:full.facts.filter(x=>x!=="gateReceipt")},phrases[3]).frontier,["gateReceipt"]),"native receipt");out.controls++;
 ck(eq(plan({...full,gateSourceOK:false},phrases[0]).frontier,["reviewGateSource"]),"source review");out.controls++;
 ck(eq(plan(full,phrases[4]).frontier,["reviewSources"]),"timing not released");out.controls++;
 witnesses.weightMissing={pareto:plan({...full,facts:full.facts.filter(x=>x!=="weights")},phrases[1]),weight:plan({...full,facts:full.facts.filter(x=>x!=="weights")},phrases[2]),regret:plan({...full,facts:full.facts.filter(x=>x!=="weights")},phrases[3])};
 return {out,witnesses,taskKinds:tasks};
};
console.log(JSON.stringify(probe(),null,2));
```
```json
{
  "out": {
    "snapshots": 9216,
    "methodChecks": 46080,
    "frontierMatches": 46080,
    "prepared": 5016,
    "needsInput": 37224,
    "blocked": 3840,
    "sourceReview": 9216,
    "combinedRequests": 9216,
    "sharedTasksDeduplicated": 23232,
    "unqualifiedReceiptIgnored": 6912,
    "controls": 20,
    "byMethod": {
      "c028_interval_feasibility@1.0.0": {
        "prepared": 4608,
        "needsInput": 4608,
        "blocked": 0
      },
      "pareto@1.0.0": {
        "prepared": 192,
        "needsInput": 7488,
        "blocked": 1536
      },
      "weight_sensitivity@1.0.0": {
        "prepared": 24,
        "needsInput": 7656,
        "blocked": 1536
      },
      "C029@1.0.0": {
        "prepared": 192,
        "needsInput": 8256,
        "blocked": 768
      },
      "timing_actions@1.0.0": {
        "prepared": 0,
        "needsInput": 9216,
        "blocked": 0
      }
    }
  },
  "witnesses": {
    "shared": {
      "s": {
        "inventory": "unknown",
        "accepted": 0,
        "gateSourceOK": true,
        "facts": []
      },
      "frontier": [
        "confirmConstraints",
        "objectives",
        "regretBasis",
        "scenarios"
      ],
      "byMethod": [
        {
          "method": "c028_interval_feasibility@1.0.0",
          "frontier": [
            "confirmConstraints"
          ]
        },
        {
          "method": "pareto@1.0.0",
          "frontier": [
            "confirmConstraints",
            "objectives"
          ]
        },
        {
          "method": "weight_sensitivity@1.0.0",
          "frontier": [
            "confirmConstraints",
            "objectives"
          ]
        },
        {
          "method": "C029@1.0.0",
          "frontier": [
            "confirmConstraints",
            "regretBasis",
            "scenarios"
          ]
        }
      ]
    },
    "weightMissing": {
      "pareto": {
        "status": "PREPARED_FOR_NATIVE_REVIEW",
        "method": "pareto@1.0.0",
        "frontier": [],
        "blocked": [],
        "authority": "NONE"
      },
      "weight": {
        "status": "NEEDS_INPUT",
        "method": "weight_sensitivity@1.0.0",
        "frontier": [
          "weights"
        ],
        "blocked": [],
        "authority": "NONE"
      },
      "regret": {
        "status": "PREPARED_FOR_NATIVE_REVIEW",
        "method": "C029@1.0.0",
        "frontier": [],
        "blocked": [],
        "authority": "NONE"
      }
    }
  },
  "taskKinds": {
    "confirmConstraints": "USER_CONFIRM",
    "measurements": "QUALIFIED_EVIDENCE",
    "gateReceipt": "INTERNAL_NATIVE_GATE",
    "objectives": "USER_CONFIRM",
    "scores": "QUALIFIED_EVIDENCE",
    "pointScores": "QUALIFIED_EVIDENCE",
    "scale": "USER_CONFIRM",
    "weights": "USER_CONFIRM",
    "scenarios": "SCENARIO_DEFINITION_AND_EVIDENCE",
    "regretBasis": "USER_CONFIRM",
    "utilities": "QUALIFIED_EVIDENCE",
    "reviewSources": "RESEARCH_REVIEW",
    "reviewGateSource": "RESEARCH_REVIEW",
    "reviewMethodSource": "RESEARCH_REVIEW",
    "scope": "USER_CONFIRM",
    "addFeasibleOptions": "REVIEW_ACTION_SCOPE"
  }
}
```

## 下一步
研究自主知识卡中真正可复用的数值推导及语义身份连接（优先选有来源的确定性公式，区分原始事实、可合法推导量、用户偏好及情景假设），连接第62/63/64/66/67轮并执行有限真实原生数学接口；先核查既有第54轮避免重复。继续积累完整版本，不发布零碎Codex任务。产品轨维护交接、独立轨另冻未见白话和方法/证据范围，模型轨核对正式方法输入及输出。未修改生产代码、训练、CI、Codex任务、合并、部署、个人数据或第三方AI运行时，零新增费用，冻结协议不变。