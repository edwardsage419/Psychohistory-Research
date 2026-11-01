# MKT209: Noom NCT04797169 事前登记、主动数字对照与30个月公开结果的证据边界

track: market
subflow: 真实商业产品机制与客观结果研究
run_date_utc: 2026-11-01T22:20Z
local_date: 2026-11-02 Asia/Singapore
target_key: (market,Noom-Health-vs-Noom-Digital-Health,NCT04797169-2021-registry+2022-protocol+2025-results,prospective-registration-active-control-long-term-inference)
observed_main_before_write: f144119d873ce5ee765388ab39b3398a1d378451
status: COMPLETE_BOUNDED_SOURCE_REVIEW
market_evidence: MARKET-E2_DIRECT_RANDOMIZED_REGISTRY_RESULTS_WITH_LIMITATIONS
independent_outcome_replication: NOT_VERIFIED
clinicaltrials_original_api_and_version_history: BLOCKED_ACCESS
full_statistical_analysis_plan_and_primary_p_value: NOT_VERIFIED
participant_level_data: NOT_ACCESSED
product_runtime: NOT_RUN
new_R_E2_E3: 0
ci_status: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE
sensitive_personal_data: NOT_ACCESSED

## 研究问题及相对MKT208的新增证据

MKT208讨论NCT06666842（2026年发表，公开登记晚于完成）与NCT03865342（2020年发表，公开登记晚于完成）。本轮发现另一项直接研究Noom产品的独立随机分组试验NCT04797169，具备研究开始前公开登记、主动数字对照、30个月计划随访及2025年公布的汇总结果。其受试者、研究版本、对照和主要结局与MKT208不同，不重复计数为此前两项试验的复现。

2021年3月10日首次提交登记，3月15日首次公开，3月22日实际研究开始；2024年5月4日完成，2025年8月11日结果首次公开。登记时序来自多个转录ClinicalTrials.gov的英文镜像；官方ClinicalTrials.gov API和原始历史版本在本轮工具中无法直接访问。此时序支持该试验的公开登记早于开始，不证明登记后全部版本与原始统计分析计划完全一致。2022年8月12日发表的JMIR研究方案晚于2021年3月入组，不能单独充当入组前冻结的完整分析计划。

## 产品版本与对照机制

研究在600人中随机分配Noom Health（302人）与Noom Digital Health（298人），年龄18至60岁、BMI大于27、英语使用者且对Noom有兴趣。研究者在Icahn School of Medicine at Mount Sinai主持，Noom参与合作与资助，方案作者包括Noom员工，研究不是无商业关系的外部复现。

两组均可记录食物和体重，接受饮食运动建议、教育内容。Noom Health另提供教练互动、群体支持、额外日志选项及每日分发的课程；数字对照以每周课程和简化日志为主。两组都有主动干预，故此比较更接近额外教练及组合功能的增量效应，不能推断Noom相对完全不用工具的效果，也无法单独识别教练因果贡献。

研究方案说明第7至12个月干预组仍有每周教练联系，因此30个月随访中“第6个月后全部服务停止”的说法不成立。方案公开了预定的分段潜变量增长曲线、6及30个月体重主要目标、缺失值MAR及MNAR敏感性计划、预设的异质性检验。完整登记版本历史与最终统计报告尚未核对。

## 2025年登记结果：原始汇总与有限算术

登记镜像公布各时间点体重均值（单位磅）：

| 时间 | Noom Health | Noom Digital Health |
| --- | ---: | ---: |
| 基线 | 210.1 | 211.7 |
| 6个月 | 199.4 | 204.6 |
| 30个月 | 197.2 | 201.6 |

仅对这些公开均值作十进制算术，Health基线至6个月为负10.7磅，Digital为负7.1磅，两个均值差值之差为负3.6磅；基线至30个月分别为负12.9和负10.1磅，差值之差为负2.8磅。此为**各时间点横截面均值的描述性相减**，可能存在不同时间点样本组成，不能视为同一批个体的平均变化、ITT因果估计、统计显著性或正式模型系数。

登记结果的“Population”注明只包括参加访问并提供数据者。当前可访问镜像未完整提供每个主要时间点的分母、置信区间、组间检验p值及原始缺失值敏感性分析。12个月完成状态220/302和222/298，合计442/600，约73.7%；这属于12个月完成指标，不能替代30个月留存率。研究记录的30个月体重使用参与者自有体重秤，由研究人员通过视频通话协助记录；测量独立性强于纯App自报，但未统一校准体重秤，也不是临床标准仪器测量。

6个月应用功能使用比例平均38.4%（Health）和17.9%（Digital），两组功能集合不同，不能直接解释为同一功能的同口径依从性提升。基线和30个月还记录饮食、心理状态、生活质量等自报量表，公开镜像没有证明这些指标具有独立因果改善。

## 科学结论、证据等级与局限

NCT04797169为直接商业产品随机试验的已发布登记汇总结果，分类MARKET-E2，且登记时序较MKT208两项研究更有利于评估前瞻性。方案在2022年正式发表，研究开始于2021年，故方案发表先后和登记先后需分别核对。

现有公开均值提示两组体重均有下降，Health组观察到更低的后期均值。无法从当前可见表格确认30个月的ITT差异、统计显著性、主要终点按原计划分析是否通过，或长期净福利。不能把相减所得负2.8磅描述为经随机化识别的教练因果效应。需进一步核对原始ClinicalTrials.gov版本历史、结果模块完整分母和统计比较、2022方案与2025结果的一致性、潜在完整论文及独立外部团队复现。

研究不使用用户私人健康信息，所有数值均来自公开研究的群体汇总。没有注册Noom、使用付费产品或采购论文。

## E每日科研治理只读增量

已确认2026-11-02的E167为实质只读审计COMPLETE，F010在2026-W45已COMPLETE；本轮没有新增E或F编号。最新R/B新增R257 S53 original225来源绑定审计，报告文件blob db8f1cd83e8541e82617cc8fe283dced199d2a63：225行来源、八个凸世界200行精确目标及梯度、S53代码与基线收据绑定，在V8执行一项正例及六项变异拒绝；这是非盲态内部人工E1，历史B盲态顺序FAIL仍开放，完整原生Node CLI NOT_RUN，正式S53验收PARTIAL。R333至R340组合P0的完整原生执行及八工作流强制调用继续未闭合。

本轮实际读取12个开放Codex PR，全部Draft且未合并。PR #3 head 97d5f74df5d84916917db943156120f08144f445，相对main f144119d873ce5ee765388ab39b3398a1d378451 比较diverged，main独有1113提交，PR独有1提交。其数学检查候选没有在PR中完成来源认证；R/B新增来源绑定审计也未自动合并PR或修复历史盲态失败。PR #1的原比较器错误接受仍须正式处理。无自动合并或跨轨文件修改。

原239队列blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，crosswalk blob 36f24235901172642c46853298aebb421f1a3552，均与既有审计一致；文件级净关闭0。上次直接核验154项（P0 27，P1 82，P2 45）只作有时间范围的历史快照。R073及PESEN v0.1冻结不变，R系列科研优先。

## F每周专题只读状态

F010关于价值权重型AI决策辅助的人类实质控制、数据生命周期及评分透明度已在本周完成。此轮Noom试验只补充研究方法上的数据缺失和用户授权边界；不新增F阶段，不做安全部署或读取敏感信息。

## 实际来源与访问范围（2026-11-02）

1. 2022年公开的原作者试验方案全文，DOI 10.2196/37541：https://www.researchprotocols.org/2022/8/e37541 。已审阅研究设计、主动对照、7至12个月教练接触、随机分配、缺失处理和统计计划。
2. NCT04797169公开登记结果镜像：https://findtrial.co/trial/NCT04797169 。已审阅2021登记与2025结果时间、600人分组、主要体重均值、12个月完成状态、6个月功能使用及不良事件。
3. NCT04797169第二登记镜像：https://ichgcp.net/clinical-trials-registry/NCT04797169 。核对2021登记日期、2024完成日期、2025结果更新及两组干预。
4. NCT04797169另一结果转录：https://hipa.ai/condition/obesity/updates/trial-results-posted-nct04797169-2025-08-11 。交叉核对公开均值及2025年8月11日结果发布日期。
5. 官方登记入口：https://clinicaltrials.gov/study/NCT04797169 。本轮官方API和历史版本访问失败，未把镜像内容声称为独立读取的官方原始字节。
6. GitHub R/B来源绑定审计：research/validation/R257_S53_ORIGINAL225_SOURCE_LINK_AUDIT_20261101T2147Z.md
7. GitHub E167与F010已归档文件、三个轨道短交接及开放PR元数据。

## 费用、执行与下一步

新增收费操作0；没有主动触发GitHub Actions。账户账单和免费额度未独立核验；因此任何可能计费的CI仍保持NOT_RUN。该报告仅是公开资料与少量十进制描述算术，未运行Noom产品、原始参与者数据或完整统计模型。

下一步优先尝试从免费官方登记历史记录确认2021版主要终点及2025结果的分母、缺失处理、组间统计检验。若原始资料继续不可访问，转向其他公开原始结果更完整的个人决策辅助产品。E轨继续R333至R340真实原生组合门及强制接入、PR #3来源与盲态边界；F本周只读。