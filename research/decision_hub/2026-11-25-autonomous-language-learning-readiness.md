# v3.2 自主认知专项第13轮（累计第72轮）：自主统计语义学习路线及真实仓库语料准备度审计

2026-11-25。RESEARCH_CANDIDATE / REPOSITORY_CORPUS_AUDIT_EXECUTED / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线 8e76feef52890f71ddd3128d0cc11d1820d82d47，13开放Draft PR，#61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e。核查最近8提交、完整未截断Git树相关路径、v3.2 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（前段及历史全文）、AGENTS 78cc1f8327ec50b5762103fedfaf1f06e85f7658、同步规程26c4d946e48f01858fb8e8c2cb06e4f7ba91bf05、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（相关标题，非全文）、第9轮27ba2f09121efdc4bf57f78a0039877d1bc86f92、第59轮445c19d01268bc4ec5e5d8b6a9eb1cfc237ab1b2、第50轮4d394d2cb6e1e1dfc667f2a8806f896a36bbdbef及第71轮既有结果。第59轮历史原生冷启动行动抽取TP6/FP6/FN9，约束原文覆盖代理1/10；不重跑、不外推为总体准确率。第50轮14门仍无本轮正式验收通过证据；12项完整范围仍保留，涉及Qwen的历史实现及验收条件按v3.2取消。未检索到的资产不代表全库不存在。

## 文献与路线（实际阅读范围：英文正式摘要及书目，未读PDF全文、未运行原作者代码、未下载外部语料、未核实数据训练许可）
1. Lafferty, McCallum & Pereira (2001), Conditional Random Fields, ICML pp.282–289，https://mlanthology.org/icml/2001/lafferty2001icml-conditional/ ：摘要介绍序列分段和标注概率框架。候选线性链CRF负责字符跨度/角色候选，复杂嵌套作用域另由语法处理；不将其概率解释为现实事实概率。
2. Zettlemoyer & Collins (2005), Learning to Map Sentences to Logical Form, arXiv作者存档2012 https://arxiv.org/abs/1207.1420 ：摘要从句子和逻辑式标注学习语法及对数线性结构模型。候选采用现有组合语义类型及可学习的局部词汇映射/解析排序；原论文任务不能直接证明中文生活决策有效。
3. Kim & Linzen (2020), COGS, https://aclanthology.org/2020.emnlp-main.731/ DOI 10.18653/v1/2020.emnlp-main.731：英语受限语义解析，作者报告同分布96–99%与组合泛化16–35%差异。仅作者摘要级结果，不是项目成绩；借鉴组合留出。
4. Li et al. (2023), SLOG, https://aclanthology.org/2023.emnlp-main.194/ DOI 10.18653/v1/2023.emnlp-main.194：摘要区分词汇与结构泛化，报告17种结构泛化测试、Transformer含预训练候选最高40.6%、结构感知解析器70.8%。仅作者报告的指定任务；不能与中文项目或不同任务横比。使用评测思想，不复制数据或权重。
5. Zettlemoyer & Collins (2009), Learning Context-Dependent Mappings from Sentences to Logical Form, https://aclanthology.org/P09-1110/ ，书目核对，正文/具体结果未审。作为跨轮语义后续阅读线索。
设计比较：A现有确定性规则作为基线和可核验降级；B字符/词特征的稀疏线性链CRF作候选提取，训练目标为条件对数似然减正则项，有限标签K、长度T的密集转移Viterbi及前向后向一般O(T K²)，特征计算另计；C带类型的加权组合语法/结构化排序，保留多个解析及未知，利用现有R61-71成果；D小型随机初始化神经编码器为后续竞争候选，训练/资源/覆盖未知。优先比较B+C与A，B/C不能直接授权确认、执行或填补事实；按实际数据和设备结果决定是否需要D。没有声称训练或性能已验证，没有现成第三方预训练权重。统计排名与硬约束语义证明分离；即使高分也需要独立义务覆盖和宿主确认。候选算法的采用、结构、特征、具体预算和训练均待所有者授权，不擅自设正式门槛。

## 实际语料资产与审计
实际通过GitHub连接器读取并解析两个固定JSON全文，校验返回blob身份：
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
均为ChatGPT研发辅助生成的项目原创公开合成开发材料；现有记录仅声明开发用途，不推定训练许可；未取得独立原始字节哈希、真人语料或外部训练授权。第9轮real_source_register.json 6a13d58897079dc181dc65a6c7e06b776abf9c91 所述NSW为历史非商业群体实验数据登记，非中文语言训练语料；未重新获取原始数据。两套语料schema分别为kind/field/span与role/quote/actor/time/modality/op等；不可直接合并标签或空字段当负例。单情节标注支持统计、字面跨度检查、精确/归一化/数字遮蔽重合、字符二元组Jaccard(>=.5为本轮启发式阈值，非语义去重证明)，以及留一情节与留一轮的字符1/2/3元组词表覆盖实际执行。每个文本内每种n元组计一次，分母是逐文本类型数之和，非全局词表大小、非模型预测准确率；跨语料覆盖亦非相同语义或独立来源。数字遮蔽先移除标点，仅用于审计，可能合并不同表达；不修改原文或用于计算。情节相似度不能排除跨语料隐性同源，未来须记录父情节及作者/生成方式，全部相关改写同组。仅数据描述统计，不训练、不生成参数权重、不调用现成AI推理服务、不从测试结果挑选超参数。4个结构控制。所有结果均为实际JS执行，同研究者定义指标，非独立验收。

## 下一完整版本的研发条件建议（研究规格，非启动授权）
保持前序12项完整范围及v3.2新目标，不能以小型语言候选替代产品闭环。优先建立统一带原文跨度、语义角色、对象/归属、时间、单位、边界、逻辑结构、条件、版本、证据及授权的IR，区分无标注与已核实负例；旧两套数据保留原版，用人工审计的派生映射而非覆盖。数据轨积累合法真实表达和独立组，独立轨冻结新语义组合、新结构、新领域、跨轮纠错、第三方主体/引述、未知和否定；公开开发集全部视为已见。按情节族、时间、来源及改写祖先分组；独立评价必须在训练/调参前隔离，不能仅靠随机按轮分割。对照A、B、C、B+C、后续D及普通AI（研发对照，无运行时依赖），同信息预算，逐层报告原文义务召回/精确、严重约束漏失和错误放行、完整IR/逻辑等价、覆盖与拒答、独立组风险、真实任务操作时间、内存、延迟和离线性能。每个新增分类必须具备多个真正独立来源情节，数据量据真实学习曲线及风险决定，不设虚构配额。若固定模型在n个独立同分布情节未发现定义好的严重错误，单侧95%二项上界1-0.05^(1/n)；仅示意独立样本量需求，当前32个公开开发情节不能套用，零错误也不证明普遍安全。未申请训练/重大版本开发、未选择最终架构、未启动Codex。实际支持环境、独立语料、合法训练许可及真实资源基线仍缺；后续在不训练前提下优先完成统一标注映射和候选解析接口可复算规格。零新增费用，无CI、合并、部署或生产修改，冻结协议不变。

## 实际复算
将固定两个JSON按上述顺序加载为docs，Node执行下列函数。无需网络或第三方包（已有原始JSON），只输出聚合统计，不复制语料正文。

```js
function audit(docs){
 const ck=(b,m)=>{if(!b)throw Error(m)},norm=s=>s.normalize("NFKC").replace(/\p{P}|\p{Z}|\s/gu,""),num=s=>norm(s).replace(/[0-9]+(?:[.][0-9]+)?/g,"#"),grams=(s,k)=>{const a=[...norm(s)];return new Set(a.slice(0,Math.max(0,a.length-k+1)).map((_,i)=>a.slice(i,i+k).join("")))},union=sets=>new Set(sets.flatMap(s=>[...s])),sim=(a,b)=>{let n=[...a].filter(x=>b.has(x)).length;return n/(a.size+b.size-n||1)},rows=[],out={datasets:[],pairAudit:{withinEpisode:0,acrossEpisode:0,exact:0,normalized:0,digitMasked:0,nearAcrossEpisode:0,nearCrossCorpus:0,maxAcross:0,maxCrossCorpus:0},coverage:[],controls:0};
 for(let d=0;d<docs.length;d++){
  let j=docs[d],labels=new Map(),dimensions={},turns=0,claims=0,spans=0,nonunique=0,missing=0;
  ck(new Set(j.cases.map(x=>x.id)).size===j.cases.length,"episode IDs");
  for(const c of j.cases){
   for(let t=0;t<c.turns.length;t++){
    let v=c.turns[t],a=d===0?v.claims:v.proposal.claims;turns++;claims+=a.length;
    rows.push({d,ep:c.id,turn:t+1,domain:c.domain,text:v.text,ng:grams(v.text,2)});
    for(const x of a){const k=d===0?x.kind:x.role,quote=d===0?x.span:x.quote;if(!labels.has(k))labels.set(k,{count:0,episodes:new Set()});let l=labels.get(k);l.count++;l.episodes.add(c.id);
     if(typeof quote!=="string"||!quote.length||!v.text.includes(quote))missing++;else{spans++;if(v.text.indexOf(quote)!==v.text.lastIndexOf(quote))nonunique++}
     for(const field of d===0?["field","op","unit","scope","ref"]:["actor","time","modality","op","ref","condition"]){dimensions[field]??={present:0,nonNull:0};if(Object.hasOwn(x,field)){dimensions[field].present++;if(x[field]!==null&&x[field]!==undefined)dimensions[field].nonNull++}}
    }
   }
  }
  let list=[...labels].map(([label,v])=>({label,count:v.count,episodes:v.episodes.size})).sort((a,b)=>a.episodes-b.episodes||a.label.localeCompare(b.label));
  out.datasets.push({id:d===0?"L":"S",episodes:j.cases.length,turns,claims,domains:new Set(j.cases.map(x=>x.domain)).size,labelTypes:list.length,labelsSingleEpisode:list.filter(x=>x.episodes===1).length,labelsAtMostTwoEpisodes:list.filter(x=>x.episodes<=2).length,spans,nonunique,missing,dimensions,labels:list,provenance:j.provenance,split:j.split});
 }
 for(let i=0;i<rows.length;i++)for(let j=i+1;j<rows.length;j++){
  let a=rows[i],b=rows[j],p=out.pairAudit,same=a.d===b.d&&a.ep===b.ep;
  if(same)p.withinEpisode++;else p.acrossEpisode++;
  if(a.text===b.text)p.exact++;if(norm(a.text)===norm(b.text))p.normalized++;if(num(a.text)===num(b.text))p.digitMasked++;
  if(!same){let s=sim(a.ng,b.ng);p.maxAcross=Math.max(p.maxAcross,s);if(s>=.5)p.nearAcrossEpisode++;if(a.d!==b.d){p.maxCrossCorpus=Math.max(p.maxCrossCorpus,s);if(s>=.5)p.nearCrossCorpus++}}
 }
 // Compare the vocabulary inventory accessible outside the held-out episode to
 // the artificially easier inventory that includes its companion turn. No fitting or prediction.
 for(let k of [1,2,3]){
  let r={n:k,types:0,groupSeen:0,turnSeen:0,rowsWithUnseenGroup:0,rowsWithCompanionGain:0,crossCorpusTypes:0,crossCorpusSeen:0};
  for(const a of rows){let own=grams(a.text,k),outside=union(rows.filter(b=>!(a.d===b.d&&a.ep===b.ep)).map(b=>grams(b.text,k))),otherTurns=union(rows.filter(b=>a!==b).map(b=>grams(b.text,k))),otherCorpus=union(rows.filter(b=>a.d!==b.d).map(b=>grams(b.text,k)));let g=[...own].filter(x=>outside.has(x)).length,t=[...own].filter(x=>otherTurns.has(x)).length;ck(g<=t,"coverage nesting");r.types+=own.size;r.groupSeen+=g;r.turnSeen+=t;r.rowsWithUnseenGroup+=g<own.size;r.rowsWithCompanionGain+=t>g;r.crossCorpusTypes+=own.size;r.crossCorpusSeen+=[...own].filter(x=>otherCorpus.has(x)).length}
  out.coverage.push(r);
 }
 // Hypothetical zero-event upper bound only if independently sampled and fixed risk definition.
 out.zeroErrorIllustration=[32,100,300,1000].map(n=>({n,upper:1-Math.pow(.05,1/n)}));
 ck(norm("每月 3，000 元。")==="每月3000元","normalize");out.controls++;
 ck(grams("甲乙甲",2).size===2,"bigrams");out.controls++;
 ck(sim(new Set(["a","b"]),new Set(["b","c"]))===1/3,"Jaccard");out.controls++;
 ck(out.pairAudit.withinEpisode+out.pairAudit.acrossEpisode===rows.length*(rows.length-1)/2,"pairs");out.controls++;
 return out;
}
```

```json
{
  "datasets": [
    {
      "id": "L",
      "episodes": 18,
      "turns": 36,
      "claims": 98,
      "domains": 15,
      "labelTypes": 34,
      "labelsSingleEpisode": 19,
      "labelsAtMostTwoEpisodes": 24,
      "spans": 98,
      "nonunique": 0,
      "missing": 0,
      "dimensions": {
        "field": {
          "present": 98,
          "nonNull": 98
        },
        "op": {
          "present": 10,
          "nonNull": 10
        },
        "unit": {
          "present": 22,
          "nonNull": 22
        },
        "scope": {
          "present": 3,
          "nonNull": 3
        },
        "ref": {
          "present": 0,
          "nonNull": 0
        }
      },
      "labels": [
        {
          "label": "ACTION",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "AUTHORIZATION_PROPOSAL",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "CONDITIONAL_ACTION",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "CONFIRMED_CHOICE",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "COUNTERFACTUAL_CLAIM",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "EVENT_DEFINITION",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "EXCEPTION",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "EXCLUSION",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "FUTURE_COST",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "OBSERVED_OUTCOME",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "PAST_COST",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "POSTHOC",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "RECORD_INTENT",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "REPORTED_EXTERNAL",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "REPORTED_POSSIBILITY",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "REPORTED_UNVERIFIED",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "RETROSPECTIVE_ESTIMATE",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "TRIGGER",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "UNAVAILABLE_EVIDENCE",
          "count": 1,
          "episodes": 1
        },
        {
          "label": "CONDITIONAL_HARD",
          "count": 2,
          "episodes": 2
        },
        {
          "label": "HARD_CONSEQUENCE",
          "count": 2,
          "episodes": 2
        },
        {
          "label": "REPORTED_ESTIMATE",
          "count": 2,
          "episodes": 2
        },
        {
          "label": "REPORTED_PROMISE",
          "count": 2,
          "episodes": 2
        },
        {
          "label": "REPORTED_UNCERTAIN",
          "count": 3,
          "episodes": 2
        },
        {
          "label": "ESTIMATE",
          "count": 3,
          "episodes": 3
        },
        {
          "label": "GOAL",
          "count": 4,
          "episodes": 3
        },
        {
          "label": "HYPOTHESIS",
          "count": 3,
          "episodes": 3
        },
        {
          "label": "PROPOSED_ACTION",
          "count": 3,
          "episodes": 3
        },
        {
          "label": "REVISION",
          "count": 3,
          "episodes": 3
        },
        {
          "label": "CONFIRM",
          "count": 5,
          "episodes": 5
        },
        {
          "label": "PREFERENCE",
          "count": 8,
          "episodes": 6
        },
        {
          "label": "UNKNOWN",
          "count": 7,
          "episodes": 7
        },
        {
          "label": "HARD",
          "count": 13,
          "episodes": 8
        },
        {
          "label": "USER_REPORTED",
          "count": 19,
          "episodes": 12
        }
      ],
      "provenance": "ORIGINAL_SYNTHETIC_DEVELOPMENT_ONLY",
      "split": "ALL_PUBLIC_DEVELOPMENT; group by episode ID; never call holdout"
    },
    {
      "id": "S",
      "episodes": 14,
      "turns": 28,
      "claims": 69,
      "domains": 14,
      "labelTypes": 9,
      "labelsSingleEpisode": 3,
      "labelsAtMostTwoEpisodes": 4,
      "spans": 69,
      "nonunique": 0,
      "missing": 0,
      "dimensions": {
        "actor": {
          "present": 69,
          "nonNull": 69
        },
        "time": {
          "present": 69,
          "nonNull": 69
        },
        "modality": {
          "present": 69,
          "nonNull": 69
        },
        "op": {
          "present": 69,
          "nonNull": 69
        },
        "ref": {
          "present": 69,
          "nonNull": 9
        },
        "condition": {
          "present": 69,
          "nonNull": 4
        }
      },
      "labels": [
        {
          "label": "estimate",
          "count": 2,
          "episodes": 1
        },
        {
          "label": "observation",
          "count": 2,
          "episodes": 1
        },
        {
          "label": "permission_intent",
          "count": 5,
          "episodes": 1
        },
        {
          "label": "fact",
          "count": 3,
          "episodes": 2
        },
        {
          "label": "criterion",
          "count": 5,
          "episodes": 3
        },
        {
          "label": "goal",
          "count": 7,
          "episodes": 6
        },
        {
          "label": "constraint",
          "count": 10,
          "episodes": 7
        },
        {
          "label": "unknown",
          "count": 10,
          "episodes": 8
        },
        {
          "label": "action",
          "count": 25,
          "episodes": 11
        }
      ],
      "provenance": "ORIGINAL_SYNTHETIC_PUBLIC_DEVELOPMENT_ONLY",
      "split": "GROUP_BY_EPISODE; all turns and paraphrases stay together; no independent holdout"
    }
  ],
  "pairAudit": {
    "withinEpisode": 32,
    "acrossEpisode": 1984,
    "exact": 0,
    "normalized": 0,
    "digitMasked": 0,
    "nearAcrossEpisode": 0,
    "nearCrossCorpus": 0,
    "maxAcross": 0.1935483870967742,
    "maxCrossCorpus": 0.1935483870967742
  },
  "coverage": [
    {
      "n": 1,
      "types": 1428,
      "groupSeen": 1191,
      "turnSeen": 1237,
      "rowsWithUnseenGroup": 58,
      "rowsWithCompanionGain": 24,
      "crossCorpusTypes": 1428,
      "crossCorpusSeen": 1029
    },
    {
      "n": 2,
      "types": 1491,
      "groupSeen": 355,
      "turnSeen": 417,
      "rowsWithUnseenGroup": 64,
      "rowsWithCompanionGain": 36,
      "crossCorpusTypes": 1491,
      "crossCorpusSeen": 231
    },
    {
      "n": 3,
      "types": 1449,
      "groupSeen": 54,
      "turnSeen": 82,
      "rowsWithUnseenGroup": 64,
      "rowsWithCompanionGain": 18,
      "crossCorpusTypes": 1449,
      "crossCorpusSeen": 33
    }
  ],
  "controls": 4,
  "zeroErrorIllustration": [
    {
      "n": 32,
      "upper": 0.0893681989862648
    },
    {
      "n": 100,
      "upper": 0.029513049607039932
    },
    {
      "n": 300,
      "upper": 0.00993608194445772
    },
    {
      "n": 1000,
      "upper": 0.0029912495450953314
    }
  ]
}
```
