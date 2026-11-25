# 自主认知专项累计第134轮候选：真实外部中文句法开发集获取与结构审计
2026-11-25。RESEARCH_CANDIDATE / EXTERNAL_DEVELOPMENT_BYTES_VERIFIED / DESCRIPTIVE_SYNTAX_AUDIT / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 9931c93dd784ab2c39c9fec363bbefc62e62bbe9，核对近期12提交、13开放PR、v3.2前15行及历史全文、同步规程前20行、唯一交接前18行、R78前60行、R133前17行、v0.7任务前10行。R78外部资料仅元数据，dev读取失败；本轮使用Git blob入口实际取得完整开发集并验证UTF8 Git SHA1，不重复元数据清点。与数据轨区分：本轮仅针对R131条件/极性候选的句法可行性诊断，不建立重复的数据登记总表。
## 来源与许可
UniversalDependencies/UD_Chinese-GSDSimp，固定commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3，zh_gsdsimp-ud-dev.conllu，blob af8cc878e7934b38ce3c1a266053100e7c47de6f，固定来源 https://github.com/UniversalDependencies/UD_Chinese-GSDSimp/blob/b79a1c2f7ba7f9b264808d91c6886a67b7f847a3/zh_gsdsimp-ud-dev.conllu 。实际读取固定Git README（R78登记blob 5cb7d4a8446b4a167915225483aa94d187f23798）、Git blob全文；Git API连接器直接返回解码文本，不是JSON，首次按JSON解析失败，改按文本处理。实际UTF8字节长度及Git blob SHA1独立计算与登记完全一致。没有SHA256，未保存原始文件至项目仓库。LICENSE.txt入口返回长度202，仅获取状态记录，不把未知文件内容当已审许可。README明确CC BY-SA 4.0标注许可与底层文本权利分离；正式官方英文页 https://universaldependencies.org/treebanks/zh_gsdsimp/ 和格式 https://universaldependencies.org/format.html 本轮实际查阅前段。官方最新全库统计4997句123289词元不是本固定dev实测分母。语料来源为wiki，经繁简转换及人工校正，原始关系人工标注转UD，部分属性自动赋值/修订；不能当真人个人决策对话、开放语义金标、训练许可或真实效果。仅对公开开发集做非训练的结构和聚合研究，不再分发句子或token正文，不读取test或train，不将dev作为独立留出。具体底层文本来源及派生模型许可仍须数据轨审定。
## 研究合同
按CoNLL-U十列读取、每句唯一ID与parallel ID、基础依存树根、节点连续、父索引、无循环及空白重建；不是完整官方validator（未查增强依存、所有属性合法性、NFC、multiword及empty节点完整语义；非整型行计数并跳过）。聚合UPOS/DEPREL、Polarity=Neg以及R131原有限提示词表在人工token边界上的精确匹配与token内部子串匹配；后者只表示词法边界风险，不能视为真实误判，跨token提示未测。对条件提示词的人工句法父节点、父节点关系及子树离散性作统计；advcl并非必然条件，不为全部条件金标；Polarity=Neg不等同逻辑作用域，属性缺失不是肯定或负例。此处使用金标token和依存关系作诊断，不是自动分词或解析能力。所有提示词和统计口径研究者选定，不训练，不根据dev调整后宣称独立泛化。实际源身份和句法结构不能证明语义义务、实体、因果、真实用户约束或数学输入资格。跨划分泄漏、相同平行情节、真实任务覆盖、训练许可、独立验收均未闭合。无实际Codex开发、CI、PR合并、部署、费用或冻结变化，v0.7任务保持不变。
## 复算
从上述固定blob读取全文UTF8，标准Node可用fs读取raw后调用audit。仅执行自有代码，外部文本按数据解析。
```js
function audit(raw){
 const ck=(b,m)=>{if(!b)throw Error(m)};
 // UTF-8 byte encoding and Git SHA1; standard JS, no dependency.
 function utf(s){let a=[];for(let x of s){let c=x.codePointAt(0);if(c<128)a.push(c);else if(c<2048)a.push(192|(c>>6),128|(c&63));else if(c<65536)a.push(224|(c>>12),128|((c>>6)&63),128|(c&63));else a.push(240|(c>>18),128|((c>>12)&63),128|((c>>6)&63),128|(c&63))}return a}
 function sha1(a){let b=a.slice(),n=b.length*8;b.push(128);while(b.length%64!==56)b.push(0);for(let i=7;i>=0;i--)b.push(Math.floor(n/2**(i*8))&255);let h=[0x67452301,0xefcdab89,0x98badcfe,0x10325476,0xc3d2e1f0],rot=(x,n)=>(x<<n)|(x>>>(32-n));for(let j=0;j<b.length;j+=64){let w=new Int32Array(80);for(let i=0;i<16;i++){let k=j+4*i;w[i]=(b[k]<<24)|(b[k+1]<<16)|(b[k+2]<<8)|b[k+3]}for(let i=16;i<80;i++)w[i]=rot(w[i-3]^w[i-8]^w[i-14]^w[i-16],1);let [a,c,d,e,f]=h;for(let i=0;i<80;i++){let v=i<20?(c&d)|(~c&e):i<40?c^d^e:i<60?(c&d)|(c&e)|(d&e):c^d^e,k=i<20?0x5a827999:i<40?0x6ed9eba1:i<60?0x8f1bbcdc:0xca62c1d6,t=(rot(a,5)+v+f+k+w[i])|0;f=e;e=d;d=rot(c,30);c=a;a=t}h=h.map((x,i)=>(x+[a,c,d,e,f][i])|0)}return h.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("")}
 const bytes=utf(raw),git=sha1(utf("blob "+bytes.length+"\0").concat(bytes));
 ck(sha1(utf("abc"))==="a9993e364706816aba3e25717850c26c9cd0d89d","hash vector");
 ck(git==="af8cc878e7934b38ce3c1a266053100e7c47de6f"&&bytes.length===1195378,"source bytes");
 const cues=["仅用于","如果","只要","若","没有","不能","不要","并非","不再","不","没","未","无","撤回","撤掉","取消"];
 const guard=new Set(["如果","只要","若","仅用于"]),polarity=new Set(["没有","不能","不要","并非","不再","不","没","未","无"]);
 const out={bytes:bytes.length,gitBlob:git,sentences:0,tokens:0,uniqueSentenceIds:0,uniqueParallelIds:0,duplicateTexts:0,validTrees:0,invalidTrees:0,textReconstructionMismatch:0,nonIntegerRows:0,pos:{},relations:{},negFeatureTokens:0,negFeatureCueExact:0,negFeatureCueSubstring:0,negFeatureRel:{},cueExactTokens:0,cueSubstringOnlyTokens:0,cueExactNegFeature:0,guardExactTokens:0,guardRel:{},guardHeadRel:{},guardHeadDiscontinuous:0,guardHeadWithAdvcl:0,guardSentenceCount:0,controls:2};
 let ids=new Set(),parallel=new Set(),texts=new Set(),inc=(o,k)=>o[k]=(o[k]??0)+1;
 for(let block of raw.trimEnd().split(/\n\n+/)){
  let lines=block.split("\n"),id=lines.find(x=>x.startsWith("# sent_id = "))?.slice(12),p=lines.find(x=>x.startsWith("# parallel_id = "))?.slice(16),txt=lines.find(x=>x.startsWith("# text = "))?.slice(9);
  ck(id&&!ids.has(id)&&p&&!parallel.has(p)&&typeof txt==="string","metadata");ids.add(id);parallel.add(p);if(texts.has(txt))out.duplicateTexts++;texts.add(txt);
  let ts=[];for(let l of lines.filter(x=>!x.startsWith("#"))){let c=l.split("\t");ck(c.length===10,"columns");if(!/^[1-9]\d*$/.test(c[0])){out.nonIntegerRows++;continue}ts.push({id:+c[0],form:c[1],pos:c[3],feat:c[5],head:+c[6],rel:c[7],misc:c[9]})}
  out.sentences++;out.tokens+=ts.length;
  const by=new Map(ts.map(t=>[t.id,t])),valid=ts.every((t,i)=>t.id===i+1&&Number.isInteger(t.head)&&t.head>=0&&t.head<=ts.length&&(t.head===0)===(t.rel==="root"))&&ts.filter(t=>t.head===0).length===1&&ts.every(t=>{let seen=new Set();while(t.head){if(seen.has(t.id)||!by.has(t.head))return false;seen.add(t.id);t=by.get(t.head)}return true});
  out.validTrees+=+valid;out.invalidTrees+=+!valid;
  let reconstructed=ts.map(t=>t.form+(t.misc.split("|").includes("SpaceAfter=No")?"":" ")).join("").trimEnd();out.textReconstructionMismatch+=+(reconstructed!==txt);
  let hasGuard=false;
  for(let t of ts){inc(out.pos,t.pos);inc(out.relations,t.rel);let neg=t.feat.split("|").includes("Polarity=Neg"),exact=cues.includes(t.form),part=cues.some(c=>t.form.includes(c));out.cueExactTokens+=+exact;out.cueSubstringOnlyTokens+=+(part&&!exact);out.cueExactNegFeature+=+(exact&&neg);if(neg){out.negFeatureTokens++;out.negFeatureCueExact+=+polarity.has(t.form);out.negFeatureCueSubstring+=+[...polarity].some(c=>t.form.includes(c));inc(out.negFeatureRel,t.rel)}
   if(guard.has(t.form)){hasGuard=true;out.guardExactTokens++;inc(out.guardRel,t.rel);let h=by.get(t.head);if(h){inc(out.guardHeadRel,h.rel);out.guardHeadWithAdvcl+=+(h.rel==="advcl");let desc=ts.filter(x=>{let q=x;for(let k=0;k<=ts.length;k++){if(q.id===h.id)return true;if(!q.head||!by.has(q.head))return false;q=by.get(q.head)}return false}).map(x=>x.id);out.guardHeadDiscontinuous+=+(desc.length!==Math.max(...desc)-Math.min(...desc)+1)}}}
  out.guardSentenceCount+=+hasGuard;
 }
 out.uniqueSentenceIds=ids.size;out.uniqueParallelIds=parallel.size;
 for(let f of [()=>out.sentences===ids.size,()=>out.validTrees+out.invalidTrees===out.sentences,()=>Object.values(out.pos).reduce((a,b)=>a+b,0)===out.tokens,()=>Object.values(out.relations).reduce((a,b)=>a+b,0)===out.tokens,()=>out.negFeatureCueExact<=out.negFeatureCueSubstring&&out.negFeatureCueSubstring<=out.negFeatureTokens,()=>out.guardHeadWithAdvcl<=out.guardExactTokens,()=>out.cueExactNegFeature<=out.cueExactTokens]){ck(f(),"control");out.controls++}
 return out
}
console.log(JSON.stringify(audit(raw),null,2));
```
## 实测
```json
{
  "bytes": 1195378,
  "gitBlob": "af8cc878e7934b38ce3c1a266053100e7c47de6f",
  "sentences": 500,
  "tokens": 12665,
  "uniqueSentenceIds": 500,
  "uniqueParallelIds": 500,
  "duplicateTexts": 0,
  "validTrees": 500,
  "invalidTrees": 0,
  "textReconstructionMismatch": 0,
  "nonIntegerRows": 0,
  "pos": {
    "ADV": 323,
    "PUNCT": 1770,
    "VERB": 1851,
    "SCONJ": 559,
    "NOUN": 3637,
    "ADJ": 313,
    "PART": 1042,
    "AUX": 365,
    "ADP": 556,
    "DET": 119,
    "CCONJ": 164,
    "X": 79,
    "PRON": 174,
    "NUM": 654,
    "PROPN": 1056,
    "SYM": 3
  },
  "relations": {
    "advmod": 330,
    "punct": 1770,
    "acl:relcl": 187,
    "mark:rel": 258,
    "nsubj": 931,
    "csubj": 47,
    "compound": 593,
    "root": 500,
    "nmod": 1798,
    "case": 921,
    "mark": 485,
    "advcl": 446,
    "aux": 152,
    "obl": 326,
    "parataxis": 235,
    "amod": 197,
    "cop": 172,
    "det": 135,
    "xcomp": 163,
    "ccomp": 217,
    "obj": 818,
    "conj": 331,
    "cc": 164,
    "appos": 127,
    "nmod:tmod": 183,
    "nummod": 614,
    "clf": 200,
    "nsubj:pass": 24,
    "aux:pass": 40,
    "acl": 80,
    "obl:agent": 9,
    "flat:name": 118,
    "discourse": 22,
    "discourse:sp": 2,
    "flat:foreign": 24,
    "orphan": 2,
    "obl:patient": 20,
    "compound:ext": 5,
    "dislocated": 5,
    "iobj": 8,
    "mark:adv": 5,
    "nsubj:outer": 1
  },
  "negFeatureTokens": 44,
  "negFeatureCueExact": 36,
  "negFeatureCueSubstring": 44,
  "negFeatureRel": {
    "advmod": 22,
    "advcl": 4,
    "aux": 3,
    "root": 7,
    "xcomp": 2,
    "parataxis": 5,
    "acl:relcl": 1
  },
  "cueExactTokens": 43,
  "cueSubstringOnlyTokens": 50,
  "cueExactNegFeature": 36,
  "guardExactTokens": 2,
  "guardRel": {
    "case": 2
  },
  "guardHeadRel": {
    "xcomp": 2
  },
  "guardHeadDiscontinuous": 0,
  "guardHeadWithAdvcl": 0,
  "guardSentenceCount": 2,
  "controls": 9
}
```
后续优先与数据轨协调许可、句法与真实决策语义之间的独立标注，不继续重复同一开发集统计；独立轨掌管未见测试。正式训练和工程另获授权。
