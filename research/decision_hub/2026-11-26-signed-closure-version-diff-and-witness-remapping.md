# 自主推理：版本差分、局部失效与证据见证稳定身份重映射
2026-11-26。RESEARCH_CANDIDATE / PREDECESSOR_CODE_REUSED_AND_EXECUTED / SYNTHETIC_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线与新增缺口
同一手动工作轮第二阶段，起点main 8489d79f8c1a883a6c75b0d1833f2d39d213004c，前阶段实际写入并回读的 research/decision_hub/2026-11-26-world-scoped-signed-inference-and-proof-retraction.md blob bb5596aa97731c536ff0b6aa66045bb4311ec7f1。沿用本轮已核对的25近期提交、15开放PR、v3.2、同步规程及唯一交接，不重新计入既有1200组研究。新增实际复用其close/verify/ref/status源码，从可信快照自动计算dirty掩码及稳定身份见证重映射；上轮由调用方指定受影响世界，且要求固定源/规则索引。本轮不实现真实授权、签名、持久事务或原生入口，不重复前轮世界闭包算法或既有分域失效、时间重放、持久预算事务。局部查重非全库证明。
## 合同、证明及边界
可信输入为带单调revision、scope、grant、世界有序身份、独立覆盖标志的快照。每条源/规则带稳定ID、版本、出处、授权代次、用途、已资格布尔值、适用世界掩码及符号槽/前件。只保留当前授权、用途且已资格的有效掩码，其余为0。资格由外部宿主提供，不以索引、相似度、已有证据或数值推断；本轮假定输入完整可信、世界顺序改变后宿主已按新编号提供正确掩码，代码不会自动推断真实世界映射。规则和源各自ID唯一，排序使输入列表顺序不影响结果；符号槽含义固定。语义槽含义、方法算法变更须另外全量重建，本轮没有专门schema版本字段，禁止直接生产使用。原型只检测递增修订，授权代次由可信宿主负责单调递增，不能替代权限账本。
若scope、grant或有序世界身份变化，全量重建。否则对所有稳定ID比较有效掩码：身份新添/移除取两侧并；同ID且语义字段、版本、来源、授权、用途等一致取掩码异或；字段变化取掩码并。所有项合并得D。独立参照直接逐世界比较有效源/规则描述集；同一世界无活跃描述变化，则其带符号闭包和原证明仍成立，因此可不重算。版本变化即使推理数值不变也使相应世界失效。算法不求最小实际影响集合，描述变化可能最终无数值变化。证据数组按ID排序后增删会改变索引：在未受影响世界，按旧索引取得稳定ID，再映射到新索引；重新验证全部保留证明。受影响世界重置，从源重新闭包；不沿用旧循环。覆盖标志变化不必重算数值，但每次修订旧发布收据均失效，覆盖不明不得输出全称支持。收据为内存可信夹具的精确比较，未绑定完整内容密码学摘要、运行实例或时效，未防恶意伪造、并发旧发布或磁盘回退，真实系统须沿已有原生实例/版本/来源/授权及原子发布合同，不能将本收据作为安全凭证。所有authority NONE。
## 实际运行
固定上轮原始报告blob，连接器读取其完整JS，提取实际close/verify/ref/status等代码并直接执行。600合成图，每18次编辑，共10800次；世界2至8，8符号槽，4至9来源、6至15规则，随机编辑12类：掩码翻转、版本/来源更正、槽位更正、资格改变、删除、新增、列表重排、新授权、用途更新、重新资格、覆盖变化、世界重排。每步对照逐世界描述差分、全量闭包及前轮独立逐世界集合闭包；验证全部保留见证及4个旧/新只读端口身份。11项控制覆盖零掩码插入后索引移位、同值版本更新、撤权与新授权不自动复用、覆盖独立、世界身份顺序及5类非法输入。两次实际完整输出一致。主循环随机源与规则为已知有限结构，不是真实语义、个人资料、训练或独立样本。初始随机源可能未获当前资格、所有世界无支持；结果不构成现实准确率。扫描次数为算法工作量代理，未测设备性能，不声称真实提速。实际结果：
```json
{
  "graphs": 600,
  "transitions": 10800,
  "dirtyWorlds": 21249,
  "fullWorlds": 53730,
  "zeroDirty": 5081,
  "partialDirty": 2754,
  "fullDirty": 2965,
  "proofChecks": 49072,
  "scanIncremental": 77695,
  "scanFull": 144789,
  "valueUnchangedButDirty": 3721,
  "staleReceiptsRejected": 43200,
  "scopeGenerationTransitions": 1883,
  "coveredChanges": 911,
  "controls": 11,
  "events": {
    "0": 919,
    "1": 889,
    "2": 898,
    "3": 910,
    "4": 838,
    "5": 899,
    "6": 880,
    "7": 931,
    "8": 952,
    "9": 906,
    "10": 911,
    "11": 867
  }
}
```
## 工程接入合同
原文语义候选ID、事件/主体/条件/修订身份与证据来源版本必须先由可信宿主确定，独立未知检测与覆盖资格保留；按有效描述集生成受影响域，而非直接信任模型的dirty列表；源ID需绑定真实来源与版本，变更授权时按当前有效资格重建；每次现行快照修订撤销旧端口的发布权，计算复用与授权复用分开。与已有v0.8局部结果、证据账本、时效、角色、方法及事务机制对接；原生端口、并发、真机、独立留出仍未执行。研究者选择了8槽、有限位宽、12编辑和固定种子，未调整产品方向、工作流、交接、冻结、证据等级，未修改生产、训练、合并、部署、主动CI或增加费用。
## 复算
将固定前轮报告作为唯一参数传入Node下列程序（实际连接器已执行，未跑Node CLI包装）。只执行已经审阅、固定身份的自有研究源码，不允许生产执行任意外部文档。
```js
const fs=require("node:fs");
const source=fs.readFileSync(process.argv[2],"utf8").split("\`\`\`js\n")[1].split("\n\`\`\`")[0];
const core=source.slice(source.indexOf("function experiment(){")+"function experiment(){".length,source.indexOf(" const out={cases:"));
const makeCore=Function(core+"\nreturn {close,verify,ref,status};");
function experiment2(makeCore){
 const {close,verify,ref,status}=makeCore(),N=8;
 const ck=(v,m)=>{if(!v)throw Error(m)},cp=x=>JSON.parse(JSON.stringify(x)),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 let seed=20261127;
 const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 const count=x=>{let n=0;while(x){n+=x&1;x>>>=1}return n};
 const cmp=(a,b)=>a.id<b.id?-1:a.id>b.id?1:0;
 function normalize(x){
  ck(Number.isSafeInteger(x.rev)&&x.rev>=0&&Number.isSafeInteger(x.grant)&&x.grant>=0&&typeof x.scope==="string"&&typeof x.covered==="boolean","context");
  ck(Array.isArray(x.worlds)&&x.worlds.length>=1&&x.worlds.length<=16&&x.worlds.every(i=>typeof i==="string"&&i)&&new Set(x.worlds).size===x.worlds.length,"worlds");
  const w=x.worlds.length,all=(1<<w)-1;
  function rows(a,kind){
   ck(Array.isArray(a)&&new Set(a.map(v=>v.id)).size===a.length,"duplicate id");
   return a.map(v=>{
    ck(typeof v.id==="string"&&v.id&&Number.isSafeInteger(v.version)&&v.version>=0&&Number.isInteger(v.p)&&v.p>=0&&v.p<N&&Number.isInteger(v.mask)&&v.mask>=0&&(v.mask&~all)===0&&Number.isSafeInteger(v.grant)&&typeof v.origin==="string"&&typeof v.scope==="string"&&typeof v.ok==="boolean","row");
    const b=kind==="r"?v.b:[];
    ck(Array.isArray(b)&&b.every(p=>Number.isInteger(p)&&p>=0&&p<N),"body");
    // Scope/authorization eligibility is a fixture, not a source truth inference.
    return {id:v.id,p:v.p,b:[...new Set(b)].sort((a,b)=>a-b),version:v.version,origin:v.origin,grant:v.grant,scope:v.scope,mask:v.ok&&v.grant===x.grant&&v.scope===x.scope?v.mask:0};
   }).sort(cmp)
  }
  return {rev:x.rev,grant:x.grant,scope:x.scope,covered:x.covered,worlds:[...x.worlds],s:rows(x.s,"s"),r:rows(x.r,"r")}
 }
 function toCore(x){return [x.worlds.length,x.s.map(v=>[v.p,v.mask]),x.r.map(v=>[v.p,v.b,v.mask])]}
 function context(a,b){return a.grant===b.grant&&a.scope===b.scope&&eq(a.worlds,b.worlds)}
 function payload(v){return [v.p,v.b,v.version,v.origin,v.grant,v.scope]}
 function diff(a,b){
  const all=(1<<b.worlds.length)-1;
  if(!context(a,b))return all;
  let d=0;
  for(const k of ["s","r"]){
   const am=new Map(a[k].map(x=>[x.id,x])),bm=new Map(b[k].map(x=>[x.id,x]));
   for(const id of new Set([...am.keys(),...bm.keys()])){
    const x=am.get(id),y=bm.get(id);
    if(!x||!y)d|=(x?.mask??0)|(y?.mask??0);
    else if(eq(payload(x),payload(y)))d|=x.mask^y.mask;
    else d|=x.mask|y.mask;
   }
  }
  return d;
 }
 // Independent conservative per-world active descriptor comparison.
 function oracleDiff(a,b){
  if(!context(a,b))return (1<<b.worlds.length)-1;
  let d=0;
  for(let i=0;i<b.worlds.length;i++){
   const bit=1<<i;
   function active(x){return ["s","r"].map(k=>x[k].filter(z=>z.mask&bit).map(z=>[z.id,...payload(z)]))}
   if(!eq(active(a),active(b)))d|=bit;
  }return d;
 }
 function initial(raw){const snap=normalize(raw),z=close(...toCore(snap));return {snap,z,dirty:(1<<snap.worlds.length)-1,full:true}}
 function advance(old,raw){
  const snap=normalize(raw);
  ck(old.z.done&&snap.rev>old.snap.rev,"stale revision");
  const dirty=diff(old.snap,snap),all=(1<<snap.worlds.length)-1;
  if(dirty===all)return {snap,z:close(...toCore(snap)),dirty,full:true};
  const prior=cp(old.z);
  // Preserve unchanged-world witness identity after canonical array insert/delete.
  const maps=Object.fromEntries(["s","r"].map(k=>[k,new Map(snap[k].map((v,i)=>[v.id,i]))]));
  for(let p=0;p<N;p++)for(let i=0;i<snap.worlds.length;i++){
   const bit=1<<i,t=prior.trace[p][i];
   if(dirty&bit){prior.trace[p][i]=null;continue}
   if(t){const v=old.snap[t[0]][t[1]],idx=maps[t[0]].get(v.id);ck(idx!==undefined,"remap disappeared");prior.trace[p][i]=[t[0],idx]}
  }
  const z=close(...toCore(snap),Infinity,prior,dirty);
  return {snap,z,dirty,full:false};
 }
 function receipt(state,p){
  return {rev:state.snap.rev,grant:state.snap.grant,scope:state.snap.scope,worlds:cp(state.snap.worlds),covered:state.snap.covered,p,status:status(state.z.a,p,(1<<state.snap.worlds.length)-1,state.z.done,state.snap.covered),authority:"NONE"};
 }
 function current(rec,state){
  return rec&&eq(rec,receipt(state,rec.p));
 }
 const out={graphs:0,transitions:0,dirtyWorlds:0,fullWorlds:0,zeroDirty:0,partialDirty:0,fullDirty:0,proofChecks:0,scanIncremental:0,scanFull:0,valueUnchangedButDirty:0,staleReceiptsRejected:0,scopeGenerationTransitions:0,coveredChanges:0,controls:0,events:{}};
 function checkAdvance(a,b){
  const z=advance(a,b),full=initial(b);
  ck(z.dirty===oracleDiff(a.snap,z.snap),"diff oracle");
  ck(eq(z.z.a,full.z.a)&&eq(z.z.a,ref(...toCore(z.snap))),"closure oracle");
  out.proofChecks+=verify(...toCore(z.snap),z.z);
  out.transitions++;const w=z.snap.worlds.length,all=(1<<w)-1;
  out.fullWorlds+=w;out.dirtyWorlds+=count(z.dirty);out.zeroDirty+=+(z.dirty===0);out.partialDirty+=+(z.dirty!==0&&z.dirty!==all);out.fullDirty+=+(z.dirty===all);
  out.scanIncremental+=z.z.scans;out.scanFull+=full.z.scans;
  if(eq(a.z.a,z.z.a)&&z.dirty)out.valueUnchangedButDirty++;
  for(let p=0;p<4;p++){
   const old=receipt(a,p),fresh=receipt(z,p);
   ck(!current(old,z)&&current(fresh,z),"publication identity");out.staleReceiptsRejected++;
  }
  return z;
 }
 function row(id,scope,grant,all,kind){
  const v={id,p:rnd(N),version:0,origin:"origin"+rnd(4),grant,scope,mask:rnd(all+1),ok:true};
  if(kind==="r")v.b=Array.from({length:1+rnd(3)},()=>rnd(N));
  return v;
 }
 for(let c=0;c<600;c++){
  const w=2+rnd(7),all=(1<<w)-1;
  let raw={rev:0,grant:0,scope:"purpose0",covered:true,worlds:Array.from({length:w},(_,i)=>"w"+i),s:Array.from({length:4+rnd(6)},(_,i)=>row("s"+i,"purpose0",0,all,"s")),r:Array.from({length:6+rnd(10)},(_,i)=>row("r"+i,"purpose0",0,all,"r"))};
  let a=initial(raw);out.graphs++;
  for(let j=0;j<18;j++){
   raw=cp(raw);raw.rev++;
   const k=rnd(2)?"s":"r",list=raw[k],idx=rnd(list.length),v=list[idx],op=rnd(12);
   if(op===0&&v)v.mask^=1<<rnd(w);
   if(op===1&&v){v.version++;v.origin="revised"+j}
   if(op===2&&v){v.p=rnd(N);v.version++}
   if(op===3&&v)v.ok=!v.ok;
   if(op===4&&v)list.splice(idx,1);
   if(op===5)list.push(row(k+"new"+j,raw.scope,raw.grant,all,k));
   if(op===6)list.reverse();
   if(op===7){raw.grant++;out.scopeGenerationTransitions++}
   if(op===8){raw.scope="purpose"+(j+1);out.scopeGenerationTransitions++}
   if(op===9&&v){v.grant=raw.grant;v.scope=raw.scope;v.version++}
   if(op===10){raw.covered=!raw.covered;out.coveredChanges++}
   if(op===11){raw.worlds.reverse()}
   out.events[op]=(out.events[op]||0)+1;
   a=checkAdvance(a,raw);
  }
 }
 const control=(v,m)=>{ck(v,m);out.controls++};
 const v={id:"z",p:0,version:0,origin:"a",grant:0,scope:"p",mask:1,ok:true};
 let raw={rev:0,grant:0,scope:"p",covered:true,worlds:["x","y"],s:[v],r:[]};
 let a=initial(raw),b=cp(raw);b.rev++;b.s.unshift({...v,id:"a",mask:0});
 let z=advance(a,b);control(z.dirty===0&&z.z.trace[0][0][1]===1&&verify(...toCore(z.snap),z.z)===1,"inactive insert remap");
 b=cp(raw);b.rev++;b.s[0].version++;z=advance(a,b);control(z.dirty===1&&eq(z.z.a,a.z.a),"same value new origin");
 b=cp(raw);b.rev++;b.grant++;z=advance(a,b);control(z.z.a.every(x=>!x),"grant no old evidence");
 b.rev++;b.grant=2;z=advance(z,b);control(z.z.a.every(x=>!x),"new grant no automatic revival");
 b=cp(raw);b.rev++;b.covered=false;z=advance(a,b);control(z.dirty===0&&!current(receipt(a,0),z)&&receipt(z,0).status==="UNRESOLVED","coverage independent");
 b=cp(raw);b.rev++;b.worlds.reverse();z=advance(a,b);control(z.full&&z.dirty===3,"world order identity rebuild");
 for(const mutate of [x=>{x.rev=0},x=>{x.s.push(cp(x.s[0]))},x=>{x.s[0].mask=8},x=>{x.worlds=["x","x"]},x=>{x.s[0].version=-1}]){
  b=cp(raw);b.rev++;mutate(b);let fail=false;try{advance(a,b)}catch(e){fail=true}control(fail,"invalid input");
 }
 return out;
}
console.log(JSON.stringify(experiment2(makeCore),null,2));
```
