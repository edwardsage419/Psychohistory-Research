# F001 个人决策系统的人类否决权、解释与最小数据原则

研究周：2026-W43（2026-10-19 至 2026-10-25）；研究日期：2026-10-24。
track: privacy_safety；subflow: F；status: COMPLETE_BOUNDED_POLICY_METHOD_REVIEW。
observed_head_before_write: ac329619b39f4cba7d6679af1ea7e98f9e8b19d7
研究性质：公开规范和监管指导的原则性候选控制研究；没有个人敏感数据、法律意见、系统实现或独立用户实验。

## 本轮直接核查的公开原始资料

1. NIST AI Risk Management Framework 1.0，2023-01-26，官方入口：https://www.nist.gov/itl/ai-risk-management-framework 。已核对框架为自愿性风险管理指导，采用 Govern、Map、Measure、Manage 四项职能；NIST 页面于 2026-10-24 显示 1.0 正在修订，后续应跟踪版本。
2. NIST AI RMF Core，官方条目：https://airc.nist.gov/airmf-resources/airmf/5-sec-core/ 。已核对 Map 3.5 明确要求界定、评估并记录人类监督流程；Map 5 涉及个人与群体影响，Manage 涉及持续监测和风险处理。
3. NIST Privacy Framework 1.0，2020 年发布，官方：https://www.nist.gov/privacy-framework/privacy-framework 。官方框架将隐私管理分为 Identify-P、Govern-P、Control-P、Communicate-P、Protect-P，属于自愿性风险治理工具。
4. 英国信息专员办公室 ICO，自动化决策及画像权利官方指南，2026-10-24 访问：https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/rights-related-to-automated-decision-making-including-profiling/ 。指南强调在法律或类似重大影响的全自动决策场景下，应有相关法律基础、告知、人工干预、争议渠道及准确性检查。其具体法律义务取决于适用法域与事实。
5. ICO 人工监督解释，2026-10-24 访问：https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/how-do-we-ensure-individual-rights-in-our-ai-systems/ 。人工参与需要真正具备改变建议的权限、能力与信息，机械点击确认可能构成自动化偏差；本文将其作为跨领域设计警示，不能推定英国法律适用于所有个人使用场景。
6. ICO Human review 审计指南，2026-10-24 访问：https://ico.org.uk/for-organisations/advice-and-services/audits/data-protection-audit-framework/toolkits/artificial-intelligence/human-review/ 。审查建议包含人工覆核记录、重新复审、反对自动建议的能力和针对误导输入的测试。

## 对未来心理史学决策基准线的候选控制

F001-C1 人类最终控制：模型输出限定为建议和情景说明。健康、工作、关系、投资等重大选择由未来使用者自主批准。默认不进行自动支付、医疗、法律、财务交易或账户变更。
F001-C2 拒绝与撤销：用户可拒绝建议、暂停模型、修改或撤销数据授权；撤销后不得再读取被撤销的数据源。实现前需要明确本地缓存、衍生数据与删除传播的技术边界。
F001-C3 解释和不确定性：每条重大建议应给出证据时间、输入类别、模型版本、关键假设、预测区间、竞争方案、未知和可能失效条件。缺乏数据时允许拒绝排序。
F001-C4 最小采集与用途隔离：未来先建立数据字段清单与用途映射，只收集实现已获同意目标所需的信息；将健康、财务、关系及第三人资料分类隔离，默认优先本地处理和最短合理保留。
F001-C5 决策审计日志：区分模型建议、用户选择和事后结果。记录撤回或覆核时，禁止把用户拒绝建议自动标记为“非理性”；必须允许用户更改偏好。
F001-C6 风险分级：高不可逆性、低可观测性、低预测置信度或涉及第三方权利时，提升人工审查要求；不能用统一的目标分数覆盖硬性安全底线。
F001-C7 监督有效性测试：未来在无真实个人数据的合成场景中，设置故意错误的输入和明显不适当的建议，检查用户是否有足够信息识别、否决和记录原因。

## 风险登记

F001-R1 自动化偏差：模型呈现数值高精度可能让使用者过度信任。候选控制：不确定性、来源与反例展示、人工拒绝路径。
F001-R2 数据二次用途：跨生活领域拼接可导致敏感推断及第三方隐私泄露。候选控制：按目的隔离、细粒度授权、最小化保留。
F001-R3 目标锁定：系统可能将某一时期的偏好固化，压制未来价值变化。候选控制：可修改偏好、保留多目标偏序与不排序选项。
F001-R4 伪解释：漂亮的语言解释可能与实际计算路径不一致。候选控制：要求绑定具体模型、输入版本、可复算评分与证据级别。
F001-R5 法域误用：将英国 ICO 的合规条款直接解释成全球通用法律。候选控制：仅作研究参考，部署前另行核实适用法域。
F001-R6 外部成本与服务依赖：安全控制若依赖收费 API 或商业隐私服务则违反项目零新增费用。候选控制：先采用公开标准、离线文档和可审计开源方案；不得提前部署。

## 科学证据、限制与验收

来源等级：STANDARDS_PRIMARY_DOCUMENTATION 和 REGULATOR_GUIDANCE，属于规范性与方法证据；不对应 R 系列真人 E2、历史 E3，也不构成这些候选控制已被验证有效。
实际完成：原始公开框架与 ICO 指南的有限页面核查、七项候选控制、六项风险记录、后续验证问题。
未完成：法规逐条法律意见、系统威胁建模、用户研究、任何数据接入、代码实现、实证效果验证。
billing_checked: 仅公开免费文献与现有工具；新增费用 0；ci_status: NOT_RUN。
next_action: F002 研究本地优先、授权撤回与衍生数据删除的生命周期模型，优先 NIST Privacy Framework 与公开隐私工程论文；本周已完成 F001，无需重复。
