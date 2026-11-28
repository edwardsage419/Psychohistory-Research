# 跨修订内部计算复用、完整依赖及原子发布合同

2026-11-28。RESEARCH_CANDIDATE / SYNTHETIC_DEVELOPMENT_EXECUTED / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NOT_ADMITTED。起始 main 8e862821e7c6e2810009201fe362958439de7f5a。v0.8 Draft #63 候选 734686980b19da9291bdd08b67d4e2519c011acf。核对近期15提交身份及最近14项文件路径，开放PR前10项、v3.2 blob 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85、同步规程。阅读 V08_ENGINE、V08_RESEARCH_INTEGRATION、V08_INDEPENDENT_HANDOFF、V08_COMPOSITION (a602867cb0ff640f3c585d6bb46890a27a6567bc)，核对 decision_resources.py 27e6151f1f909ea0076142126fa93ac4a9bb2fb4 和 decision_composition.py aea376e8c94a4959bee1afd5e8a6b8c785060d42 的类和函数合同；既有 world-bound-multistage-result-join af4daae1aaeee5a36a140d8a0f272a48c064368b、ledger-to-budgeted-threshold-integration cf792bd6aba79bc3edd2d9329084362604c4c63a。搜索 handoff/continuity/日期未返回代码结果，未确认唯一产品交接最新版，全库去重有限。近期数学与语言研究仍各自负责。当前任务仅研究跨模块计算结果复用及发布资格；不替换 v0.8 全局失效规则，不声称首次发现缓存或并发问题，不修改生产代码。

## 1. 共同合同与推导

可信宿主提供固定的无环依赖图及完整读取合同。对叶节点 x 的规范输入身份 I(x) 包含私有工作区、用途、主体、规范键、数据版本、来源及资格版本、时间口径、集合成员版本和精确输入；实际实现须用规范化编码与有界散列，不泄露原始私人内容。对确定性计算节点 n，I(n)=encode(scope,n,algorithm version,ordered input identities)。内部计算复用条件为所有身份完全相同，且当前用途、访问和保留策略允许。数学归纳：叶输入相同；按拓扑序，如果完整父输入相同且函数版本固定，复用与重算的值相同；任何缺失依赖或非确定性未绑定则保证失效。新增义务、可能世界、新候选集合和更正需要集合版本或完整查询域身份，不能只记录已返回的行。无时效证明的外部来源、时间变动、数值精度、随机种子、用户确认和模型切换均按实际读取依赖处理。研究夹具只模拟 workspace、叶版本、值及算法版本，其余必须在生产补足。

内部纯计算缓存与权威发布分离。每次发出结果前，以同一原子事务比较当前工作区、用途、实例、修订、证据/权限代次、完整依赖、方法准入及宿主签发收据；同时持久化或发布当前结果身份。旧票据始终失效，即便全部数值相等或权限恢复（ABA）。严格检查发生在发布线性化点；网络迟到消息需要客户端实例/修订校验。重新确认产生新票据，旧用户选择、计划和学习资格不能沿用。试验输出 authority NONE，签名及授权不由候选缓存自行生成。若权限撤回，私有中间结果也受删除、密钥清理及保留政策约束；仅不含已撤回数据且获当前授权的纯算术才可继续保留。试验的 grant-only 复用是无私人数据的合成计算示意，不代表可以在撤回后读取、保存或复用个人数据。

## 2. 实验与反例

人工设定9类叶输入、5个确定性内部节点：现金余量、情景来源、门槛、比较、显示。非空9位变化集合511组，各执行改值及同值改版本两种配置（共1022，部分配置重复）。比较直接独立表达式及不复用的同合同执行。基线每请求重算全部5节点。所有值均为虚构整数，没有使用现有生产模型或个人数据。初始现金8、义务2、储备3，余量3，方法量4，门槛1，两个情景收益1与3，均通过；新增义务合计4后余量1，门槛3，第一情景失败。遗漏集合成员变化即可能错误维持全通过。值相同而依赖身份改变不等于数值错误，不能把计数当真实风险率。

时序模型：check<commit、change<restore，共6个线性排列；权限、来源、方法、集合成员四种变化。对照提前检查后发布与只比较最终可见值。原子方案直接按提交时的代次和权限定义，0个错误仅为该形式模型内的性质，非实际并发实现或独立安全验收。没有模拟事务崩溃、跨进程数据库、恶意票据、网络传输、缓存污染、真实恢复、时间/用途或加密。两个实验的组合数不是独立用户样本、实际概率或运行时间。

## 3. 接口及下一阶段条件

- 语言与确认层：RawTurn 和可信确认投影产生来源、义务及完整成员集合身份；未知依赖不复用。保持原文、归属、时域、修订以及用户确认。
- 知识层：PublicFactCache/事实核验票据、来源更正、撤回、时效和适用域形成精确依赖；实时源仍待生产准入，不自动联网。
- 数学层：DecisionRegistry 固定方法及依赖版本；decision_composition 保留原完整 CompositionScope 和 MAC 续算边界。仅研究新的内部缓存，不能将旧签名检查点直接迁移为新代次。长期资源层 CashObligation/JointResourceInput 需要集合完整身份及日期、到账、计划版本；真实联合可行仍需验收。
- 反馈：观察和事前预测独立身份；撤回或口径修订触发派生资格审查，历史冻结结果可受授权审阅，旧选择资格失效；不自动写回生产参数。
- 独立验收建议：同值更正、新增记录的负依赖、删除/恢复授权、多工作区/主体/用途、时钟跨界、来源过期、方法回退、缓存污染、竞争发布及崩溃恢复分别测试；必须先独立复核现有 v0.8 保护。开发及独立留出隔离。缓存需测实际 CPU、内存、存储、重建成本和用户等待时间；没有测量前不能宣称性能优势。原子发布可通过受审宿主事务/CAS实现，具体持久化接口由经授权完整版本工程设计。保持唯一产品交接、冻结规则和现有生产安全；本轮没有启动Codex、合并、部署、训练、CI请求或新增费用。

## 4. 可复算脚本与结果

下列为本轮实际执行的标准 JavaScript，将代码块保存成 .js 后可离线使用 Node 运行，无第三方依赖。合成夹具、版本、拓扑、基线和研究任务由研究者选择。试验的字符串键非安全散列，票据为可信内存对象；生产必须校验来源、签名和访问授权，不得把它作为认证实现。

```js
function experiment(){
 const ck=(x,m)=>{if(!x)throw Error(m)};
 const names=["cash","obligations","gain","source","worlds","reserve","method","preference","grant"];
 const deps={balance:["cash","obligations","reserve"],evidence:["gain","source","worlds"],threshold:["balance","method"],comparison:["threshold","evidence","worlds"],display:["comparison","preference"]};
 const order=Object.keys(deps);
 const calc=(n,v)=>{
  if(n==="balance")return v[0]-v[1]-v[2];
  if(n==="evidence")return v[1]?v[2].map(w=>[w,v[0]+w]):null;
  if(n==="threshold")return v[0]>=0?Math.max(0,v[1]-v[0]):null;
  if(n==="comparison")return v[0]===null||v[1]===null?null:v[1].map(([w,g])=>[w,g>=v[0]]);
  return v[0]===null?null:{rows:v[0],order:v[1]};
 };
 const base=[8,2,1,true,[0,2],3,4,"cost",true];
 const changed=[5,4,2,false,[0,2,3],4,6,"time",false];
 const make=(mask,same=0)=>({workspace:"W",instance:"I",revision:mask?2:1,grantEpoch:mask&256?2:1,leaves:Object.fromEntries(names.map((n,i)=>[n,{version:mask&(1<<i)?2:1,value:mask&(1<<i)&&!(same&(1<<i))?changed[i]:base[i]}]))});
 const encode=x=>JSON.stringify(x);
 function run(s,old={}){
  const nodes=Object.fromEntries(names.map(n=>[n,{key:encode([s.workspace,n,s.leaves[n].version,s.leaves[n].value]),value:s.leaves[n].value}]));
  let reused=0,executed=0;
  for(const n of order){
   const a=deps[n].map(k=>nodes[k]),key=encode([s.workspace,n,"algorithm-v1",a.map(x=>x.key)]);
   if(old[n]?.key===key){nodes[n]=old[n];reused++}
   else{nodes[n]={key,value:calc(n,a.map(x=>x.value))};executed++}
  }
  return {nodes,reused,executed};
 }
 function oracle(s){
  const v=Object.fromEntries(names.map(n=>[n,s.leaves[n].value]));
  const room=v.cash-v.obligations-v.reserve;
  const t=room<0?null:Math.max(0,v.method-room);
  const rows=t===null||!v.source?null:v.worlds.map(w=>[w,v.gain+w>=t]);
  return rows===null?null:{rows,order:v.preference};
 }
 function ticket(s,result){return {workspace:s.workspace,instance:s.instance,revision:s.revision,grantEpoch:s.grantEpoch,key:result.nodes.display.key,value:result.nodes.display.value};}
 function publish(t,s,r){return s.leaves.grant.value&&t.workspace===s.workspace&&t.instance===s.instance&&t.revision===s.revision&&t.grantEpoch===s.grantEpoch&&t.key===r.nodes.display.key?{status:"RESEARCH",authority:"NONE",value:t.value}:{status:"BLOCKED",authority:"NONE"}}
 const o={cases:0,oracleMatches:0,globalRecompute:0,selectiveCompute:0,reused:0,oldTicketRejected:0,freshDenied:0,sameValueKeyChanges:0,weakValueOnlyStaleEvidence:0,weakMembershipFalsePass:0,controls:0};
 const s0=make(0),r0=run(s0),t0=ticket(s0,r0);
 for(let mask=1;mask<512;mask++)for(let same of [0,mask&255]){
  let s=make(mask,same),r=run(s,r0.nodes),fresh=run(s);
  ck(encode(r.nodes.display.value)===encode(oracle(s))&&r.nodes.display.key===fresh.nodes.display.key,"oracle");
  o.cases++;o.oracleMatches++;o.globalRecompute+=order.length;o.selectiveCompute+=r.executed;o.reused+=r.reused;
  ck(publish(t0,s,r).status==="BLOCKED","old ticket");o.oldTicketRejected++;
  const p=publish(ticket(s,r),s,r);ck((p.status==="RESEARCH")===s.leaves.grant.value,"grant");if(p.status==="BLOCKED")o.freshDenied++;
  if(encode(r.nodes.display.value)===encode(r0.nodes.display.value)&&r.nodes.display.key!==r0.nodes.display.key)o.sameValueKeyChanges++;
  if(same&&r.nodes.evidence.key!==r0.nodes.evidence.key&&encode(r.nodes.evidence.value)===encode(r0.nodes.evidence.value))o.weakValueOnlyStaleEvidence++;
 }
 const s=make(2);
 ck(oracle(s).rows.some(([w,ok])=>!ok)&&oracle(s0).rows.every(([w,ok])=>ok),"membership false pass");o.weakMembershipFalsePass++;
 function control(x,m){ck(x,m);o.controls++}
 control(run(make(256),r0.nodes).reused===5,"grant only arithmetic reuse");
 control(run(make(128),r0.nodes).reused===4,"preference only display");
 control(run(make(1,1),r0.nodes).nodes.display.key!==r0.nodes.display.key,"same amount correction");
 control(run(make(16),r0.nodes).nodes.evidence.key!==r0.nodes.evidence.key,"domain expansion");
 control(publish(t0,{...s0,instance:"J"},r0).status==="BLOCKED","new instance");
 control(publish(t0,{...s0,workspace:"X"},r0).status==="BLOCKED","new workspace");
 control(publish(t0,{...s0,grantEpoch:2},r0).status==="BLOCKED","grant ABA");
 control(publish(t0,{...s0,revision:3},r0).status==="BLOCKED","revision ABA");
 control(run({...s0,workspace:"X"},r0.nodes).reused===0,"workspace isolation");
 control(publish(ticket(s0,r0),s0,r0).authority==="NONE","no selection");
 control(run(make(8),r0.nodes).nodes.display.value===null,"source withdrawal");
 control(run(make(64,64),r0.nodes).nodes.threshold.key!==r0.nodes.threshold.key,"method version");
 return o;
}
function interleavings(){
 const ck=(v,m)=>{if(!v)throw Error(m)};
 let schedules=[];
 function seq(prefix,rest){if(!rest.length){if(prefix.indexOf("check")<prefix.indexOf("commit")&&prefix.indexOf("change")<prefix.indexOf("restore"))schedules.push(prefix);return}for(let i=0;i<rest.length;i++)seq([...prefix,rest[i]],[...rest.slice(0,i),...rest.slice(i+1)])}
 seq([],["check","commit","change","restore"]);
 const out={schedules:schedules.length,cases:0,nonatomicFalsePublication:0,atomicFalsePublication:0,validAtCommit:0,abaFalsePublication:0,witness:null};
 for(let kind of ["permission","source","method","membership"])for(let schedule of schedules){
  let gen=1,visible="original",allowed=true,checked=false;
  for(let step of schedule){
   if(step==="change"){gen++;visible="changed";if(kind==="permission")allowed=false}
   if(step==="restore"){gen++;visible="original";allowed=true}
   if(step==="check")checked=gen===1&&allowed;
   if(step==="commit"){
    const expected=gen===1&&allowed;
    const atomic=gen===1&&allowed;
    const weak=checked,byValue=visible==="original"&&allowed;
    out.cases++;if(expected)out.validAtCommit++;
    if(weak&&!expected){out.nonatomicFalsePublication++;out.witness??={kind,schedule,gen,allowed}}
    if(atomic!==expected)out.atomicFalsePublication++;
    if(byValue&&!expected)out.abaFalsePublication++;
   }
  }
 }
 ck(out.cases===24&&out.atomicFalsePublication===0&&out.nonatomicFalsePublication>0&&out.abaFalsePublication>0,"interleaving");
 return out
}
console.log(JSON.stringify({reuse:experiment(),publication:interleavings()},null,2));
```

```json
{
  "reuse": {
    "cases": 1022,
    "oracleMatches": 1022,
    "globalRecompute": 5110,
    "selectiveCompute": 4788,
    "reused": 322,
    "oldTicketRejected": 1022,
    "freshDenied": 512,
    "sameValueKeyChanges": 514,
    "weakValueOnlyStaleEvidence": 448,
    "weakMembershipFalsePass": 1,
    "controls": 12
  },
  "publication": {
    "schedules": 6,
    "cases": 24,
    "nonatomicFalsePublication": 8,
    "atomicFalsePublication": 0,
    "validAtCommit": 4,
    "abaFalsePublication": 12,
    "witness": {
      "kind": "permission",
      "schedule": [
        "check",
        "change",
        "commit",
        "restore"
      ],
      "gen": 2,
      "allowed": false
    }
  }
}
```

结果：1022/1022 与直接表达式一致；5110次全量节点计算基线与4788次选择性执行相差322次（约6.3%节点计数）。旧票据1022次均被拒；新票据512次因权限被拒。514个配置的最终显示值相同而身份变化，448个同值配置的证据值相同而身份变化，仅为值键丢失版本的诊断。12项专门控制通过。24个有限时序中提前检查基线错误放行8次，只比较最终可见值基线错误放行12次；原子模型按构造0次。两组结果不得作为生产能力、真实性能或独立科研验证。
