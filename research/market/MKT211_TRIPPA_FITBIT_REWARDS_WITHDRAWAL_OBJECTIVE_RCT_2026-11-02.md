# MKT211：TRIPPA真实 Fitbit Zip 随机试验的客观行为、奖励撤除与健康结果

track: market
subflow: 商业产品运行机制与真实效果研究
run_date_utc: 2026-11-02
local_date: 2026-11-02 Asia/Singapore
target_key: (market,Fitbit-Zip-TRIPPA,NCT01855776-2016-published,objective-MVPA-incentive-withdrawal-health-outcome-transfer)
baseline_main: 56fe3228dc24075491e2aaa504ab623fce5c4125
status: COMPLETE_BOUNDED_PRIMARY_ABSTRACT_AND_INSTITUTIONAL_SOURCE_AUDIT
evidence: MARKET-E2_DIRECT_HUMAN_RANDOMIZED_TRIAL_WITH_OBJECTIVE_ACTIVITY_MEASURE
full_publisher_article: NOT_ACCESSED
trial_registration_history: NOT_VERIFIED
independent_raw_data_reanalysis: NOT_RUN
modern_Fitbit_product_effect: NOT_VERIFIED
new_R_E2_E3: 0
paid_actions: NONE
CI: NOT_RUN
billing_checked: NOT_VERIFIED

## 研究问题及与既有报告去重

在MKT204的Beeminder经济承诺机制、MKT205的个性化反馈实验、MKT208至MKT209的Noom长期结果和MKT210的公开算法审查之后，优先寻找真实商业追踪产品的随机分组、客观行为终点和撤除激励后的随访。选定TRIPPA试验（Finkelstein等，2016，The Lancet Diabetes & Endocrinology，DOI 10.1016/S2213-8587(16)30284-4；NCT01855776）。本轮先以仓库代码搜索检索 TRIPPA、Fitbit、Finkelstein、NCT01855776，未返回既有匹配。此检索不足以保证全库不存在同题表述；本报告的目标键与前述市场报告区分为“Fitbit Zip直接RCT＋激励撤除＋独立测量”。

## 产品、用户输入与实验机制

真实研究设备为2013至2014年使用的 Fitbit Zip 腰部活动追踪器。用户佩戴设备采集步数；在研究的激励组，记录的每周步数用于判断现金或慈善捐赠奖励资格。研究奖励门槛包括每周50,000至70,000步以及更高步数档。设备属于自动量化及反馈工具，研究没有验证任何AI人生建议算法，也未公开完整步数识别算法、误差校准或个体长期预测模型。

800名新加坡全职雇员（21至65岁）随机分配为四组：无设备对照201人、Fitbit设备203人、Fitbit加慈善激励199人、Fitbit加现金激励197人。激励实施6个月，随后撤除，继续观察到12个月。主要终点为每周中高强度身体活动连续时段分钟数（MVPA bout min/week），由封存的独立加速度计测量，按意向治疗分析；研究还观察体重、血压等健康指标。该独立测量比直接使用产品内步数作主要因果终点更能降低同源测量偏差。实际设备使用和研究人员跟进不等于用户自主长期坚持。

## 直接随机试验结果，单位为每周MVPA分钟相对对照组的调整差值

| 观察时点 | Fitbit设备组 | 慈善激励组 | 现金激励组 |
| --- | --- | --- | --- |
| 6个月 | +16，95%CI [-2,35]，p=0.0854 | +21，95%CI [2,39]，p=0.0310 | +29，95%CI [10,47]，p=0.0024 |
| 12个月 | +37，95%CI [19,56]，p=0.0001 | +32，95%CI [12,51]，p=0.0013 | +15，95%CI [-5,34]，p=0.1363 |

12个月时现金激励组与Fitbit单独组的直接比较为 -23 MVPA分钟/周，95%CI [-42,-4]，p=0.0184。此比较发生在奖励撤除后6个月。研究报告在6和12个月均未发现体重、血压等健康终点的改善证据。

严守解释边界：
1. 12个月Fitbit组相对对照组+37分钟，是组间差值，不能称为Fitbit使用者自身增加37分钟；对照组活动减少也会产生相对差距。
2. 6个月现金奖励的相对对照优势，不能证明其优于Fitbit单独组；原摘要明确现金/慈善组相对Fitbit组的6个月增加未达到显著性。
3. 撤除现金奖励后相对Fitbit组更差，支持奖励持续性风险，不能仅凭组间比较证明单一心理机制（如内在动机受损）。
4. 健康终点“未发现改善证据”不等于证明效果精确为零。多重比较、失访、设备依从性、置信区间和健康终点统计功效需要完整论文进一步核查。
5. 研究针对2016年Fitbit Zip及特定雇员、激励和随访设计，不能直接推断2026年Fitbit/Google Health产品的效果，不能推广到Beeminder罚金契约、个人长期人生决策或心理史学R证据。

## 当前产品机制、隐私和商业边界

2026年官方 Google Health 支持文档说明当前Fitbit设备可追踪步数和活动分钟数，部分设备还可记录睡眠、运动、饮食、水、体重等，具体取决于设备。它与2016年Zip试验是不同产品世代。2026-02-27更新的Fitbit隐私政策说明部分Fitbit账户信息可导出，账户删除后多数信息30天内处理、包括备份在内的全部信息最长可达90天；迁移Google账户的用户适用Google隐私政策，故不能将旧Fitbit政策直接套用所有当前账户。官方2026-05-19的Google Health隐私问答说明旧Fitbit账户迁移和删除安排。所有隐私内容均为厂商政策声明，实际删除及第三方处理未测试。现行硬件购买价、Premium订阅实际价格与地区适用性本轮未确认，故不报价、不购买、不注册、不采集私人健康数据。

商业启示限定为未来研究问题：产品目标必须分开衡量“记录量”“行为改变”“客观最终结果”“撤除奖励后的保持”“经济成本与负担”。若以奖励或惩罚维持执行，应预先设定退出后随访、实际净福利及异质性测量。这里的候选评估维度尚非经过验证的个人决策产品设计，也不触发正式开发。

## E只读治理与F本周检查

E：本地2026-11-02已有E167实质审计，本轮只读增量核查。观察main 56fe3228dc24075491e2aaa504ab623fce5c4125，较MKT210提交768e07a91560aa50252531dce198fd2bef5d5c94新增R272两项审计提交和TH206理论提交。R272新独立V8 BigInt复算576来源行、8640字段、9世界，7项内存负例被拒；原Python生产程序裸assert在优化模式的潜在绕过仅为静态风险，完整原生变异运行NOT_RUN，R272原239正式验收未自动关闭。R333至R340组合门完整仓库原生执行和八份生产工作流强制调用仍开放，既有P0未消除。R257 S53 PR #1/#3旧比较器假阳性及来源/盲态验收仍开放。GitHub pulls集合实读12个开放PR，全部Draft、未合并；PR #3 head 97d5f74df5d84916917db943156120f08144f445 与main比较 diverged，main独有1124、PR独有1；提交差异不能证明合并冲突。original239待核队列blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f、crosswalk blob 36f24235901172642c46853298aebb421f1a3552未变化；同一固定队列快照154项（P0=27/P1=82/P2=45），文件级净减少0。未修改其他轨或冻结协议。

F：2026-W45的F010已实质完成，保持COMPLETE。本轮只读记录Fitbit/Google账户迁移、导出、删除时限以及奖励撤除的自主性问题；没有新增F编号、没有安全实测、没有私人数据处理。R073与PESEN v0.1冻结继续保持。

## 来源与实际访问范围（2026-11-02 UTC）

1. Finkelstein EA et al. (2016), TRIPPA 原始论文的PubMed摘要，含随机组别、主要客观终点、6及12个月全部关键组间估计、置信区间和p值。https://pubmed.ncbi.nlm.nih.gov/27717766/ ；DOI https://doi.org/10.1016/S2213-8587(16)30284-4 。出版社完整论文未取得，故本轮无表格级原始数据重算。
2. Duke University作者机构成果页，同论文摘要交叉核对。https://scholars.duke.edu/publication/1147644
3. Duke-NUS医学院原始机构新闻稿，说明设备依从性、撤除激励及资助。https://www.duke-nus.edu.sg/newshub/media-releases/the-effectiveness-of-activity-trackers-and-rewards-to-encourage-physical-activity
4. Google Health官方活动追踪说明。https://support.google.com/googlehealth/answer/14236510
5. Fitbit官方2026-02-27隐私政策。https://www.fitbit.com/privacy-policy
6. Google Health官方2026-05-19隐私问答。https://support.google.com/product-documentation/answer/13532616
7. ClinicalTrials.gov试验入口 https://clinicaltrials.gov/study/NCT01855776 （本轮原始历史注册版本和时间戳NOT_VERIFIED）。

next_action: 优先核查TRIPPA原始注册历史、完整论文中失访/依从性和预设对比，再寻找独立客观结果且可区分“设备追踪本身”与“外部激励”的第二项真实产品试验；避免连续扩展同一编号。E优先等待R/B原生组合门执行及正式工作流接入收据，F本周只读。没有新增收费、Actions或外部API运行。
