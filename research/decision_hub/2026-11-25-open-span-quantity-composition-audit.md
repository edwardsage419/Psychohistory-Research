# 自主认知专项累计第127轮候选：无固定指标名称的原文跨度与数量组合审计
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / PUBLIC_SYNTHETIC_DEVELOPMENT / RAW_SPAN_QUANTITY_GRAPH / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 1ea415946beefbebf81bf5ba243c8155bd488835。核对近12提交、13开放PR（#61待审）、v3.2前15行及历史全文、唯一交接前18行、R126前20行、R73前18行、R86前15行、R61前15行及以下固定资产实际源码。R126固定四字段在原64轮零候选；R86有oracle节点属性，R116/R117跨轮边；本轮研究同轮原文跨度和数量组合，不重新做跨轮引用排序、训练或扩大字段词表。
## 固定资产
research/decision_hub/2026-11-25-unified-semantic-annotation-bridge.md af648d16ee96b9af4a3efb61b413d113208bb0ca
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
research/decision_hub/2026-11-25-temporal-quantity-candidate-separation.md 8a6b42f83b80283db6e215fe48f4fb2efbf8368c
research/decision_hub/2026-11-25-field-lineage-semantic-patch.md 307f8ba1291ec9ad83aca578bd5a02508d1e6110
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
R126 76b92d0de008ad83d6a12bd2b7f247eea316932f；R86 ac7cafba4b3dd72e12531b08d36ebe7307e0a9c3；R61 17b6035732e43c56edc44cb5db07b8d49aadfd5b；唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07。旧公开合成开发语料及手工指标为ChatGPT研发辅助项目原创，非真人、独立留出或已授权训练。
## 候选合同
实际复用R74 scan的同标点子句全部跨度（最长24 UTF16），R117 temporal的ordinary（源自R115组合整数），每个数量q与同子句所有包含其完整跨度的span构成claim边；与同子句非重叠且不覆盖其他数量、星期/钟表/年代位置的span构成metric边。后者只是指标/实体词面候选，不是确定的指标、实体或关系。两类固定评分为子句边界与长度偏好，或距离与长度偏好。没有指标名称字典、训练、标注输入或强制单一选择；值、单位、位置、原文保留，所有authority NONE及outside true。相同分数按位置确定排序；排名非概率，完整有限格也非开放语义覆盖。允许左/右指标，不允许跨标点，本轮不解析角色、比较方向、主体、条件、否定、指代、实际/估计、时间范围或跨句附着。输入限128 UTF16，边数超过20000整体LIMIT且空候选；R74先枚举跨度、循环和排序不受同一个资源预算约束，不能作为生产防护或真机性能证明。缺标注不能认为没有义务，候选非空不能获得更新/数学准入。
## 评估
实际R73 build/verify保留原167标注，独立于图生成。对已有value/lower/upper明确数值（布尔/字符串不计）逐属性，检查原标注跨度内同值ordinary候选；进一步检查含完整标注跨度的claim边及全轮top20/100。仅原始显式unit完全字符串相等计unit exact，不擅自归一化CNY/month、min/minute等，也不将标注单位补进原文，matchedDifferentOrCompositeUnit还包含无单位标注但候选带单位的情况。匹配不证明真正数值角色，数值不匹配包括口语省略、否定语义、隐含值等，具体失败逐项留档。另使用R114已存在的5个初始人工指标quote/value锚评估metric边，检查精确跨度及同起点值（允许词法单位扩展）排名；并未在通用语料建立全面指标标注，不能报精度/召回或泛化。R126零候选是固定业务字段类型，与本轮无类型跨度组合口径不同，不能直接当准确率增益。13控制。所有设计、长度评分、预算与规则研究者选定，非独立验收。无新外部资料、真实个人数据、训练、Codex、CI、原生运行、PR合并、部署、费用或冻结变化。产品轨维护唯一交接。
## 复算
按上述七份文件顺序置入docs[i].content，Node标准JS，仅执行已审查项目自有源码。
```js
function load(docs){
 const c=i=>docs[i].content.split("```js\n")[1].split("\n```")[0];
 const I=Function(c(0).split(" const out={datasets:")[0]+"\nreturn {build,verify};\n}\nreturn experiment();")();
 const S=Function(c(1).split(" const blank=()=>")[0]+"\nreturn {scan};\n}\nreturn experiment();")();
 const L=Function(c(2).slice(c(2).indexOf("function experiment(A)")).split(" let out={corpusTurns:")[0]+"\nreturn {lexical,parseNum};\n}\nreturn experiment({});")();
 const T=Function("L",c(3).slice(c(3).indexOf("function experiment(L,R,I,G")).split(" // Reuse the actual R116 graph")[0]+"\nreturn {temporal};\n}\nreturn experiment(L);")(L);
 const cases=JSON.parse(c(4).split("const cases=")[1].split(";\n")[0]);
 return {I,S,T,cases}
}
function experiment(I,S,T,cases,corpora,assets){
 const ck=(v,m)=>{if(!v)throw Error(m)},same=(a,b)=>a.start===b.start&&a.end===b.end,inside=(a,b)=>a.start>=b.start&&a.end<=b.end;
 const sort=(a,b)=>b.score-a.score||a.span.start-b.span.start||a.span.end-b.span.end||a.q.start-b.q.start;
 // No metric names, semantic labels or gold fields enter construction.
 function graph(text,cap=20000){
  let s=S.scan(text),t=T.temporal(text);
  if(s.status!=="CANDIDATES_ONLY"||t.status!=="CANDIDATES_ONLY")return {status:"LIMIT",claims:[],metrics:[],authority:"NONE",outside:true};
  const claims=[],metrics=[];
  for(let q of t.ordinary){
   const cl=s.clauses.find(x=>inside(q,x));if(!cl)continue;
   for(let span of s.all.filter(x=>inside(x,cl))){
    if(inside(q,span)){
     let boundary=+(span.start===cl.start)+ +(span.end===cl.end);
     claims.push({span,q,score:4*boundary-Math.abs(span.end-span.start-8)/4,authority:"NONE",outside:true})
    }else if(span.end<=q.start||span.start>=q.end){
     if(t.ordinary.some(v=>v.start<span.end&&span.start<v.end)||t.items.some(v=>["WEEKDAY","CLOCK","DECADE"].includes(v.kind)&&v.start<span.end&&span.start<v.end))continue;
     let gap=span.end<=q.start?q.start-span.end:span.start-q.end;
     // proximity and length only; no named field vocabulary.
     metrics.push({span,q,score:-gap-Math.abs(span.end-span.start-4)/4,authority:"NONE",outside:true})
    }
    if(claims.length+metrics.length>cap)return {status:"LIMIT",claims:[],metrics:[],authority:"NONE",outside:true};
   }
  }
  return {status:"CANDIDATES_ONLY",claims:claims.sort(sort),metrics:metrics.sort(sort),authority:"NONE",outside:true}
 }
 const out={turns:0,annotations:0,quantityCandidates:0,claimEdges:0,metricEdges:0,turnsWithEdges:0,numericObligations:0,lexicalValueCoverage:0,claimExactCoverage:0,claimTop20:0,claimTop100:0,explicitUnitExact:0,matchedWithoutUnit:0,matchedDifferentOrCompositeUnit:0,missingValue:[],missingClaim:[],metricTargets:0,metricExactCoverage:0,metricTop20:0,metricTop100:0,metricRows:[],nonNumericAnnotations:0,controls:0};
 const graphs=new Map();
 for(let d=0;d<2;d++){
  let ir=I.build(corpora[d],assets[d]);ck(I.verify(ir,corpora[d],assets[d]),"IR");
  for(let ep of ir.episodes)for(let [i,t] of ep.turns.entries()){
   let g=graph(t.text),z=T.temporal(t.text);ck(g.status==="CANDIDATES_ONLY","limit");graphs.set(ep.meta.id+":"+i,{g,t,z});
   out.turns++;out.quantityCandidates+=z.ordinary.length;out.claimEdges+=g.claims.length;out.metricEdges+=g.metrics.length;out.turnsWithEdges+=+(g.claims.length+g.metrics.length>0);
   for(let e of [...g.claims,...g.metrics])ck(t.text.slice(e.span.start,e.span.end)===e.span.text&&t.text.slice(e.q.start,e.q.end)===e.q.raw&&e.authority==="NONE"&&e.outside,"span");
   for(let a of t.items){
    out.annotations++;let keys=["value","lower","upper"].filter(k=>a.dimensions[k].status==="ANNOTATED"&&typeof a.dimensions[k].value==="number");
    if(!keys.length)out.nonNumericAnnotations++;
    for(let k of keys){
     out.numericObligations++;const v=a.dimensions[k].value;
     let matches=z.ordinary.filter(q=>inside(q,a.span)&&q.value===v),rank=g.claims.findIndex(e=>same(e.span,a.span)&&e.q.value===v)+1;
     if(matches.length){out.lexicalValueCoverage++;const unit=a.dimensions.unit;
      if(unit.status==="ANNOTATED"&&matches.some(q=>q.unit===unit.value))out.explicitUnitExact++;
      else if(matches.every(q=>q.unit===null))out.matchedWithoutUnit++;
      else out.matchedDifferentOrCompositeUnit++;
     }else out.missingValue.push({id:a.id,field:a.dimensions.field.value??null,kind:k,value:v,quote:a.span.text,candidates:z.ordinary.filter(q=>inside(q,a.span)).map(q=>({raw:q.raw,value:q.value,unit:q.unit}))});
     if(rank){out.claimExactCoverage++;out.claimTop20+=+(rank<=20);out.claimTop100+=+(rank<=100)}else if(matches.length)out.missingClaim.push({id:a.id,kind:k,quote:a.span.text});
    }
   }
  }
 }
 // Earlier independent manual metric quotes are consulted only here.
 for(let c of cases){
  const {g,t}=graphs.get(c.id+":0"),[metric,quote]=c.initial.metric,[value,qquote]=c.initial.value;
  const start=t.text.indexOf(quote),qstart=t.text.indexOf(qquote);
  ck(start>=0&&qstart>=0,"gold");
  let r=g.metrics.findIndex(e=>same(e.span,{start,end:start+quote.length})&&e.q.start===qstart&&e.q.value===value)+1;
  out.metricTargets++;out.metricExactCoverage+=+(r>0);out.metricTop20+=+(r>0&&r<=20);out.metricTop100+=+(r>0&&r<=100);
  out.metricRows.push({id:c.id,metric,quote,quantity:qquote,rank:r||null,edges:g.metrics.length});
 }
 for(let test of [()=>out.turns===64,()=>out.annotations===167,()=>out.quantityCandidates===58,()=>out.lexicalValueCoverage+out.missingValue.length===out.numericObligations,()=>out.claimExactCoverage+out.missingClaim.length===out.lexicalValueCoverage,()=>out.explicitUnitExact+out.matchedWithoutUnit+out.matchedDifferentOrCompositeUnit===out.lexicalValueCoverage,()=>graph("周五下午五点前提交").claims.length===0,()=>graph("费用五百，时间三小时").metrics.every(e=>!(e.span.text.includes("费用")&&e.q.unit==="hour")),()=>graph("费用五百",0).status==="LIMIT",()=>graph("费用五百",0).claims.length===0,()=>graph("字".repeat(129)).status==="LIMIT",()=>graph("陌生指标三美元").claims.length>0,()=>graph("陌生指标三美元").authority==="NONE"]){ck(test(),"control "+out.controls);out.controls++}
 return out
}
const {I,S,T,cases}=load(docs);console.log(JSON.stringify(experiment(I,S,T,cases,docs.slice(5).map(x=>JSON.parse(x.content)),docs.slice(5).map((x,i)=>({id:i?"S":"L",sha:x.sha}))),null,2));
```
## 实测
```json
{
  "turns": 64,
  "annotations": 167,
  "quantityCandidates": 58,
  "claimEdges": 1028,
  "metricEdges": 1398,
  "turnsWithEdges": 33,
  "numericObligations": 28,
  "lexicalValueCoverage": 16,
  "claimExactCoverage": 15,
  "claimTop20": 15,
  "claimTop100": 15,
  "explicitUnitExact": 7,
  "matchedWithoutUnit": 5,
  "matchedDifferentOrCompositeUnit": 4,
  "missingValue": [
    {
      "id": "L01.1.3",
      "field": "rent",
      "kind": "value",
      "value": 3600,
      "quote": "房租三千六",
      "candidates": []
    },
    {
      "id": "L01.2.1",
      "field": "parking",
      "kind": "value",
      "value": 450,
      "quote": "停车每月四百五",
      "candidates": []
    },
    {
      "id": "L02.1.2",
      "field": "night_shift",
      "kind": "value",
      "value": 0,
      "quote": "只要夜班我就不去",
      "candidates": []
    },
    {
      "id": "L02.2.1",
      "field": "night_shift",
      "kind": "value",
      "value": 0,
      "quote": "一次都不能有",
      "candidates": [
        {
          "raw": "一次",
          "value": 1,
          "unit": "count"
        }
      ]
    },
    {
      "id": "L04.1.4",
      "field": "early_reward",
      "kind": "value",
      "value": 0,
      "quote": "提前做完没奖",
      "candidates": []
    },
    {
      "id": "L10.1.4",
      "field": "prior_probability",
      "kind": "value",
      "value": 0.8,
      "quote": "当时大概觉得八成",
      "candidates": [
        {
          "raw": "八成",
          "value": 80,
          "unit": "percent"
        }
      ]
    },
    {
      "id": "L12.1.1",
      "field": "kitchen",
      "kind": "value",
      "value": 60000,
      "quote": "厨房想留六万",
      "candidates": []
    },
    {
      "id": "L12.1.2",
      "field": "bathroom",
      "kind": "value",
      "value": 60000,
      "quote": "卫生间也得留六万",
      "candidates": []
    },
    {
      "id": "L12.1.3",
      "field": "total",
      "kind": "value",
      "value": 100000,
      "quote": "两项加起来只能十万",
      "candidates": [
        {
          "raw": "两",
          "value": 2,
          "unit": null
        }
      ]
    },
    {
      "id": "L12.2.1",
      "field": "minimums",
      "kind": "value",
      "value": 60000,
      "quote": "两个都必须至少六万",
      "candidates": [
        {
          "raw": "两个",
          "value": 2,
          "unit": "count"
        }
      ]
    },
    {
      "id": "L14.1.1",
      "field": "bonus",
      "kind": "value",
      "value": 20000,
      "quote": "同事说这家公司奖金一般两万",
      "candidates": [
        {
          "raw": "一",
          "value": 1,
          "unit": null
        }
      ]
    },
    {
      "id": "L17.1.2",
      "field": "forecast",
      "kind": "value",
      "value": 0.8,
      "quote": "八成把握这次准时",
      "candidates": [
        {
          "raw": "八成",
          "value": 80,
          "unit": "percent"
        }
      ]
    }
  ],
  "missingClaim": [
    {
      "id": "L05.1.3",
      "kind": "value",
      "quote": "到时候看谁更需要，再挪两天"
    }
  ],
  "metricTargets": 5,
  "metricExactCoverage": 5,
  "metricTop20": 3,
  "metricTop100": 5,
  "metricRows": [
    {
      "id": "S02",
      "metric": "station_walking_time",
      "quote": "离车站步行",
      "quantity": "十五",
      "rank": 8,
      "edges": 113
    },
    {
      "id": "S04",
      "metric": "free_outlets",
      "quote": "空插座",
      "quantity": "一个",
      "rank": 6,
      "edges": 47
    },
    {
      "id": "S08",
      "metric": "late_days",
      "quote": "迟到",
      "quantity": "三天",
      "rank": 3,
      "edges": 9
    },
    {
      "id": "S12",
      "metric": "repair_cost",
      "quote": "修旧相机",
      "quantity": "五百",
      "rank": 28,
      "edges": 58
    },
    {
      "id": "S13",
      "metric": "accuracy",
      "quote": "准确率必须",
      "quantity": "九成",
      "rank": 23,
      "edges": 36
    }
  ],
  "nonNumericAnnotations": 140,
  "controls": 13
}
```
后续优先处理数词省略与单位证据分离、指标组合附着与真实语料质量，不通过调参拟合这5个已见指标。正式开发与训练另获授权。
