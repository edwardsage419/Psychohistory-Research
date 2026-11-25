# 自主认知专项累计第92轮候选：当前语义根节点细化不变性与重复证据分离

2026-11-25。RESEARCH_CANDIDATE / EXACT_REFINEMENT_INVARIANCE_EXECUTED / RAW_CURRENT / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线main a9f116328fd64bad3f273806748295ad3822e556。核对近20提交、13开放PR（#61待审）、v3.2首8行及此前全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R91首20行。新增范围：R91分离存在及历史引用、历史根质量守恒；本轮验证当前存在链上的根细化及其对其他节点影响，平铺重复反例，以及单独来源支持路径夹具。未修改历史成果或原生平台。

## 固定输入
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
实际读取完整JSON并核对blob。32情节64轮167人工标注，ChatGPT研发辅助原创公开合成开发资料，非真人、独立留出或获授权训练。本轮仅当前侧32轮，3074原文候选，沿R91不含标点/空白、1..24码点跨度，存在权重1+长度mod3，相邻同时存在乘2；57标注仅事后原文起止匹配，其余3017未标注不是负例。固定任意权重、邻接与候选生成顺序均是研究夹具，不具真实语义资格。未计算真实引用或模型训练。

## 数学及边界
根节点Y∈{0,1}，已资格的互斥完备细化子标签仅在Y=1时可取一个；子条件权重d_i/S，S=Σd_i>0。根缺失时没有子标签，外部因子只依赖Y。对每个原赋值，Y=1时对子标签求和为1，Y=0时因子为1；边际化恢复原联合分布，因此所有根事件保持不变，而子事件权重为原根存在权重乘d_i/S。整数实现统一乘S，缺失项也须乘S。二维转移矩阵原为[[1,w],[1,2w]]，细化后为S乘原矩阵；平铺复制k个独立候选则为原矩阵k次乘积，并且改变邻接结构，不等价于细化。用前后向边界消息和替换块求分区、组至少一个存在及直接左右邻居边际，BigInt交叉乘精确核验；平铺组存在分子排除全部复制节点缺失的质量，细化缺失统一乘S。草稿检查发现缺失项缩放不可省略，实际运行源码已修正。第一次完整运行最后的方向控制失败：错误预期所有平铺变化均增加概率，未取得正式结果；改为方向分项及总数恒等核验，保留失败记录，不调整权重或候选。全联合投影不变由数学证明，小图逐根边际直接枚举核验；扩展图只计算根组及直接邻居，未逐一复算所有远端边际。细化每次独立从原图开始，不把各变体计成独立现实样本。真实子语义是否互斥完备、是否继承全部外部因子需证据；若子解释能共存、影响不同义务或具有不同关系则不能套用此等价，不以相同词面合并。新增独立根仍可能改变真实联合分布，未解决任意新增当前跨度的不变性。全请求预算、设备时间内存未实测。

来源夹具单独保留根ID及每条路径的必需来源集合，重复相同路径只保留一次；路径内AND、路径间OR，撤回来源重算，两个不同根即使共享同一来源也不合并。此为外部指定等价身份及有限布尔支持，不推断来源独立性、证据强度、真实主体或冲突真值，不将无支持当否定，authority NONE、outside true。未接入存在权重或真实证据资格/授权。

## 实验
长度1..4、每节点3种权重共120条链，每个位置拆成2/3/5个互斥子标签，直接枚举原赋值及细化状态，核验全根边际与子质量。原文32轮对每个3074节点单独进行2/5/10份细化及平铺复制对照；诊断.9/.99仅为模型内阈值，不是实际置信度、准确率、错误放行率。来源夹具3来源、8掩码与明确逻辑参照，同研究者设计，非独立验收。无新增外部资料或真人、训练、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。12项控制。保留既有完整版本范围及正式验收门。下一步优先研究真正可学习的语义根选择、子解释对不同义务的影响及跨模块可信接口；独立轨负责未见评价，数据轨负责合法来源，产品轨唯一交接，训练和正式版本另获授权。

## 可复算代码
按L/S顺序加载固定JSON，调用experiment(docs)。
```js
function experiment(docs){
 const ck=(v,m)=>{if(!v)throw Error(m)},u=q=>BigInt(1+[...q].length%3),eq=(a,b)=>a[0]*b[1]===b[0]*a[1],gt=(a,b)=>a[0]*b[1]>b[0]*a[1];
 function raw(t){let a=[...t],q=[];for(let i=0;i<a.length;i++)for(let j=i+1;j<=Math.min(i+24,a.length);j++){if(/[\p{P}\p{Z}\s]/u.test(a[j-1]))break;q.push({i,j,q:a.slice(i,j).join("")})}return q}
 function chain(b){let n=b.length,f=[[1n,0n]],back=Array(n+1);back[n]=[1n,1n];for(let j=0;j<n;j++){let [x,y]=f[j];f.push([x+y,b[j]*(x+2n*y)])}for(let j=n-1;j>=0;j--){let [x,y]=back[j+1];back[j]=[x+b[j]*y,x+2n*b[j]*y]}let z=f[n][0]+f[n][1];ck(z===back[0][0],"chain");return {z,f,back,p:b.map((_,j)=>f[j+1][1]*back[j+1][1])}}
 function block(w,k){let M=[[1n,0n],[0n,1n]];for(let t=0;t<k;t++)M=M.map(([a,b])=>[a+b,w*(a+2n*b)]);return M}
 function splice(base,b,j,M,S=1n){let f=base.f[j],v=base.back[j+1],q=M.map(row=>row[0]*v[0]+row[1]*v[1]);let z=f[0]*q[0]+f[1]*q[1],abs=(f[0]+f[1])*v[0]*S;let left=j>0?[f[1]*q[1],z]:null,right=null;if(j+1<b.length){let tail=b[j+1]*base.back[j+2][1];right=[f[0]*(M[0][0]+2n*M[0][1])*tail+f[1]*(M[1][0]+2n*M[1][1])*tail,z]}return {z,any:[z-abs,z],left,right}}
 function refinedMatrix(w,parts){let S=parts.reduce((a,b)=>a+b,0n),M=[[S,0n],[S,0n]];for(let d of parts){M[0][1]+=w*d;M[1][1]+=2n*w*d}return {M,S}}
 function refinedOracle(b,j,parts){let S=parts.reduce((a,b)=>a+b,0n),z=0n,p=b.map(()=>0n),children=parts.map(()=>0n);for(let mask=0;mask<2**b.length;mask++){let w=1n;for(let i=0;i<b.length;i++)if(mask&(1<<i)){w*=b[i];if(i&&(mask&(1<<(i-1))))w*=2n}if(mask&(1<<j)){parts.forEach((d,k)=>{let v=w*d;z+=v;children[k]+=v;for(let i=0;i<b.length;i++)if(mask&(1<<i))p[i]+=v})}else{let v=w*S;z+=v;for(let i=0;i<b.length;i++)if(mask&(1<<i))p[i]+=v}}return {z,p,children,S}}
 function support(paths,active){let canonical=new Map();for(let p of paths){let ids=[...new Set(p.sources)].sort();if(!ids.length)return {status:"CONFLICT",authority:"NONE"};let key=JSON.stringify([p.root,ids]);canonical.set(key,{root:p.root,ids})}let roots=new Map();for(let p of canonical.values()){let a=roots.get(p.root)||[];if(p.ids.every(x=>active.has(x)))a.push(p.ids);roots.set(p.root,a)}return {status:"FINITE",roots,authority:"NONE",outside:true}}
 let o={syntheticChains:0,syntheticRefinements:0,syntheticAllMarginalChecks:0,syntheticChildChecks:0,rawEpisodes:0,rawNodes:0,marked:0,unmarked:0,rawRefinements:0,rawRootChecks:0,rawNeighborChecks:0,flatGroupIncreases:0,flatGroupDecreases:0,flatGroupChanges:0,flatNeighborChecks:0,flatNeighborChanges:0,flatNeighborIncreases:0,flatNeighborDecreases:0,flatMarkedGroupChanges:0,flatUnmarkedGroupChanges:0,flatRoot90Crossings:0,flatRoot99Crossings:0,sourceMaskChecks:0,sourceDuplicateChecks:0,sourceWithdrawalChecks:0,sourceDistinctRootChecks:0,controls:0,records:[]};
 function walk(b){if(b.length){o.syntheticChains++;let a=chain(b);for(let j=0;j<b.length;j++)for(let k of [2,3,5]){let parts=Array.from({length:k},(_,i)=>BigInt(i+1)),v=refinedOracle(b,j,parts),x=refinedMatrix(b[j],parts),w=splice(a,b,j,x.M,x.S);ck(v.z===a.z*v.S&&w.z===v.z,"partition");v.p.forEach((p,i)=>{ck(p===a.p[i]*v.S,"all projected marginals");o.syntheticAllMarginalChecks++});v.children.forEach((p,i)=>{ck(p===a.p[j]*parts[i],"child mass");o.syntheticChildChecks++});ck(eq(w.any,[a.p[j],a.z]),"root");o.syntheticRefinements++}}if(b.length<4)for(let v of [1n,2n,3n])walk([...b,v])}walk([]);
 for(let d=0;d<docs.length;d++)for(let ep of docs[d].cases){let t=ep.turns[1],cs=d===0?t.claims:t.proposal.claims,spans=raw(t.text),b=spans.map(s=>u(s.q)),a=chain(b),marked=new Set();for(let c of cs){let q=d===0?c.span:c.quote,at=t.text.indexOf(q);ck(at>=0&&at===t.text.lastIndexOf(q),"anchor");let i=[...t.text.slice(0,at)].length,j=i+[...q].length,k=spans.findIndex(x=>x.i===i&&x.j===j);ck(k>=0,"coverage");marked.add(k)}o.rawEpisodes++;o.rawNodes+=b.length;o.marked+=marked.size;o.unmarked+=b.length-marked.size;let rec={id:ep.id,n:b.length,flatGroupChanges:0,flatNeighborChanges:0};
 for(let j=0;j<b.length;j++)for(let k of [2,5,10]){let parts=Array.from({length:k},(_,i)=>BigInt(i+1)),x=refinedMatrix(b[j],parts),base=splice(a,b,j,block(b[j],1)),v=splice(a,b,j,x.M,x.S),flat=splice(a,b,j,block(b[j],k));ck(v.z===a.z*x.S&&eq(v.any,[a.p[j],a.z]),"root invariance");o.rawRootChecks++;o.rawRefinements++;ck(eq(base.any,[a.p[j],a.z]),"base splice");if(!eq(flat.any,base.any)){o.flatGroupChanges++;rec.flatGroupChanges++;o[marked.has(j)?"flatMarkedGroupChanges":"flatUnmarkedGroupChanges"]++;o[gt(flat.any,base.any)?"flatGroupIncreases":"flatGroupDecreases"]++}
 for(let [den,num,key] of [[10n,9n,"flatRoot90Crossings"],[100n,99n,"flatRoot99Crossings"]])if(base.any[0]*den<base.any[1]*num&&flat.any[0]*den>=flat.any[1]*num)o[key]++;
 for(let side of ["left","right"])if(base[side]){ck(eq(v[side],base[side]),"neighbor invariant");ck(eq(base[side],[a.p[j+(side==="left"?-1:1)],a.z]),"neighbor baseline");o.rawNeighborChecks++;o.flatNeighborChecks++;if(!eq(flat[side],base[side])){o.flatNeighborChanges++;rec.flatNeighborChanges++;o[gt(flat[side],base[side])?"flatNeighborIncreases":"flatNeighborDecreases"]++}}
 }o.records.push(rec)}
 const paths=[{root:"A",sources:["s0","s1"]},{root:"A",sources:["s2"]},{root:"B",sources:["s0"]},{root:"C",sources:["s0"]}];
 for(let mask=0;mask<8;mask++){let active=new Set(["s0","s1","s2"].filter((_,i)=>mask&(1<<i))),a=support(paths,active);let expect=[Boolean((mask&3)===3||mask&4),Boolean(mask&1),Boolean(mask&1)];ck(["A","B","C"].every((k,i)=>Boolean(a.roots.get(k).length)===expect[i]),"support oracle");o.sourceMaskChecks++;for(let k of [2,5,10]){let v=support(paths.flatMap(p=>Array(k).fill(p)),active);ck(JSON.stringify([...v.roots])===JSON.stringify([...a.roots]),"duplicate proof");o.sourceDuplicateChecks++}if(mask&1){ck(a.roots.has("B")&&a.roots.has("C")&&a.roots.get("B").length===1&&a.roots.get("C").length===1,"distinct roots");o.sourceDistinctRootChecks++}for(let i=0;i<3;i++)if(mask&(1<<i)){let next=new Set(active);next.delete("s"+i);let v=support(paths,next);for(let k of ["A","B","C"])ck(v.roots.get(k).length<=a.roots.get(k).length,"withdrawal");o.sourceWithdrawalChecks++}}
 for(let [name,test] of [["chains",o.syntheticChains===120],["raw",o.rawEpisodes===32&&o.rawNodes===3074],["coverage",o.marked===57&&o.unmarked===3017],["refinements",o.rawRefinements===9222],["root",o.rawRootChecks===9222],["group accounting",o.flatGroupChanges===o.flatGroupIncreases+o.flatGroupDecreases],["neighbor accounting",o.flatNeighborChanges===o.flatNeighborIncreases+o.flatNeighborDecreases],["marked",o.flatMarkedGroupChanges+o.flatUnmarkedGroupChanges===o.flatGroupChanges],["source masks",o.sourceMaskChecks===8&&o.sourceDuplicateChecks===24],["withdrawal",o.sourceWithdrawalChecks===12],["distinct",o.sourceDistinctRootChecks===4],["empty",support([{root:"A",sources:[]}],new Set()).status==="CONFLICT"]]){ck(test,name);o.controls++}
 return o;
}
```

## 实测
```json
{
  "syntheticChains": 120,
  "syntheticRefinements": 1278,
  "syntheticAllMarginalChecks": 4734,
  "syntheticChildChecks": 4260,
  "rawEpisodes": 32,
  "rawNodes": 3074,
  "marked": 57,
  "unmarked": 3017,
  "rawRefinements": 9222,
  "rawRootChecks": 9222,
  "rawNeighborChecks": 18252,
  "flatGroupIncreases": 9222,
  "flatGroupDecreases": 0,
  "flatGroupChanges": 9222,
  "flatNeighborChecks": 18252,
  "flatNeighborChanges": 18252,
  "flatNeighborIncreases": 9216,
  "flatNeighborDecreases": 9036,
  "flatMarkedGroupChanges": 171,
  "flatUnmarkedGroupChanges": 9051,
  "flatRoot90Crossings": 8751,
  "flatRoot99Crossings": 6148,
  "sourceMaskChecks": 8,
  "sourceDuplicateChecks": 24,
  "sourceWithdrawalChecks": 12,
  "sourceDistinctRootChecks": 4,
  "controls": 12,
  "records": [
    {
      "id": "L01",
      "n": 55,
      "flatGroupChanges": 165,
      "flatNeighborChanges": 324
    },
    {
      "id": "L02",
      "n": 110,
      "flatGroupChanges": 330,
      "flatNeighborChanges": 654
    },
    {
      "id": "L03",
      "n": 91,
      "flatGroupChanges": 273,
      "flatNeighborChanges": 540
    },
    {
      "id": "L04",
      "n": 90,
      "flatGroupChanges": 270,
      "flatNeighborChanges": 534
    },
    {
      "id": "L05",
      "n": 157,
      "flatGroupChanges": 471,
      "flatNeighborChanges": 936
    },
    {
      "id": "L06",
      "n": 70,
      "flatGroupChanges": 210,
      "flatNeighborChanges": 414
    },
    {
      "id": "L07",
      "n": 196,
      "flatGroupChanges": 588,
      "flatNeighborChanges": 1170
    },
    {
      "id": "L08",
      "n": 133,
      "flatGroupChanges": 399,
      "flatNeighborChanges": 792
    },
    {
      "id": "L09",
      "n": 133,
      "flatGroupChanges": 399,
      "flatNeighborChanges": 792
    },
    {
      "id": "L10",
      "n": 39,
      "flatGroupChanges": 117,
      "flatNeighborChanges": 228
    },
    {
      "id": "L11",
      "n": 65,
      "flatGroupChanges": 195,
      "flatNeighborChanges": 384
    },
    {
      "id": "L12",
      "n": 67,
      "flatGroupChanges": 201,
      "flatNeighborChanges": 396
    },
    {
      "id": "L13",
      "n": 120,
      "flatGroupChanges": 360,
      "flatNeighborChanges": 714
    },
    {
      "id": "L14",
      "n": 57,
      "flatGroupChanges": 171,
      "flatNeighborChanges": 336
    },
    {
      "id": "L15",
      "n": 99,
      "flatGroupChanges": 297,
      "flatNeighborChanges": 588
    },
    {
      "id": "L16",
      "n": 65,
      "flatGroupChanges": 195,
      "flatNeighborChanges": 384
    },
    {
      "id": "L17",
      "n": 127,
      "flatGroupChanges": 381,
      "flatNeighborChanges": 756
    },
    {
      "id": "L18",
      "n": 79,
      "flatGroupChanges": 237,
      "flatNeighborChanges": 468
    },
    {
      "id": "S01",
      "n": 83,
      "flatGroupChanges": 249,
      "flatNeighborChanges": 492
    },
    {
      "id": "S02",
      "n": 76,
      "flatGroupChanges": 228,
      "flatNeighborChanges": 450
    },
    {
      "id": "S03",
      "n": 64,
      "flatGroupChanges": 192,
      "flatNeighborChanges": 378
    },
    {
      "id": "S04",
      "n": 91,
      "flatGroupChanges": 273,
      "flatNeighborChanges": 540
    },
    {
      "id": "S05",
      "n": 91,
      "flatGroupChanges": 273,
      "flatNeighborChanges": 540
    },
    {
      "id": "S06",
      "n": 66,
      "flatGroupChanges": 198,
      "flatNeighborChanges": 390
    },
    {
      "id": "S07",
      "n": 102,
      "flatGroupChanges": 306,
      "flatNeighborChanges": 606
    },
    {
      "id": "S08",
      "n": 49,
      "flatGroupChanges": 147,
      "flatNeighborChanges": 288
    },
    {
      "id": "S09",
      "n": 83,
      "flatGroupChanges": 249,
      "flatNeighborChanges": 492
    },
    {
      "id": "S10",
      "n": 141,
      "flatGroupChanges": 423,
      "flatNeighborChanges": 840
    },
    {
      "id": "S11",
      "n": 133,
      "flatGroupChanges": 399,
      "flatNeighborChanges": 792
    },
    {
      "id": "S12",
      "n": 64,
      "flatGroupChanges": 192,
      "flatNeighborChanges": 378
    },
    {
      "id": "S13",
      "n": 157,
      "flatGroupChanges": 471,
      "flatNeighborChanges": 936
    },
    {
      "id": "S14",
      "n": 121,
      "flatGroupChanges": 363,
      "flatNeighborChanges": 720
    }
  ]
}
```
