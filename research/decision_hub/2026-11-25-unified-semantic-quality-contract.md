# 第58轮：统一语义输入质量协议及组合回归规格
2026-11-25。固定main dd45037da2fe04dbb7687d110e75c2eda2eeb4ad，PR #61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e open Draft。核对v3.1、AGENTS、同步规程、近期提交、开放PR、唯一交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第2/24/27/50/53/54/55/56/57轮。源码阅读：decision_conversation.py f505aeab2d9e5e0a9c8957ce6e039dea174918a7 turn/confirm；decision_conversation_math.py aca1b4aa5cf4b4fd5b476e078b6e2aa9af197d30 build_state；decision_evidence.py b45932af6346fb0df072ffb6cb13ef0cd6991b7a ClaimInput/SourceMetadata。现有PR已有部分确认/条件阻断定向修复，保持历史记录。本轮未执行原生Python或重跑旧实验，不主张生产新增漏洞；新增多种语义缺陷同时存在时的保留、逐项修正和候选确认顺序的有限协议验证，与第2轮条件逻辑、第24轮结构化候选、第27轮端口依赖、第54轮共享参数有所区别。
## 统一契约
1. 原文义务与可舍弃的解析候选独立。可信宿主维护会话、代次、修订、原文跨度及来源、义务ID、角色/决策所有者/适用对象、版本、用途和授权。语言模型仅提出结构化解释、引用及可能缺口，不赋予确认和发布权限。没有独立的完整覆盖证据时，空候选或没有发现问题都不能表示没有底线。
2. 六类质量义务为币种/单位、周期/时间口径、比较方向/边界、主体/归属、条件/例外、角色/目标/偏好。另有通用来源真实性、数值合法性、完整性、权限及风险等要求，本实验不完整模拟。每个义务允许多个并存问题；宿主为每项保留具体来源与待核对原因，问题集合按语义资格逐项修复，确认后的新义务与冲突仍必须重新核查。实际修订可能新增缺陷，须重新执行全部相关验证器，不能仅凭集合减法证明真实修复。
3. 丢弃候选不等于撤回原有底线；仅对有权决定的个人约束允许明确撤回并保留事件，外部事实和法律/安全限制不能由用户任意撤销。实际撤回需鉴别对象、范围及授权，不以全局勾选替代。第三方外部约束经核实适用后可保留；个人权重须本人确认。条件性说明保持条件性。
4. 通过本地语义门仅意味着当前已知义务通过，实际计算还需模型适用性、输入及单位校验、联合依赖和证据资格、用户授权、硬约束、重大风险、同版本结果校验。完整建议出口须覆盖全部相关义务；局部描述只能使用独立合格依赖，明确未知与局限。确认源信息不升级事实等级。
5. 旧修复或确认收据不可在修订、来源、代次、会话、版本或用途变化后直接复用；派生输出须重验依赖和当前权限。真实实现需原子事务、服务端认证、撤回、并发和恢复测试。本轮只模拟单个义务及当前快照，所有验证/授权布尔值来自可信人工夹具；不模拟真实身份认证、持久化、跨会话、多义务合取、外部不可撤约束、新问题发现及实际用户交互。
## 现有回归入口
|来源|已有范围|下一正式验收要求|
|---|---|---|
|R55 d7eedbca02da7f66f06911fffedc8f8b82be3f90|96条币种及周期测试、10正常控制、4人工筛查见证（历史报告）|完整白话/账本/通用Constraint投影，歧义、缺失、同币种外币、跨期、多币种、源证据|
|R56 2c7810d1cad4986b9ecabdf727adab5600ed6fca|140条否定比较、14控制，原生局部gate（历史报告）|四方向、严格边界、否定/多条件、范围、显式修订及不支持语法|
|R57 e957deba40302b7f6d9ee61c34196d7ac28ce124|174条主体及叙事测试（历史报告）|主体、转述、采纳、外部期限、代理决策、目标偏好、跨轮语义|
|R2/R24/R35/R53/R54|条件、修订、结构、投影、需求及共享参数|保持既有回归，单独验证漏义务、条件分支、过期、独立端口和共同依赖|
以上是可追溯历史开发测试入口，96+140+174=410条专项计数并非410独立语义样本（可能重复和共享模板）。本轮不重跑这些原生实验或宣称其全部通过。独立轨应另行冻结自由文本情节及评分标准，开发样例不得作为独立留出。必须分开报告语义召回、错误确认、无故阻断、条件/单位/归属正确、端到端建议损害及真实交互负担。
## 组合回归
六维缺陷掩码64、修复掩码64、确认/丢弃/明确撤回三操作、覆盖资格2，共24576组。修复收据只对当前人工已知缺陷逐项关闭，修复后候选确认失效；与逐维预期判断对照。firstOnlyFalse是故意错误的“只记录首个缺陷”对照允许而预期拒绝的组数，不是当前产品实测错误。discardFalse是有覆盖资格下的4096次丢弃操作仍须保留义务；若错误将丢弃当撤回会放行。partialRetained仅固定独立描述性端口的夹具可用计数，没有执行原生描述模型，不当作实际产品收益。complete是模拟语义门通过，包含有权明确撤回的情形，不表示决策建议合格。720种六维逐一修复顺序和1956个树前缀检查，4825个语义通过状态的旧修订收据拒绝，23个专项控制。两个计算路径同一研究者设计，非独立验收。采用人工已知缺陷集合，无法发现漏检、新出现缺陷或泛化错误；修复集合单调是有限实验假设，不可套到真实语言。
```js
function experiment(){
 const ck=(x,m)=>{if(!x)throw Error(m)};
 const dimensions=["currency","period","operator","subject","condition","role"];
 const bits=m=>dimensions.filter((_,i)=>m&(1<<i));
 const identity=["session","generation","revision","obligation","source","contract","purpose"];
 function make(mask){return {session:"S",generation:1,revision:1,obligation:"O",source:"fixture text 1",contract:"semantic-v1",purpose:"decision",required:true,coverage:true,authorized:true,issues:bits(mask),candidate:"C1",confirmed:false,withdrawn:false};}
 function resolve(s,receipt){
  if(!s.authorized||!identity.every(k=>s[k]===receipt[k])||receipt.verified!==true||!Array.isArray(receipt.addressed)||!receipt.addressed.every(d=>s.issues.includes(d)))return null;
  return {...s,revision:s.revision+1,issues:s.issues.filter(d=>!receipt.addressed.includes(d)),candidate:"C"+(s.revision+1),confirmed:false};
 }
 function receipt(s,addressed){return {...Object.fromEntries(identity.map(k=>[k,s[k]])),verified:true,addressed};}
 function confirm(s,token){if(!s.authorized||!identity.every(k=>s[k]===token[k])||token.candidate!==s.candidate||!s.candidate||s.issues.length||token.userConfirmed!==true)return null;return {...s,confirmed:true};}
 function discard(s){return {...s,revision:s.revision+1,candidate:null,confirmed:false};}
 function withdraw(s,token){if(!s.authorized||!identity.every(k=>s[k]===token[k])||token.explicitWithdrawal!==true)return null;return {...s,revision:s.revision+1,withdrawn:true,candidate:null,confirmed:false};}
 function canPublish(s){return s.authorized&&s.coverage&&(s.withdrawn||(!s.required)||(s.candidate!==null&&s.confirmed&&s.issues.length===0));}
 function bind(s){return {...Object.fromEntries(identity.map(k=>[k,s[k]])),candidate:s.candidate,issues:s.issues.join("|"),confirmed:s.confirmed,withdrawn:s.withdrawn};}
 function current(s,b){return canPublish(s)&&Object.entries(bind(s)).every(([k,v])=>b[k]===v);}
 let cases=0,complete=0,blocked=0,firstOnlyFalse=0,discardFalse=0,partialRetained=0,controls=0,steps=0,stale=0,repairOrders=0,firstWitness=null;
 for(let mask=0;mask<64;mask++)for(let fixes=0;fixes<64;fixes++)for(const action of ["confirm","discard","withdraw"])for(const coverage of [false,true]){
  const s=make(mask);s.coverage=coverage;
  const addressed=bits(mask&fixes),t=resolve(s,receipt(s,addressed));ck(t!==null,"repair");
  ck(dimensions.every(d=>t.issues.includes(d)===(s.issues.includes(d)&&!addressed.includes(d))),"preservation");
  let u;if(action==="confirm")u=confirm(t,{...bind(t),userConfirmed:true})||t;else if(action==="discard")u=discard(t);else u=withdraw(t,{...bind(t),explicitWithdrawal:true});
  const expected=coverage&&(action==="withdraw"||(action==="confirm"&&dimensions.every((_,i)=>!(mask&(1<<i))||!!(fixes&(1<<i)))));
  ck(canPublish(u)===expected,"publish");cases++;if(expected)complete++;else blocked++;
  const first=bits(mask)[0],firstResolved=!first||addressed.includes(first);
  const firstOnly=coverage&&(action==="withdraw"||(action==="confirm"&&firstResolved));
  if(firstOnly&&!expected){firstOnlyFalse++;if(!firstWitness)firstWitness={mask,fixes,issues:s.issues,addressed,remaining:u.issues,action};}
  if(action==="discard"&&coverage){discardFalse++;ck(!canPublish(u),"discard != withdraw");}
  const independent={authorized:true,source:"independent point data",value:2};
  if(!expected&&independent.authorized){partialRetained++;}
  if(canPublish(u)){let b=bind(u);ck(current(u,b),"current");let v={...u,revision:u.revision+1};ck(!current(v,b),"stale");stale++;}
 }
 function walk(s,remaining){if(!remaining.length){repairOrders++;ck(canPublish(confirm(s,{...bind(s),userConfirmed:true})),"finish");return;}
  for(const d of remaining){const t=resolve(s,receipt(s,[d]));steps++;ck(t.issues.length===remaining.length-1&&!t.confirmed,"step");if(t.issues.length)ck(confirm(t,{...bind(t),userConfirmed:true})===null,"premature");walk(t,remaining.filter(x=>x!==d));}
 }
 walk(make(63),dimensions);
 const s=make(63),r=receipt(s,["currency"]);
 for(const k of identity){const bad={...r,[k]:typeof r[k]==="number"?r[k]+1:r[k]+"!"};ck(resolve(s,bad)===null,"mismatch "+k);controls++;}
 for(const bad of [{...r,verified:false},{...r,addressed:["nonexistent"]}]){ck(resolve(s,bad)===null,"bad repair");controls++;}
 ck(resolve({...s,authorized:false},r)===null,"revoked");controls++;
 const t=resolve(s,r);ck(resolve(t,r)===null,"old repair");controls++;
 ck(withdraw(t,{...bind(t),explicitWithdrawal:false})===null,"no explicit withdraw");controls++;
 const d=discard(t);ck(!canPublish(d)&&d.issues.length===5,"discard preserves");controls++;
 const p=resolve(make(0),receipt(make(0),[]));const good=confirm(p,{...bind(p),userConfirmed:true});
 ck(good&&canPublish(good),"positive");controls++;
 ck(confirm(p,{...bind(p),candidate:"forged",userConfirmed:true})===null,"candidate");controls++;
 ck(confirm(p,{...bind(p),userConfirmed:false})===null,"confirmation");controls++;
 const b=bind(good);for(const change of [{generation:2},{session:"T"},{purpose:"other"},{contract:"v2"},{authorized:false},{coverage:false},{source:"new"}]){ck(!current({...good,...change},b),"old output");controls++;}
 return {cases,complete,blocked,firstOnlyFalse,discardFalse,partialRetained,repairOrders,steps,stale,controls,firstWitness};
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实际输出
```json
{
  "cases": 24576,
  "complete": 4825,
  "blocked": 19751,
  "firstOnlyFalse": 1351,
  "discardFalse": 4096,
  "partialRetained": 19751,
  "repairOrders": 720,
  "steps": 1956,
  "stale": 4825,
  "controls": 23,
  "firstWitness": {
    "mask": 3,
    "fixes": 1,
    "issues": [
      "currency",
      "period"
    ],
    "addressed": [
      "currency"
    ],
    "remaining": [
      "period"
    ],
    "action": "confirm"
  }
}
```
## 工程接入与验收
B02/B03/B05/B06/B07/B08/B09/B11候选补充，保留第34/50轮12项完整版本范围。建议以现有EvidenceLedger/ClaimInput及版本化状态接口扩展宿主义务、修订记录、可信校验器和计算发布收据；不得把各轮有限正则简单串接当语义解决方案。统一回归入口应在固定PR的真实支持环境完整执行，分别比较规则、本地Qwen、结构化提议加可信宿主、同一数据普通AI，按情节及主体/币种/周期/方向/条件组合分层，保留未知及错误阻断。产品轨维护唯一交接，独立轨负责未见案例与验收，模型轨负责输入资格与共同计算。当前仅研究候选及实际JS协议验证，完整应用、真实Qwen/Mac/iPhone、原生回归及独立验证仍未执行。没有重大开发授权，本轮未改生产、工作流、CI、Codex、训练、合并、部署或冻结协议，零新增费用。
