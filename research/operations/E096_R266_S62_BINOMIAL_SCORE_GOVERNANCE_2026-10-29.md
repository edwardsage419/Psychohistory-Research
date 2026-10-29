# E096 R266 S62 有限二项解析第三路线与治理审计

日期：2026-10-29 UTC。目标键：(operations,R266,S62,closed-form-binomial-score-coverage-third-route)。初始 main HEAD：44f823c4c421e63cf6695575059aa3ad59da50ff。状态 COMPLETE_BOUNDED_NONBLIND_E1。只读审计其他轨，不修改R/B协议、结果、索引或Codex PR。

## 已读来源与冻结顺序

实读 S62 冻结协议 protocols/R266_S62_FINITE_WILSON_COVERAGE_PRESCORE_FREEZE_2026-10-29.md、18行落盘结果 research/validation/R266_S62_EXACT_SCORE_COVERAGE_RECEIPT_2026-10-29.json、R与B实现源码、B运行收据 research/evidence_audit/B_R266_S62_V8_EXACT_GATE_EXECUTION_RECEIPT_2026-10-29.json、原R266验收JSON、R轨最新交接、原239交叉索引及五项旧P2队列快照、七个开放Codex PR摘要。原239队列是历史快照，不能直接推断当前研究缺失。TH131已归档，A轨Dryad原CSV仍受HTTP403限制。

冻结提交6cdc35c36bdf6d2f06761dff5b04a8af8aa1bd8b；冻结文件在该提交与当前main的Git blob均为6232b63d5fd1344b9ee8c7c6ecc53444ac358994。GitHub compare显示冻结提交至结果提交300ee9e71af6c0a0a7c9916b88de62e5f2673447领先3次提交且冻结为共同祖先。R266原始有限模拟正式结题状态单独保留；S62是新增限定扩展，不能把旧结题直接升级为S62全部验收。

## 本轮互补数学路线

已有R程序逐5328条来源计算，B程序按四点成功计数卷积，B V8收据记录18行180字段一致及5项负例拒绝。为避免复制相同算法，本轮使用封闭二项分布计算：IID下 K~Bin(n,p)，反向配对下 THRESHOLD_Q1的每对成功数为Bernoulli(1/2)，THRESHOLD_HALF恒为1，THRESHOLD_Q3为1+Bernoulli(1/2)，SYMMETRIC_EXTREMES为2×Bernoulli(1/2)。各对独立，直接通过组合数计算全部成功数分布、Wilson z=2覆盖、朴素插件方差期望及真实估计方差。

本轮在隔离V8实际执行，18行每行10字段，共180项逐字段与持久化结果一致，mismatches=0。冻结反例 SYMMETRIC_EXTREMES_N6 的 IID 覆盖31/32，ANTITHETIC覆盖3/4，ANTITHETIC朴素插件方差/真实方差1/3。针对方差篡改、覆盖篡改、重复整行和证据标签升级，4项独立负例均被严格逐字段比较拒绝。第一次构造的“重复世界名”控制因IID和ANTITHETIC本来共享世界名而无效，已改为重复整行并重跑；保留该测试设计更正，不计为发现主线错误。

本轮已阅读R/B结果，为非盲态第三路线内部E1。没有重新逐字节读取5328行原始CSV、独立重算原CSV SHA256或运行归档Node CLI。原始CSV blob身份来自仓库目录，原SHA256与B记录来自已读上游收据，不作为本轮新独立验证。原R266历史CI成功信息来自原验收JSON，本轮未重跑Actions。B运行收据明确 native_node_cli=NOT_RUN。

## 协作与风险

七个开放Codex PR均待审查；#1列出R257 S53比较器假阳性，#3提出修复，未合并PR不能算main验收。R257 S53原B盲态FAIL继续保留。A轨真实数据Dryad下载HTTP403，R073第二独立真人实验复验关口仍开放。最新R主线是R266 S62，不能将历史R344目录存在视作当前已推进至R344。未发现本轮检查范围内的冻结漂移、S62落盘180字段异常或跨轨文件覆盖。全仓库历史与全部CI未逐项检查，账户账单和GitHub免费额度未独立核验。

项目统一验收标准 protocols/RESEARCH_ACCEPTANCE_STANDARD_V1_2026-10-16.md 的E2/E3表述以真实来源可复算和独立新总体为核心；近期轨报告常用“真人E2/历史E3”简写，不能据此自动升降等级。建议后续在正式验收中按标准原文和实际数据总体逐项标记，避免类别错配。

下一步 E097 优先在本地已确认免费环境完成S62原生Node CLI及字节/JSON复验；如被其他轨认领则转向R267新阶段冻结顺序。当前不触发收费CI。新真人E2、新独立总体E3及外部团队复现均为0。
