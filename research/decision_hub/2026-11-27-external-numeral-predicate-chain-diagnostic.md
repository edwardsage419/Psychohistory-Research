# 自主认知：外部真实开发语料数词依存、谓词祖先及联合路径诊断
2026-11-27。RESEARCH_CANDIDATE / REAL_EXTERNAL_DEVELOPMENT_BYTES_VERIFIED / GOLD_TOKEN_POS_CONDITIONED / RAW_NUMERAL_ANCHOR_DIAGNOSTIC / REUSED_DECODER_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。

## 基线与去重
起点及写前main c75f760d64f758e6288f4724f1689c959cbab3b5；核对20近期提交、15开放PR、v3.2及同步规程全文、唯一产品交接前20行，#63 head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft未合并。读前序数量上下文谓词80feb5e4264b555c6f7e5352178ccb5ba8117551、跨段共同见证a5589d2eda71c5abc26469f82e0ad8846efc0269、联合词端点3acea2859fa8095061cd2efb6f8918282803ab75、外部结构审计db9cc100d96d49832fe32879a706f63830301773、非投射解码0218ff41ee8fd68e5df1b2886cdfbee3368c8426前段及固定R134/R136完整实际代码。核对decision_hub目录数量、谓词、依存相关题名。已有单弧、词格、分词路径联合见证及原生数值识别不重复计。新增目标：原始数词锚跨度的真实外部标注覆盖、数量到谓词的多跳结构统计、在人工词形/词性条件下数量专用固定评分与原解码器的配对比较。非全库查重。未运行PR原生入口。

## 数据与许可
固定 UniversalDependencies/UD_Chinese-GSDSimp commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3，zh_gsdsimp-ud-dev.conllu blob af8cc878e7934b38ce3c1a266053100e7c47de6f，来源 https://github.com/UniversalDependencies/UD_Chinese-GSDSimp/blob/b79a1c2f7ba7f9b264808d91c6886a67b7f847a3/zh_gsdsimp-ud-dev.conllu 。实际两次完整Git blob读取并调用固定R134源码审计（UTF8 SHA1），1195378字节、Git blob身份一致，500句12665词元。来源说明及CC BY-SA 4.0标注许可沿用R134记录 https://universaldependencies.org/treebanks/zh_gsdsimp/ 及 https://creativecommons.org/licenses/by-sa/4.0/ ；底层原文权利分离，未重审许可全文，不复制原始第三方句子或标注至项目，不读train/test、不训练。wiki及人工/转换句法标注，已见开发数据，非真实个人决策、独立留出或语义义务金标。

## 合同
第一阶段只用原始字符串，枚举有限阿拉伯/中文数字连续串及小数尾，Unicode标量位置；不使用FORM、UPOS、HEAD决定候选。与已有NUM词元的精确位置及重叠位置对照。仅词面范围诊断，无数值归一化、单位、日期、比例、对象或真实语义确认；未精确对齐的候选不能直接算错，NUM不是全部真实数量。第二阶段输入外部人工分词、原始FORM、UPOS，NUM的位置也由人工标注给定，预测仅不读取金标HEAD/DEPREL；因此是oracle词法条件下的结构评分诊断，不是自主原文依存解析。谓词祖先定义为沿基础依存HEAD向上遇到的第一个VERB/ADJ/AUX，可能无该祖先；是句法代理，不等于真实事件谓词或语义角色。完整路径指从数词到该祖先每个节点都与标注一致。候选全部authority NONE/outside true。
实际复用R136的Eisner单根投射解码、matrix、valid、score；原始评分及新评分仅固定权重，无拟合。对NUM依存词，名词/专名/代词头+3、右侧有限量词/单位形式头+3、右侧+1、数词头-3；另对有限量词词面且词性NOUN/NUM/PART的依存词，右侧名词类头+2。词表、权重由研究者选定，形式提示不证明量词身份；可能伤害其他关系。对照distance将非根弧赋-2*距离，根弧赋0，局部排名偏向根，不能当公平强基线；主要对照为固定旧matrix，保留其实际3254/12665重现。三种树均为单根合法投射树，不保证语言正确，5个非投射金标树不一定可重现。没有关系标签预测、真实授权、数学输入资格或业务字段绑定。
对每个给定NUM分别排名直接头及谓词代理。直接头按弧分、距离、坐标；谓词候选对所有标注VERB/ADJ/AUX节点按直接弧分与经任一非谓词中间节点的两跳弧分和-2取最大，再按距离与坐标；distance谓词使用距离。K1/3/5/10取前K，实际候选数随句长和谓词数变化。两个端点同时命中是边际检索指标，不保证同一中间节点、树或真实语义共同可行；完整解码路径另计。排名不是概率。与上轮合成语义结构任务不共分母、不宣称直接接通数量语义框架。没有真实运行时或内存预算测量。

## 实际结果
500句12665词元，654个NUM在296句中。628个依存头在右侧，602个为NOUN，614个关系为nummod；427个数词的头或直接子节点恰为有限量词/单位形式之一（词面代理，不是量词真值）。567个存在谓词祖先，19个一跳、418个两跳、109个三跳、18个四跳、2个五跳、1个六跳；87个无此类祖先，不强制补槽。548个至少两跳；两跳及以下仅覆盖437个存在祖先的目标路径，谓词排名仍可通过直接弧命中更深祖先端点，不能当完整路径恢复。
原始数字串719个：540/654精确NUM位置，601/654有重叠，53个无重叠；1个恰为非NUM词元位置，178个不与任何完整单词位置完全一致（不直接作负例）。该简单扫描尚有114处NUM精确位置未恢复。
| 方法 | NUM直接头正确/654 | 谓词祖先正确/567 | 完整路径正确/567 | 全词元正确/12665 | 根正确/500 |
| --- | ---: | ---: | ---: | ---: | ---: |
| distance弱对照 | 5 | 149 | 3 | 1847 | 5 |
| 固定旧评分 | 363 | 229 | 90 | 3254 | 156 |
| 数量提示候选 | 404 | 239 | 88 | 3308 | 155 |
新评分对旧直接头45增4失，净+41；谓词端点净+10但完整路径净-2，根净-1。局部增益不保证完整语义增益；不批准直接替换。实际两次执行（第二次等价整理复算），关键指标一致，10项计数与结构控制均通过。以下完整第二次输出：
```json
{
  "sentences": 500,
  "tokens": 12665,
  "num": 654,
  "numSentences": 296,
  "gold": {
    "headPos": {
      "NOUN": 602,
      "PART": 15,
      "VERB": 16,
      "ROOT": 4,
      "NUM": 12,
      "ADJ": 3,
      "X": 1,
      "PROPN": 1
    },
    "relations": {
      "nummod": 614,
      "obl": 8,
      "root": 4,
      "parataxis": 4,
      "nsubj": 3,
      "obj": 5,
      "nmod": 2,
      "conj": 9,
      "compound": 1,
      "advcl": 1,
      "acl": 2,
      "xcomp": 1
    },
    "predicateDepth": {
      "1": 19,
      "2": 418,
      "3": 109,
      "4": 18,
      "5": 2,
      "6": 1
    },
    "noPredicate": 87,
    "root": 4,
    "headRight": 628,
    "headDistance": {
      "1": 409,
      "4+": 81,
      "2-3": 160
    },
    "classifierHeadOrChild": 427
  },
  "raw": {
    "anchors": 719,
    "exactNum": 540,
    "overlapNum": 601,
    "exactNonNum": 1,
    "unmatchedAnchors": 178
  },
  "methods": {
    "distance": {
      "headRanks": [
        4,
        418,
        515,
        608
      ],
      "predicateRanks": [
        281,
        485,
        537,
        565
      ],
      "jointRanks": [
        0,
        311,
        433,
        532
      ],
      "headCorrect": 5,
      "predicateCorrect": 149,
      "chainCorrect": 3,
      "allCorrect": 1847,
      "rootCorrect": 5,
      "validTrees": 500,
      "gains": 0,
      "losses": 358
    },
    "old": {
      "headRanks": [
        287,
        490,
        576,
        618
      ],
      "predicateRanks": [
        285,
        485,
        537,
        565
      ],
      "jointRanks": [
        147,
        369,
        484,
        542
      ],
      "headCorrect": 363,
      "predicateCorrect": 229,
      "chainCorrect": 90,
      "allCorrect": 3254,
      "rootCorrect": 156,
      "validTrees": 500,
      "gains": 0,
      "losses": 0
    },
    "typed": {
      "headRanks": [
        411,
        563,
        593,
        626
      ],
      "predicateRanks": [
        288,
        489,
        537,
        565
      ],
      "jointRanks": [
        200,
        430,
        493,
        548
      ],
      "headCorrect": 404,
      "predicateCorrect": 239,
      "chainCorrect": 88,
      "allCorrect": 3308,
      "rootCorrect": 155,
      "validTrees": 500,
      "gains": 45,
      "losses": 4
    }
  },
  "controls": 10
}
```
候选端点同时位列前5：旧484/567、新493/567；前10旧542/567、新548/567。仅候选检索上界，不能与真实路径匹配88/567混为一谈。下一责任优先为在完整原文候选词格上识别词类与多跳关系、联合约束路径证书及未知槽。考虑将旧评分保持基线，保留新评分作竞争研究；对局部评分增益引入路径退步控制。未完成与上一轮实际原生数量框架接口连接，不能宣称新的自主解析器已实现。

## 完整复算
标准Node输入raw为固定外部原始dev文本，auditReport/projectiveReport为本库固定历史报告完整文本。仅提取已审核固定自有代码，外部文本只作为数据。
```js
const c=s=>s.split("```js\n")[1].split("\n```")[0];
const verified=Function(c(auditReport).split("console.log(JSON.stringify(audit(raw)")[0]+"\nreturn audit;")()(raw);
const P=Function(c(projectiveReport).split(" const out={sentences:")[0]+"\nreturn {valid,score,decode,matrix,greedy};\n}\nreturn experiment();")();
function study(P,raw){
 const ck=(v,m)=>{if(!v)throw Error(m)},pred=new Set(["VERB","ADJ","AUX"]),nom=new Set(["NOUN","PROPN","PRON"]),clfs=new Set(["个","名","位","只","件","次","项","套","家","本","辆","张","条","台","所","种","部","人","年","月","日","天","小时","分钟","米","公里","元","岁"]);
 const out={sentences:0,tokens:0,num:0,numSentences:0,gold:{headPos:{},relations:{},predicateDepth:{},noPredicate:0,root:0,headRight:0,headDistance:{},classifierHeadOrChild:0},raw:{anchors:0,exactNum:0,overlapNum:0,exactNonNum:0,unmatchedAnchors:0},methods:{},controls:0};
 const inc=(o,k)=>o[k]=(o[k]||0)+1,modes=["distance","old","typed"],Ks=[1,3,5,10];
 for(const m of modes)out.methods[m]={headRanks:[0,0,0,0],predicateRanks:[0,0,0,0],jointRanks:[0,0,0,0],headCorrect:0,predicateCorrect:0,chainCorrect:0,allCorrect:0,rootCorrect:0,validTrees:0,gains:0,losses:0};
 function path(i,h,ts){const seen=new Set([i]),nodes=[];let p=h[i];while(p>0&&!seen.has(p)){nodes.push(p);if(pred.has(ts[p].pos))return {p,nodes,depth:nodes.length};seen.add(p);p=h[p]}return {p:null,nodes,depth:null}}
 function matrix(ts,mode){
  const old=P.matrix(ts);
  if(mode==="old")return old;
  if(mode==="distance")return old.map((row,p)=>row.map((v,i)=>!Number.isFinite(v)?v:!p?0:-2*Math.abs(i-p)));
  return old.map((row,p)=>row.map((v,i)=>{
   if(!p||!Number.isFinite(v))return v;
   if(ts[i].pos==="NUM"){if(nom.has(ts[p].pos))v+=3;if(clfs.has(ts[p].form)&&p>i)v+=3;if(p>i)v+=1;if(ts[p].pos==="NUM")v-=3}
   if(clfs.has(ts[i].form)&&["NOUN","NUM","PART"].includes(ts[i].pos)&&nom.has(ts[p].pos)&&p>i)v+=2;
   return v;
  }));
 }
 function rank(w,ts,i){return Array.from({length:ts.length},(_,j)=>j).filter(j=>j!==i).sort((a,b)=>w[b][i]-w[a][i]||Math.abs(a-i)-Math.abs(b-i)||a-b)}
 function predRank(w,ts,i,mode){
  const ids=Array.from({length:ts.length-1},(_,j)=>j+1).filter(j=>j!==i&&pred.has(ts[j].pos));
  const f=p=>{let best=w[p][i];for(let h=1;h<ts.length;h++)if(h!==i&&h!==p&&!pred.has(ts[h].pos))best=Math.max(best,w[h][i]+w[p][h]-2);return best};
  return ids.sort((a,b)=>mode==="distance"?Math.abs(a-i)-Math.abs(b-i)||a-b:f(b)-f(a)||Math.abs(a-i)-Math.abs(b-i)||a-b)
 }
 for(const block of raw.trimEnd().split(/\n\n+/)){
  const lines=block.split("\n"),txt=lines.find(x=>x.startsWith("# text = ")).slice(9);
  const ts=[null,...lines.filter(x=>!x.startsWith("#")).map(x=>x.split("\t")).filter(c=>/^[1-9]\d*$/.test(c[0])).map(c=>({id:+c[0],form:c[1],pos:c[3],head:+c[6],rel:c[7],misc:c[9]}))];
  let cursor=0;for(const t of ts.slice(1)){t.a=cursor;cursor+=[...t.form].length;t.b=cursor;if(!t.misc.split("|").includes("SpaceAfter=No"))cursor++}
  ck(ts.slice(1).map(t=>t.form+(t.misc.split("|").includes("SpaceAfter=No")?"":" ")).join("").trimEnd()===txt,"alignment");
  const gold=ts.map(t=>t?.head??-1),nums=ts.slice(1).filter(t=>t.pos==="NUM");
  ck(P.valid(gold,false),"gold tree");out.sentences++;out.tokens+=ts.length-1;out.num+=nums.length;out.numSentences+=+!!nums.length;
  const A=[];for(const m of txt.matchAll(/[0-9０-９零〇一二两俩三四五六七八九十百千万亿壹贰叁肆伍陆柒捌玖拾佰仟萬億]+(?:[.．点][0-9０-９零〇一二两三四五六七八九]+)?/gu)){let a=[...txt.slice(0,m.index)].length;A.push([a,a+[...m[0]].length])}
  out.raw.anchors+=A.length;out.raw.exactNum+=nums.filter(t=>A.some(([a,b])=>a===t.a&&b===t.b)).length;out.raw.overlapNum+=nums.filter(t=>A.some(([a,b])=>a<t.b&&b>t.a)).length;
  for(const [a,b] of A){const x=ts.slice(1).find(t=>t.a===a&&t.b===b);if(x&&x.pos!=="NUM")out.raw.exactNonNum++;if(!x)out.raw.unmatchedAnchors++}
  const computed={};
  for(const mode of modes){const w=matrix(ts,mode),d=P.decode(w);ck(d.status==="CANDIDATE"&&P.valid(d.heads,true)&&d.authority==="NONE","decode");computed[mode]={w,d};const o=out.methods[mode];o.validTrees++;o.allCorrect+=ts.slice(1).filter(t=>d.heads[t.id]===t.head).length;o.rootCorrect+=+ts.slice(1).some(t=>t.head===0&&d.heads[t.id]===0)}
  for(const t of nums){
   const i=t.id,h=t.head,g=path(i,gold,ts);inc(out.gold.headPos,h?ts[h].pos:"ROOT");inc(out.gold.relations,t.rel.split(":")[0]);if(!h)out.gold.root++;if(h>i)out.gold.headRight++;if(h)inc(out.gold.headDistance,Math.abs(h-i)<=1?"1":Math.abs(h-i)<=3?"2-3":"4+");if(g.p===null)out.gold.noPredicate++;else inc(out.gold.predicateDepth,g.depth);
   if((h&&clfs.has(ts[h].form))||ts.slice(1).some(x=>x.head===i&&clfs.has(x.form)))out.gold.classifierHeadOrChild++;
   for(const mode of modes){
    const {w,d}=computed[mode],o=out.methods[mode],p=path(i,d.heads,ts),hr=rank(w,ts,i).indexOf(h)+1,pr=g.p===null?0:predRank(w,ts,i,mode).indexOf(g.p)+1;
    ck(hr>0&&(g.p===null||pr>0),"rank");o.headCorrect+=+(d.heads[i]===h);o.predicateCorrect+=+(g.p!==null&&p.p===g.p);o.chainCorrect+=+(g.p!==null&&p.p===g.p&&JSON.stringify(p.nodes)===JSON.stringify(g.nodes));
    if(mode!=="old"){const old=computed.old.d.heads[i]===h,now=d.heads[i]===h;o.gains+=+(!old&&now);o.losses+=+(old&&!now)}
    Ks.forEach((k,j)=>{o.headRanks[j]+=+(hr<=k);o.predicateRanks[j]+=+(pr>0&&pr<=k);o.jointRanks[j]+=+(hr<=k&&pr>0&&pr<=k)})
   }
  }
 }
 for(const f of [()=>out.sentences===500,()=>out.tokens===12665,()=>out.methods.old.allCorrect===3254,()=>out.raw.exactNum<=out.raw.overlapNum&&out.raw.overlapNum<=out.num,()=>Object.values(out.gold.relations).reduce((a,b)=>a+b,0)===out.num,()=>Object.values(out.gold.predicateDepth).reduce((a,b)=>a+b,0)+out.gold.noPredicate===out.num,...modes.map(m=>()=>out.methods[m].validTrees===out.sentences&&out.methods[m].chainCorrect<=out.methods[m].predicateCorrect&&out.methods[m].jointRanks.every((x,i)=>x<=out.methods[m].headRanks[i]&&x<=out.methods[m].predicateRanks[i])),()=>out.methods.typed.headCorrect-out.methods.old.headCorrect===out.methods.typed.gains-out.methods.typed.losses]){ck(f(),"control");out.controls++}
 return out;
}
console.log(JSON.stringify(study(P,raw),null,2));
```
以上代码实际执行于连接器JS环境，Node独立包装未运行。未上传第三方原文或词表数据；仅项目自有算法及聚合统计。
## 治理
自行选定NUM标注、谓词代理、有限量词词面、启发式分数与评估指标，非正式产品规范。未训练、未修改生产、未合并PR、未部署、未主动CI、未新增费用；独立留出、真实决策对话、竞品、Mac/iPhone、原生语言及权限/计算入口未运行，保持原有冻结、验收等级、唯一交接。
