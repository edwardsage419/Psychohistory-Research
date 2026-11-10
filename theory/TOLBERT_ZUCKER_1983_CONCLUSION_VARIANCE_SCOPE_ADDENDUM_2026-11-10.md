# Tolbert 与 Zucker（1983）原著第35至39页补读：方差反驳与历史测量限制

track: theory
subflow: primary reading / D cross-reference
run_date: 2026-11-10
observed_head: 25bcd51dd58bf0c245ae84c563406e679a966b5a
source: Pamela S. Tolbert and Lynne G. Zucker (1983), Institutional Sources of Change in the Formal Structure of Organizations: The Diffusion of Civil Service Reform, 1880–1935, Administrative Science Quarterly 28(1):22–39, DOI 10.2307/2392383.
source_links:
- https://sjbae.pbworks.com/w/file/fetch/45538952/tolbertandzucker.pdf
- https://ecommons.cornell.edu/entities/publication/65b24167-62ff-49ec-8689-74b63af6894f
evidence_scope: 开放原刊复刻PDF的可检索正文，直接核读印刷35至36页讨论与方法限制、37至39页参考文献；原始城市级数据未获取。对应前一份22至34页笔记的未读部分。
research_key: (theory,Tolbert-Zucker-1983,ASQ-28-1-35to39,variance-check-and-temporal-covariate-limits)
status: PARTIAL

## 原文新增证据与审计
1. 印刷35页 Table 3 后，作者明确提出并检查一个竞争解释：城市特征的跨期方差是否系统缩小，从而使晚期预测关系消失。作者据表3称各特征方差没有系统性下降。这一作者已做的反驳必须纳入原先“晚期显著性减弱可能只是城市趋同”候选解释的证据权重，不能忽略。注意其表3是各时期风险集合的描述统计，方差未系统缩小无法排除事件数减少、风险集合选择、协变量测量变化及未观测共同冲击。
2. 印刷35至36页作者承认并明确批评：使用研究期之后的城市横截面特征会产生时间错置，当前特征可能是改革的结果；横截面设计还会混淆早期与晚期采纳的不同机制。此项是作者明确的方法警告，不应误标为本轨首次发现。
3. 印刷35页作者提出可反驳的外推猜想：若扩散早期中断，可能是未取得制度合法性，早期预测变量会持续有效；作者同时明确指出可用教育创新资料不足以检验。该猜想属于作者理论外推，非该论文已经验证的历史事实。
4. 印刷36至39页为参考文献。未见独立新数据表或额外计量结果。不能把书目当成已读参考文献全文。

## 竞争解释与可证伪设计
观察对象为1880至1935年美国城市的正式文官制度采纳。合法性传播、州法强制、内部治理需求、政治竞争和风险集合动态选择均可产生扩散模式。对作者方差检查的条件性补充：样本方差稳定也不能推出风险系数跨期稳定，因为条件分布、未观测因素及事件数可变化。未来需要在可比历史协变量和完整事件时点下估计跨期交互，并报告风险集、事件数、效应区间及稳健性；实际执行与绩效另行测量。
D004能源统计的风电101.7 MW及太阳能164.1 MW未闭合残差与此论文不共享观测单位，不能用本论文解释。C015 2026-11-10已有归档，本轮无新C编号。R073、PESEN v0.1及证据等级保持冻结。

## 执行边界
work_performed: 直接补读指定原著剩余页码，区分作者已进行的方差反驳、作者承认的测量限制与作者未验证的外推猜想。
tests: NOT_RUN（无原始城市数据，未做计量复算）
ci_status: NOT_RUN
billing_checked: NOT_VERIFIED（未主动调用收费服务或CI）
blockers: 167城事件级数据及一致历史协变量缺失；作者外推猜想缺独立样本。
next_action: 轮换到弱覆盖的文化演化或认知人类学原著，避免制度扩散专题重复；如获城市级数据再验证事件风险模型。
