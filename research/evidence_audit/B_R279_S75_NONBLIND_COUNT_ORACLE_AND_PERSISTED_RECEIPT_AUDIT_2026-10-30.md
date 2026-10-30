# B轨：R279 S75 非盲态独立计数与远端收据审计

日期：2026-10-30 UTC。审阅范围：R279 原人口校准结果及 S75 新增冻结、144行来源 CSV、九世界 JSON。原 R279 正式验收状态未修改。审计程序 research/evidence_audit/b_r279_s75_strict_receipt_20261030.js。

独立方法：Python Fraction 直接枚举两组成功次数 (kL,kH) 的九种组合，按两个 Binomial(2,theta) 质量计算样本 REL 与其为零/不超过人口 REL 的概率，不读取 R 路线的四位有序来源表。九世界 REL 期望与零事件概率均与独立 V8 144行完整枚举一致。进一步用 vL+vH 的解析公式检查 REL/RES/UNC 的有限样本偏差，九世界全部通过。

远端核验：重新通过 GitHub fetch_file 读取 research/validation/R279_S75_ALL_144_EMPIRICAL_SOURCE_ATOMS.csv（Git blob 4905c6df24a73d8a940b2442c44e91a83f4a0aab，8420字符）与 R279_S75_EXACT_RESULTS.json（blob 6c47a52eb547901e7f9ed3d006eec35450735e24，6638字符）。在 V8 中执行归档检查函数同内容，独立重算144条来源质量、四个样本统计量、逐行 Murphy 恒等式、九组人口指标和加权期望、零质量及世界唯一覆盖。144行、九世界、99正质量来源全部 PASS。

七项实际错误注入均拒绝：重复来源、删除来源、修改逐行 REL、修改汇总 Brier、把 E2 从0提升至1、将原 R279 冻结标志改为 false、篡改零质量来源的概率。拒绝分别发生于覆盖、逐行指标、汇总指标、元数据和来源概率门。

本轮是同一项目内的非盲态程序性与方法独立复核，不能称外部研究团队复现。归档 Python 的原生 CLI 和归档 JavaScript 的原生 Node CLI 尚未执行；跨运行时对归档文件完整字节的重建尚 OPEN。全仓库测试及 GitHub Actions NOT_RUN。E1=人工；新增 E2=0、E3=0。R073 和 PESEN v0.1 冻结。结论范围仅限固定四位样本和九世界，未证明真实预测的校准或模型因果有效性。

下一步原生命令行执行 R279 S75 Python --selftest / --emit，比较完整 CSV/JSON 字节；运行归档 B Node CLI 对实际远端文件复验。若有差异，保留原始 FAIL 并增量修复，不回写冻结结果。
