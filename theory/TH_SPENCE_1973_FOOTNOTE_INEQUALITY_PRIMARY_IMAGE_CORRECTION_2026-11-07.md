# Spence (1973) 原刊脚注不等式方向核查及信息均衡边界

track: theory
subflow: original_theory
run_date: 2026-11-07 Asia/Shanghai
observed_head: 6f9bd182c7533514e04ba5cb540b077d0b8d3d0f
source: Michael Spence (1973), Job Market Signaling, Quarterly Journal of Economics 87(3):355–374, DOI 10.2307/1882010
source_link: https://competitionandappropriation.econ.ucla.edu/wp-content/uploads/sites/95/2017/08/Spence1973.pdf
source_type: university-hosted scan of published original journal pages, not author's later retrospective
reading_scope: printed pp. 356–365, especially p.365 footnote 1; source scan image of printed p.365 directly inspected; pp.366–374 not systematically audited in this run
status: COMPLETE (source reading and conditional algebraic check); PARTIAL (published erratum search and full paper)
ci_status: NOT_RUN
billing_checked: no paid API, CI or cloud computation invoked; actual billing NOT_VERIFIED

## 原刊第365页脚注的方向问题

作者设两类生产率为1与2；低生产率组I的教育成本为 a1*y，高生产率组II为 a2*y，且 a2<a1。雇主对教育阈值 y* 以上支付2，以下支付1。为了使组I选择0而组II选择y*，原刊脚注正确列出两项激励约束：

1 > 2 - a1*y*
2 - a2*y* > 1

由第一式严格推出 y*>1/a1；由第二式推出 y*<1/a2。因此联合条件为：

**1/a1 < y* < 1/a2**。

原刊印刷第365页脚注1却写为 **1/a2 < y* < 1/a1**。由于原文同页脚注8明确假设 a2<a1，印刷区间为空，与其上两项激励约束矛盾。这一处为**原刊疑似上下界颠倒的排印错误**；本轮未发现作者正式勘误，不能称为已获作者确认的erratum。原刊图像已直接核对，排除PDF纯文本提取造成的方向误识别。

例：a1=1，a2=0.5，y*=1.2，则 1<1.2<2，组I不模仿的净收入1大于2−1.2=0.8；组II选择教育的净收入2−0.6=1.4大于1。原刊脚注所写区间则要求2<y*<1，无解。

## 不影响正文的另一结论

若低生产率组人口占比为 q1，不发信号时统一工资为2−q1。高生产率组在分离均衡下净收入为2−a2*y*。存在一个令其比无信号时更好的分离均衡，需要选择 y*>1/a1 且 a2*y*<q1，因此必要且充分的存在条件为 **q1>a2/a1**（严格条件及上述线性成本模型）。例如 q1=0.7，a1=1，a2=0.5，y*=1.2，高生产率组净收入1.4大于无信号工资1.3。故原刊正文的存在条件仍与正确推导一致，脚注区间错误不自动推翻正文命题。

## 与 Akerlof (1970) 的竞争机制及证据边界

Akerlof (1970) 的示例为私人质量信息改变出售商品池并可能造成无交易；Spence (1973) 研究可付成本的可观察信号如何改变雇主信念、工资与申请者行为。Spence pp.359–360 的信息反馈均衡要求观察到的信号上的主观信念与实际雇佣后生产率分布一致。未观察到的信号水平可能缺乏可反驳资料，形成持续自我确认的非信息性资格门槛。pp.363–365 的模型在相同类型完全分离下存在多个 y*，更高教育门槛增加真实信号成本而不增加排序精度。

在现实中，教育同时可能增加生产率、传递信号或改变社会网络；仅凭学历工资差无法唯一识别信号收益。检验需观察事前能力、教育成本、真实生产率、招聘门槛及未被雇佣群体，并处理选择偏差。原著是理论模型，不构成真人实验或历史因果检验。原文对不可改变的群体特征有时代性用语，不能将其当作规范性分类建议。

## 限制及后续

算术检查仅证明指定两类型模型的内部一致性。未执行完整一般均衡计算、动态信念模拟、真人实验或外部验证。后续审读 pp.366–374 的 pooling、indices 与福利讨论，并核对是否存在正式勘误。当前不新增 TH 编号，不改变 R 冻结基线，不进入模型熔炼。
