# MKT118 四次询问预算下的偏好辨识误判率

日期：2026-10-29 UTC。track=market；subflow=product research。状态 COMPLETE（有界人工实验）。基线 main 70b3e24481a50a072d7f86fa25f1eaf2f18dedae。target_key=(market,MKT118,none,query-budget error under context failure)。承接 MKT117 的时间与情境共变不可辨识实验。所有输入均为人工假设，未接入用户资料。

## 公开英文来源与实际阅读范围

1. BoTorch 官方 Preference BO 技术教程，https://archive.botorch.org/tutorials/preference_bo 。说明 noisy pairwise comparisons、PairwiseGP 与偏好查询闭环；本轮未运行 BoTorch。
2. Sekhari, Sridharan, Sun and Wu (NeurIPS 2023), Contextual Bandits and Imitation Learning with Preference-Based Active Queries，https://proceedings.neurips.cc/paper_files/paper/2023/hash/2567c95fd41459a98a73ba893775d22a-Abstract.html 。原始论文摘要支持查询次数与学习损失共同考虑，论文理论界限未用于本轮人工数值。
3. Automerge 文档与 F008 分开归档，不混作产品偏好证据。

## 人工数据、状态、算法及精确结果

二种假设 TIME 和 CONTEXT，先验各 1/2。TIME 在 t=0 的选A概率9/10、t=1为1/10；CONTEXT在c=0为9/10、c=1为1/10。每轮可问四次，回答在固定模型下独立。ALIGNED 仅问(t,c)=(0,0),(1,1)各两次；CROSS 问四种组合各一次；REPEAT_ONE_CONTEXT 四次问(0,1)；STRATIFIED_CROSS 在(0,1),(1,0)各两次；RANDOM在四种情境有放回均匀抽四次。穷举256种随机查询设计，每种设计16个二元回答序列。分类器使用精确等先验贝叶斯最小错误决策；后验最大概率小于19/20时拒答。

| 查询策略 | 正常假设下误判率 | (0,1)变为无信息时误判率 |
| :-- | --: | --: |
| ALIGNED | 1/2 | 1/2 |
| CROSS | 1/10 | 1/10 |
| REPEAT_ONE_CONTEXT | 7/250 = 2.8% | 1/2 |
| STRATIFIED_CROSS | 7/250 = 2.8% | 1/10 |
| UNIFORM_RANDOM_WITH_REPLACEMENT | 41/400 = 10.25% | 7133/32000 ≈ 22.29% |

正常情形的拒答概率：ALIGNED 1，CROSS 9/50，REPEAT与STRATIFIED各243/5000，RANDOM 36043/80000。一个情境无信息时，CROSS在95%阈值下拒答概率为1，STRATIFIED为9/50，REPEAT为1。

新增风险：四次重复同一最有信息的询问在已知独立噪声模型中达到2.8%误判率；若该情境失效，误判率升至50%。覆盖两个可区分情境的STRATIFIED在正常模型中保持2.8%，在单情境失效时为10%。随机查询平均值是对256种设计均匀平均，不代表自适应算法表现。任何结果均不能证明未来真人的真实偏好可识别。

## 实际验证与证据等级

Python 3 标准库脚本 research/market/mkt118_query_budget_exact_20261029.py 在隔离本地环境运行，使用 fractions.Fraction 精确计算，8326项程序检查，失败0；脚本本地SHA256 4a50b91d94e1817814586e6b09dcd094103356840488e0222c1b541bb24c4ba9。上传后的远端命令行复验状态须另行记录。MARKET E1：公开技术文档与原始论文说明方法，人工精确计算说明有限假设下的结果。实际BoTorch实现、真人数据、外部团队复现、长期决策改善均 NOT_RUN。模型概率及场景失效均由本轮人为设定。

输入与权限：时间、情境、候选方案、二元偏好回答及拒答可构成敏感行为轨迹，本轮未采集。状态与反馈：模型似然、后验、误判率、拒答及查询预算。候选控制：保留交叉情境覆盖，显示拒答及模型错设风险，用户可拒绝或撤销授权，重大决策需人工确认。所有候选 UNADOPTED。费用模式：使用现有会话、公开免费资料及本地Python标准库，新增付费操作0，GitHub账单未独立核验。

下一项 MKT119：考虑偏好回答的同源相关噪声和查询疲劳，比较自适应询问的停止条件与误报风险，继续维持R系列优先。
