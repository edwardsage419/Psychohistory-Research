# 自主认知专项累计第135轮候选：外部句法否定依附候选诊断
2026-11-25。RESEARCH_CANDIDATE / EXTERNAL_DEVELOPMENT_BYTES_REVERIFIED / ANNOTATION_CONDITIONED_HEAD_DIAGNOSTIC / TRAINING_NOT_AUTHORIZED / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 7bdbdc918fbcb3f64bb12427ba9e96db540bc2ca。核对近期12提交、13开放PR（#61待审）、v3.2前15行及历史全文、唯一交接前18行、R134前18行及实际源码、R131前15行、R56前12行、v0.7任务前10行。R134仅统计词法提示和属性，本轮增加从已给定否定词元及词性生成句法依附候选的定向基线、子树结构边界诊断，不重复基础统计或R56否定比较运算。
## 证据与范围
固定外部UD Chinese GSDSimp dev，commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3，blob af8cc878e7934b38ce3c1a266053100e7c47de6f；实际重新取得全文，并直接运行R134 audit（blob db9cc100d96d49832fe32879a706f63830301773），字节数1195378及Git SHA1一致。只读dev，不读train/test，不复制任何第三方语句或词元正文至公开项目。固定LICENSE.txt实际取得202字符，表明treebank CC BY-SA 4.0；R78/R134 README注明标注许可与底层文本权利分离，训练与重新分发仍未准入。实际本轮访问英文官方 https://universaldependencies.org/format.html 、https://universaldependencies.org/u/feat/Polarity.html 、https://universaldependencies.org/treebanks/zh_gsdsimp/ 前段；CoNLL-U HEAD为依存父索引或0，Polarity为词形/功能词等的属性，并非逻辑作用域标注。官方说明Features部分自动赋值，UPOS与关系为人工原始标注转换，存在误标可能。R134报告的官方页查阅不能由当时可核验的工具记录确认，本轮实际补查，不追认历史动作。无新真实个人决策资料、独立留出或模型训练。
## 方法
使用已有Polarity=Neg词元作为已知查询锚，已知分词与UPOS，绝不将人工标注当作系统自动识别。7个根节点若与实测不同以结果为准，根否定单列，不给虚构父节点。对非根锚，三种固定未训练候选：nearest所有非标点非自身词元按距离、同距右侧优先；predicateOnly只保留VERB/ADJ/AUX再同排序；soft保留全部非标点词元但优先上述词性、较少中间标点、较短距离和同距右侧优先。算法只读ID、FORM、UPOS及锚ID，不读HEAD/DEPREL；评分为固定启发式，无学习、概率、授权或事实。事后按实际HEAD评估top1/3/5和完整候选覆盖，已见开发数据，非语言理解准确率。将advmod/aux关系的锚与其他关系分层，后者包括否定性谓词等，不可一概把父节点当否定目标。原R131九个极性词面精确匹配子集单列。缺少负例和真实语义作用域标注，不能将依存父节点命中当逻辑否定范围正确。另使用完整人工依存树诊断父子树（包含否定锚）成员集合与连续跨度包络，使用独立祖先链对照；含其他否定、其他从句标签的情况仅说明句法结构复杂，并不证明真正作用域或逻辑关系。实际完整否定语义可能在锚自身、父节点、其他结构或句外。没有自动分词、自动句法解析、角色/意图、跨轮、真实条件或可信义务覆盖，不进入数学计算。所有规则、排序、标签集合和指标由研究者选定；不在同dev调参后声称独立泛化。
## 复算
从固定blob获取UTF8 raw，先调用R134原audit验证，再运行下列自有代码。11专项控制；父子树与祖先链对照在全部非根锚执行。未执行原生平台、设备、训练、Codex、CI、PR合并、部署、费用或冻结变更，v0.7范围不变。产品轨维持唯一交接；不替代数据轨许可与独立轨未见样本。
```js
function experiment(raw){
 const ck=(v,m)=>{if(!v)throw Error(m)},pred=new Set(["VERB","ADJ","AUX"]),cues=new Set(["没有","不能","不要","并非","不再","不","没","未","无"]),rank=(rows,id)=>rows.findIndex(t=>t.id===id)+1;
 // No HEAD/DEPREL used by these candidates. Known tokenization and UPOS
 // are external annotations, not project predictions.
 function propose(ts,n,mode){
  const dist=t=>Math.abs(t.id-n.id),punct=t=>ts.filter(x=>x.pos==="PUNCT"&&x.id>Math.min(t.id,n.id)&&x.id<Math.max(t.id,n.id)).length;
  let rows=ts.filter(t=>t.id!==n.id&&t.pos!=="PUNCT");
  if(mode==="predicateOnly")rows=rows.filter(t=>pred.has(t.pos));
  return rows.sort((a,b)=>(mode==="soft"?Number(!pred.has(a.pos))-Number(!pred.has(b.pos))||punct(a)-punct(b):0)||dist(a)-dist(b)||b.id-a.id)
 }
 function descendants(ts,id){
  let kids=new Map(ts.map(t=>[t.id,[]]));for(let t of ts)if(t.head)kids.get(t.head).push(t.id);
  let seen=new Set(),stack=[id];while(stack.length){let a=stack.pop();if(seen.has(a))throw Error("cycle");seen.add(a);stack.push(...kids.get(a))}return [...seen].sort((a,b)=>a-b)
 }
 const out={sentences:0,tokens:0,negativeAnnotated:0,negativeSentences:0,rootNegative:0,nonRootNegative:0,modifierNegative:0,otherNonRootNegative:0,headPos:{},headRel:{},headLeft:0,headRight:0,headCrossPunct:0,headNotPredicate:0,knownCue:0,knownCueNonRoot:0,modes:{},subtree:{count:0,discontinuous:0,hullExtraTokens:0,containsOtherNegative:0,containsOtherClause:0,headAncestorSameAsNegSubtree:0},controls:0};
 for(let mode of ["nearest","predicateOnly","soft"])out.modes[mode]={top1:0,top3:0,top5:0,covered:0,totalCandidates:0,knownCueTop1:0,modifierTop1:0,otherTop1:0};
 const inc=(m,k)=>m[k]=(m[k]??0)+1;
 for(let block of raw.trimEnd().split(/\n\n+/)){
  let ts=block.split("\n").filter(l=>!l.startsWith("#")).map(l=>{let c=l.split("\t");ck(c.length===10&&/^[1-9]\d*$/.test(c[0]),"row");return {id:+c[0],form:c[1],pos:c[3],neg:c[5].split("|").includes("Polarity=Neg"),head:+c[6],rel:c[7]}});
  out.sentences++;out.tokens+=ts.length;out.negativeSentences+=+ts.some(t=>t.neg);
  for(let n of ts.filter(t=>t.neg)){
   out.negativeAnnotated++;out.knownCue+=+cues.has(n.form);
   if(!n.head){out.rootNegative++;continue}
   out.nonRootNegative++;out.knownCueNonRoot+=+cues.has(n.form);
   const mod=["advmod","aux"].includes(n.rel);out.modifierNegative+=+mod;out.otherNonRootNegative+=+!mod;
   const h=ts[n.head-1];ck(h.id===n.head,"head");inc(out.headPos,h.pos);inc(out.headRel,h.rel);out.headLeft+=+(h.id<n.id);out.headRight+=+(h.id>n.id);out.headNotPredicate+=+!pred.has(h.pos);
   out.headCrossPunct+=+ts.some(t=>t.pos==="PUNCT"&&t.id>Math.min(n.id,h.id)&&t.id<Math.max(n.id,h.id));
   for(let mode of Object.keys(out.modes)){
    const rows=propose(ts.map(({id,pos,form})=>({id,pos,form})),{id:n.id},mode),r=rank(rows,h.id),z=out.modes[mode];z.top1+=+(r===1);z.top3+=+(r>0&&r<=3);z.top5+=+(r>0&&r<=5);z.covered+=+(r>0);z.totalCandidates+=rows.length;z.knownCueTop1+=+(cues.has(n.form)&&r===1);z.modifierTop1+=+(mod&&r===1);z.otherTop1+=+(!mod&&r===1)
   }
   const ds=descendants(ts,h.id),ns=descendants(ts,n.id);
   // Independent ancestor walk, exact oracle for subtree membership only.
   let oracle=ts.filter(t=>{let k=t.id;while(k&&k!==h.id)k=ts[k-1].head;return k===h.id}).map(t=>t.id);
   ck(JSON.stringify(ds)===JSON.stringify(oracle)&&ds.includes(n.id),"tree membership");
   const extra=ds.at(-1)-ds[0]+1-ds.length;
   out.subtree.count++;out.subtree.discontinuous+=+(extra>0);out.subtree.hullExtraTokens+=extra;out.subtree.containsOtherNegative+=+ts.some(t=>t.neg&&t.id!==n.id&&ds.includes(t.id));
   out.subtree.containsOtherClause+=+ts.some(t=>t.id!==n.id&&t.id!==h.id&&ds.includes(t.id)&&["advcl","ccomp","xcomp","acl","acl:relcl","parataxis"].includes(t.rel));
   out.subtree.headAncestorSameAsNegSubtree+=+(JSON.stringify(ds)===JSON.stringify(ns));
  }
 }
 for(let f of [()=>out.sentences===500&&out.tokens===12665,()=>out.negativeAnnotated===44&&out.knownCue===36,()=>out.rootNegative+out.nonRootNegative===44,()=>out.modifierNegative+out.otherNonRootNegative===out.nonRootNegative,()=>out.headLeft+out.headRight===out.nonRootNegative,()=>out.subtree.count===out.nonRootNegative&&out.subtree.headAncestorSameAsNegSubtree===0,()=>out.modes.nearest.covered===out.modes.soft.covered,()=>out.modes.predicateOnly.covered===out.nonRootNegative-out.headNotPredicate,()=>Object.values(out.modes).every(z=>z.top1<=z.top3&&z.top3<=z.top5&&z.top5<=z.covered&&z.modifierTop1+z.otherTop1===z.top1),()=>JSON.stringify(descendants([{id:1,head:3},{id:2,head:0},{id:3,head:2}],3))==="[1,3]",()=>propose([{id:1,pos:"NOUN"},{id:2,pos:"ADV"},{id:3,pos:"VERB"}],{id:2},"soft")[0].id===3]){ck(f(),"control "+out.controls);out.controls++}
 return out
}
console.log(JSON.stringify(experiment(raw),null,2));
```
## 实测
```json
{
  "sentences": 500,
  "tokens": 12665,
  "negativeAnnotated": 44,
  "negativeSentences": 42,
  "rootNegative": 7,
  "nonRootNegative": 37,
  "modifierNegative": 25,
  "otherNonRootNegative": 12,
  "headPos": {
    "ADJ": 3,
    "VERB": 30,
    "NOUN": 3,
    "AUX": 1
  },
  "headRel": {
    "advcl": 4,
    "parataxis": 4,
    "root": 18,
    "ccomp": 4,
    "amod": 1,
    "conj": 1,
    "obj": 1,
    "acl:relcl": 3,
    "xcomp": 1
  },
  "headLeft": 11,
  "headRight": 26,
  "headCrossPunct": 9,
  "headNotPredicate": 3,
  "knownCue": 36,
  "knownCueNonRoot": 29,
  "modes": {
    "nearest": {
      "top1": 15,
      "top3": 24,
      "top5": 27,
      "covered": 37,
      "totalCandidates": 908,
      "knownCueTop1": 14,
      "modifierTop1": 15,
      "otherTop1": 0
    },
    "predicateOnly": {
      "top1": 21,
      "top3": 31,
      "top5": 31,
      "covered": 34,
      "totalCandidates": 225,
      "knownCueTop1": 17,
      "modifierTop1": 18,
      "otherTop1": 3
    },
    "soft": {
      "top1": 21,
      "top3": 31,
      "top5": 31,
      "covered": 37,
      "totalCandidates": 908,
      "knownCueTop1": 17,
      "modifierTop1": 18,
      "otherTop1": 3
    }
  },
  "subtree": {
    "count": 37,
    "discontinuous": 0,
    "hullExtraTokens": 0,
    "containsOtherNegative": 1,
    "containsOtherClause": 20,
    "headAncestorSameAsNegSubtree": 0
  },
  "controls": 11
}
```
后续：当前开发集的词性条件化诊断完成，优先研究自动句法解析的可学习结构及获得适合个人决策的真实多轮语料；禁止未经授权训练及将本集充当独立留出。
