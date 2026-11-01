# MKT206：ProjectionLab确定性规划、情景抽样与结果可验证性

track: market
subflow: 真实商业产品运行机制与独立证据边界
run_date_utc: 2026-11-01T19:24:00Z
local_date: 2026-11-02 Asia/Singapore
target_key: (market,ProjectionLab,2026-08-18-docs+2026-06-30-engine+2025-04-11-trials,deterministic-plan-versus-scenario-success-and-calibration)
baseline_main: 5a7cdd4e557fc4cc06706c12b3afbcf63c7e5f8c
status: COMPLETE_BOUNDED_OFFICIAL_PRIMARY_DOCS_AND_ADJACENT_INDEPENDENT_RESEARCH
product_runtime: NOT_RUN
source_code_replay: NOT_RUN
commercial_product_direct_RCT: NOT_VERIFIED
real_user_outcome_improvement: NOT_VERIFIED
market_evidence: MARKET-E1_OFFICIAL_MECHANISM; MARKET-E2_ADJACENT_SIMULATION_METHOD_STUDY_ONLY
long_term_welfare: NOT_VERIFIED
new_R_E2_E3: 0
ci_status: NOT_RUN
billing_checked: NOT_VERIFIED
new_paid_operations: NONE
sensitive_personal_data: NONE

## 一、选题与既有研究去重

此前MKT200至MKT202研究的是独立退休规划计算器随机试验及预注册异质性；该试验并非ProjectionLab产品效果证据。本轮改查一个真实在售产品的预测引擎、成功概率与实际结果对照，重点解决用户可能把规划情景输出当作已校准预测的混淆。与MKT205个性化行为建议试验不重复。未登录、注册、购买或导入个人财务信息。

## 二、直接读取的官方产品运行机制

官方2026年8月18日帮助文档说明：Plan视图使用用户输入的余额、收入、支出和固定增长率，逐年形成一条确定性轨迹。Chance of Success视图对相同计划使用历史或随机市场数据，令回报、股息、通胀等随抽样路径变化。官方特别说明其他标签页遵循Plan假设，并不自动转为Chance of Success的随机结果。两者数值不同具有预期性。

官方2026年6月30日引擎文档披露：模型以每年365天为年度结算单位，汇总工资、其他收入、代扣税、支出、债务、分红、上年应纳税额、RMD、租金等，并自动计算盈余及所需提取。可逐年查看现金流和期末余额。此为产品厂商披露的运行逻辑，尚未取得生产源码及同输入独立复算。

官方2025年4月11日文档说明：随机起始年份与随机重启等抽样方式可以将试验次数增加到最多2000；历史连续序列且不循环的方式没有可增加试验次数的选项，因为重复不会产生新的历史序列。由此确认“更多抽样次数”与“更多独立历史证据”并非同义。

官方进度文档披露：实际进度点需要搭配起始时间足够早的固定日期计划，在Net Worth + Progress图叠加实际进度。这个功能提供预测与实际值的可视化对照，官方文档未给出前瞻概率校准误差、预测覆盖率或经审计的用户决策改善效果。

## 三、实际用户输入、目标与反馈

输入：账户余额、收入、支出、资产、负债、退休时间、重大生活事件、税务设定、资产收益与通胀假设。可以设置里程碑，检查净资产、现金流、提取策略与达到财务目标的情景表现。规划输入由用户维护，不要求连接银行账户。

反馈：修改输入后重新运行计划；可以按固定日期记录实际资产进度并叠加历史预测。该机制可用于识别实际与规划偏差，但不能从图形叠加推断模型因果建议有效，也不能从单个成功概率推断实际未来成功率已校准。

官方未完整公开生产模拟器源码、每一采样模式的随机数实现、历史数据完整版本身份及真实用户前瞻预测校准报告。本轮不将文档描述升级为独立工程通过。

## 四、一个可精确界定的统计限制

若假设2000次抽样彼此独立，且真实的模型内成功概率恰为90%，二项分布近似标准误为sqrt(0.9×0.1/2000)=0.006708，即0.671个百分点。单纯抽样波动的约95%正负幅度约为1.315个百分点。此数字仅是公式算术示例，非ProjectionLab真实运行、真实概率误差或模型外推准确性；有相关抽样路径时有效样本量可能更小。将试验数从500增加至2000最多降低抽样噪声，无法纠正收益分布、通胀、寿命、税制及行为假设的系统偏差。

2024年Horan发表于Financial Planning Review的独立开放论文用多类蒙特卡洛和历史收益情景研究退休提款频率，报告在控制投资在市时间可比时，提款频率对退休提款可持续性没有影响，收益波动与自相关等假设则影响结果。它是独立的相邻方法研究，未测试ProjectionLab产品、用户行为或该软件概率校准，不能计为直接产品效果试验。

## 五、隐私、价格、商业与证据局限

官方定价页面在本轮读取时列Basic每年0美元，包含预测、Monte Carlo、历史回测；Premium每年129美元，含情景比较、税务及高级功能；Pro每年549美元，面向顾问。没有实际订阅或注册。官方数据安全帮助文档称保存的计划使用Google Cloud Platform和Firebase、传输与静态数据加密，允许JSON导出及账户删除，且不要求关联银行账户。实际备份清除、服务商处理、漏洞和删除结果未测试。官方说明产品仅供教育和信息用途，不能保证预测准确性。

独立外部评论可帮助核对市场定位，但本轮没有发现可核实的ProjectionLab随机使用效果试验或长期用户福利研究。官方营销、方法公开、独立数值复算、真实决策改善必须分层。

证据分级：MARKET-E1为官方产品机制、价格和隐私陈述；MARKET-E2仅为Horan 2024相邻退休仿真方法研究，不是产品随机试验；ProjectionLab本身真人因果效果、长期预测校准及净福利为NOT_VERIFIED；MARKET-E3无可验证结果。以上均与R E1/E2/E3隔离。

## 六、E科研治理只读增量

2026-11-02本地日期已完成E167实质审计，本轮没有重复B数学验证或新增E编号。观察main 5a7cdd4e557fc4cc06706c12b3afbcf63c7e5f8c相较MKT205提交dbbde2b4efc5cced43ddf542d70fc45ab1fa74ba仅新增2个提交，分别涉及A轨Mao 2017数据设计门与理论TH204；没有更改市场、E、F及原239队列索引。A轨原文核对显示Mao2017十轮重配对及固定人群跨天重复，与R073冻结的100轮、12实验场次分割冲突，原样R073独立评分资格为FAIL_UNCHANGED；OSF原始数据HTTP403，原始复现NOT_RUN。该结论不撤销R073既有结果。

当前12个开放Codex PR逐一读取元数据均为open、Draft、merged=false，PR #1和#3属于R257 S53。PR #3 head为97d5f74df5d84916917db943156120f08144f445，相对观察main为main独有1100提交、PR独有1提交；这不等于已证明合并冲突。R333至R340复合验收真实完整checkout执行和八份原始工作流强制接入继续开放P0。original239队列Git blob为3b96d46b3d88ccafd779a08509c3cfd0e435772f，crosswalk blob为36f24235901172642c46853298aebb421f1a3552，均与前次相同；最近正式登记154项，P0 27、P1 82、P2 45，文件级净闭合0。R269原239 11-029逐项验收仍PENDING。

## 七、F本周状态及下一步

F010本周价值权重型AI的人类实质控制与个人数据生命周期专题已完成。ProjectionLab提供新的F相关观察：财务情景计划可在云端保存并以JSON导出，未来应独立检验停止云端同步、删除副本与本地离线复算能力。本轮仅只读引用，未新增F编号、未进行安全测试或接入个人财务数据。

下一高价值商业任务：查找公开实现或可审计预测误差的情景规划产品，对比固定假设、随机抽样、目标达成阈值、反馈频率与真实长期结果。若后续开展合成敏感性测试，须事前冻结输入、抽样方法、版本和评估规则，且明确区分仿真稳定性与真人有效性。E继续等待R/B复合门原生收据和正式调用证据。维持全部R系列完成后统一分类、再有条件熔炼，R073及PESEN v0.1保持冻结。

## 实际阅读的公开免费英文原始来源

1. ProjectionLab Plan vs Chance of Success，2026-08-18: https://projectionlab.com/help/plan-vs-chance-of-success
2. ProjectionLab Simulation Engine，2026-06-30: https://projectionlab.com/help/simulation-engine
3. ProjectionLab Monte Carlo Trials，2025-04-11: https://projectionlab.com/help/increase-trials-in-chance-of-success
4. ProjectionLab Actual Progress，2023-12-13: https://projectionlab.com/help/overlay-actual-progress
5. ProjectionLab Data Security，2023-06-09: https://projectionlab.com/help/data-security
6. ProjectionLab Pricing，2026-11-01访问: https://projectionlab.com/pricing
7. ProjectionLab Monte Carlo 产品说明: https://projectionlab.com/monte-carlo
8. Horan SM, 2024, Financial Planning Review, DOI 10.1002/cfp2.1183, 开放全文: https://onlinelibrary.wiley.com/doi/full/10.1002/cfp2.1183

GitHub: 仅本轨独立文件写入；无Actions运行；实际账户账单与免费额度NOT_VERIFIED。提交SHA和最终回读身份须在提交后报告，不预先填写。
