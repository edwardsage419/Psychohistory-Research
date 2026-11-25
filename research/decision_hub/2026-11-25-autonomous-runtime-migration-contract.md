# v3.2 自主认知专项第1轮（累计第60轮候选）：运行时迁移与历史证据隔离

2026-11-25。RESEARCH_CANDIDATE。main 基线 bb44b004dbd282567e00a4a7d00020d1b412d583；PR #61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，open Draft。读取v3.2、AGENTS.md、同步规程（前部）、最近10提交、13开放PR、完整树路径检索（truncated=false）、唯一近期交接 research/coordination/DECISION_WORKBENCH_PRODUCT_PRIVACY_HANDOFF_2026-11-19.md blob 5e74f4f0b37141d631740e844ad8bbbfed232e07（首尾，未逐段审查全文）、第2/58/59轮。旧Qwen训练与评价方向由v3.2取代，保留第59轮历史数据。未找到decision_hub目录名含migration/runtime/dependency/import/autonomous的专门条目，不能排除其他标题下重复内容。与第58轮单义务修复区分，本轮聚焦第三方运行入口和历史记录读写兼容。

## 固定源码审查
- main platform/future_model/pyproject.toml blob 98b211adda09baadafa58007a49bdb18a382e0bd：应用版本0.5.0，直接依赖fastapi/pydantic/uvicorn；未审核传递依赖。decision_service.py 8b35e200ef8915ba21141906a90ecd067f6c4320，decision_api.py b0f461e04506f2af92c0bac89d218aa0cac9ec5c：独立v04/v05服务、记录和复盘入口。
- 固定PR decision_conversation.py f505aeab2d9e5e0a9c8957ce6e039dea174918a7，L15、163-173、205-240、253-257：显式导入ConversationOllama，provider or ConversationOllama()，status读取provider，_ingest每次调用propose且合并options；interpret单独调用。原文匹配的规则解析claim以USER origin进入账本，source channel为user_self_report。USER标记可能合理描述信息来源，但不足以独立标记解析器身份及版本。
- decision_local_ai.py 726b7a2e0da64af7037d892ac8bf508412deb5d6，读取L1-200：环境变量控制、固定回环传输、Qwen允许名单，默认禁用；未调用模型或传输。现有安全限制保留为历史证据，默认禁用不等于从运行时移除依赖。
- decision_conversation_api.py 85ff09e20483211deec434ac252047f2c0265ef1 L23-31：start/turn均保留use_local_model布尔字段；decision_conversation_cli.py 3f6b59240a65c44ebb13857e0f030c3d4e74ddcd共享invoke入口；web/src/DecisionConversation.tsx 443b6141aeb1aa3c52595dace7a5726d7d6667eb L74-79、202-203、244、265保留模型开关及请求参数。
- decision_evidence.py b45932af6346fb0df072ffb6cb13ef0cd6991b7a L18-103、120-132：ClaimOrigin USER/LOCAL_MODEL/RULES；SourceMetadata、ClaimInput、EvidenceEntry。需分离事实来源、解释算法、版本、候选资格与历史状态，不将旧LOCAL_MODEL重命名为USER/RULES或自主来源。现有provider主要提供候选选项；本轮没有发现实际历史LOCAL_MODEL claim的数量或存在证明。

## 候选迁移契约
1. 自主解析器接口输入原文、版本化上下文、目标范围；输出候选解释、原文跨度、独立未知、算法版本及来源；候选不能自行确认、发布或联网。移除默认Ollama实例及第三方运行入口；历史适配代码保留在旧版本或隔离归档。需要完整原生API/CLI/UI/包依赖检查及断网运行验收，静态审阅不足。
2. 兼容旧start/turn的布尔参数：缺省/false继续自主路径；true继续自主路径且明确返回已停用第三方AI的通知，绝不调旧模型。此为研究选择，版本化API也可选择明确拒绝旧true，最终产品决策待授权。其他类型拒绝。旧记录只读兼容，历史来源不改，UNKNOWN不能升级；历史模型或来源不清记录须有原文、重新解析、用途授权、当前版本确认及语义义务核验才进入下一资格门。新派生须保留父记录、解析器身份与版本、原文摘要、权限快照；不能把重新解析后的结果记作旧记录自身。若旧USER/RULES缺乏可证明解析链，归为UNKNOWN。历史数据中没有原文的项目保留只读历史，允许用户重新提供信息建立新记录。合成夹具用布尔代替真实宿主验证，不是认证或持久化实现。
3. 与第58轮语义质量协议、现有数学引擎及记录恢复接口衔接。候选通过语义门仅允许进入下一适用性/证据/硬约束/数学等资格门，不能直接推荐。独立轨应测试旧请求true、配置环境变量、恶意历史字段、跨版本/权限撤回、异常恢复、依赖与实际网络行为，禁止真正调用Qwen/Ollama。产品轨更新唯一交接与历史导出边界；模型轨负责自主解析器。未授权Codex工程开发。

## 实际有限实验
JS运行16个请求类型组合，256个origin与6位资格组合。逐项对照独立写法的布尔谓词（同一研究者，非独立验收），原始夹具冻结。naiveFalse是故意忽略旧来源额外条件的简化对照错误，不是现行平台实测漏洞。126/128旧模型及UNKNOWN组合未进入下一门，2组满足全部条件。没有测试完整历史记录schema、真实原文重解析、真实权限、动态加载或网络隔离；无真实用户样本、性能测量、CI或生产准入。以下脚本在连接器JS环境实际执行等价逻辑，复制到Node可复算：

```js
const probe = function(){
 const check=(x,m)=>{if(!x)throw Error(m)};
 function entry(flag,mode){if(!["start","turn"].includes(mode))return "INVALID";if(flag!==undefined&&typeof flag!=="boolean")return "INVALID";return flag===true?"AUTONOMOUS_WITH_RETIREMENT_NOTICE":"AUTONOMOUS";}
 function derive(record,ctx){
  if(!ctx.purposeAllowed)return "PURPOSE_DENIED";
  if(record.origin==="LOCAL_MODEL"||record.origin==="UNKNOWN"){
   if(!ctx.rawAvailable)return "HISTORICAL_ONLY";
   if(!ctx.reparsed)return "REPARSE_REQUIRED";
  }
  if(!ctx.currentVersion||!ctx.confirmed||!ctx.obligationsPassed)return "PROVISIONAL";
  return "ELIGIBLE_FOR_NEXT_GATE";
 }
 let requests=0,invalid=0,notice=0,normal=0;
 for(const mode of ["start","turn"])for(const flag of [undefined,false,true,null,0,1,"true",{}]){
  const got=entry(flag,mode);const expected=flag===true?"AUTONOMOUS_WITH_RETIREMENT_NOTICE":flag===false||flag===undefined?"AUTONOMOUS":"INVALID";
  check(got===expected,"entry");requests++;if(got==="INVALID")invalid++;else if(got.includes("NOTICE"))notice++;else normal++;
 }
 let cases=0,eligible=0,legacyBlocked=0,naiveFalse=0;let counts={};
 for(const origin of ["USER","RULES","LOCAL_MODEL","UNKNOWN"])for(let mask=0;mask<64;mask++){
  const [purposeAllowed,rawAvailable,reparsed,currentVersion,confirmed,obligationsPassed]=Array.from({length:6},(_,i)=>!!(mask&(1<<i)));
  const ctx={purposeAllowed,rawAvailable,reparsed,currentVersion,confirmed,obligationsPassed},record=Object.freeze({origin,id:"historical-1"});
  const got=derive(record,ctx),legacy=origin==="LOCAL_MODEL"||origin==="UNKNOWN";
  const expected=purposeAllowed&&currentVersion&&confirmed&&obligationsPassed&&(!legacy||(rawAvailable&&reparsed));
  check((got==="ELIGIBLE_FOR_NEXT_GATE")===expected,"eligibility");
  check(record.origin===origin,"origin mutated");
  counts[got]=(counts[got]||0)+1;cases++;
  if(expected)eligible++;
  if(legacy&&!expected)legacyBlocked++;
  if(purposeAllowed&&currentVersion&&confirmed&&obligationsPassed&&!expected)naiveFalse++;
 }
 return {requests,invalid,notice,normal,cases,eligible,legacyBlocked,naiveFalse,counts};
};
console.log(JSON.stringify(probe(),null,2));
```

```json
{
  "requests": 16,
  "invalid": 10,
  "notice": 2,
  "normal": 4,
  "cases": 256,
  "eligible": 10,
  "legacyBlocked": 126,
  "naiveFalse": 6,
  "counts": {
    "PURPOSE_DENIED": 128,
    "PROVISIONAL": 70,
    "ELIGIBLE_FOR_NEXT_GATE": 10,
    "HISTORICAL_ONLY": 32,
    "REPARSE_REQUIRED": 16
  }
}
```

无第三方模型调用/训练、个人数据、生产代码更改、PR合并、部署或新增费用。原冻结协议与证据等级不变。下一轮优先研究自主组合语义的可复算解析算法及未知覆盖，与现有第24/58/59轮接口衔接；不发布零碎Codex任务。
