# 自主认知：原文段级依存候选排序及等预算诊断
2026-11-26。RESEARCH_CANDIDATE / RAW_TEXT_CANDIDATE_RANKING / REAL_EXTERNAL_DEVELOPMENT_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线及查重
起点main 78f439807e95df532a109228302a1c26bb5d73ff；实际核对25近期提交、15开放PR、#63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍draft、v3.2及同步规程、历史交接固定blob 5e74f4f0b37141d631740e844ad8bbbfed232e07前段，最新交接路径未定位。读取前序 research/decision_hub/2026-11-26-external-dependency-cross-punctuation-scope-diagnostic.md blob 0633533cebfb0cdea6aecff4e422bd3d4cdb5188、引述框架14e280d83441155ac2dfcba44a20d8393fac1321、全句分词见证4d23fdf2dbabd9a2cf92c794f19d218e13a4fb7c、联合词端点及距离/松弛排名3acea2859fa8095061cd2efb6f8918282803ab75。既有金标分词/UPOS解码和词格端点排名不重复计。本轮新增原始标点段对的方向、长度、字符二元组及有限功能关系提示的等预算排序与真实依存边评价，不以金标分词、词性、依存、正确端点作为生成输入。4项关键词检索无返回，非全库查重。
## 数据
同一已见UD_Chinese-GSDSimp dev 500句，commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3，blob af8cc878e7934b38ce3c1a266053100e7c47de6f；实际完整读取连接器文本并复用前序align及segments。许可沿用已核对固定LICENSE CC BY-SA 4.0、README记录；本轮未重审许可或独立复算原始Git字节。来源 https://github.com/UniversalDependencies/UD_Chinese-GSDSimp/tree/b79a1c2f7ba7f9b264808d91c6886a67b7f847a3 ，许可 https://creativecommons.org/licenses/by-sa/4.0/ 。只保存聚合统计及自有代码，不复制原始语料或标注，不读train/test。非独立留出、真人决策对话或训练。
## 方法
从原始文本以既有标点切分非空段，枚举所有不同段的有向依存候选(d,h)。仅用原文生成五种固定排序：距离、距离加轻微向右优先、距离加相对头段长度、距离加相邻字符二元组Jaccard、综合长度/方向/相似度/强分隔惩罚/条件与转述提示。有限提示及所有权重在本轮执行前人工选定，非学习、概率、语法证明或产品政策。每段取K=1/2/3/5个不同头段，每种排序使用严格相同候选数，平分按head索引稳定处理。无分词、POS、金标、句法树或跨轮输入，不能把段对视为独立依存弧、唯一树、语义或事实；同一段可包含多个头部/子部，禁止强制单根。生成全部候选后排序，候选预算不是实际CPU/内存上限。
在候选生成后用前序align从gold词端点映射到段；同段排除、不可映射单列。评价跨段依存弧覆盖、九类相关句法代理覆盖、唯一有向段对覆盖、全覆盖句子数；同一段对可能承载多弧，保留计数区别。每个方法相对距离按同一gold弧记录增益/损失，不选择最佳策略或调参。五项专项控制及等预算/嵌套/配对恒等式。全部标准JS实际两次一致。候选未覆盖不表示语言关系不成立，分数不作置信度，输出无授权。研究者自行选择提示、分数、预算与标签；既有开发集已见，不能推断真实泛化、认知负担或设备性能。
```json
{
  "sentences": 500,
  "aligned": 500,
  "unaligned": 0,
  "segments": 1489,
  "crossArcs": 1404,
  "crossScope": 927,
  "uniqueGoldPairs": 1070,
  "possiblePairs": 4490,
  "crossSentences": 408,
  "methods": {
    "distance": {
      "1": {
        "pairs": 1398,
        "arcs": 570,
        "scopeArcs": 372,
        "unique": 436,
        "sentencesFull": 166
      },
      "2": {
        "pairs": 2532,
        "arcs": 1040,
        "scopeArcs": 671,
        "unique": 784,
        "sentencesFull": 301
      },
      "3": {
        "pairs": 3249,
        "arcs": 1212,
        "scopeArcs": 792,
        "unique": 916,
        "sentencesFull": 350
      },
      "5": {
        "pairs": 4013,
        "arcs": 1365,
        "scopeArcs": 896,
        "unique": 1035,
        "sentencesFull": 395
      }
    },
    "direction": {
      "1": {
        "pairs": 1398,
        "arcs": 686,
        "scopeArcs": 403,
        "unique": 503,
        "sentencesFull": 171
      },
      "2": {
        "pairs": 2532,
        "arcs": 1040,
        "scopeArcs": 671,
        "unique": 784,
        "sentencesFull": 301
      },
      "3": {
        "pairs": 3249,
        "arcs": 1208,
        "scopeArcs": 781,
        "unique": 917,
        "sentencesFull": 354
      },
      "5": {
        "pairs": 4013,
        "arcs": 1363,
        "scopeArcs": 893,
        "unique": 1033,
        "sentencesFull": 396
      }
    },
    "length": {
      "1": {
        "pairs": 1398,
        "arcs": 631,
        "scopeArcs": 393,
        "unique": 479,
        "sentencesFull": 171
      },
      "2": {
        "pairs": 2532,
        "arcs": 1045,
        "scopeArcs": 676,
        "unique": 787,
        "sentencesFull": 301
      },
      "3": {
        "pairs": 3249,
        "arcs": 1214,
        "scopeArcs": 790,
        "unique": 918,
        "sentencesFull": 355
      },
      "5": {
        "pairs": 4013,
        "arcs": 1367,
        "scopeArcs": 897,
        "unique": 1036,
        "sentencesFull": 396
      }
    },
    "lexical": {
      "1": {
        "pairs": 1398,
        "arcs": 586,
        "scopeArcs": 376,
        "unique": 445,
        "sentencesFull": 168
      },
      "2": {
        "pairs": 2532,
        "arcs": 1040,
        "scopeArcs": 671,
        "unique": 784,
        "sentencesFull": 301
      },
      "3": {
        "pairs": 3249,
        "arcs": 1210,
        "scopeArcs": 789,
        "unique": 917,
        "sentencesFull": 351
      },
      "5": {
        "pairs": 4013,
        "arcs": 1366,
        "scopeArcs": 896,
        "unique": 1036,
        "sentencesFull": 396
      }
    },
    "structural": {
      "1": {
        "pairs": 1398,
        "arcs": 655,
        "scopeArcs": 398,
        "unique": 498,
        "sentencesFull": 174
      },
      "2": {
        "pairs": 2532,
        "arcs": 1053,
        "scopeArcs": 679,
        "unique": 793,
        "sentencesFull": 302
      },
      "3": {
        "pairs": 3249,
        "arcs": 1217,
        "scopeArcs": 791,
        "unique": 920,
        "sentencesFull": 354
      },
      "5": {
        "pairs": 4013,
        "arcs": 1363,
        "scopeArcs": 893,
        "unique": 1034,
        "sentencesFull": 395
      }
    }
  },
  "paired": {
    "distance": {
      "1": {
        "gain": 0,
        "loss": 0
      },
      "2": {
        "gain": 0,
        "loss": 0
      },
      "3": {
        "gain": 0,
        "loss": 0
      },
      "5": {
        "gain": 0,
        "loss": 0
      }
    },
    "direction": {
      "1": {
        "gain": 285,
        "loss": 169
      },
      "2": {
        "gain": 0,
        "loss": 0
      },
      "3": {
        "gain": 33,
        "loss": 37
      },
      "5": {
        "gain": 3,
        "loss": 5
      }
    },
    "length": {
      "1": {
        "gain": 135,
        "loss": 74
      },
      "2": {
        "gain": 14,
        "loss": 9
      },
      "3": {
        "gain": 18,
        "loss": 16
      },
      "5": {
        "gain": 4,
        "loss": 2
      }
    },
    "lexical": {
      "1": {
        "gain": 52,
        "loss": 36
      },
      "2": {
        "gain": 0,
        "loss": 0
      },
      "3": {
        "gain": 6,
        "loss": 8
      },
      "5": {
        "gain": 1,
        "loss": 0
      }
    },
    "structural": {
      "1": {
        "gain": 203,
        "loss": 118
      },
      "2": {
        "gain": 24,
        "loss": 11
      },
      "3": {
        "gain": 27,
        "loss": 22
      },
      "5": {
        "gain": 5,
        "loss": 7
      }
    }
  },
  "controls": 5,
  "unmapped": 17,
  "byRelation": {
    "distance": {
      "csubj": {
        "n": 32,
        "k1": 9,
        "k3": 27
      },
      "advcl": {
        "n": 284,
        "k1": 69,
        "k3": 239
      },
      "parataxis": {
        "n": 224,
        "k1": 108,
        "k3": 188
      },
      "xcomp": {
        "n": 34,
        "k1": 17,
        "k3": 29
      },
      "conj": {
        "n": 196,
        "k1": 112,
        "k3": 172
      },
      "ccomp": {
        "n": 71,
        "k1": 35,
        "k3": 67
      },
      "acl": {
        "n": 50,
        "k1": 13,
        "k3": 39
      },
      "mark": {
        "n": 35,
        "k1": 9,
        "k3": 31
      },
      "cc": {
        "n": 1,
        "k1": 0,
        "k3": 0
      }
    },
    "direction": {
      "csubj": {
        "n": 32,
        "k1": 25,
        "k3": 29
      },
      "advcl": {
        "n": 284,
        "k1": 194,
        "k3": 254
      },
      "parataxis": {
        "n": 224,
        "k1": 65,
        "k3": 175
      },
      "xcomp": {
        "n": 34,
        "k1": 20,
        "k3": 30
      },
      "conj": {
        "n": 196,
        "k1": 23,
        "k3": 153
      },
      "ccomp": {
        "n": 71,
        "k1": 36,
        "k3": 66
      },
      "acl": {
        "n": 50,
        "k1": 23,
        "k3": 43
      },
      "mark": {
        "n": 35,
        "k1": 17,
        "k3": 30
      },
      "cc": {
        "n": 1,
        "k1": 0,
        "k3": 1
      }
    },
    "length": {
      "csubj": {
        "n": 32,
        "k1": 16,
        "k3": 28
      },
      "advcl": {
        "n": 284,
        "k1": 122,
        "k3": 246
      },
      "parataxis": {
        "n": 224,
        "k1": 96,
        "k3": 183
      },
      "xcomp": {
        "n": 34,
        "k1": 19,
        "k3": 29
      },
      "conj": {
        "n": 196,
        "k1": 77,
        "k3": 164
      },
      "ccomp": {
        "n": 71,
        "k1": 37,
        "k3": 67
      },
      "acl": {
        "n": 50,
        "k1": 18,
        "k3": 42
      },
      "mark": {
        "n": 35,
        "k1": 8,
        "k3": 30
      },
      "cc": {
        "n": 1,
        "k1": 0,
        "k3": 1
      }
    },
    "lexical": {
      "csubj": {
        "n": 32,
        "k1": 14,
        "k3": 27
      },
      "advcl": {
        "n": 284,
        "k1": 91,
        "k3": 243
      },
      "parataxis": {
        "n": 224,
        "k1": 92,
        "k3": 185
      },
      "xcomp": {
        "n": 34,
        "k1": 16,
        "k3": 29
      },
      "conj": {
        "n": 196,
        "k1": 100,
        "k3": 169
      },
      "ccomp": {
        "n": 71,
        "k1": 35,
        "k3": 67
      },
      "acl": {
        "n": 50,
        "k1": 15,
        "k3": 39
      },
      "mark": {
        "n": 35,
        "k1": 13,
        "k3": 30
      },
      "cc": {
        "n": 1,
        "k1": 0,
        "k3": 0
      }
    },
    "structural": {
      "csubj": {
        "n": 32,
        "k1": 22,
        "k3": 28
      },
      "advcl": {
        "n": 284,
        "k1": 153,
        "k3": 250
      },
      "parataxis": {
        "n": 224,
        "k1": 86,
        "k3": 180
      },
      "xcomp": {
        "n": 34,
        "k1": 19,
        "k3": 29
      },
      "conj": {
        "n": 196,
        "k1": 53,
        "k3": 162
      },
      "ccomp": {
        "n": 71,
        "k1": 35,
        "k3": 67
      },
      "acl": {
        "n": 50,
        "k1": 19,
        "k3": 43
      },
      "mark": {
        "n": 35,
        "k1": 11,
        "k3": 31
      },
      "cc": {
        "n": 1,
        "k1": 0,
        "k3": 1
      }
    }
  },
  "top1DistinctPrecisionNumerator": {
    "distance": 436,
    "direction": 503,
    "length": 479,
    "lexical": 445,
    "structural": 498
  }
}
```
## 复算及边界
固定外部dev.conllu及前序报告按顺序传入，Node文件包装未执行，标准JS核心实际运行。仅加载已审阅固定自有源码。未修改生产、冻结、交接、证据等级、PR、训练、部署、主动CI或费用；独立留出、实际原生、真机均未执行。
```js
const [data,previous]=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8"));
const code=previous.split("\`\`\`js\n")[1].split("\n\`\`\`")[0],make=Function(code.split(" const stat=()=>")[0]+"\nreturn {align,segments};\n}\nreturn study('');");
function experiment(data,make){
 const R=make(),ck=(v,m)=>{if(!v)throw Error(m)},delim=new Set(Array.from("，,、：:；;。！？!?")),scope=new Set(["advcl","ccomp","xcomp","parataxis","conj","csubj","acl","mark","cc"]);
 const modes=["distance","direction","length","lexical","structural"],ks=[1,2,3,5],cue=["如果","若","只要","只有","除非","因为","虽然","即使","尽管","由于","假如","倘若"],continuation=["所以","因此","但是","然而","于是","那么","则","就","才","否则","仍然"],report=["表示","认为","指出","称","说","问","回答"],quotes=new Set(Array.from("“”‘’「」『』\""));
 function parts(text){
  let chars=Array.from(text),z=R.segments(chars,delim),s=Array.from({length:z.count},()=>({text:"",start:null,end:null}));for(let i=0;i<chars.length;i++){let j=z.index[i];if(j<0)continue;let v=s[j];v.text+=chars[i];v.start??=i;v.end=i+1}
  for(let i=0;i<s.length;i++){let v=s[i];v.before=i?chars.slice(s[i-1].end,v.start).join(""):"";v.after=i+1<s.length?chars.slice(v.end,s[i+1].start).join(""):"";v.len=Array.from(v.text).length;v.conditional=cue.some(w=>v.text.startsWith(w));v.cont=continuation.some(w=>v.text.startsWith(w));v.report=report.some(w=>v.text.endsWith(w));v.quote=Array.from(v.text).some(c=>quotes.has(c));v.bg=new Set(Array.from({length:Math.max(0,v.len-1)},(_,k)=>Array.from(v.text).slice(k,k+2).join("")).filter(w=>/[\p{L}\p{N}]/u.test(w)))}
  return {...z,chars,s};
 }
 function score(s,d,h,mode){
  let a=s[d],b=s[h],dist=Math.abs(d-h),right=h>d,base=-dist;
  if(mode==="distance")return base;
  if(mode==="direction")return base+(right?.25:0);
  if(mode==="length")return base+.5*Math.min(2,Math.log2((b.len+1)/(a.len+1)));
  let inter=[...a.bg].filter(x=>b.bg.has(x)).length,union=new Set([...a.bg,...b.bg]).size,sim=union?inter/union:0;
  if(mode==="lexical")return base+3*sim;
  // Small frozen, human-selected language-neutral/functional cues, no fitting.
  let barrier=0;for(let i=Math.min(d,h);i<Math.max(d,h);i++)if(/[；;。！？!?]/u.test(s[i].after))barrier++;
  let f=base+.25*(right?1:0)+.5*Math.min(2,Math.log2((b.len+1)/(a.len+1)))+3*sim-1.5*barrier;
  if(a.conditional&&right)f+=1.5;
  if(a.cont&&!right)f+=1;
  if(a.conditional&&b.cont&&right)f+=1;
  if(a.quote&&b.report&&!right)f+=2;
  if(b.report&&!right&&b.after.includes("："))f+=1;
  return f;
 }
 function ranked(z,mode){return z.s.map((_,d)=>z.s.map((_,h)=>({d,h,v:h===d?-Infinity:score(z.s,d,h,mode)})).filter(x=>x.h!==d).sort((a,b)=>b.v-a.v||a.h-b.h))}
 const counts=()=>({pairs:0,arcs:0,scopeArcs:0,unique:0,sentencesFull:0}),out={sentences:0,aligned:0,unaligned:0,segments:0,crossArcs:0,crossScope:0,uniqueGoldPairs:0,possiblePairs:0,crossSentences:0,methods:{},paired:{},controls:0,unmapped:0,byRelation:{},top1DistinctPrecisionNumerator:{}};
 for(let m of modes){out.methods[m]=Object.fromEntries(ks.map(k=>[k,counts()]));out.paired[m]=Object.fromEntries(ks.map(k=>[k,{gain:0,loss:0} ]));out.top1DistinctPrecisionNumerator[m]=0;out.byRelation[m]={}}
 for(let chunk of data.trim().split(/\n\s*\n/)){
  const lines=chunk.split(/\r?\n/),raw=lines.find(x=>x.startsWith("# text = "))?.slice(9);if(raw===undefined)continue;out.sentences++;
  const z=parts(raw),all=Object.fromEntries(modes.map(m=>[m,ranked(z,m)])); // all candidates generated before reading annotations
  const rows=lines.filter(x=>/^\d+\t/.test(x)).map(x=>x.split("\t")),align=R.align(raw,rows);
  if(!align){out.unaligned++;continue}out.aligned++;out.segments+=z.count;out.possiblePairs+=z.count*(z.count-1);
  function seg(p){let [a,b]=align.positions.get(p),v=[...new Set(z.index.slice(a,b).filter(i=>i>=0))];return v.length===1?v[0]:null}
  let arcs=[];
  for(let r of rows){let h=+r[6],d=+r[0],rel=r[7].split(":")[0];if(!h||rel==="punct"||r[3]==="PUNCT")continue;let i=seg(d),j=seg(h);if(i===null||j===null){out.unmapped++;continue}if(i!==j)arcs.push({i,j,rel,key:i+":"+j})}
  out.crossArcs+=arcs.length;out.crossScope+=arcs.filter(a=>scope.has(a.rel)).length;const gold=new Set(arcs.map(a=>a.key));out.uniqueGoldPairs+=gold.size;out.crossSentences+=+!!arcs.length;
  const selected={};
  for(let m of modes){
   selected[m]={};for(let k of ks){
    let set=new Set(all[m].flatMap(row=>row.slice(0,k).map(v=>v.d+":"+v.h)));selected[m][k]=set;
    ck(set.size===z.count*Math.min(k,Math.max(0,z.count-1)),"equal budget");
    let o=out.methods[m][k];o.pairs+=set.size;o.arcs+=arcs.filter(a=>set.has(a.key)).length;o.scopeArcs+=arcs.filter(a=>scope.has(a.rel)&&set.has(a.key)).length;o.unique+=[...gold].filter(k=>set.has(k)).length;o.sentencesFull+=+(arcs.length>0&&arcs.every(a=>set.has(a.key)));
   }
   out.top1DistinctPrecisionNumerator[m]+=[...gold].filter(k=>selected[m][1].has(k)).length;
   for(let a of arcs.filter(a=>scope.has(a.rel))){let v=out.byRelation[m][a.rel]??={n:0,k1:0,k3:0};v.n++;v.k1+=+selected[m][1].has(a.key);v.k3+=+selected[m][3].has(a.key)}
  }
  for(let m of modes)for(let k of ks)for(let a of arcs){let p=selected[m][k].has(a.key),b=selected.distance[k].has(a.key);out.paired[m][k].gain+=+(p&&!b);out.paired[m][k].loss+=+(!p&&b)}
 }
 for(let m of modes)for(let k of ks){let a=out.methods[m][k],b=out.methods.distance[k],p=out.paired[m][k];ck(a.pairs===b.pairs&&a.arcs-b.arcs===p.gain-p.loss,"paired totals")}
 for(let m of modes)for(let i=1;i<ks.length;i++)ck(out.methods[m][ks[i]].arcs>=out.methods[m][ks[i-1]].arcs,"nested");
 const ctl=(v,m)=>{ck(v,m);out.controls++};let z=parts("如果甲，乙；所以丙。");ctl(z.count===3&&z.s[0].conditional&&z.s[2].cont,"functional cues");
 ctl(ranked(parts("甲，乙，丙"),"distance")[1][0].h===0,"tie");
 ctl(ranked(parts("甲，乙，丙"),"direction")[1][0].h===2,"direction");
 ctl(ranked(parts("甲"),"structural")[0].length===0,"one segment");
 ctl(out.aligned===500&&out.crossArcs===1404&&out.crossScope===927&&out.unmapped===17,"prior accounting");
 return out;
}
console.log(JSON.stringify(experiment(data,make),null,2));
```
