# 自主认知：数词多跳路径与整句树见证联合排序
2026-11-27。RESEARCH_CANDIDATE / REAL_EXTERNAL_DEVELOPMENT_BYTES_VERIFIED / GOLD_TOKEN_POS_CONDITIONED / EXACT_FINITE_PATH_AND_TREE_PARTITION / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。

## 基线、数据与去重
起点main f31db2a713660e0b9e09f16e40b793390f9af61a；核对20近期提交、15开放PR、v3.2、同步规程全文、唯一产品交接前20行、#63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft。实际读取前序数词谓词链41032c25539db1368b8917d8ee4732174b488e86、单根投射解码c40a09357a858644a0da922097cd6367ca696df6、R134结构审计db9cc100d96d49832fe32879a706f63830301773全文及自有代码，另读取分词共同见证a5589d2eda71c5abc26469f82e0ad8846efc0269、有限冲突证书5faa95672f893c60e41433968dd7b4d43f481741前22行及目录相关题名。既有端点边际排序、单树解码、共同分词掩码不重复计。新增完整多跳路径检索、强制路径的整句最优树见证及按路径等价类枚举不同全局最优树投影。局部查重，非全库证明。
固定外部 UD_Chinese-GSDSimp commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3，dev blob af8cc878e7934b38ce3c1a266053100e7c47de6f，两次读取完整Git blob并运行R134原始UTF8 Git SHA1验证，1195378字节及摘要一致。数据来源 https://github.com/UniversalDependencies/UD_Chinese-GSDSimp/blob/b79a1c2f7ba7f9b264808d91c6886a67b7f847a3/zh_gsdsimp-ud-dev.conllu ，许可沿用已登记 https://universaldependencies.org/treebanks/zh_gsdsimp/ 及 https://creativecommons.org/licenses/by-sa/4.0/ ，底层wiki文本权利独立；未重审许可全文，不分发外部文本、未读取train/test、未训练。500句、654个NUM，567有VERB/ADJ/AUX祖先，87无此类祖先。已见公开真实文本句法开发集，非独立留出、用户决策语义金标。输入仍为外部提供的分词、词性、NUM起点，未实现自主原文句法；金标HEAD仅用于评价。原始数词扫描仅统计与上述条件化预测交集，不称端到端效果。

## A. 局部路径与完整树核验
保持上一轮旧评分及数量提示评分不变（直接提取固定matrix函数）。每弧从相应依存词所有候选头的最大分减实际分再加1作为严格正代价；路径从NUM沿头方向前进，不重复节点，遇到第一个谓词代理或虚根停止，最多6弧。以最小堆按累积代价及词元索引字典序排序。严格正增量保证每个路径的前缀在该路径前出队，故取出的终止路径依此序全局最优于该有限路径域（不是整句树最优）；限20000出队操作，非完整内存预算。单条路径无环不能保证可扩展为单根投射树。分别比较同一个候选池中完整路径、两个端点同时出现于同一候选、以及只要求分别出现于不同候选；不把端点检索当完整路径命中。
对每个NUM的数量提示前5路径，复制原评分矩阵并将路径上每个子节点除指定头之外的弧置为负无穷，运行固定Eisner单根投射最优解码。若可行，回读树每条强制弧并核对原始分数；无树只表示限定投射图内无法扩展，不能断言语言本身不可能。按受限最优树总分（等价于相对原最优分数损失最小）重排可行前5路径，同分沿用原序。只保证这5条中排名最优，不能宣称找到整个域全局最优候选。第一轮实际654×2路径搜索及3270次树核验，第二轮整理后重复执行并核对关键指标。100个小图穷举路径前K参照、100零预算控制。
结果：旧完整链前1/3/5/10命中45/132/176/239，数量评分56/149/192/252；分母654含87个无谓词祖先的虚根链。数量评分前10两个端点各自命中385，同一候选同时命中342，完整链252。前5核验3270条，3115可行、155无合法整句树、0解码预算耗尽，192个前5金标路径均有合法树见证。重排前1/3/5命中113/181/192，相较56/149/192首位恢复63失6。注意谓词端点前5命中从307降至299；局部树核验会改变端点覆盖，不能宣称所有指标改善。

## B. 直接按整句最优分数枚举不同路径
固定词元与词性、有限单根投射树域，路径取从起点至首个谓词或虚根。一个子域由固定路径前缀和禁止其末端节点使用的下一头集合表示。对该子域运行原精确解码器，得到最大分树及其投影路径p。去除所有投影为p的树后，将剩余树按首次与p不同的下一头位置分割：在原前缀末端分裂时累加旧禁止头，后续分裂时固定更长前缀并仅禁相应头。每棵不同投影的树恰属一个子域；这些子域互斥、覆盖剩余树。同一投影的其他树已被剔除，故不重复计算其路径。优先取各待处理子域最高树分，输出的不同路径依其最优整句树分非增排序。平分以固定插入序处理，不保证字典序；未枚举全部同分树，不能说唯一最优。每次子域解码上限沿原函数，新增每NUM最多300次解码；若子域未求解，停止并保留已经确认的前缀列表LIMIT，不能把余域当不存在。不同于A，B未限定6弧，但有限树无环。B只保证固定图与分数下的最优路径序，不能据分数推导语义、概率或证据资格。
150个1..5词元有限评分矩阵直接穷举所有合法树，按投影路径归组保留最大树分，核对前5分数序及每条路径各自最大分。含禁弧、无树及平分；150个零解码预算控制。同一研究者实现参照与候选，不是独立验收。真实开发集对全部654个已知NUM执行前5全局路径；不根据金标调参。对与A同一评分的前5可行路径，逐位核对B最优分不低于A，比较匹配增益和损失。实际资源计数是解码调用数、堆出入次数，未测真实CPU、RSS、Mac/iPhone；Eisner单次O(n^3)时间/O(n^2)空间，分裂最坏每输出至多n次求解，前K约O(K*n^4)时间上界（另有矩阵复制、队列、回溯），不是已证明低延迟。局部搜索最坏指数，正代价不消除组合规模。

## 实际复算结果（第二轮）
```json
{
  "sentences": 500,
  "num": 654,
  "predicate": 567,
  "rawExact": 540,
  "rawLocal10": 215,
  "rawGlobal5": 162,
  "localOracle": 100,
  "globalOracle": 150,
  "budgetControls": 250,
  "local": {
    "old": {
      "pops": 12659,
      "pushes": 185855,
      "maxPops": 33,
      "maxPushes": 1556,
      "limited": 0,
      "chain": [
        45,
        132,
        176,
        239
      ],
      "predicateChain": [
        33,
        114,
        154,
        211
      ],
      "rootChain": [
        12,
        18,
        22,
        28
      ],
      "both": [
        69,
        193,
        257,
        329
      ],
      "separate": [
        69,
        206,
        292,
        382
      ]
    },
    "typed": {
      "pops": 13043,
      "pushes": 198023,
      "maxPops": 36,
      "maxPushes": 1691,
      "limited": 0,
      "chain": [
        56,
        149,
        192,
        252
      ],
      "predicateChain": [
        43,
        131,
        170,
        224
      ],
      "rootChain": [
        13,
        18,
        22,
        28
      ],
      "both": [
        93,
        245,
        284,
        342
      ],
      "separate": [
        93,
        252,
        303,
        385
      ]
    }
  },
  "witness": {
    "calls": 3270,
    "feasible": 3115,
    "noTree": 155,
    "limit": 0,
    "goldPool": 192,
    "goldFeasible": 192,
    "rerank": [
      113,
      181,
      192
    ],
    "local": [
      56,
      149,
      192
    ],
    "rerankPred": [
      219,
      294,
      299
    ],
    "localPred": [
      58,
      252,
      307
    ],
    "rescued": 63,
    "lost": 6,
    "zeroRegret": 504
  },
  "global": {
    "calls": 7944,
    "impossible": 0,
    "limited": 0,
    "exhausted": 0,
    "maxCalls": 65,
    "chain": [
      90,
      159,
      193
    ],
    "predicateChain": [
      88,
      157,
      189
    ],
    "rootChain": [
      2,
      2,
      4
    ],
    "end": [
      259,
      339,
      397
    ],
    "gainVsRerank": [
      2,
      11,
      29
    ],
    "lossVsRerank": [
      25,
      33,
      28
    ],
    "maxDepth": 20,
    "over6": 450,
    "scoreDominance": 654,
    "topScoreTies": 306
  }
}
```
原文数词精确锚540/654，条件化A前10且原文锚存在215项。B同样只作交集诊断，未生成原始分词或词性。没有原生数量框架、实际业务语义、数学模型及权限连接，所有研究候选无权威且outside true；不得替代原生安全确认。自行选定路径代理、代价、6弧、K及预算；已见数据结果不能直接批准产品评分或预测开放文本效果。

## 完整复算
标准JS输入raw为固定外部dev文件，auditReport、projectiveReport、previousReport为上述三个固定本库报告全文。仅抽取已经审阅的项目自有代码，外部数据不执行。
```js
const c=s=>s.split("```js\n")[1].split("\n```")[0];
const verified=Function(c(auditReport).split("console.log(JSON.stringify(audit(raw)")[0]+"\nreturn audit;")()(raw);
const P=Function(c(projectiveReport).split(" const out={sentences:")[0]+"\nreturn {valid,score,decode,matrix};\n}\nreturn experiment();")();
const pcode=c(previousReport),start=pcode.indexOf(" function matrix(ts,mode)"),end=pcode.indexOf(" function rank(",start);
const matrix=Function("P",`const nom=new Set(["NOUN","PROPN","PRON"]),clfs=new Set(["个","名","位","只","件","次","项","套","家","本","辆","张","条","台","所","种","部","人","年","月","日","天","小时","分钟","米","公里","元","岁"]);${pcode.slice(start,end)};return matrix;`)(P);
function research(P,matrix,raw){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),pred=new Set(["VERB","ADJ","AUX"]);
 function lex(a,b){for(let i=0;i<Math.min(a.length,b.length);i++)if(a[i]!==b[i])return a[i]-b[i];return a.length-b.length}
 const cmp=(a,b)=>a.cost-b.cost||lex(a.path,b.path);
 function path(i,h,t){let p=[i];do{p.push(h[p.at(-1)]);ck(p.length<=h.length,"cycle")}while(!t(p.at(-1)));return p}
 function costs(w){let max=w[0].map((_,i)=>Math.max(...w.map(x=>x[i])));return w.map((row,p)=>row.map((v,i)=>Number.isFinite(v)?max[i]-v+1:Infinity))}
 function local(C,start,t,K=10,D=6,cap=20000){
  const H=[];let pops=0,pushes=0;
  function push(x){let i=H.length;H.push(x);pushes++;while(i){let p=(i-1)>>1;if(cmp(H[p],x)<=0)break;H[i]=H[p];i=p;H[i]=x}}
  function pop(){let z=H[0],x=H.pop();if(H.length){let i=0;H[0]=x;while(2*i+1<H.length){let j=2*i+1;if(j+1<H.length&&cmp(H[j+1],H[j])<0)j++;if(cmp(H[j],x)>=0)break;H[i]=H[j];i=j;H[i]=x}}return z}
  const rows=[];push({path:[start],cost:0});
  while(H.length&&rows.length<K){if(pops>=cap)return {status:"LIMIT",rows,pops,pushes};let x=pop(),i=x.path.at(-1);pops++;if(x.path.length>1&&t(i)){rows.push(x);continue}if(x.path.length-1===D)continue;for(let p=0;p<C.length;p++)if(!x.path.includes(p)&&Number.isFinite(C[p][i]))push({path:[...x.path,p],cost:x.cost+C[p][i]})}
  return {status:rows.length===K?"TOP_K":"EXHAUSTED",rows,pops,pushes};
 }
 function restricted(w,prefix,bans=[]){
  let f=w.map(x=>x.slice());
  for(let j=1;j<prefix.length;j++)for(let h=0;h<w.length;h++)if(h!==prefix[j])f[h][prefix[j-1]]=-Infinity;
  for(let h of bans)f[h][prefix.at(-1)]=-Infinity;
  let d=P.decode(f);if(d.status==="CANDIDATE"){ck(prefix.slice(0,-1).every((i,j)=>d.heads[i]===prefix[j+1])&&!bans.includes(d.heads[prefix.at(-1)]),"restriction");ck(P.valid(d.heads,true)&&P.score(w,d.heads)===d.best,"witness")}return d;
 }
 // Partition tree sets by the first differing edge of the returned path.
 function global(w,start,t,K=5,cap=300){
  let calls=0,impossible=0,serial=0,queue=[],rows=[],limited=false;
  function add(prefix,bans){
   if(calls===cap){limited=true;return}
   calls++;let d=restricted(w,prefix,bans);
   if(d.status==="LIMIT"){limited=true;return}if(d.status==="NO_TREE"){impossible++;return}
   ck(d.status==="CANDIDATE","decoder");
   const p=path(start,d.heads,t);ck(eq(p.slice(0,prefix.length),prefix),"prefix");
   queue.push({prefix,bans,path:p,score:d.best,serial:serial++});
  }
  add([start],[]);
  while(!limited&&queue.length&&rows.length<K){
   queue.sort((a,b)=>b.score-a.score||a.serial-b.serial);let z=queue.shift();
   ck(!rows.some(x=>eq(x.path,z.path)),"partition duplicate");
   rows.push({path:z.path,score:z.score});
   if(rows.length===K)break;
   for(let j=z.prefix.length-1;j<z.path.length-1&&!limited;j++){
    let prefix=z.path.slice(0,j+1),bans=j===z.prefix.length-1?[...z.bans,z.path[j+1]]:[z.path[j+1]];
    add(prefix,bans);
   }
  }
  return {status:limited?"LIMIT":rows.length===K?"TOP_K":"EXHAUSTED",rows,calls,impossible,authority:"NONE",outside:true};
 }
 function bruteLocal(C,start,t,K,D){let o=[];function go(p,s){let i=p.at(-1);if(p.length>1&&t(i)){o.push({path:p,cost:s});return}if(p.length-1===D)return;for(let j=0;j<C.length;j++)if(!p.includes(j)&&Number.isFinite(C[j][i]))go([...p,j],s+C[j][i])}go([start],0);return o.sort(cmp).slice(0,K)}
 function bruteGlobal(w,start,t){let h=Array(w.length).fill(-1),m=new Map();function go(i){if(i===h.length){if(P.valid(h,true)){let p=path(start,h,t),key=p.join(","),s=P.score(w,h);if(!m.has(key)||m.get(key).score<s)m.set(key,{path:p,score:s})}return}for(let j=0;j<h.length;j++)if(Number.isFinite(w[j][i])){h[i]=j;go(i+1)}}go(1);return m}
 const out={sentences:0,num:0,predicate:0,rawExact:0,rawLocal10:0,rawGlobal5:0,localOracle:0,globalOracle:0,budgetControls:0,local:{},witness:{calls:0,feasible:0,noTree:0,limit:0,goldPool:0,goldFeasible:0,rerank:[0,0,0],local:[0,0,0],rerankPred:[0,0,0],localPred:[0,0,0],rescued:0,lost:0,zeroRegret:0},global:{calls:0,impossible:0,limited:0,exhausted:0,maxCalls:0,chain:[0,0,0],predicateChain:[0,0,0],rootChain:[0,0,0],end:[0,0,0],gainVsRerank:[0,0,0],lossVsRerank:[0,0,0],maxDepth:0,over6:0,scoreDominance:0,topScoreTies:0}};
 for(let mode of ["old","typed"])out.local[mode]={pops:0,pushes:0,maxPops:0,maxPushes:0,limited:0,chain:[0,0,0,0],predicateChain:[0,0,0,0],rootChain:[0,0,0,0],both:[0,0,0,0],separate:[0,0,0,0]};
 for(let n=2;n<=6;n++)for(let seed=0;seed<20;seed++){
  let C=Array.from({length:n+1},(_,p)=>Array.from({length:n+1},(_,i)=>!i||p===i||(p*7+i*3+seed)%11===0?Infinity:1+((p*13+i*19+seed*7+p*i*3)%9))),t=i=>i===0||i===n,K=1+seed%10,D=1+seed%5;
  ck(eq(local(C,1,t,K,D).rows,bruteLocal(C,1,t,K,D)),"local oracle");out.localOracle++;
  ck(local(C,1,t,K,D,0).status==="LIMIT","local cap");out.budgetControls++;
 }
 for(let n=1;n<=5;n++)for(let seed=0;seed<30;seed++){
  let w=Array.from({length:n+1},(_,p)=>Array.from({length:n+1},(_,i)=>!i||p===i||(seed%4===0&&(p*13+i*7+seed)%5===0)?-Infinity:((p*37+i*19+seed*23+p*i*11)%17)-8)),t=i=>i===0||(n>1&&i===n),m=bruteGlobal(w,1,t),z=global(w,1,t,5);
  const scores=[...m.values()].map(x=>x.score).sort((a,b)=>b-a).slice(0,5);
  ck(z.status!=="LIMIT"&&eq(z.rows.map(x=>x.score),scores)&&z.rows.every(x=>m.get(x.path.join(","))?.score===x.score),"global oracle");out.globalOracle++;
  ck(global(w,1,t,5,0).status==="LIMIT","global cap");out.budgetControls++;
 }
 for(const block of raw.trimEnd().split(/\n\n+/)){
  const lines=block.split("\n"),txt=lines.find(x=>x.startsWith("# text = ")).slice(9),ts=[null,...lines.filter(x=>!x.startsWith("#")).map(x=>x.split("\t")).filter(c=>/^[1-9]\d*$/.test(c[0])).map(c=>({id:+c[0],form:c[1],pos:c[3],head:+c[6],misc:c[9]}))];
  let cur=0;for(let t of ts.slice(1)){t.a=cur;cur+=[...t.form].length;t.b=cur;if(!t.misc.split("|").includes("SpaceAfter=No"))cur++}
  const A=[...txt.matchAll(/[0-9０-９零〇一二两俩三四五六七八九十百千万亿壹贰叁肆伍陆柒捌玖拾佰仟萬億]+(?:[.．点][0-9０-９零〇一二两三四五六七八九]+)?/gu)].map(m=>{let a=[...txt.slice(0,m.index)].length;return [a,a+[...m[0]].length]});
  const gold=ts.map(x=>x?.head??-1),t=i=>i===0||pred.has(ts[i].pos),nums=ts.slice(1).filter(x=>x.pos==="NUM");out.sentences++;if(!nums.length)continue;
  let w={old:matrix(ts,"old"),typed:matrix(ts,"typed")},C={old:costs(w.old),typed:costs(w.typed)},base=P.decode(w.typed);ck(base.status==="CANDIDATE","base");
  for(let num of nums){
   let g=path(num.id,gold,t),has=g.at(-1)!==0,rx=A.some(([a,b])=>a===num.a&&b===num.b);out.num++;out.predicate+=+has;out.rawExact+=+rx;
   const hit=rows=>rows.some(x=>eq(x.path,g)),ep=rows=>rows.some(x=>x.path.at(-1)===g.at(-1));
   let pool;
   for(let mode of ["old","typed"]){
    let z=local(C[mode],num.id,t),o=out.local[mode],rows=z.rows;o.pops+=z.pops;o.pushes+=z.pushes;o.maxPops=Math.max(o.maxPops,z.pops);o.maxPushes=Math.max(o.maxPushes,z.pushes);o.limited+=+(z.status==="LIMIT");
    [1,3,5,10].forEach((k,j)=>{let s=rows.slice(0,k),h=hit(s);o.chain[j]+=+h;o.predicateChain[j]+=+(h&&has);o.rootChain[j]+=+(h&&!has);o.both[j]+=+s.some(x=>x.path[1]===g[1]&&x.path.at(-1)===g.at(-1));o.separate[j]+=+(ep(s)&&s.some(x=>x.path[1]===g[1]))});
    if(mode==="typed"){pool=rows.slice(0,5);out.rawLocal10+=+(rx&&hit(rows))}
   }
   let q=out.witness,feasible=[];q.goldPool+=+hit(pool);
   for(let [i,x] of pool.entries()){let d=restricted(w.typed,x.path);q.calls++;if(d.status==="NO_TREE"){q.noTree++;continue}if(d.status==="LIMIT"){q.limit++;continue}ck(d.status==="CANDIDATE"&&d.best<=base.best,"local tree");q.feasible++;q.zeroRegret+=+(d.best===base.best);feasible.push({...x,score:d.best,order:i})}
   feasible.sort((a,b)=>b.score-a.score||a.order-b.order);q.goldFeasible+=+hit(feasible);
   [1,3,5].forEach((k,j)=>{q.local[j]+=+hit(pool.slice(0,k));q.rerank[j]+=+hit(feasible.slice(0,k));q.localPred[j]+=+(has&&ep(pool.slice(0,k)));q.rerankPred[j]+=+(has&&ep(feasible.slice(0,k)))});
   q.rescued+=+(!hit(pool.slice(0,1))&&hit(feasible.slice(0,1)));q.lost+=+(hit(pool.slice(0,1))&&!hit(feasible.slice(0,1)));
   let z=global(w.typed,num.id,t,5),o=out.global;o.calls+=z.calls;o.impossible+=z.impossible;o.maxCalls=Math.max(o.maxCalls,z.calls);o.limited+=+(z.status==="LIMIT");o.exhausted+=+(z.status==="EXHAUSTED");
   ck(z.rows.length&&z.rows[0].score===base.best,"global first");
   if(z.status!=="LIMIT"){ck(feasible.every((x,j)=>z.rows[j]&&z.rows[j].score>=x.score),"score dominance");o.scoreDominance++}
   o.topScoreTies+=+(z.rows.length>1&&z.rows[0].score===z.rows[1].score);
   for(let x of z.rows){o.maxDepth=Math.max(o.maxDepth,x.path.length-1);o.over6+=+(x.path.length-1>6)}
   [1,3,5].forEach((k,j)=>{let s=z.rows.slice(0,k),h=hit(s),old=hit(feasible.slice(0,k));o.chain[j]+=+h;o.predicateChain[j]+=+(h&&has);o.rootChain[j]+=+(h&&!has);o.end[j]+=+ep(s);o.gainVsRerank[j]+=+(h&&!old);o.lossVsRerank[j]+=+(old&&!h)});
   out.rawGlobal5+=+(rx&&hit(z.rows));
  }
 }
 ck(out.num===654&&out.predicate===567&&out.rawExact===540,"denominator");
 ck(eq(out.local.typed.chain,[56,149,192,252])&&eq(out.witness.rerank,[113,181,192])&&out.witness.noTree===155,"repeat");
 return out;
}
console.log(JSON.stringify(research(P,matrix,raw),null,2));
```
实际执行于连接器标准JS，未另跑Node文件包装。报告只含项目原创代码及聚合计数。
## 治理
未运行完整v0.8、真实用户、独立留出、真机、竞品、训练、生产修改、合并PR、部署、主动CI或新增费用。冻结协议、原验收、唯一交接不变。下一步应把词法来源与有限共同分词见证接入树路径接口，先验证不提供人工分词词性时的实际覆盖；当前条件化诊断不能视为开放语言能力。
