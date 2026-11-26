# 自主认知：等路径数的分词候选多样性与联合依存覆盖诊断
2026-11-26。RESEARCH_CANDIDATE / REAL_EXTERNAL_DEVELOPMENT_BYTES_VERIFIED / RAW_TEXT_DIVERSE_PATH_SELECTION / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线及固定资产
起点main 9224cb54652f30ab008770217e235ac35a475553；沿用本轮核对25近期提交、15开放PR、v3.2及同步规程、历史交接固定blob前段（最新路径未定位），#63固定head 734686980b19da9291bdd08b67d4e2519c011acf。前轮K优词级路径及候选头实际执行 aa0d6c5882107b142dd555d0872b073da034a642；本轮只新增在固定前64条路径池内，按相同最终保留路径数对照覆盖多样性策略与最低成本策略。非全库查重。
固定blob按顺序：
UniversalDependencies/UD_Chinese-GSDSimp af8cc878e7934b38ce3c1a266053100e7c47de6f
rhcarvalho/cedict d7fee8237f26524b38eee220647e4c5d79f00de9
edwardsage419/Psychohistory-Research cee6b6f8d759b6aa33ec4f2863232a6583f8ae07
edwardsage419/Psychohistory-Research db9cc100d96d49832fe32879a706f63830301773
edwardsage419/Psychohistory-Research 0633533cebfb0cdea6aecff4e422bd3d4cdb5188
edwardsage419/Psychohistory-Research aa0d6c5882107b142dd555d0872b073da034a642
实际重新读取六项，复用R134 UTF8/Git SHA1实现复算前两项完整字节身份，固定上游commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3、6317ff202e14be60365c826f62e45fc9fa71d19e。沿用登记许可 CC BY-SA 4.0，底层文本及衍生分发另审；本轮未重审许可全文。来源 https://universaldependencies.org/treebanks/zh_gsdsimp/ 、https://www.mdbg.net/chinese/dictionary?page=cc-cedict 。仅聚合计数与原创算法，不复制原文或词典，不读train/test，非独立留出或个人决策语料。
## 方法
实际复用上一阶段K优路径DP、词格及词级头排序。首次运行因截取源码时先命中前方字符串内的同名终止标记，出现paths未定义，未归档；修正为从函数起点之后查找终止标记。生成最多64条按原始代价排序的完整路径，首先必保留最低成本路径，然后分别使用：原成本顺序；每轮最大化相对于已选路径词边并集的新跨度数；每轮最大化新跨度数/(1+相对最低成本增量)。平局按原池序；最终保留4或16条，全部选择只用原始文本、固定词典、路径代价与跨度，无标注、权重拟合或训练。后两者是启发式，不声称求出最优联合覆盖、符合真实语言概率或可直接上线；其较大路径池开销与后续候选对数量可能增加，因此等路径数不等于等资源。对每条选中路径产生全部可用非纯标点有向词对，再固定向右优先距离排名保留每词前5个候选头，跨路径按原文跨度去重。全部生成后才读取gold标注，评估词覆盖、完整gold路径、金标依存弧/跨段弧、候选数量、相对原代价及配对增损；只测候选覆盖，不是解析准确率、语义或执行权。跨路径并集不代表共同完整解析。
## 实际执行
标准JS完整500句运行一次，原成本策略两预算均与上一阶段真实结果核对一致；配对恒等式、等路径数、构造控制及总量检查。研究者选定64/4/16预算、新颖度和折中公式，无真实速度、用户价值或独立泛化证据；不根据本轮结果自动选正式策略。
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
  "sentences": 500,
  "tokens": 12665,
  "arcs": 10395,
  "cross": 1404,
  "poolPaths": 32000,
  "metrics": {
    "4": {
      "cost": {
        "paths": 2000,
        "uniqueWords": 15317,
        "wordHits": 10567,
        "fullSentences": 56,
        "unrankedPairs": 391032,
        "arcHits": 7299,
        "rankPairs": 77932,
        "rankHits": 5221,
        "crossHits": 1022,
        "rankCrossHits": 182,
        "sumExcess": 1272,
        "maxExcess": 2,
        "uniqueGoldCompleteButNoPath": 3,
        "pairedWordGain": 0,
        "pairedWordLoss": 0,
        "pairedArcGain": 0,
        "pairedArcLoss": 0,
        "pairedRankGain": 0,
        "pairedRankLoss": 0
      },
      "novel": {
        "paths": 2000,
        "uniqueWords": 18885,
        "wordHits": 11057,
        "fullSentences": 45,
        "unrankedPairs": 533720,
        "arcHits": 7802,
        "rankPairs": 103704,
        "rankHits": 5558,
        "crossHits": 1071,
        "rankCrossHits": 191,
        "sumExcess": 4768,
        "maxExcess": 21,
        "uniqueGoldCompleteButNoPath": 57,
        "pairedWordGain": 495,
        "pairedWordLoss": 5,
        "pairedArcGain": 605,
        "pairedArcLoss": 102,
        "pairedRankGain": 417,
        "pairedRankLoss": 80
      },
      "balanced": {
        "paths": 2000,
        "uniqueWords": 18438,
        "wordHits": 11006,
        "fullSentences": 48,
        "unrankedPairs": 513862,
        "arcHits": 7737,
        "rankPairs": 99981,
        "rankHits": 5516,
        "crossHits": 1056,
        "rankCrossHits": 188,
        "sumExcess": 3710,
        "maxExcess": 18,
        "uniqueGoldCompleteButNoPath": 51,
        "pairedWordGain": 445,
        "pairedWordLoss": 6,
        "pairedArcGain": 523,
        "pairedArcLoss": 85,
        "pairedRankGain": 367,
        "pairedRankLoss": 72
      }
    },
    "16": {
      "cost": {
        "paths": 8000,
        "uniqueWords": 21456,
        "wordHits": 11497,
        "fullSentences": 87,
        "unrankedPairs": 701272,
        "arcHits": 8576,
        "rankPairs": 139369,
        "rankHits": 6134,
        "crossHits": 1154,
        "rankCrossHits": 200,
        "sumExcess": 10903,
        "maxExcess": 16,
        "uniqueGoldCompleteButNoPath": 48,
        "pairedWordGain": 0,
        "pairedWordLoss": 0,
        "pairedArcGain": 0,
        "pairedArcLoss": 0,
        "pairedRankGain": 0,
        "pairedRankLoss": 0
      },
      "novel": {
        "paths": 8000,
        "uniqueWords": 24326,
        "wordHits": 11774,
        "fullSentences": 89,
        "unrankedPairs": 844740,
        "arcHits": 8932,
        "rankPairs": 167570,
        "rankHits": 6397,
        "crossHits": 1207,
        "rankCrossHits": 210,
        "sumExcess": 17731,
        "maxExcess": 23,
        "uniqueGoldCompleteButNoPath": 75,
        "pairedWordGain": 278,
        "pairedWordLoss": 1,
        "pairedArcGain": 396,
        "pairedArcLoss": 40,
        "pairedRankGain": 300,
        "pairedRankLoss": 37
      },
      "balanced": {
        "paths": 8000,
        "uniqueWords": 24247,
        "wordHits": 11774,
        "fullSentences": 87,
        "unrankedPairs": 836988,
        "arcHits": 8936,
        "rankPairs": 166650,
        "rankHits": 6402,
        "crossHits": 1206,
        "rankCrossHits": 210,
        "sumExcess": 17432,
        "maxExcess": 23,
        "uniqueGoldCompleteButNoPath": 77,
        "pairedWordGain": 278,
        "pairedWordLoss": 1,
        "pairedArcGain": 395,
        "pairedArcLoss": 35,
        "pairedRankGain": 301,
        "pairedRankLoss": 33
      }
    }
  },
  "controls": 10
}
```
## 复算
固定六份文件依序传入；Node包装未运行，连接器核心实际执行。只加载已审阅固定自有代码，外部文本仅作数据。未修改生产、交接、冻结、证据等级、PR、训练、部署、主动CI或费用。原生、独立留出、真机未执行。
```js
const contents=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8"));
function study(contents){
 const [raw,dict,gdoc,adoc,pdoc,prior]=contents,ck=(v,m)=>{if(!v)throw Error(m)},code=s=>s.split("```js\n")[1].split("\n```")[0];
 const src=code(prior),ac=code(adoc),gc=code(gdoc),pc=code(pdoc);
 const hash=Function(ac.slice(ac.indexOf(" function utf("),ac.indexOf(" const bytes=utf(raw)"))+"\nreturn s=>{let b=utf(s);return {bytes:b.length,sha:sha1(utf('blob '+b.length+'\\0').concat(b))}};")();
 const source=[hash(raw),hash(dict)];ck(source[0].sha==="af8cc878e7934b38ce3c1a266053100e7c47de6f"&&source[1].sha==="d7fee8237f26524b38eee220647e4c5d79f00de9","hashes");
 const G=Function("dict","const ck=(x,m)=>{if(!x)throw Error(m)};\n"+gc.slice(gc.indexOf("const words=new Set()"),gc.indexOf("function analyze(g)"))+"\nreturn {graph,cls,words};")(dict);
 const R=Function(pc.split(" const stat=()=>")[0]+"\nreturn {align,segments};\n}\nreturn study('');")();
 const start=src.indexOf(" function paths(g,k)"),end=src.indexOf(" const stat=()=>",start);ck(start>=0&&end>start,"slice");
 const P=Function("G",src.slice(start,end)+"\nreturn {paths,tokens,key,edge,rank};")(G);
 const modes=["cost","novel","balanced"],K=[4,16],limit=64,key=P.key,edge=P.edge;
 function select(pool,k,mode){
  let ids=[0],seen=new Set(pool[0].keys);
  while(ids.length<Math.min(k,pool.length)){
   let best=null;
   for(let i=0;i<pool.length;i++)if(!ids.includes(i)){
    let novel=pool[i].keys.filter(x=>!seen.has(x)).length,v=mode==="cost"?-i:mode==="novel"?novel:novel/(1+pool[i].cost-pool[0].cost);
    if(!best||v>best.v||v===best.v&&i<best.i)best={v,i};
   }
   ids.push(best.i);for(let x of pool[best.i].keys)seen.add(x);
  }return {ids,seen};
 }
 const stat=()=>({paths:0,uniqueWords:0,wordHits:0,fullSentences:0,unrankedPairs:0,arcHits:0,rankPairs:0,rankHits:0,crossHits:0,rankCrossHits:0,sumExcess:0,maxExcess:0,uniqueGoldCompleteButNoPath:0,pairedWordGain:0,pairedWordLoss:0,pairedArcGain:0,pairedArcLoss:0,pairedRankGain:0,pairedRankLoss:0});
 const out={source,sentences:0,tokens:0,arcs:0,cross:0,poolPaths:0,metrics:Object.fromEntries(K.map(k=>[k,Object.fromEntries(modes.map(m=>[m,stat()]))])),controls:0};
 const delim=new Set(Array.from("，,、：:；;。！？!?"));
 for(let block of raw.trim().split(/\n\s*\n/)){
  let ls=block.split(/\r?\n/),text=ls.find(x=>x.startsWith("# text = "))?.slice(9);if(text===undefined)continue;
  let chars=Array.from(text),seg=R.segments(chars,delim),pool=P.paths(G.graph(chars,true),limit).map(p=>({cost:p.cost,ts:P.tokens(p)}));for(let p of pool)p.keys=p.ts.map(key);
  ck(pool.length&&new Set(pool.map(p=>JSON.stringify(p.keys))).size===pool.length,"pool");out.poolPaths+=pool.length;
  let pred={};
  for(let k of K){pred[k]={};for(let mode of modes){
   let sel=select(pool,k,mode),paths=sel.ids.map(i=>pool[i]),pairs=new Set(),rank=new Set();
   ck(paths.length===Math.min(k,pool.length)&&sel.ids[0]===0&&new Set(sel.ids).size===sel.ids.length,"equal path counts");
   for(let p of paths)for(let hs of P.rank(p.ts,chars,seg.index,"right")){for(let e of hs)pairs.add(e);for(let e of hs.slice(0,5))rank.add(e)}
   pred[k][mode]={...sel,paths,pairs,rank};
  }}
  let rows=ls.filter(x=>/^\d+\t/.test(x)).map(x=>x.split("\t")),al=R.align(text,rows);ck(al,"align");
  let gold=rows.map(r=>{let [i,j]=al.positions.get(+r[0]);return {i,j}}),gs=gold.map(key),goldSig=JSON.stringify(gs),arcs=[];
  for(let [i,r] of rows.entries()){let h=+r[6],rel=r[7].split(":")[0];if(!h||rel==="punct"||r[3]==="PUNCT")continue;let d=gold[i],v=gold[h-1],a=[...new Set(seg.index.slice(d.i,d.j).filter(x=>x>=0))],b=[...new Set(seg.index.slice(v.i,v.j).filter(x=>x>=0))];arcs.push({e:edge(d,v),cross:a.length===1&&b.length===1&&a[0]!==b[0]})}
  out.sentences++;out.tokens+=gs.length;out.arcs+=arcs.length;out.cross+=arcs.filter(a=>a.cross).length;
  for(let k of K)for(let mode of modes){
   let a=pred[k][mode],b=pred[k].cost,o=out.metrics[k][mode],full=a.paths.some(p=>JSON.stringify(p.keys)===goldSig);
   o.paths+=a.paths.length;o.uniqueWords+=a.seen.size;o.wordHits+=gs.filter(x=>a.seen.has(x)).length;o.fullSentences+=+full;o.uniqueGoldCompleteButNoPath+=+(!full&&gs.every(x=>a.seen.has(x)));
   o.unrankedPairs+=a.pairs.size;o.arcHits+=arcs.filter(x=>a.pairs.has(x.e)).length;o.rankPairs+=a.rank.size;o.rankHits+=arcs.filter(x=>a.rank.has(x.e)).length;o.crossHits+=arcs.filter(x=>x.cross&&a.pairs.has(x.e)).length;o.rankCrossHits+=arcs.filter(x=>x.cross&&a.rank.has(x.e)).length;
   o.sumExcess+=a.paths.reduce((n,p)=>n+p.cost-pool[0].cost,0);o.maxExcess=Math.max(o.maxExcess,...a.paths.map(p=>p.cost-pool[0].cost));
   for(let x of gs){o.pairedWordGain+=+(a.seen.has(x)&&!b.seen.has(x));o.pairedWordLoss+=+(!a.seen.has(x)&&b.seen.has(x))}
   for(let x of arcs){o.pairedArcGain+=+(a.pairs.has(x.e)&&!b.pairs.has(x.e));o.pairedArcLoss+=+(!a.pairs.has(x.e)&&b.pairs.has(x.e));o.pairedRankGain+=+(a.rank.has(x.e)&&!b.rank.has(x.e));o.pairedRankLoss+=+(!a.rank.has(x.e)&&b.rank.has(x.e))}
  }
 }
 for(let k of K)for(let mode of modes){
  let a=out.metrics[k][mode],b=out.metrics[k].cost;
  ck(a.paths===b.paths&&a.wordHits-b.wordHits===a.pairedWordGain-a.pairedWordLoss&&a.arcHits-b.arcHits===a.pairedArcGain-a.pairedArcLoss&&a.rankHits-b.rankHits===a.pairedRankGain-a.pairedRankLoss,"paired");out.controls++;
 }
 const control=[{cost:0,keys:["a","b"]},{cost:0,keys:["a","c"]},{cost:1,keys:["d","e","f"]}];
 ck(select(control,2,"cost").ids.join()==="0,1"&&select(control,2,"novel").ids.join()==="0,2"&&select(control,2,"balanced").ids.join()==="0,2","selection control");out.controls++;
 ck(out.sentences===500&&out.tokens===12665&&out.arcs===10395&&out.cross===1404,"cohort");out.controls++;
 const old=JSON.parse(prior.split("```json\n")[1].split("\n```")[0]);
 for(let k of K){let a=out.metrics[k].cost,b=old.metrics[k];ck(a.wordHits===b.goldTokens&&a.fullSentences===b.goldCompletePath&&a.arcHits===b.goldArcs&&a.rankHits===b.rank.right[5].gold&&a.rankPairs===b.rank.right[5].pairs,"predecessor parity");out.controls++}
 return out;
}
console.log(JSON.stringify(study(contents),null,2));
```
