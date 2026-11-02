# MKT217: Statin Choice 两项直接随机试验与 Cochrane 决策质量证据交叉审查

track: market
subflow: 真实决策辅助产品机制、独立效果与失败证据
run_date_utc: 2026-11-02
local_date: 2026-11-02 Asia/Singapore
target_key: (market,Statin-Choice,2007+2010-direct-RCT-and-2024-Cochrane,knowledge-values-congruence-versus-adherence-and-regret)
observed_main_before_write: aae1ec5fcf66c581825f01df1155b4331e3f2719
status: COMPLETE_BOUNDED_ORIGINAL_TRIAL_AND_SYSTEMATIC_REVIEW
evidence_grade: MARKET-E2_DIRECT_PRODUCT_RCTS_AND_ADJACENT_SYSTEMATIC_REVIEW
original_individual_data_reanalysis: NOT_RUN
current_production_algorithm_runtime: NOT_RUN
current_version_RCT_equivalence: NOT_VERIFIED
long_term_personal_welfare: NOT_VERIFIED
R_E2_E3_new: 0
CI: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE
sensitive_personal_data: NOT_ACCESSED

## 研究选择与去重

MKT203 已讨论 Dcider 价值评分和相邻医疗决策辅助综述；MKT210 讨论 DecisionTwin 推荐不一致与未校准置信度。本轮转向可辨认的真实产品 Statin Choice，直接核对两项独立招募的随机试验，并使用 2024 Cochrane 209 项随机试验综述限定可推广的效果层次。与 MKT211 至 MKT216 的活动、症状和承诺结果目标不同。本轮没有开发个人决策产品，也没有复算 R/B 数学。

## 一、实际产品机制及版本边界

Mayo Clinic 的 Statin Choice 面向临床会诊，帮助患者与临床人员讨论是否使用他汀类药物降低心血管风险。官方公开入口 https://shareddecisions.mayoclinic.org/statindecisionaid/ 明确提示只能在临床会诊中使用。开发者实施说明 https://carethatfits.org/statin-choice-tool-kit/ 提供工作流、演示及电子病历集成资料。官网可公开查看入口，未核实机构集成价格或生产数据保存/第三方传输政策。

2007 年试验使用的是历史纸质一页式版本。研究者输入患者心血管风险因素，将十年基线风险粗分为 10%、20%、50% 三档，展示服药后绝对风险下降、药物不利因素及是否现在决定、稍后决定或与他人讨论的选择。这里的“个性化”仍存在风险分档近似，不能将其视为完全精确的个体风险预测。当前线上版本与 2007 年纸质版本不同；未获得当前生产源代码、模型参数、风险校准报告及真实使用日志。官方公开页面可确认产品存在及用途，当前价格与隐私实际处理为 UNKNOWN。

可确认的数据流：临床人员/患者提供风险背景 → 风险类别或计算结果及选项收益损害可视化 → 临床对话和价值澄清 → 选择、推迟或继续讨论。完整现代生产算法和用户长期反馈循环未披露，未实机运行。

## 二、2007 年直接产品集群随机试验

Weymiller et al., 2007, DOI 10.1001/archinte.167.10.1076。21 名内分泌科临床人员参与，98 名糖尿病患者；决策辅助 n=52，对照普通胆固醇说明册 n=46。集群/2×2 因子随机设计；研究结果包含即时知识、风险理解、决策冲突和三个月后自报服药。

直接原文结果：
* 9 分知识题，干预组较对照组多 2.4 分，95% CI 1.5 至 3.3。
* 对基线心血管风险估计准确性的 OR 22.4，95% CI 5.9 至 85.6；对药物绝对风险下降估计准确性的 OR 6.7，95% CI 2.2 至 19.7。
* 决策冲突 100 分量表组间差值为负 10.6，95% CI 负 15.4 至负 5.9。
* 三个月时，服药子样本中干预组 2/33、对照组 6/29 自报过去一周至少漏服一剂。该分母仅限随访时正在服药的参与者，服药行为为自报，不能作为全随机人群的客观依从性因果估计。
* 单中心、样本小、临床人员集群、风险基线不平衡、受试者教育程度偏高及历史版本限制外推。

2007 年论文的试验注册号为 NCT00217061，本轮未核官方注册历史与完整原始数据，注册先后证据为 PARTIAL。

## 三、2010 年第二项直接产品随机试验

Mann et al., Patient Education and Counseling, 2010, DOI 10.1016/j.pec.2009.10.008。另一项城市初级保健随机试验，150 名糖尿病患者，基线与三个月、六个月电话随访。

公开原始作者/期刊摘要：无他汀时风险估计更准确 OR 1.9，95% CI 1.0 至 3.8；服用他汀时风险估计 OR 1.4，95% CI 0.7 至 2.8。三个月和六个月的他汀依从性均未发现组间差异。其结论支持风险沟通与决策过程改善，未证明药物依从性改善。全文和原始参与者数据未获取，不能进一步审计失访、随机化执行及预注册终点。

两项试验不是同一个随机样本。2007 年自报服药子样本的有利方向与 2010 年无依从性差异可以并存；不可把 2007 年结果宣传成经第二项试验重复确认的长期服药改善。

## 四、2024 Cochrane 独立系统综述：对决策结果的证据边界

Stacey et al., 2024-01-29, DOI 10.1002/14651858.CD001431.pub6。检索至 2022 年 3 月，汇总 209 项随机试验、107,698 人、71 类医疗决定。它覆盖多个决策辅助工具，不能作为 Statin Choice 当前版本的单独产品试验，也不应把其中与上述试验重叠的研究再次当成独立样本。

* 知情价值与最终选择一致性：21 项试验、9,377 人，RR 1.75，95% CI 1.44 至 2.13；GRADE 中等确定性。
* 决策知识：107 项试验、25,492 人，100 分量表 MD +11.90，95% CI 10.60 至 13.19；高确定性。
* 正确认知风险：25 项试验、7,796 人，RR 1.94，95% CI 1.61 至 2.34。
* 决策后悔：22 项试验、3,707 人，MD 负 1.23，95% CI 负 3.05 至 +0.59；未发现整体显著差异。高确定性证据支持该综述覆盖条件下没有确认的平均后悔差异，不等于保证所有用户都不会后悔。
* 综述指出依从性、成本资源后果及偏好关联的实际健康结果仍缺充分证据；综述明确未找到直接测量 preference-linked health outcomes 的研究。

这组结果为“更懂选项、更清楚价值、更参与决策”提供真实随机试验证据；“更遵从建议、更少后悔、更长寿、更幸福”必须单独验证。对未来个人决策研究，值得事先分开测量信息理解、价值选择一致性、行为落实、长期实际福利及负面影响，不能将某一项提升为整体人生决策质量。

## 五、独立性、商业与安全

两项 Statin Choice 试验均为产品研究团队或合作研究者开展的原始随机试验，2010 年试验属于独立招募场景，但并非完全与开发者无关的外部团队复现。Cochrane 是跨产品的系统综述，独立证据等级高于单一厂商宣传，仍受到各试验测量、偏倚和干预异质性约束。

官网显示公开可访问工具入口；2019 年开发者实施材料称该工具 freely available。当前机构电子病历集成收费、数据存储、访问控制、撤销、删除、备份保留及算法源代码许可均未核实。历史研究工具的临床目的与风险信息不可用于个人医疗建议。实际账户、个人健康信息、真实产品交互、付费行为及数据安全测试均 NOT_RUN。

## 六、E 与 F 跨轨只读协调

E167 已在本地 2026-11-02 完成当日实质审计。本轮新核对 main aae1ec5fcf66c581825f01df1155b4331e3f2719；较 MKT216 6e40ac752af3e30de73cd79fae1c52122acb4049 新增 R272 预影像先验只读门候选和 TH209 理论提交。R272 最新报告明确：本地 Python 3.13.5 三模式自测通过，发现历史收据字节身份覆盖缺口并增加候选门；完整可信 checkout 原生执行、隔离再生成及生产强制调用均 NOT_RUN，P0 OPEN。R333 至 R340 八份原生产 workflow 的复合门强制调用仍 0/8，真实原生组合验收未完成。无 R E2/E3 新增。

2026-11-02 直接读取 GitHub pulls collection：12 个 open、12 个 Draft、merged_at 全 null；PR #3 head 97d5f74df5d84916917db943156120f08144f445 与 main 比较 diverged，main 独有 1147 提交，PR 独有 1 提交，不能从提交距离断言 merge conflict。PR #12 仍为 Draft，属于 R266 S62 另一目标。R257 S53 来源身份/历史盲态问题继续开放。原239队列 blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，crosswalk blob 36f24235901172642c46853298aebb421f1a3552 均未变化；最近直接登记 154 项，P0 27、P1 82、P2 45；文件级净减少 0，未进行新的逐项 CSV 科研验收。

F010 已完成本周价值权重 AI、人类实质控制与个人数据生命周期专题。本轮只读引用，不新增 F 编号。Statin Choice 强调会诊中的人类对话，但实际临床自主权、跨文化可理解性、数据删除范围没有在本轮做真实安全测试。

## 七、证据等级、费用和后续

MARKET-E1：官方产品用途、历史纸质版本机制、公开实施资料。MARKET-E2：2007/2010 两项直接产品 RCT 与 2024 跨产品系统综述。MARKET-E3：没有可确认的长期人生福利或当前产品效果。MARKET 证据不得替换 R 系列 E1/E2/E3。

本轮没有触发 GitHub Actions；当前基线 HEAD combined statuses 0、所查询 PR-triggered workflow runs 0，不能推断所有类型 CI 均为 0。账户实际 GitHub 账单及免费额度 NOT_VERIFIED，故跳过任何可能计费执行。没有付费产品/API、真实个人敏感数据、协议修改、PR 合并或跨轨写入。

下一高价值商业任务：寻找真正以非医疗人生选择为对象、能客观观察选择后的后果且具有预先注册比较组的工具；若无，则审查开源规划产品的实际预测校准。E 等待 R272 可信 checkout 原生复验与 mandatory caller 证据，R333 至 R340 组合门仍优先。R073、PESEN v0.1 冻结保持；R 模型全部完成后再统一分类，最后有条件熔炼。

## 本轮实际读取的免费英文来源

1. Mayo Statin Choice 官方入口: https://shareddecisions.mayoclinic.org/statindecisionaid/
2. Mayo 开发者实施资料: https://carethatfits.org/statin-choice-tool-kit/
3. 开发者关于免费可访问及工作流障碍的说明（2019）: https://carethatfits.org/2019/06/10/supporting-implementation-of-shared-decision-making-for-statin-therapy-initiation-in-primary-care/
4. Weymiller et al. (2007) 原始期刊全文: https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/486843
5. Mann et al. (2010) PubMed 原始作者摘要: https://pubmed.ncbi.nlm.nih.gov/19959322/
6. Stacey et al. (2024) Cochrane 原始综述: https://www.cochrane.org/evidence/CD001431_patient-decision-aids-help-people-who-are-facing-decisions-about-health-treatment-or-screening
7. Cochrane 2024 全文: https://pmc.ncbi.nlm.nih.gov/articles/PMC10823577
8. 本仓库 docs/PROJECT_WORKFLOW_REQUIREMENTS_V2_2026-10-24.md 与 docs/RESEARCH_SYNC_WORKFLOW_2026-10-15.md

提交与 Git blob 身份在实际写入后单独核验，不在报告中预填。
