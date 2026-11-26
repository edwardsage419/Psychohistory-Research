# 自主决策：主体资源资格、共享容量流与共同固定方案证书
2026-11-26。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线与查重
起点main 2eb71c5816fa4090d410b9edd1ba9a74e27e9482，核对25近期提交、15开放PR、v3.2全文、同步规程、唯一交接固定blob 5e74f4f0b37141d631740e844ad8bbbfed232e07前段，#63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft。实际读主体研究4c85af379a2f47b393a6bd070eab9cd4170786f5、条件实例f59f7ae7a2d3a8ea2e24d7bb4d8e3df590648644、数值投影e9290c4efda30628dfbd8d76691d3f1f7fee7669、C035 4f2c077e297a4b2733fa26309c99a510329ec6f4、联合政策5fed5e9108fbc97257fbf0546d521aa3cf725769和V08_COMPOSITION a602867cb0ff640f3c585d6bb46890a27a6567bc相关段落；R119历史blob读取404；共享资源和identity partition代码搜索无结果，查重有限。已有联合硬约束、跨世界统一解释、共享资源与非预知动态规划不重复计为发明。本轮新增给定主体使用资格网络时的整数流/割见证、可变权限图下共同固定分配方案的精确交集及局部重算；不是新最大流理论。公开一手来源Ford & Fulkerson (1956), Maximal Flow Through a Network, DOI https://doi.org/10.4153/CJM-1956-045-5，核对出版者索引及搜索摘要，未全文逐页审阅或复制原文。下列代码原创，未训练或使用第三方AI运行时。
## 形式合同
已确认的需求实例i具有固定整数需求d_i，资源池j具有唯一稳定身份与同量纲、同时间窗口可用余量c_j(w)，每个联合可能世界w具备使用资格边E(w)。同一池的多来源记录不得重复累计；本实验容量已由可信宿主去重和核对，未实现真实身份合并、主体授权或语言识别。需求由可拆分整数单位组成，允许同一任务分配多个池；不可拆分任务、时间连续性、切换成本、不同单位、未知容量、跨时段和多商品约束不适用。人工给定零需求表示明确的零，不以未知默认零。所有结果只读authority NONE；明确不允许以流存在替代其他底线、行动授权或个人价值。
网络源到需求节点容量d_i，资格边容量D+1（D=sum d_i），池到汇容量c_j。最大流值D等价于满足全部需求的分配。残余图可达割产生上界；验证原始分配的非负整数、行需求、列容量、使用资格以及割容量等于流值，给出可复算证书。独立子集参照：任意任务子集A需量d(A)不得超过其可达池容量c(N(A))；最大未满足量为max(0,max_A[d(A)-c(N(A))])。理由：最小割不会割断D+1的资格边（存在容量D的源割），对需求侧子集取其所有相邻池即可给出最小对应割；等式随最大流最小割定理成立。第三路线直接枚举每个整数单位的可用池分配，不调用流或割。
每个可能世界有方案（对每w存在x_w）与存在一个现在即可固定的共同方案（存在x对所有w成立）区别。若需求量、任务及池身份固定，所有世界都认可同一分配x的条件正好是每池容量取最小、每需求资格边取交集，故共同方案可用单次流精确检验。没有共同固定方案不意味着每世界不可行；只有观察或确认真实世界后允许调整且实际信息/时序与成本合格，才可能采用条件分配。不得以跨世界资格并集、第一世界或逐世界各自最优替代共同方案。覆盖未证实只展示已知域见证，端口UNKNOWN_COVERAGE；空域拒绝。未知容量或资格须由宿主保留未知、不可将缺失资格等同已确认无权。本研究未实现真实资格生成。
## 实验
连接器标准JS实际执行两次，结果一致。2304项穷尽双需求双资源嵌入3x3的有限合同（需求0..2、容量0..3、资格掩码0..3），三条路线对照；1500个固定种子多世界图，2..6世界、三个需求每项1..2单位、三个池容量0..4、资格掩码0..7。逐世界及共同方案以流证书、子集参照、单位分配穷举核对；分别统计总容量、单任务容量、资格并集和第一世界错误基线。每个多世界图6次单世界改动，重用其余世界结果，核对全量计算与共同输入是否未变。缓存仅固定数组夹具，未实现安全版本凭证、来源撤回或并发；规则扫描/世界数量不能替代墙时。7项控制（交换资格、共享瓶颈、增广重排、明确零、非法容量/资格、空域）。数值为合成组合与重复世界，不是真实用户、原生错误率或独立验收。
```json
{
  "singleCases": 2304,
  "subsetChecks": 9837,
  "bruteChecks": 9837,
  "cutChecks": 9837,
  "worldCases": 1500,
  "worldFlowChecks": 6033,
  "commonChecks": 1500,
  "adaptiveOnly": 54,
  "sumCapacityFalsePass": 2593,
  "individualFalsePass": 534,
  "unionAccessFalsePass": 196,
  "firstWorldFalseCommon": 550,
  "incompleteControls": 1500,
  "updates": 9000,
  "recomputedWorlds": 9000,
  "fullWorlds": 36198,
  "commonUnchanged": 2554,
  "controls": 7,
  "ports": {
    "MIXED": 1082,
    "NO_WORLD_HAS_PLAN": 354,
    "EVERY_WORLD_HAS_PLAN": 64
  }
}
```
## 接入
ActorResourceScope绑定精确主体、需求实例、资源池ID、用途、时域、单位、来源版本和使用资格；资源余量须经实际确认，明确需求是否可拆分。原文主体候选仍由可信宿主确认，前轮数值投影在相同资源身份内核对证据，条件实例决定需求何时生效；本研究固定需求，变化需求不得直接沿用共同方案公式。输出共同固定方案、逐世界可行性、缺额与瓶颈集合，供数学硬门及长期计划只读研究接口。下一阶段须处理重复资源报告/预留身份、源改版及不完全观测下能否选择不同方案，另行独立验收。未修改原生、交接、冻结、证据等级、PR、训练、部署、主动CI或费用。研究者选择整数可拆分模型、规模、种子、基线及编辑合同。
## 复算
标准JS（连接器执行两次；Node包装未执行）。
```js
function experiment(){
 const ck=(b,m)=>{if(!b)throw Error(m)},sum=a=>a.reduce((x,y)=>x+y,0),N=3,P=3,ALL=7,eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 let seed=20261126;
 const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 function validate(d,w){
  ck(d.length===N&&d.every(x=>Number.isSafeInteger(x)&&x>=0&&x<=3),"demands");
  ck(w.c.length===P&&w.c.every(x=>Number.isSafeInteger(x)&&x>=0&&x<=9),"capacity");
  ck(w.e.length===N&&w.e.every(x=>Number.isInteger(x)&&x>=0&&x<=ALL),"eligibility");
 }
 // Finite, divisible integer quanta; a task can draw from multiple eligible pools.
 function flow(d,w){
  validate(d,w);
  const T=sum(d),S=0,Z=N+P+1,K=Z+1;
  let cap=Array.from({length:K},()=>Array(K).fill(0));
  for(let i=0;i<N;i++){
   cap[S][1+i]=d[i];
   for(let j=0;j<P;j++)if(w.e[i]&(1<<j))cap[1+i][1+N+j]=T+1;
  }
  for(let j=0;j<P;j++)cap[1+N+j][Z]=w.c[j];
  let res=cap.map(x=>x.slice()),f=0,aug=0;
  function search(){
   let p=Array(K).fill(-1),q=[S];p[S]=S;
   for(let k=0;k<q.length;k++)for(let j=0;j<K;j++)if(p[j]<0&&res[q[k]][j]>0){p[j]=q[k];q.push(j)}
   return p;
  }
  for(;;){
   let p=search();if(p[Z]<0){
    let cut=p.map(x=>x>=0),cutValue=0;
    for(let i=0;i<K;i++)for(let j=0;j<K;j++)if(cut[i]&&!cut[j])cutValue+=cap[i][j];
    let x=Array.from({length:N},(_,i)=>Array.from({length:P},(_,j)=>cap[i+1][N+1+j]-res[i+1][N+1+j]));
    return {f,x,cut,cutValue,aug};
   }
   let v=Infinity;
   for(let j=Z;j!==S;j=p[j])v=Math.min(v,res[p[j]][j]);
   ck(v>0&&Number.isSafeInteger(v),"augmentation");
   for(let j=Z;j!==S;j=p[j]){res[p[j]][j]-=v;res[j][p[j]]+=v;}
   f+=v;aug++;
  }
 }
 function witness(d,w,x,exact=true){
  if(x.length!==N||x.some((r,i)=>r.length!==P||r.some((v,j)=>!Number.isSafeInteger(v)||v<0||v>0&&!(w.e[i]&(1<<j)))||(exact?sum(r)!==d[i]:sum(r)>d[i])))return false;
  return w.c.every((v,j)=>sum(x.map(r=>r[j]))<=v);
 }
 // Independent subset bottleneck reference: max served = total demand - largest deficit.
 function subset(d,w){
  let deficit=0,best=0;
  for(let m=1;m<1<<N;m++){
   let need=0,eligible=0;
   for(let i=0;i<N;i++)if(m&(1<<i)){need+=d[i];eligible|=w.e[i]}
   let avail=sum(w.c.filter((v,j)=>eligible&(1<<j)));
   if(need-avail>deficit){deficit=need-avail;best=m}
  }
  return {f:sum(d)-deficit,deficit,best};
 }
 function verify(d,w,z){
  ck(witness(d,w,z.x,false)&&sum(z.x.map(sum))===z.f,"primal");
  ck(z.cut[0]&&!z.cut.at(-1),"cut ends");
  let c=0;
  for(let i=0;i<N;i++){if(!z.cut[i+1])c+=d[i];for(let j=0;j<P;j++)if(z.cut[i+1]&&!z.cut[N+1+j]&&(w.e[i]&(1<<j)))c+=sum(d)+1;}
  for(let j=0;j<P;j++)if(z.cut[N+1+j])c+=w.c[j];
  ck(c===z.cutValue&&c===z.f,"dual");
  ck(z.f===subset(d,w).f,"subset reference");
  return z.f===sum(d);
 }
 // Third route: enumerate assignments of each mandatory unit.
 function brute(d,worlds){
  let units=[];for(let i=0;i<N;i++)for(let k=0;k<d[i];k++)units.push(i);
  let x=Array.from({length:N},()=>Array(P).fill(0));
  function dfs(k){
   if(k===units.length)return worlds.every(w=>witness(d,w,x));
   let i=units[k];
   for(let j=0;j<P;j++){x[i][j]++;if(worlds.every(w=>witness(d,w,x,false))&&dfs(k+1))return true;x[i][j]--}
   return false;
  }
  return dfs(0);
 }
 function common(ws){
  ck(ws.length>0,"empty world domain");
  return {c:Array.from({length:P},(_,j)=>Math.min(...ws.map(w=>w.c[j]))),e:Array.from({length:N},(_,i)=>ws.reduce((m,w)=>m&w.e[i],ALL))};
 }
 function ports(d,ws,covered){
  const each=ws.map(w=>{let z=flow(d,w);return {ok:verify(d,w,z),...z}});
  let c=common(ws),z=flow(d,c),robust=verify(d,c,z);
  ck(!robust||each.every(e=>e.ok)&&ws.every(w=>witness(d,w,z.x)),"common witness");
  const yes=each.some(x=>x.ok),no=each.some(x=>!x.ok);
  return {each,common:c,commonFlow:z,robust,worldStatus:!covered?"UNKNOWN_COVERAGE":yes&&no?"MIXED":yes?"EVERY_WORLD_HAS_PLAN":"NO_WORLD_HAS_PLAN",fixedStatus:!covered?"UNKNOWN_COVERAGE":robust?"COMMON_PLAN":"NO_COMMON_PLAN",authority:"NONE"};
 }
 const out={singleCases:0,subsetChecks:0,bruteChecks:0,cutChecks:0,worldCases:0,worldFlowChecks:0,commonChecks:0,adaptiveOnly:0,sumCapacityFalsePass:0,individualFalsePass:0,unionAccessFalsePass:0,firstWorldFalseCommon:0,incompleteControls:0,updates:0,recomputedWorlds:0,fullWorlds:0,commonUnchanged:0,controls:0,ports:{}};
 const control=(v,m)=>{ck(v,m);out.controls++};
 // Exact exhaustive 2 tasks, 2 pools embedded in 3x3, third task/pool unused.
 for(let a=0;a<=2;a++)for(let b=0;b<=2;b++)for(let c=0;c<=3;c++)for(let e=0;e<=3;e++)for(let u=0;u<4;u++)for(let v=0;v<4;v++){
  let d=[a,b,0],w={c:[c,e,0],e:[u,v,0]},z=flow(d,w),ok=verify(d,w,z);
  ck(ok===brute(d,[w]),"full exhaustive");
  out.singleCases++;out.subsetChecks++;out.bruteChecks++;out.cutChecks++;
 }
 function world(){return {c:Array.from({length:P},()=>rand(5)),e:Array.from({length:N},()=>rand(8))}}
 for(let t=0;t<1500;t++){
  let d=Array.from({length:N},()=>1+rand(2)),W=2+rand(5),ws=Array.from({length:W},world);
  let p=ports(d,ws,true);
  ck(p.robust===brute(d,ws),"robust brute");out.bruteChecks++;
  for(let i=0;i<W;i++){
   let ok=p.each[i].ok;ck(ok===brute(d,[ws[i]]),"world brute");out.bruteChecks++;
   let w=ws[i];
   if(sum(w.c)>=sum(d)&&!ok)out.sumCapacityFalsePass++;
   if(d.every((n,k)=>sum(w.c.filter((v,j)=>w.e[k]&(1<<j)))>=n)&&!ok)out.individualFalsePass++;
  }
  out.worldCases++;out.worldFlowChecks+=W;out.commonChecks++;out.subsetChecks+=W+1;out.cutChecks+=W+1;
  if(p.each.every(x=>x.ok)&&!p.robust)out.adaptiveOnly++;
  let optimistic={c:p.common.c,e:Array.from({length:N},(_,i)=>ws.reduce((m,w)=>m|w.e[i],0))};
  if(flow(d,optimistic).f===sum(d)&&!p.robust)out.unionAccessFalsePass++;
  if(p.each[0].ok&&!p.robust)out.firstWorldFalseCommon++;
  out.ports[p.worldStatus]=(out.ports[p.worldStatus]||0)+1;
  // An incomplete finite domain may display specific witnesses only.
  let q=ports(d,ws,false);ck(q.worldStatus==="UNKNOWN_COVERAGE"&&q.fixedStatus==="UNKNOWN_COVERAGE"&&q.authority==="NONE","outside");out.incompleteControls++;
  // Versioned data fixture: one world changes, other world results are reusable.
  let cache=p.each;
  for(let j=0;j<6;j++){
   const k=rand(W),nw=ws.map((w,i)=>i===k?world():w),before=common(ws),after=common(nw);
   let next=cache.slice(),z=flow(d,nw[k]);next[k]={ok:verify(d,nw[k],z),...z};
   let f=ports(d,nw,true);
   ck(eq(next,f.each),"world cache parity");
   for(let i=0;i<W;i++)if(i!==k)ck(next[i]===cache[i],"reuse");
   if(eq(before,after)){ck(eq(flow(d,before),f.commonFlow),"unchanged common inputs");out.commonUnchanged++}
   out.updates++;out.recomputedWorlds++;out.fullWorlds+=W;
   ws=nw;cache=next;
  }
 }
 const a={c:[1,1,0],e:[1,2,0]},b={c:[1,1,0],e:[2,1,0]};
 let z=ports([1,1,0],[a,b],true);
 control(z.each.every(x=>x.ok)&&!z.robust,"adaptive vs fixed");
 z=ports([1,1,0],[{c:[1,1,0],e:[1,1,0]}],true);
 control(z.worldStatus==="NO_WORLD_HAS_PLAN"&&z.each[0].f===1,"shared bottleneck");
 z=ports([1,1,0],[{c:[1,1,0],e:[3,1,0]}],true);
 control(z.robust&&z.commonFlow.x[0][1]===1&&z.commonFlow.x[1][0]===1,"augment reroute");
 control(ports([0,0,0],[{c:[0,0,0],e:[0,0,0]}],true).robust,"zero demand within explicit contract");
 for(const bad of [{c:[-1,0,0],e:[1,1,1]},{c:[1,1,1],e:[8,0,0]}]){let fail=false;try{flow([1,1,1],bad)}catch{fail=true}control(fail,"invalid input")}
 let fail=false;try{common([])}catch{fail=true}control(fail,"empty domain");
 return out;
}
console.log(JSON.stringify(experiment(),null,2));
```
