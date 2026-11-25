# 自主认知专项累计第89轮候选：双侧原文候选联合分区的有证上下界与独立结构精确分解

2026-11-25。RESEARCH_CANDIDATE / CERTIFIED_FINITE_PARTITION_BOUNDS_EXECUTED / RAW_BOTH_SIDES / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。main 52c51f2e1583437d9cf1ecb886ef689546028cab。核对近20提交、13开放PR（#61待审）、v3.2首8行及历史全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R88首24行。增量：R88仅扩大历史侧且当前数少；本轮双侧全部有限原文跨度，保持R87/88无监督全域的正权重，不按词面删边。发现密图不满足独立结构，转为严格区间；不是实际语言理解或模型训练。数学为有限独立变量单调关联及求和，不主张原创定理。

## 固定输入
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
实际读取完整JSON并核对blob。32情节64轮167标注，ChatGPT研发辅助原创公开合成开发材料，非真人、独立留出或获授权训练。两侧按R88枚举不含标点/空白的1..24码点跨度，保留起止；标注仅小图参照及事后覆盖，不用于扩展图筛选。沿用一元1+长度mod3，边1+共享字符二元组，相邻当前同时存在乘2。正权重密边不是合格语义关系；重叠跨度均可共存是原有限模型假设。每节点最多一个引用目标，NONE与OUTSIDE均有单位边权，仍为候选占位，不能当真实域外概率。只验证无监督全域分区，不计算真实语义边际、学习目标或数学决策。不同于R88的小图全/相容边际，本轮只比较全分区。

## 数学
历史存在性独立，未归一总质量A=∏(1+a_i)，归一后独立Bernoulli X_i，P(X_i=1)=a_i/(1+a_i)。给定X，当前存在集合P贡献相邻软因子及∏_{j∈P} b_j L_j(X)，L_j=2+Σ_i e_ji X_i；二状态链递推精确求和。Z=A E[chain(L)]。选定k历史变量条件化，对未固定独立变量，所有L_j为非负坐标单调函数；独立变量的单调关联可由逐坐标条件化归纳（单Bernoulli协方差=p(1-p)差值乘积非负；全协方差公式），非负单调函数的积仍单调，所以E∏L_j≥∏E L_j；若各L依赖不相交的剩余变量则相等。上界以未固定变量全部存在替代，因单调逐项成立。链系数均非负，分别代入期望与最大值得条件下界及上界，再按条件质量求和。进一步固定一变量，条件下界的产品期望不减（同一Bernoulli关联），上界不增；固定全部历史节点时精确。稀疏资格边只在独立构造的512图中使用0；扩展图不擅自删边。D=12为本夹具1/2/3一元权重概率共同分母；链每阶段乘D，最终分区界为BigInt分子除D^m。精确性和包含核验用整数；展示log10(上/下)仅前15十进制位近似，表示区间宽度，不是概率或误差保证。k=0、3用于扩展（历史不足则全固定）；按边权总和固定顺序，无训练。k全枚举只在小图。时间主要O(nm+2^k m(k+1))（另有历史排序和BigInt成本），预算计部分边扫描、条件、条件求和及链阶段，不计所有运算、构图、内存或设备时间；2百万及k≤8由研究者选定。超限整体LIMIT，无区间输出；有界不等于精确，所有输出outside=true、authority=NONE。

## 验证
3历史×3当前，全部512二值资格边图，固定非零权重；每图k=0..3，与完整历史掩码精确链参照比较；同研究者定义，非独立验收。32仓库oracle小图同样逐k检查，完全条件化及预算少一核验。双侧原文图无法完整穷举，仅依据上述证明、有限小图复算、区间嵌套及预算边界，不宣称大型独立真值。宽区间若不能用于下游阈值判定，必须保留UNKNOWN；本轮不实现阈值判定或推断实际意图。没有新增外部资料、真实设备、用户效果、训练、Codex、CI、生产修改、PR合并、部署、费用、冻结协议变更。13项专项控制。R50完整版本范围及正式验收门保留。

## 可复算代码
按L/S顺序载入固定JSON。
```js
function experiment(docs){
 const ck=(b,m)=>{if(!b)throw Error(m)};
 const grams=q=>new Set([...q].slice(0,-1).map((c,i)=>c+[...q][i+1])),u=q=>BigInt(1+[...q].length%3);
 function graph(a,b){let ag=a.map(grams),bg=b.map(grams);return {a:a.map(u),b:b.map(u),e:bg.map(v=>ag.map(w=>1n+BigInt([...v].filter(x=>w.has(x)).length)))}}
 function raw(t){let a=[...t],q=[];for(let i=0;i<a.length;i++)for(let j=i+1;j<=Math.min(i+24,a.length);j++){if(/[\p{P}\p{Z}\s]/u.test(a[j-1]))break;q.push({i,j,q:a.slice(i,j).join("")})}return q}
 // Each current position is absent or present with NONE, OUTSIDE, or one present prior.
 // D=12 is a common denominator for historical presence probabilities a/(1+a), a=1,2,3.
 const D=12n;
 function chain(b,L,scale){let x=1n,y=0n;for(let j=0;j<b.length;j++){let z=(x+y)*scale,v=(x+2n*y)*b[j]*L[j];x=z;y=v}return x+y}
 function exact(g){let n=g.a.length,m=g.b.length,z=0n;ck(n<=10,"oracle size");
  for(let mask=0;mask<2**n;mask++){let w=1n;for(let i=0;i<n;i++)if(mask&(1<<i))w*=g.a[i];
   let L=g.e.map(row=>row.reduce((s,e,i)=>s+((mask&(1<<i))?e:0n),2n));z+=w*chain(g.b,L,1n)
  }return z}
 function bounds(g,k,cap=2000000){
  let n=g.a.length,m=g.b.length,budget=0,lo=0n,hi=0n;
  const tick=()=>{if(budget>=cap)throw Error("LIMIT");budget++};
  try{
   ck(g.a.every(a=>[1n,2n,3n].includes(a)),"denominator");
   if(k>n||k>8)throw Error("LIMIT");
   let impact=Array(n).fill(0n);for(let row of g.e)for(let i=0;i<n;i++){tick();impact[i]+=row[i]}
   let selected=Array.from({length:n},(_,i)=>i).sort((a,b)=>impact[a]===impact[b]?a-b:impact[a]>impact[b]?-1:1).slice(0,k),set=new Set(selected);
   let free=g.a.reduce((w,a,i)=>set.has(i)?w:w*(1n+a),1n);
   let base=g.e.map(row=>{let l=2n*D,h=2n*D;for(let i=0;i<n;i++)if(!set.has(i)){tick();l+=row[i]*g.a[i]*(D/(1n+g.a[i]));h+=row[i]*D}return [l,h]});
   // If a remaining prior affects at most one current factor, all these factors
   // depend on disjoint independent variables, so product-of-means is exact.
   let disjoint=true;for(let i=0;i<n;i++)if(!set.has(i)){let c=0;for(let j=0;j<m;j++){tick();if(g.e[j][i]>0n)c++}if(c>1)disjoint=false}
   for(let mask=0;mask<2**k;mask++){
    tick();let w=free;for(let t=0;t<k;t++)if(mask&(1<<t))w*=g.a[selected[t]];
    let L=[],U=[];for(let j=0;j<m;j++){let s=0n;for(let t=0;t<k;t++){tick();if(mask&(1<<t))s+=D*g.e[j][selected[t]]}L.push(base[j][0]+s);U.push(base[j][1]+s)}
    // Count each chain stage as one work unit (not individual BigInt arithmetic).
    for(let j=0;j<m;j++)tick();let low=chain(g.b,L,D);lo+=w*low;
    if(disjoint)hi+=w*low;else{for(let j=0;j<m;j++)tick();hi+=w*chain(g.b,U,D)}
   }
   let den=D**BigInt(m);ck(lo<=hi&&lo>0n,"bounds");
   return {status:lo===hi?"EXACT_FINITE":"BOUNDED_FINITE",lo,hi,den,used:budget,authority:"NONE",outside:true,disjoint};
  }catch(e){if(e.message!=="LIMIT")throw e;return {status:"LIMIT",used:budget,authority:"NONE",outside:true}}
 }
 // log10 of positive BigInt using leading 15 decimal digits; display proxy only.
 function log10(x){let s=String(x),l=Math.min(15,s.length);return Math.log10(Number(s.slice(0,l)))+s.length-l}
 const width=x=>log10(x.hi)-log10(x.lo);
 let out={smallEpisodes:0,smallChecks:0,smallExactAtFull:0,smallNestingChecks:0,smallBudgetChecks:0,syntheticGraphs:0,syntheticChecks:0,syntheticExactAtZero:0,syntheticDisjoint:0,syntheticNestingChecks:0,rawEpisodes:0,rawPrior:0,rawCurrent:0,rawPairs:0,maxPrior:0,maxCurrent:0,maxPairs:0,rawPriorCovered:0,rawCurrentCovered:0,rawPriorMarked:0,rawCurrentMarked:0,rawComplete:0,rawLimit:0,rawNestingChecks:0,rawBudgetChecks:0,rawExact:0,maxUsed:0,rawWidth0:[],rawWidth3:[],controls:0,records:[]};
 function verify(g,kind){let z=exact(g),last=null;for(let k=0;k<=g.a.length;k++){let x=bounds(g,k);ck(x.status!=="LIMIT"&&x.lo<=z*x.den&&z*x.den<=x.hi,"containment");out[kind+"Checks"]++;
   if(last){ck(x.lo>=last.lo&&x.hi<=last.hi,"nested");out[kind+"NestingChecks"]++}last=x;
   if(kind==="synthetic"&&k===0){out.syntheticExactAtZero+=+(x.status==="EXACT_FINITE");out.syntheticDisjoint+=+x.disjoint}
   if(k===g.a.length){ck(x.lo===z*x.den&&x.hi===x.lo,"exact after conditioning");if(kind==="small"){out.smallExactAtFull++;let q=bounds(g,k,x.used-1);ck(q.status==="LIMIT"&&!Object.hasOwn(q,"lo"),"budget");out.smallBudgetChecks++}}
 }}
 // All 512 eligibility graphs with three historical and three current nodes, fixed weights.
 for(let mask=0;mask<512;mask++){let g={a:[1n,2n,3n],b:[2n,1n,3n],e:Array.from({length:3},(_,j)=>Array.from({length:3},(_,i)=>mask&(1<<(3*j+i))?BigInt(1+(i+j)%3):0n))};verify(g,"synthetic");out.syntheticGraphs++}
 for(let d=0;d<docs.length;d++)for(let ep of docs[d].cases){
  let [ta,tb]=ep.turns,aa=d===0?ta.claims:ta.proposal.claims,bb=d===0?tb.claims:tb.proposal.claims,quote=c=>d===0?c.span:c.quote;
  let a=aa.map(quote),b=bb.map(quote);verify(graph(a,b),"small");out.smallEpisodes++;
  let A=raw(ta.text),B=raw(tb.text);
  function covered(t,spans,qs){return qs.filter(q=>{let at=t.indexOf(q);ck(at>=0&&at===t.lastIndexOf(q),"anchor");let i=[...t.slice(0,at)].length,j=i+[...q].length;return spans.some(s=>s.i===i&&s.j===j)}).length}
  out.rawPriorMarked+=a.length;out.rawCurrentMarked+=b.length;out.rawPriorCovered+=covered(ta.text,A,a);out.rawCurrentCovered+=covered(tb.text,B,b);
  let g=graph(A.map(s=>s.q),B.map(s=>s.q)),n=A.length,m=B.length;out.rawEpisodes++;out.rawPrior+=n;out.rawCurrent+=m;out.rawPairs+=n*m;out.maxPrior=Math.max(out.maxPrior,n);out.maxCurrent=Math.max(out.maxCurrent,m);out.maxPairs=Math.max(out.maxPairs,n*m);
  let x=bounds(g,0),y=bounds(g,Math.min(3,n));out.maxUsed=Math.max(out.maxUsed,x.used,y.used);
  if(x.status==="LIMIT"||y.status==="LIMIT"){out.rawLimit++;continue}
  ck(y.lo>=x.lo&&y.hi<=x.hi,"raw nested");out.rawNestingChecks++;out.rawComplete++;out.rawExact+=+(y.status==="EXACT_FINITE");
  let lim=bounds(g,Math.min(3,n),y.used-1);ck(lim.status==="LIMIT"&&!Object.hasOwn(lim,"hi"),"raw limit");out.rawBudgetChecks++;
  let w0=width(x),w3=width(y);out.rawWidth0.push(w0);out.rawWidth3.push(w3);
  out.records.push({id:ep.id,n,m,pairs:n*m,work0:x.used,work3:y.used,log10Ratio0:w0,log10Ratio3:w3,status:y.status});
 }
 function summary(a){let b=[...a].sort((x,y)=>x-y);return {min:b[0],median:(b[Math.floor((b.length-1)/2)]+b[Math.floor(b.length/2)])/2,max:b.at(-1)}}
 out.width0=summary(out.rawWidth0);out.width3=summary(out.rawWidth3);out.rawImproved=out.records.filter(r=>r.log10Ratio3<r.log10Ratio0-1e-10).length;delete out.rawWidth0;delete out.rawWidth3;
 for(let t of [()=>out.syntheticGraphs===512,()=>out.syntheticChecks===2048,()=>out.syntheticDisjoint===64,()=>out.syntheticExactAtZero===64,()=>out.smallEpisodes===32,()=>out.smallExactAtFull===32,()=>out.rawEpisodes===32,()=>out.rawPrior===5463,()=>out.rawPrior+out.rawCurrent===8537,()=>out.rawPriorCovered+out.rawCurrentCovered===165,()=>out.rawComplete+out.rawLimit===32,()=>out.rawBudgetChecks===out.rawComplete,()=>bounds({a:[1n],b:[1n],e:[[1n]]},0,0).status==="LIMIT"]){ck(t(),"control");out.controls++}
 return out;
}
```

## 实测
```json
{
  "smallEpisodes": 32,
  "smallChecks": 142,
  "smallExactAtFull": 32,
  "smallNestingChecks": 110,
  "smallBudgetChecks": 32,
  "syntheticGraphs": 512,
  "syntheticChecks": 2048,
  "syntheticExactAtZero": 64,
  "syntheticDisjoint": 64,
  "syntheticNestingChecks": 1536,
  "rawEpisodes": 32,
  "rawPrior": 5463,
  "rawCurrent": 3074,
  "rawPairs": 544737,
  "maxPrior": 366,
  "maxCurrent": 196,
  "maxPairs": 71736,
  "rawPriorCovered": 108,
  "rawCurrentCovered": 57,
  "rawPriorMarked": 110,
  "rawCurrentMarked": 57,
  "rawComplete": 32,
  "rawLimit": 0,
  "rawNestingChecks": 32,
  "rawBudgetChecks": 32,
  "rawExact": 0,
  "maxUsed": 221880,
  "controls": 13,
  "records": [
    {
      "id": "L01",
      "n": 133,
      "m": 55,
      "pairs": 7315,
      "work0": 22056,
      "work3": 23823,
      "log10Ratio0": 10.038109224134246,
      "log10Ratio3": 9.750655570482479,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "L02",
      "n": 137,
      "m": 110,
      "pairs": 15070,
      "work0": 45431,
      "work3": 48958,
      "log10Ratio0": 20.079423701613052,
      "log10Ratio3": 19.61053963259309,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "L03",
      "n": 128,
      "m": 91,
      "pairs": 11648,
      "work0": 35127,
      "work3": 38046,
      "log10Ratio0": 16.483183940666265,
      "log10Ratio3": 15.935372496832713,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "L04",
      "n": 156,
      "m": 90,
      "pairs": 14040,
      "work0": 42301,
      "work3": 45188,
      "log10Ratio0": 16.515316036480044,
      "log10Ratio3": 16.19353132772528,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "L05",
      "n": 152,
      "m": 157,
      "pairs": 23864,
      "work0": 71907,
      "work3": 76938,
      "log10Ratio0": 28.617828666646687,
      "log10Ratio3": 27.860411951503465,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "L06",
      "n": 178,
      "m": 70,
      "pairs": 12460,
      "work0": 37521,
      "work3": 39768,
      "log10Ratio0": 12.934756629983042,
      "log10Ratio3": 12.706778996774233,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "L07",
      "n": 366,
      "m": 196,
      "pairs": 71736,
      "work0": 215601,
      "work3": 221880,
      "log10Ratio0": 37.00434574205451,
      "log10Ratio3": 36.650710090260304,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "L08",
      "n": 152,
      "m": 133,
      "pairs": 20216,
      "work0": 60915,
      "work3": 65178,
      "log10Ratio0": 24.441542838038004,
      "log10Ratio3": 23.726230891533874,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "L09",
      "n": 139,
      "m": 133,
      "pairs": 18487,
      "work0": 55728,
      "work3": 59991,
      "log10Ratio0": 24.421507833789292,
      "log10Ratio3": 23.84557840787636,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "L10",
      "n": 187,
      "m": 39,
      "pairs": 7293,
      "work0": 21958,
      "work3": 23213,
      "log10Ratio0": 7.200038896491975,
      "log10Ratio3": 7.095161584126629,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "L11",
      "n": 185,
      "m": 65,
      "pairs": 12025,
      "work0": 36206,
      "work3": 38293,
      "log10Ratio0": 12.01189453905016,
      "log10Ratio3": 11.652779621424656,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "L12",
      "n": 127,
      "m": 67,
      "pairs": 8509,
      "work0": 25662,
      "work3": 27813,
      "log10Ratio0": 12.181431636314642,
      "log10Ratio3": 11.861379298673114,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "L13",
      "n": 156,
      "m": 120,
      "pairs": 18720,
      "work0": 56401,
      "work3": 60248,
      "log10Ratio0": 22.06227849167942,
      "log10Ratio3": 21.61407026394727,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "L14",
      "n": 184,
      "m": 57,
      "pairs": 10488,
      "work0": 31579,
      "work3": 33410,
      "log10Ratio0": 10.514102815522335,
      "log10Ratio3": 10.353131820370095,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "L15",
      "n": 137,
      "m": 99,
      "pairs": 13563,
      "work0": 40888,
      "work3": 44063,
      "log10Ratio0": 17.999379789008515,
      "log10Ratio3": 17.534953120172304,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "L16",
      "n": 248,
      "m": 65,
      "pairs": 16120,
      "work0": 48491,
      "work3": 50578,
      "log10Ratio0": 12.119338337475256,
      "log10Ratio3": 11.950275484368206,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "L17",
      "n": 222,
      "m": 127,
      "pairs": 28194,
      "work0": 84837,
      "work3": 88908,
      "log10Ratio0": 23.63090659321483,
      "log10Ratio3": 23.287296732134223,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "L18",
      "n": 85,
      "m": 79,
      "pairs": 6715,
      "work0": 20304,
      "work3": 22839,
      "log10Ratio0": 14.202805842824546,
      "log10Ratio3": 13.522664969455093,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "S01",
      "n": 205,
      "m": 83,
      "pairs": 17015,
      "work0": 51212,
      "work3": 53875,
      "log10Ratio0": 15.403580766792004,
      "log10Ratio3": 15.033989907193188,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "S02",
      "n": 226,
      "m": 76,
      "pairs": 17176,
      "work0": 51681,
      "work3": 54120,
      "log10Ratio0": 14.295689566532928,
      "log10Ratio3": 14.091685590806378,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "S03",
      "n": 108,
      "m": 64,
      "pairs": 6912,
      "work0": 20865,
      "work3": 22920,
      "log10Ratio0": 11.604508539493736,
      "log10Ratio3": 11.119432072408358,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "S04",
      "n": 177,
      "m": 91,
      "pairs": 16107,
      "work0": 48504,
      "work3": 51423,
      "log10Ratio0": 16.830457784814087,
      "log10Ratio3": 16.524169235131126,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "S05",
      "n": 210,
      "m": 91,
      "pairs": 19110,
      "work0": 57513,
      "work3": 60432,
      "log10Ratio0": 16.96162302975341,
      "log10Ratio3": 16.634910011720592,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "S06",
      "n": 133,
      "m": 66,
      "pairs": 8778,
      "work0": 26467,
      "work3": 28586,
      "log10Ratio0": 12.039556444828747,
      "log10Ratio3": 11.736865748220566,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "S07",
      "n": 208,
      "m": 102,
      "pairs": 21216,
      "work0": 63853,
      "work3": 67124,
      "log10Ratio0": 19.09319522787564,
      "log10Ratio3": 18.823383305628965,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "S08",
      "n": 138,
      "m": 49,
      "pairs": 6762,
      "work0": 20385,
      "work3": 21960,
      "log10Ratio0": 9.037081035986944,
      "log10Ratio3": 8.73196224844736,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "S09",
      "n": 188,
      "m": 83,
      "pairs": 15604,
      "work0": 46979,
      "work3": 49642,
      "log10Ratio0": 15.46467299469208,
      "log10Ratio3": 15.177873203406818,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "S10",
      "n": 180,
      "m": 141,
      "pairs": 25380,
      "work0": 76423,
      "work3": 80942,
      "log10Ratio0": 26.07688470653102,
      "log10Ratio3": 25.571547434877857,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "S11",
      "n": 74,
      "m": 133,
      "pairs": 9842,
      "work0": 29793,
      "work3": 34056,
      "log10Ratio0": 23.972190608692756,
      "log10Ratio3": 22.42810378172436,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "S12",
      "n": 136,
      "m": 64,
      "pairs": 8704,
      "work0": 26241,
      "work3": 28296,
      "log10Ratio0": 11.736819959970319,
      "log10Ratio3": 11.482063198027504,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "S13",
      "n": 175,
      "m": 157,
      "pairs": 27475,
      "work0": 82740,
      "work3": 87771,
      "log10Ratio0": 29.34571776256962,
      "log10Ratio3": 28.751129663977167,
      "status": "BOUNDED_FINITE"
    },
    {
      "id": "S14",
      "n": 233,
      "m": 121,
      "pairs": 28193,
      "work0": 84822,
      "work3": 88701,
      "log10Ratio0": 22.677042899344883,
      "log10Ratio3": 22.38861435346189,
      "status": "BOUNDED_FINITE"
    }
  ],
  "width0": {
    "min": 7.200038896491975,
    "median": 16.499249988573155,
    "max": 37.00434574205451
  },
  "width3": {
    "min": 7.095161584126629,
    "median": 16.064451912278997,
    "max": 36.650710090260304
  },
  "rawImproved": 32
}
```

## 后续
优先研究对实际决策相关语义事件的局部界（全分区界很宽不能自动证明选择），以及有资格稀疏关系、候选分组与开放域覆盖。不要以增加条件化预算代替语义识别。数据轨、独立验收轨、产品轨职责不变，训练与工程另获授权。
