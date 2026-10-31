# B轨独立审计：R312 S108 全 1728 路径非盲态 Fraction 复算

日期 2026-10-31 UTC。目标键 (B,R312,S108_freeze_8e8e0c06,full_path_exactness_and_mutations)。审计在 S108 计算前冻结协议之后执行；已经阅读冻结规则和生成器的研究范围，因此 NONBLIND。不能称外部独立团队复现。

审计对象：research/validation/R312_S108_ALL_1728_TWO_STEP_PATHS.csv Git blob 390acf787d5de916ccf3d5b946fb52a08d16dc96，48 世界摘要 JSON blob 848900340c0d38ee068275345751b356ca2ef518；原 R312 一步 1152 行源 CSV blob 498eefccf66d71ebf28323be7caa97309b06e8f6。原冻结协议 blob 77ec37a7f2fef4567f9c73f4593c7b7b09146f20，新增冻结提交 8e8e0c06deb5a8e122bfcfe8c7312d679f93a98c。

方法：本地 Python 3.13.5 的 Fraction 独立审计脚本 research/evidence_audit/b_r312_s108_independent_fraction_audit_20261031.py，使用中点与半差公式而不导入 Node 生成器，独立生成 1728 条路径及 48 世界期望；与 Node 输出 CSV 的 164842 字节逐字节一致。两文件 SHA256 均为 17a84709e2d2762e3660d6ee21387d486accfe9e51627589c94ee3af4b360e54。摘要 JSON SHA256 为 e4c36c7301abaeb4a68909f7694c87e137e84bc6cfe07658f99d1b73924d942a。原 1152 条 CSV 直接从 GitHub 读取并核对每行 7 个来源/行为字段，总计 8064 项比较零差异，1152 个唯一来源键。

实际执行 Python 普通模式 PASS，python -O 模式 PASS。8 个有效错误注入全部拒绝：删行、增行、重复行、世界标签篡改、终态篡改、合格性标志篡改、离散度篡改、列名交换。明确检查变异不是 no-op。程序内显式 ValueError 验证不依赖 assert。核对完整 48×36 路径，48 个摘要、720 个配对顺序对照，结果为顺序敏感 204，第一步严格下降 22 世界，第二步严格下降 22 世界。阈值零的 16 个世界为无变化负对照。

局限：全量人工精确数学及来源一致性，仅内部非盲态 E1；独立脚本重算与外部盲态团队独立复现不同。远端归档 Node 源程序原样 CLI 尚未在本阶段执行，GitHub Actions 未运行；真实样本外预测、基线比较、校准、重采样区间及因果推断均不适用于本人工枚举的确认性结论，真人 E2 与历史 E3 为 0。若后续真人实验，需独立参与者/场次分组、预冻结预测和基线、校准与不确定性评估。R073/PESEN 冻结。

状态 INTERNAL_NONBLIND_E1_AUDIT_PASS_WITH_NATIVE_CLI_OPEN。无费用操作。
