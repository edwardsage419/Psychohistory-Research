# v3.2 自主认知专项第7轮（累计第66轮）：有根知识推理与来源撤回

2026-11-25。RESEARCH_CANDIDATE。main 683860d851312d75ae892af14fc2ec0999375b76；PR #61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，13开放Draft PR。核对最近8提交、v3.2 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（前部及此前全文）、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（相关标题及历史阅读，非本轮全文）、decision_hub目录、第3轮c0301e9a0c9371cc41a3fdecff2b2e9f18492912、第4轮8953af15d57350d892c5dddd401c5c2bdd6f237d、第10轮2ba97ae7bc3ef17830f6085054c4d016f18f7838、第18轮f55a6fb6a801bb765b96530ce71b45e58d802852、第28轮36ca07db56fc64865d6cc7a5db87384583604844、第29轮585bce3e9c878e2ead241e9fefc6f93937780790、第50轮4d394d2cb6e1e1dfc667f2a8806f896a36bbdbef、第51轮3941256a5e560a8cdc55af8b974cb89a090438ea、第52轮63f76ee0322736a2866b04822d2cf0ac203504d7、第53轮06744930cb28c581f036fd047168cf4dc71fafc7、第65轮b16928724409abc5e701dd8716371430a212dcf6、第45轮dcc14692b2c92d1f5d256e969e4d9fd135ac714e、第41轮7398d951f617d938ce27bcc46252e8dc84144797。读取相关摘要/段落，非全部历史重验。既有154份固定清单历轮处理40份、15登记方法38条来源边（37匹配1复审）为历史证据，未本轮重建或解除timing_actions复审。区别于第4轮方法执行DAG、第10轮文献适用性、第18轮反馈重放、第51/52轮检索身份和第53轮输入映射：本轮研究允许循环的有限正向知识规则、显式相反证据、最小来源支持集及来源/规则撤回。非现有平台缺陷证明。

## 数学及接口
有限签名命题用独立原子A+和A-表示显式支持与反对，不作经典否定公理，也不因缺失得出负命题。规则为已审核的正向合取前提到单一结论（有限无变量Horn形式），多条规则同头提供可选支持路径。每条直接已获资格的来源赋独立ID，其事实带单元素支持集；每次满足规则把各前提支持集合取并，并入结论。只保留按集合包含最小的支持集：若S包含T且T已支持同一命题，使用S不会增加任何当前来源子集下的可导出性，可删除S。循环从空推导开始，不允许循环自身创造事实。有限单调闭包终止；通过归纳，所有保留支持集均有有限规则证明，任意有限证明由直接事实及规则组合生成，删去超集不丢失可导出性。对于固定有效规则集合，撤回来源i后精确删除包含i的所有最小支持集即可；因为任何原有可导出的剩余来源集合都包含至少一个未撤回的最小支持。规则撤回则重算闭包（支持集仅记录来源，规则版本绑定完整快照；不宣称有完整规则路径证书）。候选缺少规则路径、人类语义映射及真实元数据校验；同一最小支持集可能包含共同研究的不同版本，不能当独立重复证据，更不能用支持集数推算概率或置信度。正反证据同时存在返回CONFLICT，均缺失UNKNOWN，单向仅为支持状态。上游冲突沿所有活动规则保守标记复审（可能包含未使用的分支），不声称正反证据导致所有结论皆真，任何知识推导始终authority NONE，不等于数学模型准入。真实外部科学事实及因果迁移仍需第10/52/53轮资格及用户授权。示例命题只是抽象夹具，不对应真实科学理论或真实登记方法。有限规则无变量、无否定前提、无默认规则、无量词、无数值推导；支持集最坏指数增长，128轮保护只适用该小型原型，尚未实现生产证明数量、内存和时间预算。源身份、有效时间窗[from,to)、实际知悉时间、使用许可由可信宿主提供；过去时点与后来才知悉的事实区分，原型只演示比较，不实现真实密码学、完整双时态查询、授权撤回存储或网络获取。blob为虚构夹具字面值，不是真实哈希。无本轮新增外部文献或数据；基本有限正向规则证明为自行推导，不主张原创数学定理。

## 实验
7个签名原子、6个来源（含两个支持同一原子的不同来源）及6条规则（含循环、合取、替代路径）。64来源掩码×64规则掩码=4096图。候选为最小支持集固定点；参照为每个来源子集枚举全部128个布尔模型，取满足事实和活动规则的模型交集，再筛最小支持集。有限正向Horn模型交集等于最小模型，独立计算路径不调用候选；同一研究者定义规则及夹具，非独立验收。遍历每图逐个撤回所有活动来源/规则；naiveStaleMethod为只缓存旧方法支持且不处理来源撤回时遗留支持的转换数，不是实际系统错误率。independentPathRetained指撤去一个原来出现在某最小支持集的来源后仍有支持路径，独立仅指集合路径有不含该来源的见证，不代表统计独立或不同研究。methodConflictReview为有M支持且存在上游冲突复审的图数。17项专项控制核验时间、知悉时间、版本、权限、身份、冲突、循环及无执行授权。研究代码和夹具为ChatGPT研发辅助生成的项目原创合成开发材料，非真人、训练数据或独立留出。未运行真实原生方法、真实全文索引、真实App、真机性能、用户效果或外部数据。未调用其他AI运行时。

## 实际复算
以下JS在连接器计算环境运行，可直接用Node复跑，无第三方包或网络。

```js
const probe = function(){
 const ck=(x,m)=>{if(!x)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 // Synthetic signed propositions. Negation is explicit, never negation by absence.
 const names=["A+","A-","B+","C+","D+","D-","M+"],N=names.length;
 const sources=[0,1,2,4,5,0]; // two distinct source records support A+
 const rules=[{body:[0,2],head:3},{body:[3],head:4},{body:[4],head:3},{body:[2],head:4},{body:[1],head:5},{body:[3,4],head:6}];
 const sorted=s=>[...s].sort((a,b)=>a-b);
 const subset=(a,b)=>(a&b)===a;
 function add(set,m){if([...set].some(x=>subset(x,m)))return false;for(const x of set)if(subset(m,x))set.delete(x);set.add(m);return true}
 function infer(sm,rm){
  const p=names.map(()=>new Set());
  sources.forEach((n,i)=>{if(sm&(1<<i))add(p[n],1<<i)});
  let change=true,rounds=0;
  while(change){change=false;if(++rounds>128)throw Error("LIMIT");
   rules.forEach((r,i)=>{if(!(rm&(1<<i)))return;let combinations=[0];for(const b of r.body)combinations=combinations.flatMap(a=>[...p[b]].map(m=>a|m));for(const m of combinations)if(add(p[r.head],m))change=true});
  }
  return p.map(sorted);
 }
 // Oracle via intersection of every propositional model, for each possible admitted source subset.
 // All rule implications are positive over signed atom IDs, so intersection is a model.
 const modelCache=new Map();
 function modelIntersection(sm,rm){
  const k=sm*64+rm;if(modelCache.has(k))return modelCache.get(k);
  let facts=0;sources.forEach((n,i)=>{if(sm&(1<<i))facts|=1<<n});
  let intersection=(1<<N)-1;
  for(let m=0;m<(1<<N);m++){
   if(!subset(facts,m))continue;
   if(rules.some((r,i)=>(rm&(1<<i))&&r.body.every(b=>m&(1<<b))&&!(m&(1<<r.head))))continue;
   intersection&=m;
  }
  modelCache.set(k,intersection);return intersection;
 }
 function oracle(sm,rm){
  const supports=names.map(()=>[]);
  for(let s=sm;;s=(s-1)&sm){
   const m=modelIntersection(s,rm);
   for(let n=0;n<N;n++)if(m&(1<<n))supports[n].push(s);
   if(!s)break;
  }
  return supports.map(a=>a.filter(m=>!a.some(x=>x!==m&&subset(x,m))).sort((x,y)=>x-y));
 }
 function classify(p,pos,neg){const a=p[pos].length>0,b=neg===null?false:p[neg].length>0;return a&&b?"CONFLICT":a?"POSITIVE_SUPPORT":b?"NEGATIVE_SUPPORT":"UNKNOWN"}
 function report(sm,rm){
  const p=infer(sm,rm);
  // All conclusions are reference-only. A conflict anywhere in the available upstream graph
  // is a review warning (conservative, may include unused alternatives).
  const conflictNodes=new Set();
  for(const [a,b] of [[0,1],[4,5]])if(classify(p,a,b)==="CONFLICT"){conflictNodes.add(a);conflictNodes.add(b)}
  let changed=true;while(changed){changed=false;rules.forEach((r,i)=>{if((rm&(1<<i))&&r.body.some(b=>conflictNodes.has(b))&&!conflictNodes.has(r.head)){conflictNodes.add(r.head);changed=true}})}
  return {supports:p,states:[classify(p,0,1),classify(p,4,5),classify(p,6,null)],methodReview:conflictNodes.has(6),authority:"NONE"};
 }
 let out={graphs:0,atomChecks:0,matched:0,minimalSupports:0,methodSupported:0,methodUnknown:0,methodConflictReview:0,revocationChecks:0,ruleWithdrawalChecks:0,independentPathRetained:0,naiveStaleMethod:0,cycleWithoutSupport:0,controls:0};
 let witness={};
 for(let rm=0;rm<64;rm++)for(let sm=0;sm<64;sm++){
  const r=report(sm,rm),gold=oracle(sm,rm);ck(eq(r.supports,gold),"model intersection "+sm+" "+rm);out.graphs++;out.atomChecks+=N;out.matched+=N;out.minimalSupports+=r.supports.reduce((a,b)=>a+b.length,0);
  ck(r.authority==="NONE","authority");if(r.supports[6].length){out.methodSupported++;if(r.methodReview)out.methodConflictReview++}else out.methodUnknown++;
  for(let i=0;i<6;i++)if(sm&(1<<i)){
   let next=report(sm^(1<<i),rm);
   const expected=r.supports.map(a=>a.filter(m=>!(m&(1<<i))));
   ck(eq(next.supports,expected),"source withdrawal");out.revocationChecks++;
   if(r.supports[6].length&&next.supports[6].length&&r.supports[6].some(m=>m&(1<<i))){out.independentPathRetained++;if(!witness.retained)witness.retained={sm,rm,removed:i,before:r.supports[6],after:next.supports[6]}}
   if(r.supports[6].length&&!next.supports[6].length){out.naiveStaleMethod++;if(!witness.stale)witness.stale={sm,rm,removed:i,before:r.supports[6],after:next.supports[6]}}
  }
  for(let i=0;i<6;i++)if(rm&(1<<i)){
   let next=report(sm,rm^(1<<i));ck(eq(next.supports,oracle(sm,rm^(1<<i))),"rule withdrawal");out.ruleWithdrawalChecks++;
  }
  if(sm===0&&(rm&6)===6){ck(r.supports.every(x=>!x.length),"unsupported cycle");out.cycleWithoutSupport++}
 }
 // Time and qualification are checked before inference. The expected manifest is trusted input.
 const manifest=[{id:"s0",version:"v1",blob:"fixture-a",from:1,to:5,known:2,permission:true},{id:"s1",version:"v1",blob:"fixture-b",from:1,to:5,known:2,permission:true}];
 function eligible(s,expected,t,now){return !!s&&s.id===expected.id&&s.version===expected.version&&s.blob===expected.blob&&s.permission===true&&expected.permission===true&&Number.isInteger(t)&&Number.isInteger(now)&&s.from===expected.from&&s.to===expected.to&&s.known===expected.known&&s.from<=t&&t<s.to&&s.known<=now&&t<=now}
 let a=manifest[0];
 for(const [s,e,t,now,want] of [[a,a,3,3,true],[a,a,1,1,false],[a,a,5,5,false],[a,a,3,2,false],[a,a,0,3,false],[{...a,blob:"changed"},a,3,3,false],[{...a,version:"v2"},a,3,3,false],[{...a,permission:false},a,3,3,false],[a,{...a,permission:false},3,3,false],[{...a,known:1},a,3,3,false],[{...a,to:9},a,6,6,false],[manifest[1],a,3,3,false]]){ck(eligible(s,e,t,now)===want,"qualification");out.controls++}
 let r=report(3,63);ck(r.states[0]==="CONFLICT"&&r.states[2]==="UNKNOWN","no explosion");out.controls++;
 ck(report(0,63).states.every(x=>x==="UNKNOWN"),"absence not negative");out.controls++;
 ck(report(4,63).supports[6].length>0,"grounded cycle");out.controls++;
 ck(report(4,63).authority==="NONE","no model authority");out.controls++;
 ck(report(4|16,63).methodReview,"upstream conflict");out.controls++;
 return {out,witness};
};
console.log(JSON.stringify(probe(),null,2));
```

实际输出：
```json
{
  "out": {
    "graphs": 4096,
    "atomChecks": 28672,
    "matched": 28672,
    "minimalSupports": 17952,
    "methodSupported": 832,
    "methodUnknown": 3264,
    "methodConflictReview": 574,
    "revocationChecks": 12288,
    "ruleWithdrawalChecks": 12288,
    "independentPathRetained": 464,
    "naiveStaleMethod": 832,
    "cycleWithoutSupport": 16,
    "controls": 17
  },
  "witness": {
    "stale": {
      "sm": 13,
      "rm": 33,
      "removed": 0,
      "before": [
        13
      ],
      "after": []
    },
    "retained": {
      "sm": 45,
      "rm": 33,
      "removed": 0,
      "before": [
        13,
        44
      ],
      "after": [
        44
      ]
    }
  }
}
```

## 下一接口
将语义目标/缺口变为可信知识查询，使用第51/52轮固定资产身份及第53轮原生义务映射；需构建真实带作用域、来源、版本及正反证据的知识卡，再执行相关性到资格的实际跨模块连接。优先选少量真实已登记方法及其固定来源，验证结构化科学适用条件与缺失证据的反向查询；不将研究原型自动登记为生产模型。产品轨维护唯一交接，独立轨保管未见来源变化与冲突测试。无生产代码、训练、CI、Codex任务、合并、部署、个人数据或新增费用，冻结协议不变。