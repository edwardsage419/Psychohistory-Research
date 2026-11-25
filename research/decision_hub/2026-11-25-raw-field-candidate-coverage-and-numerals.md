# 自主认知专项累计第115轮候选：原文字段覆盖审计与组合中文数量词法
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / RAW_TEXT_LEXICAL_CANDIDATES / PUBLIC_SYNTHETIC_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 7be37e102e3e636c148ff45e3aa05c6e0885be81。核对近期12提交、13开放PR（#61待审）、v3.2前15行及历史全文、唯一交接前18行、R114前20行与全文、R104/R77/R82前段及实际代码、R62实际parse、R74实际scan。区别R104严格数量图接口、R77全语料边搜索和R114手工字段修订：本轮在R114实际5例上对照原始候选覆盖，新增有限可组合中文整数词法，另在既有64轮语料执行原句词法及原R62严格数量候选扫描。
## 固定资产
research/decision_hub/2026-11-25-field-lineage-semantic-patch.md 307f8ba1291ec9ad83aca578bd5a02508d1e6110
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-25-raw-text-reference-search.md 16075b3ba567ee6dc3496300beab1417172a6c42
research/decision_hub/2026-11-25-typed-quantity-compositional-atoms.md ada3d84a46e4d9a411ebf762884d13a5c5e87686
research/decision_hub/2026-11-25-unified-quantity-candidate-interface.md d15592a912a7a15df3fb19b045e530c4b0d315cc
research/decision_hub/2026-11-25-compositional-concept-provenance-bridge.md 71638778d5b2898ace849285d93aa682f61554ba
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
唯一交接 5e74f4f0b37141d631740e844ad8bbbfed232e07。两个语料及R114人工属性为ChatGPT研发辅助原创公开合成开发材料，已见、非真人、训练或独立留出。
## 方法与边界
parseNum使用十进制位权组合、标准形式回写确认，范围0..9999整数，支持两替换为二的有限规范化。首次运行canonical inverse断言失败，未写入；中间零占位被错误当作连续数位，修正后重新全量往返。第二次增加有限邻接防截断控制，拒绝若干万亿/小数/近似/负号片段；这不是完整语义或对抗保护。lexical按最长连续数字字符片段生成候选，查看紧邻有限单位后缀；九成按九个十分之一转90百分比，非概率或事实；隐含货币不默认人民币。词法仍可能截断复杂表达或把词汇、序数、日期、被否定条件当候选。未支持完整中文数量、大小数、负数、区间、相对数量、时间语义、合计、跨币种、换算。输出始终outside=true/authority NONE，不能直接当作完整量、数学输入或修订。规范整数往返同作者算法验证有限一致性，非独立语言准确率。
R114人工字段初始和修订均计（不同于最终25字段）。角色锚用R74每角色前50精确跨度，概念锚用R82有限词典全5位来源及最长8字子串，来源是假定；引用用R77每轮100跨度端点、允许一处内部标点，核对标注目标边前20/100。R62严格量原算法独立按周期枚举子串。词法候选数与严格类型原子数不具同等语义，不能作为准确率比较。人工字段仅在生成后对照，词法设计已知样例，非未见泛化。数值字段匹配仅允许同起点及数值子跨度或带紧邻单位的全跨度且值相等；不证明指标、单位、主体、边界和修订对象。角色/概念锚不命中仍可能有包含跨度或其他表达，命中不证明属性语义。无完整负例所以未测precision。未执行R114 revise、原生C028、真实用户、完整义务、设备性能或独立验收。整数域、后缀、预算和匹配规则为研究者选择，未获产品政策确认。无训练、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。
## 复算
按上述八份固定源码及JSON顺序读取docs[i].content，Node标准JS。仅加载已审查自有代码，不执行任意外部文档。
```js
function load(docs){
 const code=i=>docs[i].content.split("```js\n")[1].split("\n```")[0];
 function f(i,marker,names,entry="experiment"){const s=code(i),start=s.indexOf(entry==="probe"?"const probe = function()":"function experiment(");return Function(s.slice(start).split(marker)[0]+"\nreturn {"+names+"};\n}"+(entry==="probe"?";":"")+"\nreturn "+entry+"();")()}
 return {cases:JSON.parse(code(0).split("const cases=")[1].split(";\n")[0]),S:f(1," const blank=()=>","scan"),R:f(2," const pos=","search"),Q:f(3," const groups=","parse,periods","probe"),C:f(5," // Independent expected mapping","candidates"),corpora:docs.slice(6).map(x=>JSON.parse(x.content))}
}
function experiment(A){
 const {cases,S,R,Q,C,corpora}=A,ck=(x,m)=>{if(!x)throw Error(m)};
 const digit="零一二三四五六七八九",powers=["","十","百","千"];
 function render(n){if(n===0)return "零";let s="",zero=false;for(let k=3;k>=0;k--){let x=Math.floor(n/10**k)%10;if(x){if(zero&&s)s+="零";if(!(k===1&&x===1&&!s))s+=digit[x];s+=powers[k];zero=false}else if(s)zero=true}return s}
 function parseNum(s){
  if(/^(?:0|[1-9][0-9]{0,3})$/.test(s))return +s;
  const normalized=s.replace(/两/g,"二");let n=0,part=0,last=10000,prev=false;
  if(!normalized)return null;
  if(normalized==="零")return 0;
  for(let c of normalized){if(c==="零"){if(prev)return null;continue}
   let d=digit.indexOf(c);if(d>=1){if(prev)return null;part=d;prev=true;continue}
   let k=powers.indexOf(c);if(k<1)return null;let scale=10**k;if(scale>=last)return null;n+=(prev?part:1)*scale;part=0;prev=false;last=scale}
  n+=part;return n>=0&&n<=9999&&render(n)===normalized?n:null
 }
 const suffixes=[["分钟","minute"],["小时","hour"],["美元","USD"],["韩元","KRW"],["人民币","CNY"],["天","day"],["秒","second"],["个","count"],["套","count"],["次","count"],["成","tenth"],["%","percent"]];
 function lexical(s){
  if(typeof s!=="string"||s.length>128)return {status:"LIMIT",items:[]};
  const items=[];
  for(let m of s.matchAll(/[零一二三四五六七八九两十百千]+|[0-9]+/gu)){
   let n=parseNum(m[0]);if(n===null)continue;
   let start=m.index,end=start+m[0].length,u=suffixes.find(([word])=>s.startsWith(word,end));
   // Avoid known unsupported compound magnitude/approximation/decimal fragments.
   if(/[万亿点.负\-]/u.test(s[start-1]??"")||/[万亿点.来多]/u.test(s[end]??""))continue;
   if(u?.[1]==="tenth"&&n>10)continue;
   items.push({start,end:u?end+u[0].length:end,numericEnd:end,raw:s.slice(start,u?end+u[0].length:end),value:u?.[1]==="tenth"?n*10:n,unit:u?.[1]==="tenth"?"percent":u?.[1]??null,authority:"NONE",outside:true})
  }
  return {status:"CANDIDATES_ONLY",items}
 }
 let out={corpusTurns:0,lexicalCandidates:0,unitKnown:0,unitUnknown:0,strictQuantityCandidates:0,fieldCases:0,fields:0,roleAnchorTop50:0,conceptAnchor:0,numberFields:0,numberLexicalMatches:0,numberUnitsMissing:0,referenceCases:0,referenceTop20:0,referenceTop100:0,referenceLimit:0,controls:0,rows:[]};
 for(let d of corpora)for(let e of d.cases)for(let t of e.turns){let z=lexical(t.text);ck(z.status==="CANDIDATES_ONLY","corpus limit");out.corpusTurns++;out.lexicalCandidates+=z.items.length;out.unitKnown+=z.items.filter(x=>x.unit!==null).length;out.unitUnknown+=z.items.filter(x=>x.unit===null).length;
  for(let i=0;i<t.text.length;i++)if(Object.keys(Q.periods).some(p=>t.text.startsWith(p,i)))for(let j=i+1;j<=t.text.length;j++)out.strictQuantityCandidates+=+(Q.parse(t.text.slice(i,j)).status==="CANDIDATE");
 }
 for(let c of cases){
  let e=corpora[1].cases.find(x=>x.id===c.id),a=e.turns[0],b=e.turns[1];
  let records=[a,b].map(t=>({text:t.text,scan:S.scan(t.text),lex:lexical(t.text).items,concepts:[]}));
  for(let r of records)for(let i=0;i<r.text.length;i++)for(let j=i+1;j<=Math.min(r.text.length,i+8);j++)r.concepts.push(...C.candidates(r.text.slice(i,j),31,i).records);
  out.fieldCases++;let details=[];
  for(let [i,m] of [[0,c.initial],[1,c.patch]])for(let [field,[value,quote]] of Object.entries(m)){
   let r=records[i],start=r.text.indexOf(quote),end=start+quote.length;ck(start>=0&&start===r.text.lastIndexOf(quote),"gold");
   let role=Object.values(r.scan.ranked).some(v=>v.slice(0,50).some(x=>x.start===start&&x.end===end)),concept=r.concepts.some(x=>x.span[0]===start&&x.span[1]===end);
   out.fields++;out.roleAnchorTop50+=+role;out.conceptAnchor+=+concept;
   let number=null;if(field==="value"){out.numberFields++;number=r.lex.find(x=>x.start===start&&(x.end===end||x.numericEnd===end)&&x.value===value)??null;if(number){out.numberLexicalMatches++;out.numberUnitsMissing+=+(number.unit===null)}}
   details.push({turn:i+1,field,quote,roleAnchor:role,conceptAnchor:concept,number})
  }
  const old=a.proposal.claims[+c.old.split(".").at(-1)-1].quote,edit=b.proposal.claims[+c.edit.split(".").at(-1)-1].quote;
  const z=R.search(a.text,b.text,100,true);let rank=z.edges.findIndex(x=>x.a.start===a.text.indexOf(old)&&x.a.text===old&&x.b.start===b.text.indexOf(edit)&&x.b.text===edit)+1;
  out.referenceCases++;out.referenceLimit+=+(z.status==="LIMIT");out.referenceTop20+=+(rank>0&&rank<=20);out.referenceTop100+=+(rank>0&&rank<=100);out.rows.push({id:c.id,referenceRank:rank||null,referenceStatus:z.status,details})
 }
 for(let n=0;n<10000;n++)ck(parseNum(render(n))===n,"canonical inverse "+n);
 for(let [s,n] of [["十二",12],["两",2],["五百",500],["九千九百九十九",9999],["一百零二",102],["二十",20],["十",10],["一百二",null],["一千二",null],["十十",null],["零零",null],["百",null]]){ck(parseNum(s)===n,"numeric "+s);out.controls++}
 for(let t of [()=>lexical("九成").items[0].value===90,()=>lexical("十二分钟").items[0].unit==="minute",()=>lexical("七百").items[0].unit===null,()=>lexical("一百二").items.length===0,()=>lexical("甲".repeat(129)).status==="LIMIT",()=>out.corpusTurns===64,()=>out.numberFields===9,()=>out.strictQuantityCandidates===0,()=>out.rows.every(r=>r.details.every(d=>d.number===null||d.number.authority==="NONE")),()=>["三万","十来","1.5","负三","-3"].every(s=>lexical(s).items.length===0)]){ck(t(),"control");out.controls++}
 out.canonicalRoundTrips=10000;return out
}
console.log(JSON.stringify(experiment(load(docs)),null,2));
```
## 实测
```json
{
  "corpusTurns": 64,
  "lexicalCandidates": 68,
  "unitKnown": 39,
  "unitUnknown": 29,
  "strictQuantityCandidates": 0,
  "fieldCases": 5,
  "fields": 32,
  "roleAnchorTop50": 5,
  "conceptAnchor": 0,
  "numberFields": 9,
  "numberLexicalMatches": 9,
  "numberUnitsMissing": 2,
  "referenceCases": 5,
  "referenceTop20": 3,
  "referenceTop100": 5,
  "referenceLimit": 0,
  "controls": 22,
  "rows": [
    {
      "id": "S02",
      "referenceRank": 21,
      "referenceStatus": "CANDIDATES_ONLY",
      "details": [
        {
          "turn": 1,
          "field": "metric",
          "quote": "离车站步行",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 1,
          "field": "role",
          "quote": "必须",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 1,
          "field": "relation",
          "quote": "以内",
          "roleAnchor": true,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 1,
          "field": "value",
          "quote": "十五",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": {
            "start": 23,
            "end": 27,
            "numericEnd": 25,
            "raw": "十五分钟",
            "value": 15,
            "unit": "minute",
            "authority": "NONE",
            "outside": true
          }
        },
        {
          "turn": 1,
          "field": "unit",
          "quote": "分钟",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 1,
          "field": "scope",
          "quote": "任何一套",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 2,
          "field": "value",
          "quote": "十二",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": {
            "start": 6,
            "end": 10,
            "numericEnd": 8,
            "raw": "十二分钟",
            "value": 12,
            "unit": "minute",
            "authority": "NONE",
            "outside": true
          }
        }
      ]
    },
    {
      "id": "S04",
      "referenceRank": 1,
      "referenceStatus": "CANDIDATES_ONLY",
      "details": [
        {
          "turn": 1,
          "field": "metric",
          "quote": "空插座",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 1,
          "field": "value",
          "quote": "一个",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": {
            "start": 28,
            "end": 30,
            "numericEnd": 29,
            "raw": "一个",
            "value": 1,
            "unit": "count",
            "authority": "NONE",
            "outside": true
          }
        },
        {
          "turn": 1,
          "field": "modality",
          "quote": "家里只有",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 2,
          "field": "value",
          "quote": "两个",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": {
            "start": 8,
            "end": 10,
            "numericEnd": 9,
            "raw": "两个",
            "value": 2,
            "unit": "count",
            "authority": "NONE",
            "outside": true
          }
        },
        {
          "turn": 2,
          "field": "modality",
          "quote": "刚核实",
          "roleAnchor": true,
          "conceptAnchor": false,
          "number": null
        }
      ]
    },
    {
      "id": "S08",
      "referenceRank": 1,
      "referenceStatus": "CANDIDATES_ONLY",
      "details": [
        {
          "turn": 1,
          "field": "metric",
          "quote": "迟到",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 1,
          "field": "value",
          "quote": "三天",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": {
            "start": 14,
            "end": 16,
            "numericEnd": 15,
            "raw": "三天",
            "value": 3,
            "unit": "day",
            "authority": "NONE",
            "outside": true
          }
        },
        {
          "turn": 1,
          "field": "unit",
          "quote": "天",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 1,
          "field": "period",
          "quote": "上个月",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 1,
          "field": "modality",
          "quote": "实际",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 2,
          "field": "value",
          "quote": "两天",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": {
            "start": 10,
            "end": 12,
            "numericEnd": 11,
            "raw": "两天",
            "value": 2,
            "unit": "day",
            "authority": "NONE",
            "outside": true
          }
        },
        {
          "turn": 2,
          "field": "modality",
          "quote": "实际",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        }
      ]
    },
    {
      "id": "S12",
      "referenceRank": 79,
      "referenceStatus": "CANDIDATES_ONLY",
      "details": [
        {
          "turn": 1,
          "field": "metric",
          "quote": "修旧相机",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 1,
          "field": "value",
          "quote": "五百",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": {
            "start": 6,
            "end": 8,
            "numericEnd": 8,
            "raw": "五百",
            "value": 500,
            "unit": null,
            "authority": "NONE",
            "outside": true
          }
        },
        {
          "turn": 1,
          "field": "modality",
          "quote": "大约",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 2,
          "field": "value",
          "quote": "七百",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": {
            "start": 5,
            "end": 7,
            "numericEnd": 7,
            "raw": "七百",
            "value": 700,
            "unit": null,
            "authority": "NONE",
            "outside": true
          }
        },
        {
          "turn": 2,
          "field": "modality",
          "quote": "维修店说",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 2,
          "field": "evidenceLimit",
          "quote": "还没有书面报价",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        }
      ]
    },
    {
      "id": "S13",
      "referenceRank": 2,
      "referenceStatus": "CANDIDATES_ONLY",
      "details": [
        {
          "turn": 1,
          "field": "metric",
          "quote": "准确率必须",
          "roleAnchor": true,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 1,
          "field": "role",
          "quote": "必须",
          "roleAnchor": true,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 1,
          "field": "relation",
          "quote": "不低于",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 1,
          "field": "value",
          "quote": "九成",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": {
            "start": 24,
            "end": 26,
            "numericEnd": 25,
            "raw": "九成",
            "value": 90,
            "unit": "percent",
            "authority": "NONE",
            "outside": true
          }
        },
        {
          "turn": 1,
          "field": "unit",
          "quote": "九成",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 2,
          "field": "scope",
          "quote": "正式交付",
          "roleAnchor": false,
          "conceptAnchor": false,
          "number": null
        },
        {
          "turn": 2,
          "field": "exclusion",
          "quote": "试验阶段不套用这个底线",
          "roleAnchor": true,
          "conceptAnchor": false,
          "number": null
        }
      ]
    }
  ],
  "canonicalRoundTrips": 10000
}
```
后续：优先数量与实体/约束绑定及真实语料准备，保留未支持、歧义、否定及未确认状态。独立轨留出未见案例，产品轨维护唯一交接。正式版本与训练仍需授权。
