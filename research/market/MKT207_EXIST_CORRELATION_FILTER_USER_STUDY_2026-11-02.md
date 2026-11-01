# MKT207：Exist 多源个人追踪、相关性呈现与真人信息筛选研究

track: market
subflow: 商业产品机制与直接真人使用证据
run_date_utc: 2026-11-01T20:17:22Z
local_date: 2026-11-02 Asia/Singapore
target_key: (market,Exist,API-v2-2026-and-Jones-Kelly-2018,correlation-interpretation-and-user-rated-information-filter)
baseline_main: ff5230bd28e5a4017c9aa717a173633056b29e2b
status: COMPLETE_BOUNDED_PRIMARY_PRODUCT_DOCS_AND_INDEPENDENT_DIRECT_USER_STUDY
product_runtime: NOT_RUN
product_source_code_replay: NOT_RUN
human_evidence: DIRECT_EXIST_20_PERSON_OBSERVATIONAL_STUDY_AND_LEAVE_ONE_PERSON_OUT_CLASSIFIER_EVALUATION
real_decision_improvement: NOT_VERIFIED
causal_long_term_welfare: NOT_VERIFIED
market_evidence: MARKET-E1_OFFICIAL_DOCUMENTED_MECHANISM; MARKET-E2_DIRECT_INDEPENDENT_HUMAN_INFORMATION_RELEVANCE_STUDY
new_R_E2_E3: 0
ci_status: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE
personal_sensitive_data: NOT_ACCESSED

## 一、选题与去重

MKT200至MKT202讨论退休规划实验，MKT203讨论价值权重型AI，MKT204讨论经济承诺，MKT205讨论个性化反馈随机试验，MKT206讨论财务情景模拟。本轮转向真实在售的多源个人量化产品Exist，优先寻找直接使用该产品的独立真人研究，重点衡量“发现的相关性是否对使用者有意义”。目标键按产品、版本、证据缺口与前轮区分。未使用任何付费产品或真实私人资料。

## 二、官方机制及实际输入输出

1. 用户通过穿戴设备、日历、运动和生产力服务自动同步数据，也可手动输入情绪、习惯、标签及自定义量化指标。官方API将属性值存为用户本地日期粒度的date/value对；缺失日可返回null，当前文档明确不存逐小时或逐分钟的属性时间序列。属性有类型、来源服务、分组和模板，可在授权范围内读取。
2. 相关性对象公开两个属性、相关系数value、p值、stars置信展示、period观察期、offset日间偏移、文本说明及用户主观rating。官方示例展示线性相关值和显著性字段，历史与API描述表明同时比较当日及相邻两日。相关性每周生成，最多使用约一年数据；知识库要求某属性至少有三个星期的非缺失数据。产品文档的星期更新日表述存在历史差异，统一记录为“每周”，不把具体星期日作为稳定承诺。
3. 这是从个人历史观测中发现同现或次日关联的探索机制。官方明确提示相关不等于因果。公开API说明足以重建数据接口和部分显示规则；生产计算源码、全部筛选条件、多重比较调整、序列自相关处理和前瞻校准证据未在本轮来源中得到完整公开，状态UNKNOWN。
4. 用户可查看相关性、长期趋势和每周汇总，给相关性打“有用”等主观标签。官方2026年4月23日更新提供PDF报告、最多五属性的CSV导出，以及全量JSON导出。官方2026年11月2日访问定价为每月USD6.99或每年USD62.90，30天试用，试用结束需要付费；本轮未注册，费用为0。
5. 官方隐私政策2023年10月6日版本披露，断开第三方同步阻止后续采集，但历史已采集数据不会随断开自动删除；账户删除后仍可能在备份和归档中保留“商业上合理的期间”，没有明确最长时限。公司可在并购等特定情形转移信息，公开政策与实际删除效果应分开验证。真实服务商运行和数据生命周期未做独立安全测试。

## 三、直接独立真人研究：Jones与Kelly（2018）

独立来源：Jones SL, Kelly R. Dealing with Information Overload in Multifaceted Personal Informatics Systems. Human-Computer Interaction 33(1), 1至48, 2018，DOI 10.1080/07370024.2017.1302334。大学机构仓储提供作者接受稿，已实际查阅摘要、研究方法、留出评估、主要数值及局限。

研究在约三个月中让20名参与者使用Exist收集跨领域个人数据，随后对相关性信息进行评价。研究中200条相关性主观评价构成后续统计模型的一部分，每人10条。研究者另外构建预测“用户是否认为一条相关性有趣”的筛选器，使用leave-one-participant-out交叉验证，每轮留出1人，其他19人训练，避免同一参与者记录同时出现在训练和测试组。

核验的结果：
* 论文所描述的当时Exist显示基线中，43.5%的相关性被参与者评为有趣。
* 仅用p<0.05过滤的基线，其论文报告的“正确识别有趣与无趣”总体分类率为53.4%。这一总体准确率不能直接当作展示结果的precision。
* 候选分类器平均将44.6%的相关性标记为有趣，即平均减少55.4%的展示量。不同分类器表现不同，不应把这个均值误归到单一模型。
* 最佳Random Tree分类器对“展示为有趣”类别的precision达到81.3%，比论文定义的最佳p值筛选基线高34.4个百分点；最佳召回率达到72.5%。不能把81.3%解读为决策正确率、因果发现准确率或人生目标达成率。
* 研究方法讨论了令人惊讶、可用性及跨类别关系对用户主观兴趣的影响。论文承认参与者一次性查看大量结果的实验方式可能偏离日常分批查看习惯；所获数据已经被当时Exist的p<0.2预筛选，可能遗漏其他有趣但统计不显著的关系。历史产品行为不能直接等同2026年的生产规则。

证据层级：MARKET-E2为真实Exist参与者的非随机、有限样本主观信息相关性评价及内部按人留出分类器评价。该研究不是独立外部新队列复现，也没有随机验证筛选器是否提高长期行为或人生决策结果。论文提出的分类器是研究者候选机制，本轮没有证据确认其已部署到2026年的Exist产品。没有读取受试者原始个人数据或运行作者代码。

## 四、科学与产品风险的具体分离

1. 统计显著性：p值和星级描述一条相关性在某种统计假设下的显著性，无法自动判断行动价值。多指标、多配对、多时间偏移、时间趋势及自相关可能提高误报风险。当前API文档未充分说明相关校正方法，不能直接断言产品完全没有校正。
2. 信息筛选：按用户兴趣排序能够改善被展示内容的主观相关性；在健康、财务或关系等高风险场景，重要但令人不悦的信号可能被兴趣筛选压低。论文自身提醒“有趣”和“重要”不同，未来研究需要额外的高风险提示与漏报测量。
3. 行为改善：Exist公开API和真人研究支持“能够聚合数据、显示相关性、使用者对某些相关性评价为有趣”。“由此提高长期决策质量、健康、财富或福利”仍未验证。不存在本轮新增R真人E2或历史E3。
4. 未来验证候选：以完全公开的人工序列事前固定假设和时间切分，分别检查相关性显著性、展示兴趣precision、重要信号召回、事后独立行动与长期结果。当前阶段仅研究方法，不开展个人辅助决策产品开发或个人数据实验。

## 五、E只读科研治理增量

2026-11-02本地日期已完成E167实质审计，本轮未制造新的E编号。读取main最新三提交：R178新增独立JavaScript BigInt数值检查脚本与R/B报告；理论轨TH204交接。R178报告声称30世界270个PMF单元及300项精确等式一致，30个logloss浮点误差小于1e-12，三项定向篡改被拒绝；这是R/B同一执行主体内部人工E1，原239 08-002正式科学验收仍PARTIAL，Node.js完整本地CLI仍NOT_RUN。E只核对源码与报告范围，不重复数值验证。

原239待核队列blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，crosswalk v7.8 blob 36f24235901172642c46853298aebb421f1a3552，均与E167/MKT206相同。最近直接报告队列154项，P0 27、P1 82、P2 45，文件级净减少0；不得把R178内部数值通过算成正式队列关闭。

本轮逐一读取12个开放Codex PR元数据，全部open、draft=true、merged=false。PR #1/#3的R257 S53来源身份及冻结盲态问题未闭合；PR #3 head 97d5f74df5d84916917db943156120f08144f445 与本轮main ff5230bd28e5a4017c9aa717a173633056b29e2b 比较为main独有1104提交、PR独有1提交，版本差异不代表必然合并冲突。PR #10明确记录R271旧B门对“R073=MODIFIED”元数据篡改仍可能接受，候选新oracle可拒绝；属于尚未合并的独立候选审计，不据此提升R科研等级。R333至R340复合验收真实完整仓库原生执行和八份原始工作流强制接入仍未核验，历史P0风险保持开放。没有合并、强推或改写跨轨文件。

理论TH204、C010与D003状态只读：C010当天COMPLETE，D003本周COMPLETE，历史因果争议仍PARTIAL。R073及PESEN v0.1冻结不变。

## 六、F本周专题、费用及后续

F010在2026-W45已完成实质研究。本轮新增的Exist隐私政策是具体产品对照材料，断开同步与历史数据删除分离，备份保留期限未明。仅只读补充，不新增F编号，不执行实际删除、安全或敏感数据实验。

无付费服务、产品购买、个人敏感数据、GitHub Actions调度或新自动化。账户账单与免费额度未独立核验，ci_status=NOT_RUN。远端提交SHA、blob与提交关联状态应在实际提交和回读后报告。

下一高价值市场问题：寻找具有公开算法实现、独立客观行为评价的多目标个人决策工具；如继续Exist，优先检查2018研究的分类器代码和后续外部复现，避免无证据连续增量。E继续追踪R333至R340真实原生组合验收和PR #10元数据覆盖缺口，F仅本周必要只读检查。

## 本轮实际读取的免费英文原始资料

1. Exist官方网站及定价，2026-11-02访问：https://exist.io/
2. Exist API object types，2026-11-02访问：https://developer.exist.io/reference/object_types/
3. Exist correlations API，2026-11-02访问：https://developer.exist.io/reference/correlations/
4. Exist attribute API，2026-11-02访问：https://developer.exist.io/reference/attributes/
5. Exist最少数据量，2023-09-20更新：https://kb.exist.io/article/18-how-long-does-it-take-to-find-correlations
6. Exist次日关联，2022-02-09更新：https://kb.exist.io/article/55-will-exist-find-correlations-across-multiple-days
7. Exist PDF/CSV/JSON导出，2026-04-23更新：https://jenny.exist.io/blog/pdf-export/
8. Exist隐私政策，2023-10-06更新：https://exist.io/privacy/
9. Jones与Kelly 2018大学作者接受稿：https://purehost.bath.ac.uk/ws/portalfiles/portal/153257196/ExaminedLife_MINOR_REVISION.docx_3.pdf
10. University of Bath机构出版记录：https://researchportal.bath.ac.uk/en/publications/dealing-with-information-overload-in-multifaceted-personal-inform/
11. DOI：https://doi.org/10.1080/07370024.2017.1302334
