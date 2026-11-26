# 自主认知：组合角色候选、量词法及原始遗漏恢复实验
2026-11-26。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / PUBLIC_SYNTHETIC_DEVELOPMENT / POST_INSPECTION_DIAGNOSTIC / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线与去重
起始main 78508bb9de3b0b1ef50f7a66300418891b228219；核对12近期提交、15开放PR、v3.2/同步规程/唯一产品交接/前轮研究前14行，唯一交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07。Draft #63 head 734686980b19da9291bdd08b67d4e2519c011acf仍draft/unmerged。检索role candidate/contextual role/cue-free/open span/coordination/candidate obligation；审阅R102统一义务接口 bdf9bc7a42f33d9c48708970d6ac03a78ef276de及R115原词法源码，继承R74/R77及前轮边界多样性研究。新增在同一原文上将外部角色线索、选择分支、桥接范围、模态与数量词法、同句编辑提示组合成候选，而非重复R115数值往返或R102义务接口。全库去重有限。固定#63未重新运行，条件0/5、账本修订0/10等原生指标不变。
## 固定资产
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-25-raw-text-reference-search.md 16075b3ba567ee6dc3496300beab1417172a6c42
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
实际完整读取并核对连接器blob，非独立Git字节复算。仅执行已审阅固定项目自有JS，生产禁止执行外部文档。R74 scan/gold/cues、R77 spans、R115 lexical均直接复用。两套32情节64轮167原标注，67角色目标（25约束30行动12修订）及原候选遗漏25（9/13/3）。已见公开原创ChatGPT辅助合成开发材料；本轮先查看25项遗漏，再设计组合候选，属于事后开发诊断，不能宣称盲测、独立泛化、训练、真实用户或真实准确率。算法运行只输入当前原文及是否有前轮，不读标签、领域、目标字段或标注ref。旧有词法68项实际重新核对一致。
## 方法
保留R74旧候选原分数，新增候选来自R77长度≤24 UTF16、最多一个内部标点的跨度；候选角色为软假设，不赋予权限。context：同一分句外部现有角色词面证据，跨度边界基础分+2减有限距离；choice：或者/还是/或/和两侧端点候选，基础分+4，仅作为行动备选证据，和尤其可能是并列实体而非选择。bridge：跨一个内部标点且原角色提示在内，加4。包括跨强句界的候选，仅研究几何覆盖，正式解析不得跨句自动绑定。modal：限定通用许可/义务功能词只有、只能、不得、不许、不要、不可、别、务必、必须、得，加4；numeric_modal：R115完整数量词法在跨度内且最早/最晚/前/后/以内/以外/以上/以下等时间比较提示，加4；repair：存在前轮、当前跨度包含R115量、同一强句含前面/之前/原来/说错/不对/更正/修正，加3。后四类通用功能词由研究者检查遗漏后选定，不增加领域业务词表，但仍属有限提示规则，不是通用组合语义。只有数值而无模态提示不自动产生新硬约束。新跨度多证据取最大分，既有候选分数不改；同分按位置。每角色K=1/5/10/20/50；额外比较前轮起点轮流策略。单角色完整候选池可增加，K相同是上限相同而非实际输出数量或CPU相同，报告实际候选总数，禁止声称等资源性能提升。
## 结果：完整候选池
| 模式 | 67项命中 | 恢复原遗漏 | 候选总数 | 约束 | 行动 | 修订 |
|---|---:|---:|---:|---:|---:|---:|
| base | 42 | 0 | 1584 | 16/25 | 17/30 | 9/12 |
| context | 43 | 1 | 4007 | 16/25 | 18/30 | 9/12 |
| choice | 51 | 9 | 4107 | 16/25 | 26/30 | 9/12 |
| bridge | 52 | 10 | 8251 | 16/25 | 27/30 | 9/12 |
| modal | 59 | 17 | 8602 | 23/25 | 27/30 | 9/12 |
| numeric_modal | 59 | 17 | 8617 | 23/25 | 27/30 | 9/12 |
| repair | 60 | 18 | 8636 | 23/25 | 27/30 | 10/12 |
第一轮单独实验context/choice/bridge结果43/51/52，本轮完整重算一致。完整池结果仅指精确原文+粗角色候选是否存在；未测角色真值、条件逻辑、主体、单位、引用目标、真正解析树或权限。新增提示会产生错误角色假设，不使用未标注作为负例，无法估计precision。完整池比原算法增大，不等于实际推荐质量提高。
## 有限预算结果（原顺序）
| K | 模式 | 命中 | 较同K基线新增 | 丢失 | 实际候选数 | 完整目标轮 |
|---:|---|---:|---:|---:|---:|---:|
| 1 | base | 22 | 0 | 0 | 66 | 11 |
| 1 | context | 22 | 0 | 0 | 66 | 11 |
| 1 | choice | 23 | 1 | 0 | 74 | 11 |
| 1 | bridge | 23 | 1 | 0 | 74 | 11 |
| 1 | modal | 23 | 4 | 3 | 85 | 13 |
| 1 | numeric_modal | 23 | 4 | 3 | 87 | 13 |
| 1 | repair | 23 | 4 | 3 | 88 | 13 |
| 5 | base | 34 | 0 | 0 | 326 | 18 |
| 5 | context | 34 | 0 | 0 | 330 | 18 |
| 5 | choice | 38 | 4 | 0 | 369 | 18 |
| 5 | bridge | 38 | 4 | 0 | 369 | 18 |
| 5 | modal | 43 | 9 | 0 | 424 | 23 |
| 5 | numeric_modal | 43 | 9 | 0 | 432 | 23 |
| 5 | repair | 44 | 10 | 0 | 437 | 24 |
| 10 | base | 37 | 0 | 0 | 606 | 21 |
| 10 | context | 37 | 0 | 0 | 660 | 21 |
| 10 | choice | 44 | 7 | 0 | 727 | 23 |
| 10 | bridge | 44 | 7 | 0 | 727 | 23 |
| 10 | modal | 50 | 13 | 0 | 829 | 28 |
| 10 | numeric_modal | 50 | 13 | 0 | 842 | 28 |
| 10 | repair | 51 | 14 | 0 | 851 | 29 |
| 20 | base | 42 | 0 | 0 | 1019 | 26 |
| 20 | context | 42 | 0 | 0 | 1290 | 26 |
| 20 | choice | 50 | 8 | 0 | 1380 | 29 |
| 20 | bridge | 50 | 8 | 0 | 1405 | 29 |
| 20 | modal | 57 | 15 | 0 | 1560 | 35 |
| 20 | numeric_modal | 57 | 15 | 0 | 1575 | 35 |
| 20 | repair | 58 | 16 | 0 | 1584 | 36 |
| 50 | base | 42 | 0 | 0 | 1523 | 26 |
| 50 | context | 42 | 0 | 0 | 2724 | 26 |
| 50 | choice | 50 | 8 | 0 | 2824 | 29 |
| 50 | bridge | 51 | 9 | 0 | 3286 | 29 |
| 50 | modal | 58 | 16 | 0 | 3537 | 36 |
| 50 | numeric_modal | 58 | 16 | 0 | 3552 | 36 |
| 50 | repair | 59 | 17 | 0 | 3561 | 37 |
同K基线为R74原始顺序；diverse表为同起点轮流基线，不能跨策略混报。保留全部退步及正例未覆盖，见完整结果；标注情节族不是独立样本，未作统计显著性结论。
## 负面诊断与安全边界
首次整合控制预期最早八点能由R115量词法支持，实际失败：R115将数字邻接点作为小数歧义而排除；保留原词法，不修改实验主算法，改用明确的三天前正向控制，最早八点作为已知缺口。全量重跑后10项控制通过。另4个事后设计反例（并列物品、他人转述、过去时间事实、含过去提示但无真实修订）检查候选过宽。候选存在不能作确认、写入、正式硬门或推荐。所有结果的宿主信封authority NONE/outside true，真实原生适配尚无；原历史R74输出仅研究对象。原语料中未标注不能解释为无义务，未命中不能解释为无约束。原生解释器、真实会话、权限、数学及设备均未运行，未测独立样本；本轮不声称完成分词或自研模型训练。正式接入须保留独立义务及完整语义资格，所有人称、时态、引语、作用域、逻辑、修订目标与来源需要宿主确认。下一步应以候选作用域和多候选竞争减少这些反例，并研究从原文到可信义务的可复算连接，不能仅扩展提示词。自行选择规则、权重、上限，未变更已授权任务、唯一交接、历史冻结、R073/PESEN或证据等级；未修改生产、合并PR、部署、训练、外部AI运行依赖、主动CI或增加费用。
## 复算
固定五份文件全文按顺序作为contents传入，Node标准JS。整合代码实际运行两次完整结果一致，原始第一阶段计数再次核对。报告内含全部代码、原遗漏逐项及汇总，不另造ZIP。
```js
function experiment(contents){
 const ck=(x,m)=>{if(!x)throw Error(m)},docs=contents.slice(0,2).map(JSON.parse),obj=(a,f)=>Object.fromEntries(a.map(k=>[k,f(k)])),key=x=>x.start+":"+x.end;
 function load(s,mark,names){let x=s.split("```js\n")[1].split("\n```")[0].split(mark)[0];return Function(x+"\nreturn {"+names+"};\n}\nreturn experiment();")()}
 const R=load(contents[2]," const blank=","scan,gold,cues"),Q=load(contents[3]," const pos=","spans");
 let code=contents[4].split("```js\n")[1].split("\n```")[0];let L=Function(code.slice(code.indexOf("function experiment(A)")).split(" let out={corpusTurns:")[0]+"\nreturn {lexical};\n}\nreturn experiment({});")();
 const roles=["constraint","action","revision"],ks=[1,5,10,20,50],modes=["base","context","choice","bridge","modal","numeric_modal","repair"],rank=(a,b)=>b.score-a.score||a.start-b.start||a.end-b.end;
 const connectors=["或者","还是","或","和"],punct=/[，。！？；、：,.!?;:\s]/u;
 const modal=["只有","只能","不得","不许","不要","不可","别","务必","必须","得"],temporal=["最早","最晚","前","后","以内","以外","以上","以下"],repair=["前面","之前","原来","说错","不对","更正","修正"];
 function propose(text,hasPrior){
  let z=R.scan(text);ck(z.status==="CANDIDATES_ONLY","scan");
  const all=Q.spans(text,true),old=obj(roles,r=>new Map(z.ranked[r].map(v=>[key(v),v]))),links=[],numbers=L.lexical(text).items;
  for(const c of z.clauses)for(let p=c.start;p<c.end;p++){const w=connectors.find(w=>text.startsWith(w,p)&&p+w.length<c.end&&p>c.start);if(w){links.push({p,q:p+w.length,c});p+=w.length-1}}
  const hits=obj(roles,r=>R.cues[r].flatMap(w=>{let a=[];for(let p=text.indexOf(w);p>=0;p=text.indexOf(w,p+1))a.push({start:p,end:p+w.length});return a}));
  const alt=obj(modes,m=>obj(roles,r=>new Map(old[r])));
  let strong=[];for(let i=0,j=0;i<=text.length;i++)if(i===text.length||/[。！？；.!?;]/u.test(text[i])){strong.push({start:j,end:i,text:text.slice(j,i)});j=i+1}
  for(let v of all){let bridged=[...v.text].some(ch=>punct.test(ch)),c=z.clauses.find(c=>c.start<=v.start&&v.end<=c.end),s=strong.find(c=>c.start<=v.start&&v.end<=c.end),num=numbers.some(n=>n.start>=v.start&&n.end<=v.end);
   for(let r of roles){if(old[r].has(key(v)))continue;
    let h=c?hits[r].filter(h=>h.start>=c.start&&h.end<=c.end):[],dist=h.length?Math.min(...h.map(h=>Math.max(0,h.start-v.end,v.start-h.end))):Infinity;
    let contextual=Number.isFinite(dist)?v.score+2-Math.min(dist,12)/4:null;
    let choice=r==="action"&&links.some(l=>v.start>=l.c.start&&v.end<=l.c.end&&(v.end===l.p||v.start===l.q))?v.score+4:null;
    let directBridge=bridged&&R.cues[r].some(w=>v.text.includes(w))?v.score+4:null;
    let mod=r==="constraint"&&!bridged&&modal.some(w=>v.text.includes(w))?v.score+4:null;
    let tm=r==="constraint"&&!bridged&&num&&temporal.some(w=>v.text.includes(w))?v.score+4:null;
    let rep=r==="revision"&&!bridged&&hasPrior&&num&&s&&repair.some(w=>s.text.includes(w))?v.score+3:null;
    for(let m of modes.slice(1)){let mi=modes.indexOf(m),scores=[contextual,...(mi>=2?[choice]:[]),...(mi>=3?[directBridge]:[]),...(mi>=4?[mod]:[]),...(mi>=5?[tm]:[]),...(mi>=6?[rep]:[])].filter(x=>x!==null);if(scores.length&&(!bridged||mi>=3))alt[m][r].set(key(v),{...v,score:Math.max(...scores),authority:"NONE",outside:true})}
   }
  }
  return {sets:obj(modes,m=>obj(roles,r=>[...alt[m][r].values()].sort(rank))),numbers:numbers.length,authority:"NONE",outside:true}
 }
 function diversify(a,k){let g=new Map();for(let v of a){if(!g.has(v.start))g.set(v.start,[]);g.get(v.start).push(v)}let x=[];while(x.length<k){let more=false;for(let q of g.values()){if(q.length){x.push(q.shift());more=true;if(x.length===k)break}}if(!more)break}return x}
 const blank=()=>({hit:0,newHit:0,lost:0,count:0,allTurns:0,roles:obj(roles,r=>[0,0])});
 let o={episodes:0,turns:0,annotations:0,targets:0,missing:0,numbers:0,roleMissing:obj(roles,r=>0),full:obj(modes,m=>({hit:0,added:0,count:0,roles:obj(roles,r=>[0,0])})),metrics:obj(ks,k=>obj(modes,m=>blank())),diverse:obj(ks,k=>obj(modes,m=>blank())),rows:[],controls:0,contrast:[]};
 const hit=(a,g)=>a.some(x=>key(x)===g.k);
 for(let d=0;d<2;d++)for(let ep of docs[d].cases){o.episodes++;for(let ti=0;ti<ep.turns.length;ti++){
  let t=ep.turns[ti],p=propose(t.text,ti>0);o.turns++;o.numbers+=p.numbers;
  let choices=obj(ks,k=>obj(modes,m=>obj(roles,r=>p.sets[m][r].slice(0,k)))),div=obj(ks,k=>obj(modes,m=>obj(roles,r=>diversify(p.sets[m][r],k))));
  for(let m of modes)for(let r of roles){o.full[m].count+=p.sets[m][r].length;ck(new Set(p.sets[m][r].map(key)).size===p.sets[m][r].length,"unique");for(let k of ks){o.metrics[k][m].count+=choices[k][m][r].length;o.diverse[k][m].count+=div[k][m][r].length}}
  let aa=d?t.proposal.claims:t.claims;o.annotations+=aa.length;let targets=aa.flatMap(a=>R.gold(d,a).map(r=>{let q=d?a.quote:a.span,s=t.text.indexOf(q);ck(s>=0&&s===t.text.lastIndexOf(q),"unique gold");return {r,q,k:s+":"+(s+q.length)}}));
  for(let g of targets){o.targets++;let base=hit(p.sets.base[g.r],g);if(!base){o.missing++;o.roleMissing[g.r]++}
   let row={id:ep.id+"."+(ti+1),role:g.r,q:g.q,full:{}};
   for(let m of modes){let h=hit(p.sets[m][g.r],g);o.full[m].hit+=+h;o.full[m].added+=+(!base&&h);o.full[m].roles[g.r][0]+=+h;o.full[m].roles[g.r][1]++;row.full[m]=h;
    for(let k of ks)for(let [metric,a] of [[o.metrics,choices],[o.diverse,div]]){let b=metric[k][m],h=hit(a[k][m][g.r],g),old=hit(a[k].base[g.r],g);b.hit+=+h;b.newHit+=+(!old&&h);b.lost+=+(old&&!h);b.roles[g.r][0]+=+h;b.roles[g.r][1]++}}
   if(!base)o.rows.push(row)
  }
  for(let m of modes)for(let k of ks)for(let [metric,a] of [[o.metrics,choices],[o.diverse,div]])if(targets.length&&targets.every(g=>hit(a[k][m][g.r],g)))metric[k][m].allTurns++;
 }}
 ck(o.targets===67&&o.missing===25&&o.full.base.hit===42&&o.episodes===32&&o.annotations===167&&o.numbers===68,"coverage");
 ck(ks.every((k,i)=>o.metrics[k].base.hit===[22,34,37,42,42][i]),"old parity");
 ck(o.full.context.hit===43&&o.full.choice.hit===51&&o.full.bridge.hit===52,"first run parity");
 for(let [t,r,q,m,expected,prior] of [["买书或者喝茶。","action","喝茶","choice",true,false],["买书或者喝茶。","action","买书","choice",true,false],["甲。乙","action","乙","choice",false,false],["继续，等待","action","继续，等待","bridge",true,false],["继续。等待","action","继续。等待","bridge",true,false],["最早八点","constraint","最早八点","numeric_modal",false,false],["三天前","constraint","三天前","numeric_modal",true,false],["八点","constraint","八点","numeric_modal",false,false],["五百，之前说错。","revision","五百","repair",true,true],["五百，之前说错。","revision","五百","repair",false,false]]){let a=propose(t,prior);ck(a.sets[m][r].some(v=>v.text===q)===expected,"control "+t);ck(a.authority==="NONE"&&a.outside,"authority");o.controls++}
 for(let [t,r,q,m,prior] of [["盐和糖放在桌上。","action","糖","choice",false],["我朋友说不要保存。","constraint","不要保存","modal",false],["我三天前吃过饭。","constraint","三天前","numeric_modal",false],["五百，之前的事我不知道。","revision","五百","repair",true]]){let a=propose(t,prior);o.contrast.push({text:t,role:r,span:q,mode:m,present:a.sets[m][r].some(v=>v.text===q),authority:a.authority});ck(a.authority==="NONE","contrast authority")}
 return o
}
const contents=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8"));
console.log(JSON.stringify(experiment(contents),null,2));
```
## 实际输出
metrics/diverse元组依次为命中、新增、丢失、候选总数、完整目标轮、约束[命中,分母]、行动[命中,分母]、修订[命中,分母]。
```json
{
  "episodes": 32,
  "turns": 64,
  "annotations": 167,
  "targets": 67,
  "missing": 25,
  "numbers": 68,
  "roleMissing": {
    "constraint": 9,
    "action": 13,
    "revision": 3
  },
  "full": {
    "base": {
      "hit": 42,
      "added": 0,
      "count": 1584,
      "roles": {
        "constraint": [
          16,
          25
        ],
        "action": [
          17,
          30
        ],
        "revision": [
          9,
          12
        ]
      }
    },
    "context": {
      "hit": 43,
      "added": 1,
      "count": 4007,
      "roles": {
        "constraint": [
          16,
          25
        ],
        "action": [
          18,
          30
        ],
        "revision": [
          9,
          12
        ]
      }
    },
    "choice": {
      "hit": 51,
      "added": 9,
      "count": 4107,
      "roles": {
        "constraint": [
          16,
          25
        ],
        "action": [
          26,
          30
        ],
        "revision": [
          9,
          12
        ]
      }
    },
    "bridge": {
      "hit": 52,
      "added": 10,
      "count": 8251,
      "roles": {
        "constraint": [
          16,
          25
        ],
        "action": [
          27,
          30
        ],
        "revision": [
          9,
          12
        ]
      }
    },
    "modal": {
      "hit": 59,
      "added": 17,
      "count": 8602,
      "roles": {
        "constraint": [
          23,
          25
        ],
        "action": [
          27,
          30
        ],
        "revision": [
          9,
          12
        ]
      }
    },
    "numeric_modal": {
      "hit": 59,
      "added": 17,
      "count": 8617,
      "roles": {
        "constraint": [
          23,
          25
        ],
        "action": [
          27,
          30
        ],
        "revision": [
          9,
          12
        ]
      }
    },
    "repair": {
      "hit": 60,
      "added": 18,
      "count": 8636,
      "roles": {
        "constraint": [
          23,
          25
        ],
        "action": [
          27,
          30
        ],
        "revision": [
          10,
          12
        ]
      }
    }
  },
  "metrics": {
    "1": {
      "base": [
        22,
        0,
        0,
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
      "context": [
        22,
        0,
        0,
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
      "choice": [
        23,
        1,
        0,
        74,
        11,
        [
          10,
          25
        ],
        [
          7,
          30
        ],
        [
          6,
          12
        ]
      ],
      "bridge": [
        23,
        1,
        0,
        74,
        11,
        [
          10,
          25
        ],
        [
          7,
          30
        ],
        [
          6,
          12
        ]
      ],
      "modal": [
        23,
        4,
        3,
        85,
        13,
        [
          10,
          25
        ],
        [
          7,
          30
        ],
        [
          6,
          12
        ]
      ],
      "numeric_modal": [
        23,
        4,
        3,
        87,
        13,
        [
          10,
          25
        ],
        [
          7,
          30
        ],
        [
          6,
          12
        ]
      ],
      "repair": [
        23,
        4,
        3,
        88,
        13,
        [
          10,
          25
        ],
        [
          7,
          30
        ],
        [
          6,
          12
        ]
      ]
    },
    "5": {
      "base": [
        34,
        0,
        0,
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
      "context": [
        34,
        0,
        0,
        330,
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
      "choice": [
        38,
        4,
        0,
        369,
        18,
        [
          14,
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
      "bridge": [
        38,
        4,
        0,
        369,
        18,
        [
          14,
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
      "modal": [
        43,
        9,
        0,
        424,
        23,
        [
          19,
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
      "numeric_modal": [
        43,
        9,
        0,
        432,
        23,
        [
          19,
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
      "repair": [
        44,
        10,
        0,
        437,
        24,
        [
          19,
          25
        ],
        [
          15,
          30
        ],
        [
          10,
          12
        ]
      ]
    },
    "10": {
      "base": [
        37,
        0,
        0,
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
      "context": [
        37,
        0,
        0,
        660,
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
      "choice": [
        44,
        7,
        0,
        727,
        23,
        [
          15,
          25
        ],
        [
          20,
          30
        ],
        [
          9,
          12
        ]
      ],
      "bridge": [
        44,
        7,
        0,
        727,
        23,
        [
          15,
          25
        ],
        [
          20,
          30
        ],
        [
          9,
          12
        ]
      ],
      "modal": [
        50,
        13,
        0,
        829,
        28,
        [
          21,
          25
        ],
        [
          20,
          30
        ],
        [
          9,
          12
        ]
      ],
      "numeric_modal": [
        50,
        13,
        0,
        842,
        28,
        [
          21,
          25
        ],
        [
          20,
          30
        ],
        [
          9,
          12
        ]
      ],
      "repair": [
        51,
        14,
        0,
        851,
        29,
        [
          21,
          25
        ],
        [
          20,
          30
        ],
        [
          10,
          12
        ]
      ]
    },
    "20": {
      "base": [
        42,
        0,
        0,
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
      "context": [
        42,
        0,
        0,
        1290,
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
      "choice": [
        50,
        8,
        0,
        1380,
        29,
        [
          16,
          25
        ],
        [
          25,
          30
        ],
        [
          9,
          12
        ]
      ],
      "bridge": [
        50,
        8,
        0,
        1405,
        29,
        [
          16,
          25
        ],
        [
          25,
          30
        ],
        [
          9,
          12
        ]
      ],
      "modal": [
        57,
        15,
        0,
        1560,
        35,
        [
          23,
          25
        ],
        [
          25,
          30
        ],
        [
          9,
          12
        ]
      ],
      "numeric_modal": [
        57,
        15,
        0,
        1575,
        35,
        [
          23,
          25
        ],
        [
          25,
          30
        ],
        [
          9,
          12
        ]
      ],
      "repair": [
        58,
        16,
        0,
        1584,
        36,
        [
          23,
          25
        ],
        [
          25,
          30
        ],
        [
          10,
          12
        ]
      ]
    },
    "50": {
      "base": [
        42,
        0,
        0,
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
      "context": [
        42,
        0,
        0,
        2724,
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
      "choice": [
        50,
        8,
        0,
        2824,
        29,
        [
          16,
          25
        ],
        [
          25,
          30
        ],
        [
          9,
          12
        ]
      ],
      "bridge": [
        51,
        9,
        0,
        3286,
        29,
        [
          16,
          25
        ],
        [
          26,
          30
        ],
        [
          9,
          12
        ]
      ],
      "modal": [
        58,
        16,
        0,
        3537,
        36,
        [
          23,
          25
        ],
        [
          26,
          30
        ],
        [
          9,
          12
        ]
      ],
      "numeric_modal": [
        58,
        16,
        0,
        3552,
        36,
        [
          23,
          25
        ],
        [
          26,
          30
        ],
        [
          9,
          12
        ]
      ],
      "repair": [
        59,
        17,
        0,
        3561,
        37,
        [
          23,
          25
        ],
        [
          26,
          30
        ],
        [
          10,
          12
        ]
      ]
    }
  },
  "diverse": {
    "1": {
      "base": [
        22,
        0,
        0,
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
      "context": [
        22,
        0,
        0,
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
      "choice": [
        23,
        1,
        0,
        74,
        11,
        [
          10,
          25
        ],
        [
          7,
          30
        ],
        [
          6,
          12
        ]
      ],
      "bridge": [
        23,
        1,
        0,
        74,
        11,
        [
          10,
          25
        ],
        [
          7,
          30
        ],
        [
          6,
          12
        ]
      ],
      "modal": [
        23,
        4,
        3,
        85,
        13,
        [
          10,
          25
        ],
        [
          7,
          30
        ],
        [
          6,
          12
        ]
      ],
      "numeric_modal": [
        23,
        4,
        3,
        87,
        13,
        [
          10,
          25
        ],
        [
          7,
          30
        ],
        [
          6,
          12
        ]
      ],
      "repair": [
        23,
        4,
        3,
        88,
        13,
        [
          10,
          25
        ],
        [
          7,
          30
        ],
        [
          6,
          12
        ]
      ]
    },
    "5": {
      "base": [
        38,
        0,
        0,
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
      "context": [
        37,
        0,
        1,
        330,
        21,
        [
          14,
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
      "choice": [
        42,
        5,
        1,
        369,
        21,
        [
          14,
          25
        ],
        [
          19,
          30
        ],
        [
          9,
          12
        ]
      ],
      "bridge": [
        42,
        5,
        1,
        369,
        21,
        [
          14,
          25
        ],
        [
          19,
          30
        ],
        [
          9,
          12
        ]
      ],
      "modal": [
        48,
        11,
        1,
        424,
        26,
        [
          20,
          25
        ],
        [
          19,
          30
        ],
        [
          9,
          12
        ]
      ],
      "numeric_modal": [
        48,
        11,
        1,
        432,
        26,
        [
          20,
          25
        ],
        [
          19,
          30
        ],
        [
          9,
          12
        ]
      ],
      "repair": [
        49,
        12,
        1,
        437,
        27,
        [
          20,
          25
        ],
        [
          19,
          30
        ],
        [
          10,
          12
        ]
      ]
    },
    "10": {
      "base": [
        39,
        0,
        0,
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
      "context": [
        38,
        0,
        1,
        660,
        22,
        [
          14,
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
      "choice": [
        46,
        8,
        1,
        727,
        25,
        [
          14,
          25
        ],
        [
          23,
          30
        ],
        [
          9,
          12
        ]
      ],
      "bridge": [
        46,
        8,
        1,
        727,
        25,
        [
          14,
          25
        ],
        [
          23,
          30
        ],
        [
          9,
          12
        ]
      ],
      "modal": [
        53,
        15,
        1,
        829,
        31,
        [
          21,
          25
        ],
        [
          23,
          30
        ],
        [
          9,
          12
        ]
      ],
      "numeric_modal": [
        53,
        15,
        1,
        842,
        31,
        [
          21,
          25
        ],
        [
          23,
          30
        ],
        [
          9,
          12
        ]
      ],
      "repair": [
        54,
        16,
        1,
        851,
        32,
        [
          21,
          25
        ],
        [
          23,
          30
        ],
        [
          10,
          12
        ]
      ]
    },
    "20": {
      "base": [
        41,
        0,
        0,
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
      "context": [
        41,
        0,
        0,
        1290,
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
      "choice": [
        49,
        8,
        0,
        1380,
        28,
        [
          16,
          25
        ],
        [
          24,
          30
        ],
        [
          9,
          12
        ]
      ],
      "bridge": [
        48,
        8,
        1,
        1405,
        27,
        [
          15,
          25
        ],
        [
          24,
          30
        ],
        [
          9,
          12
        ]
      ],
      "modal": [
        55,
        15,
        1,
        1560,
        33,
        [
          22,
          25
        ],
        [
          24,
          30
        ],
        [
          9,
          12
        ]
      ],
      "numeric_modal": [
        55,
        15,
        1,
        1575,
        33,
        [
          22,
          25
        ],
        [
          24,
          30
        ],
        [
          9,
          12
        ]
      ],
      "repair": [
        56,
        16,
        1,
        1584,
        34,
        [
          22,
          25
        ],
        [
          24,
          30
        ],
        [
          10,
          12
        ]
      ]
    },
    "50": {
      "base": [
        42,
        0,
        0,
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
      "context": [
        41,
        0,
        1,
        2724,
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
      "choice": [
        49,
        8,
        1,
        2824,
        28,
        [
          16,
          25
        ],
        [
          24,
          30
        ],
        [
          9,
          12
        ]
      ],
      "bridge": [
        49,
        8,
        1,
        3286,
        28,
        [
          16,
          25
        ],
        [
          24,
          30
        ],
        [
          9,
          12
        ]
      ],
      "modal": [
        56,
        15,
        1,
        3537,
        34,
        [
          23,
          25
        ],
        [
          24,
          30
        ],
        [
          9,
          12
        ]
      ],
      "numeric_modal": [
        56,
        15,
        1,
        3552,
        34,
        [
          23,
          25
        ],
        [
          24,
          30
        ],
        [
          9,
          12
        ]
      ],
      "repair": [
        57,
        16,
        1,
        3561,
        35,
        [
          23,
          25
        ],
        [
          24,
          30
        ],
        [
          10,
          12
        ]
      ]
    }
  },
  "rows": [
    {
      "id": "L03.2",
      "role": "revision",
      "q": "停课还能退五百",
      "full": {
        "base": false,
        "context": false,
        "choice": false,
        "bridge": false,
        "modal": false,
        "numeric_modal": false,
        "repair": true
      }
    },
    {
      "id": "L05.1",
      "role": "constraint",
      "q": "只有十天假",
      "full": {
        "base": false,
        "context": false,
        "choice": false,
        "bridge": false,
        "modal": true,
        "numeric_modal": true,
        "repair": true
      }
    },
    {
      "id": "L05.1",
      "role": "action",
      "q": "到时候看谁更需要，再挪两天",
      "full": {
        "base": false,
        "context": false,
        "choice": false,
        "bridge": true,
        "modal": true,
        "numeric_modal": true,
        "repair": true
      }
    },
    {
      "id": "L11.1",
      "role": "constraint",
      "q": "九点前到",
      "full": {
        "base": false,
        "context": false,
        "choice": false,
        "bridge": false,
        "modal": false,
        "numeric_modal": false,
        "repair": false
      }
    },
    {
      "id": "L11.2",
      "role": "constraint",
      "q": "最早八点",
      "full": {
        "base": false,
        "context": false,
        "choice": false,
        "bridge": false,
        "modal": false,
        "numeric_modal": false,
        "repair": false
      }
    },
    {
      "id": "L12.1",
      "role": "constraint",
      "q": "两项加起来只能十万",
      "full": {
        "base": false,
        "context": false,
        "choice": false,
        "bridge": false,
        "modal": true,
        "numeric_modal": true,
        "repair": true
      }
    },
    {
      "id": "L13.1",
      "role": "action",
      "q": "把他拉黑",
      "full": {
        "base": false,
        "context": false,
        "choice": false,
        "bridge": false,
        "modal": false,
        "numeric_modal": false,
        "repair": false
      }
    },
    {
      "id": "L15.2",
      "role": "revision",
      "q": "证书是必须的",
      "full": {
        "base": false,
        "context": false,
        "choice": false,
        "bridge": false,
        "modal": false,
        "numeric_modal": false,
        "repair": false
      }
    },
    {
      "id": "L18.1",
      "role": "constraint",
      "q": "不要保存",
      "full": {
        "base": false,
        "context": false,
        "choice": false,
        "bridge": false,
        "modal": true,
        "numeric_modal": true,
        "repair": true
      }
    },
    {
      "id": "L18.2",
      "role": "constraint",
      "q": "原文不要留",
      "full": {
        "base": false,
        "context": false,
        "choice": false,
        "bridge": false,
        "modal": true,
        "numeric_modal": true,
        "repair": true
      }
    },
    {
      "id": "S02.1",
      "role": "action",
      "q": "东边",
      "full": {
        "base": false,
        "context": false,
        "choice": true,
        "bridge": true,
        "modal": true,
        "numeric_modal": true,
        "repair": true
      }
    },
    {
      "id": "S02.1",
      "role": "action",
      "q": "西边",
      "full": {
        "base": false,
        "context": false,
        "choice": true,
        "bridge": true,
        "modal": true,
        "numeric_modal": true,
        "repair": true
      }
    },
    {
      "id": "S04.1",
      "role": "constraint",
      "q": "我们两个人都得能用厨房",
      "full": {
        "base": false,
        "context": false,
        "choice": false,
        "bridge": false,
        "modal": true,
        "numeric_modal": true,
        "repair": true
      }
    },
    {
      "id": "S04.1",
      "role": "action",
      "q": "买电饭煲",
      "full": {
        "base": false,
        "context": false,
        "choice": true,
        "bridge": true,
        "modal": true,
        "numeric_modal": true,
        "repair": true
      }
    },
    {
      "id": "S04.1",
      "role": "action",
      "q": "买小烤箱",
      "full": {
        "base": false,
        "context": false,
        "choice": true,
        "bridge": true,
        "modal": true,
        "numeric_modal": true,
        "repair": true
      }
    },
    {
      "id": "S05.1",
      "role": "action",
      "q": "报考执照",
      "full": {
        "base": false,
        "context": true,
        "choice": true,
        "bridge": true,
        "modal": true,
        "numeric_modal": true,
        "repair": true
      }
    },
    {
      "id": "S06.2",
      "role": "constraint",
      "q": "先别替我决定",
      "full": {
        "base": false,
        "context": false,
        "choice": false,
        "bridge": false,
        "modal": true,
        "numeric_modal": true,
        "repair": true
      }
    },
    {
      "id": "S07.2",
      "role": "constraint",
      "q": "不要把风险偏好设成激进",
      "full": {
        "base": false,
        "context": false,
        "choice": false,
        "bridge": false,
        "modal": true,
        "numeric_modal": true,
        "repair": true
      }
    },
    {
      "id": "S10.1",
      "role": "action",
      "q": "周五买菜",
      "full": {
        "base": false,
        "context": false,
        "choice": true,
        "bridge": true,
        "modal": true,
        "numeric_modal": true,
        "repair": true
      }
    },
    {
      "id": "S10.1",
      "role": "action",
      "q": "周六早起",
      "full": {
        "base": false,
        "context": false,
        "choice": true,
        "bridge": true,
        "modal": true,
        "numeric_modal": true,
        "repair": true
      }
    },
    {
      "id": "S12.1",
      "role": "action",
      "q": "修旧相机",
      "full": {
        "base": false,
        "context": false,
        "choice": false,
        "bridge": false,
        "modal": false,
        "numeric_modal": false,
        "repair": false
      }
    },
    {
      "id": "S12.1",
      "role": "action",
      "q": "买二手相机",
      "full": {
        "base": false,
        "context": false,
        "choice": false,
        "bridge": false,
        "modal": false,
        "numeric_modal": false,
        "repair": false
      }
    },
    {
      "id": "S12.2",
      "role": "revision",
      "q": "维修店说要七百",
      "full": {
        "base": false,
        "context": false,
        "choice": false,
        "bridge": false,
        "modal": false,
        "numeric_modal": false,
        "repair": false
      }
    },
    {
      "id": "S14.1",
      "role": "action",
      "q": "先发消息沟通",
      "full": {
        "base": false,
        "context": false,
        "choice": true,
        "bridge": true,
        "modal": true,
        "numeric_modal": true,
        "repair": true
      }
    },
    {
      "id": "S14.1",
      "role": "action",
      "q": "等到周末当面说",
      "full": {
        "base": false,
        "context": false,
        "choice": true,
        "bridge": true,
        "modal": true,
        "numeric_modal": true,
        "repair": true
      }
    }
  ],
  "controls": 10,
  "contrast": [
    {
      "text": "盐和糖放在桌上。",
      "role": "action",
      "span": "糖",
      "mode": "choice",
      "present": true,
      "authority": "NONE"
    },
    {
      "text": "我朋友说不要保存。",
      "role": "constraint",
      "span": "不要保存",
      "mode": "modal",
      "present": true,
      "authority": "NONE"
    },
    {
      "text": "我三天前吃过饭。",
      "role": "constraint",
      "span": "三天前",
      "mode": "numeric_modal",
      "present": true,
      "authority": "NONE"
    },
    {
      "text": "五百，之前的事我不知道。",
      "role": "revision",
      "span": "五百",
      "mode": "repair",
      "present": true,
      "authority": "NONE"
    }
  ]
}
```
