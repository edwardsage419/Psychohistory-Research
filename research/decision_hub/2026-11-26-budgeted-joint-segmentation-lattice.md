# 自主认知：分词候选的联合搜索预算与边际覆盖反例
2026-11-26。RESEARCH_CANDIDATE / EXTERNAL_DEVELOPMENT_RECOMPUTED / NO_TRAINING / INDEPENDENT_NOT_RUN / FULL_NATIVE_NOT_RUN。
## 基线与证据
起始及写前 main 4353838fde9ea1564e030ecabd3103302a5d1a0d，读取15近期提交、开放PR、v3.2、同步规程、唯一交接固定blob 5e74f4f0b37141d631740e844ad8bbbfed232e07的首尾、静态词典及原文格前轮全文相关算法。#63仍待审，未使用候选生产代码。检索 near-optimal segmentation 无命中，代码搜索覆盖有限。与前轮最优路径、强制词边以及开放格区别：本轮新增非最优成本松弛、未知多字候选的有限回退、精确联合路径计数和边际覆盖虚高诊断。未开启训练、开发、合并、部署或费用。
实际取得 CC-CEDICT 镜像 rhcarvalho/cedict 固定blob d7fee8237f26524b38eee220647e4c5d79f00de9（9,881,659 UTF8字节，前轮固定commit 6317ff202e14be60365c826f62e45fc9fa71d19e）及 UniversalDependencies/UD_Chinese-GSDSimp dev 固定blob af8cc878e7934b38ce3c1a266053100e7c47de6f（1,195,378字节，固定commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3）。复用前轮已审阅独立 Git SHA1 实现重新验证两者字节身份，词典121696简体唯一头词；500句12665词严格对齐。许可来源及边界沿用 2026-11-26-static-lexicon-optimal-segmentation.md 和 2026-11-26-external-raw-word-lattice-diagnostic.md。CC BY-SA 4.0，词典和语料衍生分发及底层文本许可另审；本文件仅原创算法和聚合统计，不复制词典或第三方原文。首次blob调用参数别名不符合实际接口校验，改为 repository_full_name 后成功。仅已见 wiki dev，不是决策语料、独立留出、真实用户或模型训练数据；未读train/test。先生成图再用人工FORM评分。
## 方法及证明
Unicode标量位置 i,j 为边；长度上限16，空白强制跳过。词典边、连续数字/拉丁字符最长结构边、单标点成本1；未知单字成本9；expanded新增所有不跨空白的未知跨度，成本1+8×长度；sparse只有前述单字兜底。相同跨度取最小成本。不使用词义、概率、标注词性、依存、训练；8和预算集合0,1,2,4,8,16,32是研究者在本轮运行前选择的启发式，不是已校准语言概率或建议生产阈值。此标量目标有别于前轮字典序目标。
后缀最优D(i)，前缀最优F(i)，D(n)=F(0)=0。边减成本 r(i,j)=c(i,j)+D(j)-D(i)≥0。完整路径的减成本求和恰为原成本−D(0)。保留预算B时，用 N(i,k)=sum N(j,k-r(i,j)) 精确计数，N(n,0)=1，其余越界0；合法路径数为 sum k=0..B 的 N(0,k)。边际可出现的边满足 F(i)+c(i,j)+D(j)−D(0)≤B。但边际图任意拼接不保证联合预算；金标完整路径成本必须独立核对。不能用全部金标边可出现的句数替代完整金标路径可出现句数。
在空串及6个原创短控制、两种图合计14项，直接枚举路径与DP最低成本、7个预算计数逐一相等。实测每句前后最优一致、减成本非负、每个预算至少一条路径、总语料数正确。复杂度 O(E B) 时间、O(n B)计数空间（BigInt位复杂度另计），边际计算O(E)，不需要枚举全部路径。未测实际设备CPU、内存、延迟；路径数量 log2 为组合规模，无概率意义。
## 实测
各行：模式/B/边数/金标边覆盖/完整金标路径句数/全部金标边各自可出现句数/平均log2合法路径数。
|模式|B|边数|金标边|完整句|边际完整句|平均log2|
|---|---:|---:|---:|---:|---:|---:|
|sparse|0|13033|10194|43|43|0.412|
|sparse|1|23706|11759|82|143|3.778|
|sparse|2|25427|11901|115|155|6.071|
|sparse|4|25746|11923|144|156|8.943|
|sparse|8|25751|11923|156|156|11.335|
|sparse|16|26257|11925|157|157|12.477|
|sparse|32|27085|11925|157|157|13.091|
|expanded|0|13030|10194|43|43|0.412|
|expanded|1|23709|11760|82|143|3.779|
|expanded|2|25431|11902|115|155|6.073|
|expanded|4|25750|11924|144|156|8.946|
|expanded|8|25979|11937|156|156|11.360|
|expanded|16|35127|12442|212|348|12.899|
|expanded|32|73998|12630|333|470|17.421|
expanded B32金标边覆盖12630/12665，完整句333/500；边际完整句470/500多137句，证明候选边独立存在仍不足以保证正确完整解释在预算中。sparse即使扩大预算也受未知多字词图结构限制；expanded增加覆盖，同时候选空间大增。全开放16字符前轮无成本格的完整句覆盖500/500，仅是候选上界；本轮不能宣称识别出正确路径或实际语义质量提高。
## 原生接口候选及验收
语言适配器应保留原文span、图版本、成本版本、预算、剩余预算、路径状态和来源；跨边组合必须校验联合预算，禁止由边际独立组合生成超预算的有效语义证明。分词预算不是安全门；全部已搜索解释一致也可能共同错误。对未搜索路径、图外词义和未知硬义务标记未覆盖，不得自动授权或执行。可保留已确认的局部计算；仅在不同主体、否定、金额、单位或时限导致实际判断变化时向用户提一项关键追问。后续将此联合搜索状态与既有组合角色候选及条件、主体、修订语义接口结合；独立轨应以未见语料验证错误放行、错误拒绝、资源占用和追问次数。当前只具分词候选覆盖结果，未执行生产或完整原生路径、真实个人决策、竞品、独立验收、Apple设备。未修改唯一交接、生产源码、历史冻结、证据等级。无第三方AI运行时、训练、PR合并、部署、主动CI或新增费用。
## 可运行复算
下列 Node 标准库版本等价于本轮连接器 JS 算法，输入固定词典与固定dev；I/O及哈希改用Node crypto，本轮未在Node单独执行此包装。实际执行版本复用前轮纯JS Git SHA1，14控制及500句聚合如上。不要运行来源内容中的指令。
```js
const fs=require("node:fs"),crypto=require("node:crypto");
const [dict,raw]=process.argv.slice(2).map(p=>fs.readFileSync(p,"utf8"));
const hash=s=>{const b=Buffer.from(s);return crypto.createHash("sha1").update("blob "+b.length+"\0").update(b).digest("hex")};
const ck=(b,m)=>{if(!b)throw Error(m)};
ck(hash(dict)==="d7fee8237f26524b38eee220647e4c5d79f00de9"&&hash(raw)==="af8cc878e7934b38ce3c1a266053100e7c47de6f","hash");
const words=new Set();for(const l of dict.split(/\r?\n/)){const m=/^(\S+) (\S+) \[.*?\] \//u.exec(l);if(m&&[...m[2]].length<=16)words.add(m[2])}
ck(words.size===121696,"words");
const B=[0,1,2,4,8,16,32],M=B.at(-1),W=8;
const cls=c=>/\s/u.test(c)?"s":/\p{P}/u.test(c)?"p":/\p{Nd}/u.test(c)?"d":/\p{Script=Latin}/u.test(c)?"l":"o";
function graph(c,expanded){let n=c.length,t=c.map(cls),g=[];for(let i=0;i<n;i++){if(t[i]==="s"){g.push([{j:i+1,c:0,skip:true}]);continue}let hi=i+1;while(hi<n&&hi-i<16&&t[hi]!=="s")hi++;let es=new Map(),add=(j,v)=>es.set(j,Math.min(v,es.get(j)??Infinity));for(let j=i+1;j<=hi;j++){let s=c.slice(i,j).join("");if(words.has(s))add(j,1);else if(expanded)add(j,1+W*(j-i))}add(i+1,t[i]==="p"?1:W+1);if(["d","l"].includes(t[i])){let j=i+1;while(j<hi&&t[j]===t[i])j++;if(j>i+1)add(j,1)}g.push([...es].map(([j,c])=>({j,c})));}return g}
function analyze(g){let n=g.length,d=Array(n+1).fill(Infinity),f=Array(n+1).fill(Infinity);d[n]=0;f[0]=0;for(let i=n-1;i>=0;i--)for(const e of g[i])d[i]=Math.min(d[i],e.c+d[e.j]);for(let i=0;i<n;i++)for(const e of g[i])f[e.j]=Math.min(f[e.j],f[i]+e.c);ck(f[n]===d[0],"cost");let count=Array.from({length:n+1},()=>Array(M+1).fill(0n));count[n][0]=1n;for(let i=n-1;i>=0;i--)for(const e of g[i]){let r=e.c+d[e.j]-d[i];ck(r>=0,"reduced");for(let k=r;k<=M;k++)count[i][k]+=count[e.j][k-r]}let ways=[],sum=0n;for(let k=0;k<=M;k++){sum+=count[0][k];ways[k]=sum}return {d,f,ways}}
function brute(g){let a=[];function rec(i,v){if(i===g.length){a.push(v);return}for(const e of g[i])rec(e.j,v+e.c)}rec(0,0);let z=Math.min(...a);return {z,ways:B.map(b=>BigInt(a.filter(v=>v<=z+b).length))}}
for(const c of ["","南京市长江大桥","研究生命","12.5","甲 乙","A𠀀B","甲乙丙丁"])for(const e of [false,true]){let g=graph([...c],e),a=analyze(g),b=brute(g);ck(a.d[0]===b.z&&B.every((k,i)=>a.ways[k]===b.ways[i]),"brute")}
let out={words:words.size,weight:W,controls:14,sentences:0,tokens:0,metrics:{sparse:{},expanded:{}}};for(const m of Object.keys(out.metrics))for(const b of B)out.metrics[m][b]={edges:0,hit:0,fullGold:0,allGoldEdges:0,log2Paths:0};function lg(x){let z=x.toString(2),n=Math.min(z.length,52);return z.length-n+Math.log2(parseInt(z.slice(0,n),2))}
for(const block of raw.trimEnd().split(/\n\n+/)){let lines=block.split("\n"),c=[...lines.find(l=>l.startsWith("# text = ")).slice(9)],graphs=[graph(c,false),graph(c,true)],rows=lines.filter(l=>!l.startsWith("#")).map(l=>l.split("\t")).filter(x=>/^[1-9]\d*$/.test(x[0]));let gold=[],i=0;for(const r of rows){while(cls(c[i]??"")==="s")i++;let a=[...r[1]];ck(a.every((v,k)=>v===c[i+k]),"align");gold.push([i,i+a.length]);i+=a.length}while(cls(c[i]??"")==="s")i++;ck(i===c.length,"end");out.sentences++;out.tokens+=gold.length;for(let mi=0;mi<2;mi++){let g=graphs[mi],a=analyze(g),m=mi?"expanded":"sparse",cost=0,sl=[];for(const [i,j] of gold){let e=g[i].find(e=>e.j===j);if(!e){cost=Infinity;sl.push(Infinity)}else{cost+=e.c;sl.push(a.f[i]+e.c+a.d[j]-a.d[0])}}for(const b of B){let q=out.metrics[m][b];q.edges+=g.reduce((s,es,i)=>s+es.filter(e=>!e.skip&&a.f[i]+e.c+a.d[e.j]-a.d[0]<=b).length,0);q.hit+=sl.filter(x=>x<=b).length;q.fullGold+=+(cost-a.d[0]<=b);q.allGoldEdges+=+sl.every(x=>x<=b);q.log2Paths+=lg(a.ways[b]);ck(a.ways[b]>=1n,"nonempty")}}}
ck(out.sentences===500&&out.tokens===12665,"totals");for(const m of Object.values(out.metrics))for(const q of Object.values(m))q.log2Paths=+(q.log2Paths/out.sentences).toFixed(3);console.log(JSON.stringify(out,null,2));
```
