# 自主认知：公开白话开发集的候选边界多样性与连续词序消融
2026-11-26。RESEARCH_CANDIDATE / FIXED_RESEARCH_CODE_EXECUTED / PUBLIC_SYNTHETIC_DEVELOPMENT / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线与重复控制
起始main 50b8c0f15b2de73af1bade87341c151f91159a23；核对12近期提交、15开放PR、v3.2与同步规程前12行、唯一产品交接前12行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、前轮条件方向研究前12行。Draft #63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍open/draft/unmerged，开发方固定公开回执 PUBLIC_DEVELOPMENT.json blob c5e51676e2bc5ea6184a9b324cc5150c14b89d20；条件0/5、账本修订0/10、主体1/4、数值单位7/23，原生指标没有因本轮改变。容器git ls-remote因DNS无法解析github.com，使用GitHub连接器读取并执行原研究JS，未重跑原生Python解释器、ASGI或设备。检索reference candidate/raw text reference/segmentation/word lattice/revision-aware/character ngram，读R116 bd97b82e4043d90def1015f244213f0cc8415309、R103 f8326373525aa598b5a78920947536cfc70b0d1b、R77 20c8df044c3a4d48f1819a7f401901d5ecde7a3e相关报告。已有R74角色跨度、R77跨轮边、R103统一跨度图、R116数量软绑定不重计。本轮增量为同预算下起点/终点多样化及连续字序二元组的固定消融，不宣称新通用分词算法、全库去重或已改善完整语义。
## 固定输入
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-25-raw-text-reference-search.md 16075b3ba567ee6dc3496300beab1417172a6c42
完整读取并核对连接器返回Git blob身份，非本地原始字节哈希复算。R74实际调用scan/gold、R77实际调用spans/search，原始代码未改；代码加载仅限固定项目自有研究源码，禁止执行任意网络文本。R74角色gold函数仅在评估使用。两语料32情节64轮167标注，67角色目标（约束25、行动30、修订12，可能与原标注重叠），12条唯一已标注引用。皆为ChatGPT辅助原创已见公开合成开发资料，非真人、训练、独立留出。未标注不视为负例，不计算precision、真实准确率、真实认知负担或科学准入。候选只输入文本；无领域/标签/ref输入，标注用于生成之后评分。研究者选择预算、二元组权重4及启发式，未拟合或训练，不能宣称盲测。
## A 同一角色预算的边界多样性
在R74已排序候选池中比较原序、起点循环、终点循环、交替起终点。起点循环优先选择当前未使用的起点中原排名最高者，全部已覆盖则清空该轮边界；禁止重复选择同一跨度。终点对称；交替每次在两类边界之间切换。全部模式严格使用同一每轮每角色候选预算，未增加词典、角色词面或搜索范围。保持原始UTF16坐标，不做真实词法切分。候选数量相等不等于实际CPU相等；额外线性扫描可能增加耗时，未测设备性能或优化实现。以原文精确起止+角色命中计分，复现R74六档原始命中22/31/34/37/42/42。42/67在原角色排序池可搜索，其余25无论如何重排也无法恢复（其中R74已知1个不在跨度域、24缺词面门）。
| 每角色K | 原排序 | 起点 | 终点 | 交替 | 实际候选总数（各模式） |
|---:|---:|---:|---:|---:|---:|
 | 1 | 22 | 22 | 22 | 22 | 66 | 
 | 3 | 31 | 32 | 26 | 32 | 198 | 
 | 5 | 34 | 38 | 27 | 34 | 326 | 
 | 10 | 37 | 39 | 32 | 39 | 606 | 
 | 20 | 42 | 41 | 40 | 41 | 1019 | 
 | 50 | 42 | 42 | 42 | 42 | 1523 | 
K=5起点38 vs34，完整覆盖有目标轮22 vs18；K=10起点及交替39 vs37，完整覆盖23 vs21，新增行动S01.2“申请培训岗”和S06.1“参加长跑活动”。K=20起点和交替41 vs42，均少1行动；终点在K=3/5/10/20普遍退步，不能把多样性无条件替代旧排序。K=50所有模式42。绝对改善限已有标注跨度，未确认角色/条件/指代正确，未测产品追问。
## B 跨轮引用端点预算与词序
沿R77允许一个内部标点的跨度池，比较原排序、按起点组轮流取候选、原排序+连续二元字组Jaccard乘4、两者组合。保留原4倍字符集合Jaccard及修订词面分数；不跨标点组成二元组、重复二元组只计一次、零集合相似度0。此为局部顺序证据，并非真正分词、句法或概念同义。严格同一两端预算，完整枚举候选边；所有原排序边的分数及精确位置逐项与实际R77 search返回核对。保留原始方向（第2轮引用第1轮），不能推广任意多轮或隐含修订。每情节端点K至100，最多10000边；仅候选计数限制，非全请求CPU/内存预算。
| K | 模式 | 两端覆盖/12 | top1 | top5 | top20 | top100 | 累计边数 |
|---:|---|---:|---:|---:|---:|---:|---:|
 | 10 | original | 7 | 3 | 6 | 7 | 7 | 3200 | 
 | 10 | diverse | 8 | 3 | 6 | 7 | 8 | 3200 | 
 | 10 | order | 7 | 4 | 6 | 7 | 7 | 3200 | 
 | 10 | combined | 8 | 4 | 6 | 7 | 8 | 3200 | 
 | 30 | original | 10 | 3 | 6 | 6 | 9 | 28800 | 
 | 30 | diverse | 12 | 3 | 6 | 8 | 11 | 28800 | 
 | 30 | order | 10 | 4 | 6 | 6 | 9 | 28800 | 
 | 30 | combined | 12 | 4 | 6 | 7 | 11 | 28800 | 
 | 100 | original | 12 | 3 | 6 | 6 | 10 | 313700 | 
 | 100 | diverse | 12 | 3 | 6 | 6 | 10 | 313700 | 
 | 100 | order | 12 | 4 | 6 | 7 | 10 | 313700 | 
 | 100 | combined | 12 | 4 | 6 | 7 | 10 | 313700 | 
K=30起点多样化两端10→12，top100 9→11，top20 6→8；组合top20只有7，说明词序加分可能抵消部分改善。K=100原与多样化均12端点覆盖，top100 10；词序使top1 3→4、top20 6→7，但L03.2.1原735→词序774，L08.2.2原23→26，L15.2.1原146→150，均为退步。K=30多样化累计28800条边，K=100原排序313700条边，前者top100 11/12而后者10/12；不等于90.8%实际性能改善，候选池大小、额外排序与设备耗时未测。边覆盖及排序不证明唯一修订对象或可提交账本；旧许可、语义歧义及真实事实仍由宿主确认。
## C 接入边界
建议将多样化作为可配置候选生成策略（保留原路径及明确预算），连续字序作为软证据，原义务缺失仍outside=true。所有研究候选authority NONE，不自行更新账本或正式数学参数。R74角色池的25个缺失目标及跨轮低排名仍为关键瓶颈，后续应测词法候选、组合角色及原生端到端投影，而非继续盲目扩大K。完整语言能力、分词词典或统计模型训练仍未实现/授权；开发方原生报告不重复计为本轮运行。研究者自行选定边界策略及预算；独立轨保管未见案例、产品轨维护唯一交接、模型轨提供可信义务及计算资格。无个人数据、新外部AI依赖、生产改动、PR合并、部署、CI主动执行、训练或费用。R073、PESEN、冻结和历史证据不变。
## D 复算
固定四个文件全文按顺序作为contents传入，Node标准JS。以下整合代码实际执行两次，完整输出相同；与先前分别运行的角色和边实验关键计数核对一致，10个控制均通过。代码和逐引用排名及两条角色变化随报告归档，无单独ZIP。
```js
function replay(contents){
 const ck=(b,m)=>{if(!b)throw Error(m)},docs=contents.slice(0,2).map(JSON.parse),obj=(ks,fn)=>Object.fromEntries(ks.map(k=>[k,fn(k)]));
 function load(s,marker,names){let code=s.split("```js\n")[1].split("\n```")[0].split(marker)[0];return Function(code+"\nreturn {"+names+"};\n}\nreturn experiment();")()}
 const R=load(contents[2]," const blank=","scan,gold"),Q=load(contents[3]," const pos=","spans,search");
 const roles=["constraint","action","revision"],ks=[1,3,5,10,20,50],modes=["original","start","end","alternating"],ek=[10,30,100],em=["original","diverse","order","combined"],top=[1,5,20,100];
 function diversify(a,k,mode){if(mode==="original")return a.slice(0,k);let x=[],used=new Set(),ss=new Set(),se=new Set();while(x.length<Math.min(a.length,k)){let group=mode==="start"?"start":mode==="end"?"end":x.length%2?"end":"start",seen=group==="start"?ss:se;let p=a.find(v=>!used.has(v)&&!seen.has(v[group]));if(!p){seen.clear();p=a.find(v=>!used.has(v))}ck(!!p,"available");x.push(p);used.add(p);seen.add(p[group])}return x}
 function diverse(a,k){let g=new Map();for(const s of a){if(!g.has(s.start))g.set(s.start,[]);g.get(s.start).push(s)}let z=[];while(z.length<k){let more=false;for(const q of g.values()){if(q.length){z.push(q.shift());more=true;if(z.length===k)break}}if(!more)break}return z}
 const punct=/[，。！？；、：,.!?;:\s]/u;
 function grams(s){let a=[...s],z=new Set();for(let i=1;i<a.length;i++)if(!punct.test(a[i-1])&&!punct.test(a[i]))z.add(a[i-1]+a[i]);return z}
 function jac(a,b){let n=0;for(const x of a)if(b.has(x))n++;return n/(a.size+b.size-n||1)}
 function rank(a,b,k,m){let x=m==="diverse"||m==="combined"?diverse(a,k):a.slice(0,k),y=m==="diverse"||m==="combined"?diverse(b,k):b.slice(0,k);let A=new Map(x.map(s=>[s,grams(s.text)])),B=new Map(y.map(s=>[s,grams(s.text)])),edges=[];for(let p of x)for(let q of y)edges.push({a:p,b:q,score:p.score+q.score+4*jac(p.chars,q.chars)+2*Number(q.cue)+(m==="order"||m==="combined"?4*jac(A.get(p),B.get(q)):0)});edges.sort((p,q)=>q.score-p.score||p.a.start-q.a.start||p.a.end-q.a.end||p.b.start-q.b.start||p.b.end-q.b.end);return {x,y,edges}}
 const span=(t,s)=>{let p=t.indexOf(s);ck(p>=0&&p===t.lastIndexOf(s),"unique");return [p,p+s.length]},same=(s,a)=>s.start===a[0]&&s.end===a[1],ann=(t,d)=>d?t.proposal.claims:t.claims,quote=(a,d)=>d?a.quote:a.span;
 let o={episodes:0,turns:0,annotations:0,roleTargets:0,rankable:0,roleTurns:0,refs:0,role:obj(ks,k=>obj(modes,m=>({hits:0,candidates:0,allTurns:0,byRole:obj(roles,r=>[0,0])}))),edge:obj(ek,k=>obj(em,m=>({endpoints:0,hits:obj(top,n=>0),edges:0,candidates:0}))),roleChanges:[],edgeRows:[]};
 for(let d=0;d<2;d++)for(let ep of docs[d].cases){
  o.episodes++;ck(ep.turns.length===2,"two turns");let t=ep.turns.map(v=>v.text),a=Q.spans(t[0],true),b=Q.spans(t[1],true),rr=obj(ek,k=>obj(em,m=>rank(a,b,k,m)));
  for(let k of ek){let z=rr[k].original.edges,q=Q.search(t[0],t[1],k,true);ck(q.status==="CANDIDATES_ONLY"&&z.length===q.edges.length&&z.every((e,i)=>e.score===q.edges[i].score&&same(e.a,[q.edges[i].a.start,q.edges[i].a.end])&&same(e.b,[q.edges[i].b.start,q.edges[i].b.end])),"R77 parity");for(let m of em){let p=rr[k][m],s=o.edge[k][m];ck(p.x.length<=k&&p.y.length<=k,"budget");s.edges+=p.edges.length;s.candidates+=p.x.length+p.y.length}}
  for(let ti=0;ti<2;ti++){let p=R.scan(t[ti]);ck(p.status==="CANDIDATES_ONLY","scan");o.turns++;let c=obj(ks,k=>obj(modes,m=>obj(roles,r=>diversify(p.ranked[r],k,m))));for(let k of ks)for(let m of modes)for(let r of roles){let v=c[k][m][r];ck(v.length===Math.min(k,p.ranked[r].length)&&new Set(v).size===v.length,"budget");o.role[k][m].candidates+=v.length}
   let labels=ann(ep.turns[ti],d);o.annotations+=labels.length;let targets=labels.flatMap(x=>R.gold(d,x).map(r=>({r,q:quote(x,d),s:span(t[ti],quote(x,d))})));o.roleTargets+=targets.length;o.roleTurns+=+(targets.length>0);const hit=(a,g)=>a.some(x=>same(x,g.s));
   for(let g of targets){o.rankable+=+hit(p.ranked[g.r],g);let row={id:ep.id+"."+(ti+1),role:g.r,quote:g.q,top10:{}};for(let k of ks)for(let m of modes){let s=o.role[k][m],h=+hit(c[k][m][g.r],g);s.hits+=h;s.byRole[g.r][0]+=h;s.byRole[g.r][1]++;if(k===10)row.top10[m]=h}if(row.top10.original!==row.top10.alternating)o.roleChanges.push(row)}for(let k of ks)for(let m of modes)if(targets.length&&targets.every(g=>hit(c[k][m][g.r],g)))o.role[k][m].allTurns++}
  let prev=ann(ep.turns[0],d),cur=ann(ep.turns[1],d);
  for(let i=0;i<cur.length;i++){let q=cur[i],f=d?q.ref:q.supersedes;if(typeof f!=="string")continue;let ix=[];if(d){let m=/^([^.]+)\.(\d+)\.(\d+)$/.exec(f);if(m&&m[1]===ep.id&&+m[2]===1)ix=[+m[3]-1]}else{let m=/^([^:]+):t(\d+):(.+)$/.exec(f);if(m&&m[1]===ep.id&&+m[2]===0)ix=prev.map((v,j)=>v.field===m[3]?j:-1).filter(j=>j>=0)}if(ix.length!==1)continue;o.refs++;let A=span(t[0],quote(prev[ix[0]],d)),B=span(t[1],quote(q,d)),row={id:ep.id+".2."+(i+1),ranks:{}};for(let k of ek)for(let m of em){let p=rr[k][m],s=o.edge[k][m],covered=p.x.some(v=>same(v,A))&&p.y.some(v=>same(v,B)),j=p.edges.findIndex(e=>same(e.a,A)&&same(e.b,B));ck((j>=0)===covered,"edge coverage");s.endpoints+=+covered;for(let n of top)s.hits[n]+=+(j>=0&&j<n);if(k===100)row.ranks[m]=j<0?null:j+1}o.edgeRows.push(row)}
 }
 ck(o.episodes===32&&o.turns===64&&o.annotations===167&&o.roleTargets===67&&o.rankable===42&&o.refs===12,"coverage");ck(ks.every((k,i)=>o.role[k].original.hits===[22,31,34,37,42,42][i]),"R74 parity");
 let x=[{start:0,end:1},{start:0,end:2},{start:1,end:2},{start:2,end:3}];ck(diversify(x,3,"start").map(v=>v.start).join()==="0,1,2","start");ck(diversify(x,3,"end").map(v=>v.end).join()==="1,2,3","end");ck(diversify(x,0,"alternating").length===0,"zero");ck(diversify(x,99,"alternating").length===4,"cap");ck(jac(grams("甲乙丙"),grams("丙乙甲"))===0,"order");ck(grams("甲，乙").size===0,"punct");ck(grams("甲甲甲").size===1,"repeat");ck(jac(grams("甲"),grams("乙"))===0,"empty");let z=diverse(Q.spans("甲乙丙丁。戊己庚辛",true),3);ck(z.length===3&&new Set(z.map(v=>v.start)).size===3,"diversity");ck(diverse(x,0).length===0,"zero diversity");o.controls=10;return o
}
const contents=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8"));
console.log(JSON.stringify(replay(contents),null,2));
```
## E 复算输出
角色表元组依次为命中、候选总数、完整覆盖轮数、约束[命中,分母]、行动[命中,分母]、修订[命中,分母]。边表字段详见代码。
```json
{
  "episodes": 32,
  "turns": 64,
  "annotations": 167,
  "roleTargets": 67,
  "rankable": 42,
  "roleTurns": 44,
  "refs": 12,
  "role": {
    "1": {
      "original": [
        22,
        66,
        11,
        [
          10,
          25
        ],
        [
          6,
          30
        ],
        [
          6,
          12
        ]
      ],
      "start": [
        22,
        66,
        11,
        [
          10,
          25
        ],
        [
          6,
          30
        ],
        [
          6,
          12
        ]
      ],
      "end": [
        22,
        66,
        11,
        [
          10,
          25
        ],
        [
          6,
          30
        ],
        [
          6,
          12
        ]
      ],
      "alternating": [
        22,
        66,
        11,
        [
          10,
          25
        ],
        [
          6,
          30
        ],
        [
          6,
          12
        ]
      ]
    },
    "3": {
      "original": [
        31,
        198,
        15,
        [
          14,
          25
        ],
        [
          10,
          30
        ],
        [
          7,
          12
        ]
      ],
      "start": [
        32,
        198,
        16,
        [
          14,
          25
        ],
        [
          10,
          30
        ],
        [
          8,
          12
        ]
      ],
      "end": [
        26,
        198,
        13,
        [
          12,
          25
        ],
        [
          7,
          30
        ],
        [
          7,
          12
        ]
      ],
      "alternating": [
        32,
        198,
        16,
        [
          14,
          25
        ],
        [
          10,
          30
        ],
        [
          8,
          12
        ]
      ]
    },
    "5": {
      "original": [
        34,
        326,
        18,
        [
          14,
          25
        ],
        [
          11,
          30
        ],
        [
          9,
          12
        ]
      ],
      "start": [
        38,
        326,
        22,
        [
          15,
          25
        ],
        [
          14,
          30
        ],
        [
          9,
          12
        ]
      ],
      "end": [
        27,
        326,
        14,
        [
          13,
          25
        ],
        [
          7,
          30
        ],
        [
          7,
          12
        ]
      ],
      "alternating": [
        34,
        326,
        18,
        [
          14,
          25
        ],
        [
          11,
          30
        ],
        [
          9,
          12
        ]
      ]
    },
    "10": {
      "original": [
        37,
        606,
        21,
        [
          15,
          25
        ],
        [
          13,
          30
        ],
        [
          9,
          12
        ]
      ],
      "start": [
        39,
        606,
        23,
        [
          15,
          25
        ],
        [
          15,
          30
        ],
        [
          9,
          12
        ]
      ],
      "end": [
        32,
        606,
        17,
        [
          14,
          25
        ],
        [
          10,
          30
        ],
        [
          8,
          12
        ]
      ],
      "alternating": [
        39,
        606,
        23,
        [
          15,
          25
        ],
        [
          15,
          30
        ],
        [
          9,
          12
        ]
      ]
    },
    "20": {
      "original": [
        42,
        1019,
        26,
        [
          16,
          25
        ],
        [
          17,
          30
        ],
        [
          9,
          12
        ]
      ],
      "start": [
        41,
        1019,
        25,
        [
          16,
          25
        ],
        [
          16,
          30
        ],
        [
          9,
          12
        ]
      ],
      "end": [
        40,
        1019,
        24,
        [
          16,
          25
        ],
        [
          15,
          30
        ],
        [
          9,
          12
        ]
      ],
      "alternating": [
        41,
        1019,
        25,
        [
          16,
          25
        ],
        [
          16,
          30
        ],
        [
          9,
          12
        ]
      ]
    },
    "50": {
      "original": [
        42,
        1523,
        26,
        [
          16,
          25
        ],
        [
          17,
          30
        ],
        [
          9,
          12
        ]
      ],
      "start": [
        42,
        1523,
        26,
        [
          16,
          25
        ],
        [
          17,
          30
        ],
        [
          9,
          12
        ]
      ],
      "end": [
        42,
        1523,
        26,
        [
          16,
          25
        ],
        [
          17,
          30
        ],
        [
          9,
          12
        ]
      ],
      "alternating": [
        42,
        1523,
        26,
        [
          16,
          25
        ],
        [
          17,
          30
        ],
        [
          9,
          12
        ]
      ]
    }
  },
  "edge": {
    "10": {
      "original": {
        "endpoints": 7,
        "hits": {
          "1": 3,
          "5": 6,
          "20": 7,
          "100": 7
        },
        "edges": 3200,
        "candidates": 640
      },
      "diverse": {
        "endpoints": 8,
        "hits": {
          "1": 3,
          "5": 6,
          "20": 7,
          "100": 8
        },
        "edges": 3200,
        "candidates": 640
      },
      "order": {
        "endpoints": 7,
        "hits": {
          "1": 4,
          "5": 6,
          "20": 7,
          "100": 7
        },
        "edges": 3200,
        "candidates": 640
      },
      "combined": {
        "endpoints": 8,
        "hits": {
          "1": 4,
          "5": 6,
          "20": 7,
          "100": 8
        },
        "edges": 3200,
        "candidates": 640
      }
    },
    "30": {
      "original": {
        "endpoints": 10,
        "hits": {
          "1": 3,
          "5": 6,
          "20": 6,
          "100": 9
        },
        "edges": 28800,
        "candidates": 1920
      },
      "diverse": {
        "endpoints": 12,
        "hits": {
          "1": 3,
          "5": 6,
          "20": 8,
          "100": 11
        },
        "edges": 28800,
        "candidates": 1920
      },
      "order": {
        "endpoints": 10,
        "hits": {
          "1": 4,
          "5": 6,
          "20": 6,
          "100": 9
        },
        "edges": 28800,
        "candidates": 1920
      },
      "combined": {
        "endpoints": 12,
        "hits": {
          "1": 4,
          "5": 6,
          "20": 7,
          "100": 11
        },
        "edges": 28800,
        "candidates": 1920
      }
    },
    "100": {
      "original": {
        "endpoints": 12,
        "hits": {
          "1": 3,
          "5": 6,
          "20": 6,
          "100": 10
        },
        "edges": 313700,
        "candidates": 6337
      },
      "diverse": {
        "endpoints": 12,
        "hits": {
          "1": 3,
          "5": 6,
          "20": 6,
          "100": 10
        },
        "edges": 313700,
        "candidates": 6337
      },
      "order": {
        "endpoints": 12,
        "hits": {
          "1": 4,
          "5": 6,
          "20": 7,
          "100": 10
        },
        "edges": 313700,
        "candidates": 6337
      },
      "combined": {
        "endpoints": 12,
        "hits": {
          "1": 4,
          "5": 6,
          "20": 7,
          "100": 10
        },
        "edges": 313700,
        "candidates": 6337
      }
    }
  },
  "roleChanges": [
    {
      "id": "S01.2",
      "role": "action",
      "quote": "申请培训岗",
      "top10": {
        "original": 0,
        "start": 1,
        "end": 0,
        "alternating": 1
      }
    },
    {
      "id": "S06.1",
      "role": "action",
      "quote": "参加长跑活动",
      "top10": {
        "original": 0,
        "start": 1,
        "end": 0,
        "alternating": 1
      }
    }
  ],
  "edgeRows": [
    {
      "id": "L03.2.1",
      "ranks": {
        "original": 735,
        "diverse": 623,
        "order": 774,
        "combined": 652
      }
    },
    {
      "id": "L08.2.2",
      "ranks": {
        "original": 23,
        "diverse": 22,
        "order": 26,
        "combined": 24
      }
    },
    {
      "id": "L15.2.1",
      "ranks": {
        "original": 146,
        "diverse": 132,
        "order": 150,
        "combined": 136
      }
    },
    {
      "id": "S01.2.1",
      "ranks": {
        "original": 2,
        "diverse": 2,
        "order": 1,
        "combined": 1
      }
    },
    {
      "id": "S02.2.1",
      "ranks": {
        "original": 21,
        "diverse": 21,
        "order": 13,
        "combined": 13
      }
    },
    {
      "id": "S03.2.1",
      "ranks": {
        "original": 3,
        "diverse": 3,
        "order": 2,
        "combined": 2
      }
    },
    {
      "id": "S04.2.1",
      "ranks": {
        "original": 1,
        "diverse": 1,
        "order": 1,
        "combined": 1
      }
    },
    {
      "id": "S08.2.1",
      "ranks": {
        "original": 1,
        "diverse": 1,
        "order": 1,
        "combined": 1
      }
    },
    {
      "id": "S10.2.1",
      "ranks": {
        "original": 1,
        "diverse": 1,
        "order": 1,
        "combined": 1
      }
    },
    {
      "id": "S11.2.1",
      "ranks": {
        "original": 69,
        "diverse": 58,
        "order": 41,
        "combined": 39
      }
    },
    {
      "id": "S12.2.1",
      "ranks": {
        "original": 79,
        "diverse": 74,
        "order": 79,
        "combined": 74
      }
    },
    {
      "id": "S13.2.1",
      "ranks": {
        "original": 2,
        "diverse": 2,
        "order": 2,
        "combined": 2
      }
    }
  ],
  "controls": 10
}
```
