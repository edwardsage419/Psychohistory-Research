# 自主认知：标点段商图与单头无环解析假设的结构边界
2026-11-26。RESEARCH_CANDIDATE / GOLD_CONDITIONED_STRUCTURAL_DIAGNOSTIC / REAL_EXTERNAL_DEVELOPMENT_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线
起点main cd8811c7dbd872eeb8b29104a182813b3cbffa0d，沿用本轮已核对v3.2、同步规程、25近期提交、15开放PR、固定历史交接（最新路径未定位），#63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍draft。前序段对候选排序 f70c690eb9280275b86c294f72fcd8655980de21 与跨标点诊断 research/decision_hub/2026-11-26-external-dependency-cross-punctuation-scope-diagnostic.md blob 0633533cebfb0cdea6aecff4e422bd3d4cdb5188；后者align/segments实际复用。既有词级依存解码及共同分词见证不重做，本轮针对将多个词压缩为一个原始标点段后，是否仍能保留单头无环结构的假设做诊断。非全库查重。
## 数据
同一已见UD_Chinese-GSDSimp dev 500句，固定commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3，blob af8cc878e7934b38ce3c1a266053100e7c47de6f。实际重新读取完整数据，许可沿用固定LICENSE CC BY-SA 4.0、README既有记录；本轮未独立重算原始Git字节、未重审许可。来源 https://github.com/UniversalDependencies/UD_Chinese-GSDSimp/tree/b79a1c2f7ba7f9b264808d91c6886a67b7f847a3 ，许可 https://creativecommons.org/licenses/by-sa/4.0/ 。不复制语料或标注，仅聚合计数与自有源码。无train/test读取、真人决策对话或独立留出。
## 合同及数学
原文标点段为节点，映射gold非root非punct边到不同段的有向关系，方向dependent→head；同段边不计，不能映射的单列。多个词弧可能共用同一段对，保留段对权重（弧计数）及九类从句/并列/标记代理计数。此处金标专供结构上界诊断，绝不作为生产候选生成输入。
一般树的任意顶点合并（非连通词集合）不保证所得商图仍为树。若某段有多个不同头段或商图有有向环，则任何单头无环段级表示均不能保留全部已映射有向段对。多个零出度不单独视为不可保留：可能通过新增未标注段对连接。固定每节点最多一个出边时，保留的gold弧数不超过各节点最大段对权重之和；唯一段对数不超过有出边节点数和n-1的较小者。对每节点枚举不选或选择任一gold头段，过滤环，独立分别最大化全部弧、九类代理弧及唯一段对数量，得到任何单头无环解析能保留的精确森林上界。三种最优值可能来自不同森林，不声称同时达到；任意树的已匹配边子集为森林，故上界成立。不保证可用未观察边扩展为实际语言树。枚举乘积超过100000时不运行精确部分，保留简单上界；此帽只控制完整枚举组合数，非设备墙时。用可达性SCC与独立Kahn检查有向环一致。不能把多头或环误判为原词级UD标注有错，也不证明句法语义、方法适用或授权。
## 实际结果
标准JS实际两次一致；5专项控制，逐句核对枚举组合与各上界及两种循环检测。原文段数和外部边计数与上轮一致。研究者选定段划分、权重、目标、枚举预算和标签；合成控制及真实开发诊断均非独立产品测试，未测真实用户/设备。所有研究输出无授权。
```json
{
  "sentences": 500,
  "aligned": 500,
  "segments": 1489,
  "crossSentences": 408,
  "crossArcs": 1404,
  "scopeArcs": 927,
  "uniquePairs": 1070,
  "anyMultiHead": 48,
  "multiHeadSegments": 56,
  "anyCycle": 66,
  "cyclicComponents": 68,
  "maxSCC": 3,
  "anyMultiOrCycle": 77,
  "anyMultipleZeroHead": 4,
  "treeNecessaryFails": 77,
  "weightUpper": 1347,
  "scopeUpper": 898,
  "pairUpper": 981,
  "exactSentences": 500,
  "exactArcsDenominator": 1404,
  "exactScopeDenominator": 927,
  "exactPairsDenominator": 1070,
  "exactUpper": 1297,
  "exactScopeUpper": 877,
  "exactPairUpper": 981,
  "cycleAdditionalLoss": 50,
  "enumerated": 25973,
  "skippedLarge": 0,
  "controls": 5,
  "unmapped": 17
}
```
## 接入
保留段级多关系候选图，不以树约束过早剪枝；需要在词级或事件级建立更准确的表示，再连接条件、主体、证据和科学方法。金标上界仅用于诊断，不提供实际最优解析策略。未修改生产、PR、交接、冻结、证据等级、训练、部署、主动CI或费用。
## 复算
固定dev.conllu和前序报告依序输入；仅加载审阅的自有固定JS。Node包装未运行，连接器核心已执行。
```js
const [data,previous]=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8"));
const code=previous.split("\`\`\`js\n")[1].split("\n\`\`\`")[0],make=Function(code.split(" const stat=()=>")[0]+"\nreturn {align,segments};\n}\nreturn study('');");
function study(data,make){
 const R=make(),ck=(v,m)=>{if(!v)throw Error(m)},delim=new Set(Array.from("，,、：:；;。！？!?")),scope=new Set(["advcl","ccomp","xcomp","parataxis","conj","csubj","acl","mark","cc"]);
 function analyze(n,arcs){
  const g=Array.from({length:n},()=>new Map());for(let a of arcs){ck(a.d!==a.h,"cross");let v=g[a.d].get(a.h)??{weight:0,scope:0};v.weight++;v.scope+=+scope.has(a.rel);g[a.d].set(a.h,v)}
  // Edges point dependent -> head. Transitive reachability for SCC identification.
  let reach=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j||g[i].has(j)));
  for(let k=0;k<n;k++)for(let i=0;i<n;i++)if(reach[i][k])for(let j=0;j<n;j++)reach[i][j]||=reach[k][j];
  let seen=new Set(),components=[];
  for(let i=0;i<n;i++)if(!seen.has(i)){let c=[];for(let j=0;j<n;j++)if(reach[i][j]&&reach[j][i]){seen.add(j);c.push(j)}components.push(c)}
  // A functional acyclic subgraph retaining one outgoing edge for each
  // non-root is a necessary condition for a segment dependency tree.
  const multi=g.filter(x=>x.size>1).length,cyclic=components.filter(x=>x.length>1),edgeCount=g.reduce((s,v)=>s+v.size,0),rootCount=g.filter(x=>!x.size).length;
  const weightUpper=g.reduce((s,m)=>s+Math.max(0,...[...m.values()].map(v=>v.weight)),0);
  const scopeUpper=g.reduce((s,m)=>s+Math.max(0,...[...m.values()].map(v=>v.scope)),0);
  // Any single-head acyclic subgraph must omit at least one directed pair
  // from every nontrivial SCC that has no alternative edges selected outside.
  // We do NOT subtract one per SCC from the single-head upper bound:
  // a multi-head deletion might already break a cycle.
  const pairUpper=Math.min(g.filter(x=>x.size).length,Math.max(0,n-1));
  // Exhaustive gold-conditioned maximum weighted forest for small graphs.
  // Each node can choose none or one observed outgoing pair, no unseen
  // pair gets positive value. This is an upper-bound diagnostic for any
  // single-head parse, never used as input to a real parser.
  let combinations=g.reduce((s,v)=>s*(v.size+1),1),exact=null,scopeExact=null,pairsExact=null,visited=0;
  if(combinations<=100000){
   const head=Array(n).fill(-1);
   function walk(i,w,s,p){
    if(i===n){
     visited++;for(let j=0;j<n;j++){let local=new Set(),k=j;while(k!==-1){if(local.has(k))return;local.add(k);k=head[k]}}
     exact=Math.max(exact??0,w);scopeExact=Math.max(scopeExact??0,s);pairsExact=Math.max(pairsExact??0,p);return;
    }
    head[i]=-1;walk(i+1,w,s,p);
    for(let [h,v] of g[i]){head[i]=h;walk(i+1,w+v.weight,s+v.scope,p+1)}
    head[i]=-1;
   }
   walk(0,0,0,0);ck(visited===combinations&&exact<=weightUpper&&scopeExact<=scopeUpper&&pairsExact<=pairUpper,"oracle bounds");
  }
  // Independent Kahn elimination for cycle detection, do not depend on SCC.
  let incoming=Array(n).fill(0);for(let m of g)for(let h of m.keys())incoming[h]++;
  let queue=incoming.flatMap((v,i)=>v===0?[i]:[]),removed=0;while(queue.length){let i=queue.pop();removed++;for(let h of g[i].keys())if(--incoming[h]===0)queue.push(h)}
  ck((removed!==n)===!!cyclic.length,"cycle oracle");
  return {multi,cyclic:cyclic.length,largestSCC:Math.max(0,...components.map(c=>c.length)),rootCount,edgeCount,weightUpper,scopeUpper,pairUpper,exact,scopeExact,pairsExact,combinations,visited};
 }
 const out={sentences:0,aligned:0,segments:0,crossSentences:0,crossArcs:0,scopeArcs:0,uniquePairs:0,anyMultiHead:0,multiHeadSegments:0,anyCycle:0,cyclicComponents:0,maxSCC:0,anyMultiOrCycle:0,anyMultipleZeroHead:0,treeNecessaryFails:0,weightUpper:0,scopeUpper:0,pairUpper:0,exactSentences:0,exactArcsDenominator:0,exactScopeDenominator:0,exactPairsDenominator:0,exactUpper:0,exactScopeUpper:0,exactPairUpper:0,cycleAdditionalLoss:0,enumerated:0,skippedLarge:0,controls:0,unmapped:0};
 for(let chunk of data.trim().split(/\n\s*\n/)){
  let ls=chunk.split(/\r?\n/),text=ls.find(x=>x.startsWith("# text = "))?.slice(9);if(text===undefined)continue;out.sentences++;
  let rows=ls.filter(x=>/^\d+\t/.test(x)).map(x=>x.split("\t")),z=R.align(text,rows);if(!z)continue;out.aligned++;
  let s=R.segments(z.chars,delim),arcs=[];
  function seg(p){let [a,b]=z.positions.get(p),v=[...new Set(s.index.slice(a,b).filter(i=>i>=0))];return v.length===1?v[0]:null}
  for(let r of rows){let h=+r[6],rel=r[7].split(":")[0];if(!h||rel==="punct"||r[3]==="PUNCT")continue;let d=seg(+r[0]),k=seg(h);if(d===null||k===null){out.unmapped++;continue}if(d!==k)arcs.push({d,h:k,rel})}
  let v=analyze(s.count,arcs),sc=arcs.filter(a=>scope.has(a.rel)).length;
  out.segments+=s.count;out.crossSentences+=+!!arcs.length;out.crossArcs+=arcs.length;out.scopeArcs+=sc;out.uniquePairs+=v.edgeCount;
  out.anyMultiHead+=+(v.multi>0);out.multiHeadSegments+=v.multi;out.anyCycle+=+(v.cyclic>0);out.cyclicComponents+=v.cyclic;out.maxSCC=Math.max(out.maxSCC,v.largestSCC);out.anyMultiOrCycle+=+(v.multi>0||v.cyclic>0);out.anyMultipleZeroHead+=+(v.rootCount>1);out.treeNecessaryFails+=+(v.multi>0||v.cyclic>0);out.weightUpper+=v.weightUpper;out.scopeUpper+=v.scopeUpper;out.pairUpper+=v.pairUpper;
  if(v.exact!==null){out.exactSentences++;out.exactArcsDenominator+=arcs.length;out.exactScopeDenominator+=sc;out.exactPairsDenominator+=v.edgeCount;out.exactUpper+=v.exact;out.exactScopeUpper+=v.scopeExact;out.exactPairUpper+=v.pairsExact;out.cycleAdditionalLoss+=v.weightUpper-v.exact;out.enumerated+=v.visited}else out.skippedLarge++;
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 let z=analyze(3,[{d:0,h:1,rel:"advcl"},{d:0,h:2,rel:"obj"},{d:0,h:2,rel:"obj"}]);ctl(z.multi===1&&z.weightUpper===2&&z.exact===2&&z.scopeExact===1,"multihead distinct objective");
 z=analyze(2,[{d:0,h:1,rel:"advcl"},{d:1,h:0,rel:"conj"}]);ctl(z.cyclic===1&&z.weightUpper===2&&z.exact===1,"cycle");
 z=analyze(3,[{d:0,h:1,rel:"advcl"},{d:1,h:2,rel:"conj"}]);ctl(z.exact===2&&z.pairsExact===2&&!z.cyclic,"chain");
 z=analyze(3,[]);ctl(z.exact===0&&z.rootCount===3,"missing connections");
 ctl(out.aligned===500&&out.crossArcs===1404&&out.scopeArcs===927&&out.uniquePairs===1070,"prior totals");
 return out;
}
console.log(JSON.stringify(study(data,make),null,2));
```
