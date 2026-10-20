# R143 Arthur 1989：路径依赖与技术锁定

原目录P1 / 06-001 Institutional Path Dependence，2026-10-20。一手研究 Arthur (1989), *Competing Technologies, Increasing Returns, and Lock-In by Historical Events*, DOI https://doi.org/10.2307/2234208；实际核阅原刊p118–122。严格采用原 Table1 技术采用模型的R/S两类子例，以Fraction求精确吸收概率，不将技术采用概率冒称具体历史制度预测。

- 等可能入场、正反馈时，d=nA−nB到±3锁定；从d0=0最终锁定A或B各1/2，首次锁定平均19/3次，首达概率P(τ=3+2j)=(3/8)(5/8)^j。
- 固定3R/3S共20种6步排列，RRRSSS→6A，SSSRRR→6B，交替RSRSRS→3A3B；两条独立树/DP概率路线吻合。去掉正反馈后，20种顺序均3A3B。
- 附加B技术成长斜率更大的反事实**不是Arthur原Table1**；主研究无新增E2真人或E3历史预测。

归档：[事前冻结协议](../../protocols/R143_ARTHUR_1989_INCREASING_RETURNS_PATH_DEPENDENCE_EXACT_ABSORBING_FREEZE_2026-10-20.md)｜[科学报告](R143_ARTHUR_1989_SCIENTIFIC_REPORT_2026-10-20.md)｜[86项Python单测＋计算程序＋全机器结果ZIP](R143_Arthur1989_Path_Dependence_86_Tests.zip)｜[结果摘要](R143_RESULTS_SUMMARY.json)｜[科研验收状态](R143_FINAL_ACCEPTANCE_STATUS.json)｜[双环境CI](../../.github/workflows/r143-arthur1989-path-dependence-86-tests.yml)。

解压后运行：`python -m unittest -q test_r143_arthur1989_exact.py`；`python r143_arthur1989_exact.py > replay.json`。R073/PESEN v0.1冻结；全部R学习结束后再分类归纳、后熔炼。
**正式远端复验：** [GitHub Actions 39395394113](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39395394113) completed/success；原始研究源码commit `3b0ff26f9997af474d303fc3edb9f2c29ab6c150`。Python3.11 job118536757583运行86个unittest in 0.077s；Python3.12 job118536757840运行86个in 0.100s。共172次真单测、零失败，两个环境各四项SHA256均通过、全部20顺序及首达概率机器JSON逐字节回放成功。[详细机器验收收据](R143_PHASE_A_172_REAL_TESTS_ARTHUR_EXACT_ABSORBING_GITHUB_CI_RECEIPT.json)。E2/E3新增均为0。
