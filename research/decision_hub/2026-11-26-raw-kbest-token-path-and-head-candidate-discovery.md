# 自主认知：原文K优分词路径与无金标输入的词级候选头发现
2026-11-26。RESEARCH_CANDIDATE / REAL_EXTERNAL_DEVELOPMENT_BYTES_VERIFIED / RAW_TEXT_PATH_RANKING / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线
起点main 9f6d257e3c6172b0a051718a9301eaeef8300da1；沿用本轮已核对v3.2、同步规程、25近期提交、15开放PR、固定历史交接前段（最新路径未定位），#63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft。前序真实原文词格联合预算、金标端点边际排名3acea2859fa8095061cd2efb6f8918282803ab75、全句分词见证4d23fdf2dbabd9a2cf92c794f19d218e13a4fb7c已有联合可行性及gold oracle诊断；本轮新增完全依据原文和固定词典选择实际K优分词路径，并对每条路径全部词生成候选头，事后对照依存弧，非金标端点选择、分词上界或完整语义预测。前两阶段段对排序及商图边界不重复。局部查重有限。
## 固定资产
按下列顺序实际读取连接器blob：
UniversalDependencies/UD_Chinese-GSDSimp af8cc878e7934b38ce3c1a266053100e7c47de6f
rhcarvalho/cedict d7fee8237f26524b38eee220647e4c5d79f00de9
edwardsage419/Psychohistory-Research cee6b6f8d759b6aa33ec4f2863232a6583f8ae07
edwardsage419/Psychohistory-Research db9cc100d96d49832fe32879a706f63830301773
edwardsage419/Psychohistory-Research 0633533cebfb0cdea6aecff4e422bd3d4cdb5188
前两项分别为UD_Chinese-GSDSimp dev commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3及CC-CEDICT镜像commit 6317ff202e14be60365c826f62e45fc9fa71d19e。实际复用第四项UTF8/Git SHA1实现独立复算两份字节身份均匹配；第五项align/segments及第三项expanded词格实际执行。来源 https://universaldependencies.org/treebanks/zh_gsdsimp/ 及 https://www.mdbg.net/chinese/dictionary?page=cc-cedict ，既有许可登记CC BY-SA 4.0、底层文本权利另审，本轮未重审许可全文；只保存聚合结果及自有代码，不复制第三方文本或词条，未读取train/test。已见500句wiki开发集，非独立留出、真人个人对话或授权训练。
## 方法及证明
沿用固定expanded格（字典/结构边、16标量长度、空白跳过、未知跨度代价）。从后往前，每个顶点对每条出边连接其后缀前K条路径，按总代价、第一边终点及后缀排名稳定排序取K。精确性：一条出边下第K名之后的后缀有至少K条同边且不劣的替代，不能进入全局按相同稳定顺序的前K；归纳至起点。路径不依据gold排序，不使用预训练权重、学习、POS或概率；研究者选定K=1/4/16。每条路径对非纯标点词生成所有不同词的有向候选头；三种排名均依赖路径和原文：词序距离、同距离略优先右侧、跨原始标点段附加1成本。每词保留H=1/3/5或全候选；按原文精确半开区间合并跨路径候选，任一保留边对有实际共同路径见证，不保证所有保留边来自同一完整路径或形成合法依存树。不同路径策略候选数不等，不声称等算力。路径枚举和头候选只读无权限。
所有路径与候选生成完成后才读取当前句gold行，逐字对齐评分：金标词边并集、完整gold分词路径是否实际进入前K（与各词边际出现分开）、非root非punct弧的精确端点对覆盖、九类从句/并列/标记代理及跨段弧覆盖，分别统计。候选覆盖不等同实际正确依存关系、全句解析或科学决策。K优DP穷举300个小图×3预算独立对照，核对路径稳定次序；实际完整开发集运行一次，未宣称第二次独立执行。候选生成内存与复杂度未测设备，不将路径数直接当速度。全部指标在同一已见开发语料，研究者选定路径成本继承、预算、排名及评价口径；无真实语言泛化结论。
```json
{
  "source": [
    {
      "bytes": 1195378,
      "sha": "af8cc878e7934b38ce3c1a266053100e7c47de6f"
    },
    {
      "bytes": 9881659,
      "sha": "d7fee8237f26524b38eee220647e4c5d79f00de9"
    }
  ],
  "words": 121696,
  "sentences": 500,
  "tokens": 12665,
  "arcs": 10395,
  "scope": 2618,
  "cross": 1404,
  "unmappedCross": 17,
  "controls": 900,
  "metrics": {
    "1": {
      "pathCount": 500,
      "pathTokens": 12615,
      "uniqueTokens": 12615,
      "goldTokens": 10015,
      "goldCompletePath": 35,
      "goldAllMarginal": 35,
      "unrankedPairs": 279534,
      "goldArcs": 6623,
      "scopeArcs": 1841,
      "crossArcs": 947,
      "rank": {
        "distance": {
          "1": {
            "pairs": 10794,
            "gold": 1129,
            "scope": 311,
            "cross": 34
          },
          "3": {
            "pairs": 32382,
            "gold": 3413,
            "scope": 695,
            "cross": 87
          },
          "5": {
            "pairs": 53965,
            "gold": 4526,
            "scope": 978,
            "cross": 176
          }
        },
        "right": {
          "1": {
            "pairs": 10794,
            "gold": 1964,
            "scope": 230,
            "cross": 21
          },
          "3": {
            "pairs": 32382,
            "gold": 3878,
            "scope": 725,
            "cross": 88
          },
          "5": {
            "pairs": 53965,
            "gold": 4721,
            "scope": 975,
            "cross": 172
          }
        },
        "crossPenalty": {
          "1": {
            "pairs": 10794,
            "gold": 1318,
            "scope": 333,
            "cross": 17
          },
          "3": {
            "pairs": 32382,
            "gold": 3574,
            "scope": 712,
            "cross": 76
          },
          "5": {
            "pairs": 53965,
            "gold": 4623,
            "scope": 979,
            "cross": 159
          }
        }
      },
      "costExcess": 0
    },
    "4": {
      "pathCount": 2000,
      "pathTokens": 51732,
      "uniqueTokens": 15317,
      "goldTokens": 10567,
      "goldCompletePath": 56,
      "goldAllMarginal": 59,
      "unrankedPairs": 391032,
      "goldArcs": 7299,
      "scopeArcs": 1971,
      "crossArcs": 1022,
      "rank": {
        "distance": {
          "1": {
            "pairs": 15006,
            "gold": 1263,
            "scope": 347,
            "cross": 34
          },
          "3": {
            "pairs": 46742,
            "gold": 3792,
            "scope": 744,
            "cross": 91
          },
          "5": {
            "pairs": 79402,
            "gold": 5007,
            "scope": 1045,
            "cross": 184
          }
        },
        "right": {
          "1": {
            "pairs": 14656,
            "gold": 2166,
            "scope": 237,
            "cross": 22
          },
          "3": {
            "pairs": 45617,
            "gold": 4300,
            "scope": 774,
            "cross": 93
          },
          "5": {
            "pairs": 77932,
            "gold": 5221,
            "scope": 1037,
            "cross": 182
          }
        },
        "crossPenalty": {
          "1": {
            "pairs": 14950,
            "gold": 1468,
            "scope": 371,
            "cross": 17
          },
          "3": {
            "pairs": 46667,
            "gold": 3963,
            "scope": 761,
            "cross": 80
          },
          "5": {
            "pairs": 79183,
            "gold": 5115,
            "scope": 1048,
            "cross": 167
          }
        }
      },
      "costExcess": 465
    },
    "16": {
      "pathCount": 8000,
      "pathTokens": 211287,
      "uniqueTokens": 21456,
      "goldTokens": 11497,
      "goldCompletePath": 87,
      "goldAllMarginal": 135,
      "unrankedPairs": 701272,
      "goldArcs": 8576,
      "scopeArcs": 2223,
      "crossArcs": 1154,
      "rank": {
        "distance": {
          "1": {
            "pairs": 24422,
            "gold": 1408,
            "scope": 398,
            "cross": 34
          },
          "3": {
            "pairs": 79538,
            "gold": 4427,
            "scope": 828,
            "cross": 103
          },
          "5": {
            "pairs": 140061,
            "gold": 5856,
            "scope": 1164,
            "cross": 208
          }
        },
        "right": {
          "1": {
            "pairs": 24386,
            "gold": 2593,
            "scope": 251,
            "cross": 27
          },
          "3": {
            "pairs": 79165,
            "gold": 5060,
            "scope": 859,
            "cross": 102
          },
          "5": {
            "pairs": 139369,
            "gold": 6134,
            "scope": 1154,
            "cross": 200
          }
        },
        "crossPenalty": {
          "1": {
            "pairs": 24233,
            "gold": 1658,
            "scope": 424,
            "cross": 17
          },
          "3": {
            "pairs": 79565,
            "gold": 4614,
            "scope": 844,
            "cross": 87
          },
          "5": {
            "pairs": 140071,
            "gold": 5987,
            "scope": 1164,
            "cross": 186
          }
        }
      },
      "costExcess": 1057
    }
  }
}
```
## 复算及后续
按固定资产顺序传入本地文件，标准JS核心实际执行，Node文件包装未运行。只加载已审阅自有研究代码，外部内容仅作数据。应进一步研究无需gold的联合分词/词级结构消歧、方法目标语义与独立验证，不将更多K或词典命中等同理解。未修改生产、冻结、交接、证据等级、PR、训练、部署、主动CI或费用；真实原生、真机和独立留出未执行。
```js
const contents=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8"));
function study(contents){
 const [raw,dict,gdoc,adoc,pdoc]=contents,ck=(v,m)=>{if(!v)throw Error(m)},code=s=>s.split("```js\n")[1].split("\n```")[0],ac=code(adoc),gc=code(gdoc),pc=code(pdoc);
 const hash=Function(ac.slice(ac.indexOf(" function utf("),ac.indexOf(" const bytes=utf(raw)"))+"\nreturn s=>{let b=utf(s);return {bytes:b.length,sha:sha1(utf('blob '+b.length+'\\0').concat(b))}};")();
 const source=[hash(raw),hash(dict)];ck(source[0].sha==="af8cc878e7934b38ce3c1a266053100e7c47de6f"&&source[1].sha==="d7fee8237f26524b38eee220647e4c5d79f00de9","independent blob hashes");
 const G=Function("dict","const ck=(x,m)=>{if(!x)throw Error(m)};\n"+gc.slice(gc.indexOf("const words=new Set()"),gc.indexOf("function analyze(g)"))+"\nreturn {graph,cls,words};")(dict);
 const R=Function(pc.split(" const stat=()=>")[0]+"\nreturn {align,segments};\n}\nreturn study('');")();
 const K=[1,4,16],H=[1,3,5],modes=["distance","right","crossPenalty"],delim=new Set(Array.from("，,、：:；;。！？!?")),scope=new Set(["advcl","ccomp","xcomp","parataxis","conj","csubj","acl","mark","cc"]);
 // Exact k shortest paths in a DAG. Every tail contributes at most K
 // entries; rank cost then first end position then tail order.
 function paths(g,k){
  let n=g.length,p=Array.from({length:n+1},()=>[]);p[n]=[{cost:0,end:n,next:null,tailRank:0}];
  for(let i=n-1;i>=0;i--){
   let z=[];for(let e of g[i])for(let [r,t] of p[e.j].entries())z.push({cost:e.c+t.cost,start:i,end:e.j,skip:!!e.skip,next:t,tailRank:r});
   z.sort((a,b)=>a.cost-b.cost||a.end-b.end||a.tailRank-b.tailRank);p[i]=z.slice(0,k);
  }return p[0];
 }
 function tokens(p){let a=[];for(let t=p;t?.next;t=t.next)if(!t.skip)a.push({i:t.start,j:t.end});return a}
 const key=t=>t.i+":"+t.j,edge=(d,h)=>key(d)+">"+key(h);
 function rank(ts,chars,index,mode){
  const ws=ts.filter(t=>!chars.slice(t.i,t.j).every(c=>G.cls(c)==="p"));
  return ws.map((d,i)=>ws.map((h,j)=>({h,j,score:Math.abs(j-i)+(mode==="right"&&j<i?.25:0)+(mode==="crossPenalty"&&index[d.i]!==index[h.i]?1:0)})).filter(x=>x.j!==i).sort((a,b)=>a.score-b.score||a.j-b.j).map(x=>edge(d,x.h)));
 }
 const stat=()=>({pathCount:0,pathTokens:0,uniqueTokens:0,goldTokens:0,goldCompletePath:0,goldAllMarginal:0,unrankedPairs:0,goldArcs:0,scopeArcs:0,crossArcs:0,rank:{},costExcess:0});
 const out={source,words:G.words.size,sentences:0,tokens:0,arcs:0,scope:0,cross:0,unmappedCross:0,controls:0,metrics:Object.fromEntries(K.map(k=>[k,stat()]))};for(let o of Object.values(out.metrics))for(let m of modes)o.rank[m]=Object.fromEntries(H.map(h=>[h,{pairs:0,gold:0,scope:0,cross:0}]));
 for(let block of raw.trim().split(/\n\s*\n/)){
  const ls=block.split(/\r?\n/),text=ls.find(x=>x.startsWith("# text = "))?.slice(9);if(text===undefined)continue;
  let chars=Array.from(text),g=G.graph(chars,true),ps=paths(g,K.at(-1)),seg=R.segments(chars,delim);
  ck(ps.length>0&&ps.every((p,i)=>!i||ps[i-1].cost<=p.cost),"sorted paths");
  let ts=ps.map(tokens),sigs=new Set(ts.map(p=>JSON.stringify(p.map(key))));ck(sigs.size===ts.length,"distinct paths");
  // All candidate sets are constructed from raw text BEFORE accessing labels.
  let pred={};
  for(let k of K){
   let take=ts.slice(0,k),un=new Set(take.flatMap(t=>t.map(key))),pairs=new Set(),ranked=Object.fromEntries(modes.map(m=>[m,Object.fromEntries(H.map(h=>[h,new Set()]))]));
   for(let p of take){
    let r=rank(p,chars,seg.index,"distance");for(let v of r)for(let e of v)pairs.add(e);
    for(let m of modes){let r=m==="distance"?rank(p,chars,seg.index,"distance"):rank(p,chars,seg.index,m);for(let h of H)for(let v of r)for(let e of v.slice(0,h))ranked[m][h].add(e)}
   }
   pred[k]={take,un,pairs,ranked};
  }
  const rows=ls.filter(x=>/^\d+\t/.test(x)).map(x=>x.split("\t")),al=R.align(text,rows);ck(al,"gold alignment");
  const gold=rows.map(r=>{let [i,j]=al.positions.get(+r[0]);return {i,j}}),gs=new Set(gold.map(key)),goldSig=JSON.stringify(gold.map(key)),arcs=[];
  for(let i=0;i<rows.length;i++){let r=rows[i],h=+r[6],rel=r[7].split(":")[0];if(!h||rel==="punct"||r[3]==="PUNCT")continue;let d=gold[i],v=gold[h-1],sa=[...new Set(seg.index.slice(d.i,d.j).filter(x=>x>=0))],sb=[...new Set(seg.index.slice(v.i,v.j).filter(x=>x>=0))],mapped=sa.length===1&&sb.length===1,cross=mapped&&sa[0]!==sb[0];out.unmappedCross+=+!mapped;arcs.push({e:edge(d,v),scope:scope.has(rel),cross})}
  out.sentences++;out.tokens+=gold.length;out.arcs+=arcs.length;out.scope+=arcs.filter(a=>a.scope).length;out.cross+=arcs.filter(a=>a.cross).length;
  for(let k of K){
   let p=pred[k],o=out.metrics[k];o.pathCount+=p.take.length;o.pathTokens+=p.take.reduce((n,t)=>n+t.length,0);o.uniqueTokens+=p.un.size;o.goldTokens+=[...gs].filter(x=>p.un.has(x)).length;o.goldCompletePath+=+p.take.some(t=>JSON.stringify(t.map(key))===goldSig);o.goldAllMarginal+=+[...gs].every(x=>p.un.has(x));o.unrankedPairs+=p.pairs.size;o.goldArcs+=arcs.filter(x=>p.pairs.has(x.e)).length;o.scopeArcs+=arcs.filter(x=>x.scope&&p.pairs.has(x.e)).length;o.crossArcs+=arcs.filter(x=>x.cross&&p.pairs.has(x.e)).length;o.costExcess+=ps[Math.min(k,ps.length)-1].cost-ps[0].cost;
   for(let m of modes)for(let h of H){let z=o.rank[m][h],set=p.ranked[m][h];ck([...set].every(e=>p.pairs.has(e)),"path witness");z.pairs+=set.size;z.gold+=arcs.filter(x=>set.has(x.e)).length;z.scope+=arcs.filter(x=>x.scope&&set.has(x.e)).length;z.cross+=arcs.filter(x=>x.cross&&set.has(x.e)).length}
  }
 }
 // independent exhaustive short DAG path enumeration, sorted by cost then
 // lexicographic path endpoints. No gold data or hand-assigned ranking.
 let seed=20261126;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 for(let t=0;t<300;t++){
  let n=2+rnd(7),g=Array.from({length:n},(_,i)=>Array.from({length:Math.min(n-i,3)},(_,j)=>({j:i+j+1,c:rnd(4)})).filter((e,j)=>j===0||rnd(2))),all=[];
  function walk(i,c,p){if(i===n){all.push({cost:c,ends:p});return}for(let e of g[i])walk(e.j,c+e.c,[...p,e.j])}walk(0,0,[]);
  const cmp=(a,b)=>{for(let i=0;i<Math.min(a.length,b.length);i++)if(a[i]!==b[i])return a[i]-b[i];return a.length-b.length};
  all.sort((a,b)=>a.cost-b.cost||cmp(a.ends,b.ends));for(let k of K){let z=paths(g,k).map(p=>({cost:p.cost,ends:tokens(p).map(t=>t.j)}));ck(JSON.stringify(z)===JSON.stringify(all.slice(0,k)),"exhaustive K");out.controls++}
 }
 ck(out.sentences===500&&out.tokens===12665&&out.arcs===10395&&out.cross===1404,"cohort counts");
 for(let i=1;i<K.length;i++){let a=out.metrics[K[i-1]],b=out.metrics[K[i]];ck(a.goldTokens<=b.goldTokens&&a.goldArcs<=b.goldArcs,"nested path coverage");for(let m of modes)for(let h of H)ck(a.rank[m][h].gold<=b.rank[m][h].gold,"nested heads")}
 return out;
}
console.log(JSON.stringify(study(contents),null,2));
```
