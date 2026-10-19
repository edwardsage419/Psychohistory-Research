# R121：独立级联模型的单次传播、独立随机活边与期望次模性

研究日期：2026-10-19（Asia/Taipei）。
原239候选目录：P0 / 04-004 Independent Cascade Model。
**正式科研状态**：CLOSED_BOUNDED_KKT_2003_ORIGINAL_ONE_CHANCE_INDEPENDENT_CASCADE_AND_LIVE_EDGES。
**限定模型学习验收**：LEARNING_COMPLETE_BOUNDED_KKT_2003_IC_ONE_CHANCE_INDEPENDENT_LIVE_EDGES。
真正独立人类行为预测E2评分=0；不改R073和PESEN v0.1的冻结内容。保留“先全部R学习，后统一归类，最后熔炼”研究顺序。

## 一手原学术来源

[Kempe、Kleinberg、Tardos (2003), *Maximizing the Spread of Influence through a Social Network*](https://doi.org/10.1145/956750.956769)，[原作者Cornell发布的10页SIGKDD PDF](https://www.cs.cornell.edu/home/kleinber/kdd03-inf.pdf)，真实核阅PDF第2页的Two Basic Diffusion Models与第4页的Independent Cascade/Theorem 2.2/Claim 2.3。原文规定一名节点第一次被激活时才能分别向尚未激活邻居做一次独立概率尝试，无论成功失败不得对同一目标重复尝试；成功目标下一轮成为传播源；无撤回。原作者Claim 2.3说明每条有向边**事前相互独立**掷成功/失败硬币，最终从种子沿成功边可达的节点集合与动态逐轮过程最终激活集合的概率分布完全相同。Theorem 2.2是在该原模型下种子集合对**期望**人数的次模性，而不是“每名真人一定遵从”的保证。

[Goldenberg、Libai、Muller (2001), *Talk of the Network*](https://doi.org/10.1023/A:1011122126881)，[Tel Aviv University原作者学院公开摘要](https://cris.tau.ac.il/en/publications/talk-of-the-network-a-complex-systems-look-at-the-underlying-proc/)为早期营销传播模型文献背景；本期只核实正式书目与摘要，未宣称取得其全文随机元胞自动机模拟源码或真实用户逐人购买数据。

## 机制与验证

源码使用Python标准库Fraction，提供两套独立运算：
1. **动态单次尝试事件树**：从当期首次激活frontier出发，对每条指向未激活目标的出边仅抽一次独立硬币，若成功目标于下一轮加入；从所有路径累积最终frozenset节点集合概率。
2. **每条有向边提前独立决定live/blocked**：独立枚举全边随机硬币，计算在live图上从种子可达的集合概率；不调用第一套动态运算。

两套方法各自概率总和严格为1，并在每一个可能的最终激活节点集合上给出完全相同的Fraction概率。全枚举 n=1、2、3 节点全部有向简单图（1、4、64种），边概率方案一统一1/2，方案二根据两节点编号奇偶取1/4或3/4，各图所有初始种子子集，合计**1,060组纯数学比较案例**。所有模型实例的**期望**影响函数另外经过单调/次模检查。1,060不是1,060个真实人类网络或外部实验。

**与R120线性阈值（LT）的可核数字区别**：两源各有一条边到同目标，参数1/2、1/4。IC两条边独立成功，使目标被至少一条边激活概率**5/8**，两源种子后的期望总激活人数**21/8**；LT把这些数当目标入边权重时，目标随机阈值≤3/4激活，期望人数**11/4**。IC两条入边同时live的概率1/8，R120 LT则每个目标最多挑选一条live入边，不能同时存在；因此两个模型不能因某些单源结果一样而被擅自融合/等价化。

四节点链0→1(1/2)、1→2(2/3)、2→3(3/4)的期望总激活人数25/12，最后节点激活概率1/4；三节点定向环各边1/2、种子0的期望人数7/4。另p=0、p=1、两个传播源在同一轮同时成功、空种子、无重复尝试、无自发激活、边和节点非法输入都通过独立测试。

**真正GitHub Actions [39256571643](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39256571643) success：48项单元测试全部通过，0项失败；1,060组数学网络×种子×边概率的完整终态分布均一致。** 原源码、测试、科研报告的SHA256与成功机器收据已由CI自动提交，并由GitHub读取验证。

## 验收归档文件

- [计算前冻结规范](../../protocols/R121_KKT_2003_INDEPENDENT_CASCADE_ONE_SHOT_LIVE_EDGE_DISTRIBUTIONS_FREEZE_2026-10-19.md)
- [第一手论文、单次传播、独立活边及次模边界科学报告](R121_KKT_2003_INDEPENDENT_CASCADE_LIVE_EDGE_ONE_CHANCE_FIRSTPARTY_SCIENTIFIC_REPORT_2026-10-19.md)
- [两套独立精确概率计算程序](r121_kkt_2003_independent_cascade_exact.py)
- [48项真实数学单元测试](test_r121_kkt_2003_independent_cascade_exact.py)
- [真实机器测试计数及文件SHA256收据](R121_PHASE_A_IC_48_TEST_1060_FULL_DISTRIBUTION_GITHUB_CI_ACCEPTANCE.json)
- [正式阶段科研验收范围](R121_FINAL_ACCEPTANCE_STATUS.json)

复算：`PYTHONPATH=research/R121 python -m unittest -v research/R121/test_r121_kkt_2003_independent_cascade_exact.py`，Python3.11原生标准库。不含真实个人行为数据。

研究尚未复跑KKT原2003大型合作网络/贪心优化性能、Goldenberg2001营销网络原个体资料、跨实验E2真实预测或长期历史事件前瞻估计；数学正确性不意味着边概率在现实中可独立识别或各种社会影响都是独立传播。继续按照既定R研究目录推进，整体归类与模型熔炼最后进行。
