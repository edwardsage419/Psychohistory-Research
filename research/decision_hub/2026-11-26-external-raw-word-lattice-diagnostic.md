# 自主认知：真实外部开发集的无词典原文词边界格与精确路径计数
2026-11-26。RESEARCH_CANDIDATE / EXTERNAL_DEVELOPMENT_BYTES_REVERIFIED / RAW_TEXT_CANDIDATE_LATTICE / NO_TRAINING / INDEPENDENT_NOT_RUN / FULL_NATIVE_NOT_RUN。
## 基线及去重
起始main 14cc8c7911d3e74ccd89ca80841305d174de5026；核对12近期提交、15开放PR、v3.2/同步规程/唯一产品交接/前轮效果报告前18行（交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07）。Draft #63仍draft/unmerged固定head 734686980b19da9291bdd08b67d4e2519c011acf。检查R134结构、R135给定金标否定锚、R133来源图前段，检索segmentation/tokenization/dependency decoder/unsegmented/word boundary/lexical lattice/external development/treebank，已有R136/R137给定金标分词与词性依存解码不能当作自主分词。本轮新增原文Unicode标量词边界格、紧凑区间及路径计数、无词典贪心分词反例；不重复句法解码、基础统计或67个已见合成语义角色优化。全库去重有限。
## 外部来源、许可及隔离
UniversalDependencies/UD_Chinese-GSDSimp 固定commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3，zh_gsdsimp-ud-dev.conllu Git blob af8cc878e7934b38ce3c1a266053100e7c47de6f；实际重新取得完整blob，并复用R134 audit（research/decision_hub/2026-11-25-external-ud-development-corpus-structural-audit.md blob db9cc100d96d49832fe32879a706f63830301773）独立重算Git SHA1与字节长度1195378一致。读取固定README及LICENSE（5cb7d4a8446b4a167915225483aa94d187f23798及9af2e0b2f73cf29fe1f60cb6376b176d9c2ba846），CC BY-SA 4.0仅确认treebank许可，GSD README区分原始文本权利。只做公开dev的非训练聚合诊断，未复制第三方语句/token正文到仓库。训练/派生模型/重新分发许可仍由数据轨审定。该wiki文本不同于用户决策对话，不是独立未见留出；R134–137已使用同一开发集。官方英文来源本轮实际查询 https://universaldependencies.org/treebanks/zh_gsd/index.html 、https://universaldependencies.org/treebanks/zh_hk/index.html 、https://universaldependencies.org/treebanks/zh_cfl/index.html 、https://universaldependencies.org/contributing/licensing.html 。HK固定commit a6b7e7dcc17f161694ec8fb9e27549490ba6e58f README 39d3f8cdd87079bb3ab6733f4e685f839325d6be明确仅test，影视字幕及立法记录且与Cantonese-HK平行；CFL固定commit 9cb1724ff3f633efe8e5b59d8f577841cc12577d README 6096a6df4d7c23a8c635443a679fee361a2ad8c4为学习者作文、有原句/修订对齐及许可声明；本轮只读两者README/LICENSE，不下载正文或test/train，不声明新语料实测。GSD和GSDSimp为平行源，不能当独立样本。外部真实开发正文实测仍仅一个来源。
## 研究合同
从# text原文直接按Unicode标量生成有限词跨度；不输入人工FORM/UPOS/HEAD或词典、训练权重。空白为强制跳过边；open允许所有不跨空白且长度≤K的非空跨度；punct增加Unicode标点独立边；script再禁止跨Han、Latin、Nd、other等字符类边界。K=1/2/4/8/16/32由研究者选择。不是语言知识或实际分词树；词内标点、跨文字系统词、含空格词、组合字素、未建模字词都可能被排除。没有文本归一化或繁简折叠。比较只在候选生成之后严格对齐人工FORM，跳过词间空白，不向后搜索替代匹配；失败句单列，不算分母。原文来源、标注缺陷和分词规范影响结果。gold token/span、UPOS与Polarity只在评估使用，不能当模型输入。完整句覆盖指每个标注词都在格中，非正确分词预测。实际贪心基线每步取最长合法边，以精确词跨度微F1和整句完全匹配计分；不使用人工标签。无领域语义、否定范围、条件或决策理解。
每起点合法终点为连续整数区间[lo,hi]，以区间替代所有显式边，无损表示本研究定义的候选图。路径计数F(n)=1,F(i)=sum(F(j),j=lo..hi)；后缀和S(i)=F(i)+S(i+1)，F(i)=S(lo)-S(hi+1)，用BigInt精确计算。另用显式边的正向DP直接核对每个格。路径数的log2是组合规模指标，无概率，不是熵估计或真实解析难度。区间记录数为非空白起点数，显式边数为词候选；强制空白跳过边参与路径计数但不计词候选。单位记录大小不等同内存；实际生成范围的循环仍含K，BigInt运算不是常数成本；未测真机时间、内存、电量、预算截断或实际语义排序。仅无训练算法诊断，不能把候选空间完备当作语义准确。所有结果无操作权。
## 实测
原始500句12665词元，严格对齐500句12665词元，跳过0句0词元。实际9000个格路径计数与直接DP逐一一致，53项专项/聚合控制通过，重复执行完整输出一致。
| K | 模式 | 标注词覆盖 | 完整句覆盖 | 显式边数 | 区间记录数 | 最长贪心F1 | 贪心完整句 | 平均log2路径数 |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | open | 6444/12665 | 0 | 20000 | 20000 | 0.39455074 | 0 | 0 |
| 1 | punct | 6444/12665 | 0 | 20000 | 20000 | 0.39455074 | 0 | 0 |
| 1 | script | 6444/12665 | 0 | 20000 | 20000 | 0.39455074 | 0 | 0 |
| 2 | open | 12074/12665 | 234 | 39478 | 20000 | 0.27957178 | 0 | 27.282652 |
| 2 | punct | 12064/12665 | 233 | 36427 | 20000 | 0.45232243 | 1 | 23.603652 |
| 2 | script | 12059/12665 | 233 | 35718 | 20000 | 0.47361019 | 1 | 22.824089 |
| 4 | open | 12584/12665 | 447 | 76869 | 20000 | 0.02920933 | 0 | 37.014793 |
| 4 | punct | 12560/12665 | 435 | 64201 | 20000 | 0.24705404 | 0 | 31.532524 |
| 4 | script | 12538/12665 | 426 | 61140 | 20000 | 0.28945658 | 0 | 30.266052 |
| 8 | open | 12658/12665 | 493 | 145419 | 20000 | 0.00935186 | 0 | 38.862439 |
| 8 | punct | 12612/12665 | 463 | 102432 | 20000 | 0.23656895 | 0 | 32.810691 |
| 8 | script | 12585/12665 | 451 | 94508 | 20000 | 0.29764407 | 0 | 31.398903 |
| 16 | open | 12665/12665 | 500 | 257880 | 20000 | 0.00621206 | 0 | 38.95573 |
| 16 | punct | 12619/12665 | 470 | 135084 | 20000 | 0.23755437 | 0 | 32.853956 |
| 16 | script | 12592/12665 | 458 | 121092 | 20000 | 0.30220259 | 0 | 31.435967 |
| 32 | open | 12665/12665 | 500 | 394904 | 20000 | 0.00354872 | 0 | 38.956 |
| 32 | punct | 12619/12665 | 470 | 143708 | 20000 | 0.23636587 | 0 | 32.854 |
| 32 | script | 12592/12665 | 458 | 126519 | 20000 | 0.30167532 | 0 | 31.436 |
详细输出保留长度、词性、否定属性子集及遗漏原因；遗漏原因按长度、空白、标点、文字系统的顺序归类，互斥但非所有因果。研究诊断使用同一真实外部dev，候选空间覆盖与贪心精度分开，不能声称已完成开放分词或提高真实语义质量。不同预算下完整路径规模可能巨大，后续宜复用无损格、组合语义及独立未知检测，按候选搜索预算提供局部分析；不以全枚举替代自主语义。新外部来源仅元数据待数据轨审定，不访问测试集；独立轨保管未见真实情节。无生产源码修改、训练、第三方AI运行依赖、PR合并、部署、主动CI或增加费用，R073/PESEN及冻结不变。自行选择字符分类、长度、贪心及统计口径，未测实际用户或原生平台。
## 复算
固定外部原始dev与R134报告全文作为输入；Node标准JS，运行自有审核代码，外部语料只作数据。完整结果无第三方原文，未另造ZIP。
```js
function experiment(raw,auditDoc){
 const ck=(b,m)=>{if(!b)throw Error(m)},audit=Function(auditDoc.split("```js\n")[1].split("\n```")[0].split("console.log(JSON.stringify(audit(raw)")[0]+"\nreturn audit;")();
 const verified=audit(raw),K=[1,2,4,8,16,32],modes=["open","punct","script"],obj=(a,f)=>Object.fromEntries(a.map(k=>[k,f(k)])),key=(i,j)=>i+":"+j;
 const cls=c=>/\s/u.test(c)?"space":/\p{P}/u.test(c)?"punct":/\p{Script=Han}/u.test(c)?"han":/\p{Nd}/u.test(c)?"digit":/\p{Script=Latin}/u.test(c)?"latin":"other";
 // Generate from raw Unicode scalar coordinates, no gold tokens or tags.
 function ranges(chars,k,mode){
  const t=chars.map(cls),n=t.length,end=Array(n).fill(n);
  for(let i=n-1;i>=0;i--)end[i]=i+1<n&&t[i]===t[i+1]?end[i+1]:i+1;
  let out=[];
  for(let i=0;i<n;i++){
   if(t[i]==="space"){out.push({i,lo:i+1,hi:i+1,skip:true});continue}
   let hi=i+1;while(hi<n&&hi-i<k&&t[hi]!=="space")hi++;
   if(mode!=="open"){
    if(t[i]==="punct")hi=i+1;
    else for(let j=i+1;j<hi;j++)if(t[j]==="punct"){hi=j;break}
   }
   if(mode==="script")hi=Math.min(hi,end[i]);
   out.push({i,lo:i+1,hi,skip:false});
  }return out
 }
 function countPaths(rs){
  let n=rs.length,dp=Array(n+1).fill(0n),s=Array(n+2).fill(0n);
  dp[n]=1n;s[n]=1n;
  for(let i=n-1;i>=0;i--){let {lo,hi}=rs[i];dp[i]=s[lo]-s[hi+1];s[i]=dp[i]+s[i+1]}
  return dp[0]
 }
 function directPaths(rs){let n=rs.length,d=Array(n+1).fill(0n);d[0]=1n;for(let i=0;i<n;i++)for(let j=rs[i].lo;j<=rs[i].hi;j++)d[j]+=d[i];return d[n]}
 function greedy(rs){let x=[];for(let i=0;i<rs.length;){let r=rs[i];if(!r.skip)x.push(key(i,r.hi));i=r.hi}return x}
 function align(chars,forms){let i=0,z=[];for(let f of forms){while(i<chars.length&&cls(chars[i])==="space")i++;let a=[...f];if(!a.length||a.some((c,j)=>c!==chars[i+j]))return null;z.push([i,i+a.length]);i+=a.length}while(i<chars.length&&cls(chars[i])==="space")i++;return i===chars.length?z:null}
 const blank=()=>({tokens:0,hit:0,completeSentences:0,edges:0,ranges:0,greedyPred:0,greedyHit:0,greedyExact:0,log2PathsSum:0,maxPathBits:0,negTokens:0,negHit:0,missReasons:{length:0,space:0,punct:0,script:0},pos:{}});
 let o={source:{bytes:verified.bytes,gitBlob:verified.gitBlob,sentences:verified.sentences,tokens:verified.tokens,nonIntegerRows:verified.nonIntegerRows},alignedSentences:0,alignedTokens:0,skippedSentences:0,skippedTokens:0,unicodeScalars:0,maxSentenceScalars:0,rawCharsByClass:{},goldLength:{},metrics:obj(K,k=>obj(modes,m=>blank())),controls:0,pathChecks:0};
 const inc=(o,k,n=1)=>o[k]=(o[k]??0)+n;
 function log2big(x){const b=x.toString(2);return b.length-1+Math.log2(parseInt(b.slice(0,Math.min(52,b.length)),2)/2**(Math.min(52,b.length)-1))}
 for(let block of raw.trimEnd().split(/\n\n+/)){
  let lines=block.split("\n"),txt=lines.find(x=>x.startsWith("# text = "))?.slice(9),rows=lines.filter(l=>!l.startsWith("#")).map(l=>l.split("\t")).filter(c=>/^[1-9]\d*$/.test(c[0]));
  ck(typeof txt==="string","text");let chars=[...txt];
  // Construct all candidate lattices before accessing gold forms.
  let lattices=obj(K,k=>obj(modes,m=>ranges(chars,k,m))),gold=align(chars,rows.map(c=>c[1]));
  if(!gold){o.skippedSentences++;o.skippedTokens+=rows.length;continue}
  o.alignedSentences++;o.alignedTokens+=rows.length;o.unicodeScalars+=chars.length;o.maxSentenceScalars=Math.max(o.maxSentenceScalars,chars.length);for(let c of chars)inc(o.rawCharsByClass,cls(c));
  let gset=new Set(gold.map(([i,j])=>key(i,j)));ck(gset.size===gold.length,"unique gold");
  for(let [i,j] of gold)inc(o.goldLength,String(j-i));
  for(let k of K)for(let m of modes){
   let rs=lattices[k][m],s=o.metrics[k][m],ways=countPaths(rs);ck(ways===directPaths(rs)&&ways>0n,"path count");o.pathChecks++;
   s.edges+=rs.reduce((n,r)=>n+(r.skip?0:r.hi-r.lo+1),0);s.ranges+=rs.filter(r=>!r.skip).length;s.log2PathsSum+=log2big(ways);s.maxPathBits=Math.max(s.maxPathBits,ways.toString(2).length);
   let pred=greedy(rs);s.greedyPred+=pred.length;s.greedyHit+=pred.filter(x=>gset.has(x)).length;s.greedyExact+=+(pred.length===gold.length&&pred.every(x=>gset.has(x)));
   let all=true;
   for(let t=0;t<gold.length;t++){
    let [i,j]=gold[t],p=rows[t][3],neg=rows[t][5].split("|").includes("Polarity=Neg"),hit=!rs[i].skip&&j>=rs[i].lo&&j<=rs[i].hi;
    s.tokens++;s.hit+=+hit;s.negTokens+=+neg;s.negHit+=+(neg&&hit);if(!s.pos[p])s.pos[p]=[0,0];s.pos[p][0]+=+hit;s.pos[p][1]++;
    if(!hit){all=false;let c=chars.slice(i,j).map(cls),why=j-i>k?"length":c.includes("space")?"space":m!=="open"&&c.includes("punct")&&c.length>1?"punct":m==="script"&&new Set(c).size>1?"script":null;ck(why!==null,"reason");s.missReasons[why]++}
   }
   s.completeSentences+=+all;
  }
 }
 ck(o.alignedSentences+o.skippedSentences===verified.sentences&&o.alignedTokens+o.skippedTokens===verified.tokens,"totals");
 for(let k of K){let a=o.metrics[k];ck(a.open.hit>=a.punct.hit&&a.punct.hit>=a.script.hit,"coverage nesting");ck(a.open.edges>=a.punct.edges&&a.punct.edges>=a.script.edges,"edge nesting");o.controls+=2;for(let m of modes){let s=a[m];ck(s.tokens===o.alignedTokens&&Object.values(s.missReasons).reduce((a,b)=>a+b,0)===s.tokens-s.hit,"account");o.controls++;s.meanLog2Paths=Number((s.log2PathsSum/o.alignedSentences).toFixed(6));delete s.log2PathsSum;s.greedyF1=Number((2*s.greedyHit/(s.greedyPred+s.tokens)).toFixed(8))}}
 for(let m of modes)for(let i=1;i<K.length;i++){ck(o.metrics[K[i]][m].hit>=o.metrics[K[i-1]][m].hit,"monotone");o.controls++}
 for(let [txt,k,mode,n] of [["甲乙丙",3,"open",4n],["甲，乙",3,"punct",1n],["甲A乙",3,"script",1n],["甲 乙",3,"open",1n],["甲𠀀乙",2,"open",3n],["",4,"open",1n],["12",2,"script",2n]]){let r=ranges([...txt],k,mode);ck(countPaths(r)===n&&directPaths(r)===n,"synthetic");o.controls++}
 // Corrupt alignment is never silently shifted to a different occurrence.
 ck(align([..."甲乙甲"],["甲","甲"])===null,"align fail");o.controls++;
 return o
}
const fs=require("node:fs"); console.log(JSON.stringify(experiment(fs.readFileSync(process.argv[2],"utf8"),fs.readFileSync(process.argv[3],"utf8")),null,2));
```
## 完整聚合输出
```json
{
  "source": {
    "bytes": 1195378,
    "gitBlob": "af8cc878e7934b38ce3c1a266053100e7c47de6f",
    "sentences": 500,
    "tokens": 12665,
    "nonIntegerRows": 0
  },
  "alignedSentences": 500,
  "alignedTokens": 12665,
  "skippedSentences": 0,
  "skippedTokens": 0,
  "unicodeScalars": 20022,
  "maxSentenceScalars": 135,
  "rawCharsByClass": {
    "han": 16729,
    "punct": 1821,
    "latin": 359,
    "digit": 1088,
    "space": 22,
    "other": 3
  },
  "goldLength": {
    "1": 6444,
    "2": 5630,
    "3": 234,
    "4": 276,
    "5": 46,
    "6": 15,
    "7": 4,
    "8": 9,
    "9": 4,
    "10": 2,
    "14": 1
  },
  "metrics": {
    "1": {
      "open": {
        "tokens": 12665,
        "hit": 6444,
        "completeSentences": 0,
        "edges": 20000,
        "ranges": 20000,
        "greedyPred": 20000,
        "greedyHit": 6444,
        "greedyExact": 0,
        "maxPathBits": 1,
        "negTokens": 44,
        "negHit": 22,
        "missReasons": {
          "length": 6221,
          "space": 0,
          "punct": 0,
          "script": 0
        },
        "pos": {
          "ADV": [
            156,
            323
          ],
          "PUNCT": [
            1766,
            1770
          ],
          "VERB": [
            598,
            1851
          ],
          "SCONJ": [
            521,
            559
          ],
          "NOUN": [
            728,
            3637
          ],
          "ADJ": [
            29,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            326,
            365
          ],
          "ADP": [
            450,
            556
          ],
          "DET": [
            72,
            119
          ],
          "CCONJ": [
            153,
            164
          ],
          "X": [
            8,
            79
          ],
          "PRON": [
            138,
            174
          ],
          "NUM": [
            262,
            654
          ],
          "PROPN": [
            192,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 0,
        "greedyF1": 0.39455074
      },
      "punct": {
        "tokens": 12665,
        "hit": 6444,
        "completeSentences": 0,
        "edges": 20000,
        "ranges": 20000,
        "greedyPred": 20000,
        "greedyHit": 6444,
        "greedyExact": 0,
        "maxPathBits": 1,
        "negTokens": 44,
        "negHit": 22,
        "missReasons": {
          "length": 6221,
          "space": 0,
          "punct": 0,
          "script": 0
        },
        "pos": {
          "ADV": [
            156,
            323
          ],
          "PUNCT": [
            1766,
            1770
          ],
          "VERB": [
            598,
            1851
          ],
          "SCONJ": [
            521,
            559
          ],
          "NOUN": [
            728,
            3637
          ],
          "ADJ": [
            29,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            326,
            365
          ],
          "ADP": [
            450,
            556
          ],
          "DET": [
            72,
            119
          ],
          "CCONJ": [
            153,
            164
          ],
          "X": [
            8,
            79
          ],
          "PRON": [
            138,
            174
          ],
          "NUM": [
            262,
            654
          ],
          "PROPN": [
            192,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 0,
        "greedyF1": 0.39455074
      },
      "script": {
        "tokens": 12665,
        "hit": 6444,
        "completeSentences": 0,
        "edges": 20000,
        "ranges": 20000,
        "greedyPred": 20000,
        "greedyHit": 6444,
        "greedyExact": 0,
        "maxPathBits": 1,
        "negTokens": 44,
        "negHit": 22,
        "missReasons": {
          "length": 6221,
          "space": 0,
          "punct": 0,
          "script": 0
        },
        "pos": {
          "ADV": [
            156,
            323
          ],
          "PUNCT": [
            1766,
            1770
          ],
          "VERB": [
            598,
            1851
          ],
          "SCONJ": [
            521,
            559
          ],
          "NOUN": [
            728,
            3637
          ],
          "ADJ": [
            29,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            326,
            365
          ],
          "ADP": [
            450,
            556
          ],
          "DET": [
            72,
            119
          ],
          "CCONJ": [
            153,
            164
          ],
          "X": [
            8,
            79
          ],
          "PRON": [
            138,
            174
          ],
          "NUM": [
            262,
            654
          ],
          "PROPN": [
            192,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 0,
        "greedyF1": 0.39455074
      }
    },
    "2": {
      "open": {
        "tokens": 12665,
        "hit": 12074,
        "completeSentences": 234,
        "edges": 39478,
        "ranges": 20000,
        "greedyPred": 10127,
        "greedyHit": 3186,
        "greedyExact": 0,
        "maxPathBits": 94,
        "negTokens": 44,
        "negHit": 44,
        "missReasons": {
          "length": 591,
          "space": 0,
          "punct": 0,
          "script": 0
        },
        "pos": {
          "ADV": [
            319,
            323
          ],
          "PUNCT": [
            1768,
            1770
          ],
          "VERB": [
            1840,
            1851
          ],
          "SCONJ": [
            559,
            559
          ],
          "NOUN": [
            3588,
            3637
          ],
          "ADJ": [
            300,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            365,
            365
          ],
          "ADP": [
            556,
            556
          ],
          "DET": [
            118,
            119
          ],
          "CCONJ": [
            164,
            164
          ],
          "X": [
            19,
            79
          ],
          "PRON": [
            174,
            174
          ],
          "NUM": [
            422,
            654
          ],
          "PROPN": [
            837,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 27.282652,
        "greedyF1": 0.27957178
      },
      "punct": {
        "tokens": 12665,
        "hit": 12064,
        "completeSentences": 233,
        "edges": 36427,
        "ranges": 20000,
        "greedyPred": 11340,
        "greedyHit": 5429,
        "greedyExact": 1,
        "maxPathBits": 86,
        "negTokens": 44,
        "negHit": 44,
        "missReasons": {
          "length": 591,
          "space": 0,
          "punct": 10,
          "script": 0
        },
        "pos": {
          "ADV": [
            319,
            323
          ],
          "PUNCT": [
            1766,
            1770
          ],
          "VERB": [
            1840,
            1851
          ],
          "SCONJ": [
            559,
            559
          ],
          "NOUN": [
            3588,
            3637
          ],
          "ADJ": [
            300,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            365,
            365
          ],
          "ADP": [
            556,
            556
          ],
          "DET": [
            118,
            119
          ],
          "CCONJ": [
            164,
            164
          ],
          "X": [
            11,
            79
          ],
          "PRON": [
            174,
            174
          ],
          "NUM": [
            422,
            654
          ],
          "PROPN": [
            837,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 23.603652,
        "greedyF1": 0.45232243
      },
      "script": {
        "tokens": 12665,
        "hit": 12059,
        "completeSentences": 233,
        "edges": 35718,
        "ranges": 20000,
        "greedyPred": 11511,
        "greedyHit": 5725,
        "greedyExact": 1,
        "maxPathBits": 83,
        "negTokens": 44,
        "negHit": 44,
        "missReasons": {
          "length": 591,
          "space": 0,
          "punct": 10,
          "script": 5
        },
        "pos": {
          "ADV": [
            319,
            323
          ],
          "PUNCT": [
            1766,
            1770
          ],
          "VERB": [
            1840,
            1851
          ],
          "SCONJ": [
            559,
            559
          ],
          "NOUN": [
            3588,
            3637
          ],
          "ADJ": [
            300,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            365,
            365
          ],
          "ADP": [
            556,
            556
          ],
          "DET": [
            118,
            119
          ],
          "CCONJ": [
            164,
            164
          ],
          "X": [
            11,
            79
          ],
          "PRON": [
            174,
            174
          ],
          "NUM": [
            417,
            654
          ],
          "PROPN": [
            837,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 22.824089,
        "greedyF1": 0.47361019
      }
    },
    "4": {
      "open": {
        "tokens": 12665,
        "hit": 12584,
        "completeSentences": 447,
        "edges": 76869,
        "ranges": 20000,
        "greedyPred": 5206,
        "greedyHit": 261,
        "greedyExact": 0,
        "maxPathBits": 127,
        "negTokens": 44,
        "negHit": 44,
        "missReasons": {
          "length": 81,
          "space": 0,
          "punct": 0,
          "script": 0
        },
        "pos": {
          "ADV": [
            322,
            323
          ],
          "PUNCT": [
            1770,
            1770
          ],
          "VERB": [
            1851,
            1851
          ],
          "SCONJ": [
            559,
            559
          ],
          "NOUN": [
            3635,
            3637
          ],
          "ADJ": [
            313,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            365,
            365
          ],
          "ADP": [
            556,
            556
          ],
          "DET": [
            118,
            119
          ],
          "CCONJ": [
            164,
            164
          ],
          "X": [
            39,
            79
          ],
          "PRON": [
            174,
            174
          ],
          "NUM": [
            632,
            654
          ],
          "PROPN": [
            1041,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 37.014793,
        "greedyF1": 0.02920933
      },
      "punct": {
        "tokens": 12665,
        "hit": 12560,
        "completeSentences": 435,
        "edges": 64201,
        "ranges": 20000,
        "greedyPred": 7023,
        "greedyHit": 2432,
        "greedyExact": 0,
        "maxPathBits": 116,
        "negTokens": 44,
        "negHit": 44,
        "missReasons": {
          "length": 81,
          "space": 0,
          "punct": 24,
          "script": 0
        },
        "pos": {
          "ADV": [
            322,
            323
          ],
          "PUNCT": [
            1766,
            1770
          ],
          "VERB": [
            1851,
            1851
          ],
          "SCONJ": [
            559,
            559
          ],
          "NOUN": [
            3635,
            3637
          ],
          "ADJ": [
            313,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            365,
            365
          ],
          "ADP": [
            556,
            556
          ],
          "DET": [
            118,
            119
          ],
          "CCONJ": [
            164,
            164
          ],
          "X": [
            30,
            79
          ],
          "PRON": [
            174,
            174
          ],
          "NUM": [
            621,
            654
          ],
          "PROPN": [
            1041,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 31.532524,
        "greedyF1": 0.24705404
      },
      "script": {
        "tokens": 12665,
        "hit": 12538,
        "completeSentences": 426,
        "edges": 61140,
        "ranges": 20000,
        "greedyPred": 7338,
        "greedyHit": 2895,
        "greedyExact": 0,
        "maxPathBits": 112,
        "negTokens": 44,
        "negHit": 44,
        "missReasons": {
          "length": 81,
          "space": 0,
          "punct": 24,
          "script": 22
        },
        "pos": {
          "ADV": [
            322,
            323
          ],
          "PUNCT": [
            1766,
            1770
          ],
          "VERB": [
            1851,
            1851
          ],
          "SCONJ": [
            559,
            559
          ],
          "NOUN": [
            3635,
            3637
          ],
          "ADJ": [
            313,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            365,
            365
          ],
          "ADP": [
            556,
            556
          ],
          "DET": [
            118,
            119
          ],
          "CCONJ": [
            164,
            164
          ],
          "X": [
            29,
            79
          ],
          "PRON": [
            174,
            174
          ],
          "NUM": [
            600,
            654
          ],
          "PROPN": [
            1041,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 30.266052,
        "greedyF1": 0.28945658
      }
    },
    "8": {
      "open": {
        "tokens": 12665,
        "hit": 12658,
        "completeSentences": 493,
        "edges": 145419,
        "ranges": 20000,
        "greedyPred": 2733,
        "greedyHit": 72,
        "greedyExact": 0,
        "maxPathBits": 134,
        "negTokens": 44,
        "negHit": 44,
        "missReasons": {
          "length": 7,
          "space": 0,
          "punct": 0,
          "script": 0
        },
        "pos": {
          "ADV": [
            323,
            323
          ],
          "PUNCT": [
            1770,
            1770
          ],
          "VERB": [
            1851,
            1851
          ],
          "SCONJ": [
            559,
            559
          ],
          "NOUN": [
            3637,
            3637
          ],
          "ADJ": [
            313,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            365,
            365
          ],
          "ADP": [
            556,
            556
          ],
          "DET": [
            119,
            119
          ],
          "CCONJ": [
            164,
            164
          ],
          "X": [
            72,
            79
          ],
          "PRON": [
            174,
            174
          ],
          "NUM": [
            654,
            654
          ],
          "PROPN": [
            1056,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 38.862439,
        "greedyF1": 0.00935186
      },
      "punct": {
        "tokens": 12665,
        "hit": 12612,
        "completeSentences": 463,
        "edges": 102432,
        "ranges": 20000,
        "greedyPred": 4869,
        "greedyHit": 2074,
        "greedyExact": 0,
        "maxPathBits": 121,
        "negTokens": 44,
        "negHit": 44,
        "missReasons": {
          "length": 7,
          "space": 0,
          "punct": 46,
          "script": 0
        },
        "pos": {
          "ADV": [
            323,
            323
          ],
          "PUNCT": [
            1766,
            1770
          ],
          "VERB": [
            1851,
            1851
          ],
          "SCONJ": [
            559,
            559
          ],
          "NOUN": [
            3637,
            3637
          ],
          "ADJ": [
            313,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            365,
            365
          ],
          "ADP": [
            556,
            556
          ],
          "DET": [
            118,
            119
          ],
          "CCONJ": [
            164,
            164
          ],
          "X": [
            59,
            79
          ],
          "PRON": [
            174,
            174
          ],
          "NUM": [
            626,
            654
          ],
          "PROPN": [
            1056,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 32.810691,
        "greedyF1": 0.23656895
      },
      "script": {
        "tokens": 12665,
        "hit": 12585,
        "completeSentences": 451,
        "edges": 94508,
        "ranges": 20000,
        "greedyPred": 5417,
        "greedyHit": 2691,
        "greedyExact": 0,
        "maxPathBits": 116,
        "negTokens": 44,
        "negHit": 44,
        "missReasons": {
          "length": 7,
          "space": 0,
          "punct": 46,
          "script": 27
        },
        "pos": {
          "ADV": [
            323,
            323
          ],
          "PUNCT": [
            1766,
            1770
          ],
          "VERB": [
            1851,
            1851
          ],
          "SCONJ": [
            559,
            559
          ],
          "NOUN": [
            3637,
            3637
          ],
          "ADJ": [
            313,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            365,
            365
          ],
          "ADP": [
            556,
            556
          ],
          "DET": [
            118,
            119
          ],
          "CCONJ": [
            164,
            164
          ],
          "X": [
            56,
            79
          ],
          "PRON": [
            174,
            174
          ],
          "NUM": [
            602,
            654
          ],
          "PROPN": [
            1056,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 31.398903,
        "greedyF1": 0.29764407
      }
    },
    "16": {
      "open": {
        "tokens": 12665,
        "hit": 12665,
        "completeSentences": 500,
        "edges": 257880,
        "ranges": 20000,
        "greedyPred": 1501,
        "greedyHit": 44,
        "greedyExact": 0,
        "maxPathBits": 134,
        "negTokens": 44,
        "negHit": 44,
        "missReasons": {
          "length": 0,
          "space": 0,
          "punct": 0,
          "script": 0
        },
        "pos": {
          "ADV": [
            323,
            323
          ],
          "PUNCT": [
            1770,
            1770
          ],
          "VERB": [
            1851,
            1851
          ],
          "SCONJ": [
            559,
            559
          ],
          "NOUN": [
            3637,
            3637
          ],
          "ADJ": [
            313,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            365,
            365
          ],
          "ADP": [
            556,
            556
          ],
          "DET": [
            119,
            119
          ],
          "CCONJ": [
            164,
            164
          ],
          "X": [
            79,
            79
          ],
          "PRON": [
            174,
            174
          ],
          "NUM": [
            654,
            654
          ],
          "PROPN": [
            1056,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 38.95573,
        "greedyF1": 0.00621206
      },
      "punct": {
        "tokens": 12665,
        "hit": 12619,
        "completeSentences": 470,
        "edges": 135084,
        "ranges": 20000,
        "greedyPred": 3887,
        "greedyHit": 1966,
        "greedyExact": 0,
        "maxPathBits": 121,
        "negTokens": 44,
        "negHit": 44,
        "missReasons": {
          "length": 0,
          "space": 0,
          "punct": 46,
          "script": 0
        },
        "pos": {
          "ADV": [
            323,
            323
          ],
          "PUNCT": [
            1766,
            1770
          ],
          "VERB": [
            1851,
            1851
          ],
          "SCONJ": [
            559,
            559
          ],
          "NOUN": [
            3637,
            3637
          ],
          "ADJ": [
            313,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            365,
            365
          ],
          "ADP": [
            556,
            556
          ],
          "DET": [
            118,
            119
          ],
          "CCONJ": [
            164,
            164
          ],
          "X": [
            66,
            79
          ],
          "PRON": [
            174,
            174
          ],
          "NUM": [
            626,
            654
          ],
          "PROPN": [
            1056,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 32.853956,
        "greedyF1": 0.23755437
      },
      "script": {
        "tokens": 12665,
        "hit": 12592,
        "completeSentences": 458,
        "edges": 121092,
        "ranges": 20000,
        "greedyPred": 4542,
        "greedyHit": 2600,
        "greedyExact": 0,
        "maxPathBits": 116,
        "negTokens": 44,
        "negHit": 44,
        "missReasons": {
          "length": 0,
          "space": 0,
          "punct": 46,
          "script": 27
        },
        "pos": {
          "ADV": [
            323,
            323
          ],
          "PUNCT": [
            1766,
            1770
          ],
          "VERB": [
            1851,
            1851
          ],
          "SCONJ": [
            559,
            559
          ],
          "NOUN": [
            3637,
            3637
          ],
          "ADJ": [
            313,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            365,
            365
          ],
          "ADP": [
            556,
            556
          ],
          "DET": [
            118,
            119
          ],
          "CCONJ": [
            164,
            164
          ],
          "X": [
            63,
            79
          ],
          "PRON": [
            174,
            174
          ],
          "NUM": [
            602,
            654
          ],
          "PROPN": [
            1056,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 31.435967,
        "greedyF1": 0.30220259
      }
    },
    "32": {
      "open": {
        "tokens": 12665,
        "hit": 12665,
        "completeSentences": 500,
        "edges": 394904,
        "ranges": 20000,
        "greedyPred": 861,
        "greedyHit": 24,
        "greedyExact": 0,
        "maxPathBits": 134,
        "negTokens": 44,
        "negHit": 44,
        "missReasons": {
          "length": 0,
          "space": 0,
          "punct": 0,
          "script": 0
        },
        "pos": {
          "ADV": [
            323,
            323
          ],
          "PUNCT": [
            1770,
            1770
          ],
          "VERB": [
            1851,
            1851
          ],
          "SCONJ": [
            559,
            559
          ],
          "NOUN": [
            3637,
            3637
          ],
          "ADJ": [
            313,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            365,
            365
          ],
          "ADP": [
            556,
            556
          ],
          "DET": [
            119,
            119
          ],
          "CCONJ": [
            164,
            164
          ],
          "X": [
            79,
            79
          ],
          "PRON": [
            174,
            174
          ],
          "NUM": [
            654,
            654
          ],
          "PROPN": [
            1056,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 38.956,
        "greedyF1": 0.00354872
      },
      "punct": {
        "tokens": 12665,
        "hit": 12619,
        "completeSentences": 470,
        "edges": 143708,
        "ranges": 20000,
        "greedyPred": 3581,
        "greedyHit": 1920,
        "greedyExact": 0,
        "maxPathBits": 121,
        "negTokens": 44,
        "negHit": 44,
        "missReasons": {
          "length": 0,
          "space": 0,
          "punct": 46,
          "script": 0
        },
        "pos": {
          "ADV": [
            323,
            323
          ],
          "PUNCT": [
            1766,
            1770
          ],
          "VERB": [
            1851,
            1851
          ],
          "SCONJ": [
            559,
            559
          ],
          "NOUN": [
            3637,
            3637
          ],
          "ADJ": [
            313,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            365,
            365
          ],
          "ADP": [
            556,
            556
          ],
          "DET": [
            118,
            119
          ],
          "CCONJ": [
            164,
            164
          ],
          "X": [
            66,
            79
          ],
          "PRON": [
            174,
            174
          ],
          "NUM": [
            626,
            654
          ],
          "PROPN": [
            1056,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 32.854,
        "greedyF1": 0.23636587
      },
      "script": {
        "tokens": 12665,
        "hit": 12592,
        "completeSentences": 458,
        "edges": 126519,
        "ranges": 20000,
        "greedyPred": 4287,
        "greedyHit": 2557,
        "greedyExact": 0,
        "maxPathBits": 116,
        "negTokens": 44,
        "negHit": 44,
        "missReasons": {
          "length": 0,
          "space": 0,
          "punct": 46,
          "script": 27
        },
        "pos": {
          "ADV": [
            323,
            323
          ],
          "PUNCT": [
            1766,
            1770
          ],
          "VERB": [
            1851,
            1851
          ],
          "SCONJ": [
            559,
            559
          ],
          "NOUN": [
            3637,
            3637
          ],
          "ADJ": [
            313,
            313
          ],
          "PART": [
            1042,
            1042
          ],
          "AUX": [
            365,
            365
          ],
          "ADP": [
            556,
            556
          ],
          "DET": [
            118,
            119
          ],
          "CCONJ": [
            164,
            164
          ],
          "X": [
            63,
            79
          ],
          "PRON": [
            174,
            174
          ],
          "NUM": [
            602,
            654
          ],
          "PROPN": [
            1056,
            1056
          ],
          "SYM": [
            3,
            3
          ]
        },
        "meanLog2Paths": 31.436,
        "greedyF1": 0.30167532
      }
    }
  },
  "controls": 53,
  "pathChecks": 9000
}
```
