# 自主认知专项累计第118轮候选：民用日期锚定与历史解释版本重放
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / CIVIL_DATE_FIXTURES / PUBLIC_SYNTHETIC_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 866e86147409ee852b6bdfff2bb5939ee07568c8。核对近期12提交、13开放PR（#61待审）、v3.2前15行及历史全文、唯一交接前18行、R117前20行及实际时间词法、R115词法源码、R100前18行、R114前20行。区别R100显式到账双时间、R114字段来源、R117未锚定时间词法：新增有限民用日期解析及原始锚点固定、版本核验，不重做到账/规划。
## 固定资产
research/decision_hub/2026-11-25-temporal-quantity-candidate-separation.md 8a6b42f83b80283db6e215fe48f4fb2efbf8368c
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
R100 65008b82d4720e931c99bd66ed03228b1f8ef69e；R114 307f8ba1291ec9ad83aca578bd5a02508d1e6110；唯一交接 5e74f4f0b37141d631740e844ad8bbbfed232e07。两套语料为ChatGPT研发辅助原创公开合成开发材料，非真人、训练、独立留出。
## 合同
复用R117实际temporal和R115词法；仅接收整个输入恰为单个时间候选的研究解释。显式上/本/这/下周某日，在可信宿主给定的民用日期和周一开周政策下求日历日；上/下/本月、这个月及去年/今年/明年求半开日期区间。JS UTC日算术仅借用公历日期算法，不代表当地午夜UTC或真实时刻。输入锚点限制1900..2099，输出可能跨到边界邻年，未实现完整时区、夏令时、工作日、节日、日历数据库或自然语用。未显式周归属、时钟、年代、当天/隔天、重复日程、时长、复合句保持未知；不能凭相同时间确认事件身份。周一开周、表达映射和限域为研究者选择，未经真实用户确认不作为正式产品政策。历史语料无可信真实日期，全部48时间候选不强行锚定；假定日期仅统计有限候选可解释性，不作为历史事实或整句解析。
研究收据绑定source/text/候选/原始anchor id+日期+状态/政策/root/version/value。verify以独立给定当前所需版本、来源和锚点记录重算结构；允许标记及事件根来自可信合成夹具，不是真实身份、授权、签名、防篡改或事务。旧解释在观察时间改变时不重新锚定；新版本需宿主另行确定真实修订对象、语义、来源及时间锚，本轮仅模拟已明确选择后的独立版本校验，不实现真实提交CAS或用户确认流程。撤回原始锚点或来源拒绝当前使用，不退回旧版本，不擦除旧合成记录；没有真实隐私删除、持久化、备份、并发、重放攻击防护。所有authority NONE。相同日期不同事件根不合并。不能由词法候选直接触发实际日程或数学模型。
## 实验
实际32情节64轮的48时间候选均无真实锚点；14个人工公历固定例（8星期，6月/年区间），跨闰日、月、年、周日边界，参照为研究者显式日期表。对照故意用后续观察日重新解释相同原文；选择会漂移的夹具，不能推断真实发生频率。新旧版本及来源撤回、字段篡改、不同根、未知时间等控制；同一研究者非独立验收。所有合成锚点并非用户个人资料，未访问实际日程。未执行原生数学、真机或真实效果。无训练、Codex、CI、生产修改、PR合并、部署、费用或冻结变化。
## 复算
按上述四份固定文件顺序置入docs[i].content。Node标准JS，执行已审查项目自有源码。
```js
function load(docs){
 const code=i=>docs[i].content.split("```js\n")[1].split("\n```")[0];
 const L=Function(code(1).slice(code(1).indexOf("function experiment(A)")).split(" let out={corpusTurns:")[0]+"\nreturn {lexical,parseNum};\n}\nreturn experiment({});")();
 const T=Function("L",code(0).slice(code(0).indexOf("function experiment(L,R,I,G")).split(" // Reuse the actual R116 graph")[0]+"\nreturn {temporal};\n}\nreturn experiment(L);")(L);
 return T
}
function experiment(T,corpora){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),copy=x=>JSON.parse(JSON.stringify(x));
 const DAY=86400000;
 function parseDate(s){
  if(typeof s!=="string"||!/^\d{4}-\d{2}-\d{2}$/.test(s))return null;
  const d=new Date(s+"T00:00:00Z");if(!Number.isFinite(+d)||d.toISOString().slice(0,10)!==s||+s.slice(0,4)<1900||+s.slice(0,4)>2099)return null;
  return +d/DAY
 }
 const fmt=n=>new Date(n*DAY).toISOString().slice(0,10);
 function resolve(c,anchor,policy){
  if(!anchor||!anchor.qualified||policy!=="monday-week@1")return null;
  let day=parseDate(anchor.date);if(day===null)return null;
  let d=new Date(day*DAY),y=d.getUTCFullYear(),m=d.getUTCMonth();
  if(c.kind==="WEEKDAY"){
   let shift={"上":-1,"本":0,"这":0,"下":1}[c.detail.week];
   if(shift===undefined)return null;
   let weekday=(d.getUTCDay()+6)%7;
   let x=day-weekday+7*shift+c.detail.weekday-1;
   return {kind:"DATE",date:fmt(x)}
  }
  if(c.kind==="RELATIVE_PERIOD"){
   let l=c.detail.label,shift={"上个月":-1,"下个月":1,"这个月":0,"本月":0}[l];
   if(shift!==undefined)return {kind:"PERIOD",start:fmt(Date.UTC(y,m+shift,1)/DAY),endExclusive:fmt(Date.UTC(y,m+shift+1,1)/DAY)};
   let ys={"去年":-1,"今年":0,"明年":1}[l];
   if(ys!==undefined)return {kind:"PERIOD",start:fmt(Date.UTC(y+ys,0,1)/DAY),endExclusive:fmt(Date.UTC(y+ys+1,0,1)/DAY)}
  }
  return null
 }
 function propose(text,anchor,source,root,version,policy){
  let t=T.temporal(text);
  if(t.status!=="CANDIDATES_ONLY")return null;
  // Only a single full-span temporal expression is admitted to this bounded contract.
  if(t.items.length!==1||t.items[0].start!==0||t.items[0].end!==text.length)return null;
  let candidate=t.items[0],value=resolve(candidate,anchor,policy);
  if(!value)return null;
  return {schema:"civil-temporal-research@1",root,version,source,text,candidate,anchor:copy(anchor),policy,value,authority:"NONE"}
 }
 function verify(r,sourceRecords,anchorRecords,expected){
  if(!r||r.root!==expected.root||r.version!==expected.version||r.source!==expected.source||r.policy!==expected.policy||r.anchor.id!==expected.anchorId)return false;
  const s=sourceRecords[r.source],a=anchorRecords[r.anchor.id];
  if(!s?.allowed||!a?.allowed||!a.qualified||a.id!==r.anchor.id)return false;
  return eq(r,propose(s.text,a,r.source,r.root,r.version,expected.policy))
 }
 // Explicit independently written calendar table, not derived by resolve.
 const rows=[
 ["2024-02-29","下周五","2024-03-08","2024-03-07","2024-03-15"],
 ["2024-02-29","本周四","2024-02-29","2024-03-07","2024-03-07"],
 ["2024-02-29","上周一","2024-02-19","2024-03-07","2024-02-26"],
 ["2026-12-31","下周一","2027-01-04","2027-01-07","2027-01-11"],
 ["2027-01-01","本周日","2027-01-03","2027-01-08","2027-01-10"],
 ["2027-01-03","下周五","2027-01-08","2027-01-04","2027-01-15"],
 ["2027-01-04","上周日","2027-01-03","2027-01-11","2027-01-10"],
 ["2026-11-25","下周五","2026-12-04","2026-12-02","2026-12-11"]
 ];
 const periodRows=[
 ["2024-03-01","上个月","2024-02-01","2024-03-01","2024-04-01","2024-03-01","2024-04-01"],
 ["2024-01-31","下个月","2024-02-01","2024-03-01","2024-02-01","2024-03-01","2024-04-01"],
 ["2026-12-31","下个月","2027-01-01","2027-02-01","2027-01-01","2027-02-01","2027-03-01"],
 ["2027-01-01","上个月","2026-12-01","2027-01-01","2027-02-01","2027-01-01","2027-02-01"],
 ["2024-02-29","今年","2024-01-01","2025-01-01","2025-01-01","2025-01-01","2026-01-01"],
 ["2026-12-31","明年","2027-01-01","2028-01-01","2027-01-01","2028-01-01","2029-01-01"]
 ];
 let out={corpusTurns:0,corpusTemporal:0,corpusEligibleIfAnchored:0,corpusNoActualAnchor:0,calendarFixtures:0,calendarChecks:0,naiveDrift:0,sourceRevocationChecks:0,mutationRejections:0,revisionChecks:0,distinctIdentityChecks:0,unresolvedControls:0,controls:0,example:null};
 const anchor=(id,date)=>({id,date,qualified:true,allowed:true});
 for(let d of corpora)for(let e of d.cases)for(let t of e.turns){let z=T.temporal(t.text);out.corpusTurns++;for(let c of z.items){out.corpusTemporal++;ck(resolve(c,null,"monday-week@1")===null,"no historical anchor");out.corpusNoActualAnchor++;if(resolve(c,anchor("hypothetical","2026-11-25"),"monday-week@1"))out.corpusEligibleIfAnchored++}}
 const fixtures=[...rows.map(([date,text,want,later,drift])=>({date,text,want:{kind:"DATE",date:want},later,drift:{kind:"DATE",date:drift}})),...periodRows.map(([date,text,start,endExclusive,later,ls,le])=>({date,text,want:{kind:"PERIOD",start,endExclusive},later,drift:{kind:"PERIOD",start:ls,endExclusive:le}}))];
 for(let [i,f] of fixtures.entries()){
  let a=anchor("a"+i,f.date),b=anchor("b"+i,f.later),sources={s:{text:f.text,allowed:true}},anchors={[a.id]:a,[b.id]:b},expected={root:"event"+i,version:1,source:"s",anchorId:a.id,policy:"monday-week@1"};
  let r=propose(f.text,a,"s",expected.root,1,expected.policy);ck(r&&eq(r.value,f.want),"calendar "+f.text+" "+f.date);out.calendarFixtures++;
  const snapshot=copy(r);
  // Current time changes, but frozen interpretation only reads original anchor.
  let naive=propose(f.text,b,"s",expected.root,1,expected.policy);ck(eq(naive.value,f.drift),"later reference "+f.text);out.calendarChecks+=2;out.naiveDrift+=+!eq(naive.value,r.value);
  ck(verify(r,sources,anchors,expected)&&eq(r,snapshot),"replay");out.calendarChecks++;
  for(let [s,aa] of [[{s:{...sources.s,allowed:false}},anchors],[sources,{...anchors,[a.id]:{...a,allowed:false}}],[sources,{[b.id]:b}],[sources,{...anchors,[a.id]:{...a,qualified:false}}]]){ck(!verify(r,s,aa,expected),"withdraw");out.sourceRevocationChecks++}
  for(let change of [x=>x.anchor.date=b.date,x=>x.anchor.id=b.id,x=>x.root="other",x=>x.version=2,x=>x.policy="other",x=>x.value=naive.value,x=>x.authority="EXECUTE"]){let z=copy(r);change(z);ck(!verify(z,sources,anchors,expected),"mutated");out.mutationRejections++}
  // A new version requires separate host-confirmed target and source. No text-only update.
  const r2=propose(f.text,b,"s2",expected.root,2,expected.policy),ex2={...expected,source:"s2",version:2,anchorId:b.id},s2={...sources,s2:{text:f.text,allowed:true}};
  ck(verify(r2,s2,anchors,ex2)&&!verify(r,s2,anchors,ex2)&&eq(r,snapshot),"version");out.revisionChecks++;
  let other=propose(f.text,a,"s","different-event",1,expected.policy);ck(eq(other.value,r.value)&&!verify(other,sources,anchors,expected),"different events");out.distinctIdentityChecks++;
  if(i===7)out.example={old:r.value,newInterpretationIfExplicitlyRevised:r2.value,oldAnchor:a.date,newAnchor:b.date};
 }
 for(let s of ["周五","九点","下午五点","七十年代","当天","隔天","周末","每天","每周","每月","每年","半天","三天","下周五下午五点"]){ck(propose(s,anchor("x","2026-11-25"),"s","e",1,"monday-week@1")===null,"unresolved "+s);out.unresolvedControls++}
 for(let t of [()=>out.corpusTurns===64&&out.corpusTemporal===48&&out.corpusNoActualAnchor===48,()=>out.calendarFixtures===14,()=>out.naiveDrift===14,()=>parseDate("2023-02-29")===null,()=>parseDate("2024-02-29")!==null,()=>parseDate("2024-13-01")===null,()=>propose("下周五",anchor("x","2026-11-25"),"s","e",1,"unknown")===null,()=>propose("下周五",{...anchor("x","2026-11-25"),qualified:false},"s","e",1,"monday-week@1")===null]){ck(t(),"control");out.controls++}
 return out
}
console.log(JSON.stringify(experiment(load(docs),docs.slice(2).map(x=>JSON.parse(x.content))),null,2));
```
## 实测
```json
{
  "corpusTurns": 64,
  "corpusTemporal": 48,
  "corpusEligibleIfAnchored": 6,
  "corpusNoActualAnchor": 48,
  "calendarFixtures": 14,
  "calendarChecks": 42,
  "naiveDrift": 14,
  "sourceRevocationChecks": 56,
  "mutationRejections": 98,
  "revisionChecks": 14,
  "distinctIdentityChecks": 14,
  "unresolvedControls": 14,
  "controls": 8,
  "example": {
    "old": {
      "kind": "DATE",
      "date": "2026-12-04"
    },
    "newInterpretationIfExplicitlyRevised": {
      "kind": "DATE",
      "date": "2026-12-11"
    },
    "oldAnchor": "2026-11-25",
    "newAnchor": "2026-12-02"
  }
}
```
下一步：在可信事件对象与时间锚点绑定基础上研究截止时间和跨决策计划冲突，保持开放语义、真实来源、独立验收边界。产品轨维护唯一交接，正式版本及训练另获授权。
