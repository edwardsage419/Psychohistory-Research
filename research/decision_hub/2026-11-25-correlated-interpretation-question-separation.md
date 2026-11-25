# 自主认知专项累计第132轮候选：关联解释域的决策分离与最少澄清字段
2026-11-25。RESEARCH_CANDIDATE / EXACT_FINITE_SUPPORT_EXECUTED / SYNTHETIC_DEVELOPMENT / HOST_QUALIFIED_DOMAIN_ONLY / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main d5df77493164cbff630e523f1709acd0338c6d80。核对近期12提交、13开放PR（#61待审）、v3.2前15行及上一轮全文、唯一交接前18行、R131前17行及实际源码、R65前25行、R92前22行、R40前18行、v0.7任务前10行。R65明确完整笛卡尔解释域可用单维边检验相关性，但非笛卡尔域无此保证；R40处理多步有成本、含糊与拒答策略；本轮仅填补关联有限支持中的确定回答字段集合分离，不重做问询DP、角色分类或产品工程。
## 固定资产
research/decision_hub/2026-11-25-condition-polarity-attachment-candidate-audit.md 81df7d2fc56f29084ecc623b98cdf0991d3260d4
research/decision_hub/2026-11-25-unified-semantic-annotation-bridge.md af648d16ee96b9af4a3efb61b413d113208bb0ca
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
R65 b16928724409abc5e701dd8716371430a212dcf6；R92 a6948a9074c5adc974077d365c7c96672ecdfdcd；R40 56b1885f277b70797974ad48e80884a2d99dde81；v0.7任务 cae356da125f808c9a7feebe3940cc71e2347927。语料为ChatGPT研发辅助原创公开合成开发材料，非真人、独立留出或授权训练。
## 数学合同及证明
外部可信宿主已确认完整非空有限联合解释域 H⊆{0,1}^3 与每解释的单个二元决策出口 f(h)；三个坐标仅模拟守卫/目标/角色，实际含义、解释资格、真实数学、完整义务由外部给定。为使所问字段集合 Q 的确切答案唯一决定出口，对所有 f(h)≠f(k) 的解释对，必须且只需 Q 与差异字段集合 D(h,k) 相交：若不相交，两解释答案相同而出口不同；若全部相交，任意相同答案的解释只能共享出口。故最少字段是差异集合族的最小击中集，枚举8个字段子集精确求解、保留所有最小集合。一般维度问题为组合优化，未实现大域预算或优化。不同解释不赋概率，不独立扩展成笛卡尔域。示例关联支持 {000,011}，出口0与1；没有单坐标相邻解释，R65的单边诊断不能在此域使用；询问第一或第二坐标均能分离。本轮local对照是故意错误地将该诊断用于关联域，非R65原方法在合法域的错误。localInsufficient指仅询问全部被单边诊断标记的字段仍无法保证分离；localFalseInvariant为其中local=0且出口变化。最小字段数不等同真实问题数、用户认知成本或最优自适应决策树；确定回答、固定域、单一出口，无拒答、模糊回答、隐私或实际询问生成。必需确认字段用required掩码外加，即使出口不变仍独立保留（实验指定角色bit2，仅研究夹具，不是产品正式规则）；授权、重大风险和全部原文义务不能因数学等价省略。覆盖未知返回UNKNOWN、空域CONFLICT，所有authority NONE，无写入、推荐、自动更新或执行权。实际R131原始图均outside true，四项既有条件边仅核对出处及候选规模；不构造或宣称从它自动获得合格H、f、角色或确定答案。
## 实验
8个三维二值解释，255非空支持×256二元出口真值表，65280合成组合；全部比较击中集与独立按回答投影分桶直接核对，两路径同一研究者，共同夹具，非独立验收。再逐组要求角色字段，130560次分离比较合计；相同出口标签及支持的重复投影计数非独立样本。16项专项控制。实际调用R131 graph重查S中4条条件边的原文锚，非真实领域语义或用户测量。研究者选择维数、出口、单位字段成本及角色确认要求；未执行真机、原生、训练、Codex、CI、PR合并、部署、费用或冻结变更；不修改v0.7任务。产品轨维护唯一交接。
## 复算
按上述五份文件顺序置入docs[i].content，Node标准JS，仅加载已审查自有源码。
```js
function load(docs){
 const c=docs[0].content.split("```js\n")[1].split("\n```")[0];
 const {I,S}=Function(c.split("function experiment(I,S,corpora,assets)")[0]+"\nreturn load;")()(docs.slice(1));
 const graph=Function("I","S",c.slice(c.indexOf("function experiment(I,S,corpora,assets)")).split(" const out={turns:")[0]+"\nreturn graph;\n}\nreturn experiment(I,S);")(I,S);
 return graph
}
function experiment(graph,corpus){
 const ck=(v,m)=>{if(!v)throw Error(m)},pop=n=>{let k=0;while(n){n&=n-1;k++}return k},W=Array.from({length:8},(_,i)=>i);
 // Explicit externally specified finite domain. Coordinates are abstract
 // guard, target and role; outputs are arbitrary binary decision signatures.
 function solve(support,labels,covered=true,required=0){
  if(!covered||!Number.isInteger(support)||support<0||support>255||!Number.isInteger(labels)||labels<0||labels>255||!Number.isInteger(required)||required<0||required>7)return {status:"UNKNOWN",authority:"NONE"};
  if(!support)return {status:"CONFLICT",authority:"NONE"};
  const ws=W.filter(w=>support&(1<<w)),val=w=>(labels>>w)&1,clauses=new Set();let local=0;
  for(let i=0;i<ws.length;i++)for(let j=i+1;j<ws.length;j++){
   let a=ws[i],b=ws[j],d=a^b;if(val(a)===val(b))continue;
   clauses.add(d);if(pop(d)===1)local|=d
  }
  let best=4,choices=[];
  for(let q=0;q<8;q++){
   if((q&required)!==required||[...clauses].some(d=>!(d&q)))continue;
   let cost=pop(q);if(cost<best){best=cost;choices=[]}if(cost===best)choices.push(q)
  }
  return {status:clauses.size?"VARIES":"INVARIANT_CONDITIONAL",minimum:best,choices,local,clauses:[...clauses].sort((a,b)=>a-b),authority:"NONE"}
 }
 // Independent direct partition verification, no pair constraints.
 function reference(support,labels,required=0){
  const ws=W.filter(w=>support&(1<<w)),ok=[];
  for(let q=0;q<8;q++){
   if((q&required)!==required)continue;
   let bins=new Map(),valid=true;
   for(let w of ws){let k=w&q,y=(labels>>w)&1;if(bins.has(k)&&bins.get(k)!==y){valid=false;break}bins.set(k,y)}
   if(valid)ok.push(q)
  }
  let min=Math.min(...ok.map(pop));return {minimum:min,choices:ok.filter(q=>pop(q)===min)}
 }
 let out={cases:0,invariant:0,varies:0,localFalseInvariant:0,localInsufficient:0,minimumHistogram:[0,0,0,0],mandatoryCases:0,mandatoryMinimumIncrease:0,partitionChecks:0,rawCandidateExamples:[],controls:0,witness:null};
 for(let m=1;m<256;m++)for(let l=0;l<256;l++){
  let r=solve(m,l),o=reference(m,l);ck(r.minimum===o.minimum&&JSON.stringify(r.choices)===JSON.stringify(o.choices),"oracle");
  out.cases++;out.partitionChecks++;out.minimumHistogram[r.minimum]++;
  out.invariant+=+(r.status==="INVARIANT_CONDITIONAL");out.varies+=+(r.status==="VARIES");
  if(r.status==="VARIES"&&!r.local){out.localFalseInvariant++;out.witness??={support:W.filter(w=>m&(1<<w)),labels:W.filter(w=>l&(1<<w)),result:r}}
  if(r.clauses.some(d=>!(d&r.local)))out.localInsufficient++;
  // Require separate confirmation of role (bit 2), even when decision
  // signature alone is invariant. This is a research contract, not policy.
  let s=solve(m,l,true,4),p=reference(m,l,4);ck(s.minimum===p.minimum&&JSON.stringify(s.choices)===JSON.stringify(p.choices),"mandatory");
  out.mandatoryCases++;out.partitionChecks++;out.mandatoryMinimumIncrease+=+(s.minimum>r.minimum);
 }
 // Use actual R131 candidate graph for two existing raw texts, no automatic
 // semantic mapping. Select exact existing annotated guard/target only for
 // post-hoc illustration of the source identity, not evaluation of solve.
 for(let e of corpus.cases)for(let t of e.turns)for(let a of t.claims??t.proposal.claims){
  if(typeof a.condition!=="string"||!a.quote)continue;
  let g=graph(t.text),hits=g.edges.filter(x=>x.guard.text===a.condition&&x.target.text===a.quote);
  ck(hits.length>0,"actual edge");
  out.rawCandidateExamples.push({id:e.id,guard:a.condition,target:a.quote,edgeCount:g.edges.length,authority:g.authority,outside:g.outside})
 }
 for(let f of [()=>out.cases===65280,()=>out.invariant+out.varies===out.cases,()=>out.minimumHistogram.reduce((a,b)=>a+b,0)===out.cases,()=>out.localFalseInvariant>0,()=>out.localInsufficient>=out.localFalseInvariant,()=>out.mandatoryCases===out.cases,()=>out.rawCandidateExamples.length===4,()=>solve(9,8).local===0&&solve(9,8).minimum===1,()=>JSON.stringify(solve(9,8).choices)===JSON.stringify([1,2]),()=>solve(9,8,false).status==="UNKNOWN",()=>solve(0,0).status==="CONFLICT",()=>solve(255,0,true,4).minimum===1,()=>solve(255,0).minimum===0,()=>solve(255,170).minimum===1,()=>solve(256,0).status==="UNKNOWN",()=>solve(9,8).authority==="NONE"]){ck(f(),"control "+out.controls);out.controls++}
 return out
}
console.log(JSON.stringify(experiment(load(docs),JSON.parse(docs[4].content)),null,2));
```
## 实测
```json
{
  "cases": 65280,
  "invariant": 12610,
  "varies": 52670,
  "localFalseInvariant": 6656,
  "localInsufficient": 12032,
  "minimumHistogram": [
    12610,
    21062,
    22110,
    9498
  ],
  "mandatoryCases": 65280,
  "mandatoryMinimumIncrease": 30672,
  "partitionChecks": 130560,
  "rawCandidateExamples": [
    {
      "id": "S03",
      "guard": "如果周五需要加班",
      "target": "周五答疑就取消",
      "edgeCount": 203,
      "authority": "NONE",
      "outside": true
    },
    {
      "id": "S06",
      "guard": "如果医生允许",
      "target": "参加长跑活动",
      "edgeCount": 314,
      "authority": "NONE",
      "outside": true
    },
    {
      "id": "S09",
      "guard": "如果集合改到周一早上",
      "target": "隔天出发也可以",
      "edgeCount": 308,
      "authority": "NONE",
      "outside": true
    },
    {
      "id": "S13",
      "guard": "正式交付",
      "target": "准确率的要求仅用于正式交付",
      "edgeCount": 544,
      "authority": "NONE",
      "outside": true
    }
  ],
  "controls": 16,
  "witness": {
    "support": [
      1,
      2
    ],
    "labels": [
      1
    ],
    "result": {
      "status": "VARIES",
      "minimum": 1,
      "choices": [
        1,
        2
      ],
      "local": 0,
      "clauses": [
        3
      ],
      "authority": "NONE"
    }
  }
}
```
下一步优先研究从实际原文候选到关系身份及可核查联合支持的连接；数据轨/独立轨负责合法真实资料和未见验证，避免重复有限枚举。正式工程、训练另获授权。
