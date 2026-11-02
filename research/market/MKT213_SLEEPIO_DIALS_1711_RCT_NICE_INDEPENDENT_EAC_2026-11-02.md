# MKT213：Sleepio 数字化行为干预、真实生活质量结果与独立卫生技术评估

track: market
subflow: 商业产品机制与独立有效性研究
run_date_utc: 2026-11-02
local_date: 2026-11-02 Asia/Singapore
target_key: (market,Sleepio,DIALS-ISRCTN60530898-2018+NICE-HTG624-2022,patient-reported-welfare-versus-objective-clinical-outcomes+independent-economic-assessment)
baseline_main: 0642e84aacce75b568d9aeee2ed044f3391bc85e
status: COMPLETE_BOUNDED_PRIMARY_RCT_AND_INDEPENDENT_HTA_REVIEW
evidence_scope: MARKET-E2_DIRECT_RANDOMIZED_PRODUCT_TRIAL_WITH_SELF_REPORTED_FUNCTIONAL_WELLBEING; MARKET-E2_INDEPENDENT_EAC_METHOD_REPLICATION_OF_NONRANDOMIZED_RESOURCE_MODEL
raw_individual_data_reanalysis: NOT_RUN
trial_registry_historical_version: NOT_VERIFIED
product_algorithm_execution: NOT_RUN
new_R_E2_E3: 0
ci_status: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE

## 选题与去重

MKT211 和 MKT212 分别审阅 Fitbit 追踪及激励的活动步数变化，未证明长期健康或整体福利。本轮改为研究直接商业产品 Sleepio 对用户自报生活质量、心理健康和功能健康的随机试验，以及独立卫生技术评估机构对经济模型的重新计算。目标是区分可测中间指标、使用者重视的结果、长期保持、经济效果和因果外推。Sleepio 属于限定医疗问题的数字治疗，不能将结果直接转移到一般人生规划或 AI 决策辅助。

## 真实产品输入、状态、建议和反馈

Sleepio 由 Big Health 开发，提供网页与移动端六次自动化认知行为治疗课程。用户先完成入门问卷和睡眠评估，课程间记录睡眠日记。官方 FAQ 确认课程依据用户困难和进展定制，提供提醒、行为与认知技能、社区及知识库。官方 suitability 页面确认系统会依据每周进展及课程选择调整内容，包含睡眠限制等可能带来暂时白天嗜睡的措施，特定疾病和高风险职业需要额外医疗评估。

可核实状态输入为自报症状、问卷、睡眠日记和每周进展。完整生产个性化规则、参数、模型版本、预测概率校准和开放源码均未得到确认。不能把“个性化”推定为学习型 AI，也不能把课程推荐视为个人长期福利最优策略。

2026年 NHS Thames Valley 地区官方页面说明符合当地 GP 登记条件的居民可免费使用一年，属于有地域资格的机构覆盖权益，非全球免费价格。NICE 2022 年评估使用的每启动用户 £45 是当时卫生系统模型输入，不能当作2026年公开零售价格。实际个人订阅价格和开放自部署许可 NOT_VERIFIED，本轮未注册、购买或输入真实健康数据。

隐私：NHS 地区页面将 Big Health 描述为 Sleepio 平台数据控制者，官方 FAQ 声称数据托管于美国；完整2026删除、导出、第三方处理和备份时限没有完成原始政策逐项核对。产品适用性声明提示睡眠限制和夜间离床可能对特定人群带来嗜睡或跌倒风险。实际安全效果 NOT_TESTED。

## 直接随机试验：DIALS，2018年9月25日在线发表

Espie 等，JAMA Psychiatry，DOI 10.1001/jamapsychiatry.2018.2745，开放全文 PMC6583463。2015年12月至2016年12月招募1711名自报失眠症状成年人，随机分配 Sleepio 数字 CBT 加常规照护 853 人，睡眠卫生教育加常规照护 858 人。主要结局在第4、8、24周评估，三个主要结局均为参与者自报量表。

第24周经调整的组间差异：
* PROMIS Global Health：+1.76分，95% CI [1.22,2.30]，Cohen d=0.31。
* Warwick Edinburgh Mental Wellbeing：+2.95分，95% CI [2.13,3.76]，d=0.38。
* Glasgow Sleep Impact Index：负18.72分，95% CI [负22.04,负15.41]，d=负1.46，低分表示较少睡眠相关生活质量损害。
* 睡眠状况指标 SCI：+4.91分，95% CI [4.27,5.56]。

研究采用意向治疗分析和缺失值敏感性分析，但实际接受至少一次课程的干预组为689/853即80.8%，完成至少四次课程491/853即57.6%，完成六次413/853即48.4%。治疗组评估失访高于对照组，缺失机制不能从公开汇总结果完全排除偏倚。1711人中约91.1%为白人，外推至其他文化与语言人群需要新证据。没有直接测量死亡、临床事件、客观就业收入或多年整体福利。

论文的中介分析报告45.5%至84.0%范围的统计中介比例，依赖中介识别假设，不能直接作为个体因果机制已经独立确认的证据。关系满意度 RAS 第24周差异约0.01，p=0.98，未见明显改善。论文还记录干预组在第8周更常报告头痛、疲劳、极度嗜睡等被归因于课程的体验。不能仅摘取正向生活质量结果而忽略这些不利信号。

研究由 Big Health 资助，开发者及多名作者存在公司关联。资助方参与设计、实施、数据管理和论文过程，论文称未参与数据分析。此处属于发表的直接随机证据，不等于完全商业独立的产品验证。

## 独立 NICE 外部评估中心：支持与边界

英国 NICE HTG624 于2022年5月20日发布，2025年12月从旧编号迁移但实质建议未变。外部评估中心 EAC 审查28项研究，其中列为12项随机对照研究，但包括6项随机试验的二次分析，不能误记为12个独立随机人群。评估认为 Sleepio 对失眠症状有证据支持，同时指出研究异质、失访较高、与面对面 CBT 或其他数字 CBT 的直接比较不足。

独立复算的具体增量：EAC 获得 Sampson 等2021年医疗资源使用模型的患者级数据，重跑多层广义线性模型并改变季节性和协变量设定。原论文估计每人每年节省 £5.53，EAC 对应估计 £6.64，方向接近。该数据属于引入 Sleepio 的地区准实验观察，且无法把 NHS 医疗资源记录与单个 Sleepio 使用者的症状改善关联。EAC 复算支持所审计统计模型的稳定性，不能单独建立产品导致节省的个体因果关系。

NICE 经济结论依赖当时协商的 £45 启动用户价格及资源使用模型。其2022年基准情景预计一年每人净节省约 £4.52，三年推断存在更大不确定性。此处不能视为当前采购报价或已证实跨三年的实际节省。NICE 指出有面对面 CBT 条件的适格者应优先考虑面对面治疗。用户筛选、语言、互联网可达性和临床风险均影响实际推广。

## 对心理史学未来决策方法的有限启发

1. 在研究协议中分别预设输入与依从性、近期中间行为、使用者自报体验、客观长期结果和负面影响；对中间结果的改善不自动赋予整体福利改善标签。
2. 报告干预分配效果与完成课程人群效果，明确缺失数据机制；不能只展示坚持使用者的事后表现。
3. 产品是否值得采用同时依赖适用人群、使用负担、风险、比较基准和可持续商业价格。NICE 外部评估的模型重算是可借鉴的治理方式。
4. 产品真实算法仍不透明。未来若研究建议排序或价值分数，须预先记录用户目标与规则版本，并测试推荐稳定性及弃权条件。这是候选方法，不是科学规律或产品开发授权。

## E 当日只读治理增量

观察 main 0642e84aacce75b568d9aeee2ed044f3391bc85e。最新 R/B 变更为 R127 original239 P0 05-003 的1990年Van Huyck等人 Table 2 107人汇总转移 sharp bounds。R/B报告证明若场次内人员身份稳定，至少89人从第1至第10轮改变努力水平；该结论是发表的人类聚合边际的部分识别，个体转移矩阵不可识别，正式05-003验收 PARTIAL，新增 R E2/E3 为0。随后修复独立JS检查器的 Git blob NUL 分隔符，未修改R127原冻结协议。

已直接读取 original239 队列 CSV，154条，P0=27、P1=82、P2=45；blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，与MKT212相同。crosswalk blob 36f24235901172642c46853298aebb421f1a3552，文件级待办净减少0。E167于本地11月2日已完成实质审计，本轮无新增E编号，无数学重复复算。

GitHub REST pulls collection 实际返回12个 open PR，全部 Draft，merged_at=null。PR #3 仍为R257 S53非盲态严格收据门候选，main 相对其head独有1133个提交，PR独有1个，GitHub mergeable=true只代表当前技术元数据，不能取代来源身份与历史盲态审查。PR #1旧比较器假阳性、PR #10 R271 元数据覆盖缺口、PR #12 R266原生审计均保持未合并候选。R272已复现的 Python -O P0 false acceptance、R333至R340 0/8工作流强制调用缺口继续开放。没有自动合并、重写或改动跨轨文件。R073、PESEN v0.1冻结不变。

理论轨最新 TH207 交接属于解释性民族志和精确尾概率检查，不产生R新等级；F010 本地2026-W45专题已经完成，后续只读，未新增F编号。未读取个人健康、财务或关系数据。

## 原始公开来源与访问边界

* Sleepio 官方机制与风险，2026年11月2日访问：https://info.sleepio.com/suitability 和 https://info.sleepio.com/faq
* DIALS 开放全文，2018年9月25日在线发表：https://pmc.ncbi.nlm.nih.gov/articles/PMC6583463/ ，DOI 10.1001/jamapsychiatry.2018.2745
* DIALS ISRCTN 登记入口：https://www.isrctn.com/ISRCTN60530898 ，网站要求 JavaScript/cookie，原始版本时间线 NOT_VERIFIED
* NICE 2022 HTG624 独立评估摘要：https://www.nice.org.uk/guidance/htg624/chapter/3-Evidence 和 https://www.nice.org.uk/guidance/htg624/chapter/4-Committee-discussion ，网页检索可读但部分正文直接访问返回403，使用官方搜索文本与 NICE 解说交叉核对
* NICE 真实世界证据解说：https://indepth.nice.org.uk/using-real-world-data-to-measure-impact-on-patient-and-system-outcomes-for-a-digital-health-technology/index.html
* NHS Thames Valley 地区覆盖与数据责任：https://thamesvalley.icb.nhs.uk/your-health/sleep ，官方搜索摘要可见，直接访问返回502；地域条件不外推
* 本仓库R/B直接阅读：research/validation/R127_05_003_TABLE2_SHARP_TRANSITION_BOUNDS_20261102.md；research/validation/R272_P0_NATIVE_OPTIMIZED_FALSE_ACCEPTANCE_20261102.md；research/validation/R333_R340_P0_EIGHT_WORKFLOW_CALLER_REACHABILITY_AUDIT_2026-11-02.md
* 本仓库E/F已完成：research/operations/E167_R269_ORIGINAL239_P0_SCOPE_AND_OPEN_PR_GOVERNANCE_2026-11-02.md；research/privacy_safety/F010_VALUES_AI_HUMAN_OVERRIDE_DATA_LIFECYCLE_2026-W45.md

next_action: 市场优先找Sleepio或其他直接产品的独立客观生活结果与长期随访，或验证DIALS原始登记时间及失访敏感性；避免连续重复步数中间指标。E只读追踪R272明确异常修复和R333至R340完整原生门及生产调用，PR按独立目标键分流。F本周维持只读。GitHub Actions 未触发；账单和免费额度未核实，不执行可能计费CI。无新增收费操作。
