# v3.2 自主认知专项第15轮（累计第74轮）：有界语义候选搜索及排序瓶颈

2026-11-25。RESEARCH_CANDIDATE / REPOSITORY_CORPUS_EVALUATION_EXECUTED / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线 f0165084702334e492618c5882788036e996c570；13开放Draft PR，#61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e。核查最近8提交、v3.2 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（前段及历史全文）、AGENTS 78cc1f8327ec50b5762103fedfaf1f06e85f7658、同步规程26c4d946e48f01858fb8e8c2cb06e4f7ba91bf05、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（相关标题非全文）、第73轮af648d16ee96b9af4a3efb61b413d113208bb0ca、第61轮17b6035732e43c56edc44cb5db07b8d49aadfd5b、第59轮445c19d01268bc4ec5e5d8b6a9eb1cfc237ab1b2。R61既有有限逻辑多树，R59已有实际原生基线，R73已统一标注；本轮不重复上述，研究真实仓库文本上的候选跨度搜索与人工固定排序造成的覆盖瓶颈。未重新运行原生解释器，不与R59不同指标直接横比。

## 固定输入
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
实际读取两套JSON全文并核对连接器blob身份。32情节64轮167原标注均为ChatGPT研发辅助项目原创合成公开开发材料；本轮仅取约束、行动、修订三类明确标注正例，修订可与行动/约束双重计数，未标注内容不能当负例。无真人、独立留出、训练许可确认或外部原始语料；无新外部事实。非全语义任务。

## 实验合同
算法仅接收原文，无标注、领域或答案作为输入；单轮独立，未使用真实跨轮状态。固定人工词汇及权重，未拟合、训练、按结果调权；词汇由研究者基于一般语言直觉及既有项目知识拟定，开发语料已经公开且研究者可能已见，不能称盲测。最长128 UTF16位置输入；按列出的标点和空白切分，再枚举每段全部1..24 UTF16长度子串，候选搜索复杂度O(T L)个跨度（L=24），每角色词汇匹配成本另计；排序O(M log M)。实际代码未计运行时与内存，不是移动设备资源测量。跨度边界与词面完整包含；不识别复杂标点、中文分词、代词、否定作用域、语义组合或真实意图。对每个跨度分别按三类词面命中生成角色候选，命中数截断为2、句界或连接词边界加分、偏离长度8扣分；固定排序及同分位置打破平局。多个角色可能同时存在，不强制消歧。所有结果authority NONE/coverage UNVERIFIED，top K仅检索工作预算，不证明候选集合完整、不能代替R58独立义务核查、R63联合逻辑及用户确认。对于漏掉的原文继续保持未知，不能将搜索失败解释为没有义务。比较原始分句精确及包含覆盖、完整跨度集合精确覆盖、词面门后可排序覆盖、每轮每角色top1/3/5/10/20/50。分句及完整跨度无角色过滤，仅比较几何覆盖上界；候选召回以原文起止和粗角色相同为准，未评估主体/条件/修订目标、完整IR或实际建议。不同角色的候选总数可含相同跨度；预算是候选条数，不是用户需回答的问题数。没有精度/误报率计算，因为R73确认部分文本未标注。MRR分子为rank倒数和，缺失为0，除targets才为MRR。专项控制13项。所有模型参数和词典均为研究方案，非正式产品标准。

## 实际结果及解释
{
  "targets": 67,
  "clauseExact": 34,
  "clauseContains": 66,
  "latticeExact": 66,
  "rankable": 42,
  "top1": 22,
  "top3": 31,
  "top5": 34,
  "top10": 37,
  "top20": 42,
  "top50": 42,
  "reciprocalRankSum": 27.497169394073413,
  "noLattice": 1,
  "noCue": 24,
  "below50": 0
}
完整跨度覆盖仅证明原始标注位于候选搜索空间，不证明找到正确语义；词汇过滤丢失与排序损失分别报告，不能借扩大候选数宣称真实泛化。多候选与top1同一排序器比较，不是实际PR或普通AI对照。修订仅记录角色候选，不执行历史更改。每轮可能有多个标注，完整轮召回另计。实际数据见下；研究结论优先依据低召回/负结果，不把候选数量当进展。后续应采用能区分部分监督未知的结构化候选排序研究，固定多结构表示，研究可复算学习目标与候选集上界；在明确授权前不训练。先核对真实语言数据许可及独立冻结集，独立轨掌握未见情节，产品轨维护唯一交接。完整版本12项范围维持，未授权新Codex任务或最终路线。

## 复算
将固定两个JSON按L/S顺序解析成docs，执行下列JS；无需第三方依赖，非生产实现。

```js
function experiment(docs){
 const ck=(b,m)=>{if(!b)throw Error(m)},roles=["constraint","action","revision"];
 const cues={constraint:["必须","不能","不得","最多","至少","上限","下限","以内","以外","不超过","不少于","只要","底线","限制","不去","不联系","强制","要求"],action:["选择","申请","参加","取消","继续","停止","购买","辞职","换","去","留","走","出发","报名","学习","上课","调整","申请","转","挪","延期","退","做","记录"],revision:["改","撤","取消","替换","不再","重新","刚核实","实际是","暂时不","仅用于","不作为","纠正","更新"]};
 const punct=/[，。！？；、：,.!?;:\s]/u,edges=["或者","还是","但是","如果","而且","以及","或者说","然后","并且","就","且","和","或","再"];
 const rankSort=(a,b)=>b.score-a.score||a.start-b.start||a.end-b.end;
 function scan(text){
  if(typeof text!=="string"||!text.length||text.length>128)return {status:"LIMIT_OR_INVALID",authority:"NONE"};
  const clauses=[],all=[],ranked=Object.fromEntries(roles.map(r=>[r,[]]));
  let start=0;
  for(let i=0;i<=text.length;i++)if(i===text.length||punct.test(text[i])){
   if(i>start)clauses.push({start,end:i,text:text.slice(start,i)});start=i+1;
  }
  for(const c of clauses)for(let i=c.start;i<c.end;i++)for(let j=i+1;j<=Math.min(c.end,i+24);j++){
   const s=text.slice(i,j),v={start:i,end:j,text:s};all.push(v);
   const left=i===c.start||edges.some(x=>text.slice(c.start,i).endsWith(x)),right=j===c.end||edges.some(x=>text.startsWith(x,j));
   for(const role of roles){
    const hits=[...new Set(cues[role])].filter(x=>s.includes(x));
    if(!hits.length)continue;
    // Fixed hand-authored integers; no fit, calibration, or post-run weight changes.
    const score=4*Math.min(2,hits.length)+3*Number(left)+3*Number(right)-Math.abs(s.length-8)/4;
    ranked[role].push({...v,role,score,hits,authority:"NONE"});
   }
  }
  for(const r of roles)ranked[r].sort(rankSort);
  return {status:"CANDIDATES_ONLY",clauses,all,ranked,authority:"NONE",coverage:"UNVERIFIED"};
 }
 function gold(d,a){
  const r=[];
  if(d===0){if(["HARD","CONDITIONAL_HARD"].includes(a.kind))r.push("constraint");if(["PROPOSED_ACTION","CONDITIONAL_ACTION","ACTION"].includes(a.kind))r.push("action");if(a.kind==="REVISION")r.push("revision")}
  else{if(a.role==="constraint")r.push("constraint");if(a.role==="action")r.push("action");if(["replace","retract"].includes(a.op))r.push("revision")}
  return r;
 }
 const blank=()=>({targets:0,clauseExact:0,clauseContains:0,latticeExact:0,rankable:0,top1:0,top3:0,top5:0,top10:0,top20:0,top50:0,reciprocalRankSum:0,noLattice:0,noCue:0,below50:0});
 let out={turns:0,spanCandidates:0,roleCandidates:0,clauseCandidates:0,peakSpanCandidates:0,peakRoleCandidates:0,byRole:Object.fromEntries(roles.map(r=>[r,blank()])),byCorpus:{L:blank(),S:blank()},total:blank(),turnsWithTargets:0,allTargetsTop1:0,allTargetsTop10:0,allTargetsTop50:0,controls:0,examples:{},budget:{1:0,3:0,5:0,10:0,20:0,50:0}};
 for(let d=0;d<docs.length;d++)for(const ep of docs[d].cases)for(let ti=0;ti<ep.turns.length;ti++){
  const turn=ep.turns[ti],z=scan(turn.text);ck(z.status==="CANDIDATES_ONLY","input");out.turns++;out.spanCandidates+=z.all.length;out.clauseCandidates+=z.clauses.length;
  const n=roles.reduce((n,r)=>n+z.ranked[r].length,0);out.roleCandidates+=n;out.peakSpanCandidates=Math.max(out.peakSpanCandidates,z.all.length);out.peakRoleCandidates=Math.max(out.peakRoleCandidates,n);
  for(const k of [1,3,5,10,20,50])out.budget[k]+=roles.reduce((n,r)=>n+Math.min(k,z.ranked[r].length),0);
  const ranks=[];
  for(const a of d===0?turn.claims:turn.proposal.claims)for(const r of gold(d,a)){
   const q=d===0?a.span:a.quote,st=turn.text.indexOf(q),en=st+q.length;ck(st>=0&&st===turn.text.lastIndexOf(q),"span");
   const match=x=>x.start===st&&x.end===en;
   const cl=z.clauses.some(match),cc=z.clauses.some(x=>x.start<=st&&en<=x.end),lat=z.all.some(match),idx=z.ranked[r].findIndex(match),rank=idx<0?Infinity:idx+1;ranks.push(rank);
   ck(!Number.isFinite(rank)||lat,"rank subset");ck(!cl||cc,"clause containment");
   for(const b of [out.total,out.byRole[r],out.byCorpus[d===0?"L":"S"]]){
    b.targets++;b.clauseExact+=+cl;b.clauseContains+=+cc;b.latticeExact+=+lat;b.rankable+=+Number.isFinite(rank);b.noLattice+=+!lat;b.noCue+=+(lat&&!Number.isFinite(rank));b.below50+=+(Number.isFinite(rank)&&rank>50);b.reciprocalRankSum+=Number.isFinite(rank)?1/rank:0;for(const k of [1,3,5,10,20,50])b["top"+k]+=+(rank<=k);
   }
   const record={episode:ep.id,turn:ti+1,role:r,quote:q,rank:Number.isFinite(rank)?rank:null,clauseExact:cl,latticeExact:lat};
   if(!lat&&!out.examples.noLattice)out.examples.noLattice=record;
   if(lat&&!Number.isFinite(rank)&&!out.examples.noCue)out.examples.noCue=record;
   if(rank>1&&rank<=10&&!out.examples.multi)out.examples.multi=record;
   if(Number.isFinite(rank)&&rank>50&&!out.examples.below50)out.examples.below50=record;
  }
  if(ranks.length){out.turnsWithTargets++;out.allTargetsTop1+=+ranks.every(x=>x<=1);out.allTargetsTop10+=+ranks.every(x=>x<=10);out.allTargetsTop50+=+ranks.every(x=>x<=50)}
 }
 const tests=[()=>scan("").status==="LIMIT_OR_INVALID",()=>scan("甲".repeat(129)).status==="LIMIT_OR_INVALID",()=>scan("，。").all.length===0,()=>scan("必须去").ranked.constraint.some(x=>x.text==="必须去"),()=>scan("必须去").ranked.action.some(x=>x.text==="必须去"),()=>scan("改为申请").ranked.revision.some(x=>x.text==="改为申请"),()=>scan("必须去，不能走").all.every(x=>!punct.test(x.text)),()=>scan("甲乙").ranked.constraint.length===0,()=>scan("必须去").authority==="NONE",()=>scan("必须去").coverage==="UNVERIFIED",()=>out.total.targets===Object.values(out.byRole).reduce((n,r)=>n+r.targets,0),()=>out.total.targets===out.total.noLattice+out.total.noCue+out.total.rankable,()=>[1,3,5,10,20].every((k,i)=>out.total["top"+k]<=out.total["top"+[3,5,10,20,50][i]])];
 for(const test of tests){ck(test(),"control");out.controls++}return out;
}
```

```json
{
  "turns": 64,
  "spanCandidates": 8537,
  "roleCandidates": 1584,
  "clauseCandidates": 182,
  "peakSpanCandidates": 366,
  "peakRoleCandidates": 85,
  "byRole": {
    "constraint": {
      "targets": 25,
      "clauseExact": 19,
      "clauseContains": 25,
      "latticeExact": 25,
      "rankable": 16,
      "top1": 10,
      "top3": 14,
      "top5": 14,
      "top10": 15,
      "top20": 16,
      "top50": 16,
      "reciprocalRankSum": 12.226190476190476,
      "noLattice": 0,
      "noCue": 9,
      "below50": 0
    },
    "action": {
      "targets": 30,
      "clauseExact": 6,
      "clauseContains": 29,
      "latticeExact": 29,
      "rankable": 17,
      "top1": 6,
      "top3": 10,
      "top5": 11,
      "top10": 13,
      "top20": 17,
      "top50": 17,
      "reciprocalRankSum": 8.320978917882943,
      "noLattice": 1,
      "noCue": 12,
      "below50": 0
    },
    "revision": {
      "targets": 12,
      "clauseExact": 9,
      "clauseContains": 12,
      "latticeExact": 12,
      "rankable": 9,
      "top1": 6,
      "top3": 7,
      "top5": 9,
      "top10": 9,
      "top20": 9,
      "top50": 9,
      "reciprocalRankSum": 6.95,
      "noLattice": 0,
      "noCue": 3,
      "below50": 0
    }
  },
  "byCorpus": {
    "L": {
      "targets": 23,
      "clauseExact": 12,
      "clauseContains": 22,
      "latticeExact": 22,
      "rankable": 13,
      "top1": 5,
      "top3": 9,
      "top5": 10,
      "top10": 12,
      "top20": 13,
      "top50": 13,
      "reciprocalRankSum": 7.30952380952381,
      "noLattice": 1,
      "noCue": 9,
      "below50": 0
    },
    "S": {
      "targets": 44,
      "clauseExact": 22,
      "clauseContains": 44,
      "latticeExact": 44,
      "rankable": 29,
      "top1": 17,
      "top3": 22,
      "top5": 24,
      "top10": 25,
      "top20": 29,
      "top50": 29,
      "reciprocalRankSum": 20.18764558454961,
      "noLattice": 0,
      "noCue": 15,
      "below50": 0
    }
  },
  "total": {
    "targets": 67,
    "clauseExact": 34,
    "clauseContains": 66,
    "latticeExact": 66,
    "rankable": 42,
    "top1": 22,
    "top3": 31,
    "top5": 34,
    "top10": 37,
    "top20": 42,
    "top50": 42,
    "reciprocalRankSum": 27.497169394073413,
    "noLattice": 1,
    "noCue": 24,
    "below50": 0
  },
  "turnsWithTargets": 44,
  "allTargetsTop1": 11,
  "allTargetsTop10": 21,
  "allTargetsTop50": 26,
  "controls": 13,
  "examples": {
    "multi": {
      "episode": "L02",
      "turn": 1,
      "role": "constraint",
      "quote": "只要夜班我就不去",
      "rank": 2,
      "clauseExact": false,
      "latticeExact": true
    },
    "noCue": {
      "episode": "L03",
      "turn": 2,
      "role": "revision",
      "quote": "停课还能退五百",
      "rank": null,
      "clauseExact": false,
      "latticeExact": true
    },
    "noLattice": {
      "episode": "L05",
      "turn": 1,
      "role": "action",
      "quote": "到时候看谁更需要，再挪两天",
      "rank": null,
      "clauseExact": false,
      "latticeExact": false
    }
  },
  "budget": {
    "1": 66,
    "3": 198,
    "5": 326,
    "10": 606,
    "20": 1019,
    "50": 1523
  }
}
```

未修改生产代码、训练、CI、PR合并、部署或新增费用，冻结协议不变。