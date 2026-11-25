# 自主认知专项累计第128轮候选：口语数词省略、大数与比例尺度
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / RAW_NUMERAL_COMPOSITION / PUBLIC_SYNTHETIC_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 84b175e91cfad5e7e3f126b936c12b63c15f73d4。核对近12提交、13开放PR（#61待审）、v3.2前15行及历史全文、同步规程前20行、唯一交接前18行、R127前16行及实际图、R115前17行及源码、R62前16行、原L数值标注。R115已有0..9999规范数词，R62有ASCII倍率精确量，R127已定位缺口；本轮针对可组合中文数词、尺度和原文图增量，不重做类型比较、语义角色或训练。
## 固定资产
research/decision_hub/2026-11-25-open-span-quantity-composition-audit.md 175f8b48a4cc46cb3b41b7b65b13b06448bf461a
research/decision_hub/2026-11-25-unified-semantic-annotation-bridge.md af648d16ee96b9af4a3efb61b413d113208bb0ca
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
research/decision_hub/2026-11-25-temporal-quantity-candidate-separation.md 8a6b42f83b80283db6e215fe48f4fb2efbf8368c
research/decision_hub/2026-11-25-field-lineage-semantic-patch.md 307f8ba1291ec9ad83aca578bd5a02508d1e6110
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
R62 ada3d84a46e4d9a411ebf762884d13a5c5e87686；唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07。原资料及新夹具均为ChatGPT研发辅助原创公开合成开发材料，已见、非真人、独立留出或授权训练。
## 方法与边界
复用R115 parseNum/render及R117 ordinary，保留原候选完全不变。新增规范中文万级组合：非零高组1..9999乘10000加低组0..9999；低组非零且小于1000需零占位，10..19显式一十；通过规范回写验证低组，允许两到二的有限规范化。范围至99999999，不支持亿、混合阿拉伯位权、负数、小数、区间、近似、复杂语义和所有口语变体。省略规则：若合法前缀末位百/千/万后有一个非零数字，且前缀是该位权整数倍，给出前缀+该数字×下一低位权候选（如三千六=3600、一万六=16000、一千二百三=1230）。它是显式假设的有限口语解析候选，保留outside=true和原文，非确定的说话者意图；未建全可能歧义域，禁止自动采用、概率或虚构其他数值。规范三千零六为3006，不能混同。新增候选仅来自最大连续中文数字串，拒绝亿及指定邻接负号/小数/近似/混合数字、与旧词法候选或既有钟表/日期/年代重叠，范围外仍可能有旧词法误片段或新误解析（如未列出的语言环境），不宣称全量消除错误。相邻单位复用R115有限词表；省略币种不补，原始无单位量仍null。比例从已有percent候选派生同一原文的ratio有理数n/100及便于旧图对照的浮点value；两种尺度是同一个词法证据的等价表示，不得当两个独立事实、不据此推断概率或准确率含义。保留原始percent。无完整单位周期转换、否定零值、隐含量或跨句附着。R127 graph实际调用同一代码，仅替换数量输入，额外尺度表示可能增加图边及排序竞争；无生产预算、原生、真实语义确认、权威或执行许可。
## 实验
复用既有64轮167标注、28数值义务，按R127同值/同跨度口径比较旧新；新ratio视图只作数值候选，匹配不证明量纲或事实。所有旧候选逐项保留；没有完整负标注，不能证明误识别率未增加。新匹配无单位单列；剩余缺口完整记录。高组1..9999步长37×12低组构造规范算术对照，低组拼写使用旧render，非独立语言标准；9×9×3口语结构算术对照来自同一假设，非真实用语采样。21专项控制包括非法大数、数位差异、近似/负值、比例、时间隔离。所有规则、范围、样本和评估由研究者选择，同一研究者两路径、非独立验收。未训练、未新增第三方模型、Codex、CI、原生、PR合并、部署、费用或冻结变化。产品轨维护唯一交接。
## 复算
按上述八文件顺序置入docs[i].content，Node标准JS，仅执行已审查自有源码。
```js
function load(docs){
 const c=i=>docs[i].content.split("```js\n")[1].split("\n```")[0],a=c(0);
 const {I,S,T}=Function(a.split("function experiment(I,S,T,cases")[0]+"\nreturn load;")()(docs.slice(1));
 const L=Function(c(3).slice(c(3).indexOf("function experiment(A)")).split(" let out={corpusTurns:")[0]+"\nreturn {parseNum,render};\n}\nreturn experiment({});")();
 const makeGraph=T=>Function("S","T",a.slice(a.indexOf("function experiment(I,S,T,cases")).split(" const out={turns:")[0]+"\nreturn graph;\n}\nreturn experiment(null,S,T);")(S,T);
 return {I,T,L,makeGraph}
}
function experiment(I,T,L,makeGraph,corpora,assets){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),overlap=(a,b)=>a.start<b.end&&b.start<a.end,inside=(a,b)=>a.start>=b.start&&a.end<=b.end;
 const digit="零一二三四五六七八九",scale={百:100,千:1000,万:10000};
 function standard(s){
  if(!s.includes("万"))return L.parseNum(s);
  const p=s.split("万");if(p.length!==2||!p[0])return null;
  const high=L.parseNum(p[0]);if(high===null||high===0||/[0-9]/.test(s))return null;
  if(!p[1])return high*10000;
  const zero=p[1].startsWith("零"),tail=zero?p[1].slice(1):p[1];
  const norm=tail.startsWith("一十")?tail.slice(1):tail;
  const low=L.parseNum(norm);
  if(low===null||low===0||zero!==(low<1000))return null;
  const expected=(zero?"零":"")+(L.render(low).startsWith("十")?"一":"")+L.render(low);
  if(p[1].replace(/两/g,"二")!==expected)return null;
  return high*10000+low
 }
 function number(s){
  let v=standard(s);
  if(v!==null)return {value:v,kind:"CANONICAL",assumption:null};
  // Finite colloquial suffix: after an explicit hundreds/thousands/ten-thousands
  // position, a terminal nonzero digit denotes the next lower position.
  const m=/^(.+?[百千万])([一二三四五六七八九两])$/u.exec(s);
  if(!m)return null;
  const prefix=standard(m[1]),place=scale[m[1].at(-1)],d=digit.indexOf(m[2].replace("两","二"));
  if(prefix===null||prefix%place!==0||d<1)return null;
  return {value:prefix+d*place/10,kind:"COLLOQUIAL_ELLIPSIS",assumption:"terminal_digit_next_lower_place"};
 }
 const suffixes=[["分钟","minute"],["小时","hour"],["美元","USD"],["韩元","KRW"],["人民币","CNY"],["天","day"],["秒","second"],["个","count"],["套","count"],["次","count"],["成","tenth"],["%","percent"]];
 function extend(text){
  let t=T.temporal(text);
  if(t.status!=="CANDIDATES_ONLY")return t;
  let ordinary=t.ordinary.map(x=>({...x})),added=[],ratios=[];
  for(let m of text.matchAll(/[零一二三四五六七八九两十百千万亿]+/gu)){
   let raw=m[0],start=m.index,end=start+raw.length;
   if(/[亿]/u.test(raw)||/[万亿点.负\-0-9]/u.test(text[start-1]??"")||/[万亿点.来多0-9]/u.test(text[end]??""))continue;
   let n=number(raw);if(!n||n.kind==="CANONICAL"&&!raw.includes("万"))continue;
   let u=suffixes.find(([word])=>text.startsWith(word,end)),fullEnd=end+(u?.[0].length??0);
   // Do not reinterpret an unsupported large percentage or existing clock/date.
   if(u?.[1]==="tenth"||u?.[1]==="percent"||t.items.some(v=>["WEEKDAY","CLOCK","DECADE"].includes(v.kind)&&overlap(v,{start,end:fullEnd}))||t.raw.some(x=>overlap(x,{start,end:fullEnd})))continue;
   let q={start,end:fullEnd,numericEnd:end,raw:text.slice(start,fullEnd),value:n.value,unit:u?.[1]??null,kind:n.kind,assumption:n.assumption,authority:"NONE",outside:true};
   ordinary.push(q);added.push(q)
  }
  // Represent percentage and ratio as alternative exact scales of one lexical atom.
  for(let q of ordinary.filter(x=>x.unit==="percent")){
   ratios.push({...q,value:q.value/100,unit:"ratio",rational:{numerator:q.value,denominator:100},derivedFrom:{start:q.start,end:q.end,unit:"percent",value:q.value},kind:"EQUIVALENT_SCALE",authority:"NONE",outside:true})
  }
  ordinary.push(...ratios);ordinary.sort((a,b)=>a.start-b.start||a.end-b.end||+(a.kind==="EQUIVALENT_SCALE")- +(b.kind==="EQUIVALENT_SCALE"));
  return {...t,ordinary,added,ratios}
 }
 const oldG=makeGraph(T),newG=makeGraph({temporal:extend});
 const out={turns:0,annotations:0,obligations:0,oldValue:0,newValue:0,oldClaim:0,newClaim:0,oldTop20:0,newTop20:0,oldTop100:0,newTop100:0,oldQuantities:0,newRepresentations:0,newNumericSpans:0,newRatioViews:0,oldClaimEdges:0,newClaimEdges:0,oldMetricEdges:0,newMetricEdges:0,oldCandidatesPreserved:0,newWithoutUnit:0,recovered:[],remaining:[],regressions:[],canonicalChecks:0,ellipsisChecks:0,controls:0};
 for(let d=0;d<2;d++){
  const ir=I.build(corpora[d],assets[d]);ck(I.verify(ir,corpora[d],assets[d]),"IR");
  for(let ep of ir.episodes)for(let t of ep.turns){
   let a=T.temporal(t.text),b=extend(t.text),g=oldG(t.text),h=newG(t.text);
   ck(g.status==="CANDIDATES_ONLY"&&h.status==="CANDIDATES_ONLY","graph");
   out.turns++;out.oldQuantities+=a.ordinary.length;out.newRepresentations+=b.ordinary.length;out.newNumericSpans+=b.added.length;out.newRatioViews+=b.ratios.length;
   out.oldClaimEdges+=g.claims.length;out.newClaimEdges+=h.claims.length;out.oldMetricEdges+=g.metrics.length;out.newMetricEdges+=h.metrics.length;
   for(let q of a.ordinary){ck(b.ordinary.some(x=>eq(x,q)),"old candidate");out.oldCandidatesPreserved++}
   for(let q of [...b.added,...b.ratios])ck(t.text.slice(q.start,q.end)===q.raw&&q.authority==="NONE"&&q.outside,"anchor");
   for(let item of t.items){
    out.annotations++;
    for(let k of ["value","lower","upper"]){
     let f=item.dimensions[k];if(f.status!=="ANNOTATED"||typeof f.value!=="number")continue;
     let v=f.value;out.obligations++;
     let has=q=>inside(q,item.span)&&q.value===v,old=a.ordinary.some(has),now=b.ordinary.filter(has);
     const rank=z=>z.claims.findIndex(e=>e.span.start===item.span.start&&e.span.end===item.span.end&&e.q.value===v)+1;
     let ro=rank(g),rn=rank(h);
     out.oldValue+=+old;out.newValue+=+(now.length>0);out.oldClaim+=+(ro>0);out.newClaim+=+(rn>0);
     out.oldTop20+=+(ro>0&&ro<=20);out.newTop20+=+(rn>0&&rn<=20);out.oldTop100+=+(ro>0&&ro<=100);out.newTop100+=+(rn>0&&rn<=100);
     if(old&&!now.length)out.regressions.push(item.id+":"+k);
     if(!old&&now.length){out.newWithoutUnit+=+now.every(q=>q.unit===null);out.recovered.push({id:item.id,quote:item.span.text,value:v,representations:now.map(q=>({raw:q.raw,unit:q.unit,kind:q.kind,assumption:q.assumption??null})),claimRank:rn||null})}
     if(!now.length)out.remaining.push({id:item.id,quote:item.span.text,value:v})
    }
   }
  }
 }
 // Generated canonical arithmetic checks independent of parsing implementation.
 for(let high=1;high<=9999;high+=37)for(let low of [0,1,9,10,19,99,100,101,999,1000,1001,9999]){
  let tail=low?L.render(low):"",s=L.render(high)+"万"+(low&&low<1000?"零":"")+(tail.startsWith("十")?"一":"")+tail;
  ck(number(s)?.value===high*10000+low&&number(s)?.kind==="CANONICAL","canonical "+s);out.canonicalChecks++
 }
 for(let d=1;d<=9;d++)for(let e=1;e<=9;e++)for(let p of ["百","千","万"]){
  let s=digit[d]+p+digit[e],n=number(s);
  ck(n?.kind==="COLLOQUIAL_ELLIPSIS"&&n.value===d*scale[p]+e*scale[p]/10,"ellipsis "+s);out.ellipsisChecks++
 }
 for(let test of [()=>out.turns===64&&out.annotations===167&&out.obligations===28,()=>out.oldValue===16&&out.oldClaim===15,()=>out.oldQuantities===58&&out.oldClaimEdges===1028&&out.oldMetricEdges===1398,()=>out.newValue>=out.oldValue&&out.regressions.length===0,()=>number("一万零六")?.value===10006,()=>number("一万六")?.value===16000,()=>number("三千零六")?.value===3006,()=>number("三千六")?.value===3600,()=>number("一千二百三")?.value===1230,()=>number("一万万")===null,()=>number("一万零二千")===null,()=>number("一万二百")===null,()=>extend("负三千六").added.length===0,()=>extend("三千六点五").added.length===0,()=>extend("六万多").added.length===0,()=>extend("一亿六万").added.length===0,()=>extend("六万").added[0]?.unit===null,()=>extend("八成").ratios[0]?.rational.numerator===80&&extend("八成").ratios[0]?.value===0.8,()=>extend("周五下午五点").ordinary.length===0,()=>extend("字".repeat(129)).status==="LIMIT",()=>newG("陌生指标三千六").claims.length>0]){ck(test(),"control "+out.controls);out.controls++}
 return out
}
const {I,T,L,makeGraph}=load(docs);console.log(JSON.stringify(experiment(I,T,L,makeGraph,docs.slice(6).map(x=>JSON.parse(x.content)),docs.slice(6).map((x,i)=>({id:i?"S":"L",sha:x.sha}))),null,2));
```
## 实测
```json
{
  "turns": 64,
  "annotations": 167,
  "obligations": 28,
  "oldValue": 16,
  "newValue": 25,
  "oldClaim": 15,
  "newClaim": 24,
  "oldTop20": 15,
  "newTop20": 23,
  "oldTop100": 15,
  "newTop100": 24,
  "oldQuantities": 58,
  "newRepresentations": 68,
  "newNumericSpans": 7,
  "newRatioViews": 3,
  "oldClaimEdges": 1028,
  "newClaimEdges": 1161,
  "oldMetricEdges": 1398,
  "newMetricEdges": 1608,
  "oldCandidatesPreserved": 58,
  "newWithoutUnit": 7,
  "recovered": [
    {
      "id": "L01.1.3",
      "quote": "房租三千六",
      "value": 3600,
      "representations": [
        {
          "raw": "三千六",
          "unit": null,
          "kind": "COLLOQUIAL_ELLIPSIS",
          "assumption": "terminal_digit_next_lower_place"
        }
      ],
      "claimRank": 2
    },
    {
      "id": "L01.2.1",
      "quote": "停车每月四百五",
      "value": 450,
      "representations": [
        {
          "raw": "四百五",
          "unit": null,
          "kind": "COLLOQUIAL_ELLIPSIS",
          "assumption": "terminal_digit_next_lower_place"
        }
      ],
      "claimRank": 1
    },
    {
      "id": "L10.1.4",
      "quote": "当时大概觉得八成",
      "value": 0.8,
      "representations": [
        {
          "raw": "八成",
          "unit": "ratio",
          "kind": "EQUIVALENT_SCALE",
          "assumption": null
        }
      ],
      "claimRank": 24
    },
    {
      "id": "L12.1.1",
      "quote": "厨房想留六万",
      "value": 60000,
      "representations": [
        {
          "raw": "六万",
          "unit": null,
          "kind": "CANONICAL",
          "assumption": null
        }
      ],
      "claimRank": 11
    },
    {
      "id": "L12.1.2",
      "quote": "卫生间也得留六万",
      "value": 60000,
      "representations": [
        {
          "raw": "六万",
          "unit": null,
          "kind": "CANONICAL",
          "assumption": null
        }
      ],
      "claimRank": 2
    },
    {
      "id": "L12.1.3",
      "quote": "两项加起来只能十万",
      "value": 100000,
      "representations": [
        {
          "raw": "十万",
          "unit": null,
          "kind": "CANONICAL",
          "assumption": null
        }
      ],
      "claimRank": 4
    },
    {
      "id": "L12.2.1",
      "quote": "两个都必须至少六万",
      "value": 60000,
      "representations": [
        {
          "raw": "六万",
          "unit": null,
          "kind": "CANONICAL",
          "assumption": null
        }
      ],
      "claimRank": 2
    },
    {
      "id": "L14.1.1",
      "quote": "同事说这家公司奖金一般两万",
      "value": 20000,
      "representations": [
        {
          "raw": "两万",
          "unit": null,
          "kind": "CANONICAL",
          "assumption": null
        }
      ],
      "claimRank": 2
    },
    {
      "id": "L17.1.2",
      "quote": "八成把握这次准时",
      "value": 0.8,
      "representations": [
        {
          "raw": "八成",
          "unit": "ratio",
          "kind": "EQUIVALENT_SCALE",
          "assumption": null
        }
      ],
      "claimRank": 13
    }
  ],
  "remaining": [
    {
      "id": "L02.1.2",
      "quote": "只要夜班我就不去",
      "value": 0
    },
    {
      "id": "L02.2.1",
      "quote": "一次都不能有",
      "value": 0
    },
    {
      "id": "L04.1.4",
      "quote": "提前做完没奖",
      "value": 0
    }
  ],
  "regressions": [],
  "canonicalChecks": 3252,
  "ellipsisChecks": 243,
  "controls": 21
}
```
后续：独立量纲、币种与周期的来源组合，以及否定/隐含零的语义逻辑；优先验证真实样本，不以本语料覆盖率当最终准确率。正式开发、训练另获授权。
