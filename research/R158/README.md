# R158 冲突事件过程模型｜60组人工事件条件泊松序列与因果可识别性审计

2026-10-21。原目录 **P2/06-016 Conflict Event Process Models**。本研究正式 **CLOSED_BOUNDED_E1**，只涉及抽象八期事件计数和人为给定参数，未使用真实冲突、国家、死伤、组织或历史事件记录。

**原始文献核对：** [Hawkes (1971) *Biometrika* 原刊](https://doi.org/10.1093/biomet/58.1.83)发表时间、期刊、原摘要及初始页码核对；原摘要明确某些自激点过程与双随机过程存在相同二阶统计结构，**只凭事件聚集不能唯一认定因果自激机制**。[Ferland、Latour与Oraichi (2006)](https://doi.org/10.1111/j.1467-9892.2006.00496.x)原出版方摘要核对，作者提出整数值Poisson条件过程。本项目采用的\(\lambda_t=\mu+\alpha n_{t-1}\)是独立自建的一阶离散计数模型，**不是**Hawkes原文的连续时间模型，也没有完整重建2006年INGARCH机制。

**冻结试验：** 四条人造八期计数序列×三个基础事件率μ∈{1/2,1,2}×五个滞后响应α∈{0,1/4,1/2,3/4,1}，恰好60组完整计算。每期条件事件率严格保存为Fraction；两套独立对数似然实现（lgamma与真实整数阶乘）逐场景匹配到1e−12。额外计算15套独立条件过程期望值路径，12期内直接递推与有限等比级数严格分数相等。α=1时无稳定长期平均事件率，不能因为短期强度有限就推论过程平稳。

**竞争对照：** H1=(1,0,2,0,3,0,2,1)，基础率μ=1时α=1/2相对α=0总对数评分降低3.306852819440。H2=(0,1,3,2,0,1,4,0)，μ=1/2时α=1/2相对α=0总对数评分提高2.124618986159。全零事件序列在给定μ下对所有α具有完全相同的条件似然。**这是冻结人工数据与固定参数的数学演算；不构成现实冲突模型的优胜、行为传染因果论证或独立预测。**

**真实GitHub机器验证：** [初轮CI run39522593818](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39522593818)与[固定SHA256终轮CI run39522688331](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39522688331)均success。Python3.11/3.12每轮各87个真实单测，最终归档第三任务再执行87项并核验四项固定哈希，累计435次真实测试执行、87种不同测试方法、0失败。所有原始JSON和完整源码、测试ZIP已在[提交ff041f5](https://github.com/edwardsage419/Psychohistory-Research/commit/ff041f579861599433fede037a16962fc35938f0)永久写入main。

**完整材料：** [计算前冻结协议](../../protocols/R158_HAWKES1971_FERLAND2006_60_ARTIFICIAL_EVENT_HISTORY_PRESCORE_FREEZE_2026-10-21.md)（提交e03fd09）｜[完整学术报告](R158_SCIENTIFIC_REPORT_2026-10-21.md)｜[源程序](r158_poisson_count_process.py)｜[87项测试](test_r158_poisson_count_process.py)｜[44970字节全部结果JSON](R158_EXACT_RESULTS.json)｜[源程序测试与全结果ZIP](R158_Poisson_Event_60_Worlds_87_Tests.zip)｜[正式机器验收](R158_FINAL_MACHINE_ACCEPTANCE.json)。

SHA256：
* 原生程序 `43890ab779c71d134a713f47c71d40e740f4a224553d5bd6e5d7913d967a94e9`
* 87项测试 `0f7ddeaade1b842924c9ad4e3e4c30444be5f30a28bf2031954a4c0c9a555d82`
* 全量JSON `c3708c476d0d9b8344433b9008197b5622390d82ea52f11896d1cbc08f185635`
* 永久ZIP `34aaa668e4cde991a2bc806df48a476bef978b4c305fd247ca573f04966914e4`

独立复算：进入 `research/R158`，运行 `python r158_poisson_count_process.py > R158_EXACT_RESULTS.json` 与 `python -m unittest -q test_r158_poisson_count_process.py`。标准库，无第三方依赖。

本轮新增真人E2=0、真实外部历史事件预测E3=0。R073及PESEN v0.1保持冻结。下一原模型目录 **R159 P1/07-001 Dual Inheritance Theory（双重继承理论）**。继续遵守先完成全部既定R系列，再归纳分类，最后模型熔炼的顺序。
