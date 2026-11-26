# 自主认知：原文修订候选与已确认历史记录的联合排序
2026-11-26。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / PUBLIC_SYNTHETIC_DEVELOPMENT / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线和范围
起始及写前main 320e07f28e664c73b10b91f6adec6510aa965862，读取18次近期提交、15开放Draft PR、v3.2、同步规程、唯一交接前20行（固定blob 5e74f4f0b37141d631740e844ad8bbbfed232e07）。#63 head 734686980b19da9291bdd08b67d4e2519c011acf，未重跑。前序原文引用搜索R77（固定blob见下）完全从双轮原文枚举边，R76已在给定原文角色/字段节点时测试；本轮实际复用最新开放角色候选并假定历史首轮已由宿主确认，比较当前原文修订跨度与历史根的联合排名、上下文扩展及相同跨度预算下的目标排序。前两轮联合搜索与未完成决策证明是有限人工结构，本轮回到已有真实仓库原文（人工合成），不重复数学实验，不声称全库无重复。未将已确认历史夹具等同于真实记录或授权。
## 固定资产
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-25-raw-text-reference-search.md 16075b3ba567ee6dc3496300beab1417172a6c42
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
research/decision_hub/2026-11-25-temporal-quantity-candidate-separation.md 8a6b42f83b80283db6e215fe48f4fb2efbf8368c
research/decision_hub/2026-11-26-compositional-role-candidate-recovery.md b0bea7b4c101c170be2aaa2355973739b125e0b7
research/decision_hub/2026-11-26-clock-event-and-open-role-projection.md ef103587b216ad07c1a47102ddb7cb8d2975283d
全部读取连接器blob身份匹配，未重算Git原始字节。两套32情节64轮原语料为项目ChatGPT研发辅助原创合成公开开发材料，12显式引用标注为评价目标；无独立留出、真人或训练。当前算法只输入第二轮原文及首轮人工标注的原文跨度与记录根作为已确认历史夹具，未使用当前标注、领域、字段或正确引用生成候选。历史kind保留但不参与排序。仅固定已审阅项目自有JS加载，生产禁止执行外部文档。开发数据及旧规则均已见，不能称盲测。此次根据既有研究选择局部/同强句相似度和权重，未拟合。
## 方法
复用clock-event-and-open-role-projection的propose输出all.revision完整池；每个当前跨度与所有历史根组合。字符集合Jaccard和相邻双字符集合Jaccard相加为sim，过滤标点/空白；local=c.score+4*sim(当前跨度,旧原文)；context=local+2*sim(包含当前跨度的强句上下文,旧原文)。上下文从之前最近强句标点至之后最近强句标点；若候选自身跨强句则可能包含多句，仍仅检索。分数是人工排序量非概率。所有候选authority NONE；不按语义资格裁决；同文不同根保留。比较全局链接前K=5/10/20/50/100及两段式当前跨度前K后对每跨度分别取前1或前2历史根。后者预算边数按前2实际容量报告，前1略少；不把两者当相同预算。诊断另在给定正确当前跨度时测目标排名，属于评价oracle，不能当原生效果。原标注中未明确引用的轮不作负例。条件、作用域、角色、主体、来源、授予代次、版本、修订目标均不能由相似度确认；有条件修订单独标记未解决，任何候选都不能执行。所有同分项按稳定字符串顺序排列，不能据此消歧。候选池规模最坏为旧propose复杂度乘历史记录数，尚无生产资源预算。
## 实际输出
标准JS连接器执行以下完整代码，核对固定数据、边界原文、目标引用存在及排名单调、同文不同根分数相同与空历史控制。未运行Node CLI、产品原生代码、真机、训练或独立验收。
```json
{
  "episodes": 32,
  "targets": 12,
  "priorRecords": 110,
  "currentCandidates": 1046,
  "pairs": 3609,
  "fullHits": 12,
  "exactCurrent": 12,
  "missing": [],
  "targetRankWithKnownCurrent": {
    "local": [
      2,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      2,
      1,
      2,
      1
    ],
    "context": [
      2,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      2,
      1
    ]
  },
  "budget": {
    "local": {
      "5": {
        "hit": 10,
        "edges": 71
      },
      "10": {
        "hit": 10,
        "edges": 126
      },
      "20": {
        "hit": 12,
        "edges": 236
      },
      "50": {
        "hit": 12,
        "edges": 552
      },
      "100": {
        "hit": 12,
        "edges": 1052
      }
    },
    "context": {
      "5": {
        "hit": 10,
        "edges": 71
      },
      "10": {
        "hit": 11,
        "edges": 126
      },
      "20": {
        "hit": 12,
        "edges": 236
      },
      "50": {
        "hit": 12,
        "edges": 552
      },
      "100": {
        "hit": 12,
        "edges": 1052
      }
    }
  },
  "separated": {
    "5": {
      "current": 12,
      "edges": 118,
      "local1": 9,
      "local2": 12,
      "context1": 10,
      "context2": 12
    },
    "10": {
      "current": 12,
      "edges": 226,
      "local1": 9,
      "local2": 12,
      "context1": 10,
      "context2": 12
    },
    "20": {
      "current": 12,
      "edges": 426,
      "local1": 9,
      "local2": 12,
      "context1": 10,
      "context2": 12
    },
    "50": {
      "current": 12,
      "edges": 998,
      "local1": 9,
      "local2": 12,
      "context1": 10,
      "context2": 12
    },
    "100": {
      "current": 12,
      "edges": 1732,
      "local1": 9,
      "local2": 12,
      "context1": 10,
      "context2": 12
    }
  },
  "rows": [
    {
      "episode": "L03",
      "quote": "停课还能退五百",
      "target": "L03:t0:refundability",
      "currentRank": 4,
      "rank": {
        "local": 12,
        "context": 8
      },
      "knownCurrent": {
        "local": 2,
        "context": 2
      }
    },
    {
      "episode": "L08",
      "quote": "暂时不算进比较",
      "target": "L08:t0:anticipated_regret",
      "currentRank": 4,
      "rank": {
        "local": 14,
        "context": 12
      },
      "knownCurrent": {
        "local": 1,
        "context": 1
      }
    },
    {
      "episode": "L15",
      "quote": "证书是必须的",
      "target": "L15:t0:credential",
      "currentRank": 1,
      "rank": {
        "local": 1,
        "context": 1
      },
      "knownCurrent": {
        "local": 1,
        "context": 1
      }
    },
    {
      "episode": "S01",
      "quote": "转去调度部这项先撤掉",
      "target": "S01.1.2",
      "currentRank": 2,
      "rank": {
        "local": 1,
        "context": 1
      },
      "knownCurrent": {
        "local": 1,
        "context": 1
      }
    },
    {
      "episode": "S02",
      "quote": "步行上限改为十二分钟",
      "target": "S02.1.3",
      "currentRank": 1,
      "rank": {
        "local": 1,
        "context": 1
      },
      "knownCurrent": {
        "local": 1,
        "context": 1
      }
    },
    {
      "episode": "S03",
      "quote": "周五答疑就取消",
      "target": "S03.1.3",
      "currentRank": 1,
      "rank": {
        "local": 1,
        "context": 1
      },
      "knownCurrent": {
        "local": 1,
        "context": 1
      }
    },
    {
      "episode": "S04",
      "quote": "插座数量刚核实是两个",
      "target": "S04.1.4",
      "currentRank": 1,
      "rank": {
        "local": 1,
        "context": 1
      },
      "knownCurrent": {
        "local": 1,
        "context": 1
      }
    },
    {
      "episode": "S08",
      "quote": "实际是两天迟到",
      "target": "S08.1.2",
      "currentRank": 1,
      "rank": {
        "local": 1,
        "context": 1
      },
      "knownCurrent": {
        "local": 1,
        "context": 1
      }
    },
    {
      "episode": "S10",
      "quote": "不作为强制条件了",
      "target": "S10.1.2",
      "currentRank": 1,
      "rank": {
        "local": 2,
        "context": 1
      },
      "knownCurrent": {
        "local": 2,
        "context": 1
      }
    },
    {
      "episode": "S11",
      "quote": "撤回临时分析的许可",
      "target": "S11.1.1",
      "currentRank": 5,
      "rank": {
        "local": 3,
        "context": 3
      },
      "knownCurrent": {
        "local": 1,
        "context": 1
      }
    },
    {
      "episode": "S12",
      "quote": "维修店说要七百",
      "target": "S12.1.2",
      "currentRank": 1,
      "rank": {
        "local": 2,
        "context": 2
      },
      "knownCurrent": {
        "local": 2,
        "context": 2
      }
    },
    {
      "episode": "S13",
      "quote": "准确率的要求仅用于正式交付",
      "target": "S13.1.3",
      "currentRank": 1,
      "rank": {
        "local": 1,
        "context": 1
      },
      "knownCurrent": {
        "local": 1,
        "context": 1
      }
    }
  ],
  "unlabelledEpisodes": 20,
  "unlabelledCandidateEpisodes": 3,
  "guardedReferences": 2,
  "guardedRows": [
    {
      "episode": "S03",
      "quote": "周五答疑就取消",
      "condition": "如果周五需要加班",
      "guardStatus": "UNRESOLVED",
      "target": "S03.1.3"
    },
    {
      "episode": "S13",
      "quote": "准确率的要求仅用于正式交付",
      "condition": "正式交付",
      "guardStatus": "UNRESOLVED",
      "target": "S13.1.3"
    }
  ],
  "controls": 50,
  "authority": "NONE"
}
```
## 解释与后续
fullHits仅代表已标注跨度和旧记录根存在于候选对中，不能说明正确操作、范围、条件、事实或权限。原语料历史根通过人工夹具提供，不能与完全原文R77直接横比。历史中未标注的义务可能缺失。正确当前跨度的目标排名只作诊断。对照同文不同根说明高分无法替代根确认。条件引用没有被算法解析或解决，guardedRows只从评价标注提取，用于暴露验收缺口。不可把未标注轮的候选称假阳性。下一轮应重点接入来源绑定、条件方向和状态更新的真正原生入口，保留拒答、未知与不写入。若排名结果不改善或仍有低覆盖，保留负结果，不围绕12例继续调参。研究者自行选排序、K、历史确认夹具，未修改生产、唯一交接、历史冻结/证据等级；未启动新Codex任务、训练、合并、部署、主动CI或增加费用。
## 可执行复算
将固定八份文件UTF8全文按上述次序作为contents；下方Node包装读文件并核对Git blob SHA1，包装未单独运行；核心experiment实际执行。仅加载固定自有已审查源码。
```js
const fs=require("node:fs"),crypto=require("node:crypto");
const expected=["be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb","05c239f3f3b1f46235fa2464d2945c21c6c08132","bbdc12dfe65b24aa24e6b1d25a04955766cadab4","16075b3ba567ee6dc3496300beab1417172a6c42","07dcbda9532dbc3b330abfd79a399cb52aa91aeb","8a6b42f83b80283db6e215fe48f4fb2efbf8368c","b0bea7b4c101c170be2aaa2355973739b125e0b7","ef103587b216ad07c1a47102ddb7cb8d2975283d"];
const buffers=process.argv.slice(2).map(p=>fs.readFileSync(p));
if(buffers.length!==expected.length||buffers.some((b,i)=>crypto.createHash("sha1").update("blob "+b.length+"\0").update(b).digest("hex")!==expected[i]))throw Error("asset identity");
function experiment(contents){
 const ck=(b,m)=>{if(!b)throw Error(m)},docs=contents.slice(0,2).map(JSON.parse),code=contents[7].split("```js\n")[1].split("\n```")[0],P=Function("input",code.split(" const out={episodes:")[0]+"\nreturn {propose};\n}\nreturn experiment(input);")(contents.slice(0,7));
 const ks=[5,10,20,50,100],modes=["local","context"],ch=s=>new Set([...s].filter(c=>!/[\p{P}\s]/u.test(c))),grams=s=>{let a=[...s];return new Set(a.slice(1).map((v,i)=>a[i]+v).filter(v=>!/[\p{P}\s]/u.test(v)))},jac=(a,b)=>{let k=0;for(let x of a)if(b.has(x))k++;return k/(a.size+b.size-k||1)},sim=(a,b)=>jac(ch(a),ch(b))+jac(grams(a),grams(b)),key=(x)=>x.start+":"+x.end;
 function prior(ep,d){return (d?ep.turns[0].proposal.claims:ep.turns[0].claims).map((x,i)=>({id:d?ep.id+".1."+(i+1):ep.id+":t0:"+x.field,quote:d?x.quote:x.span,kind:d?x.role:x.kind}))}
 function search(text,history){const pool=P.propose(text,true).all.revision;let links=[];for(const c of pool){ck(text.slice(c.start,c.end)===c.text,"span");const strong=text.slice(Math.max(0,text.slice(0,c.start).search(/[^。！？；.!?;]*$/u)),c.end)+text.slice(c.end).split(/[。！？；.!?;]/u)[0];for(const h of history){let a=sim(c.text,h.quote),b=sim(strong,h.quote);links.push({key:key(c),id:h.id,local:c.score+4*a,context:c.score+4*a+2*b,localSim:a,contextSim:b})}}return {pool,links}}
 const rank=(x,m)=>[...x].sort((a,b)=>b[m]-a[m]||a.key.localeCompare(b.key)||a.id.localeCompare(b.id));
 const out={episodes:0,targets:0,priorRecords:0,currentCandidates:0,pairs:0,fullHits:0,exactCurrent:0,missing:[],targetRankWithKnownCurrent:{local:[],context:[]},budget:Object.fromEntries(modes.map(m=>[m,Object.fromEntries(ks.map(k=>[k,{hit:0,edges:0}]))])),separated:Object.fromEntries(ks.map(k=>[k,{current:0,edges:0,local1:0,local2:0,context1:0,context2:0}])),rows:[],unlabelledEpisodes:0,unlabelledCandidateEpisodes:0,guardedReferences:0,guardedRows:[],controls:0,authority:"NONE"};
 for(let d=0;d<2;d++)for(let ep of docs[d].cases){let t=ep.turns[1],h=prior(ep,d),z=search(t.text,h);out.episodes++;out.priorRecords+=h.length;out.currentCandidates+=z.pool.length;out.pairs+=z.links.length;const refs=(d?t.proposal.claims:t.claims).filter(x=>d?x.ref:x.supersedes);if(!refs.length){out.unlabelledEpisodes++;out.unlabelledCandidateEpisodes+=+(z.links.length>0)}const sorted=Object.fromEntries(modes.map(m=>[m,rank(z.links,m)]));for(let m of modes)for(let k of ks)out.budget[m][k].edges+=Math.min(k,sorted[m].length);for(let k of ks)out.separated[k].edges+=Math.min(k,z.pool.length)*Math.min(2,h.length);
 for(const r of refs){let q=d?r.quote:r.span,s=t.text.indexOf(q),id=d?r.ref:r.supersedes;ck(s>=0&&s===t.text.lastIndexOf(q)&&h.filter(x=>x.id===id).length===1,"gold");out.targets++;const g=s+":"+(s+q.length),match=x=>x.id===id&&x.key===g,hit=z.pool.some(c=>key(c)===g),rr={episode:ep.id,quote:q,target:id,currentRank:z.pool.findIndex(c=>key(c)===g)+1,rank:{},knownCurrent:{}};out.exactCurrent+=+hit;out.fullHits+=+z.links.some(match);if(!hit)out.missing.push(rr);for(let m of modes){let v=sorted[m].findIndex(match)+1;rr.rank[m]=v;let a=sorted[m].filter(x=>x.key===g),j=a.findIndex(match)+1;rr.knownCurrent[m]=j;out.targetRankWithKnownCurrent[m].push(j);for(let k of ks){out.budget[m][k].hit+=+(v>0&&v<=k);let b=out.separated[k];if(rr.currentRank>0&&rr.currentRank<=k){b[m+"1"]+=+(j===1);b[m+"2"]+=+(j>0&&j<=2)}}}for(let k of ks)out.separated[k].current+=+(rr.currentRank>0&&rr.currentRank<=k);if(d&&r.condition){out.guardedReferences++;out.guardedRows.push({episode:ep.id,quote:q,condition:r.condition,guardStatus:"UNRESOLVED",target:id})}out.rows.push(rr)}
 }
 ck(out.episodes===32&&out.targets===12,"counts");ck(out.fullHits===out.exactCurrent,"all targets finite");for(let m of modes){for(let k of ks)ck(out.budget[m][k].hit<=out.fullHits,"coverage bound");for(let i=1;i<ks.length;i++)ck(out.budget[m][ks[i]].hit>=out.budget[m][ks[i-1]].hit,"monotonic")}out.controls+=4;
 const h=[{id:"A",quote:"每周工时最多十小时"},{id:"B",quote:"每周工时最多十小时"}],q="每周工时改为八小时";let z=search(q,h);ck(z.links.length>0,"ambiguous example");for(let x of z.links.filter(x=>x.id==="A")){let b=z.links.find(v=>v.key===x.key&&v.id==="B");ck(b&&b.local===x.local&&b.context===x.context,"same text different roots");out.controls++}ck(search(q,[]).links.length===0,"missing history");out.controls++;return out
}
console.log(JSON.stringify(experiment(buffers.map(b=>b.toString("utf8"))),null,2));
```
