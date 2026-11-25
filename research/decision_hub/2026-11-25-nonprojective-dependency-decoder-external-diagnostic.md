# 自主认知专项累计第137轮：非投射单根依存树搜索与评分缺陷
2026-11-25。RESEARCH_CANDIDATE / EXACT_UNRESTRICTED_DECODER_EXECUTED / EXTERNAL_DEVELOPMENT_ANNOTATION_CONDITIONED / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 6bebd37ebb3f85e6e575e6a0ac36c525dd43ce18。核对近期12提交、14开放PR、v3.2前12行及历史全文、唯一交接前12行、R136实际源码及R134原audit。新增Draft PR #62 head e61bbad10932edabc9a87483e5407fdae6c751cc，其作者报告631 Python测试、84移动测试通过，硬义务12/27、条件0/5、他人主体0/4、账本修订0/10，未独立复验，未合并。本轮不改变工程候选或验收门。
## 来源与数据
实际检索英文ACL书目及作者PDF搜索摘要（未打开或分析PDF全文）：McDonald, Pereira, Ribarov & Hajič (2005), Non-Projective Dependency Parsing using Spanning Tree Algorithms, https://aclanthology.org/H05-1066/ 。借鉴有向最大生成树的Chu-Liu-Edmonds收缩思路，自写算法，不复现论文训练或性能。R134 db9cc100d96d49832fe32879a706f63830301773、R136 c40a09357a858644a0da922097cd6367ca696df6，实际重新取得UD Chinese GSDSimp dev blob af8cc878e7934b38ce3c1a266053100e7c47de6f，调用R134验证字节与Git SHA1，实际复用R136固定评分、投射解码、校验及求和。沿用既有数据许可边界，未读取train/test、训练或重新分发原文。已见开发集仅诊断，外部给定分词及UPOS。
## 数学
在虚根0的有向图上求最大生成树。每非根节点选最大入弧；若形成环，收缩成单点，外部入弧权重减去被替代的环内入弧，出弧不变；递归求解后恢复所有环内入弧，唯独去除实际外部进入的节点入弧。固定环内入弧总权重是常数，调整后的目标等价于原树目标；递归收缩减少节点，恢复合法根树。令M=n(max w-min w)+1，从每个虚根出弧扣M，任何两棵树原分差不超过n(max-min)，故先最小化根出弧数，再最大化原分；若最优树根数不为1，则没有单根可行树。限定有限整数安全范围的夹具，未实现任意大整数、恶意输入或全面资源防护。简单收缩实现并非论文优化复杂度承诺；累计边扫描和路径操作预算，未计入构图/内存/回溯；最多200词元。超预算LIMIT。无树NO_TREE仅指给定有限图。单一最优树不保证语言语义正确，始终outside true、authority NONE。与R136完全相同评分比较，分数严格增益和金标匹配分开，平分时选择不同树也可能导致匹配变化；不能将全部匹配差异归因于非投射。300个小矩阵独立枚举单根无环树对照，10项控制；同研究者，非独立验收。未使用真实数据训练，评分与预算由研究者选定。无CI、正式代码、部署、PR合并、新费用或冻结变更。
## 复算
a,b为R134/R136完整连接器内容对象，raw为固定源UTF8。仅执行已审查自有源码。
```js
function load(a,b,raw){
 const code=x=>x.content.split("```js\n")[1].split("\n```")[0];
 const audit=Function(code(a).split("console.log(JSON.stringify(audit(raw)")[0]+"\nreturn audit;")();
 const P=Function(code(b).split(" const out={sentences:")[0]+"\nreturn {valid,score,decode,matrix};\n}\nreturn experiment();")();
 return {P,verified:audit(raw)}
}
function experiment(P,raw){
 const ck=(x,m)=>{if(!x)throw Error(m)};
 // Maximum rooted directed tree with a lexicographic penalty on root arcs.
 function solve(w,limit=10000000){
  const n=w.length-1;if(n<1||n>200)return {status:"LIMIT"};
  let values=w.flat().filter(Number.isFinite);if(!values.length)return {status:"NO_TREE"};
  let M=n*(Math.max(...values)-Math.min(...values))+1,ops=0,serial=n+1,limited=false,cycles=0;
  const take=()=>{if(++ops>limit){limited=true;return false}return true};
  function mst(nodes,edges){
   let ins=new Map();
   for(let e of edges){if(!take())return null;if(e.v!==0&&(!ins.has(e.v)||ins.get(e.v).w<e.w))ins.set(e.v,e)}
   if(nodes.some(v=>v!==0&&!ins.has(v)))return null;
   let cycle=null,done=new Set([0]);
   for(let v of nodes){if(done.has(v))continue;let trail=new Set(),j=v;
    while(!done.has(j)&&!trail.has(j)){if(!take())return null;trail.add(j);j=ins.get(j).u}
    if(trail.has(j)){cycle=new Set([j]);for(let k=ins.get(j).u;k!==j;k=ins.get(k).u)cycle.add(k);break}
    for(let k of trail)done.add(k)
   }
   if(!cycle)return [...ins.values()];
   cycles++;let z=serial++,ne=[];
   for(let e of edges){if(!take())return null;let x=cycle.has(e.u),y=cycle.has(e.v);if(x&&y)continue;ne.push({u:x?z:e.u,v:y?z:e.v,w:e.w-(y?ins.get(e.v).w:0),prev:e})}
   let t=mst(nodes.filter(v=>!cycle.has(v)).concat(z),ne);if(!t)return null;
   let result=t.map(e=>e.prev),enter=t.find(e=>e.v===z);ck(enter,"enter");
   for(let v of cycle)if(v!==enter.prev.v)result.push(ins.get(v));return result
  }
  let edges=[];for(let u=0;u<=n;u++)for(let v=1;v<=n;v++)if(u!==v&&Number.isFinite(w[u][v]))edges.push({u,v,w:w[u][v]-(u===0?M:0)});
  let r=mst(Array.from({length:n+1},(_,i)=>i),edges);
  if(limited)return {status:"LIMIT"};if(!r||r.filter(e=>e.u===0).length!==1)return {status:"NO_TREE"};
  let h=Array(n+1).fill(-1);for(let e of r)h[e.v]=e.u;
  ck(P.valid(h,false),"valid");return {status:"CANDIDATE",heads:h,best:P.score(w,h),ops,cycles,authority:"NONE",outside:true}
 }
 function oracle(w){let n=w.length-1,h=Array(n+1).fill(-1),best=-Infinity;function go(i){if(i>n){if(P.valid(h,false))best=Math.max(best,P.score(w,h));return}for(let p=0;p<=n;p++)if(p!==i&&Number.isFinite(w[p][i])){h[i]=p;go(i+1)}}go(1);return best}
 let out={sentences:0,tokens:0,nonPunct:0,projectiveCorrect:0,unrestrictedCorrect:0,projectiveNonPunct:0,unrestrictedNonPunct:0,projectiveRoot:0,unrestrictedRoot:0,negativeNonroot:0,projectiveNeg:0,unrestrictedNeg:0,unrestrictedNonProjective:0,goldNonProjective:0,strictScoreGain:0,equalScore:0,improved:0,worse:0,equal:0,goldScoreStrictlyBelow:0,oracleCases:0,oracleNoTree:0,ops:0,maxOps:0,cycles:0,controls:0};
 for(let block of raw.trimEnd().split(/\n\n+/)){
  let ts=[null,...block.split("\n").filter(l=>!l.startsWith("#")).map(l=>{let c=l.split("\t");return {pos:c[3],head:+c[6],neg:c[5].split("|").includes("Polarity=Neg")}})],gold=ts.map(t=>t?.head??-1),w=P.matrix(ts),p=P.decode(w),r=solve(w);
  ck(p.status==="CANDIDATE"&&r.status==="CANDIDATE"&&r.best>=p.best&&r.best>=P.score(w,gold),"score domain");
  out.sentences++;out.tokens+=ts.length-1;out.ops+=r.ops;out.maxOps=Math.max(out.maxOps,r.ops);out.cycles+=r.cycles;
  out.unrestrictedNonProjective+=+!P.valid(r.heads,true);out.goldNonProjective+=+!P.valid(gold,true);out.strictScoreGain+=+(r.best>p.best);out.equalScore+=+(r.best===p.best);out.goldScoreStrictlyBelow+=+(r.best>P.score(w,gold));
  let x=0,y=0;for(let i=1;i<ts.length;i++){let u=p.heads[i]===gold[i],v=r.heads[i]===gold[i];x+=+u;y+=+v;if(ts[i].pos!=="PUNCT"){out.nonPunct++;out.projectiveNonPunct+=+u;out.unrestrictedNonPunct+=+v}if(!gold[i]){out.projectiveRoot+=+u;out.unrestrictedRoot+=+v}if(ts[i].neg&&gold[i]){out.negativeNonroot++;out.projectiveNeg+=+u;out.unrestrictedNeg+=+v}}
  out.projectiveCorrect+=x;out.unrestrictedCorrect+=y;out.improved+=+(y>x);out.worse+=+(y<x);out.equal+=+(y===x)
 }
 for(let n=1;n<=5;n++)for(let seed=0;seed<60;seed++){
  let w=Array.from({length:n+1},(_,p)=>Array.from({length:n+1},(_,i)=>!i||p===i||(seed%5===0&&((p*13+i*7+seed)%4===0))?-Infinity:((p*37+i*19+seed*23+p*i*11)%17)-8));
  let o=oracle(w),r=solve(w);ck(Number.isFinite(o)?r.status==="CANDIDATE"&&r.best===o:r.status==="NO_TREE","oracle");out.oracleCases++;out.oracleNoTree+=+!Number.isFinite(o)
 }
 for(let f of [()=>out.sentences===500&&out.tokens===12665,()=>out.projectiveCorrect===3254,()=>out.goldNonProjective===5,()=>out.strictScoreGain+out.equalScore===500,()=>out.improved+out.worse+out.equal===500,()=>solve([[-Infinity,1,1],[-Infinity,-Infinity,-Infinity],[-Infinity,-Infinity,-Infinity]]).status==="NO_TREE",()=>solve([[-Infinity,1],[-Infinity,-Infinity]],0).status==="LIMIT",()=>solve([[-Infinity,1],[-Infinity,-Infinity]]).best===1,()=>out.oracleCases===300,()=>out.negativeNonroot===37]){ck(f(),"control "+out.controls);out.controls++}
 return out
}
const {P}=load(a,b,raw);console.log(JSON.stringify(experiment(P,raw),null,2));
```
## 实测
```json
{
  "sentences": 500,
  "tokens": 12665,
  "nonPunct": 10895,
  "projectiveCorrect": 3254,
  "unrestrictedCorrect": 3257,
  "projectiveNonPunct": 2924,
  "unrestrictedNonPunct": 2894,
  "projectiveRoot": 156,
  "unrestrictedRoot": 152,
  "negativeNonroot": 37,
  "projectiveNeg": 22,
  "unrestrictedNeg": 21,
  "unrestrictedNonProjective": 153,
  "goldNonProjective": 5,
  "strictScoreGain": 57,
  "equalScore": 443,
  "improved": 187,
  "worse": 155,
  "equal": 158,
  "goldScoreStrictlyBelow": 500,
  "oracleCases": 300,
  "oracleNoTree": 3,
  "ops": 21993061,
  "maxOps": 913196,
  "cycles": 11781,
  "controls": 10
}
```
下一步：优先诊断可学习评分与多解不确定性；针对#62待独立验收的硬义务、条件、主体和修订链安排独立审查，不将现有开发集用作留出。现有v0.7任务不变。
