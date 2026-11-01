# F010: 价值权重型 AI 决策辅助的人类实质控制与个人数据生命周期

track: privacy_safety
subflow: F 每周独立高价值专题
week: 2026-W45 Asia/Singapore
run_date_utc: 2026-11-01
local_date: 2026-11-02 Asia/Singapore
target_key: (privacy_safety,values-based-AI-decision-aids,2026-W45-v1,meaningful-human-control-score-opacity-export-erasure)
baseline_main: d81f03e70ee7b65debfac2601f7a9f221b9cf559
status: COMPLETE_BOUNDED_PRIMARY_STANDARD_AND_PRODUCT_POLICY_REVIEW
real_personal_data: NOT_ACCESSED
real_product_deployment: NOT_RUN
actual_security_or_erasure_testing: NOT_RUN
new_R_E2_E3: 0
ci_status: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE

## 研究问题

用户预设价值权重、AI 生成选项及“价值一致性分数”可能帮助梳理选择，也可能通过未经校准的分数造成自动化偏见。对未来个人决策辅助系统，需要区分用户真正保有决定权、只是在界面上存在确认按钮、以及系统是否把未经核验的结果包装为客观结论。本专题只做安全和伦理方法储备，不构建产品，也不读取任何人的健康、财务或关系数据。

## 本周独立原始资料与具体发现

1. 英国信息专员办公室 ICO 的 AI 与数据保护指导明确指出，在涉及重大法律或类似重大影响的自动决策中，形式化人工点击不足以构成有意义的人工介入。审阅者需要有能力和权限改变结果，积极检查推荐及其输入，并警惕自动化偏见和难以解释的模型。其对 UK GDPR Article 22 的法律解释有特定适用条件，不能直接推定普通个人决策日志应用已经触发 Article 22。
2. 欧洲数据保护委员会 EDPB 的官方个人权利指南区分信息获取、更正、删除、限制处理、可携带、反对及某些纯自动重大决定的权利；这些权利的适用范围取决于处理依据和情境。不能把“账户删除”一句宣传等同于已经证明所有副本和衍生分析都被删除。
3. 美国 NIST 2023 年 AI RMF 1.0 是自愿风险管理框架，适用于记录治理、风险映射、测量和管理。它是方法来源，不能视为 Dcider 或未来项目已获得安全认证。
4. Dcider 2025-12-20 隐私政策披露用户价值权重、决策描述、选择结果及事后评分等处理内容；云端和 AI 服务商参与处理，操作日志最长90天，删除后备份最长30天，部分法律与业务保留例外。官方首页声称最终选择由用户负责，服务条款承认 AI 可能存在错误和偏见。以上是公开政策陈述，实际删除、权限和服务商行为未独立验证。

## 候选研究要求与可证伪条件

A. 用户控制。未来实验应能分别记录 AI 建议、用户独立初始判断、最终选择和覆盖原因；在撤去建议后测量独立判断能力。重要选择须保留拒绝、延后、修正权重及不使用 AI 的路径。不能把点击确认次数当作实质自主性的证据。

B. 分数解释。若系统给出数值排序，需保存用户权重版本、输入选项、模型版本、分数来源及未知项。测试权重小幅变化、选项重排、删除候选选项和时间推移是否产生无解释的排序变化。对未披露算法的产品只能记录待检，不能声称已经验证公平性或稳定性。

C. 数据最小化与撤销。将“停止新的 AI 处理”“停止第三方传输”“删除主数据库记录”“删除缓存和备份”“删除派生画像或摘要”“导出原始输入与权重版本”作为独立审计问题。删除完成应有可解释的范围、时限和例外记录，不能从一份操作回执推断所有复制品已经不可恢复。研究阶段禁止采集真实私人决策日志。

D. 结果真实性。决策日志由用户自报的“结果评分”只能证明其提交了一个评分。应独立标记主观满意度、客观行为、实际损失、第三方确认、因果效果和长期福利；不得以审计链真实性代替结果真实性。

E. 公平与跨文化。价值清单可能遗漏文化背景、家庭义务、关系承诺及非金钱目标。不同语言表述和文化环境的等价性需要独立测量；没有真人证据时保持 UNKNOWN。重要价值冲突应允许多个非支配选项，避免强制给出唯一人生最优解。

## 证据与限制

本周完成的是一次独立标准与真实产品政策交叉阅读，COMPLETE。F009 的 W44 研究覆盖见证与基础设施共同根问题，F010 聚焦人类自主性、价值评分和个人决策数据，目标与证据缺口不同。无新增人工安全阶段、模拟世界计数、真实应用安全测试或外部用户效果。未来系统安全合规、真实数据删除完成、法律适用性和公平性均 NOT_VERIFIED。任何候选设计均不提升为科学定律或已部署安全措施。

## 实际读取的免费英文原始来源

https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/how-do-we-ensure-individual-rights-in-our-ai-systems/
https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/how-do-we-ensure-fairness-in-ai/what-is-the-impact-of-article-22-of-the-uk-gdpr-on-fairness/
https://www.edpb.europa.eu/sme/be-compliant/respect-individuals-rights_en
https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
https://dcider.app/privacy
https://dcider.app/terms
https://dcider.app/

next_action: 本周专题已满足一次实质研究目标。后续仅只读跟踪独立新证据，优先由市场轨检索真实产品结果，避免继续扩展同一 F 编号或提前启动个人产品开发。R 主线、R073 与 PESEN v0.1 冻结不变。
