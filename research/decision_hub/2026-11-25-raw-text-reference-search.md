# v3.2 自主认知专项第18轮（累计第77轮）：原始双轮文本引用候选及预算瓶颈

2026-11-25。RESEARCH_CANDIDATE / RAW_TEXT_CANDIDATE_GRAPH_EXECUTED / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。实际main 49db5ed4676f45e5a8b9af4dcf8c4a24e01b9b4f，13开放Draft PR，#61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e。核查最新8提交、v3.2 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（前段及历史全文）、AGENTS 78cc1f8327ec50b5762103fedfaf1f06e85f7658、同步规程26c4d946e48f01858fb8e8c2cb06e4f7ba91bf05、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（相关标题非全文）、R74 bbdc12dfe65b24aa24e6b1d25a04955766cadab4、R75 0fae5d3a25e09632b0ad3d49593393b74f0589e6、R76 a12f23fb34de26baa7189d6c9cbf50a516dc34c0。R76在给定原始角色/字段/跨度节点时12/12首位命中；本轮取消原始文本搜索中的人工节点、角色及字段输入，测量原文跨度到引用边的候选覆盖和排序差距。改编R74跨度算法及R76固定特征排序，不复用训练模型，也未实际连接CRF；R75边际目标思想仅用于条件单边诊断。无新增外部文献或事实。

## 固定输入
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
实际读取两个固定完整JSON并核对连接器返回blob。32情节64轮167原标注，12明确引用，45第二轮无明确引用标注。全部为ChatGPT研发辅助原创合成公开开发资料，非真人、独立留出，训练许可未确认。所有语料为已见，规则权重由研究者固定指定，未拟合、不根据结果调权；不宣称盲测。完整搜索仅输入两轮文本，不输入标注、角色、领域、field、ref；在生成候选以后才用标注评估。精确原文起止覆盖为代理指标，并非完整引用语义正确、真实事实、权威或修改许可。

## 方法
长度128 UTF16上限，枚举每段长度1..24的候选，边界得分6满分、长度偏差惩罚，允许一个内部标点的变体额外惩罚2；两端不能是标点。桥接变体仅扩大几何候选，不判定语义跨句。用两端跨度评分之和、4倍字符集合Jaccard及2倍当前修订词面命中构造边分数，无人工角色/字段；排序同分以原文位置稳定打破。引用边仅从第二轮指向第一轮，不能覆盖任意跨轮、多个主体、事件或隐式引用。所有输出authority NONE。无互斥限制、无自动引用写入、无完整角色判断或语义义务验证。全边枚举O(Nprev*Ncur)且排序O(M log M)，每边相似度额外有字符集合计算；200000边硬上限，超限LIMIT且不产生确定性。首次运行断言所有情节均可完整搜索失败，停止未写入。修正记录每个LIMIT及其目标，保持原上限和权重，不截断后声称完整；无效输入也显式拒绝。端点预算K=5/10/30/100分别取各轮固定评分前K；全边rank1/5/20/100评估按全情节边排序（多个正确边可共存，前K仅计算预算非用户负担）。对照另给正确当前跨度（仅诊断，使用标注），计算对旧跨度排序及单边部分监督目标：logsumexp(全部候选边分数及NO_LINK/OUTSIDE两个零分选项)-正例分数；无明确引用标注时相容全集，损失0。比较强制NO_LINK新增损失，仅限当前跨度可搜索的节点；无正例不等于无引用。该局部目标不构建全图分区或全体语义模型，不训练、不计算更新，不把概率当真实事实。无负例标签所以不评估precision；不以rank误差宣称产品缺陷。代码按情节累计边数一次，命中统计按12条正例，LIMIT不计为完成搜索或错误语义，仍保留总分母。13专项控制。未运行原生平台、实际CRF或设备，无性能、真机或独立验收。

## 复算及实际结果
将固定两个JSON按L/S顺序解析为docs，执行下列JS，标准运行时即可，不需要网络或外部库。
```js
function experiment(docs){
 const ck=(b,m)=>{if(!b)throw Error(m)},punct=/[，。！？；、：,.!?;:\s]/u,connect=["或者","还是","但是","如果","而且","以及","然后","并且","就","且","和","或","再"];
 const revision=["改","撤","取消","替换","不再","重新","刚核实","实际是","暂时不","仅用于","不作为","纠正","更新"];
 const budgets=[5,10,30,100],edgeBudgets=[1,5,20,100],blank=()=>({episodes:0,limited:0,requested:0,executed:0,targets:0,limitedTargets:0,covered:0,rank1:0,rank5:0,rank20:0,rank100:0});
 function spans(s,bridge){
  if(typeof s!=="string"||s.length>128||!s.length)return [];
  let out=[];
  for(let i=0;i<s.length;i++)if(!punct.test(s[i]))for(let j=i+1;j<=Math.min(s.length,i+24);j++){
   let x=s.slice(i,j),p=[...x].filter(v=>punct.test(v)).length;
   if(p>(bridge?1:0))break;
   if(punct.test(s[j-1]))continue;
   let left=i===0||punct.test(s[i-1])||connect.some(v=>s.slice(0,i).endsWith(v)),right=j===s.length||punct.test(s[j])||connect.some(v=>s.startsWith(v,j));
   out.push({start:i,end:j,text:x,score:3*(+left+ +right)-Math.abs(x.length-8)/4-2*p,cue:revision.some(v=>x.includes(v)),chars:new Set([...x].filter(v=>!punct.test(v)))});
  }return out.sort((a,b)=>b.score-a.score||a.start-b.start||a.end-b.end);
 }
 const jac=(a,b)=>{let n=0;for(const x of a.chars)if(b.chars.has(x))n++;return n/(a.chars.size+b.chars.size-n||1)};
 const edgeScore=(a,b)=>a.score+b.score+4*jac(a,b)+2*Number(b.cue);
 function search(x,y,k=Infinity,bridge=false){
  if(typeof x!=="string"||typeof y!=="string"||!x.length||!y.length||x.length>128||y.length>128)return {status:"INVALID",authority:"NONE",a:[],b:[],edges:[],requested:0};
  let a=spans(x,bridge).slice(0,k),b=spans(y,bridge).slice(0,k),requested=a.length*b.length;
  if(requested>200000)return {status:"LIMIT",authority:"NONE",a,b,edges:[],requested};
  let edges=[];for(const u of a)for(const v of b)edges.push({a:u,b:v,score:edgeScore(u,v)});
  edges.sort((x,y)=>y.score-x.score||x.a.start-y.a.start||x.a.end-y.a.end||x.b.start-y.b.start||x.b.end-y.b.end);
  return {status:"CANDIDATES_ONLY",authority:"NONE",a,b,edges,requested};
 }
 const pos=(text,q)=>{let s=text.indexOf(q);ck(s>=0&&s===text.lastIndexOf(q),"span");return [s,s+q.length]},same=(a,b)=>a.start===b[0]&&a.end===b[1],quote=(a,d)=>d===0?a.span:a.quote;
 const lse=xs=>{let m=Math.max(...xs);return m+Math.log(xs.reduce((s,x)=>s+Math.exp(x-m),0))};
 let r={episodes:0,turns:0,positiveEdges:0,unmarkedCurrentNodes:0,full:blank(),bridge:blank(),budgets:Object.fromEntries(budgets.map(k=>[k,blank()])),currentSpanTop30:0,priorSpanTop30:0,revisionCueGold:0,oracleCurrentSpanTop1:0,oracleCurrentSpanTop5:0,oracleCurrentSpanTop20:0,conditionalLossSum:0,conditionalLossCount:0,unmarkedForcedNoLink:0,unmarkedZeroSignal:0,unmarkedAdditionalLoss:0,unmarkedUnavailable:0,records:[],controls:0,limits:[]};
 function account(z,s,id,mode){s.episodes++;s.requested+=z.requested;s.executed+=z.edges.length;if(z.status==="LIMIT"){s.limited++;r.limits.push({id,mode,requested:z.requested})}else ck(z.status==="CANDIDATES_ONLY","valid search")}
 function evaluate(z,g,s){s.targets++;if(z.status==="LIMIT"){s.limitedTargets++;return null}let i=z.edges.findIndex(e=>same(e.a,g.a)&&same(e.b,g.b));if(i>=0){s.covered++;for(const k of edgeBudgets)s["rank"+k]+=+(i<k)}return i<0?null:i+1}
 for(let d=0;d<docs.length;d++)for(const e of docs[d].cases){
  const [t0,t1]=e.turns;
  const full=search(t0.text,t1.text),bridge=search(t0.text,t1.text,Infinity,true),small=budgets.map(k=>search(t0.text,t1.text,k));
  r.episodes++;r.turns+=2;
  account(full,r.full,e.id,"full");account(bridge,r.bridge,e.id,"bridge");small.forEach((z,i)=>account(z,r.budgets[budgets[i]],e.id,"K"+budgets[i]));
  const aa=d===0?t0.claims:t0.proposal.claims,bb=d===0?t1.claims:t1.proposal.claims;
  for(let i=0;i<bb.length;i++){
   const cur=bb[i],ref=d===0?cur.supersedes:cur.ref,q=pos(t1.text,quote(cur,d)),cond=full.edges.filter(z=>same(z.b,q));
   if(typeof ref!=="string"){
    r.unmarkedCurrentNodes++;
    if(cond.length){let all=lse([0,0,...cond.map(x=>x.score)]);ck(all===lse([0,0,...cond.map(x=>x.score)]),"same compatible set");r.unmarkedZeroSignal++;r.unmarkedAdditionalLoss+=all;r.unmarkedForcedNoLink+=+(all>0)}else r.unmarkedUnavailable++;
    continue;
   }
   let prev;
   if(d===0){let m=/^([^:]+):t0:(.+)$/.exec(ref);ck(m&&m[1]===e.id,"ref");let v=aa.filter(x=>x.field===m[2]);ck(v.length===1,"reference");prev=v[0]}
   else{let m=/^([^.]+)\.1\.(\d+)$/.exec(ref);ck(m&&m[1]===e.id&&aa[+m[2]-1],"reference");prev=aa[+m[2]-1]}
   const g={a:pos(t0.text,quote(prev,d)),b:q};r.positiveEdges++;
   let raw=evaluate(full,g,r.full),wide=evaluate(bridge,g,r.bridge),bs=small.map((z,j)=>evaluate(z,g,r.budgets[budgets[j]]));
   let p=full.a.findIndex(x=>same(x,g.a))+1,c=full.b.findIndex(x=>same(x,g.b))+1;
   r.priorSpanTop30+=+(p>0&&p<=30);r.currentSpanTop30+=+(c>0&&c<=30);r.revisionCueGold+=+(c>0&&full.b[c-1].cue);
   let oracle=cond.findIndex(z=>same(z.a,g.a))+1;
   if(oracle>0){r.oracleCurrentSpanTop1+=+(oracle<=1);r.oracleCurrentSpanTop5+=+(oracle<=5);r.oracleCurrentSpanTop20+=+(oracle<=20);r.conditionalLossSum+=lse([0,0,...cond.map(z=>z.score)])-cond[oracle-1].score;r.conditionalLossCount++}
   r.records.push({episode:e.id,currentId:i+1,priorSpanRank:p||null,currentSpanRank:c||null,rawEdgeRank:raw,bridgedEdgeRank:wide,budgetRanks:bs,oracleCurrentSpanRank:oracle||null});
  }
 }
 for(const test of [()=>spans("甲，乙",false).every(x=>!x.text.includes("，")),()=>spans("甲，乙",true).some(x=>x.text==="甲，乙"),()=>search("甲".repeat(129),"乙").status==="INVALID",()=>search("","乙").status==="INVALID",()=>search("甲","乙").edges.length===1,()=>search("甲".repeat(128),"乙".repeat(128)).status==="LIMIT",()=>r.positiveEdges===12,()=>budgets.every((k,i)=>i===0||r.budgets[k].covered>=r.budgets[budgets[i-1]].covered),()=>r.full.rank1<=r.full.rank5&&r.full.rank5<=r.full.rank20&&r.full.rank20<=r.full.rank100,()=>r.unmarkedCurrentNodes===45,()=>r.conditionalLossSum>=0,()=>r.unmarkedZeroSignal+r.unmarkedUnavailable===45,()=>[r.full,r.bridge,...Object.values(r.budgets)].every(s=>s.episodes===32&&s.targets===12&&s.executed<=s.requested&&s.covered+s.limitedTargets<=12)]){ck(test(),"control");r.controls++}
 return r;
}
```
```json
{
  "episodes": 32,
  "turns": 64,
  "positiveEdges": 12,
  "unmarkedCurrentNodes": 45,
  "full": {
    "episodes": 32,
    "limited": 0,
    "requested": 544737,
    "executed": 544737,
    "targets": 12,
    "limitedTargets": 0,
    "covered": 12,
    "rank1": 3,
    "rank5": 6,
    "rank20": 6,
    "rank100": 10
  },
  "bridge": {
    "episodes": 32,
    "limited": 1,
    "requested": 2017385,
    "executed": 1785177,
    "targets": 12,
    "limitedTargets": 0,
    "covered": 12,
    "rank1": 3,
    "rank5": 6,
    "rank20": 6,
    "rank100": 10
  },
  "budgets": {
    "5": {
      "episodes": 32,
      "limited": 0,
      "requested": 800,
      "executed": 800,
      "targets": 12,
      "limitedTargets": 0,
      "covered": 5,
      "rank1": 3,
      "rank5": 5,
      "rank20": 5,
      "rank100": 5
    },
    "10": {
      "episodes": 32,
      "limited": 0,
      "requested": 3200,
      "executed": 3200,
      "targets": 12,
      "limitedTargets": 0,
      "covered": 7,
      "rank1": 3,
      "rank5": 6,
      "rank20": 7,
      "rank100": 7
    },
    "30": {
      "episodes": 32,
      "limited": 0,
      "requested": 28800,
      "executed": 28800,
      "targets": 12,
      "limitedTargets": 0,
      "covered": 10,
      "rank1": 3,
      "rank5": 6,
      "rank20": 6,
      "rank100": 9
    },
    "100": {
      "episodes": 32,
      "limited": 0,
      "requested": 260615,
      "executed": 260615,
      "targets": 12,
      "limitedTargets": 0,
      "covered": 12,
      "rank1": 3,
      "rank5": 6,
      "rank20": 6,
      "rank100": 10
    }
  },
  "currentSpanTop30": 12,
  "priorSpanTop30": 10,
  "revisionCueGold": 9,
  "oracleCurrentSpanTop1": 3,
  "oracleCurrentSpanTop5": 8,
  "oracleCurrentSpanTop20": 9,
  "conditionalLossSum": 34.07543182890778,
  "conditionalLossCount": 12,
  "unmarkedForcedNoLink": 45,
  "unmarkedZeroSignal": 45,
  "unmarkedAdditionalLoss": 532.2551127406414,
  "unmarkedUnavailable": 0,
  "records": [
    {
      "episode": "L03",
      "currentId": 1,
      "priorSpanRank": 25,
      "currentSpanRank": 8,
      "rawEdgeRank": 567,
      "bridgedEdgeRank": 770,
      "budgetRanks": [
        null,
        null,
        384,
        567
      ],
      "oracleCurrentSpanRank": 22
    },
    {
      "episode": "L08",
      "currentId": 2,
      "priorSpanRank": 3,
      "currentSpanRank": 8,
      "rawEdgeRank": 23,
      "bridgedEdgeRank": 23,
      "budgetRanks": [
        null,
        17,
        23,
        23
      ],
      "oracleCurrentSpanRank": 3
    },
    {
      "episode": "L15",
      "currentId": 1,
      "priorSpanRank": 47,
      "currentSpanRank": 1,
      "rawEdgeRank": 142,
      "bridgedEdgeRank": 146,
      "budgetRanks": [
        null,
        null,
        null,
        142
      ],
      "oracleCurrentSpanRank": 30
    },
    {
      "episode": "S01",
      "currentId": 1,
      "priorSpanRank": 6,
      "currentSpanRank": 2,
      "rawEdgeRank": 2,
      "bridgedEdgeRank": 2,
      "budgetRanks": [
        null,
        2,
        2,
        2
      ],
      "oracleCurrentSpanRank": 2
    },
    {
      "episode": "S02",
      "currentId": 1,
      "priorSpanRank": 40,
      "currentSpanRank": 1,
      "rawEdgeRank": 21,
      "bridgedEdgeRank": 21,
      "budgetRanks": [
        null,
        null,
        null,
        21
      ],
      "oracleCurrentSpanRank": 16
    },
    {
      "episode": "S03",
      "currentId": 1,
      "priorSpanRank": 5,
      "currentSpanRank": 2,
      "rawEdgeRank": 3,
      "bridgedEdgeRank": 3,
      "budgetRanks": [
        3,
        3,
        3,
        3
      ],
      "oracleCurrentSpanRank": 3
    },
    {
      "episode": "S04",
      "currentId": 1,
      "priorSpanRank": 1,
      "currentSpanRank": 2,
      "rawEdgeRank": 1,
      "bridgedEdgeRank": 1,
      "budgetRanks": [
        1,
        1,
        1,
        1
      ],
      "oracleCurrentSpanRank": 1
    },
    {
      "episode": "S08",
      "currentId": 1,
      "priorSpanRank": 1,
      "currentSpanRank": 1,
      "rawEdgeRank": 1,
      "bridgedEdgeRank": 1,
      "budgetRanks": [
        1,
        1,
        1,
        1
      ],
      "oracleCurrentSpanRank": 1
    },
    {
      "episode": "S10",
      "currentId": 1,
      "priorSpanRank": 1,
      "currentSpanRank": 1,
      "rawEdgeRank": 1,
      "bridgedEdgeRank": 1,
      "budgetRanks": [
        1,
        1,
        1,
        1
      ],
      "oracleCurrentSpanRank": 1
    },
    {
      "episode": "S11",
      "currentId": 1,
      "priorSpanRank": 7,
      "currentSpanRank": 11,
      "rawEdgeRank": 60,
      "bridgedEdgeRank": 69,
      "budgetRanks": [
        null,
        null,
        56,
        60
      ],
      "oracleCurrentSpanRank": 5
    },
    {
      "episode": "S12",
      "currentId": 1,
      "priorSpanRank": 29,
      "currentSpanRank": 2,
      "rawEdgeRank": 78,
      "bridgedEdgeRank": 79,
      "budgetRanks": [
        null,
        null,
        77,
        78
      ],
      "oracleCurrentSpanRank": 26
    },
    {
      "episode": "S13",
      "currentId": 1,
      "priorSpanRank": 3,
      "currentSpanRank": 2,
      "rawEdgeRank": 2,
      "bridgedEdgeRank": 2,
      "budgetRanks": [
        2,
        2,
        2,
        2
      ],
      "oracleCurrentSpanRank": 2
    }
  ],
  "controls": 13,
  "limits": [
    {
      "id": "L07",
      "mode": "bridge",
      "requested": 232208
    }
  ]
}
```

## 后续
把原始跨度候选与可学习的多角色/跨轮图特征相连，研究结构化部分监督、候选覆盖缺口与候选权威分离。以本轮结果定位语义信息缺口，避免反复扩大固定词面候选。先核查合法真实语言资料、独立留出及支持环境，设计完整版本的自主语言学习许可与评价要求；训练须另获授权。保留R50完整版本12项范围、v3.2方向，唯一交接由产品轨维护。未修改生产代码、启动训练、Codex、CI、PR合并、部署或新增费用，冻结协议不变。