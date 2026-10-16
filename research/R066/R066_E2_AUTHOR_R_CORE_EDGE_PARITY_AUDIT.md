# R066：原作者 R 家庭网络边与 Python 边的全体逐边核验

日期 2026-10-16。结果 **AUTHOR_R_CORE_EDGE_PARITY_PASS**。

原始数据：Harvard Dataverse `doi:10.7910/DVN/RAHSVM` V1.0，16 村庄、2125 行；数据、作者 R 源码与代码本均经精确 SHA256 校验。事先提交 [完整逐边协议](../../protocols/R066_E2_AUTHOR_R_EDGE_PARITY_2026-10-16.md)，commit `b6f82e636bf13a71c6f510a4cbf13166306d30b4`。

[GitHub Actions run 38865507356](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38865507356)：两个作业 `completed/success`，11 项合成测试通过，且在真实 runner 内使用 `r-lib/actions/setup-r@v2` 安装 R。R 从原作者经 SHA256 核验的 `LL_SpecialIssue_Replication.R` **直接提取并执行**完整的 `make_el` 和 `convert_to_hh` 函数，16 村庄按 `hhnum` 排序、四类各 5 槽关系提名、`ego/hhh/hh1..hh11` 家庭成员多对多匹配，构建每村无向去重去自环家庭网络。另一侧独立 Python 重建。两个进程生成的临时边全集以 `(village,category,min_household_position,max_household_position)` 逐条求集合差。

| 网络 | 原生 R 来源派生无向边 | Python 无向边 | 逐边集合差 |
|---|---:|---:|---:|
| 走访 visit | 4845 | 4845 | 0 |
| 用餐 meal | 4110 | 4110 | 0 |
| 借用 borrow | 2785 | 2785 | 0 |
| 传闻 rumor | 3027 | 3027 | 0 |
| **总计（分类后）** | **14767** | **14767** | **0** |

跨类别合并的唯一无向边数 **8659**；分类总边数 `14767` 包含同一家庭边可能在多种关系中出现，不可混同独立家庭联系数。

由于模型曾因直接 `(village_number,ego)` 键出现重复与提名不匹配而 `JOIN_CANDIDATE_BLOCKED`，此次结果严格属于**作者家庭网络层**的另外一套方法，并未回溯取消旧判定。

**关键边界：** 本次验证原作者两个 R 核心函数的真实执行与 Python 源码等价输出，不是作者论文全部 R/igraph 回归图表以及因果分析的逐数复现。尚未开展任何 DeGroot、Friedkin–Johnsen 或 Hegselmann–Krause 真人数据模型拟合；没有 E3 新队列验证。用户级原始行、家庭别名和临时逐边集合没有上传到 GitHub。仅存 [匿名对照 JSON](R066_E2_AUTHOR_R_CORE_EDGE_PARITY_RESULTS.json) 和代码/CI。

`R066_AUTHOR_R_CORE_EDGE_PARITY=PASS`；`R066_FULL_AUTHOR_IGRAPH_ANALYSIS_PARITY=OPEN`；`R066_REAL_THREE_MODEL_PREDICTION=OPEN`；`PESEN_v0.1=FROZEN`。
