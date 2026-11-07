# Henrich 2004 与同期评论的竞争机制审读：高阶惩罚可观察性

track: theory
run_date: 2026-11-07 (Asia/Singapore)
target_key: (theory,Henrich2004-plus-Possajennikov2004,10.1016/S0167-2681(03)00094-5+10.1016/S0167-2681(03)00111-2,higher-order-punishment-observability)
observed_head: 998c933852ea4ed0883afb73fdb448e6222c911e
status: PRIMARY_SPECIFIED_SECTIONS_READ; COMPETING_ORIGINAL_COMMENT_READ; NO_EMPIRICAL_REPLICATION

## 原始来源和实际范围
Joseph Henrich (2004), Cultural group selection, coevolutionary processes and large-scale cooperation, Journal of Economic Behavior & Organization 53(1):3–35, DOI https://doi.org/10.1016/S0167-2681(03)00094-5 。直接读取作者刊前排印版第23–26页，特别是第6.3节第24–26页；第6.4节第26页开头。原始开放文件 https://coevolution.fas.harvard.edu/sites/g/files/omnuum5841/files/culture_cognition_coevol_lab/files/henrich_2004.pdf 。
Alex Possajennikov (2004), Comment on “cultural group selection, coevolutionary processes and large-scale cooperation” by Joseph Henrich, DOI https://doi.org/10.1016/S0167-2681(03)00111-2 。同一PDF的独立Discussion，第1–4页，重点第2–4页；该PDF随后还含其他作者评论与回复，不能把整份PDF视为Henrich单篇文章。
本轮直接核对的是原始论文及同期原始学术评论，未直接读取Henrich & Boyd (2001) 的完整原始模型或评论后作者回复。

## 机制与关键竞争解释
Henrich第6.3节提出：当合作常见且违约稀少时，不执行高阶惩罚的短期收益优势随惩罚阶数上升而缩小；若从众传递的强度对各阶均足够稳定，微弱的从众偏好也可能在某个高阶压过收益偏向模仿，之后通过逐级惩罚维持低阶惩罚与合作。原文是援引Henrich & Boyd (2001)的理论结果；本轮没有重新证明原始模型定理。

Possajennikov同期评论提出直接竞争条件：越高阶的惩罚事件越罕见，观察到相应行为并模仿的机会也可能减少。若从众传递强度随惩罚阶数衰减，收益差缩小不足以单独保证高阶惩罚稳定。原作者论证中从众强度跨阶的假设因此需要实证或独立模型支持。

可操作的理论辨别：设阶数k的收益差绝对值为d_k，从众维持力为s_k。原论证依赖存在某阶使s_k>d_k；仅有d_k趋近0不能推出该条件，除非约束s_k的衰减。构造性逻辑反例：d_k=2^(-k)，s_k=4^(-k) 时对所有k>=1都有s_k<d_k。此例只否定从“收益差递减”单独推出“终有从众占优”的推理；不等于对原作者完整动力学模型的反驳，也不证明这些函数符合真实心理机制。

另一项识别边界：评论指出合作行动可能由处罚威慑或模仿产生；仅凭行为合作率无法区分内化的利他偏好、策略性服从和规范压力。群体形成过程和群体稳定性也未由Price恒等式自动识别。

## 证据类型与适用范围
原文为数学/演化理论论证与引用既有实验；评论是原始学术批评；上述指数例为构造性逻辑反例。没有直接真人行为检验、历史数据检验或预测效果。适用范围为群体规范传递、惩罚链与群体间差异的理论识别。外推到跨文化、跨时代的具体社会必须另外估计惩罚事件的可见性、学习机制和群体形成过程。
与TH188从众/同质性识别、TH200互惠、TH217文化人口规模原著主题区分；此记录聚焦高阶惩罚可观察性这一同期竞争批评，不新增项目级融合。
未读：Henrich第6.4节余下及后续章节、Henrich & Boyd 2001原始模型全文、同期其他评论和作者逐项回复。

C当日已完成2026-11-07 C013；D本周已完成2026-11-02 D003。R073与PESEN v0.1冻结不变。独立数学程序测试NOT_RUN；真人/历史验证NOT_RUN；CI NOT_RUN；新增收费0；账单状态NOT_VERIFIED。
