# 自主认知专项累计第117轮候选：时间位置、持续时长与普通数量分离
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / RAW_TEXT_TEMPORAL_CANDIDATES / PUBLIC_SYNTHETIC_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main bd97b82e4043d90def1015f244213f0cc8415309。核对近12提交、13开放PR（#61待审）、v3.2前15行及历史全文、唯一交接前18行、R116/R100/R62相关前段、R115及R116实际源码、两套语料全文。R100是显式到账时序；本轮是原文时间词法候选与数量排序隔离，不执行到账或长期计划，不宣称开放语言理解。
## 固定资产
research/decision_hub/2026-11-25-quantity-aware-reference-candidate-binding.md 813d164fbde157b6ab7015f9830835f8273f2e91
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
research/decision_hub/2026-11-25-raw-text-reference-search.md 16075b3ba567ee6dc3496300beab1417172a6c42
research/decision_hub/2026-11-25-unified-semantic-annotation-bridge.md af648d16ee96b9af4a3efb61b413d113208bb0ca
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
R100 65008b82d4720e931c99bd66ed03228b1f8ef69e；R62 ada3d84a46e4d9a411ebf762884d13a5c5e87686；唯一交接 5e74f4f0b37141d631740e844ad8bbbfed232e07。两套原有ChatGPT研发辅助原创公开合成开发语料，均已见、非真人、训练或独立留出。
## 合同
复用R115 lexical/parseNum，有限组合词法识别星期位置、钟表位置、年代、相对/重复期间、持续时长或天数计数。原文位置与候选类型独立，全部authority NONE/outside true。星期不自动解析具体日期，周相对项未绑定基准；时钟不自动填上午下午、时区或日期，带下午的5仍保留词面小时5和partOfDay，不能当24小时05:00。年代保留未知世纪；相对期间保留anchor null；持续时长与计数仍待语义判断。半天保留0.5天词面候选，不规定实际工作小时。没有真实时间定位、时区计算、工作日日历、事件/主体身份、量词完整覆盖、语法否定作用域、日期歧义、绝对时点、夏令时、跨轮锚点或动作权限。规则仅开发原型，可能误识别固定表达、非规范钟表、词汇重叠；clock接受0..23且部分时段不检验相容性，只是候选；时分若未写分则0仅词法标记，不赋精确时刻。持续项的邻接过滤继承部分R115限制，不是完整合法性。原始数值候选全保留；仅在普通数量排序加分视图隔离与星期/钟表/年代跨度重叠的词法候选，不能据此证明它不是另一个可行解析。时长保留数值分支，新增独立时间候选不会自动参与引用排序。没有通过单位相等或星期相等推定相同事件。研究者选择词法类型和隔离规则，非产品最终政策；不以无限扩展规则代替开放语义。
## 实验
在同一32情节64轮12条已标唯一引用上直接复用R116 graph，两种lexical视图仅数量排序输入有差异；同一前100跨度、桥接预算、分数和所有边保留。逐轮时间候选、原文切片、隔离数、数量边计数及12个目标排名比较。前述原R116数值总计68和有数量配对边18888复现；未执行原R116完整控制，而使用其图函数。无完整真实时间标注或负例，时间候选数量不能当准确率；14项人工控制为开发验证，非独立留出。未识别实际对象/概念，不把排序变化当完整语义提升。无实际数学执行、权限、设备或真人效果。无新增费用、训练、Codex、CI、生产修改、PR合并、部署或冻结变化。
## 复算
按上述六份固定文件顺序读取docs[i].content，Node标准JS。仅加载已审查自有代码。
```js
function load(docs){
 const code=i=>docs[i].content.split("```js\n")[1].split("\n```")[0];
 const L=Function(code(1).slice(code(1).indexOf("function experiment(A)")).split(" let out={corpusTurns:")[0]+"\nreturn {lexical,parseNum};\n}\nreturn experiment({});")();
 const R=Function(code(2).split(" const pos=")[0]+"\nreturn {search};\n}\nreturn experiment();")();
 const I=Function(code(3).split(" const out={datasets:")[0]+"\nreturn {build,verify};\n}\nreturn experiment();")();
 const G=Function(code(0).slice(code(0).indexOf("function experiment(L,R,I")).split(" const metrics=()=>")[0]+"\nreturn {graph};\n}\nreturn experiment(L,R);".replace("return experiment(L,R);","return experiment(L,R,null);"));
 return {L,R,I,G}
}
function experiment(L,R,I,G,corpora,assets){
 const ck=(b,m)=>{if(!b)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),overlap=(a,b)=>a.start<b.end&&b.start<a.end;
 function temporal(s){
  if(typeof s!=="string"||s.length>128)return {status:"LIMIT",items:[],ordinary:[],raw:[],isolated:[]};
  const z=L.lexical(s),items=[];
  function add(m,kind,detail){items.push({start:m.index,end:m.index+m[0].length,raw:m[0],kind,detail,authority:"NONE",outside:true})}
  const wd={"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"日":7,"天":7};
  for(const m of s.matchAll(/(上|下|本|这)?周([一二三四五六日天])/gu))add(m,"WEEKDAY",{week:m[1]??null,weekday:wd[m[2]],date:null});
  for(const m of s.matchAll(/(凌晨|早上|上午|中午|下午|晚上)?([零一二三四五六七八九两十百千]+|[0-9]+)点(半|[零一二三四五六七八九两十]+分|[0-9]+分)?/gu)){
   const hour=L.parseNum(m[2]),minute=m[3]==="半"?30:m[3]?L.parseNum(m[3].slice(0,-1)):0;
   if(hour!==null&&hour<=23&&minute!==null&&minute<=59)add(m,"CLOCK",{hour,minute,partOfDay:m[1]??null,date:null,timezone:null,resolved:false});
  }
  for(const m of s.matchAll(/([一二三四五六七八九]十)年代/gu))add(m,"DECADE",{decade:L.parseNum(m[1]),century:null});
  for(const m of s.matchAll(/上个月|下个月|这个月|本月|去年|今年|明年|当天|隔天|周末|每天|每周|每月|每年/gu))add(m,"RELATIVE_PERIOD",{label:m[0],anchor:null});
  for(const m of s.matchAll(/([零一二三四五六七八九两十百千]+|[0-9]+|半)(分钟|小时|天|周|年)/gu)){
   if(items.some(x=>overlap(x,{start:m.index,end:m.index+m[0].length})))continue;
   let n=m[1]==="半"?0.5:L.parseNum(m[1]);
   if(n!==null&&!/[万亿点.负\-]/u.test(s[m.index-1]??"")&&!/[万亿点.来多]/u.test(s[m.index+m[0].length]??""))add(m,"DURATION_OR_DAY_COUNT",{value:n,unit:m[2],role:null});
  }
  items.sort((a,b)=>a.start-b.start||a.end-b.end);
  // Keep original lexemes. Only remove overlap with calendar/clock candidates from ordinary bonus.
  const isolated=z.items.filter(x=>items.some(y=>["WEEKDAY","CLOCK","DECADE"].includes(y.kind)&&overlap(x,y)));
  const ordinary=z.items.filter(x=>!isolated.includes(x));
  return {status:"CANDIDATES_ONLY",items,ordinary,raw:z.items,isolated,authority:"NONE",outside:true}
 }
 // Reuse the actual R116 graph twice, varying only the lexical view.
 const oldG=G(L,R),newG=G({lexical:s=>{let t=temporal(s);return {status:t.status,items:t.ordinary}}},R);
 const out={episodes:0,turns:0,rawNumbers:0,ordinaryNumbers:0,isolatedNumbers:0,temporalCandidates:0,kinds:{},numberPairEdgesOld:0,numberPairEdgesNew:0,edges:0,targets:0,oldHit20:0,newHit20:0,oldHit100:0,newHit100:0,rankImproved:0,rankWorsened:0,rankUnchanged:0,controls:0,rows:[],isolated:[]};
 for(let d=0;d<corpora.length;d++){
  const ir=I.build(corpora[d],assets[d]);ck(I.verify(ir,corpora[d],assets[d]),"IR");
  for(const e of ir.episodes){
   out.episodes++;
   for(let [i,t] of e.turns.entries()){
    let q=temporal(t.text);ck(q.status==="CANDIDATES_ONLY","temporal");
    out.turns++;out.rawNumbers+=q.raw.length;out.ordinaryNumbers+=q.ordinary.length;out.isolatedNumbers+=q.isolated.length;out.temporalCandidates+=q.items.length;
    for(let x of q.items){ck(t.text.slice(x.start,x.end)===x.raw&&x.authority==="NONE","span");out.kinds[x.kind]=(out.kinds[x.kind]||0)+1}
    if(q.isolated.length)out.isolated.push({id:e.meta.id,turn:i+1,removedFromBonus:q.isolated.map(x=>x.raw),temporal:q.items.filter(x=>q.isolated.some(y=>overlap(x,y))).map(x=>({raw:x.raw,kind:x.kind,detail:x.detail}))});
   }
   const [a,b]=e.turns,old=oldG.graph(a.text,b.text),now=newG.graph(a.text,b.text);
   ck(old.status==="CANDIDATES_ONLY"&&now.status==="CANDIDATES_ONLY"&&old.edges.length===now.edges.length,"graph");
   out.edges+=old.edges.length;
   out.numberPairEdgesOld+=old.edges.filter(x=>x.pairs.length).length;out.numberPairEdgesNew+=now.edges.filter(x=>x.pairs.length).length;
   for(let cur of b.items.filter(x=>x.reference.status==="UNIQUE_CANDIDATE")){
    const prev=a.items.find(x=>x.id===cur.reference.candidates[0]);
    const match=x=>x.a.start===prev.span.start&&x.a.end===prev.span.end&&x.b.start===cur.span.start&&x.b.end===cur.span.end;
    let o=old.ranked.findIndex(match)+1,n=now.ranked.findIndex(match)+1;
    ck(o>0&&n>0,"candidate preserved");out.targets++;out.oldHit20+=+(o<=20);out.newHit20+=+(n<=20);out.oldHit100+=+(o<=100);out.newHit100+=+(n<=100);out.rankImproved+=+(n<o);out.rankWorsened+=+(n>o);out.rankUnchanged+=+(n===o);
    out.rows.push({id:e.meta.id,old:o,new:n,oldPairs:old.ranked[o-1].pairs.length,newPairs:now.ranked[n-1].pairs.length});
   }
  }
 }
 const t=s=>temporal(s);
 for(let test of [
 ()=>out.turns===64&&out.targets===12,
 ()=>out.rawNumbers===68&&out.rawNumbers===out.ordinaryNumbers+out.isolatedNumbers,
 ()=>out.numberPairEdgesOld===18888&&out.numberPairEdgesNew<=out.numberPairEdgesOld,
 ()=>t("下周五必须交").items.some(x=>x.kind==="WEEKDAY"&&x.detail.week==="下"&&x.detail.weekday===5&&x.detail.date===null),
 ()=>t("周五下午五点前提交").items.some(x=>x.kind==="CLOCK"&&x.detail.hour===5&&x.detail.partOfDay==="下午"&&x.detail.resolved===false)&&t("周五下午五点前提交").ordinary.length===0,
 ()=>t("九点前到").items.some(x=>x.kind==="CLOCK"&&x.detail.partOfDay===null),
 ()=>t("七十年代").items.some(x=>x.kind==="DECADE"&&x.detail.century===null)&&t("七十年代").ordinary.length===0,
 ()=>t("四周最多十小时").items.filter(x=>x.kind==="DURATION_OR_DAY_COUNT").length===2,
 ()=>t("三天迟到").ordinary.some(x=>x.value===3&&x.unit==="day")&&t("三天迟到").items.some(x=>x.kind==="DURATION_OR_DAY_COUNT"&&x.detail.role===null),
 ()=>t("七百").ordinary[0].unit===null,
 ()=>t("半天").items.some(x=>x.detail.value===0.5),
 ()=>t("周五十二分钟").ordinary.some(x=>x.value===12&&x.unit==="minute")||t("周五，十二分钟").ordinary.some(x=>x.value===12&&x.unit==="minute"),
 ()=>t("甲".repeat(129)).status==="LIMIT",
 ()=>out.rankImproved+out.rankWorsened+out.rankUnchanged===12
 ]){ck(test(),"control "+out.controls);out.controls++}
 return out
}
const A=load(docs);
const c=docs[0].content.split("```js\n")[1].split("\n```")[0];
const G=Function("L","R",c.slice(c.indexOf("function experiment(L,R,I")).split(" const metrics=()=>")[0]+"\nreturn {graph};\n}\nreturn experiment(L,R,null);");
const corpora=docs.slice(4).map(x=>JSON.parse(x.content)),assets=[{id:"L",sha:"be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb"},{id:"S",sha:"05c239f3f3b1f46235fa2464d2945c21c6c08132"}];
console.log(JSON.stringify(experiment(A.L,A.R,A.I,G,corpora,assets),null,2));
```
## 实测
```json
{
  "episodes": 32,
  "turns": 64,
  "rawNumbers": 68,
  "ordinaryNumbers": 58,
  "isolatedNumbers": 10,
  "temporalCandidates": 48,
  "kinds": {
    "RELATIVE_PERIOD": 14,
    "DURATION_OR_DAY_COUNT": 20,
    "WEEKDAY": 10,
    "DECADE": 1,
    "CLOCK": 3
  },
  "numberPairEdgesOld": 18888,
  "numberPairEdgesNew": 12423,
  "edges": 313700,
  "targets": 12,
  "oldHit20": 7,
  "newHit20": 7,
  "oldHit100": 10,
  "newHit100": 10,
  "rankImproved": 0,
  "rankWorsened": 0,
  "rankUnchanged": 12,
  "controls": 14,
  "rows": [
    {
      "id": "L03",
      "old": 814,
      "new": 814,
      "oldPairs": 0,
      "newPairs": 0
    },
    {
      "id": "L08",
      "old": 23,
      "new": 23,
      "oldPairs": 0,
      "newPairs": 0
    },
    {
      "id": "L15",
      "old": 146,
      "new": 146,
      "oldPairs": 0,
      "newPairs": 0
    },
    {
      "id": "S01",
      "old": 2,
      "new": 2,
      "oldPairs": 0,
      "newPairs": 0
    },
    {
      "id": "S02",
      "old": 12,
      "new": 12,
      "oldPairs": 1,
      "newPairs": 1
    },
    {
      "id": "S03",
      "old": 3,
      "new": 3,
      "oldPairs": 1,
      "newPairs": 0
    },
    {
      "id": "S04",
      "old": 1,
      "new": 1,
      "oldPairs": 1,
      "newPairs": 1
    },
    {
      "id": "S08",
      "old": 1,
      "new": 1,
      "oldPairs": 1,
      "newPairs": 1
    },
    {
      "id": "S10",
      "old": 1,
      "new": 1,
      "oldPairs": 0,
      "newPairs": 0
    },
    {
      "id": "S11",
      "old": 69,
      "new": 69,
      "oldPairs": 0,
      "newPairs": 0
    },
    {
      "id": "S12",
      "old": 22,
      "new": 22,
      "oldPairs": 1,
      "newPairs": 1
    },
    {
      "id": "S13",
      "old": 2,
      "new": 2,
      "oldPairs": 0,
      "newPairs": 0
    }
  ],
  "isolated": [
    {
      "id": "L04",
      "turn": 1,
      "removedFromBonus": [
        "五"
      ],
      "temporal": [
        {
          "raw": "下周五",
          "kind": "WEEKDAY",
          "detail": {
            "week": "下",
            "weekday": 5,
            "date": null
          }
        }
      ]
    },
    {
      "id": "L07",
      "turn": 2,
      "removedFromBonus": [
        "七十"
      ],
      "temporal": [
        {
          "raw": "七十年代",
          "kind": "DECADE",
          "detail": {
            "decade": 70,
            "century": null
          }
        }
      ]
    },
    {
      "id": "L17",
      "turn": 2,
      "removedFromBonus": [
        "五"
      ],
      "temporal": [
        {
          "raw": "周五",
          "kind": "WEEKDAY",
          "detail": {
            "week": null,
            "weekday": 5,
            "date": null
          }
        }
      ]
    },
    {
      "id": "S03",
      "turn": 1,
      "removedFromBonus": [
        "三",
        "五"
      ],
      "temporal": [
        {
          "raw": "周三",
          "kind": "WEEKDAY",
          "detail": {
            "week": null,
            "weekday": 3,
            "date": null
          }
        },
        {
          "raw": "周五",
          "kind": "WEEKDAY",
          "detail": {
            "week": null,
            "weekday": 5,
            "date": null
          }
        }
      ]
    },
    {
      "id": "S03",
      "turn": 2,
      "removedFromBonus": [
        "五",
        "五"
      ],
      "temporal": [
        {
          "raw": "周五",
          "kind": "WEEKDAY",
          "detail": {
            "week": null,
            "weekday": 5,
            "date": null
          }
        },
        {
          "raw": "周五",
          "kind": "WEEKDAY",
          "detail": {
            "week": null,
            "weekday": 5,
            "date": null
          }
        }
      ]
    },
    {
      "id": "S09",
      "turn": 2,
      "removedFromBonus": [
        "一"
      ],
      "temporal": [
        {
          "raw": "周一",
          "kind": "WEEKDAY",
          "detail": {
            "week": null,
            "weekday": 1,
            "date": null
          }
        }
      ]
    },
    {
      "id": "S10",
      "turn": 1,
      "removedFromBonus": [
        "五",
        "六"
      ],
      "temporal": [
        {
          "raw": "周五",
          "kind": "WEEKDAY",
          "detail": {
            "week": null,
            "weekday": 5,
            "date": null
          }
        },
        {
          "raw": "周六",
          "kind": "WEEKDAY",
          "detail": {
            "week": null,
            "weekday": 6,
            "date": null
          }
        }
      ]
    }
  ]
}
```
下一责任：将不同类型候选和实体/语义角色共同表示，重点研究真实文本属性识别与跨轮时间锚定；数据轨推进合法真实资料，独立轨保管未见样本，产品轨维护唯一交接。正式版本与训练另获授权。
