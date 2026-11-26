# 长期个人决策：实际进度对账、修订血缘与未来策略重新准入
2026-11-26。RESEARCH_CANDIDATE / PREDECESSOR_CODE_EXECUTED / SYNTHETIC_EXECUTED / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线
同一手动轮第四阶段，起点main 6e86b9fd6d602c3bf25219cbd0c7c8e96f554eec。沿用本轮核对v3.2、同步规程、25近期提交、15开放PR、固定交接、#63固定head 734686980b19da9291bdd08b67d4e2519c011acf；未运行原生。实际加载两份固定自有研究源码：
research/decision_hub/2026-11-26-time-varying-task-cost-liquidity-dp.md 56f16ddab494b41aa07852045653fbdf20f28341
research/decision_hub/2026-11-26-observed-balance-policy-partition-and-replanning.md b5be4353d489e8b9ab09a39ac9e11f2929c2bd5a
复用P.solve/oracle/unpack及下游原函数；R101双时间账本、R124实际成本与剩余时间、R125依赖失效、条件知识时间重放已有通用机制，不重复发明。本轮新增三类独立实际记录（真实进度、实际到账、实际支付）的有限完整清单、与本轮观察分组策略原型的真实函数连接、未来域必须匹配实际记录版本，即使同值修订也拒绝旧计算范围。查重有限。
## 合同
固定单一虚构主体、3任务、3期、仅第0期实际数据，第1期起为未来策略。宿主人工给定完整根清单及期初已核实余额；三种实际记录分别有根、版本、获知时间、实际发生期、类型、授权代次与资格。截止获知时间按完整连续版本选择最后当前记录，最新撤回或失去资格保留UNKNOWN_ACTUAL，不回退旧值；预测收入、计划进度和实际记录类型隔离。无真实鉴权、来源认证、持久化、完整生效时点、签名、跨系统去重、现实现金账户、并发、实际观察的历史删除/撤回权限，历史重放限于仍获授权的夹具。实际进度为已完成数量，不由预期计划推定；已发生余额=已核实期初+实际到账-实际支付；剩余需求=原需求-实际完成。若负余额直接标记ACTUAL_DEFICIT，不将其截断为零，不把现有不足自动解释为未来不可行或执行借贷。未来域未覆盖、旧版本或缺少授权则返回UNKNOWN_FUTURE_SCOPE，同时允许已核对的实际快照独立呈现；这与未来情景真实适用性分开。
仅当未来世界由宿主明确重新确认，并绑定当前三个实际记录的精确ID/版本及授权代次，才运行上一轮真实P.solve，参数为当前余额、剩余需求、第一期起及新的已确认未来域。实际世界可能已超出旧情景，不能凭旧情景树推断新的未来覆盖；本轮不实现自动排除旧世界或自动重新确认。夹具重资格仍选原数值世界，属于人工条件，不代表真实证据。新域的数值可与旧域相同，但当前性独立。所有条件输出只读authority NONE；未来失败不改写已发生历史。真实已完成进度、未来情景覆盖和可行动许可必须分别确认。
## 实际执行
1000个随机合成图（固定种子），每图两个非零需求、真实进度、已到账、已付、期初余额，另添加计划及预测诱饵。核对直接余额和剩余需求；负余额不计算；其余调用实际前轮观察策略及独立全排程参照。比较错误地以计划进度替实际、以预测收入增加当前现金的故意错误基线。追加实际进度与支出更正后检查原截止时点重放、旧未来域拒绝（包括同值版本）、外部重新确认后直接复算；撤回、缺少实际记录及6控制。实际连接器执行两次完整结果一致。所有数值是合成结构重复计算，不是真实产品错误率、独立用户或真实预测。
```json
{
  "graphs": 1000,
  "snapshotChecks": 1784,
  "policyChecks": 1444,
  "staleScopeRejects": 660,
  "withdrawalRejects": 784,
  "oldHistoryChecks": 784,
  "changedNumericalState": 641,
  "sameValueNewVersionRejects": 19,
  "plannedAsActualFalsePass": 102,
  "plannedAsActualFalseReject": 30,
  "forecastAsCashFalsePass": 223,
  "missingActualChecks": 2352,
  "deficitChecks": 216,
  "controls": 6,
  "example": {
    "b": 0,
    "rem": [
      0,
      0,
      0
    ],
    "forecast": 4
  }
}
```
## 接入及限制
需在原生真实观察账本与未来方法调度之间添加明确的ActualProgressSnapshot和FutureScenarioBasis；当前研究仅绑定实际根版本，实际产品还要绑定期初余额来源、任务版本、权限、当前性、来源资格、方法版本、场景内容与原生事务，不能直接将此夹具作为完整准入门。原生、独立留出、真实数据、真实回滚、Mac/iPhone和性能未运行。研究者选择有限单期已发生合同、清单、时间、整数金额、外部重资格和错误对照；未修改生产、唯一交接、冻结、证据等级、PR、训练、部署、主动CI或费用。
## 复算
固定两份报告按上述顺序传入；Node包装未运行，核心连接器实际执行。
```js
const code=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8").split("\`\`\`js\n")[1].split("\n\`\`\`")[0]);
const make=Function(code[0].split(" const out={graphs:")[0]+"\nreturn {valid,actions,solve,verify,oracle};\n}\nreturn study();");
const make2=Function("make",code[1].slice(code[1].indexOf("function experiment(make){")).split(" const out={graphs:")[0]+"\nreturn {solve,oracle,unpack};\n}\nreturn experiment(make);");
function experiment(make,make2){
 const P=make2(make),ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),copy=x=>JSON.parse(JSON.stringify(x)),sum=a=>a.reduce((s,x)=>s+x,0);
 let seed=20261202;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 // Only a finite, confirmed, complete manifest of period-zero actuals.
 const rootKinds={progress:"PROGRESS",income:"RECEIPT",expense:"PAYMENT"};
 function snapshot(log,host){
  if(!host.allowed||!host.covered||!Number.isSafeInteger(host.opening)||host.opening<0)return {status:"UNKNOWN_QUALIFICATION",authority:"NONE"};
  const rows={},versions={};
  for(const root of Object.keys(rootKinds)){
   const hist=log.filter(x=>x.root===root&&x.received<=host.asOf&&x.period===0&&x.kind===rootKinds[root]).sort((a,b)=>a.version-b.version);
   if(!hist.length)return {status:"UNKNOWN_ACTUAL",authority:"NONE"};
   if(hist.some((v,i)=>v.version!==i+1||i&&v.received<hist[i-1].received))return {status:"INVALID_LINEAGE",authority:"NONE"};
   const x=hist.at(-1);
   if(!x.qualified||x.grant!==host.grant||x.value===null)return {status:"UNKNOWN_ACTUAL",authority:"NONE"};
   rows[root]=x.value;versions[root]=[x.id,x.version];
  }
  if(!Array.isArray(rows.progress)||rows.progress.length!==3||rows.progress.some((v,i)=>!Number.isInteger(v)||v<0||v>host.d[i])||[rows.income,rows.expense].some(v=>!Number.isSafeInteger(v)||v<0))return {status:"INVALID_ACTUAL",authority:"NONE"};
  const balance=host.opening+rows.income-rows.expense,remaining=host.d.map((v,i)=>v-rows.progress[i]);
  if(balance<0)return {status:"ACTUAL_DEFICIT",balance,remaining,versions,authority:"NONE"};
  return {status:"ACTUAL_SNAPSHOT",balance,remaining,versions,authority:"NONE"};
 }
 function admit(log,host,domain){
  let s=snapshot(log,host);
  if(s.status!=="ACTUAL_SNAPSHOT")return {status:s.status,snapshot:s,authority:"NONE"};
  // A new future scenario contract is required after any change to actual lineage.
  if(!domain||!domain.covered||domain.grant!==host.grant||!eq(domain.basis,s.versions)||domain.start!==1||domain.worlds.length===0||domain.worlds.some(p=>!eq(p.d,host.d)))return {status:"UNKNOWN_FUTURE_SCOPE",snapshot:s,authority:"NONE"};
  const signals=domain.worlds.map(()=>[0,0,0]),z=P.solve(domain.worlds,signals,s.balance,true,1,s.remaining);
  return {status:z.ok?"CONDITIONAL_PLAN":"CONDITIONAL_NO_PLAN",snapshot:s,plan:z,scope:{asOf:host.asOf,grant:host.grant,domain:domain.version,basis:s.versions},authority:"NONE"};
 }
 const record=(root,version,value,received,extra={})=>({root,kind:rootKinds[root],id:root+"@"+version,version,value,received,period:0,qualified:true,grant:1,...extra});
 function domainFor(host,s,worlds,version){return {covered:true,grant:host.grant,basis:copy(s.versions),start:1,worlds,version}}
 const out={graphs:0,snapshotChecks:0,policyChecks:0,staleScopeRejects:0,withdrawalRejects:0,oldHistoryChecks:0,changedNumericalState:0,sameValueNewVersionRejects:0,plannedAsActualFalsePass:0,plannedAsActualFalseReject:0,forecastAsCashFalsePass:0,missingActualChecks:0,deficitChecks:0,controls:0,example:null};
 for(let g=0;g<1000;g++){
  let d=[1+rnd(2),1+rnd(2),0],host={d,opening:rnd(7),asOf:1,allowed:true,covered:true,grant:1};
  let progress=[rnd(d[0]+1),rnd(d[1]+1),0],income=rnd(5),expense=rnd(7);
  let log=[record("progress",1,progress,1),record("income",1,income,1),record("expense",1,expense,1),
   {root:"income",kind:"FORECAST",value:4,received:0,period:0},{root:"progress",kind:"PLAN",value:d,received:0,period:0}];
  const original=JSON.stringify(log),s=snapshot(log,host),b=host.opening+income-expense,rem=d.map((n,i)=>n-progress[i]);
  ck(s.balance===b&&eq(s.remaining,rem),"direct actual snapshot");out.snapshotChecks++;
  if(b<0){ck(s.status==="ACTUAL_DEFICIT"&&admit(log,host,null).status==="ACTUAL_DEFICIT","deficit");out.deficitChecks++;out.graphs++;continue}
  const jobs=Array.from({length:3},()=>({release:0,deadline:1+rnd(2)}));
  const ws=Array.from({length:2},()=>({d,jobs:jobs.map(j=>({...j,cost:Array.from({length:3},()=>rnd(4))})),cap:[0,1+rnd(3),1+rnd(3)],income:Array.from({length:3},()=>rnd(5)),mandatory:Array.from({length:3},()=>rnd(3)),reserve:Array.from({length:3},()=>rnd(3))}));
  let f=domainFor(host,s,ws,1),z=admit(log,host,f),sig=ws.map(()=>[0,0,0]),o=P.oracle(ws,sig,b,true,1,rem);
  ck((z.status==="CONDITIONAL_PLAN")===o.ok&&z.authority==="NONE","actual planner");out.policyChecks++;
  if(o.ok)ck(P.unpack(z.plan,ws,sig,b,true,1,rem),"witness");
  const fakeProgress=d.map((n,i)=>Math.min(n,1)),fakeRem=d.map((n,i)=>n-fakeProgress[i]),naive=P.oracle(ws,sig,b,true,1,fakeRem);
  out.plannedAsActualFalsePass+=+(!o.ok&&naive.ok);out.plannedAsActualFalseReject+=+(o.ok&&!naive.ok);
  if(!o.ok&&P.oracle(ws,sig,b+4,true,1,rem).ok){out.forecastAsCashFalsePass++;out.example??={b,rem,forecast:4}}
  // Correct progress and expense on day 2. Source versions are independent roots.
  const revisedProgress=[rnd(d[0]+1),rnd(d[1]+1),0],revisedExpense=rnd(7),later={...host,asOf:2};
  const changed=[...log,record("progress",2,revisedProgress,2),record("expense",2,revisedExpense,2)];
  let s2=snapshot(changed,later);
  ck(s2.balance===host.opening+income-revisedExpense&&eq(s2.remaining,d.map((n,i)=>n-revisedProgress[i])),"revision direct");out.snapshotChecks++;
  ck(eq(snapshot(changed,host),s),"historical as-of");out.oldHistoryChecks++;
  ck(JSON.stringify(log)===original,"append-only");
  if(s2.status==="ACTUAL_SNAPSHOT"){
   ck(admit(changed,later,f).status==="UNKNOWN_FUTURE_SCOPE","old basis");out.staleScopeRejects++;
   if(s2.balance===s.balance&&eq(s2.remaining,s.remaining))out.sameValueNewVersionRejects++;else out.changedNumericalState++;
   // Requalification is explicitly given by host fixture, never inferred from old model.
   let fresh=domainFor(later,s2,ws,2),r=admit(changed,later,fresh),q=P.oracle(ws,sig,s2.balance,true,1,s2.remaining);
   ck((r.status==="CONDITIONAL_PLAN")===q.ok,"future recompute");out.policyChecks++;
  }
  let withdrawn=[...log,record("expense",2,null,2)],r=admit(withdrawn,later,f);
  ck(r.status==="UNKNOWN_ACTUAL","no old source fallback");out.withdrawalRejects++;
  for(let root of Object.keys(rootKinds)){ck(snapshot(log.filter(x=>x.root!==root),host).status==="UNKNOWN_ACTUAL","missing actual");out.missingActualChecks++}
  out.graphs++;
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 let h={d:[1,1,0],opening:3,asOf:1,allowed:true,covered:true,grant:1},l=[record("progress",1,[0,0,0],1),record("income",1,2,1),record("expense",1,1,1)];
 ctl(snapshot(l,h).balance===4,"known snapshot");
 ctl(snapshot(l,{...h,allowed:false}).status==="UNKNOWN_QUALIFICATION","withdraw authorization");
 ctl(snapshot(l,{...h,grant:2}).status==="UNKNOWN_ACTUAL","old grant");
 ctl(snapshot([...l,record("income",3,2,1)],h).status==="INVALID_LINEAGE","version gap");
 ctl(snapshot([...l,record("progress",2,[2,0,0],1)],h).status==="INVALID_ACTUAL","overstated progress");
 ctl(admit(l,h,null).status==="UNKNOWN_FUTURE_SCOPE","actual knowledge independent of future coverage");
 return out;
}
console.log(JSON.stringify(experiment(make,make2),null,2));
```
