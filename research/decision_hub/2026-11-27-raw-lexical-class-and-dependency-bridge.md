# 自主认知：静态词义线索、粗词类序列与原文依存树连接
2026-11-27。RESEARCH_CANDIDATE / REAL_EXTERNAL_DEVELOPMENT_BYTES_VERIFIED / RAW_TEXT_SEGMENTATION_CLASS_TREE_EXECUTED / GOLD_BOUNDARY_ABLATION / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。

## 基线与去重
起点main a404afcb85b027c20edd16dbd85caf3deb0737a6。核对20近期提交、15开放PR、v3.2与同步规程全文、唯一产品交接前20行，PR #63 head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft未合并。读取目录词格/词性/分词相关题名、静态词典分词6eb499cc01f023f352167cbe886d2f3144136cc7、原文K优分词aa0d6c5882107b142dd555d0872b073da034a642、前序数量关系树见证7fb3086a5e8a3ebdec65230838fbfee34df17405前段。原文分词和人工词性条件下的树搜索已有；新增在固定分词上从静态释义和字符结构产生四类粗词性、序列解码及直接复用依存树函数，并消融金标词边界。只做局部查重，不称全库无重复或项目历史绝对首次。

## 固定来源及许可
实际两次完整读取CC-CEDICT镜像固定commit 6317ff202e14be60365c826f62e45fc9fa71d19e，blob d7fee8237f26524b38eee220647e4c5d79f00de9，9881659字节（含CRLF），头部125474 entries/date 2026-11-24/CC BY-SA 4.0；MDBG发布及社区编纂，基于Paul Andrew Denisowski 1997/1998 CEDICT。源 https://github.com/rhcarvalho/cedict/blob/6317ff202e14be60365c826f62e45fc9fa71d19e/cedict_1_0_ts_utf-8_mdbg.txt ；官方英文来源 https://www.mdbg.net/chinese/dictionary?page=cc-cedict 。本轮实际检查镜像许可头，沿用既有许可审查，未重读完整法律文本。实际解析简体头词及英文释义中的有限线索，不保存词条或派生索引到本库，不声称释义为正式UPOS标签。未来派生词典分发与训练须独立许可审定。
固定UD_Chinese-GSDSimp dev commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3，blob af8cc878e7934b38ce3c1a266053100e7c47de6f，1195378字节；来源 https://universaldependencies.org/treebanks/zh_gsdsimp/ ，标注CC BY-SA 4.0，底层文本权利分离。两份字节身份均复用静态词典研究和R134自有Git SHA1实际两次核验。500句12665词元，已见wiki公开开发集，非真实决策、独立留出、训练；未读train/test，未分发文本。词典与开发资料可能有来源关联，未证无污染。

四份固定本库报告完整读取并抽取自有已审阅函数，依次：
research/decision_hub/2026-11-26-static-lexicon-optimal-segmentation.md 6eb499cc01f023f352167cbe886d2f3144136cc7
research/decision_hub/2026-11-26-external-raw-word-lattice-diagnostic.md 86dcd5387b89c5302b1c139ad57a17b22f5d5a1d
research/decision_hub/2026-11-25-external-ud-development-corpus-structural-audit.md db9cc100d96d49832fe32879a706f63830301773
research/decision_hub/2026-11-25-projective-dependency-decoder-external-diagnostic.md c40a09357a858644a0da922097cd6367ca696df6

## 合同及方法
保持原静态词典globalStructured分词完全不变：先最小未知字符再最小词数，确定性选择一条最优路径；不从gold造词典或决定边界。粗类别N=名词/专名/代词，P=动词/形容词/助动词，Q=NUM，O=其他。仅四类代理，不能等同完整UPOS或语义角色。输入为原文词面；oracle分支额外给正确词边界，不提供词性或头。固定解释提示：显式括号类名、以to开头的英语释义作为P线索、a/an/the或显式名词线索为N，其他非空释义给弱N提示，多个释义取每类最高分；不是词典提供正式词性、词义消歧或概率。英文to也可能是介词、英语译法与中文词性并非一一对应；显式标记同样可能误配。形态基线固定N+1，数字完整形式Q+8，纯标点/符号O+12，有限功能词O+6。gloss加入释义线索，context在同样局部评分上通过Viterbi加相邻转移 Q→N +2、N→P及P→N +1；无拟合、无训练、研究者事前选择固定规则。其他转移0；可能对功能词、专名、真实谓词造成错误。每个词预测N/P/Q/O，映射到NOUN/VERB/NUM/X供原Eisner树求解器（纯标点/符号优先映射PUNCT，不同于粗词类统计）。全部500句合法单根投射树不代表正确解析。数量关系链从预测Q出发沿头到第一个预测P或虚根，原标注参照从NUM出发至第一个VERB/ADJ/AUX或虚根；必须原文跨度逐项匹配。包含87无谓词祖先的根链。正确头匹配精确原文依存词和头跨度或虚根；allArc不要求粗标签一致，numArc额外要求Q。只用已返回分词、粗标签、树，不输出实际角色、业务义务、可靠性、授权或数学参数。所有输出只作研究候选，authority NONE、outside true的产品边界沿用，原型统计函数不实现真实权限/未知门。固定分词先于词类，尚未真正联合优化分词、词类及树。

## A. 原文连续流程与金标边界消融
500句，12665词元，654数词。原分词基线12618预测词、9998精确词边、36完整分词句复现。原文粗词类正确须词边和四类同时相同；分母12665。原文数量结构结果：
| 方法 | 粗类正确 | 依存头正确 | Q且头正确 | Q且完整链正确 |
| --- | ---: | ---: | ---: | ---: |
| shape | 6822 | 1302 | 84 | 0 |
| gloss | 7779 | 1814 | 182 | 36 |
| context | 7729 | 1787 | 220 | 42 |
给正确边界条件下：
| 方法 | 粗类正确 | 依存头正确 | Q且头正确 | Q且完整链正确 |
| --- | ---: | ---: | ---: | ---: |
| shape | 8365 | 1937 | 94 | 3 |
| gloss | 9497 | 2626 | 216 | 43 |
| context | 9310 | 2663 | 261 | 51 |
首次执行与整理后第二次核心指标一致；首次输出含未使用的goldChains=0占位，不是语料计数，第二次移除。形态基线P全无，属于弱对照；静态词典为非学习竞争基线，不能据此称优于专业工具。context在原文下Q头+38、链+6、整体粗类-50、依存头-27；给正确分词仍明显有词类及结构错误。没有真实对话效果、当前原生入口、训练或新部署。
 
## B. 保留不同整句词类解释
在相同固定原文分词和context固定评分上，精确K优Viterbi：状态为末类b，保留至该状态分数前K的不同完整前缀，后继只依赖b，故每个被截断前缀已有K个不劣同状态替代，归纳保证最终前K。固定分数降序、标签字符串字典序打破平分（不同于A的局部回溯平分，单列一致数）；100个1..5词元整数矩阵与4^n完全枚举前4逐项一致。取K=1/2/4，分别对每个实际序列跑同一全局树解码；候选类型、依存头、NUM完整链在同句实际树之间取并集，只计去重原文锚。不是不同预算等算力比较，不把并集各边当同一树见证；每个完整链来自同一个实际树。完整词类句子要求同一个序列的全部边界及四类一致。只取4个序列、每个1棵树，不是完整可行域；没有概率、语义、生产准入。上下文转移固定且词类平分可能严重；同分备选不同不代表真实可信度。未测CPU、RSS、Mac/iPhone或模型优势。以下是第二次真实运行完整聚合输出（per数组顺序预测数、金标数、精确命中）：
```json
{
  "sentences": 500,
  "tokens": 12665,
  "nums": 654,
  "dictEntries": 125474,
  "headwords": 121696,
  "raw": {
    "shape": {
      "predicted": 12618,
      "spanHit": 9998,
      "classHit": 6822,
      "per": {
        "N": [
          8907,
          4867,
          3517
        ],
        "P": [
          0,
          2529,
          0
        ],
        "Q": [
          566,
          654,
          436
        ],
        "O": [
          3145,
          4615,
          2869
        ]
      },
      "allArc": 1302,
      "numArc": 84,
      "chain": 0,
      "eligibleChain": 436,
      "trees": 500
    },
    "gloss": {
      "predicted": 12618,
      "spanHit": 9998,
      "classHit": 7779,
      "per": {
        "N": [
          5815,
          4867,
          2978
        ],
        "P": [
          3070,
          2529,
          1491
        ],
        "Q": [
          566,
          654,
          436
        ],
        "O": [
          3167,
          4615,
          2874
        ]
      },
      "allArc": 1814,
      "numArc": 182,
      "chain": 36,
      "eligibleChain": 436,
      "trees": 500
    },
    "context": {
      "predicted": 12618,
      "spanHit": 9998,
      "classHit": 7729,
      "per": {
        "N": [
          5906,
          4867,
          3046
        ],
        "P": [
          3151,
          2529,
          1515
        ],
        "Q": [
          580,
          654,
          436
        ],
        "O": [
          2981,
          4615,
          2732
        ]
      },
      "allArc": 1787,
      "numArc": 220,
      "chain": 42,
      "eligibleChain": 436,
      "trees": 500
    }
  },
  "oracle": {
    "shape": {
      "predicted": 12665,
      "spanHit": 12665,
      "classHit": 8365,
      "per": {
        "N": [
          8975,
          4867,
          4862
        ],
        "P": [
          0,
          2529,
          0
        ],
        "Q": [
          542,
          654,
          541
        ],
        "O": [
          3148,
          4615,
          2962
        ]
      },
      "allArc": 1937,
      "numArc": 94,
      "chain": 3,
      "eligibleChain": 541,
      "trees": 500
    },
    "gloss": {
      "predicted": 12665,
      "spanHit": 12665,
      "classHit": 9497,
      "per": {
        "N": [
          6007,
          4867,
          4193
        ],
        "P": [
          2944,
          2529,
          1791
        ],
        "Q": [
          542,
          654,
          541
        ],
        "O": [
          3172,
          4615,
          2972
        ]
      },
      "allArc": 2626,
      "numArc": 216,
      "chain": 43,
      "eligibleChain": 541,
      "trees": 500
    },
    "context": {
      "predicted": 12665,
      "spanHit": 12665,
      "classHit": 9310,
      "per": {
        "N": [
          5879,
          4867,
          4113
        ],
        "P": [
          3125,
          2529,
          1837
        ],
        "Q": [
          684,
          654,
          547
        ],
        "O": [
          2977,
          4615,
          2813
        ]
      },
      "allArc": 2663,
      "numArc": 261,
      "chain": 51,
      "eligibleChain": 547,
      "trees": 500
    }
  },
  "controls": 6,
  "exactSeg": 36,
  "glossEvidence": 9760,
  "glossAmbiguous": 237,
  "kbest": {
    "oracleCases": 100,
    "paths": 2000,
    "tieFirst": 455,
    "contextSameFirst": 476,
    "bestScoreSame": 500,
    "byK": {
      "1": {
        "uniqueTypedSpans": 12618,
        "typedHits": 7724,
        "uniqueHeadPairs": 12618,
        "headHits": 1780,
        "numHeadHits": 220,
        "numChainHits": 42,
        "completeClassSentences": 0
      },
      "2": {
        "uniqueTypedSpans": 13131,
        "typedHits": 7839,
        "uniqueHeadPairs": 14280,
        "headHits": 1987,
        "numHeadHits": 238,
        "numChainHits": 44,
        "completeClassSentences": 0
      },
      "4": {
        "uniqueTypedSpans": 13920,
        "typedHits": 7909,
        "uniqueHeadPairs": 16139,
        "headHits": 2218,
        "numHeadHits": 246,
        "numChainHits": 48,
        "completeClassSentences": 1
      }
    },
    "goldCompleteClass": 0
  }
}
```

## 完整复算
标准JS变量dict/raw为上述固定第三方文件全文，docs为四个固定本库报告全文的数组。仅执行经审查的固定自有函数，第三方文件只作数据。Node包装未另执行。
```js
const c=s=>s.split("```js\n")[1].split("\n```")[0];
const L=Function(c(docs[0]).split(" let o={dictionary:")[0]+"\nreturn {graph,global,gh,verified};\n}\nreturn experiment;")()(dict,raw,docs[2],docs[1]);
const P=Function(c(docs[3]).split(" const out={sentences:")[0]+"\nreturn {valid,score,decode,matrix};\n}\nreturn experiment();")();
function study(dict,raw,L,P){
 const ck=(x,m)=>{if(!x)throw Error(m)},classes=["N","P","Q","O"],pred=new Set(["VERB","ADJ","AUX"]),nom=new Set(["NOUN","PROPN","PRON"]),coarse=p=>nom.has(p)?"N":pred.has(p)?"P":p==="NUM"?"Q":"O";
 const func=new Set("的 地 得 了 着 过 吗 呢 吧 啊 和 与 或 及 而 但 如果 因为 所以 在 从 对 向 被 把 将 很 更 最 都 也 又 不 没 未 无 就 才 还 已经 仅 只 每 各".split(" "));
 const nform=/^[0-9０-９零〇一二两俩三四五六七八九十百千万亿壹贰叁肆伍陆柒捌玖拾佰仟萬億]+(?:[.．点][0-9０-９零〇一二两三四五六七八九]+)?$/u;
 const punct=s=>/^[\p{P}\p{S}]+$/u.test(s),map=new Map();let entries=0;
 for(const line of dict.split(/\r?\n/)){
  if(!line||line.startsWith("#"))continue;let m=/^(\S+) (\S+) \[.*?\] \/(.*)\/$/u.exec(line);if(!m)throw Error("dict line");entries++;
  const s=m[2];if([...s].length>16||/\s/u.test(s))continue;
  let x=map.get(s)||[0,0,0,0];
  for(let g of m[3].split(/[\/;]/)){
   g=g.trim();let p=/^\((?:verb|adjective|auxiliary|modal verb)\)/i.test(g),o=/^\((?:adverb|particle|preposition|conjunction|interjection|suffix|prefix|classifier|measure word)\)/i.test(g),q=/^\((?:numeral|number)\)/i.test(g),n=/^\((?:noun|pronoun|surname|proper noun)\)/i.test(g);
   let t=g.replace(/^(?:\([^)]*\)\s*)+/,"").trim();
   if(p||/^to [a-z]/i.test(t))x[1]=Math.max(x[1],4);
   else if(o)x[3]=Math.max(x[3],4);
   else if(q)x[2]=Math.max(x[2],4);
   else if(n||/^(?:a|an|the) /i.test(t))x[0]=Math.max(x[0],3);
   else if(t)x[0]=Math.max(x[0],1);
  }
  map.set(s,x);
 }
 ck(entries===125474,"dict entries");
 function scores(s,gloss){
  let v=gloss?(map.get(s)||[0,0,0,0]).slice():[0,0,0,0];v[0]+=1;
  if(nform.test(s))v[2]+=8;if(punct(s))v[3]+=12;if(func.has(s))v[3]+=6;return v;
 }
 function transition(a,b){return a===2&&b===0?2:a===0&&b===1||a===1&&b===0?1:0}
 function decode(forms,mode){
  const S=forms.map(s=>scores(s,mode!=="shape"));if(mode!=="context")return S.map(v=>v.indexOf(Math.max(...v)));
  let prev=[0,0,0,0],back=[];
  for(let i=0;i<S.length;i++){let next=[],bp=[];for(let b=0;b<4;b++){let a=0;for(let j=1;j<4;j++)if(prev[j]+(i?transition(j,b):0)>prev[a]+(i?transition(a,b):0))a=j;next[b]=prev[a]+S[i][b]+(i?transition(a,b):0);bp[b]=a}prev=next;back.push(bp)}
  let j=prev.indexOf(Math.max(...prev)),out=[];for(let i=S.length-1;i>=0;i--){out[i]=j;j=back[i][j]}return out;
 }
 const cmp=(a,b)=>b.s-a.s||(a.p<b.p?-1:a.p>b.p?1:0);
 function kbest(S,K){
  if(!S.length)return [{p:"",s:0}];
  let dp=S[0].map((s,b)=>[{p:String(b),s}]);
  for(let i=1;i<S.length;i++)dp=S[i].map((s,b)=>dp.flatMap((rows,a)=>rows.map(x=>({p:x.p+b,s:x.s+s+transition(a,b)}))).sort(cmp).slice(0,K));
  return dp.flat().sort(cmp).slice(0,K);
 }
 function seqScore(S,p){return p.split("").reduce((s,b,i)=>s+S[i][+b]+(i?transition(+p[i-1],+b):0),0)}
 const blank=()=>({predicted:0,spanHit:0,classHit:0,per:{N:[0,0,0],P:[0,0,0],Q:[0,0,0],O:[0,0,0]},allArc:0,numArc:0,chain:0,eligibleChain:0,trees:0});
 const out={sentences:0,tokens:0,nums:0,dictEntries:entries,headwords:map.size,raw:{},oracle:{},controls:0,exactSeg:0,glossEvidence:0,glossAmbiguous:0,kbest:{oracleCases:0,paths:0,tieFirst:0,contextSameFirst:0,bestScoreSame:0,byK:{},goldCompleteClass:0}};
 const modes=["shape","gloss","context"];for(let m of modes){out.raw[m]=blank();out.oracle[m]=blank()}
 for(let k of [1,2,4])out.kbest.byK[k]={uniqueTypedSpans:0,typedHits:0,uniqueHeadPairs:0,headHits:0,numHeadHits:0,numChainHits:0,completeClassSentences:0};
 const key=(a,b)=>a+":"+b;
 function chain(i,ts,h,predicate){let z=[];for(let count=0;count<ts.length;count++){let j=h[i];if(j===0){z.push("ROOT");return z}if(j<1||j>=ts.length)return null;z.push(key(ts[j].a,ts[j].b));if(predicate(j))return z;i=j}return null}
 function tree(forms,spans,labels){
  const ts=[null,...forms.map((form,i)=>({form,a:spans[i][0],b:spans[i][1],pos:punct(form)?"PUNCT":({N:"NOUN",P:"VERB",Q:"NUM",O:"X"})[classes[labels[i]]]}))];
  const d=P.decode(P.matrix(ts));ck(d.status==="CANDIDATE"&&P.valid(d.heads,true),"tree");return {ts,d,labels};
 }
 function evaluate(forms,spans,gold,mode,o){
  const {ts,d,labels}=tree(forms,spans,decode(forms,mode));o.trees++;
  const gm=new Map(gold.slice(1).map(t=>[key(t.a,t.b),t]));
  for(let t of gold.slice(1))o.per[coarse(t.pos)][1]++;
  o.predicted+=forms.length;
  for(let i=1;i<ts.length;i++){let t=ts[i],label=classes[labels[i-1]],g=gm.get(key(t.a,t.b));o.per[label][0]++;if(!g)continue;o.spanHit++;if(label===coarse(g.pos)){o.classHit++;o.per[label][2]++}
   let h=d.heads[i],target=g.head===0?"ROOT":key(gold[g.head].a,gold[g.head].b),actual=h===0?"ROOT":key(ts[h].a,ts[h].b);o.allArc+=+(target===actual);
   if(g.pos==="NUM"){o.numArc+=+(target===actual&&label==="Q");let gc=chain(g.id,gold,gold.map(x=>x?.head??-1),j=>pred.has(gold[j].pos)),pc=chain(i,ts,d.heads,j=>ts[j].pos==="VERB");o.eligibleChain+=+(label==="Q");o.chain+=+(label==="Q"&&JSON.stringify(gc)===JSON.stringify(pc))}
  }
 }
 // Exact top-K class sequence with a separately specified lexical tie order.
 for(let n=1;n<=5;n++)for(let seed=0;seed<20;seed++){
  let S=Array.from({length:n},(_,i)=>Array.from({length:4},(_,j)=>(i*13+j*7+i*j*3+seed*11)%9-4)),rows=[];
  function go(p){if(p.length===n){rows.push({p,s:seqScore(S,p)});return}for(let j=0;j<4;j++)go(p+j)}
  go("");ck(JSON.stringify(kbest(S,4))===JSON.stringify(rows.sort(cmp).slice(0,4)),"kbest oracle");out.kbest.oracleCases++;
 }
 for(const block of raw.trimEnd().split(/\n\n+/)){
  const lines=block.split("\n"),txt=lines.find(x=>x.startsWith("# text = ")).slice(9),chars=[...txt],g=L.global(L.graph(chars,true)).pred,forms=g.map(e=>chars.slice(e.i,e.j).join("")),spans=g.map(e=>[e.i,e.j]);
  const S=forms.map(s=>scores(s,true)),seq=kbest(S,4),legacy=decode(forms,"context").join(""),trees=seq.map(x=>tree(forms,spans,x.p.split("").map(Number)));
  ck(seq[0].s===seqScore(S,legacy),"same optimum");
  out.kbest.bestScoreSame++;out.kbest.contextSameFirst+=+(seq[0].p===legacy);out.kbest.tieFirst+=+(seq.length>1&&seq[0].s===seq[1].s);out.kbest.paths+=seq.length;
  const gold=[null,...lines.filter(x=>!x.startsWith("#")).map(x=>x.split("\t")).filter(c=>/^[1-9]\d*$/.test(c[0])).map(c=>({id:+c[0],form:c[1],pos:c[3],head:+c[6],misc:c[9]}))];let cur=0;
  for(let t of gold.slice(1)){t.a=cur;cur+=[...t.form].length;t.b=cur;if(!t.misc.split("|").includes("SpaceAfter=No"))cur++;const v=map.get(t.form);out.glossEvidence+=+!!v;out.glossAmbiguous+=+(!!v&&v.filter(x=>x>=3).length>1)}
  out.sentences++;out.tokens+=gold.length-1;out.nums+=gold.slice(1).filter(t=>t.pos==="NUM").length;out.exactSeg+=+(JSON.stringify(spans)===JSON.stringify(gold.slice(1).map(t=>[t.a,t.b])));
  for(let m of modes){evaluate(forms,spans,gold,m,out.raw[m]);evaluate(gold.slice(1).map(t=>t.form),gold.slice(1).map(t=>[t.a,t.b]),gold,m,out.oracle[m])}
  const typedGold=new Set(gold.slice(1).map(t=>key(t.a,t.b)+"|"+coarse(t.pos))),gh=gold.map(x=>x?.head??-1),goldHead=new Set(gold.slice(1).map(t=>key(t.a,t.b)+"|"+(t.head===0?"ROOT":key(gold[t.head].a,gold[t.head].b)))),goldNum=new Set(gold.slice(1).filter(t=>t.pos==="NUM").map(t=>key(t.a,t.b)+"|"+(t.head===0?"ROOT":key(gold[t.head].a,gold[t.head].b)))),goldChain=new Set(gold.slice(1).filter(t=>t.pos==="NUM").map(t=>key(t.a,t.b)+"|"+JSON.stringify(chain(t.id,gold,gh,j=>pred.has(gold[j].pos)))));
  let T=new Set(),H=new Set(),NH=new Set(),CH=new Set(),complete=false;
  for(let i=0;i<trees.length;i++){
   let {ts,d,labels}=trees[i],thisT=new Set();
   for(let j=1;j<ts.length;j++){
    let t=ts[j],k=key(t.a,t.b),h=d.heads[j],pair=k+"|"+(h===0?"ROOT":key(ts[h].a,ts[h].b)),tag=k+"|"+classes[labels[j-1]];
    T.add(tag);thisT.add(tag);H.add(pair);
    if(labels[j-1]===2){NH.add(pair);CH.add(k+"|"+JSON.stringify(chain(j,ts,d.heads,k=>ts[k].pos==="VERB")))}
   }
   complete ||= thisT.size===typedGold.size&&[...typedGold].every(x=>thisT.has(x));
   const o=out.kbest.byK[i+1];if(o){o.uniqueTypedSpans+=T.size;o.typedHits+=[...typedGold].filter(x=>T.has(x)).length;o.uniqueHeadPairs+=H.size;o.headHits+=[...goldHead].filter(x=>H.has(x)).length;o.numHeadHits+=[...goldNum].filter(x=>NH.has(x)).length;o.numChainHits+=[...goldChain].filter(x=>CH.has(x)).length;o.completeClassSentences+=+complete}
  }
 }
 for(let group of [out.raw,out.oracle])for(let m of modes){let x=group[m];ck(x.classHit<=x.spanHit&&x.chain<=x.eligibleChain&&x.eligibleChain<=out.nums&&Object.values(x.per).reduce((s,a)=>s+a[2],0)===x.classHit,"counts");out.controls++}
 ck(out.sentences===500&&out.tokens===12665&&out.nums===654&&out.raw.shape.spanHit===9998&&out.exactSeg===36,"baseline");
 ck(out.raw.shape.classHit===6822&&out.raw.gloss.classHit===7779&&out.raw.context.classHit===7729&&out.raw.context.chain===42&&out.oracle.context.chain===51,"repeat");
 for(const f of ["typedHits","headHits","numHeadHits","numChainHits","uniqueTypedSpans","uniqueHeadPairs","completeClassSentences"])ck(out.kbest.byK[1][f]<=out.kbest.byK[2][f]&&out.kbest.byK[2][f]<=out.kbest.byK[4][f],"nested");
 return out;
}
console.log(JSON.stringify(study(dict,raw,L,P),null,2));
```
## 治理及下一责任
自行选择粗类、释义提示、功能词、分数、转移、K与评估口径，属于已见开发研究，未获正式产品替换或训练授权。未调用第三方预训练模型、未训练、未运行完整v0.8、未修改生产、未合并PR、未部署、未主动CI、未新增费用；冻结和唯一交接不变。下一阶段优先把固定分词单路径扩展为有预算的多分词/词类联合假设并保留共同路径见证，再研究与原生数量义务/条件/来源的可信语义桥。避免只扩大搜索或以人工金标填补运行时缺失。
