# R289 科学报告：原239目录01-004 有限理性满意化与四报价顺序搜索

日期2026-10-23 Asia/Taipei。由用户所定研究顺序推动：原239项全部学习→统一归纳分类→最后原创模型熔炼。**本项是原目录P1补缺，而不是新增第240/241/242项原候选**。始终区分外部文献理论线索、人工模型数学与真实人类样本的实证验证。

[先行事前冻结](../../protocols/R289_SIMON_SATISFICING_3_DGPS_2_THRESHOLDS_486_FULL_SOURCES_PRESCORE_FREEZE_2026-10-23.md) GitHub提交[27fa695d](https://github.com/edwardsage419/Psychohistory-Research/commit/27fa695d5e0c612fd77fb3a3fc5af26a543c0a27)，先于完整结果生成。

## 机制、独立计算与边界

原始理论文献Simon (1955), *A Behavioral Model of Rational Choice*, QJE 69(1):99–118，DOI https://doi.org/10.2307/1884852。原始研究探讨有限资源的决策简化；本项目选取**四次报价流、有限检查成本、事前愿望阈值的自建教学性情境**，没有从1955文章复算真实行为数据。

有四个按序出现的随机报价，每个取值1、3、5，三人造分布UNIFORM=(1/3,1/3,1/3)、LOW_HEAVY=(1/2,1/4,1/4)、HIGH_HEAVY=(1/4,1/4,1/2)；两种冻结阈值H=3或5。首次看见收益≥H即接受并停止，否则强制观察第四个即选最后结果。每多看一个报价付出1/2成本。每人工情境完全穷举3^4=81个有序原四报价，3×2共486全正source。保存每次原source概率、实际观察次数、是否达阈值、最终收益、净收益，以及两个明确不同的基准：真实可实施的第一项立即拿取、**不可实施的知道四报价未来的全知最高值**。

路线A全部原来源直接执行在线阈值停止，按质量积分净收益、期望观察次数、永未达标概率和比较基准。路线B不使用全source枚举，从单次报价概率q=P[x<H]，m_hit=Σ_{x≥H}p_xx及μ=Σp_xx闭式推导：
E[观察数]=1+q+q²+q³；
E[最终收益]=m_hit(1+q+q²)+q³μ；
E[净收益]=E[最终收益]−(E[观察数]−1)/2；
P[四项都不达标]=q^4；
E[全知最高值]=1+2(1−p1^4)+2(1−(p1+p3)^4)。
全部六世界在分数域完全一致，第三独立程序从CSV逐四报价重算，连最后被迫停止未达标情况也保留。

|真报价机制|阈值3：净收益期望|阈值5：净收益期望|
|---|---:|---:|
|UNIFORM|67/18≈3.7222|100/27≈3.7037|
|LOW_HEAVY|27/8=3.375|197/64≈3.0781|
|HIGH_HEAVY|133/32≈4.1563|35/8=4.375|

因此在当前固定成本和分布下，较高愿望阈值**不是**普遍优选。这个数学分布差异不等同真实人对搜索策略的偏好、心理资源测量或因果效果，也不能与知道所有未来报价的oracle直接公平评比。只有E1有限人工数学，不获得真人E2、历史E3。

## 验收记录及源保全

全部来源：[R289_ALL_486_ORIGINAL_SEQUENTIAL_OFFER_SOURCES.csv](R289_ALL_486_ORIGINAL_SEQUENTIAL_OFFER_SOURCES.csv)，共486个带机制标签原始数学配置，6个人工世界；[解析和枚举结果JSON](R289_EXACT_SATISFICING_RESULTS.json) · [SHA256机器凭证](R289_MACHINE_RECEIPT.json) · [运行源码](r289_exact_satisficing.py)。原CSV SHA256 `df97e2f058f5c79d70b6d2edecad6a8d75dc227f659a69b19dca3bf73cef285a`，结果JSON SHA256 `519f77466a6013d6eda99c11fc5266ca70cf426f5f18250f68012d3407aeae3b`。

[GitHub Actions run39910079877](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39910079877)三个作业全部completed/success，Python3.11与3.12各70个**真实运行**的unit test，共140通过；第三独立审计执行[不导入原模型的审核代码](../catalogue_audit/independent_r287_r289_source_audit.py)，直接逐CSV重建所有原来源、精确质量、实际结果、独立数学解析和SHA。所有原CSV/结果JSON/摘要经机器人永久main归档[提交cbfbbdca](https://github.com/edwardsage419/Psychohistory-Research/commit/cbfbbdcaf54a45faea84bc0a00f20b396f31cd41)。

正式研究决定：**CLOSED_BOUNDED_E1_ARTIFICIAL_R289_MODEL_MECHANICS**，原01-004获得一个独立、可复现、仅人工数学范围的主R。未读取真实个体被试的trial-level资料，未实现完整原作者具体实验复现，新增真人E2=0、真实历史E3=0，R073及PESEN v0.1维持冻结。其它早期研究包可能已包含文献介绍，后续避免重复计为独立实验。下一项按照原目录剩余待核队列推进。
