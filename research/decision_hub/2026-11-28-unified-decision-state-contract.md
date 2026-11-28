# 统一决策状态与跨模块合同候选
2026-11-28。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / NATIVE_NOT_RUN / authority NONE。
基线 d242f65c897418bcef231b66a0393faa0cec96cc；开放PR63/62/61/60/59。读取PR63固定候选734686980b19da9291bdd08b67d4e2519c011acf的V08_ENGINE与V08_COMPOSITION。继承RawTurn、ConversationHub、CompositionScope、GroupedPort、DecisionRegistry、CandidateRegistry及原生资源账本，不建立平行权威。唯一近期交接及全库去重未核实。
## 合同
RawTurn原文及坐标→语义候选→宿主确认义务与账本→证据资格和用途核验→参数投影→方法适用性及硬约束→联合计划→计算见证→原子发布→授权记录与观察。候选永不直接写权威账本。每个参数保留身份、原文依赖、证据版本、主体、单位、时间、实际/预测/假设类别、情景支持、用途及缺失状态。集合依赖包含成员身份及否定依赖。单位换算须先由受审方法产生新派生值，不能直接匹配不同单位。跨期现金按事件顺序，任务按身份去重。未知不等于零，不等于不适用。局部结果authority NONE。
作用域复用CompositionScope；增加类型化参数口径和完整依赖清单，不改变既有接口语义。计算缓存仅内部纯计算；发布重新核验当前宿主。方法未准入仅隔离运行。结果区分可行见证、不可行覆盖、未完成、前沿及失效。检查点认证不替代覆盖证明。个人反馈不得自动训练或推断未选择反事实。
## 有限合同负向复算
```js
function experiment(){let fields=["instance","revision","grant","evidence","world","method","unit","period","subject","membership"];let base=Object.fromEntries(fields.map(k=>[k,1]));let o={cases:0,correct:0,weakFalse:0};for(let mask=0;mask<1024;mask++)for(let confirmed of [false,true])for(let fresh of [false,true]){let p={...base};fields.forEach((k,i)=>{if(mask>>i&1)p[k]=2});let ok=confirmed&&fresh&&fields.every(k=>p[k]===base[k]);let ref=confirmed&&fresh&&mask===0;if(ok!==ref)throw Error("mismatch");o.cases++;o.correct+=+ok;o.weakFalse+=+(confirmed&&fresh&&p.unit===base.unit&&!ok)}return o}
console.log(experiment())
```
实测 {"cases":4096,"correct":1,"weakFalse":511}。十字段固定整数标记的全掩码及确认/时效布尔组合；仅检验严格同一作用域的必要条件，非通用语义兼容性、单位转换、实际时效或独立验收。参照与实现逻辑等价，属于合同真值表；与既有跨修订研究存在概念重叠，不视为新独立样本。参数及合同扩展由研究者提出。
## 后续验收矩阵
原文遗漏/错归属→语义义务；过期/撤回/恶意来源→事实资格；不同单位/主体/时间→参数映射；共享资源重复→账本；未来信息泄漏→策略分组；遗漏分支/错误剪枝→覆盖证书；崩溃/重放/撤回→恢复及发布；反馈污染→事前事后隔离；离线真机→设备资源与可用性。各项需原生入口、独立留出、固定版本及对照，未执行不得标PASS。
下一步统一可执行原型及资产索引，未授权正式版本开发、训练、合并、部署或新增费用。