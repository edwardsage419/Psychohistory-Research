# 自主认知专项累计第103轮候选：角色候选与跨轮引用的统一跨度图

2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_INTEGRATION_EXECUTED / PUBLIC_SYNTHETIC_DEVELOPMENT / NATIVE_NOT_RUN / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线main 3a1e3221ad223f18240342e1bddb471ca5d583f0。核对近20提交、13开放PR（#61待审）、v3.2首18行及此前全文、唯一交接首18行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R102/R77/精确Top-K/R80前18行及固定R102/Top-K代码。复用R73、R74、R102、精确Top-K四项实际研究源码；本轮新增统一跨度节点、跨轮边及独立引用义务保留、角色前置过滤的损失诊断。未重新证明Top-K剪枝或训练排序，不运行R80不同评分、原生应用或长期规划。

## 固定资产
research/decision_hub/2026-11-25-unified-semantic-annotation-bridge.md af648d16ee96b9af4a3efb61b413d113208bb0ca
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-25-unified-candidate-obligation-interface.md bdf9bc7a42f33d9c48708970d6ac03a78ef276de
research/decision_hub/2026-11-25-certified-top-k-reference-search.md a14c24b7ab28971668469a32a86bd0b4cb88a63a
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
实际获取全文并核对连接器blob。前四为项目自有研究源码，仅加载已核验的固定代码；生产禁止执行任意外部文本。32情节64轮，167原标注，172角色义务；57第二轮标注节点中12个有明确唯一候选引用、45未标注引用。ChatGPT研发辅助原创合成公开开发资料，非真人、独立留出或训练许可。候选路径只输入文本和范围；原标注及链接仅供另一条诊断路径，不给候选生成器。复用原权重及原始UTF16跨度模式（不含跨标点桥接）；本轮未重新运行穷举参照，仅核验历史Top-K已标匹配计数。

## 合同
节点身份为固定语料blob/情节/轮/修订/原文UTF16起止，不含角色：同一原文跨度的多个角色作为独立候选标签，引用边可连接没有角色标签的跨度。这里共享的是原文位置，不是现实对象、概念同一性、实际事件身份或用户确认；同一跨度可能表达多个义务，原义务及引用记录独立保留。边为第二轮到第一轮的候选，分数沿既有固定算法。exact top K仅指该算法排序，不是语义完整性或概率。全局候选之外始终保留outside=true；NO_ANNOTATED_LINK转换为UNANNOTATED_REFERENCE，不是NO_LINK或负例。明确引用的跨度对命中仅为锚点定位，不赋予实际修改权限。角色标签存在也不是语义真值。完整语义仍UNVERIFIED，所有authority NONE。真实多轮、概念归属、条件范围、知识资格、确认与数学入口未实现。

每角色预算10/50、每情节引用预算20/100，研究者选定。比较在同一原始Top-K结果上事后要求两端各有任一角色标签的过滤对照；不等同于重新在角色候选图内排序的Top-K，后者本轮未执行。两侧角色过滤可能删掉实际有引用的跨度，因为部分角色根本不支持或未命中；不以增加候选数量为真实理解进步。候选束按固定文本及范围重算、结构比较，删边、篡改节点、方向、作用域或权限拒绝；不是真实签名、授权、并发或生产安全。独立覆盖由人工夹具提供，缺覆盖仍保留诊断及义务；边搜索超限整体不返回图。本预算仅沿Top-K访问计数，角色搜索、构图、重复校验、实际时间内存未受同一总预算控制。

## 实验
32情节×4预算组合=128请求。角色义务、引用义务全量保留，节点文本与方向及唯一位置身份核验；历史已标引用匹配数不变。按每模式记录角色节点、无角色节点、边数、角色过滤后仍保留的已标引用。无负例或独立标注覆盖，禁止计算真实precision/accuracy或将未标引用判为不存在。128覆盖/范围/预算检查、768结构篡改检查、11控制。参照同研究者/同源开发样例；无实际授权、训练、外部数据、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。保留既有正式版本范围和验收门。

## 复算
按固定资产顺序读取报告文本及JSON。仅加载可信固定自有代码。
```js
function load(text,marker,names,args=[],params=[]){
 let src=text.split("```js\n")[1].split("\n```")[0].split(marker)[0];
 return Function(...params,src+"\nreturn {"+names+"};\n}\nreturn experiment("+params.join(",")+");")(...args)
}
function experiment(IR,U,R,docs,assets){
 const ck=(v,m)=>{if(!v)throw Error(m)},canon=x=>x===null||typeof x!=="object"?JSON.stringify(x):Array.isArray(x)?"["+x.map(canon).join(",")+"]":"{"+Object.keys(x).sort().map(k=>JSON.stringify(k)+":"+canon(x[k])).join(",")+"}",eq=(a,b)=>canon(a)===canon(b),clone=x=>JSON.parse(JSON.stringify(x));
 const nodeId=(s,a,b)=>JSON.stringify([s.asset,s.episode,s.turn,s.revision,a,b]);
 function build(texts,scopes,rk,ek,cap=200000){
  const no=status=>({status,authority:"NONE",outside:true});
  if(!Number.isInteger(ek)||ek<1||!Number.isInteger(cap)||cap<0)return no("INVALID");
  if(scopes[0].asset!==scopes[1].asset||scopes[0].episode!==scopes[1].episode||scopes[0].turn!==1||scopes[1].turn!==2)return no("INVALID_SCOPE");
  let roles=texts.map((t,i)=>U.propose(t,scopes[i],rk));
  if(roles.some(x=>x.status!=="CANDIDATES_ONLY"))return no("UNKNOWN_ROLE_SEARCH");
  let z=R.optimized(R.spans(texts[0],false),R.spans(texts[1],false),ek,cap);
  if(z.status!=="EXACT_TOP_K")return no(z.status);
  let nodes=new Map(),edges=[],roleSets=[new Set(),new Set()];
  function add(i,a,b){
   let id=nodeId(scopes[i],a,b);
   if(!nodes.has(id))nodes.set(id,{id,scope:clone(scopes[i]),span:{start:a,end:b,text:texts[i].slice(a,b),encoding:"UTF16"},roles:[],authority:"NONE"});
   return nodes.get(id)
  }
  for(let i=0;i<2;i++)for(let v of roles[i].items){let n=add(i,v.span.start,v.span.end);n.roles.push({id:v.id,role:v.role,score:v.score});roleSets[i].add(n.id)}
  for(let e of z.top){let a=add(0,e.a.start,e.a.end),b=add(1,e.b.start,e.b.end);edges.push({id:JSON.stringify([b.id,a.id]),from:b.id,to:a.id,score:e.score,authority:"NONE"})}
  return {status:"CANDIDATES_ONLY",authority:"NONE",outside:true,coverage:"UNVERIFIED",scopes:clone(scopes),rk,ek,nodes:[...nodes.values()],edges,roleBundles:roles,roleEndpoints:roleSets.map(s=>[...s]),visits:z.visits,scored:z.scored}
 }
 function audit(bundle,texts,scopes,rk,ek,turns,covered=true,cap=200000){
  let expected=build(texts,scopes,rk,ek,cap);
  if(expected.status!=="CANDIDATES_ONLY")return {status:expected.status,authority:"NONE"};
  if(!eq(bundle,expected))return {status:"INVALID_BINDING",authority:"NONE"};
  let rows=turns.map((t,i)=>U.audit(bundle.roleBundles[i],texts[i],scopes[i],rk,U.obligations(t),covered).rows);
  let byId=new Map(turns[0].items.map(x=>[x.id,x])),edgeSet=new Set(bundle.edges.map(x=>x.id)),roleSets=bundle.roleEndpoints.map(x=>new Set(x));
  let refs=turns[1].items.map(x=>{
   if(x.reference.status!=="UNIQUE_CANDIDATE")return {id:x.id,status:x.reference.status==="NO_ANNOTATED_LINK"?"UNANNOTATED_REFERENCE":"UNRESOLVED_ANNOTATION",outside:true,authority:"NONE"};
   let p=byId.get(x.reference.candidates[0]);ck(p,"prior reference");
   let a=nodeId(scopes[0],p.span.start,p.span.end),b=nodeId(scopes[1],x.span.start,x.span.end),hit=edgeSet.has(JSON.stringify([b,a]));
   return {id:x.id,status:hit?"EDGE_ANCHOR_MATCHED":"MISSING_EDGE",bothRoleAnchors:roleSets[0].has(a)&&roleSets[1].has(b),outside:true,authority:"NONE"}
  });
  return {status:covered?"ANCHOR_DIAGNOSTIC":"UNKNOWN_COVERAGE",authority:"NONE",semanticStatus:"UNVERIFIED",outside:true,rows,refs}
 }
 let o={datasets:0,episodes:0,requests:0,positiveRefs:0,unannotatedRefs:0,roleObligations:0,retentionChecks:0,referenceRetentionChecks:0,coverageChecks:0,scopeChecks:0,mutationChecks:0,budgetChecks:0,controls:0,byMode:{}};
 for(let rk of [10,50])for(let ek of [20,100])o.byMode[rk+"_"+ek]={nodes:0,edges:0,roleEndpointNodes:0,rolelessNodes:0,edgesBothRoleAnchors:0,positive:0,matched:0,matchedWithBothRoleAnchors:0,missed:0,unannotated:0,visits:0,scored:0};
 for(let d=0;d<docs.length;d++){
  let m=IR.build(docs[d],assets[d]);ck(IR.verify(m,docs[d],assets[d]),"IR");o.datasets++;
  for(let e of m.episodes){
   let turns=e.turns,texts=turns.map(t=>t.text),scopes=turns.map((_,i)=>({asset:assets[d].sha,episode:e.meta.id,turn:i+1,revision:1}));o.episodes++;
   let positive=turns[1].items.filter(x=>x.reference.status==="UNIQUE_CANDIDATE").length,unannotated=turns[1].items.filter(x=>x.reference.status==="NO_ANNOTATED_LINK").length,obs=turns.flatMap(U.obligations);
   o.positiveRefs+=positive;o.unannotatedRefs+=unannotated;o.roleObligations+=obs.length;
   for(let rk of [10,50])for(let ek of [20,100]){
    let b=build(texts,scopes,rk,ek),a=audit(b,texts,scopes,rk,ek,turns),z=o.byMode[rk+"_"+ek];o.requests++;
    ck(b.status==="CANDIDATES_ONLY"&&a.status==="ANCHOR_DIAGNOSTIC"&&a.authority==="NONE"&&a.semanticStatus==="UNVERIFIED","status");
    ck(eq(a.rows.flat().map(x=>x.id),obs.map(x=>x.id)),"retain role");o.retentionChecks+=obs.length;
    ck(eq(a.refs.map(x=>x.id),turns[1].items.map(x=>x.id))&&a.refs.every(x=>x.outside&&x.authority==="NONE"),"retain refs");o.referenceRetentionChecks+=a.refs.length;
    let nodes=new Map(b.nodes.map(n=>[n.id,n]));ck(nodes.size===b.nodes.length&&b.edges.every(x=>nodes.has(x.from)&&nodes.has(x.to)&&nodes.get(x.from).scope.turn===2&&nodes.get(x.to).scope.turn===1),"graph identity");
    ck(b.nodes.every(n=>n.span.text===texts[n.scope.turn-1].slice(n.span.start,n.span.end)&&n.authority==="NONE"),"text");
    z.nodes+=b.nodes.length;z.edges+=b.edges.length;z.roleEndpointNodes+=b.nodes.filter(n=>n.roles.length).length;z.rolelessNodes+=b.nodes.filter(n=>!n.roles.length).length;
    z.edgesBothRoleAnchors+=b.edges.filter(x=>nodes.get(x.from).roles.length&&nodes.get(x.to).roles.length).length;
    z.positive+=positive;z.matched+=a.refs.filter(x=>x.status==="EDGE_ANCHOR_MATCHED").length;z.matchedWithBothRoleAnchors+=a.refs.filter(x=>x.status==="EDGE_ANCHOR_MATCHED"&&x.bothRoleAnchors).length;z.missed+=a.refs.filter(x=>x.status==="MISSING_EDGE").length;z.unannotated+=a.refs.filter(x=>x.status==="UNANNOTATED_REFERENCE").length;z.visits+=b.visits;z.scored+=b.scored;
    let c=audit(b,texts,scopes,rk,ek,turns,false);ck(c.status==="UNKNOWN_COVERAGE"&&eq(c.refs,a.refs)&&eq(c.rows,a.rows),"coverage");o.coverageChecks++;
    let altered=[scopes[0],{...scopes[1],revision:2}];ck(audit(b,texts,altered,rk,ek,turns).status==="INVALID_BINDING","scope");o.scopeChecks++;
    for(let mutate of [v=>{v.coverage="VERIFIED"},v=>{v.authority="EXECUTE"},v=>{v.edges.pop()},v=>{v.edges[0].to=v.edges[0].from},v=>{v.nodes[0].span.text+="伪"},v=>{v.scopes[0].episode="other"}]){
     let c=clone(b);mutate(c);ck(audit(c,texts,scopes,rk,ek,turns).status==="INVALID_BINDING","tamper");o.mutationChecks++
    }
    let lim=build(texts,scopes,rk,ek,b.visits-1);ck(lim.status==="LIMIT"&&!Object.hasOwn(lim,"edges")&&!Object.hasOwn(lim,"nodes"),"budget");o.budgetChecks++;
   }
  }
 }
 for(let [n,t] of [["counts",o.episodes===32&&o.positiveRefs===12&&o.unannotatedRefs===45],["obligations",o.roleObligations===172],["requests",o.requests===128],["retention",o.retentionChecks===688&&o.referenceRetentionChecks===228],["rank",Object.entries(o.byMode).every(([k,v])=>v.matched===(k.endsWith("_20")?6:10))],["not negative",Object.values(o.byMode).every(v=>v.unannotated===45&&v.matched+v.missed===12)],["node count",Object.values(o.byMode).every(v=>v.roleEndpointNodes+v.rolelessNodes===v.nodes)],["filter",Object.values(o.byMode).every(v=>v.matchedWithBothRoleAnchors<=v.matched)],["scope",o.scopeChecks===128&&o.coverageChecks===128],["budget",o.budgetChecks===128],["mutation",o.mutationChecks===768]]){ck(t,n);o.controls++}
 return o
}
// IR=load(report73," const out={datasets:","build,verify")
// Scan=load(report74," const blank=()=>","scan")
// U=load(report102," let o={datasets:","propose,obligations,audit",[null,Scan],["IR","Scan"])
// R=load(reportTopK," let result={episodes:","spans,optimized")
// experiment(IR,U,R,docs,assets)
```

## 实测
```json
{
  "datasets": 2,
  "episodes": 32,
  "requests": 128,
  "positiveRefs": 12,
  "unannotatedRefs": 45,
  "roleObligations": 172,
  "retentionChecks": 688,
  "referenceRetentionChecks": 228,
  "coverageChecks": 128,
  "scopeChecks": 128,
  "mutationChecks": 768,
  "budgetChecks": 128,
  "controls": 11,
  "byMode": {
    "10_20": {
      "nodes": 856,
      "edges": 640,
      "roleEndpointNodes": 562,
      "rolelessNodes": 294,
      "edgesBothRoleAnchors": 116,
      "positive": 12,
      "matched": 6,
      "matchedWithBothRoleAnchors": 4,
      "missed": 6,
      "unannotated": 45,
      "visits": 26602,
      "scored": 8406
    },
    "10_100": {
      "nodes": 1869,
      "edges": 3200,
      "roleEndpointNodes": 562,
      "rolelessNodes": 1307,
      "edgesBothRoleAnchors": 448,
      "positive": 12,
      "matched": 10,
      "matchedWithBothRoleAnchors": 5,
      "missed": 2,
      "unannotated": 45,
      "visits": 64220,
      "scored": 24576
    },
    "50_20": {
      "nodes": 1706,
      "edges": 640,
      "roleEndpointNodes": 1427,
      "rolelessNodes": 279,
      "edgesBothRoleAnchors": 131,
      "positive": 12,
      "matched": 6,
      "matchedWithBothRoleAnchors": 4,
      "missed": 6,
      "unannotated": 45,
      "visits": 26602,
      "scored": 8406
    },
    "50_100": {
      "nodes": 2637,
      "edges": 3200,
      "roleEndpointNodes": 1427,
      "rolelessNodes": 1210,
      "edgesBothRoleAnchors": 548,
      "positive": 12,
      "matched": 10,
      "matchedWithBothRoleAnchors": 5,
      "missed": 2,
      "unannotated": 45,
      "visits": 64220,
      "scored": 24576
    }
  }
}
```

## 后续
优先统一数量和概念候选及证据来源接口；减少继续扩大同一合成集数学试验，合法语料、实际自主学习与独立泛化仍为主阻塞。正式训练及工程版本另获授权。数据、独立验收、产品轨职责不变。
