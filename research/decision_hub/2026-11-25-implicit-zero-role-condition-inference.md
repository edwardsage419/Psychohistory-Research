# 自主认知专项累计第130轮候选：隐含零值、角色隔离及条件推理
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / HOST_CONDITIONED_SEMANTIC_INFERENCE / SYNTHETIC_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 690793b11fed5dc8d67a93c96aecac2c6b6b59ad。核对近期12提交、13开放PR（#61待审）、v3.2前15行及历史全文、同步规程前17行、唯一交接前18行、R129前17行、R63前17行、R56前14行、R49前12行。R56已研究否定比较方向，R63已研究数量原子联合逻辑，R128/R129尚有3个隐含零值缺口。本轮新增经独立语义确认的零量推导、事实与政策隔离及条件守卫，不重复一般否定解析或原生验证。
## 固定资产
research/decision_hub/2026-11-25-quantity-unit-period-evidence-composition.md c89fbaede02776da34e6861328fa1933a855fb4c
research/decision_hub/2026-11-25-colloquial-numeral-magnitude-ratio-candidates.md f6684299a3720a533e44343b123edff085c7ee05
research/decision_hub/2026-11-25-open-span-quantity-composition-audit.md 175f8b48a4cc46cb3b41b7b65b13b06448bf461a
research/decision_hub/2026-11-25-unified-semantic-annotation-bridge.md af648d16ee96b9af4a3efb61b413d113208bb0ca
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
research/decision_hub/2026-11-25-temporal-quantity-candidate-separation.md 8a6b42f83b80283db6e215fe48f4fb2efbf8368c
research/decision_hub/2026-11-25-field-lineage-semantic-patch.md 307f8ba1291ec9ad83aca578bd5a02508d1e6110
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
R63 296465980e23a1d8082f81a8181343668965328b；R56 2c7810d1cad4986b9ecabdf727adab5600ed6fca；R49 0377f7f24cfa45014f4536b770d292872266a080；唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07。所有样例为ChatGPT研发辅助项目原创公开合成开发材料，非真人、独立留出或授权训练。
## 合同与证明
原R73 IR核对L02.1.2、L02.2.1、L04.1.4的实际原文和数值标注；实际R129 scan重查原词法未找到0。三例的主体/指标、语义角色、守卫、非负域及单位由研究者人工提供；无原文自动解析、无自主识别夜班、否定作用域、条件或真实币种。第三例模拟CNY是纯计算夹具，不代表原文已提供币种。不可称语料自主覆盖28/28。有限命题“无正值”且x非负推出x=0，适用于数量、非负金额；负值可能存在则不能推导。POLICY的守卫蕴涵仅限制候选行动在可能世界中的可接受性，不从用户拒绝条件推导实际发生频次，不证明无夜班就必然接受岗位；REPORT的守卫蕴涵只在已知条件为真时限制该变量，不能推导逆命题或否定守卫后的值。合格报告在本实验被外部明确作为硬情景前提，不代表任何用户报告自动成为事实。未确认、缺少当前来源或覆盖返回UNKNOWN；矛盾空域CONFLICT，不真空推出零。有限世界x∈{0,1,2}及early二值，全支持由研究者指定，未声称真实非负数量上限、概率或用户偏好。条件守卫可为always/early。POLICY保持原可能世界不变，计算条件合格PASS/FAIL/MIXED并独立判定事实零是否由该域蕴涵；REPORT在硬前提下筛选违反守卫的世界，再判断事实零。各源必须当前有效；原始语句、角色、意义、单位、窗口/指标/非负域组合共5个模拟独立源。实际R129 normalize/compare在已确认身份下精确比较零，不构造可信事实或原生C028准入；依赖列表额外保留角色源，使用时重核当前版本。测试只验证已知源和纯函数、非真实认证、签名、存储、跨轮授权、完整义务或抗恶意输入；手工语义假设没有通过独立来源确证。无自动更新、执行或建议权，authority NONE。
## 实验
原三项0义务逐项检查原文、既有词法、人工语义后数学投影。2角色×2守卫×2领域×64支持子集（含空）×2资格状态=1024次世界判断，与独立直接条件筛选参照对照（同一研究者，共同有限合同，非独立验收）。naivePolicyFalseFacts/naiveReportFalseFacts统计若把已评估的语义零直接升级为事实零但世界域未蕴涵该值的组合，包含事实明确非零及不确定，非现实错误率。每个类型合同逐项撤回/改版本五源，共40+40控制；另16专项控制。研究者选择角色、守卫、单位、窗口、有限域及硬前提资格。无真实用户、设备、原生运行、训练、Codex、CI、PR合并、部署、费用或冻结变更。产品轨维护唯一交接。
## 复算
按上述十份文件顺序置入docs[i].content，Node标准JS，仅执行已审查项目自有源码。
```js
function load(docs){
 const c=docs[0].content.split("```js\n")[1].split("\n```")[0];
 const A=Function(c.split("function experiment(I,E,corpora,assets)")[0]+"\nreturn load;")()(docs.slice(1));
 const U=Function("I","E",c.slice(c.indexOf("function experiment(I,E,corpora,assets)")).split(" const out={turns:")[0]+"\nreturn {scan,normalize,compare};\n}\nreturn experiment(I,E);")(A.I,A.E);
 return {...A,U}
}
function experiment(I,U,corpora,assets){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 // Explicitly annotated development hypotheses, not language-parser outputs.
 const specs=[
  {id:"L02.1.2",quote:"只要夜班我就不去",kind:"POLICY",domain:"count",metric:"night_shift",guard:"always"},
  {id:"L02.2.1",quote:"一次都不能有",kind:"POLICY",domain:"count",metric:"night_shift",guard:"always"},
  {id:"L04.1.4",quote:"提前做完没奖",kind:"REPORT",domain:"money",metric:"early_reward",guard:"early"}
 ];
 const ir=I.build(corpora[0],assets[0]);ck(I.verify(ir,corpora[0],assets[0]),"IR");
 const byId=new Map(ir.episodes.flatMap(e=>e.turns.flatMap(t=>t.items.map(a=>[a.id,{a,text:t.text}]))));
 const out={existingZeroObligations:0,rawZeroCoverage:0,hostConditionedZeroCoverage:0,sourceChecks:0,worldCases:0,policyCases:0,reportCases:0,unknownCases:0,conflictCases:0,policyPass:0,policyFail:0,policyMixed:0,reportConditional:0,reportActualZero:0,reportActualUnknown:0,naivePolicyFalseFacts:0,naiveReportFalseFacts:0,withdrawals:0,staleVersions:0,controls:0,examples:[]};
 // "no positive occurrence" over nonnegative scalar domain entails x=0
 // only as the relevant proposition. Policy restricts acceptable options;
 // it never eliminates possible factual worlds.
 function project(spec,records,active){
  if(!spec||!["POLICY","REPORT"].includes(spec.kind)||!["always","early"].includes(spec.guard)||!["count","money"].includes(spec.domain)||records.length!==5||new Set(records.map(r=>r.source)).size!==5||!records.every(r=>r.confirmed===true&&active.get(r.source)===r.version))return null;
  const [raw,role,meaning,unit,scope]=records;
  if(raw.value!==spec.quote||role.value!==spec.kind||meaning.value!=="NO_POSITIVE"||scope.value!==spec.guard||scope.metric!==spec.metric||scope.nonnegative!==true||scope.window!=="W"||!["count","USD","CNY","KRW"].includes(unit.value)||(spec.domain==="count")!==(unit.value==="count"))return null;
  const z=U.normalize({...raw,value:0,unit:null},unit,{...scope,value:"total"}, {...meaning,value:spec.metric},active);
  if(!z)return null;
  return {kind:spec.kind,guard:spec.guard,metric:spec.metric,zero:z,deps:records.map(r=>[r.source,r.version]),authority:"NONE"}
 }
 function classify(p,worlds,active,qualified){
  if(!qualified||!p||!p.deps.every(([s,v])=>active.get(s)===v)||!Array.isArray(worlds)||worlds.some(w=>!Number.isInteger(w.x)||w.x<0||w.x>2||typeof w.early!=="boolean"))return {status:"UNKNOWN",authority:"NONE"};
  if(!worlds.length)return {status:"CONFLICT",authority:"NONE"};
  const guard=w=>p.guard==="always"||w.early;
  const zero=w=>U.compare(p.zero,{...p.zero,n:String(w.x),d:"1"})==="EQ";
  if(p.kind==="POLICY"){
   const ok=worlds.map(w=>!guard(w)||zero(w)),yes=ok.filter(Boolean).length;
   return {status:"EVALUATED",kind:"POLICY",eligibility:yes===worlds.length?"PASS":yes===0?"FAIL":"MIXED",factZero:worlds.every(zero)?"ENTAILED":worlds.every(w=>!zero(w))?"EXCLUDED":"UNKNOWN",worlds:worlds.length,authority:"NONE"}
  }
  // A qualified conditional report is treated as a stipulated hard model
  // premise only inside this experiment. No converse or false-guard inference.
  const kept=worlds.filter(w=>!guard(w)||zero(w));
  if(!kept.length)return {status:"CONFLICT",authority:"NONE"};
  return {status:"EVALUATED",kind:"REPORT",condition:p.guard,factZero:kept.every(zero)?"ENTAILED":kept.every(w=>!zero(w))?"EXCLUDED":"UNKNOWN",worlds:kept.length,authority:"NONE"}
 }
 function reference(spec,ws,qualified){
  if(!qualified)return {status:"UNKNOWN",authority:"NONE"};
  if(!ws.length)return {status:"CONFLICT",authority:"NONE"};
  let g=w=>spec.guard==="always"||w.early;
  let r=spec.kind==="POLICY"?ws:ws.filter(w=>!g(w)||w.x===0);
  if(!r.length)return {status:"CONFLICT",authority:"NONE"};
  let factZero=r.every(w=>w.x===0)?"ENTAILED":r.every(w=>w.x!==0)?"EXCLUDED":"UNKNOWN";
  if(spec.kind==="REPORT")return {status:"EVALUATED",kind:"REPORT",condition:spec.guard,factZero,worlds:r.length,authority:"NONE"};
  let bad=ws.filter(w=>g(w)&&w.x>0).length;
  return {status:"EVALUATED",kind:"POLICY",eligibility:bad===0?"PASS":bad===ws.length?"FAIL":"MIXED",factZero,worlds:ws.length,authority:"NONE"}
 }
 const mk=(source,value,extra={})=>({source,value,version:1,confirmed:true,...extra});
 const make=(s,unit)=>[mk("raw",s.quote),mk("role",s.kind),mk("meaning","NO_POSITIVE"),mk("unit",unit),mk("scope",s.guard,{metric:s.metric,nonnegative:true,window:"W"})];
 const worlds=[false,true].flatMap(early=>[0,1,2].map(x=>({early,x})));
 const active=new Map(["raw","role","meaning","unit","scope"].map(x=>[x,1]));
 for(let s of specs){
  const {a,text}=byId.get(s.id);ck(a.span.text===s.quote&&a.dimensions.value.value===0&&text.slice(a.span.start,a.span.end)===s.quote,"actual annotation");out.sourceChecks++;out.existingZeroObligations++;
  const scan=U.scan(text);out.rawZeroCoverage+=+scan.numbers.some(q=>q.start>=a.span.start&&q.end<=a.span.end&&q.value===0);
  const p=project(s,make(s,s.domain==="count"?"count":"CNY"),active);ck(p&&p.zero.n==="0","zero projection");out.hostConditionedZeroCoverage++;
  out.examples.push({id:s.id,quote:s.quote,kind:p.kind,guard:p.guard,unrestricted:classify(p,worlds,active,true)});
 }
 // Extend beyond corpus hypotheses, not by adding phrase-specific parser rules.
 for(let kind of ["POLICY","REPORT"])for(let guard of ["always","early"])for(let domain of ["count","money"]){
  let spec={kind,guard,domain,metric:"m",quote:"synthetic semantic premise"},rec=make(spec,domain==="count"?"count":"USD"),p=project(spec,rec,active);ck(p,"projection");
  for(let mask=0;mask<64;mask++)for(let qualified of [false,true]){
   let ws=worlds.filter((_,i)=>mask&(1<<i)),z=classify(p,ws,active,qualified),o=reference(spec,ws,qualified);
   ck(eq(z,o),"reference");out.worldCases++;out.policyCases+=+(kind==="POLICY");out.reportCases+=+(kind==="REPORT");
   if(z.status==="UNKNOWN"){out.unknownCases++;continue}
   if(z.status==="CONFLICT"){out.conflictCases++;continue}
   if(kind==="POLICY"){
    out.policyPass+=+(z.eligibility==="PASS");out.policyFail+=+(z.eligibility==="FAIL");out.policyMixed+=+(z.eligibility==="MIXED");
    out.naivePolicyFalseFacts+=+(z.factZero!=="ENTAILED");
   }else{
    out.reportConditional+=+(guard==="early");out.reportActualZero+=+(z.factZero==="ENTAILED");out.reportActualUnknown+=+(z.factZero==="UNKNOWN");
    out.naiveReportFalseFacts+=+(z.factZero!=="ENTAILED");
   }
  }
  for(let key of active.keys()){
   let m=new Map(active);m.delete(key);ck(project(spec,rec,m)===null&&classify(p,worlds,m,true).status==="UNKNOWN","withdraw");out.withdrawals++;
   m=new Map(active);m.set(key,2);ck(project(spec,rec,m)===null&&classify(p,worlds,m,true).status==="UNKNOWN","stale");out.staleVersions++
  }
 }
 let s=specs[0],r=make(s,"count"),p=project(s,r,active),s2=specs[2],r2=make(s2,"CNY"),p2=project(s2,r2,active);
 for(let f of [()=>out.worldCases===1024,()=>out.existingZeroObligations===3&&out.rawZeroCoverage===0,()=>out.hostConditionedZeroCoverage===3,()=>project(s,make(s,"USD"),active)===null,()=>project(s2,make(s2,"count"),active)===null,()=>project(s,r.map((x,i)=>i===1?{...x,confirmed:false}:x),active)===null,()=>project(s,r.map((x,i)=>i===4?{...x,nonnegative:false}:x),active)===null,()=>project(s,r.map((x,i)=>i===2?{...x,value:"NOT_ALWAYS"}:x),active)===null,()=>project(s,r.map((x,i)=>i===0?{...x,value:"一次都不能有"}:x),active)===null,()=>classify(p,worlds,active,true).factZero==="UNKNOWN",()=>classify(p,worlds,active,true).eligibility==="MIXED",()=>classify(p2,[{x:2,early:false}],active,true).factZero==="EXCLUDED",()=>classify(p2,[{x:2,early:true}],active,true).status==="CONFLICT",()=>classify(p2,worlds.filter(w=>w.early),active,true).factZero==="ENTAILED",()=>classify(p2,[],active,true).status==="CONFLICT",()=>classify(p2,worlds,active,false).status==="UNKNOWN"]){ck(f(),"control "+out.controls);out.controls++}
 return out
}
const {I,U}=load(docs);console.log(JSON.stringify(experiment(I,U,docs.slice(8).map(x=>JSON.parse(x.content)),docs.slice(8).map((x,i)=>({id:i?"S":"L",sha:x.sha}))),null,2));
```
## 实测
```json
{
  "existingZeroObligations": 3,
  "rawZeroCoverage": 0,
  "hostConditionedZeroCoverage": 3,
  "sourceChecks": 3,
  "worldCases": 1024,
  "policyCases": 512,
  "reportCases": 512,
  "unknownCases": 512,
  "conflictCases": 44,
  "policyPass": 36,
  "policyFail": 36,
  "policyMixed": 180,
  "reportConditional": 120,
  "reportActualZero": 120,
  "reportActualUnknown": 72,
  "naivePolicyFalseFacts": 240,
  "naiveReportFalseFacts": 96,
  "withdrawals": 40,
  "staleVersions": 40,
  "controls": 16,
  "examples": [
    {
      "id": "L02.1.2",
      "quote": "只要夜班我就不去",
      "kind": "POLICY",
      "guard": "always",
      "unrestricted": {
        "status": "EVALUATED",
        "kind": "POLICY",
        "eligibility": "MIXED",
        "factZero": "UNKNOWN",
        "worlds": 6,
        "authority": "NONE"
      }
    },
    {
      "id": "L02.2.1",
      "quote": "一次都不能有",
      "kind": "POLICY",
      "guard": "always",
      "unrestricted": {
        "status": "EVALUATED",
        "kind": "POLICY",
        "eligibility": "MIXED",
        "factZero": "UNKNOWN",
        "worlds": 6,
        "authority": "NONE"
      }
    },
    {
      "id": "L04.1.4",
      "quote": "提前做完没奖",
      "kind": "REPORT",
      "guard": "early",
      "unrestricted": {
        "status": "EVALUATED",
        "kind": "REPORT",
        "condition": "early",
        "factZero": "UNKNOWN",
        "worlds": 4,
        "authority": "NONE"
      }
    }
  ]
}
```
下一步：以实际原文及独立标注研究语义角色、条件附着、否定作用域候选及保守未知检测，避免把人工映射当作自主理解。正式开发及训练另获授权。
