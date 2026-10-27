# F003 派生决策记忆的引用证据、语义校验与人工纠错
日期：2026-10-28。第44周额外独立专题；F002授权撤销生命周期已完成且保留原状态。性质：未来方法候选，非个人产品实现或规范授权。新增费用0，真实敏感数据0。

## 原始依据
英文开源项目Decision Journal固定提交 `95269a7db776ce74165c811b9195feed17049b3d` 的 `src/main/memory/validate.ts`、`store.ts`、`context.ts` 和单元测试。MKT085已确认：引文存在性通过子串匹配，模型声明的explicit/self-described可直接approved；否定反转的人工陈述可在引文真实存在时形成错误已批准记忆。17项合同检查通过。该结论是固定源码的条件性安全反例，未证实模型在真实运行中产生过此类错误。

方法参考：
* NIST AI RMF 1.0（2023-01-26）：https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
* NIST Privacy Framework（2020-01）：https://www.nist.gov/privacy-framework/privacy-framework
* UK ICO 关于AI个体权利及有意义人工审查：https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/how-do-we-ensure-individual-rights-in-our-ai-systems/

上述标准与监管指南提供风险管理和人工审查方法，不等于对特定产品的法律合规判定。

## 未来候选控制与可检验反例
1. 分开保存用户原始陈述、原文证据跨度、模型生成命题、模型版本、生成时间和用户确认状态。引用存在性、语义蕴含性、用户确认属于不同证据字段。
2. 任何模型生成的长期偏好、价值、身份或重要人生约束，初始为待确认。用户明确写入的原文可显示为原文事实，模型改写的命题仍需语义一致性检验及可撤销确认。不能把引文匹配自动当作用户认可命题。
3. 决策编辑、删除、时间状态变化后，派生记忆保留来源版本并进入重验；一个来源撤销时逐一核对剩余来源，不以旧缓存默认继续支持。撤销授权停止后续外发与使用，已发送给外部服务的历史数据按真实保留政策披露无法追溯撤回的边界。
4. 展示“不知道”“相互矛盾”“暂时不愿表态”状态；允许纠错、驳回、查看来源和申诉。保留审计记录时按最小化原则处理敏感内容，优先本地、短期保留及权限隔离。
5. 严格禁止模型基于一次情绪、单次行动或错误命题预设永久效用权重，重大决策不自动执行。候选评估用人工否定反转、时点变化、重复来源、来源删除、拒绝重提和迟到响应反例。

## 证据与边界
固定源码与人工反例为SOURCE_E1/SYNTHETIC_E1；候选控制为PROPOSAL_UNADOPTED；真实部署安全、误判率、跨文化公平、外部效果为UNKNOWN。没有接入真实个人数据、购买服务、调用模型API或提前实现个人决策产品。F004后续候选：跨文化偏好表达与拒绝自动画像的公平性测试；本周F003已满足一个额外专题增量。
