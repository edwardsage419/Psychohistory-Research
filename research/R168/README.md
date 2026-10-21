# R168 文化累积与棘轮效应：原始实验争论审计与64组精确有限模型

日期：2026年10月21日。原目录 **P1/07-010 Cumulative Cultural Evolution**。本阶段数学结果正式 **CLOSED_BOUNDED_E1**；Derex 2013 真人实验的原始数据关口为 **BLOCKED_SOURCE_ACCESS**，仍未通过真实人群独立预测验收。

## 一手实验与学术争议已系统核验

[Derex等2013年《Nature》原论文](https://doi.org/10.1038/nature12774)使用2、4、8、16人规模的双任务电脑实验研究箭头与渔网制造。出版方页面公开列出图1、图2、图3的XLS数据下载入口。[Andersson与Read2014年《Nature》质疑](https://doi.org/10.1038/nature13411)指出，大群体中「至少有人保留复杂技能」概率更高，可能只是独立抽样机会更多；[Derex等2014年回复](https://doi.org/10.1038/nature13412)维护群体知识保留、技能提高及多样性的结论，同时区分个体层与群体层估计。回复报道的单人复杂技能使用率与群体规模线性关系P=0.11、二次关系P=0.14，这两项具体统计在0.05标准下均未显著。

**真实数据访问：** [Nature原始图表读取审计run39538185600](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39538185600)证明当时服务器向自动检索返回3038字节验证页面，未取得任何一份XLS原始文件。另一项[Derex等2015年独立真人文化学习研究](https://doi.org/10.1098/rspb.2015.0719)及其[Dryad原数据](https://doi.org/10.5061/dryad.1425c)的CC0许可证、687002字节XLSX、MD5已从官方API核对，然而文件流403与官方下载API401，仍未取得原始字节。Social Sciences Replication Project关于Derex2013年的Ho与Wu文件经核实只有预先计划，结果章节仍为待补，不能视为正式复现成功。这些限制记录在[原始数据与2014争论审计](R168_EMPIRICAL_ACCESS_AND_2014_DISPUTE_AUDIT_2026-10-21.md)。

## 64组事前冻结的三层文化技能模型

本项目另构造完全人工的技能前沿水平0、1、2，人口N取2、4、8、16，个体复制成功率f取1/2与3/4，创新率u取0与1/8，观察渠道为全群体参与或单一有效渠道，初始技能水平0或2。全部 **4×2×2×2×2=64组**，每组保留五期完整三状态概率分布。人工前沿为多个技能尝试结果的最大值，**不能解释成每个人的平均技术能力或真实文化累积水平**。所有条件提前冻结于[计算前协议](../../protocols/R168_CUMULATIVE_CULTURE_64_THREE_LEVEL_SAMPLING_WORLDS_PRESCORE_FREEZE_2026-10-21.md)（提交b949ff7）。

两套独立数学实现：直接按最大值累积分布公式计算，另以逐次独立抽样的动态规划算法计算，均用Python Fraction。全部32套完整三状态随机转移矩阵以及64组×5时间点的概率向量严格一致，结果存放[107255字节的全部JSON](R168_EXACT_RESULTS.json)。

**冻结数学发现：**

1. 某个技能的个人复制成功率始终只有1/2，2人全面共享时至少有一人成功的概率为3/4；16人全面共享时为 **65535/65536≈99.9985%**。这是简单的抽样机会影响，即使个人能力一分未变，群体最高技能保留率仍可接近100%。
2. 2人群体充分共享且个人成功率1/2，与16人群体实际上只有一条学习渠道、个人成功率3/4，两者的群体保留率都为3/4。只观察一次群体是否掌握技能，无法单独识别每个人的复制准确率。
3. 当创新率为零时，技能0是吸收状态。人工技能2最终仍以概率1完全丧失，只是时间会随有效独立学习机会增加而大幅延长：个人成功率1/2、充分共享时，2人的预期完整丧失时间为**8代**，16人为**131072代**。短时间能保留复杂技能，不自动代表具有永久的棘轮机制。
4. 创新率为1/8时，初始技能0在第一期至多上升到1，两期后才有可能到达2；全部有创新组合的长期稳定分布亦由精确有理数方程验证。

上述都是项目自建模型推导。**没有重新拟合Derex实验、没有证明2013/2014争论中的哪一方最终正确，也没有对真实历史科技复杂度做预测**。

## GitHub计算核验及归档

[首次CI39539043139](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39539043139)成功；[SHA256固定与永久归档CI39539126007](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39539126007)成功。Python3.11和Python3.12两个环境各两次执行109个真实单测；独立归档任务另外重跑109项，总计 **545次测试执行，109种不同测试方法，0失败**。源码、全量JSON和测试ZIP由归档任务提交[1c4f1a7](https://github.com/edwardsage419/Psychohistory-Research/commit/1c4f1a777e79c9afc67c8750dd39295644a8e3a8)永久进入main。

研究文件：[英文科学报告](R168_SCIENTIFIC_REPORT_2026-10-21.md)｜[事前冻结协议](../../protocols/R168_CUMULATIVE_CULTURE_64_THREE_LEVEL_SAMPLING_WORLDS_PRESCORE_FREEZE_2026-10-21.md)｜[实证可得性审计](R168_EMPIRICAL_ACCESS_AND_2014_DISPUTE_AUDIT_2026-10-21.md)｜[原创程序](r168_cumulative_cultural_frontier_exact.py)｜[109项测试](test_r168_cumulative_cultural_frontier_exact.py)｜[完整JSON](R168_EXACT_RESULTS.json)｜[全程序与结果ZIP](R168_Cumulative_Culture_64_Worlds_109_Tests.zip)｜[正式机器验收](R168_FINAL_MACHINE_ACCEPTANCE.json)。

四项固定SHA256：
* 程序 `f203de0c441fc9d2111899ff8517170697dad3e940ba84b5b99f5a58705efe80`
* 测试 `8411ed9df0e0d8a5c6e9f5a70aa9dd352314129898c7fdaf5abac4cd0ee4c215`
* JSON `ce460cd0c591b399d86b61671548a75daf68b86b1827f0d8b3274cb376302019`
* ZIP `4da18ba2bd77320d3802a0eb2be38a414efdd3030f1459a375cd4fd0ed9cd7d6`

从 `research/R168` 运行 `python r168_cumulative_cultural_frontier_exact.py > R168_EXACT_RESULTS.json` 及 `python -m unittest -q test_r168_cumulative_cultural_frontier_exact.py` 即可复算，全部依赖Python标准库。

**科研证据：** R168数学E1完成；真人原数据E2关口因合法下载不可得而阻塞，新增E2=0、真实历史E3=0。R073/PESEN v0.1继续冻结。下一原目录 **R169 P2/07-011 Coevolving Networks（共演化网络）**。先完成既定全部R模型，最后再统一归纳分类与熔炼。
