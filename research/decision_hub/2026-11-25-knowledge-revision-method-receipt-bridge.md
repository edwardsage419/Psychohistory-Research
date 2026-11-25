# 自主认知专项累计第106轮候选：知识撤回与方法准备收据的修订失效桥接

2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / SYNTHETIC_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main f598110c6a6ad96e5217e2fa87ad0737397eb539。核对15近期提交、13开放PR（#61待审）、v3.2全文、同步规程前30行、唯一交接前18行、R105全文、R64前30行、R54前18行及R66/R67完整代码。唯一交接 blob 5e74f4f0b37141d631740e844ad8bbbfed232e07。增量为R66实际知识闭包及冲突报告接入R67实际准备规划，修订绑定的合成收据和跨方法选择性失效；与R105的概念候选及方法卡身份并列接口不同。没有重建概念识别或真实知识图谱。

## 固定资产
research/decision_hub/2026-11-25-grounded-knowledge-provenance-inference.md 1a7a8560ff3349635966857a07a4e71b1680f7f6
research/decision_hub/2026-11-25-native-method-backward-knowledge-planning.md ca51e90ab907c50524243231dc905f7ad1067ea8
原有R66的M+在本轮仅人工映射为合成measurements资格；抽象命题不能推出真实测量数值、单位、目标或知识科学资格。仅用于测试宿主资格传播。用户目标在所有夹具中已独立确认，方法来源身份及共有筛查来源固定通过；timing_actions仍依原R67保留复审。R66冲突传播采用原算法的保守策略（含未使用替代分支）。候选收据为旧快照scope、constraint、完整规则掩码及M+最小支持集列表。任一字段变化或知识不合格，旧收据不得作为当前准备凭证；保守比较整个规则掩码和所有支持集，可能在替代证明仍有效时额外重算。未改变实际数学引擎。scope和constraint改变后清单待确认；objective改变只撤回目标得分、点值、尺度及权重，明确独立的情景效用合同保留。假设两个已接受方案，非真实gate输出；即使夹具有收据，原生执行未运行。实际生产还须绑定完整约束、候选、主体、单位、有效期、来源、权限、原生结果、引擎版本及防重放身份；本候选没有可信授权、原生收据鉴权、并发事务、持久化或真实跨轮解析。

64来源掩码×64规则掩码×2范围版本×2约束版本×2目标版本=32768快照；每快照5方法。使用R66布尔模型交集参照、独立图传递闭包和R67直接条件参照核对实际桥接。相同研究者定义夹具与参照，非独立评价。缓存基线刻意使用旧完整输入不失效；naiveFalsePrepared仅表示夹具相对合同的错误准备，不能解释为原生产品错误率。准备状态authority NONE，不代表执行、推荐或科学准入。所有合成材料为ChatGPT辅助研发项目原创开发材料，非真人、授权训练、独立留出。无新外部资料、第三方AI运行时、训练、CI、费用、部署、PR合并或冻结协议变更。

## 可复算代码
从固定Git版本读取上述两报告全文，分别以字符串docs[0].content及docs[1].content供给。Node标准JS，无其他依赖。
```js
function load(doc,marker,names){const s=doc.split("```js\n")[1].split("\n```")[0].split(marker)[0];return Function(s+"\nreturn {"+names+"};\n};\nreturn probe();")()}
const K=load(docs[0].content," let out={graphs:","report,oracle,rules");
const P=load(docs[1].content," let out={snapshots:","plan,reference,facts,ids,phrases");
function experiment(K,P){
 const ck=(x,m)=>{if(!x)throw Error(m)},eq=(x,y)=>JSON.stringify(x)===JSON.stringify(y);
 const old={sm:4,rm:63,scope:1,constraint:1,objective:1};
 const start=K.report(old.sm,old.rm);
 function ticket(s,r){return [s.scope,s.constraint,s.rm,r.supports[6]]}
 const original=ticket(old,start);
 function qualified(r){return r.supports[6].length>0&&!r.methodReview}
 function assemble(s,r){
  const facts=P.facts.filter(x=>!["measurements","gateReceipt"].includes(x));
  if(s.scope!==old.scope)facts.length=0;
  if(s.objective!==old.objective)for(const x of ["objectives","scores","pointScores","scale","weights"]){let i=facts.indexOf(x);if(i>=0)facts.splice(i,1)}
  if(qualified(r)){facts.push("measurements");if(eq(ticket(s,r),original))facts.push("gateReceipt")}
  return {inventory:s.scope===1&&s.constraint===1?"nonempty":"unknown",accepted:2,gateSourceOK:true,facts};
 }
 let out={snapshots:0,methodChecks:0,oracleMatches:0,prepared:0,naiveFalsePrepared:0,staleTicketRejected:0,scopeChanges:0,objectiveChanges:0,knowledgeUnqualified:0,unchangedTicket:0,controls:0,byMethod:{},example:{}};
 for(let i=0;i<5;i++)out.byMethod[P.ids[i]]={prepared:0,naiveFalsePrepared:0};
 for(let sm=0;sm<64;sm++)for(let rm=0;rm<64;rm++){
  let r=K.report(sm,rm),o=K.oracle(sm,rm);ck(eq(r.supports,o),"knowledge oracle");
  // Independent reachability from explicit conflicting signed atoms, using graph transitive closure.
  const n=7, reach=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j));
  K.rules.forEach((rule,i)=>{if(rm&(1<<i))for(const b of rule.body)reach[b][rule.head]=true});
  for(let k=0;k<n;k++)for(let i=0;i<n;i++)for(let j=0;j<n;j++)reach[i][j] ||= reach[i][k]&&reach[k][j];
  const conflict=[[0,1],[4,5]].filter(([a,b])=>o[a].length&&o[b].length).flat().some(i=>reach[i][6]);
  const good=o[6].length>0&&!conflict;ck(good===qualified(r),"conflict oracle");
  for(let scope of [1,2])for(let constraint of [1,2])for(let objective of [1,2]){
   const s={sm,rm,scope,constraint,objective},a=assemble(s,r);
   const same=scope===1&&constraint===1&&rm===63&&eq(o[6],start.supports[6])&&good;
   const expected={inventory:scope===1&&constraint===1?"nonempty":"unknown",accepted:2,gateSourceOK:true,facts:P.facts.filter(x=>x==="measurements"?good:x==="gateReceipt"?same:scope===1&&(!["objectives","scores","pointScores","scale","weights"].includes(x)||objective===1))};
   ck(eq([...a.facts].sort(),[...expected.facts].sort()),"fact binding");
   out.snapshots++;if(!same)out.staleTicketRejected++;else out.unchangedTicket++;if(scope===2)out.scopeChanges++;if(objective===2)out.objectiveChanges++;if(!good)out.knowledgeUnqualified++;
   const cached={inventory:"nonempty",accepted:2,gateSourceOK:true,facts:P.facts};
   for(let i=0;i<5;i++){
    let z=P.plan(a,P.phrases[i]),e=P.reference(expected,i),naive=P.plan(cached,P.phrases[i]);
    ck(eq(z.frontier,e.frontier)&&eq(z.blocked,e.blocked)&&z.authority==="NONE","planner");
    const ready=!e.frontier.length&&!e.blocked.length;ck((z.status==="PREPARED_FOR_NATIVE_REVIEW")===ready,"ready");
    out.methodChecks++;out.oracleMatches++;
    if(ready){out.prepared++;out.byMethod[P.ids[i]].prepared++}
    if(naive.status==="PREPARED_FOR_NATIVE_REVIEW"&&!ready){out.naiveFalsePrepared++;out.byMethod[P.ids[i]].naiveFalsePrepared++}
    if(sm===4&&rm===63&&scope===1&&constraint===1&&objective===2)out.example[P.ids[i]]=z;
   }
  }
 }
 const full=assemble(old,start);
 for(const t of [()=>qualified(start),()=>full.facts.includes("gateReceipt"),()=>!assemble({...old,constraint:2},start).facts.includes("gateReceipt"),()=>!assemble({...old,scope:2},start).facts.includes("gateReceipt"),()=>assemble({...old,objective:2},start).facts.includes("gateReceipt"),()=>!assemble({...old,sm:0},K.report(0,63)).facts.includes("measurements"),()=>!assemble({...old,sm:20},K.report(20,63)).facts.includes("measurements"),()=>out.example[P.ids[1]].status==="NEEDS_INPUT",()=>out.example[P.ids[3]].status==="PREPARED_FOR_NATIVE_REVIEW",()=>out.methodChecks===163840]){ck(t(),"control");out.controls++}
 return out
}
console.log(JSON.stringify(experiment(K,P),null,2));
```
## 实测
```json
{
  "snapshots": 32768,
  "methodChecks": 163840,
  "oracleMatches": 163840,
  "prepared": 532,
  "naiveFalsePrepared": 130540,
  "staleTicketRejected": 32760,
  "scopeChanges": 16384,
  "objectiveChanges": 16384,
  "knowledgeUnqualified": 30704,
  "unchangedTicket": 8,
  "controls": 10,
  "byMethod": {
    "c028_interval_feasibility@1.0.0": {
      "prepared": 516,
      "naiveFalsePrepared": 32252
    },
    "pareto@1.0.0": {
      "prepared": 4,
      "naiveFalsePrepared": 32764
    },
    "weight_sensitivity@1.0.0": {
      "prepared": 4,
      "naiveFalsePrepared": 32764
    },
    "C029@1.0.0": {
      "prepared": 8,
      "naiveFalsePrepared": 32760
    },
    "timing_actions@1.0.0": {
      "prepared": 0,
      "naiveFalsePrepared": 0
    }
  },
  "example": {
    "c028_interval_feasibility@1.0.0": {
      "status": "PREPARED_FOR_NATIVE_REVIEW",
      "method": "c028_interval_feasibility@1.0.0",
      "frontier": [],
      "blocked": [],
      "authority": "NONE"
    },
    "pareto@1.0.0": {
      "status": "NEEDS_INPUT",
      "method": "pareto@1.0.0",
      "frontier": [
        "objectives"
      ],
      "blocked": [],
      "authority": "NONE"
    },
    "weight_sensitivity@1.0.0": {
      "status": "NEEDS_INPUT",
      "method": "weight_sensitivity@1.0.0",
      "frontier": [
        "objectives"
      ],
      "blocked": [],
      "authority": "NONE"
    },
    "C029@1.0.0": {
      "status": "PREPARED_FOR_NATIVE_REVIEW",
      "method": "C029@1.0.0",
      "frontier": [],
      "blocked": [],
      "authority": "NONE"
    },
    "timing_actions@1.0.0": {
      "status": "NEEDS_INPUT",
      "method": "timing_actions@1.0.0",
      "frontier": [
        "reviewSources"
      ],
      "blocked": [],
      "authority": "NONE"
    }
  }
}
```
后续：以真实语义修订、原生收据与证据资格连接代替人工映射，测试实际输入值变化、撤权及跨版本恢复；保留独立留出、真实语义泛化及产品端验收，未授权正式开发。产品轨维护唯一交接。
