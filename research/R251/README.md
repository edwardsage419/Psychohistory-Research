# R251 李雅普诺夫稳定性（11-011，P2）

九世界405完整初值—时点人工原source，真实有界E1结题`CLOSED_BOUNDED_E1_DISCRETE_LYAPUNOV_CANDIDATE_AND_TWO_STEP_PROOFS`。

[事前冻结](../../protocols/R251_LYAPUNOV_9_RATIONAL_MAP_WORLDS_405_SOURCES_PRESCORE_FREEZE_2026-10-23.md) · [完整科学报告](R251_SCIENTIFIC_REPORT_2026-10-23.md) · [原生Fraction形式多项式源码](r251_exact_lyapunov.py) · [全部405源CSV](R251_ALL_405_ORIGINAL_LYAPUNOV_SOURCE_ATOMS.csv) · [完整源结果JSON](R251_EXACT_RESULTS.json) · [SHA256机器收据](R251_FINAL_MACHINE_ACCEPTANCE.json) · [正式验收](R251_FINAL_ACCEPTANCE_STATUS.json)。

核心：V=x²严格单步下降的线性/三次局部系统可证明吸引，恒等与符号翻转V不变只稳定不渐近；中心化Logistic r3局部单步V在正侧反而增加，但第二次迭代严格内缩证明局部渐近吸引，因此单个候选充分条件失败≠系统不稳定。

[GitHub Actions run39894992871](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39894992871)三job成功，Python3.11和3.12各84真实测试共168通过，全部来源永久机器人归档[4fdebd05](https://github.com/edwardsage419/Psychohistory-Research/commit/4fdebd05aac54718b48a7b925f8993fd9647ddba)。新增真人E2/历史E3=0，R073/PESEN v0.1冻结。原目录下条11-012 Entropy and Information Theory（R252）。
