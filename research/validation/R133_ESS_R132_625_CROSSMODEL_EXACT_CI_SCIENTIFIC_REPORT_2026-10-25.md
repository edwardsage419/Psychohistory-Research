# R133严格ESS与R132连续复制子相图的625个二策略人工博弈交叉审计

日期2026-10-25。original239 05-009，E1合成数学。既有R133原刊研究继续保持2026-10-20的有界验收；本次为增量跨代码一致性验证，不开展R系列统一分类或模型熔炼。

## 来源、事前冻结和独立算法
R133依据 Maynard Smith & Price (1973), *The Logic of Animal Conflict*, Nature 246:15–18，DOI 10.1038/246015a0 的严格ESS双条件。R132依据 Taylor & Jonker (1978), *Evolutionarily Stable Strategies and Game Dynamics*, DOI 10.1016/0025-5564(78)90077-9 的连续复制子方程。所用625个整数矩阵均为本项目数学构造，不是动物或人类行为数据。

事前冻结协议 `research/validation/R133_ESS_R132_PHASE_PORTRAIT_625_CROSSMODEL_PROTOCOL_FREEZE_2026-10-25.md`，blob `3560563dfc68f46b137e0db6df7f7c4d6bab9327`，先于本轮脚本和CI。
独立审计程序 `research/validation/r133_ess_r132_phase_portrait_bridge.py`，blob `b2ace7b7792093f10f8a82c14249d93996066243`。读取此前已在真实CI中独立核查的 R132 625行CSV，blob `6f1a5b18c5fd11aba9a656fa5667516334499e30`；再读取既有 R133 正式验收 `research/R133/R133_FINAL_ACCEPTANCE_STATUS.json`，blob `70d36423e87eca9a14f7b6f9f18177e66c9116d5`。两份输入的Git blob身份均强制检查。

新程序直接从a,b,c,d推断纯A严格ESS、纯B严格ESS和内部混合严格ESS，不调用R132相图分类代码。先计算ESS判据，再逐行比对R132相图结果。全部625/625行一致，包含弱Nash边界。聚合结果为纯A严格ESS300、纯B严格ESS300、两纯策略同时严格ESS100、内部混合严格ESS100、没有严格ESS25。与旧R133正式验收的五项冻结统计全部一致。两项负对照明确拒绝“只有严格一阶Nash才是ESS”和“中性弱Nash也算严格ESS”。

## CI核验与有限科学结论
GitHub Actions run `40122771095`，head `1adf985bfce3d75ac466fb3bcb5179661ad89541`，job `120957709958`，`completed/success`，实际日志打印 `R133_frozen_status_verified=true`、`crossmodel_class_matches=625`、`R133_625_EXACT_BRIDGE_PASS`。
工作流 `.github/workflows/r133_ess_r132_phase_portrait_625_e1.yml`，blob `d5579fc25180f19241d86fabe417601cdf23879c`。

限定状态：`PASS_BOUNDED_INTERNAL_R133_ESS_R132_PHASE_PORTRAIT_BRIDGE_625_E1_CI`。仅证明二策略固定有限支付域下，静态严格ESS分类与相应连续复制子相图一致。R131既有三策略ESS与动态不等价反例依然成立，不能把二策略结论推广到一般三策略或多群体系统。

此CI没有重新执行R133原ZIP中的36项旧测试，原R133既有CI run `39368129476` 独立保留；本次审计执行的是新Python程序和既有验收JSON的身份核查。数据与数学假设共享，属于项目内部方法复核，尚无外部团队独立复现。E2真人预测新增0，E3历史预测新增0。原239全局队列与R073、PESEN v0.1均不修改。免费公开标准Ubuntu runner，无新增收费资源。
