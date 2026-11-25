# 自主认知专项累计第91轮候选：语义存在与引用分离、候选质量守恒及表示细化

2026-11-25。RESEARCH_CANDIDATE / MASS_CONSERVATION_EXECUTED / RAW_BOTH_SIDES / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。main fd247faa333ce35aab8ce98dfa46075d9bf28d76。核对近20提交、13开放PR（#61待审）、v3.2首8行及此前全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R90首23行。新增范围：R90诊断候选数量驱动的存在概率膨胀；本轮改变研究模型结构，分离存在及条件引用，实际审计候选复制、细化与新增的质量守恒。不是保持R90原联合分布的等价算法，不宣称最终模型或真实预测改善。

## 固定输入
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
实际读取完整JSON并核对blob。32情节64轮167标注，ChatGPT研发辅助原创公开合成开发资料，非真人、独立留出或获授权训练。沿R90枚举两侧不含标点/空白的1..24码点跨度，固定一元1+长度mod3，关系分数1+共享二元组数，相邻当前同时存在乘2。标注仅小图参照和事后几何覆盖。正密边只是候选，未确认语义身份或资格。全部当前3074节点、544737原文关系，历史候选ID用同一轮的码点起止；不把相同文字不同位置合并。真实等价性、概念、跨会话身份及来源资格仍未实现。

## 数学与选择
存在链保留一元及相邻因子，但不再乘历史引用分区因子。任意当前存在向量Y，条件历史状态X下每存在节点的引用分布归一为1（多个节点条件独立为本轮候选假设），不存在则只有ABSENT。因此对引用求和后存在分布只由存在链决定，历史候选数或条件引用参数变化不会机械增加存在赔率。可把独立历史存在模型作为先验；本轮未计算全历史隐变量下的引用边际，只检验127个有限候选可用掩码条件分布归一；原文实验引用列表为全部候选可用的假设，不声称其真实存在。存在分区和每位置边际用前后向BigInt精确求和，O(m)阶段，另计大整数及构图开销。相邻软因子仍可能引起偏差，新增当前跨度也可能改变链及存在概率，不承诺当前候选扩展不变性。

固定研究预算为NONE 1/4、OUTSIDE 1/4、域内候选合计1/2，空候选时域内质量转OUTSIDE（3/4）。域内按正分数比例分配。该人工预算非事实概率、校准或最终产品门槛，真实域外不确定性独立保留，所有结果authority NONE。若同一已确认表示ID重复且分数一致则去重，冲突分数拒绝，实际重复通过复制同一对象构造；绝非根据词面推断语义等价。对已存在根质量M进行显式细化，子质量M*w_i/Σw，保留其他根与NONE/OUTSIDE；子ID冲突拒绝。新增真正独立根不能同时无条件保留所有原质量及未知质量：可在明确条件下从OUTSIDE转移指定比例（本轮示例1/3），或重新拟定分布并标记变更，真实转移资格另审。本轮转移和细化皆为可信夹具指定的结构操作，未实现真实授权或自动等价检测。允许转移全部OUTSIDE的数学接口不意味着真实开放域消失；域外未知标志需独立保留。全程整数交叉乘核验。无训练、拟合、真实关系排序或真实概率校准。

## 实验
363个长度1..5、每节点三种一元权重的链及32仓库标注小图，与直接完整当前存在赋值参照核对；同研究者编写非独立验收。原文双侧扩展，复算R90存在下界≥.99计数，比较修改模型的精确存在边际≥.9/.99，仅是结构诊断，两模型不同不能视为准确率改善。每当前节点以最大边分数根为重复/细化对象，2/5/10份复制与不同权重细化，核验所有原质量及总和；普通平铺重归一基线将重复视独立根，检验原组质量变化；独立新增根重归一与显式OUTSIDE转移对照。oldPresenceInflation计数为正边导致条件赔率严格增大的代数检查，非逐次全联合边际实测。无新增外部资料、独立留出、真实语义或设备实测；未实现全请求资源预算。14项控制，未训练、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。保留既有完整版本范围与验收门。

## 可复算代码
按L/S顺序加载固定JSON。
```js
function experiment(docs){
 const ck=(v,m)=>{if(!v)throw Error(m)},u=q=>BigInt(1+[...q].length%3),grams=q=>{let a=[...q];return new Set(a.slice(0,-1).map((c,i)=>c+a[i+1]))};
 function raw(t){let a=[...t],q=[];for(let i=0;i<a.length;i++)for(let j=i+1;j<=Math.min(i+24,a.length);j++){if(/[\p{P}\p{Z}\s]/u.test(a[j-1]))break;q.push({i,j,q:a.slice(i,j).join("")})}return q}
 // Presence chain independent of reference candidate multiplicity.
 function chain(b){
  let n=b.length,f=[[1n,0n]],back=Array(n+1);back[n]=[1n,1n];
  for(let j=0;j<n;j++){let [x,y]=f[j];f.push([x+y,b[j]*(x+2n*y)])}
  for(let j=n-1;j>=0;j--){let [x,y]=back[j+1];back[j]=[x+b[j]*y,x+2n*b[j]*y]}
  let z=f[n][0]+f[n][1];ck(z===back[0][0],"backward");return {z,p:b.map((_,j)=>f[j+1][1]*back[j+1][1])}
 }
 function oracle(b){let z=0n,p=b.map(()=>0n);for(let s=0;s<2**b.length;s++){let w=1n;for(let j=0;j<b.length;j++)if(s&(1<<j)){w*=b[j];if(j&&(s&(1<<(j-1))))w*=2n}z+=w;for(let j=0;j<b.length;j++)if(s&(1<<j))p[j]+=w}return {z,p}}
 // A fixed proposal budget: 1/4 NONE, 1/4 OUTSIDE, 1/2 known if a list
 // exists. All integer numerators share denominator 4*S (S=sum scores).
 // With no list, the known reserve goes to OUTSIDE. Not a calibrated distribution.
 function allocation(rows){
  let groups=new Map();
  for(let {id,w} of rows){ck(typeof id==="string"&&typeof w==="bigint"&&w>0n,"input");if(groups.has(id)&&groups.get(id)!==w)return {status:"CONFLICT",authority:"NONE"};groups.set(id,w)}
  let s=[...groups.values()].reduce((a,b)=>a+b,0n);
  if(!s)return {status:"FINITE",den:4n,none:1n,outside:3n,known:new Map(),authority:"NONE"};
  return {status:"FINITE",den:4n*s,none:s,outside:s,known:new Map([...groups].map(([id,w])=>[id,2n*w])),authority:"NONE"}
 }
 const same=(a,b)=>a.status===b.status&&a.den===b.den&&a.none===b.none&&a.outside===b.outside&&a.known.size===b.known.size&&[...a.known].every(([id,v])=>b.known.get(id)===v);
 const total=a=>a.none+a.outside+[...a.known.values()].reduce((x,y)=>x+y,0n);
 // Explicit refinement: subdivide an existing mass, never re-score the children as independent roots.
 function refine(a,id,parts){
  if(!a.known.has(id)||!parts.length||new Set(parts.map(x=>x.id)).size!==parts.length||parts.some(x=>x.id===id||a.known.has(x.id)||x.w<=0n))return {status:"CONFLICT",authority:"NONE"};
  let s=parts.reduce((n,x)=>n+x.w,0n),parent=a.known.get(id),known=new Map([...a.known].filter(([k])=>k!==id).map(([k,v])=>[k,v*s]));
  for(let x of parts)known.set(x.id,parent*x.w);
  return {status:"FINITE",den:a.den*s,none:a.none*s,outside:a.outside*s,known,authority:"NONE"}
 }
 // A new root can be proposed from an explicitly allocated fraction of OUTSIDE.
 // This is a stipulated transfer, not a discovered fact or automatic authorization.
 function transfer(a,id,n,d){
  if(a.known.has(id)||n<0n||d<=0n||n>d)return {status:"CONFLICT",authority:"NONE"};
  let known=new Map([...a.known].map(([k,v])=>[k,v*d]));known.set(id,a.outside*n);
  return {status:"FINITE",den:a.den*d,none:a.none*d,outside:a.outside*(d-n),known,authority:"NONE"}
 }
 let out={smallEpisodes:0,smallPresenceChecks:0,syntheticChains:0,syntheticPresenceChecks:0,conditionalHistoryMasks:0,rawEpisodes:0,rawCurrent:0,rawPairs:0,marked:0,unmarked:0,old99:0,new90:0,new99:0,new90Marked:0,new90Unmarked:0,allocationChecks:0,duplicateChecks:0,refinementChecks:0,transferChecks:0,flatDuplicateChanged:0,flatAdditionChanged:0,oldPresenceInflation:0,controls:0,records:[]};
 function checkChain(b,kind){let a=chain(b),o=oracle(b);ck(a.z===o.z,"partition");a.p.forEach((v,i)=>{ck(v===o.p[i],"marginal");out[kind+"PresenceChecks"]++})}
 // All chains up to length 5, weights 1..3. 363 chains.
 function walk(b){if(b.length){checkChain(b,"synthetic");out.syntheticChains++}if(b.length<5)for(let i=1n;i<=3n;i++)walk([...b,i])}walk([]);
 // Check conditional reference normalization for every available-set mask.
 for(let n=0;n<=6;n++)for(let mask=0;mask<2**n;mask++){let rows=Array.from({length:n},(_,i)=>({id:String(i),w:BigInt(1+i%3)})).filter((_,i)=>mask&(1<<i));let a=allocation(rows);ck(total(a)===a.den,"conditional mass");out.conditionalHistoryMasks++}
 for(let d=0;d<docs.length;d++)for(let ep of docs[d].cases){
  let [ta,tb]=ep.turns,bb=d===0?tb.claims:tb.proposal.claims,quote=c=>d===0?c.span:c.quote;
  checkChain(bb.map(c=>u(quote(c))),"small");out.smallEpisodes++;
  let A=raw(ta.text),B=raw(tb.text),marked=new Set(),ag=A.map(s=>grams(s.q)),b=B.map(s=>u(s.q)),p=chain(b);out.rawEpisodes++;out.rawCurrent+=B.length;out.rawPairs+=A.length*B.length;
  for(let c of bb){let q=quote(c),at=tb.text.indexOf(q);ck(at>=0&&at===tb.text.lastIndexOf(q),"anchor");let i=[...tb.text.slice(0,at)].length,j=i+[...q].length,k=B.findIndex(x=>x.i===i&&x.j===j);ck(k>=0,"current coverage");marked.add(k)}
  out.marked+=marked.size;out.unmarked+=B.length-marked.size;let rec={id:ep.id,n:A.length,m:B.length,marked:marked.size,old99:0,new90:0,new99:0};
  for(let j=0;j<B.length;j++){
   let g=grams(B[j].q),rows=A.map((s,i)=>({id:s.i+":"+s.j,w:1n+BigInt([...g].filter(x=>ag[i].has(x)).length)})),a=allocation(rows);ck(a.status==="FINITE"&&total(a)===a.den,"allocation");out.allocationChecks++;
   // Reproduce R90's conservative presence bound exactly.
   let L=24n+rows.reduce((s,x,i)=>s+x.w*u(A[i].q)*(12n/(1n+u(A[i].q))),0n),tn=1n,td=1n;
   for(let k of [j-1,j+1])if(k>=0&&k<B.length){tn*=1n+4n*b[k];td*=1n+2n*b[k]}
   let oldNum=b[j]*tn*L,oldDen=12n*td+oldNum;
   if(100n*oldNum>=99n*oldDen){out.old99++;rec.old99++}
   if(10n*p.p[j]>=9n*p.z){out.new90++;rec.new90++;out[marked.has(j)?"new90Marked":"new90Unmarked"]++}
   if(100n*p.p[j]>=99n*p.z){out.new99++;rec.new99++}
   // At fixed current graph, any normalized reference list leaves the presence partition invariant.
   ck(total(a)===a.den,"normalization");
   if(rows.length){
    let root=rows.reduce((x,y)=>y.w>x.w?y:x),s=rows.reduce((n,x)=>n+x.w,0n);
    for(let copies of [2,5,10]){
     let dup=allocation(rows.concat(Array(copies-1).fill(root)));ck(same(a,dup),"duplicate stable");out.duplicateChecks++;
     let k=BigInt(copies),flatS=s+(k-1n)*root.w;
     if(k*root.w*s!==root.w*flatS)out.flatDuplicateChanged++;
     let parts=Array.from({length:copies},(_,i)=>({id:"child:"+i,w:BigInt(i+1)})),v=refine(a,root.id,parts),q=parts.reduce((n,x)=>n+v.known.get(x.id),0n);
     ck(total(v)===v.den&&q*a.den===a.known.get(root.id)*v.den&&v.none*a.den===a.none*v.den&&v.outside*a.den===a.outside*v.den&&[...a.known].every(([id,w])=>id===root.id||v.known.get(id)*a.den===w*v.den),"refinement");out.refinementChecks++;
    }
    let newRoot={id:"new",w:1n},flat=allocation([...rows,newRoot]);if(flat.known.get(root.id)*a.den!==a.known.get(root.id)*flat.den)out.flatAdditionChanged++;
    let v=transfer(a,"new",1n,3n);ck(total(v)===v.den&&v.none*a.den===a.none*v.den&&[...a.known].every(([id,w])=>v.known.get(id)*a.den===w*v.den)&&v.outside*a.den*3n===a.outside*v.den*2n,"transfer");out.transferChecks++;
    // Old model unnormalized local odds strictly increase with a duplicate present history target.
    if(rows.length&&root.w>0n)out.oldPresenceInflation++;
   }
  }out.records.push(rec)
 }
 for(let t of [()=>out.syntheticChains===363,()=>out.conditionalHistoryMasks===127,()=>out.smallEpisodes===32&&out.smallPresenceChecks===57,()=>out.rawEpisodes===32&&out.rawCurrent===3074&&out.rawPairs===544737,()=>out.marked===57&&out.unmarked===3017,()=>out.old99===3074,()=>out.duplicateChecks===3*out.rawCurrent,()=>out.refinementChecks===out.duplicateChecks,()=>out.transferChecks===out.rawCurrent,()=>out.new99===0,()=>allocation([{id:"x",w:1n},{id:"x",w:2n}]).status==="CONFLICT",()=>refine(allocation([{id:"x",w:1n}]),"x",[{id:"x",w:1n}]).status==="CONFLICT",()=>transfer(allocation([]),"x",2n,1n).status==="CONFLICT",()=>allocation([]).outside===3n]){ck(t(),"control");out.controls++}
 return out;
}
```

## 实测
```json
{
  "smallEpisodes": 32,
  "smallPresenceChecks": 57,
  "syntheticChains": 363,
  "syntheticPresenceChecks": 1641,
  "conditionalHistoryMasks": 127,
  "rawEpisodes": 32,
  "rawCurrent": 3074,
  "rawPairs": 544737,
  "marked": 57,
  "unmarked": 3017,
  "old99": 3074,
  "new90": 157,
  "new99": 0,
  "new90Marked": 14,
  "new90Unmarked": 143,
  "allocationChecks": 3074,
  "duplicateChecks": 9222,
  "refinementChecks": 9222,
  "transferChecks": 3074,
  "flatDuplicateChanged": 9222,
  "flatAdditionChanged": 3074,
  "oldPresenceInflation": 3074,
  "controls": 14,
  "records": [
    {
      "id": "L01",
      "n": 133,
      "m": 55,
      "marked": 1,
      "old99": 55,
      "new90": 4,
      "new99": 0
    },
    {
      "id": "L02",
      "n": 137,
      "m": 110,
      "marked": 2,
      "old99": 110,
      "new90": 5,
      "new99": 0
    },
    {
      "id": "L03",
      "n": 128,
      "m": 91,
      "marked": 1,
      "old99": 91,
      "new90": 5,
      "new99": 0
    },
    {
      "id": "L04",
      "n": 156,
      "m": 90,
      "marked": 2,
      "old99": 90,
      "new90": 5,
      "new99": 0
    },
    {
      "id": "L05",
      "n": 152,
      "m": 157,
      "marked": 2,
      "old99": 157,
      "new90": 7,
      "new99": 0
    },
    {
      "id": "L06",
      "n": 178,
      "m": 70,
      "marked": 2,
      "old99": 70,
      "new90": 4,
      "new99": 0
    },
    {
      "id": "L07",
      "n": 366,
      "m": 196,
      "marked": 2,
      "old99": 196,
      "new90": 8,
      "new99": 0
    },
    {
      "id": "L08",
      "n": 152,
      "m": 133,
      "marked": 2,
      "old99": 133,
      "new90": 6,
      "new99": 0
    },
    {
      "id": "L09",
      "n": 139,
      "m": 133,
      "marked": 3,
      "old99": 133,
      "new90": 6,
      "new99": 0
    },
    {
      "id": "L10",
      "n": 187,
      "m": 39,
      "marked": 1,
      "old99": 39,
      "new90": 2,
      "new99": 0
    },
    {
      "id": "L11",
      "n": 185,
      "m": 65,
      "marked": 2,
      "old99": 65,
      "new90": 3,
      "new99": 0
    },
    {
      "id": "L12",
      "n": 127,
      "m": 67,
      "marked": 2,
      "old99": 67,
      "new90": 4,
      "new99": 0
    },
    {
      "id": "L13",
      "n": 156,
      "m": 120,
      "marked": 2,
      "old99": 120,
      "new90": 6,
      "new99": 0
    },
    {
      "id": "L14",
      "n": 184,
      "m": 57,
      "marked": 2,
      "old99": 57,
      "new90": 4,
      "new99": 0
    },
    {
      "id": "L15",
      "n": 137,
      "m": 99,
      "marked": 2,
      "old99": 99,
      "new90": 5,
      "new99": 0
    },
    {
      "id": "L16",
      "n": 248,
      "m": 65,
      "marked": 2,
      "old99": 65,
      "new90": 3,
      "new99": 0
    },
    {
      "id": "L17",
      "n": 222,
      "m": 127,
      "marked": 3,
      "old99": 127,
      "new90": 7,
      "new99": 0
    },
    {
      "id": "L18",
      "n": 85,
      "m": 79,
      "marked": 3,
      "old99": 79,
      "new90": 6,
      "new99": 0
    },
    {
      "id": "S01",
      "n": 205,
      "m": 83,
      "marked": 2,
      "old99": 83,
      "new90": 4,
      "new99": 0
    },
    {
      "id": "S02",
      "n": 226,
      "m": 76,
      "marked": 1,
      "old99": 76,
      "new90": 4,
      "new99": 0
    },
    {
      "id": "S03",
      "n": 108,
      "m": 64,
      "marked": 1,
      "old99": 64,
      "new90": 4,
      "new99": 0
    },
    {
      "id": "S04",
      "n": 177,
      "m": 91,
      "marked": 1,
      "old99": 91,
      "new90": 5,
      "new99": 0
    },
    {
      "id": "S05",
      "n": 210,
      "m": 91,
      "marked": 1,
      "old99": 91,
      "new90": 3,
      "new99": 0
    },
    {
      "id": "S06",
      "n": 133,
      "m": 66,
      "marked": 2,
      "old99": 66,
      "new90": 4,
      "new99": 0
    },
    {
      "id": "S07",
      "n": 208,
      "m": 102,
      "marked": 2,
      "old99": 102,
      "new90": 6,
      "new99": 0
    },
    {
      "id": "S08",
      "n": 138,
      "m": 49,
      "marked": 1,
      "old99": 49,
      "new90": 3,
      "new99": 0
    },
    {
      "id": "S09",
      "n": 188,
      "m": 83,
      "marked": 1,
      "old99": 83,
      "new90": 4,
      "new99": 0
    },
    {
      "id": "S10",
      "n": 180,
      "m": 141,
      "marked": 2,
      "old99": 141,
      "new90": 7,
      "new99": 0
    },
    {
      "id": "S11",
      "n": 74,
      "m": 133,
      "marked": 2,
      "old99": 133,
      "new90": 6,
      "new99": 0
    },
    {
      "id": "S12",
      "n": 136,
      "m": 64,
      "marked": 2,
      "old99": 64,
      "new90": 4,
      "new99": 0
    },
    {
      "id": "S13",
      "n": 175,
      "m": 157,
      "marked": 2,
      "old99": 157,
      "new90": 7,
      "new99": 0
    },
    {
      "id": "S14",
      "n": 233,
      "m": 121,
      "marked": 1,
      "old99": 121,
      "new90": 6,
      "new99": 0
    }
  ]
}
```

## 后续
优先研究当前跨度表示细化的稳定性、真实语义身份与义务覆盖、候选质量分配的可学习机制及独立评价。当前消除的是指定历史候选数量直接乘入存在赔率的结构路径；未解决实际白话理解、重复当前节点、候选间依赖、未知检测、正确引用、统计校准或产品效果。数据轨、独立验收轨及产品轨职责不变，训练与正式工程另获授权。
