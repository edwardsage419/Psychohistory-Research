# 自主认知：外部静态词汇知识、全局分词与最优路径歧义
2026-11-26。RESEARCH_CANDIDATE / EXTERNAL_LEXICON_AND_DEVELOPMENT_BYTES_VERIFIED / NO_TRAINING / RAW_TEXT_SEGMENTATION / INDEPENDENT_NOT_RUN / FULL_NATIVE_NOT_RUN。
## 基线与去重
起始main 642166812612a6a761faf41b09afcbf405a429fa；核对12近期提交、15开放PR、v3.2/同步规程/唯一产品交接/前轮词边界报告前15行，唯一交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07。Draft #63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍draft/unmerged。检索CEDICT/lexicon/dictionary/segmentation/word lattice/lexical knowledge。前轮只构造原文候选格与最长基线；本轮新增静态外部词典、无训练全局选择、所有最优路径强制词边的计数。全库去重有限。原生代码、完整语义及设备未运行。
## 固定来源、许可、证据
CC-CEDICT，MDBG发布、社区编纂，基于Paul Andrew Denisowski 1997/1998 CEDICT。英文官方页 https://www.mdbg.net/chinese/dictionary?page=cc-cedict 和 https://cc-cedict.org/editor/editor.php?handler=Download 实际检索；明确CC BY-SA 4.0归属和相同许可。读取第三方镜像 https://github.com/rhcarvalho/cedict/blob/6317ff202e14be60365c826f62e45fc9fa71d19e/cedict_1_0_ts_utf-8_mdbg.txt 固定commit 6317ff202e14be60365c826f62e45fc9fa71d19e README及Git blob d7fee8237f26524b38eee220647e4c5d79f00de9；fetch_file内容为空，改用fetch_blob实际取得全文。头部date 2026-11-24T20:43:35Z, entries=125474, license CC BY-SA 4.0。自行流式UTF8 Git SHA1重算与镜像一致（含CRLF），证明镜像字节身份，不证明官方独立快照逐字相同或词义正确。只读取词条头部，未使用英文释义、拼音、统计频次、权重、训练或任何第三方AI推理。衍生词汇表单独许可管理，未来发布须归属及相同许可审定；本报告仅聚合统计和原创算法，未重新分发词条正文、词典或第三方语料。外部词典本身不是自主原创词汇知识成果；系统自主维护的是候选选择和来源机制。无需购买数据。
UD Chinese GSDSimp dev 固定commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3 blob af8cc878e7934b38ce3c1a266053100e7c47de6f；复用R134审计 research/decision_hub/2026-11-25-external-ud-development-corpus-structural-audit.md blob db9cc100d96d49832fe32879a706f63830301773 实际复算UTF8长度1195378及Git SHA1。复用上一轮 research/decision_hub/2026-11-26-external-raw-word-lattice-diagnostic.md blob 86dcd5387b89c5302b1c139ad57a17b22f5d5a1d 的原文范围、对齐、贪心函数。首次加载前轮函数因缺少auditDoc参数报错，改为提取已审阅的独立函数块，未改变原算法，完整实验重跑两次。只读已见wiki dev，非真人个人决策、独立留出或训练。未访问任何train/test，标注/底层文本许可仍分离；不借用人工FORM/UPOS/HEAD作为算法输入。词典与wiki可能存在文本相关性，未证明无污染；不能当独立跨来源泛化。
## 方法
从镜像严格匹配繁体、简体、拼音、释义起始格式；词长上限16 Unicode标量、保留简体头词去重。传统头词数量仅在同一筛选范围统计，不做繁简转换或传统测试。使用原开放格查询词典，未知单字兜底（标点代价0，其他未知字代价1），空白强制跳过。字典边成本(0,1)，未知字成本(1,1)，空白(0,0)；取字典头词和未知单字合法路径中先最小未知字，再最小词数的词典序目标。globalStructured增加有限长度同类连续数字/拉丁字符最长边，计(0,1)，属于字符结构启发式，未证明数词/实体语义；若边已在词典中不重复计数。对比单字、无词典类别双字、词典前向/反向最长匹配和两全局算法。固定规则在本轮评分前选定，没有拟合参数或根据标注造词典。先生成全部候选，再读取金标。注意全部结构边及词典边只是假设，不保证词义、角色、义务、主体、时间或计算资格。未验证真实设备资源。
全局DP对每节点存最小字典序成本D(i)及达到该成本的后缀路径数N(i)，N(n)=1；等成本边的后缀计数求和。只遍历最优边，P(i)为最优前缀路径数。边(i,j)的最优完整路径次数为P(i)N(j)，等于N(0)时该边为所有最优路径共有。保留多个最优路径的联合图，而非独立边际组合；单一返回路径以较长边打破并列，仅为评分基线。最优图中的强制词边不等于真实词边或置信概率；全局评分错误会在全部最优路径中一致发生，必须保留未知。completeOptimalGold只统计所有金标边均在最优图；因精确无重叠覆盖原文且最优边满足DP，整条金标路径属于该图（空白跳过边固定）。对短句和16个自造控制以直接枚举全部路径核对成本、计数、强制边。未做完整语义或词频统计学习。
## 实测
| 模式 | 预测词数 | 精确命中 | Precision % | Recall % | F1 % | 整句完全匹配 |
|---|---:|---:|---:|---:|---:|---:|
| char | 20000 | 6444 | 32.22 | 50.88 | 39.46 | 0 |
| script2 | 11511 | 5725 | 49.74 | 45.20 | 47.36 | 1 |
| dictForward | 13556 | 9676 | 71.38 | 76.40 | 73.80 | 19 |
| dictReverse | 13556 | 9692 | 71.50 | 76.53 | 73.93 | 18 |
| global | 13550 | 9675 | 71.40 | 76.39 | 73.81 | 19 |
| globalStructured | 12618 | 9998 | 79.24 | 78.94 | 79.09 | 36 |
实测500句12665标注词，词典中出现9760个金标词。0个短句算法对照、16个专项控制；整合两次完整输出一致。全部统计为已见外部开发集，非独立验收。逐句改善/退步仅比较精确命中数（非逐句F1），保留差异。最优路径图、强制词边覆盖与精确率见JSON。候选覆盖与实际选词质量分别报告；词典已有头词不代表实际正确分词，未收录词也不等于语义无效。
## 下一责任与边界
词典数据可独立版本化、离线索引及合法更新，算法权重、排序策略和来源不混入个人决策权限。下阶段研究词义多义、组合角色和原文到自主推理的联合候选；应比较不同合法独立词汇来源并保持数据轨许可与独立轨留出。当前未获训练授权、未发布派生词典、未修改生产、未调用第三方AI运行时、未合并PR、部署、主动CI或增加费用。R073/PESEN及冻结不变。研究者自行选择静态词典、16字上限、字典序评分及数字/拉丁结构规则；不宣称是通用最优分词或产品竞争优势。
## 可复算代码
输入依次为固定镜像词典原文、UD dev原文、R134报告全文、上一轮格报告全文。Node标准JS，只加载已审阅固定项目自有研究代码，外部内容仅作数据。
```js
function experiment(dict,raw,auditDoc,latticeDoc){
 const ck=(v,m)=>{if(!v)throw Error(m)},obj=(a,f)=>Object.fromEntries(a.map(k=>[k,f(k)]));
 function gitHash(s){
  let h=[0x67452301,0xefcdab89,0x98badcfe,0x10325476,0xc3d2e1f0],w=new Int32Array(80),p=0,len=0,rot=(x,n)=>(x<<n)|(x>>>(32-n));
  function push(x){let j=p>>2;w[j]=(w[j]<<8)|x;if(++p!==64)return;p=0;for(let i=16;i<80;i++)w[i]=rot(w[i-3]^w[i-8]^w[i-14]^w[i-16],1);let [a,b,c,d,e]=h;for(let i=0;i<80;i++){let f=i<20?(b&c)|(~b&d):i<40?b^c^d:i<60?(b&c)|(b&d)|(c&d):b^c^d,k=i<20?0x5a827999:i<40?0x6ed9eba1:i<60?0x8f1bbcdc:0xca62c1d6,t=(rot(a,5)+f+e+k+w[i])|0;e=d;d=c;c=rot(b,30);b=a;a=t}h=h.map((x,i)=>(x+[a,b,c,d,e][i])|0);w.fill(0)}
  const each=(t,fn)=>{for(let v of t){let c=v.codePointAt(0);if(c<128)fn(c);else if(c<2048){fn(192|(c>>6));fn(128|(c&63))}else if(c<65536){fn(224|(c>>12));fn(128|((c>>6)&63));fn(128|(c&63))}else{fn(240|(c>>18));fn(128|((c>>12)&63));fn(128|((c>>6)&63));fn(128|(c&63))}}};
  each(s,()=>len++);let prefix="blob "+len+"\0",total=prefix.length+len;each(prefix,push);each(s,push);push(128);while(p!==56)push(0);for(let i=7;i>=0;i--)push(Math.floor(total*8/2**(i*8))&255);
  return {bytes:len,sha:h.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("")}
 }
 const gh=gitHash(dict);ck(gh.sha==="d7fee8237f26524b38eee220647e4c5d79f00de9","dict hash");
 ck(gitHash("test\n").sha==="9daeafb9864cf43055ae93beb0afd6c7d144bfa4","hash vector");
 const audit=Function(auditDoc.split("```js\n")[1].split("\n```")[0].split("console.log(JSON.stringify(audit(raw)")[0]+"\nreturn audit;")(),verified=audit(raw);
 const src=latticeDoc.split("```js\n")[1].split("\n```")[0];
 const L=Function("const key=(i,j)=>i+':'+j;\n"+src.slice(src.indexOf(" const cls="),src.indexOf(" const blank="))+"\nreturn {ranges,align,cls,greedy};")();
 let words=new Set(),entries=0,invalid=0,excluded=0,trad=new Set(),max=0;
 for(let line of dict.split(/\r?\n/)){if(!line||line.startsWith("#"))continue;entries++;let m=/^(\S+) (\S+) \[.*?\] \//u.exec(line);if(!m){invalid++;continue}let s=m[2];if([...s].length>16||/\s/u.test(s)){excluded++;continue}words.add(s);trad.add(m[1]);max=Math.max(max,[...s].length)}
 ck(entries===125474&&invalid===0,"entries");const modes=["char","script2","dictForward","dictReverse","global","globalStructured"];
 function graph(chars,structured){
  let rs=L.ranges(chars,16,"open");return rs.map(({i,lo,hi,skip})=>{
   if(skip)return [{i,j:i+1,c:[0,0],skip:true}];
   let edges=[];for(let j=lo;j<=hi;j++){let s=chars.slice(i,j).join("");if(words.has(s))edges.push({i,j,c:[0,1],known:true})}
   if(!edges.some(e=>e.j===i+1))edges.push({i,j:i+1,c:[L.cls(chars[i])==="punct"?0:1,1],known:false});
   if(structured&&["digit","latin"].includes(L.cls(chars[i]))){let j=i+1;while(j<hi&&L.cls(chars[j])===L.cls(chars[i]))j++;if(j>i+1&&!edges.some(e=>e.j===j))edges.push({i,j,c:[0,1],known:false,structured:true})}
   return edges.sort((a,b)=>b.j-a.j)
  })
 }
 const cmp=(a,b)=>a[0]-b[0]||a[1]-b[1],plus=(a,b)=>[a[0]+b[0],a[1]+b[1]],key=e=>e.i+":"+e.j;
 function global(g){
  let n=g.length,dp=Array(n+1),count=Array(n+1).fill(0n),back=Array(n+1);dp[n]=[0,0];count[n]=1n;
  for(let i=n-1;i>=0;i--)for(let e of g[i]){let c=plus(e.c,dp[e.j]);if(!dp[i]||cmp(c,dp[i])<0){dp[i]=c;count[i]=count[e.j];back[i]=e}else if(cmp(c,dp[i])===0)count[i]+=count[e.j]}
  let prefix=Array(n+1).fill(0n);prefix[0]=1n;let forced=[],optimalEdges=[],pred=[];
  for(let i=0;i<n;i++)for(let e of g[i])if(cmp(plus(e.c,dp[e.j]),dp[i])===0&&prefix[i]){prefix[e.j]+=prefix[i];if(!e.skip){optimalEdges.push(e);if(prefix[i]*count[e.j]===count[0])forced.push(e)}}
  for(let i=0;i<n;){let e=back[i];if(!e.skip)pred.push(e);i=e.j}
  ck(prefix[n]===count[0],"path count");return {pred,forced,optimalEdges,count:count[0],cost:dp[0]}
 }
 function greedy(g,rev){let n=g.length,z=[];if(!rev){for(let i=0;i<n;){let e=g[i][0];if(!e.skip)z.push(e);i=e.j}}else{let ends=Array.from({length:n+1},()=>[]);for(let es of g)for(let e of es)ends[e.j].push(e);for(let j=n;j>0;){let e=ends[j].sort((a,b)=>a.i-b.i)[0];if(!e.skip)z.push(e);j=e.i}z.reverse()}return z}
 function brute(g){let best=null,paths=[];function rec(i,c,p){if(i===g.length){if(!best||cmp(c,best)<0){best=c;paths=[p]}else if(cmp(c,best)===0)paths.push(p);return}for(let e of g[i])rec(e.j,plus(c,e.c),[...p,e])}rec(0,[0,0],[]);let forced=paths[0].filter(e=>!e.skip&&paths.every(p=>p.some(x=>key(x)===key(e))));return {cost:best,count:BigInt(paths.length),forced:forced.map(key).sort()}}
 let o={dictionary:{...gh,entries,invalid,excluded,uniqueSimplified:words.size,uniqueTraditional:trad.size,max},source:{sentences:verified.sentences,tokens:verified.tokens,gitBlob:verified.gitBlob},sentences:0,tokens:0,lexiconGold:0,metrics:obj(modes,m=>({pred:0,hit:0,exact:0})),ambiguity:obj(["global","globalStructured"],m=>({sentences:0,forced:0,forcedHit:0,optimalEdges:0,optimalGoldHit:0,completeOptimalGold:0,multi:0,maxCountBits:0,unknownChars:0,graphEdges:0})),controls:0,bruteChecks:0,changes:obj(["global","globalStructured"],m=>({improved:0,regressed:0,equal:0}))};
 for(let block of raw.trimEnd().split(/\n\n+/)){let lines=block.split("\n"),text=lines.find(x=>x.startsWith("# text = ")).slice(9),chars=[...text],rows=lines.filter(x=>!x.startsWith("#")).map(x=>x.split("\t")).filter(c=>/^[1-9]\d*$/.test(c[0]));
  let g=graph(chars,false),gs=graph(chars,true),p=global(g),ps=global(gs),toEdges=x=>x.map(k=>{let [i,j]=k.split(":").map(Number);return {i,j}}),preds={char:toEdges(L.greedy(L.ranges(chars,1,"open"))),script2:toEdges(L.greedy(L.ranges(chars,2,"script"))),dictForward:greedy(g,false),dictReverse:greedy(g,true),global:p.pred,globalStructured:ps.pred};
  let gold=L.align(chars,rows.map(c=>c[1]));ck(gold,"alignment");let s=new Set(gold.map(([i,j])=>i+":"+j));o.sentences++;o.tokens+=gold.length;o.lexiconGold+=rows.filter(c=>words.has(c[1])).length;
  let hits={};for(let m of modes){let z=preds[m],v=o.metrics[m],hit=z.filter(e=>s.has(key(e))).length;hits[m]=hit;v.pred+=z.length;v.hit+=hit;v.exact+=+(hit===z.length&&z.length===gold.length)}
  for(let [m,v,gg] of [["global",p,g],["globalStructured",ps,gs]]){let q=o.ambiguity[m],ss=new Set(v.optimalEdges.map(key));q.sentences++;q.forced+=v.forced.length;q.forcedHit+=v.forced.filter(e=>s.has(key(e))).length;q.optimalEdges+=ss.size;q.optimalGoldHit+=[...s].filter(k=>ss.has(k)).length;q.completeOptimalGold+=+([...s].every(k=>ss.has(k)));q.multi+=+(v.count>1n);q.maxCountBits=Math.max(q.maxCountBits,v.count.toString(2).length);q.unknownChars+=v.cost[0];q.graphEdges+=gg.flat().filter(e=>!e.skip).length;let diff=hits[m]-hits.dictForward;o.changes[m][diff>0?"improved":diff<0?"regressed":"equal"]++;
   if(chars.length<=12){let z=brute(gg);ck(cmp(z.cost,v.cost)===0&&z.count===v.count&&JSON.stringify(z.forced)===JSON.stringify(v.forced.map(key).sort()),"brute");o.bruteChecks++}
  }
 }
 for(let s of ["","甲乙丙","南京市长江大桥","12.5","A𠀀B","甲 乙","不可能","研究生命起源"])for(let b of [false,true]){let g=graph([...s],b),p=global(g),z=brute(g);ck(cmp(z.cost,p.cost)===0&&z.count===p.count&&JSON.stringify(z.forced)===JSON.stringify(p.forced.map(key).sort()),"control");o.controls++}
 ck(o.sentences===500&&o.tokens===12665&&o.metrics.script2.hit===5725&&o.metrics.char.hit===6444,"baseline");
 for(let v of Object.values(o.metrics)){v.precision=v.hit/v.pred;v.recall=v.hit/o.tokens;v.f1=2*v.hit/(v.pred+o.tokens)}
 for(let v of Object.values(o.ambiguity)){v.forcedPrecision=v.forcedHit/v.forced;v.forcedRecall=v.forcedHit/o.tokens;ck(v.forced<=v.optimalEdges&&v.forcedHit<=v.optimalGoldHit,"subset")}
 return o
}
const fs=require("node:fs"); console.log(JSON.stringify(experiment(...process.argv.slice(2).map(p=>fs.readFileSync(p,"utf8"))),null,2));
```
## 实际聚合输出
```json
{
  "dictionary": {
    "bytes": 9881659,
    "sha": "d7fee8237f26524b38eee220647e4c5d79f00de9",
    "entries": 125474,
    "invalid": 0,
    "excluded": 4,
    "uniqueSimplified": 121696,
    "uniqueTraditional": 122890,
    "max": 15
  },
  "source": {
    "sentences": 500,
    "tokens": 12665,
    "gitBlob": "af8cc878e7934b38ce3c1a266053100e7c47de6f"
  },
  "sentences": 500,
  "tokens": 12665,
  "lexiconGold": 9760,
  "metrics": {
    "char": {
      "pred": 20000,
      "hit": 6444,
      "exact": 0,
      "precision": 0.3222,
      "recall": 0.5088037899723648,
      "f1": 0.3945507423848156
    },
    "script2": {
      "pred": 11511,
      "hit": 5725,
      "exact": 1,
      "precision": 0.4973503605247155,
      "recall": 0.45203316225819185,
      "f1": 0.4736101919258769
    },
    "dictForward": {
      "pred": 13556,
      "hit": 9676,
      "exact": 19,
      "precision": 0.7137798760696371,
      "recall": 0.763995262534544,
      "f1": 0.7380343999084703
    },
    "dictReverse": {
      "pred": 13556,
      "hit": 9692,
      "exact": 18,
      "precision": 0.7149601652404839,
      "recall": 0.765258586656139,
      "f1": 0.7392547957743794
    },
    "global": {
      "pred": 13550,
      "hit": 9675,
      "exact": 19,
      "precision": 0.7140221402214022,
      "recall": 0.7639163047769444,
      "f1": 0.7381270265115392
    },
    "globalStructured": {
      "pred": 12618,
      "hit": 9998,
      "exact": 36,
      "precision": 0.7923601204628309,
      "recall": 0.7894196604816424,
      "f1": 0.7908871573784757
    }
  },
  "ambiguity": {
    "global": {
      "sentences": 500,
      "forced": 13138,
      "forcedHit": 9497,
      "optimalEdges": 13967,
      "optimalGoldHit": 9871,
      "completeOptimalGold": 23,
      "multi": 154,
      "maxCountBits": 5,
      "unknownChars": 1398,
      "graphEdges": 26688,
      "forcedPrecision": 0.7228649718374182,
      "forcedRecall": 0.7498618239242005
    },
    "globalStructured": {
      "sentences": 500,
      "forced": 12208,
      "forcedHit": 9820,
      "optimalEdges": 13033,
      "optimalGoldHit": 10194,
      "completeOptimalGold": 43,
      "multi": 153,
      "maxCountBits": 5,
      "unknownChars": 112,
      "graphEdges": 27626,
      "forcedPrecision": 0.8043905635648755,
      "forcedRecall": 0.7753651796288985
    }
  },
  "controls": 16,
  "bruteChecks": 0,
  "changes": {
    "global": {
      "improved": 2,
      "regressed": 2,
      "equal": 496
    },
    "globalStructured": {
      "improved": 183,
      "regressed": 1,
      "equal": 316
    }
  }
}
```
