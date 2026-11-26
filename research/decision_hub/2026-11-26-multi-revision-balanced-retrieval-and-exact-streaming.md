# 自主认知：同轮多修订混合检索的候选预算分配与精确流式前K搜索
2026-11-26。RESEARCH_CANDIDATE / RECOMBINED_PUBLIC_SYNTHETIC_DEVELOPMENT / CONNECTOR_JS_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。

## 基线与去重
起点及写前REST branches/main均为7602500dabf2e23b870728670848b7dbeb6772a0。读取20近期提交、15开放PR、decision_hub目录相关题名、v3.2及同步规程（blob 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85、26c4d946e48f01858fb8e8c2cb06e4f7ba91bf05），唯一产品交接前20行（5e74f4f0b37141d631740e844ad8bbbfed232e07）。#63仍在开放列表，未重新运行或核验其最新head。本轮实际读取前轮correlated-revision-worlds-and-descriptive-receipt b423dc1ef25582bc72d73f11efd1d3deb9cad3b4、raw-revision-to-confirmed-history-joint-ranking 6e17e892bc7bcc512efed8e28b8f29bee05c5877（含评分脚本）、conditional-edit-occurrence-scope-and-actual-history f59f7ae7a2d3a8ea2e24d7bb4d8e3df590648644、joint-guard-role-history-candidate-audit 94f6de457f60655cabb8f65dd90c6e4be81591cb 的报告前段。已有单项修订、条件/角色/历史三元组、给定路径掩码的多个编辑世界及一般前K检索研究，本轮只研究多个已标注修订组合下的候选资源分配及该固定词面评分的精确流式实现。不重复上一轮数学世界和事务试验，不声称全库无重复。

固定两份输入：
1. research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
2. research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
实际完整读取多次并核对连接器返回blob，未独立重算Git原始字节；复算包装提供字节核对。既有32情节64轮为ChatGPT研发辅助原创公开合成开发数据，非真人、非独立留出，不训练。历史110条来自首轮人工标注原文，模拟历史记录，不是实际已确认账本。首次运行发现字段标签不唯一，拒绝继续，改用情节ID与记录出现序号构成独立身份；实际有1个重复标签差额，所有12项显式引用均唯一映射到原记录，未把重复标签当成同一历史身份。当前标注仅用于选择评估组合、确定目标及评分，候选生成及排序不读取当前标注。研究者选定评分权重、候选边界、人工拼接、预算及比较策略；非盲测。

## 方法及适用边界
对12个有且仅有一个显式历史引用的第二轮原文，全部有序不同情节配对，共132组。使用全角分号拼接原文，保留每个组成原文的真实局部标点及偏移，已知的人工拼接边界充当两个候选组；不声称自动从任意自然语言发现编辑组。另构造12×20=240组带单个已标注目标及一个无显式引用标注情节的混合输入，后者不能当真实负样本，未计算精度。历史范围分别为两个情节的全部首轮记录，以及32情节全部110条记录；两者均包含目标，前者由实验构造提供情节范围，不能当自动决策范围识别。对同一来源的正反顺序不是独立样本。未将条件、撤回授权、事实报告、目标或角色提升等不同编辑类别强行映射成数值变更。
每个原始标点段枚举长度2至32的UTF16跨度（本原型未转Unicode标量协议），历史记录文字为检索对象。评分S=4(J字+J双字)+2(J段字+J段双字)+边界项；边界项为是否匹配段首、段尾的0.5之和。J为集合Jaccard。评分只作线索，不能充当语义概率。按分数、人工组序号、原文起止、记录出现身份依次排序，完全确定但同分不代表真实更优。三种预算策略：global全局排序；equal按人工两个组轮流取其下一高分候选；spanRound按同一原文跨度分桶，依各桶首项全局顺序轮流取各桶下一历史候选。每策略前K边数严格一致，K=5、10、20、50、100。候选跨度及记录根双精确命中才计召回，任意候选仍authority NONE、无数学发布/账本写入权限。仅诊断候选覆盖，未实现分词共同路径见证、条件作用域、语义角色、修订目标资格或实际关联编辑世界。评分策略与前序使用propose的报告不同，不把两者的分数直接比较或称复现。

## 实际结果一：预算分配
连接器标准JS实际执行，首次身份检查失败，修正后完整成功一次。132组在两范围的完整枚举池都包含两目标（非准确率）。累计候选边数局部历史150652、全历史2328040；每输入最大1764、27720。所有策略的预算、命中分拆及单调性检查通过，另3专项控制。同文不同根同分且身份保留，空历史无候选。每范围双目标计264，表为同时召回两项的场景数：

| K | 局部global | 局部equal | 局部spanRound | 全历史global | 全历史equal | 全历史spanRound |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 6 | 26 | 4 | 2 | 10 | 2 |
| 10 | 8 | 30 | 8 | 2 | 12 | 2 |
| 20 | 30 | 54 | 24 | 18 | 30 | 22 |
| 50 | 68 | 80 | 50 | 42 | 56 | 42 |
| 100 | 100 | 90 | 64 | 56 | 56 | 42 |

逐目标命中数（按K依序5/10/20/50/100）：局部global 62/100/144/194/230，equal 112/124/172/206/220，spanRound 60/100/136/170/190；全历史global 52/88/124/158/178，equal 80/88/132/176/176，spanRound 52/90/128/154/154。单独目标的局部历史排名：L03 56、L08 55、L15 2、S01 9、S02 1、S03 3、S04 1、S08 1、S10 19、S11 11、S12 2、S13 9。K20混合输入仅计已标注目标，局部global/equal/spanRound为153/159/141（240组），全历史119/120/123。equal在较小预算的人工双组检索中较好，但局部K100退步10组，全历史仍有102/132组缺完整双修订（K20）；spanRound无稳定优势。保留负结果，不继续针对12项已见样本调分。已知分组、词面边界及历史范围都是重要限制。原文完整召回不等于共同编辑见证、用户理解或允许执行。

## 方法二：精确流式搜索
仅优化上述固定评分的global排序及分组独立前K候选生成。给定两个双字集合大小a,b，J<=min(a,b)/max(a,b)（二者都空时按本算法J=0）。预计算段相似度，先精确计算字符集合相似度，再用双字J上界构造S上界；已有K项时，只有上界严格低于第K项实际分数（实现保留1e-12浮点安全余量）才跳过该候选的精确双字交集。相等时不可剪枝，保留确定排序键。按全序流式维护至多K项。证明：已保留K个严格更优候选且第K阈值不随继续遍历下降，被剪枝项不可能进入最终前K。该数学界在实数评分成立；浮点实现只在本次固定数据和控制中复核，不声称任意极大输入下形式化保证。若原文已被正确划成独立分组、评分不依赖其他组且使用同一全序，每组前K的并集足以恢复全局前K：未进入某组前K的候选至少被本组K项优先，不能进入全局前K。分组身份仍需真实引擎提供；不能凭这条性质推断语言分组真实或联合语义成立。流式算法仍访问全部候选对，预处理、原文、历史特征、段上下文等另耗空间；K只限制保留候选记录数，非整个进程内存上限。全量穷举对照同时保留大量候选，仅为实验。未测真实运行时间、峰值RSS、移动设备能耗；不把跳过双字交集比例换算为整体加速。

## 实际结果二：精确复算
连接器标准JS实际执行一次。32轮×110条历史，累计274670候选对；32轮的三个K分别和全枚举排序精确比较，96/96一致。132个有序双组×三个K，使用每组前K合并与全量合并排序比较，396/396一致。3专项控制：任选首情节额外检查每个剪枝上界（该额外审计计算不计节省）、空文本候选、保留记录数上界及计数。

| K | 候选对数 | 精确双字交集次数 | 跳过次数 | 单轮最大保留记录 |
| --- | ---: | ---: | ---: | ---: |
| 5 | 274670 | 116296 | 158374 | 5 |
| 20 | 274670 | 159625 | 115045 | 20 |
| 100 | 274670 | 221675 | 52995 | 100 |

两阶段共6专项控制；未执行Node文件包装、优化模式、原生引擎、独立验收、真实用户、竞品、Mac/iPhone。算法不需要第三方AI或训练。仅原创研究报告与代码，无个人数据、外部材料再分发、正式产品开发、PR合并、部署、主动CI或新增费用。冻结、历史证据等级及交接文件不变。

## 完整复算核心
将本报告两个函数保存到同一个JS文件，并追加末尾Node包装。两函数为实际运行代码；包装未单独执行。输入为上述固定两份JSON全文，仅处理数据，不执行外部输入。
~~~js
function study(contents){
 const ck=(v,m)=>{if(!v)throw Error(m)}, ds=contents.map(JSON.parse), eps=[],hist=[];
 for(let d=0;d<2;d++)for(let ep of ds[d].cases){const h=(d?ep.turns[0].proposal.claims:ep.turns[0].claims).map((x,i)=>({ep:ep.id,id:ep.id+":occ:"+(i+1),label:d?ep.id+".1."+(i+1):ep.id+":t0:"+x.field,q:d?x.quote:x.span}));hist.push(...h);const t=ep.turns[1];const refs=(d?t.proposal.claims:t.claims).filter(x=>d?x.ref:x.supersedes).map(x=>{const a=h.filter(y=>y.label===(d?x.ref:x.supersedes));ck(a.length===1,"ambiguous gold reference");return {q:d?x.quote:x.span,id:a[0].id}});eps.push({id:ep.id,text:t.text,h,refs})}
 ck(new Set(hist.map(x=>x.id)).size===hist.length,"history IDs");
 const ks=[5,10,20,50,100],modes=["global","equal","spanRound"],tagged=eps.filter(e=>e.refs.length===1);
 const ch=s=>new Set([...s].filter(c=>!/[\p{P}\s]/u.test(c))),grams=s=>{let a=[...s];return new Set(a.slice(1).map((v,i)=>a[i]+v).filter(v=>!/[\p{P}\s]/u.test(v)))},fe=s=>[ch(s),grams(s)],jac=(a,b)=>{let k=0;for(let x of a)if(b.has(x))k++;return k/(a.size+b.size-k||1)},sim=(a,b)=>jac(a[0],b[0])+jac(a[1],b[1]);
 const hf=hist.map(h=>({...h,f:fe(h.q)}));
 function pool(t,history){const a=[];for(const m of t.matchAll(/[^，。！？；、：,.!?;:\s]+/gu)){const s=m[0],o=m.index,ctx=fe(s);for(let i=0;i<s.length;i++)for(let j=i+2;j<=s.length&&j-i<=32;j++){const q=s.slice(i,j),f=fe(q),edge=(+(i===0)+ +(j===s.length))/2;for(const h of history)a.push({s:o+i,e:o+j,id:h.id,ep:h.ep,score:4*sim(f,h.f)+2*sim(ctx,h.f)+edge})}}return a}
 const cmp=(a,b)=>b.score-a.score||a.side-b.side||a.s-b.s||a.e-b.e||(a.id<b.id?-1:a.id>b.id?1:0);
 const cache=new Map(eps.map(e=>[e.id,pool(e.text,hf).map(x=>({...x,side:0})).sort(cmp)]));
 function order(sorted,mode,limit=100){if(mode==="global")return sorted.slice(0,limit);const buckets=new Map();for(const x of sorted){const key=mode==="equal"?x.side:x.side+":"+x.s+":"+x.e;if(!buckets.has(key))buckets.set(key,[]);const g=buckets.get(key);if(g.length<limit)g.push(x)}
  const groups=[...buckets.values()];const a=[];for(let i=0;a.length<Math.min(limit,sorted.length);i++)for(let g of groups)if(i<g.length&&a.length<limit)a.push(g[i]);return a}
 function metrics(){return Object.fromEntries(modes.map(m=>[m,Object.fromEntries(ks.map(k=>[k,{edges:0,hits:0,both:0,firstOnly:0,secondOnly:0,none:0}]))]))}
 const out={episodes:eps.length,history:hist.length,duplicateLabels:hist.length-new Set(hist.map(x=>x.label)).size,tagged:tagged.length,controls:0,scopes:{},single:{}};
 function combined(a,b,scope){const off=a.text.length+1,keep=x=>scope==="all"||x.ep===a.id||x.ep===b.id;const A=cache.get(a.id).filter(keep),B=cache.get(b.id).filter(keep).map(x=>({...x,s:x.s+off,e:x.e+off,side:1}));let i=0,j=0,z=[];while(i<A.length&&j<B.length)z.push(cmp(A[i],B[j])<=0?A[i++]:B[j++]);return z.concat(A.slice(i),B.slice(j))}
 for(const scope of ["pair","all"]){let res={cases:0,fullBoth:0,pool:0,baseline:metrics(),mixed:{cases:0,hits:{global:0,equal:0,spanRound:0},edges:0},maxPool:0};out.scopes[scope]=res;
 for(const a of tagged)for(const b of tagged){if(a.id===b.id)continue;
  const raw=a.text+"；"+b.text,offset=a.text.length+1,sorted=combined(a,b,scope);
  const targets=[a,b].map((e,i)=>{let q=e.refs[0].q,s=e.text.indexOf(q);ck(s>=0&&s===e.text.lastIndexOf(q),"gold anchor");return {s:s+(i?offset:0),e:s+q.length+(i?offset:0),id:e.refs[0].id,side:i,q}});
  const hit=(x,t)=>x.s===t.s&&x.e===t.e&&x.id===t.id&&x.side===t.side;
  ck(targets.every(t=>raw.slice(t.s,t.e)===t.q),"span bound");res.cases++;res.pool+=sorted.length;res.maxPool=Math.max(res.maxPool,sorted.length);
  const full=targets.map(t=>sorted.some(x=>hit(x,t)));res.fullBoth+=full.every(Boolean);
  for(const m of modes){const ranked=order(sorted,m);ck(ranked.length===Math.min(100,sorted.length)&&new Set(ranked).size===ranked.length,"unique prefix");let last=0;for(const k of ks){const arr=ranked.slice(0,k),[h1,h2]=targets.map(t=>arr.some(x=>hit(x,t))),v=res.baseline[m][k];v.edges+=arr.length;v.hits+=+h1+ +h2;v.both+=h1&&h2;v.firstOnly+=h1&&!h2;v.secondOnly+=!h1&&h2;v.none+=!h1&&!h2;ck(+h1+ +h2>=last,"monotonic");last=+h1+ +h2} }
 }
 for(const a of tagged)for(const b of eps.filter(e=>!e.refs.length)){const list=combined(a,b,scope);let s=a.text.indexOf(a.refs[0].q),id=a.refs[0].id,e=s+a.refs[0].q.length;for(let m of modes)res.mixed.hits[m]+=order(list,m,20).some(x=>x.side===0&&x.s===s&&x.e===e&&x.id===id);res.mixed.cases++;res.mixed.edges+=Math.min(20,list.length)}
 for(let m of modes)for(let k of ks){let v=res.baseline[m][k];ck(v.both+v.firstOnly+v.secondOnly+v.none===res.cases&&v.hits===2*v.both+v.firstOnly+v.secondOnly,"partition");ck(v.edges===res.baseline.global[k].edges,"equal budget")}
 }
 for(const e of tagged){const z=cache.get(e.id).filter(x=>x.ep===e.id);let s=e.text.indexOf(e.refs[0].q),e1=s+e.refs[0].q.length;out.single[e.id]=z.findIndex(x=>x.s===s&&x.e===e1&&x.id===e.refs[0].id)+1}
 const synthetic=[{id:"A",ep:"x",q:"每周最多十小时",f:fe("每周最多十小时")},{id:"B",ep:"x",q:"每周最多十小时",f:fe("每周最多十小时")}];const z=pool("每周改成八小时",synthetic);ck(z.length>0&&z.every(x=>z.some(y=>x.s===y.s&&x.e===y.e&&x.id!==y.id&&x.score===y.score)),"same text different roots");out.controls++;
 ck(pool("没有历史",[]).length===0,"empty history");out.controls++;
 ck(tagged.length===12&&eps.length===32&&hist.length===110,"source counts");out.controls++;return out
}
function boundedStudy(contents){
 const ck=(x,m)=>{if(!x)throw Error(m)},eps=[],hist=[],ks=[5,20,100];
 for(let d=0;d<2;d++)for(const ep of JSON.parse(contents[d]).cases){const t=ep.turns[1];eps.push({id:ep.id,t:t.text,tagged:(d?t.proposal.claims:t.claims).some(x=>d?x.ref:x.supersedes)});hist.push(...(d?ep.turns[0].proposal.claims:ep.turns[0].claims).map((x,i)=>({id:ep.id+":occ:"+(i+1),q:d?x.quote:x.span})))}
 const ch=s=>new Set([...s].filter(c=>!/[\p{P}\s]/u.test(c))),grams=s=>{let a=[...s];return new Set(a.slice(1).map((v,i)=>a[i]+v).filter(v=>!/[\p{P}\s]/u.test(v)))},fe=s=>[ch(s),grams(s)],jac=(a,b)=>{let k=0;for(let x of a)if(b.has(x))k++;return k/(a.size+b.size-k||1)},sim=(a,b)=>jac(a[0],b[0])+jac(a[1],b[1]);
 const hf=hist.map(h=>({...h,f:fe(h.q)})),cmp=(a,b)=>b.score-a.score||a.side-b.side||a.s-b.s||a.e-b.e||(a.id<b.id?-1:a.id>b.id?1:0);
 const out={episodes:eps.length,roots:hf.length,fullPairs:0,byK:{},mergeChecks:0,controls:0};
 for(const k of ks)out.byK[k]={pairs:0,exactGrams:0,pruned:0,peakRetained:0,checks:0};
 function enumerate(t,k=null,verify=false){let kept=[],stats={pairs:0,exactGrams:0,pruned:0,peakRetained:0};
  for(const m of t.matchAll(/[^，。！？；、：,.!?;:\s]+/gu)){const s=m[0],o=m.index,ctx=fe(s),cs=hf.map(h=>2*sim(ctx,h.f));for(let i=0;i<s.length;i++)for(let j=i+2;j<=s.length&&j-i<=32;j++){const q=s.slice(i,j),f=fe(q),edge=(+(i===0)+ +(j===s.length))/2;for(let hi=0;hi<hf.length;hi++){const h=hf[hi],u=jac(f[0],h.f[0]),v=Math.min(f[1].size,h.f[1].size)/(Math.max(f[1].size,h.f[1].size)||1),upper=4*(u+v)+cs[hi]+edge;stats.pairs++;
    if(k!==null&&kept.length===k&&upper<kept[k-1].score-1e-12){stats.pruned++;if(verify)ck(4*(u+jac(f[1],h.f[1]))+cs[hi]+edge<=upper+1e-12,"upper");continue}
    const score=4*(u+jac(f[1],h.f[1]))+cs[hi]+edge;stats.exactGrams++;ck(score<=upper+1e-12,"upper");const x={s:o+i,e:o+j,id:h.id,score,side:0};
    if(k===null)kept.push(x);else if(kept.length<k||cmp(x,kept[k-1])<0){let lo=0,high=kept.length;while(lo<high){let mid=(lo+high)>>1;if(cmp(x,kept[mid])<0)high=mid;else lo=mid+1}if(kept.length===k)kept.pop();kept.splice(lo,0,x)}
    stats.peakRetained=Math.max(stats.peakRetained,kept.length)
  }}}
  if(k===null)kept.sort(cmp);ck(stats.pairs===stats.exactGrams+stats.pruned,"partition");return {kept,stats}}
 const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b),all=new Map(),tops=new Map();
 for(const e of eps){const z=enumerate(e.t);all.set(e.id,z.kept);out.fullPairs+=z.stats.pairs;const t=new Map();tops.set(e.id,t);for(const k of ks){let b=enumerate(e.t,k);ck(equal(b.kept,z.kept.slice(0,k)),"top k");t.set(k,b.kept);let o=out.byK[k];for(let f of ["pairs","exactGrams","pruned"])o[f]+=b.stats[f];o.peakRetained=Math.max(o.peakRetained,b.stats.peakRetained);o.checks++}}
 const offset=(xs,o)=>xs.map(x=>({...x,s:x.s+o,e:x.e+o,side:1})),tagged=eps.filter(e=>e.tagged);
 for(const a of tagged)for(const b of tagged){if(a===b)continue;const off=a.t.length+1,whole=[...all.get(a.id),...offset(all.get(b.id),off)].sort(cmp);for(const k of ks){const split=[...tops.get(a.id).get(k),...offset(tops.get(b.id).get(k),off)].sort(cmp).slice(0,k);ck(equal(split,whole.slice(0,k)),"merge top k");out.mergeChecks++}}
 const probe=enumerate(eps[0].t,5,true);ck(equal(probe.kept,all.get(eps[0].id).slice(0,5)),"verify pruned");out.controls++;
 ck(enumerate("。！？",5).kept.length===0,"empty");out.controls++;
 ck(Object.values(out.byK).every(x=>x.peakRetained<=100&&x.pairs===out.fullPairs),"counts");out.controls++;
 return out
}
const fs=require("node:fs"),crypto=require("node:crypto");
const expected=["be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb","05c239f3f3b1f46235fa2464d2945c21c6c08132"];
const buffers=process.argv.slice(2).map(p=>fs.readFileSync(p));
if(buffers.length!==2||buffers.some((b,i)=>crypto.createHash("sha1").update("blob "+b.length+"\0").update(b).digest("hex")!==expected[i]))throw Error("asset identity");
const contents=buffers.map(b=>b.toString("utf8"));
console.log(JSON.stringify({retrieval:study(contents),streaming:boundedStudy(contents)},null,2));
~~~
说明：归档中study的模板字符串改为等价字符串连接以方便转录，boundedStudy删除一行注释；以上转录及文件包装未单独重跑。结果为连接器实际执行上述同算法。

## 下一责任及优先级
语言研究：以原生原文坐标和分组不确定性连接已有共同路径候选，避免将人工组或历史范围当自然理解，不能对所有未知自动补全。模型轨：比较相同评分的精确流式搜索和现有原生检索，并保留未获覆盖证明时的UNKNOWN。独立验收轨：持有未见多编辑案例，核查同句多修订、跨句照应、重复根、未标注目标、跨作用域、更正与撤回，比较召回、错误确定性、追问和资源实测。待正式授权后实现原生接入，不以检索实验提升v0.8条件或账本指标。
