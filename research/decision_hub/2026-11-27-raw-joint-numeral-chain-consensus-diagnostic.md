# 自主认知：原文联合词法、数量关系评分与一致性误放行
2026-11-27。RESEARCH_CANDIDATE / REAL_EXTERNAL_DEVELOPMENT_BYTES_VERIFIED / RAW_LEXICAL_AND_TREE_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。

## 基线与数据
起点及写前近期提交首位 2f6d2a3c3812ed15329a73901ee7b58ab4345d20。实际核对30近期提交、10开放PR、v3.2及同步规程全文、#63元数据（Draft未合并，head 734686980b19da9291bdd08b67d4e2519c011acf）。找到历史唯一交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07并读前6000字符，但未定位当前main的交接路径及最新修订。局部查重。此前数量关系评分仅在人工分词/词性条件下运行；此前联合词法实验只使用旧树评分。本轮交叉组合，并新增同一数词完整链一致性错误与独立原文扫描排序消融。

固定前序文件均在上述commit的research/decision_hub/：
seg 2026-11-26-static-lexicon-optimal-segmentation.md blob 6eb499cc01f023f352167cbe886d2f3144136cc7；
lat 2026-11-26-external-raw-word-lattice-diagnostic.md blob 86dcd5387b89c5302b1c139ad57a17b22f5d5a1d；
audit 2026-11-25-external-ud-development-corpus-structural-audit.md blob db9cc100d96d49832fe32879a706f63830301773；
tree 2026-11-25-projective-dependency-decoder-external-diagnostic.md blob c40a09357a858644a0da922097cd6367ca696df6；
lex 2026-11-27-raw-lexical-class-and-dependency-bridge.md blob 4e11926f9f174bcff0ae972119a8efdfb457659d；
joint 2026-11-27-joint-segmentation-class-budgeted-witness.md blob f7e550ca97f77b7d5ff93ea9f260d042b338bd01；
num 2026-11-27-external-numeral-predicate-chain-diagnostic.md blob 41032c25539db1368b8917d8ee4732174b488e86。
实际重复读取完整CC-CEDICT镜像 rhcarvalho/cedict 固定blob d7fee8237f26524b38eee220647e4c5d79f00de9（9881659字节），UD_Chinese-GSDSimp固定dev blob af8cc878e7934b38ce3c1a266053100e7c47de6f（1195378字节）；沿用seg的Git SHA1及audit验证通过。来源commit、CC BY-SA 4.0、底层文本权利独立及限制沿用seg、num，未重审许可全文、未复制第三方文本、未训练、未读train/test。公开已见wiki开发集非独立留出或真实个人决策。500句12665词元654数词；719原始数字串中540恰好对齐NUM标注。人工标注只参与评价。

## 实际方法
同一原文词格、相同词类预算K4，固定分词与联合词法分别使用旧matrix及num中已固定的数量提示matrix，未改参数。每句各四次单根投射树解码，共8000次，逐树检查合法及原分数重算。链终止于首个谓词代理或ROOT；比较字符跨度序列，不拼接候选树，不等同完整语义。候选粗类P映射VERB，金标谓词用S.pred。数词目标按四候选的存在性及链序列分类：missing全部无精确锚；stable有至少一个锚且所有出现链相同；mixed存在多个不同链；unanimous为stable且四候选均有锚。rawStable仅对原文数字串且四候选完整链相同，无需金标参与选取。rawStableNotGold是无精确NUM金标的原文锚，不能直接当真实语言错误。额外按每候选与独立原始数字串精确对齐的粗Q数量降序重排，同分保留原序。该提示仅检验锚，不是完整语义反向约束；尚未实现真正事件/对象/单位/条件反馈。四算法均无权威。候选预算相同不等于CPU或内存相同。

## 结果
| 指标 | fixedOld | fixedTyped | jointOld | jointTyped |
| --- | ---: | ---: | ---: | ---: |
| top完整链 |42|43|40|42|
| union完整链 |48|50|46|49|
| headTop |220|266|221|268|
| headUnion |246|274|248|276|
| anchorTop |436|436|436|436|
| anchorUnion |441|441|441|441|
| stable |293|302|291|300|
| stableCorrect |33|40|30|38|
| stableWrong |260|262|261|262|
| missing |213|213|213|213|
| mixed |148|139|150|141|
| unanimous |288|297|286|295|
| unanimousCorrect |33|40|30|38|
| unanimousWrong |255|257|256|257|
| rawStable |325|330|325|332|
| rawStableCorrect |33|40|30|38|
| rawStableNotGold |37|33|39|37|
| top新增对fixedOld |0|10|0|10|
| top丢失对fixedOld |0|9|2|10|

四组rerankChanged、rerankGained、rerankLost均0，故重排top和head与原首位一致。21项聚合一致性检查通过，其中20项分组恒等式、1项历史数值及数据规模复现。首次完整运行通过断言，但输出阶段误将L.gh对象当函数导致无结果输出；重新完整执行后成功，不声称两次输出一致。fixedTyped首位净+1但9个旧正确链丢失；同一数词四链一致的297个目标中257个错误，约86.5%，直接反证一致性足以放行。rawStable仅40/330与完整金标链一致，且33锚未精确对应NUM；此是开发集诊断，非真实决策错误率或独立校准。未批准替换原算法。

## 复算
以下标准JS以d对象为输入，各键为上列固定文件的{content,sha}，dict与raw为固定外部blob全文。沿用joint的函数提取包装，新增num的matrix提取及下列统计循环；仅执行项目自有已审阅源码，第三方文本仅作数据。
```js
const c=s=>s.content.split("\x60\x60\x60js\n")[1].split("\n\x60\x60\x60")[0];
const L=Function(c(d.seg).split(" let o={dictionary:")[0]+"\nreturn {graph,global,gh,verified};\n}\nreturn experiment;")()(dict,raw,d.audit.content,d.lat.content);
const P=Function(c(d.tree).split(" const out={sentences:")[0]+"\nreturn {valid,score,decode,matrix};\n}\nreturn experiment();")();
const S=Function("return function(dict){"+c(d.lex).split("function study(dict,raw,L,P){")[1].split(" const cmp=")[0]+"\nreturn {scores,transition,coarse,pred,classes,punct};}")()(dict);
const paths=Function("S","const cmp=(a,b)=>a.u-b.u||a.v-b.v||(a.key<b.key?-1:a.key>b.key?1:0);function paths("+c(d.joint).split("function paths(")[1].split("\nfunction chain(")[0]+"\nreturn paths;")(S);
const pc=c(d.num),i=pc.indexOf(" function matrix(ts,mode)"),j=pc.indexOf(" function rank(",i);
const typed=Function("P",'const nom=new Set(["NOUN","PROPN","PRON"]),clfs=new Set(["个","名","位","只","件","次","项","套","家","本","辆","张","条","台","所","种","部","人","年","月","日","天","小时","分钟","米","公里","元","岁"]);'+pc.slice(i,j)+';return matrix;')(P);
const ck=(x,m)=>{if(!x)throw Error(m)},span=t=>t.a+":"+t.b,chain=(i,ts,h,pred)=>{let z=[];for(let k=0;k<ts.length;k++){let j=h[i];if(!j){z.push("ROOT");return JSON.stringify(z)}z.push(span(ts[j]));if(pred(j))return JSON.stringify(z);i=j}throw Error("cycle")};
const fresh=()=>({top:0,union:0,headTop:0,headUnion:0,anchorTop:0,anchorUnion:0,stable:0,stableCorrect:0,stableWrong:0,missing:0,mixed:0,unanimous:0,unanimousCorrect:0,unanimousWrong:0,rawStable:0,rawStableCorrect:0,rawStableNotGold:0,rerankTop:0,rerankHead:0,rerankChanged:0,gained:0,lost:0,rerankGained:0,rerankLost:0});
let out={sentences:0,nums:0,rawAnchors:0,rawGold:0,treeCalls:0,metrics:{fixedOld:fresh(),fixedTyped:fresh(),jointOld:fresh(),jointTyped:fresh()},checks:0};
for(let block of raw.trimEnd().split(/\n\n+/)){
 let lines=block.split("\n"),txt=lines.find(x=>x.startsWith("# text = ")).slice(9),chars=[...txt],g=L.graph(chars,true),fix=L.global(g),chosen=new Map(fix.pred.map(e=>[e.i,e.j])),fg=g.map((es,i)=>es.filter(e=>e.skip||chosen.get(i)===e.j));
 let gold=[null,...lines.filter(x=>!x.startsWith("#")).map(x=>x.split("\t")).filter(c=>/^[1-9]\d*$/.test(c[0])).map(c=>({id:+c[0],form:c[1],pos:c[3],head:+c[6],misc:c[9]}))];let cur=0;for(let t of gold.slice(1)){t.a=cur;cur+=[...t.form].length;t.b=cur;if(!t.misc.split("|").includes("SpaceAfter=No"))cur++}
 let gh=gold.map(t=>t?.head??-1),nums=gold.slice(1).filter(t=>t.pos==="NUM"),goldMap=new Map(nums.map(t=>[span(t),{chain:chain(t.id,gold,gh,j=>S.pred.has(gold[j].pos)),head:t.head?span(gold[t.head]):"ROOT"}]));
 let rawAnchors=new Set();for(let m of txt.matchAll(/[0-9０-９零〇一二两俩三四五六七八九十百千万亿壹贰叁肆伍陆柒捌玖拾佰仟萬億]+(?:[.．点][0-9０-９零〇一二两三四五六七八九]+)?/gu)){let a=[...txt.slice(0,m.index)].length;rawAnchors.add(a+":"+(a+[...m[0]].length))}
 out.sentences++;out.nums+=nums.length;out.rawAnchors+=rawAnchors.size;out.rawGold+=[...rawAnchors].filter(a=>goldMap.has(a)).length;
 let rows={};for(let [prefix,seq] of [["fixed",paths(fg,chars,4,"lex")],["joint",paths(g,chars,4,"lex")]]){
 ck(seq.length===4,"four paths");for(let [suffix,mode] of [["Old","old"],["Typed","typed"]]){
 let key=prefix+suffix,stat=out.metrics[key],arr=seq.map(p=>{
 let ts=[null,...p.ts.map(t=>({...t,pos:S.punct(t.form)?"PUNCT":({N:"NOUN",P:"VERB",Q:"NUM",O:"X"})[S.classes[t.label]]}))],w=typed(ts,mode),d=P.decode(w);out.treeCalls++;ck(d.status==="CANDIDATE"&&P.valid(d.heads,true)&&P.score(w,d.heads)===d.best,"tree witness");
 let m=new Map();for(let i=1;i<ts.length;i++)if(ts[i].label===2)m.set(span(ts[i]),{chain:chain(i,ts,d.heads,j=>ts[j].pos==="VERB"),head:d.heads[i]?span(ts[d.heads[i]]):"ROOT"});return m
 });rows[key]=arr;let rer=arr.map((m,i)=>({m,i,score:[...rawAnchors].filter(a=>m.has(a)).length})).sort((a,b)=>b.score-a.score||a.i-b.i)[0];stat.rerankChanged+=+(rer.i!==0);
 for(let [a,v] of goldMap){let q=arr.map(m=>m.get(a)),hit=x=>x?.chain===v.chain,hh=x=>x?.head===v.head,distinct=new Set(q.filter(Boolean).map(x=>x.chain)),n=q.filter(Boolean).length;
 stat.top+=+hit(q[0]);stat.union+=+q.some(hit);stat.headTop+=+hh(q[0]);stat.headUnion+=+q.some(hh);stat.anchorTop+=+!!q[0];stat.anchorUnion+=+(n>0);stat.rerankTop+=+hit(rer.m.get(a));stat.rerankHead+=+hh(rer.m.get(a));stat.rerankGained+=+(!hit(q[0])&&hit(rer.m.get(a)));stat.rerankLost+=+(hit(q[0])&&!hit(rer.m.get(a)));
 if(n===0)stat.missing++;else if(distinct.size===1){stat.stable++;stat.stableCorrect+=+q.some(hit);stat.stableWrong+=+!q.some(hit);if(n===4){stat.unanimous++;stat.unanimousCorrect+=+q.some(hit);stat.unanimousWrong+=+!q.some(hit)}}else stat.mixed++;
 }
 for(let a of rawAnchors){let q=arr.map(m=>m.get(a));if(q.every(Boolean)&&new Set(q.map(x=>x.chain)).size===1){stat.rawStable++;stat.rawStableCorrect+=+(q[0].chain===goldMap.get(a)?.chain);stat.rawStableNotGold+=+!goldMap.has(a)}}
 }}
 for(let key of ["fixedTyped","jointOld","jointTyped"]){let base=rows.fixedOld[0],alt=rows[key][0];for(let [a,v] of goldMap){let b=base.get(a)?.chain===v.chain,t=alt.get(a)?.chain===v.chain;out.metrics[key].gained+=+(!b&&t);out.metrics[key].lost+=+(b&&!t)}}
}
for(let v of Object.values(out.metrics)){ck(v.stable+v.missing+v.mixed===out.nums,"partition");ck(v.stableCorrect+v.stableWrong===v.stable,"stable");ck(v.unanimousCorrect+v.unanimousWrong===v.unanimous,"unanimous");ck(v.top<=v.union&&v.anchorTop<=v.anchorUnion,"union");ck(v.rerankTop-v.top===v.rerankGained-v.rerankLost,"rerank");out.checks+=5}
ck(out.sentences===500&&out.nums===654&&out.metrics.fixedOld.top===42&&out.metrics.fixedOld.union===48&&out.metrics.jointOld.top===40&&out.metrics.jointOld.union===46&&out.rawGold===540,"previous controls");out.checks++;console.log(JSON.stringify(out));
```

## 下一责任与边界
研究者自主选择K4、四组合、完整链一致性分类和原始数字扫描重排。保留无权威与未知，进一步研究异质独立结构证据及对原文义务、单位、对象和条件的实际双向反馈，不能把词面扫描、一致性或共同树当资格。未执行v0.8原生入口、真实决策语义金标、独立留出、真人、竞品、设备资源、训练、生产集成、主动CI、合并或部署。不修改历史冻结、唯一交接或PR。零新增费用。
