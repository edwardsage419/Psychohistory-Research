# 自主认知：完整原文多修订边界候选与历史记录多样化
2026-11-26。RESEARCH_CANDIDATE / RECOMBINED_PUBLIC_SYNTHETIC_DEVELOPMENT / CONNECTOR_JS_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。

## 基线、去重、数据
起点及写前main 44699ee35272e118e404369ca65d454a87f90ff5。核对20近期提交、15开放PR、decision_hub目录相关题名、v3.2及同步规程（blob 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85、26c4d946e48f01858fb8e8c2cb06e4f7ba91bf05），唯一产品交接前20行（5e74f4f0b37141d631740e844ad8bbbfed232e07）。#63仍在开放列表，未重跑原生。读取前轮3d7e79b1535b48770fefcdb0d084cfde433dcc36、边界多样性62ce014c62b4e8415ef92f31aec9a3236802bc83、条件封套6f3bf015c3a82faaf863c8cc38a14230e75e7fc0、高阶联合支持d827adc15f983c9c66c4f9fb989d2d911b92a9c6相关段落。增量是取消人工修订组输入，以完整原文产生分配候选，及无分隔情况下历史根多样性预算，不重复前轮人工组和流式算法，不宣称全库无重复。
固定输入：
1. research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
2. research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
实际读取完整文本并核对连接器blob身份。未独立重算原始Git字节，Node包装提供核对。32既有原创合成情节、110历史记录、12唯一显式历史引用。按情节ID与出现序号保留独立记录，原字段重复标签不合并。历史来自首轮标注，作为模拟记录，非真实确认账本。选择12有唯一引用的第二轮，去终止句号后有序拼接不同情节，四种连接形式每种132，共528个双目标重复组合；另每种固定12个有标注与无显式引用标注的混合组合，只评估已标注项。组合和评分由研究者选择，既有语料已见、同源重复，不是独立样本、训练、真人或自然语料。目标与拼接偏移仅用于评分，生成只读取完整原文与全部历史原文及其身份。

## 方法
原文用Unicode标量坐标；按标点及空白产生长度2至32的跨度，保留同一候选池供所有策略比较。历史原文去标点空白，字符与相邻双字集合Jaccard；沿前轮4倍局部相似度+2倍所在标点段相似度+0/0.5/1边界项。历史双字组在去标点后生成，可能跨原标点，故与前轮并非完全相同的通用相似度合同；本次强分隔全历史结果与前轮三档一致仅为有限核对。稳定排序按分数、起止、身份。评分非概率。global为全局前K；strong按原文强标点切分后按组首最高分排序，组间轮流；clause将弱标点、空白也作分组边界；cue为强标点加另外/此外/同时/并且/而且的起点候选。按跨度起点分桶，可能有跨度越过连接词，不代表结构封闭。全量候选数相同；不同分配模式不能相加作为同预算算法。
针对逗号/无分隔，root25和root50先保留前floor(K×25%或50%)个不同历史身份的最高分跨度，再按全局分数补齐，rootRound按历史身份轮流分配。此处不同身份只是检索多样性，不意味着不同修订，也不排除同一根多次修订。未检测引语、否定、主体、条件、跨句语义、实际修订资格。所有输出authority NONE，不能作为正式修订组、确认票据或数学发布。
先分两项实验实际执行；整合版对所有组合重新全局排序后分桶，与先前的局部分桶保留前K实现作复核。66项两目标同时召回汇总全部一致。逐例检查候选预算、命中分拆、身份、Unicode及原文锚。两项前期执行分别3个专项控制通过，整合版4个专项控制通过，不把重复控制计为独立验收。未测设备耗时/内存，缓存仅为重复合成情节复算，非产品部署策略。

## 结果
K20双目标同时召回：
| 连接 | global | strong | clause | cue | root25 | root50 | rootRound |
|---|---:|---:|---:|---:|---:|---:|---:|
| ； | 18 | 30 | 12 | 30 | 未执行 | 未执行 | 未执行 |
| ， | 18 | 18 | 12 | 18 | 30 | 26 | 12 |
| 另外 | 10 | 10 | 7 | 21 | 未执行 | 未执行 | 未执行 |
| NONE | 10 | 10 | 7 | 10 | 13 | 12 | 3 |
其中逗号root25改善18→30，但无分隔仅10→13，且逐目标命中109→107。rootRound在无分隔K20仅3/132。不能把多样性无条件替代全局排序。细分标点分组在逗号K20退步18→12；连接词辅助在人工加入“另外”时10→21，但该词可能出现在引语或非编辑连接中，结果不能证明真实分组语义。人工无分隔仍有原句内部标点，未覆盖完全无标点文本。候选跨度可跨cue分组边界，见cueCrossingTop20；不能将分组当共同语义路径或证据支持。保留负结果，不围绕已见12项调参。研究目标仍为自主原文理解与独立决策计算。

完整整合复算输出：
```json
{
  "episodes": 32,
  "history": 110,
  "targets": 12,
  "variants": {
    "；": {
      "cases": 132,
      "pool": 2328040,
      "metrics": {
        "global": {
          "10": {
            "edges": 1320,
            "hits": 88,
            "both": 2,
            "none": 46,
            "roots": 252
          },
          "20": {
            "edges": 2640,
            "hits": 124,
            "both": 18,
            "none": 26,
            "roots": 404
          },
          "50": {
            "edges": 6600,
            "hits": 158,
            "both": 42,
            "none": 16,
            "roots": 835
          }
        },
        "strong": {
          "10": {
            "edges": 1320,
            "hits": 88,
            "both": 12,
            "none": 56,
            "roots": 394
          },
          "20": {
            "edges": 2640,
            "hits": 132,
            "both": 30,
            "none": 30,
            "roots": 526
          },
          "50": {
            "edges": 6600,
            "hits": 176,
            "both": 56,
            "none": 12,
            "roots": 1030
          }
        },
        "clause": {
          "10": {
            "edges": 1320,
            "hits": 88,
            "both": 12,
            "none": 56,
            "roots": 694
          },
          "20": {
            "edges": 2640,
            "hits": 88,
            "both": 12,
            "none": 56,
            "roots": 964
          },
          "50": {
            "edges": 6600,
            "hits": 154,
            "both": 42,
            "none": 20,
            "roots": 2062
          }
        },
        "cue": {
          "10": {
            "edges": 1320,
            "hits": 88,
            "both": 12,
            "none": 56,
            "roots": 394
          },
          "20": {
            "edges": 2640,
            "hits": 132,
            "both": 30,
            "none": 30,
            "roots": 526
          },
          "50": {
            "edges": 6600,
            "hits": 176,
            "both": 56,
            "none": 12,
            "roots": 1030
          }
        }
      },
      "splitAtJoin": {
        "strong": 132,
        "clause": 132,
        "cue": 132
      },
      "distinctTargetGroups": {
        "strong": 132,
        "clause": 132,
        "cue": 132
      },
      "mixed": {
        "cases": 12,
        "hits": {
          "global": 5,
          "strong": 6,
          "clause": 4,
          "cue": 6
        }
      },
      "cueCrossingTop20": 0
    },
    "，": {
      "cases": 132,
      "pool": 2328040,
      "metrics": {
        "global": {
          "10": {
            "edges": 1320,
            "hits": 88,
            "both": 2,
            "none": 46,
            "roots": 252
          },
          "20": {
            "edges": 2640,
            "hits": 124,
            "both": 18,
            "none": 26,
            "roots": 404
          },
          "50": {
            "edges": 6600,
            "hits": 158,
            "both": 42,
            "none": 16,
            "roots": 835
          }
        },
        "strong": {
          "10": {
            "edges": 1320,
            "hits": 88,
            "both": 2,
            "none": 46,
            "roots": 252
          },
          "20": {
            "edges": 2640,
            "hits": 124,
            "both": 18,
            "none": 26,
            "roots": 404
          },
          "50": {
            "edges": 6600,
            "hits": 158,
            "both": 42,
            "none": 16,
            "roots": 835
          }
        },
        "clause": {
          "10": {
            "edges": 1320,
            "hits": 88,
            "both": 12,
            "none": 56,
            "roots": 694
          },
          "20": {
            "edges": 2640,
            "hits": 88,
            "both": 12,
            "none": 56,
            "roots": 964
          },
          "50": {
            "edges": 6600,
            "hits": 154,
            "both": 42,
            "none": 20,
            "roots": 2062
          }
        },
        "cue": {
          "10": {
            "edges": 1320,
            "hits": 88,
            "both": 2,
            "none": 46,
            "roots": 252
          },
          "20": {
            "edges": 2640,
            "hits": 124,
            "both": 18,
            "none": 26,
            "roots": 404
          },
          "50": {
            "edges": 6600,
            "hits": 158,
            "both": 42,
            "none": 16,
            "roots": 835
          }
        },
        "root25": {
          "10": {
            "edges": 1320,
            "hits": 92,
            "both": 6,
            "none": 46,
            "roots": 312
          },
          "20": {
            "edges": 2640,
            "hits": 140,
            "both": 30,
            "none": 22,
            "roots": 688
          },
          "50": {
            "edges": 6600,
            "hits": 158,
            "both": 42,
            "none": 16,
            "roots": 1592
          }
        },
        "root50": {
          "10": {
            "edges": 1320,
            "hits": 82,
            "both": 12,
            "none": 62,
            "roots": 660
          },
          "20": {
            "edges": 2640,
            "hits": 132,
            "both": 26,
            "none": 26,
            "roots": 1320
          },
          "50": {
            "edges": 6600,
            "hits": 165,
            "both": 47,
            "none": 14,
            "roots": 3300
          }
        },
        "rootRound": {
          "10": {
            "edges": 1320,
            "hits": 66,
            "both": 6,
            "none": 72,
            "roots": 1320
          },
          "20": {
            "edges": 2640,
            "hits": 84,
            "both": 12,
            "none": 60,
            "roots": 2640
          },
          "50": {
            "edges": 6600,
            "hits": 85,
            "both": 12,
            "none": 59,
            "roots": 6600
          }
        }
      },
      "splitAtJoin": {
        "strong": 0,
        "clause": 132,
        "cue": 0
      },
      "distinctTargetGroups": {
        "strong": 0,
        "clause": 132,
        "cue": 0
      },
      "mixed": {
        "cases": 12,
        "hits": {
          "global": 5,
          "strong": 5,
          "clause": 4,
          "cue": 5
        }
      },
      "cueCrossingTop20": 0
    },
    "另外": {
      "cases": 132,
      "pool": 4082430,
      "metrics": {
        "global": {
          "10": {
            "edges": 1320,
            "hits": 73,
            "both": 2,
            "none": 61,
            "roots": 263
          },
          "20": {
            "edges": 2640,
            "hits": 109,
            "both": 10,
            "none": 33,
            "roots": 382
          },
          "50": {
            "edges": 6600,
            "hits": 142,
            "both": 29,
            "none": 19,
            "roots": 738
          }
        },
        "strong": {
          "10": {
            "edges": 1320,
            "hits": 73,
            "both": 2,
            "none": 61,
            "roots": 263
          },
          "20": {
            "edges": 2640,
            "hits": 109,
            "both": 10,
            "none": 33,
            "roots": 382
          },
          "50": {
            "edges": 6600,
            "hits": 142,
            "both": 29,
            "none": 19,
            "roots": 738
          }
        },
        "clause": {
          "10": {
            "edges": 1320,
            "hits": 56,
            "both": 6,
            "none": 82,
            "roots": 602
          },
          "20": {
            "edges": 2640,
            "hits": 68,
            "both": 7,
            "none": 71,
            "roots": 813
          },
          "50": {
            "edges": 6600,
            "hits": 133,
            "both": 29,
            "none": 28,
            "roots": 1695
          }
        },
        "cue": {
          "10": {
            "edges": 1320,
            "hits": 62,
            "both": 7,
            "none": 77,
            "roots": 410
          },
          "20": {
            "edges": 2640,
            "hits": 106,
            "both": 21,
            "none": 47,
            "roots": 508
          },
          "50": {
            "edges": 6600,
            "hits": 156,
            "both": 40,
            "none": 16,
            "roots": 950
          }
        }
      },
      "splitAtJoin": {
        "strong": 0,
        "clause": 0,
        "cue": 132
      },
      "distinctTargetGroups": {
        "strong": 0,
        "clause": 100,
        "cue": 132
      },
      "mixed": {
        "cases": 12,
        "hits": {
          "global": 6,
          "strong": 6,
          "clause": 4,
          "cue": 6
        }
      },
      "cueCrossingTop20": 331
    },
    "NONE": {
      "cases": 132,
      "pool": 3537930,
      "metrics": {
        "global": {
          "10": {
            "edges": 1320,
            "hits": 73,
            "both": 2,
            "none": 61,
            "roots": 263
          },
          "20": {
            "edges": 2640,
            "hits": 109,
            "both": 10,
            "none": 33,
            "roots": 381
          },
          "50": {
            "edges": 6600,
            "hits": 139,
            "both": 28,
            "none": 21,
            "roots": 719
          }
        },
        "strong": {
          "10": {
            "edges": 1320,
            "hits": 73,
            "both": 2,
            "none": 61,
            "roots": 263
          },
          "20": {
            "edges": 2640,
            "hits": 109,
            "both": 10,
            "none": 33,
            "roots": 381
          },
          "50": {
            "edges": 6600,
            "hits": 139,
            "both": 28,
            "none": 21,
            "roots": 719
          }
        },
        "clause": {
          "10": {
            "edges": 1320,
            "hits": 56,
            "both": 6,
            "none": 82,
            "roots": 600
          },
          "20": {
            "edges": 2640,
            "hits": 68,
            "both": 7,
            "none": 71,
            "roots": 816
          },
          "50": {
            "edges": 6600,
            "hits": 133,
            "both": 29,
            "none": 28,
            "roots": 1683
          }
        },
        "cue": {
          "10": {
            "edges": 1320,
            "hits": 73,
            "both": 2,
            "none": 61,
            "roots": 263
          },
          "20": {
            "edges": 2640,
            "hits": 109,
            "both": 10,
            "none": 33,
            "roots": 381
          },
          "50": {
            "edges": 6600,
            "hits": 139,
            "both": 28,
            "none": 21,
            "roots": 719
          }
        },
        "root25": {
          "10": {
            "edges": 1320,
            "hits": 76,
            "both": 3,
            "none": 59,
            "roots": 315
          },
          "20": {
            "edges": 2640,
            "hits": 107,
            "both": 13,
            "none": 38,
            "roots": 680
          },
          "50": {
            "edges": 6600,
            "hits": 140,
            "both": 29,
            "none": 21,
            "roots": 1601
          }
        },
        "root50": {
          "10": {
            "edges": 1320,
            "hits": 61,
            "both": 5,
            "none": 76,
            "roots": 660
          },
          "20": {
            "edges": 2640,
            "hits": 102,
            "both": 12,
            "none": 42,
            "roots": 1320
          },
          "50": {
            "edges": 6600,
            "hits": 138,
            "both": 28,
            "none": 22,
            "roots": 3300
          }
        },
        "rootRound": {
          "10": {
            "edges": 1320,
            "hits": 48,
            "both": 2,
            "none": 86,
            "roots": 1320
          },
          "20": {
            "edges": 2640,
            "hits": 58,
            "both": 3,
            "none": 77,
            "roots": 2640
          },
          "50": {
            "edges": 6600,
            "hits": 58,
            "both": 3,
            "none": 77,
            "roots": 6600
          }
        }
      },
      "splitAtJoin": {
        "strong": 0,
        "clause": 0,
        "cue": 0
      },
      "distinctTargetGroups": {
        "strong": 0,
        "clause": 100,
        "cue": 0
      },
      "mixed": {
        "cases": 12,
        "hits": {
          "global": 6,
          "strong": 6,
          "clause": 4,
          "cue": 6
        }
      },
      "cueCrossingTop20": 0
    }
  },
  "controls": 4,
  "authority": "NONE",
  "work": {
    "pairs": 6471410,
    "cacheMiss": 469,
    "cacheHit": 1557
  }
}
```

## 复算
以下函数为整合复算实际运行代码。Node文件包装未执行，调用者需从固定提交获取两份数据，不执行外部文本。
```js
function study(contents){
 const ck=(x,m)=>{if(!x)throw Error(m)},eps=[],hist=[],ks=[10,20,50],modes=["global","strong","clause","cue","root25","root50","rootRound"],seps=["；","，","另外",""];
 for(let d=0;d<2;d++)for(const ep of JSON.parse(contents[d]).cases){
  const h=(d?ep.turns[0].proposal.claims:ep.turns[0].claims).map((x,i)=>({id:ep.id+":occ:"+(i+1),label:d?ep.id+".1."+(i+1):ep.id+":t0:"+x.field,q:d?x.quote:x.span}));hist.push(...h);
  const t=ep.turns[1],rs=(d?t.proposal.claims:t.claims).filter(x=>d?x.ref:x.supersedes).map(x=>{const z=h.filter(y=>y.label===(d?x.ref:x.supersedes));ck(z.length===1,"ref");return {q:d?x.quote:x.span,id:z[0].id}});eps.push({id:ep.id,t:t.text.replace(/[。！？.!?]+$/u,""),rs})
 }
 const tag=eps.filter(e=>e.rs.length===1),neg=eps.filter(e=>!e.rs.length);
 const chars=s=>Array.from(s),fe=s=>{const a=chars(s);return [new Set(a),new Set(a.slice(1).map((x,i)=>a[i]+x))]},jac=(a,b)=>{let n=0;for(const x of a)if(b.has(x))n++;return n/(a.size+b.size-n||1)},sim=(a,b)=>jac(a[0],b[0])+jac(a[1],b[1]);
 const hf=hist.map(h=>({...h,f:fe(h.q.replace(/[\p{P}\s]/gu,""))})),cmp=(a,b)=>b.score-a.score||a.s-b.s||a.e-b.e||(a.id<b.id?-1:a.id>b.id?1:0),key=x=>x.s+":"+x.e+":"+x.id;
 const delim=/^[，。！？；、：,.!?;:\s]$/u,strong=/^[。！？；.!?;]$/u,cache=new Map(),work={pairs:0,cacheMiss:0,cacheHit:0};
 function local(s){
  if(cache.has(s)){work.cacheHit++;return cache.get(s)}
  work.cacheMiss++;const a=chars(s),ctx=fe(s),cs=hf.map(h=>2*sim(ctx,h.f)),z=[];
  for(let i=0;i<a.length;i++)for(let j=i+2;j<=a.length&&j-i<=32;j++){let f=fe(a.slice(i,j).join("")),edge=(+(i===0)+ +(j===a.length))/2;for(let k=0;k<hf.length;k++)z.push({s:i,e:j,id:hf[k].id,score:4*sim(f,hf[k].f)+cs[k]+edge})}
  z.sort(cmp);work.pairs+=z.length;if(cache.size>=64)cache.delete(cache.keys().next().value);cache.set(s,z);return z
 }
 function raw(t){
  const a=chars(t),cuts={strong:[0],clause:[0],cue:[0]},z=[];
  for(let i=0;i<a.length;i++){
   if(strong.test(a[i])){cuts.strong.push(i+1);cuts.cue.push(i+1)}
   if(delim.test(a[i]))cuts.clause.push(i+1);
   if(["另外","此外","同时","并且","而且"].some(w=>a.slice(i,i+chars(w).length).join("")===w))cuts.cue.push(i)
  }
  for(let m of ["strong","clause","cue"])cuts[m]=[...new Set(cuts[m])].sort((a,b)=>a-b);
  for(let i=0;i<a.length;){if(delim.test(a[i])){i++;continue}let j=i+1;while(j<a.length&&!delim.test(a[j]))j++;for(let x of local(a.slice(i,j).join("")))z.push({...x,s:x.s+i,e:x.e+i});i=j}
  z.sort(cmp);return {a,cuts,z}
 }
 function group(p,ls){let j=0;while(j+1<ls.length&&ls[j+1]<=p)j++;return j}
 function select(p,k,m){
  const z=p.z;if(m==="global")return z.slice(0,k);
  let buckets=new Map();for(let x of z){let id=m.startsWith("root")?x.id:group(x.s,p.cuts[m]);let b=buckets.get(id);if(!b){b=[];buckets.set(id,b)}if(b.length<k)b.push(x)}
  let g=[...buckets.values()],a=[];
  if(m==="root25"||m==="root50"){let q=Math.min(g.length,Math.floor(k*(m==="root25"?.25:.5)));a=g.slice(0,q).map(b=>b[0]);let s=new Set(a.map(key));for(let x of z){if(a.length===Math.min(k,z.length))break;if(!s.has(key(x))){a.push(x);s.add(key(x))}}}
  else for(let i=0;a.length<Math.min(k,z.length);i++)for(let b of g)if(b[i]&&a.length<k)a.push(b[i]);
  ck(a.length===Math.min(k,z.length)&&new Set(a.map(key)).size===a.length,"selection");return a
 }
 function target(e,off){let q=e.rs[0].q,i=e.t.indexOf(q);ck(i>=0&&i===e.t.lastIndexOf(q),"anchor");let s=chars(e.t.slice(0,i)).length+off;return {s,e:s+chars(q).length,id:e.rs[0].id,q}}
 const metric=()=>({edges:0,hits:0,both:0,none:0,roots:0}),out={episodes:eps.length,history:hist.length,targets:tag.length,variants:{},controls:0,authority:"NONE"};
 for(let sep of seps){let ms=sep==="，"||sep===""?modes:modes.slice(0,4);let v={cases:0,pool:0,metrics:Object.fromEntries(ms.map(m=>[m,Object.fromEntries(ks.map(k=>[k,metric()]))])),splitAtJoin:{strong:0,clause:0,cue:0},distinctTargetGroups:{strong:0,clause:0,cue:0},mixed:{cases:0,hits:Object.fromEntries(modes.slice(0,4).map(m=>[m,0]))},cueCrossingTop20:0};out.variants[sep||"NONE"]=v;
  for(let a of tag)for(let b of tag){if(a===b)continue;let off=chars(a.t+sep).length,p=raw(a.t+sep+b.t),ts=[target(a,0),target(b,off)];ck(ts.every(t=>p.a.slice(t.s,t.e).join("")===t.q),"scalar");v.cases++;v.pool+=p.z.length;
   for(let m of ["strong","clause","cue"]){v.splitAtJoin[m]+=p.cuts[m].includes(off)||(sep==="另外"&&p.cuts[m].includes(off-2));v.distinctTargetGroups[m]+=p.cuts[m].some(c=>c>=ts[0].e&&c<=ts[1].s)}
   for(let m of ms)for(let k of ks){let x=select(p,k,m),n=ts.filter(t=>x.some(y=>key(y)===key(t))).length,r=v.metrics[m][k];r.edges+=x.length;r.hits+=n;r.both+=n===2;r.none+=n===0;r.roots+=new Set(x.map(y=>y.id)).size;if(m==="cue"&&k===20)v.cueCrossingTop20+=x.filter(y=>p.cuts.cue.some(c=>y.s<c&&c<y.e)).length}
  }
  for(let i=0;i<tag.length;i++){let a=tag[i],b=neg[i%neg.length],p=raw(a.t+sep+b.t),t=target(a,0);v.mixed.cases++;for(let m of modes.slice(0,4))v.mixed.hits[m]+=select(p,20,m).some(x=>key(x)===key(t))}
  for(let m of ms)for(let k of ks){let r=v.metrics[m][k];ck(r.edges===v.metrics.global[k].edges&&r.hits===v.cases+r.both-r.none,"budget/partition")}
 }
 ck(tag.length===12&&hist.length===110&&eps.length===32,"counts");out.controls++;
 let a=raw("甲😀改为八小时；乙改为两天");ck(a.a.join("")==="甲😀改为八小时；乙改为两天"&&a.cuts.strong.includes(8),"unicode");out.controls++;
 ck(raw("。！？").z.length===0,"empty");out.controls++;
 let z=[{s:0,e:2,id:"a",score:3},{s:0,e:2,id:"b",score:3},{s:1,e:3,id:"a",score:2}];ck(select({z},2,"rootRound").map(x=>x.id).join("")==="ab","same text distinct roots");out.controls++;
 out.work=work;return out
}
const fs=require("node:fs"),crypto=require("node:crypto");
const expected=["be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb","05c239f3f3b1f46235fa2464d2945c21c6c08132"];
const buffers=process.argv.slice(2).map(p=>fs.readFileSync(p));
if(buffers.length!==2||buffers.some((b,i)=>crypto.createHash("sha1").update("blob "+b.length+"\0").update(b).digest("hex")!==expected[i]))throw Error("asset identity");
console.log(JSON.stringify(study(buffers.map(b=>b.toString("utf8"))),null,2));
```

## 后续责任与限制
研究端保留边界候选的多解释及原文锚，下一轮应将候选生成接到可审计的主体、条件、时间、数量与历史根关联，区分真实编辑、引用、否定和未决义务；避免继续穷举同源组合充当新证据。独立轨保管未见原文，测自然多编辑、无标点、引语、不同主体、连续更正同根、条件取消及遗漏。仅经宿主确认的原生语义进入数学引擎。未执行完整产品、独立留出、真实用户、Mac/iPhone、训练、部署、主动CI；无个人资料、第三方AI运行时依赖或新增费用。生产代码、冻结、证据等级、交接及PR不变。
