# 自主认知专项累计第113轮候选：标注条件下的跨轮修订检索消融
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / REAL_REPOSITORY_TEXT_RETRIEVAL / ORACLE_ANNOTATIONS / PUBLIC_SYNTHETIC_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main d916fd5acec2a59e9b267fdb6f7e17931f25eb2c。核对近期12提交、13开放PR（#61待审）、v3.2前15行及历史全文、唯一交接前18行、R112前18行与全文、R86前22行、R64前30行、R73前22行及原函数，两个语料全部标注。区别R64有限语法识别、R86有向特征、R112原文跨轮检索：本轮以已给定标注作为理想诊断输入，对真实研究检索器进行上下文编辑消融，不声称解决自动指代、否定或修订识别。
## 固定资产
research/decision_hub/2026-11-25-contextual-goal-discovery-method-preparation.md 6e566bb73ae1b34a25945ef29843d6a16d07b5b9
research/decision_hub/2026-11-25-unified-semantic-annotation-bridge.md af648d16ee96b9af4a3efb61b413d113208bb0ca
research/decision_hub/2026-11-24-content-method-retrieval/config.json ff838223473dd27aed6865ccaa0971b90ded17c7
research/decision_hub/2026-11-24-content-method-retrieval/probe.js 7d78f8c89ac73a2228ddca40dd45ad8b02366554
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
research/decision_methods/C028_INTERVAL_HARD_CONSTRAINT_FEASIBILITY_2026-11-20.md 7cb8d5e3631dd17c0650cec06139d88b5bfcc700
research/decision_methods/C028_MANSKI_1990_UNOBSERVED_ALTERNATIVES_BOUNDS_2026-11-20.md a221a3a1e95ca3262a3574ab7685890f5f50d6d5
research/decision_methods/C004_DYNAMIC_UTILITY_MULTI_OBJECTIVE_ROBUST_2026-10-27.md 0d04c633a26437ad6017946cd528c4dc68db3d83
research/decision_methods/C029_SCENARIO_MINIMAX_REGRET_INFORMATION_BOUNDARY_2026-11-20.md a2588cfdd47e547a46a7ee8cde2644caf81198d9
research/decision_methods/VOI_IMPERFECT_BINARY_SIGNAL_METHOD_CARD_2026-11-20.md bd494e2e1200a526dcb11d454e423ff9aebccd33
research/decision_methods/C009_OPTION_VALUE_INFORMATION_REVERSIBILITY_2026-11-01.md 5048081b0a277f4bc511aff2293020268fd5c57c
research/decision_methods/C035_BLEICHRODT_PINTO_WAKKER_2001_ELICITATION_CORRECTION_BOUNDARIES_2026-11-20.md 40d77d89356e7f3d3c8e02e3a93fd6f634ec09d2
research/decision_methods/C036_TWO_STAGE_ADJUSTABLE_FEASIBILITY_QUANTIFIER_BOUNDARY_2026-11-23.md d2438afcc93f8568cb3a0ef00285fa2f66b34f23
R64 da54c5b88ed0f19f5c5d272230a1959b811f5b5e；R86 ac7cafba4b3dd72e12531b08d36ebe7307e0a9c3；唯一交接 5e74f4f0b37141d631740e844ad8bbbfed232e07。8卡连接器全文回读，blob匹配原配置，未独立核验字节、原论文、许可或科学准入；两语料既有公开原创合成开发样例，非真人、独立留出或训练。
## 方法及边界
R73实际build/verify复用标注IR及引用候选；R28实际BM25与R112历史查询扩展、8卡、32情节级主题标签保持相同。四种检索：raw=全历史原文+自动历史扩展，spanOnly=全部既有标注的有限角色跨度+扩展，editAware=人工引用明确时移除被替代/撤回根及非正向撤回表达，guarded=再隔离条件/范围不明相关跨度或暂停许可意图对应情节检索。所有阶段均教师给定标注；原始标注有遗漏、含未来设计信息，不能作开放语义识别、真实权限或证据。S03条件取消、S13范围限定、S11许可撤回由研究者基于实际原文明确标为三种特殊控制；即使唯一引用仍不能全局删除。S03保留原行动供条件核验，S13保留原底线供作用域核验，guarded暂不把两者传检索；这不是最终决策状态，不能当作不存在条件。S11第二轮仅模拟可信宿主暂停该情节检索，未执行真实撤权、访问控制或擦除；L18仅保存/训练限制不等于禁止临时分析。权限意图不授予授权，合成语料处理不涉及真实私密记录。对未标注引用、否定作用域、主体/时间冲突、无标注修订及多分支仍不具自动处理能力。spanOnly/edited使用原标注片段可能丢失原文作用域、否定或未标事实，绝不可直接进数学计算。标签复用R112的两轮相同主题，不适合精确评估修订后用户意图；尤其L08排除后仍保留旧regret主题，故指标只用于与固定历史基线的可比性，不能判定真实相关性改善。所有结果仅研究候选，未连接实际方法执行。研究者决定角色允许表、特殊守卫和比较策略，未来真实实现必须以自主解析候选和独立可信确认代替oracle。统计retired为旧节点，retiredSpanChecks为身份集合检查，不是物理删除或内容不可泄露；naiveGlobalRetractions为三项不宜无条件删除的标注修改，非原生漏洞。无新增外部数据、训练、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。
## 复算
按上述六文件顺序读取docs[i].content，按R112同一8卡选法组装cards（含原cfg元数据及实际body），Node标准JS，仅加载已审查项目自有源码，不执行任意网络文档。
```js
function load(docs){
 const src=docs[3].content;
 const R=Function(src.slice(src.indexOf("function toks("),src.indexOf("function run("))+"\nreturn {rank};")();
 const ir=docs[1].content.split("```js\n")[1].split("\n```")[0].split(" const out={datasets:")[0];
 const I=Function(ir+"\nreturn {build,verify};\n}\nreturn experiment();")();
 const old=docs[0].content.split("```js\n")[1].split("\n```")[0];
 const labels=JSON.parse(old.split("const labels=")[1].split(";\n")[0]);
 return {R,I,labels}
}
function experiment(R,I,labels,cfg,cards,corpora,assets){
 const ck=(x,m)=>{if(!x)throw Error(m)},hist=cfg.queries.map(q=>({path:q.id,group:q.id,body:q.zh,expanded:q.expanded}));
 function retrieve(text){if(!text)return [];let n=R.rank(hist,text,"body")[0],ex=n?hist.find(x=>x.path===n.path).expanded:"";return R.rank(cards,text+(ex?" "+ex:""),"body").slice(0,3).map(x=>x.group)}
 // Teacher-forced edit policies based on annotations, NOT inferred from raw language.
 // S03 is conditional (whole original sentence); S13 narrows scope; S11 is a permission intent.
 // L08 excludes criterion; L15 promotes a goal to constraint.
 const guards={"S03.2.1":"CONDITIONAL","S13.2.1":"SCOPE_CHANGE","S11.2.1":"PERMISSION_INTENT"};
 const safeRoles=new Set(["constraint","action","goal","criterion","preference","report","estimate","cost","unknown","hypothesis","consequence","scope_modifier","confirmation","revision","choice","observation","counterfactual","retrospective","trigger","event_definition"]);
 const modes=["raw","spanOnly","editAware","guarded"];
 let out={episodes:0,turns:0,annotatedLinks:0,uniqueLinks:0,retired:0,conditional:0,scopeChange:0,permissionIntent:0,privacyHold:0,unresolvedEdit:0,naiveGlobalRetractions:0,guardedQueries:0,retiredSpanChecks:0,activeSpanChecks:0,rankChanged:0,controls:0,metrics:Object.fromEntries(modes.map(m=>[m,{positive:0,negative:0,hit1:0,hit3:0,recalled:0,relevant:0,negativeNonempty:0,nonempty:0}])),rows:[]};
 for(let d=0;d<corpora.length;d++){
  let a=I.build(corpora[d],assets[d]);ck(I.verify(a,corpora[d],assets[d]),"IR");
  for(let e of a.episodes){
   out.episodes++;let active=new Map(),all=new Map(),excluded=new Set(),uncertain=new Set(),hold=false;
   for(let t=0;t<e.turns.length;t++){
    let turn=e.turns[t];out.turns++;
    for(let x of turn.items){
     all.set(x.id,x);
     const edit=x.dimensions.edit.value,ref=x.reference;
     if(ref.original.status==="ANNOTATED"){out.annotatedLinks++;if(ref.status==="UNIQUE_CANDIDATE")out.uniqueLinks++}
     if(["replace","retract","exclude","promote_to_hard"].includes(edit)){
      if(ref.status!=="UNIQUE_CANDIDATE"||!active.has(ref.candidates[0])){out.unresolvedEdit++;uncertain.add(x.id);continue}
      let target=ref.candidates[0],g=guards[x.id];
      if(g){uncertain.add(target);uncertain.add(x.id);
       if(g==="CONDITIONAL")out.conditional++;
       if(g==="SCOPE_CHANGE")out.scopeChange++;
       if(g==="PERMISSION_INTENT"){out.permissionIntent++;hold=true}
       out.naiveGlobalRetractions++;continue
      }
      active.delete(target);excluded.add(target);out.retired++;
      if(edit==="retract"||edit==="exclude"){excluded.add(x.id);continue}
     }
     active.set(x.id,x)
    }
    // privacy intent in the two privacy episodes is not actual authorization.
    // S11 second-turn hold models trusted-host precaution; L18 scope remains unspecified.
    const raw=e.turns.slice(0,t+1).map(v=>v.text).join("。");
    const spans=xs=>xs.filter(x=>safeRoles.has(x.role)).sort((a,b)=>a.id.localeCompare(b.id,undefined,{numeric:true})).map(x=>x.span.text).join("。");
    let spanOnly=spans([...all.values()]),editAware=spans([...active.values()]);
    // Conservative branch: suspend the implicated scope from retrieval, not erase it.
    let guarded=hold?"":spans([...active.values()].filter(x=>!uncertain.has(x.id)));
    if(hold)out.privacyHold++;else if(guarded)out.guardedQueries++;
    for(let id of excluded){ck(!active.has(id),"retired identity");out.retiredSpanChecks++}
    for(let id of active.keys()){ck(all.has(id)&&!excluded.has(id),"active identity");out.activeSpanChecks++}
    const ranks={raw:retrieve(raw),spanOnly:retrieve(spanOnly),editAware:retrieve(editAware),guarded:retrieve(guarded)};
    if(t>0&&JSON.stringify(ranks.raw)!==JSON.stringify(ranks.guarded))out.rankChanged++;
    const target=labels[e.meta.id];ck(Array.isArray(target),"label");
    for(let m of modes){let v=out.metrics[m],r=ranks[m],n=target.filter(g=>r.includes(g)).length;v.nonempty+=+!!r.length;if(target.length){v.positive++;v.hit1+=+(target.includes(r[0]));v.hit3+=+(n>0);v.relevant+=target.length;v.recalled+=n}else{v.negative++;v.negativeNonempty+=+!!r.length}}
    out.rows.push({id:e.meta.id,turn:t+1,retired:[...excluded],uncertain:[...uncertain],hold,active:[...active.keys()],ranks})
   }
  }
 }
 for(let v of Object.values(out.metrics))v.recall=v.recalled/v.relevant;
 for(let test of [()=>out.turns===64,()=>out.annotatedLinks===12,()=>out.uniqueLinks===12,()=>out.retired===9,()=>out.conditional===1&&out.scopeChange===1&&out.permissionIntent===1,()=>out.privacyHold===1,()=>out.rows.find(r=>r.id==="S11"&&r.turn===2).ranks.guarded.length===0,()=>out.rows.find(r=>r.id==="S03"&&r.turn===2).active.includes("S03.1.3"),()=>out.rows.find(r=>r.id==="S13"&&r.turn===2).active.includes("S13.1.3")]){ck(test(),"control "+out.controls);out.controls++}
 return out
}
const cfg=JSON.parse(docs[2].content),corpora=docs.slice(4).map(d=>JSON.parse(d.content));
const {R,I,labels}=load(docs);
const assets=[{id:"L",sha:"be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb"},{id:"S",sha:"05c239f3f3b1f46235fa2464d2945c21c6c08132"}];
console.log(JSON.stringify(experiment(R,I,labels,cfg,cards,corpora,assets),null,2));
```
## 实测
```json
{
  "episodes": 32,
  "turns": 64,
  "annotatedLinks": 12,
  "uniqueLinks": 12,
  "retired": 9,
  "conditional": 1,
  "scopeChange": 1,
  "permissionIntent": 1,
  "privacyHold": 1,
  "unresolvedEdit": 0,
  "naiveGlobalRetractions": 3,
  "guardedQueries": 62,
  "retiredSpanChecks": 12,
  "activeSpanChecks": 262,
  "rankChanged": 21,
  "controls": 9,
  "metrics": {
    "raw": {
      "positive": 56,
      "negative": 8,
      "hit1": 21,
      "hit3": 41,
      "recalled": 47,
      "relevant": 90,
      "negativeNonempty": 7,
      "nonempty": 63,
      "recall": 0.5222222222222223
    },
    "spanOnly": {
      "positive": 56,
      "negative": 8,
      "hit1": 21,
      "hit3": 39,
      "recalled": 48,
      "relevant": 90,
      "negativeNonempty": 6,
      "nonempty": 61,
      "recall": 0.5333333333333333
    },
    "editAware": {
      "positive": 56,
      "negative": 8,
      "hit1": 21,
      "hit3": 39,
      "recalled": 48,
      "relevant": 90,
      "negativeNonempty": 6,
      "nonempty": 60,
      "recall": 0.5333333333333333
    },
    "guarded": {
      "positive": 56,
      "negative": 8,
      "hit1": 21,
      "hit3": 38,
      "recalled": 47,
      "relevant": 90,
      "negativeNonempty": 6,
      "nonempty": 60,
      "recall": 0.5222222222222223
    }
  }
}
```
逐轮记录身份和主题排名：
```json
[{"id":"L01","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L01.1.1","L01.1.2","L01.1.3","L01.1.4"],"ranks":{"raw":["feasibility","regret","allocation"],"spanOnly":["feasibility","regret","allocation"],"editAware":["feasibility","regret","allocation"],"guarded":["feasibility","regret","allocation"]}},{"id":"L01","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["L01.1.1","L01.1.2","L01.1.3","L01.1.4","L01.2.1"],"ranks":{"raw":["feasibility","regret","allocation"],"spanOnly":["feasibility","regret","allocation"],"editAware":["feasibility","regret","allocation"],"guarded":["feasibility","regret","allocation"]}},{"id":"L02","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L02.1.1","L02.1.2","L02.1.3","L02.1.4"],"ranks":{"raw":["regret","feasibility","timing"],"spanOnly":["regret","feasibility","timing"],"editAware":["regret","feasibility","timing"],"guarded":["regret","feasibility","timing"]}},{"id":"L02","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["L02.1.1","L02.1.2","L02.1.3","L02.1.4","L02.2.1","L02.2.2"],"ranks":{"raw":["timing","regret","causal"],"spanOnly":["timing","regret","information"],"editAware":["timing","regret","information"],"guarded":["timing","regret","information"]}},{"id":"L03","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L03.1.1","L03.1.2","L03.1.3","L03.1.4"],"ranks":{"raw":["feasibility","allocation","causal"],"spanOnly":["feasibility","allocation","causal"],"editAware":["feasibility","allocation","causal"],"guarded":["feasibility","allocation","causal"]}},{"id":"L03","turn":2,"retired":["L03.1.2"],"uncertain":[],"hold":false,"active":["L03.1.1","L03.1.3","L03.1.4","L03.2.1"],"ranks":{"raw":["feasibility","allocation","causal"],"spanOnly":["feasibility","allocation","causal"],"editAware":["feasibility","allocation","causal"],"guarded":["feasibility","allocation","causal"]}},{"id":"L04","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L04.1.1","L04.1.2","L04.1.3","L04.1.4"],"ranks":{"raw":["timing","multiobjective","causal"],"spanOnly":["timing","multiobjective","causal"],"editAware":["timing","multiobjective","causal"],"guarded":["timing","multiobjective","causal"]}},{"id":"L04","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["L04.1.1","L04.1.2","L04.1.3","L04.1.4","L04.2.1","L04.2.2"],"ranks":{"raw":["timing","regret","measurement"],"spanOnly":["timing","regret","measurement"],"editAware":["timing","regret","measurement"],"guarded":["timing","regret","measurement"]}},{"id":"L05","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L05.1.1","L05.1.2","L05.1.3"],"ranks":{"raw":["regret","feasibility","multiobjective"],"spanOnly":["regret","feasibility","multiobjective"],"editAware":["regret","feasibility","multiobjective"],"guarded":["regret","feasibility","multiobjective"]}},{"id":"L05","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["L05.1.1","L05.1.2","L05.1.3","L05.2.1","L05.2.2"],"ranks":{"raw":["timing","multiobjective","causal"],"spanOnly":["feasibility","regret","allocation"],"editAware":["feasibility","regret","allocation"],"guarded":["feasibility","regret","allocation"]}},{"id":"L06","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L06.1.1","L06.1.2","L06.1.3"],"ranks":{"raw":["causal","information","regret"],"spanOnly":["causal","information","regret"],"editAware":["causal","information","regret"],"guarded":["causal","information","regret"]}},{"id":"L06","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["L06.1.1","L06.1.2","L06.1.3","L06.2.1","L06.2.2"],"ranks":{"raw":["timing","causal","information"],"spanOnly":["causal","information","regret"],"editAware":["causal","information","regret"],"guarded":["causal","information","regret"]}},{"id":"L07","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L07.1.1","L07.1.2","L07.1.3"],"ranks":{"raw":["causal","feasibility","multiobjective"],"spanOnly":["causal","feasibility","multiobjective"],"editAware":["causal","feasibility","multiobjective"],"guarded":["causal","feasibility","multiobjective"]}},{"id":"L07","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["L07.1.1","L07.1.2","L07.1.3","L07.2.1","L07.2.2"],"ranks":{"raw":["causal","measurement","feasibility"],"spanOnly":["causal","feasibility","measurement"],"editAware":["causal","feasibility","measurement"],"guarded":["causal","feasibility","measurement"]}},{"id":"L08","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L08.1.1","L08.1.2","L08.1.3"],"ranks":{"raw":["regret","feasibility","allocation"],"spanOnly":["regret","feasibility","allocation"],"editAware":["regret","feasibility","allocation"],"guarded":["regret","feasibility","allocation"]}},{"id":"L08","turn":2,"retired":["L08.1.2","L08.2.2"],"uncertain":[],"hold":false,"active":["L08.1.1","L08.1.3","L08.2.1"],"ranks":{"raw":["regret","causal","feasibility"],"spanOnly":["regret","causal","feasibility"],"editAware":["regret","feasibility","allocation"],"guarded":["regret","feasibility","allocation"]}},{"id":"L09","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L09.1.1","L09.1.2"],"ranks":{"raw":[],"spanOnly":["regret","timing","allocation"],"editAware":["regret","timing","allocation"],"guarded":["regret","timing","allocation"]}},{"id":"L09","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["L09.1.1","L09.1.2","L09.2.1","L09.2.2","L09.2.3"],"ranks":{"raw":["multiobjective","information","causal"],"spanOnly":["regret","timing","allocation"],"editAware":["regret","timing","allocation"],"guarded":["regret","timing","allocation"]}},{"id":"L10","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L10.1.1","L10.1.2","L10.1.3","L10.1.4"],"ranks":{"raw":["regret","causal","feasibility"],"spanOnly":["regret","feasibility","multiobjective"],"editAware":["regret","feasibility","multiobjective"],"guarded":["regret","feasibility","multiobjective"]}},{"id":"L10","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["L10.1.1","L10.1.2","L10.1.3","L10.1.4","L10.2.1"],"ranks":{"raw":["regret","causal","feasibility"],"spanOnly":["regret","feasibility","multiobjective"],"editAware":["regret","feasibility","multiobjective"],"guarded":["regret","feasibility","multiobjective"]}},{"id":"L11","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L11.1.1","L11.1.2","L11.1.3","L11.1.4"],"ranks":{"raw":["feasibility","causal","allocation"],"spanOnly":["feasibility","allocation","causal"],"editAware":["feasibility","allocation","causal"],"guarded":["feasibility","allocation","causal"]}},{"id":"L11","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["L11.1.1","L11.1.2","L11.1.3","L11.1.4","L11.2.1","L11.2.2"],"ranks":{"raw":["feasibility","causal","allocation"],"spanOnly":["feasibility","allocation","causal"],"editAware":["feasibility","allocation","causal"],"guarded":["feasibility","allocation","causal"]}},{"id":"L12","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L12.1.1","L12.1.2","L12.1.3","L12.1.4"],"ranks":{"raw":["feasibility","allocation","regret"],"spanOnly":["feasibility","allocation","regret"],"editAware":["feasibility","allocation","regret"],"guarded":["feasibility","allocation","regret"]}},{"id":"L12","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["L12.1.1","L12.1.2","L12.1.3","L12.1.4","L12.2.1","L12.2.2"],"ranks":{"raw":["feasibility","allocation","regret"],"spanOnly":["feasibility","allocation","regret"],"editAware":["feasibility","allocation","regret"],"guarded":["feasibility","allocation","regret"]}},{"id":"L13","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L13.1.1","L13.1.2","L13.1.3","L13.1.4"],"ranks":{"raw":["feasibility","allocation","causal"],"spanOnly":["feasibility","allocation","causal"],"editAware":["feasibility","allocation","causal"],"guarded":["feasibility","allocation","causal"]}},{"id":"L13","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["L13.1.1","L13.1.2","L13.1.3","L13.1.4","L13.2.1","L13.2.2"],"ranks":{"raw":["timing","feasibility","allocation"],"spanOnly":["timing","feasibility","allocation"],"editAware":["timing","feasibility","allocation"],"guarded":["timing","feasibility","allocation"]}},{"id":"L14","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L14.1.1","L14.1.2","L14.1.3"],"ranks":{"raw":["allocation","regret","feasibility"],"spanOnly":[],"editAware":[],"guarded":[]}},{"id":"L14","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["L14.1.1","L14.1.2","L14.1.3","L14.2.1","L14.2.2"],"ranks":{"raw":["timing","regret","information"],"spanOnly":["timing","regret","information"],"editAware":["timing","regret","information"],"guarded":["timing","regret","information"]}},{"id":"L15","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L15.1.1","L15.1.2","L15.1.3","L15.1.4"],"ranks":{"raw":["regret","multiobjective","causal"],"spanOnly":["feasibility","causal","allocation"],"editAware":["feasibility","causal","allocation"],"guarded":["feasibility","causal","allocation"]}},{"id":"L15","turn":2,"retired":["L15.1.1"],"uncertain":[],"hold":false,"active":["L15.1.2","L15.1.3","L15.1.4","L15.2.1","L15.2.2"],"ranks":{"raw":["regret","multiobjective","causal"],"spanOnly":["regret","multiobjective","timing"],"editAware":["regret","multiobjective","timing"],"guarded":["regret","multiobjective","timing"]}},{"id":"L16","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L16.1.1","L16.1.2","L16.1.3","L16.1.4"],"ranks":{"raw":["regret","multiobjective","feasibility"],"spanOnly":["regret","multiobjective","feasibility"],"editAware":["regret","multiobjective","feasibility"],"guarded":["regret","multiobjective","feasibility"]}},{"id":"L16","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["L16.1.1","L16.1.2","L16.1.3","L16.1.4","L16.2.1","L16.2.2"],"ranks":{"raw":["regret","multiobjective","feasibility"],"spanOnly":["regret","multiobjective","feasibility"],"editAware":["regret","multiobjective","feasibility"],"guarded":["regret","multiobjective","feasibility"]}},{"id":"L17","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L17.1.1","L17.1.2","L17.1.3"],"ranks":{"raw":["feasibility","multiobjective","causal"],"spanOnly":["feasibility","multiobjective","causal"],"editAware":["feasibility","multiobjective","causal"],"guarded":["feasibility","multiobjective","causal"]}},{"id":"L17","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["L17.1.1","L17.1.2","L17.1.3","L17.2.1","L17.2.2","L17.2.3"],"ranks":{"raw":["causal","multiobjective","feasibility"],"spanOnly":["causal","multiobjective","feasibility"],"editAware":["causal","multiobjective","feasibility"],"guarded":["causal","multiobjective","feasibility"]}},{"id":"L18","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["L18.1.1","L18.1.2"],"ranks":{"raw":["feasibility","regret","allocation"],"spanOnly":["feasibility","regret","allocation"],"editAware":["feasibility","regret","allocation"],"guarded":["feasibility","regret","allocation"]}},{"id":"L18","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["L18.1.1","L18.1.2","L18.2.1","L18.2.2","L18.2.3"],"ranks":{"raw":["feasibility","measurement","regret"],"spanOnly":["feasibility","regret","allocation"],"editAware":["feasibility","regret","allocation"],"guarded":["feasibility","regret","allocation"]}},{"id":"S01","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["S01.1.1","S01.1.2","S01.1.3","S01.1.4"],"ranks":{"raw":["regret","feasibility","information"],"spanOnly":["regret","feasibility","multiobjective"],"editAware":["regret","feasibility","multiobjective"],"guarded":["regret","feasibility","multiobjective"]}},{"id":"S01","turn":2,"retired":["S01.1.2","S01.2.1"],"uncertain":[],"hold":false,"active":["S01.1.1","S01.1.3","S01.1.4","S01.2.2"],"ranks":{"raw":["regret","feasibility","information"],"spanOnly":["regret","feasibility","multiobjective"],"editAware":["regret","feasibility","multiobjective"],"guarded":["regret","feasibility","multiobjective"]}},{"id":"S02","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["S02.1.1","S02.1.2","S02.1.3"],"ranks":{"raw":["feasibility","regret","allocation"],"spanOnly":["timing","multiobjective","causal"],"editAware":["timing","multiobjective","causal"],"guarded":["timing","multiobjective","causal"]}},{"id":"S02","turn":2,"retired":["S02.1.3"],"uncertain":[],"hold":false,"active":["S02.1.1","S02.1.2","S02.2.1"],"ranks":{"raw":["feasibility","regret","allocation"],"spanOnly":["timing","multiobjective","causal"],"editAware":[],"guarded":[]}},{"id":"S03","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["S03.1.1","S03.1.2","S03.1.3"],"ranks":{"raw":["measurement","multiobjective","causal"],"spanOnly":["measurement","multiobjective","causal"],"editAware":["measurement","multiobjective","causal"],"guarded":["measurement","multiobjective","causal"]}},{"id":"S03","turn":2,"retired":[],"uncertain":["S03.1.3","S03.2.1"],"hold":false,"active":["S03.1.1","S03.1.2","S03.1.3"],"ranks":{"raw":["measurement","multiobjective","causal"],"spanOnly":["measurement","multiobjective","causal"],"editAware":["measurement","multiobjective","causal"],"guarded":["measurement","multiobjective","causal"]}},{"id":"S04","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["S04.1.1","S04.1.2","S04.1.3","S04.1.4"],"ranks":{"raw":["regret","multiobjective","feasibility"],"spanOnly":["regret","multiobjective","feasibility"],"editAware":["regret","multiobjective","feasibility"],"guarded":["regret","multiobjective","feasibility"]}},{"id":"S04","turn":2,"retired":["S04.1.4"],"uncertain":[],"hold":false,"active":["S04.1.1","S04.1.2","S04.1.3","S04.2.1"],"ranks":{"raw":["regret","timing","multiobjective"],"spanOnly":["regret","timing","multiobjective"],"editAware":["timing","causal","multiobjective"],"guarded":["timing","causal","multiobjective"]}},{"id":"S05","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["S05.1.1","S05.1.2","S05.1.3"],"ranks":{"raw":["feasibility","timing","allocation"],"spanOnly":["feasibility","timing","allocation"],"editAware":["feasibility","timing","allocation"],"guarded":["feasibility","timing","allocation"]}},{"id":"S05","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["S05.1.1","S05.1.2","S05.1.3","S05.2.1"],"ranks":{"raw":["feasibility","timing","causal"],"spanOnly":["feasibility","timing","causal"],"editAware":["feasibility","timing","causal"],"guarded":["feasibility","timing","causal"]}},{"id":"S06","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["S06.1.1","S06.1.2"],"ranks":{"raw":["measurement","multiobjective","timing"],"spanOnly":["regret","measurement","timing"],"editAware":["regret","measurement","timing"],"guarded":["regret","measurement","timing"]}},{"id":"S06","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["S06.1.1","S06.1.2","S06.2.1","S06.2.2"],"ranks":{"raw":["measurement","multiobjective","timing"],"spanOnly":["regret","measurement","timing"],"editAware":["regret","measurement","timing"],"guarded":["regret","measurement","timing"]}},{"id":"S07","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["S07.1.1","S07.1.2","S07.1.3"],"ranks":{"raw":["regret","multiobjective","causal"],"spanOnly":["causal","feasibility","allocation"],"editAware":["causal","feasibility","allocation"],"guarded":["causal","feasibility","allocation"]}},{"id":"S07","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["S07.1.1","S07.1.2","S07.1.3","S07.2.1","S07.2.2"],"ranks":{"raw":["multiobjective","causal","timing"],"spanOnly":["multiobjective","timing","measurement"],"editAware":["multiobjective","timing","measurement"],"guarded":["multiobjective","timing","measurement"]}},{"id":"S08","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["S08.1.1","S08.1.2","S08.1.3"],"ranks":{"raw":["causal","feasibility","allocation"],"spanOnly":["causal","feasibility","allocation"],"editAware":["causal","feasibility","allocation"],"guarded":["causal","feasibility","allocation"]}},{"id":"S08","turn":2,"retired":["S08.1.2"],"uncertain":[],"hold":false,"active":["S08.1.1","S08.1.3","S08.2.1"],"ranks":{"raw":["causal","feasibility","timing"],"spanOnly":["causal","feasibility","allocation"],"editAware":["causal","feasibility","allocation"],"guarded":["causal","feasibility","allocation"]}},{"id":"S09","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["S09.1.1","S09.1.2","S09.1.3","S09.1.4"],"ranks":{"raw":["regret","multiobjective","timing"],"spanOnly":["multiobjective","timing","causal"],"editAware":["multiobjective","timing","causal"],"guarded":["multiobjective","timing","causal"]}},{"id":"S09","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["S09.1.1","S09.1.2","S09.1.3","S09.1.4","S09.2.1"],"ranks":{"raw":["multiobjective","regret","timing"],"spanOnly":["allocation","multiobjective","regret"],"editAware":["allocation","multiobjective","regret"],"guarded":["allocation","multiobjective","regret"]}},{"id":"S10","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["S10.1.1","S10.1.2","S10.1.3","S10.1.4"],"ranks":{"raw":["feasibility","regret","multiobjective"],"spanOnly":["feasibility","regret","multiobjective"],"editAware":["feasibility","regret","multiobjective"],"guarded":["feasibility","regret","multiobjective"]}},{"id":"S10","turn":2,"retired":["S10.1.2","S10.2.1"],"uncertain":[],"hold":false,"active":["S10.1.1","S10.1.3","S10.1.4","S10.2.2"],"ranks":{"raw":["multiobjective","measurement","feasibility"],"spanOnly":["multiobjective","measurement","feasibility"],"editAware":["feasibility","regret","multiobjective"],"guarded":["feasibility","regret","multiobjective"]}},{"id":"S11","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["S11.1.1","S11.1.2","S11.1.3"],"ranks":{"raw":["timing","regret","allocation"],"spanOnly":[],"editAware":[],"guarded":[]}},{"id":"S11","turn":2,"retired":[],"uncertain":["S11.1.1","S11.2.1"],"hold":true,"active":["S11.1.1","S11.1.2","S11.1.3","S11.2.2"],"ranks":{"raw":["measurement","timing","information"],"spanOnly":[],"editAware":[],"guarded":[]}},{"id":"S12","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["S12.1.1","S12.1.2","S12.1.3","S12.1.4","S12.1.5"],"ranks":{"raw":["regret","feasibility","allocation"],"spanOnly":["timing","information","multiobjective"],"editAware":["timing","information","multiobjective"],"guarded":["timing","information","multiobjective"]}},{"id":"S12","turn":2,"retired":["S12.1.2"],"uncertain":[],"hold":false,"active":["S12.1.1","S12.1.3","S12.1.4","S12.1.5","S12.2.1","S12.2.2"],"ranks":{"raw":["regret","feasibility","timing"],"spanOnly":["timing","information","multiobjective"],"editAware":["timing","information","multiobjective"],"guarded":["timing","information","multiobjective"]}},{"id":"S13","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["S13.1.1","S13.1.2","S13.1.3"],"ranks":{"raw":["timing","information","multiobjective"],"spanOnly":["timing","information","multiobjective"],"editAware":["timing","information","multiobjective"],"guarded":["timing","information","multiobjective"]}},{"id":"S13","turn":2,"retired":[],"uncertain":["S13.1.3","S13.2.1"],"hold":false,"active":["S13.1.1","S13.1.2","S13.1.3","S13.2.2"],"ranks":{"raw":["timing","information","multiobjective"],"spanOnly":["timing","information","multiobjective"],"editAware":["timing","information","multiobjective"],"guarded":["timing","information","measurement"]}},{"id":"S14","turn":1,"retired":[],"uncertain":[],"hold":false,"active":["S14.1.1","S14.1.2","S14.1.3","S14.1.4"],"ranks":{"raw":["regret","timing","information"],"spanOnly":["regret","timing","information"],"editAware":["regret","timing","information"],"guarded":["regret","timing","information"]}},{"id":"S14","turn":2,"retired":[],"uncertain":[],"hold":false,"active":["S14.1.1","S14.1.2","S14.1.3","S14.1.4","S14.2.1"],"ranks":{"raw":["allocation","causal","timing"],"spanOnly":["allocation","causal","timing"],"editAware":["allocation","causal","timing"],"guarded":["allocation","causal","timing"]}}]
```
下一责任：继续研究真实原文候选对编辑/条件/主体的识别，要求独立未见数据并保留未知；不能用本oracle实验声称自主语义能力。产品轨维护唯一交接，正式版本另获授权。
