# 自主认知与科学知识：联合解释域的带符号推理、证据见证与撤回重算
2026-11-26。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。非自然语言正确率、生产接入、正式权限或科学准入。
## 基线与去重
固定main 17ae7c154b348c2147aa90d6469c020915d71a60，核对25近期提交、15开放PR、v3.2全文、同步规程、AGENTS前段、唯一产品交接固定blob 5e74f4f0b37141d631740e844ad8bbbfed232e07前段及#63固定head 734686980b19da9291bdd08b67d4e2519c011acf，未重跑。比较#63交付基线后22份报告，读取联合语义搜索 d827adc15f983c9c66c4f9fb989d2d911b92a9c6、效果等价 18ae7920f9ca317da66d1d50ba7f0fc3d8951c26、条件政策 529750962f2686179703de19e37d5e037fd75d0d、条件时序 52c64f77aae28680aac0e5d53dc692aae8b5dd6c、方法隔离 ae545156e4ed8d39a96f940ab3aaac0b6cecad51、未完成证书 7f37403fc178117f61107833289ad60a15dcc3d7、知识资格 df5a962a58ba0601b6014fad47c39cd3ebdb0e33 报告前段。既有R66正向闭包、R125失效、共同解释和授权规则不重计。本轮新增在同一有限联合解释域内，将正负证据、递归规则适用范围、同世界见证与部分完成、世界局部撤回合为可复算原型。搜索antichain/provenance/paraconsistent/truth maintenance未返回匹配，不能作全库无重复证明。
## 一手来源与原创范围
核对de Kleer 1986 An assumption-based TMS 出版者摘要 https://doi.org/10.1016/0004-3702%2886%2990080-9 （以假设集合组织支持）；Green/Karvounarakis/Tannen 2007 Provenance Semirings 作者论文搜索摘要 https://www.cs.ucdavis.edu/~green/papers/pods07.pdf （来源注释与Datalog）。本轮只核对题名及摘要，不声称逐页复现、取得代码许可或完整ATMS/半环实现；不复制第三方文本/代码。以下算法、夹具、反例均为原创有限研究。
## 合同与数学
可信宿主先给出非空、已编号的联合解释域W，候选本身无权确认W覆盖现实。每个原子用独立正/负支持两个槽；负槽不是缺失正槽。每个合格来源或已授权规则有适用世界集合；此实验以位掩码模拟资格，不推断授权、来源真值、语言解析或现实概率。规则是有限正Horn规则，前件可引用任一符号槽，不含默认否定、缺失即假、反证、经典爆炸、优先规则或反事实因果。固定世界身份、规则/来源槽位及含义，不复用索引代表不同来源。源掩码并集初始化；规则 h<-b1,...,bk 的新支持为 G_r∩S(b1)∩...∩S(bk)，与S(h)取并。每个世界独立递增至最小不动点，最多N×|W|个新增支持；完整扫描无变化才表示完成。证明：每个固定世界的位投影保持并交及规则推导；迭代从来源出发，归纳每个支持可由有限推导获得，闭包稳定时满足全部规则；任一模型包含来源并在每步包含所有新增支持，故闭包为最小模型。允许显式冲突存在，不推出未支持的无关命题。
每个新位保存一个来源或已启用规则的索引见证，规则只可使用已存在支持，首次支持产生有穷无环证明；独立验证器逐递归核对世界、规则头、全部前件及实际来源。仅保存一个有效见证，未计算所有替代证明、最小证明或独立来源数。世界不同的支持可由不同规则导出，逐世界支持全称不能机械要求一个共同来源，也不能将不同世界的前件拼接。相同世界两符号均有支持才是CONFLICT_WITNESS；跨世界正负不同为DIFFERENT_WORLDS（完整且每个世界有一符号）；任一世界两者缺失则UNRESOLVED。只有域覆盖经宿主另证、完整闭包、各世界同符号且无反符号时才可声明有限条件一致支持；不是现实真值、硬门准入或推荐。在预算截断时仅已有冲突见证可以确证，缺反符号不能证明无冲突。覆盖不明仍可展示具体冲突反例，不发布全称。
撤回及来源/规则适用改变：在固定世界及槽位合同下，可信变更掩码D覆盖全部受影响世界；将D内旧支持和旧见证清空，再按新来源/规则对D完整重算，D外旧完整闭包及见证保留。因世界之间没有推导边，D外无改变；D内从底重新获得最小闭包，避免旧循环自证。该程序只接受完整前代，调用方必须保证D覆盖真实变更；真实生产需从版本化差异生成D，绑定原文身份、授权代次、来源资格/时效、用途和规则图版本；世界集或槽位语义变化时全量重建，撤回后新授权需重新核验，不自动沿用旧来源。本实验无授权实现、签名、持久化、原生接口、真实个人数据或训练。算法成本以规则检查次数及位掩码范围报告；每次规则需O(k)位运算，理论最坏迭代随新增支持，见证存储O(N×W)，固定JS位宽上限16；未测Mac/iPhone、墙时、内存或真实语料。
## 实际实验
首轮800组低位取模LCG产生0个池化虚假支持/冲突及0个早期冲突，发现测试覆盖不足，废弃为主结论（保留该负面诊断，不合并计数）。改为同固定seed的高位缩放、1200合成图、8符号槽、2至8世界、4至12来源、8至24规则，前件1至3槽，随机来源及规则世界掩码。每图比较按世界的独立集合规则闭包，前200图另枚举所有256候选原子集合、取满足来源和规则的模型交集。节点预算0/1/4/12/32/96为规则扫描帽，初始来源免费，检查部分闭包单调、最终一致性和已有见证。每图10次单世界来源/规则掩码翻转，比较选择性重算、全量位掩码闭包和逐世界参照，同时验证全部存留见证及未受影响世界。9项控制含替代证明、跨世界符号、假合取、撤回循环、不爆炸、截断、覆盖未知、伪造索引、早期冲突。两个故意错误基线分别池化任何世界出现的来源和规则、只保留所有世界共同出现的来源和规则；计数是原子/命题/端口重复结构，非真实系统错误率或独立样本。主实验完整实际执行两次，结果一致。
```json
{
  "cases": 1200,
  "modelChecks": 200,
  "worldAtomChecks": 48208,
  "proofChecks": 416157,
  "partialChecks": 28800,
  "earlyConflict": 9461,
  "pooledFalseSupport": 387,
  "pooledFalseConflict": 495,
  "universalMiss": 1180,
  "updates": 12000,
  "updateWorlds": 12000,
  "fullWorlds": 60260,
  "unchangedWorldChecks": 386080,
  "incrementalScans": 338189,
  "fullScans": 466604,
  "controls": 9,
  "statuses": {
    "CONFLICT_WITNESS": 3011,
    "ALL_POS": 155,
    "ALL_NEG": 160,
    "UNRESOLVED": 1414,
    "DIFFERENT_WORLDS": 60
  }
}
```
## 接入与下一责任
建议研究端口WorldSupportClosure、SignedEvidenceWitness、WorldScopedRetraction及完整性/覆盖独立标志。复用现有v0.8原文候选、知识资格、当前性、会话实例、局部分析、数学硬门及历史账本；先将原文候选的作用域/主体/条件/时点/修订目标投影到同一受信世界域，再在独立参数资格内调用数学。不得使用本闭包越过用户确认或把任意语言候选作为可信事实。下一阶段需要实测原生有限解释域到证据端口、覆盖丢失与来源/权限变更的生产级验证；独立轨保管未见样本。研究者自主选择图规模、随机种子、规则语义和预算；未更改生产、交接、历史冻结、证据等级、PR、训练、部署、CI或费用。
## 完整复算
以下标准JS在连接器执行两次，使用Node同语法可运行但本轮未执行Node CLI。
```js
function experiment(){
 const ck=(x,m)=>{if(!x)throw Error(m)}, N=8;
 let seed=20261126;
 const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 const eq=(a,b)=>a.length===b.length&&a.every((v,i)=>v===b[i]);
 const clone=x=>JSON.parse(JSON.stringify(x));
 function close(w,s,r,cap=Infinity,prior=null,dirty=null){
  const all=(1<<w)-1,d=dirty===null?all:dirty;
  ck(w>=1&&w<=16&&d>=0&&(d&~all)===0&&(!prior?d===all:prior.done),"scope");
  let a=prior?prior.a.map(x=>x&~d):Array(N).fill(0);
  let trace=prior?clone(prior.trace):Array.from({length:N},()=>Array(w).fill(null));
  for(let p=0;p<N;p++)for(let i=0;i<w;i++)if(d&(1<<i))trace[p][i]=null;
  let scans=0,rounds=0;
  function add(p,v,proof){
   const fresh=v&~a[p];a[p]|=v;
   for(let i=0;i<w;i++)if(fresh&(1<<i))trace[p][i]=proof;
   return !!fresh;
  }
  s.forEach(([p,m],k)=>add(p,m&d,["s",k]));
  if(!d)return {a,trace,done:true,scans,rounds};
  for(let changed=true;changed;){
   changed=false;
   for(let k=0;k<r.length;k++){
    if(scans===cap)return {a,trace,done:false,scans,rounds};
    scans++;let [h,b,m]=r[k],v=m&d;for(const p of b)v&=a[p];
    if(add(h,v,["r",k]))changed=true;
   }
   rounds++;
  }
  return {a,trace,done:true,scans,rounds};
 }
 function verify(w,s,r,z){
  let count=0;
  for(let i=0;i<w;i++){
   let bit=1<<i,seen=new Set(),active=new Set();
   function proof(p){
    if(seen.has(p))return;
    ck(!active.has(p),"cycle in proof");active.add(p);
    const t=z.trace[p][i];ck(t&&t.length===2,"missing proof");
    if(t[0]==="s"){const q=s[t[1]];ck(q&&q[0]===p&&(q[1]&bit),"source proof");}
    else{ck(t[0]==="r","proof kind");const q=r[t[1]];ck(q&&q[0]===p&&(q[2]&bit),"rule proof");for(const b of q[1]){ck(z.a[b]&bit,"missing premise");proof(b)}}
    active.delete(p);seen.add(p);
   }
   for(let p=0;p<N;p++)if(z.a[p]&bit){proof(p);count++}else ck(z.trace[p][i]===null,"unsupported trace");
  }return count;
 }
 function ref(w,s,r){
  const a=Array(N).fill(0);
  for(let i=0;i<w;i++){
   const bit=1<<i, active=new Set(s.filter(x=>x[1]&bit).map(x=>x[0]));
   let left=r.filter(x=>x[2]&bit).slice();
   for(;;){
    const ready=left.filter(x=>x[1].every(p=>active.has(p)));
    if(!ready.length)break;
    for(const x of ready)active.add(x[0]);
    left=left.filter(x=>!ready.includes(x));
   }
   for(const p of active)a[p]|=bit;
  }return a;
 }
 function modelRef(w,s,r){
  let a=Array(N).fill(0);
  for(let i=0;i<w;i++){
   const bit=1<<i;let both=(1<<N)-1;
   for(let m=0;m<(1<<N);m++){
    if(s.some(([p,v])=>(v&bit)&&!(m&(1<<p))))continue;
    if(r.some(([h,b,v])=>(v&bit)&&b.every(p=>m&(1<<p))&&!(m&(1<<h))))continue;
    both&=m;
   }
   for(let p=0;p<N;p++)if(both&(1<<p))a[p]|=bit;
  }return a;
 }
 function status(a,p,all,done,covered=true){
  let x=a[p*2],y=a[p*2+1];
  if(x&y)return "CONFLICT_WITNESS";
  if(!done||!covered)return "UNRESOLVED";
  if(x===all&&!y)return "ALL_POS";
  if(y===all&&!x)return "ALL_NEG";
  if((x|y)===all)return "DIFFERENT_WORLDS";
  return "UNRESOLVED";
 }
 const out={cases:0,modelChecks:0,worldAtomChecks:0,proofChecks:0,partialChecks:0,earlyConflict:0,pooledFalseSupport:0,pooledFalseConflict:0,universalMiss:0,updates:0,updateWorlds:0,fullWorlds:0,unchangedWorldChecks:0,incrementalScans:0,fullScans:0,controls:0,statuses:{}};
 const control=(x,m)=>{ck(x,m);out.controls++};
 const s0=[[2,1],[4,2]],r0=[[0,[2],3],[0,[4],3]];
 control(status(close(2,s0,r0).a,0,3,true)==="ALL_POS","alternate proof");
 control(status(close(2,[[0,1],[1,2]],[]).a,0,3,true)==="DIFFERENT_WORLDS","cross-world signs");
 control(close(2,[[2,1],[4,2]],[[0,[2,4],3]]).a[0]===0,"cross-world join");
 const rr=[[2,[0],1],[0,[2],1]],old=close(1,[[0,1]],rr);
 control(old.a[0]===1&&old.a[2]===1&&close(1,[[0,0]],rr,Infinity,old,1).a.every(x=>x===0),"cycle");
 control(close(1,[[0,1],[1,1]],[]).a[2]===0,"no explosion");
 control(status([1,0,0,0,0,0,0,0],0,1,false)==="UNRESOLVED","partial absence");
 control(status([1,0,0,0,0,0,0,0],0,1,true,false)==="UNRESOLVED","outside coverage");
 let z=close(1,[[0,1]],[[2,[0],1]]);
 let bad=clone(z);bad.trace[2][0]=["r",999];
 let rejected=false;try{verify(1,[[0,1]],[[2,[0],1]],bad)}catch(e){rejected=true}
 control(rejected,"tampered proof");
 control(status(close(1,[[0,1],[1,1]],[[2,[0],1]],0).a,0,1,false)==="CONFLICT_WITNESS","early conflict");
 for(let c=0;c<1200;c++){
  const w=2+rand(7),all=(1<<w)-1;
  let s=Array.from({length:4+rand(9)},()=>[rand(N),rand(all+1)]);
  let r=Array.from({length:8+rand(17)},()=>[rand(N),Array.from({length:1+rand(3)},()=>rand(N)),rand(all+1)]);
  const exact=close(w,s,r),v=ref(w,s,r);
  ck(exact.done&&eq(exact.a,v),"reference");out.cases++;out.worldAtomChecks+=w*N;
  out.proofChecks+=verify(w,s,r,exact);
  if(c<200){ck(eq(v,modelRef(w,s,r)),"model intersection");out.modelChecks++}
  const pooled=close(1,s.map(([p,m])=>[p,+!!m]),r.map(([h,b,m])=>[h,b,+!!m])).a;
  const universal=close(1,s.map(([p,m])=>[p,+(m===all)]),r.map(([h,b,m])=>[h,b,+(m===all)])).a;
  for(let p=0;p<N;p++){
   if(pooled[p]&&!v[p])out.pooledFalseSupport++;
   if(v[p]===all&&!universal[p])out.universalMiss++;
  }
  for(let p=0;p<N/2;p++){
   if(pooled[2*p]&&pooled[2*p+1]&&!(v[2*p]&v[2*p+1]))out.pooledFalseConflict++;
   const q=status(v,p,all,true);out.statuses[q]=(out.statuses[q]||0)+1;
  }
  let prev=Array(N).fill(0);
  for(const cap of [0,1,4,12,32,96]){
   const z=close(w,s,r,cap);out.proofChecks+=verify(w,s,r,z);
   ck(z.a.every((x,i)=>(x&~v[i])===0&&(prev[i]&~x)===0),"partial subset monotone");
   if(z.done)ck(eq(z.a,v),"complete");
   for(let p=0;p<N/2;p++){
    const q=status(z.a,p,all,z.done);
    if(q!=="UNRESOLVED")ck(q===status(v,p,all,true),"early status");
    if(!z.done&&q==="CONFLICT_WITNESS")out.earlyConflict++;
    out.partialChecks++;
   }
   prev=z.a;
  }
  let last=exact;
  for(let j=0;j<10;j++){
   let bit=1<<rand(w);
   if(j%2===0){let k=rand(s.length);s[k]=[s[k][0],s[k][1]^bit]}
   else{let k=rand(r.length);r[k]=[r[k][0],r[k][1],r[k][2]^bit]}
   const inc=close(w,s,r,Infinity,last,bit),full=close(w,s,r);
   ck(inc.done&&eq(inc.a,full.a)&&eq(inc.a,ref(w,s,r)),"selective reclosure");
   ck(inc.a.every((x,i)=>(x&~bit)===(last.a[i]&~bit)),"untouched world");
   out.proofChecks+=verify(w,s,r,inc);
   out.updates++;out.updateWorlds++;out.fullWorlds+=w;out.unchangedWorldChecks+=(w-1)*N;
   out.incrementalScans+=inc.scans;out.fullScans+=full.scans;
   last=inc;
  }
 }
 return out;
}
console.log(JSON.stringify(experiment(),null,2));
```
