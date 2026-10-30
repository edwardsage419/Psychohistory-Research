# A轨：NV_games 真实来源的 period 重置语义与独立性阻塞补充

日期 2026-10-30 UTC。目标键 (A,NayVorobeychik2016,JohnNay-datafsm-c2e55eab,period-reset-and-identity-negative-control)。状态 STATIC_SOURCE_NEGATIVE_CONTROL_COMPLETE / REAL_RDA_DECODE_NOT_RUN / R073_NOT_QUALIFIED。

## 本轮实际新增的上游阅读
固定作者公开仓库 https://github.com/JohnNay/datafsm ，commit c2e55eab12f1a24d3a5b09a9b42aeefff8bc5be4。实读 README.md Git blob ad58c0e2bc424c64a2d555ed793f85c3f3150833、R/data.R Git blob 2a1dc849c34036026f45d1238d586376b876ec5f、man/NV_games.Rd Git blob be625b217505dd05781f5bd9c12925df673a7ac0、DESCRIPTION Git blob a27bb2ea9212451dc3827dd2fb58f7673c74e1ab。主论文 Nay 与 Vorobeychik (2016), Predicting Human Cooperation, PLOS ONE, DOI https://doi.org/10.1371/journal.pone.0155656 。

README 的 **Fake Data Example** 明确生成1000次重复的10轮人工游戏，代码 `period = rep(seq(rounds), reps)`，故同一个 period=1 在这一包作者提供的标准示例里重复1000次。这个人工示例说明 period 只表达局内轮次，不能被用作稳定参与者、场次或配对 ID。该示例完全人工，严禁作为 NV_games 的真人行数或真实重复局数。README 还把模型输入描述为每行一个时间点行动，原示例没有稳定身份字段，且每次 period=1 重启；训练与测试如果仅按 period 或单行随机拆分，可能跨同一序列共享历史。此项是对候选数据处理的具体负例门，尚未证实作者对 NV_games 做过此错误切分。

R/data.R 与 man/NV_games.Rd 为同一51列数据字典的源注释与自动生成帮助页，属于一条文档证据链，不能冒充两次独立原始数据核验。文档声称168386条行为记录、30种变体、八项原研究；实际 RDA 逐行解码仍 NOT_RUN。该文档没有提供稳定参与者/配对/会话 ID；group 是游戏版本，data 是八项来源研究代码。不能据此构造 R073 冻结的独立百轮双人实验评分。原论文 S2 ZIP 公开链接 https://doi.org/10.1371/journal.pone.0155656.s002 本轮再次尝试打开未能取得二进制；CSV 表头、行数、局次边界仍 NOT_VERIFIED。二进制 RDA 的原有固定 Git blob 36a961908385a7fe33ba688479b5dfc7b0a6b609，许可：软件 MIT，八项真人数据再分发权 UNKNOWN。

## 复现准备与阻塞
已固定可执行的下一步检查：在无需付费的本地 R 环境解析原 RDA 或出版社 S2 ZIP；统计各 data/group/period 的记录量、最大局内轮次、每轮重复数、缺失值及历史列重置；追溯真正参与者/配对/会话键，按原实验逐项去重；只有独立来源与100轮条件核验通过才考虑冻结 R073 的外部评分。此轮没有获取原始二进制并解析，不能报告真实行级核验完成。E2样本外预测0，E3历史预测0，新增费用0。原始真人数据未再发布。
