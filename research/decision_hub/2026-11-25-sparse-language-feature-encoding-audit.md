# 自主认知专项累计第85轮候选：稀疏语言特征编码及纯互斥对照修正

2026-11-25。RESEARCH_CANDIDATE / FIXED_FEATURE_AUDIT_EXECUTED / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。main 2a74a2b7e797f15629b80ccca8f305965b434563。核对近20提交、13开放PR、v3.2首8行及历史全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R84前30行、R72前14行、R78前22行。区别于R72词表覆盖、R78静态模型预算、R74候选排序，本轮从固定实际仓库文本枚举有限跨度并编码可学习稀疏特征，实际计数参数规模代理及哈希别名；同时修复R84软因子混杂的纯互斥对照。不修改R84历史。未训练、未拟合、未选择最终编码器。

## 纯互斥修正
R84的4/5边原anti为[2,1,1,1]，旧hard为[1,1,1,0]；本轮修正为[2,1,1,0]。0/1边仍改为[1,1,1,0]，其他因素保持。完整64赋值逐个核对：新权重等于原权重乘两个新增允许指示量；729部分标注掩码直接穷举。历史136冲突及568混合质量损失计数复算；新计数只反映删去赋值造成的未归一分区质量损失，非概率、准确率或效果，质量随分区定义。相同研究者、非独立验收。

## 编码接口及实际输入
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
两固定完整JSON，核对blob。公开原创合成开发数据（ChatGPT研发辅助），32情节64轮167标注，非真人、独立留出或获授权训练。采用Unicode码点位置枚举不含标点/空白的1..24码点跨度；原始标注UTF16位置转码点用于事后几何覆盖，真实字素簇、跨标点和长跨度未实现。每跨度提取显式类型元组：偏置、长度、左右相邻字符、边界字符类型、首尾字符、字符类型序列、1/2/3元组；去重集合（二值特征）。不使用标签、答案、领域或后续轮作为输入。保留原文位置于实际span索引，不把编码当语义身份；真实概念来源、关系特征需后续接入，本轮仅语言局部特征。形状分类、长度24、角色数21沿研究候选或研究者选择，非最终门。全部语料特征字典只用于同集规模审计，不是词表训练或正式部署词表；不能泄露到独立留出。哈希为固定32位FNV式UTF16字符算法取模，非加密或安全身份；类型键JSON元组。全局别名为不同特征键数减占用桶数；同一行别名为行内不同特征数减桶数；即使行内无碰撞，跨行共享桶仍可能干扰学习。统计无预测或梯度、准确率不可推断。对21角色各自完整float32权重数组估算4*21*维数，仅参数字节，排除字典、稀疏索引、梯度、优化器、推理、关系因子、框架开销及设备内存；未实测Mac/iPhone资源。非选择维数的充分依据。没有新增外部资料或真人效果。12项控制。同一研究者执行，非独立验收。无生产修改、训练、Codex、CI、PR合并、部署、费用、冻结协议变更。

## 可复算代码
按L/S顺序载入两个JSON。
```js
function experiment(docs){
 const ck=(x,m)=>{if(!x)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 // Correct R84: keep every surviving assignment's weight unchanged.
 const u=[[1,2],[1,3],[2,1],[1,2],[2,3],[3,2]],soft=[1,1,1,3],anti=[2,1,1,1],hard=[1,1,1,0],edges=[[0,1],[1,2],[2,3],[3,4],[4,5],[0,5]];
 const p=[soft,anti,hard,soft,anti,soft],correct=[hard,anti,hard,soft,[2,1,1,0],soft],old=[hard,anti,hard,soft,hard,soft];
 function weight(q,policy){return q.reduce((w,b,i)=>w*BigInt(u[i][b]),1n)*edges.reduce((w,[a,b],i)=>w*BigInt(policy[i][q[a]+2*q[b]]),1n)}
 let ablation={masks:0,conflicts:0,oldConflicts:0,pureMassLoss:0,mixedMassLoss:0,changedSurvivingMass:0,assignmentChecks:0};
 const worlds=Array.from({length:64},(_,s)=>Array.from({length:6},(_,i)=>(s>>i)&1));
 const ws=worlds.map(q=>{let a=weight(q,p),b=weight(q,correct),c=weight(q,old),allow=!(q[0]&&q[1])&&!(q[4]&&q[5]);ck(b===(allow?a:0n),"pure intervention");ablation.assignmentChecks++;return [a,b,c]});
 function walk(m){if(m.length<6){for(let x=1;x<=3;x++)walk([...m,x]);return}let z=[0n,0n,0n];for(let i=0;i<64;i++)if(worlds[i].every((b,j)=>m[j]&(1<<b)))ws[i].forEach((w,j)=>z[j]+=w);ablation.masks++;ablation.conflicts+=+(z[0]>0n&&z[1]===0n);ablation.oldConflicts+=+(z[0]>0n&&z[2]===0n);ablation.pureMassLoss+=+(z[0]>z[1]);ablation.mixedMassLoss+=+(z[0]>z[2]);ablation.changedSurvivingMass+=+(z[1]!==z[2]);}
 walk([]);
 // Typed tuples avoid ambiguous concatenation. No labels or target answers enter the encoder.
 const punct=/[\p{P}\p{Z}\s]/u,shape=c=>c===undefined?"EDGE":/\p{N}/u.test(c)?"N":/\p{Script=Han}/u.test(c)?"H":/\p{L}/u.test(c)?"L":"X";
 function encode(a,i,j){
  const s=a.slice(i,j),f=new Set(),add=(...x)=>f.add(JSON.stringify(x));
  add("bias");add("len",j-i);add("left",a[i-1]??null);add("right",a[j]??null);add("boundary",shape(a[i-1]),shape(a[j]));add("ends",s[0],s.at(-1));add("shape",s.map(shape).join(""));
  for(let k=1;k<=3;k++)for(let n=0;n+k<=s.length;n++)add("ng",k,s.slice(n,n+k).join(""));
  return f;
 }
 // Deterministic 32-bit hash, UTF16 code units. Hash only features, not semantic IDs or source receipts.
 function hash(s){let h=2166136261;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}return h>>>0}
 let vocab=new Set(),rowSets=[],goldSets=[],out={turns:0,episodes:0,candidates:0,features:0,maxActive:0,uniqueFeatures:0,marked:0,markedRepresentable:0,nonUniqueVectorRows:0,buckets:[],roles:21,controls:0};
 let maxCandidates=0;
 for(let d=0;d<docs.length;d++)for(let e of docs[d].cases){out.episodes++;for(let t of e.turns){
  out.turns++;let a=[...t.text],n=0,bySpan=new Map(),sig=new Map();
  for(let i=0;i<a.length;i++)for(let j=i+1;j<=Math.min(a.length,i+24);j++){if(punct.test(a[j-1]))break;let f=encode(a,i,j);n++;out.candidates++;out.features+=f.size;out.maxActive=Math.max(out.maxActive,f.size);for(let x of f)vocab.add(x);rowSets.push(f);bySpan.set(i+":"+j,f);let k=JSON.stringify([...f].sort());sig.set(k,(sig.get(k)||0)+1)}
  out.nonUniqueVectorRows += [...sig.values()].filter(x=>x>1).reduce((s,x)=>s+x,0);
  maxCandidates=Math.max(maxCandidates,n);
  for(let c of d===0?t.claims:t.proposal.claims){out.marked++;let q=d===0?c.span:c.quote,at=t.text.indexOf(q);ck(at>=0&&at===t.text.lastIndexOf(q),"span");let i=[...t.text.slice(0,at)].length,j=i+[...q].length,fs=bySpan.get(i+":"+j);if(fs){out.markedRepresentable++;goldSets.push(fs)}}
 }}
 out.uniqueFeatures=vocab.size;out.maxCandidatesPerTurn=maxCandidates;out.averageActive=out.features/out.candidates;out.exactDenseFloat32RoleWeightsBytes=4*21*vocab.size;
 for(let b of [1024,4096,16384,65536]){
  let buckets=new Map();for(let x of vocab){let k=hash(x)%b;buckets.set(k,(buckets.get(k)||0)+1)}
  let coll=0,local=0,gold=0,max=0;
  for(let f of rowSets){let n=f.size-new Set([...f].map(x=>hash(x)%b)).size;coll+=n;local+=+(n>0);max=Math.max(max,n)}
  for(let f of goldSets)gold+=+(f.size>new Set([...f].map(x=>hash(x)%b)).size);
  out.buckets.push({dimension:b,occupied:buckets.size,globalAliasExcess:vocab.size-buckets.size,featuresInSharedBuckets:[...buckets.values()].filter(n=>n>1).reduce((s,n)=>s+n,0),localCollisionRows:local,localExcess:coll,markedCollisionRows:gold,maxLocalExcess:max,denseFloat32RoleWeightsBytes:4*21*b})
 }
 for(let test of [()=>ablation.masks===729,()=>ablation.conflicts===136&&ablation.oldConflicts===136,()=>ablation.mixedMassLoss===568,()=>ablation.assignmentChecks===64,()=>out.episodes===32&&out.turns===64&&out.marked===167,()=>out.markedRepresentable<=167,()=>eq([...encode(["甲","乙"],0,2)],[...encode(["甲","乙"],0,2)]),()=>hash("test")===hash("test"),()=>out.buckets.every(x=>x.globalAliasExcess>=0&&x.localCollisionRows<=out.candidates),()=>out.buckets.every(x=>x.markedCollisionRows<=out.markedRepresentable),()=>out.buckets.every((x,i,a)=>!i||x.localExcess<=a[i-1].localExcess),()=>out.buckets.every(x=>x.occupied<=x.dimension)]){ck(test(),"control");out.controls++}
 return {ablation,encoding:out};
}
```

## 实测
```json
{
  "ablation": {
    "masks": 729,
    "conflicts": 136,
    "oldConflicts": 136,
    "pureMassLoss": 448,
    "mixedMassLoss": 568,
    "changedSurvivingMass": 256,
    "assignmentChecks": 64
  },
  "encoding": {
    "turns": 64,
    "episodes": 32,
    "candidates": 8537,
    "features": 144442,
    "maxActive": 63,
    "uniqueFeatures": 10045,
    "marked": 167,
    "markedRepresentable": 165,
    "nonUniqueVectorRows": 28,
    "buckets": [
      {
        "dimension": 1024,
        "occupied": 1024,
        "globalAliasExcess": 9021,
        "featuresInSharedBuckets": 10044,
        "localCollisionRows": 1351,
        "localExcess": 1661,
        "markedCollisionRows": 62,
        "maxLocalExcess": 4,
        "denseFloat32RoleWeightsBytes": 86016
      },
      {
        "dimension": 4096,
        "occupied": 3708,
        "globalAliasExcess": 6337,
        "featuresInSharedBuckets": 9146,
        "localCollisionRows": 427,
        "localExcess": 437,
        "markedCollisionRows": 10,
        "maxLocalExcess": 2,
        "denseFloat32RoleWeightsBytes": 344064
      },
      {
        "dimension": 16384,
        "occupied": 7457,
        "globalAliasExcess": 2588,
        "featuresInSharedBuckets": 4648,
        "localCollisionRows": 67,
        "localExcess": 67,
        "markedCollisionRows": 1,
        "maxLocalExcess": 1,
        "denseFloat32RoleWeightsBytes": 1376256
      },
      {
        "dimension": 65536,
        "occupied": 9278,
        "globalAliasExcess": 767,
        "featuresInSharedBuckets": 1484,
        "localCollisionRows": 27,
        "localExcess": 27,
        "markedCollisionRows": 1,
        "maxLocalExcess": 1,
        "denseFloat32RoleWeightsBytes": 5505024
      }
    ],
    "roles": 21,
    "controls": 12,
    "maxCandidatesPerTurn": 366,
    "averageActive": 16.919526765842804,
    "exactDenseFloat32RoleWeightsBytes": 843780
  }
}
```

## 下一责任
保留稀疏精确特征作可解释基线；哈希压缩仅在独立效果与资源评估后考虑，不以碰撞率直接推断语义效果。接入概念及关系因子需要可追溯来源/未知义项和共享角色索引；随后比较固定/自主学习模型需另获训练授权及合法独立语料。R50完整版本范围保留。数据、独立验收、产品轨职责不变。
