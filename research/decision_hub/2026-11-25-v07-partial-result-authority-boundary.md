# v0.7 局部结果与决策授权边界：原生接入审计
2026-11-25。SOURCE_INSPECTED / ABSTRACT_GUARD_MODEL_EXECUTED / RESEARCH_ONLY / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。main 8c18401bd6a2a6a4e4c77c8d94644adf022602c4；候选 Draft #62 e61bbad10932edabc9a87483e5407fdae6c751cc。核对最新main、v3.2与同步规程全文、开放PR列表、近期提交、候选验收与开发报告、独立交接。未确认产品轨唯一近期交接的具体文件；去重依据已读取的第27轮原始研究提交984bf62a969ac0f368f21496fcacaecf903a6a38及相关提交检索，不能保证全库无重叠。第27轮已建立局部端口、有限域及依赖失效；本轮不重计该数学算法。

## 实际源码审查
固定候选 platform/future_model/src/psychohistory/decision_conversation.py，blob ed1c5aa8407f53ef3dfc1484ba1a18ef1edabcad。395–403行全局ready；426–443行清空analysis后在未confirmed时直接返回；480–489行select以analysis非空、ACCEPT和时间资格及确认作门槛；497–504行plan依赖已选方案及analysis；506–524行save有授权检查及analysis/state非空检查；571–591行_view依据analysis非空选择ANALYZED/CLARIFY；618–634行result_receipt以analysis非空标记COMPUTED。645行起的plain_measure_differences依赖已筛查方案。决策数学投影文件blob de49b71a3c8bb63c81539dd9c69b3c02b3e94c23。开发报告R57有第三方预算阻塞充分到岗信息、L02有未知夜班阻塞已有超限方案的记录；未重新执行原生入口。
现状保持全局阻断，未发现该抽象风险已实际发生；若未来把局部结果直接塞进现有analysis容器，phase/receipt/save以及带ACCEPT行的select可能取得额外资格。不能用全局ready=true或删掉阻塞项解锁局部计算。

## 设计候选
保留现有完整analysis及其资格规则，新增独立partial_analysis只读描述出口（不复用完整feasibility ACCEPT或推荐字段）。每个局部项绑定session、revision、授权代次、方法版本、原文及当前证据ID/单位/时间/主体/条件/范围、依赖及未决项。仅在可信宿主核对相关依赖时公布；未能界定相关未决影响时保持条件表达或UNKNOWN。收入差等描述项无选择、计划、保存为完整决定、执行或自动学习权限；条件违反证据不是全局最终拒绝。旧版本客户端应保持原CLARIFY与analysis=null，局部数据由明确支持的新客户端单独显示，旧客户端不能误解为完整分析。收据新增独立局部层，不抬高READY/COMPUTED；保留全局未决提示。选择/计划/完整记录只读服务端完整analysis，不能信任客户端提供的局部结果；部分草稿持久化另需授权与独立类型，不纳入本候选。撤回、旧修订、跨会话、来源变化、条件范围变化应失效，不能仅凭数值一致复用。独立测试须检查Web/API/CLI、历史与复盘、权限及旧客户端；当前只做结构研究。

## 实验
9个布尔开关全枚举512组合，抽象现行资格及人为设计的反面接入（含ACCEPT的局部结果写进analysis），再比较独立只读字段方案。ready和其底层因素在实验中独立取值，含真实运行不可能组合；计数不是实际缺陷、概率、用户覆盖率或独立样本。full/partial为人工夹具，选项身份、真实资源日期、授权代次及持久化未执行，抽象saveGrant合并其余存储前提；plan仅有定向空analysis控制。分离方案复用同一守卫故零差异是结构不变性 sanity check，不是独立安全验证。选择五个局部前提与夹具由本轮研究者确定，非正式产品阈值。以下代码可直接Node运行（实际本轮JS执行），无第三方依赖。
```js
function run(){
 const out={cases:0,blocked:0,partialVisible:0,naivePhaseEscalations:0,naiveSelectEscalations:0,naiveSaveEscalations:0,separatedEscalations:0,controls:0};
 // Source-derived guard model, not actual ConversationHub execution.
 const gate=(a,confirmed,temporal,saveGrant,planSelected)=>({
   analyzed:a!==null,
   select:confirmed&&a!==null&&a.feasibility.some(x=>x.status==="ACCEPT"&&temporal),
   plan:confirmed&&planSelected&&a!==null,
   save:saveGrant&&a!==null
 });
 const full={feasibility:[{status:"ACCEPT"}]};
 const partial={kind:"DESCRIPTIVE_ONLY",feasibility:[{status:"ACCEPT"}],authority:"NONE"};
 for(let i=0;i<512;i++){
   const [ready,context,option,source,scope,fresh,confirm,temporal,grant]=Array.from({length:9},(_,j)=>!!(i&(1<<j)));
   const analysis=ready?full:null, local=context&&option&&source&&scope&&fresh?partial:null;
   const old=gate(analysis,confirm,temporal,grant,false);
   const naive=gate(analysis??local,confirm,temporal,grant,false);
   const separate=gate(analysis,confirm,temporal,grant,false);
   out.cases++;
   if(!ready){out.blocked++;if(local)out.partialVisible++;}
   out.naivePhaseEscalations+=+(!old.analyzed&&naive.analyzed);
   out.naiveSelectEscalations+=+(!old.select&&naive.select);
   out.naiveSaveEscalations+=+(!old.save&&naive.save);
   out.separatedEscalations+=+(JSON.stringify(old)!==JSON.stringify(separate));
 }
 function ck(v){if(!v)throw Error("control");out.controls++}
 ck(out.cases===512);ck(out.blocked===256);ck(out.partialVisible===8);
 ck(out.naivePhaseEscalations===8);ck(out.naiveSelectEscalations===2);
 ck(out.naiveSaveEscalations===4);ck(out.separatedEscalations===0);
 ck(!gate(null,true,true,true,true).plan);
 ck(!gate(null,true,true,true,true).select);
 ck(!gate(null,true,true,true,true).save);
 return out;
}
console.log(JSON.stringify(run()));
```
实测：
```json
{
  "cases": 512,
  "blocked": 256,
  "partialVisible": 8,
  "naivePhaseEscalations": 8,
  "naiveSelectEscalations": 2,
  "naiveSaveEscalations": 4,
  "separatedEscalations": 0,
  "controls": 10
}
```
后续应以真实候选分支执行R57/L02及修改/撤回/过期对照，测试局部层不提高现有授权；需要实现时纳入所有者批准的完整版本。无生产修改、训练、CI触发请求、合并、部署、冻结改变或新增费用。