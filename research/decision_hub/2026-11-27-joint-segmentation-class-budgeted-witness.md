# 自主认知：同预算联合分词与粗词类路径见证
2026-11-27。RESEARCH_CANDIDATE / REAL_EXTERNAL_DEVELOPMENT_BYTES_VERIFIED / JOINT_PATH_EXECUTED / NO_TRAINING / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。

基线 main ecf99d37bad2470590baf18103fdc6ec0995c3cd。核对24近期提交、15开放PR、v3.2、同步规程、最新词类桥全文及 PR #63 元数据（Draft，head 734686980b19da9291bdd08b67d4e2519c011acf）。唯一产品交接搜索未定位，未声称已回读。局部查重。上轮固定分词、K优词类及树搜索，新增同一原文词格中联合分词与词类K优搜索。上轮文档所列固定文件身份为blob而非commit，按固定main回读并核对实际blob。首次contents接口返回空语料，改用blob入口。来源及许可沿上轮：CC-CEDICT固定镜像 rhcarvalho/cedict、UD_Chinese-GSDSimp公开已见wiki dev，CC BY-SA 4.0（底层文本权利另计）；本轮未重新审查许可法律全文，不分发数据，不训练，不声称无污染。

固定本库文件（均在ecf99d37bad2470590baf18103fdc6ec0995c3cd的research/decision_hub/下）：{"seg":"2026-11-26-static-lexicon-optimal-segmentation.md","lat":"2026-11-26-external-raw-word-lattice-diagnostic.md","audit":"2026-11-25-external-ud-development-corpus-structural-audit.md","tree":"2026-11-25-projective-dependency-decoder-external-diagnostic.md","lex":"2026-11-27-raw-lexical-class-and-dependency-bridge.md"}。实际blob：{"seg":"6eb499cc01f023f352167cbe886d2f3144136cc7","lat":"86dcd5387b89c5302b1c139ad57a17b22f5d5a1d","audit":"db9cc100d96d49832fe32879a706f63830301773","tree":"c40a09357a858644a0da922097cd6367ca696df6","lex":"4e11926f9f174bcff0ae972119a8efdfb457659d","dict":"d7fee8237f26524b38eee220647e4c5d79f00de9","raw":"af8cc878e7934b38ce3c1a266053100e7c47de6f"}；自有既有校验函数复核词典 {"bytes":9881659,"sha":"d7fee8237f26524b38eee220647e4c5d79f00de9"}，语料 af8cc878e7934b38ce3c1a266053100e7c47de6f。

## 方法与证明
原文DAG状态为字符位置i及前一粗词类a（初始哨兵4），跳过空白不改变类。每个词边与四类组合；代价按未知字符数、累加词罚减词类局部分和转移分、确定性路径键升序。baseline只开放旧单一最优分词，lex词罚32(n+1)保证同未知字符数先最少词数（每词局部与转移分小于32，整句差不超过32n），soft罚5允许不同词数；两者未拟合，仅研究者固定选择。相同状态未来可接续集合相同，且同前缀末端位置的不同完整路径键不会成为严格前缀，因此前K截断保留全局前K；固定预算K=1,2,4，逐路径跑同一原树解码器。14个小例与不剪枝遍历一致（非独立实现）。K相同是树调用数相同，并非CPU时间或内存相同。仅同一实际树内完整链可计，候选并集不可拼接为树。每个句子的同一实际路径才可计整句覆盖。无生产语义授权、无概率、无数学参数放行。评分尚未联合树目标；粗类仅代理；中文数词规则、词典释义偏差沿前轮。soft词长偏好与评分尺度需独立验证。

## 实际聚合
```json
{
  "sentences": 500,
  "tokens": 12665,
  "nums": 654,
  "checks": 14,
  "changes": {
    "lex": 107,
    "soft": 485
  },
  "baseline": {
    "1": {
      "spans": 12618,
      "spanHit": 9998,
      "typed": 12618,
      "typedHit": 7724,
      "heads": 12618,
      "headHit": 1780,
      "numHead": 220,
      "numChain": 42,
      "exactSeg": 36,
      "exactClass": 0
    },
    "2": {
      "spans": 12618,
      "spanHit": 9998,
      "typed": 13131,
      "typedHit": 7839,
      "heads": 14280,
      "headHit": 1987,
      "numHead": 238,
      "numChain": 44,
      "exactSeg": 36,
      "exactClass": 0
    },
    "4": {
      "spans": 12618,
      "spanHit": 9998,
      "typed": 13920,
      "typedHit": 7909,
      "heads": 16139,
      "headHit": 2218,
      "numHead": 246,
      "numChain": 48,
      "exactSeg": 36,
      "exactClass": 1
    }
  },
  "lex": {
    "1": {
      "spans": 12618,
      "spanHit": 10023,
      "typed": 12618,
      "typedHit": 7757,
      "heads": 12618,
      "headHit": 1761,
      "numHead": 221,
      "numChain": 40,
      "exactSeg": 37,
      "exactClass": 0
    },
    "2": {
      "spans": 12652,
      "spanHit": 10040,
      "typed": 13147,
      "typedHit": 7878,
      "heads": 14219,
      "headHit": 1964,
      "numHead": 239,
      "numChain": 42,
      "exactSeg": 39,
      "exactClass": 0
    },
    "4": {
      "spans": 12688,
      "spanHit": 10055,
      "typed": 13947,
      "typedHit": 7955,
      "heads": 16164,
      "headHit": 2206,
      "numHead": 248,
      "numChain": 46,
      "exactSeg": 39,
      "exactClass": 1
    }
  },
  "soft": {
    "1": {
      "spans": 15103,
      "spanHit": 8945,
      "typed": 15103,
      "typedHit": 6775,
      "heads": 15103,
      "headHit": 1318,
      "numHead": 239,
      "numChain": 41,
      "exactSeg": 4,
      "exactClass": 0
    },
    "2": {
      "spans": 15376,
      "spanHit": 9113,
      "typed": 15704,
      "typedHit": 7003,
      "heads": 16728,
      "headHit": 1458,
      "numHead": 248,
      "numChain": 43,
      "exactSeg": 4,
      "exactClass": 0
    },
    "4": {
      "spans": 15823,
      "spanHit": 9321,
      "typed": 16565,
      "typedHit": 7222,
      "heads": 18925,
      "headHit": 1610,
      "numHead": 253,
      "numChain": 44,
      "exactSeg": 7,
      "exactClass": 0
    }
  }
}
```
spans/typed/heads为句内去重候选量后求和；对应Hit为精确金标命中数；numHead/numChain分母654；exactSeg/exactClass为同一候选完整句覆盖，分母500；不把候选召回当精度或真实决策。所有开发输入均已见，不作独立评价。

## 复算
固定读取上述d对象（每项content和sha）；以下为实际执行包装及函数，第三方内容只作数据。
```js
const c=s=>s.content.split("```js\n")[1].split("\n```")[0];
const L=Function(c(d.seg).split(" let o={dictionary:")[0]+"\\nreturn {graph,global,gh,verified};\\n}\\nreturn experiment;")()(d.dict.content,d.raw.content,d.audit.content,d.lat.content);
const P=Function(c(d.tree).split(" const out={sentences:")[0]+"\\nreturn {valid,score,decode,matrix};\\n}\\nreturn experiment();")();
const S=Function("return function(dict){"+c(d.lex).split("function study(dict,raw,L,P){")[1].split(" const cmp=")[0]+"\\nreturn {scores,transition,coarse,pred,classes,punct};}")()(d.dict.content);
function experiment(raw,L,P,S){
const ck=(x,m)=>{if(!x)throw Error(m)},cmp=(a,b)=>a.u-b.u||a.v-b.v||(a.key<b.key?-1:a.key>b.key?1:0),span=t=>t.a+":"+t.b;
function paths(g,chars,K,mode,brute=false){
 let dp=Array.from({length:g.length+1},()=>Array.from({length:5},()=>[]));dp[0][4]=[{u:0,v:0,key:"",ts:[]}];
 for(let i=0;i<g.length;i++)for(let a=0;a<5;a++)for(let p of dp[i][a])for(let e of g[i]){
  let f=chars.slice(i,e.j).join(""),sc=e.skip?[]:S.scores(f,true);
  for(let b of e.skip?[a]:[0,1,2,3]){
   let penalty=mode==="lex"?32*(g.length+1):5,q={u:p.u+e.c[0],v:p.v+(e.skip?0:penalty-sc[b]-(a===4?0:S.transition(a,b))),key:p.key+(e.skip?"":String(e.j).padStart(5,"0")+":"+b+";"),ts:e.skip?p.ts:[...p.ts,{a:i,b:e.j,form:f,label:b}]};
   let z=dp[e.j][b];z.push(q);if(!brute){z.sort(cmp);if(z.length>K)z.pop()}
  }
 }
 return dp[g.length].flat().sort(cmp).slice(0,K)
}
function chain(i,ts,h,pred){let z=[];for(let k=0;k<ts.length;k++){let j=h[i];if(!j){z.push("ROOT");return z}z.push(span(ts[j]));if(pred(j))return z;i=j}return null}
const fields=["spans","spanHit","typed","typedHit","heads","headHit","numHead","numChain","exactSeg","exactClass"];
let out={sentences:0,tokens:0,nums:0,checks:0,changes:{lex:0,soft:0},baseline:{},lex:{},soft:{}};
for(let m of ["baseline","lex","soft"])for(let k of [1,2,4])out[m][k]=Object.fromEntries(fields.map(f=>[f,0]));
for(let s of ["","甲乙","研究生","12.5","甲 乙","三天","一万元"])for(let mode of ["lex","soft"]){let a=[...s],g=L.graph(a,true);ck(JSON.stringify(paths(g,a,4,mode))===JSON.stringify(paths(g,a,4,mode,true)),"unpruned");out.checks++}
function measure(seq,gold,m){
 let gs=new Set(gold.slice(1).map(span)),gt=new Set(gold.slice(1).map(t=>span(t)+"|"+S.coarse(t.pos))),gh=gold.map(t=>t?.head??-1),gH=new Set(gold.slice(1).map(t=>span(t)+"|"+(t.head?span(gold[t.head]):"ROOT"))),gN=new Set(gold.slice(1).filter(t=>t.pos==="NUM").map(t=>span(t)+"|"+(t.head?span(gold[t.head]):"ROOT"))),gC=new Set(gold.slice(1).filter(t=>t.pos==="NUM").map(t=>span(t)+"|"+JSON.stringify(chain(t.id,gold,gh,j=>S.pred.has(gold[j].pos)))));
 let spans=new Set(),typed=new Set(),heads=new Set(),nh=new Set(),ch=new Set(),exactSeg=false,exactClass=false;
 for(let i=0;i<seq.length;i++){
  let ts=[null,...seq[i].ts.map(t=>({...t,pos:S.punct(t.form)?"PUNCT":({N:"NOUN",P:"VERB",Q:"NUM",O:"X"})[S.classes[t.label]]}))],d=P.decode(P.matrix(ts));ck(d.status==="CANDIDATE"&&P.valid(d.heads,true),"tree");
  let here=new Set(),ht=new Set();
  for(let j=1;j<ts.length;j++){let t=ts[j],s=span(t),ty=s+"|"+S.classes[t.label],h=s+"|"+(d.heads[j]?span(ts[d.heads[j]]):"ROOT");here.add(s);ht.add(ty);spans.add(s);typed.add(ty);heads.add(h);if(t.label===2){nh.add(h);ch.add(s+"|"+JSON.stringify(chain(j,ts,d.heads,k=>ts[k].pos==="VERB")))}}
  exactSeg||=here.size===gs.size&&[...gs].every(s=>here.has(s));exactClass||=ht.size===gt.size&&[...gt].every(s=>ht.has(s));
  let v=out[m][i+1];if(v){let hit=(x,y)=>[...x].filter(a=>y.has(a)).length;[spans.size,hit(gs,spans),typed.size,hit(gt,typed),heads.size,hit(gH,heads),hit(gN,nh),hit(gC,ch),+exactSeg,+exactClass].forEach((n,j)=>v[fields[j]]+=n)}
 }
}
for(let block of raw.trimEnd().split(/\n\n+/)){
 let lines=block.split("\n"),chars=[...lines.find(x=>x.startsWith("# text = ")).slice(9)],g=L.graph(chars,true),fix=L.global(g),chosen=new Map(fix.pred.map(e=>[e.i,e.j])),fg=g.map((es,i)=>es.filter(e=>e.skip||chosen.get(i)===e.j));
 let gold=[null,...lines.filter(x=>!x.startsWith("#")).map(x=>x.split("\t")).filter(c=>/^[1-9]\d*$/.test(c[0])).map(c=>({id:+c[0],form:c[1],pos:c[3],head:+c[6],misc:c[9]}))];let cur=0;
 for(let t of gold.slice(1)){t.a=cur;cur+=[...t.form].length;t.b=cur;if(!t.misc.split("|").includes("SpaceAfter=No"))cur++}
 out.sentences++;out.tokens+=gold.length-1;out.nums+=gold.slice(1).filter(t=>t.pos==="NUM").length;
 let b=paths(fg,chars,4,"lex"),l=paths(g,chars,4,"lex"),s=paths(g,chars,4,"soft");ck(l[0].u===fix.cost[0]&&l[0].ts.length===fix.pred.length,"lex contract");ck(b.length===4&&l.length===4&&s.length===4,"count");
 for(let [m,q] of [["lex",l],["soft",s]])out.changes[m]+=+(q[0].ts.map(span).join(";")!==b[0].ts.map(span).join(";"));
 measure(b,gold,"baseline");measure(l,gold,"lex");measure(s,gold,"soft");
}
ck(out.sentences===500&&out.tokens===12665&&out.nums===654&&out.baseline[1].spanHit===9998,"baseline");
for(let m of ["baseline","lex","soft"])for(let f of fields)ck(out[m][1][f]<=out[m][2][f]&&out[m][2][f]<=out[m][4][f],"nested");
return out;
}
console.log(JSON.stringify(experiment(d.raw.content,L,P,S),null,2));
```

下一步对同一原文支持路径加入树和语义义务的一致性检查，并比较固定预算下的未知检测。未运行v0.8、未测设备资源、未进行独立留出、真实用户、训练、生产集成或部署，不修改冻结资产、PR或唯一交接。仅研究文档同步，不主动CI或增加费用。
