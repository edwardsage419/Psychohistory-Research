# 自主认知：全句共同分词见证与依存端点覆盖上下界
2026-11-26。RESEARCH_CANDIDATE / EXTERNAL_DEVELOPMENT_RECOMPUTED / ORACLE_DIAGNOSTIC / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线及去重
本轮起始 main a74d80486f91a45994c3333b0660b05f9adfa515，写前 a74d80486f91a45994c3333b0660b05f9adfa515。已核对最新提交、开放PR、v3.2、同步规程、固定唯一交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07前段。#63仍Draft，未重跑。前轮 external-joint-word-endpoint-dependency-candidates 报告已测两词共同预算及候选头排序；更早联合分词报告已测完整金标路径。本轮新增同一条分词路径上最大金标词覆盖、实际见证中同时保留的依存弧端点数及严格上界、所有单弧均可保留仍不存在完整共同路径的反例计数。非全库无重复证明。
## 来源与许可
复用固定UD Chinese GSDSimp dev blob af8cc878e7934b38ce3c1a266053100e7c47de6f 与 CC-CEDICT 镜像 blob d7fee8237f26524b38eee220647e4c5d79f00de9，独立Git SHA1重算一致。固定源commit分别 b79a1c2f7ba7f9b264808d91c6886a67b7f847a3、6317ff202e14be60365c826f62e45fc9fa71d19e。复用自有R134审计blob db9cc100d96d49832fe32879a706f63830301773 与联合预算blob cee6b6f8d759b6aa33ec4f2863232a6583f8ae07。许可沿用已登记官方英文来源 https://universaldependencies.org/treebanks/zh_gsdsimp/ 与 https://www.mdbg.net/chinese/dictionary?page=cc-cedict ，CC BY-SA 4.0 与wiki底层权利分离；本轮未重新审阅许可全文，不分发第三方词条及原文，不读train/test。已见wiki开发数据，仅作非训练诊断，非独立留出或真实决策对话。
## 算法与证明
沿用 expanded 格与预算0/2/8/32。设后缀最短成本D(i)，减成本r=c+D(j)-D(i)>=0；总减成本为路径成本减全局最优。给定人工标注跨度，仅作为oracle评价，对每边设置命中指示I。V(i,b)=max_{e:i->j,r<=b}(I(e)+V(j,b-r))，终点仅剩余精确预算0可行。对0..B取最大，平局选较低预算，再按稳定边顺序选择；回溯验证实际成本和命中数。时间O(E*B)，DP空间O(n*B)，另有原前轮全点对距离O(nE)及O(n²)空间。非训练，不用金标给实际产品选择路径。依存树在k个保留词上诱导森林，非根弧数至多max(0,k-1)，与独立可行弧数取最小构成任何预算路径的共同弧上界；见证弧数提供最大共同弧数下界，二者不等时未求精确弧最优。弧只检验两金标端点共存，不是预测弧或关系。全弧独立可行且所有金标词边际可行并不保证完整树端点共存。120个原创短DAG×4预算穷举与DP逐一比较，未独立评价真实语言预测。研究者选择预算和oracle目标，继承前轮代价。
## 实际运行结果
```json
{
  "source": {
    "bytes": 1195378,
    "sha": "af8cc878e7934b38ce3c1a266053100e7c47de6f"
  },
  "dict": {
    "bytes": 9881659,
    "sha": "d7fee8237f26524b38eee220647e4c5d79f00de9"
  },
  "words": 121696,
  "sentences": 500,
  "tokens": 12665,
  "arcs": 12165,
  "controls": 480,
  "metrics": {
    "0": {
      "marginalTokens": 10194,
      "jointMaxTokens": 10177,
      "marginalArcs": 8338,
      "witnessArcs": 8327,
      "arcUpper": 8338,
      "pairwiseAll": 43,
      "pairwiseAllButNoFull": 0,
      "full": 43,
      "lossSentences": 16
    },
    "2": {
      "marginalTokens": 11902,
      "jointMaxTokens": 11377,
      "marginalArcs": 10877,
      "witnessArcs": 10107,
      "arcUpper": 10493,
      "pairwiseAll": 152,
      "pairwiseAllButNoFull": 37,
      "full": 115,
      "lossSentences": 149
    },
    "8": {
      "marginalTokens": 11937,
      "jointMaxTokens": 11917,
      "marginalArcs": 10940,
      "witnessArcs": 10912,
      "arcUpper": 10931,
      "pairwiseAll": 156,
      "pairwiseAllButNoFull": 0,
      "full": 156,
      "lossSentences": 10
    },
    "32": {
      "marginalTokens": 12630,
      "jointMaxTokens": 12352,
      "marginalArcs": 12092,
      "witnessArcs": 11661,
      "arcUpper": 11827,
      "pairwiseAll": 464,
      "pairwiseAllButNoFull": 131,
      "full": 333,
      "lossSentences": 148
    }
  }
}
```
未测运行设备资源，不构成语义准确率。下一步研究无需金标的结构约束解析与原生条件/角色接口；禁止以更大预算或候选覆盖作为理解证明。未改生产、交接、PR、训练、部署、主动CI、历史冻结、费用。
## 可执行复算
固定四个UTF8文件按 raw,dict,R134审计报告,联合预算报告 顺序传入。Node I/O包装未单独执行，核心在标准JS连接器实际运行。
```js
const fs=require('node:fs');
function study(raw,dict,a,g){
 const ck=(b,m)=>{if(!b)throw Error(m)},code=s=>s.split("```js\n")[1].split("\n```")[0],ac=code(a),gc=code(g);
 const hash=Function(ac.slice(ac.indexOf(" function utf("),ac.indexOf(" const bytes=utf(raw)"))+"\nreturn s=>{let b=utf(s);return {bytes:b.length,sha:sha1(utf('blob '+b.length+'\\0').concat(b))}};")();
 const rh=hash(raw),dh=hash(dict);
 ck(rh.sha==="af8cc878e7934b38ce3c1a266053100e7c47de6f"&&dh.sha==="d7fee8237f26524b38eee220647e4c5d79f00de9","hash");
 const G=Function("dict","const ck=(x,m)=>{if(!x)throw Error(m)};\n"+gc.slice(gc.indexOf("const words=new Set()"),gc.indexOf("function analyze(g)"))+"\nreturn {graph,cls,words};")(dict);
 const budgets=[0,2,8,32],key=(i,j)=>i+":"+j;
 function solve(g,gold){
  let n=g.length,d=Array(n+1).fill(Infinity);d[n]=0;for(let i=n-1;i>=0;i--)for(let e of g[i])d[i]=Math.min(d[i],e.c+d[e.j]);
  let labels=new Map(gold.map((v,k)=>[key(v.i,v.j),k]));
  let dp=Array.from({length:n+1},()=>Array(33).fill(null));dp[n][0]={v:0,p:null};
  for(let i=n-1;i>=0;i--)for(let e of g[i]){let delta=e.c+d[e.j]-d[i],idx=labels.get(key(i,e.j));ck(delta>=0&&Number.isInteger(delta),"delta");
   for(let b=delta;b<=32;b++){let child=dp[e.j][b-delta];if(!child)continue;let v=child.v+(idx!==undefined?1:0);if(!dp[i][b]||v>dp[i][b].v)dp[i][b]={v,p:{j:e.j,b:b-delta,idx}};}}
  return {base:d[0],best:B=>{let b=0;for(let k=1;k<=B;k++)if(dp[0][k]&&dp[0][k].v>dp[0][b].v)b=k;let k=b,i=0,sel=new Set(),cost=0;while(i<n){let p=dp[i][k].p;let e=g[i].find(e=>e.j===p.j);cost+=e.c;if(p.idx!==undefined)sel.add(p.idx);i=p.j;k=p.b}ck(cost-d[0]===b&&sel.size===dp[0][b].v,"witness");return {sel,b}}};
 }
 let out={source:rh,dict:dh,words:G.words.size,sentences:0,tokens:0,arcs:0,controls:0,metrics:Object.fromEntries(budgets.map(B=>[B,{marginalTokens:0,jointMaxTokens:0,marginalArcs:0,witnessArcs:0,arcUpper:0,pairwiseAll:0,pairwiseAllButNoFull:0,full:0,lossSentences:0}]))};
 // independent exhaustive path enumeration on short synthetic graphs, including deterministic random costs
 for(let seed=0;seed<120;seed++){let n=1+seed%7,gs=Array.from({length:n},(_,i)=>Array.from({length:n-i},(_,k)=>({j:i+k+1,c:1+((seed*17+i*7+k*13)%12)}))),gold=Array.from({length:n},(_,i)=>({i,j:i+1})),s=solve(gs,gold),paths=[];function go(i,c,t){if(i===n){paths.push({c,t});return}for(let e of gs[i])go(e.j,c+e.c,t+(e.j===i+1?1:0))}go(0,0,0);let min=Math.min(...paths.map(x=>x.c));ck(min===s.base,"min");for(let B of budgets){let max=Math.max(...paths.filter(x=>x.c<=min+B).map(x=>x.t));ck(max===s.best(B).sel.size,"oracle");out.controls++}}
 for(let block of raw.trimEnd().split(/\n\n+/)){let lines=block.split("\n"),c=[...lines.find(l=>l.startsWith("# text = ")).slice(9)],rows=lines.filter(l=>!l.startsWith("#")).map(l=>l.split("\t")).filter(x=>/^[1-9]\d*$/.test(x[0])),gold=[],i=0;for(let r of rows){while(G.cls(c[i]??"")==="s")i++;let a=[...r[1]];ck(a.every((v,k)=>v===c[i+k]),"align");gold.push({i,j:i+a.length,head:+r[6]-1});i+=a.length}while(G.cls(c[i]??"")==="s")i++;ck(i===c.length,"end");
  let gr=G.graph(c,true),n=c.length,ds=Array.from({length:n+1},()=>Array(n+1).fill(Infinity));for(let i=0;i<=n;i++){ds[i][i]=0;for(let j=i;j<n;j++)if(Number.isFinite(ds[i][j]))for(let e of gr[j])ds[i][e.j]=Math.min(ds[i][e.j],ds[i][j]+e.c)}
  let s=solve(gr,gold),base=ds[0][n];ck(s.base===base,"base");let e=gold.map(x=>({...x,c:gr[x.i].find(v=>v.j===x.j)?.c??Infinity})),sl=e.map(x=>ds[0][x.i]+x.c+ds[x.j][n]-base),arc=e.flatMap((x,k)=>{if(x.head<0)return [];let y=e[x.head],p=x,q=y;if(p.i>q.i)[p,q]=[q,p];return [{k,h:x.head,c:ds[0][p.i]+p.c+ds[p.j][q.i]+q.c+ds[q.j][n]-base}]});out.sentences++;out.tokens+=e.length;out.arcs+=arc.length;
  for(let B of budgets){let q=out.metrics[B],best=s.best(B),k=best.sel.size,m=sl.filter(v=>v<=B).length,ma=arc.filter(v=>v.c<=B).length,wa=arc.filter(v=>best.sel.has(v.k)&&best.sel.has(v.h)).length,u=Math.min(ma,Math.max(0,k-1));ck(k<=m&&wa<=u,"bounds");q.marginalTokens+=m;q.jointMaxTokens+=k;q.marginalArcs+=ma;q.witnessArcs+=wa;q.arcUpper+=u;q.pairwiseAll+=+(ma===arc.length&&m===e.length);q.pairwiseAllButNoFull+=+(ma===arc.length&&m===e.length&&k<e.length);q.full+=+(k===e.length);q.lossSentences+=+(k<m)}
 }
 ck(out.sentences===500&&out.tokens===12665&&out.arcs===12165,"totals");return out;
}
console.log(JSON.stringify(study(...process.argv.slice(2).map(p=>fs.readFileSync(p,'utf8'))),null,2));
```
