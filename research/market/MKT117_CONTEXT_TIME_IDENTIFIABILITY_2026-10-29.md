# MKT117 成对偏好的时间漂移与情境变化不可辨识边界

日期：2026年10月29日。轨道：market。状态：BOUNDED_SYNTHETIC_E1。无真人数据，无新增费用。

## 仓库与新增性
本轮起点main为3ac13df3b7d35fb95953ef1355559c026f8f6dec。已读MKT116、E085、F008、R256 S52、TH120。MKT116检验矛盾回答和撤销；本轮研究时间与情境共变时的识别界限。

## 英文来源与证据
1. [开放原始论文] Son et al. (2024), Right Now, Wrong Then: Non-Stationary Direct Preference Optimization under Preference Drift, https://arxiv.org/abs/2407.18676 。使用动态Bradley-Terry模型和时间折扣研究变化偏好，主要面向LLM偏好优化。
2. [原刊公开论文] Saha and Gupta (2022), Optimal and Efficient Dynamic Regret Algorithms for Non-Stationary Dueling Bandits, https://proceedings.mlr.press/v162/saha22b.html 。研究变化偏好下的成对反馈与动态遗憾。
3. [原刊公开论文] Bengs et al. (2022), Stochastic Contextual Dueling Bandits under Linear Stochastic Transitivity Models, https://proceedings.mlr.press/v162/bengs22a.html 。研究情境条件化的成对偏好。
4. [官方技术文档] BoTorch Preference BO, https://botorch.org/docs/tutorials/preference_bo 。说明成对比较接口；本轮没有执行BoTorch。

## 独立人工实验
Node标准库脚本research/market/mkt117_preference_identifiability_20261029.js在本地执行38项断言，失败0。TIME模型在t=0选择A概率0.9，t=1为0.1；CONTEXT模型在c=0选择A概率0.9，c=1为0.1；STATIC固定0.5。这些数值完全由本轮人为设定。

初始两次观察(t=0,c=0,选A)和(t=1,c=1,选B)，TIME和CONTEXT联合似然均为0.81，STATIC为0.25。对这两条观察，时间漂移与情境变化完全不可区分。增加交叉观察(t=0,c=1,选A)和(t=1,c=0,选B)后，TIME四次似然0.6561，CONTEXT为0.0081，似然比81。交叉设计在这些人工假设下提高辨识力，仍存在随机误判。固定时点与情境下相反回答在全部模型中概率均非零，单次矛盾不能证明真实漂移。

脚本还核验ABSTAIN不产生授权，撤销最新授权后返回NO_ACTIVE_PREFERENCE，旧批准不会自动复活。

## 机制与限制
所需真实输入：候选结果、时点、情境、成对回答、拒答、撤销、授权版本。状态：事件级偏好与模型似然。算法目标：建议追加辨识性询问，不能由此形成唯一人生效用权重。反馈：重复或交叉询问可能增加信息；解释需显示模型假设、样本覆盖与不可辨识原因。隐私：时间与情境关联的个人偏好可能敏感，本轮没有采集。费用：免费公开论文与Node标准库；真实产品运营费用未知。局限：二时点二情境、已知概率、人工观测、无真人长期决策验证。

证据等级MARKET E1。论文支持研究方法存在，38项程序检查支持本轮人工反例。论文理论保证不可外推为人生决策质量。候选控制均UNADOPTED：分开记录时间和情境；支持拒答、矛盾与撤销；提示不可辨识；高影响决策需人工授权。R系列主线及冻结协议不变。

下一项MKT118：固定问答预算下比较交叉、重复与随机询问的误判率。