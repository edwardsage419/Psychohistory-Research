# 自主认知专项累计第129轮候选：数值、单位、周期及独立证据组合
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / SYNTHETIC_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 4f22cc0d3ca2f7e18993f9b5543e2159971fb3c0。核对近期12提交、13开放PR（#61待审）、v3.2前15行及历史全文、同步规程前17行、唯一交接前18行、R128前16行与实际代码、R62/R54前12行。R62已有严格ASCII类型量与精确比较，R54有共享参数资格，本轮复用R128中文候选并新增有限周期词面候选、分别确认四类证据及撤回控制，非重新实现通用量纲系统或训练。
## 固定资产
research/decision_hub/2026-11-25-colloquial-numeral-magnitude-ratio-candidates.md f6684299a3720a533e44343b123edff085c7ee05
research/decision_hub/2026-11-25-open-span-quantity-composition-audit.md 175f8b48a4cc46cb3b41b7b65b13b06448bf461a
research/decision_hub/2026-11-25-unified-semantic-annotation-bridge.md af648d16ee96b9af4a3efb61b413d113208bb0ca
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
research/decision_hub/2026-11-25-temporal-quantity-candidate-separation.md 8a6b42f83b80283db6e215fe48f4fb2efbf8368c
research/decision_hub/2026-11-25-field-lineage-semantic-patch.md 307f8ba1291ec9ad83aca578bd5a02508d1e6110
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
R62 ada3d84a46e4d9a411ebf762884d13a5c5e87686；R54 412a98c4bd335864a32f27aa796fc8a42414e7f4；唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07。无新外部数据或资料；已有单位换算沿R62，未重审标准。
## 合同
R128 extend提供原文数值候选，保持缺单位null及等价尺度身份。有限周期词面在同标点范围与数量候选关联，可能多个，不能证明实际附着关系；四周仅词面候选，并非已知四周统计周期。每月、上个月、四周不能凭词面互换，未实现实际日期区间。所有候选authority NONE、outside true。normalize单独接受可信宿主确认的值、单位、聚合周期及明确窗口身份、指标身份，四源版本均需匹配当前active；缺任一拒绝，原文显式单位与确认值冲突拒绝，原无单位只能由外部独立确认补全。没有真实鉴权、字段与原文绑定证书、数据存储、来源覆盖、跨端事务或真用户确认，人工记录仅作数学输入模拟。原文候选扫描与人工确认输入是两个分离的研究阶段，本轮未建立从候选到可信事实的自动转换。固定9类单位及ratio，秒/分/时可按整数换算，百分比及比例按有理数表示；天作为独立日计数，不转成24小时，货币代码各自独立，不做汇率或跨周期换算。以BigInt交叉乘法比较同维度、基础单位、周期、窗口、指标身份，非原生C028。窗口及指标标识由外部给定，相等不代表真实事实资格。normalize未实现全面恶意输入验证，compare仅接受本次合格投影，旧投影必须重新核验，不能直接缓存用于撤权后判断。无概率、现实建议或执行权。
## 实验
已有64轮167标注的28数值义务，沿R128同值与原跨度口径；显式unit字符串相等、有限别名、全无单位、其余（含无标注或复合单位）分别统计，周期只计同标注跨度内关联候选，不等同正确附着；不以标注单位补充原文。9×9单位、3×3周期、3×3整数值、同异窗口、同异指标=26244组精确比较；直接数值算术参照与明确兼容关系核验，均同研究者、非独立验收。百分比与ratio额外等价控制。8源逐项撤回及8旧版本拦截，14专项控制。所有数据为ChatGPT研发辅助原创公开合成开发资料，非真人、独立留出或授权训练。研究者选择词表、单位兼容、版本及周期合同；没有真实设备、实际运行性能或全请求资源防护。无训练、Codex、CI、原生、PR合并、部署、费用或冻结变化。产品轨维护唯一交接。
## 复算
按上述九份文件顺序置入docs[i].content，Node标准JS，仅执行已审查自有源码。
```js
function load(docs){
 const c=docs[0].content.split("```js\n")[1].split("\n```")[0];
 const A=Function(c.split("function experiment(I,T,L,makeGraph,corpora,assets)")[0]+"\nreturn load;")()(docs.slice(1));
 const E=Function("I","T","L","makeGraph",c.slice(c.indexOf("function experiment(I,T,L,makeGraph,corpora,assets)")).split(" const oldG=makeGraph(T)")[0]+"\nreturn {extend};\n}\nreturn experiment(I,T,L,makeGraph);")(A.I,A.T,A.L,A.makeGraph);
 return {...A,E}
}
function experiment(I,E,corpora,assets){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),inside=(a,b)=>a.start>=b.start&&a.end<=b.end;
 const units={USD:["money","USD",1,1],CNY:["money","CNY",1,1],KRW:["money","KRW",1,1],second:["duration","second",1,1],minute:["duration","second",60,1],hour:["duration","second",3600,1],day:["day_count","day",1,1],count:["count","count",1,1],percent:["ratio","ratio",1,100],ratio:["ratio","ratio",1,1]};
 function scan(text){
  let z=E.extend(text);if(z.status!=="CANDIDATES_ONLY")return {status:"LIMIT",numbers:[],periods:[],authority:"NONE"};
  const periods=[];
  for(let m of text.matchAll(/每月|每周|每天|每年|四周|上个月|下个月|这个月|本月/gu))periods.push({start:m.index,end:m.index+m[0].length,raw:m[0],kind:({"每月":"month_rate","每周":"week_rate","每天":"day_rate","每年":"year_rate","四周":"four_week_window","上个月":"previous_month","下个月":"next_month","这个月":"current_month","本月":"current_month"})[m[0]],authority:"NONE",outside:true});
  let numbers=z.ordinary.map(q=>({...q,periodCandidates:periods.filter(p=>!/[，。；！？、,;.!?]/u.test(text.slice(Math.min(p.start,q.start),Math.max(p.end,q.end))))}));
  return {status:"CANDIDATES_ONLY",numbers,periods,authority:"NONE",outside:true}
 }
 // Trusted fixture records: explicit, separately confirmed unit/horizon/identity,
 // each with independent current source version. No text-derived permission.
 function normalize(q,u,h,id,active){
  if(!q||!u||!h||!id||![q,u,h,id].every(x=>x.confirmed===true&&active.get(x.source)===x.version)||!Object.hasOwn(units,u.value)||!["total","month_rate","week_rate","year_rate","day_rate","four_week_window"].includes(h.value)||typeof h.window!=="string"||!h.window||typeof id.value!=="string"||!id.value)return null;
  if(q.unit!==null&&q.unit!==u.value)return null;
  let [dim,base,n,d]=units[u.value],num,den;
  if(q.unit==="ratio"){if(!q.rational||!Number.isSafeInteger(q.rational.numerator)||q.rational.denominator!==100||q.rational.numerator/100!==q.value)return null;num=BigInt(q.rational.numerator);den=100n}
  else {if(!Number.isSafeInteger(q.value)||q.value<0)return null;num=BigInt(q.value);den=1n}
  return {n:(num*BigInt(n)).toString(),d:(den*BigInt(d)).toString(),dim,base,period:h.value,window:h.window,identity:id.value,deps:[q,u,h,id].map(x=>[x.source,x.version]),authority:"NONE"}
 }
 function compare(a,b){
  if(!a||!b||["dim","base","period","window","identity"].some(k=>a[k]!==b[k]))return "UNKNOWN";
  let x=BigInt(a.n)*BigInt(b.d),y=BigInt(b.n)*BigInt(a.d);return x<y?"LT":x>y?"GT":"EQ"
 }
 const out={turns:0,obligations:0,valueCovered:0,explicitUnitExact:0,aliasUnitExact:0,missingUnit:0,otherUnit:0,periodTokens:0,matchedWithPeriodCandidate:0,periodRows:[],mathPairs:0,comparable:0,unknown:0,rawNumberWrong:0,sourceWithdrawalChecks:0,staleVersionChecks:0,controls:0};
 for(let d=0;d<2;d++){
  let ir=I.build(corpora[d],assets[d]);ck(I.verify(ir,corpora[d],assets[d]),"IR");
  for(let e of ir.episodes)for(let t of e.turns){
   let z=scan(t.text);out.turns++;out.periodTokens+=z.periods.length;
   for(let a of t.items)for(let k of ["value","lower","upper"]){
    let f=a.dimensions[k];if(f.status!=="ANNOTATED"||typeof f.value!=="number")continue;out.obligations++;
    let ms=z.numbers.filter(q=>inside(q,a.span)&&q.value===f.value);if(!ms.length)continue;out.valueCovered++;
    let u=a.dimensions.unit.value;
    if(ms.some(q=>q.unit!==null&&q.unit===u))out.explicitUnitExact++;
    else if(ms.some(q=>q.unit!==null&&({min:"minute",h:"hour",s:"second"})[u]===q.unit))out.aliasUnitExact++;
    else if(ms.every(q=>q.unit===null))out.missingUnit++;
    else out.otherUnit++;
    let ps=ms.flatMap(q=>q.periodCandidates.filter(p=>inside(p,a.span)));
    if(ps.length){out.matchedWithPeriodCandidate++;out.periodRows.push({id:a.id,quote:a.span.text,unit:u??null,periods:[...new Set(ps.map(x=>x.raw))]})}
   }
  }
 }
 const mk=(x,source)=>({...x,source,version:1,confirmed:true});
 const record=(value,unit,period,window,identity,prefix)=>[mk({value,unit},prefix+"q"),mk({value:unit},prefix+"u"),mk({value:period,window},prefix+"h"),mk({value:identity},prefix+"i")];
 const active=new Map(["aq","au","ah","ai","bq","bu","bh","bi"].map(x=>[x,1]));
 const types=["USD","CNY","KRW","second","minute","hour","day","count","percent"],periods=["total","month_rate","four_week_window"];
 const refFactors={USD:1,CNY:1,KRW:1,second:1,minute:60,hour:3600,day:1,count:1,percent:0.01};
 for(let u of types)for(let v of types)for(let p of periods)for(let r of periods)for(let a of [0,1,60])for(let b of [0,1,60])for(let sameWindow of [false,true])for(let sameIdentity of [false,true]){
  let x=record(a,u,p,"W","metric","a"),y=record(b,v,r,sameWindow?"W":"V",sameIdentity?"metric":"other","b");
  let z=compare(normalize(...x,active),normalize(...y,active));
  let compatible=(u===v||["second","minute","hour"].includes(u)&&["second","minute","hour"].includes(v))&&p===r&&sameWindow&&sameIdentity;
  let aa=a*refFactors[u],bb=b*refFactors[v],o=!compatible?"UNKNOWN":aa<bb?"LT":aa>bb?"GT":"EQ";
  ck(z===o,"reference");out.mathPairs++;out.comparable+=+(z!=="UNKNOWN");out.unknown+=+(z==="UNKNOWN");
  if(z!=="UNKNOWN"&&(a<b?"LT":a>b?"GT":"EQ")!==z)out.rawNumberWrong++;
 }
 const x=record(60,"minute","total","W","metric","a"),y=record(1,"hour","total","W","metric","b");
 ck(compare(normalize(...x,active),normalize(...y,active))==="EQ","base");
 for(let source of active.keys()){
  let m=new Map(active);m.delete(source);ck(compare(normalize(...x,m),normalize(...y,m))==="UNKNOWN","withdraw");out.sourceWithdrawalChecks++;
  m=new Map(active);m.set(source,2);ck(compare(normalize(...x,m),normalize(...y,m))==="UNKNOWN","stale");out.staleVersionChecks++
 }
 const scalar=scan("八成").numbers.find(q=>q.unit==="ratio"),ratio=[mk(scalar,"aq"),mk({value:"ratio"},"au"),mk({value:"total",window:"W"},"ah"),mk({value:"metric"},"ai")],pct=record(80,"percent","total","W","metric","b");
 for(let test of [()=>out.turns===64&&out.obligations===28&&out.valueCovered===25,()=>out.explicitUnitExact+out.aliasUnitExact+out.missingUnit+out.otherUnit===25,()=>out.mathPairs===26244,()=>out.comparable+out.unknown===out.mathPairs,()=>compare(normalize(...ratio,active),normalize(...pct,active))==="EQ",()=>normalize({...x[0],unit:null},null,x[2],x[3],active)===null,()=>normalize(x[0],{...x[1],value:"hour"},x[2],x[3],active)===null,()=>normalize(x[0],x[1],null,x[3],active)===null,()=>normalize(x[0],x[1],{...x[2],window:""},x[3],active)===null,()=>normalize({...x[0],confirmed:false},x[1],x[2],x[3],active)===null,()=>scan("三千六").numbers.every(q=>q.unit===null),()=>scan("每月四百五").numbers.some(q=>q.value===450&&q.periodCandidates.some(p=>p.kind==="month_rate")),()=>scan("每月收入，费用三百").numbers.every(q=>q.periodCandidates.length===0),()=>scan("周五下午五点").numbers.length===0]){ck(test(),"control "+out.controls);out.controls++}
 return out
}
const {I,E}=load(docs);console.log(JSON.stringify(experiment(I,E,docs.slice(7).map(x=>JSON.parse(x.content)),docs.slice(7).map((x,i)=>({id:i?"S":"L",sha:x.sha}))),null,2));
```
## 实测
```json
{
  "turns": 64,
  "obligations": 28,
  "valueCovered": 25,
  "explicitUnitExact": 7,
  "aliasUnitExact": 0,
  "missingUnit": 12,
  "otherUnit": 6,
  "periodTokens": 9,
  "matchedWithPeriodCandidate": 3,
  "periodRows": [
    {
      "id": "L01.1.1",
      "quote": "房租加停车每月最多四千",
      "unit": "CNY/month",
      "periods": [
        "每月"
      ]
    },
    {
      "id": "L01.2.1",
      "quote": "停车每月四百五",
      "unit": "CNY/month",
      "periods": [
        "每月"
      ]
    },
    {
      "id": "L15.1.3",
      "quote": "四周最多十小时",
      "unit": "hour/4weeks",
      "periods": [
        "四周"
      ]
    }
  ],
  "mathPairs": 26244,
  "comparable": 405,
  "unknown": 25839,
  "rawNumberWrong": 54,
  "sourceWithdrawalChecks": 8,
  "staleVersionChecks": 8,
  "controls": 14
}
```
下一步：否定与隐含零值、条件作用域及真正的指标身份确认，优先补真实独立语料。正式开发与训练另获授权。
