# 自主认知专项累计第114轮候选：稳定语义对象的字段修订及来源依赖
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / ORACLE_FIELD_MAPPING / PUBLIC_SYNTHETIC_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main ef78d7eb10e5bd64fc079fd0b836308f62761371。核对近12提交、13开放PR（#61待审）、v3.2前15行及历史全文、唯一交接前18行、R113前20行、R2 README全文、R64前17行、R62前20行及比较代码、两语料12条实际修订原始标注。R64已有有限中文解析和稳定约束版本；R113暴露新语句替换导致语义丢失；本轮增加逐字段原文来源、精确更新、父版本拒绝与继承来源撤回，并实际调用R73/R28代码。未重做R64规则、训练或R113全语料实验。
## 固定资产
research/decision_hub/2026-11-25-unified-semantic-annotation-bridge.md af648d16ee96b9af4a3efb61b413d113208bb0ca
research/decision_hub/2026-11-25-annotation-conditioned-context-retrieval-ablation.md 884f6c938c9cc50f69da6a1b1b896e1eb7621487
research/decision_hub/2026-11-24-content-method-retrieval/config.json ff838223473dd27aed6865ccaa0971b90ded17c7
research/decision_hub/2026-11-24-content-method-retrieval/probe.js 7d78f8c89ac73a2228ddca40dd45ad8b02366554
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
research/decision_methods/C028_INTERVAL_HARD_CONSTRAINT_FEASIBILITY_2026-11-20.md 7cb8d5e3631dd17c0650cec06139d88b5bfcc700
research/decision_methods/C028_MANSKI_1990_UNOBSERVED_ALTERNATIVES_BOUNDS_2026-11-20.md a221a3a1e95ca3262a3574ab7685890f5f50d6d5
research/decision_methods/C004_DYNAMIC_UTILITY_MULTI_OBJECTIVE_ROBUST_2026-10-27.md 0d04c633a26437ad6017946cd528c4dc68db3d83
research/decision_methods/C029_SCENARIO_MINIMAX_REGRET_INFORMATION_BOUNDARY_2026-11-20.md a2588cfdd47e547a46a7ee8cde2644caf81198d9
research/decision_methods/VOI_IMPERFECT_BINARY_SIGNAL_METHOD_CARD_2026-11-20.md bd494e2e1200a526dcb11d454e423ff9aebccd33
research/decision_methods/C009_OPTION_VALUE_INFORMATION_REVERSIBILITY_2026-11-01.md 5048081b0a277f4bc511aff2293020268fd5c57c
research/decision_methods/C035_BLEICHRODT_PINTO_WAKKER_2001_ELICITATION_CORRECTION_BOUNDARIES_2026-11-20.md 40d77d89356e7f3d3c8e02e3a93fd6f634ec09d2
research/decision_methods/C036_TWO_STAGE_ADJUSTABLE_FEASIBILITY_QUANTIFIER_BOUNDARY_2026-11-23.md d2438afcc93f8568cb3a0ef00285fa2f66b34f23
R2 README 801d48d62a05659d3afedf1f56a555afa12c5236；R64 da54c5b88ed0f19f5c5d272230a1959b811f5b5e；R62 ada3d84a46e4d9a411ebf762884d13a5c5e87686；唯一交接 5e74f4f0b37141d631740e844ad8bbbfed232e07。实际获取8卡正文及连接器blob，匹配历史配置；未独立核验字节、重审论文、许可或新增科学准入。
## 合同
从S语料12条跨轮编辑中的5个replace场景S02/04/08/12/13（全12条含L/S，选择5项S replace，其中均有唯一引用）手工建立有限属性映射，逐字段绑定当前或旧整轮原文唯一UTF16跨度。手工概念、数值及作用域由研究者从原文提供，属oracle，不是自主解析。允许字段清单由夹具独立设定，示例函数参数p.allowedKeys模拟可信宿主输入，不能来自非可信候选；本轮无真实鉴权、可靠签发、全schema、事件持久化、并发CAS或真正防重放。只在父版本、根、可信确认及允许标记匹配时创建新版本；未变字段逐项保留旧来源，变更及新增字段绑定新原文。父对象留存仅合成实验，未实现真实擦除或历史权限。当前资格采用全部字段来源获准的保守合同；旧值失效与旧整轮来源撤回区别：旧整轮包含仍有效的指标、比较符或作用域，撤回时新对象也必须停止用于检索。旧值不再作为当前阈值，依赖保留不会将旧值重新作为事实。未实现字段级独立授权、替代来源、跨设备、真实删除或完整未知传播。S12单位未明确，保持未提供，禁止据此调用金额模型；S13仅正式交付适用，试验不适用、其他阶段未知。S02以原文人工确定到车站步行分钟和上限，不宣称已自动解析中文数字。S04当前数量及S08当前修订结果为用户报告，非外部事实。例中的数学检查是直接有限点值逻辑，未调用原生C028或R62 compare。其他7条修订含条件取消、许可撤回、类别变化及撤回，沿R113保留研究边界，本轮未实现其统一修订。所有authority NONE。
## 实验
R73 build/verify实际转换全S语料并核对固定原标注，随后5例唯一引用。每字段继承/变更、原文切片、历史冻结、六种拒绝（未确认、无许可、错根、旧父、额外字段、重复提交）及三个来源缺失条件。字段正确性以人工给定映射核对，同研究者自测，不是独立验收。S02测5点与旧阈值差异，S13测3阶段×3点，不构造概率或真实建议。检索部分调用R28 BM25及R112历史扩展方法，在5例比较原文、只留最新片段（其他标注片段保持）、逐字段组合（其他标注片段保持）。不同于R113精确顺序与完整集合，replace是本轮针对单编辑诊断，不将其数值视为复现R113排名。逐字段组合只用于检索线索，原文片段顺序、重叠及语法可能不完整，缺失语义仍未知；没有将标签或方法名作为扩展输入。其他未变片段在源撤回时同样须隔离；本轮仅在全源许可时进行检索，不提供撤回后的实际检索器接口。不以5个手工例断言总体准确率改善，保留排名退步和空结果。未实现自动理解、真实权限、原生模型、设备性能或独立效果。全部合成开发资料为ChatGPT研发辅助原创，非真人、训练或独立留出。无新增费用、训练、Codex、CI、生产修改、PR合并、部署或冻结变化。
## 复算
按上述五份文件顺序置于docs[i].content，按cfg.docs中每组首项读取8份自有档案正文，置入cards（保留元数据及body）。仅加载已审查自有代码，不执行任意外部文档。Node标准JS。
```js
function load(docs){
 const src=docs[3].content;
 const R=Function(src.slice(src.indexOf("function toks("),src.indexOf("function run("))+"\nreturn {rank};")();
 const ir=docs[0].content.split("```js\n")[1].split("\n```")[0].split(" const out={datasets:")[0];
 const I=Function(ir+"\nreturn {build,verify};\n}\nreturn experiment();")();
 return {R,I}
}
const cases=[{"id":"S02","old":"S02.1.3","edit":"S02.2.1","initial":{"metric":["station_walking_time","离车站步行"],"role":["hard","必须"],"relation":["<=","以内"],"value":[15,"十五"],"unit":["min","分钟"],"scope":["all_options","任何一套"]},"patch":{"value":[12,"十二"]}},{"id":"S04","old":"S04.1.4","edit":"S04.2.1","initial":{"metric":["free_outlets","空插座"],"value":[1,"一个"],"modality":["reported","家里只有"]},"patch":{"value":[2,"两个"],"modality":["reported","刚核实"]}},{"id":"S08","old":"S08.1.2","edit":"S08.2.1","initial":{"metric":["late_days","迟到"],"value":[3,"三天"],"unit":["day","天"],"period":["last_month","上个月"],"modality":["observation","实际"]},"patch":{"value":[2,"两天"],"modality":["observation","实际"]}},{"id":"S12","old":"S12.1.2","edit":"S12.2.1","initial":{"metric":["repair_cost","修旧相机"],"value":[500,"五百"],"modality":["approximate","大约"]},"patch":{"value":[700,"七百"],"modality":["reported_quote","维修店说"],"evidenceLimit":["no_written_quote","还没有书面报价"]}},{"id":"S13","old":"S13.1.3","edit":"S13.2.1","initial":{"metric":["accuracy","准确率必须"],"role":["hard","必须"],"relation":[">=","不低于"],"value":[90,"九成"],"unit":["percent","九成"]},"patch":{"scope":["formal_delivery","正式交付"],"exclusion":["trial","试验阶段不套用这个底线"]}}];
function experiment(R,I,cfg,cards,corpus,asset,cases){
 const ck=(x,m)=>{if(!x)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),clone=x=>JSON.parse(JSON.stringify(x));
 const ir=I.build(corpus,asset);ck(I.verify(ir,corpus,asset),"IR");
 const hist=cfg.queries.map(q=>({path:q.id,group:q.id,body:q.zh,expanded:q.expanded}));
 function retrieve(q){if(!q)return [];let n=R.rank(hist,q,"body")[0],e=n?hist.find(x=>x.path===n.path).expanded:"";return R.rank(cards,q+(e?" "+e:""),"body").slice(0,3).map(x=>x.group)}
 function fields(mapping,turn,source){return Object.fromEntries(Object.entries(mapping).map(([k,[value,quote]])=>{
  let start=turn.text.indexOf(quote);ck(start>=0&&start===turn.text.lastIndexOf(quote),"span "+source+" "+quote);
  return [k,{value,source,start,end:start+quote.length,quote}]
 }))}
 function revise(state,p,confirmed,expected,allowed){
  if(!confirmed||!allowed||p.root!==state.root||p.parent!==state.version||p.parent!==expected)return null;
  if(Object.keys(p.fields).some(k=>!p.allowedKeys.includes(k)))return null;
  return {root:state.root,version:p.id,parent:state.version,fields:{...clone(state.fields),...clone(p.fields)},authority:"NONE"}
 }
 function view(state,sources){
  let f=state.fields,missing=Object.keys(f).filter(k=>!sources.has(f[k].source));
  return {status:missing.length?"UNKNOWN_SOURCE":"RESEARCH_ONLY",missing,query:missing.length?"":Object.values(f).map(x=>x.quote).join("。"),authority:"NONE"}
 }
 let out={cases:0,fields:0,inherited:0,updatedOrAdded:0,sourceChecks:0,oldUnchanged:0,rejectedEdits:0,withdrawalChecks:0,mathChecks:0,staleThresholdDifferences:0,controls:0,rows:[]};
 for(let c of cases){
  const e=ir.episodes.find(x=>x.meta.id===c.id),[a,b]=e.turns,old=a.items.find(x=>x.id===c.old),edit=b.items.find(x=>x.id===c.edit);
  ck(edit.reference.status==="UNIQUE_CANDIDATE"&&edit.reference.candidates[0]===old.id&&edit.dimensions.edit.value==="replace","actual reference");
  const id1=c.id+":turn1",id2=c.id+":turn2";
  const s={root:old.id,version:old.id,parent:null,fields:fields(c.initial,a,id1),authority:"NONE"},before=JSON.stringify(s);
  const patch={root:s.root,parent:s.version,id:edit.id,fields:fields(c.patch,b,id2),allowedKeys:Object.keys(c.patch)};
  const v=revise(s,patch,true,s.version,true);ck(v&&v.root===s.root&&v.parent===s.version,"identity");out.cases++;
  for(let [k,f] of Object.entries(v.fields)){
   let expected=Object.hasOwn(patch.fields,k)?patch.fields[k]:s.fields[k];ck(eq(f,expected),"exact update");out.fields++;
   if(Object.hasOwn(patch.fields,k))out.updatedOrAdded++;else out.inherited++;
   let t=f.source===id1?a:b;ck(t.text.slice(f.start,f.end)===f.quote,"field origin");out.sourceChecks++;
  }
  ck(JSON.stringify(s)===before,"history");out.oldUnchanged++;
  for(let args of [[s,patch,false,s.version,true],[s,patch,true,s.version,false],[s,{...patch,root:"other"},true,s.version,true],[s,{...patch,parent:"stale"},true,s.version,true],[s,{...patch,fields:{...patch.fields,unapproved:{value:1}}},true,s.version,true],[v,patch,true,v.version,true]]){ck(revise(...args)===null,"reject");out.rejectedEdits++}
  let all=new Set([id1,id2]),q=view(v,all);ck(q.status==="RESEARCH_ONLY","full");
  for(let set of [new Set(),new Set([id1]),new Set([id2])]){let z=view(v,set),missing=Object.keys(v.fields).filter(k=>!set.has(v.fields[k].source));ck(z.status==="UNKNOWN_SOURCE"&&eq(z.missing,missing)&&z.query==="","withdrawal");out.withdrawalChecks++}
  // Diagnostic query uses exact source fragments, never the old threshold;
  // it is not a full natural-language reconstruction or numeric truth.
  let other=[...a.items.filter(x=>x.id!==old.id),...b.items.filter(x=>x.id!==edit.id)].map(x=>x.span.text).join("。");
  const raw=retrieve(a.text+"。"+b.text),replace=retrieve(other+"。"+edit.span.text),composed=retrieve(other+"。"+q.query);
  out.rows.push({id:c.id,root:v.root,parent:v.parent,version:v.version,fields:v.fields,raw,replace,composed,query:q.query});
  if(c.id==="S02"){
   ck(v.fields.value.value===12&&v.fields.unit.value==="min"&&v.fields.role.value==="hard"&&v.fields.scope.value==="all_options","walk");
   for(let n of [11,12,13,15,16]){
    const current=n<=v.fields.value.value,expected=n<=12,stale=n<=s.fields.value.value;
    ck(current===expected,"walk math");out.mathChecks++;out.staleThresholdDifferences+=+(stale!==current)
   }
  }
  if(c.id==="S13"){
   ck(v.fields.value.value===90&&v.fields.scope.value==="formal_delivery"&&v.fields.exclusion.value==="trial","scope");
   for(let stage of ["formal_delivery","trial","unknown"])for(let n of [89,90,91]){
    const actual=stage===v.fields.scope.value?(n>=v.fields.value.value?"PASS":"FAIL"):stage===v.fields.exclusion.value?"NOT_APPLICABLE":"UNKNOWN";
    const expected=stage==="trial"?"NOT_APPLICABLE":stage==="unknown"?"UNKNOWN":n>=90?"PASS":"FAIL";
    ck(actual===expected,"scope math");out.mathChecks++;
   }
  }
 }
 for(let t of [()=>out.cases===5,()=>out.fields===out.inherited+out.updatedOrAdded,()=>out.sourceChecks===out.fields,()=>out.rejectedEdits===30,()=>out.withdrawalChecks===15,()=>out.mathChecks===14,()=>out.staleThresholdDifferences===2,()=>out.rows.find(r=>r.id==="S02").query.includes("离车站步行"),()=>!out.rows.find(r=>r.id==="S02").query.includes("十五"),()=>!Object.hasOwn(out.rows.find(r=>r.id==="S12").fields,"unit")]){ck(t(),"control");out.controls++}
 return out
}
const cfg=JSON.parse(docs[2].content),corpus=JSON.parse(docs[4].content);
const {R,I}=load(docs);
console.log(JSON.stringify(experiment(R,I,cfg,cards,corpus,{id:"S",sha:"05c239f3f3b1f46235fa2464d2945c21c6c08132"},cases),null,2));
```
## 实测
```json
{
  "cases": 5,
  "fields": 25,
  "inherited": 15,
  "updatedOrAdded": 10,
  "sourceChecks": 25,
  "oldUnchanged": 5,
  "rejectedEdits": 30,
  "withdrawalChecks": 15,
  "mathChecks": 14,
  "staleThresholdDifferences": 2,
  "controls": 10,
  "rows": [
    {
      "id": "S02",
      "root": "S02.1.3",
      "parent": "S02.1.3",
      "version": "S02.2.1",
      "fields": {
        "metric": {
          "value": "station_walking_time",
          "source": "S02:turn1",
          "start": 18,
          "end": 23,
          "quote": "离车站步行"
        },
        "role": {
          "value": "hard",
          "source": "S02:turn1",
          "start": 16,
          "end": 18,
          "quote": "必须"
        },
        "relation": {
          "value": "<=",
          "source": "S02:turn1",
          "start": 27,
          "end": 29,
          "quote": "以内"
        },
        "value": {
          "value": 12,
          "source": "S02:turn2",
          "start": 6,
          "end": 8,
          "quote": "十二"
        },
        "unit": {
          "value": "min",
          "source": "S02:turn1",
          "start": 25,
          "end": 27,
          "quote": "分钟"
        },
        "scope": {
          "value": "all_options",
          "source": "S02:turn1",
          "start": 11,
          "end": 15,
          "quote": "任何一套"
        }
      },
      "raw": [
        "feasibility",
        "regret",
        "allocation"
      ],
      "replace": [],
      "composed": [
        "feasibility",
        "regret",
        "allocation"
      ],
      "query": "离车站步行。必须。以内。十二。分钟。任何一套"
    },
    {
      "id": "S04",
      "root": "S04.1.4",
      "parent": "S04.1.4",
      "version": "S04.2.1",
      "fields": {
        "metric": {
          "value": "free_outlets",
          "source": "S04:turn1",
          "start": 30,
          "end": 33,
          "quote": "空插座"
        },
        "value": {
          "value": 2,
          "source": "S04:turn2",
          "start": 8,
          "end": 10,
          "quote": "两个"
        },
        "modality": {
          "value": "reported",
          "source": "S04:turn2",
          "start": 4,
          "end": 7,
          "quote": "刚核实"
        }
      },
      "raw": [
        "regret",
        "timing",
        "multiobjective"
      ],
      "replace": [
        "timing",
        "causal",
        "multiobjective"
      ],
      "composed": [
        "causal",
        "timing",
        "multiobjective"
      ],
      "query": "空插座。两个。刚核实"
    },
    {
      "id": "S08",
      "root": "S08.1.2",
      "parent": "S08.1.2",
      "version": "S08.2.1",
      "fields": {
        "metric": {
          "value": "late_days",
          "source": "S08:turn1",
          "start": 16,
          "end": 18,
          "quote": "迟到"
        },
        "value": {
          "value": 2,
          "source": "S08:turn2",
          "start": 10,
          "end": 12,
          "quote": "两天"
        },
        "unit": {
          "value": "day",
          "source": "S08:turn1",
          "start": 15,
          "end": 16,
          "quote": "天"
        },
        "period": {
          "value": "last_month",
          "source": "S08:turn1",
          "start": 0,
          "end": 3,
          "quote": "上个月"
        },
        "modality": {
          "value": "observation",
          "source": "S08:turn2",
          "start": 7,
          "end": 9,
          "quote": "实际"
        }
      },
      "raw": [
        "causal",
        "feasibility",
        "timing"
      ],
      "replace": [
        "causal",
        "feasibility",
        "allocation"
      ],
      "composed": [
        "causal",
        "feasibility",
        "allocation"
      ],
      "query": "迟到。两天。天。上个月。实际"
    },
    {
      "id": "S12",
      "root": "S12.1.2",
      "parent": "S12.1.2",
      "version": "S12.2.1",
      "fields": {
        "metric": {
          "value": "repair_cost",
          "source": "S12:turn1",
          "start": 0,
          "end": 4,
          "quote": "修旧相机"
        },
        "value": {
          "value": 700,
          "source": "S12:turn2",
          "start": 5,
          "end": 7,
          "quote": "七百"
        },
        "modality": {
          "value": "reported_quote",
          "source": "S12:turn2",
          "start": 0,
          "end": 4,
          "quote": "维修店说"
        },
        "evidenceLimit": {
          "value": "no_written_quote",
          "source": "S12:turn2",
          "start": 9,
          "end": 16,
          "quote": "还没有书面报价"
        }
      },
      "raw": [
        "regret",
        "feasibility",
        "timing"
      ],
      "replace": [
        "timing",
        "information",
        "multiobjective"
      ],
      "composed": [
        "timing",
        "information",
        "multiobjective"
      ],
      "query": "修旧相机。七百。维修店说。还没有书面报价"
    },
    {
      "id": "S13",
      "root": "S13.1.3",
      "parent": "S13.1.3",
      "version": "S13.2.1",
      "fields": {
        "metric": {
          "value": "accuracy",
          "source": "S13:turn1",
          "start": 16,
          "end": 21,
          "quote": "准确率必须"
        },
        "role": {
          "value": "hard",
          "source": "S13:turn1",
          "start": 19,
          "end": 21,
          "quote": "必须"
        },
        "relation": {
          "value": ">=",
          "source": "S13:turn1",
          "start": 21,
          "end": 24,
          "quote": "不低于"
        },
        "value": {
          "value": 90,
          "source": "S13:turn1",
          "start": 24,
          "end": 26,
          "quote": "九成"
        },
        "unit": {
          "value": "percent",
          "source": "S13:turn1",
          "start": 24,
          "end": 26,
          "quote": "九成"
        },
        "scope": {
          "value": "formal_delivery",
          "source": "S13:turn2",
          "start": 9,
          "end": 13,
          "quote": "正式交付"
        },
        "exclusion": {
          "value": "trial",
          "source": "S13:turn2",
          "start": 14,
          "end": 25,
          "quote": "试验阶段不套用这个底线"
        }
      },
      "raw": [
        "timing",
        "information",
        "multiobjective"
      ],
      "replace": [
        "timing",
        "information",
        "measurement"
      ],
      "composed": [
        "timing",
        "information",
        "multiobjective"
      ],
      "query": "准确率必须。必须。不低于。九成。九成。正式交付。试验阶段不套用这个底线"
    }
  ]
}
```
后续优先用已有自主候选生成器检验这些手工字段的可识别性与独立数据准备度，不能用oracle成功替代开放语义。产品轨维护唯一交接，正式版本另获授权。
