# MKT205：个性化行为建议的随机试验、统计边界与12个月反馈反例

track: market
subflow: 商业产品机制与独立有效性
run_date_utc: 2026-11-01
local_date: 2026-11-02 Asia/Singapore
target_key: (market,MyBehavior+SMARTER,2015-pilot+2022-6m-and-12m-published,personalized-suggestion-versus-generic-advice-and-tailored-feedback-incremental-effect)
baseline_main: 2969fa6155db5a56f5073b9dc7b348d9dbac5a8b
status: COMPLETE_BOUNDED_PRIMARY_FULL_TEXT_METHODS_AND_RESULTS_REVIEW
product_runtime: NOT_RUN
independent_product_code_replay: NOT_RUN
direct_MyBehavior_pilot: MARKET-E2_SMALL_RANDOMIZED_PILOT
SMARTER_adjacent_randomized_6m_12m: MARKET-E2_RANDOMIZED_DIFFERENT_INTERVENTION
Exist_or_commercial_product_specific_causal_outcome: NOT_VERIFIED
long_term_net_welfare: NOT_VERIFIED
new_R_E2_E3: 0
ci_status: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE
sensitive_personal_data: NONE

## 一、选题去重和问题

MKT194已核查Exist的多源数据、相关性API、每周相关计算及2024年纠正后的反馈元分析。本轮不重复Exist接口、安全模拟或统计校正。MKT198至MKT199已研究TRIPPA的运动奖励实验。本轮新增独立的个性化建议实证对照：MyBehavior研究原型的3周小型随机试验，以及SMARTER研究原型的502人6个月和12个月随机试验，审查建议生成的实际机制、干预效果和原论文摘要与正文的统计差异。

这两套研究原型不是Exist、Beeminder、Dcider或其他商业应用的随机验证。两篇SMARTER结果报告使用同一批502名受试者，禁止当成两项独立随机试验。所有阅读限公开英文论文，不注册产品或接入个人数据。

## 二、MyBehavior：可具体核对的建议机制与小样本实验

来源：Rabbi M et al. 2015，JMIR mHealth and uHealth 3(2):e42，DOI 10.2196/mhealth.4160。原始全文 https://mhealth.jmir.org/2015/2/e42/ ，于2026-11-01 UTC直接阅读方法、建议生成、统计计划和结果。

实际用户输入及状态：研究参与者使用Android手机，内置加速度计和GPS连续识别步行、跑步、静止和驾驶，论文报告采用Gaussian Mixture Model进行活动识别。用户可以补录运动、在USDA食物库选择食品及份量，并以食物照片辅助回忆。应用将逐秒活动归纳为分钟及连续事件，按位置、轨迹与食物成分聚类。用户还可设置体重方向目标。论文描述了数据流和模型类别，未取得公开生产源码及独立工程复算。

建议机制：系统根据既有行为的频率和能量消耗生成可执行的小幅改变，例如在熟悉地点增加短时步行、保留既有低热量饮食、尝试过去偶尔完成的活动。每日生成10条饮食和10条活动候选，90%来自常见行为的利用，10%来自少见行为的探索；90/10比例由作者启发式选取。论文将其置于multi-armed bandit框架，但公开描述不能证明已执行完整的在线奖励估计、探索概率优化或反事实策略评估。建议排序与实际收益的校准未获独立验证。

研究招募18人，完成17人。第一周所有人仅记录数据，随后随机分为个性化建议组9人、专业人员生成通用建议组8人，再观察两周。研究者知晓分组，论文明确注册为回顾性注册 NCT02359981。样本多为大学生，干预非常短。

关键统计核查：摘要将步行改善概括为P=.05；正文存在两种不同检验。按步行趋势方向的Fisher精确检验报告P=.05，实验组7/9呈正向趋势，对照组6/8呈负向趋势。按每日步行时长变化的两样本t检验为t(15)=2.1、P=.055、95% CI [负0.23,19.052]分钟、d=0.9。后一个检验在双侧5%标准下未达到显著，置信区间包含零。不能把摘要的P=.05当作所有步行指标都显著的证明。饮食变化组间P=.15，未达显著。建议可执行性主观评分实验组均值3.4、对照组2.5、P<.001，但该指标属于主观意愿。作者团队包含产品开发者，属于内部原型研究，未验证长期真实福利。

## 三、SMARTER：较大样本的增量反馈零效应

来源：Burke LE et al. 2022，Obesity 30(1):75至84，DOI 10.1002/oby.23321，6个月结果 https://pubmed.ncbi.nlm.nih.gov/34898011/ 。同一试验的12个月结果为 Burke LE et al. 2022，Journal of Medical Internet Research 24(7):e38243，DOI 10.2196/38243，开放原始全文 https://www.jmir.org/2022/7/e38243/ 。本轮直接阅读12个月原文的Methods、Outcomes、Statistical Analysis、Results和Discussion，6个月报告以期刊原文及PubMed摘要核对。

SMARTER随机分配502人，每组251人。两组均接受90分钟一对一行为咨询、Fitbit Charge 2、电子体重秤和饮食自我记录工具。仅SM+FB组额外收到研究者开发的规则化个性化反馈应用，每天最多3条消息，按记录数据选择行为建议。对照组SM保留相同追踪设备与基础支持。这项试验估计的是额外个性化反馈在共同自我监测和初始咨询之上的增量效果，不能估计完全没有工具与干预时的差异，也不能归因于Fitbit商业应用自身。

6个月结果：SM+FB体重相对基线平均变化负3.16%，SM负3.20%，两组变化差报告负0.04个百分点，95% CI [负0.99,0.91]，P=.940。没有发现组间额外反馈效果。

12个月结果：SM+FB平均变化负2.12%，SM负2.39%，组间比较报告负0.27个百分点，95% CI [负1.57,1.03]，P=.68。达到至少5%减重者为SM+FB 66/251即26.3%，SM 73/251即29.1%，组间P=.49。12个月保留394/502即78.5%，存在缺失结果及部分远程体重测量和预设填补，受COVID时期影响。研究者报告敏感性分析仍未发现显著组间效果。该试验没有证明额外反馈导致长期更好减重。

在收到反馈的组内，打开消息比例越高，减重越多，回归系数b=负0.10，95% CI [负0.13,负0.07]，P<.001；该分析是组内观察关联，打开行为可能反映动机、追踪依从性等共同因素，不能作为随机分配反馈的因果效果。论文报告12个月反馈打开比例中位数约42.19%，研究者指出长期自我记录下降使算法缺少可用输入。

## 四、可比较之处与不能比较之处

MyBehavior提供一个具体的行为建议生成流程，强调历史可行行为、情境和启发式90/10探索；SMARTER的核心是依据自我监测记录选择预制反馈消息。两者都把原始数据转成行动提示，实际算法与干预强度不同，研究人群、观察时长和终点也不同。MyBehavior 17人3周初步信号无法推翻SMARTER 502人12个月的增量反馈零效应；SMARTER也不能证明MyBehavior机制在其它人群无效。

与既有MKT194 Exist相关性发现的区别：Exist官方公开的是相关描述和统计汇总，未公开受控建议策略效果；MyBehavior研究的是可执行建议，SMARTER随机检验额外反馈。三者没有直接的随机头对头比较。对未来个人决策研究，候选评价必须分别保存原始输入覆盖率、推荐产生率、实际阅读率、建议执行率、独立测量的目标结果、负面溢出、退出后的持续性与用户自主性。上述只是研究测量建议，尚无授权启动产品开发。

## 五、E与F只读交叉治理，2026-11-02本地日期

E167本地当日实质审计已完成，故本轮不新增E编号或重复B数学复算。最新R/B新增 original239 11-029 的逐项审查，R269有限人工E1方法复算及历史三项CI成功已有证据，R073、R105、R106分别提供不同冻结任务的真人分组留出证据。原239该条的正式itemwise队列裁定仍PENDING，不能由研究报告自动关闭。R333至R340八份原工作流的组合验收强制调用为0/8，push路径覆盖为0/8；该结论属于源码静态检查，完整原生执行NOT_RUN，正式P0仍开放。PR #1和PR #3属于独立的R257 S53问题，不应合并问题键。

本轮查询main 2969fa6155db5a56f5073b9dc7b348d9dbac5a8b，12个开放PR均Draft、merged_at=null，PR #3相对main独有1个提交、main独有1097个提交，仍需来源身份、冻结盲态和兼容性审查。队列blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f、crosswalk blob 36f24235901172642c46853298aebb421f1a3552均未变化，最近正式队列154项，P0 27、P1 82、P2 45，文件级净闭合0。未修改R/B、理论轨或共享索引。

F010本周关于价值权重AI的人类实质控制与数据生命周期专题已完成。此次文献额外显示，追踪依从性下降可能使个性化反馈无输入；未来应研究缺失输入时的弃权、人工覆盖及对不确定性的显示。该增量尚不构成新的独立F专题，不新增F编号，不读取任何私人健康、财务或关系资料。

## 六、证据、成本与下轮

MARKET-E1：MyBehavior和SMARTER原始公开技术论文中可直接核查的机制与实现描述，未进行源码原生执行。
MARKET-E2：MyBehavior小样本随机可行性试验；SMARTER 502人随机试验的6个月及12个月结果，同一队列只计一次。Exist等商业产品的直接因果效果仍NOT_VERIFIED。
MARKET-E3：跨人群、长期净福利和独立复现NOT_VERIFIED。不得与R E1/E2/E3混淆。

本轮仅使用公开免费英文论文和已连接GitHub只读资料，无新增服务、付款、付费API、云计算、敏感个人数据或Actions触发。GitHub账户账单与免费额度NOT_VERIFIED；新提交不视为CI通过或科学结题。

下一高价值市场问题：寻找已有真实商业用户的随机建议实验，尤其比较追踪本身、反馈增量、推荐实际执行和长期真实结果。E轨优先等待R/B可信完整checkout的R333至R340复合门原生执行和强制调用验收；原239 11-029维持正式裁定待决。R073和PESEN v0.1冻结保持。

## 公开英文原始来源，2026-11-01 UTC阅读

1. https://mhealth.jmir.org/2015/2/e42/ ，Rabbi et al. 2015，MyBehavior原始全文，尤其Methods和Results。
2. https://www.jmir.org/2022/7/e38243/ ，Burke et al. 2022，SMARTER 12个月原始全文。
3. https://pubmed.ncbi.nlm.nih.gov/34898011/ ，Burke et al. 2022，SMARTER 6个月结果。
4. https://exist.io/ 及 https://kb.exist.io/article/37-what-are-correlations ，仅与MKT194既有市场研究交叉对照。
5. 仓库内部原始文件：research/market/MKT194_EXIST_CORRELATIONS_SOURCE_CONTROL_AND_FEEDBACK_EVIDENCE_2026-11-01.md；research/operations/E167_R269_ORIGINAL239_P0_SCOPE_AND_OPEN_PR_GOVERNANCE_2026-11-02.md；research/validation/R269_11_029_ITEMWISE_ROLE_AND_E2_SCOPE_REVIEW_20261101T1745Z.md；research/validation/R333_R340_P0_EIGHT_WORKFLOW_CALLER_REACHABILITY_AUDIT_2026-11-02.md；research/privacy_safety/F010_VALUES_AI_HUMAN_OVERRIDE_DATA_LIFECYCLE_2026-W45.md。
