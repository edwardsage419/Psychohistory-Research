# 自主认知专项累计第88轮候选：当前节点子集消元与原文历史候选扩展

2026-11-25。RESEARCH_CANDIDATE / EXACT_SUBSET_ELIMINATION_EXECUTED / RAW_PRIOR_ORACLE_CURRENT / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。main cbf740574b8e07734a78d6fb5a8d178005e513ab。核对最近20提交、13开放PR（#61待审）、v3.2首8行及此前全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R87报告前33行。增量：保持R87固定权重及合法域不变，用当前节点子集消元替代枚举历史存在掩码；随后扩大历史原文候选。未重新实现完整语言模型或原生运行时。

## 输入
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
读取两个完整JSON并核对blob。32情节64轮167人工标注，12明确引用，ChatGPT研发辅助原创公开合成开发资料，非真人、独立留出或获授权训练。小图复用R87候选与权重：一元1+码点长度mod3，边1+共享字符二元组数，相邻当前节点同时存在乘2；没有新增拟合。每个当前节点最多一个历史目标。扩展图的历史候选直接从原文所有不含标点/空白、长度1..24码点的跨度生成；当前仍由标注给定。历史候选允许同时存在，不能将其视为真实节点或完整语义。扩展图仅计算无监督全域分区及每当前节点ABSENT/NO_LINK/OUTSIDE三个分子，不计算逐历史节点或全部链接边际，不声称全量推理；不将未标注历史跨度设为负例或正例，标注仅事后几何覆盖。所有输出authority NONE、outside true，模型归一不能当现实概率。

## 数学
设n个历史节点、m个当前节点。固定分配给历史i的当前链接节点子集T，若T为空，其历史存在性求和为1+a_i（已监督存在或额外固定时为a_i）；否则存在性强制1，贡献a_i乘T内各边权积。按历史节点逐个进行不相交子集卷积：D_new[S∪T]+=D_old[S]*w_i[T]，T与S不交，且满足当前链接资格；初始D[空]=1。最后枚举已链接子集S与当前存在集合P⊇S，乘P的一元权重、相邻存在因子及每个P\S的NO_LINK/OUTSIDE允许数；非存在节点必须允许ABSENT。每个完整赋值唯一对应历史目标分组及当前存在集合，因此分配律给出精确分区；重复引用同一历史节点允许。额外固定节点/选择同样通过掩码实现。单次分区主要子集循环O(n 3^m)，构造子集权重O(n m 2^m)，最后组合O(m 3^m)，工作数组O(2^m)（不含输入和大整数）；适合m小n大，m大时仍指数。与R87 O(2^n m(n+3))存在掩码法不同，实际选择须按资源和图结构；两轮计数单位不同，不能直接称为实测加速倍数。全请求所有子查询统一累计计数，超限清除结果，m>12保护，2百万上限为研究者选择；只计子集权重循环、卷积项和最终组合，未计所有循环、BigInt位成本、输入构建、内存或真实设备时间。扩展候选不等于语义覆盖。真实数学执行仍需可信宿主及独立义务检查。

## 验证范围
小图以独立递归完整赋值BigInt参照比较全/相容分区与全部944边际分子，预算恰好及少一计数验证；同一研究者编写，非独立验收。扩展图规模大，不可穷举完整历史掩码；仅以已在小图核对的算法、NO_LINK/OUTSIDE对称性、非负剩余质量及预算边界核验，不声称扩展图有独立完整参照。扩大历史候选不证明语义准确性、排序效果或真实设备可运行。标注目标覆盖为原文字面起止，不评价其他义项。固定语料没有长对话，当前候选仍人工给定；无新外部资料。11项控制。无训练、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。保留R50完整范围及正式验收门。

## 复算代码
按L/S顺序加载固定JSON。
```js
function experiment(docs){
 const ck=(v,m)=>{if(!v)throw Error(m)};
 const grams=q=>new Set([...q].slice(0,-1).map((c,i)=>c+[...q][i+1]));
 const u=q=>BigInt(1+[...q].length%3);
 function graph(a,b,refs){let ag=a.map(grams),bg=b.map(grams);return {n:a.length,m:b.length,a:a.map(u),b:b.map(u),edges:bg.map(v=>ag.map(w=>1n+BigInt([...v].filter(x=>w.has(x)).length))),refs}}
 function raw(t){let a=[...t],q=[];for(let i=0;i<a.length;i++)for(let j=i+1;j<=Math.min(i+24,a.length);j++){if(/[\p{P}\p{Z}\s]/u.test(a[j-1]))break;q.push({i,j,q:a.slice(i,j).join("")})}return q}
 // 0 absent, 1 none, 2 outside, 3+i link to historical i. obs means R87's
 // oracle supervision: all prior/current nodes present and marked reference fixed.
 function allowed(g,j,c,obs,extra){
  return (!obs||c!==0&&(g.refs[j]<0||c===3+g.refs[j]))&&(!extra||extra.kind!=="choice"||extra.i!==j||extra.c===c)
 }
 function subset(g,obs,extra,budget){
  if(g.m>12)throw Error("LIMIT");const size=2**g.m,all=size-1,tick=()=>{if(budget.used>=budget.cap)throw Error("LIMIT");budget.used++};
  let dp=Array(size).fill(0n);dp[0]=1n;
  for(let i=0;i<g.n;i++){
   let w=Array(size).fill(0n);w[0]=obs||extra?.kind==="prior"&&extra.i===i?g.a[i]:1n+g.a[i];
   let mask=0;for(let j=0;j<g.m;j++)if(allowed(g,j,3+i,obs,extra))mask|=1<<j;
   for(let s=mask;s;s=(s-1)&mask){
    tick();let z=g.a[i];for(let j=0;j<g.m;j++)if(s&(1<<j))z*=g.edges[j][i];w[s]=z;
   }
   let next=Array(size).fill(0n);
   for(let s=0;s<size;s++)if(dp[s]){
    let rem=mask&~s;for(let t=rem;;t=(t-1)&rem){tick();next[s|t]+=dp[s]*w[t];if(t===0)break}
   }dp=next;
  }
  let z=0n;
  // s linked current positions, p present positions. Nonlinked present states
  // have separate NO_LINK/OUTSIDE multiplicity; absence has multiplicity one.
  for(let s=0;s<size;s++)if(dp[s])for(let p=0;p<size;p++)if((p&s)===s){
   tick();let w=dp[s];
   for(let j=0;j<g.m;j++){
    let bit=1<<j;if(p&bit){
     w*=g.b[j];if(j&&(p&(bit>>1)))w*=2n;
     if(!(s&bit))w*=BigInt(+allowed(g,j,1,obs,extra)+ +allowed(g,j,2,obs,extra))
    }else if(!allowed(g,j,0,obs,extra)){w=0n;break}
   }z+=w;
  }return z;
 }
 function oracle(g,obs){
  let z=0n,prior=Array(g.n).fill(0n),choices=Array.from({length:g.m},()=>Array(g.n+3).fill(0n)),a=[],b=[],worlds=0;
  function cur(j,w){if(j===g.m){z+=w;worlds++;a.forEach((v,i)=>{if(v)prior[i]+=w});b.forEach((v,i)=>choices[i][v]+=w);return}
   for(let c=0;c<g.n+3;c++){if(c>=3&&!a[c-3]||obs&&(c===0||g.refs[j]>=0&&c!==3+g.refs[j]))continue;
    let v=c===0?1n:g.b[j]*(c>=3?g.edges[j][c-3]:1n);if(j&&b[j-1]&&c)v*=2n;b.push(c);cur(j+1,w*v);b.pop()}
  }
  function hist(i,w){if(i===g.n){cur(0,w);return}for(let v=obs?1:0;v<=1;v++){a.push(v);hist(i+1,w*(v?g.a[i]:1n));a.pop()}}
  hist(0,1n);return {z,prior,choices,worlds};
 }
 function run(g,cap,expanded=false){
  let budget={used:0,cap};
  try{let results=[];for(let obs of expanded?[false]:[false,true]){
    let z=subset(g,obs,null,budget);
    let prior=expanded?[]:g.a.map((_,i)=>subset(g,obs,{kind:"prior",i},budget));
    let choices=g.b.map((_,i)=>Array.from({length:expanded?3:g.n+3},(_,c)=>subset(g,obs,{kind:"choice",i,c},budget)));
    results.push({z,prior,choices});
   }return {status:"EXACT_FINITE",outside:true,authority:"NONE",used:budget.used,results};
  }catch(e){if(e.message!=="LIMIT")throw e;return {status:"LIMIT",outside:true,authority:"NONE",used:budget.used,results:null}}
 }
 let out={episodes:0,partitions:0,marginals:0,oracleWorlds:0,smallBudgetChecks:0,maxSmallOps:0,rawEpisodes:0,rawPriorCandidates:0,maxRawPrior:0,maxCurrent:0,rawPriorMarked:0,rawPriorCovered:0,rawReferenceTargets:0,rawReferenceCovered:0,rawPartitions:0,rawMarginals:0,rawLimits:0,maxRawOps:0,rawBoundaryChecks:0,rawOver20:0,rawMaxZBits:0,controls:0,records:[]};
 for(let d=0;d<docs.length;d++)for(let ep of docs[d].cases){
  let [ta,tb]=ep.turns,aa=d===0?ta.claims:ta.proposal.claims,bb=d===0?tb.claims:tb.proposal.claims,quote=c=>d===0?c.span:c.quote;
  let a=aa.map(quote),b=bb.map(quote),refs=bb.map(c=>{let s=d===0?c.supersedes:c.ref;if(typeof s!=="string")return -1;let i=d===0?aa.findIndex(x=>x.field===s.split(":").at(-1)):Number(s.split(".").at(-1))-1;ck(i>=0&&i<a.length,"ref");return i});
  let g=graph(a,b,refs),v=run(g,2000000);ck(v.status==="EXACT_FINITE","small");out.episodes++;out.maxSmallOps=Math.max(out.maxSmallOps,v.used);
  for(let k=0;k<2;k++){let x=v.results[k],y=oracle(g,!!k);ck(x.z===y.z,"z");out.partitions++;out.oracleWorlds+=y.worlds;
   x.prior.forEach((q,i)=>{ck(q===y.prior[i],"prior");out.marginals++});x.choices.forEach((row,j)=>row.forEach((q,c)=>{ck(q===y.choices[j][c],"choice");out.marginals++}));
  }
  ck(run(g,v.used-1).status==="LIMIT"&&run(g,v.used).status==="EXACT_FINITE","boundary");out.smallBudgetChecks+=2;
  let spans=raw(ta.text),idx=a.map(q=>{let at=ta.text.indexOf(q);ck(at>=0&&at===ta.text.lastIndexOf(q),"anchor");let i=[...ta.text.slice(0,at)].length,j=i+[...q].length;return spans.findIndex(s=>s.i===i&&s.j===j)});
  out.rawEpisodes++;out.rawPriorCandidates+=spans.length;out.maxRawPrior=Math.max(out.maxRawPrior,spans.length);out.maxCurrent=Math.max(out.maxCurrent,b.length);out.rawPriorMarked+=a.length;out.rawPriorCovered+=idx.filter(i=>i>=0).length;
  for(let x of refs)if(x>=0){out.rawReferenceTargets++;out.rawReferenceCovered+=+(idx[x]>=0)}
  out.rawOver20+=+(spans.length>20);
  let rg=graph(spans.map(s=>s.q),b,[]),rv=run(rg,2000000,true);out.maxRawOps=Math.max(out.maxRawOps,rv.used);
  if(rv.status==="LIMIT"){ck(rv.results===null,"no partial");out.rawLimits++}
  else{let x=rv.results[0];out.rawPartitions++;out.rawMaxZBits=Math.max(out.rawMaxZBits,x.z.toString(2).length);
   // Separate identity: sum exact absent/none/outside plus all-linked aggregate,
   // obtained by restricting a current node to link choices only via a graph projection:
   // here check NO_LINK and OUTSIDE symmetry and finite positive residual.
   for(let row of x.choices){ck(row[0]>0n&&row[1]===row[2]&&row[1]>0n&&row.reduce((a,b)=>a+b,0n)<=x.z,"expanded invariant");out.rawMarginals+=3}
   let limited=run(rg,rv.used-1,true);ck(limited.status==="LIMIT"&&limited.results===null,"raw boundary");out.rawBoundaryChecks++;
  }
  out.records.push({id:ep.id,prior:g.n,current:g.m,smallOps:v.used,fullZ:String(v.results[0].z),observedZ:String(v.results[1].z),rawPrior:spans.length,rawOps:rv.used,rawStatus:rv.status});
 }
 for(let t of [()=>out.episodes===32,()=>out.partitions===64,()=>out.marginals===944,()=>out.oracleWorlds===8840,()=>out.smallBudgetChecks===64,()=>out.rawPriorMarked===110,()=>out.rawReferenceTargets===12,()=>out.rawPartitions+out.rawLimits===32,()=>out.rawBoundaryChecks===out.rawPartitions,()=>out.rawPriorCovered<=out.rawPriorMarked,()=>run(graph(["甲"],["乙"],[-1]),0).status==="LIMIT"]){ck(t(),"control");out.controls++}
 return out;
}
```

## 实测
```json
{
  "episodes": 32,
  "partitions": 64,
  "marginals": 944,
  "oracleWorlds": 8840,
  "smallBudgetChecks": 64,
  "maxSmallOps": 3172,
  "rawEpisodes": 32,
  "rawPriorCandidates": 5463,
  "maxRawPrior": 366,
  "maxCurrent": 3,
  "rawPriorMarked": 110,
  "rawPriorCovered": 108,
  "rawReferenceTargets": 12,
  "rawReferenceCovered": 12,
  "rawPartitions": 32,
  "rawMarginals": 171,
  "rawLimits": 0,
  "maxRawOps": 31649,
  "rawBoundaryChecks": 32,
  "rawOver20": 32,
  "rawMaxZBits": 588,
  "controls": 11,
  "records": [
    {
      "id": "L01",
      "prior": 4,
      "current": 1,
      "smallOps": 300,
      "fullZ": "1424",
      "observedZ": "324",
      "rawPrior": 133,
      "rawOps": 939,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "L02",
      "prior": 4,
      "current": 2,
      "smallOps": 1304,
      "fullZ": "16160",
      "observedZ": "5184",
      "rawPrior": 137,
      "rawOps": 4966,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "L03",
      "prior": 4,
      "current": 1,
      "smallOps": 252,
      "fullZ": "1134",
      "observedZ": "48",
      "rawPrior": 128,
      "rawOps": 904,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "L04",
      "prior": 4,
      "current": 2,
      "smallOps": 1304,
      "fullZ": "3344",
      "observedZ": "576",
      "rawPrior": 156,
      "rawOps": 5650,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "L05",
      "prior": 3,
      "current": 2,
      "smallOps": 856,
      "fullZ": "13184",
      "observedZ": "6480",
      "rawPrior": 152,
      "rawOps": 5506,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "L06",
      "prior": 3,
      "current": 2,
      "smallOps": 856,
      "fullZ": "3804",
      "observedZ": "1080",
      "rawPrior": 178,
      "rawOps": 6442,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "L07",
      "prior": 3,
      "current": 2,
      "smallOps": 856,
      "fullZ": "5966",
      "observedZ": "2160",
      "rawPrior": 366,
      "rawOps": 13210,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "L08",
      "prior": 3,
      "current": 2,
      "smallOps": 749,
      "fullZ": "5102",
      "observedZ": "360",
      "rawPrior": 152,
      "rawOps": 5506,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "L09",
      "prior": 2,
      "current": 3,
      "smallOps": 1854,
      "fullZ": "10679",
      "observedZ": "6144",
      "rawPrior": 139,
      "rawOps": 19863,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "L10",
      "prior": 4,
      "current": 1,
      "smallOps": 300,
      "fullZ": "684",
      "observedZ": "108",
      "rawPrior": 187,
      "rawOps": 1317,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "L11",
      "prior": 4,
      "current": 2,
      "smallOps": 1304,
      "fullZ": "56061",
      "observedZ": "19008",
      "rawPrior": 185,
      "rawOps": 6694,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "L12",
      "prior": 4,
      "current": 2,
      "smallOps": 1304,
      "fullZ": "3480",
      "observedZ": "672",
      "rawPrior": 127,
      "rawOps": 4606,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "L13",
      "prior": 4,
      "current": 2,
      "smallOps": 1304,
      "fullZ": "8736",
      "observedZ": "1728",
      "rawPrior": 156,
      "rawOps": 5650,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "L14",
      "prior": 3,
      "current": 2,
      "smallOps": 856,
      "fullZ": "2704",
      "observedZ": "900",
      "rawPrior": 184,
      "rawOps": 6658,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "L15",
      "prior": 4,
      "current": 2,
      "smallOps": 1142,
      "fullZ": "2432",
      "observedZ": "72",
      "rawPrior": 137,
      "rawOps": 4966,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "L16",
      "prior": 4,
      "current": 2,
      "smallOps": 1304,
      "fullZ": "8406",
      "observedZ": "2016",
      "rawPrior": 248,
      "rawOps": 8962,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "L17",
      "prior": 3,
      "current": 3,
      "smallOps": 3172,
      "fullZ": "23770",
      "observedZ": "10800",
      "rawPrior": 222,
      "rawOps": 31649,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "L18",
      "prior": 2,
      "current": 3,
      "smallOps": 1854,
      "fullZ": "19501",
      "observedZ": "12000",
      "rawPrior": 85,
      "rawOps": 12195,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "S01",
      "prior": 4,
      "current": 2,
      "smallOps": 1122,
      "fullZ": "99280",
      "observedZ": "19440",
      "rawPrior": 205,
      "rawOps": 7414,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "S02",
      "prior": 3,
      "current": 1,
      "smallOps": 163,
      "fullZ": "576",
      "observedZ": "108",
      "rawPrior": 226,
      "rawOps": 1590,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "S03",
      "prior": 3,
      "current": 1,
      "smallOps": 163,
      "fullZ": "168",
      "observedZ": "18",
      "rawPrior": 108,
      "rawOps": 764,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "S04",
      "prior": 4,
      "current": 1,
      "smallOps": 240,
      "fullZ": "912",
      "observedZ": "48",
      "rawPrior": 177,
      "rawOps": 1247,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "S05",
      "prior": 3,
      "current": 1,
      "smallOps": 196,
      "fullZ": "378",
      "observedZ": "144",
      "rawPrior": 210,
      "rawOps": 1478,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "S06",
      "prior": 2,
      "current": 2,
      "smallOps": 500,
      "fullZ": "170",
      "observedZ": "64",
      "rawPrior": 133,
      "rawOps": 4822,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "S07",
      "prior": 3,
      "current": 2,
      "smallOps": 856,
      "fullZ": "12132",
      "observedZ": "5400",
      "rawPrior": 208,
      "rawOps": 7522,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "S08",
      "prior": 3,
      "current": 1,
      "smallOps": 168,
      "fullZ": "351",
      "observedZ": "64",
      "rawPrior": 138,
      "rawOps": 974,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "S09",
      "prior": 4,
      "current": 1,
      "smallOps": 300,
      "fullZ": "1377",
      "observedZ": "352",
      "rawPrior": 188,
      "rawOps": 1324,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "S10",
      "prior": 4,
      "current": 2,
      "smallOps": 1122,
      "fullZ": "35280",
      "observedZ": "1512",
      "rawPrior": 180,
      "rawOps": 6514,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "S11",
      "prior": 3,
      "current": 2,
      "smallOps": 766,
      "fullZ": "778",
      "observedZ": "112",
      "rawPrior": 74,
      "rawOps": 2698,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "S12",
      "prior": 5,
      "current": 2,
      "smallOps": 1569,
      "fullZ": "161728",
      "observedZ": "6048",
      "rawPrior": 136,
      "rawOps": 4930,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "S13",
      "prior": 3,
      "current": 2,
      "smallOps": 726,
      "fullZ": "13527",
      "observedZ": "2160",
      "rawPrior": 175,
      "rawOps": 6334,
      "rawStatus": "EXACT_FINITE"
    },
    {
      "id": "S14",
      "prior": 4,
      "current": 1,
      "smallOps": 300,
      "fullZ": "540",
      "observedZ": "96",
      "rawPrior": 233,
      "rawOps": 1639,
      "rawStatus": "EXACT_FINITE"
    }
  ]
}
```

## 后续
需解决当前原文候选数量过大、真实语义覆盖与开放域未知；可研究精确分解/经证明的区间及结构化候选预算，避免以截断后的确定结果取代原义务。当前仍未实现完整白话理解或真实数学引擎联动。数据、独立验收、产品轨责任不变。
