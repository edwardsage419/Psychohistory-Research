# 自主认知专项累计第104轮候选：数量原子、组合逻辑与统一跨度图

2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_INTEGRATION_EXECUTED / PUBLIC_SYNTHETIC_DEVELOPMENT / NATIVE_NOT_RUN / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线main f8326373525aa598b5a78920947536cfc70b0d1b。核对近20提交、13开放PR（#61待审）、v3.2首18行及此前全文、唯一交接首18行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R103/R62/R63/R82首18行、R62/R63完整源码。实际复用R73/R74/R102/Top-K/R103/R62/R63七份固定研究代码，增加独立数量分支、类型原子序列化及逻辑树跨度连接。R82概念来源体系尚未接入；不执行原生C028、长期规划或生产应用。

## 固定资产
research/decision_hub/2026-11-25-unified-semantic-annotation-bridge.md af648d16ee96b9af4a3efb61b413d113208bb0ca
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-25-unified-candidate-obligation-interface.md bdf9bc7a42f33d9c48708970d6ac03a78ef276de
research/decision_hub/2026-11-25-certified-top-k-reference-search.md a14c24b7ab28971668469a32a86bd0b4cb88a63a
research/decision_hub/2026-11-25-unified-reference-candidate-interface.md 5b55d2104f74246d3e6d5accc31da1140c22bedd
research/decision_hub/2026-11-25-typed-quantity-compositional-atoms.md ada3d84a46e4d9a411ebf762884d13a5c5e87686
research/decision_hub/2026-11-25-joint-quantity-semantic-inference.md 296465980e23a1d8082f81a8181343668965328b
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
全文实际获取并核对连接器blob；只加载已核验的项目自有研究代码，生产不得执行外部文档。两套公开原创ChatGPT研发辅助合成开发语料非真人、独立留出或训练许可。另设72个双轮数量夹具及12个组合逻辑夹具，均人工已知语法、非开放语言。

## 接口及限制
R103保留原角色及引用图。新增数量分支直接从原文显式周期起点枚举所有尾端，使用原R62完整子串parse，不能受角色或引用候选过滤；候选子串可截断真实语义后缀，不能视为完整义务或可执行值。原图同一范围UTF16跨度共享节点，不将相同数值、单位、指标或文本视为同一实体/资源。类型化候选保留原始文本、周期、指标、单位、比较及精确BigInt分子分母（研究序列化十进制字符串）；转换后仅为传输候选，未实现生产schema。R63仅对整轮原文执行完整逻辑解析，原子连接相同跨度节点，多树保留；复算时使用原始解析对象而非反序列化图执行。全部authority NONE，outside true，coverage UNVERIFIED。所有未支持类型、比例、中文数词、隐含单位、真实主体、时限、条件、原文完整性均待研究。当前语料的value/lower/upper/unit标注仅作为字段存在诊断，不保证每项可直接解析为单个量；精确锚点为整个标注跨度匹配，不表示数学语义召回。候选生成不读取标注。实际合成比较使用独立人工变量身份与资格，R62仍要求指标、周期、币种一致并区分界限和点值。逻辑实验调用原R63 solve，矩形域及绑定皆人工指定；实际跨主体或共享资源身份未识别。没有由图候选直接进入实际数学权限。预算限制新增数量子串parse调用，原角色搜索、边搜索、树解析、数据传输和真实时间内存不在共同预算内。超量时不返回合并图；非生产保护。

## 实验
32情节64轮167标注的现有语料实测数量分支127次parse尝试，零候选。保留此负面结果；不能把接口整合当作语言能力进步。记录原图节点/边保留情况及有数量字段的标注条数。72对人工有限语法以4种指标/币种/周期配对、3个阈值、3个点值、2种比较构成，实际接图并用原R62 compare；直接人工整数参照，同研究者非独立验收。12个组合逻辑夹具与独立半秒网格直接布尔参照，测试同一量或不同量、严格互补及边界；不重复R63完整矩形试验。所有参数、句式、绑定、预算由研究者选择。12控制，72数量预算及12逻辑预算检查。未测真实比例解析、概念来源、完整原文义务或实际设备性能。无新外部数据、训练、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。保留正式版本范围和验收门。

## 复算
按固定资产顺序获取全文，使用以下函数（仅固定可信研究代码）。
```js
function load(text,marker,names,args=[],params=[],entry="experiment"){
 let src=text.split("```js\n")[1].split("\n```")[0].split(marker)[0];
 return Function(...params,src+"\nreturn {"+names+"};\n}\nreturn "+entry+"("+params.join(",")+");")(...args)
}
function experiment(IR,G,Q,J,docs,assets){
 const ck=(v,m)=>{if(!v)throw Error(m)},clone=x=>JSON.parse(JSON.stringify(x)),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 function serialize(p){return JSON.parse(JSON.stringify(p,(_,x)=>typeof x==="bigint"?x.toString():x))}
 // Independent branch; does not require role or reference span retrieval.
 function quantities(text,cap=10000){
  if(typeof text!=="string"||text.length>128)return {status:"LIMIT",items:[]};
  let items=[],attempts=0;
  for(let i=0;i<text.length;i++)if(Object.keys(Q.periods).some(p=>text.startsWith(p,i)))for(let j=i+1;j<=text.length;j++){
   if(attempts>=cap)return {status:"LIMIT",items:[],attempts};attempts++;
   let p=Q.parse(text.slice(i,j));if(p.status==="CANDIDATE")items.push({start:i,end:j,atom:p})
  }
  return {status:"CANDIDATES_ONLY",items,attempts}
 }
 function merge(texts,scopes,qcap=10000){
  let b=G.build(texts,scopes,10,20);if(b.status!=="CANDIDATES_ONLY")return {status:b.status,authority:"NONE"};
  let nodes=new Map(b.nodes.map(n=>[n.id,{...n,quantities:[]} ])),logic=[],counts={attempts:0,quantities:0,newNodes:0,logicAtoms:0,trees:0};
  function add(i,a,c){
   let id=G.nodeId(scopes[i],a,c);
   if(!nodes.has(id)){counts.newNodes++;nodes.set(id,{id,scope:clone(scopes[i]),span:{start:a,end:c,text:texts[i].slice(a,c),encoding:"UTF16"},roles:[],quantities:[],authority:"NONE"})}
   return nodes.get(id)
  }
  for(let i=0;i<2;i++){
   let z=quantities(texts[i],qcap-counts.attempts);if(z.status==="LIMIT")return {status:"LIMIT",authority:"NONE"};counts.attempts+=z.attempts;
   for(let x of z.items){let n=add(i,x.start,x.end);n.quantities.push({source:"typed-atom-0.2",atom:serialize(x.atom),authority:"NONE"});counts.quantities++}
   let p=J.parse(texts[i]);
   if(p.status==="CANDIDATE"){
    let ids=p.atoms.map(x=>add(i,x.start,x.end).id);counts.logicAtoms+=ids.length;counts.trees+=p.trees.length;
    logic.push({turn:i+1,status:"CANDIDATES_ONLY",atoms:p.atoms.map((x,k)=>({node:ids[k],atom:serialize(x)})),trees:p.trees,authority:"NONE",outside:true})
   }else logic.push({turn:i+1,status:p.status,authority:"NONE",outside:true});
  }
  return {status:"CANDIDATES_ONLY",authority:"NONE",outside:true,coverage:"UNVERIFIED",graph:b,nodes:[...nodes.values()],logic,counts}
 }
 // Exact compare only after independently supplied variable identity and qualification.
 function compare(c,m,binding){
  if(!binding.qualified||binding.boundId!==binding.pointId)return "UNKNOWN";
  return Q.compare(Q.parse(c),Q.parse(m),true)
 }
 let o={datasets:0,episodes:0,turns:0,claims:0,annotatedQuantityFields:0,annotatedQuantityClaims:0,corpusAttempts:0,corpusQuantityCandidates:0,corpusLogicCandidates:0,corpusExactQuantityAnchors:0,corpusMissingQuantityAnchors:0,corpusRetainedNodes:0,corpusRetainedEdges:0,corpusGraphChecks:0,fixturePairs:0,fixtureQuantityCandidates:0,fixtureNewNodes:0,fixtureLogicAtoms:0,fixtureTrees:0,fixtureComparisons:0,fixtureUnknownIdentity:0,fixtureUnknownType:0,fixturePass:0,fixtureFail:0,logicChecks:0,logicUnknownIdentity:0,logicLimitChecks:0,quantityLimitChecks:0,controls:0,witnesses:{}};
 for(let d=0;d<docs.length;d++){
  let m=IR.build(docs[d],assets[d]);ck(IR.verify(m,docs[d],assets[d]),"IR");o.datasets++;
  for(let e of m.episodes){let texts=e.turns.map(t=>t.text),scopes=e.turns.map((_,i)=>({asset:assets[d].sha,episode:e.meta.id,turn:i+1,revision:1})),z=merge(texts,scopes);ck(z.status==="CANDIDATES_ONLY","corpus merge");o.episodes++;o.turns+=2;o.corpusAttempts+=z.counts.attempts;o.corpusQuantityCandidates+=z.counts.quantities;o.corpusLogicCandidates+=z.logic.filter(x=>x.status==="CANDIDATES_ONLY").length;
   let byId=new Map(z.nodes.map(n=>[n.id,n]));ck(z.graph.nodes.every(n=>byId.has(n.id)&&eq(byId.get(n.id).roles,n.roles))&&z.graph.edges.every(e=>byId.has(e.from)&&byId.has(e.to)),"graph preserve");o.corpusRetainedNodes+=z.graph.nodes.length;o.corpusRetainedEdges+=z.graph.edges.length;o.corpusGraphChecks++;
   for(let i=0;i<2;i++)for(let x of e.turns[i].items){o.claims++;let fields=["value","lower","upper","unit"].filter(k=>x.dimensions[k].status==="ANNOTATED");o.annotatedQuantityFields+=fields.length;if(!fields.length)continue;o.annotatedQuantityClaims++;let n=byId.get(G.nodeId(scopes[i],x.span.start,x.span.end));if(n?.quantities.length)o.corpusExactQuantityAnchors++;else{o.corpusMissingQuantityAnchors++;o.witnesses.missing??={episode:e.meta.id,quote:x.span.text,fields}}}
  }
 }
 let forms=[
 {bound:"每周工时",point:"每周工时",bu:"小时",pu:"分钟",factorB:60,factorP:1,compatible:true},
 {bound:"总预算",point:"总预算",bu:"美元",pu:"USD",factorB:1,factorP:1,compatible:true},
 {bound:"总预算",point:"总预算",bu:"美元",pu:"人民币",factorB:1,factorP:1,compatible:false},
 {bound:"每周工时",point:"每天工时",bu:"小时",pu:"小时",factorB:1,factorP:1,compatible:false}
 ];
 for(let [fi,f] of forms.entries())for(let x of [0,1,2])for(let y of [0,1,60])for(let op of ["最多","少于"]){
  let c=f.bound+op+x+f.bu,m=f.point+"为"+y+f.pu,texts=[m,c],scopes=texts.map((_,i)=>({asset:"synthetic",episode:"fixture"+o.fixturePairs,turn:i+1,revision:1})),z=merge(texts,scopes);
  ck(z.status==="CANDIDATES_ONLY"&&z.counts.quantities>=2,"fixture merge");o.fixturePairs++;o.fixtureQuantityCandidates+=z.counts.quantities;o.fixtureNewNodes+=z.counts.newNodes;o.fixtureLogicAtoms+=z.counts.logicAtoms;o.fixtureTrees+=z.counts.trees;
  for(let i=0;i<2;i++){let n=z.nodes.find(n=>n.id===G.nodeId(scopes[i],0,texts[i].length));ck(n?.quantities.some(q=>q.atom.source===texts[i]),"full atom node")}
  let expected=!f.compatible?"UNKNOWN":(op==="最多"?y*f.factorP<=x*f.factorB:y*f.factorP<x*f.factorB)?"PASS":"FAIL";
  ck(compare(c,m,{qualified:true,boundId:"X",pointId:"X"})===expected,"comparison");o.fixtureComparisons++;o[expected==="UNKNOWN"?"fixtureUnknownType":expected==="PASS"?"fixturePass":"fixtureFail"]++;
  ck(compare(c,m,{qualified:true,boundId:"X",pointId:"Y"})==="UNKNOWN"&&compare(c,m,{qualified:false,boundId:"X",pointId:"X"})==="UNKNOWN","identity");o.fixtureUnknownIdentity+=2;
  let lim=merge(texts,scopes,0);ck(lim.status==="LIMIT"&&!Object.hasOwn(lim,"nodes"),"quantity cap");o.quantityLimitChecks++;
 }
 for(let x of [0,1,2])for(let op of ["且","或者"])for(let same of [false,true]){
  let text=`每周工时少于${x}秒${op}每周工时至少${x}秒`,texts=["每周工时为1秒",text],scopes=texts.map((_,i)=>({asset:"synthetic",episode:"logic"+o.logicChecks,turn:i+1,revision:1})),z=merge(texts,scopes),p=J.parse(text),q=J.q,domains={X:{metric:"工时",period:"week",unit:"s",lo:q(0n),hi:q(2n)},Y:{metric:"工时",period:"week",unit:"s",lo:q(0n),hi:q(2n)}};
  ck(z.logic[1].atoms.length===2&&z.logic[1].trees.length===1&&z.logic[1].atoms.every(a=>z.nodes.some(n=>n.id===a.node)),"logic graph");
  let vals=[];for(let a=0;a<=4;a++)for(let b=0;b<=4;b++){let l=a<2*x,h=(same?a:b)>=2*x;vals.push(op==="且"?l&&h:l||h)}
  let expected=vals.every(Boolean)?"PASS":vals.every(v=>!v)?"FAIL":"UNKNOWN";
  ck(J.solve(p,["X",same?"X":"Y"],domains,true).status===expected,"logic");o.logicChecks++;
  ck(J.solve(p,["X","X"],domains,false).status==="UNKNOWN","logic qualification");o.logicUnknownIdentity++;
  ck(J.solve(p,["X",same?"X":"Y"],domains,true,0).status==="LIMIT","logic cap");o.logicLimitChecks++;
 }
 for(let t of [()=>o.episodes===32&&o.turns===64&&o.claims===167,()=>o.corpusAttempts===127&&o.corpusQuantityCandidates===0,()=>o.corpusMissingQuantityAnchors===o.annotatedQuantityClaims,()=>o.fixturePairs===72,()=>o.fixtureComparisons===72,()=>o.fixturePass+o.fixtureFail+o.fixtureUnknownType===72,()=>o.fixtureUnknownIdentity===144,()=>o.logicChecks===12,()=>o.logicLimitChecks===12,()=>Q.parse("总预算最多3万元").status==="AMBIGUOUS_CURRENCY",()=>Q.parse("每周工时最多3美元").status==="TYPE_MISMATCH",()=>Q.parse("总预算最多3%").status==="UNKNOWN_UNIT"]){ck(t(),"control");o.controls++}
 return o
}
// IR=load(report73," const out={datasets:","build,verify")
// Scan=load(report74," const blank=()=>","scan")
// U=load(report102," let o={datasets:","propose,obligations,audit",[null,Scan],["IR","Scan"])
// R=load(reportTopK," let result={episodes:","spans,optimized")
// G=load(report103," let o={datasets:","build,audit,nodeId",[IR,U,R],["IR","U","R"])
// Q=load(report62," const groups=","parse,compare,periods",[],[],"probe")
// J=load(report63," // Conservative Boolean baseline","parse,solve,q",[],[],"probe")
// experiment(IR,G,Q,J,docs,assets)
```

## 实测
```json
{
  "datasets": 2,
  "episodes": 32,
  "turns": 64,
  "claims": 167,
  "annotatedQuantityFields": 63,
  "annotatedQuantityClaims": 40,
  "corpusAttempts": 127,
  "corpusQuantityCandidates": 0,
  "corpusLogicCandidates": 0,
  "corpusExactQuantityAnchors": 0,
  "corpusMissingQuantityAnchors": 40,
  "corpusRetainedNodes": 856,
  "corpusRetainedEdges": 640,
  "corpusGraphChecks": 32,
  "fixturePairs": 72,
  "fixtureQuantityCandidates": 144,
  "fixtureNewNodes": 0,
  "fixtureLogicAtoms": 72,
  "fixtureTrees": 72,
  "fixtureComparisons": 72,
  "fixtureUnknownIdentity": 144,
  "fixtureUnknownType": 36,
  "fixturePass": 20,
  "fixtureFail": 16,
  "logicChecks": 12,
  "logicUnknownIdentity": 12,
  "logicLimitChecks": 12,
  "quantityLimitChecks": 72,
  "controls": 12,
  "witnesses": {
    "missing": {
      "episode": "L01",
      "quote": "房租加停车每月最多四千",
      "fields": [
        "value",
        "unit"
      ]
    }
  }
}
```

## 后续
应优先推动合法语言语料、真正可学习的组合语义和独立评价准备；现有有限数量解析仅为结构化降级及精确计算部件，不继续用扩展规则宣称开放理解。概念和知识证据接口仍需实际连接，正式训练及工程另获授权。
