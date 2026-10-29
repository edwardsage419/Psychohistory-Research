# F008 第六阶段：ARK建档路径与拒绝越权访问的候选安全门

日期：2026-10-29 UTC。目标键：(privacy_safety,F008,phase6,unprotected-create-path-and-fail-closed-policy)。状态 PHASE6_BOUNDED_SYNTHETIC_POLICY_COMPLETE，F008总体IN_PROGRESS。

## 官方英文来源与本轮真实增量

Automerge Repo Keyhive官方API指南 https://automerge.org/docs/keyhive/ark-api-guide/ ，本轮直接核对文档创建路径：repo.create2通过idFactory创建受Keyhive保护并加密的文档；repo.create绕过idFactory，会静默创建没有访问控制或加密的unprotected文档。官方建议用isUnprotectedDoc(url)识别；未保护文档成员查询可能返回undefined，成员操作抛UnprotectedDocError。官方示例buildServerSubductionPolicy允许未保护文档ID绕过权限检查。以上属于官方文档陈述，当前包为Alpha，行为可能变化。

F008第五阶段已经登记未保护文档权限绕过。本轮新增可操作的创建路径风险：仅在创建后检查成员列表为空可能漏掉通过repo.create产生的未保护文档。未来候选规则是在创建时显式核验受保护状态，服务端必须确认授权策略已启用、网络适配器经过授权包装，并将无权限/未知/版本过旧一律拒绝。这里的候选规则不代表Automerge默认实现。

## 本地人工安全门实验

使用Python标准库建立纯人工Request状态：protected、server_policy_enabled、adapter_wrapped、online、version_current五个布尔条件，access等级none/relay/read/edit/admin，操作fetch/read/push/grant。候选门规定五个布尔条件均为真且访问级别达到操作阈值时才放行。对2^5×5×4=640个组合完整枚举，允许10，拒绝630。全部640项显式检查通过，拒绝全部未保护文档、未启用服务端策略、未包装适配器、离线、过期授权版本的组合。源码 research/privacy_safety/f008_keyhive_protection_gate_20261029.py，本地Python 3执行及py_compile通过。

这是自建策略的内部一致性检查。没有安装ARK、没有真实网络适配器、没有真实加密、密钥轮换、撤销同步或设备丢失测试。实际库运行时授权拒绝能力仍NOT_RUN；即使应用拒绝渲染，离线设备旧明文、旧密钥及备份擦除也不能据此判为完成。尤其离线时拒绝应用操作不等于物理擦除缓存。

## 风险与未来候选控制

R16：创建路径混用。受保护文档必须显式走保护创建路径并在创建后校验标识；误用repo.create导致敏感文档未加密的风险需运行时测试。
R17：策略未部署或适配器绕过。服务端策略、网络适配器和授权版本分别检查；缺一拒绝。
R18：撤销与历史副本。授权版本落后、设备离线或密钥/备份状态未知时，显示PENDING/UNVERIFIED，不宣称全局擦除。
R19：拒答与申诉。误拒绝时允许用户发起本地人工复核，禁止自动扩大权限。

全部控制 UNADOPTED。没有处理真实个人数据或实施个人决策产品。使用公开英文资料、现有执行环境、标准库；主动新增费用0，GitHub账单及免费额度UNKNOWN。证据为官方文档支持的API语义加人工E1策略测试，实际安全效果、跨设备撤销与历史数据删除尚未验证。

下一项F008：在可用的零费用固定版本ARK本地依赖出现后，优先对repo.create与repo.create2、未保护文档同步策略及旧授权版本重放进行真实运行时测试；依赖不可用则继续源码和测试审计，不进行收费安装。
