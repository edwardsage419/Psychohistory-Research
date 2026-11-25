# 自主认知专项累计第111轮候选：统一研究结果信封及分层状态隔离
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / SYNTHETIC_DEVELOPMENT / NATIVE_PLATFORM_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 21d737e835d1a99ca2a41c9dee566d656075e41c。核对近期12提交、13开放PR（#61待审）、v3.2全文、同步规程前30行、唯一交接前25行、R50前22行、R60前35行、R105/R110前22行、R106源码及下列六项完整源码。旧R50/R60规格保留历史，冲突的Qwen安排由v3.2取代。R102已有候选原文范围，R67已有需求规划，R101已有实际账本与研究DP，R107已有事务模型，R110已有用途与长期规划实验；新增统一的分层结果信封和分支级当前性检查，非新建算法、正式产品schema或完整版本规范。
## 固定资产
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-25-unified-candidate-obligation-interface.md bdf9bc7a42f33d9c48708970d6ac03a78ef276de
research/decision_hub/2026-11-25-native-method-backward-knowledge-planning.md ca51e90ab907c50524243231dc905f7ad1067ea8
research/decision_hub/2026-11-25-semantic-resource-ledger-temporal-bridge.md 65008b82d4720e931c99bd66ed03228b1f8ef69e
research/decision_hub/2026-11-25-complementarity-realization-timing.md a1ea992561b43252c99e882494640b290a8fa5a4
research/decision_hub/2026-11-25-integrated-ledger-planning-candidate.md 907f12081ddce7bb752ae498bcf21f4b4b218a60
R50 4d394d2cb6e1e1dfc667f2a8806f896a36bbdbef；R60 b6826e37638286947f1eff691d07d57bf4e7d10e；R105 c1593a63195955f492140d21a54f34162fbcea8a；R110 c9f8c9741eb2b021dddb2e9f795da624068f8f7f；唯一交接 5e74f4f0b37141d631740e844ad8bbbfed232e07。
## 候选合同
共同字段schema/lane/version/kind/scope/input/state/authority/payload，分别标记语义诊断、方法准备及研究数学计算。独立可信宿主提供所需分支清单、会话主体用途代次、确认过的结构化数学输入和记录覆盖。R102 propose/audit使用R74真实scan及独立人工合成义务；锚匹配仍UNVERIFIED；空义务夹具不证明理解任意文本。R67原plan仅C028准备，不提供真实原生gate收据、accepted固定0，不执行C028；不把语义匹配升级为已确认输入。R101 bridge/valid中的bridge实际执行R100 ledger和R99 DP，固定当前日、两实际记录根清单、四期两情景0/4；独立结构化规划输入与语义分支完全分开，因此语义未识别仍可提供已经确认的局部研究计算。绝不宣称已从原文自主理解到长期规划。信封的verify重新生成对应分支并比较完整规范化结构，适用于有限合成输入，不是签名、可靠序列化标准、真正授权或原生执行证明。每分支只绑定在该固定合同内使用的变量；log、模型版本、源身份、完整语义义务、时点均固定夹具，未来可变输入需要纳入依赖；全局代次改变全部失效。当前只输出状态元数据，payload内部含R101全日志结构快照，不可直接导出私有内容。未实现真实权限、跨端存储、撤回擦除、原子发布、输入攻击防护、资源预算或实际产品展示。不同分支不共享已确认事实、不自动选择方法，未来须连接可信语义投影。没有总体PASS或推荐资格，所有authority NONE。缺分支明确MISSING，重复/未知分支集合拒绝；状态不可借用其他分支。研究者选择的版本标签、分支边界与严格重算规则尚非产品政策。
## 实验
2文本×2候选数×2语义覆盖×2目标确认×2测量资格×2方法身份×2账本覆盖×2到账资格×2期初余额=512合成上下文。各分支状态以独立有限条件核对，R99枚举核对合格规划终点组，语义锚成员查询复用propose（非独立理解真值）。所有信封以真实原有候选函数生成。globalFalseSuccess计若简单把任何一个方法准备或研究计算的正状态提升为全局成功的上下文，属于故意不合法基线；partialContexts为其中至少一层未具正状态的情景，不能当产品误差率。跨分支、修改版本/状态/权威字段等全部重算核对；同一研究者、非独立验收。重复调用计数不视为独立科学样本。无新增外部事实、费用、训练、Codex、CI、生产修改、PR合并、部署或冻结变更。所有合成材料为ChatGPT辅助研发原创开发夹具，非真人、训练或独立留出。
## 复算
将固定六份Markdown全文按上列顺序置于docs[i].content。仅加载已审查自有代码，不执行任意网络文本。Node标准JS。
```js
function code(doc){return doc.content.split("```js\n")[1].split("\n```")[0]}
function loadExperiment(doc,marker,exports,args="",values=[]){const s=code(doc);let start=s.indexOf("function experiment(");return Function(...args.split(",").filter(Boolean),s.slice(start).split(marker)[0]+"\nreturn {"+exports+"};\n}\nreturn experiment("+args+");")(...values)}
function loadAll(docs){
 const Scan=loadExperiment(docs[0]," const blank=()=>","scan");
 const Sem=loadExperiment(docs[1]," let o={datasets:","propose,audit","IR,Scan,docs,assets",[null,Scan,null,null]);
 const M=Function(code(docs[2]).split(" let out={snapshots:")[0]+"\nreturn {plan,reference,facts,phrases};\n};\nreturn probe();")();
 const L=loadExperiment(docs[3]," let o={scenarios:","parse,ingest,view");
 const P=loadExperiment(docs[4]," let o={scenarios:","dp,oracle,pack");
 const B=loadExperiment(docs[5]," let o={scenarios:","bridge,valid","L,P",[L,P]);
 return {Sem,M,L,P,B}
}
function experiment(A){
 const {Sem,M,L,P,B}=A,ck=(v,m)=>{if(!v)throw Error(m)},clone=x=>JSON.parse(JSON.stringify(x));
 const canon=x=>x===null||typeof x!=="object"?JSON.stringify(x):Array.isArray(x)?"["+x.map(canon).join(",")+"]":"{"+Object.keys(x).sort().map(k=>JSON.stringify(k)+":"+canon(x[k])).join(",")+"}";
 const eq=(a,b)=>canon(a)===canon(b);
 const log=[];for(let e of [{id:"b",text:"实际R2第1日到账1美元",received:1,qualified:true},{id:"a",text:"实际R1第2日到账3美元",received:2,qualified:true},{id:"c",text:"更正实际R1第2日到账4美元，替代版本1",received:4,qualified:true}])ck(L.ingest(log,e)==="ACCEPT","ingest");
 const ids=["semantic","method","longitudinal"];
 const specs={semantic:{version:"R102",kind:"DIAGNOSTIC",states:["ANCHORS_ONLY","INCOMPLETE_ANCHORS","UNKNOWN_COVERAGE","LIMIT_OR_INVALID","EMPTY_FIXTURE_SCOPE","INVALID_BINDING","LIMIT","INVALID"]},method:{version:"R67",kind:"PREPARATION",states:["PREPARED_FOR_NATIVE_REVIEW","NEEDS_INPUT","NEEDS_SCOPE","BLOCKED","OUT_OF_SCOPE"]},longitudinal:{version:"R101",kind:"RESEARCH_CALCULATION",states:["CONDITIONAL","UNKNOWN_SOURCE","UNKNOWN_QUALIFICATION","UNKNOWN_RECONCILIATION","UNKNOWN_TIME","UNKNOWN_LANGUAGE","UNKNOWN_COVERAGE","LIMIT"]}};
 function inputs(c,lane){
  let scope={session:"S",subject:"U",purpose:lane,generation:c.generation};
  if(lane==="semantic")return {scope,text:c.text,covered:c.covered,k:c.k};
  if(lane==="method")return {scope,goal:c.goal,measurement:c.measurement,methodIdentity:c.methodIdentity};
  return {scope,covered:c.ledgerCovered,source:c.source,opening:c.opening};
 }
 function produce(c,lane){
  const spec=specs[lane],x=inputs(c,lane);let payload;
  if(lane==="semantic"){
   const bundle=Sem.propose(x.text,x.scope,x.k);
   // Independent fixture marks exact whole original span as a constraint.
   // For a nonspecific message the obligation is deliberately absent, not a coverage proof.
   const obs=x.text==="每月支出最多100美元"?[{id:"fixture-C",role:"constraint",span:{start:0,end:x.text.length,text:x.text,encoding:"UTF16"}}]:[];
   payload=Sem.audit(bundle,x.text,x.scope,x.k,obs,x.covered);
  }else if(lane==="method"){
   // No native gate receipt in this experiment. Structured input supplied
   // independently by trusted fixture, never promoted from semantic anchors.
   payload=M.plan({inventory:"nonempty",accepted:0,gateSourceOK:true,facts:x.measurement?["measurements"]:[]},M.phrases[0],x.methodIdentity,x.goal);
  }else{
   const host={qualified:true,covered:x.covered,generation:x.scope.generation,asOf:4,opening:x.opening};
   const req={text:"用当前余额完成旧计划并培训",day:4,asOf:4,generation:x.scope.generation};
   payload=B.bridge(log,req,new Set(x.source?["b","c"]:["b","a"]),[{root:"R2",day:1},{root:"R1",day:2}],{hours:4,income:0,reserve:0,finish:2,cost:1},host);
  }
  ck(spec.states.includes(payload.status)&&payload.authority==="NONE","upstream contract");
  return {schema:"research-envelope@1",lane,version:spec.version,kind:spec.kind,scope:x.scope,input:x,state:payload.status,authority:"NONE",payload}
 }
 function verify(r,c,lane){
  if(!r||!ids.includes(lane))return false;
  return eq(r,produce(c,lane))
 }
 function present(rows,c){
  // Trusted independent list of requested lanes. Unknown or duplicate lanes
  // must not silently substitute for a missing one.
  let seen=new Set();for(let r of rows){if(!r||!ids.includes(r.lane)||seen.has(r.lane))return {state:"INVALID_SET",authority:"NONE"};seen.add(r.lane)}
  return {state:"RESEARCH_ONLY",authority:"NONE",lanes:ids.map(lane=>{
   let r=rows.find(x=>x.lane===lane);
   if(!r)return {lane,state:"MISSING"};
   if(!verify(r,c,lane))return {lane,state:"STALE_OR_INVALID"};
   return {lane,state:r.state,kind:r.kind};
  })}
 }
 let o={contexts:0,receipts:0,valid:0,semanticChecks:0,methodChecks:0,planningChecks:0,partialContexts:0,prepared:0,conditional:0,globalFalseSuccess:0,mutationsRejected:0,scopeCrossRejected:0,selectiveRetained:0,selectiveRejected:0,controls:0,example:null};
 for(const text of ["每月支出最多100美元","以后怎么办"])for(const k of [0,50])for(const covered of [false,true])for(const goal of [false,true])for(const measurement of [false,true])for(const methodIdentity of [false,true])for(const ledgerCovered of [false,true])for(const source of [false,true])for(const opening of [0,2]){
  const c={text,k,covered,goal,measurement,methodIdentity,ledgerCovered,source,opening,generation:1};
  let rows=ids.map(l=>produce(c,l)),v=present(rows,c);o.contexts++;o.receipts+=3;
  ck(v.state==="RESEARCH_ONLY"&&v.authority==="NONE"&&v.lanes.every((l,i)=>l.state===rows[i].state),"presentation");o.valid+=3;
  // Independently compare exact branch contracts. For semantic search,
  // anchor membership is read directly from candidate output (not a gold truth claim).
  const b=Sem.propose(text,rows[0].scope,k);let matched=b.items.some(x=>x.role==="constraint"&&x.span.start===0&&x.span.end===text.length);
  const wantSem=!covered?"UNKNOWN_COVERAGE":text==="以后怎么办"?"EMPTY_FIXTURE_SCOPE":matched?"ANCHORS_ONLY":"INCOMPLETE_ANCHORS";
  ck(rows[0].state===wantSem&&rows[0].payload.semanticStatus==="UNVERIFIED","sem");o.semanticChecks++;
  const wantM=!goal?"NEEDS_SCOPE":!methodIdentity||!measurement?"NEEDS_INPUT":"PREPARED_FOR_NATIVE_REVIEW";
  ck(rows[1].state===wantM,"method");o.methodChecks++;o.prepared+=+(wantM==="PREPARED_FOR_NATIVE_REVIEW");
  const wantP=!ledgerCovered?"UNKNOWN_QUALIFICATION":!source?"UNKNOWN_SOURCE":"CONDITIONAL";
  ck(rows[2].state===wantP,"plan");if(wantP==="CONDITIONAL"){let p=P.oracle({cash:opening+5,hours:4,income:0,reserve:0,finish:2,cost:1},[0,4]);ck(rows[2].payload.balance===opening+5&&eq(rows[2].payload.trained,P.pack(p.trained))&&eq(rows[2].payload.old,P.pack(p.old)),"plan oracle");o.conditional++}
  o.planningChecks++;
  if(wantM==="PREPARED_FOR_NATIVE_REVIEW"||wantP==="CONDITIONAL"){
   o.globalFalseSuccess++;if(wantSem!=="ANCHORS_ONLY"||wantM!=="PREPARED_FOR_NATIVE_REVIEW"||wantP!=="CONDITIONAL")o.partialContexts++;
  }
  for(let i=0;i<3;i++){
   for(let change of [r=>r.authority="EXECUTE",r=>r.kind="FINAL",r=>r.version="other",r=>r.scope.generation++,r=>r.state="PASS",r=>r.payload.authority="EXECUTE",r=>delete r.input]){
    let r=clone(rows[i]);change(r);ck(!verify(r,c,ids[i]),"mutation");o.mutationsRejected++
   }
   ck(!verify(rows[i],c,ids[(i+1)%3]),"cross lane");o.scopeCrossRejected++;
   ck(!verify(rows[i],{...c,generation:2},ids[i]),"generation");o.scopeCrossRejected++;
  }
  for(const [changed,lane] of [[{...c,k:k===0?50:0},"semantic"],[{...c,goal:!goal},"method"],[{...c,opening:2-opening},"longitudinal"]]){
   for(let r of rows){const valid=verify(r,changed,r.lane);ck(valid===(r.lane!==lane),"selective");if(valid)o.selectiveRetained++;else o.selectiveRejected++}
  }
  if(!o.example&&wantP==="CONDITIONAL"&&wantM==="NEEDS_SCOPE"&&wantSem==="INCOMPLETE_ANCHORS")o.example=v;
 }
 let c={text:"以后怎么办",k:0,covered:true,goal:true,measurement:true,methodIdentity:true,ledgerCovered:true,source:true,opening:0,generation:1},rows=ids.map(l=>produce(c,l));
 for(let t of [()=>present([rows[0],rows[0]],c).state==="INVALID_SET",()=>present([{lane:"foreign"}],c).state==="INVALID_SET",()=>present([],c).lanes.every(x=>x.state==="MISSING"),()=>present([rows[2]],c).lanes[2].state==="CONDITIONAL",()=>present(rows,{...c,generation:2}).lanes.every(x=>x.state==="STALE_OR_INVALID"),()=>o.contexts===512,()=>o.valid===3*o.contexts,()=>o.selectiveRejected===3*o.contexts]){ck(t(),"control");o.controls++}
 return o
}
console.log(JSON.stringify(experiment(loadAll(docs)),null,2));
```
## 实测
```json
{
  "contexts": 512,
  "receipts": 1536,
  "valid": 1536,
  "semanticChecks": 512,
  "methodChecks": 512,
  "planningChecks": 512,
  "partialContexts": 174,
  "prepared": 64,
  "conditional": 128,
  "globalFalseSuccess": 176,
  "mutationsRejected": 10752,
  "scopeCrossRejected": 3072,
  "selectiveRetained": 3072,
  "selectiveRejected": 1536,
  "controls": 8,
  "example": {
    "state": "RESEARCH_ONLY",
    "authority": "NONE",
    "lanes": [
      {
        "lane": "semantic",
        "state": "INCOMPLETE_ANCHORS",
        "kind": "DIAGNOSTIC"
      },
      {
        "lane": "method",
        "state": "NEEDS_SCOPE",
        "kind": "PREPARATION"
      },
      {
        "lane": "longitudinal",
        "state": "CONDITIONAL",
        "kind": "RESEARCH_CALCULATION"
      }
    ]
  }
}
```
下一步：将可变原文义务、证据、计算收据及R107/R108/R109用途和代次合同接入同一版本化接口；优先解决真实开放语言、原生入口及独立验证瓶颈，避免以更多重复有限枚举替代证据。产品轨维护唯一交接，正式版本仍待所有者授权。
