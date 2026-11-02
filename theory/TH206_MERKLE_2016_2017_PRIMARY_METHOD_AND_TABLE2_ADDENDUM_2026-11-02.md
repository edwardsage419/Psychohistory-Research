# TH206 补记：Merkle 2016与2017原始IRT模型、选择机制和表格人数审计

track: theory
subflow: pure_theory
run_date: 2026-11-02 (Asia/Singapore)
observed_head: 4e04047fe75597d22a0dfd0f1ace5f9b94eee71d
target_key: (theory,MerkleSteyversMellersTetlock2016+2017,2015-online-first/2016-journal+2017-author-manuscript,IRT_forecast_time_model_selection_MNAR_unidimensionality_table2_count)
status: PRIMARY_SOURCE_AUDIT_COMPLETE_BOUNDED; TABLE2_DISCREPANCY_OPEN; REAL_DATA_REESTIMATION_NOT_RUN
scope: TH206方法补记，非新TH，非R轨模型拟合或科学验收。

## 原始来源及本轮实际阅读范围

[A] Edgar C. Merkle, Mark Steyvers, Barbara Mellers, Philip E. Tetlock (2016), *Item Response Models of Probability Judgments: Application to a Geopolitical Forecasting Tournament*, *Decision* 3(1):1–19, DOI 10.1037/dec0000032。作者所在大学保存的开放Online First版（封面注明2015-04-06先行发表），https://faculty.wharton.upenn.edu/wp-content/uploads/2015/07/2015---item-response-models-of-probabability-judgments_1.pdf 。直接审读PDF内部印刷pp2–7、10–12的模型、样本、分割验证及Table 1；正文第4–6页Eq(3)–(23)及第7页Figure 1重点核验。期刊最终排版逐字比较NOT_RUN；版权属作者/出版社，未复制原文至仓库。

[A] Edgar C. Merkle, Mark Steyvers, Barbara Mellers, Philip E. Tetlock (2017), *A Neglected Dimension of Good Forecasting Judgment: The Questions We Choose Also Matter*, *International Journal of Forecasting* 33(4):817–832, DOI 10.1016/j.ijforecast.2017.04.002。作者本人公开手稿 https://ecmerkle.github.io/pub/MerkleSteyversMellersTetlock2017.pdf ，直接审读手稿印刷pp2–10、11–16、18–21的Models、Data、Unidimensionality、Simple Example、Full Data、Simulation、Missingness Mechanisms；第4页Eq(4)–(8)、第9页DETECT、第10页Table 1/2已目视核验。作者手稿与期刊最终排版是否完全相同NOT_VERIFIED，下面的一人差异限定在此作者公开稿。

[B] Hauenstein, Thomas, Illingworth, Dougherty (2025), *Rethinking the Role of Teams and Training in Geopolitical Forecasting*, *Psychological Science* 36(1):3–18, DOI 10.1177/09567976241266481。作为既有TH206的竞争重分析背景，本轮只对照该原作公开正文的IRT模型介绍，未重新估计2025 M1–M7；其补充PDF、OSF/JAGS代码仍NOT_READ。

## 新增原始方法事实及竞争解释

1. 2016年原作使用1593名参与者与199题的竞赛资料背景，实际IRT研究限制为几乎完成133道二元题的241人，约占1593人的15.13%。作者在印刷p6承认，筛选高参与率可减轻MAR问题，同时产生选择偏差。其“out-of-sample”实验随机隐藏同一数据集30%的已报告预测，并保留每位预测者和每道题的部分记录用于训练；原刊p7 Figure 1的probit预测R²为IRT 0.43、仅题目0.15、仅个人0.05。这属于同资料内部留出预测，不等于跨年代、跨事件或独立队伍外部验证。p10–11 Table 1的20次重采样，训练与测试**各自同名指标**Spearman相关：Brier 0.48、标准化Brier 0.59、IRT 0.73；0.73的测试目标仍为IRT估计，不可直接转述为对真实结局的预测相关。
2. 2016年模型对probit转换后预测用题目难度的指数时间曲线；Eq(6)显示b_{2j}下标，但正文p5–6明确说明实际拟合共享一个b2，允许各题b0/b1不同。2017年作者公开稿p4 Eq(5)改用**线性时间项**：μ_ij=β_0j+β_1j t_ij+λ_(j,1)θ_(a,i)。作者明确解释此为对2016年指数曲线的简化。两版公式及参数先验不同，不能直接当作相同实现。
3. 2017年Eq(6)–(8)对选择指标d_ij（选题=1）建Bernoulli/probit方程：probit(P(d_ij=1))=β_(0,J+j)+λ_(J+j,1)θ_(a,i)+λ_(J+j,2)θ_(r,i)。预测能力θ_a与参与倾向θ_r是两个潜变量，且作者施加对角协方差、固定各一项载荷为1的识别约束；2017年对比MAR与MNAR时的潜在能力定义受模型限制。该论文使用775人、157个二元题，仅保留每人每题首次预测，忽略原实验团队/训练条件，极端0和1改为0.001与0.999。
4. 单维性诊断明确有反证。2017年手稿p9对选题的跨四年DETECT最大2.3（两簇，作者称强多维），限制单年后为0.58（中度）；对预测值为0.72（三簇）。因跨年进入、退出和题目构成改变，单一稳定能力因子在整个历史时期并非已证明的事实。2017年手稿p16–17指出退出与稀疏作答是不同缺失机制，单年子样本中的低频预测者有时得到不同方向的修正。
5. 2017年p18–19的100次模拟有2次不收敛，98次可比较。仅第一年选题信息对四年“预测+选题”能力估计的平均相关为0.24（IQR 0.20–0.28）；两边**共享选题数据**。改用只依赖预测的MAR能力估计为参照时，平均相关降至0.12（IQR 0.08–0.16），98次中97次为正。该模拟支持选题有有限信息，且对“额外能力”的解释受共用信息、共同样本与潜变量有效性约束。作者p20也承认错设MNAR机制可能比MAR产生更大偏差。

## 新发现：2017年作者公开稿Table 2的样本人数相差1

手稿p9正文称四道例题至少作答一题的预测者为**771/775**。手稿p10 Table 2的13种非零作答模式频数（按原表顺序）：
`1,1,1,15,11,8,64,173,1,87,31,34,345`。
标准库整数求和为**772**，与正文771差1。第10页原始表格图像已直接核对，排除纯文本提取的频数字符误读。

逐题按表格模式重新计数，四题作答人数分别为**671、595、454、453**。除以772，四舍五入至两位小数分别为**0.87、0.77、0.59、0.59**，与同页Table 1四题公布的作答率相容。若除以771，四舍五入也得到相同两位数，因此Table 1无法裁决哪一个总人数正确。手稿未给出可独立核查的个体原始记录，本轮无法判定正文771、某个Table 2频数、或样本过滤口径何者有误；不得擅自更正为772，也不得声称期刊正式版存在同一错误。

## 证据边界与对R的局部理论关联

竞争解释一：参与频率和选题结构携带真实预测能力信息。解释二：持续参与、题目可及性、时间机会、激励、淘汰和团队制度同时影响选题与已观测成绩。解释三：两者并存。现有IRT关联和内部重抽样无法唯一裁决因果路径。2017年潜在能力因子与2025年M2/M7条件效应亦属不同模型与样本选择，不可把模型间系数变化等同实验因果效应变化。

个人层：概率判断及领域专长；群体层：团队信息共享；制度层：开放题目、激励、退出与评分；历史层：四年参与结构变动。仅做局部机制联系。未启动R拟合、真实因果估计、历史预测或跨模型融合。R073、PESEN v0.1冻结；R E1/E2/E3及MARKET证据等级无新增。

## 实际检查、C/D、下一步

Python标准库执行：Table 2的13项整数求和=772，四列逐题计数=671/595/454/453，2016样本比241/1593=15.13%，2017模拟有效重复98/100，相关系数均值0.24与0.12差0.12；以上仅算术和文献内部一致性检查，非原始真人数据复算。原始IRT重估、补充材料和独立预测均NOT_RUN。

C010：2026-11-02 COMPLETE，本轮只读；D003：2026-W45于2026-11-02 COMPLETE，本轮只读。没有新C/D编号。新增收费操作0；实际账户计费NOT_VERIFIED；未主动运行收费风险未确认的CI。

下一步：如能免费获得2017年正式发表版及原始作答模式表，确认一人差异是否沿用；再读取2025年补充方法PDF中的先验/交叉载荷/缺失假设。随后转向当前弱覆盖的独立学科原著，避免持续扩展预测评分微专题。全部R完成后统一分类，再有条件熔炼。
