# 自主认知：原子组等价压缩、有界联合求解及原文集体表达锚定诊断
2026-11-27。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / RECOMBINED_PUBLIC_DEVELOPMENT / CONNECTOR_JS_EXECUTED / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。

## 基线和去重
起点及写前main e21f68bad4ffeff7d3449f771003a7022d396ee5。核对20次近期提交、15项开放PR、v3.2全文、同步规程（blob 26c4d946e48f01858fb8e8c2cb06e4f7ba91bf05）、唯一产品交接前20行、前序多容量及原子组报告、相关联合修订和原文多修订报告。PR #63 head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft，未重跑。前轮已实现容量、SCC残余支持、原子组独立分支。本轮新增相同目标边指标等价类压缩、单调传播、有界求解及受控原文集体表达类型和身份锚。未完成全库查重，不声明算法首创。实际本地解压上一轮ZIP，其SHA256 a188184f5bafa2f097e9c67be98d0a1330a2782c3bce98481866be02df2c5533 与原报告一致；study.py b9f68c76b2f82142e0e56adcb0888ceb3ee39fce243186986aa318e22532e2ee，bundles.py 4313b58a3e14baf838de11b9cc01b67fa7134b4b15ccbed51cc242cde391d33f。实际调用固定study.py的solve；未import带主循环的bundles.py。

## A 等价压缩和传播
固定已资格化义务组、候选边、非负整数容量。边指标X_ij=1当义务i选择见证j。原子组(members,j)要求其全部X_ij相等。并查集将共享同一个边指标的组进行传递闭包：所有原约束等价于每个连接分量内的指标相等，不能因为共享义务i但目标j不同就合并指标。传播规则：任一指标因边缺失为假则整个分量假；若任一义务只有该目标可选则整个分量真；真假冲突或空候选行立即排除。对于某右节点，当前单选行数若超过容量立即排除，等于容量时可移除其他行的该目标。每次传播只删除候选边，故有限终止，且不会排除合法世界。对尚未定值分量枚举真和假，两个分支互斥且穷尽其合法取值；分量都确定时调用固定残余匹配求全部支持。对全部可行叶的支持取并，等于完整有限域内支持。此证明仅涵盖给定数学合同，不涵盖真实语言资格。原分支上界2^k，压缩上界2^c（c为不同等价分量数且c<=k）；传播可进一步减少。最坏仍指数。重复扫描、复制候选行、求解器排序和预算未覆盖的开销存在；节点预算并非时间或内存限制。当前不返回世界级证书、原子组分支身份、真实授权或续算票据。边际支持不能独立重组。搜索被截断或候选覆盖不全时不返回强制边或确定冲突；未资格化合同返回UNQUALIFIED。所有结果仅研究，无写权限。

## B 实际执行
Python 3.13.5，原创合成结构。四类4×3全部二值边图、容量[2,2,2]，加固定seed 20261127的1000个随机图（3至7根、2至4见证、0至8组，容量0至n、边生成概率0.7仅为实验设计）。每图直接枚举所有候选赋值，检查容量和组谓词；与压缩算法可行性、边支持、强制边逐项比较。四种节点预算0、1、3、9，每种检查完成结果精确、截断仅正支持且无强制；另每图检查候选覆盖未知。参照为同一研究者独立代码路径，非独立科学验收。
| 类别 | 配置 | 可行 | 原始分支理论调用 | 实际节点 | 实际匹配调用 | 截断预算试次 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 同目标链 | 4096 | 1008 | 32768 | 4258 | 1008 | 4177 |
| 跨目标重叠 | 4096 | 976 | 32768 | 4966 | 1088 | 4525 |
| 重复三角 | 4096 | 1304 | 65536 | 4474 | 1304 | 4285 |
| 混合 | 4096 | 616 | 65536 | 4450 | 640 | 4273 |
| 随机 | 1000 | 293 | 57369 | 1290 | 340 | 1141 |
| 合计 | 17384 | 4197 | 253977 | 19438 | 4380 | 18401 |
全部主要配置与直接参照一致；69536个预算控制试次；12项专项控制通过，另6个规模控制均与直接赋值参照一致。匹配调用较旧逐原始布尔分支理论调用减少约98.28%，不是实测整体时延或内存改善。实际8义务、2见证、容量均8的规模控制中，4/8/16/32/64/128条循环重复或传递重叠组均压缩成1个分量、3节点、2次匹配；128组原理论2^128分支未实际运行，不能说实际完成2^128次。普通及-O结果逐字节相同，使用显式check抛错。源码和回执SHA256：
compress.py d353a2ed09d56e457ce6ca4d04cd1b04081c9b7496c8aa44a4356702b393cd92
result.json/result_opt.json 99aee73712331f67e9c1aa2cd0e6b14034de5e49c35db40af0957072e5318032
完整Python源码及两份结果随当轮聊天ZIP；GitHub报告不冒称包含ZIP字节。复算 python compress.py result.json；python -O compress.py result_opt.json；cmp result.json result_opt.json。

## C 集体表达原文审计及受控锚定
固定原始公开合成开发资产（非自然语料、非独立留出）：
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
实际完整读取两个JSON，连接器报告blob身份，未独立复算原始Git字节。32情节64轮；固定词表扫描发现16轮。人工逐轮分类见下方audits（仅审计命中项的主要含义，不是全面标注，不计算自然语料召回率）。包括L02.1一次都不能有（标量否定）、L06.0八次都没坏（重复观察）、L07.0平均（子串干扰）、L12.0两项加起来（合计）、L12.1两个都必须（分配确认）、S02.0任何一套都（跨方案约束）、S04.0我们两个人都（多主体）、S14.1两种方式都先留着（保留候选）；L01.0房租加停车属于未命中合计反例。不能据词项直接授予多根修订或共同见证资格。

受控实验把110条已有首轮标注的原文片段作为模拟历史记录，按情节隔离，不是已确认真实账本；同情节内枚举142个不同记录无序对（生成时固定顺序），分别构造七种人工明示引号、连接词和后缀模板（分配、合计、排他、保留、不确定、转述、条件），总994。解析器仅做Unicode标量引号锚、精确文本及唯一身份匹配、引号外完整前后缀查表；不是开放解析器，不校验量纲、角色、属性适用性，有些合成句故意不自然，尤其将任意两条记录按月计算只是结构探针。生成和解析共享模板，结果是合同往返而非泛化评估。994条锚及候选类型均一致；包含“都”的720条若机械赋予分配类型，578条与模板类型不同（基线扫描完整句，包括引号内文字）。每对另测试重复历史身份、缺失历史锚、未知转述包装三种，分别142/142返回UNKNOWN，总426项。无真实权限、训练、完整原生入口、语义正确性或实际提问测量；ANCHORED_CANDIDATE仅结构候选，不能自动转换为数学组。两次执行上述统计一致。以下为本次第二次实际执行函数；输入固定两JSON解析所得数组。

```js
function run(corpora){
 const cues=/都|均|各|分别|一起|同时|两项|两个|两种|两套|两家|两个人|合计|加起来|共同|全部|所有/g;
 const audits={"L02.1":"scalar_negation","L05.0":"distributed_plan","L05.1":"possible_distributed_demand","L06.0":"repeated_events","L07.0":"lexical_substring","L08.0":"alternative_emotions","L12.0":"aggregate_cap","L12.1":"distributed_confirmation","L15.0":"goal_list","L17.0":"event_count","S01.0":"option_list","S02.0":"distributed_constraint","S04.0":"multiple_actors","S04.1":"quantity","S07.0":"criteria_list","S14.1":"retain_options"};
 const inc=(o,k,n=1)=>o[k]=(o[k]||0)+n;
 const check=(v,msg)=>{if(!v)throw Error(msg)};
 const frames=[
  ["","都按月计算。","DISTRIBUTIVE"],
  ["","合计不超过一千元。","AGGREGATE"],
  ["","只能选一个。","EXCLUSIVE"],
  ["","都先保留。","RETAIN"],
  ["","不一定都按月计算。","UNCERTAIN"],
  ["他说，","都按月计算。","REPORTED"],
  ["如果获准，","都按月计算。","CONDITIONAL"]
 ];
 function parse(text,history){
  const ch=Array.from(text), spans=[];let s=-1;
  for(let i=0;i<ch.length;i++){
    if(ch[i]==="「"){if(s>=0)return {status:"UNKNOWN",authority:"NONE"};s=i;}
    if(ch[i]==="」"){if(s<0)return {status:"UNKNOWN",authority:"NONE"};spans.push({start:s+1,end:i,raw:ch.slice(s+1,i).join("")});s=-1;}
  }
  if(s>=0||spans.length!==2)return {status:"UNKNOWN",authority:"NONE"};
  const [x,y]=spans;
  if(ch.slice(x.end+1,y.start-1).join("")!=="和")return {status:"UNKNOWN",authority:"NONE"};
  const p=ch.slice(0,x.start-1).join(""),q=ch.slice(y.end+1).join("");
  const f=frames.find(z=>z[0]===p&&z[1]===q);
  const matches=spans.map(z=>history.filter(h=>h.raw===z.raw).map(h=>h.id));
  return {status:f&&matches.every(m=>m.length===1)&&matches[0][0]!==matches[1][0]?"ANCHORED_CANDIDATE":"UNKNOWN",kind:f?.[2]??null,spans,matches,authority:"NONE"};
 }
 let out={episodes:0,turns:0,cue_turns:0,marker_categories:{},history_records:0,eligible_pairs:0,skipped_pairs:0,frame_cases:0,exact_candidate:0,naive_du_cases:0,naive_du_wrong_distributive:0,duplicate_ambiguity:0,missing_anchor:0,unknown_wrapper:0,by_kind:{},unmarked_aggregate_examples:[]};
 for(const corpus of corpora)for(const ep of corpus.cases){
  out.episodes++;
  ep.turns.forEach((t,i)=>{
   out.turns++;const id=ep.id+"."+i;
   const found=[...t.text.matchAll(cues)];
   if(found.length){out.cue_turns++;check(audits[id],"unreviewed cue turn "+id);inc(out.marker_categories,audits[id]);}
   if(!found.length&&id==="L01.0")out.unmarked_aggregate_examples.push({id,text:t.text});
  });
  const t=ep.turns[0];const hist=(t.claims??t.proposal.claims).map((c,i)=>({raw:c.span??c.quote,id:ep.id+":"+i}));out.history_records+=hist.length;
  for(let i=0;i<hist.length;i++)for(let j=i+1;j<hist.length;j++){
   const x=hist[i],y=hist[j];
   if([x,y].some(z=>!z.raw||/[「」]/.test(z.raw)||hist.filter(h=>h.raw===z.raw).length!==1||!t.text.includes(z.raw))){out.skipped_pairs++;continue;}
   out.eligible_pairs++;
   for(const [pre,post,kind] of frames){
    const raw=pre+"「"+x.raw+"」和「"+y.raw+"」"+post;
    const p=parse(raw,hist);out.frame_cases++;inc(out.by_kind,kind);
    check(p.status==="ANCHORED_CANDIDATE"&&p.kind===kind&&p.matches[0][0]===x.id&&p.matches[1][0]===y.id&&p.authority==="NONE","frame roundtrip");
    for(const z of p.spans)check(Array.from(raw).slice(z.start,z.end).join("")===z.raw,"anchor");
    out.exact_candidate++;
    if(raw.includes("都")){out.naive_du_cases++;out.naive_du_wrong_distributive+=kind!=="DISTRIBUTIVE";}
   }
   const raw="「"+x.raw+"」和「"+y.raw+"」都按月计算。";
   check(parse(raw,[...hist,{raw:x.raw,id:"duplicate:"+x.id}]).status==="UNKNOWN","ambiguous identity");out.duplicate_ambiguity++;
   check(parse(raw,hist.filter(h=>h.id!==x.id)).status==="UNKNOWN","missing identity");out.missing_anchor++;
   check(parse("听别人讲："+raw,hist).status==="UNKNOWN","unknown scope");out.unknown_wrapper++;
  }
 }
 return out;
}
```

执行结果：
```json
{
  "episodes": 32,
  "turns": 64,
  "cue_turns": 16,
  "marker_categories": {
    "scalar_negation": 1,
    "distributed_plan": 1,
    "possible_distributed_demand": 1,
    "repeated_events": 1,
    "lexical_substring": 1,
    "alternative_emotions": 1,
    "aggregate_cap": 1,
    "distributed_confirmation": 1,
    "goal_list": 1,
    "event_count": 1,
    "option_list": 1,
    "distributed_constraint": 1,
    "multiple_actors": 1,
    "quantity": 1,
    "criteria_list": 1,
    "retain_options": 1
  },
  "history_records": 110,
  "eligible_pairs": 142,
  "skipped_pairs": 0,
  "frame_cases": 994,
  "exact_candidate": 994,
  "naive_du_cases": 720,
  "naive_du_wrong_distributive": 578,
  "duplicate_ambiguity": 142,
  "missing_anchor": 142,
  "unknown_wrapper": 142,
  "by_kind": {
    "DISTRIBUTIVE": 142,
    "AGGREGATE": 142,
    "EXCLUSIVE": 142,
    "RETAIN": 142,
    "UNCERTAIN": 142,
    "REPORTED": 142,
    "CONDITIONAL": 142
  },
  "unmarked_aggregate_examples": [
    {
      "id": "L01.0",
      "text": "我和室友合租，房租加停车每月最多四千，水电另算。房租三千六，车位得问房东。"
    }
  ]
}
```

## D 下一阶段与边界
本轮自行选定等价分量、传播、预算、图族、受控模板、人工分类和比较基线；未授权为产品标准。应进一步独立验证自然原文中共同指代、未明示范围、跨主体、量纲和条件的候选发现，不能把精确引号模板当作白话理解；明确来源及真正组关系后才接入压缩算法。输出保留原文身份、资格/覆盖状态及组约束，未来完整世界或可核验分支证书另研。真实用户、独立留出、完整v0.8入口、竞品、设备性能、并发写入、撤回均未执行。未修改生产、训练、合并PR、部署、主动CI或增加费用；冻结协议、历史证据等级、唯一交接不变。
