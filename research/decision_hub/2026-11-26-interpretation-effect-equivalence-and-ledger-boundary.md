# 自主认知：解释效果等价、长期账本修订边界与条件性读取
2026-11-26。RESEARCH_CANDIDATE / REUSED_PROPOSAL_CODE_EXECUTED / FINITE_SYNTHETIC_EFFECT_DOMAIN / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。非语言泛化验收、正式权限实现或生产修复。
## 基线与查重
起始main e0f54b9ec485e065737b4d5f3a8aae5dc221b6e1；核对12近期提交、15开放PR、v3.2/同步规程/唯一交接/前轮报告前12行（唯一交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07）。Draft #63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍draft/unmerged。检索clarification/interpretation/semantic projection/effect equivalence/counterfactual edit/partial result/commutativity/confluence/effect signature/semantic equivalence/revision transaction/future-sensitive/field lineage/confirmation scope。查阅R5 eae10ff00db50587513bc72f628a7f0b8cd5ed8b、R40 1507376849edac68a46f352063a814b0434fd81a、R132 3a725062c742cc0116d29e0f28640bfacbecafbf、具名前沿3893ca17f29334772217ca8871d4fb199e158a12、v0.7投影审计e6027255ada9eee5cfee3351c260ce9e9486191d报告前段。已有最少澄清、共同解释支持、字段血缘、计算发布事务不重做；本轮专门区分当前计算等价、有限未来读取等价和带记录身份/来源/权限的修订效果等价。不是全库无重复证明。
固定#63实际读decision_evidence.py blob e50cb06065e3b1571aef9104bb6109ab1b522bba（含_validate_correction/coherent_history/trace/draft_claims/confirm_claim/verify_claim）、decision_semantics.py 8c6ea6914b5b6e4f01d70331ed5c75c0dc32221b（含blocking_obligations）、decision_conversation_math.py 73557b6650b1a77727c968b114ddfd17c1f591bd（_active_evidence/_operator/build_state前段）、decision_conversation.py 3d961454e971b9d505606e9b0156dcb280fd6587（confirm/_project/_compute）。实际原生已含明确修订目标及同源核对、硬约束角色/比较防护、确认前提及计算失效；本轮不声称该候选存在直接用计算相等进行自动修订的漏洞。仅读源码，未执行这些Python原生函数、API/CLI/Web或物理设备。
## 固定资产
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-25-raw-text-reference-search.md 16075b3ba567ee6dc3496300beab1417172a6c42
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
research/decision_hub/2026-11-25-temporal-quantity-candidate-separation.md 8a6b42f83b80283db6e215fe48f4fb2efbf8368c
research/decision_hub/2026-11-26-compositional-role-candidate-recovery.md b0bea7b4c101c170be2aaa2355973739b125e0b7
research/decision_hub/2026-11-26-clock-event-and-open-role-projection.md ef103587b216ad07c1a47102ddb7cb8d2975283d
全部连接器blob身份实际核对，未独立复算Git原始字节。仅加载固定已审阅项目自有JS；实际复用前轮propose链。两套开发语料为ChatGPT辅助原创公开合成已见案例，未增加训练或独立样本。只调用三个既有情节的当前轮与五个前轮反例，不将其算作新的独立语料，也不针对67项覆盖继续调参。
## 合同与数学
两条人工已确认独立硬记录A/B，均为同一周同一工时单位、上限<=、初始版本1、不同root/source。真实产品可能有不同指标、条件、主体、期限；本轮只研究同一行动同时受两条硬门限制的极简域。六个语义解释：更正A、更正B、仅报告不写、A同效果的另一语言推导、A数值相同但来源身份待确认、A硬底线降级为估计。最后两项未获修订资格，不能据此撤回原有底线；只在显式假设中计算可能影响。模拟的降级仅删去该硬门，绝无实际授权。每个世界的模拟状态为原始账本的独立拷贝，不改变当前账本或历史。用C(w,x)表示假设状态对行动x的布尔硬门；仅域非空且由外部可信夹具认定覆盖时才检查所有解释的条件性一致结果。此结果是关于假设的只读出口，不得作为已确认当前事实、无条件通过或建议。未见解释、资格、真实义务仍未知；没有概率。
修订效果E(w)独立于C：元组为操作、记录根、期望版本、角色、比较符、新值、来源、单位、周期及授权代次。NO_WRITE与UNQUALIFIED分开；后者不是已允许不处理。准备操作必须域完整、当前有效、操作及来源资格具备，且所有解释效果完全相同；有一项资格不足即隔离，有多种效果即须确认目标。统一NO_WRITE不做写入。即使统一更正，仍须明确匹配具体效果的确认票据。相同数值或所有有限查询同结果不足以推出效果相同，反例为两个独立根的同值新版本，来源和历史仍不同。证明：当前查询函数是状态的投影，非单射；当存在E(w1)≠E(w2)但C(w1,x)=C(w2,x)时，选择任一效果不能保证满足另一解释的用户意图。相同效果只在给定元组完整性、外部资格、真实确认和事务条件满足时才可准备；不能视为通用语义等价。没有真正签名、授权、CAS、持久化、提交或自动修订；RESEARCH_PREPARED也始终authority NONE。主循环的确认票据人为从第一解释构造，不是系统推断或真实用户确认。
## 实验
3 A旧阈值×3 B旧阈值×3新阈值×4行动用量×63非空解释支持=6804配置。实际直接逐解释核对当前硬门及单独构造的效果资格参照；后者与候选共享人工定义与输入，不是独立科学验证。每配置检查账本不变及未知覆盖；432个准备案例追加无确认拒绝，14个单项变异（当前性、权限、来源、覆盖、确认、root、version、source、grant、role、unit、scope、cap、op）。3个空域/未知覆盖控制。没有写入真实个人账本。附加按1701个唯一阈值及支持域遍历0..3的全部当前查询及未来仅A/仅B局部查询（后者是显式假设的另一读取范围，不是自动撤回另一硬底线），以及在已资格解释域中核验一次精确root/no-write答复是否足以分离效果。问题字段、回答与域人为给定，没有实际提问、答复、问题成本、拒答或用户负担测量；不重复声称最少澄清DP。
实测6804中当前条件出口一致5892、变化912；一致但未来同用量局部查询变化1818，一致但修订准备受阻5352（其中942为多种已资格效果）；准备432，其中108具有不同语言推导但完全相同效果；只读不写108。故意错误基线在当前一致且首解释是更正时按首解释准备写入，4590组被研究效果门阻止，非实际写入或产品错误率。780组所有模拟数值/角色/根投影相同，但仍不可合并为合法修订效果。附加有限全查询结果及源案例详见JSON。若完整域外另有义务/解释，禁止声明所有条件已确定。查询数值是有限计数，不是现实概率或真实用户表现。
## 既有语言候选的边界
实际复用propose检查L15.2证书角色提升（target null）、S12.2维修店报价（target null、来源未验证、unit null）、L11.2最早八点（event null、日期时区未知）。五个原反例候选也仍存在；本轮只根据明确缺失资格给出隔离说明，不自动判定其完整语义或确认真值，不将五个反例视为被算法消歧或已实现生产阻断。当前产品语义指标未重测。实用交互建议：若当前只读查询在可信有限域下结果一致，可呈现有条件局部分析；若用户要修改长期条件，另确认哪个记录、修改类型、来源及适用范围。对同一修订效果的不同表述不需要强迫用户选择语言分析树，但仍须确认真正效果。对于不同来源的报价，保留并列证据与未决资格，不把新的报告直接当作已确认测量。对未消歧钟点/事件仅展示假设分支。允许拒答并保持原确认账本；本实验没有实现实际拒答流程。
## 下一责任与限制
候选接口区分ConditionalReadSignature、PersistentEffectSignature、EffectQualification及显式确认收据；复用v0.8已有语义/证据账本、原生确认/失效及版本协议，不增加重复数学模型。需接入真实语义候选域的覆盖资格、原文/主体/条件/时效/授权、事务及独立留出，尤其不能把现有67项候选覆盖转作质量门。研究者自行选择二根、六解释、时间量范围与确认模型；下一步优先独立语义质量及真实原生连接，并核对合法外部语料资产。产品轨维护唯一交接，独立轨保管未见留出。未修改生产、训练、合并PR、部署、主动CI或增加费用；R073/PESEN/冻结及历史证据等级不变。
## 复算
固定八份文件全文依次作为contents，Node标准JS；实际整合两次，完整输出一致；与首轮核心计数核对一致。报告包含代码、输出，无单独ZIP。
```js
function experiment(contents){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),clone=x=>JSON.parse(JSON.stringify(x)),code=i=>contents[i].split("```js\n")[1].split("\n```")[0],docs=contents.slice(0,2).map(JSON.parse);
 const P=Function("input",code(7).split(" const out={episodes:")[0]+"\nreturn {propose};\n}\nreturn experiment(input);")(contents.slice(0,7));
 const mk=(a,b)=>[{root:"A",version:1,role:"hard",cap:a,op:"<=",source:"old-A",unit:"hours",scope:"week",grant:"g1"},{root:"B",version:1,role:"hard",cap:b,op:"<=",source:"old-B",unit:"hours",scope:"week",grant:"g1"}];
 const meanings=[{id:0,op:"correct",root:"A",source:"new-A"},{id:1,op:"correct",root:"B",source:"new-B"},{id:2,op:"read_only_report",root:null,source:"report"},{id:3,op:"correct",root:"A",source:"new-A"},{id:4,op:"correct",root:"A",source:"other-A"},{id:5,op:"downgrade",root:"A",source:"new-A"}];
 function effect(w,base,n){
  if(w.op==="read_only_report")return {kind:"NO_WRITE"};
  const old=base.find(x=>x.root===w.root);
  if(w.op!=="correct"||!old||w.source!=="new-"+w.root)return {kind:"UNQUALIFIED",reason:w.op==="downgrade"?"EXPLICIT_ROLE_CHANGE_REQUIRED":"SOURCE_IDENTITY_UNRESOLVED"};
  return {kind:"CORRECT",root:old.root,expectedVersion:old.version,role:old.role,op:old.op,cap:n,source:w.source,unit:old.unit,scope:old.scope,grant:old.grant};
 }
 function simulate(w,base,n){
  let x=clone(base);
  if(w.op==="read_only_report")return x;
  let i=x.findIndex(a=>a.root===w.root);if(w.op==="downgrade"){x[i].role="estimate";return x}
  x[i]={...x[i],version:x[i].version+1,cap:n,source:w.source};return x
 }
 function decision(state,cost,only=null){return state.filter(x=>x.role==="hard"&&(!only||x.root===only)).every(x=>cost<=x.cap)?"PASS":"FAIL"}
 function invariant(a){return a.length&&a.every(x=>x===a[0])?a[0]:"UNKNOWN"}
 function read(base,n,ws,cost,covered){
  if(!covered||!ws.length)return {joint:"UNKNOWN",futureA:"UNKNOWN",futureB:"UNKNOWN",authority:"NONE"};
  const states=ws.map(w=>simulate(w,base,n));
  return {joint:invariant(states.map(s=>decision(s,cost))),futureA:invariant(states.map(s=>decision(s,cost,"A"))),futureB:invariant(states.map(s=>decision(s,cost,"B"))),authority:"NONE"}
 }
 function prepare(base,n,ws,ctx){
  if(!ctx.covered||!ctx.current||!ctx.allowed||!ctx.sourceConfirmed||!ws.length)return {status:"BLOCKED",authority:"NONE"};
  const es=ws.map(w=>effect(w,base,n));
  if(es.some(x=>x.kind==="UNQUALIFIED"))return {status:"UNQUALIFIED_EFFECT",authority:"NONE"};
  if(!es.every(x=>eq(x,es[0])))return {status:"AMBIGUOUS_EFFECT",authority:"NONE"};
  if(es[0].kind==="NO_WRITE")return {status:"NO_WRITE",authority:"NONE"};
  if(!ctx.explicitConfirmation||!eq(ctx.confirmedEffect,es[0]))return {status:"CONFIRM_EFFECT",authority:"NONE"};
  return {status:"RESEARCH_PREPARED",effect:es[0],authority:"NONE"}
 }
 function ref(base,n,ws,ctx){
  if(!ctx.covered||!ctx.current||!ctx.allowed||!ctx.sourceConfirmed||!ws.length)return "BLOCKED";
  if(ws.some(w=>w.op==="downgrade"||w.id===4))return "UNQUALIFIED_EFFECT";
  const labels=new Set(ws.map(w=>w.op==="read_only_report"?"N":w.root));
  if(labels.size!==1)return "AMBIGUOUS_EFFECT";
  if(labels.has("N"))return "NO_WRITE";
  if(!ctx.explicitConfirmation)return "CONFIRM_EFFECT";
  const root=[...labels][0],e=ctx.confirmedEffect;
  return e&&e.kind==="CORRECT"&&e.root===root&&e.expectedVersion===1&&e.role==="hard"&&e.op==="<="&&e.cap===n&&e.source==="new-"+root&&e.unit==="hours"&&e.scope==="week"&&e.grant==="g1"?"RESEARCH_PREPARED":"CONFIRM_EFFECT"
 }
 const ok={covered:true,current:true,allowed:true,sourceConfirmed:true,explicitConfirmation:true};
 let o={cases:0,readInvariant:0,readVaries:0,readInvariantButFutureVaries:0,readInvariantButCommitBlocked:0,readInvariantButAmbiguous:0,readInvariantNoWrite:0,fullEffectPrepared:0,naiveWrongWrite:0,ambiguousAliasResolved:0,numericEqualButEffectDiffers:0,unknownCoverage:0,confirmationControls:0,mutationControls:0,unqualified:0,status:{},examples:{},publicCases:[],contrasts:[],futureSweep:{domains:0,allCurrentAndFutureQueriesInvariant:0,allInvariantButWriteBlocked:0,allCurrentQueriesInvariantButFutureVaries:0,explicitRootQuestionSeparatesQualifiedEffects:0,qualifiedEffectDomains:0},outsideControls:0};
 for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let n=0;n<3;n++)for(let c=0;c<4;c++)for(let m=1;m<64;m++){
  let base=mk(a,b),before=JSON.stringify(base),ws=meanings.filter(w=>m&(1<<w.id)),ctx={...ok,confirmedEffect:effect(ws[0],base,n)},p=prepare(base,n,ws,ctx),z=read(base,n,ws,c,true);
  ck(p.status===ref(base,n,ws,ctx),"prepare oracle");ck(JSON.stringify(base)===before,"immutable");
  let expected=ws.map(w=>{let A=a,B=b;if(w.op==="downgrade")A=Infinity;else if(w.op==="correct"){if(w.root==="A")A=n;else B=n}return c<=A&&c<=B?"PASS":"FAIL"});
  ck(z.joint===invariant(expected),"direct gate");
  o.cases++;o.status[p.status]=(o.status[p.status]||0)+1;
  let stable=z.joint!=="UNKNOWN",futures=z.futureA==="UNKNOWN"||z.futureB==="UNKNOWN";
  if(stable){o.readInvariant++;if(futures){o.readInvariantButFutureVaries++;if(!o.examples.future)o.examples.future={a,b,n,c,m,z,p}}}else o.readVaries++;
  if(p.status==="RESEARCH_PREPARED"){o.fullEffectPrepared++;if(ws.length>1)o.ambiguousAliasResolved++}
  if(p.status==="UNQUALIFIED_EFFECT")o.unqualified++;
  if(stable&&p.status==="NO_WRITE")o.readInvariantNoWrite++;
  if(stable&&p.status==="AMBIGUOUS_EFFECT"){o.readInvariantButAmbiguous++;if(!o.examples.sameNow)o.examples.sameNow={a,b,n,c,m,z,p}}
  if(stable&&!["RESEARCH_PREPARED","NO_WRITE"].includes(p.status))o.readInvariantButCommitBlocked++;
  if(stable&&ws[0].op==="correct"&&p.status!=="RESEARCH_PREPARED"){o.naiveWrongWrite++;if(!o.examples.naive)o.examples.naive={a,b,n,c,m,z,p}}
  let ss=ws.map(w=>simulate(w,base,n).map(x=>[x.root,x.role,x.cap]));
  if(ws.length>1&&ss.every(x=>eq(x,ss[0]))&&!["RESEARCH_PREPARED","NO_WRITE"].includes(p.status))o.numericEqualButEffectDiffers++;
  let u=read(base,n,ws,c,false);ck(u.joint==="UNKNOWN"&&prepare(base,n,ws,{...ctx,covered:false}).status==="BLOCKED","unknown");o.unknownCoverage++;
  if(p.status==="RESEARCH_PREPARED"){let q=prepare(base,n,ws,{...ctx,explicitConfirmation:false});ck(q.status==="CONFIRM_EFFECT","no implicit write");o.confirmationControls++}
  // Count each support/cap domain once, not once per cost. All four
  // current and future queries are evaluated without editing the ledger.
  if(c===0){
   let f=o.futureSweep;f.domains++;
   let rr=[0,1,2,3].map(cost=>read(base,n,ws,cost,true));
   let j=rr.every(v=>v.joint!=="UNKNOWN"),all=j&&rr.every(v=>v.futureA!=="UNKNOWN"&&v.futureB!=="UNKNOWN");
   if(all){f.allCurrentAndFutureQueriesInvariant++;if(!["RESEARCH_PREPARED","NO_WRITE"].includes(p.status))f.allInvariantButWriteBlocked++}
   if(j&&!all)f.allCurrentQueriesInvariantButFutureVaries++;
   if(!ws.some(w=>effect(w,base,n).kind==="UNQUALIFIED")){
    f.qualifiedEffectDomains++;
    // A hypothetical exact answer identifies effect root (A/B/no write).
    // This is a finite partition check, not an actual dialogue or user answer.
    let groups=new Map();for(let w of ws){let k=w.root??"N";if(!groups.has(k))groups.set(k,[]);groups.get(k).push(effect(w,base,n))}
    ck([...groups.values()].every(xs=>xs.every(x=>eq(x,xs[0]))),"root partition");
    f.explicitRootQuestionSeparatesQualifiedEffects++;
   }
  }
 }
 let base=mk(1,2),w=[meanings[0],meanings[3]],ctx={...ok,confirmedEffect:effect(w[0],base,2)};
 for(let patch of [{current:false},{allowed:false},{sourceConfirmed:false},{covered:false},{explicitConfirmation:false},{confirmedEffect:{...ctx.confirmedEffect,root:"B"}},{confirmedEffect:{...ctx.confirmedEffect,expectedVersion:0}},{confirmedEffect:{...ctx.confirmedEffect,source:"other-A"}},{confirmedEffect:{...ctx.confirmedEffect,grant:"g0"}},{confirmedEffect:{...ctx.confirmedEffect,role:"estimate"}},{confirmedEffect:{...ctx.confirmedEffect,unit:"days"}},{confirmedEffect:{...ctx.confirmedEffect,scope:"month"}},{confirmedEffect:{...ctx.confirmedEffect,cap:1}},{confirmedEffect:{...ctx.confirmedEffect,op:"<"}}]){ck(prepare(base,2,w,{...ctx,...patch}).status!=="RESEARCH_PREPARED","mutant");o.mutationControls++}
 // An empty or incomplete interpretation domain must not imply no obligation.
 for(let ws of [[],w])for(let covered of [false,true])if(!covered||!ws.length){ck(read(base,2,ws,1,covered).joint==="UNKNOWN"&&prepare(base,2,ws,{...ctx,covered}).status==="BLOCKED","outside");o.outsideControls++}
 for(let [d,id,ti,q,kind] of [[0,"L15",1,"证书是必须的","ROLE_CHANGE_CANDIDATE"],[1,"S12",1,"维修店说要七百","REPORTED_VALUE_CHANGE_CANDIDATE"],[0,"L11",1,"最早八点","CLOCK_BOUND"]]){
  let e=docs[d].cases.find(x=>x.id===id),z=P.propose(e.turns[ti].text,ti>0),v=z.newer.find(x=>x.text===q&&x.kind===kind);ck(v&&v.authority==="NONE","raw public candidate");o.publicCases.push({id,turn:ti+1,q,kind,detail:v.detail,write:"BLOCKED_UNRESOLVED_TARGET_OR_QUALIFICATION"})
 }
 for(let [s,prior,q,kind] of [["我昨天九点前到",false,"九点前到","CLOCK_BOUND"],["是否已经到账",false,"已经到账","QUESTION_COMPLEMENT"],["这台电脑大约五百",false,"这台电脑","COST_BEARER_CANDIDATE"],["证书是必须的",true,"证书是必须的","ROLE_CHANGE_CANDIDATE"],["同事说要七百",true,"同事说要七百","REPORTED_VALUE_CHANGE_CANDIDATE"]]){
  let z=P.propose(s,prior),v=z.newer.find(x=>x.text===q&&x.kind===kind);ck(v&&v.authority==="NONE","contrast");o.contrasts.push({s,q,kind,write:"BLOCKED_UNRESOLVED_TARGET_OR_QUALIFICATION"})
 }
 return o
}
const contents=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8"));
console.log(JSON.stringify(experiment(contents),null,2));
```
## 实测输出
```json
{
  "cases": 6804,
  "readInvariant": 5892,
  "readVaries": 912,
  "readInvariantButFutureVaries": 1818,
  "readInvariantButCommitBlocked": 5352,
  "readInvariantButAmbiguous": 942,
  "readInvariantNoWrite": 108,
  "fullEffectPrepared": 432,
  "naiveWrongWrite": 4590,
  "ambiguousAliasResolved": 108,
  "numericEqualButEffectDiffers": 780,
  "unknownCoverage": 6804,
  "confirmationControls": 432,
  "mutationControls": 14,
  "unqualified": 5184,
  "status": {
    "RESEARCH_PREPARED": 432,
    "AMBIGUOUS_EFFECT": 1080,
    "NO_WRITE": 108,
    "UNQUALIFIED_EFFECT": 5184
  },
  "examples": {
    "sameNow": {
      "a": 0,
      "b": 0,
      "n": 0,
      "c": 0,
      "m": 3,
      "z": {
        "joint": "PASS",
        "futureA": "PASS",
        "futureB": "PASS",
        "authority": "NONE"
      },
      "p": {
        "status": "AMBIGUOUS_EFFECT",
        "authority": "NONE"
      }
    },
    "naive": {
      "a": 0,
      "b": 0,
      "n": 0,
      "c": 0,
      "m": 3,
      "z": {
        "joint": "PASS",
        "futureA": "PASS",
        "futureB": "PASS",
        "authority": "NONE"
      },
      "p": {
        "status": "AMBIGUOUS_EFFECT",
        "authority": "NONE"
      }
    },
    "future": {
      "a": 0,
      "b": 0,
      "n": 0,
      "c": 1,
      "m": 33,
      "z": {
        "joint": "FAIL",
        "futureA": "UNKNOWN",
        "futureB": "FAIL",
        "authority": "NONE"
      },
      "p": {
        "status": "UNQUALIFIED_EFFECT",
        "authority": "NONE"
      }
    }
  },
  "publicCases": [
    {
      "id": "L15",
      "turn": 2,
      "q": "证书是必须的",
      "kind": "ROLE_CHANGE_CANDIDATE",
      "detail": {
        "target": null,
        "operation": "promote_to_hard_candidate"
      },
      "write": "BLOCKED_UNRESOLVED_TARGET_OR_QUALIFICATION"
    },
    {
      "id": "S12",
      "turn": 2,
      "q": "维修店说要七百",
      "kind": "REPORTED_VALUE_CHANGE_CANDIDATE",
      "detail": {
        "target": null,
        "source": "UNVERIFIED_REPORT",
        "unit": null
      },
      "write": "BLOCKED_UNRESOLVED_TARGET_OR_QUALIFICATION"
    },
    {
      "id": "L11",
      "turn": 2,
      "q": "最早八点",
      "kind": "CLOCK_BOUND",
      "detail": {
        "clock": {
          "start": 2,
          "end": 4,
          "raw": "八点",
          "kind": "CLOCK",
          "detail": {
            "hour": 8,
            "minute": 0,
            "partOfDay": null,
            "date": null,
            "timezone": null,
            "resolved": false
          },
          "authority": "NONE",
          "outside": true
        },
        "op": ">=",
        "event": null
      },
      "write": "BLOCKED_UNRESOLVED_TARGET_OR_QUALIFICATION"
    }
  ],
  "contrasts": [
    {
      "s": "我昨天九点前到",
      "q": "九点前到",
      "kind": "CLOCK_BOUND",
      "write": "BLOCKED_UNRESOLVED_TARGET_OR_QUALIFICATION"
    },
    {
      "s": "是否已经到账",
      "q": "已经到账",
      "kind": "QUESTION_COMPLEMENT",
      "write": "BLOCKED_UNRESOLVED_TARGET_OR_QUALIFICATION"
    },
    {
      "s": "这台电脑大约五百",
      "q": "这台电脑",
      "kind": "COST_BEARER_CANDIDATE",
      "write": "BLOCKED_UNRESOLVED_TARGET_OR_QUALIFICATION"
    },
    {
      "s": "证书是必须的",
      "q": "证书是必须的",
      "kind": "ROLE_CHANGE_CANDIDATE",
      "write": "BLOCKED_UNRESOLVED_TARGET_OR_QUALIFICATION"
    },
    {
      "s": "同事说要七百",
      "q": "同事说要七百",
      "kind": "REPORTED_VALUE_CHANGE_CANDIDATE",
      "write": "BLOCKED_UNRESOLVED_TARGET_OR_QUALIFICATION"
    }
  ],
  "futureSweep": {
    "domains": 1701,
    "allCurrentAndFutureQueriesInvariant": 384,
    "allInvariantButWriteBlocked": 249,
    "allCurrentQueriesInvariantButFutureVaries": 611,
    "explicitRootQuestionSeparatesQualifiedEffects": 405,
    "qualifiedEffectDomains": 405
  },
  "outsideControls": 3
}
```
