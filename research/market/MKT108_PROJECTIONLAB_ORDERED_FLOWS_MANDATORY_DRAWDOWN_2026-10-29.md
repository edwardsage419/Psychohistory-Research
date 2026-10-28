# MKT108 ProjectionLab 顺序现金流目标、强制拨款与多目标冲突

日期：2026-10-29（Asia/Singapore）。轨道：market。状态：BOUNDED_OFFICIAL_DOCUMENT_REVIEW_AND_SYNTHETIC。证据：MARKET E1。新增费用0。

## 去重及研究定位
已读 MKT002（确定性与Monte Carlo分离）、MKT079（税务Optimizer束搜索与目标敏感性）、MKT107（restic保留边界）及本周F005。本轮只研究现金流目标按序分配、强制目标的账户提款、目标顺序对结果的影响；没有重复模拟随机投资路径或束搜索。

## 英文官方原始来源
S1 2026-09-10 《How to Add Flows to your Plan》 https://projectionlab.com/help/cash-flow-priorities 。按序处理Flow；Maximize Contribution优先填满目标；% of Remaining Income以更高优先级处理后的余额为基数；Specific Amount固定周期金额；余额可储蓄或作为自主消费。
S2 2026-07-24 《How can I set up mandatory goals that must always be completed?》 https://projectionlab.com/help/mandatory-goals 。Always Fund目标优先于普通Flow，若当期盈余不足可以提取其他账户资金；Fund with Income受当期收入约束。官方没有在该页面给出所有资产不足时的完整执行细则。
S3 2026-07-20 《How Do I Create A New Plan?》 https://projectionlab.com/help/create-new-plan 。账户、收入、里程碑、Flow由用户输入并可重新排序。
S4 2023-01-18 《How should I update my plan(s) as things change over time?》 https://projectionlab.com/help/update-plans-over-time 。官方建议保留固定起始日的原计划，与使用当前财务状态滚动更新的另一计划比较；此建议不等于自动统计校准。
S5 2026-10-29查询 https://projectionlab.com/pricing 。Basic $0/年，Premium $129/年，Pro $549/年；现金流预测和多计划列在Premium权益。未登录核验单个Flow编辑功能在免费层的具体边界。
S6 https://projectionlab.com/security 。隐私与安全描述为厂商自述，未独立审计。

## 产品机制的可证实部分
输入：账户余额、收入、固定/可选支出、退休和财务目标、资金流目标及排序、强制资金流选项。状态：逐年账户和现金流、目标缺口、可用收入、资金分配及潜在提款。算法：文档支持先强制目标，再按配置的Flow顺序分配；百分比基于剩余收入。完整内部税务、账户提款优先顺序及极端资产不足分支未公开独立验证。
目标：用户选择资金流优先级与财务里程碑，未建立唯一跨人生领域效用权重。反馈：可重排Flow、比较计划、观察实际进度。真实自适应学习及前瞻预测校准未知。解释性：顺序、资金流和年度Cash Flow可观察；冲突排序的社会或心理效用没有独立证据。隐私：不需要链接银行账户的官方宣传；云数据处理及安全有效性未独立复验。费用：本轮只读公开免费英文资料，没有注册、订阅或调用计费API。

## 22项独立人工检查
脚本：research/market/mkt108_projectionlab_flow_order_mandatory_synthetic_20261029.js。已在隔离JavaScript环境执行并重新读取远端脚本复验，22项PASS、0 FAIL。
纯人工单期可分配盈余1000，A紧急基金缺口700且Maximize，B退休投资取剩余收入50%，C额外还贷固定300：
顺序A→B→C，人工分配 A=700、B=150、C=150；
顺序C→B→A，人工分配 C=300、B=350、A=350。
两种顺序的总投入均为1000，单项结果明显不同。人工强制目标300、盈余200、其他可提款资产500，概念模型为收入200加资产提款100。该提款数仅说明官方描述允许跨账户补足的后果；实际产品资产优先级、税务及资产不足时行为均UNKNOWN。
脚本还模拟资产仅50时强制目标无法全额满足的情形，此分支属于研究者的假设实现，**不能声称产品真实行为为部分完成**。

## 候选控制与科学边界
C1 记录目标顺序、强制标记、硬性资金限制、目标缺口、每步剩余资源与理由，展示同一输入不同排序的结果。
C2 强制目标应独立展示潜在资产提款、税务及机会成本，重大不可逆行动需要人工确认；用户可以拒绝建议。
C3 采用无单一效用权重的目标冲突展示，保留Pareto候选和不确定状态；本轮人工顺序模型不是Pareto优化器。
C4 固定原始基准计划并保存滚动更新计划，区分事实偏离、假设更新与用户价值偏好变化。
C5 仅使用人工数据进行未来实验，先冻结对照与评分；不得据厂商功能宣称人生决策效果。

证据等级：S1至S5为厂商官方文档和价格，S6为厂商自述；22项为人工机制反例。真实引擎运行、用户长期收益、第三方安全审计、前瞻校准均UNKNOWN。下一项MKT109优先比较Beeminder缓冲收缩与ProjectionLab强制目标的“偏离反馈和人类授权”差异，避免继续重复财务模拟。