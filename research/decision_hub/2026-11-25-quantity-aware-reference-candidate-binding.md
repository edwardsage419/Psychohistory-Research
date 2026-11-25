# 自主认知专项累计第116轮候选：数量词法与跨轮引用候选软绑定
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / RAW_TEXT_CANDIDATE_GRAPH / PUBLIC_SYNTHETIC_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 5d68787f882a8c3a535d0e4f3a1aa2c663ddb3ad。核对近期12提交、13开放PR（#61待审）、v3.2前15行及历史全文、唯一交接前18行、R115前18行及实际词法源码、R87前16行、R103前19行、R77实际搜索及R73转换源码。R87给定标注节点联合推理，R103原角色与引用图，R104独立严格量分支，R115新增词法；本轮新增实际原文数量跨度与原引用边的候选组合及软排序，非重复全图联合分区或训练。
## 固定资产
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
research/decision_hub/2026-11-25-raw-text-reference-search.md 16075b3ba567ee6dc3496300beab1417172a6c42
research/decision_hub/2026-11-25-unified-semantic-annotation-bridge.md af648d16ee96b9af4a3efb61b413d113208bb0ca
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
R87 4c86134031439991991c7bfb9c2bc10fc1aa4dab；R103 5b55d2104f74246d3e6d5accc31da1140c22bedd；唯一交接 5e74f4f0b37141d631740e844ad8bbbfed232e07。两套公开原创ChatGPT研发辅助合成开发语料均已见，非真人、训练、独立留出。
## 合同
直接复用R115 lexical及R77 search，每轮前100跨度、允许一处内部标点，保留所有有限候选边。只依据完整包含关系把数量词法跨度附着到引用边两端；两端数值候选的笛卡尔积均保留；单位词面相等加2、任一未知单位加1、其余加0，研究者选择的固定分数，未训练/拟合或证明最优。若多个配对取最高加分，不认为相同单位代表同一指标、主体、时段或真实单位；个/套/次在原词法归一为count，更不能视为实体同一。两端无数量保持原分数。不同单位不删除，因为可能换算或修改口径；未知货币不补齐。分数只作为排序，非语义概率。保留原始及增强排序和前100并集，后者预算至200边，比较时报告实际大小，不能称同预算提升。原文候选生成完全不输入标注；R73标注仅在事后定位12个唯一已标引用；未标注不视负例。目标边有数量对不等于正确数量绑定，边内多对可能互相冲突；没有实体识别、语义角色解析、实际更新、硬约束或真实模型调用。S13只修改作用域可能不含当前数值，不能因无数量对删除。条件、否定、隐含单位、主体及概念仍未知。候选不赋予authority，始终outside=true。边数cap为研究限制且在原搜索后检查，非提前资源防护；数量配对笛卡尔积未统一计费，不是生产内存/延迟上限。保留已知R115词法局限。
## 实验及复算
同一32情节64轮、12已标引用；比较原排序及数量加分排序的精确边位置、命中数量及并集，保留每个边的变化。不测precision（缺负标签）、真实用户、独立验收、原生执行或设备。计数为边与候选，非独立样本。10项控制包括同单位不同实体、不同单位、未知单位、无新数量及预算拒绝。所有权重和预算由研究者选定，尚非产品政策。无新费用、训练、Codex、CI、生产修改、PR合并、部署或冻结变化。
按上述五文件顺序置入docs[i].content，Node标准JS，仅加载已审查项目自有源码。
```js
function load(docs){
 const code=i=>docs[i].content.split("```js\n")[1].split("\n```")[0];
 const L=Function(code(0).slice(code(0).indexOf("function experiment(A)")).split(" let out={corpusTurns:")[0]+"\nreturn {lexical};\n}\nreturn experiment({});")();
 const R=Function(code(1).split(" const pos=")[0]+"\nreturn {search};\n}\nreturn experiment();")();
 const I=Function(code(2).split(" const out={datasets:")[0]+"\nreturn {build,verify};\n}\nreturn experiment();")();
 return {L,R,I}
}
function experiment(L,R,I,corpora,assets){
 const ck=(v,m)=>{if(!v)throw Error(m)},contains=(s,n)=>s.start<=n.start&&s.end>=n.end;
 function graph(a,b,k=100,cap=10000){
  const z=R.search(a,b,k,true),x=L.lexical(a),y=L.lexical(b);
  if(z.status!=="CANDIDATES_ONLY"||x.status!=="CANDIDATES_ONLY"||y.status!=="CANDIDATES_ONLY"||z.edges.length>cap)return {status:"LIMIT_OR_UNKNOWN",authority:"NONE",edges:[],outside:true};
  const an=z.a.map(s=>x.items.filter(n=>contains(s,n))),bn=z.b.map(s=>y.items.filter(n=>contains(s,n)));
  const am=new Map(z.a.map((s,i)=>[s,an[i]])),bm=new Map(z.b.map((s,i)=>[s,bn[i]]));
  const edges=z.edges.map((e,i)=>{
   const a=am.get(e.a),b=bm.get(e.b),pairs=a.flatMap(p=>b.map(q=>({p,q,unit:p.unit===null||q.unit===null?"UNKNOWN":p.unit===q.unit?"SAME_SURFACE_UNIT":"DIFFERENT_SURFACE_UNIT"})));
   // Soft evidence only. No pair is discarded; no implied conversion or co-reference.
   const same=pairs.some(p=>p.unit==="SAME_SURFACE_UNIT");
   const unknown=pairs.some(p=>p.unit==="UNKNOWN");
   const bonus=same?2:unknown?1:0;
   return {a:e.a,b:e.b,baseRank:i+1,baseScore:e.score,score:e.score+bonus,pairs,authority:"NONE",outside:true}
  });
  const ranked=[...edges].sort((a,b)=>b.score-a.score||a.baseRank-b.baseRank);
  return {status:"CANDIDATES_ONLY",authority:"NONE",outside:true,edges,ranked,counts:{old:x.items.length,current:y.items.length}}
 }
 const metrics=()=>({targets:0,hit1:0,hit20:0,hit100:0,hit200:0});
 const out={episodes:0,turns:0,edges:0,numberPairEdges:0,ambiguousPairEdges:0,knownDifferentUnitEdges:0,unknownUnitEdges:0,targets:0,targetsWithPair:0,targetsWithoutPair:0,uncoveredTargets:0,rankImproved:0,rankWorsened:0,rankUnchanged:0,baseline:metrics(),quantityAware:metrics(),union100:0,unionSizeSum:0,controls:0,rows:[]};
 const key=e=>JSON.stringify([e.a.start,e.a.end,e.b.start,e.b.end]);
 function stat(m,r){m.targets++;if(r>0){m.hit1+=+(r===1);m.hit20+=+(r<=20);m.hit100+=+(r<=100);m.hit200+=+(r<=200)}}
 for(let d=0;d<corpora.length;d++){
  let ir=I.build(corpora[d],assets[d]);ck(I.verify(ir,corpora[d],assets[d]),"IR");
  for(let e of ir.episodes){const [a,b]=e.turns,z=graph(a.text,b.text);ck(z.status==="CANDIDATES_ONLY","graph");out.episodes++;out.turns+=2;out.edges+=z.edges.length;
   for(let edge of z.edges){out.numberPairEdges+=+(edge.pairs.length>0);out.ambiguousPairEdges+=+(edge.pairs.length>1);out.knownDifferentUnitEdges+=+edge.pairs.some(x=>x.unit==="DIFFERENT_SURFACE_UNIT");out.unknownUnitEdges+=+edge.pairs.some(x=>x.unit==="UNKNOWN");ck(edge.authority==="NONE"&&edge.outside,"authority")}
   const union=new Set([...z.edges.slice(0,100),...z.ranked.slice(0,100)].map(key));out.unionSizeSum+=union.size;
   for(let cur of b.items.filter(x=>x.reference.status==="UNIQUE_CANDIDATE")){
    const old=a.items.find(x=>x.id===cur.reference.candidates[0]);ck(old,"ref");
    let target=edge=>edge.a.start===old.span.start&&edge.a.end===old.span.end&&edge.b.start===cur.span.start&&edge.b.end===cur.span.end;
    let i=z.edges.findIndex(target),j=z.ranked.findIndex(target);ck((i<0)===(j<0),"preserve");
    out.targets++;stat(out.baseline,i+1);stat(out.quantityAware,j+1);
    if(i<0){out.uncoveredTargets++;out.rows.push({id:e.meta.id,cur:cur.id,baseRank:null,quantityRank:null});continue}
    let edge=z.edges[i];out.targetsWithPair+=+(edge.pairs.length>0);out.targetsWithoutPair+=+(edge.pairs.length===0);out.rankImproved+=+(j<i);out.rankWorsened+=+(j>i);out.rankUnchanged+=+(j===i);out.union100+=+union.has(key(edge));
    out.rows.push({id:e.meta.id,cur:cur.id,baseRank:i+1,quantityRank:j+1,pairs:edge.pairs.map(x=>({old:x.p.raw,current:x.q.raw,unit:x.unit}))})
   }
  }
 }
 let same=graph("步行最多十五分钟，等待最多十五分钟","改为十二分钟");
 let cross=graph("最多十五美元","改为十二分钟");
 let unknown=graph("费用大约五百","改为七百");
 let noNum=graph("准确率必须不低于九成","仅用于正式交付");
 const tests=[()=>out.episodes===32&&out.targets===12,()=>out.targetsWithPair+out.targetsWithoutPair+out.uncoveredTargets===12,()=>out.rankImproved+out.rankWorsened+out.rankUnchanged+out.uncoveredTargets===12,()=>out.union100>=out.baseline.hit100&&out.union100>=out.quantityAware.hit100,()=>same.edges.some(e=>e.a.text.includes("步行")&&e.pairs.some(p=>p.unit==="SAME_SURFACE_UNIT"))&&same.edges.some(e=>e.a.text.includes("等待")&&e.pairs.some(p=>p.unit==="SAME_SURFACE_UNIT")),()=>cross.edges.some(e=>e.pairs.some(p=>p.unit==="DIFFERENT_SURFACE_UNIT")),()=>unknown.edges.some(e=>e.pairs.some(p=>p.unit==="UNKNOWN")),()=>noNum.edges.every(e=>e.pairs.length===0),()=>graph("甲乙","丙丁",100,0).edges.length===0,()=>same.authority==="NONE"&&same.outside];
 for(let t of tests){ck(t(),"control "+out.controls);out.controls++}
 return out
}
const {L,R,I}=load(docs),corpora=docs.slice(3).map(x=>JSON.parse(x.content)),assets=[{id:"L",sha:"be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb"},{id:"S",sha:"05c239f3f3b1f46235fa2464d2945c21c6c08132"}];
console.log(JSON.stringify(experiment(L,R,I,corpora,assets),null,2));
```
## 实测
```json
{
  "episodes": 32,
  "turns": 64,
  "edges": 313700,
  "numberPairEdges": 18888,
  "ambiguousPairEdges": 4044,
  "knownDifferentUnitEdges": 3315,
  "unknownUnitEdges": 13623,
  "targets": 12,
  "targetsWithPair": 5,
  "targetsWithoutPair": 7,
  "uncoveredTargets": 0,
  "rankImproved": 2,
  "rankWorsened": 1,
  "rankUnchanged": 9,
  "baseline": {
    "targets": 12,
    "hit1": 3,
    "hit20": 6,
    "hit100": 10,
    "hit200": 11
  },
  "quantityAware": {
    "targets": 12,
    "hit1": 3,
    "hit20": 7,
    "hit100": 10,
    "hit200": 11
  },
  "union100": 10,
  "unionSizeSum": 3451,
  "controls": 10,
  "rows": [
    {
      "id": "L03",
      "cur": "L03.2.1",
      "baseRank": 735,
      "quantityRank": 814,
      "pairs": []
    },
    {
      "id": "L08",
      "cur": "L08.2.2",
      "baseRank": 23,
      "quantityRank": 23,
      "pairs": []
    },
    {
      "id": "L15",
      "cur": "L15.2.1",
      "baseRank": 146,
      "quantityRank": 146,
      "pairs": []
    },
    {
      "id": "S01",
      "cur": "S01.2.1",
      "baseRank": 2,
      "quantityRank": 2,
      "pairs": []
    },
    {
      "id": "S02",
      "cur": "S02.2.1",
      "baseRank": 21,
      "quantityRank": 12,
      "pairs": [
        {
          "old": "十五分钟",
          "current": "十二分钟",
          "unit": "SAME_SURFACE_UNIT"
        }
      ]
    },
    {
      "id": "S03",
      "cur": "S03.2.1",
      "baseRank": 3,
      "quantityRank": 3,
      "pairs": [
        {
          "old": "五",
          "current": "五",
          "unit": "UNKNOWN"
        }
      ]
    },
    {
      "id": "S04",
      "cur": "S04.2.1",
      "baseRank": 1,
      "quantityRank": 1,
      "pairs": [
        {
          "old": "一个",
          "current": "两个",
          "unit": "SAME_SURFACE_UNIT"
        }
      ]
    },
    {
      "id": "S08",
      "cur": "S08.2.1",
      "baseRank": 1,
      "quantityRank": 1,
      "pairs": [
        {
          "old": "三天",
          "current": "两天",
          "unit": "SAME_SURFACE_UNIT"
        }
      ]
    },
    {
      "id": "S10",
      "cur": "S10.2.1",
      "baseRank": 1,
      "quantityRank": 1,
      "pairs": []
    },
    {
      "id": "S11",
      "cur": "S11.2.1",
      "baseRank": 69,
      "quantityRank": 69,
      "pairs": []
    },
    {
      "id": "S12",
      "cur": "S12.2.1",
      "baseRank": 79,
      "quantityRank": 22,
      "pairs": [
        {
          "old": "五百",
          "current": "七百",
          "unit": "UNKNOWN"
        }
      ]
    },
    {
      "id": "S13",
      "cur": "S13.2.1",
      "baseRank": 2,
      "quantityRank": 2,
      "pairs": []
    }
  ]
}
```
下一责任：在明确指标/实体及作用域的独立语义候选基础上再比较绑定，避免继续用单位相等替代指代；优先积累合法真实语言与独立留出。正式版本与训练另获授权；产品轨维护唯一交接。
