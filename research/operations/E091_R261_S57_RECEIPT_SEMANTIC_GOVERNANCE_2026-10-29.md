# E091 R261 S57 持久化收据的语义约束与治理审计

UTC 2026-10-29。目标键：(operations,R261,S57-1003be30,persisted-receipt-metadata-coverage-and-scoring-identities)。状态 COMPLETE_BOUNDED_NONBLIND_E1。初始 main HEAD 631c374ae8accdd5d8b58e7d0bc8269d71e0196c。

## 直接读取的远端证据及去重

通过 GitHub 连接器读取 S57 冻结协议，blob `3e6cdb5f0613d3b3434855541f49d758f9587803`；R 正式报告，blob `95637154f3074ee340dbea7cff488b7b5a99ffc9`；B 独立 Fraction 审计，blob `8fe265ed378d9a9186f862ebc6ef8b87f612bd6f`；R 轨交接，blob `bf6b1b2fd8a8885589174d34036d6cbdbba4e821`；R 持久化 JSON `research/validation/R261_S57_PREFIX_BRIER_EXACT_RESULTS_2026-10-29.json`，blob `8efb576b3ef6e5868ad54854d721e97b8621c6a4`。事前冻结 commit `1003be30bb7c7b003cf02496cf02bf663147a71f` 先于评分提交 `25605688fffbedf2976df31a255eba0ee5b01153`。

R 已解析 9216 条人工来源，B 已独立推导 27×16 个科学字段。本轮选择互补的 **落盘 JSON 元数据、唯一覆盖、风险代数恒等式** 审计，先读过 R/B 结果，属于非盲态内部核验。没有再次完整读取原 9216 行 CSV，也没有运行原 B 的完整 JSON Python CLI。

## V8 BigInt 精确检查

直接对真实远端 JSON 解析并执行 BigInt 精确分数运算。检查身份 R261/S57、E1 分类、E2/E3=0、来源 blob、R073/PESEN 冻结、oracle 非样本外标记；27 个唯一 (world,K0)、九世界各 K0=0/1/2、来源分层每世界 256/512/256、总 9216；概率界 [0,1]；oracle Brier=p(1-p)；前缀信息收益=oracle 风险减前缀风险；均场超额风险=(MF 预测概率减真实条件概率)²；前缀≤oracle≤均场风险；联合正确 Brier=p(1-p)；联合错误独立近似的额外风险=(错误概率减真实概率)²。

真实执行 **450 项显式断言，失败 0**。27 组、九世界和总 9216 来源计数一致。六个独立错误注入全部被拒绝：重复复合键、E2 伪升级、来源行数篡改、oracle 风险篡改、联合风险篡改、R073 冻结状态篡改。

本轮 V8 检查通过 GitHub 连接器读取的原始 JSON 在隔离执行环境运行。该第三路线审计程序尚未归档为 Node CLI，因此不能声称完成归档后命令行验收；450 次代数与元数据检查也不代表重新计算全部原始来源。

## 治理状态与开放关口

最新检查的 R 系列为 R261 S57；理论 TH126 已归档。A 轨 ds007822 原始许可冲突仍开放，不能作为 R073 直接复验。R257 S53 原 B 盲态失败保留。Codex PR #1 至 #6 均 OPEN、merged=false；PR #1 的检查器假阳性和 PR #3 的严格门仍属待审证据，PR #4/#5/#6 的 CLI 补充也没有计为 main 已验收。

检查范围未发现本轮冻结协议变更、同名覆盖或 E1 误升级；未完成全仓历史审计。未独立核验账户账单和免费 CI 额度，没有启动 Actions。新增 E2=0、E3=0、外部独立团队复现=0。

未关闭关口：R261 S57 完整原 JSON Python CLI、R Node CLI、原 CSV 第三路线全量来源核验。下一轮如继续应选择其中一个具体关口，记录已读范围和非盲态。
