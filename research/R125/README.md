# R125：Erdős–Rényi 与 Gilbert 两种随机图——一手定义、有限精确概率及连通性

日期：2026-10-20（Asia/Taipei），原候选目录 **P0 04-018 Erdős Rényi Random Graph**。

**正式科研状态**：CLOSED_BOUNDED_ORIGINAL_ERDOS_RENYI_1959_GNM_AND_GILBERT_1959_GNP_FINITE_EXACT。
**限定学习状态**：LEARNING_COMPLETE_BOUNDED_ERDOS_RENYI_1959_GNM_GILBERT_1959_GNP_EXACT_SMALL_GRAPH_MODELS。
**E2真人原始行为预测0条**；R073与PESEN v0.1继续冻结，先完成原R系列全部学习，之后统一归纳、分类，最后熔炼。

## 真正核阅的原创学术论文

1. [Erdős & Rényi (1959), *On Random Graphs I*, Publ. Math. Debrecen 6:290–297](https://www.cse.cuhk.edu.hk/~cslui/CMSC5734/erdos-1959-11.pdf)：实读及截图核对原刊290–291页，开篇明定**固定恰m条边、全部满足条件的有标签无向图等概率**的G(n,m)模型。原刊291页Theorem1讨论m≈n ln n / 2时n→∞全图连通概率的数学极限；不能误称此为四节点有限图精确答案。
2. [E. N. Gilbert (1959), *Random Graphs*, Ann. Math. Stat. 30(4):1141–1144](https://doi.org/10.1214/aoms/1177706098)，[CMU保存原刊PDF](https://www.stat.cmu.edu/~brian/780/bibliography/09%20Other%20Models/Gilbert%20-%201959%20-%20Random%20graphs.pdf)：实读及截图核对原刊1141–1142页；所有潜在边**彼此独立以p出现**的G(n,p)模型及1142页Eq4的P(全连通)递推。
3. [Erdős & Rényi (1960), *On the Evolution of Random Graphs*, 卷5:17–61](https://real.mtak.hu/200959/)及[Rényi研究院原作者论文](https://users.renyi.hu/~p_erdos/1960-10.pdf)：核对原官方书目及公开片段的“巨型连通分量”渐近背景，**没有**宣称完整逐页核验1960全篇证明或复现其大样本随机图相图。

**三个边界不能混**：G(n,m)固定m、G(n,p)独立p；两者在后者条件化到恰m条边且该事件有正概率时才具有相同分布；“巨型连通分量”出现的渐近门槛（平均度约1）不等于**全体节点完全连通**的更高门槛（量级ln n）。这两种极限事件都不是n≤5小图的真实社会预测。

## 独立精确代码实际验收

两套各自独立的连通性计算：
- **全图枚举**：遍历n=1..5全部无向简单有标签图，含孤立点，DFS得到真实连通分量、最大分量、孤立点数和顶点0的度；对每一固定m以1/C(K,m)加权，对每个p以p^m(1−p)^{K−m}加权。
- **Gilbert1959来源原式**：完全不调用图枚举，直接按论文印刷1142页的连通递推Eq.(4)求P_n(p)，与上法严格Fraction一致。另以Binomial边数/度数、Gnm Hypergeometric度数与n(1−p)^{n−1}孤立数期望独立公式校验。
- **有限覆盖**：n=1..5共有1+2+8+64+1024=**1,099张纯数学图**；在p=0、1/3、1/2、1计算**4,396个图×参数权重**；各(n,m)共有**25个固定边数完整分布桶**。针对所有合法条件事件，逐图证明G(n,p)在给定边数m后的概率等于G(n,m)条件概率，零概率事件严格fail-closed。
- **没有输入任何真实社交图**，所有图是独立数学枚举，不是1,099场真实社会实验。

冻结的n4构造（本项目算例而非原作者真人数据）：

| 指标 | ER G(n=4,m=3) | Gilbert G(n=4,p=1/2) |
|---|---:|---:|
| 边数期望 | 3 | 3 |
| 边数方差 | 0 | 3/2 |
| 全图连通概率 | **16/20=4/5** | **38/64=19/32** |
| 孤点人数期望 | **1/5** | **1/2** |

独立p模型中恰好3条边的概率为5/16，附加这一条件后每个具体三边图概率1/20，恰等于固定m模型。因而**同平均度不等于同连通概率**，同时两模型有明确可证明的条件分布关系。

## GitHub真实CI，含完整失败修复轨迹

前期发生三次真实失败，已在[预冻结协议R125-CORR-001/002](../../protocols/R125_ERDOS_RENYI_1959_GNM_GILBERT_1959_GNP_FINITE_EXACT_FREEZE_2026-10-20.md)和[科学报告](R125_ERDOS_RENYI_GNM_GILBERT_GNP_FIRSTPARTY_FINITE_EXACT_SCIENTIFIC_REPORT_2026-10-20.md)逐项保留：
- [首次失败39344720876](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39344720876)：54项中两项失败，原因是Gnp端点p=0或1仍将概率0的**不可能状态**存入分布dict；修正后只保留正概率支持集，但仍计入所有理论上可枚举图。
- [序列化失败39344789785](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39344789785)及[39344898582](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39344898582)：54项数学校验实际通过，但后续将Fraction表示的连通图数量写进JSON机器验收时抛类型错误，**整体CI仍是failure**；将严格整数的图数16、38转换为JSON原生整数，保留有理数概率不变。
- **最终**[GitHub Actions 39345096433](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39345096433) **completed success，54项单元测试全部通过，0项失败**，并独立重放1099图、4396加权、25分布桶，GitHub机器人提交程序、测试、科研报告三个文件SHA256及完整收据，[已回读的机器验收](R125_PHASE_A_GNM_GNP_54_TEST_1099_GRAPH_25_BUCKET_CI_ACCEPTANCE.json)。

## 正式材料

- [计算前冻结合同及CORR-001/002](../../protocols/R125_ERDOS_RENYI_1959_GNM_GILBERT_1959_GNP_FINITE_EXACT_FREEZE_2026-10-20.md)
- [第一手Gilbert与ER原文和完整数学解释报告](R125_ERDOS_RENYI_GNM_GILBERT_GNP_FIRSTPARTY_FINITE_EXACT_SCIENTIFIC_REPORT_2026-10-20.md)
- [可运行原生Python数学程序](r125_erdos_renyi_gnm_gilbert_gnp_exact.py)
- [54项单元测试](test_r125_erdos_renyi_gnm_gilbert_gnp_exact.py)
- [真实CI及文件SHA256收据](R125_PHASE_A_GNM_GNP_54_TEST_1099_GRAPH_25_BUCKET_CI_ACCEPTANCE.json)
- [正式科研验收、原失败与成功边界](R125_FINAL_ACCEPTANCE_STATUS.json)

本地复算（Python 3.11标准库）：PYTHONPATH=research/R125 python -m unittest -v research/R125/test_r125_erdos_renyi_gnm_gilbert_gnp_exact.py 。

**科研限制**：这是一手随机图数学复核，不等于任何真实社会网络的连边同概率/独立假设得到支持，也不是巨型分量的完整渐近算法模拟、真实人类行为E2或历史事件外部前瞻E3。保持先R系列学习后分类后熔炼，R073与PESEN v0.1均冻结。
