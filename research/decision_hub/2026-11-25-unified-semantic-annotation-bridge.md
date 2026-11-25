# v3.2 自主认知专项第14轮（累计第73轮）：统一语义标注转换及缺失信息保留

2026-11-25。RESEARCH_CANDIDATE / REPOSITORY_CORPUS_CONVERSION_EXECUTED / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线 6b74c7cf312afbbd1fcc93ec812c5028b9f5642e，13开放Draft PR，#61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e。核查最近8提交、v3.2 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（前段及历史全文）、AGENTS 78cc1f8327ec50b5762103fedfaf1f06e85f7658、同步规程26c4d946e48f01858fb8e8c2cb06e4f7ba91bf05、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（相关标题非全文）、第72轮82f53eb20bcb7b49e0e56088a7c2c586000627fa、第58轮ad1f8ab7be83d28391ee62ce77a44d5f59804bef、第24轮与第9轮两个实际语料。区别于R58语义义务资格协议及R72语料统计：本轮执行真实仓库JSON的保守跨schema转换、完整逻辑内容往返、引用候选解析、字符标注重叠和缺失掩码审计。未重跑原生方法或训练。

## 固定输入
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
实际读两个完整JSON及连接器返回blob身份。均为ChatGPT研发辅助项目原创合成公开开发资料，无独立真人样本或训练许可确认。保留原版，不向仓库复制完整派生语料（可按代码复算）。没有新增外部资料、原论文审查、个人数据或第三方权重。

## 候选IR与语义保护
annotation-bridge/0.1仅标注研究交换格式，不是运行时可信语义IR、最终分类体系或生产准入。每条记录包含源数据集、情节/轮/出现序号、UTF16唯一原文跨度、原始标签、粗粒度角色、完整原始标注、13个分离维度、原有引用与解析候选。注意两schema的op：L表示比较关系（包括==，不得默认转为C028四种不等式）；S表示add/retract/replace修订操作。L的operation单独投影，S的数学比较符未标注。L主体、时间、情态没有独立字段；保留UNANNOTATED，不从叙述自动归属本人。EXPLICIT_NULL仅表示原标注存在null，不能视为无条件、无约束或否定；ANNOTATED只是已有开发标签，不是真实确认。sourceAnnotation保留其余原始字段（如n/failures/successes/relative/action），不因为粗角色映射失去原始结构；CONFIRM保持confirmation，REVISION保持revision，避免将上下文变更自动翻译成新的硬约束；HARD_CONSEQUENCE保持consequence而非约束；报告、估计、反事实、追溯记录、权限意图与事实资格分离。S fact粗映射report，criterion不自动映射preference，原始细类保留。分类映射由本轮研究者制定，未独立语义审定，粗角色可能不足；不宣称语义无损（仅原始JSON逻辑内容无损往返）。不将条件字符串解析为逻辑树，不将scope数组/字符串当同义或自动拆分约束；不自动解析单位组合、角色、数值范围/区间真假、完整义务或事实。数学接口须经R58/62/63/67/70可信字段资格另行确认，当前authority NONE，training NOT_AUTHORIZED，无生产执行。

S引用按同情节一基轮次及标注序号解析，L引用按同情节零基轮次及field筛选既往候选；唯一候选不等于真实语义指代、授权撤回或替换。无引用、未解、多解区分；保留原值，不自动变更历史状态。若源记录相同标注文本出现多处，则本原型拒绝，不强行选择；本批次全部唯一。使用原文UTF16位置，不做归一化。未来CRF/序列标签接口必须将未标注字符保留为未知监督掩码，不把所有未标注字符自动标O。对重叠标注不可强行压成单BIO层，需多头或跨度图并人工审定。现有唯一跨度并不代表全义务覆盖。当前只统计字符覆盖/重叠，不训练、不生成BIO监督标签、不推断负例；角色映射及未标注维度均须独立审计。真实模型学习需另外授权。

## 实际验证
完整源JSON（含非claim元数据及轮/情节顺序）往返恢复，对象键排序后逻辑内容相同，不是原始文件字节、独立密码学哈希或真实语义准确率验证。核验器从可信固定原文重建规范IR并比较，且反向恢复全文；同一转换实现、非独立算法/安全验收。每个实际标注进行五种确定非法变化：授权扩大、跨度偏移、角色破坏、虚构主体、源标注与细类同步篡改；与独立保存原始资料比较均拒绝。额外控制训练许可、删除标注、文本修改、维度角色分离、null/未标注区分和权限。不能检测可信源本身错误、真实事实/权限、漏标、同源污染或正确但不同转换规范；不能推断对抗安全或模型准确率。实际结果如下，代码仅依赖JS，无训练、额外库或网络（已有固定输入时）。

```js
function experiment(docs,assets){
 const ck=(b,m)=>{if(!b)throw Error(m)},clone=x=>JSON.parse(JSON.stringify(x)),canon=x=>x===null||typeof x!=="object"?JSON.stringify(x):Array.isArray(x)?"["+x.map(canon).join(",")+"]":"{"+Object.keys(x).sort().map(k=>JSON.stringify(k)+":"+canon(x[k])).join(",")+"}",eq=(a,b)=>canon(a)===canon(b);
 const L={HARD:"constraint",CONDITIONAL_HARD:"constraint",PREFERENCE:"preference",GOAL:"goal",USER_REPORTED:"report",UNKNOWN:"unknown",UNAVAILABLE_EVIDENCE:"unknown",REPORTED_UNCERTAIN:"report",REPORTED_PROMISE:"report",REPORTED_POSSIBILITY:"report",REPORTED_EXTERNAL:"report",REPORTED_UNVERIFIED:"report",REPORTED_ESTIMATE:"estimate",ESTIMATE:"estimate",PAST_COST:"cost",FUTURE_COST:"cost",PROPOSED_ACTION:"action",CONDITIONAL_ACTION:"action",ACTION:"action",CONFIRMED_CHOICE:"choice",OBSERVED_OUTCOME:"observation",COUNTERFACTUAL_CLAIM:"counterfactual",HYPOTHESIS:"hypothesis",POSTHOC:"retrospective",RETROSPECTIVE_ESTIMATE:"retrospective",RECORD_INTENT:"permission_intent",AUTHORIZATION_PROPOSAL:"permission_intent",EVENT_DEFINITION:"event_definition",TRIGGER:"trigger",EXCEPTION:"scope_modifier",EXCLUSION:"scope_modifier",HARD_CONSEQUENCE:"consequence",REVISION:"revision",CONFIRM:"confirmation"};
 const S={action:"action",criterion:"criterion",unknown:"unknown",constraint:"constraint",goal:"goal",fact:"report",observation:"observation",permission_intent:"permission_intent",estimate:"estimate"};
 const known=(a,k)=>!Object.hasOwn(a,k)?{status:"UNANNOTATED"}:a[k]===null?{status:"EXPLICIT_NULL"}:{status:"ANNOTATED",value:clone(a[k])};
 const omit=(a,ks)=>Object.fromEntries(Object.entries(a).filter(([k])=>!ks.includes(k)));
 function build(j,asset){
  const d=asset.id,manifest={schema:"annotation-bridge/0.1",asset:clone(asset),sourceMeta:omit(j,["cases"]),purpose:"PUBLIC_DEVELOPMENT_ONLY",training:"NOT_AUTHORIZED",authority:"NONE",episodes:[]};
  for(const ep of j.cases){
   const E={meta:omit(ep,["turns"]),turns:[]};manifest.episodes.push(E);
   for(let ti=0;ti<ep.turns.length;ti++){
    const t=ep.turns[ti],src=d==="L"?t.claims:t.proposal.claims;
    const T={text:t.text,meta:d==="L"?omit(t,["text","claims"]):omit(t,["text","proposal"]),proposalMeta:d==="S"?omit(t.proposal,["claims"]):null,items:[]};E.turns.push(T);
    for(let i=0;i<src.length;i++){
     const a=src[i],q=d==="L"?a.span:a.quote,start=t.text.indexOf(q);ck(typeof q==="string"&&q.length&&start>=0&&start===t.text.lastIndexOf(q),"unique span");
     const tag=d==="L"?a.kind:a.role,role=(d==="L"?L:S)[tag];ck(role,"unmapped label");
     let ref=d==="L"?a.supersedes:a.ref,links=[];
     if(typeof ref==="string"){
      if(d==="S"){let m=/^([^.]+)\.(\d+)\.(\d+)$/.exec(ref);if(m&&m[1]===ep.id&&+m[2]>=1&&+m[2]<=ti&&+m[3]>=1&&+m[3]<=ep.turns[+m[2]-1].proposal.claims.length)links.push(ref)}
      else {let m=/^([^:]+):t(\d+):(.+)$/.exec(ref);if(m&&m[1]===ep.id&&+m[2]<ti){ep.turns[+m[2]].claims.forEach((v,k)=>{if(v.field===m[3])links.push(`${ep.id}.${+m[2]+1}.${k+1}`)})}}
     }
     T.items.push({id:`${ep.id}.${ti+1}.${i+1}`,span:{start,end:start+q.length,text:q,encoding:"UTF16"},role,originalLabel:tag,dimensions:{actor:known(a,"actor"),time:known(a,"time"),modality:known(a,"modality"),field:known(a,"field"),relation:d==="L"?known(a,"op"):{status:"UNANNOTATED"},edit:d==="S"?known(a,"op"):known(a,"operation"),condition:known(a,"condition"),scope:known(a,"scope"),unit:known(a,"unit"),value:known(a,"value"),lower:known(a,"lo"),upper:known(a,"hi")},reference:{original:d==="L"?known(a,"supersedes"):known(a,"ref"),candidates:links,status:typeof ref!=="string"?"NO_ANNOTATED_LINK":links.length===1?"UNIQUE_CANDIDATE":links.length?"AMBIGUOUS":"UNRESOLVED"},sourceAnnotation:clone(a),authority:"NONE"});
    }
   }
  }return manifest;
 }
 function restore(m){
  const d=m.asset.id;return {...clone(m.sourceMeta),cases:m.episodes.map(e=>({...clone(e.meta),turns:e.turns.map(t=>d==="L"?{...clone(t.meta),text:t.text,claims:t.items.map(x=>clone(x.sourceAnnotation))}:{...clone(t.meta),text:t.text,proposal:{...clone(t.proposalMeta),claims:t.items.map(x=>clone(x.sourceAnnotation))}})}))};
 }
 // Verification compares to a trusted, independently retrieved fixed source, not self-declared raw payload.
 function verify(m,j,a){try{return eq(restore(m),j)&&eq(m,build(j,a))}catch{return false}}
 const out={datasets:[],claims:0,roundTrip:0,refs:0,uniqueRefs:0,unresolvedRefs:0,ambiguousRefs:0,overlapPairs:0,overlapTurns:0,characters:0,unannotatedCharacters:0,multilabelCharacters:0,mutations:0,rejected:0,controls:0,roleCounts:{},dimensionCounts:{},witnesses:[]};
 const ms=docs.map((j,i)=>build(j,assets[i]));
 for(let d=0;d<ms.length;d++){
  let m=ms[d],j=docs[d],a=assets[d];ck(verify(m,j,a),"roundtrip");out.roundTrip++;
  const ds={id:a.id,episodes:m.episodes.length,turns:0,claims:0,links:0,unique:0,unresolved:0,ambiguous:0,overlapPairs:0,overlapTurns:0,characters:0,unannotated:0,multilabel:0};
  for(const e of m.episodes)for(const t of e.turns){
   ds.turns++;ds.claims+=t.items.length;out.claims+=t.items.length;const masks=Array.from({length:t.text.length},()=>[]);
   let overlaps=0;
   for(let i=0;i<t.items.length;i++){
    const x=t.items[i];ck(t.text.slice(x.span.start,x.span.end)===x.span.text,"span");
    out.roleCounts[x.role]=(out.roleCounts[x.role]??0)+1;
    for(const [k,v] of Object.entries(x.dimensions)){out.dimensionCounts[k]??={ANNOTATED:0,UNANNOTATED:0,EXPLICIT_NULL:0};out.dimensionCounts[k][v.status]++}
    if(x.reference.status!=="NO_ANNOTATED_LINK"){ds.links++;out.refs++;let k=x.reference.status==="UNIQUE_CANDIDATE"?"unique":x.reference.status==="AMBIGUOUS"?"ambiguous":"unresolved";ds[k]++;out[k==="unique"?"uniqueRefs":k==="ambiguous"?"ambiguousRefs":"unresolvedRefs"]++;if(k!=="unique")out.witnesses.push({id:x.id,reference:x.reference})}
    for(let p=x.span.start;p<x.span.end;p++)masks[p].push(x.id);
    for(let h=0;h<i;h++){let y=t.items[h];if(x.span.start<y.span.end&&y.span.start<x.span.end){overlaps++;if(out.witnesses.length<10)out.witnesses.push({overlap:[x.id,y.id]})}}
   }
   ds.overlapPairs+=overlaps;ds.overlapTurns+=+(overlaps>0);ds.characters+=masks.length;ds.unannotated+=masks.filter(x=>x.length===0).length;ds.multilabel+=masks.filter(x=>x.length>1).length;
  }
  out.datasets.push(ds);out.overlapPairs+=ds.overlapPairs;out.overlapTurns+=ds.overlapTurns;out.characters+=ds.characters;out.unannotatedCharacters+=ds.unannotated;out.multilabelCharacters+=ds.multilabel;
  // Each actual claim gets five distinct corruptions. Includes synchronized raw/derived edit.
  for(let e=0;e<m.episodes.length;e++)for(let t=0;t<m.episodes[e].turns.length;t++)for(let i=0;i<m.episodes[e].turns[t].items.length;i++){
   for(const mutate of [x=>{x.authority="EXECUTE"},x=>{x.span.start++},x=>{x.role="UNDECLARED_ROLE"},x=>{x.dimensions.actor={status:"ANNOTATED",value:"invented"}},x=>{if(d===0)x.sourceAnnotation.kind="UNKNOWN_MUTATION";else x.sourceAnnotation.role="UNKNOWN_MUTATION";x.originalLabel="UNKNOWN_MUTATION"}]){
    let z=clone(m);mutate(z.episodes[e].turns[t].items[i]);out.mutations++;ck(!verify(z,j,a),"corruption");out.rejected++;
   }
  }
 }
 for(const [i,m] of ms.entries()){
  const z=clone(m);z.training="AUTHORIZED";ck(!verify(z,docs[i],assets[i]),"training");out.controls++;
  const y=clone(m);y.episodes[0].turns[0].items.pop();ck(!verify(y,docs[i],assets[i]),"omission");out.controls++;
  const w=clone(m);w.episodes[0].turns[0].text+="。";ck(!verify(w,docs[i],assets[i]),"text");out.controls++;
 }
 const l=ms[0].episodes.flatMap(e=>e.turns.flatMap(t=>t.items)),s=ms[1].episodes.flatMap(e=>e.turns.flatMap(t=>t.items));
 ck(l.every(x=>x.dimensions.actor.status==="UNANNOTATED"&&x.dimensions.time.status==="UNANNOTATED"),"no invented actor/time");out.controls++;
 ck(s.every(x=>x.dimensions.relation.status==="UNANNOTATED"),"no edit as relation");out.controls++;
 ck(s.some(x=>x.dimensions.condition.status==="EXPLICIT_NULL")&&l.some(x=>x.dimensions.condition.status==="UNANNOTATED"),"null distinct");out.controls++;
 ck(ms.every(m=>m.authority==="NONE"&&m.training==="NOT_AUTHORIZED"),"no authority");out.controls++;
 return out;
}
```
执行 experiment(docs, assets)，docs为按L/S顺序解析的原始JSON，assets为以下固定记录：
```json
[
  {
    "id": "L",
    "path": "research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json",
    "sha": "be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb"
  },
  {
    "id": "S",
    "path": "research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json",
    "sha": "05c239f3f3b1f46235fa2464d2945c21c6c08132"
  }
]
```
实际输出：
```json
{
  "datasets": [
    {
      "id": "L",
      "episodes": 18,
      "turns": 36,
      "claims": 98,
      "links": 3,
      "unique": 3,
      "unresolved": 0,
      "ambiguous": 0,
      "overlapPairs": 0,
      "overlapTurns": 0,
      "characters": 1050,
      "unannotated": 351,
      "multilabel": 0
    },
    {
      "id": "S",
      "episodes": 14,
      "turns": 28,
      "claims": 69,
      "links": 9,
      "unique": 9,
      "unresolved": 0,
      "ambiguous": 0,
      "overlapPairs": 0,
      "overlapTurns": 0,
      "characters": 716,
      "unannotated": 228,
      "multilabel": 0
    }
  ],
  "claims": 167,
  "roundTrip": 2,
  "refs": 12,
  "uniqueRefs": 12,
  "unresolvedRefs": 0,
  "ambiguousRefs": 0,
  "overlapPairs": 0,
  "overlapTurns": 0,
  "characters": 1766,
  "unannotatedCharacters": 579,
  "multilabelCharacters": 0,
  "mutations": 835,
  "rejected": 835,
  "controls": 10,
  "roleCounts": {
    "constraint": 25,
    "scope_modifier": 2,
    "report": 30,
    "unknown": 18,
    "preference": 8,
    "confirmation": 5,
    "cost": 2,
    "revision": 3,
    "estimate": 7,
    "consequence": 2,
    "action": 30,
    "hypothesis": 3,
    "choice": 1,
    "trigger": 1,
    "observation": 3,
    "counterfactual": 1,
    "retrospective": 2,
    "goal": 11,
    "permission_intent": 7,
    "event_definition": 1,
    "criterion": 5
  },
  "dimensionCounts": {
    "actor": {
      "ANNOTATED": 69,
      "UNANNOTATED": 98,
      "EXPLICIT_NULL": 0
    },
    "time": {
      "ANNOTATED": 69,
      "UNANNOTATED": 98,
      "EXPLICIT_NULL": 0
    },
    "modality": {
      "ANNOTATED": 69,
      "UNANNOTATED": 98,
      "EXPLICIT_NULL": 0
    },
    "field": {
      "ANNOTATED": 98,
      "UNANNOTATED": 69,
      "EXPLICIT_NULL": 0
    },
    "relation": {
      "ANNOTATED": 10,
      "UNANNOTATED": 157,
      "EXPLICIT_NULL": 0
    },
    "edit": {
      "ANNOTATED": 72,
      "UNANNOTATED": 95,
      "EXPLICIT_NULL": 0
    },
    "condition": {
      "ANNOTATED": 5,
      "UNANNOTATED": 97,
      "EXPLICIT_NULL": 65
    },
    "scope": {
      "ANNOTATED": 3,
      "UNANNOTATED": 164,
      "EXPLICIT_NULL": 0
    },
    "unit": {
      "ANNOTATED": 22,
      "UNANNOTATED": 145,
      "EXPLICIT_NULL": 0
    },
    "value": {
      "ANNOTATED": 39,
      "UNANNOTATED": 128,
      "EXPLICIT_NULL": 0
    },
    "lower": {
      "ANNOTATED": 1,
      "UNANNOTATED": 166,
      "EXPLICIT_NULL": 0
    },
    "upper": {
      "ANNOTATED": 1,
      "UNANNOTATED": 166,
      "EXPLICIT_NULL": 0
    }
  },
  "witnesses": []
}
```

## 后续与验收
先完善标注字段语义及有来源的负例/未标注区分，审查引述、否定、主体、跨轮引用、单位与条件，设计不训练的自主候选结构搜索（固定人工权重/有限语法，比较排序、候选覆盖与拒绝；不能从公开测试调权后称独立泛化）。优先用现有真实仓库语料诊断缺口，独立轨隔离未见情节族与来源；后续需合法真实语言资料、训练许可、支持环境及设备测量。保持R50完整版本12项范围及v3.2方向；研究格式并非正式架构决定，暂不发布零碎Codex任务。未改生产代码、训练、CI、PR合并、部署或增加费用，冻结协议不变。
