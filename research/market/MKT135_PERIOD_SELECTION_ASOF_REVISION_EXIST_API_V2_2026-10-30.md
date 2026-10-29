# MKT135 分期选择敏感性、历史修订时间与 Exist API v2 机制审查

日期：2026-10-30 Asia/Singapore。目标键：(market,MKT135,none,time-varying-selection-gamma-asof-label-revision-Exist-v2)。状态：COMPLETE_BOUNDED_ARTIFICIAL_E1。仅为未来候选方法储备，继续先完成全部 R 系列，后统一归纳，最后模型熔炼。无真实个人数据。

## 1. 独立人工精确实验

与 MKT134 的单期结果相关缺失互补，本轮把观察机制拆成 A、B 两个等权时期。A 的可见联合质量 P(S=1,Y=1)=1/16、P(S=1,Y=0)=3/16；B 对调为3/16、1/16。两期被观察比例均为1/4，可见阳性率分别1/4、3/4。未观察结果的真实组成未知。

每期分别给定入样率比 r_t=P(S=1|Y=1,t)/P(S=1|Y=0,t) 的假设区间 [1/Gamma_t,Gamma_t]。由 q_t=P(Y=1|S=1,t) 得 p_t=q_t/[r_t(1-q_t)+q_t]，与物理可行区间 [P(S=1,Y=1),1-P(S=1,Y=0)] 相交。以下为精确可行界，非置信区间：

| Gamma_A, Gamma_B | A 总体阳性率 | B 总体阳性率 | 两期等权总体均值 |
| --- | --- | --- | --- |
| 2,2 | [1/7,2/5] | [3/5,6/7] | [13/35,22/35] |
| 1,3 | [1/4,1/4] | [1/2,9/10] | [3/8,23/40] |
| 3,1 | [1/10,1/2] | [3/4,3/4] | [17/40,5/8] |

将两期可见记录直接合并，阳性比例为1/2。如果未经论证地给合并数据指定 Gamma=1，就会错误地得到总体1/2的点结论。分期 Gamma=(1,3) 时，同一可见资料允许总体3/8至23/40。Gamma 是分析者的假设，不能从数据自动推断。两期等权是假设的目标总体定义；现实人口比例不同必须另给权重。

第二项人工实验为三条预测记录 X、Y、Z，分别有事件发生时间、预测生成时间及标签版本可见时间。X预测1/4、最初标签0在时点2可见、时点4改为1；Y预测3/4、最初标签1在时点2可见、时点5改为0；Z预测1/2、时点3首次标签1。使用时点3可见的三个标签，Brier平均为1/8；使用时点6最新修订的三个标签，Brier平均为11/24，差1/3。时点1无任何已可见标签，正确状态为无可评分样本。

两个评分均可成为不同预先声明评价目标：as-of 当时可见标签，或后来裁定的最终标签。后者用于还原时点3模型训练输入时会发生未来信息泄漏。真实标签修正是否更接近真值，仍需独立裁定。事件发生时间不能替代记录可用时间。

归档程序 research/market/mkt135_period_selection_asof_revision_20261030.js，标准JavaScript BigInt精确有理数，独立V8实际执行19项断言和7项非法输入负例全部通过；尚未运行归档文件的原生Node CLI。人工E1，新增真人E2=0、历史E3=0、外部独立复现=0。此处没有统计抽样误差或真实选择率估计。

## 2. Exist 产品官方机制深读

2026-10-29 UTC 公开英文官方资料核验，未注册账户、申请令牌或调用受限接口。

* 输入：日粒度 activity、mood、sleep、finance、health、custom 等属性，既可来自服务同步，也可手动记录。API v2 以 name、date、value 表示日值；同一属性同一天的更新是覆盖已有总值，最多35条批量写入。非空值不能改回 null。数据类型只进行宽泛校验，来源端须自行保障语义正确。
* 状态与算法：官方相关性接口返回 period、offset、value、p、stars、文字解释，支持同日及相邻日相关分析。官方知识库称至少三周有效数据后计算相关性，按周更新。相关系数及星级属于描述性关联，不能当因果效应、未来人生最优策略或独立预测校准证据。
* 反馈及修正：官方 FAQ 称多数服务定期刷新当日及上一周数据；API 属性更新接口允许按历史日期覆盖旧值。官方所查文档没有给出可查询的完整历史版本链或每次覆盖的记录可用时间证明，因此不能直接依赖其单日 date/value 恢复旧时点的训练视图。这是接口文档范围的审计结论，不能据此断言其内部数据库从不保存版本。
* 权限与隐私：API v2 OAuth2 按属性组分别申请读写 scope，写入前需取得 attribute ownership，同一属性只有一个写入服务拥有者；用户可改变所有者，多个OAuth客户端的令牌可分别撤销。API读取受 scope 约束。真实权限实现、后台访问控制及删除证明未独立审计。
* 解释性：可返回相关系数、p值、星级及自然语言解释；未发现可独立复算的完整相关性选择、重复检验校正、长期决策收益评估材料。
* 费用：2026-10-30公开定价为个人每月USD 6.99或每年USD 62.90，30天试用。试用注册页面要求支付卡信息，不符合本项目绝对零新增费用操作约束。商业账户另行定价。
* 产品边界：官方文档支持上述接口语义和价格；用户改善、隐私执行与安全性能仍为未独立验证范围。没有将厂商叙述提升为科研E2/E3。

官方来源：
https://developer.exist.io/reference/writing_data/
https://developer.exist.io/reference/attributes/
https://developer.exist.io/reference/correlations/
https://developer.exist.io/reference/authentication/oauth2/
https://developer.exist.io/reference/attribute_ownership/
https://developer.exist.io/guide/migrating/
https://kb.exist.io/article/55-will-exist-find-correlations-across-multiple-days
https://kb.exist.io/article/18-how-long-does-it-take-to-find-correlations
https://exist.io/
https://exist.io/signup/

独立方法背景：Todem et al. (2010), Semiparametric regression models and sensitivity analysis of longitudinal data with non-random dropouts, DOI 10.1111/j.1467-9574.2009.00435.x；El Lahib et al. (2026), Temporal Leakage in Search-Engine Date-Filtered Web Retrieval, https://arxiv.org/abs/2602.00758 。文献用于解释方法风险，以上精确数值来自本轮人工设定和程序，不归因于论文实证。

## 3. 候选控制、局限和后续

候选记录字段：event_at、first_observed_at、revision_at、source_version、model_frozen_at、evaluation_cutoff、sampling_stratum、Gamma_assumption、selection_unknown、final_adjudication_status。预测复盘需要分别报告当时可用数据得分和最终裁定得分，留存更正轨迹。高风险建议在区间跨越决策阈值或历史输入无法重建时弃权，不预设唯一人生效用权重。

未调用计费API、未购买产品/论文、未使用云GPU/付费CI或新增订阅。GitHub账单与免费额度尚未独立核验。下一项MKT136：带迟到更正的时间窗校准与可用性截止测试，优先寻找独立免费原始方法文献。