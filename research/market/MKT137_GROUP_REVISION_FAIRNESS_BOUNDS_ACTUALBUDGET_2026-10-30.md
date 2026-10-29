# MKT137 方向性标签修订、分组校准部分识别与 Actual Budget 机制

日期：2026-10-30 Asia/Singapore。目标键：(market,MKT137,none,asof-group-calibration-revision-ActualBudget)。状态：COMPLETE_BOUNDED_ARTIFICIAL_E1。维持R系列全部完成后归纳、最后熔炼；无真实个人数据。

## 1. 预设人工实验

两个组各4条二元预测，A固定p=1/4，B固定p=3/4。各组仅有2条标签可见，其余2条始终未知。cutoff4的可见标签A=[0,1]、B=[1,1]；cutoff8只修订A首条0为1；cutoff10再修订B首条1为0。修订按其实际可见时间应用，历史as-of快照不被覆盖。对每个cutoff枚举4个未知二元标签的全部16种完成方式，不给完成方式设定等概率或缺失随机假设。

每组校准误差定义为 |组内真实阳性率 - 固定预测概率|，两组差定义为A误差减B误差。Brier差同样为A减B。所有计算使用整数，校准差单位1/4，Brier差单位1/8。

| cutoff | 校准差可行界 A减B | Brier差可行界 A减B | 校准差大于0/等于0/小于0的完成方式 |
| --- | --- | --- | --- |
| 4 | [-1/4,1/2] | [-1/8,3/8] | 8/6/2 |
| 8 | [0,3/4] | [0,1/2] | 14/2/0 |
| 10 | [-1/4,3/4] | [-1/8,3/8] | 11/4/1 |

cutoff8的16种可能结果中，A的分组校准误差均不低于B，但存在2种平局，无法断言严格更差。cutoff10的B组标签修订使组间优劣重新不可确定。三个cutoff均不能保证A严格更差，因此固定规则“仅当差值下界严格大于0才判定A更差”均返回ABSTAIN。16种完成方式的计数只是可行世界组合数，不能当作发生概率、置信水平或群体公平性的实际统计结论。

归档程序：research/market/mkt137_group_calibration_revision_bounds_20261030.js。已在V8中执行全部48种人工完成方式，9项正向断言及4项非法输入拒绝PASS；原生Node.js CLI及GitHub Actions NOT_RUN。人工E1，真人样本外E2预测0、历史E3新增0、外部独立复现0。这里的公平性仅指两组校准误差比较，未覆盖机会平等、不同损失偏好或因果公平。

## 2. Actual Budget 英文官方机制深读

产品官方站点 https://actualbudget.org/ ，规则 https://actualbudget.org/docs/budgeting/rules/ ，API https://actualbudget.org/docs/api/reference/ ，同步与安全 https://actualbudget.org/docs/getting-started/sync/ ，预算方法 https://actualbudget.org/docs/budgeting/ 。仅公开文档审查，未安装、登录、银行连接或运行服务。

* 数据输入：账户、交易日期、整数金额、原始商户、分类、备注、清算状态、可选银行导入ID；支持手工录入、文件导入和可选银行同步。
* 状态表达：账户余额、按月预算、分类、交易、规则、周期计划及同步副本。Envelope预算以当前可用现金约束支出分配，Tracking预算允许未来收入支出计划。
* 算法：交易导入后依次执行条件动作规则，后执行的匹配规则覆盖同字段先前结果；规则分pre/default/post阶段，阶段内自动按具体程度排序。用户重命名商户和分类时可自动产生规则。导入ID避免重复；无导入ID时基于金额、日期、商户进行启发式匹配，官方要求复核。
* 目标与反馈：超支后调整预算分类、每月重新规划；规则可由用户查看、修改、删除。属于可解释的预算反馈与规则自动化，公开资料没有提供经验证的长期人生多目标效用优化或真实行为改善因果试验。
* 隐私与权限：设备本地有完整数据，选定服务器可同步；可选端到端加密覆盖预算数据。官方明确银行同步令牌另存服务器，**不受预算数据端到端加密保护**；设备本地数据仍为明文，建议设备全盘加密。遗失加密口令且无本地副本时无法恢复。服务器部署、备份、权限及银行服务商另需审计。
* 费用：官方开源产品本身免费，官方演示页面明确100% free/open source。自行部署到已有设备可能符合零新增费用；任何托管服务器、银行同步提供商的收费或硬件费用均未获授权，不能默认免费。
* 证据分层：以上功能、规则与加密范围为官方技术文档支持；未独立运行、审计加密实现或验证市场效果。算法说明可以启发“用户可检查的修正规则”，不能当作心理史学科学验证。

## 3. 候选控制与后续

候选记录字段：prediction_at、group_id、group_definition_version、label_first_seen_at、label_revision_at、label_version、audit_cutoff、missing_label_count、group_calibration_bounds、ranking_abstain、rule_change_log。多目标价值权重保持未定。下一项MKT138：标签缺失的群组依赖与差异性修订选择，在冻结样本定义后测试。保留R073及PESEN冻结。

无新增订阅、付费API、付费CI或敏感数据。GitHub实际账单及免费权益未核验。
