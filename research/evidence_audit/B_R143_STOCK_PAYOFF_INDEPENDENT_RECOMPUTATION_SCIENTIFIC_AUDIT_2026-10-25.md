# B 独立科学验证：R143 完整存量与原始收益的双路径复算

日期：2026-10-25。B 独立协议先冻结于 commit `b21936d7746311860fa208a0a922f62b96de2ba6`，后提交本轮计算源码。研究对象是 R143 1989 Arthur Table1 人工技术采用过程的九个固定参数世界，证据等级 E1。

## 方法独立性与具体执行

R 主线使用 d=nA−nB 的五状态转移、Cramer 行列式与未合并的行动树。B 脚本完全从原始收益 `R:(2+nA,nB)`、`S:(nA,2+nB)` 开始，以独立完整存量 `(nA,nB,lock)` 的 Python Fraction 概率递推计算12轮。脚本没有导入主流程模块，也没有调用其 `q_a`、矩阵或 Cramer 求解器。仅在执行结束后读取 R 主线完整 JSON 作逐项比较。

九组世界各有12轮，**108项概率质量守恒**全部精确为1；每组12轮结束有13种存量状态。九组 A锁、B锁、未锁三类概率合计**27项与主流程逐分数完全一致**。基线独立得到 `A=B=29643/65536`、`none=3125/32768`。独立二轮反例得到 `A=B=0`、`none=1`，拒绝把 d=±2 误当永久锁定。所有结果来自实际运行本地 Python 3.13。

## 原始可复算材料

* 独立执行脚本：`research/evidence_audit/r143_b_stock_payoff_independent.py`，Git blob `395157379d4cce003a8029d87563fcdaccb77982`，本地执行源 Git blob 完全相同，SHA256 `150a06853f65b68a6b3814d9e3a8fd962e3943debf1ea5c3d932b76e22580821`。
* 完整9世界×12轮守恒及27项最终比较机器收据：`research/evidence_audit/B_R143_STOCK_PAYOFF_9_WORLD_INDEPENDENT_RESULTS_2026-10-25.json`，Git blob `c83fcfef8e82ae2c575a82d6458120d7993839df`，本地 SHA256 `98c1307d44eeb61fe1fbb0f55ca35f3db49d5b6c521da6321f8d2b1dad92beb1`。
* 复算命令：`python research/validation/r143_arrival_tie_bias_cramer_path_enum.py --output results.json`，随后 `python research/evidence_audit/r143_b_stock_payoff_independent.py --reference results.json --output audit.json`。输出 `PASS B R143 direct stock payoff 9 worlds; 27 independent exact comparisons`。
* R 主线九组原始有理数 CSV：`research/validation/R143_ARRIVAL_TIE_BIAS_9_WORLD_EXACT_ROWS_2026-10-25.csv`。

## 科学证据范围与验收缺口

本次独立性是同一项目内部不同算法和不同状态表述的程序性复核。**没有其他研究者在独立数据与独立环境下复现**。参数 p、a 均人为指定，没有从历史制度数据估计。没有样本外预测、数据泄漏型训练集、概率校准、独立真实样本、bootstrap 置信区间或真实历史因果识别，因此这些实证验收项标记 `NOT_APPLICABLE_E1_ONLY`，不能记为 PASS。负对照仅检验有限数学实现中的错误锁定解释，不能替代真实负对照实验。

科学状态 `PASS_BOUNDED_LOCAL_INTERNAL_METHOD_INDEPENDENT_E1`；远端 GitHub Actions 本轮新程序 `NOT_RUN`。R143 原有 2026-10-20 历史 CI 仍属于旧源码的独立验收记录。新增 E2=0、E3=0、外部团队独立复现=0。R073 与 PESEN v0.1 保持冻结。R127 历史协议差异及 R136 原负对照缺陷继续列为未解决。
