# 自主认知专项累计第86轮候选：有方向跨轮特征、共享编码及语义属性隔离

2026-11-25。RESEARCH_CANDIDATE / FIXED_FEATURE_SHARING_EXECUTED / ORACLE_NODES_AND_ATTRIBUTES / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线 main c08fb1a763352c0458e6a2913fffd8b66c83822f。核对最近20提交、13开放PR（#61待审）、v3.2首8行及此前全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R85、R76、R73、R64前16行。区别于R76引用分区及排序、R64版本身份、R85原文稀疏编码：本轮研究跨轮边的有方向共享特征分解、显式属性缺失、监督字段隔离及静态特征条目规模，不重做排序或训练。无新增外部资料。

## 输入及边界
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
读取完整固定JSON并核对blob。32情节64轮167标注，ChatGPT研发辅助公开原创合成开发材料，非真人、独立留出或获授权训练。节点及属性由原标注提供，属于teacher-forced诊断，绝不声称由原文自动识别。使用原文跨度、左右8个UTF16字符和1..3码点元组，保留原文锚点。L与S的operation/comparison分离；L角色kind与S role保留原始类别、不宣称跨schema语义等价。10维主体、时间、情态、修订操作、比较符、条件、field、角色、单位、scope独立记录ANNOTATED/EXPLICIT_NULL/UNANNOTATED；缺失不补默认，不等同否定或无条件。属性变化为反事实夹具，不是实际语言变化或真实监督标签。没有独立否定维度，现有modality只能表达部分情态，否定作用域仍未实现。实际实体身份、版本、授权、真实概念与知识来源另走可信宿主；特征不是身份。

## 方法
同情节前轮与当前轮全部标注节点两两候选，不根据ref筛选；只在事后核对12条已标引用，不将45个未标/空引用视为负例。对照无方向的词面集合并集；有方向的先前/当前词面特征块加有符号轮距、同原文、共享特征数；再加标注提供的10维节点属性和有方向关系特征，含相等/不等/未知。无方向集合为故意简化的诊断对照，不是原生平台。真实边方向由时序确定，反向测试是编码区分性检查、非预测任务。有向特征使用轮距，反向一定不同是设计保证。方向不能决定哪条边真实成立；唯一向量不是唯一意图。节点块前缀分离，边特征不重复；固定整数权重由特征键哈希确定（非训练、非安全哈希），逐边验证完整加法分数等于先前节点分数+当前节点分数+关系分数。完整条目计数以每候选边复制特征为对照；共享计数以参与边节点一次存储、边关系每边存储为假设，忽略索引、字典、实际字节、构建和缓存开销；没有实测设备性能、复杂交互或非加法模型。实际代码为审计同时生成两种形式，不宣称已经减少运行内存。标签隔离仅验证改动ref/supersedes/expected/forbid/question/outcome不改变节点特征，不代表全系统无泄漏；原标注属性本身是oracle信息，部署时不能作为已知字段。当前轮后面的同轮文本可作为该轮完整输入上下文；不使用未来轮。无训练、校准、准确率、独立效果。所有特征仅候选用途，执行权限NONE；未实现持久化、真实授权或原生接入。

## 可复算代码
按L/S顺序载入两个JSON。
```js
function experiment(docs){
 const ck=(x,m)=>{if(!x)throw Error(m)},key=(...a)=>JSON.stringify(a),ordered=a=>[...a].sort(),sig=a=>JSON.stringify(ordered(a)),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const dimensions=["actor","time","modality","operation","comparison","condition","field","role","unit","scope"];
 // Allowlist; no ref/supersedes, outcome, expected, forbid, question, IDs or domain in features.
 const known=(obj,k)=>!Object.hasOwn(obj,k)?["UNANNOTATED"]:obj[k]===null?["EXPLICIT_NULL"]:["ANNOTATED",obj[k]];
 function node(d,t,c,turn,index){
  let q=d===0?c.span:c.quote,at=t.text.indexOf(q);ck(at>=0&&at===t.text.lastIndexOf(q),"anchor");
  let attrs={actor:known(c,"actor"),time:known(c,"time"),modality:known(c,"modality"),operation:known(c,d===0?"operation":"op"),comparison:d===0?known(c,"op"):["UNANNOTATED"],condition:known(c,"condition"),field:known(c,"field"),role:known(c,d===0?"kind":"role"),unit:known(c,"unit"),scope:known(c,"scope")};
  return {q,at,end:at+q.length,turn,index,attrs,left:t.text.slice(Math.max(0,at-8),at),right:t.text.slice(at+q.length,at+q.length+8)};
 }
 function lexical(n){let f=new Set([key("len",[...n.q].length),key("left",n.left),key("right",n.right)]);let a=[...n.q];for(let k=1;k<=3;k++)for(let i=0;i+k<=a.length;i++)f.add(key("ng",k,a.slice(i,i+k).join("")));return f}
 function typed(n){let f=new Set(lexical(n));for(let d of dimensions)f.add(key("attr",d,n.attrs[d]));return f}
 function relation(a,b,meta){
  let f=new Set([key("gap",b.turn-a.turn),key("sameQuote",a.q===b.q)]),x=lexical(a),y=lexical(b);
  let inter=[...x].filter(v=>y.has(v)).length;f.add(key("sharedCount",inter));
  if(meta)for(let d of dimensions){let u=a.attrs[d],v=b.attrs[d];f.add(key("pair",d,u,v));f.add(key("agreement",d,u[0]!=="ANNOTATED"||v[0]!=="ANNOTATED"?"UNRESOLVED":eq(u,v)?"EQUAL":"DIFFERENT"))}
  return f;
 }
 function features(a,b,mode){
  let x=mode==="typed"?typed(a):lexical(a),y=mode==="typed"?typed(b):lexical(b);
  if(mode==="unordered")return new Set([...x,...y]);
  return new Set([...x].map(v=>key("prior",v)).concat([...y].map(v=>key("current",v)),[...relation(a,b,mode==="typed")]));
 }
 // Pure factorized additive score, deterministic integer weights from a key hash; not fitted.
 function w(s){let h=2166136261;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}return (h>>>0)%17-8}
 const sum=f=>[...f].reduce((n,k)=>n+w(k),0);
 const roleScore=(n,side)=>sum([...typed(n)].map(v=>key(side,v)));
 const result={episodes:0,nodes:0,edges:0,markedLinks:0,unmarkedCurrent:0,priorNodes:0,currentNodes:0,flatFeatureEntries:0,sharedNodeEntries:0,sharedRelationEntries:0,maxFlatEntries:0,scoreChecks:0,featureVocab:0,fieldStates:{},reverseSame:{unordered:0,directed:0,typed:0},sameSignatureExtraEdges:{unordered:0,directed:0,typed:0},knownLinkTieGroups:{unordered:0,directed:0,typed:0},metadataMutations:0,metadataMutationDetected:0,rawMutationInvisible:0,leakageChecks:0,controls:0};
 const vocab=new Set();
 for(let d=0;d<docs.length;d++)for(let ep of docs[d].cases){
  result.episodes++;let rows=ep.turns.map((t,ti)=>(d===0?t.claims:t.proposal.claims).map((c,i)=>node(d,t,c,ti,i)));
  ck(rows.length===2,"turns");let [a,b]=rows;result.priorNodes+=a.length;result.currentNodes+=b.length;result.nodes+=a.length+b.length;
  for(let n of [...a,...b])for(let dim of dimensions){let s=n.attrs[dim][0],o=result.fieldStates[dim]??={};o[s]=(o[s]||0)+1}
  // Only nodes participating in edges stored; use side-specific coefficient blocks.
  if(a.length&&b.length){result.sharedNodeEntries+=a.reduce((v,n)=>v+typed(n).size,0)+b.reduce((v,n)=>v+typed(n).size,0)}
  let ac=a.map(n=>roleScore(n,"prior")),bc=b.map(n=>roleScore(n,"current"));
  let groups={unordered:new Map(),directed:new Map(),typed:new Map()};
  for(let i=0;i<a.length;i++)for(let j=0;j<b.length;j++){
   let u=a[i],v=b[j];result.edges++;
   for(let mode of Object.keys(groups)){
    let f=features(u,v,mode),s=sig(f);groups[mode].set(s,(groups[mode].get(s)||[]).concat([[i,j]]));
    result.reverseSame[mode]+=+(s===sig(features(v,u,mode)));
    if(mode==="typed"){result.flatFeatureEntries+=f.size;result.maxFlatEntries=Math.max(result.maxFlatEntries,f.size);for(let k of f)vocab.add(k);let rel=relation(u,v,true);result.sharedRelationEntries+=rel.size;ck(sum(f)===ac[i]+bc[j]+sum(rel),"factorization");result.scoreChecks++}
   }
  }
  for(let mode of Object.keys(groups))for(let g of groups[mode].values())result.sameSignatureExtraEdges[mode]+=g.length-1;
  let bb=d===0?ep.turns[1].claims:ep.turns[1].proposal.claims,aa=d===0?ep.turns[0].claims:ep.turns[0].proposal.claims;
  for(let j=0;j<bb.length;j++){
   let c=bb[j],ref=d===0?c.supersedes:c.ref;
   if(typeof ref==="string"){
    let i=d===0?aa.findIndex(x=>x.field===ref.split(":").at(-1)):Number(ref.split(".").at(-1))-1;ck(i>=0&&i<a.length,"reference");result.markedLinks++;
    for(let mode of Object.keys(groups))result.knownLinkTieGroups[mode]+=+(groups[mode].get(sig(features(a[i],b[j],mode))).length>1);
   }else result.unmarkedCurrent++;
   // Change labels of the reference and future/outcome metadata; never used as features.
   let fake={...c,ref:"fake",supersedes:"fake",expected:"fake",forbid:["fake"],question:"fake",outcome:"fake"};
   ck(sig(typed(node(d,ep.turns[1],fake,1,j)))===sig(typed(b[j])),"label leakage");result.leakageChecks++;
   for(let dim of ["actor","time","modality","operation","condition"]){
    let v={...b[j],attrs:{...b[j].attrs,[dim]:["ANNOTATED","COUNTERFACTUAL_FIXTURE"]}};
    result.metadataMutations++;if(sig(typed(v))!==sig(typed(b[j])))result.metadataMutationDetected++;
    if(sig(lexical(v))===sig(lexical(b[j])))result.rawMutationInvisible++;
    if(a.length)ck(sig(features(a[0],v,"typed"))!==sig(features(a[0],b[j],"typed")),"metadata relation");
   }
  }
 }
 result.featureVocab=vocab.size;result.sharedTotalEntries=result.sharedNodeEntries+result.sharedRelationEntries;result.savedEntries=result.flatFeatureEntries-result.sharedTotalEntries;
 for(let t of [()=>result.episodes===32,()=>result.nodes===167,()=>result.markedLinks===12,()=>result.unmarkedCurrent===45,()=>result.scoreChecks===result.edges,()=>result.reverseSame.unordered===result.edges,()=>result.reverseSame.directed===0,()=>result.reverseSame.typed===0,()=>result.metadataMutationDetected===result.metadataMutations,()=>result.rawMutationInvisible===result.metadataMutations,()=>result.leakageChecks===result.currentNodes,()=>result.savedEntries>=0,()=>result.fieldStates.actor.UNANNOTATED>0]){ck(t(),"control");result.controls++}
 return result;
}
```

## 实测
```json
{
  "episodes": 32,
  "nodes": 167,
  "edges": 191,
  "markedLinks": 12,
  "unmarkedCurrent": 45,
  "priorNodes": 110,
  "currentNodes": 57,
  "flatFeatureEntries": 16547,
  "sharedNodeEntries": 5219,
  "sharedRelationEntries": 4393,
  "maxFlatEntries": 121,
  "scoreChecks": 191,
  "featureVocab": 3199,
  "fieldStates": {
    "actor": {
      "UNANNOTATED": 98,
      "ANNOTATED": 69
    },
    "time": {
      "UNANNOTATED": 98,
      "ANNOTATED": 69
    },
    "modality": {
      "UNANNOTATED": 98,
      "ANNOTATED": 69
    },
    "operation": {
      "UNANNOTATED": 95,
      "ANNOTATED": 72
    },
    "comparison": {
      "ANNOTATED": 10,
      "UNANNOTATED": 157
    },
    "condition": {
      "UNANNOTATED": 97,
      "ANNOTATED": 5,
      "EXPLICIT_NULL": 65
    },
    "field": {
      "ANNOTATED": 98,
      "UNANNOTATED": 69
    },
    "role": {
      "ANNOTATED": 167
    },
    "unit": {
      "ANNOTATED": 22,
      "UNANNOTATED": 145
    },
    "scope": {
      "ANNOTATED": 3,
      "UNANNOTATED": 164
    }
  },
  "reverseSame": {
    "unordered": 191,
    "directed": 0,
    "typed": 0
  },
  "sameSignatureExtraEdges": {
    "unordered": 0,
    "directed": 0,
    "typed": 0
  },
  "knownLinkTieGroups": {
    "unordered": 0,
    "directed": 0,
    "typed": 0
  },
  "metadataMutations": 285,
  "metadataMutationDetected": 285,
  "rawMutationInvisible": 285,
  "leakageChecks": 57,
  "controls": 13,
  "sharedTotalEntries": 9612,
  "savedEntries": 6935
}
```

## 后续
原文候选与概念关系证据需要同样的显式属性和来源分离；后续可设计共享编码与R84联合因素的计算接口、独立数据和资源预算。真实长对话、非标注属性抽取、语义角色学习及组合泛化仍未知。研究者选定特征、窗口、维度、对照、整数权重。13项控制为同一研究者设计，非独立验收。保留R50完整版本范围及正式验收门，无训练、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。
