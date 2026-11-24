# 第46轮：模型分歧、最大相容假设分支与证据身份隔离
2026-11-24。固定 main f211f008f3a3caf7b2dbaa66271562d92f07467e；PR #61 HEAD 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，open Draft。核对v3.1、AGENTS、同步规程、近期提交、开放PR、唯一协调交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第4/27/38/39/45轮。原生 decision_planner.py blob f2d3d21b853afe9dc757a33e83cd3d6160f8dd7b 的 _model_disagreements 已展示不同领导集合与规则分歧、建议核查口径，非现有产品错误证明。第39轮已有差分约束与单个包含最小冲突核；第38轮已有准则共同领先与重复投票反例。本轮处理同一可比世界域上可撤销、尚未核实的假设集合，枚举全部最大相容组合与全部包含最小冲突核，比较任意最大基数组合选择、重复假设与条件性结论。关键词 maximal consistent/minimal correction/model conflict/assumption conflict/truth maintenance 未找到同一提交，不能证明全库无重复。纯原创有限演算，无新增外部来源主张。
## 数学合同
固定非空有限世界域F，表示已获资格的共同事实及已确认的联合结构。每项可撤销假设c_i为同一可比域中的约束支持集合；只有身份、版本、口径及语义明确时才可组合，模型的数值点预测、普通置信区间、相异准则或互斥模型结构不能默认解释为确定支持。用户偏好、硬底线、重要授权不得作为可删除假设。F空时报告事实冲突并停止该域，不能自动撤销事实或真空推理。已确认的模型互斥、依赖和联合可行域必须先编码，不能用本轮任意可兼容集合替代。没有事实覆盖时F不能凭空有限化。
对于可撤销假设的索引子集S，定义 W(S)=F∩交集_{i∈S}c_i，空假设的交集取全域。相容 iff W(S)非空。包含最大相容集合是无法再加入任一其余假设的相容S，未必最大基数。包含最小冲突集合是W(S)为空而每个严格子集相容；至少一项有问题，不指认哪项错误。事实不参与任意删除。每个w∈F的真值签名 J(w)={i:w∈c_i}；S相容 iff 存在w使S⊆J(w)。故所有包含最大相容集合正好是不同签名的包含最大元素。证明：相容S有一个签名超集，最大性强制相等；最大签名的任何严格超集均无世界见证。W(S)在最大S时恰为签名等于S的世界；联合B为这些世界的并集。每条最小冲突核为所有不相容集合的一个生成子集；有限条件保证任何不相容集合包含某个最小核。
对任一已经限定口径的二元查询q，若B⊆q则在全部最大相容分支中为真，若B∩q为空则在全部分支中为假，否则UNKNOWN。必须保留每个分支的条件和冲突原因。最大相容分支策略本身只是条件推理规则：它会删除仅满足非最大签名的事实允许世界；不能宣称真实世界必满足某一最大组合。无独立证据支持此额外覆盖假设时，无条件查询只能在F上判定；B上确定的结论若F上未知，仍只能条件呈现。若用户只确认某一假设范围，则仅在其支持非空且获资格时计算，不自动使用最大相容策略。不同分支的效用或评价标准不可比时不做数值平均。分支安全保证依赖全部实际允许世界而非仅最优假设组合；任何必需模型缺失或不适用仍要显式说明。
完全相同的约束副本不会改变签名包含关系，最大分支世界并集不变；按最大基数或票数选择可因复制改变。来源同一不代表每条不同主张相同；语义相同也不代表外部来源独立。身份去重必须以稳定来源/版本/主张及内容绑定；同身份不同内容报告冲突，不能默默取最后值。不得把多个相关模型的置信度相乘。
## 实验
4个抽象世界，15个非空事实支持域，三个可撤销约束各15个非空支持，50625组；每组直接穷举8个假设子集，与最大签名算法对照全部最大集合及分支世界并集；核查最小冲突核及对所有子集的完备性；16种二元查询逐一比较所有分支、联合B与事实F。最大基数基线保留所有同基数最大集合（非随意打破平局），复制第一个假设后以额外一票重算。cardinalityLoss统计仅按最大基数漏掉相容分支世界；cloneBias为复制使最大基数世界并集改变；arbitraryCertainty为最大基数基线确定、全部最大分支仍未知的查询次数；unsupportedFactual为全部最大分支确定、事实F仍未知的查询次数，明确条件性结论的边界。另核对空事实域、重复身份与冲突身份。计数为合成枚举频数，查询重复不是独立案例。两算法同一研究者设计，非独立科学验收。
```js
function experiment(){
 const check=(v,m)=>{if(!v)throw Error(m)};
 const masks=Array.from({length:16},(_,i)=>i),nonempty=masks.slice(1);
 const pop=m=>m.toString(2).split("1").length-1;
 const union=xs=>xs.reduce((a,b)=>a|b,0);
 const subset=(a,b)=>(a&b)===a;
 const maximal=xs=>xs.filter(a=>!xs.some(b=>a!==b&&subset(a,b)));
 const minimal=xs=>xs.filter(a=>!xs.some(b=>a!==b&&subset(b,a)));
 const status=(w,q)=>!w?"CONFLICT":!(w&q)?"FALSE":subset(w,q)?"TRUE":"UNKNOWN";
 let cases=0,conflicts=0,multi=0,subsetChecks=0,coreChecks=0,queryChecks=0,cloneChecks=0,cloneBias=0,cardinalityLoss=0,arbitraryCertainty=0,unsupportedFactual=0,conditionalCertainty=0,conditionalUnknown=0,emptyBaseControls=0;
 let witness=null,cloneWitness=null;
 for(const F of nonempty)for(const x of nonempty)for(const y of nonempty)for(const z of nonempty){
  cases++;const C=[x,y,z],worlds=nonempty.filter(w=>pop(w)===1&&subset(w,F));
  // Candidate: truth signatures of each factual world; maximal patterns encode all maximal compatible bundles.
  const sig=worlds.map(w=>C.reduce((m,c,i)=>m|(subset(w,c)?1<<i:0),0));
  const M=maximal([...new Set(sig)]);
  const B=union(worlds.filter((w,i)=>M.includes(sig[i])));
  // Reference: directly enumerate every retained assumption subset and intersect supports with fixed facts.
  const support=s=>C.reduce((w,c,i)=>s&(1<<i)?w&c:w,F);
  const feasible=masks.slice(0,8).filter(s=>support(s));
  const ref=maximal(feasible);
  check(M.slice().sort().join()===ref.join(),"all maximal bundles");
  check(B===union(ref.map(support)),"repair world union");subsetChecks+=8;
  const cores=minimal(masks.slice(1,8).filter(s=>!support(s)));
  for(const c of cores){
   check(!support(c)&&[0,1,2].every(i=>!(c&(1<<i))||support(c^(1<<i))),"minimal conflict");coreChecks++;
  }
  for(const s of masks.slice(0,8))check(!support(s)===cores.some(c=>subset(c,s)),"conflict completeness");
  if(!support(7))conflicts++;
  if(M.length>1)multi++;
  const card=ref.filter(s=>pop(s)===Math.max(...ref.map(pop)));
  const cardWorld=union(card.map(support));
  if(cardWorld!==B){cardinalityLoss++;if(!witness)witness={F,C,bundles:ref,repairWorlds:B,largestBundles:card,largestWorlds:cardWorld,cores};}
  // Naive ranking counts an exact copy of assumption 0 as another vote.
  const cloneScore=s=>pop(s)+(s&1?1:0);
  const cloneCard=ref.filter(s=>cloneScore(s)===Math.max(...ref.map(cloneScore)));
  const cloneWorld=union(cloneCard.map(support));
  if(cloneWorld!==cardWorld){cloneBias++;if(!cloneWitness)cloneWitness={F,C,bundles:ref,cardWorld,cloneWorld,repairWorlds:B};}
  // Check maximal-bundle semantics unaffected by duplicate predicate, before semantic-ID dedup too.
  const cloneSig=sig.map(s=>s|(s&1?8:0)),cm=maximal([...new Set(cloneSig)]);
  check(union(worlds.filter((w,i)=>cm.includes(cloneSig[i])))===B,"clone invariance");cloneChecks++;
  for(const q of masks){
   const each=ref.map(s=>status(support(s),q));
   const expected=each.every(s=>s==="TRUE")?"TRUE":each.every(s=>s==="FALSE")?"FALSE":"UNKNOWN";
   const b=status(B,q),f=status(F,q),v=status(cardWorld,q);
   check(b===expected,"branch agreement");
   check(f==="UNKNOWN"||f===b,"factual consequence preserved");
   queryChecks++;
   if(b==="UNKNOWN"){conditionalUnknown++;if(v!=="UNKNOWN")arbitraryCertainty++;}
   else {conditionalCertainty++;if(f==="UNKNOWN")unsupportedFactual++;}
  }
 }
 // Explicit scope guards: factual contradiction stops; optional alternatives are never factual automatically.
 for(const F of [0]){check(status(F,15)==="CONFLICT","empty factual support");emptyBaseControls++;}
 const claims=[{id:"source:A:v1",mask:3},{id:"source:A:v1",mask:3}];
 function dedup(cs){const m=new Map();for(const c of cs){if(m.has(c.id)&&m.get(c.id)!==c.mask)throw Error("identity conflict");m.set(c.id,c.mask);}return m;}
 check(dedup(claims).size===1,"same identity");let rejected=false;try{dedup([...claims,{id:"source:A:v1",mask:5}]);}catch(e){rejected=true;}check(rejected,"same identity divergent content");
 check(cardinalityLoss>0&&cloneBias>0&&arbitraryCertainty>0,"nontrivial");
 return {cases,conflicts,multi,subsetChecks,coreChecks,queryChecks,cloneChecks,cloneBias,cardinalityLoss,arbitraryCertainty,unsupportedFactual,conditionalCertainty,conditionalUnknown,emptyBaseControls,witness,cloneWitness};
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实际输出
```json
{
  "cases": 50625,
  "conflicts": 35714,
  "multi": 14160,
  "subsetChecks": 405000,
  "coreChecks": 53604,
  "queryChecks": 810000,
  "cloneChecks": 50625,
  "cloneBias": 7902,
  "cardinalityLoss": 5190,
  "arbitraryCertainty": 41484,
  "unsupportedFactual": 217372,
  "conditionalCertainty": 656122,
  "conditionalUnknown": 153878,
  "emptyBaseControls": 1,
  "witness": {
    "F": 3,
    "C": [
      1,
      1,
      2
    ],
    "bundles": [
      3,
      4
    ],
    "repairWorlds": 3,
    "largestBundles": [
      3
    ],
    "largestWorlds": 1,
    "cores": [
      5,
      6
    ]
  },
  "cloneWitness": {
    "F": 3,
    "C": [
      1,
      2,
      2
    ],
    "bundles": [
      1,
      6
    ],
    "cardWorld": 2,
    "cloneWorld": 3,
    "repairWorlds": 3
  }
}
```
## 接入
B04/B05/B06/B07/B08/B10候选增量。先查目标、单位、时间、条件、输入身份、同一事实基础及版本；同合同计算矛盾先复算，异准则按第38轮解释，不可比不强行融合。将事实、用户底线、可撤销假设、互斥结构、预测和未核实陈述分开；必要时列出最小冲突核与所有最大相容条件分支，不按模型数量推选。优先给出事实域稳定结果；分支条件结果显式标记，若覆盖未证则不升级为无条件建议。保留分支条件及查询见证，允许补证、假设修订、撤回后重算。组合搜索有指数复杂度，超过预算时明确部分覆盖，不得宣称完整冲突诊断。独立轨预留事实冲突、同来源多个不等价主张、置信区间误用、分支未覆盖、互斥依赖、重复/身份冲突、不同价值权重及不完整搜索；模型轨研究联合连续域及优先级明确的假设；产品轨评估实际解释负担。未运行原生产品、Qwen、实机、真人或独立验收；无生产修改、Codex、CI、训练、合并、部署、冻结协议变更，零新增费用。
