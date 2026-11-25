# v3.2 自主认知专项第17轮（累计第76轮）：部分监督跨轮引用图与联合候选搜索

2026-11-25。RESEARCH_CANDIDATE / FIXED_SCORE_GRAPH_EXECUTED / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。实际main 412439ac53fcb755fadae8c9320a4d74e68ac705，13开放Draft PR，#61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e。核查最新8提交、v3.2 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（前段及历史全文）、AGENTS 78cc1f8327ec50b5762103fedfaf1f06e85f7658、同步规程26c4d946e48f01858fb8e8c2cb06e4f7ba91bf05、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（相关标题，非全文）。发现R75主报告0fae5d3a25e09632b0ad3d49593393b74f0589e6及增补84b2c651b628139c84ea43ee1d7c7ff3989756b8已完成固定参数CRF边际似然、梯度与数值极端验证，因此取消原拟重复实验。新增范围为跨轮引用边的候选图、局部部分监督目标及显式联合限制下的精确分区函数和边边际。复用R73标注身份、R64引用修订思想；未再次运行R75或原生解释器。无新增文献或外部事实，本轮数学为有限加权求和，不主张原创定理。

## 实际仓库数据
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
两套JSON全文实际解析并核对连接器返回blob，32情节64轮，原创合成公开开发资料（ChatGPT研发辅助），非真人/独立留出，训练许可未确认。为隔离引用问题，本轮由原始标注提供当前与历史节点、角色、跨度、可用field，而非从原始白话抽取这些信息（teacher-forced）；隐去ref/supersedes评分，所有同情节前轮标注均为候选，另有NO_LINK和OUTSIDE两个研究性占位节点。当前仅双轮语料，无长期记忆、真实权威身份、引用解析或修订执行。S的引用由一基索引定位，L按零基轮次和field定位；所有12条已标引用均唯一（此前R73已验证结构）；真实泛化及语义正确性未知。其他未标/显式null一律保留全部选择相容，不升级为已知无引用。词面字符集合Jaccard、相同原标签、明确同field、按既往出现次序的相对位置为四固定特征，权重1/2/1/0.25由研究者选定，未训练或调参；同分以ID排序，仅排序分数，不是权限或校准概率。全部候选包括错误及未知，未评估误报率；最新标注基线是简单研究对照，非普通AI/现有平台。实际输入每个第二轮标注一个当前节点，真实图没有经认证的跨节点互斥规则，禁止从标签推断唯一目标关系。对于已标注边，负对数似然log Z(all)-log Z(compatible)，固定分数；未标注时相容集=全集，损失/梯度0。把未标注/空字段强制NO_LINK会新增未经确认的监督。损失差不代表准确率或训练收益。实际只计算固定分数与期望，没有权重更新。全部计算权限NONE；候选不得自动撤回或替换原有记录。

## 联合结构合同与验证
合成小图有1..3当前节点，两个旧目标A/B及可重复NONE。每条边权为固定正整数，分区函数Z=Σ合法赋值∏边权。若且仅若可信任务合同明确两个不同当前操作不能引用同一旧目标，才打开distinct；现实中多条更正可引用同一旧事实，禁止默认互斥。状态(i,used)递推加权和，used为已选真实目标位图；固定当前选择掩码后计算分子Z(edge)，边边际为Z(edge)/Z。无合法赋值Z=0返回冲突，不虚构概率。没有互斥时分区分解为独立节点；有互斥时同一局部最佳可能不能组成合法图。比较局部最大分数拼接与合法联合域，及错误开启互斥导致的质量损失；计数是合成组合，不是现实概率或产品缺陷。一般复杂度随目标数量指数增长，本轮仅2目标，未测手机资源或任意图、循环、复杂因素；独立留出及正式训练另授权。合成图以BigInt精确求和，与直接列举完整赋值及边计数独立计算路径对照，同一研究者定义，不是独立科学验收。禁止将分区概率作为现实事实或安全许可。没有实现真实联合模型学习或生产语义图。

## 复算及实际结果
将上述固定JSON按L/S顺序解析为docs，运行以下JS，无外部依赖。实际执行完整语料及有限图，8项边界控制。
```js
function experiment(docs){
 const ck=(b,m)=>{if(!b)throw Error(m)},theta=[1,2,1,.25],dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
 const chars=s=>new Set([...s]),jac=(a,b)=>{a=chars(a);b=chars(b);let n=[...a].filter(x=>b.has(x)).length;return n/(a.size+b.size-n||1)};
 const fold=xs=>{const max=Math.max(...xs.map(x=>x.score)),w=xs.map(x=>Math.exp(x.score-max)),z=w.reduce((s,v)=>s+v,0);return {logZ:max+Math.log(z),mean:theta.map((_,k)=>xs.reduce((s,x,i)=>s+w[i]*x.f[k],0)/z)}};
 let r={corpus:{episodes:0,secondTurnNodes:0,edges:0,annotatedRefs:0,unannotatedOrNull:0,top1:0,top3:0,all:0,latestCorrect:0,partialLoss:0,forcedNullAdditionalLoss:0,artificialSignalNodes:0,records:[]},joint:{cases:0,valid:0,conflict:0,edgeChecks:0,exactAgreement:0,independentArgmaxInvalid:0,unjustifiedDistinctConflict:0,unjustifiedDistinctMassLoss:0},controls:0};
 for(let d=0;d<docs.length;d++)for(const e of docs[d].cases){
  r.corpus.episodes++;let previous=[];
  for(let ti=0;ti<e.turns.length;ti++){
   const aa=d===0?e.turns[ti].claims:e.turns[ti].proposal.claims;
   for(let i=0;i<aa.length;i++){
    if(!ti)continue;
    let a=aa[i],id=`${e.id}.${ti+1}.${i+1}`,q=d===0?a.span:a.quote,tag=d===0?a.kind:a.role;
    // Given current and prior annotation nodes, hide ref/supersedes from scoring.
    let edges=previous.map((b,j)=>{let f=[+(tag===b.tag),+(typeof a.field==="string"&&a.field===b.field),jac(q,b.quote),(j+1)/Math.max(1,previous.length)];return {id:b.id,f,score:dot(theta,f)}});
    edges.push({id:"NO_LINK",f:[0,0,0,0],score:0},{id:"OUTSIDE",f:[0,0,0,0],score:0});
    edges.sort((a,b)=>b.score-a.score||a.id.localeCompare(b.id));let all=fold(edges);
    let c=r.corpus;c.secondTurnNodes++;c.edges+=edges.length;
    let ref=d===0?a.supersedes:a.ref;
    if(typeof ref==="string"){
     let gold=[];
     if(d===1)gold=previous.filter(b=>b.id===ref).map(b=>b.id);
     else{let m=/^([^:]+):t(\d+):(.+)$/.exec(ref);ck(m&&m[1]===e.id,"ref format");gold=previous.filter(b=>b.turn===+m[2]&&b.field===m[3]).map(b=>b.id)}
     ck(gold.length===1,"unique anchored reference");
     let pos=edges.findIndex(x=>x.id===gold[0])+1;ck(pos>0,"missing edge");let p=fold(edges.filter(x=>gold.includes(x.id)));
     c.annotatedRefs++;c.all++;c.top1+=+(pos===1);c.top3+=+(pos<=3);c.latestCorrect+=+(previous.at(-1)?.id===gold[0]);c.partialLoss+=all.logZ-p.logZ;c.records.push({id,target:gold[0],rank:pos,candidates:edges.length,latest:previous.at(-1)?.id});
    }else{
     c.unannotatedOrNull++;
     // No reference annotation: all choices remain compatible, exact zero objective.
     const partial=fold(edges);ck(all.logZ===partial.logZ&&all.mean.every((x,i)=>x===partial.mean[i]),"zero signal");
     let n=fold(edges.filter(x=>x.id==="NO_LINK"));c.forcedNullAdditionalLoss+=all.logZ-n.logZ;c.artificialSignalNodes+=+(all.mean.some((x,i)=>Math.abs(x-n.mean[i])>1e-12));
    }
   }
   previous.push(...aa.map((a,i)=>({id:`${e.id}.${ti+1}.${i+1}`,turn:ti,tag:d===0?a.kind:a.role,field:a.field,quote:d===0?a.span:a.quote})));
  }
 }
 // Exact weighted partitions on synthetic graphs. Targets A/B, repeatable NONE.
 // Distinctness is a confirmed scope policy, NEVER inferred from count/role.
 const W=[[2n,3n,1n],[3n,2n,1n],[1n,4n,2n]];
 function partition(m,distinct){let cache=new Map();function walk(i,used){if(i===m.length)return 1n;let key=i+":"+used;if(cache.has(key))return cache.get(key);let z=0n;for(let j=0;j<3;j++)if((m[i]&(1<<j))&&(!distinct||j===2||!(used&(1<<j))))z+=W[i][j]*walk(i+1,distinct&&j<2?used|(1<<j):used);cache.set(key,z);return z}return walk(0,0)}
 function enumerate(m,distinct){let z=0n,edge=m.map(()=>[0n,0n,0n]);function walk(y,w){if(y.length===m.length){z+=w;y.forEach((v,i)=>edge[i][v]+=w);return}let i=y.length;for(let j=0;j<3;j++)if((m[i]&(1<<j))&&(!distinct||j===2||!y.includes(j)))walk([...y,j],w*W[i][j])}walk([],1n);return {z,edge}}
 for(let n=1;n<=3;n++){
  function loop(m){if(m.length<n){for(let j=1;j<=7;j++)loop([...m,j]);return}
   const unconstrained=partition(m,false),constrained=partition(m,true);ck(constrained<=unconstrained,"subset");r.joint.unjustifiedDistinctConflict+=+(unconstrained>0n&&constrained===0n);r.joint.unjustifiedDistinctMassLoss+=+(constrained<unconstrained);
   let best=m.map((mask,i)=>[0,1,2].filter(j=>mask&(1<<j)).sort((a,b)=>Number(W[i][b]-W[i][a])||a-b)[0]);
   r.joint.independentArgmaxInvalid+=+(constrained>0n&&best.filter(x=>x!==2).length!==new Set(best.filter(x=>x!==2)).size);
   for(const distinct of [false,true]){let z=partition(m,distinct),b=enumerate(m,distinct);r.joint.cases++;ck(z===b.z,"partition");r.joint.exactAgreement++;r.joint[z?"valid":"conflict"]++;
    for(let i=0;i<n;i++){let sum=0n;for(let j=0;j<3;j++){let q=m.slice();q[i]&=1<<j;let v=partition(q,distinct);ck(v===b.edge[i][j],"edge numerator");sum+=v;r.joint.edgeChecks++}ck(sum===z,"marginal mass")}
   }
  }loop([])
 }
 for(const test of [()=>partition([1,1],false)===6n,()=>partition([1,1],true)===0n,()=>partition([4,4],true)===1n,()=>partition([0,7],false)===0n,()=>partition([7,7],true)<partition([7,7],false),()=>r.corpus.annotatedRefs===12,()=>r.corpus.secondTurnNodes===r.corpus.annotatedRefs+r.corpus.unannotatedOrNull,()=>r.corpus.top1<=r.corpus.top3&&r.corpus.top3<=r.corpus.all]){ck(test(),"control");r.controls++}
 return r;
}
```
```json
{
  "corpus": {
    "episodes": 32,
    "secondTurnNodes": 57,
    "edges": 305,
    "annotatedRefs": 12,
    "unannotatedOrNull": 45,
    "top1": 12,
    "top3": 12,
    "all": 12,
    "latestCorrect": 4,
    "partialLoss": 9.044125770594361,
    "forcedNullAdditionalLoss": 94.24857458781574,
    "artificialSignalNodes": 45,
    "records": [
      {
        "id": "L03.2.1",
        "target": "L03.1.2",
        "rank": 1,
        "candidates": 6,
        "latest": "L03.1.4"
      },
      {
        "id": "L08.2.2",
        "target": "L08.1.2",
        "rank": 1,
        "candidates": 5,
        "latest": "L08.1.3"
      },
      {
        "id": "L15.2.1",
        "target": "L15.1.1",
        "rank": 1,
        "candidates": 6,
        "latest": "L15.1.4"
      },
      {
        "id": "S01.2.1",
        "target": "S01.1.2",
        "rank": 1,
        "candidates": 6,
        "latest": "S01.1.4"
      },
      {
        "id": "S02.2.1",
        "target": "S02.1.3",
        "rank": 1,
        "candidates": 5,
        "latest": "S02.1.3"
      },
      {
        "id": "S03.2.1",
        "target": "S03.1.3",
        "rank": 1,
        "candidates": 5,
        "latest": "S03.1.3"
      },
      {
        "id": "S04.2.1",
        "target": "S04.1.4",
        "rank": 1,
        "candidates": 6,
        "latest": "S04.1.4"
      },
      {
        "id": "S08.2.1",
        "target": "S08.1.2",
        "rank": 1,
        "candidates": 5,
        "latest": "S08.1.3"
      },
      {
        "id": "S10.2.1",
        "target": "S10.1.2",
        "rank": 1,
        "candidates": 6,
        "latest": "S10.1.4"
      },
      {
        "id": "S11.2.1",
        "target": "S11.1.1",
        "rank": 1,
        "candidates": 5,
        "latest": "S11.1.3"
      },
      {
        "id": "S12.2.1",
        "target": "S12.1.2",
        "rank": 1,
        "candidates": 7,
        "latest": "S12.1.5"
      },
      {
        "id": "S13.2.1",
        "target": "S13.1.3",
        "rank": 1,
        "candidates": 5,
        "latest": "S13.1.3"
      }
    ]
  },
  "joint": {
    "cases": 798,
    "valid": 745,
    "conflict": 53,
    "edgeChecks": 6804,
    "exactAgreement": 798,
    "independentArgmaxInvalid": 205,
    "unjustifiedDistinctConflict": 53,
    "unjustifiedDistinctMassLoss": 328
  },
  "controls": 8
}
```

## 后续
下一优先级是将R74的原始文本候选跨度、R75部分监督局部模型、R76引用图接口组合成实际原始文本输入的候选结构搜索，清楚区分人工标注节点与自主生成节点，分别测候选上界、结构可行性、未知、跨轮和联合约束。不得利用公开开发集调参后冒充独立泛化。独立轨隔离未见语料，真实许可/训练另获授权；继续保留完整版本12项范围及v3.2自主核心。唯一交接由产品轨维护。未改生产代码、启动训练、Codex、CI、合并、部署或新增费用，冻结协议不变。