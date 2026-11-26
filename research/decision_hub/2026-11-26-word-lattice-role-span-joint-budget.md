# 自主认知：词格与原文角色跨度的联合预算连接
2026-11-26。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / PUBLIC_SYNTHETIC_DEVELOPMENT / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线与去重
起始main db71afc3bc83460f8d07efc57246b58fbfbc7330，核对12近期提交、8开放PR、v3.2前12行及既有完整规程、同步规程前21行、唯一产品交接固定blob 5e74f4f0b37141d631740e844ad8bbbfed232e07首尾，固定#63仍open；未重跑该候选。前轮本地joint_semantics.py为有限六字段合成图最小状态成本，本轮没有直接执行该Python程序；实际连接既有原始决策文本上的角色候选与真实词典分词图，仅研究跨度边界联合可达性，尚未连接全部六字段语义。db71afc研究外部wiki dev词边及金标路径，本轮换为既有决策开发集及角色候选；b4faa9a已研究角色召回，本轮固定其评分，新增词格过滤及多跨度联合最小成本。R133已有条件边关联投影，本轮关注同一分词路径的联合端点成本，不将几何支持当成真实条件/角色或修订解释。去重非全库证明。直接git ls-remote因DNS失败；GitHub连接器成功读取。未修改任何既有文件或唯一交接。
## 固定资产
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-25-raw-text-reference-search.md 16075b3ba567ee6dc3496300beab1417172a6c42
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
research/decision_hub/2026-11-26-compositional-role-candidate-recovery.md b0bea7b4c101c170be2aaa2355973739b125e0b7
CC-CEDICT镜像 rhcarvalho/cedict 固定blob d7fee8237f26524b38eee220647e4c5d79f00de9，前轮固定commit 6317ff202e14be60365c826f62e45fc9fa71d19e。实际重新读取词典及六份文件，连接器返回blob身份与前轮相符，词典121696唯一简体词头；本轮未独立复算原始Git字节哈希，Node包装提供实际文件哈希校验。词典CC BY-SA 4.0，来源/许可边界沿用db71afc及静态词典报告；不复制第三方词典内容，衍生数据分发另审。两套32情节64轮167标注、67目标、44有角色目标的轮均为项目原创ChatGPT辅助公开合成已见开发材料，非真人、独立留出、训练或真实使用。候选生成只输入原文和是否有前轮，标签只用于评分；前轮repair规则本已事后检查遗漏，故非盲测。
## 算法
沿用词格最长16 Unicode标量、空白跳过、词典词/数字拉丁最长结构边/单标点成本1、未知单字9；expanded另允许未知跨度成本1+8L。相同边取最小成本。成本为启发式整数非概率。角色候选为固定前轮repair完整池，原评分和顺序不修改；原始坐标UTF16严格转换为Unicode标量，核对每个跨度原文。对于DAG中任意i<=j，d(i,j)为从i到j的最小路径成本，以拓扑DP计算。给定要求边界集合P，去重排序并加入0,n得到p0...pm。最小附加成本C(P)=sum d(p_k,p_{k+1})-d(0,n)。证明：每条经过全部指定节点的路径在这些节点分段，每段成本不小于相应最小成本；各段最优路径可直接拼接，达到下界。因此C(P)精确，且随P包含关系单调。嵌套/交叉跨度可共享边界；边界可达不推出语义可共存。对角色跨度(s,e)计算C({s,e})；先过滤C<=B，再以旧评分截取每类K=5,20,全部。完整目标轮额外计算全部金标边界联合成本；该计算是评价oracle，不向候选生成提供标签。逐跨度与独立删去跨过指定节点的边再做最短路核对，非独立团队验收。复杂度所有起点最短路O(nE)时间O(n²)距离空间；每个有限端点集排序后O(m log m)求值，枚举所有候选对O(M²)，不保证实际设备资源；不应在产品中无界枚举。
## 结果
三次实验：首次加载截断标记错误导致SyntaxError，修正为固定代码实际标记；后运行角色过滤与跨度对实验，最后组合实现实际再运行并核对关键计数一致。六个短控制串、两图及全部边界子集178检查；17,400候选/轮联合最短路oracle检查通过；253跨度对oracle检查通过。无CI、生产或设备运行。
原repair 8636候选、60/67完整池命中、38/44目标轮全部命中。B0过滤后4114候选、60/67、38/44，候选数减少4522/8636=52.3622%；每类K5原437候选44/67、24/44，过滤后432候选49/67、28/44（新增5、丢失0）；K20原1584候选58/67、36/44，过滤后1484候选58/67、36/44。B1 K5回到44/67，说明预算扩大不保证固定K排名质量单调；B4及以上全部候选恢复。两图在本开发集统计完全一致，不据此泛化。当前原标注全部候选均边界可达时的完整轮未出现预算内边际虚增，不能据此认为风险不存在。
在sparse图，对每轮去重后的7326角色跨度（忽略角色标签以隔离几何），实际枚举659958个同轮无序不同跨度对，核对联合成本>=各自成本最大值。如下：
|B|分别可达对|联合可达对|分别可达但联合超预算|受影响轮|
|---:|---:|---:|---:|---:|
|0|149426|148599|827|10|
|1|534659|425000|109659|52|
|2|656314|604958|51356|48|
|4|659958|659816|142|6|
B1中例如L01.1两个跨度各自附加成本1、联合成本2；B0中L02.1存在两跨度各自最优、联合需增加1。具体见JSON。上述为枚举候选几何反例，非语言错误率或真实决策错误；跨强句的候选可存在，禁止自动语义绑定。完整原标注在此集没有观察到联合丢失；两者并不矛盾。固定K结果变化受排序与候选量共同影响，未测实际计算时间/内存、精度、独立泛化或最优语义解析。
## 接口与下一责任
分词候选格版本、原文UTF16/标量转换、已要求边界集合、联合最小额外成本、搜索预算与来源一起保留；必要时计算完整原始路径见证。候选过滤不能当硬门：图外词义、角色、引用、否定、条件、数值、真实身份和时效未解决；任何未知或被裁剪义务必须保留可审查状态。B0只能作为显示/排序候选实验，不采用为生产默认阈值；被删跨度应可恢复或进入独立未知检测。真实宿主、原生数学和账本权限仍独立；本轮authority NONE、outside true。下一步将词格端点状态和来源绑定的角色/关系/数值/引用真实联合候选接入同一有限状态，避免重复调分词预算；独立轨保管未见语料，重点验证条件0/5及修订0/10是否实际改善。自行选择边界公式、预算、K、跨度对统计，不改变所有者方向。没有训练、第三方AI运行依赖、PR合并、部署、主动CI、费用或历史证据升级。
## 复算
以下标准Node包装需依序传入上述六份固定原始文件及CC-CEDICT文件。核心函数已在连接器JS实际执行；Node I/O及哈希包装未单独执行。仅对固定项目自有已审查研究源码使用Function加载；不可用于运行网络不可信文本。
```js
const fs=require("node:fs"),crypto=require("node:crypto");
const files=process.argv.slice(2);if(files.length!==7)throw Error("six research assets and dictionary required");
const bufs=files.map(p=>fs.readFileSync(p)),hash=b=>crypto.createHash("sha1").update("blob "+b.length+"\0").update(b).digest("hex");
const expected=["be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb","05c239f3f3b1f46235fa2464d2945c21c6c08132","bbdc12dfe65b24aa24e6b1d25a04955766cadab4","16075b3ba567ee6dc3496300beab1417172a6c42","07dcbda9532dbc3b330abfd79a399cb52aa91aeb","b0bea7b4c101c170be2aaa2355973739b125e0b7","d7fee8237f26524b38eee220647e4c5d79f00de9"];
if(bufs.some((b,i)=>hash(b)!==expected[i]))throw Error("asset hash mismatch");
function experiment(content,dict){
 const ck=(x,m)=>{if(!x)throw Error(m)},code=content[5].split("```js\n")[1].split("\n```")[0];
 ck(code.includes(" let o={episodes:"),"loader");
 const P=Function("input",code.split(" let o={episodes:")[0]+"\nreturn {propose,R};\n}\nreturn experiment(input);")(content.slice(0,5));
 const words=new Set();for(const l of dict.split(/\r?\n/)){const m=/^(\S+) (\S+) \[.*?\] /u.exec(l);if(m&&[...m[2]].length<=16)words.add(m[2])}ck(words.size===121696,"dictionary");
 const cls=c=>/\s/u.test(c)?"s":/\p{P}/u.test(c)?"p":/\p{Nd}/u.test(c)?"d":/\p{Script=Latin}/u.test(c)?"l":"o";
 function lattice(c,expanded){let t=c.map(cls),g=[];for(let i=0;i<c.length;i++){if(t[i]==="s"){g.push([{j:i+1,c:0}]);continue}let hi=i+1;while(hi<c.length&&hi-i<16&&t[hi]!=="s")hi++;let es=new Map(),add=(j,v)=>es.set(j,Math.min(v,es.get(j)??Infinity));for(let j=i+1;j<=hi;j++){if(words.has(c.slice(i,j).join("")))add(j,1);else if(expanded)add(j,1+8*(j-i))}add(i+1,t[i]==="p"?1:9);if(["d","l"].includes(t[i])){let j=i+1;while(j<hi&&t[j]===t[i])j++;if(j>i+1)add(j,1)}g.push([...es].map(([j,c])=>({j,c})))}return g}
 function allpairs(g){let n=g.length;return Array.from({length:n+1},(_,s)=>{let d=Array(n+1).fill(Infinity);d[s]=0;for(let i=s;i<n;i++)if(Number.isFinite(d[i]))for(let e of g[i])d[e.j]=Math.min(d[e.j],d[i]+e.c);return d})}
 function required(d,ps){let s=[...new Set([0,...ps,d.length-1])].sort((a,b)=>a-b),v=0;for(let i=1;i<s.length;i++)v+=d[s[i-1]][s[i]];return v-d[0].at(-1)}
 function independent(g,ps){let n=g.length,d=Array(n+1).fill(Infinity);d[0]=0;for(let i=0;i<n;i++)for(let e of g[i])if(!ps.some(x=>i<x&&x<e.j))d[e.j]=Math.min(d[e.j],d[i]+e.c);return d[n]}
 const roles=["constraint","action","revision"],B=[0,1,2,4,8,16,32],K=[5,20,Infinity],key=x=>x.start+":"+x.end;
 const blank=()=>({candidates:0,hit:0,allTargetTurns:0,jointTargetTurns:0,added:0,lost:0,individualButNotJoint:0});
 const out={words:words.size,episodes:0,turns:0,annotations:0,targets:0,targetTurns:0,controls:0,checks:0,rawCandidates:0,baseline:Object.fromEntries(K.map(k=>[k,blank()])),modes:{},counterexamples:[],pair:{turns:0,pairs:0,distinctSpans:0,oracleChecks:0,budgets:Object.fromEntries(B.slice(0,4).map(b=>[b,{marginalPairs:0,jointPairs:0,unsupportedPairs:0,affectedTurns:0,examples:[]}]))},authority:"NONE",outside:true};
 for(let mode of ["sparse","expanded"]){out.modes[mode]={};for(let b of B)out.modes[mode][b]=Object.fromEntries(K.map(k=>[k,blank()]))}
 for(let raw of ["","南京市长江大桥","研究生命","A𠀀B","甲 乙","12.5"])for(let expanded of [false,true]){
  let g=lattice([...raw],expanded),d=allpairs(g);for(let mask=0;mask<(1<<Math.max(0,g.length-1));mask++){let ps=Array.from({length:Math.max(0,g.length-1)},(_,i)=>i+1).filter(i=>mask&(1<<(i-1)));ck(required(d,ps)+d[0].at(-1)===independent(g,ps),"control");out.controls++}
 }
 for(let [ds,doc] of content.slice(0,2).map(JSON.parse).entries())for(let ep of doc.cases){out.episodes++;for(let [ti,t] of ep.turns.entries()){
  out.turns++;let raw=t.text,chars=[...raw],offset=new Map([[0,0]]),u=0;for(let [i,c] of chars.entries()){u+=c.length;offset.set(u,i+1)}
  const pos=x=>{ck(offset.has(x),"UTF16 boundary");return offset.get(x)},points=x=>[pos(x.start),pos(x.end)];
  let candidate=P.propose(raw,ti>0).sets.repair;for(let role of roles)for(let x of candidate[role])ck(raw.slice(x.start,x.end)===x.text,"span");
  let aa=ds?t.proposal.claims:t.claims;out.annotations+=aa.length;
  let gold=aa.flatMap(a=>P.R.gold(ds,a).map(r=>{let q=ds?a.quote:a.span,s=raw.indexOf(q);ck(s>=0&&s===raw.lastIndexOf(q),"gold");return {r,start:s,end:s+q.length,q}}));
  out.targets+=gold.length;out.targetTurns+=+(gold.length>0);
  const has=(set,x)=>set[x.r].some(y=>key(y)===key(x)),select=(pool,k)=>Object.fromEntries(roles.map(r=>[r,pool[r].slice(0,k)]));
  const base=Object.fromEntries(K.map(k=>[k,select(candidate,k)]));
  for(let k of K){let v=out.baseline[k],b=base[k];v.candidates+=roles.reduce((n,r)=>n+b[r].length,0);v.hit+=gold.filter(x=>has(b,x)).length;v.allTargetTurns+=+(gold.length>0&&gold.every(x=>has(b,x)))}
  out.rawCandidates+=roles.reduce((n,r)=>n+candidate[r].length,0);
  for(let [mode,expanded] of [["sparse",false],["expanded",true]]){
   let g=lattice(chars,expanded),d=allpairs(g),goldps=gold.flatMap(points),joint=required(d,goldps),opt=d[0].at(-1);
   ck(joint+opt===independent(g,goldps),"gold joint oracle");out.checks++;
   let costs=Object.fromEntries(roles.map(r=>[r,candidate[r].map(x=>{let ps=points(x),v=required(d,ps);ck(v+opt===independent(g,ps),"candidate oracle");out.checks++;return {x,v}})]));
   for(let b of B){let pool=Object.fromEntries(roles.map(r=>[r,costs[r].filter(x=>x.v<=b).map(x=>x.x)]));for(let k of K){let s=select(pool,k),v=out.modes[mode][b][k],all=gold.length>0&&gold.every(x=>has(s,x));v.candidates+=roles.reduce((n,r)=>n+s[r].length,0);for(let x of gold){let h=has(s,x),old=has(base[k],x);v.hit+=+h;v.added+=+(h&&!old);v.lost+=+(old&&!h)}v.allTargetTurns+=+all;v.jointTargetTurns+=+(all&&joint<=b);v.individualButNotJoint+=+(all&&joint>b);if(k===Infinity&&all&&joint>b)out.counterexamples.push({id:ep.id+"."+(ti+1),mode,b,joint,individual:gold.map(x=>({q:x.q,r:x.r,cost:required(d,points(x))}))})}}
   if(mode==="sparse"){
    let o=out.pair;o.turns++;let spans=new Map();for(let role of roles)for(let {x,v} of costs[role]){let ps=points(x),k=ps.join(":");if(!spans.has(k))spans.set(k,{ps,q:x.text,c:v})}
    let s=[...spans.values()];o.distinctSpans+=s.length;let affected=new Set();
    for(let i=0;i<s.length;i++)for(let j=i+1;j<s.length;j++){let x=s[i],y=s[j],ps=[...x.ps,...y.ps],c=required(d,ps),m=Math.max(x.c,y.c);ck(c>=m,"monotone");o.pairs++;if((i===0&&j===1)||(c>m&&o.oracleChecks<200)){ck(c+opt===independent(g,ps),"pair oracle");o.oracleChecks++}
     for(let b of B.slice(0,4))if(m<=b){let v=o.budgets[b];v.marginalPairs++;if(c<=b)v.jointPairs++;else{v.unsupportedPairs++;affected.add(b);if(v.examples.length<3)v.examples.push({id:ep.id+"."+(ti+1),x:x.q,y:y.q,xCost:x.c,yCost:y.c,jointCost:c})}}}
    for(let b of affected)o.budgets[b].affectedTurns++;
   }
  }
 }}
 for(let v of Object.values(out.pair.budgets))ck(v.marginalPairs===v.jointPairs+v.unsupportedPairs,"count");
 ck(out.episodes===32&&out.turns===64&&out.annotations===167&&out.targets===67&&out.rawCandidates===8636&&out.baseline.Infinity.hit===60,"upstream totals");
 return out;
}
const texts=bufs.map(b=>b.toString("utf8"));console.log(JSON.stringify(experiment(texts.slice(0,6),texts[6]),null,2));
```
## 实际完整结果
```json
{
  "words": 121696,
  "episodes": 32,
  "turns": 64,
  "annotations": 167,
  "targets": 67,
  "targetTurns": 44,
  "controls": 178,
  "checks": 17400,
  "rawCandidates": 8636,
  "baseline": {
    "5": {
      "candidates": 437,
      "hit": 44,
      "allTargetTurns": 24,
      "jointTargetTurns": 0,
      "added": 0,
      "lost": 0,
      "individualButNotJoint": 0
    },
    "20": {
      "candidates": 1584,
      "hit": 58,
      "allTargetTurns": 36,
      "jointTargetTurns": 0,
      "added": 0,
      "lost": 0,
      "individualButNotJoint": 0
    },
    "Infinity": {
      "candidates": 8636,
      "hit": 60,
      "allTargetTurns": 38,
      "jointTargetTurns": 0,
      "added": 0,
      "lost": 0,
      "individualButNotJoint": 0
    }
  },
  "modes": {
    "sparse": {
      "0": {
        "5": {
          "candidates": 432,
          "hit": 49,
          "allTargetTurns": 28,
          "jointTargetTurns": 28,
          "added": 5,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "20": {
          "candidates": 1484,
          "hit": 58,
          "allTargetTurns": 36,
          "jointTargetTurns": 36,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "Infinity": {
          "candidates": 4114,
          "hit": 60,
          "allTargetTurns": 38,
          "jointTargetTurns": 38,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        }
      },
      "1": {
        "5": {
          "candidates": 437,
          "hit": 44,
          "allTargetTurns": 24,
          "jointTargetTurns": 24,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "20": {
          "candidates": 1580,
          "hit": 58,
          "allTargetTurns": 36,
          "jointTargetTurns": 36,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "Infinity": {
          "candidates": 7814,
          "hit": 60,
          "allTargetTurns": 38,
          "jointTargetTurns": 38,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        }
      },
      "2": {
        "5": {
          "candidates": 437,
          "hit": 44,
          "allTargetTurns": 24,
          "jointTargetTurns": 24,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "20": {
          "candidates": 1584,
          "hit": 58,
          "allTargetTurns": 36,
          "jointTargetTurns": 36,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "Infinity": {
          "candidates": 8613,
          "hit": 60,
          "allTargetTurns": 38,
          "jointTargetTurns": 38,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        }
      },
      "4": {
        "5": {
          "candidates": 437,
          "hit": 44,
          "allTargetTurns": 24,
          "jointTargetTurns": 24,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "20": {
          "candidates": 1584,
          "hit": 58,
          "allTargetTurns": 36,
          "jointTargetTurns": 36,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "Infinity": {
          "candidates": 8636,
          "hit": 60,
          "allTargetTurns": 38,
          "jointTargetTurns": 38,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        }
      },
      "8": {
        "5": {
          "candidates": 437,
          "hit": 44,
          "allTargetTurns": 24,
          "jointTargetTurns": 24,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "20": {
          "candidates": 1584,
          "hit": 58,
          "allTargetTurns": 36,
          "jointTargetTurns": 36,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "Infinity": {
          "candidates": 8636,
          "hit": 60,
          "allTargetTurns": 38,
          "jointTargetTurns": 38,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        }
      },
      "16": {
        "5": {
          "candidates": 437,
          "hit": 44,
          "allTargetTurns": 24,
          "jointTargetTurns": 24,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "20": {
          "candidates": 1584,
          "hit": 58,
          "allTargetTurns": 36,
          "jointTargetTurns": 36,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "Infinity": {
          "candidates": 8636,
          "hit": 60,
          "allTargetTurns": 38,
          "jointTargetTurns": 38,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        }
      },
      "32": {
        "5": {
          "candidates": 437,
          "hit": 44,
          "allTargetTurns": 24,
          "jointTargetTurns": 24,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "20": {
          "candidates": 1584,
          "hit": 58,
          "allTargetTurns": 36,
          "jointTargetTurns": 36,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "Infinity": {
          "candidates": 8636,
          "hit": 60,
          "allTargetTurns": 38,
          "jointTargetTurns": 38,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        }
      }
    },
    "expanded": {
      "0": {
        "5": {
          "candidates": 432,
          "hit": 49,
          "allTargetTurns": 28,
          "jointTargetTurns": 28,
          "added": 5,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "20": {
          "candidates": 1484,
          "hit": 58,
          "allTargetTurns": 36,
          "jointTargetTurns": 36,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "Infinity": {
          "candidates": 4114,
          "hit": 60,
          "allTargetTurns": 38,
          "jointTargetTurns": 38,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        }
      },
      "1": {
        "5": {
          "candidates": 437,
          "hit": 44,
          "allTargetTurns": 24,
          "jointTargetTurns": 24,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "20": {
          "candidates": 1580,
          "hit": 58,
          "allTargetTurns": 36,
          "jointTargetTurns": 36,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "Infinity": {
          "candidates": 7814,
          "hit": 60,
          "allTargetTurns": 38,
          "jointTargetTurns": 38,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        }
      },
      "2": {
        "5": {
          "candidates": 437,
          "hit": 44,
          "allTargetTurns": 24,
          "jointTargetTurns": 24,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "20": {
          "candidates": 1584,
          "hit": 58,
          "allTargetTurns": 36,
          "jointTargetTurns": 36,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "Infinity": {
          "candidates": 8613,
          "hit": 60,
          "allTargetTurns": 38,
          "jointTargetTurns": 38,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        }
      },
      "4": {
        "5": {
          "candidates": 437,
          "hit": 44,
          "allTargetTurns": 24,
          "jointTargetTurns": 24,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "20": {
          "candidates": 1584,
          "hit": 58,
          "allTargetTurns": 36,
          "jointTargetTurns": 36,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "Infinity": {
          "candidates": 8636,
          "hit": 60,
          "allTargetTurns": 38,
          "jointTargetTurns": 38,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        }
      },
      "8": {
        "5": {
          "candidates": 437,
          "hit": 44,
          "allTargetTurns": 24,
          "jointTargetTurns": 24,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "20": {
          "candidates": 1584,
          "hit": 58,
          "allTargetTurns": 36,
          "jointTargetTurns": 36,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "Infinity": {
          "candidates": 8636,
          "hit": 60,
          "allTargetTurns": 38,
          "jointTargetTurns": 38,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        }
      },
      "16": {
        "5": {
          "candidates": 437,
          "hit": 44,
          "allTargetTurns": 24,
          "jointTargetTurns": 24,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "20": {
          "candidates": 1584,
          "hit": 58,
          "allTargetTurns": 36,
          "jointTargetTurns": 36,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "Infinity": {
          "candidates": 8636,
          "hit": 60,
          "allTargetTurns": 38,
          "jointTargetTurns": 38,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        }
      },
      "32": {
        "5": {
          "candidates": 437,
          "hit": 44,
          "allTargetTurns": 24,
          "jointTargetTurns": 24,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "20": {
          "candidates": 1584,
          "hit": 58,
          "allTargetTurns": 36,
          "jointTargetTurns": 36,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        },
        "Infinity": {
          "candidates": 8636,
          "hit": 60,
          "allTargetTurns": 38,
          "jointTargetTurns": 38,
          "added": 0,
          "lost": 0,
          "individualButNotJoint": 0
        }
      }
    }
  },
  "counterexamples": [],
  "pair": {
    "turns": 64,
    "pairs": 659958,
    "distinctSpans": 7326,
    "oracleChecks": 253,
    "budgets": {
      "0": {
        "marginalPairs": 149426,
        "jointPairs": 148599,
        "unsupportedPairs": 827,
        "affectedTurns": 10,
        "examples": [
          {
            "id": "L02.1",
            "x": "不去。A说不用常上",
            "y": "不去。A说不用常上夜",
            "xCost": 0,
            "yCost": 0,
            "jointCost": 1
          },
          {
            "id": "L02.1",
            "x": "不去。A说不用常上",
            "y": "可只要夜班我就不去。A说不用常上夜",
            "xCost": 0,
            "yCost": 0,
            "jointCost": 1
          },
          {
            "id": "L02.1",
            "x": "不去。A说不用常上",
            "y": "就不去。A说不用常上夜",
            "xCost": 0,
            "yCost": 0,
            "jointCost": 1
          }
        ]
      },
      "1": {
        "marginalPairs": 534659,
        "jointPairs": 425000,
        "unsupportedPairs": 109659,
        "affectedTurns": 52,
        "examples": [
          {
            "id": "L01.1",
            "x": "车每月最多四千",
            "y": "租加停车每月最多四千",
            "xCost": 1,
            "yCost": 1,
            "jointCost": 2
          },
          {
            "id": "L01.1",
            "x": "车每月最多四千",
            "y": "月最多四千",
            "xCost": 1,
            "yCost": 1,
            "jointCost": 2
          },
          {
            "id": "L01.1",
            "x": "车每月最多四千",
            "y": "车位得问房",
            "xCost": 1,
            "yCost": 1,
            "jointCost": 2
          }
        ]
      },
      "2": {
        "marginalPairs": 656314,
        "jointPairs": 604958,
        "unsupportedPairs": 51356,
        "affectedTurns": 48,
        "examples": [
          {
            "id": "L01.1",
            "x": "车每月最多四千",
            "y": "位得问房",
            "xCost": 1,
            "yCost": 2,
            "jointCost": 3
          },
          {
            "id": "L01.1",
            "x": "车每月最多四千",
            "y": "租加停车每月最",
            "xCost": 1,
            "yCost": 2,
            "jointCost": 3
          },
          {
            "id": "L01.1",
            "x": "车每月最多四千",
            "y": "月最多四千，水",
            "xCost": 1,
            "yCost": 2,
            "jointCost": 3
          }
        ]
      },
      "4": {
        "marginalPairs": 659958,
        "jointPairs": 659816,
        "unsupportedPairs": 142,
        "affectedTurns": 6,
        "examples": [
          {
            "id": "L04.2",
            "x": "期会失去报名资",
            "y": "作日，延期会失",
            "xCost": 2,
            "yCost": 3,
            "jointCost": 5
          },
          {
            "id": "L04.2",
            "x": "期会失去报名资",
            "y": "作日，延期会失去报",
            "xCost": 2,
            "yCost": 3,
            "jointCost": 5
          },
          {
            "id": "L04.2",
            "x": "去报名资",
            "y": "作日，延期会失去报",
            "xCost": 2,
            "yCost": 3,
            "jointCost": 5
          }
        ]
      }
    }
  },
  "authority": "NONE",
  "outside": true
}
```
