# 自主认知：等依存候选预算下的分词多样性及跨句段配额诊断
2026-11-26。RESEARCH_CANDIDATE / REAL_EXTERNAL_DEVELOPMENT_BYTES_VERIFIED / EQUAL_UNIQUE_ARC_COUNT / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。

## 基线、问题及资产
起点 main e31e51f28574c0615cd5f8a9409d9ab24f195965；读取v3.2与同步规程、15近期提交、15开放PR，#63 head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft；最新唯一交接路径未定位，已核对决策枢纽文件清单，非全库去重。前轮仅固定路径数，候选弧数量增加。本轮控制每句最终唯一弧数量，考察多样性及跨段最低配额；不等于控制时间/内存或完整解析。前轮同一已见开发集，不能视作独立评价。

六个输入依次固定：
1. UniversalDependencies/UD_Chinese-GSDSimp blob af8cc878e7934b38ce3c1a266053100e7c47de6f（commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3）
2. rhcarvalho/cedict blob d7fee8237f26524b38eee220647e4c5d79f00de9（commit 6317ff202e14be60365c826f62e45fc9fa71d19e）
3. 本库 cee6b6f8d759b6aa33ec4f2863232a6583f8ae07
4. 本库 db9cc100d96d49832fe32879a706f63830301773
5. 本库 0633533cebfb0cdea6aecff4e422bd3d4cdb5188
6. 本库 aa0d6c5882107b142dd555d0872b073da034a642
第七项为起点main的 research/decision_hub/2026-11-26-diverse-token-path-selection-equal-count-diagnostic.md。实际读取以上资产，复用既有Git blob SHA1计算校验前两项1,195,378及9,881,659字节均匹配。来源 https://universaldependencies.org/treebanks/zh_gsdsimp/ 与 https://www.mdbg.net/chinese/dictionary?page=cc-cedict ，继承CC BY-SA 4.0许可登记，底层文本另审，未重审全文；只保存聚合计数与原创代码，不复制语料或词典。未读取train/test、未训练。

## 方法
固定每句前64条路径池，4/16条路径分别选最低成本与先前balanced折中策略。每条路径产生非纯标点词的全部有向候选头。按原文端点合并，记录最低右偏距离排名r、出现路径数n，按(r升序,n降序,原文端点字符串升序)排序。B为同句同K最低成本路径集合的r<=5唯一候选数。按0/10/20%预留跨段候选：先取排序最高的min(floor(B*f),可用跨段数)，再从整体排序补齐B。配额仅是下限，天然跨段候选仍可继续保留。每句在读取gold行前完成所有候选生成。基线r<=5集合因B定义而精确复现。跨段判定要求两端各映射到唯一非负句段编号且不同；scope是九类UD关系代理，不是实际语义作用域正确性。跨路径并集不保证同一分词路径、合法树或完整语义。排序、预算和配额均由研究者选择，未拟合，不自动准入。

## 实际运行结果
标准JS连接器核心完成500句、12665词、10395非root非punct依存弧、1404跨段弧。12项等预算与配对恒等式检查；两档基线完全复现上一轮候选数、总弧覆盖、跨段覆盖。首次源码截取误命中字符串内的终止标记而SyntaxError，修正为从select函数起点之后定位，未计为成功运行。完整成功运行一次，Node包装未运行。
| K | 路径 | 配额 | 唯一候选 | 跨段候选 | 正确弧 | 正确跨段弧 | scope代理 | 相对基线新增 | 相对基线丢失 |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
|4|cost|0|77932|12818|5221|182|1037|0|0|
|4|cost|0.1|77932|13149|5217|185|1038|3|7|
|4|cost|0.2|77932|15823|5144|198|1037|16|93|
|4|balanced|0|77932|10694|5036|146|974|309|494|
|4|balanced|0.1|77932|11134|5026|147|974|310|505|
|4|balanced|0.2|77932|14535|4961|162|963|313|573|
|16|cost|0|139369|22740|6134|200|1154|0|0|
|16|cost|0.1|139369|23215|6133|202|1155|2|3|
|16|cost|0.2|139369|28058|6097|222|1162|22|59|
|16|balanced|0|139369|20049|6064|190|1130|245|315|
|16|balanced|0.1|139369|20718|6061|192|1132|246|319|
|16|balanced|0.2|139369|26495|5963|210|1119|258|429|

同等最终弧数下，balanced策略在此排序中两档总覆盖均下降，不能把先前等路径数覆盖收益解释为同等候选资源优势。16路径cost的20%最低跨段配额增加22条跨段弧及8条scope代理，净少37条总体弧；不能据此宣称改进语义解析，不能确定一般情景最优配额。反例：分词候选多样性可能使更多不同词占用前排，导致原有正确候选被挤出。下一研究责任：比较无需gold的跨段头排序与基于词角色的候选分配，并检验同一完整路径的联合见证；维持原生确认、未知和硬门，独立留出由独立轨负责。未改生产、冻结、证据等级、PR、交接、训练、部署、主动CI或新增费用。设备时间与内存未测，真实用户、竞品和独立留出未执行。

## 复算
本地Node将以上七个文件依序传入。固定自有前序代码切片经审阅，外部文本仅作数据。以下核心为实际执行版本，文件包装未执行。
```js
const files=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8"));
const code=files.pop().split("\x60\x60\x60js\n")[1].split("\n\x60\x60\x60")[0];
const prefix=code.slice(code.indexOf("function study(contents)"),code.indexOf(" const stat=()=>",code.indexOf(" function select(")));
const experiment=String.raw`
 const modes2=["cost","balanced"],reserves=[0,.1,.2],out={source,sentences:0,tokens:0,arcs:0,cross:0,metrics:{},controls:0};
 const delim=new Set(Array.from("，,、：:；;。！？!?")),scope=new Set(["advcl","ccomp","xcomp","parataxis","conj","csubj","acl","mark","cc"]);
 const cmp=(a,b)=>a.r-b.r||b.n-a.n||(a.e<b.e?-1:a.e>b.e?1:0);
 function allocate(list,B,f){let q=Math.min(Math.floor(B*f),list.filter(a=>a.cross).length),chosen=new Set(list.filter(a=>a.cross).slice(0,q).map(a=>a.e));for(let a of list){if(chosen.size===B)break;chosen.add(a.e)}return chosen}
 for(let block of raw.trim().split(/\n\s*\n/)){
  let ls=block.split(/\r?\n/),txt=ls.find(x=>x.startsWith("# text = "))?.slice(9);if(txt===undefined)continue;
  let chars=Array.from(txt),seg=R.segments(chars,delim),pool=P.paths(G.graph(chars,true),limit).map(p=>({cost:p.cost,ts:P.tokens(p)}));for(let p of pool)p.keys=p.ts.map(key);
  let pred={};
  function group(s){let [i,j]=s.split(":").map(Number),a=[...new Set(seg.index.slice(i,j).filter(x=>x>=0))];return a.length===1?a[0]:null}
  for(let k of K){let lists={};for(let mode of modes2){let sel=select(pool,k,mode),map=new Map();for(let i of sel.ids){for(let heads of P.rank(pool[i].ts,chars,seg.index,"right"))for(let [r,e] of heads.entries()){let x=map.get(e);if(x){x.r=Math.min(x.r,r+1);x.n++}else{let [d,h]=e.split(">"),a=group(d),b=group(h);map.set(e,{e,r:r+1,n:1,cross:a!==null&&b!==null&&a!==b})}}}lists[mode]=[...map.values()].sort(cmp)}
   let B=lists.cost.filter(a=>a.r<=5).length;pred[k]={};
   for(let mode of modes2)for(let f of reserves){let list=lists[mode],id=mode+":"+f,S=allocate(list,B,f);ck(S.size===B,"equal budget infeasible");pred[k][id]={S,B,cross:list.filter(a=>a.cross&&S.has(a.e)).length};}
  }
  let rows=ls.filter(x=>/^\d+\t/.test(x)).map(x=>x.split("\t")),al=R.align(txt,rows);ck(al,"align");
  let gold=rows.map(r=>{let [i,j]=al.positions.get(+r[0]);return {i,j}}),arcs=[];
  for(let [i,r] of rows.entries()){let h=+r[6],rel=r[7].split(":")[0];if(!h||rel==="punct"||r[3]==="PUNCT")continue;let d=gold[i],v=gold[h-1],a=group(key(d)),b=group(key(v));arcs.push({e:edge(d,v),cross:a!==null&&b!==null&&a!==b,scope:scope.has(rel)})}
  out.sentences++;out.tokens+=rows.length;out.arcs+=arcs.length;out.cross+=arcs.filter(a=>a.cross).length;
  for(let k of K){let base=pred[k]["cost:0"].S;for(let [id,p] of Object.entries(pred[k])){let o=out.metrics[k+":"+id]??={pairs:0,crossPairs:0,hits:0,crossHits:0,scopeHits:0,gain:0,loss:0};o.pairs+=p.B;o.crossPairs+=p.cross;for(let a of arcs){let x=p.S.has(a.e),y=base.has(a.e);o.hits+=+x;o.crossHits+=+(x&&a.cross);o.scopeHits+=+(x&&a.scope);o.gain+=+(x&&!y);o.loss+=+(!x&&y)}}}
 }
 for(let k of K){let b=out.metrics[k+":cost:0"];ck(b.pairs===(k===4?77932:139369)&&b.hits===(k===4?5221:6134)&&b.crossHits===(k===4?182:200),"prior parity");for(let [id,o] of Object.entries(out.metrics).filter(([id])=>id.startsWith(k+":"))){ck(o.pairs===b.pairs&&o.hits-b.hits===o.gain-o.loss,"paired identities");out.controls++}}
 ck(out.sentences===500&&out.tokens===12665&&out.arcs===10395&&out.cross===1404,"cohort");return out;
}
`;
console.log(JSON.stringify(Function(prefix+experiment+"\nreturn study;")()(files),null,2));
```
