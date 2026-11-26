# 自主认知：等弧预算跨段边界排序及共同分词见证诊断
2026-11-26。RESEARCH_CANDIDATE / REAL_EXTERNAL_DEVELOPMENT_BYTES_VERIFIED / EQUAL_UNIQUE_ARC_COUNT / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。

## 基线与范围
起点 main 72836aa4e98fa9c9d781dac889f3652b216245fd；读取 v3.2、同步规程、20近期提交清单及其中8项文件身份、3篇前序研究全文、15开放PR，#63 head 734686980b19da9291bdd08b67d4e2519c011acf 为Draft。最新唯一交接未定位，非全库去重。前序 equal-arc-budget-cross-segment-allocation 已比较多样性及最低配额；本轮固定最低成本16条路径，比较跨段排序与共同路径见证。前序已见开发集，绝非独立样本。
固定六个输入依序：
1. UniversalDependencies/UD_Chinese-GSDSimp af8cc878e7934b38ce3c1a266053100e7c47de6f（commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3）
2. rhcarvalho/cedict d7fee8237f26524b38eee220647e4c5d79f00de9（commit 6317ff202e14be60365c826f62e45fc9fa71d19e）
3. 本库 cee6b6f8d759b6aa33ec4f2863232a6583f8ae07
4. 本库 db9cc100d96d49832fe32879a706f63830301773
5. 本库 0633533cebfb0cdea6aecff4e422bd3d4cdb5188
6. 本库 aa0d6c5882107b142dd555d0872b073da034a642
第七项为固定起点main的 research/decision_hub/2026-11-26-diverse-token-path-selection-equal-count-diagnostic.md。
实际重新读取全部七项，继承原始Git SHA1独立计算实现，前两项完整字节1,195,378及9,881,659，摘要匹配。来源 https://universaldependencies.org/treebanks/zh_gsdsimp/ 与 https://www.mdbg.net/chinese/dictionary?page=cc-cedict ，沿用CC BY-SA 4.0登记，底层文本另审，本轮未重审许可全文。仅原创算法及聚合数，无语料再分发；未读train/test，未训练。

## 方法
每句固定最低成本16条分词路径，依存头排序按前序向右优先距离、跨路径取最低排名r、支持路径数n、端点字符串顺序。候选预算B为r<=5的唯一候选数。除基线外，先取最多floor(.2B)跨段候选，然后按原始排序补足B（配额为最低下限）。跨段排序对照：原排序reserve；support按支持路径数降序、段距升序、原排序；headBoundary按段距升序、头词至朝向依存词一侧的句段边界的字符距离升序、原排序；headRound按依存词跨度分组，每轮取各组下一最高排名项，组序为其首次出现在原排序中的位置。无标注、无拟合、无词性声称。候选全部生成后才读取gold。
对每条候选弧保存16位路径掩码M，命中gold弧集合H。联合见证存在当且仅当所有M的交集非空；每句可共存弧上界为max_p sum_{e in H} 1[p in M(e)]，分别算全部、跨段、九类scope关系代理。该见证只证端点可处于同一分词路径，不保证树、关系标签、语义或可执行性。多个目标的最大值可能来自不同路径。空集不计为失败。算法和预算研究者选择，不作生产准入；不能把路径支持数当概率。

## 实际结果
标准JS连接器运行500句、10395弧、1404跨段弧、2618 scope代理弧；前序两档基线复现（16路径、0及20%配额），5项配对预算恒等式，以及逐句逐策略联合掩码/最大值等价检查。首次编译因modes重复声明失败，改名modeList后完整执行一次；未计失败为成功。Node包装未执行。
| mode | pairs | crossPairs | hits | crossHits | scopeHits | gain | loss | jointAll | jointCross | jointScope | allWitnessFail | crossWitnessFail | scopeWitnessFail | crossMulti | scopeMulti |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| base |139369|22740|6134|200|1154|0|0|5711|200|1139|160|0|12|41|287|
| reserve |139369|28058|6097|222|1162|22|59|5688|222|1147|160|0|12|46|289|
| support |139369|36655|5924|280|1157|102|312|5535|280|1144|159|0|10|62|282|
| headBoundary |139369|32846|6103|300|1204|104|135|5704|300|1190|160|0|11|70|300|
| headRound |139369|31934|6101|273|1189|74|107|5699|272|1173|160|1|13|61|296|

headBoundary相对基线跨段增加100（50%）、总体净少31，scope代理增加50；同等最终弧数不等于等时间、内存。headBoundary的跨段300全部有同句共同分词见证（70句多跨段命中），但全部命中6103仅5704为同一路径上界之和，160句缺共同见证。headRound存在1句跨段命中不可同时见证。支持度策略反例：跨段增80但总体损210。结果支持保留边界排序候选，不证明一般泛化或自然语言理解准确率增加50%。下一阶段：固定预算下结合角色候选与关系类型、共同路径见证作为跨模块合同，候选分歧保留未知，独立轨控制未见样本。未改生产、PR、冻结、证据等级、交接、训练、部署或主动CI。未测设备耗时/内存、真机、真人决策、竞品与独立留出。

## 复算
以下为成功运行核心的Node文件包装，包装未执行。固定七份文件依序传入；只加载已审阅的自有前序代码，外部文本仅作数据。
```js
const contents=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8"));
const d=contents.pop().split("\x60\x60\x60js\n")[1].split("\n\x60\x60\x60")[0];
const prefix=d.slice(d.indexOf("function study(contents)"),d.indexOf(" const stat=()=>",d.indexOf(" function select(")));
const experiment=String.raw`
 const out={source,sentences:0,arcs:0,cross:0,scope:0,metrics:{},checks:0};
 const delim=new Set(Array.from("，,、：:；;。！？!?")),scope=new Set(["advcl","ccomp","xcomp","parataxis","conj","csubj","acl","mark","cc"]);
 const cmp=(a,b)=>a.r-b.r||b.n-a.n||(a.e<b.e?-1:a.e>b.e?1:0);
 const modeList=["base","reserve","support","headBoundary","headRound"];
 for(let block of raw.trim().split(/\n\s*\n/)){
  let ls=block.split(/\r?\n/),txt=ls.find(x=>x.startsWith("# text = "))?.slice(9);if(txt===undefined)continue;
  let chars=Array.from(txt),seg=R.segments(chars,delim),pool=P.paths(G.graph(chars,true),16).map(p=>P.tokens(p)),map=new Map();
  let group=s=>{let [i,j]=s.split(":").map(Number),a=[...new Set(seg.index.slice(i,j).filter(x=>x>=0))];return a.length===1?a[0]:null};
  let bounds=new Map();for(let [i,g] of seg.index.entries())if(g>=0){let v=bounds.get(g)??[i,i+1];v[1]=i+1;bounds.set(g,v)}
  for(let [pi,ts] of pool.entries())for(let hs of P.rank(ts,chars,seg.index,"right"))for(let [ri,e] of hs.entries()){
    let v=map.get(e);if(v){v.r=Math.min(v.r,ri+1);v.n++;v.mask|=1<<pi;continue}
    let [d,h]=e.split(">"),a=group(d),b=group(h),cross=a!==null&&b!==null&&a!==b,[i,j]=h.split(":").map(Number);
    let boundary=cross?(b>a?i-bounds.get(b)[0]:bounds.get(b)[1]-j):0;
    map.set(e,{e,d,h,r:ri+1,n:1,mask:1<<pi,cross,sd:cross?Math.abs(a-b):0,boundary})
  }
  let list=[...map.values()].sort(cmp),B=list.filter(x=>x.r<=5).length,q=Math.min(Math.floor(B*.2),list.filter(x=>x.cross).length),cross=list.filter(x=>x.cross),pred={};
  for(let mode of modeList){
   let c=cross.slice();if(mode==="support")c.sort((a,b)=>b.n-a.n||a.sd-b.sd||cmp(a,b));
   if(mode==="headBoundary")c.sort((a,b)=>a.sd-b.sd||a.boundary-b.boundary||cmp(a,b));
   if(mode==="headRound"){
    let groups=new Map();for(let x of c){let g=groups.get(x.d)??[];g.push(x);groups.set(x.d,g)}
    let rr=[];for(let j=0;rr.length<c.length;j++)for(let g of groups.values())if(g[j])rr.push(g[j]);c=rr;
   }
   let S=new Set(mode==="base"?[]:c.slice(0,q).map(x=>x.e));for(let x of list){if(S.size===B)break;S.add(x.e)}ck(S.size===B,"budget");pred[mode]=S;
  }
  let rows=ls.filter(x=>/^\d+\t/.test(x)).map(x=>x.split("\t")),al=R.align(txt,rows);ck(al,"align");
  let arcs=[];for(let r of rows){let h=+r[6],rel=r[7].split(":")[0];if(!h||rel==="punct"||r[3]==="PUNCT")continue;let d=al.positions.get(+r[0]).join(":"),v=al.positions.get(h).join(":"),a=group(d),b=group(v);arcs.push({e:d+">"+v,cross:a!==null&&b!==null&&a!==b,scope:scope.has(rel)})}
  out.sentences++;out.arcs+=arcs.length;out.cross+=arcs.filter(a=>a.cross).length;out.scope+=arcs.filter(a=>a.scope).length;
  for(let mode of modeList){
   let S=pred[mode],base=pred.base,o=out.metrics[mode]??={pairs:0,crossPairs:0,hits:0,crossHits:0,scopeHits:0,gain:0,loss:0,jointAll:0,jointCross:0,jointScope:0,allWitnessFail:0,crossWitnessFail:0,scopeWitnessFail:0,crossMulti:0,scopeMulti:0};
   o.pairs+=B;o.crossPairs+=cross.filter(x=>S.has(x.e)).length;
   let hit=arcs.filter(a=>S.has(a.e));o.hits+=hit.length;o.crossHits+=hit.filter(a=>a.cross).length;o.scopeHits+=hit.filter(a=>a.scope).length;
   for(let a of arcs){o.gain+=+(S.has(a.e)&&!base.has(a.e));o.loss+=+(!S.has(a.e)&&base.has(a.e))}
   for(let [subset,joint,fail,multi] of [[hit,"jointAll","allWitnessFail",null],[hit.filter(a=>a.cross),"jointCross","crossWitnessFail","crossMulti"],[hit.filter(a=>a.scope),"jointScope","scopeWitnessFail","scopeMulti"]]){
    let mask=(1<<pool.length)-1,counts=Array(pool.length).fill(0);for(let a of subset){let m=map.get(a.e).mask;mask&=m;for(let i=0;i<pool.length;i++)counts[i]+=+(!!(m&(1<<i)))}
    let mx=Math.max(0,...counts);ck(mx<=subset.length&&(!subset.length||((mx===subset.length)===!!mask)),"witness");o[joint]+=mx;o[fail]+=+(subset.length>1&&!mask);if(multi)o[multi]+=+(subset.length>1)
   }
  }
 }
 const b=out.metrics.base;ck(out.sentences===500&&out.arcs===10395&&out.cross===1404&&b.pairs===139369&&b.hits===6134&&b.crossHits===200,"prior baseline");ck(out.metrics.reserve.hits===6097&&out.metrics.reserve.crossHits===222,"prior reserve");
 for(let o of Object.values(out.metrics)){ck(o.pairs===b.pairs&&o.hits-b.hits===o.gain-o.loss,"paired");out.checks++}return out;
}
`;
console.log(JSON.stringify(Function(prefix+experiment+"\nreturn study;")()(contents),null,2));
```
