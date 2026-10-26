# MKT044 ProjectionLab 固定日期基线、动态计划与预测归因

日期：2026-10-26，Asia/Singapore。研究轨：market。状态：COMPLETE_BOUNDED_OFFICIAL_DOCUMENTATION_AND_EXACT_SYNTHETIC_COUNTEREXAMPLE。前置 main HEAD：7b2cb547f1e0a30ae802e0d0b0634c341a7f2b02。此前 MKT002、MKT027、MKT028 已研究随机模拟、区块重采样和弹性支出，本轮专注固定起点、计划修订、时间对齐及结果归因，避免重复。新增费用 0。未注册产品、未使用真实财务数据、未调用收费 API、未运行厂商引擎或 Actions。

## 1. 官方机制，来源为英文资料

2023-01-21 官方《What are fixed-date plans?》明确两种计划起点。Start Now 始终从当前日期开始，继承 Current Finances 的最新余额。Fixed Date 具有独立的固定起始条件与固定起始日期，可以保存初始计划供后续实际进度对照。来源：https://projectionlab.com/help/fixed-date-plans

2023-01-18 官方《How should I update my plan(s)》建议分别保留很少修改的固定日期原始计划，以及持续更新、继承当前财务数据的动态计划。属于官方建议的操作方式，不能据此推断系统自动创建不可修改的审计快照。来源：https://projectionlab.com/help/update-plans-over-time

2023-12-13 官方《How do I compare actual progress to my projections?》指出，实际进度叠加需要 progress points 和起始时间足够早的 fixed-date plan；从当前日期开始的计划无法显示起点以前的进度。来源：https://projectionlab.com/help/overlay-actual-progress

2024-12-14 What If 帮助文档及 2024-12-13 v4.2.0 更新日志介绍基准与修改后计划叠加、年度条目差异和里程碑变化；这些是交互比较功能的厂商文档证据。来源：https://projectionlab.com/help/using-what-if 以及 https://projectionlab.com/changelog

2026-08-18 官方说明，Plan 使用固定年度增长假设，Chance of Success 使用历史或随机市场路径；其他标签页使用 Plan 的假设。两者基于同一计划输入，但随机情景不构成现实概率已校准的证明。来源：https://projectionlab.com/help/plan-vs-chance-of-success

## 2. 可复算合成反例：计划起点漂移和因素混合

定义人工两年终值 F(B,r,h)=B(1+r)^h。仅为演示时间与状态版本混合风险的自建数学模型，未复现厂商现金流、税收、随机模拟或 UI。2026 年原计划初始 B0=100、r0=5%；2027 年新财务快照 B1=120、新假设 r1=8%。同为两年预测视窗时：
F(100,5%,2)=110.25；
F(120,5%,2)=132.30；
F(100,8%,2)=116.64；
F(120,8%,2)=139.968。
总差 29.718。两因素对称分解为起始余额 22.689，增长假设 7.029，合计 29.718。交互项为 1.278，不能直接将终值上升全部归功于改进的决策能力。

若对齐到相同的 2028 年末，原 2026 计划两年预测为 110.25，新 2027 计划仅剩一年预测为 F(120,8%,1)=129.60，差额 19.35。将 2027 年计划的两年终值 139.968 直接与 2026 年计划的 2028 终值比较，会将不同目标日期混为同一预测。

Python 3 标准库精确复算：
```python
from fractions import Fraction as Q

def f(balance, growth, horizon):
    return balance * (1 + growth) ** horizon

b0, b1 = Q(100), Q(120)
r0, r1 = Q(5, 100), Q(8, 100)
a = f(b0, r0, 2)
b = f(b1, r0, 2)
c = f(b0, r1, 2)
d = f(b1, r1, 2)
balance_effect = (b - a + d - c) / 2
assumption_effect = (c - a + d - b) / 2
interaction = d - b - c + a
assert (a, b, c, d) == (Q("110.25"), Q("132.3"), Q("116.64"), Q("139.968"))
assert balance_effect == Q("22.689")
assert assumption_effect == Q("7.029")
assert interaction == Q("1.278")
assert balance_effect + assumption_effect == d - a
assert f(b1, r1, 1) - a == Q("19.35")
print("same_horizon_delta", d - a)
print("balance_effect", balance_effect, "assumption_effect", assumption_effect)
print("same_calendar_target_delta", f(b1, r1, 1) - a)
```
本轮已在本地以 Fraction 独立运行并核对上述数值。所有金额与增长率均为人工参数，不构成财务建议、真实用户改善或产品实测。

## 3. 产品研究维度

真实输入：用户手动设置财务账户、负债、收入、支出、增长率、事件和里程碑。官方文档说明 Now 计划继承 Current Finances，Fixed Date 使用独立起始条件。状态：当前财务快照、固定日期起始状态、计划时间轴、情景结果和进度点。算法：官方说明年度确定性模拟和历史或随机情景，完整计算引擎源码未核对。目标：用户配置的财务里程碑、支出约束和阈值。反馈：可记录实际进度并对照原始计划，更新动态计划及 What If；未获得自动根据历史预测误差进行统计校准的独立证据。

解释性：年度条目差异、情景叠加及进度图能展示部分差异来源；文档未证明系统自动保留完整不可篡改的计划版本链、参数哈希、评分冻结时点或因果归因。隐私与权限：2026-08-12 厂商安全页称使用 Google Cloud Firestore，TLS 与静态加密、MFA、数据导出及删除，备份按固定周期到期；其 SOC 2 对齐表述不等于该产品已获 SOC 2 认证，云提供商认证不应移作产品认证。来源：https://projectionlab.com/security

费用：2026-10-26 官网 Basic 为 0 美元每年，Premium 129 美元每年，Pro 549 美元每年；What If、Compare、Multiple Plans 属 Premium 列表。来源：https://projectionlab.com/pricing 。本研究只审查公开页面，不注册试用或使用付费功能。

## 4. 候选风险与控制

MKT044-R1：动态 Now 计划随余额更新而改变起点，历史预测误差可能被重置。候选控制：保留不可静默修改的预测生成时间、固定目标日期、数据截止时间和原始快照。
MKT044-R2：新旧计划比较同时混合状态更新与参数修订。候选控制：对同一预测视窗执行两因素或多因素情景分解，并明确交互项及其归因约定。
MKT044-R3：比较不同目标年份的终值，误报预测改善。候选控制：先统一预测目标日、计量单位、通胀基期和样本窗口。
MKT044-R4：事后改动目标阈值造成看似达标。候选控制：原始目标、经用户批准的修订目标、描述性基准分别版本化，不预设唯一人生效用权重。
MKT044-R5：厂商云端存储及导出形成副本。候选控制：将数据访问授权、导出、删除和备份生命周期分开记录，遵守 F002。
MKT044-R6：将 Monte Carlo 情景占比当作真实未来校准概率。候选控制：报告模拟假设、抽样方法、敏感性和独立外推评分缺口。

以上均为未来研究候选，不改变冻结 R 系列协议，不开发个人决策产品。

## 5. E 与 F 状态、证据等级

2026-10-26 的 E004 至 E012 已有实质审计。本轮新核查 R174 第三方法及 B 轨收据，另见独立路径 E013。2026-W44 F002 已完成撤销、衍生数据和备份生命周期专题，本轮不重复创建 F。MKT044 对 F 的新增问题是原始计划、动态计划、进度点和导出副本是否具有独立的撤销与删除边界。

证据等级：MARKET_E1_OFFICIAL_DOC + INDEPENDENT_EXACT_SYNTHETIC_ARITHMETIC。官方功能与定价为厂商公开陈述，独立数学计算只支持人工模型。未验证真实引擎、用户长期效果、独立安全合规或现实预测校准。新增真人 E2=0，历史 E3=0。

## 6. 下一项

MKT045：深读 ProjectionLab Progress Points 的编辑、历史覆盖、导出与数据时间戳规则，核查固定原始计划在长期追踪中能否提供可追溯的预测评分账本。若资料不足，转向公开开源的 forecast ledger 与版本化预测机制。维持零新增费用与先 R 系列、后归纳、最后熔炼的主线。
