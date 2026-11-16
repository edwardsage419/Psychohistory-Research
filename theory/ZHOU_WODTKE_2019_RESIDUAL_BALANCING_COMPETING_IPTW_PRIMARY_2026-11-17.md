# Zhou 与 Wodtke：残差平衡作为纵向逆概率加权的竞争方法

track: theory
run_date: 2026-11-17 Asia/Singapore
observed_head: e8f5e70a2ec6d2a8a5d9a0c16abcb97fc767af32
target_key: (theory,arxiv:1807.10869,2019-03-29-version,conditional-residual-moment-versus-treatment-density)
status: PARTIAL
source: https://arxiv.org/abs/1807.10869
source_version: arXiv HTML 显示 2019-03-29 稿本，初始提交 2018-07-28；本轮未核最终期刊版 DOI
evidence_type: original author manuscript, methodological derivation, not independent causal validation

## 阅读范围
直接阅读作者公开英文稿的摘要、§1、§2及§3.1，核查公式(1)至(13)与对应文字。§3.2以后、模拟数值表、实证应用及最终出版版本尚未系统阅读。

## 独立竞争机制
Robins、Hernán、Brumback (2000) 的 IPTW 需要估计每期处理分配条件概率或密度。Zhou 与 Wodtke 提出先估计处理后混杂变量的条件均值，再构造残差，使用熵平衡寻找权重，使残差与未来处理、既往处理及混杂历史的选定函数在加权样本中满足矩约束。§3.1 式(11)至(13)给出理论动机。它避免直接拟合连续处理的完整条件密度，但仍依赖残差模型与平衡函数选择。

设 r_t=g(X_t)-E[g(X_t)|X_{<t},D_{<t}]。理想加权伪总体满足 E*[r_t h(X_{<t},D_{1:T})]=0，对适当函数 h 成立。实际有限维矩约束只检验所选择的 g,h；即使所有已选样本矩为零，也不能推出任意未选函数的条件独立。这个区分是本轮的逻辑审查，不能视为作者实验结果。

## 与已有档案去重
既有 C014 (2026-11-08) 已完整记录 Robins et al. (2000) pp.555–560 的纵向权重、删失、正值性及附录算术。既有 theory/ROBINS_HERNAN_BRUMBACK_2000_TIME_DEPENDENT_CONFOUNDING_PRIMARY_SCOPE_2026-11-17.md 记录 pp.550–554。本轮没有复算 C014，也没有新增 C 编号。新增价值限于 Zhou 与 Wodtke 的独立竞争估计策略及有限矩约束的识别边界。

## 适用范围与不可识别性
原稿应用例子涉及竞选负面广告和战争公众支持；它们的经验结论本轮尚未审查。残差平衡仍需一致性、序贯可交换性、正值性及充分的模型/矩条件。潜在未测混杂、确定性决策路径、错误时间戳、测量误差与干扰不会因为样本平衡自动消失。其声称的效率及稳健性优势须依赖后续模拟和独立实证核验，当前标记 NOT_VERIFIED。未来个人决策 C 研究只能借鉴方法；不使用真实个人资料，也不确定人生目标权重。

## C、D与科学边界
C 2026-11-17：目录 C014 已有同类纵向因果成果；本轮增加独立竞争方法的理论储备，正式 C 当日新验收未确认。D 2026-W47：D005 迁移专题存在，独立数据可比性验收未确认。R 科学验收关闭 0。R073 与 PESEN v0.1 保持冻结。
Program tests NOT_RUN; real behavior validation NOT_RUN; CI NOT_RUN; billing NOT_VERIFIED; no paid resources or CI triggered.

## 下一步
核读 §3.2 至结论的熵优化目标、可行性、仿真设计和实证数据来源；检查权重平衡是否存在不可行或近正值性失败的具体反例。若无独立证据，转向欠覆盖历史或人类学原著。
