# MKT214：juli 两项主动对照随机试验的留存、效果与商业证据边界

track: market
subflow: 商业产品机制、真实用户效果与负面证据
run_date_utc: 2026-11-02
local_date: 2026-11-02 Asia/Singapore
target_key: (market,juli,2024-depression-RCT-ISRCTN12329547+2024-asthma-RCT-ISRCTN87679686,per-protocol-versus-ITT+attrition+quality-of-life+conflict-of-interest)
baseline_main: 1596f0efe9252ff9f263f5d87bf04603e62d3b6d
status: COMPLETE_BOUNDED_PRIMARY_TRIAL_AND_OFFICIAL_PRODUCT_POLICY_REVIEW
evidence_scope: MARKET-E2_TWO_DIRECT_RANDOMIZED_PRODUCT_TRIALS_WITH_ACTIVE_CONTROL_AND_HIGH_ATTRITION
raw_participant_reanalysis: NOT_RUN
trial_registry_original_history: NOT_VERIFIED
algorithm_native_execution: NOT_RUN
independent_external_team_replication: NOT_VERIFIED
new_R_E2_E3: 0
ci_status: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE

## 1. 选题与独立增量

MKT213 审阅 Sleepio 失眠干预对自报生活质量的效果及 NICE 独立评估。本轮转向真实个人量化产品 juli，同一产品在抑郁症状与哮喘两类人群中分别进行了随机试验。关注完整产品与仅每日情绪或症状记录的主动对照之间的增量、完整随机样本与完成随访者之间的选择差异，以及生产算法和真实决策改善是否可验证。两项试验的样本与疾病不同，研究团队及商业利益关系有重叠，不能把它们称为完全独立团队的跨疾病复现。

## 2. 用户输入、状态、建议、反馈和费用

2024 年发表的抑郁试验原始方法说明，juli 完整版提示用户每日按五档表情和情绪能量维度记录心情，允许记录自认重要的诱因；经手机及可穿戴设备被动取得睡眠、活动、锻炼、月经周期及心率变异性，展示与情绪的关联，并提供行为激活建议、服药提醒和正向情绪日记。主动对照版也每日提醒并记录情绪，故两组比较的是额外功能组合的增量，不能识别单个相关性、传感器或推荐算法的因果贡献。

2024 年哮喘试验描述症状、服药提醒、环境位置相关天气、花粉和空气污染等候选诱因，以及活动、睡眠、心率变异性展示与行为建议。用户输入目标及状态的完整生产数据结构、相关性调整规则、因果模型、推荐排序权重、模型版本和概率校准没有公开可复算的确认。研究没有运行 App 或读取真人健康资料。

2026-11-02 读取 juli.health 官方机构页面：为医疗机构提供按患者许可和不限人数许可两种方案；官方 providers 页面显示每月 25 美元起覆盖 10 名患者，许可证可由机构提供给患者免费使用。官方 pricing 页面称每名患者许可 30 天不活跃后释放。这里是机构采购报价及厂商机制说明，个人订阅费用、现时各地区实际可用性与长期服务承诺未独立核验；本项目未购买。

## 3. 抑郁症状随机试验，2024 年 6 月 7 日

Kandola 等，Digital Health，DOI 10.1177/20552076241260409，ISRCTN12329547。2021 年 5 月至 2023 年 1 月随机分配 908 人，8 周内比较完整版 juli 与有限功能注意力对照。第 2 周仍有评估者 662 人，完整第 8 周评估者 456 人，占随机样本 50.2%，失访 452 人。

主要论文采用完成随访者的 per-protocol 分析：8 周 PHQ-8 经基线调整组间系数为负 0.94 分，95% CI 负 1.87 至负 0.22，p=0.045；达到症状缓解的调整 OR 为 2.22，95% CI 1.45 至 3.39。论文同时明确：modified ITT 和 full ITT 的主要 PHQ-8 终点均未达到统计显著性；SF-12 健康相关生活质量与症状恶化的组间差异未被确认。研究将达到 MCID 及症状恶化列为事后新增终点，不能作为全部预注册终点。

论文指出分析由与公司没有财务利益冲突的统计人员完成，但多名作者是 juli Health 股东、创办人或顾问。原始受试者数据、ISRCTN 历史快照及原始预分析计划的独立版本核验仍未完成。

## 4. 哮喘随机试验，2024 年 4 月 29 日

Kandola 等，Journal of Medical Internet Research，DOI 10.2196/50855，ISRCTN87679686。2021 年 5 月至 2023 年 4 月随机分配 411 人，完整版 juli 204 人，主动对照 207 人。第 2 周 262 人仍提供结果，第 8 周 152 人，占随机样本 37.0%，失访 259 人。

完整随访者分组为干预 67 人、对照 85 人，显示完成随访后的分组比例不均衡。per-protocol 的第 8 周 ACT 经调整差异为正 1.91 分，95% CI 0.31 至 3.51，p=0.02；达到至少 3 分临床重要改善的 OR 为 2.38，95% CI 1.20 至 4.70。modified ITT 在纳入第 2 周有记录的 262 人并插补后，ACT 经调整差异为正 1.56 分，95% CI 0.32 至 2.79，p=0.01。两种分析均未显示 8 周缓解率或 SF-12 身体、心理生活质量的显著组间改善。

论文特别说明，完整 ITT 411 人的第 8 周原始结局并不完整，modified ITT 排除了第 2 周以前失访者；不能将 262 人的插补结果称为全部随机样本的直接观察。其作者、商业资助与抑郁试验存在重叠，统计分析由无该公司财务利益冲突的人员完成。个体原始数据仅称可向作者合理申请，未取得。

## 5. 两试验的交叉判断及不能推断的内容

共同点：完整产品包含被动传感器与主动记录、反馈、提醒及建议；主动对照保留部分记录与提醒；均在 8 周得到完成随访者的正向症状结果；主要结局来自自报量表；失访分别为 49.8% 与 63.0%；均未证实 SF-12 生活质量改善。两者不支持把相关性解释当作经过实验单独识别的因果机制，也不支持对整体人生决策净福利的外推。

差异：抑郁试验的完整随机样本 ITT 主要终点不显著，哮喘试验的 modified ITT 在插补后仍显示 ACT 改善。应分开报告，不应混合为单一成功率或将 908 与 411 人合并估计产品疗效。

公司官网声称“two independent rigorous clinical trials”及“proven to improve outcomes”。实际论文确有两项不同疾病的随机研究和与公司无财务利益的统计分析人员，但多名作者为同一公司的股东或创办人，资金及团队存在交叠。故厂商所谓 independent 不能自动升级为外部无利益团队复现。用户留存宣传中的行业平均和倍数也未获得独立验证。

## 6. F010 本周安全专题的只读对照

juli.health 官方隐私政策标明生效日 2022-10-06。政策列出健康数据、设备数据、环境地理数据、使用数据及第三方服务；部分数据可由用户选择连接。政策承诺依适用法律提供访问、更正、删除、可携带和撤回同意途径，但实际端到端删除与备份清除未测试。政策称去标识汇总数据可无限期保留，第三方处理和跨境传输可能存在。F010 已于本周完成，本轮只提供实际产品对照，无新增 F 编号或实际敏感数据读取。

## 7. E 只读增量与开放风险

2026-11-02 当天 E167 已完成实质审计。此次重新读取 main=1596f0efe9252ff9f263f5d87bf04603e62d3b6d、R272 新候选及 R333 至 R340 八份 workflow 的既有静态审计。R272 新增 fail-closed 独立收据候选报告，CPython 3.13.5 普通及优化模式各完成 1 正例和 11 变异拒绝，独立重建 576 行与 9 世界的归档字节；但完整真实仓库读取与生产强制调用 NOT_RUN，原生产生成器的 Python -O 假接受仍存在，P0 OPEN。R333 至 R340 的 0/8 强制调用缺口与完整原生执行缺口仍开放。

GitHub pulls 集合实际返回 12 个 open PR，全部 Draft、merged_at=null，最近更新均在 2026-10-29。PR #3 为独立 R257 S53 目标，main 相对其 head 独有 1136 个提交，PR 独有 1 个，来源身份与历史盲态问题未闭合；不得自动合并。original239 pending queue Git blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，crosswalk blob 36f24235901172642c46853298aebb421f1a3552，均与前轮一致，最近直接计数为 154 项、P0 27、P1 82、P2 45，文件级净减少 0。没有重算 B 轨科学数学，也没有改动共享索引、冻结协议或跨轨文件。

理论轨最新 TH207 是民族志原始资料时间线与档案证据审查，不升级 R E2/E3。F010 2026-W45 已 COMPLETE。R073、PESEN v0.1 维持 FROZEN。

## 8. 原始公开英文来源与实际访问边界

1. 抑郁 RCT 2024-06-07，PubMed 原始摘要及开放全文： https://pubmed.ncbi.nlm.nih.gov/38854919/ ，https://pmc.ncbi.nlm.nih.gov/articles/PMC11162123/ 。PMC 完整页曾返回正文片段，随后重访触发浏览器验证；主要结果、方法与统计边界由 PubMed 原始摘要和此前可读全文交叉支持。
2. 哮喘 RCT 2024-04-29，开放原始论文： https://www.jmir.org/2024/1/e50855 。
3. juli 官方产品机制及机构价格： https://www.juli.co/ ，https://www.juli.health/providers ，https://www.juli.health/pricing 。
4. juli 官方隐私政策（标注 2022-10-06）： https://www.juli.health/privacy-policy 。
5. 官方研究登记入口： https://www.isrctn.com/ISRCTN12329547 ，https://www.isrctn.com/ISRCTN87679686 。原始历史注册版本 NOT_VERIFIED。
6. 仓库已读：research/operations/E167_R269_ORIGINAL239_P0_SCOPE_AND_OPEN_PR_GOVERNANCE_2026-11-02.md；research/privacy_safety/F010_VALUES_AI_HUMAN_OVERRIDE_DATA_LIFECYCLE_2026-W45.md；research/validation/R272_P0_FAILCLOSED_INDEPENDENT_RECEIPT_CANDIDATE_20261102.md；research/validation/R333_R340_P0_EIGHT_WORKFLOW_CALLER_REACHABILITY_AUDIT_2026-11-02.md；docs/ORIGINAL_239_PENDING_154_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-25.csv。

next_action: 市场优先核对 juli 两个 ISRCTN 的原始注册时间和预先统计分析计划，或转向更少失访、具有客观长期结果的真实决策辅助产品；不为相同产品反复编号。E 只读追踪 R272 完整原生门及 R333 至 R340 强制调用，PR #3 独立验收。F010 本周只读。无新增费用、产品注册或 Actions 调度，账户实际账单及剩余免费额度 NOT_VERIFIED。
