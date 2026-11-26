# 自主认知：外部中文依存开发集的跨标点关系与作用域候选预算
2026-11-26。RESEARCH_CANDIDATE / REAL_EXTERNAL_DEVELOPMENT_DATA_EXECUTED / GOLD_ENDPOINT_DIAGNOSTIC / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线
起点main 8d32d5680b0389fc91e820833798466c6c726e36，沿用本轮已核对的v3.2、同步规程、25近期提交、15开放PR、历史交接固定blob（最新路径未定位），#63固定head 734686980b19da9291bdd08b67d4e2519c011acf。既有词格全路径与依存边端点研究已使用同一UD开发集，不将该500句重复算为新的独立语料；本轮新增仅由原始标点生成的段级有向配对范围诊断，重点检查跨标点的从句、并列、引述相关句法关系，区别于前序词边界可达性或依存树推断。已有原文跨句主体、条件与引语研究，本轮不重新调规则。非全库查重。
## 来源、许可与读取范围
Universal Dependencies / UD_Chinese-GSDSimp，固定commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3，zh_gsdsimp-ud-dev.conllu blob af8cc878e7934b38ce3c1a266053100e7c47de6f。实际从连接器读取完整blob文本1035788 JS字符，未独立计算Git原始字节SHA或字节数。实际核对同commit LICENSE.txt blob 9af2e0b2f73cf29fe1f60cb6376b176d9c2ba846，CC BY-SA 4.0；README.md前20行blob 5cb7d4a8446b4a167915225483aa94d187f23798，简体版本由传统GSD转换并人工纠正。来源链接 https://github.com/UniversalDependencies/UD_Chinese-GSDSimp/tree/b79a1c2f7ba7f9b264808d91c6886a67b7f847a3 ，许可 https://creativecommons.org/licenses/by-sa/4.0/ 。不复制原文、标注或训练资料，仅保存聚合计数、原始算法及未对齐句ID；第三方原始权利及再分发另审。固定开发集已见于项目，非独立留出、真实个人决策数据或授权训练。
## 方法
从CoNLL-U的# text仅按原始逗号/顿号/冒号/分号/句末标点生成非空连续段，空白跳过；不依据金标词性、依存、head或标签生成段。考虑同段和距离至多k（0、1、2、3、全范围）的有向段对（含自对），计候选段对数量。原始词表仅在评价时逐字对齐到# text，不可对齐整句显式跳过，不暗中用gold替代原文。金标head与dependent跨度均唯一落入一个非标点段时，用段距检查相应有向段对是否在候选域；跨多个段或无归属记unmapped。计所有非punct且非root的依存边，另对advcl/ccomp/xcomp/parataxis/conj/csubj/acl/mark/cc九个基类及各标签分别报告；标签选择由研究者预设，仅为与从句连接、并列、标记相关的句法代理，不等同条件、引述、主体归属、真实语义作用域或科学决策。另统计按强标点单独分段的跨段边。段对被覆盖只说明保留了搜索范围，不证明词边界、关系类型、方向、语义真值或方法选择正确。对全范围的所有可映射边理论上必覆盖，不视为模型能力；段对数量只是候选空间代理，不能换算实际墙时/内存。没有自动选择正确关系，无跨文档/多轮标注，无真实自然语言解析。全部研究输出authority NONE。
## 实际结果
完整开发集标准JS实际执行两次一致，五项专项控制和各标签聚合恒等式控制。全部候选由原文标点生成，金标仅对齐和评分；未训练或调参。记录完整边/句/段对计数和未映射结果，避免按句法边覆盖宣称语义准确率。未运行原生平台、独立留出、真实用户或真机。研究者选择标点集合、九标签及候选半径；这些不是正式产品策略。
```json
{
  "sentences": 500,
  "aligned": 500,
  "unaligned": 0,
  "tokens": 12665,
  "nonPunctArcs": 10395,
  "scopeArcs": 2618,
  "sentencesWithScope": 466,
  "sentencesWithCrossScope": 375,
  "sentencesWithHardCrossScope": 0,
  "segments": 1489,
  "pairs": {
    "0": 1489,
    "1": 3467,
    "2": 4627,
    "3": 5233,
    "Infinity": 5979
  },
  "allArcs": {
    "arcs": 10395,
    "unmapped": 17,
    "cross": 1404,
    "hardCross": 0,
    "dist": {
      "0": 8974,
      "1": 855,
      "2": 324,
      "3": 117,
      "4": 58,
      "5": 35,
      "6": 8,
      "7": 4,
      "9": 1,
      "10": 1,
      "11": 1
    },
    "hits": {
      "0": 8974,
      "1": 9829,
      "2": 10153,
      "3": 10270,
      "Infinity": 10378
    }
  },
  "scope": {
    "arcs": 2618,
    "unmapped": 2,
    "cross": 927,
    "hardCross": 0,
    "dist": {
      "0": 1689,
      "1": 553,
      "2": 225,
      "3": 78,
      "4": 35,
      "5": 22,
      "6": 7,
      "7": 4,
      "9": 1,
      "10": 1,
      "11": 1
    },
    "hits": {
      "0": 1689,
      "1": 2242,
      "2": 2467,
      "3": 2545,
      "Infinity": 2616
    }
  },
  "byRelation": {
    "acl": {
      "arcs": 267,
      "unmapped": 0,
      "cross": 50,
      "hardCross": 0,
      "dist": {
        "0": 217,
        "1": 25,
        "2": 15,
        "3": 5,
        "4": 2,
        "5": 3
      },
      "hits": {
        "0": 217,
        "1": 242,
        "2": 257,
        "3": 262,
        "Infinity": 267
      }
    },
    "mark": {
      "arcs": 748,
      "unmapped": 0,
      "cross": 35,
      "hardCross": 0,
      "dist": {
        "0": 713,
        "1": 20,
        "2": 11,
        "3": 1,
        "4": 1,
        "5": 1,
        "6": 1
      },
      "hits": {
        "0": 713,
        "1": 733,
        "2": 744,
        "3": 745,
        "Infinity": 748
      }
    },
    "csubj": {
      "arcs": 47,
      "unmapped": 0,
      "cross": 32,
      "hardCross": 0,
      "dist": {
        "0": 15,
        "1": 25,
        "2": 4,
        "3": 1,
        "4": 1,
        "6": 1
      },
      "hits": {
        "0": 15,
        "1": 40,
        "2": 44,
        "3": 45,
        "Infinity": 47
      }
    },
    "advcl": {
      "arcs": 446,
      "unmapped": 0,
      "cross": 284,
      "hardCross": 0,
      "dist": {
        "0": 162,
        "1": 194,
        "2": 52,
        "3": 22,
        "4": 11,
        "5": 5
      },
      "hits": {
        "0": 162,
        "1": 356,
        "2": 408,
        "3": 430,
        "Infinity": 446
      }
    },
    "parataxis": {
      "arcs": 235,
      "unmapped": 2,
      "cross": 224,
      "hardCross": 0,
      "dist": {
        "0": 9,
        "1": 108,
        "2": 64,
        "3": 23,
        "4": 12,
        "5": 9,
        "6": 2,
        "7": 3,
        "9": 1,
        "10": 1,
        "11": 1
      },
      "hits": {
        "0": 9,
        "1": 117,
        "2": 181,
        "3": 204,
        "Infinity": 233
      }
    },
    "xcomp": {
      "arcs": 163,
      "unmapped": 0,
      "cross": 34,
      "hardCross": 0,
      "dist": {
        "0": 129,
        "1": 23,
        "2": 7,
        "3": 2,
        "6": 1,
        "7": 1
      },
      "hits": {
        "0": 129,
        "1": 152,
        "2": 159,
        "3": 161,
        "Infinity": 163
      }
    },
    "ccomp": {
      "arcs": 217,
      "unmapped": 0,
      "cross": 71,
      "hardCross": 0,
      "dist": {
        "0": 146,
        "1": 46,
        "2": 21,
        "3": 2,
        "4": 1,
        "5": 1
      },
      "hits": {
        "0": 146,
        "1": 192,
        "2": 213,
        "3": 215,
        "Infinity": 217
      }
    },
    "conj": {
      "arcs": 331,
      "unmapped": 0,
      "cross": 196,
      "hardCross": 0,
      "dist": {
        "0": 135,
        "1": 112,
        "2": 50,
        "3": 22,
        "4": 7,
        "5": 3,
        "6": 2
      },
      "hits": {
        "0": 135,
        "1": 247,
        "2": 297,
        "3": 319,
        "Infinity": 331
      }
    },
    "cc": {
      "arcs": 164,
      "unmapped": 0,
      "cross": 1,
      "hardCross": 0,
      "dist": {
        "0": 163,
        "2": 1
      },
      "hits": {
        "0": 163,
        "1": 163,
        "2": 164,
        "3": 164,
        "Infinity": 164
      }
    }
  },
  "maxHop": 11,
  "controls": 16,
  "unalignedIDs": []
}
```
## 接入建议
保留跨弱标点的候选连接，切分不能默认关闭条件、转述或论元作用域；预算不足应标明外部未知。后续真正需要无gold关系排序、开放语义验证、合法口语开发及独立轨未见留出。未修改生产、PR、交接、冻结、历史证据等级、训练、部署、主动CI或费用。
## 复算
传入固定上游dev.conllu全文，标准JS核心已执行；Node包装未执行。
```js
function study(content){
 const ck=(x,m)=>{if(!x)throw Error(m)};
 const rels=new Set(["advcl","ccomp","xcomp","parataxis","conj","csubj","acl","mark","cc"]);
 const soft=new Set(Array.from("，,、：:；;")),hard=new Set(Array.from("。！？!?")),all=new Set([...soft,...hard]),radii=[0,1,2,3,Infinity];
 function segments(chars,delim){
  let index=Array(chars.length).fill(-1),count=0,last=false;
  for(let i=0;i<chars.length;i++){
   if(delim.has(chars[i])){last=false;continue}
   if(/\s/u.test(chars[i]))continue;
   if(!last){count++;last=true}
   index[i]=count-1;
  }
  return {index,count};
 }
 function align(text,rows){
  const chars=Array.from(text),positions=new Map();let cursor=0;
  for(let row of rows){
   while(cursor<chars.length&&/\s/u.test(chars[cursor]))cursor++;
   const form=Array.from(row[1]);
   if(chars.slice(cursor,cursor+form.length).join("")!==row[1])return null;
   positions.set(+row[0],[cursor,cursor+form.length]);cursor+=form.length;
  }
  while(cursor<chars.length&&/\s/u.test(chars[cursor]))cursor++;
  return cursor===chars.length?{chars,positions}:null;
 }
 const stat=()=>({arcs:0,unmapped:0,cross:0,hardCross:0,dist:{},hits:Object.fromEntries(radii.map(n=>[String(n),0]))});
 let out={sentences:0,aligned:0,unaligned:0,tokens:0,nonPunctArcs:0,scopeArcs:0,sentencesWithScope:0,sentencesWithCrossScope:0,sentencesWithHardCrossScope:0,segments:0,pairs:Object.fromEntries(radii.map(n=>[String(n),0])),allArcs:stat(),scope:stat(),byRelation:{},maxHop:0,controls:0,unalignedIDs:[]};
 for(let chunk of content.trim().split(/\n\s*\n/)){
  let lines=chunk.split(/\r?\n/),text=lines.find(x=>x.startsWith("# text = "))?.slice(9),id=lines.find(x=>x.startsWith("# sent_id = "))?.slice(12);
  if(text===undefined)continue;
  const rows=lines.filter(x=>/^\d+\t/.test(x)).map(x=>x.split("\t"));
  ck(rows.every(r=>r.length===10),"conllu row");
  out.sentences++;out.tokens+=rows.length;
  let z=align(text,rows);
  if(!z){out.unaligned++;out.unalignedIDs.push(id);continue}
  out.aligned++;
  let {chars,positions}=z,s=segments(chars,all),h=segments(chars,hard),n=s.count;
  out.segments+=n;
  for(let k of radii){let count=0;for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(Math.abs(i-j)<=k)count++;out.pairs[String(k)]+=count;ck(count===n+2*Array.from({length:Math.min(n-1,k)},(_,i)=>n-i-1).reduce((a,b)=>a+b,0),"pair formula")}
  const get=(p,seg)=>{
   const [start,end]=positions.get(p),vals=[...new Set(seg.index.slice(start,end).filter(x=>x>=0))];
   return vals.length===1?vals[0]:null;
  };
  let any=false,cross=false,hcross=false;
  for(let row of rows){
   let child=+row[0],head=+row[6],rel=row[7].split(":")[0];
   if(!head||rel==="punct"||row[3]==="PUNCT")continue;
   ck(positions.has(head),"head exists");out.nonPunctArcs++;
   let isScope=rels.has(rel);
   if(isScope){out.scopeArcs++;any=true}
   let a=get(child,s),b=get(head,s),ah=get(child,h),bh=get(head,h),v=[out.allArcs];
   if(isScope){v.push(out.scope,out.byRelation[rel]??=stat())}
   for(let k of v){
    k.arcs++;
    if(a===null||b===null){k.unmapped++;continue}
    let d=Math.abs(a-b);k.dist[d]=(k.dist[d]||0)+1;k.cross+=+(d>0);k.hardCross+=+(ah!==null&&bh!==null&&ah!==bh);
    for(let radius of radii)k.hits[String(radius)]+=+(d<=radius);
   }
   if(isScope&&a!==null&&b!==null){let d=Math.abs(a-b);cross||=d>0;hcross||=ah!==null&&bh!==null&&ah!==bh;out.maxHop=Math.max(out.maxHop,d)}
  }
  out.sentencesWithScope+=+any;out.sentencesWithCrossScope+=+cross;out.sentencesWithHardCrossScope+=+hcross;
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 const s=segments(Array.from("先说，后来；再想。"),all);ctl(s.count===3&&s.index[0]===0&&s.index[3]===1&&s.index[6]===2,"raw boundary");
 ctl(segments(Array.from("，；。"),all).count===0,"empty");
 ctl(segments(Array.from("甲，；乙"),all).count===2,"consecutive separators");
 ctl(align("甲 乙",[["1","甲"],["2","乙"]]).positions.get(2)[0]===2,"spaces");
 ctl(align("甲乙",[["1","甲"],["2","丙"]])===null,"unaligned fail closed");
 for(let v of [out.allArcs,out.scope,...Object.values(out.byRelation)]){
  ctl(v.hits.Infinity===v.arcs-v.unmapped&&v.cross===v.hits.Infinity-v.hits["0"],"accounting");
  ck(radii.every((n,i)=>!i||v.hits[String(n)]>=v.hits[String(radii[i-1])]),"nested");
 }
 return out;
}
console.log(JSON.stringify(study(require("node:fs").readFileSync(process.argv[2],"utf8")),null,2));
```
