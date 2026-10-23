# R290 科学报告：01-011 信号检测理论的有限离散似然决策

日期：2026-10-23 Asia/Taipei。沿原始239模型目录的P1缺口新增独立主研究R290；原目录239项不变。研究性质为有限人工数学E1，真人E2=0，历史E3=0。

## 文献与事前冻结

Tanner, W. P., Jr. & Swets, J. A. (1954), A decision-making theory of visual detection, Psychological Review 61(6):401–409. DOI https://doi.org/10.1037/h0058700；PubMed https://pubmed.ncbi.nlm.nih.gov/13215690/ 。本文只根据公开一手文献书目信息和似然决策机制建立新的有限离散人工实验。**未复算原文真人实验、未拟合高斯SDT的d'、未开展真实外部预测。**

[预评分数学协议](../../protocols/R290_SIGNAL_DETECTION_3_DGPS_2_PRIORS_2_COSTS_120_CELL_PRESCORE_FREEZE_2026-10-23.md)先于分析结果独立冻结，GitHub提交 [696e86b0](https://github.com/edwardsage419/Psychohistory-Research/commit/696e86b029581d2b00dc79bdd2219c59427a7980)。

## 模型与独立审计

信号与噪声标签y=1/0，证据x取0、1、2、3、4。三个冻结条件分布MONOTONE、CENTERED和IDENTICAL；信号先验1/2或3/4；误报和漏报损失依次为(1,1)或(1,3)。这构成12个人工世界，每世界10个按标签区分的联合来源单元，共120个完整source cells。所有运算使用Fraction精确有理数。

逐证据点贝叶斯决策：当 pi*C_FN*P(x|signal) > (1-pi)*C_FP*P(x|noise)，才判信号，精确平局判噪声。六种单一证据阈值策略为x>=t，t从0到5，并列最优取最小t；另保留固定t=3。风险R=(1-pi)*C_FP*FAR+pi*C_FN*(1-HR)，FAR与HR分别是条件误报率与条件命中率。

主程序从全部120联合概率源独立求和，另有解析下界逐证据点累加两类成本权重的最小值。第三方审计程序**完全不导入主模型**，独立重算CSV中所有120条来源、每世界32个任意决策集合共384项、72个阈值ROC点，并核对源级损失与CSV/JSON SHA256。两种数学路线对12世界的最优值逐分数相等。

## 12个人工世界精确结果

| 条件 | signal prior | FP:FN | 完整最优风险 | 最佳单阈值风险 | t |
|---|---|---|---:|---:|---:|
| MONOTONE | 1/2 | 1:1 | 5/21 | 5/21 | 2 |
| MONOTONE | 1/2 | 1:3 | 8/21 | 8/21 | 1 |
| MONOTONE | 3/4 | 1:1 | 4/21 | 4/21 | 1 |
| MONOTONE | 3/4 | 1:3 | 1/4 | 1/4 | 0 |
| CENTERED | 1/2 | 1:1 | **1/6** | **1/3** | 1 |
| CENTERED | 1/2 | 1:3 | 11/42 | 8/21 | 1 |
| CENTERED | 3/4 | 1:1 | 11/84 | 4/21 | 1 |
| CENTERED | 3/4 | 1:3 | 1/4 | 1/4 | 0 |
| IDENTICAL | 1/2 | 1:1 | 1/2 | 1/2 | 0 |
| IDENTICAL | 1/2 | 1:3 | 1/2 | 1/2 | 0 |
| IDENTICAL | 3/4 | 1:1 | 1/4 | 1/4 | 0 |
| IDENTICAL | 3/4 | 1:3 | 1/4 | 1/4 | 0 |

主要机制反例：CENTERED信号证据最优选择集合{1,2,3}，不能由任一单一x>=t生成；先验相等和误判损失相等时，完整贝叶斯风险为1/6，最佳单阈值风险1/3，固定情境下后者是前者的两倍。该数字仅适用于冻结人工分布。

负控制：IDENTICAL条件信号与噪声的证据分布完全相同，任何规则的条件命中率与误报率都相等；先验、误判成本可以改变最优常量动作和风险，但不增加信号本身可区分信息。固定分布下提高漏报成本或提高信号先验，也不会缩减贝叶斯判信号证据集合（等号平局规则按冻结约定）。

## 复现、限制与归档

[执行程序与117项真测试](r290_exact_signal_detection.py)；
[120条全来源数据](R290_ALL_120_ORIGINAL_LABELED_SIGNAL_SOURCE_CELLS.csv)；
[12世界精确结果和72ROC点](R290_EXACT_SIGNAL_DETECTION_RESULTS.json)；
[SHA256机读凭证](R290_MACHINE_RECEIPT.json)；
[独立来源审计及三个逆向测试](../catalogue_audit/independent_r290_source_audit.py)。

[GitHub自动归档工作流39911658107](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39911658107)于2026-10-23 completed/success，并将程序、全来源、结果、审计程序与哈希永久提交main。后续双Python持续集成验收结论需独立读取其成功运行记录后更新，不预先宣称。

科研范围：CLOSED_BOUNDED_E1_ARTIFICIAL_R290_MODEL_MECHANICS；没有原作者真人实证重现、跨实验预测或历史泛化。原R073及PESEN v0.1继续冻结；下一个P1原目录候选是01-013 Theory of Reasoned Action。原239项全面科学结题仍未建立，研究完毕之后才能进行统一分类与熔炼。
