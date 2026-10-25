# MKT029 Beeminder 历史数据修正、扣费申诉、退出约束与隐私生命周期

date: 2026-10-25 (UTC+08)
track: commercial_market
subflow: market
status: COMPLETE_BOUNDED_OFFICIAL_DOCUMENT_AND_TOY_STATE_TEST
prewrite_main_head_observed: dbbcbd3f56df8c16142de3f72e6b68bcffeec6d8
prior: MKT001（分段目标、safebuf、autoratchet 与七日约束），MKT028（ProjectionLab 情景支出规则）
source_language: English only
evidence: MARKET_E1_OFFICIAL_HELP_API_AND_POLICY; EXPLORATORY_SYNTHETIC_TOY_STATE_CHECKS_8_PASS; INDEPENDENT_COMMITMENT_LITERATURE_NOT_PRODUCT_VALIDATION
real_product_executed: NO
paid_account_or_authenticated_api: NO
new_CI: NOT_RUN
new_spend: 0 (account-wide billing and GitHub allowance not independently verified)
personal_sensitive_data: NONE
frozen_R_protocols_modified: NO

## 1. 相对 MKT001 的新增事实

MKT001 已确认 road/roadall、delta、safebuf、safebump、autoratchet 和七日 akrasia horizon。本轮转向其**历史观测修正如何影响已经到期的承诺**、争议处理时限、退出权和数据留存。来源是官方公开 API、帮助与隐私政策；未创建真实目标、授权账户或测试收费服务。

**F1 历史记录改写可立即触发偏离。** 官方《When do derailments happen?》与《How do I fix incorrect data?》说明，删除、回填或修正过去的数据，可能使最近已过截止日的累计观测落到红线错误一侧，并立即触发 derailment，甚至不在当前截止时刻。自动同步的数据可能再次覆盖用户在 Beeminder 中的手工修正，通常需要回源修改。由此不能将“修正错误观测”视为对既有风险状态没有影响的操作。具体服务器计费和重算实现没有独立执行证据。

**F2 API 支持幂等写入标识。** 官方 API 的 datapoint `requestid` 在单目标内标识数据点。相同 `requestid` 和相同内容会被识别为重复；相同标识但不同内容会更新已有点。文档同时提供 `updated_at` 以避免无变化时重新拉取全量数据。此设计能帮助降低网络重试造成的重复计数，仍需区分重试、修正、历史版本和授权来源；未验证真实 API 的并发竞态。

**F3 申诉窗口与收费时序。** 官方《What happens when I derail?》说明通常先发送 legitimacy check，约24小时后处理收费，建议尽量提前至少6小时向支持人员反馈错误或非正当偏离。支持人员可处理争议；实际退款和个案决定没有独立验证。选择 No-Excuses Mode 后，厂商公开规则规定即使发生疾病、事故或漏记也不能按普通理由取消收费；用户可主动退出此模式，但退出不追溯已发生的偏离。其支持团队仍接受沟通，不能推定保证退款。

**F4 目标退出与账户删除存在不同边界。** 目标归档通常延后七天，在此期间仍可能偏离；创建不足七天的目标可有例外。账户创建不足七天或没有活跃目标时可直接删除。较老且有活跃目标的账户须联系支持并确认身份，厂商声明收到确认后删除账户与目标；等待期间会尽力归档目标并取消订阅，但外部脚本仍可能触发费用，需另行停用。支付处理商的历史交易金额与日期、支持邮件可无限期留存，备份可能短期存在，论坛账户另行删除。完整备份消除时间与所有衍生数据清理未独立审计。

**F5 授权撤销、历史记录与公开可见性分离。** 官方条款对 YNAB 集成明确称，撤销访问后停止后续读取，但 Beeminder 目标历史仍保存，直到删除目标或账户。官方隐私帮助称，新目标默认图表公开、原始数据点私有；他人可见图表和统计，仍可能由曲线推断敏感行为。用户可将目标设为私有。此结论限于所述 YNAB 集成和官方默认可见性，不外推至所有连接器。

**F6 费用和承诺机制。** 2026-03-06 更新的官方价格帮助说明：注册本身免费，通常可有3个免费活跃目标；若首周未创建目标则可能收取5美元；超线承诺损失通常最低5美元（首周0美元试用承诺例外），也可选订阅。真实扣费与退出约束使该产品不能用于本项目的零费用实操测试。本轮没有注册、授权、购买或支付。

## 2. 独立科研与厂商营销证据的隔离

Bhattacharya、Garber、Goldhaber-Fiebert 的2015年 NBER 论文在超过4000名运动承诺意向参与者中随机改变较长与较短承诺合同的引导，报告较长承诺引导与目标达成、后续续约存在关联的实验结果。Carrera 等2019年工作论文研究1248名健身参与者，报告承诺工具可提高运动量，但对承诺的选择也受到错误自我认知与估值噪声影响。Himmler 等2019年发表于 AEJ: Applied Economics 的软承诺田野实验报告考试参与及通过率提升，单纯提醒组没有同样效果。以上属于**不同干预场景的独立行为研究**，不能当作 Beeminder 特定产品、货币惩罚或未来跨领域人生决策模型的因果有效性证明；本轮只核查公开论文摘要与书目信息，未独立复算原始数据。

## 3. 输入、状态、算法、目标、反馈与解释边界

输入：目标类型、用户选定的分段红线、时间与截止点、手工数据点或第三方同步、来源身份、`requestid`、隐私设置、承诺金额、退出状态。状态：当前值、历史截止时点是否越线、时间安全缓冲、等待申诉、已收费或已归档状态，以及数据来源授权状态。官方 API 明示分段轨迹与缓冲字段；完整生产求值、并发顺序和收费实现未获独立源码或运行证据。

算法与目标：用户事先设定的单目标约束，服务按累计观测和红线判断风险并提供提醒及承诺损失。官方文档未证明自动学习个人长期价值、自动重估人生目标或实现跨领域效用优化。反馈与自我修正：用户可回填或纠错、调整未来目标、申请人工复核；自动数据回源覆盖可能再次改变历史。解释性：单目标阈值与数据版本可解释，但误记、自动同步和人工争议对结果的影响必须另行记录。隐私与权限：公开图表、私有数据、授权连接器、历史副本、账户删除与支付记录分属不同生命周期。费用：可能出现真实扣费，本项目不触发。

## 4. 八项独立玩具状态测试

本轮实际用 Python 3 标准库执行下列抽象规则，8/8 PASS。它们检验本文自行规定的最小状态机，**不是** Beeminder 真实 API、付款、归档或隐私系统的执行测试。阈值固定5，累计数值按指定日求和，故意不模拟厂商的完整不同 goal type、宽限期、图表与收费规则。

| 测试 | 结果 |
| --- | --- |
| 已记录6大于等于阈值5，先前截止安全 | PASS |
| 将历史同一记录6改为4，先前截止变红 | PASS |
| 再将历史记录修回6，恢复抽象安全判定 | PASS |
| 重复写入相同标识，不产生第二条记录 | PASS |
| 撤销数据来源授权后，禁止抽象新导入 | PASS |
| 撤销授权后，原有历史记录仍在 | PASS |
| 将目标标记归档，不等于清空历史 | PASS |
| 显式本地清空后，抽象记录集合为空 | PASS |

复算脚本：

```python
from dataclasses import dataclass, field

@dataclass
class ToyGoal:
    threshold: int = 5
    points: dict = field(default_factory=dict)
    source_authorized: bool = True
    active: bool = True

    def put(self, key, day, value):
        self.points[key] = (day, value)

    def observed(self, day):
        return sum(value for date, value in self.points.values() if date <= day)

    def red(self, day):
        return self.observed(day) < self.threshold

    def import_point(self, key, day, value):
        if not self.source_authorized:
            return False
        self.put(key, day, value)
        return True

checks = []
g = ToyGoal()
g.put("a", 1, 6)
checks.append(not g.red(1))
g.put("a", 1, 4)
checks.append(g.red(1))
g.put("a", 1, 6)
checks.append(not g.red(1))
g.put("a", 1, 6)
checks.append(len(g.points) == 1 and g.observed(1) == 6)
g.source_authorized = False
checks.append(not g.import_point("b", 2, 3))
checks.append(g.observed(2) == 6)
g.active = False
checks.append(not g.active and len(g.points) == 1)
g.points.clear()
checks.append(len(g.points) == 0)
assert len(checks) == 8 and all(checks)
print("8/8 PASS")
```

抽象状态模型的恢复安全仅是重算结果，不意味着厂商已经撤销真实收费或退回资金。撤销授权后历史仍存的规则与官方 YNAB 条款相容，但该测试没有证明真实服务器的数据删除行为。

## 5. 候选风险与零费用方法储备

MKT029-R1：历史数据修正触发既有截止点重新评估，错误计费或错误警报风险。候选控制：事件时间、接收时间、来源、修正前后值和重新评估范围分开记录；在未来模型中使用可回放的合成版本事件。
MKT029-R2：自动数据源覆盖手工纠正。候选控制：单一来源权威与冲突日志，源头纠正、幂等键、可见的历史版本。
MKT029-R3：七日退出约束与紧急安全需要冲突。候选控制：未来人生辅助系统必须保留即时暂停、拒绝建议、人工纠错及紧急撤权；不得自动产生经济惩罚。
MKT029-R4：No-Excuses Mode 可能在健康突变、事故和不可抗力下造成不合理后果。候选控制：保留硬性生存和安全底线，允许无条件停止自动决策。
MKT029-R5：公开图表即使隐藏原始数据，也可能泄漏行为模式。候选控制：敏感目标默认私有，单独检查统计图、共享链接和第三方缓存。
MKT029-R6：连接器撤权、目标归档、账户删除、支付记录与备份删除不同步。候选控制：分别列出授权、采集、存储、派生、导出、备份和法律保留状态，不能以一个“已删除”标志覆盖全部。
以上均是原则性候选，不预设唯一人生效用权重，不进入个人产品开发。

## 6. E 当日只读治理核对

已读取本日 E002、E003 及 F001，确认 E 当日已完成跨轨实质检查，本轮避免重复新建 E004。远端主线新增 R155 与 R156 两组方法研究，均保留冻结先行、源码、机器收据及独立 B 方法记录。R155 75个人工 Bass 世界，60个正创新率世界的三阶初始销量导数可反演，15个零创新率世界不可辨；B 独立 Taylor 方法逐行复核 75/75，检测非线性项缺失的48个突变案例。R156 96个人工资本积累世界，B 的变换变量方法 96/96 精确一致；凹函数模型42个非稳态世界可在理想初始流与加速度下反演，AK 家族不能凭同一观测分离储蓄与折旧。均是内部 E1，非真人 E2 或历史 E3。

直接查询 R156 最新科学报告提交 `dbbcbd3f56df8c16142de3f72e6b68bcffeec6d8` 的 Actions head_sha，返回0项；新方法 CI 未验收。R155 历史家电发货数据侦察发现1960至1985年26个年度数据的“出货量”与“首次采用人数”不一致，原始行尚未取得，不能充作 R155 历史 E3。original239 v7.8 仍有154条 provisional itemwise audit open，内部 schema/date 仍指向 v7.6/2026-10-24，登记为元数据滞后；本轮未改索引。R136 冻结负对照未通过与缺完整 CSV 仍开放。未执行全仓冻结哈希核验，不宣称全仓协议无变化；本轮未修改任何 R、E、F、TH、C、A、B 文件或冻结协议。

## 7. F 本周专题状态

2026-W43 F001 已归档，覆盖人工否决权、最小数据与解释。本轮只追加 MKT029 候选风险，避免同周重复 F 专题。下一周 F002 建议以授权撤回与衍生数据生命周期为专题，特别对照 Beeminder 的连接器撤权保留历史、退出等待、账户删除、备份和付款记录；仅公开标准与原则性方法，不接入真实敏感数据。

## 8. 公开来源与证据等级

S1 Beeminder 官方 API，2026-10-25访问：https://api.beeminder.com/
S2 官方历史越线说明：https://help.beeminder.com/article/13-when-do-derailments-happen
S3 官方纠错说明：https://help.beeminder.com/article/39-how-do-i-fix-incorrect-data
S4 官方扣费与申诉：https://help.beeminder.com/article/17-what-happens-when-i-derail
S5 官方 No-Excuses Mode：https://help.beeminder.com/article/360-what-is-no-excuses-mode
S6 官方七日目标退出：https://help.beeminder.com/article/44-how-do-i-quit-a-goal
S7 官方账户删除与保留：https://help.beeminder.com/article/48-how-do-i-delete-my-account
S8 官方目标可见性：https://help.beeminder.com/article/102-privacy
S9 官方隐私条款及 YNAB 撤权：https://www.beeminder.com/terms
S10 官方费用说明，标记2026-03-06更新：https://help.beeminder.com/article/19-how-much-does-beeminder-cost
S11 Bhattacharya et al. (2015), NBER Working Paper 21406：https://www.nber.org/papers/w21406
S12 Carrera et al. (2019/2021), NBER Working Paper 26161：https://www.nber.org/papers/w26161
S13 Himmler et al. (2019), AEJ Applied Economics 11(2)：https://pubs.aeaweb.org/doi/10.1257/app.20170288
S14 前序 MKT001：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/market/MKT001_BEEMINDER_BUFFER_RATCHET_API_2026-10-24.md
S15 E003：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/operations/E003_R136_FROZEN_NEGATIVE_CONTROL_INCIDENT_DELTA_2026-10-25.md
S16 F001：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md

证据分级：官方产品帮助、API、条款为 MARKET_E1_VENDOR_DOCUMENTED，可能随产品变更；8项本地测试为 EXPLORATORY_TOY_MODEL_8_PASS；三篇独立行为研究仅支持各自实验环境的承诺方法研究，非 Beeminder 效果验证。无真实 API、收费、真实敏感数据、真实世界预测校准、外部产品安全验证。主动新增费用0，账户整体账单及 GitHub 免费额度未独立核验。

## 9. 下一项具体研究

MKT030 优先研究 Beeminder 目标公开图表的隐私泄漏边界与 API 的 `secret`/`datapublic` 字段，检查“数据点私有但图形公开”的推断风险；若文档没有新增证据，转向 Dcider 的偏好记录与结果反馈机制。E 按日只读，F 下周推进 F002。R 系列全部完成后才归纳分类，之后模型熔炼。
