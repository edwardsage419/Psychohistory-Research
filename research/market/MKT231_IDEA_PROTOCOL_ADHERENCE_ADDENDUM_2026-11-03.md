# MKT231 增量审查：IDEA 设备实际使用、原始方案与可获取数据边界

track: market
subflow: commercial_product_research + E_daily_readonly + F_weekly_readonly
run_date_utc: 2026-11-02
local_date: 2026-11-03 Asia/Singapore
target_key: (market,BodyMedia-FIT-Core-IDEA,NCT01131871-2013-protocol-vs-2016-publication,wear-adherence+protocol-version+data-access)
prior_report: research/market/MKT231_IDEA_BODYMEDIA_470_24MONTH_RCT_CORRECTED_ABSTRACT_2026-11-03.md
observed_main_before_write: 69e7d31fcb9a2595b22c71641446cfad4d5734b9
status: COMPLETE_BOUNDED_ORIGINAL_PROTOCOL_AND_PUBLICATION_RECHECK
evidence_grade: MARKET-E2_DIRECT_HUMAN_RCT_PUBLICATION; MARKET-E1_DOCUMENTED_PROTOCOL_AND_DATA_ACCESS
participant_level_reanalysis: NOT_RUN
registry_original_history: NOT_VERIFIED
production_device_execution: NOT_RUN
new_R_E2_E3: 0
ci: NOT_RUN
billing: ACCOUNT_BILLING_AND_ACTIONS_FREE_QUOTA_NOT_VERIFIED
sensitive_personal_data: NOT_ACCESSED
paid_operations: NONE

## 1. 本轮新增来源与主要发现

已存在MKT231研究2016年JAMA原文、24个月体重与正式勘误。本轮围绕同一试验补充先前缺失的原始研究方案、设备实际使用分布和公开数据申请边界，因此沿用MKT231目标，不新增MKT编号。实际直接阅读：

1. JAMA正式论文HTML，尤其Results设备依从性段、Methods统计计划与两组干预，2016-09-20: https://jamanetwork.com/journals/jama/fullarticle/2553448/
2. NIH/NHLBI BioLINCC IDEA公开研究资源目录、访问说明及研究资料，数据目录最近更新2018-07-02: https://biolincc.nhlbi.nih.gov/studies/idea/
3. BioLINCC公开39页《Innovative Approaches for Diet, Exercise, and Activity (IDEA) Protocol》，页首版本明确为2013-02-10，审阅第1、4、5、7、8、31至34页；资源目录的Protocol PDF链接见上述BioLINCC页面。
4. ClinicalTrials.gov登记入口 NCT01131871: https://clinicaltrials.gov/study/NCT01131871 。本轮未取得可验证的原始注册历史版本。

## 2. 设备实际使用的新增定量证据

JAMA Results原文明确：增强组237人中191人领取设备且至少佩戴一天，比例191/237 = 80.59%。这是一项联合条件，剩余46人不能在缺乏细节时全部定性为“领取后从未佩戴”。在191名达到该联合条件者中，设备实际佩戴天数中位数170天，四分位区间68至347天；在佩戴日中，每天佩戴分钟数中位数241.1分钟，四分位区间99.3至579.1分钟，即中位数约4.02小时/佩戴日。设备从第7个月开始提供至第24个月，名义窗口约18个月。

这些公开统计提示设备使用的实际剂量存在很大异质性。170天不能当作全部237人的中位佩戴天数，也不能把241.1分钟解释为全试验每天平均佩戴时间。设备使用量是随机分配后的行为；按使用量分组直接比较体重将引入选择偏倚。既有随机试验识别的是增强方案分配的意向治疗比较，无法单凭此分布断言低依从性造成较差减重，也无法独立识别设备的纯粹使用效应。

原论文同时明确：24个月独立体重测量完成率74.5%，标准组72.5%、增强组76.4%。缺失体重采用似然混合模型和多重插补敏感性分析，MAR仍是需审查的假设。原MKT231的2.4公斤组间差值与更正结果保持不变。

## 3. 公开原始方案与2016论文的对应

BioLINCC方案页首版本为2013-02-10，晚于论文报告的2010至2012年招募期。它能证明2013年文档版本的研究设计，不能独立证明随机分配之前就已冻结同样的所有条款。需要最早的ClinicalTrials.gov历史快照、研究伦理/DSMB修订史，才能完成事前性判断。

公开方案明确：主要终点为基线至24个月体重变化；拟用线性混合模型，调整种族、性别、测量时间、干预与时间交互，考虑受试者和招募队列随机效应，主要检验24个月交互项；多项次要比较拟用Holm法；缺失体重假定MAR，敏感性分析拟用多重插补。JAMA论文的方法章节明确报告24个月体重、线性混合效应模型、性别/种族/招募期、Holm次要比较和多重插补，主要结构一致。不能据此宣称已完整审计所有原始版本、模型代码或参与者级输出。

存在值得记录的**实施描述差异**：2013方案的设计图和第7页写增强组另加tailored text prompts，而标准组接收non-tailored提醒；2016论文正文把两组的每周短信描述为共同干预，未明确报告这项差异是否实际执行或取消。该差异目前是“方案计划与发表描述之间待核”，不能声称实际有差异化短信，更不能把所有观察效果直接归因于设备硬件。应优先查修订方案、补充材料或作者的实施说明。

## 4. 数据来源与隐私限制

NIH BioLINCC把IDEA列为Open BioLINCC Study，公开数据字典、带注释表格、方案和论文资源。参与者级数据需要注册账户后提交申请；网站明确注册免费，实际数据申请是否具有额外资格或协议要求尚未完整核实。本轮没有注册、申请、下载或读取参与者级健康数据，遵守本项目敏感资料禁令。原始数据重算、佩戴剂量与结果关联及个体缺失机制均NOT_RUN。

目录正文的标准组人数写232，JAMA正式论文分析样本写233；这一数值不一致需要核对BioLINCC数据集筛选口径或目录编辑，不能在未见数据时宣称研究随机化错误。论文明确最初471人随机、1人被发现不符合条件，470人纳入分析，标准233、增强237。当前报告沿用原论文主分析分组。

## 5. 产品与证据边界

用户输入：传感器活动及能量消耗，饮食手工录入；状态与目标：活动量、热量及研究目标；反馈：上臂设备屏幕、厂商网站、研究人员定期接触。具体传感器估算算法、历史商业价格、当前服务及删除政策均未独立验证。

MARKET-E1：方案、产品使用流程和BioLINCC目录描述，属于公开文档证据。
MARKET-E2：已发表随机试验的24个月客观体重差异及设备使用分布，属于真实人类试验公开结果，原始数据独立复算NOT_RUN。
MARKET-E3：跨设备、跨人群、长期整体福利或当前AI人生决策改善，NOT_VERIFIED。
R系列E1/E2/E3：本轮均未新增；不得混用等级。

## 6. E当天治理只读复核

E168于本地2026-11-03已完成实质治理审计，本轮未重复建立E编号。当前main在写入前为69e7d31fcb9a2595b22c71641446cfad4d5734b9。最近R/B新增R127原始1990论文Table 2全部10期、490个聚合整数格的单人图像核对；70个列合计与最小值检查及6个负例通过，独立第二读者和个体级轨迹仍缺，正式队列保持PARTIAL，新R E2/E3为0。来源：research/validation/R127_05_003_PRIMARY_1990_TABLE2_ALL_PERIODS_SOURCE_CHECK_20261102.md。

original239待核CSV blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，本轮实际读154行，P0=27、P1=82、P2=45；crosswalk blob 36f24235901172642c46853298aebb421f1a3552，均与前轮一致，文件级净减少0。12个开放Codex PR均Draft、merged_at=null；PR #3 head 97d5f74df5d84916917db943156120f08144f445 对本轮main比较为diverged，main独有1222提交、PR独有1提交。PR #8/#9的历史字节身份依赖仍需独立验收。

R272当前生产YAML blob 3132b08cf4ee64b55f5112d2249894ea0ec9d42d未变化，包含contents:write、先--emit后assert及自动git push，候选强制入口未接入，P0仍OPEN。R333至R340八份生产工作流组合验收强制调用仍无关闭证据。main protected=false为本轮GitHub分支读取结果。没有自动合并、改写跨轨文件或冻结协议；R073和PESEN v0.1冻结不变。

## 7. F本周只读与费用、下一步

F010为2026-W45已完成的价值权重、人类实质控制和数据生命周期专题，本轮只读。IDEA实际设备佩戴分布提醒未来研究区分分配使用权、真实使用量、客观结果和用户负担。历史设备及第三方网站删除完成情况UNKNOWN。没有新增F编号、实际安全测试或个人健康数据访问。

当前main在写入前查询到Actions运行0、check runs 0、combined status条目0；未主动触发CI。账户实际账单及Actions免费额度NOT_VERIFIED，故不运行潜在计费CI。GitHub提交需要完成后远端回读才能报告COMPLETE。

next_action: 若需要进一步研究IDEA，仅核对最早ClinicalTrials.gov登记历史、方案修订记录及是否实际发送差异化短信；若无法取得独立新证据，立即切换到非健康领域具有客观决策改善结果的独立产品实验。E继续跟踪R272生产权限及R333至R340验收调用；F本周只读。全部R系列完成前不开展统一分类、模型熔炼或个人决策产品开发。
