# 跨决策现金义务身份并集与修订传播
2026-11-25。RESEARCH_CANDIDATE / EXACT_FINITE_DEVELOPMENT_EXECUTED / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。固定main 79a1f225598fefa5b3ac34042e28b83fc2c66cf6；Draft #62 e61bbad10932edabc9a87483e5407fdae6c751cc。核对近期12提交、14开放PR、v3.2首10行及前轮全文、唯一交接前18行 blob 5e74f4f0b37141d631740e844ad8bbbfed232e07；读取R96/97/98/100报告主要合同与算法（提交 ef2e5e3733583da44267c5a6e16c2560a7741c28、9c32e8e20de270b00f366a3ff2dda5bf031b0fcc、f8a16f272ec27d0d95fe90d7f323c8969b6c2978、6d7786c5226f76875b93b6393527a8c200e69dfc）。这些已有联合资源域、跨期承诺前沿、旧目标机会损失和双时间账本。本轮仅研究来自不同决策的同一现金义务的身份并集、错误重复合并及修订传播，非新优化算法。查重采用相关提交检索及正文抽查，不能保证全库无重叠。

## 源码边界
候选 platform/future_model/src/psychohistory/decision_resources.py blob 53708241b09e03d1bef7beed17cb304db508bf3c，ResourceState为单快照，evaluate_resources遍历option逐个比较现金余额、储备和future_cost。decision_records.py blob e2b0492b413f99c1cff44ae357e1d2c52c8ba6ba，529–564行授权绑定来源记录最新修订，resource_for_reuse剥离旧options。现有单决策替代方案独立分析是合理设计，不应误判为缺陷；跨决策同时采用的计划需要另行联合合同。未修改产品，不宣称已观察真实资金超支。

## 合同
可信宿主提供同一账户、同一时点、同一货币、完整所选计划现金义务集；仅已确认非负未来一次性支出。每个义务有跨决策规范身份、精确整数金额、支付阶段（OUTSTANDING或已反映于当前余额REFLECTED）、来源资格及截止时点。相同身份且上述内容相同只计一次；不同身份即使金额相同仍独立计；同一身份不同内容返回CONFLICT，缺资格/覆盖/时点/币种返回UNKNOWN。真实身份需要证据或用户确认，禁止以名称、金额相同或语言相似自动合并；REFLECTED必须有账本对账证据，未核对不能视为已支付。余额已反映实际付款，不重复扣除；未来收入、退款、分期、借贷、账户间转移和时间容量不在合同。R100保留实际与预测区别。
令B为当前余额、R为储备底线，U为所选计划中唯一且未付款的义务身份并集，联合余量M=B−R−sum(amount(i), i∈U)。M≥0只说明给定范围内现金可行；不能作为实际执行或整体建议资格。新计划不能自动占用资金，旧计划取消也不能擅自释放义务。对一个规范义务修订后，所有引用该身份的决策投影及联合分析必须核验新版本；已失效或未确认的新版本不得回退为旧值。此代码只模拟全量投影重写，未实现真实反向索引、并发、事务、版本收据或持久化。工程候选可用义务→决策→结果的反向依赖索引，合并时重新绑定当前账本代次，需按前轮发布事务、授权和实例身份规则审查。

## 实验
9个余额×3储备×4个A独有费用×4个B独有费用×4个附加费用×2种身份关系，3456个合成组合。参照为直接生成公式，非独立研究者。对照分别为各计划单独可行但联合不可行、直接加总重复费用产生错误拒绝、按金额去重产生错误放行；计数可重叠，不是现有产品错误率或现实概率。每组再修改规范义务F增加1单位，验证所有投影同时改变但并集总额只增加1。13项专项控制。研究者选取整数、范围、同账户及静态合同；未经实际用户、原生API、训练、真机或独立验收。所有输出authority NONE。未新增费用、训练、PR合并、部署或冻结变更。复算Node标准JS，无第三方依赖。

```js
function experiment(){
 const ok=(x,m)=>{if(!x)throw Error(m)};
 // All identifiers, coverage, amounts and currency are host-qualified fixtures.
 // balance already includes all actual payments through the same cutoff.
 function evaluate(balance,reserve,rows,covered=true){
  const u={authority:"NONE"};
  if(!covered||!Number.isSafeInteger(balance)||!Number.isSafeInteger(reserve)||reserve<0||!Array.isArray(rows))return {...u,status:"UNKNOWN"};
  const seen=new Map();
  for(const a of rows){
   if(!a.id||!a.qualified||a.currency!=="CNY"||a.cutoff!==1||!Number.isSafeInteger(a.amount)||a.amount<0||!["OUTSTANDING","REFLECTED"].includes(a.stage))return {...u,status:"UNKNOWN"};
   const sig=JSON.stringify([a.amount,a.stage,a.currency,a.cutoff]);
   if(seen.has(a.id)&&seen.get(a.id).sig!==sig)return {...u,status:"CONFLICT"};
   seen.set(a.id,{sig,row:a});
  }
  let total=0;
  for(const {row} of seen.values())if(row.stage==="OUTSTANDING")total+=row.amount;
  if(!Number.isSafeInteger(total)||!Number.isSafeInteger(balance-reserve-total))return {...u,status:"UNKNOWN"};
  const margin=balance-reserve-total;
  return {...u,status:margin>=0?"FEASIBLE_WITHIN_SCOPE":"INFEASIBLE_WITHIN_SCOPE",total,margin};
 }
 const row=(id,amount,stage="OUTSTANDING")=>({id,amount,stage,qualified:true,currency:"CNY",cutoff:1});
 let z={cases:0,unionChecks:0,separateFalseFeasible:0,naiveSumFalseInfeasible:0,amountDedupFalseFeasible:0,revisionChecks:0,controls:0,witnesses:{}};
 for(let balance=0;balance<=8;balance++)for(let reserve=0;reserve<=2;reserve++)for(let a=0;a<=3;a++)for(let b=0;b<=3;b++)for(let fee=0;fee<=3;fee++)for(let same of [false,true]){
  let A=[row("A",a),row("F",fee)],B=[row("B",b),row(same?"F":"G",fee)],all=[...A,...B],v=evaluate(balance,reserve,all);
  let truth=a+b+fee*(same?1:2),room=balance-reserve,pass=truth<=room;
  ok(v.total===truth&&v.margin===room-truth&&(v.status==="FEASIBLE_WITHIN_SCOPE")===pass,"direct formula");
  z.cases++;z.unionChecks++;
  if(a+fee<=room&&b+fee<=room&&!pass){z.separateFalseFeasible++;z.witnesses.separate??={balance,reserve,a,b,fee,same,truth}}
  if(a+b+2*fee>room&&pass){z.naiveSumFalseInfeasible++;z.witnesses.sum??={balance,reserve,a,b,fee,same,truth}}
  if([...new Set([a,b,fee,fee])].reduce((s,x)=>s+x,0)<=room&&!pass){z.amountDedupFalseFeasible++;z.witnesses.amount??={balance,reserve,a,b,fee,same,truth}}
  // A correction to a canonical obligation must reach every projection of its identity.
  const corrected=all.map(x=>x.id==="F"?{...x,amount:fee+1}:x);
  let v2=evaluate(balance,reserve,corrected);
  ok(v2.total===truth+1&&v2.margin===v.margin-1,"propagate identity");
  z.revisionChecks++;
 }
 const ck=x=>{ok(x,"control");z.controls++};
 ck(evaluate(10,3,[row("A",5),row("B",4)]).status==="INFEASIBLE_WITHIN_SCOPE");
 ck(evaluate(10,3,[row("F",4),row("F",4)]).total===4);
 ck(evaluate(10,3,[row("F",4),row("G",4)]).total===8);
 ck(evaluate(10,3,[row("F",4),row("F",5)]).status==="CONFLICT");
 ck(evaluate(10,3,[row("F",4),row("F",4,"REFLECTED")]).status==="CONFLICT");
 ck(evaluate(10,3,[row("F",4,"REFLECTED"),row("G",2)]).total===2);
 ck(evaluate(10,3,[{...row("F",4),qualified:false}]).status==="UNKNOWN");
 ck(evaluate(10,3,[{...row("F",4),currency:"USD"}]).status==="UNKNOWN");
 ck(evaluate(10,3,[{...row("F",4),cutoff:2}]).status==="UNKNOWN");
 ck(evaluate(10,3,[row("F",4)],false).status==="UNKNOWN");
 ck(evaluate(10,3,[row("F",7)]).margin===0);
 ck(evaluate(10,3,[row("F",-1)]).status==="UNKNOWN");
 ck(z.cases===3456&&z.revisionChecks===3456);
 return z;
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实测
```json
{
  "cases": 3456,
  "unionChecks": 3456,
  "separateFalseFeasible": 539,
  "naiveSumFalseInfeasible": 215,
  "amountDedupFalseFeasible": 599,
  "revisionChecks": 3456,
  "controls": 13,
  "witnesses": {
    "separate": {
      "balance": 1,
      "reserve": 0,
      "a": 0,
      "b": 0,
      "fee": 1,
      "same": false,
      "truth": 2
    },
    "amount": {
      "balance": 1,
      "reserve": 0,
      "a": 0,
      "b": 0,
      "fee": 1,
      "same": false,
      "truth": 2
    },
    "sum": {
      "balance": 1,
      "reserve": 0,
      "a": 0,
      "b": 0,
      "fee": 1,
      "same": true,
      "truth": 1
    }
  }
}
```
后续：连接真实原生现金快照、实际付款身份与已授权跨决策承诺；检验并行确认、撤回和更正时旧投影失效；独立轨测试未见情景，产品轨负责唯一交接和交互。不可将该研究作为完整版本授权。