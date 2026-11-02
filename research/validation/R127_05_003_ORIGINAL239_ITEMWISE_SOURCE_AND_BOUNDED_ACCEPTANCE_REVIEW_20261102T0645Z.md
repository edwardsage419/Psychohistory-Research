# R127 / original239 05-003 逐项原始来源与有限科研验收审查

track: R+B
subflow: original239 P0 itemwise scientific adjudication
run_date_utc: 2026-11-02T06:45Z
observed_main_before_write: fe76e28cb581284d48826b89299b2bd569c3b903
target_key: (R+B,05-003/R127,2026-10-20 prescore freeze,original-source-and-bounded-acceptance)
status: COMPLETE_BOUNDED_ITEMWISE_SCIENTIFIC_REVIEW / GOVERNANCE_QUEUE_UPDATE_PENDING
proposed_disposition: ACCEPT_BOUNDED_PRIMARY_COORDINATION_GAME_MECHANISM_AND_PUBLISHED_AGGREGATES
scope: 1990 published Treatment A minimum-effort payoff, original session marginals, exact static equilibrium and constructed 2x2 comparison
evidence_grade: PRIMARY_PUBLISHED_HUMAN_AGGREGATE_PLUS_INTERNAL_NONBLIND_EXACT_MATHEMATICS
new_real_human_individual_E2_predictions: 0
new_historical_E3_predictions: 0
external_team_replication: NOT_RUN
CI_new: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE

## 1. 来源与冻结边界

主来源：Van Huyck, Battalio & Beil (1990), *Tacit Coordination Games, Strategic Uncertainty, and Coordination Failure*, American Economic Review 80(1):234–248。高校收藏的15页原刊扫描：https://econweb.ucsd.edu/~jandreoni/Econ264/papers/Van%20Huyck%20et%20al%20AER%201990.pdf 。本轮直接查看扫描的印刷240与241页Table 2图像，逐场核对首末轮7级行动频数。其余原刊页、原支付参数的来源深度沿用既有R127已记录的阅读范围，未在本轮重新逐页检查。

计算前冻结：protocols/R127_VAN_HUYCK_1990_MINIMUM_EFFORT_ORIGINAL_TABLE2_AND_2X2_RISK_SELECTION_FREEZE_2026-10-20.md，main Git blob 4734ede5133701d622acfda76c4f9474bf660b21。原R127 README Git blob 56dd79e793460ae74dfddd9d173b60cedbbdca96；原有限验收JSON Git blob 3aa5ed67f4d38f91474352627451e46500cde210；历史CI收据 Git blob 55bdf82b9e7869c63d46aa4f76ba6bc672dddecb。历史CI run 39348775741 的成功结论取自原有收据，本轮没有重新查询全部CI jobs或重新运行原程序。

original239交叉索引 docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v7.8_2026-10-25.json，Git blob 36f24235901172642c46853298aebb421f1a3552，含239行。05-003 当前仍是 PROVISIONAL_PRIMARY_README_LINK，manual_primary_mapping_and_acceptance_review=PENDING。实际待核CSV Git blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，本轮按内容解析154条，其中P0 27、P1 82、P2 45。不能因为R127历史README写CLOSED_BOUNDED而自动认定original239已逐项采纳。

## 2. 本轮独立算术与反证边界

在连接器侧JavaScript V8独立执行，不导入R127 Python源码；无随机种子。直接将已冻结的七场首末轮7级人数作为输入，检查14个边际向量各自人数守恒。七场人数16、16、14、15、16、16、14，总计107；首轮努力7有33，首轮努力1有2，末轮努力1有77，与原刊Table 2图像及历史记录一致。

独立计算七场各自的整数运输边际严格界并相加：首末努力不同人数89至107；努力7转努力1人数10至33；其他努力转入努力1人数75至77。所有界限依赖同一场次首末参与者身份稳定，且不同指标的极值不必由同一潜在配对实现。此处重算闭式界，未重复执行既有独立最小费用流程序；界限可达性仍由先前归档研究支持。个人身份转移与因果学习参数均不可识别。

独立按十分之一美元整数单位复算原Treatment A支付 u_i=6/10+(2/10)min(e)-(1/10)e_i。穷举n=2,3,4时共2793个行动向量、75117个个人候选偏离付款，严格纯Nash各为7个且均为同努力行动。另穷举a,b,c,d各取0至5的1296个自构对称二人矩阵，双严格对角Nash有225个，其中收益占优与风险占优相反30个，风险判据并列55个。后一类矩阵是本项目数学构造，不是1990原实验的额外真人场次。原实验多人maximin安全选择不得冒称为Harsanyi–Selten两人风险占优定理。

本轮执行结果：上述守恒、精确整数枚举及闭式边际计算均PASS；未重新执行R127 Python unittest、完整原始源码或GitHub Actions。与先前R127完整数值验证属于同研究团队的非盲交叉计算，不构成外部团队独立复现。

## 3. 逐项科学裁定与剩余缺口

针对original239 05-003 Coordination Game的有限目标，已有来源足以支持：原作者1990最低努力收益结构、多个严格纯均衡、收益占优与最坏情形安全标准的分离、原刊七场107人首末边际，以及本项目二人严格双Nash的有限数学反例。故本轮提出 ACCEPT_BOUNDED_PRIMARY_COORDINATION_GAME_MECHANISM_AND_PUBLISHED_AGGREGATES 的科学建议，明确限定在上述机制及已发表聚合观察。建议E治理轨独立审阅来源映射、历史冻结先后与机器收据后，决定是否将05-003从provisional队列转为已完成有限逐项验收。R轨没有修改docs索引或待核队列，本轮队列净减少0项。

不得随此裁定提升的事项：原作者107人逐人原始时序未取得；新增真人E2预测0；历史E3预测0；学习动力学、个体信念与均衡选择因果机制未识别；Cooper1990全文与Harsanyi–Selten1988原书未直接核阅；独立外部团队复现NOT_RUN。原1990论文发表汇总属于真人观测的来源证据，不能被标成新开展的个体样本外评分。

## 4. A公开数据侦察：实际取得的候选二进制身份

核对Dal Bó & Fréchette (2011) AER DOI 10.1257/aer.101.1.411，以及第三方作者Fabian Dvorak的公开stratEst仓库 fdvorak/stratEst，当前读取版本master最近提交 c05aae64eadc8f5e2bbf8b98b14b884f5b393be7。连接器实际取得 data/DF2011.rda 的base64内容，解码3298字节，头部425a6839为bzip2格式，Git blob 52e216b02e1a7ab7fb1a6e335b5f7e2ef6b7f5a0。该仓库DESCRIPTION标注stratEst 1.1.8、GPL-3；R/data_DF2011.R文档标注7358行和treatment/id/game/period/choice/other.choice等字段。旧0.1.2文档使用supergame/cooperation/other_cooperation命名，版本语义必须固定。

该文件是已取得二进制候选，尚未解析RData内部行、唯一身份、对手配对、场次边界、原作者与第三方再分发权利差异。R073冻结协议要求按同处理5场训练、整场留出并使用t-1/t-2合法历史；现有DF2011六字段没有显式session标识。R073原冻结测试适配资格UNKNOWN，不能把game/supergame直接当作独立session，也不能称已做跨实验评分。候选文件没有写入公开仓库。

## 5. 去重、费用和下一步

已查12个开放Codex PR，#1/#3仍open且仅为R257 S53待审代码；本次R127逐项审查没有复制其实现。R272正式生产验收P0仍开放，R333至R340复合调用路径仍待验证；R257 S53历史盲态失败仍保留。R073/PESEN v0.1冻结。E1、E2、E3与MARKET严格隔离。

无购买、收费API、额外算力、CI或Actions触发；实际账户费用与剩余免费额度NOT_VERIFIED。

next: E轨对05-003开展独立逐项治理裁定；R轨优先在完整可信仓库上执行R272只读preimage-first原生验证并审查生产强制调用；A轨在许可允许时解析DF2011二进制、验证treatment×id×game×period唯一性和配对语义，之后再决定是否设计与R073冻结模型兼容的独立外部评分。