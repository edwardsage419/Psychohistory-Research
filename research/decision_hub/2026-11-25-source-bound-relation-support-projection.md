# 自主认知专项累计第133轮候选：来源绑定的原文关系支持与联合投影
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / RAW_RELATION_SUPPORT / PUBLIC_SYNTHETIC_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 3a725062c742cc0116d29e0f28640bfacbecafbf。核对近期12提交、13开放PR（#61待审）、v3.2前15行及历史全文、唯一交接前18行、v0.7任务前10行、R132前16行、R93/R87/R81前15行及实际R131/R132复用代码。
## 查重勘误
R132在查重时遗漏R93（2026-11-25-correlated-semantic-decision-certificates.md，blob 1e17a6a47458c19e46f52151a59a0b6bf863a6f0）。R93已经研究关联域最小固定澄清集合、击中集证明及答案分组复算。R132的核心算法和相关性结论实质重复；R132新增长为任意二元出口真值表的穷举与指定必确认字段，以及R131原文关系锚回查；不得把R132视为全新方法、独立验证或额外独立样本。保留原记录，补充此勘误；后续查重须核对已知相关标题实际正文，避免以扩大合成计数代替关键缺口。
## 固定资产
research/decision_hub/2026-11-25-correlated-interpretation-question-separation.md 2ef743e0ea767dcc3ba551eff819eae71b1e2df7
research/decision_hub/2026-11-25-condition-polarity-attachment-candidate-audit.md 81df7d2fc56f29084ecc623b98cdf0991d3260d4
research/decision_hub/2026-11-25-unified-semantic-annotation-bridge.md af648d16ee96b9af4a3efb61b413d113208bb0ca
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
R93 1e17a6a47458c19e46f52151a59a0b6bf863a6f0；R87 4c86134031439991991c7bfb9c2bc10fc1aa4dab；R81 f078d341a783dedf4be2ea9d6e1d5de6faaf618d；v0.7任务 cae356da125f808c9a7feebe3940cc71e2347927；唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07。原语料为ChatGPT研发辅助项目原创公开合成开发材料，非真人、独立留出或授权训练。
## 增量
R81已有人工关系约束CSP，R87已有人工节点存在与引用联合推理。本轮实际重用R131对原始64轮生成的关系边，以来源/版本/全文及原文锚、条件跨度、目标跨度、关系类型形成完整有限图。比较全图中守卫/目标/关系的联合支持，与分别去重后取笛卡尔积的虚增组合。后者仅表示不在R131有限枚举关系中的组合，不能判断自然语言中必然无效，也不表示真实误判率。图外解释始终保留outside；排序只用于显示，不能取top20或top100充当全图。纯函数模拟可信宿主确认一个或多个坐标的允许值，直接筛选真实关系边，保留原始关联，重新计算完整图核验结构、当前源、版本、全文、确切字段和值。没有全局语义覆盖、角色、身份、因果、真实许可或合格数学映射；不允许进入R132确定决策域。空结果是NO_ENUMERATED_MATCH，不是事实冲突；缺少/撤回/过期/篡改返回UNKNOWN；输出永远authority NONE、outside true。源标识为合成情节和轮次，人工active和confirmed仅模拟当前性；不是实际认证、持久化事务、可靠加密收据或独立语义确认。原文可能重复或含有跨句关系、未建模提示、隐含条件；本轮仅现有R131图域，不补造关系或通过强制唯一解释得出用户意图。
## 实验
实际重放原64轮全图，统计联合与独立边际组合；遍历每个已有坐标值，投影与直接过滤核对，四项既有S条件标注仅事后用作人工选定的原文坐标，比较确认守卫/目标/两者后的有限边数。无完整负标注，不估计真实精度，人工坐标不能当作自动语义识别。四例各执行撤回、过期、8种输入/图/收据变异，11专项控制。每次重放全图作验证，未测设备性能或生产资源预算，依赖R131有限输入规则。研究者选择字段和模拟确认；非独立验收。无训练、原生平台、Codex、CI、PR合并、部署、费用或冻结变更。v0.7任务范围不变。
## 复算
按上述六份文件顺序置入docs[i].content，Node标准JS，仅执行已审查自有源码。
```js
function load(docs){
 const c=docs[0].content.split("```js\n")[1].split("\n```")[0];
 return Function(c.split("function experiment(graph,corpus)")[0]+"\nreturn load;")()(docs.slice(1));
}
function experiment(graph,corpora){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const span=s=>[s.start,s.end,s.text],key=s=>JSON.stringify(span(s));
 const edge=e=>JSON.stringify([e.anchor.start,e.anchor.end,e.anchor.raw,e.anchor.kind,span(e.guard),span(e.target),e.relation]);
 function build(raw){
  const g=graph(raw.text);
  if(g.status!=="CANDIDATES_ONLY")return null;
  const rows=g.edges.map(e=>({id:edge(e),g:key(e.guard),t:key(e.target),rel:e.relation,score:e.score}));
  ck(new Set(rows.map(e=>e.id)).size===rows.length,"duplicate edge");
  return {source:raw.source,version:raw.version,text:raw.text,rows,authority:"NONE",outside:true};
 }
 // Full finite graph replay, not an assertion that the language is understood.
 // The synthetic host supplies exact permitted coordinate values, never
 // chooses new edges by taking the product of marginal sets.
 function filter(raw,index,receipt,active){
  if(!raw||!index||active.get(raw.source)!==raw.version||!eq(index,build(raw))||!receipt||receipt.confirmed!==true||receipt.source!==raw.source||receipt.version!==raw.version||receipt.text!==raw.text||!Array.isArray(receipt.predicates)||receipt.predicates.some(p=>!["g","t","rel"].includes(p.field)||!Array.isArray(p.allowed)||!p.allowed.length||new Set(p.allowed).size!==p.allowed.length||p.allowed.some(v=>!index.rows.some(r=>r[p.field]===v))))return {status:"UNKNOWN",rows:[],outside:true,authority:"NONE"};
  const rows=index.rows.filter(r=>receipt.predicates.every(p=>p.allowed.includes(r[p.field])));
  return {status:rows.length?"FINITE_CANDIDATES":"NO_ENUMERATED_MATCH",rows:rows.map(r=>r.id),outside:true,authority:"NONE"};
 }
 const out={turns:0,turnsWithEdges:0,edges:0,independentCartesianPairs:0,unsupportedPairs:0,turnsWithUnsupportedPairs:0,relationTriples:0,unsupportedTriples:0,annotatedTargets:0,top20Missing:0,top100Missing:0,guardOnlyRemaining:0,targetOnlyRemaining:0,bothRemaining:0,exactPairRetained:0,filterChecks:0,withdrawalChecks:0,staleChecks:0,mutationChecks:0,controls:0,examples:[]};
 for(let d=0;d<2;d++)for(let ep of corpora[d].cases)for(let [i,t] of ep.turns.entries()){
  let raw={source:ep.id+":"+i,version:1,text:t.text},idx=build(raw);ck(idx,"graph");out.turns++;
  if(!idx.rows.length)continue;
  out.turnsWithEdges++;out.edges+=idx.rows.length;
  const gs=[...new Set(idx.rows.map(r=>r.g))],ts=[...new Set(idx.rows.map(r=>r.t))],rs=[...new Set(idx.rows.map(r=>r.rel))];
  let pairs=new Set(idx.rows.map(r=>JSON.stringify([r.g,r.t]))),triples=new Set(idx.rows.map(r=>JSON.stringify([r.g,r.t,r.rel])));
  out.independentCartesianPairs+=gs.length*ts.length;out.unsupportedPairs+=gs.length*ts.length-pairs.size;out.turnsWithUnsupportedPairs+=+(gs.length*ts.length>pairs.size);
  out.relationTriples+=gs.length*ts.length*rs.length;out.unsupportedTriples+=gs.length*ts.length*rs.length-triples.size;
  let active=new Map([[raw.source,1]]),base={source:raw.source,version:1,text:raw.text,confirmed:true,predicates:[]};
  // Test every actual endpoint and relation projection; no new labels.
  for(let [field,values] of [["g",gs],["t",ts],["rel",rs]])for(let v of values){
   let q={...base,predicates:[{field,allowed:[v]}]},z=filter(raw,idx,q,active);
   ck(eq(z.rows,idx.rows.filter(r=>r[field]===v).map(r=>r.id))&&z.outside&&z.authority==="NONE","single projection");out.filterChecks++;
  }
  for(let a of t.claims??t.proposal.claims){
   if(d!==1||typeof a.condition!=="string"||!a.quote)continue;
   let g0=t.text.indexOf(a.condition),t0=t.text.indexOf(a.quote);
   ck(g0>=0&&t0>=0,"anchor");
   let g=JSON.stringify([g0,g0+a.condition.length,a.condition]),k=JSON.stringify([t0,t0+a.quote.length,a.quote]),rank=idx.rows.findIndex(r=>r.g===g&&r.t===k)+1;
   ck(rank>0,"existing annotation");out.annotatedTargets++;out.top20Missing+=+(rank>20);out.top100Missing+=+(rank>100);
   let p={field:"g",allowed:[g]},q={field:"t",allowed:[k]},one=filter(raw,idx,{...base,predicates:[p]},active),two=filter(raw,idx,{...base,predicates:[q]},active),both=filter(raw,idx,{...base,predicates:[p,q]},active);
   out.guardOnlyRemaining+=one.rows.length;out.targetOnlyRemaining+=two.rows.length;out.bothRemaining+=both.rows.length;
   ck(eq(both.rows,idx.rows.filter(r=>r.g===g&&r.t===k).map(r=>r.id)),"joint projection");out.exactPairRetained+=+(both.rows.length>0);
   const r={...base,predicates:[p,q]};
   ck(filter(raw,idx,r,new Map()).status==="UNKNOWN","withdraw");out.withdrawalChecks++;
   ck(filter(raw,idx,r,new Map([[raw.source,2]])).status==="UNKNOWN","stale");out.staleChecks++;
   let bads=[[{...raw,source:"other"},idx,r],[raw,{...idx,rows:idx.rows.slice(0,20)},r],[raw,{...idx,rows:idx.rows.map((x,j)=>j?x:{...x,rel:"other"})},r],[raw,idx,{...r,confirmed:false}],[raw,idx,{...r,version:2}],[raw,idx,{...r,text:r.text+"。"}],[raw,idx,{...r,predicates:[{field:"g",allowed:["invented"]}]}],[raw,idx,{...r,predicates:[{field:"authority",allowed:["PASS"]}]}]];
   for(let [x,y,z] of bads){ck(filter(x,y,z,active).status==="UNKNOWN","mutation");out.mutationChecks++}
   out.examples.push({id:ep.id,guard:a.condition,target:a.quote,rank,rows:idx.rows.length,guardOnly:one.rows.length,targetOnly:two.rows.length,both:both.rows.length,outside:both.outside});
  }
 }
 for(let f of [()=>out.turns===64,()=>out.edges===2842,()=>out.annotatedTargets===4&&out.exactPairRetained===4,()=>out.top20Missing===1&&out.top100Missing===0,()=>out.unsupportedPairs>0,()=>out.unsupportedTriples>=out.unsupportedPairs,()=>out.bothRemaining<=out.guardOnlyRemaining&&out.bothRemaining<=out.targetOnlyRemaining,()=>out.mutationChecks===32,()=>out.withdrawalChecks===4&&out.staleChecks===4,()=>{let raw={source:"s",version:1,text:"如果下雨，明天取消"},idx=build(raw),a=new Map([["s",1]]);return filter(raw,idx,{source:"s",version:1,text:raw.text,confirmed:true,predicates:[]},a).outside===true},()=>{let raw={source:"s",version:1,text:"没有条件提示"},idx=build(raw),a=new Map([["s",1]]);return filter(raw,idx,{source:"s",version:1,text:raw.text,confirmed:true,predicates:[]},a).status==="NO_ENUMERATED_MATCH"}]){ck(f(),"control "+out.controls);out.controls++}
 return out
}
console.log(JSON.stringify(experiment(load(docs),docs.slice(4).map(x=>JSON.parse(x.content))),null,2));
```
## 实测
```json
{
  "turns": 64,
  "turnsWithEdges": 8,
  "edges": 2842,
  "independentCartesianPairs": 4271,
  "unsupportedPairs": 1429,
  "turnsWithUnsupportedPairs": 8,
  "relationTriples": 9973,
  "unsupportedTriples": 7131,
  "annotatedTargets": 4,
  "top20Missing": 1,
  "top100Missing": 0,
  "guardOnlyRemaining": 252,
  "targetOnlyRemaining": 22,
  "bothRemaining": 4,
  "exactPairRetained": 4,
  "filterChecks": 693,
  "withdrawalChecks": 4,
  "staleChecks": 4,
  "mutationChecks": 32,
  "controls": 11,
  "examples": [
    {
      "id": "S03",
      "guard": "如果周五需要加班",
      "target": "周五答疑就取消",
      "rank": 1,
      "rows": 203,
      "guardOnly": 28,
      "targetOnly": 6,
      "both": 1,
      "outside": true
    },
    {
      "id": "S06",
      "guard": "如果医生允许",
      "target": "参加长跑活动",
      "rank": 31,
      "rows": 314,
      "guardOnly": 76,
      "targetOnly": 4,
      "both": 1,
      "outside": true
    },
    {
      "id": "S09",
      "guard": "如果集合改到周一早上",
      "target": "隔天出发也可以",
      "rank": 1,
      "rows": 308,
      "guardOnly": 28,
      "targetOnly": 8,
      "both": 1,
      "outside": true
    },
    {
      "id": "S13",
      "guard": "正式交付",
      "target": "准确率的要求仅用于正式交付",
      "rank": 1,
      "rows": 544,
      "guardOnly": 120,
      "targetOnly": 4,
      "both": 1,
      "outside": true
    }
  ]
}
```
后续优先合法真实数据与组合泛化，避免继续围绕同一公开开发集做重复计数；开放语义覆盖和可信联合解释资格仍为核心阻塞。正式工程和训练另获授权。
