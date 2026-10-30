# B轨补充：R280 S76 GitHub 持久化字节身份及 CI 门

日期：2026-10-30 UTC。基线 main HEAD `c214007685ae115c74c32545a817b9ab57fd0200`。冻结提交 `468ebb3006e864437fb8fc17cfcb39ed70b1bc1e` 先于全部新增结果。此前 B 报告中的远端文件字节重取 OPEN 已通过本补充关闭。此补充是同项目内部非盲态归档复核，不能升级为外部独立科学复现。

从 GitHub main 实时重新读取 R 原生 Python、B 原生 Python、A 复算 Python、完整768行CSV、三世界JSON及 R/A/B 三份科学审计报告，8/8 个文件的 Git blob 与本轮实际本地生成或执行的文件完全一致。关键身份：R源 `ebe5ff429b21850fd6b2724d81152267f6c01f63`；B源 `694daac7a45fec413fb2162e9a06986654963ee6`；A源 `aea61764df2c8699d4c949345c0fa6bec17a5cea`；CSV `3d2b095f7a54510ff4c9d6e7cd70c8bf35054cc5`；JSON `bd5187280bd5b1411536ada915b235830ba51481`。远端CSV为768行，三真率各256行；JSON freeze_commit 正确，证据等级 E1。

原 B 脚本第一次创建提交 `3cac0779f7cc0750fa4fb1b20a184d15820ba556` 额外包含一个空行，导致初始 blob 与本地执行源不相同。本轮检测后使用原文件 blob SHA 乐观并发校验修正该空行，提交 `3a3c72bbe75bbde51d3bef63692b02a301a2f0ed`，最终 B blob 与本地实际执行脚本严格一致。该格式差异未改变计算语义，原提交保留可追溯。

本地原生 R --selftest/--emit PASS；本地原生 B 对完整CSV/JSON验证 PASS，75独立二项组合、768行、48训练前缀和六个错误注入全部通过。远端原文已重新获取并验证字节身份；没有在第二台机器上独立执行远端源码。A的公开原始真人CSV由连接器直接完整读取并通过独立JavaScript核验；归档A Python脚本只完成语法编译，未对原始CSV进行原生命令行复算。

本轮提交比较 `c2140076...main` 至结果报告提交显示新增10个提交、9份新增文件，旧研究文件在最终 diff 中无修改。原 original239 v7.8 blob `36f24235901172642c46853298aebb421f1a3552`，154项待核队列 blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f` 未变。PR #1、#3 仍 open。GitHub 全部事件 Actions 查询在最终结果提交返回0项；本轮没有触发 Actions，CI=NOT_RUN。账单与免费额度未独立核验。

科研状态：R280 S76 有界人工 E1 内部数学与持久化身份核验通过；外部独立复现、真人E2预测、历史E3预测仍0；原 R280 正式有界验收不变。R073/PESEN v0.1冻结。
