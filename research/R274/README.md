# R274 跨时期留出（12-004，P0）

科研状态：**CLOSED_BOUNDED_E1_FINITE_ARTIFICIAL_TEMPORAL_HOLDOUT**。冻结三个人工时间机制×三种固定预测政策，九world各有完整64个有序人工源，合计576条模型标识来源。先训练t1到t4，未来t5/t6作测试。合法Laplace q=(K+1)/6，固定半概率q=1/2；另保留**非法未来标签回填**q=(K+J+1)/8作信息泄漏反例，其测试分数不得当成可部署预测性能。

[事前冻结](../../protocols/R274_TEMPORAL_HOLDOUT_9_SIXBIT_WORLDS_576_ORIGINAL_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [原生代码](r274_exact_temporal_holdout.py) · [全部576有序来源CSV](R274_ALL_576_ORIGINAL_FORWARD_HOLDOUT_SOURCES.csv) · [完整9世界未来Brier结果JSON](R274_EXACT_RESULTS.json) · [机器SHA256凭证](R274_MACHINE_RECEIPT.json) · [科学报告](R274_SCIENTIFIC_REPORT_2026-10-23.md) · [正式机器验收](R274_FINAL_ACCEPTANCE_STATUS.json)。

STABLE_HALF 下合法历史Laplace Brier 5/18、非法未来泄漏成绩27/128、事前半概率基线1/4；上升及下降概率时合法历史Laplace 55/144、非法事后分数131/512、合法半概率1/4。完整原source和独立Binomial(4,a)×Binomial(2,b)解析过程九world严格Fraction一致。

[GitHub Actions run39903501667](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39903501667)，Python3.11和3.12各82项真单测共164全部通过，第三来源审计和机器人原数据永久归档全部success。[全部原来源提交df5ad9d9](https://github.com/edwardsage419/Psychohistory-Research/commit/df5ad9d907fed3fe1c2c17d8d12eb10ad25c081b)。

新增真实E2/E3=0，R073/PESEN v0.1仍冻结。原目录下一项12-005 Equifinality Analysis（拟R275）。原R全部学习完成后再统一归纳分类与熔炼。
