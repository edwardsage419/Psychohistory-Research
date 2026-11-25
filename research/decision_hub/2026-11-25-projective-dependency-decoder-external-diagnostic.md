# 自主认知专项累计第136轮候选：单根投射依存树全局解码与外部开发集诊断
2026-11-25。RESEARCH_CANDIDATE / EXACT_PROJECTIVE_DECODER_EXECUTED / EXTERNAL_DEVELOPMENT_ANNOTATION_CONDITIONED / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 48a7312da60760c84ba2afd20cd6dd1ec0ae760c。核对近期12提交、13开放PR、v3.2前15行及历史全文、唯一交接前18行、R135前15行、R72前22行、R61前12行、v0.7任务前10行；R135只做已知否定锚的局部依附排序，R61是固定布尔表达式解析，本轮新增全句单根投射依存解码算法，未训练或改动正式工程。
## 来源与数据
Eisner (1996), Three New Probabilistic Models for Dependency Parsing: An Exploration, COLING, https://aclanthology.org/C96-1058/ ，DOI 10.3115/992628.992688，实际检索英文书目与出版商摘要（报告三次方依存解析算法），未通读PDF、未运行作者代码或复现概率模型。以下为自写Eisner式弧分解最大分数动态规划，不声称原创数学。固定UD Chinese GSDSimp dev blob af8cc878e7934b38ce3c1a266053100e7c47de6f，commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3，实际重新取得全文并调用R134原audit（db9cc100d96d49832fe32879a706f63830301773）核验1195378字节及Git SHA1。R135 d81cbedafee148a0c1e065f39254bac7abe6e14d；R72 82f53eb20bcb7b49e0e56088a7c2c586000627fa；R61 17b6035732e43c56edc44cb5db07b8d49aadfd5b。仅外部开发集，未读取train/test，未重新分发文本、未训练；CC BY-SA 4.0树库许可及底层文本权利的区别沿R134/135，训练准入未闭合。
## 数学与实验
每条有向弧赋固定整数分数w(h,i)，目标最大化各词元唯一父弧分数和。局部基线逐词取同一分数最大父节点，可能多根或循环，不是现有产品。全局动态规划使用左右端点为头的完整跨度C、不完整跨度I；I由左右完整跨度拼接并加端点弧，C由完整与不完整跨度拼接。根r枚举时连接左完整跨度C(1,r,0)、右完整跨度C(r,n,1)及w(0,r)，确保单根；回溯记录父节点。弧分解及投射约束下标准跨度分解覆盖合法树，最优子结构及归纳保证最优，时间O(n^3)、图表空间O(n^2)，不含输入与资源开销。仅允许投射树，非投射金标未必在解域；完整句法树也不保证语义正确。固定分数为研究者选定的距离惩罚、根谓词偏好、词性组合及标点惩罚，未拟合权重，不从句法真值读取评分；输入仍需外部给定token及UPOS，不是原文自主分词。使用HEAD作事后无标签依附匹配代理，包含及排除标点分别统计、根及否定锚单列。合法树与依附准确分离，局部非法树的逐弧匹配仅诊断。金标投射性用弧内部词元祖先关系检验；每个输出检查单根无环、投射、分数一致；金标在域内时最优分数不得低于其分数。200个确定性1..5词元整数矩阵（含禁弧）与独立枚举合法树最大分对照，同一研究者、非独立验收；11控制。超过200词元或10000000图表操作LIMIT，不返回截断树，预算不覆盖构图、内存、回溯、真机时间。输出authority NONE、outside true，单一最优树不证明完整解释，不生成语义约束或数学资格。无训练、原生、Codex、CI、PR合并、部署、费用或冻结变化，v0.7不变。用户未指定评分，全部研究者选定；不能把已见开发集结果当泛化或用于直接部署。
## 复算
先以固定原始raw运行R134 audit，再执行下列标准JS。
```js
function experiment(raw){
 const ck=(v,m)=>{if(!v)throw Error(m)},pred=new Set(["VERB","ADJ","AUX"]);
 function valid(h,projective){
  let n=h.length-1;if(h.slice(1).filter(x=>x===0).length!==1)return false;
  for(let i=1;i<=n;i++){let seen=new Set(),j=i;while(j){if(!Number.isInteger(j)||j<1||j>n||seen.has(j))return false;seen.add(j);j=h[j]}}
  if(projective)for(let i=1;i<=n;i++)for(let j=Math.min(i,h[i])+1;j<Math.max(i,h[i]);j++){let k=j;while(k&&k!==h[i])k=h[k];if(k!==h[i])return false}
  return true
 }
 const score=(w,h)=>h.slice(1).reduce((s,p,i)=>s+w[p][i+1],0);
 function decode(w,limit=10000000){
  let n=w.length-1;if(n<1||n>200)return {status:"LIMIT"};let count=0;
  // Complete/incomplete spans; direction 0=head right, 1=head left.
  const make=()=>Array.from({length:n+1},()=>Array.from({length:n+1},()=>[-Infinity,-Infinity]));
  const C=make(),I=make(),bc=make(),bi=make();
  for(let i=1;i<=n;i++)C[i][i]=[0,0];
  for(let len=1;len<n;len++)for(let s=1;s+len<=n;s++){
   let t=s+len,b=-Infinity,k=-1;
   for(let r=s;r<t;r++){if(++count>limit)return {status:"LIMIT"};let v=C[s][r][1]+C[r+1][t][0];if(v>b){b=v;k=r}}
   I[s][t][0]=b+w[t][s];I[s][t][1]=b+w[s][t];bi[s][t]=[k,k];
   for(let r=s;r<t;r++){if(++count>limit)return {status:"LIMIT"};let v=C[s][r][0]+I[r][t][0];if(v>C[s][t][0]){C[s][t][0]=v;bc[s][t][0]=r}}
   for(let r=s+1;r<=t;r++){if(++count>limit)return {status:"LIMIT"};let v=I[s][r][1]+C[r][t][1];if(v>C[s][t][1]){C[s][t][1]=v;bc[s][t][1]=r}}
  }
  let best=-Infinity,root=-1;for(let r=1;r<=n;r++){if(++count>limit)return {status:"LIMIT"};let v=C[1][r][0]+C[r][n][1]+w[0][r];if(v>best){best=v;root=r}}
  if(root<0)return {status:"NO_TREE"};
  let heads=Array(n+1).fill(-1);heads[root]=0;
  function trace(s,t,d,complete){if(s===t)return;let r=(complete?bc:bi)[s][t][d];ck(Number.isInteger(r)&&r>=s&&r<=t,"trace");if(!complete){heads[d?t:s]=d?s:t;trace(s,r,1,true);trace(r+1,t,0,true)}else if(d===0){trace(s,r,0,true);trace(r,t,0,false)}else{trace(s,r,1,false);trace(r,t,1,true)}}
  trace(1,root,0,true);trace(root,n,1,true);
  ck(valid(heads,true)&&score(w,heads)===best,"decoded tree");
  return {status:"CANDIDATE",heads,best,count,authority:"NONE",outside:true}
 }
 function brute(w){let n=w.length-1,h=Array(n+1).fill(-1),best=-Infinity;function go(i){if(i>n){if(valid(h,true))best=Math.max(best,score(w,h));return}for(let p=0;p<=n;p++)if(p!==i&&Number.isFinite(w[p][i])){h[i]=p;go(i+1)}}go(1);return best}
 function matrix(ts){
  let n=ts.length-1;return Array.from({length:n+1},(_,p)=>Array.from({length:n+1},(_,i)=>{
   if(!i||p===i)return -Infinity;
   if(!p)return pred.has(ts[i].pos)?4:ts[i].pos==="PUNCT"?-8:0;
   let a=ts[p].pos,b=ts[i].pos,d=Math.abs(i-p),v=-2*d;
   if(a==="PUNCT")v-=8;
   if(pred.has(a)&&["NOUN","PROPN","PRON","ADV","AUX","SCONJ","PUNCT","PART"].includes(b))v+=4;
   if(["NOUN","PROPN"].includes(a)&&["ADJ","DET","NUM"].includes(b))v+=4;
   return v
  }))
 }
 function greedy(w){return w[0].map((_,i)=>{if(!i)return -1;let p=0;for(let j=1;j<w.length;j++)if(w[j][i]>w[p][i])p=j;return p})}
 const out={sentences:0,tokens:0,nonPunct:0,goldProjective:0,processed:0,limited:0,greedyTree:0,greedyProjective:0,globalTree:0,globalProjective:0,greedyCorrect:0,globalCorrect:0,greedyNonPunctCorrect:0,globalNonPunctCorrect:0,globalImprovedSentences:0,globalWorseSentences:0,globalEqualSentences:0,greedyRootCorrect:0,globalRootCorrect:0,globalGoldScoreHigher:0,globalGoldScoreEqual:0,globalGoldScoreLower:0,negativeNonroot:0,greedyNegCorrect:0,globalNegCorrect:0,oracleCases:0,oracleNoTree:0,maxTokens:0,chartOps:0,maxChartOps:0,controls:0};
 for(let block of raw.trimEnd().split(/\n\n+/)){
  let ts=[null,...block.split("\n").filter(l=>!l.startsWith("#")).map(l=>{let c=l.split("\t");return {pos:c[3],head:+c[6],neg:c[5].split("|").includes("Polarity=Neg")}})];
  let n=ts.length-1,gold=ts.map(t=>t?.head??-1);out.sentences++;out.maxTokens=Math.max(n,out.maxTokens);let gp=valid(gold,true);out.goldProjective+=+gp;
  const w=matrix(ts),g=greedy(w),r=decode(w);
  if(r.status==="LIMIT"){out.limited++;continue}ck(r.status==="CANDIDATE","parse");
  out.processed++;out.tokens+=n;out.chartOps+=r.count;out.maxChartOps=Math.max(out.maxChartOps,r.count);
  out.greedyTree+=+valid(g,false);out.greedyProjective+=+valid(g,true);out.globalTree+=+valid(r.heads,false);out.globalProjective+=+valid(r.heads,true);
  let a=0,b=0;for(let i=1;i<=n;i++){let x=g[i]===gold[i],y=r.heads[i]===gold[i];a+=+x;b+=+y;if(ts[i].pos!=="PUNCT"){out.nonPunct++;out.greedyNonPunctCorrect+=+x;out.globalNonPunctCorrect+=+y}if(!gold[i]){out.greedyRootCorrect+=+x;out.globalRootCorrect+=+y}if(ts[i].neg&&gold[i]){out.negativeNonroot++;out.greedyNegCorrect+=+x;out.globalNegCorrect+=+y}}
  out.greedyCorrect+=a;out.globalCorrect+=b;out.globalImprovedSentences+=+(b>a);out.globalWorseSentences+=+(b<a);out.globalEqualSentences+=+(b===a);
  let gs=score(w,gold);out.globalGoldScoreHigher+=+(r.best>gs);out.globalGoldScoreEqual+=+(r.best===gs);out.globalGoldScoreLower+=+(r.best<gs);
  if(gp)ck(r.best>=gs,"projective gold lower bound");
  if(valid(g,true))ck(r.best===score(w,g),"greedy optimum");
 }
 // Deterministic varied integer arc matrices, independent exhaustive tree reference.
 for(let n=1;n<=5;n++)for(let seed=0;seed<40;seed++){
  let w=Array.from({length:n+1},(_,p)=>Array.from({length:n+1},(_,i)=>!i||p===i||(seed%5===0&&((p*13+i*7+seed)%4===0))?-Infinity:((p*37+i*19+seed*23+p*i*11)%17)-8));
  let b=brute(w),r=decode(w);ck(Number.isFinite(b)?r.status==="CANDIDATE"&&r.best===b:r.status==="NO_TREE","brute");out.oracleCases++;out.oracleNoTree+=+!Number.isFinite(b)
 }
 for(let f of [()=>out.sentences===500,()=>out.processed+out.limited===500,()=>out.globalTree===out.processed&&out.globalProjective===out.processed,()=>out.globalImprovedSentences+out.globalWorseSentences+out.globalEqualSentences===out.processed,()=>out.globalGoldScoreHigher+out.globalGoldScoreEqual+out.globalGoldScoreLower===out.processed,()=>out.oracleCases===200,()=>decode(matrix([null,{pos:"VERB"},{pos:"NOUN"}]),0).status==="LIMIT",()=>!valid([-1,2,1],false),()=>!valid([-1,0,0],false),()=>!valid([-1,3,4,0,3],true),()=>decode([[-Infinity,0],[-Infinity,-Infinity]]).heads[1]===0]){ck(f(),"control "+out.controls);out.controls++}
 return out
}
console.log(JSON.stringify(experiment(raw),null,2));
```
## 实测
```json
{
  "sentences": 500,
  "tokens": 12665,
  "nonPunct": 10895,
  "goldProjective": 495,
  "processed": 500,
  "limited": 0,
  "greedyTree": 0,
  "greedyProjective": 0,
  "globalTree": 500,
  "globalProjective": 500,
  "greedyCorrect": 2263,
  "globalCorrect": 3254,
  "greedyNonPunctCorrect": 1900,
  "globalNonPunctCorrect": 2924,
  "globalImprovedSentences": 359,
  "globalWorseSentences": 55,
  "globalEqualSentences": 86,
  "greedyRootCorrect": 491,
  "globalRootCorrect": 156,
  "globalGoldScoreHigher": 500,
  "globalGoldScoreEqual": 0,
  "globalGoldScoreLower": 0,
  "negativeNonroot": 37,
  "greedyNegCorrect": 16,
  "globalNegCorrect": 22,
  "oracleCases": 200,
  "oracleNoTree": 2,
  "maxTokens": 84,
  "chartOps": 7638689,
  "maxChartOps": 296394,
  "controls": 11
}
```
后续：比较非投射解码、可学习弧特征和解析不确定性保留，优先解决合法数据及真实决策语义关联，训练另获授权。
