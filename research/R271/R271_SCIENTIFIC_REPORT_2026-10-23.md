# R271 正式科学报告：预注册分析、未校正多重择优和事先声明的家族校正

日期2026-10-23 Asia/Taipei。原239模型目录12-001 Preregistration and Registered Reports（P0）。研究编号R271，科学证据等级限定E1：人工公平二元零假设、完整有理概率空间；未实施真实注册报告或真实人类实验。

## 1. 第一来源与本研究的限定目标
Nosek, B.A. et al. (2018), *The preregistration revolution*, PNAS 115(11):2600–2606, DOI https://doi.org/10.1073/pnas.1708274114；Chambers, C.D. (2013), *Registered reports: a new publishing initiative at Cortex*, Cortex 49(3):609–610, DOI https://doi.org/10.1016/j.cortex.2012.12.016 。两篇论文分别讨论预注册与期刊注册报告制度。**本次研究只建立关于选择多个分析与假阳性风险的有限数学例子，没有在实际注册平台预先注册，也没有期刊Stage 1接收或任何真实发表偏差实证评价**。

## 2. 事前冻结的模型与原始来源
[原始冻结协议](../../protocols/R271_PREREGISTRATION_9_DECISION_WORLDS_13104_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)首先经GitHub提交[commit b5a1d888](https://github.com/edwardsage419/Psychohistory-Research/commit/b5a1d888ee830759f599cf39cae8120ed3f84d59)，随后才编写程序及查看正式计算输出。

真实数据机制冻结为每个原bit独立Bernoulli(1/2)，因此所有待检验成功率高于1/2的单侧检验在零假设下。每个区块包含4个原独立bit，原始精确p_value(K)=sum_{j=K}^4 C(4,j)/16。K=0..4的p依次1、15/16、11/16、5/16、1/16；所有候选检验家族的共同nominal阈值alpha=1/8。

同一预定m∈{1,2,3}独立区块数，对比三冻结分析政策：FROZEN_FIRST只报告先选的第一个区块；FLEXIBLE_ANY在看到全部m结果后选择至少一个未经校正的raw p≤1/8报告；BONFERRONI_ANY公开事前检验家族m并要求raw p≤1/(8m)。每个m的原source全集有2^(4m)种，等质量2^(-4m)，共3×(16+256+4096)=**13104条带world/policy标签完整人工source**。三政策共享相同原bit，因此独立原source类型按m合计4368，不能将13104解释为13104个实验。

## 3. 精确独立计算方法
路线A穷举全部13104种原bit数据，逐block实际重新计算四次Bernoulli成功数、全部raw binomial p值、冻结policy的报告选择索引以及是否报告阳性，并用Fraction来源质量分别积分九world真实零假设下的声明阳性概率。
路线B完全不调用来源枚举：单块K=4的概率为1/16，m个独立区块均未命中的概率(15/16)^m，故FROZEN_FIRST永远1/16、FLEXIBLE_ANY为1−(15/16)^m；BONFERRONI_ANY取上述联合概率仅当最小可实现raw p=1/16不大于alpha/m，否则严格0。九world概率与路线A严格有理一致。
路线C GitHub CI第三job另写逐原bit的CSV内容审计，重新复核选择索引、每block raw p、总原概率质量、每world阳性概率，且核验source和result SHA256。

## 4. 九世界最终真实零假设误报结果

|原始独立检验区块m|预先固定第一个检验|事后未校正择优|事前Bonferroni校正|
|---|---:|---:|---:|
|1|1/16|1/16|1/16|
|2|1/16|31/256|31/256|
|3|1/16|721/4096|0|

名义家族误报阈值1/8=12.5%。当m=3且未经校正事后择优报告，零假设下声明阳性的概率达到721/4096约17.60%，已超过冻结阈值；原先固定第一个检验则所有m只有1/16=6.25%。在m=2时，未经校正家族风险31/256约12.11%，虽已高于固定单次检验，却仍未超过12.5%，不能将所有探索行为都描写为“必定超越名义阈值”。m=3的Bonferroni要求p≤1/24，而四bit精确单侧检验最小p只有1/16，所以此项退化成全部不拒绝，说明统计离散性与保守性边界，绝不意味着Bonferroni的所有真实应用必定过度保守或不可能发现效果。

在本设计下，假设是真正已知H0，false positive确实有概率解释；并未建立真实发表概率、人类报告偏差或真实研究者是否违反预注册的因果效应。

## 5. GitHub正式执行和永久来源归档
[完整可运行Python程序](r271_exact_preregistration_familywise.py) · [全部13104原source和每块raw p值CSV](R271_ALL_13104_ORIGINAL_NULL_POLICY_SOURCE_TYPES.csv) · [九world完整精确结果JSON](R271_EXACT_NULL_REPORTING_RESULTS.json) · [机器SHA256凭证](R271_MACHINE_RECEIPT.json) · [最终GitHub CI run39902734610](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39902734610)。

Python3.11与3.12各82项真实unittest通过、共164项；第三独立来源逐行验证通过，三job全completed/success。全原CSV、结果JSON和机读SHA永久机器人提交入main：[3d99415b](https://github.com/edwardsage419/Psychohistory-Research/commit/3d99415bfe7da4449462c42da8d8ecafb83a9d88)。
原source CSV SHA256：`c38bd5cf3fa01195dded1c9d73ad66d4aefde8d073fecfcd81bc2736e9340a8e`；结果JSON SHA256：`8d3ad41e74dfcc7e1ea63ace34060f887f3d009baf30a24b097f4525cd9736fc`。

## 6. 研究边界、方向与目录
预注册理论上需要在结果揭晓前锁定假设、选择标准、排除规则、分析方法、比较家族以及偏离方案的审计轨迹；注册报告还有真实编辑与同行评审制度，本研究没有评估这些制度机制。冻结协议只证明有限人工检验家族的概率特征；**预注册本身不能让错误的分析有效，也不会自动对全部多重比较实施校正**。新真人E2=0、真实历史E3=0，R073/PESEN v0.1仍冻结。

按原239目录，下一模型是12-002 Out of Sample Prediction（P0，拟R272）。用户决定仍生效：先完成全部原R系列模型学习研究，再统一归纳分类，最后才开始熔炼；个人辅助决策体系实施继续暂缓。
