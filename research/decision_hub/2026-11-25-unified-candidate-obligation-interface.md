# 自主认知专项累计第102轮候选：原文候选与独立语义义务的统一研究接口

2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_INTEGRATION_EXECUTED / PUBLIC_SYNTHETIC_DEVELOPMENT / NATIVE_NOT_RUN / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线main 4dc2396abfe47ebc95327b3da715462455ca5a5a。核对近20提交、13开放PR（#61待审）、v3.2首22行、唯一交接首22行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R58/R73/R74/R101首22行及R73/R74完整代码。实际复用R73统一标注IR build/restore/verify及R74原文scan/gold；新增共同候选输出、独立义务对齐及失败保留接口，非重新训练或重写候选搜索。R58为既有质量合同，本轮只测原文跨度和角色对齐、候选覆盖未知及范围绑定，不声称执行R58全部质量门或R101长期规划链。

## 固定输入
research/decision_hub/2026-11-25-unified-semantic-annotation-bridge.md af648d16ee96b9af4a3efb61b413d113208bb0ca
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
读取完整报告与两份JSON并核对blob。仅加载可信固定自有研究代码，禁止生产执行任意外部内容。32情节64轮167标注，项目原创ChatGPT研发辅助合成开发样例，非真人、独立留出或授权训练。原文生成候选不读标注，义务从另一条固定标注路径导入，使用R73 span UTF16、角色及独立edit维度。R74历史固定词汇、权重、topK和排序不改；S中replace/retract另有revision义务，可与原角色并存。其他角色不在搜索能力范围，保留UNSUPPORTED_ROLE，不删除。完整义务清单只是既有开发标注（未证明真实原文全部义务）；所有结果authority NONE、semanticStatus UNVERIFIED、outside true。人工covered仅代表夹具给定范围，不是实际开放语言覆盖。锚点完全匹配仅为粗角色及原文位置对齐，未验证主体、时间、条件、单位、比较方向、真实指代或语义真值。未模拟真实用户确认、权限、事实证据、数学调用或自动执行。

## 接口
propose(text,scope,k,cap)：仅原文及范围进入既有R74 scan，候选包含稳定范围内角色跨度ID、原文UTF16、原分数与NONE；每角色topK、覆盖未验证。scope包含固定数据blob/情节/轮/修订，真实会话权限与版本需更完整。audit重新生成同范围候选并作结构比较，保留外部义务列表及每条ANCHOR_MATCHED/MISSING_CANDIDATE/UNSUPPORTED_ROLE，不以候选清空义务；空清单只为夹具空范围，不确认没有底线。独立覆盖缺失保留UNKNOWN_COVERAGE；所有锚点匹配也仅ANCHORS_ONLY，不给确认资格。未使用R73标注作为算法输入或候选修复。无密码学签名、外部身份认证、真实并发、持久化或防任意恶意输入证明。输出条数cap在生成完整列表后才检查，超限无候选，但不保护搜索/排序内存或时间；不是全请求预算。重算验绑定有额外开销，完整一致性会保守拒绝其他合法候选实现。原文候选角色仅三类，尚未整合概念/指代/数量模型或原生方法。

## 实验
64轮×4个每角色预算0/1/10/50。R73完整转换与恢复核验、独立R74 gold规则对照目标角色集合，逐义务核验排名成员关系。所有未支持角色及未命中义务保留，不将未标注视为负例，不报精度。naiveNonemptyIncomplete统计只要有任一候选就假定完整的错误代理在已有标注范围仍不全的次数，非实际放行或真实产品错误率；naiveEmptyWithObligations统计空候选但仍有已有标注义务。候选版本/角色/跨度/权限/覆盖篡改或删项与重算比较拒绝；不证明对抗安全。所有匹配与参照同研究者、同源公开开发资料，非独立泛化验证。11专项控制。参数、适配方式、闭域夹具及预算由研究者选定。无新增外部资料、训练、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。保留正式版本范围及验收门。

## 复算
按固定输入顺序加载报告文本及JSON，assets为对应{id:"L"/"S",path,sha}。仅执行已核验可信自有代码。
```js
function load(text,marker,names){
 let src=text.split("```js\n")[1].split("\n```")[0].split(marker)[0];
 return Function(src+"\nreturn {"+names+"};\n}\nreturn experiment();")()
}
function experiment(IR,Scan,docs,assets){
 const ck=(v,m)=>{if(!v)throw Error(m)},roles=["constraint","action","revision"],canon=x=>x===null||typeof x!=="object"?JSON.stringify(x):Array.isArray(x)?"["+x.map(canon).join(",")+"]":"{"+Object.keys(x).sort().map(k=>JSON.stringify(k)+":"+canon(x[k])).join(",")+"}",eq=(a,b)=>canon(a)===canon(b),clone=x=>JSON.parse(JSON.stringify(x));
 // The adapter's only input for proposal generation is the original text and scope.
 function propose(text,scope,k,cap=10000){
  if(!Number.isInteger(k)||k<0||!Number.isInteger(cap)||cap<0)return {status:"INVALID",authority:"NONE"};
  let z=Scan.scan(text);if(z.status!=="CANDIDATES_ONLY")return {status:z.status,authority:"NONE"};
  let items=roles.flatMap(role=>z.ranked[role].slice(0,k).map(v=>({id:JSON.stringify([scope,role,v.start,v.end]),role,span:{start:v.start,end:v.end,text:v.text,encoding:"UTF16"},score:v.score,authority:"NONE"})));
  if(items.length>cap)return {status:"LIMIT",authority:"NONE"};
  return {status:"CANDIDATES_ONLY",scope:clone(scope),text,k,items,coverage:"UNVERIFIED",authority:"NONE",outside:true}
 }
 // Independent pre-existing annotations stay on the host side. Never derive
 // obligations from the retrieved list. Revision and action/constraint can coexist.
 function obligations(t){
  return t.items.flatMap(x=>{
   let rs=roles.includes(x.role)?[x.role]:[];
   if(x.dimensions.edit.status==="ANNOTATED"&&["replace","retract"].includes(x.dimensions.edit.value)&&!rs.includes("revision"))rs.push("revision");
   if(!rs.length)rs=[x.role];
   return rs.map(role=>({id:JSON.stringify([x.id,role]),role,span:clone(x.span),annotationId:x.id}))
  })
 }
 // Scope and manifest are supplied by a trusted test harness, not by the proposer.
 // Alignment is a diagnostic only. Even all matched does not mean semantic truth.
 function audit(bundle,text,scope,k,obs,covered,cap=10000){
  let expected=propose(text,scope,k,cap);
  if(expected.status!=="CANDIDATES_ONLY")return {status:expected.status,authority:"NONE"};
  if(!eq(bundle,expected))return {status:"INVALID_BINDING",authority:"NONE"};
  let matches=new Map(bundle.items.map(v=>[JSON.stringify([v.role,v.span.start,v.span.end]),v.id])),rows=obs.map(o=>({id:o.id,role:o.role,status:!roles.includes(o.role)?"UNSUPPORTED_ROLE":matches.has(JSON.stringify([o.role,o.span.start,o.span.end]))?"ANCHOR_MATCHED":"MISSING_CANDIDATE",candidate:matches.get(JSON.stringify([o.role,o.span.start,o.span.end]))??null}));
  return {status:!covered?"UNKNOWN_COVERAGE":rows.some(x=>x.status!=="ANCHOR_MATCHED")?"INCOMPLETE_ANCHORS":rows.length?"ANCHORS_ONLY":"EMPTY_FIXTURE_SCOPE",rows,semanticStatus:"UNVERIFIED",authority:"NONE",outside:true}
 }
 let o={datasets:0,turns:0,claims:0,obligations:0,targets:0,unsupported:0,overlapRoleSpans:0,requests:0,coverageChecks:0,mutationChecks:0,limitChecks:0,scopeChecks:0,manifestRetentionChecks:0,roleOracleChecks:0,controls:0,byK:{},examples:{}};
 for(let k of [0,1,10,50])o.byK[k]={proposals:0,matched:0,missing:0,unsupported:0,allTargetTurns:0,targetTurns:0,fullAnchorTurns:0,emptyTargetTurns:0,naiveNonemptyIncomplete:0,naiveEmptyWithObligations:0};
 for(let d=0;d<docs.length;d++){
  let m=IR.build(docs[d],assets[d]);ck(IR.verify(m,docs[d],assets[d]),"IR");o.datasets++;
  for(let ei=0;ei<m.episodes.length;ei++)for(let ti=0;ti<m.episodes[ei].turns.length;ti++){
   let t=m.episodes[ei].turns[ti],scope={asset:assets[d].sha,episode:m.episodes[ei].meta.id,turn:ti+1,revision:1},obs=obligations(t),src=docs[d].cases[ei].turns[ti],raw=d===0?src.claims:src.proposal.claims;
   o.turns++;o.claims+=t.items.length;o.obligations+=obs.length;let target=obs.filter(x=>roles.includes(x.role));o.targets+=target.length;o.unsupported+=obs.length-target.length;
   // Cross-check the original R74 target selection on original raw annotation.
   let gold=raw.flatMap((x,i)=>Scan.gold(d,x).map(role=>JSON.stringify([t.items[i].id,role]))).sort();
   ck(eq(gold,target.map(x=>x.id).sort()),"role bridge mismatch");o.roleOracleChecks+=raw.length;
   let spans=new Map();for(let x of obs){let k=JSON.stringify([x.span.start,x.span.end]);let z=spans.get(k)||new Set();z.add(x.role);spans.set(k,z)}o.overlapRoleSpans+=[...spans.values()].filter(s=>s.size>1).length;
   for(let k of [0,1,10,50]){
    let b=propose(t.text,scope,k),a=audit(b,t.text,scope,k,obs,true),z=o.byK[k];o.requests++;ck(a.authority==="NONE"&&a.semanticStatus==="UNVERIFIED"&&a.outside===true,"no authority");
    ck(eq(a.rows.map(x=>x.id),obs.map(x=>x.id)),"retention");o.manifestRetentionChecks+=obs.length;
    let targetRows=a.rows.filter(x=>roles.includes(x.role)),matched=targetRows.filter(x=>x.status==="ANCHOR_MATCHED").length;
    // Separate search-side rank membership reference.
    let s=Scan.scan(t.text);for(let x of obs){let expected=roles.includes(x.role)&&s.ranked[x.role].slice(0,k).some(y=>y.start===x.span.start&&y.end===x.span.end);ck((a.rows.find(y=>y.id===x.id).status==="ANCHOR_MATCHED")===expected,"rank membership")}
    z.proposals+=b.items.length;z.matched+=matched;z.missing+=target.length-matched;z.unsupported+=obs.length-target.length;
    if(target.length){z.targetTurns++;z.allTargetTurns+=+(matched===target.length)}else z.emptyTargetTurns++;
    z.fullAnchorTurns+=+(a.status==="ANCHORS_ONLY");
    z.naiveNonemptyIncomplete+=+(b.items.length>0&&a.rows.some(x=>x.status!=="ANCHOR_MATCHED"));
    z.naiveEmptyWithObligations+=+(b.items.length===0&&obs.length>0);
    if(b.items.length&&a.rows.some(x=>x.status!=="ANCHOR_MATCHED"))o.examples.incomplete??={scope,text:t.text,k,missing:a.rows.filter(x=>x.status!=="ANCHOR_MATCHED")};
    let no=audit(b,t.text,scope,k,obs,false);ck(no.status==="UNKNOWN_COVERAGE"&&eq(no.rows,a.rows),"coverage");o.coverageChecks++;
    // Mutation of scope, item ID, authority, coverage, omission. Each mismatch
    // is rejected against recomputed fixed candidate output, not a signature.
    for(let mutate of [x=>{x.authority="EXECUTE"},x=>{x.coverage="VERIFIED"},x=>{x.scope.revision++},...(b.items.length?[x=>{x.items.pop()},x=>{x.items[0].span.start++},x=>{x.items[0].role="goal"}]:[])]){
     let v=clone(b);mutate(v);ck(audit(v,t.text,scope,k,obs,true).status==="INVALID_BINDING","mutation");o.mutationChecks++;
    }
    ck(audit(b,t.text,{...scope,revision:2},k,obs,true).status==="INVALID_BINDING","stale");o.scopeChecks++;
    if(b.items.length){let v=propose(t.text,scope,k,b.items.length-1);ck(v.status==="LIMIT"&&!Object.hasOwn(v,"items"),"cap");o.limitChecks++}
   }
  }
 }
 for(let [n,t] of [["counts",o.turns===64&&o.claims===167&&o.targets===67],["requests",o.requests===256],["manifest",o.manifestRetentionChecks===4*o.obligations],["role",o.roleOracleChecks===167],["coverage",o.coverageChecks===256],["zero",o.byK[0].matched===0],["historical ranking",o.byK[1].matched===22&&o.byK[50].matched<=42],["monotone",o.byK[1].matched<=o.byK[10].matched&&o.byK[10].matched<=o.byK[50].matched],["unsupported retained",Object.values(o.byK).every(x=>x.unsupported===o.unsupported)],["invalid",propose("甲",{id:1},-1).status==="INVALID"],["empty outside",propose("。",{id:1},1).outside===true]]){ck(t,n);o.controls++}
 return o
}
// experiment(load(report73," const out={datasets:","build,restore,verify"),load(report74," const blank=()=>","scan,gold"),docs,assets)
```

## 实测
```json
{
  "datasets": 2,
  "turns": 64,
  "claims": 167,
  "obligations": 172,
  "targets": 67,
  "unsupported": 105,
  "overlapRoleSpans": 5,
  "requests": 256,
  "coverageChecks": 256,
  "mutationChecks": 1191,
  "limitChecks": 141,
  "scopeChecks": 256,
  "manifestRetentionChecks": 688,
  "roleOracleChecks": 167,
  "controls": 11,
  "byK": {
    "0": {
      "proposals": 0,
      "matched": 0,
      "missing": 67,
      "unsupported": 105,
      "allTargetTurns": 0,
      "targetTurns": 44,
      "fullAnchorTurns": 0,
      "emptyTargetTurns": 20,
      "naiveNonemptyIncomplete": 0,
      "naiveEmptyWithObligations": 64
    },
    "1": {
      "proposals": 66,
      "matched": 22,
      "missing": 45,
      "unsupported": 105,
      "allTargetTurns": 11,
      "targetTurns": 44,
      "fullAnchorTurns": 6,
      "emptyTargetTurns": 20,
      "naiveNonemptyIncomplete": 41,
      "naiveEmptyWithObligations": 17
    },
    "10": {
      "proposals": 606,
      "matched": 37,
      "missing": 30,
      "unsupported": 105,
      "allTargetTurns": 21,
      "targetTurns": 44,
      "fullAnchorTurns": 6,
      "emptyTargetTurns": 20,
      "naiveNonemptyIncomplete": 41,
      "naiveEmptyWithObligations": 17
    },
    "50": {
      "proposals": 1523,
      "matched": 42,
      "missing": 25,
      "unsupported": 105,
      "allTargetTurns": 26,
      "targetTurns": 44,
      "fullAnchorTurns": 7,
      "emptyTargetTurns": 20,
      "naiveNonemptyIncomplete": 40,
      "naiveEmptyWithObligations": 17
    }
  },
  "examples": {
    "incomplete": {
      "scope": {
        "asset": "be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb",
        "episode": "L01",
        "turn": 1,
        "revision": 1
      },
      "text": "我和室友合租，房租加停车每月最多四千，水电另算。房租三千六，车位得问房东。",
      "k": 1,
      "missing": [
        {
          "id": "[\"L01.1.2\",\"scope_modifier\"]",
          "role": "scope_modifier",
          "status": "UNSUPPORTED_ROLE",
          "candidate": null
        },
        {
          "id": "[\"L01.1.3\",\"report\"]",
          "role": "report",
          "status": "UNSUPPORTED_ROLE",
          "candidate": null
        },
        {
          "id": "[\"L01.1.4\",\"unknown\"]",
          "role": "unknown",
          "status": "UNSUPPORTED_ROLE",
          "candidate": null
        }
      ]
    }
  }
}
```

## 后续
集中解决非三类语义、词面检索的漏召回、跨轮身份及独立真实数据准入。共同接口可继续接已有数量/引用/知识候选，但不能把多候选并集视作真实覆盖。完整自主语义能力、训练授权、独立样本及真实原生入口仍为主要阻塞。数据轨/产品轨/独立验收轨责任不变，正式工程另获授权。
