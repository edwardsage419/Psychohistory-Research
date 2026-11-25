# 自主认知专项累计第80轮候选：引用排序的字序、数值归一与局部上下文消融

2026-11-25。RESEARCH_CANDIDATE / FIXED_FEATURE_ABLATION_EXECUTED / NO_TRAINING / INDEPENDENT_ACCEPTANCE_NOT_RUN。main b8d7cf5d5926b6d1b41b2a52b4e0a77ed9485512。核查近15提交、13开放PR（#61待审）、v3.2首8行及此前全文、唯一交接首15行（blob 5e74f4f0b37141d631740e844ad8bbbfed232e07），复用前轮R77及精确Top-K研究，不重复候选加速。输入两固定完整JSON：research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb；research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132。公开原创合成开发情节32、已标引用12；非真人、独立留出，训练授权未获。研究者在看到12条既有正例后选定特征及权重，属于已见集探索；没有拟合或权重更新、没有验证集模型选择，禁止将任何最佳变体作为已证实泛化。

## 研究问题与方法
R77字符集合重合忽略字序、数量变化、局部名词先行项。保持普通跨度候选全集及原评分，比较四种固定增量：字符二元组Jaccard乘4、有限单位前数值归一后的二元组Jaccard乘4、跨度左右最多8个非标点字符的归一化上下文二元组Jaccard乘4、三特征各乘2。权重、窗口、单位集合由研究者选择，不是语言语法或权威证据。数字归一只用于候选排序，原值不修改；不能识别全部中文数词、币种、时间、指代或否定，保留精确原文。排序按分数和原位置；标签仅用于生成候选后评估。32情节枚举全部544737对；有正例的情节才执行各变体排序；其余没有明确负例，不能计算误报、准确率、校准或全体任务成功率。MRR在12已标正例上平均倒数排名；同一数据的多变体结果相关。无真实运行性能、无模型训练、无权限提升。前轮精确剪枝证书仅适用于原评分；新评分未验证其剪枝，不能沿用旧上界。归一实现是有限启发式，clean先去标点会使小数点等信息丢失；禁止将归一文本用于数学或事实投影。

## 可复算程序
按L/S顺序传入两完整JSON，标准JS执行。
```js
function experiment(docs){
 const ck=(b,m)=>{if(!b)throw Error(m)},punct=/[，。！？；、：,.!?;:\s]/u,connect=["或者","还是","但是","如果","而且","以及","然后","并且","就","且","和","或","再"],revision=["改","撤","取消","替换","不再","重新","刚核实","实际是","暂时不","仅用于","不作为","纠正","更新"];
 const clean=s=>s.replace(/[，。！？；、：,.!?;:\s]/gu,"");
 // Digit runs only when bounded by common units; avoid turning 一项/一个 into a measurement by default.
 const norm=s=>clean(s).replace(/[0-9０-９]+(?:[.．][0-9０-９]+)?(?=元|分钟|小时|天|周|月|年|成|%|％|公里|米|块)/gu,"#").replace(/[零〇一二两三四五六七八九十百千万亿半]+(?=元|分钟|小时|天|周|月|年|成|公里|米|块)/gu,"#");
 const chars=s=>new Set([...s]),grams=s=>new Set([...s].slice(0,-1).map((x,i)=>x+[...s][i+1]));
 const jac=(a,b)=>{let n=0;for(const x of a)if(b.has(x))n++;return n/(a.size+b.size-n||1)};
 function spans(s){
  if(!s.length||s.length>128)throw Error("length");
  let out=[];
  for(let i=0;i<s.length;i++)if(!punct.test(s[i]))for(let j=i+1;j<=Math.min(s.length,i+24);j++){
   let x=s.slice(i,j);if(punct.test(x))break;
   let left=i===0||punct.test(s[i-1])||connect.some(v=>s.slice(0,i).endsWith(v)),right=j===s.length||punct.test(s[j])||connect.some(v=>s.startsWith(v,j));
   let l=i;while(l>0&&!punct.test(s[l-1])&&i-l<8)l--;let h=j;while(h<s.length&&!punct.test(s[h])&&h-j<8)h++;
   // Only local flanks; never use future turns or annotations.
   out.push({start:i,end:j,score:3*(+left+ +right)-Math.abs(x.length-8)/4,cue:revision.some(v=>x.includes(v)),c:chars(x),g:grams(x),ng:grams(norm(x)),ctx:grams(norm(s.slice(l,h)))})
  }
  return out;
 }
 const configs=["base","bigram","normalized","context","joint"];
 const sc=(a,b)=>{let s=a.score+b.score+4*jac(a.c,b.c)+2*Number(b.cue),g=jac(a.g,b.g),n=jac(a.ng,b.ng),c=jac(a.ctx,b.ctx);return [s,s+4*g,s+4*n,s+4*c,s+2*g+2*n+2*c]};
 const key=(a,b)=>[a.start,a.end,b.start,b.end].join(":");
 const cmp=(x,y)=>y.s-x.s||x.a.start-y.a.start||x.a.end-y.a.end||x.b.start-y.b.start||x.b.end-y.b.end;
 const out={episodes:0,positiveEdges:0,edges:0,controls:0,results:Object.fromEntries(configs.map(k=>[k,{top1:0,top5:0,top20:0,top100:0,mrr:0,improved:0,worse:0,tied:0}])),records:[]};
 for(let d=0;d<docs.length;d++)for(const e of docs[d].cases){
  let [t0,t1]=e.turns,a=spans(t0.text),b=spans(t1.text),rows=[],targets=[],aa=d===0?t0.claims:t0.proposal.claims,bb=d===0?t1.claims:t1.proposal.claims;out.episodes++;
  for(let u of a)for(let v of b)rows.push({a:u,b:v,ss:sc(u,v),key:key(u,v)});
  out.edges+=rows.length;
  function loc(s,q){let i=s.indexOf(q);ck(i>=0&&i===s.lastIndexOf(q),"anchor");return [i,i+q.length]}
  for(let c of bb){let ref=d===0?c.supersedes:c.ref;if(typeof ref!=="string")continue;let p=d===0?aa.find(x=>x.field===ref.split(":").at(-1)):aa[Number(ref.split(".").at(-1))-1];ck(!!p,"prior");targets.push([...loc(t0.text,d===0?p.span:p.quote),...loc(t1.text,d===0?c.span:c.quote)].join(":"))}
  if(!targets.length)continue;
  let recs=targets.map(k=>({id:e.id,key:k,ranks:{}}));
  for(let i=0;i<configs.length;i++){let cfg=configs[i];for(let row of rows)row.s=row.ss[i];rows.sort(cmp);for(let rec of recs){let rank=rows.findIndex(x=>x.key===rec.key)+1;ck(rank>0,"candidate missing");rec.ranks[cfg]=rank;let m=out.results[cfg];for(let n of [1,5,20,100])m["top"+n]+=+(rank<=n);m.mrr+=1/rank;let base=rec.ranks.base;m.improved+=+(rank<base);m.worse+=+(rank>base);m.tied+=+(rank===base)}}
  out.positiveEdges+=targets.length;out.records.push(...recs)
 }
 for(let m of Object.values(out.results))m.mrr/=out.positiveEdges;
 for(let test of [()=>norm("十二分钟")==="#分钟",()=>norm("一个目标")==="一个目标",()=>norm("三天")==="#天",()=>grams("甲乙丙").size===2,()=>jac(grams("甲乙"),grams("乙甲"))===0,()=>out.episodes===32,()=>out.positiveEdges===12,()=>out.edges===544737,()=>out.results.base.top1===3&&out.results.base.top5===6&&out.results.base.top20===6&&out.results.base.top100===10,()=>Object.values(out.results).every(m=>m.improved+m.worse+m.tied===12),()=>Object.values(out.results).every(m=>m.top1<=m.top5&&m.top5<=m.top20&&m.top20<=m.top100)]){ck(test(),"control");out.controls++}
 return out;
}
```

## 实测
```json
{
  "episodes": 32,
  "positiveEdges": 12,
  "edges": 544737,
  "controls": 11,
  "results": {
    "base": {
      "top1": 3,
      "top5": 6,
      "top20": 6,
      "top100": 10,
      "mrr": 0.37189364527171564,
      "improved": 0,
      "worse": 0,
      "tied": 12
    },
    "bigram": {
      "top1": 4,
      "top5": 6,
      "top20": 7,
      "top100": 10,
      "mrr": 0.4302576169285979,
      "improved": 4,
      "worse": 3,
      "tied": 5
    },
    "normalized": {
      "top1": 4,
      "top5": 6,
      "top20": 7,
      "top100": 10,
      "mrr": 0.4302576169285979,
      "improved": 4,
      "worse": 3,
      "tied": 5
    },
    "context": {
      "top1": 3,
      "top5": 6,
      "top20": 8,
      "top100": 10,
      "mrr": 0.3743771588673163,
      "improved": 3,
      "worse": 2,
      "tied": 7
    },
    "joint": {
      "top1": 4,
      "top5": 6,
      "top20": 7,
      "top100": 10,
      "mrr": 0.43115287490287485,
      "improved": 5,
      "worse": 2,
      "tied": 5
    }
  },
  "records": [
    {
      "id": "L03",
      "key": "11:15:3:10",
      "ranks": {
        "base": 567,
        "bigram": 581,
        "normalized": 581,
        "context": 601,
        "joint": 600
      }
    },
    {
      "id": "L08",
      "key": "12:23:15:22",
      "ranks": {
        "base": 23,
        "bigram": 26,
        "normalized": 26,
        "context": 19,
        "joint": 22
      }
    },
    {
      "id": "L15",
      "key": "10:12:0:6",
      "ranks": {
        "base": 142,
        "bigram": 146,
        "normalized": 146,
        "context": 146,
        "joint": 150
      }
    },
    {
      "id": "S01",
      "key": "18:23:0:10",
      "ranks": {
        "base": 2,
        "bigram": 1,
        "normalized": 1,
        "context": 2,
        "joint": 1
      }
    },
    {
      "id": "S02",
      "key": "16:29:0:10",
      "ranks": {
        "base": 21,
        "bigram": 13,
        "normalized": 13,
        "context": 16,
        "joint": 13
      }
    },
    {
      "id": "S03",
      "key": "20:26:9:16",
      "ranks": {
        "base": 3,
        "bigram": 2,
        "normalized": 2,
        "context": 3,
        "joint": 2
      }
    },
    {
      "id": "S04",
      "key": "24:33:0:10",
      "ranks": {
        "base": 1,
        "bigram": 1,
        "normalized": 1,
        "context": 1,
        "joint": 1
      }
    },
    {
      "id": "S08",
      "key": "11:18:7:14",
      "ranks": {
        "base": 1,
        "bigram": 1,
        "normalized": 1,
        "context": 1,
        "joint": 1
      }
    },
    {
      "id": "S10",
      "key": "12:20:15:23",
      "ranks": {
        "base": 1,
        "bigram": 1,
        "normalized": 1,
        "context": 1,
        "joint": 1
      }
    },
    {
      "id": "S11",
      "key": "2:8:1:10",
      "ranks": {
        "base": 60,
        "bigram": 38,
        "normalized": 38,
        "context": 44,
        "joint": 33
      }
    },
    {
      "id": "S12",
      "key": "4:8:0:7",
      "ranks": {
        "base": 78,
        "bigram": 78,
        "normalized": 78,
        "context": 78,
        "joint": 78
      }
    },
    {
      "id": "S13",
      "key": "16:26:0:13",
      "ranks": {
        "base": 2,
        "bigram": 2,
        "normalized": 2,
        "context": 2,
        "joint": 2
      }
    }
  ]
}
```

## 边界与下游
无正例标签的节点维持未知；各候选只供研究排序，不产生更正授权。必须用独立真实语言及明确负例验证增量，按情节隔离；未获训练授权不训练。数据轨负责合法语料，独立轨负责未见评价，产品轨维护唯一交接；手动窗口继续研究组合语义与可学习特征，候选先保留不自动准入。无生产代码、Codex、CI、PR合并、部署、费用或冻结协议变更。
