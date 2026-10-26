# A轨 Kuper-Smith与Korn 2025 真人双人互动镜像复现准备

日期：2026-10-26。状态：EXECUTABLE_PREPARATION_SELFTEST_PASS / REAL_ROWS_NOT_REEXECUTED / LICENSE_PENDING / R073_TRANSFER_NOT_APPROVED。

## 来源和既有事实

英文原作者仓库 `dnhi-lab/losses_gains_2x2` 固定提交 `345348cdc0018e8e030b05fb47dc845fd3e0d29a`。本轮重新读取公开来源Git树、`analysis/format_data_Exp_1_2_3.m`、`analysis/exclude_participants_iterated.m`、README和MIT LICENSE。清洗CSV的Git blob `ffd6776f3e9fd1444c84e50e4c61e3ff418a2488`，仓库元数据大小3139058字节。原作者格式化脚本定义实验、六人组、本人、对手、全局试次、区块、本人和对手当轮二元行为及上一试次行为字段。

此前独立归档 `KUPER_SMITH_KORN_2025_RAW_CLEAN_36000_33702_ROW_AUDIT_2026-10-26.md` 已核验原始36000行、清洗33702行、实验2/3清洗26601行及239个可见双人配对标识。本轮无法通过当前文件接口重新获取3.1MB CSV文本，未重新执行真实行级镜像检验，不重复计入前次核验。

## 新增可执行资格程序

新归档 `research/data_scout/kuper_smith_korn_dyad_mirror_gate_20261026.js`，仅使用Node.js内置fs，无收费API、无数据再分发。接收本地公开清洗CSV路径，按实验、群组、本人、全局试次建立键，逐条寻找同一试次对手的互为镜像记录；分别统计缺失镜像、对手身份不互指、本人/对手行动不互换、区块不一致、重复键、行为编码、上一试次字段缺失、独立组人数及双人配对数量。输出聚合统计，不上传个人行。明确区分缺失镜像与真正矛盾的镜像；完整六人组15种无向配对仅作为结构性参考。

本轮已实际执行两个合成自检：互为镜像的两条行成功识别2个有向镜像及1个无向互动；故意将对手动作改坏后检出2项镜像行动冲突。结果 `SELFTEST_PASS`。这两项是E1程序测试，绝不计为真人E2核验。

在有完整原始CSV且数据许可明确后，可执行：

`node research/data_scout/kuper_smith_korn_dyad_mirror_gate_20261026.js /path/to/data_Exp_1_2_3_cleaned.csv`

## 开放阻塞和R073边界

清洗CSV真实镜像运行、跨缺失试次的时间顺序、双方共同可见信息、不同收益矩阵与R073冻结输入映射、按六人组整体留出、以及真人数据许可范围仍待验证。作者仓库根MIT许可的文字涵盖软件及相关文档，真人行为CSV的独立再分发范围仍需谨慎核实。本轮不再分发CSV、不访问非公开个人数据。

原R073模型与评分规则、PESEN v0.1均保持冻结；没有真实预测评分，E2=0，E3=0，外部独立复现=0。没有主动新增费用。
