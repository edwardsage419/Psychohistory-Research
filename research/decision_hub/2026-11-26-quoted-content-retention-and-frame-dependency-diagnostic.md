# 自主认知：引述内容保留、作用域框架及外部依存关系诊断
2026-11-26。RESEARCH_CANDIDATE / REAL_EXTERNAL_DEVELOPMENT_DATA_EXECUTED / PREDECESSOR_CODE_EXECUTED / GOLD_ENDPOINT_DIAGNOSTIC / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线
起点main eb978db8ad6a5256213d1dbdf662b91787826888；沿用本轮已核对v3.2、同步规程、25近期提交、15开放PR、历史交接固定blob（最新路径未定位），#63固定head 734686980b19da9291bdd08b67d4e2519c011acf。前阶段外部跨标点依存诊断 research/decision_hub/2026-11-26-external-dependency-cross-punctuation-scope-diagnostic.md blob 0633533cebfb0cdea6aecff4e422bd3d4cdb5188，实际复用其align函数；前轮原生目标引述审计8fb6c4a7b4ad9d8251ea3137a998730a2e21f5e4已证明仅对明确目标发现而言屏蔽引述可减少模板误触发。本轮专门区分请求权限隔离与内容语法保留，不重复引号栈发明、金标词格或外部语料数量。
## 来源
同一固定UD_Chinese-GSDSimp开发集 af8cc878e7934b38ce3c1a266053100e7c47de6f，commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3，500句已见开发材料，完整文本实际读取。上一阶段已经核对同commit LICENSE.txt CC BY-SA 4.0，README前20行；本轮未重新下载许可，不复制原句或标注，仅保存聚合计数与未配平句ID。来源 https://github.com/UniversalDependencies/UD_Chinese-GSDSimp/tree/b79a1c2f7ba7f9b264808d91c6886a67b7f847a3 ，许可 https://creativecommons.org/licenses/by-sa/4.0/ 。连接器报告固定blob，未重算原始Git字节；非真实个人对话、授权训练、独立留出。
## 方法
从# text的Unicode标量原文构建引号框架树，支持显式“”、‘’、「」、『』与ASCII双引号，保留每个框架独立ID和父关系、字符所属框架；标记符本身不当作内容，开闭失衡整句标为未知，不默认将其归属本人或删除。没有引号语义分类（作品名、术语、反讽、直接转述等均可能）、转述者识别、未标记转述、跨句引述延续、字符转义或开放语言理解；ASCII双引号也可能作其他符号，真实适用性未知。框架结构只是原文候选，非权限。用前序align将金标词跨度用于事后评价，若某词内容跨框架或无归属，记UNMAPPED。只计非root、非punct依存边；失衡句的边单独报告。按端点同属根框架、同属引述框架、祖先跨越、不同引述框架及不可映射分类；九类从句/并列/标记相关依存边另行计量。两个故意过度简化对照：若将引述内容完全删除，所有已知至少一个端点位于引述框架的边均无法保留；若保留框架内部但禁止跨框架，祖先或兄弟跨越边会丢失。这只是结构性候选丢失诊断，不是现有产品实际错误、关系正确率、事实资格或执行权限。结构框架保留内容，并不意味着可以执行其中请求、将引述当事实或自动认定说话者。所有候选authority NONE。
## 实际执行
标准JS核心实际两次一致。原文生成框架，gold仅评价；九个专项/计数控制含嵌套、兄弟、失衡与ASCII。记录全部计数、失衡句及按标签分布。样本为同一已见500句，不能用两阶段相加声称1000句独立证据。研究者选定引号集合、分类、比较基线及句法代理，不作为正式产品默认。未运行原生、独立留出、真实用户、设备、训练。
```json
{
  "sentences": 500,
  "aligned": 500,
  "quoteSentences": 36,
  "balancedQuoteSentences": 36,
  "malformedQuoteSentences": 0,
  "quoteFrames": 43,
  "maxDepth": 1,
  "nonPunctArcs": 10395,
  "balancedQuoteArcs": 960,
  "malformedArcs": 0,
  "byClass": {
    "OUTSIDE": 10188,
    "SAME_QUOTED_FRAME": 127,
    "PARENT_OR_ANCESTOR_CROSS": 76,
    "DISTINCT_QUOTED_FRAMES": 4,
    "UNMAPPED": 0
  },
  "scopeArcs": {
    "OUTSIDE": 2572,
    "SAME_QUOTED_FRAME": 28,
    "PARENT_OR_ANCESTOR_CROSS": 14,
    "DISTINCT_QUOTED_FRAMES": 4,
    "UNMAPPED": 0
  },
  "byRelation": {
    "advmod": {
      "OUTSIDE": 327,
      "SAME_QUOTED_FRAME": 3,
      "PARENT_OR_ANCESTOR_CROSS": 0,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "acl": {
      "OUTSIDE": 262,
      "SAME_QUOTED_FRAME": 2,
      "PARENT_OR_ANCESTOR_CROSS": 3,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "mark": {
      "OUTSIDE": 740,
      "SAME_QUOTED_FRAME": 8,
      "PARENT_OR_ANCESTOR_CROSS": 0,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "nsubj": {
      "OUTSIDE": 942,
      "SAME_QUOTED_FRAME": 7,
      "PARENT_OR_ANCESTOR_CROSS": 7,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "csubj": {
      "OUTSIDE": 46,
      "SAME_QUOTED_FRAME": 1,
      "PARENT_OR_ANCESTOR_CROSS": 0,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "compound": {
      "OUTSIDE": 587,
      "SAME_QUOTED_FRAME": 10,
      "PARENT_OR_ANCESTOR_CROSS": 1,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "nmod": {
      "OUTSIDE": 1931,
      "SAME_QUOTED_FRAME": 40,
      "PARENT_OR_ANCESTOR_CROSS": 10,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "case": {
      "OUTSIDE": 897,
      "SAME_QUOTED_FRAME": 11,
      "PARENT_OR_ANCESTOR_CROSS": 13,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "advcl": {
      "OUTSIDE": 441,
      "SAME_QUOTED_FRAME": 3,
      "PARENT_OR_ANCESTOR_CROSS": 2,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "aux": {
      "OUTSIDE": 188,
      "SAME_QUOTED_FRAME": 4,
      "PARENT_OR_ANCESTOR_CROSS": 0,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "obl": {
      "OUTSIDE": 350,
      "SAME_QUOTED_FRAME": 1,
      "PARENT_OR_ANCESTOR_CROSS": 4,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "parataxis": {
      "OUTSIDE": 233,
      "SAME_QUOTED_FRAME": 0,
      "PARENT_OR_ANCESTOR_CROSS": 2,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "amod": {
      "OUTSIDE": 189,
      "SAME_QUOTED_FRAME": 8,
      "PARENT_OR_ANCESTOR_CROSS": 0,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "cop": {
      "OUTSIDE": 168,
      "SAME_QUOTED_FRAME": 0,
      "PARENT_OR_ANCESTOR_CROSS": 4,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "det": {
      "OUTSIDE": 134,
      "SAME_QUOTED_FRAME": 1,
      "PARENT_OR_ANCESTOR_CROSS": 0,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "xcomp": {
      "OUTSIDE": 160,
      "SAME_QUOTED_FRAME": 1,
      "PARENT_OR_ANCESTOR_CROSS": 2,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "ccomp": {
      "OUTSIDE": 212,
      "SAME_QUOTED_FRAME": 1,
      "PARENT_OR_ANCESTOR_CROSS": 4,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "obj": {
      "OUTSIDE": 799,
      "SAME_QUOTED_FRAME": 5,
      "PARENT_OR_ANCESTOR_CROSS": 14,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "conj": {
      "OUTSIDE": 319,
      "SAME_QUOTED_FRAME": 7,
      "PARENT_OR_ANCESTOR_CROSS": 1,
      "DISTINCT_QUOTED_FRAMES": 4,
      "UNMAPPED": 0
    },
    "cc": {
      "OUTSIDE": 159,
      "SAME_QUOTED_FRAME": 5,
      "PARENT_OR_ANCESTOR_CROSS": 0,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "appos": {
      "OUTSIDE": 119,
      "SAME_QUOTED_FRAME": 1,
      "PARENT_OR_ANCESTOR_CROSS": 7,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "nummod": {
      "OUTSIDE": 607,
      "SAME_QUOTED_FRAME": 5,
      "PARENT_OR_ANCESTOR_CROSS": 2,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "clf": {
      "OUTSIDE": 199,
      "SAME_QUOTED_FRAME": 1,
      "PARENT_OR_ANCESTOR_CROSS": 0,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "flat": {
      "OUTSIDE": 142,
      "SAME_QUOTED_FRAME": 0,
      "PARENT_OR_ANCESTOR_CROSS": 0,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "discourse": {
      "OUTSIDE": 22,
      "SAME_QUOTED_FRAME": 2,
      "PARENT_OR_ANCESTOR_CROSS": 0,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "orphan": {
      "OUTSIDE": 2,
      "SAME_QUOTED_FRAME": 0,
      "PARENT_OR_ANCESTOR_CROSS": 0,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "dislocated": {
      "OUTSIDE": 5,
      "SAME_QUOTED_FRAME": 0,
      "PARENT_OR_ANCESTOR_CROSS": 0,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    },
    "iobj": {
      "OUTSIDE": 8,
      "SAME_QUOTED_FRAME": 0,
      "PARENT_OR_ANCESTOR_CROSS": 0,
      "DISTINCT_QUOTED_FRAMES": 0,
      "UNMAPPED": 0
    }
  },
  "blanketMaskDrops": 207,
  "opaqueFrameDrops": 80,
  "blanketMaskScopeDrops": 46,
  "opaqueFrameScopeDrops": 18,
  "controls": 9,
  "malformedIDs": []
}
```
## 接入
原文解析阶段宜保留文本、框架及跨框架候选关系，方法发现和权限核验阶段独立处理请求是否由用户采纳；禁止用删除整段内容的方式替代完整语言表示。失衡及未标记语境需独立保留未知。实际科学事实来源仍经可信宿主、适用合同及来源版本核验。未修改生产、PR、交接、冻结、证据等级、训练、部署、主动CI或费用。
## 复算
固定外部dev.conllu及前序报告按顺序传入；仅加载审查过的项目自有JS。Node包装未运行，连接器核心已执行。
```js
const [data,previous]=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8"));
const code=previous.split("\`\`\`js\n")[1].split("\n\`\`\`")[0],make=Function(code.split(" const stat=()=>")[0]+"\nreturn {align,segments};\n}\nreturn study('');");
function study(content,make){
 const R=make(),ck=(v,m)=>{if(!v)throw Error(m)},pairs={"“":"”","‘":"’","「":"」","『":"』",'"':'"'},closers=new Set(Object.values(pairs)),rels=new Set(["advcl","ccomp","xcomp","parataxis","conj","csubj","acl","mark","cc"]);
 function frames(chars){
  let nodes=[{id:0,parent:null,start:0,end:chars.length}],stack=[0],owner=Array(chars.length).fill(null),errors=[],maxDepth=0;
  for(let i=0;i<chars.length;i++){
   let c=chars[i],t=nodes[stack.at(-1)];
   if(stack.length>1&&c===t.close){t.end=i;stack.pop();continue}
   if(Object.hasOwn(pairs,c)){let id=nodes.length;nodes.push({id,parent:t.id,start:i+1,end:null,close:pairs[c]});stack.push(id);maxDepth=Math.max(maxDepth,stack.length-1);continue}
   if(closers.has(c)){errors.push({at:i,type:"UNMATCHED_CLOSE"});continue}
   owner[i]=t.id;
  }
  for(let id of stack.slice(1))errors.push({at:nodes[id].start-1,type:"UNCLOSED"});
  return {nodes,owner,errors,maxDepth};
 }
 function ancestor(nodes,a,b){
  for(let k=b;k!==null;k=nodes[k].parent)if(k===a)return true;
  return false;
 }
 function classify(nodes,a,b){
  if(a===null||b===null)return "UNMAPPED";
  if(a===0&&b===0)return "OUTSIDE";
  if(a===b)return "SAME_QUOTED_FRAME";
  if(ancestor(nodes,a,b)||ancestor(nodes,b,a))return "PARENT_OR_ANCESTOR_CROSS";
  return "DISTINCT_QUOTED_FRAMES";
 }
 const names=["OUTSIDE","SAME_QUOTED_FRAME","PARENT_OR_ANCESTOR_CROSS","DISTINCT_QUOTED_FRAMES","UNMAPPED"],counts=()=>Object.fromEntries(names.map(n=>[n,0]));
 const out={sentences:0,aligned:0,quoteSentences:0,balancedQuoteSentences:0,malformedQuoteSentences:0,quoteFrames:0,maxDepth:0,nonPunctArcs:0,balancedQuoteArcs:0,malformedArcs:0,byClass:counts(),scopeArcs:counts(),byRelation:{},blanketMaskDrops:0,opaqueFrameDrops:0,blanketMaskScopeDrops:0,opaqueFrameScopeDrops:0,controls:0,malformedIDs:[]};
 for(let chunk of content.trim().split(/\n\s*\n/)){
  let ls=chunk.split(/\r?\n/),text=ls.find(x=>x.startsWith("# text = "))?.slice(9),id=ls.find(x=>x.startsWith("# sent_id = "))?.slice(12);if(text===undefined)continue;
  let rows=ls.filter(x=>/^\d+\t/.test(x)).map(x=>x.split("\t"));out.sentences++;
  let z=R.align(text,rows);if(!z)continue;out.aligned++;
  let f=frames(z.chars),quoted=f.nodes.length>1||f.errors.length>0;
  if(quoted){out.quoteSentences++;out.quoteFrames+=f.nodes.length-1;out.maxDepth=Math.max(out.maxDepth,f.maxDepth);if(f.errors.length){out.malformedQuoteSentences++;out.malformedIDs.push(id)}else out.balancedQuoteSentences++}
  function who(p){let [a,b]=z.positions.get(p),s=[...new Set(f.owner.slice(a,b).filter(v=>v!==null))];return s.length===1?s[0]:null}
  for(let row of rows){
   let h=+row[6],p=+row[0],rel=row[7].split(":")[0];if(!h||rel==="punct"||row[3]==="PUNCT")continue;
   out.nonPunctArcs++;
   if(f.errors.length){out.malformedArcs++;continue}
   if(quoted)out.balancedQuoteArcs++;
   let k=classify(f.nodes,who(p),who(h));out.byClass[k]++;(out.byRelation[rel]??=counts())[k]++;
   let sc=rels.has(rel);if(sc)out.scopeArcs[k]++;
   if(["SAME_QUOTED_FRAME","PARENT_OR_ANCESTOR_CROSS","DISTINCT_QUOTED_FRAMES"].includes(k)){out.blanketMaskDrops++;if(sc)out.blanketMaskScopeDrops++}
   if(["PARENT_OR_ANCESTOR_CROSS","DISTINCT_QUOTED_FRAMES"].includes(k)){out.opaqueFrameDrops++;if(sc)out.opaqueFrameScopeDrops++}
  }
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 let z=frames(Array.from("甲说“乙说‘丙’。”丁"));
 ctl(!z.errors.length&&z.nodes.length===3&&z.maxDepth===2,"nested");
 ctl(classify(z.nodes,0,2)==="PARENT_OR_ANCESTOR_CROSS"&&classify(z.nodes,2,1)==="PARENT_OR_ANCESTOR_CROSS","ancestor");
 ctl(classify(z.nodes,2,2)==="SAME_QUOTED_FRAME","internal");
 z=frames(Array.from("甲“乙”又“丙”"));ctl(classify(z.nodes,1,2)==="DISTINCT_QUOTED_FRAMES","siblings");
 ctl(frames(Array.from("甲“乙")).errors.length===1,"unclosed");
 ctl(frames(Array.from("甲”乙")).errors.length===1,"unmatched close");
 ctl(!frames(Array.from('甲"乙"丙')).errors.length,"ascii");
 ctl(Object.values(out.byClass).reduce((a,b)=>a+b,0)+out.malformedArcs===out.nonPunctArcs,"account");
 ctl(out.blanketMaskDrops>=out.opaqueFrameDrops&&out.blanketMaskScopeDrops>=out.opaqueFrameScopeDrops,"nested baseline");
 return out;
}
console.log(JSON.stringify(study(data,make),null,2));
```
