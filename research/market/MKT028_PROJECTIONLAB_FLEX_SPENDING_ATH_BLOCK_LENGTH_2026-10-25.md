# MKT028 ProjectionLab 弹性支出、历史峰值阈值与区块长度交互

date: 2026-10-25 (UTC+08)
track: commercial_market
subflow: market
status: COMPLETE_BOUNDED_OFFICIAL_DOC_AND_EXACT_SYNTHETIC_ENUMERATION
prewrite_main_head_observed: 3e95b56782c9669957a2676476ac76d0c5e91404
prior: MKT002、MKT027；本轮新增 2026-07-22 Flexible Spending 操作说明中的 ATH 触发、净流量排除、Scope、Step/Linear、试验次数，以及支出底线和区块长度联动的穷举合成实验。
source_language: English only
evidence: MARKET_E1_OFFICIAL_HELP_AND_CHANGELOG + EXPLORATORY_EXACT_SYNTHETIC_ARITHMETIC
product_engine_executed: NO
formal_preregistered_scientific_validation: NO
new_CI: NOT_RUN
new_spend: 0 (account-wide billing and GitHub allowances not independently checked)
privacy: no personal data, paid accounts, authentication, cloud compute, or personal decision product

## 1. 本轮新增的可核实产品机制

**F1，2026-07-22 官方操作文档。** ProjectionLab 的 Optimize > Flexible Spending 提供 None 与 Flexible 两种模式。规则按组合投资表现相对历史最高值 ATH 的回撤触发；官方明确该表现指标排除存入和提取现金流。可设多个规则、开始结束日期，触发模式为 Step 或在规则间 Linear 插值。默认规则示例为“回撤20%时，可自由裁量支出减少30%”，用户可调整比例。此为厂商公开功能说明，尚无真实引擎运行或源码核对。

**F2，支出范围与保护例外。** Scope 可选 Discretionary Spending，或 All Spending；后者仍排除税、债务支付、真实资产保险与 HOA 费用。支出输入可标记 Discretionary、Essential、Hybrid、Not Spending。用户可自定义 Spending 指标纳入税、按揭本金等条目，出租物业支出始终排除。因而“支出指标”与“可调整支出”不应混为一个集合；对 Hybrid 的内部按比例拆分算法，本轮没有源码证据。

**F3，结果展示与试验次数。** Flexible Spending 界面提供年度支出图与 Chance of Success。官方文档称 Pulse Check 运行98条试验、Full Run运行196条，并将 Flex/No Flex 结果归入6种类别。这些是特定界面的官方文档数值，不能替代 MKT002 记录的其他 Monte Carlo 页面上限，更不能推断产品现实成功概率已校准。

**F4，版本和定价。** 官方 2025-10-13 v4.4.0 首次公开 Flex Spending 与 Block Bootstrap；2026-10-25 官网列 Basic $0/year、Premium $129/year、Pro $549/year，Flexible Spending 列在 Premium 权益。未注册、购买或试用。官方宣称新抽样更真实，尚无独立真实市场外推评分支撑该优越性。

## 2. 有界合成实验，独立于厂商产品

**预设计算规则（本轮分析前明确，未在 GitHub 事前冻结，不计作正式预注册验收）：**
初始可提款余额100单位，四年，基础历史收益 U=+1/5、U=+1/5、D=-1/5、D=-1/5。所有路径都由这4个历史位置抽取。Block Length 1：4个单年位置每次有放回抽取，四次拼接，共4^4=256个等权位置序列（相同收益值的重复位置仍分别计权）。Block Length 2：重叠连续区块 UU、UD、DD，每次等权有放回抽取两个区块，得到3^2=9个等权位置序列。两者都是**本报告自行规定的**合成采样器，未知是否与厂商具体边界及权重实现一致。

年度先计算余额投资回报，再支付当年费用。基础可自由裁量支出10，必要支出 E∈{10,15,20}；No Flex 每年支付 E+10。Flex 使用独立于存取款的市场价格指数 P，P0=ATH0=1，Pt=Pt-1*(1+rt)，ATHt=max(ATHt-1,Pt)。若 Pt/ATHt ≤4/5（相对历史峰值回撤至少20%），当年可自由裁量支出减少50%至5，否则为10。选择50%作为本报告实验参数，**不是**官方默认30%。按 Step 阈值而非 Linear 插值。余额递推 Bt=Bt-1*(1+rt)-Et-Dt。若任意年 Bt<0，该路径记为失败，后续负值只供诊断，不能解释为可实际借款或可持续提款。成功指四个年末余额均非负。无税、通胀、借贷、交易成本、收入、行为反弹或账户异质性。

**标准库 Fraction 穷举结果（本轮实际运行）：**

| 必要支出 E | 区块长度 | 路径位置数 | 无弹性成功数 | 有弹性成功数 | 有弹性新增成功数 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 1 | 256 | 176 | 240 | 64 |
| 10 | 2 | 9 | 6 | 8 | 2 |
| 15 | 1 | 256 | 112 | 144 | 32 |
| 15 | 2 | 9 | 5 | 5 | 0 |
| 20 | 1 | 256 | 48 | 80 | 32 |
| 20 | 2 | 9 | 2 | 4 | 2 |

固定 E=15 时，长度1无弹性112/256=7/16，有弹性144/256=9/16；长度2分别5/9、5/9。区块长度变化改变了合成样本路径分布，因此不能把两种占比差异归因于支出政策本身；弹性支出在此简化模型下从未增加提款金额，故本次所有成对路径中均未出现“原成功、弹性后失败”。

**完整可运行复算脚本，Python 3 标准库，使用有理数且无随机种子：**

```python
from fractions import Fraction as Q
from itertools import product

historical = (Q(1, 5), Q(1, 5), -Q(1, 5), -Q(1, 5))

def paths(length):
    blocks = [historical[i:i + length]
              for i in range(len(historical) - length + 1)]
    for selection in product(blocks, repeat=4 // length):
        yield sum(selection, ())

def succeeds(sequence, essential, flex):
    balance, index, peak = Q(100), Q(1), Q(1)
    survived = True
    for annual_return in sequence:
        index *= 1 + annual_return
        peak = max(peak, index)
        cut = flex and 5 * index <= 4 * peak
        discretionary = Q(5) if cut else Q(10)
        balance = balance * (1 + annual_return) - essential - discretionary
        if balance < 0:
            survived = False
    return survived

for essential in (10, 15, 20):
    for length in (1, 2):
        seqs = list(paths(length))
        baseline = [succeeds(s, Q(essential), False) for s in seqs]
        flexible = [succeeds(s, Q(essential), True) for s in seqs]
        rescued = sum(not a and b for a, b in zip(baseline, flexible))
        assert not any(a and not b for a, b in zip(baseline, flexible))
        print(essential, length, len(seqs),
              sum(baseline), sum(flexible), rescued)
```

预期标准输出逐行：`10 1 256 176 240 64`、`10 2 9 6 8 2`、`15 1 256 112 144 32`、`15 2 9 5 5 0`、`20 1 256 48 80 32`、`20 2 9 2 4 2`。

**解释边界：** 以上是完全人为的四年收益、两种区块抽样和三档必要支出条件下的有限路径计数。没有真实市场历史分布、抽样误差估计、现实概率校准、用户行为有效性或厂商引擎独立复现。此处的50%消费削减是否可行完全未经过行为实验。以相同必要支出比较两种采样器才有可比性，且仅限各自合成条件。

## 3. 输入、状态、目标、反馈、解释与隐私

输入：账户、收入、支出类别、回报历史或随机分布、区块长度、ATH回撤阈值、弹性幅度、Step/Linear、适用时段及目标。状态：逐年资产余额、回撤、支出类别和模拟结果；本报告自建模型额外显式记录不含存取款的指数 P 与历史峰值。算法：产品公开披露行为阈值与重采样概念，完整内部时序、插值、Hybrid 划分及现金流优先级未独立验证。

目标：用户定义的财务约束和分类，不设统一人生效用权重。反馈：界面可调阈值和查看路径/分布；未见公开证据证明会从真实行为偏差自动校准规则。解释：公开规则可理解，但模型内成功比例仍依赖抽样权重、现金流、分类与支出削减的可行性。隐私：沿用 MKT027 的厂商云端存储、导出和账户删除声明，未独立检验实际删除传播；本轮没有真实财务数据。费用：官网 Premium 包含 Flexible Spending，价格见上，不发生项目消费。

候选风险 MKT028-R1：用余额（含提款）计算回撤，会误触发消费削减；候选控制：明确市场表现指数与现金流分离。
MKT028-R2：把 Essential、Hybrid、Not Spending 错划为可裁减，侵蚀生存底线；候选控制：硬性保护类别与例外明示。
MKT028-R3：区块长度及重叠抽样改变样本分布，成功比例跨设置不可直接比较；候选控制：报告抽样单位、区块边界、路径权重及敏感性。
MKT028-R4：模拟假定的50%裁减行为未必真实可执行；候选控制：记录行为可行性与执行偏差，不把设定视为实测事实。
MKT028-R5：高精度模拟比例导致过度信任；候选控制：展示模型内路径占比、外部校准缺口与拒绝自动执行选项。

## 4. E 当日只读治理增量

已读取本日 E002/E003；本日实质治理审计已经完成，本轮避免再创建 E004。读取最新 R153 透明修订、第三方法科学报告、B独立审计、R154 科学报告及近期提交记录。

**新核对的治理事实：** R153 原冻结144项边际门槛3e-28有48项失败，首次失败保留；首次执行后透明修订001将门槛调整为1e-25，144项才通过，结论限定为 `PASS_BOUNDED_INTERNAL_WITH_DISCLOSED_AMENDMENT`。R153 科学报告另记录216循环、108吸引力比较、B的96项凸目标扰动；这些均为同一组24个人工世界的内部E1，不构成独立真实数据。R154新三时点可识别性报告记录100个人工世界，86个非稳态世界在本组离散网格内可唯一反演，14个稳态世界仍有歧义；源代码及收据已归档，报告明示新CI未运行。此次未重新执行R153/R154代码，未做全仓冻结文件哈希审计。

E003登记的R136冻结负对照失败与缺失完整CSV继续开放；original239 v7.8 的154项逐项待核是既有登记，本轮未重新计算索引。未见本轮需改写R系列或其冻结协议的理由。未对最新提交运行新CI；不把`[skip ci]`、GitHub提交成功或旧CI记录当作新算法CI通过。R系列先行的研究顺序不变。

## 5. F 本周状态

2026-W43 F001 已归档并完成（人类否决权、最小采集、解释和审计日志）。本轮没有重复创建F专题。为下一周F002登记新增候选风险：财务数据中 Essential/Hybrid 标签错误导致安全底线侵蚀，ATH触发策略的解释与拒绝路径，导出副本与云端保存数据的授权撤回边界。此处仅为原则性风险记录，没有接入个人数据、实施控制或开发产品。

## 6. 来源、归档与下一项

S1 官方 Flexible Spending 帮助，2026-07-22：https://projectionlab.com/help/flex-spending
S2 官方 v4.4.0 发布说明，2025-10-13：https://projectionlab.com/blog/whats-new-v440
S3 官方更新日志：https://projectionlab.com/changelog
S4 官方支出录入帮助，2026-09-09：https://projectionlab.com/help/adding-expenses-to-your-plan
S5 官方价格页，2026-10-25访问：https://projectionlab.com/pricing
S6 前序 MKT027：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/market/MKT027_PROJECTIONLAB_BLOCK_BOOTSTRAP_SEQUENCE_RISK_AND_CORRELATED_ACCOUNTS_2026-10-25.md
S7 E003：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/operations/E003_R136_FROZEN_NEGATIVE_CONTROL_INCIDENT_DELTA_2026-10-25.md
S8 F001：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md

证据分级：厂商官方帮助与定价为 MARKET_E1_OFFICIAL_DOCUMENTED_CLAIM；本轮Fraction穷举为 EXPLORATORY_SYNTHETIC_EXACT（仅验证本文构造）；R153/R154是仓库记录的内部数学E1。第三方独立产品验证、真实个人样本、真实预测校准与安全验证均未成立。没有购买、计费API、收费CI、GPU、云部署、敏感数据；主动新增费用0，账户整体账单与免费额度未核验。

下一项 MKT029：研究 Beeminder 的安全缓冲、目标曲线 ratchet、承诺损失与误报纠错机制；先读取已有 Beeminder 市场报告，优先官方文档及可核查的真实用户行为证据，避免连续重复同一产品。E继续按日只读，F下周推进F002。保留先完整R系列、再统一归纳、最后模型熔炼的主线。
