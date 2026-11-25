# 自主认知专项累计第131轮候选：条件与极性作用域原文连接审计
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / PUBLIC_SYNTHETIC_DEVELOPMENT / RAW_ATTACHMENT_CANDIDATES / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 6e44ecf50e9e8de0d8a3eb76766cd0d3bf44ab9c。核对近期12提交、13开放PR（#61待审）、v3.2全文、唯一交接前18行、v0.7任务包前17行、R130前18行、R61前13行、R83前16行、R84前15行。R61已有固定布尔表达式多树，R83为已知跨度角色检索，R84为人工候选联合因子，R130为人工角色及条件确认后数学推理。本轮仅原文条件边和极性/编辑锚点作用域候选生成、在既有标注上测覆盖及排名；不做训练、通用角色分类、继续扩大业务词表或改动Codex任务。
## 固定资产
research/decision_hub/2026-11-25-unified-semantic-annotation-bridge.md af648d16ee96b9af4a3efb61b413d113208bb0ca
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
R130 aa30d5d4cd66d4bc2bc736372b9c0485b63f1362；R61 17b6035732e43c56edc44cb5db07b8d49aadfd5b；R83 e3b3e5bbfa240d926af410552f04b6ef6512f113；R84 fdaab2691c5b86a383f4daf5b7875d4279e67920；v0.7任务包 cae356da125f808c9a7feebe3940cc71e2347927。原语料为ChatGPT研发辅助项目原创公开合成开发材料，非真人、独立留出或授权训练。
## 方法与边界
实际R74全跨度扫描（同标点子句、最长24 UTF16）与R73 IR。有限17词提示表按预定次序最长优先的有限匹配（并非一般分词），条件前置/后接、极性、编辑锚分离。条件跨度起点为前置词起点或后接词终点，目标跨度在同句内允许前向、后向或内嵌（目标始于守卫之前且包含守卫），禁止跨句强标点；仅采用原文字面，不预设领域指标、动作、实体。极性/编辑候选包含锚点，保留全部合法跨度；极性提示可能表达比较、引用、否定、其他词内成分，编辑提示可能是条件取消，不直接判为逻辑否定或真实撤回。分数为固定边界、距离及长度启发式，非概率，不能确证句法、逻辑、角色、语用或权限。条件范围、真实动作与事件、否定目标、隐含条件、跨句、多层结构、引述、反问、例外、身份、来源及完整义务未解析。没有提示或无候选仍outside true及authority NONE，不能证明无条件/否定/义务。超过50000边整体LIMIT；R74枚举、内部循环不受累计预算，非实际资源防护。所有候选不允许直接计算、执行或修改。
## 评估
沿用原64轮167标注，图生成不读取标注；S中4项有独立原文condition字符串的精确条件与目标跨度作边评估，比较相邻完整子句基线（故意狭窄，仅条件子句紧邻完整目标子句）；L的条件标签及编码没有同等字面锚，不补造精确边标注，逐项记录其7个相关角色及锚出现。S中negated 7项检查精确作用域候选是否存在及排名，分别记录极性和编辑锚；这只是既有标注的跨度覆盖代理，negated标签与逻辑否定未必等价。S中其他modality有同跨度提示候选的数量不是错误率，标注不完备且允许条件、编辑、极性同现。14专项控制；所有规则、排序、范围及测试由研究者选择，已见语料，无训练、真实独立验证、完整负例或泛化证据。无新外部资料、原生产品运行、Codex改动、CI、PR合并、部署、费用或冻结变化。后续研究在独立归档累积，v0.7范围不变。
## 复算
按上述四份文件顺序置入docs[i].content，Node标准JS，仅执行已审查自有源码。
```js
function load(docs){
 const c=i=>docs[i].content.split("```js\n")[1].split("\n```")[0];
 const I=Function(c(0).split(" const out={datasets:")[0]+"\nreturn {build,verify};\n}\nreturn experiment();")();
 const S=Function(c(1).split(" const blank=()=>")[0]+"\nreturn {scan};\n}\nreturn experiment();")();
 return {I,S}
}
function experiment(I,S,corpora,assets){
 const ck=(v,m)=>{if(!v)throw Error(m)},same=(a,b)=>a.start===b.start&&a.end===b.end,inside=(a,b)=>a.start>=b.start&&a.end<=b.end,overlap=(a,b)=>a.start<b.end&&b.start<a.end;
 const words=[["仅用于","guard_after"],["如果","guard_before"],["只要","guard_before"],["若","guard_before"],["没有","polarity"],["不能","polarity"],["不要","polarity"],["并非","polarity"],["不再","polarity"],["不","polarity"],["没","polarity"],["未","polarity"],["无","polarity"],["撤回","edit"],["撤掉","edit"],["取消","edit"]];
 function graph(text,cap=50000){
  let s=S.scan(text);if(s.status!=="CANDIDATES_ONLY")return {status:"LIMIT",edges:[],scopes:[],authority:"NONE",outside:true};
  const anchors=[];for(let i=0;i<text.length;){let m=words.find(([w])=>text.startsWith(w,i));if(!m){i++;continue}anchors.push({start:i,end:i+m[0].length,raw:m[0],kind:m[1]});i+=m[0].length}
  const edges=[],scopes=[],sentence=(a,b)=>!/[。！？；.!?;]/u.test(text.slice(Math.min(a.start,b.start),Math.max(a.end,b.end))),boundary=x=>s.clauses.reduce((n,c)=>n+ +(x.start===c.start)+ +(x.end===c.end),0);
  for(let a of anchors){
   if(a.kind.startsWith("guard")){
    const gs=s.all.filter(x=>x.start===(a.kind==="guard_after"?a.end:a.start)&&x.end>a.end);
    for(let g of gs)for(let t of s.all){
     if(!sentence(g,t)||same(g,t))continue;
     let rel=inside(g,t)&&t.start<g.start?"embedded":t.start>=g.end?"forward":t.end<=g.start?"backward":null;
     if(!rel)continue;
     let gap=rel==="embedded"?0:rel==="forward"?t.start-g.end:g.start-t.end;
     edges.push({anchor:a,guard:g,target:t,relation:rel,score:4*boundary(g)+4*boundary(t)-gap-Math.abs(t.end-t.start-8)/4,authority:"NONE",outside:true});
     if(edges.length+scopes.length>cap)return {status:"LIMIT",edges:[],scopes:[],authority:"NONE",outside:true}
    }
   }else for(let t of s.all.filter(x=>inside(a,x))){
    scopes.push({anchor:a,scope:t,score:4*boundary(t)-Math.abs(t.end-t.start-8)/4,authority:"NONE",outside:true});
    if(edges.length+scopes.length>cap)return {status:"LIMIT",edges:[],scopes:[],authority:"NONE",outside:true}
   }
  }
  edges.sort((a,b)=>b.score-a.score||a.guard.start-b.guard.start||a.guard.end-b.guard.end||a.target.start-b.target.start||a.target.end-b.target.end);
  scopes.sort((a,b)=>b.score-a.score||a.scope.start-b.scope.start||a.scope.end-b.scope.end||a.anchor.start-b.anchor.start);
  return {status:"CANDIDATES_ONLY",anchors,edges,scopes,authority:"NONE",outside:true}
 }
 const out={turns:0,annotations:0,anchors:0,guardAnchors:0,polarityAnchors:0,editAnchors:0,edges:0,scopes:0,conditionTargets:0,conditionExact:0,conditionTop20:0,conditionTop100:0,adjacentClauseExact:0,negatedTargets:0,negatedScopeExact:0,negatedTop20:0,negatedTop100:0,negatedPolarityOnly:0,negatedEditOnly:0,nonnegatedAnnotatedWithCue:0,conditionRows:[],negatedRows:[],unanchoredLegacy:[],controls:0};
 for(let d=0;d<2;d++){
  let ir=I.build(corpora[d],assets[d]);ck(I.verify(ir,corpora[d],assets[d]),"IR");
  for(let ep of ir.episodes)for(let t of ep.turns){
   let g=graph(t.text),s=S.scan(t.text);ck(g.status==="CANDIDATES_ONLY","limit");out.turns++;out.anchors+=g.anchors.length;out.guardAnchors+=g.anchors.filter(a=>a.kind.startsWith("guard")).length;out.polarityAnchors+=g.anchors.filter(a=>a.kind==="polarity").length;out.editAnchors+=g.anchors.filter(a=>a.kind==="edit").length;out.edges+=g.edges.length;out.scopes+=g.scopes.length;
   for(let e of g.edges)ck(t.text.slice(e.guard.start,e.guard.end)===e.guard.text&&t.text.slice(e.target.start,e.target.end)===e.target.text&&e.outside&&e.authority==="NONE","edge anchor");
   for(let e of g.scopes)ck(t.text.slice(e.scope.start,e.scope.end)===e.scope.text&&inside(e.anchor,e.scope)&&e.outside,"scope anchor");
   for(let a of t.items){
    out.annotations++;
    let c=a.dimensions.condition,m=a.dimensions.modality;
    // Only S has separately anchored, literal condition text. L condition
    // codes are not raw spans, and legacy role labels do not imply boundaries.
    if(d===1&&c.status==="ANNOTATED"&&typeof c.value==="string"){
     let i=t.text.indexOf(c.value);ck(i>=0&&i===t.text.lastIndexOf(c.value),"guard anchor");
     let guard={start:i,end:i+c.value.length},rank=g.edges.findIndex(e=>same(e.guard,guard)&&same(e.target,a.span))+1;
     out.conditionTargets++;out.conditionExact+=+(rank>0);out.conditionTop20+=+(rank>0&&rank<=20);out.conditionTop100+=+(rank>0&&rank<=100);
     let k=s.clauses.findIndex(x=>same(x,guard)),adj=k>=0&&!!s.clauses[k+1]&&same(s.clauses[k+1],a.span);out.adjacentClauseExact+=+adj;
     out.conditionRows.push({id:a.id,guard:c.value,target:a.span.text,rank:rank||null,relation:rank?g.edges[rank-1].relation:null,adjacentClauseExact:adj,edges:g.edges.length})
    }
    if(d===0&&["CONDITIONAL_HARD","CONDITIONAL_ACTION","TRIGGER","EXCEPTION","HARD_CONSEQUENCE"].includes(a.originalLabel))out.unanchoredLegacy.push({id:a.id,quote:a.span.text,label:a.originalLabel,condition:c.status,markerInside:g.anchors.some(x=>x.kind.startsWith("guard")&&inside(x,a.span))});
    if(d===1&&m.status==="ANNOTATED"){
     let all=g.scopes.filter(e=>same(e.scope,a.span));
     if(m.value==="negated"){
      let rank=g.scopes.findIndex(e=>same(e.scope,a.span))+1;
      out.negatedTargets++;out.negatedScopeExact+=+(rank>0);out.negatedTop20+=+(rank>0&&rank<=20);out.negatedTop100+=+(rank>0&&rank<=100);
      out.negatedPolarityOnly+=+(all.length>0&&all.every(e=>e.anchor.kind==="polarity"));out.negatedEditOnly+=+(all.length>0&&all.every(e=>e.anchor.kind==="edit"));
      out.negatedRows.push({id:a.id,quote:a.span.text,rank:rank||null,cues:[...new Set(all.map(e=>e.anchor.raw))],role:a.role,edit:a.dimensions.edit.value??null})
     }else if(all.length)out.nonnegatedAnnotatedWithCue++;
    }
   }
  }
 }
 for(let f of [()=>out.turns===64&&out.annotations===167,()=>out.conditionTargets===4,()=>out.conditionExact>=out.adjacentClauseExact,()=>out.negatedTargets===7,()=>graph("如果下雨，明天取消").edges.some(e=>e.guard.text==="如果下雨"&&e.target.text==="明天取消"),()=>graph("要求仅用于正式交付").edges.some(e=>e.guard.text==="正式交付"&&e.target.text==="要求仅用于正式交付"&&e.relation==="embedded"),()=>graph("如果下雨。明天取消").edges.every(e=>!e.target.text.includes("明天")),()=>graph("没有计划").anchors[0].raw==="没有",()=>graph("撤回授权").anchors[0].kind==="edit",()=>graph("不低于三百").scopes.length>0,()=>graph("随便说说").anchors.length===0&&graph("随便说说").outside,()=>graph("如果下雨，明天取消",0).status==="LIMIT",()=>graph("如果下雨，明天取消",0).edges.length===0,()=>graph("字".repeat(129)).status==="LIMIT"]){ck(f(),"control "+out.controls);out.controls++}
 return out
}
const {I,S}=load(docs);console.log(JSON.stringify(experiment(I,S,docs.slice(2).map(x=>JSON.parse(x.content)),docs.slice(2).map((x,i)=>({id:i?"S":"L",sha:x.sha}))),null,2));
```
## 实测
```json
{
  "turns": 64,
  "annotations": 167,
  "anchors": 78,
  "guardAnchors": 8,
  "polarityAnchors": 67,
  "editAnchors": 3,
  "edges": 2842,
  "scopes": 1148,
  "conditionTargets": 4,
  "conditionExact": 4,
  "conditionTop20": 3,
  "conditionTop100": 4,
  "adjacentClauseExact": 2,
  "negatedTargets": 7,
  "negatedScopeExact": 7,
  "negatedTop20": 7,
  "negatedTop100": 7,
  "negatedPolarityOnly": 5,
  "negatedEditOnly": 2,
  "nonnegatedAnnotatedWithCue": 14,
  "conditionRows": [
    {
      "id": "S03.2.1",
      "guard": "如果周五需要加班",
      "target": "周五答疑就取消",
      "rank": 1,
      "relation": "forward",
      "adjacentClauseExact": true,
      "edges": 203
    },
    {
      "id": "S06.1.1",
      "guard": "如果医生允许",
      "target": "参加长跑活动",
      "rank": 31,
      "relation": "forward",
      "adjacentClauseExact": false,
      "edges": 314
    },
    {
      "id": "S09.2.1",
      "guard": "如果集合改到周一早上",
      "target": "隔天出发也可以",
      "rank": 1,
      "relation": "forward",
      "adjacentClauseExact": true,
      "edges": 308
    },
    {
      "id": "S13.2.1",
      "guard": "正式交付",
      "target": "准确率的要求仅用于正式交付",
      "rank": 1,
      "relation": "embedded",
      "adjacentClauseExact": false,
      "edges": 544
    }
  ],
  "negatedRows": [
    {
      "id": "S01.2.1",
      "quote": "转去调度部这项先撤掉",
      "rank": 1,
      "cues": [
        "撤掉"
      ],
      "role": "action",
      "edit": "retract"
    },
    {
      "id": "S05.2.1",
      "quote": "我本人暂时没有换工作的打算",
      "rank": 1,
      "cues": [
        "没有"
      ],
      "role": "action",
      "edit": "add"
    },
    {
      "id": "S10.2.1",
      "quote": "不作为强制条件了",
      "rank": 1,
      "cues": [
        "不"
      ],
      "role": "constraint",
      "edit": "retract"
    },
    {
      "id": "S11.1.2",
      "quote": "不要保存",
      "rank": 2,
      "cues": [
        "不要"
      ],
      "role": "permission_intent",
      "edit": "add"
    },
    {
      "id": "S11.1.3",
      "quote": "不要拿去训练",
      "rank": 4,
      "cues": [
        "不要"
      ],
      "role": "permission_intent",
      "edit": "add"
    },
    {
      "id": "S11.2.1",
      "quote": "撤回临时分析的许可",
      "rank": 8,
      "cues": [
        "撤回"
      ],
      "role": "permission_intent",
      "edit": "retract"
    },
    {
      "id": "S11.2.2",
      "quote": "之前的对话不要再用于计算",
      "rank": 2,
      "cues": [
        "不要"
      ],
      "role": "permission_intent",
      "edit": "add"
    }
  ],
  "unanchoredLegacy": [
    {
      "id": "L04.2.2",
      "quote": "延期会失去报名资格",
      "label": "HARD_CONSEQUENCE",
      "condition": "UNANNOTATED",
      "markerInside": false
    },
    {
      "id": "L05.1.3",
      "quote": "到时候看谁更需要，再挪两天",
      "label": "CONDITIONAL_ACTION",
      "condition": "UNANNOTATED",
      "markerInside": false
    },
    {
      "id": "L09.2.1",
      "quote": "午饭后如果没有会议",
      "label": "TRIGGER",
      "condition": "UNANNOTATED",
      "markerInside": true
    },
    {
      "id": "L09.2.3",
      "quote": "有会议就先不走",
      "label": "EXCEPTION",
      "condition": "UNANNOTATED",
      "markerInside": false
    },
    {
      "id": "L13.2.2",
      "quote": "如果再有人身威胁我就不联系",
      "label": "CONDITIONAL_HARD",
      "condition": "ANNOTATED",
      "markerInside": true
    },
    {
      "id": "L14.1.3",
      "quote": "不发就撑不住",
      "label": "HARD_CONSEQUENCE",
      "condition": "UNANNOTATED",
      "markerInside": false
    },
    {
      "id": "L16.1.4",
      "quote": "只要有明显安全风险我就换路",
      "label": "CONDITIONAL_HARD",
      "condition": "UNANNOTATED",
      "markerInside": true
    }
  ],
  "controls": 14
}
```
后续：针对作用域歧义及候选爆炸，研究可证实的联合推理与有限澄清，而非无限扩词；同时优先推进独立真实语料资格。正式开发、训练另获授权。
