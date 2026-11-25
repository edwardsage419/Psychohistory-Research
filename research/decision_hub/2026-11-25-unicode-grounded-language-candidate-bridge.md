# 原文数量及跨轮引用候选的跨端字符身份、边界与可信传输
2026-11-25。RESEARCH_CANDIDATE / REUSED_JS_RESEARCH_EXECUTED / PINNED_PYTHON_FRAGMENTS_EXECUTED / PUBLIC_SYNTHETIC_DEVELOPMENT / FULL_APP_NOT_RUN / INDEPENDENT_NOT_RUN。起始main 8e9ec9f21f2d61d0f4ad086100ae5331a87e0507；固定Draft #62 e61bbad10932edabc9a87483e5407fdae6c751cc，仍待审。核对近期12提交、14开放PR、v3.2/同步规程/唯一产品交接前22行（交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07）。检索reference/span graph/numeral/semantic obligation/dependency decoder/condition polarity/UTF16/Unicode/offset/span identity/normalization/coordinate。审阅R102 3a1e3221ad223f18240342e1bddb471ca5d583f0、R103 f8326373525aa598b5a78920947536cfc70b0d1b、R104 1778d44ab329ff9533536f11f9e2469ca4d95ed8、R116 bd97b82e4043d90def1015f244213f0cc8415309、R131 d5df77493164cbff630e523f1709acd0338c6d80及R30 0bcf8448bd05f553dd612cb000f07b78e8b65803合同前段；R103/104已有UTF16位置和稳定原文身份，前轮v0.7语义批审已有同文跨作用域问题。本轮增量为实际跨语言位置转换、非法标量跨度筛查、排序预算前后连接、原文变更失效和原生Python出现ID核验。未重复角色/引用/数量生成理论或训练。全库去重有限。
## 固定资产
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md @ 5d68787f882a8c3a535d0e4f3a1aa2c663ddb3ad @ 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
research/decision_hub/2026-11-25-raw-text-reference-search.md @ 20c8df044c3a4d48f1819a7f401901d5ecde7a3e @ 16075b3ba567ee6dc3496300beab1417172a6c42
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json @ 8e9ec9f21f2d61d0f4ad086100ae5331a87e0507 @ be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json @ 8e9ec9f21f2d61d0f4ad086100ae5331a87e0507 @ 05c239f3f3b1f46235fa2464d2945c21c6c08132
实际连接器获取全文并核对blob；仅加载已审查项目自有JS代码中的lexical、spans、search、edgeScore。两公开开发集32情节64轮167已有标注、12已标明确引用，均为ChatGPT辅助研发合成开发语料；五种前缀变化由研究者构造（空、备注、非基本平面符号、扩展汉字、组合音标），仍为同源样例，前缀仅用于编码压力，不保证现实语言同义。未训练、未用标注生成候选；标注只用于事后位置诊断。R115和R77原有限词法/跨度规则、评分、长度及预算不改；两边各20或100候选，不是最终边TopK，也不是独立语义覆盖证明。
## A 数量及引用候选位置传输
JS字符串使用UTF16索引，Python str在合法Unicode标量文本中按码点计数。可信原文s由标量c_i组成，定义U(0)=0，U(i+1)=U(i)+该标量的UTF16长度(1或2)。合法文本上U严格递增，标量半开区间[i,j)唯一映射[U(i),U(j))；仅在两端属于U且原文字面匹配时逆转。UTF8字节边界同理。拒绝孤立代理码元、跨半个标量的边界、空范围、错误编码或错误引文；组合字符/字素簇可能含多个标量，不声称已实现Swift Character或用户感知字素边界。Unicode标量位置只作为候选协议，不自动确认语义。归一化后的文字可做搜索，必须保留原文与可审计映射，不能用归一化相等替代原文身份。实验保守拒绝不同原文票据，不实现归一化映射、自动修复或真实签名。
实际运行320个文本变体、340个数量候选，340/340往返一致；模拟直接将UTF16数字位置作为码点索引136处不同。835个标注位置诊断，334处直接错位；120个引用锚点对诊断48处直接错位（12原始引用×5前缀×2预算）。不是独立语言误差率。64个文本NFC归一化会变化。研究候选使用可信原文与会话、轮次、修订及授权代次的完全相等，仍authority NONE。
## B 跨轮候选图边界与预算
实际R77 spans产生90659个候选，1410个含非合法标量端点的跨度；每端先截取20/100预算的原列表中累计396个无效节点，原1642500条边中38454条至少一端无效。删除非法节点后，在固定原评分下对全部合法跨度重新取前K，恢复384个合法节点，原有效边全部保留；12次节点缺口因合法数量不足（累计396减384），不是搜索准确率损失。原已标边命中100/120，事后过滤与前置过滤均仍100/120；无语义召回提升，保留未命中20个诊断。前置过滤仍按既有UTF16长度打分，没处理跨字素语义、偏差或新排序；本轮新增校验仍在原跨度枚举后，不能宣称全请求预算、运行加速或内存保护。所有候选非计算授权，outside未在旧search返回值中显式字段化，接入必须独立保留未验证覆盖。真实开放语言、主体、条件和义务的识别仍未解决。JS 22项控制；两次实际运行输出相同（归档代码为第二次运行版本，仅去掉注释）。
## C Python原生出现ID及跨端身份
固定候选decision_semantics.py blob c7158c996f82c208b4d142b2863ddc3e27efa267；occurrence 109–120 FNV1a UTF16 fc5cf5fe，fingerprint 105–106 fcf4a607。实际从前轮已核对的逐字转录脚本提取函数，未改函数体；再次核验两FNV。FNV只作片段转录核对。容器Python3.13.5标准库执行，未执行完整interpret/原生会话/Swift或App。5前缀×3原文×3后缀×2字段90主案例，每例UTF16、UTF8、码点3种表示转换后调用实际occurrence，270/270结果逐字一致。直接以UTF16位置截取54组不同，以UTF8位置截取90组不同；直接传错误UTF16起点导致36组出现ID不同（其中还有只影响终点的输入，故不同计数）。原生ID只含位置、字段、原文，原文前缀全角/半角在相同位置可能得到同ID；3个NFKC相等但原文不同控制中2个原生ID相同，增加原文SHA256、轮次、修订、代次后3/3区分。360个变化控制（轮、修订、代次、原文）、10个非法输入控制及3个归一化控制均通过。证据是片段行为和跨端适配需求，未证明真实App错误路径；完整产品各端协议可能已有自己的位置映射，须在真实入口核查。不存在用夹具直接获得硬约束确认、事实资格、真实密码学授权或执行权。实际Python脚本重复运行一致。
Python本地可复算代码：native_occurrence.py SHA256 77e6c4e238c527266a138c6141c874f75bc127b1285e043d86420812a6349fdd；probe.py 4c111bce0b154fc9daf194b994ea8a7ad16a4571c07eac5f07f8301b9f8721a9；results.json d6ab226593bc81f8d588d2a620e98fb0ba17dc504f400fe522ad75a1276fbd97。实际代码在会话研究包中，核心片段调用及结果见下。JS固定资产复算代码附后。
## 实测
```json
{
  "episodes": 32,
  "turnVariants": 320,
  "requests": 320,
  "lexical": 340,
  "lexicalRoundTrips": 340,
  "lexicalNaiveWrong": 136,
  "spanCandidates": 90659,
  "invalidScalarSpans": 1410,
  "rankedNodes": 38185,
  "naiveInvalidTopK": 396,
  "restoredValidTopK": 384,
  "edgesOld": 1642500,
  "edgesInvalid": 38454,
  "edgesFiltered": 1604046,
  "edgesNew": 1641300,
  "positiveReferences": 120,
  "oldHits": 100,
  "filteredHits": 100,
  "newHits": 100,
  "referenceAnchorRoundTrips": 120,
  "referenceNaiveWrong": 48,
  "annotationAnchors": 835,
  "annotationNaiveWrong": 334,
  "normalizationChanges": 64,
  "controls": 22,
  "witness": {
    "episode": "L01",
    "prefix": "🧭：",
    "k": 100,
    "badNodes": 6,
    "invalidEdges": 591,
    "oldNodes": 200,
    "newNodes": 200
  }
}
```
Python：
```json
{"cases":90,"identity_controls":360,"invalid_controls":10,"native_scalar_roundtrips":270,"normalization_controls":3,"normalized_aliases":2,"source_identity_mismatch":36,"utf16_naive_wrong":54,"utf8_naive_wrong":90}
```
## JS 实际复算
按四份固定资产顺序将全文作为字符串docs，标准JS执行；禁止加载未经审核的网络文档。
```js
function load(docs){
 const c=i=>docs[i].split("```js\n")[1].split("\n```")[0];
 const L=Function(c(0).slice(c(0).indexOf("function experiment(A)")).split(" let out={corpusTurns:")[0]+"\nreturn {lexical};\n}\nreturn experiment({});")();
 const R=Function(c(1).split(" const pos=")[0]+"\nreturn {spans,search,edgeScore};\n}\nreturn experiment();")();
 return {L,R,corpora:docs.slice(2).map(JSON.parse)}
}
function experiment({L,R,corpora}){
 const ck=(x,m)=>{if(!x)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 function boundaries(s){
  if(typeof s!=="string")return null;
  let a=[0],u=0;for(let c of s){let x=c.codePointAt(0);if(x>=0xd800&&x<=0xdfff)return null;u+=c.length;a.push(u)}
  return a;
 }
 function toCP(s,a,b,raw,map=boundaries(s)){
  if(!map||!Number.isSafeInteger(a)||!Number.isSafeInteger(b)||a<0||b<=a||b>s.length||s.slice(a,b)!==raw)return null;
  let i=map.indexOf(a),j=map.indexOf(b);if(i<0||j<0)return null;
  return {start:i,end:j,raw,encoding:"UNICODE_SCALAR"};
 }
 function toUTF16(s,p,map=boundaries(s)){
  if(!map||p.encoding!=="UNICODE_SCALAR"||!Number.isSafeInteger(p.start)||!Number.isSafeInteger(p.end)||p.start<0||p.end<=p.start||p.end>=map.length)return null;
  let a=map[p.start],b=map[p.end];return s.slice(a,b)===p.raw?{start:a,end:b,raw:p.raw,encoding:"UTF16"}:null;
 }
 function qualified(s,spans){
  let map=boundaries(s);return spans.filter(x=>toCP(s,x.start,x.end,x.text,map)!==null)
 }
 function ticket(s,scope,p){return {s,scope:{...scope},p:{...p},authority:"NONE"}}
 function reuse(t,s,scope){return t.s===s&&eq(t.scope,scope)&&toUTF16(s,t.p)!==null&&t.authority==="NONE"}
 const prefixes=["","备注：","🧭：","𠀀：","e\u0301："],o={episodes:0,turnVariants:0,requests:0,lexical:0,lexicalRoundTrips:0,lexicalNaiveWrong:0,spanCandidates:0,invalidScalarSpans:0,rankedNodes:0,naiveInvalidTopK:0,restoredValidTopK:0,edgesOld:0,edgesInvalid:0,edgesFiltered:0,edgesNew:0,positiveReferences:0,oldHits:0,filteredHits:0,newHits:0,referenceAnchorRoundTrips:0,referenceNaiveWrong:0,annotationAnchors:0,annotationNaiveWrong:0,normalizationChanges:0,controls:0,witness:null};
 const quote=(c,d)=>d===0?c.span:c.quote;
 for(let d=0;d<corpora.length;d++)for(let e of corpora[d].cases){
  o.episodes++;
  let [a,b]=e.turns,prev=d===0?a.claims:a.proposal.claims,cur=d===0?b.claims:b.proposal.claims;
  for(let prefix of prefixes){
   let texts=[prefix+a.text,prefix+b.text];if(texts.some(s=>s.length>128))throw Error("text cap");
   let maps=texts.map(boundaries),lists=texts.map((s,i)=>{
    o.turnVariants++;o.normalizationChanges+=+(s.normalize("NFC")!==s);
    let z=L.lexical(s);ck(z.status==="CANDIDATES_ONLY","lexical");
    for(let n of z.items){let p=toCP(s,n.start,n.end,n.raw,maps[i]);ck(p&&eq(toUTF16(s,p,maps[i]),{start:n.start,end:n.end,raw:n.raw,encoding:"UTF16"}),"numeric round trip");o.lexical++;o.lexicalRoundTrips++;o.lexicalNaiveWrong+=+([...s].slice(n.start,n.end).join("")!==n.raw)}
    let q=R.spans(s,true),ok=qualified(s,q);o.spanCandidates+=q.length;o.invalidScalarSpans+=q.length-ok.length;
    for(let c of [prev,cur][i]){let raw=quote(c,d),a=s.indexOf(raw,prefix.length);ck(a>=prefix.length,"annotation");let p=toCP(s,a,a+raw.length,raw,maps[i]);ck(p&&toUTF16(s,p,maps[i]).start===a,"annotation roundtrip");o.annotationAnchors++;o.annotationNaiveWrong+=+([...s].slice(a,a+raw.length).join("")!==raw)}
    return {q,ok}
   });
   for(let k of [20,100]){
    o.requests++;
    let old=R.search(...texts,k,true);ck(old.status==="CANDIDATES_ONLY","reference");
    let clean=old.edges.filter(e=>toCP(texts[0],e.a.start,e.a.end,e.a.text,maps[0])&&toCP(texts[1],e.b.start,e.b.end,e.b.text,maps[1]));
    let aa=lists[0].ok.slice(0,k),bb=lists[1].ok.slice(0,k),fresh=[];
    for(let a of aa)for(let b of bb)fresh.push({a,b,score:R.edgeScore(a,b)});
    fresh.sort((x,y)=>y.score-x.score||x.a.start-y.a.start||x.a.end-y.a.end||x.b.start-y.b.start||x.b.end-y.b.end);
    o.rankedNodes+=old.a.length+old.b.length;
    let badNodes=old.a.filter(x=>!toCP(texts[0],x.start,x.end,x.text,maps[0])).length+old.b.filter(x=>!toCP(texts[1],x.start,x.end,x.text,maps[1])).length;
    o.naiveInvalidTopK+=badNodes;o.restoredValidTopK+=aa.length+bb.length-(old.a.length+old.b.length-badNodes);
    o.edgesOld+=old.edges.length;o.edgesFiltered+=clean.length;o.edgesInvalid+=old.edges.length-clean.length;o.edgesNew+=fresh.length;
    let keys=new Set(fresh.map(e=>[e.a.start,e.a.end,e.b.start,e.b.end].join(":")));
    ck(clean.every(e=>keys.has([e.a.start,e.a.end,e.b.start,e.b.end].join(":"))),"valid topk retained");
    for(let c of cur){let ref=d===0?c.supersedes:c.ref;if(typeof ref!=="string")continue;
     let p=d===0?prev.find(x=>x.field===ref.split(":t0:")[1]):prev[+ref.split(".").at(-1)-1];ck(p,"reference identity");
     let x=quote(p,d),y=quote(c,d),i=texts[0].indexOf(x,prefix.length),j=texts[1].indexOf(y,prefix.length);ck(i>=0&&j>=0,"gold position");
     let A=toCP(texts[0],i,i+x.length,x,maps[0]),B=toCP(texts[1],j,j+y.length,y,maps[1]);ck(A&&B,"gold coordinate");o.referenceAnchorRoundTrips++;
     o.referenceNaiveWrong+=+([...texts[0]].slice(i,i+x.length).join("")!==x||[...texts[1]].slice(j,j+y.length).join("")!==y);
     let has=es=>es.some(e=>e.a.start===i&&e.a.end===i+x.length&&e.b.start===j&&e.b.end===j+y.length);
     o.positiveReferences++;o.oldHits+=+has(old.edges);o.filteredHits+=+has(clean);o.newHits+=+has(fresh);
    }
    if(badNodes&&!o.witness)o.witness={episode:e.id,prefix,k,badNodes,invalidEdges:old.edges.length-clean.length,oldNodes:old.a.length+old.b.length,newNodes:aa.length+bb.length}
   }
  }
 }
 let s="🧭预算三小时",p=toCP(s,2,4,"预算"),scope={session:"s",turn:1,revision:1,epoch:1};
 const t=ticket(s,scope,p);
 for(let x of [o.episodes===32,o.turnVariants===320,o.requests===320,o.positiveReferences===120,o.annotationAnchors===835,o.invalidScalarSpans>0,o.lexicalNaiveWrong>0,o.edgesInvalid>0,o.oldHits===o.filteredHits,o.newHits>=o.oldHits,toCP(s,1,2,s.slice(1,2))===null,toCP(s,0,1,s.slice(0,1))===null,toCP("\ud800",0,1,"\ud800")===null,toCP(s,2,4,"错误")===null,toCP(s,-1,4,"预算")===null,reuse(t,s,scope),!reuse(t,s,{...scope,turn:2}),!reuse(t,s,{...scope,revision:2}),!reuse(t,s,{...scope,epoch:2}),!reuse(t,"🧭预算四小时",scope),!reuse(ticket("e\u0301预算",scope,toCP("e\u0301预算",2,4,"预算")),"é预算",scope),toUTF16(s,{...p,encoding:"UTF16"})===null]){ck(x,"control "+o.controls);o.controls++}
 return o
}
console.log(JSON.stringify(experiment(load(docs)),null,2));
```
## Python 核心复算入口（完整试验见会话研究包）
从固定原生decision_semantics.py提取函数，或直接运行已核对原始模块。以下核心转换与实际试验相同；该紧凑入口未单独执行。
```python
from decision_semantics import occurrence
def boundaries(s):
    p=[0];b=[0]
    for c in s:
        if 0xd800<=ord(c)<=0xdfff:raise ValueError("surrogate")
        p.append(p[-1]+len(c.encode("utf-16-le"))//2)
        b.append(b[-1]+len(c.encode("utf-8")))
    return p,b
def convert(s,start,end,raw,encoding):
    u,b=boundaries(s)
    m={"UTF16":u,"UTF8":b,"UNICODE_SCALAR":list(range(len(s)+1))}.get(encoding)
    if m is None or type(start) is not int or type(end) is not int or start not in m or end not in m or start>=end:raise ValueError("invalid boundary")
    i,j=m.index(start),m.index(end)
    if s[i:j]!=raw:raise ValueError("source mismatch")
    return i,j
s="🧭：预算最多三千元";raw="预算最多三千元"
u,b=boundaries(s)
a,z=convert(s,u[2],u[-1],raw,"UTF16")
assert occurrence(raw,a,field="cost_max",subject="",hard=True)["span"]=={"start":2,"end":len(s)}
```
## v0.8接口及后续
原文传输协议需要编码类型、原始UTF8字节摘要及合法标量校验、非空半开范围、原引文、会话实例、轮次、修订、语义义务身份；搜索可用归一化副本，但必须能回到原始输入。推荐共享标量坐标作为研究候选（也可统一UTF8字节，只能选定一种明确规范并写迁移），各端用经测试适配器处理UI位置，避免截断UTF16代理对；单字素显示、组合字符、原文序列化、换行、真实iPhone/Mac/浏览器/CLI与SQLite回放需要端到端验证。相同原文位置可有多个角色/条件候选，资格仍依独立语义覆盖、主体/单位/时间/来源及明确确认；不能仅因位置一致自动复用科学参数。近期R102/103/104/116/131及本轮为可复用接口研究；不构成完整自主语言能力。后续应在固定开发集与独立未见输入上验证端到端真实参数及原生数学，不继续以候选数量代替理解进度。产品轨维护唯一交接，独立轨保管未见资料。研究者自行选择字符前缀、有限预算、标量协议及人工作用域；无真实数据、训练、原生完整产品运行、Codex、CI、PR合并、部署、费用或冻结变化。
