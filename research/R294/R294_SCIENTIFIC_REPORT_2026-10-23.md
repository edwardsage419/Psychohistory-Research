# R294 科学报告：01-018双曲折扣、指数折扣、准双曲折扣与时间一致性的精确人工对照

日期2026-10-23 Asia/Taipei。本研究按原239候选目录01-018 Hyperbolic Discounting（P1）新增独立R294。正式科学范围仅为有限人工参数选择E1；**没有真人E2、历史E3或原作者实际消费储蓄回归复现**。

## 理论来源和预先冻结

Strotz (1955), *Myopia and Inconsistency in Dynamic Utility Maximization*, *Review of Economic Studies* 23(3):165–180, DOI https://doi.org/10.2307/2295722；David Laibson (1997), *Golden Eggs and Hyperbolic Discounting*, *Quarterly Journal of Economics* 112(2), DOI https://doi.org/10.1162/003355397555253，[作者本人公开书目](https://laibson.scholars.harvard.edu/publications/golden-eggs-and-hyperbolic-discounting)。文献涉及动态不一致偏好与承诺等机制。本轮的奖励组合、参数、两期比较及全部数学结果都是项目自行设定的教学性人工机制，对原作者的实际数据和福利模型不作复算声称。

[结果之前的R294冻结协议](../../protocols/R294_HYPERBOLIC_EXPONENTIAL_QUASI_72_WORLDS_144_DECISIONS_PRESCORE_FREEZE_2026-10-23.md)，冻结提交[9c78d082](https://github.com/edwardsage419/Psychohistory-Research/commit/9c78d082902cedffb8ad64159915d8d6f5e12299)。

## 完整人工世界与评分协议

两选项：较早A在t=1得到a，较晚B在t=2得到b。a∈{2,3,4}，b∈{5,7}构成6种正奖励配置，每种在t=0和t=1分别重新计算两选项当前价值，精确平局选A。三类折扣模型：

* HYPERBOLIC：D_k(d)=1/(1+kd)，k∈{0,1/2,1,2,3}，**30世界×2=60条source**；
* EXPONENTIAL：D_δ(d)=δ^d，δ∈{1/2,3/5,4/5}，**18世界×2=36条source**；
* QUASI_HYPERBOLIC_BETA_DELTA：D(0)=1，D(d>0)=βδ^d，β∈{1/2,1}，δ∈{3/5,4/5}，**24世界×2=48条source**。

因此72个人工世界与144条双时点决策原source（不是72个真人受试者或随机样本）。所有收益折现和选择使用Python Fraction精确有理数，双时点都具唯一来源行；保存配置、当前时点、折扣后的A/B价值、精确平局标志、选择及同世界偏好反转，禁止事后调参。

## 精确反转条件与负对照

指数折扣下从t=0到t=1共同前进一期，两选项价值比都为 bδ/a。因此在本合同里**任意δ都不会因单纯时点平移产生偏好反转**。

双曲折扣下，t0偏好B且t1偏好A当且仅当

`b/a > (1+2k)/(1+k)` 且 `b/a <= 1+k`。

以a=3、b=5、k=1为例，t0两选项价值分别为A=3/2、B=5/3，故选B；t1分别为A=3、B=5/2，故选A。双曲函数的参数固定，选择依当期与奖励时间的相对距离改变，显示单个自主决策者计划与执行可能不一致的代数例子。

准双曲折扣在t0两选项皆被β缩减，偏好B当且仅当bδ>a；t1即时A无β折扣，选A当且仅当a>=bβδ。所以反转条件是`bδ>a`和`bβδ<=a`。a=3、b=5、δ=4/5、β=1/2满足反转；β=1恢复普通指数折扣，因此未发生反转。

第三独立源码逐世界核查全部72个反转布尔值及144条原收益，**没有把未来选择隐含写入当前效用**，也未把参数格点反转频率当成人类行为基准发生率。

## 人工参数网格结果与适用边界

| 模型家族 | 人工配置 | B→A反转 |
|---|---:|---:|
| 双曲 | 30 | 8 |
| 指数 | 18 | 0 |
| 准双曲βδ | 24 | 7 |
| 合计 | **72** | **15** |

这15个只是预先指定参数网格中的模型反转世界数，参数配置不带真实人口抽样权重。真实人能否被这些函数识别、未来自己是否真的改变选择、能否承诺执行、长期消费与储蓄的外推效果，**均未得到任何实证证据**。

## 独立审计与正式归档

[完整主模型源码与583项数学单元测试](r294_exact_discounting_time_inconsistency.py)；
[144个逐时点原source](R294_ALL_144_EXACT_INTERTEMPORAL_DECISION_SOURCES.csv)；
[72个人工世界结果](R294_EXACT_DISCOUNT_REVERSALS.json)；
[源CSV/结果JSON的SHA256凭证](R294_MACHINE_RECEIPT.json)；
[独立不导入主程序的12项逆向核验代码](../catalogue_audit/independent_r294_source_audit.py)。

[GitHub Actions run39919476504](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39919476504)三job completed/success，双Python3.11/3.12各583项实际主单测与12项独立源码审计，第三作业再次独立验证144源、72世界、来源完整性与SHA；源文件及结果永久归档于[commit70df8df6](https://github.com/edwardsage419/Psychohistory-Research/commit/70df8df6f89ed974450133115416a518ce02165b)。

正式限定结论：CLOSED_BOUNDED_E1_ARTIFICIAL_R294_TIME_INCONSISTENCY。无新真人E2，历史E3=0；既有R073及PESEN v0.1均冻结。下一原始P1待审查项为01-019 Habit Formation，继续先学完原R系列，再分类，再模型熔炼。
