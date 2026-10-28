# MKT110 ProjectionLab现金流强制目标与流动性储备的可行性边界
日期：2026-10-29（Asia/Singapore）。轨道：market。证据：MARKET E1。官方英文文档与人工约束枚举，零新增费用。

## 去重
MKT108研究Flow排序，MKT109研究Beeminder追赶负担与ProjectionLab跨账户强制资金。本轮新增：当目标和最低储备无法同时满足时，必须分别标记可行性与违规候选，不预先指定人生效用权重。

## 官方资料与证据
S1 ProjectionLab 2026-07-24 https://projectionlab.com/help/mandatory-goals ：Always Fund允许动用其他账户，文档未明确说明所有可提款资金不足时的终止、报错或最终缺口行为，状态UNKNOWN。
S2 ProjectionLab 2026-09-10 https://projectionlab.com/help/cash-flow-priorities ：Flows按顺序分配，支持最大化、剩余收入百分比和固定金额。
S3 pymoo 0.6.2 https://www.pymoo.org/constraints/index.html ：公开说明可行性优先、惩罚、约束违反作为目标及epsilon方法。不能推断ProjectionLab采用pymoo。
S4 pymoo https://pymoo.org/constraints/as_obj.html ：约束违反作为目标可以揭示权衡，也可能输出不可行候选。
S5 ProjectionLab 2026-08-12 https://projectionlab.com/security ：厂商描述TLS、静态加密、MFA、账户删除和备份按周期过期，独立安全与实际删除验证UNKNOWN。
S6 ProjectionLab https://projectionlab.com/pricing ：Basic免费，Premium每年129美元，Pro每年549美元。未注册或购买。

## 输入、状态、目标、反馈与算法
官方资料支持收入、支出、账户余额、Flow优先级、目标金额和资金来源的输入；状态包括现金盈余、账户资产和资金分配。官方文档支持优先顺序与跨账户提款反馈。实际生产引擎的资产选择、透支防护、资金耗尽后的处理、长期效用学习与前瞻校准均UNKNOWN。
人工模型设当期盈余200美元、可提款资产150美元、最低保留100美元、目标贡献300美元。贡献x为200到300每10美元一格。提款x−200，余额350−x，目标缺口max(0,300−x)，储备违规max(0,x−250)。忽略税费、借款、资产限制及价格波动。

## 实际人工检验
research/market/mkt110_financial_feasibility_frontier_20261029.js 在隔离V8执行84项确定性断言，0失败。11个候选均不能同时满足完整贡献与最低储备。保留储备时最多贡献250，目标缺口50。贡献300则储备缺口50。贡献270则目标缺口30、储备缺口20。六个非支配候选为250、260、270、280、290、300，它们全部存在至少一项违规。非支配不等于满足硬约束或获得执行许可。

## 候选控制及局限
C1 先报告FEASIBLE或INFEASIBLE、约束版本、资金缺口及剩余流动性。
C2 无可行解时拒绝自动执行，显示不同放松条件的影响，由人类选择是否调整目标或储备。
C3 如展示违规Pareto候选，逐项标记违反量，重大资金操作逐项人工确认。
C4 对实际产品的资金耗尽路径、生产算法、长期收益和独立安全验证保持UNKNOWN；人工算术不能升级为真人E2。
C5 仅用免费公开文档及人工数据，禁止收费API、付费注册及收费CI。

下一项MKT111：审查开源求解器在无可行解时的退出状态和约束违反向量。
