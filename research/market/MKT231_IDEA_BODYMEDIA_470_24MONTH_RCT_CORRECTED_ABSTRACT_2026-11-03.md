# MKT231：IDEA试验的长期客观结果、可穿戴反馈与原刊更正

track: market
subflow: commercial_product_research + E_daily_readonly + F_weekly_readonly
run_date_utc: 2026-11-02
local_date: 2026-11-03 Asia/Singapore
target_key: (market,BodyMedia-FIT-Core-IDEA,NCT01131871-2016-JAMA-corrected,24month-objective-weight-vs-web-self-monitoring+transposed-abstract)
baseline_main_before_write: 0e23670b4f808e10d366aa0bcba84bad7f2822c5
status: COMPLETE_BOUNDED_PRIMARY_ARTICLE_AND_FORMAL_CORRECTION_AUDIT
evidence_grade: MARKET-E2_DIRECT_HISTORICAL_HUMAN_RANDOMIZED_TRIAL
current_product_availability: NOT_VERIFIED
independent_participant_data_reanalysis: NOT_RUN
original_protocol_and_registry_version_history: NOT_VERIFIED
production_device_algorithm_replay: NOT_RUN
long_term_general_life_welfare: NOT_VERIFIED
new_R_E2_E3: 0
ci: NOT_RUN
billing_checked: ACCOUNT_BILLING_AND_ACTIONS_FREE_QUOTA_NOT_VERIFIED
paid_actions: NONE
personal_sensitive_data: NOT_ACCESSED

## 一、去重和问题

已有MKT198/MKT211研究Fitbit Zip在TRIPPA的800人随机试验，观察6个月激励与12个月活动和健康指标。本轮改审另一产品、另一独立样本及24个月客观结果：BodyMedia FIT Core上臂可穿戴反馈与研究网站自我记录的随机比较。两项试验不合并样本，不宣称对2026年Fitbit或其他现代设备的直接因果验证。与MKT225财务日记、MKT229/MKT230承诺机制的目标键也不同。

## 二、历史产品的真实使用机制

IDEA试验先为全部参与者提供6个月共同的饮食、运动和群体辅导。自第7个月起，标准组通过研究网站主动录入饮食和活动；增强组使用BodyMedia FIT Core多传感器上臂设备及厂商网站记录能量消耗、活动和饮食，设备小屏幕及网站提供反馈。两组继续接受月度小组辅导、每月短电话和每周短信，均有行为干预。研究者可在电话辅导时访问相关记录。

输入：传感器测量的活动与能量消耗，用户录入饮食。
状态：每日活动和饮食监测，研究阶段的体重等独立评价。
目标：研究规定的饮食和活动目标；未见原论文证实设备具备个体最优目标的预测能力。
反馈：设备显示、厂商网站及共同的人类辅导。
算法：多传感器能耗估计和网站反馈的完整源代码与校准数据未取得。
商业：FIT Core是历史商业设备；2026年是否仍可购买或订阅、历史价格及许可没有独立确认，均不使用或购买。
隐私：设备及研究网站可记录行为与饮食，历史服务的删除、撤销、备份政策本轮未取得；没有读取私人健康资料。

原刊方法明确为上臂BodyMedia FIT Core。不能把它替换为Fitbit、智能手表或当前AI教练。对照组也进行网站自我追踪，所以识别的是在共同辅导背景下“设备与配套界面”相对“网站自我记录”的增量效果，不能解释为自我追踪相对完全不追踪的效果。

## 三、随机试验与24个月结果

Jakicic et al., JAMA 2016, 316(11):1161–1171, DOI 10.1001/jama.2016.12858。2010至2012年招募471人，开始干预并纳入分析470人：标准组233，增强组237；年龄18至35岁，入组BMI为25至小于40。第24个月体重由研究评估测量，属于客观结果。

| 已更正的正式论文指标 | 网站自我记录标准组 | FIT Core增强组 |
| --- | ---: | ---: |
| 基线平均体重 | 95.2 kg | 96.3 kg |
| 24个月平均体重 | 89.3 kg | 92.8 kg |
| 24个月模型估计平均减重 | 5.9 kg | 3.5 kg |

增强组比标准组少减重2.4 kg，95% CI 1.0至3.7 kg，p=0.002。两组均出现减重，研究主要假设所期望的设备增量改善没有得到支持，观察到的方向相反。不能用组间差值称“设备让所有用户增重2.4 kg”，也不能断言其他设备会出现同一效果。

第24个月仅74.5%有体重数据。原论文使用线性混合模型，在观察到的数据条件下假定缺失随机，并用多重插补作敏感性分析。若失访并非随机，估计可能偏倚。论文报告两组体成分、体能、活动及饮食均有改善，但未发现相应指标的显著组间差异；不能把这些次要结果解读为健康损害已确认。

## 四、实质来源一致性问题：原刊正式勘误

JAMA于2016年10月11日正式发表更正《Transposed Data in Abstract》，DOI 10.1001/jama.2016.15063，明确说明2016年9月20日原刊摘要正文与表格的24个月两组体重被对调。更正后的数值为标准组89.3 kg，增强组92.8 kg。原刊页面还记录2016年9月22日线上修正。原始未更正PDF或其文本抽取可能保留错误组别配对，不能据此反转结论。

本轮以JAMA现行HTML原文Table 2和正式更正页为组别身份基准，独立做公开均值的简单算术5.9减3.5等于2.4。没有从原始参与者数据重建混合模型、置信区间或p值。此处“独立”仅指公开数值核对，不代表独立团队复现。

## 五、研究可用性与限制

1. 随机比较具有较强因果识别，但试验包含共同辅导，设备于第7个月加入，不能隔离佩戴、网站、反馈、使用依从性及行为替代各自的单独作用。
2. 论文约四分之一缺少24个月体重，缺失随机假设需要保留。研究没有无干预组，不能把两组各自减重全部归因于干预。
3. 结果属于特定年轻成人、2010年代上臂设备、特定生活方式干预；当前设备世代、一般人生选择、长期整体福利与其他文化环境的外推保持UNKNOWN。
4. 研究注册号NCT01131871由原刊报告，原始注册时间戳、预设分析版本历史及参与者级数据本轮未直接取得，故不能宣称完成注册一致性复核。
5. 原论文披露研究者与体重管理和设备企业的历史合作/资助关系；试验由美国NIH/NHLBI资助。利益披露不能替代偏倚审查，也不自动推翻结果。
6. MKT198/MKT211 TRIPPA是另一随机试验：Fitbit Zip组12个月活动量相对对照改善，仍未发现体重或血压等健康改善。两项试验共同说明“记录或活动量变化”与“客观下游结果”应分别测量；不可跨试验直接合并效应量。

MARKET-E1：历史商业设备及反馈机制来自原刊方法描述，非本轮生产执行。
MARKET-E2：2016年直接真人随机试验，24个月客观体重结果和正式勘误，限历史试验。
MARKET-E3：跨产品长期人生福利改善和当前AI建议效果，NOT_VERIFIED。
R E1/E2/E3：N/A，本轮新增均为0。

## 六、E每日治理与F本周状态

E168于本地2026-11-03已完成实质只读审计，本轮仅交叉检查。写入前main为0e23670b4f808e10d366aa0bcba84bad7f2822c5。R/B新增R127 original239 05-003的有限独立精确数学审计：本地三种Python模式21次单测通过，但原始1990论文Table 2没有在该轮重新独立逐格核对，正式队列仍PARTIAL。该审计不得自动减少P0或升级真人证据。original239待核CSV blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，crosswalk blob 36f24235901172642c46853298aebb421f1a3552，均与E168一致；文件级净减少0。该快照的历史154项，P0 27/P1 82/P2 45，本轮未重新做完整科学逐项验收。

当前12个开放Codex PR均为Draft，未合并。PR #3 head 97d5f74df5d84916917db943156120f08144f445 相对本轮main比较为diverged，main独有1218提交，PR独有1提交；mergeable元数据不能代替来源/盲态审查。PR #8/#9仍未合并，保留R170历史字节身份依赖。R272生产YAML blob 3132b08cf4ee64b55f5112d2249894ea0ec9d42d未变化，仍包含contents:write、先--emit后assert及自动git push，单入口验收候选尚未接入，P0 OPEN。R333至R340组合强制接入未取得关闭证据。R073及PESEN v0.1冻结不变。没有跨轨改写、PR合并或生产Actions操作。

F010为2026-W45已完成的价值权重、实质人类控制与数据生命周期专题。本轮只读关联一项安全边界：行为记录频率、设备依从性、客观结果和潜在负担应分别披露；历史BodyMedia数据删除的实际完成情况UNKNOWN。没有新增F编号，没有实际安全测试或个人敏感数据访问。

## 七、原始来源、费用与下一步

访问日期：2026-11-02 UTC，公开英文来源。

1. JAMA 2016完整在线原文，直接审阅方法、Table 2、缺失数据、限制、利益披露：https://jamanetwork.com/journals/jama/fullarticle/2553448/
2. JAMA 2016正式更正，直接核对两组体重对调和正确映射：https://jamanetwork.com/journals/jama/fullarticle/2556196
3. NIH PubMed原始摘要交叉核对：https://pubmed.ncbi.nlm.nih.gov/27654602/
4. 研究注册入口，原始历史版本未核实：https://clinicaltrials.gov/study/NCT01131871
5. 仓库已归档对照：research/market/MKT198_FITBIT_TRIPPA_RANDOMIZED_INCENTIVE_WITHDRAWAL_2026-11-01.md 和 research/market/MKT211_TRIPPA_FITBIT_REWARDS_WITHDRAWAL_OBJECTIVE_RCT_2026-11-02.md。

没有注册产品、购买设备、付费访问论文、读取个人资料或主动触发Actions。当前main提交的Actions运行查询为0；这不能穷尽所有类型CI。账户账单和Actions剩余免费额度NOT_VERIFIED。

next_action: 优先寻找IDEA原始注册历史及24个月设备使用依从性公开数据，确认是否可审查实际使用差异。若没有合法免费资料，转向非健康领域具有客观下游结果和真正独立实验的决策工具。E继续跟踪R272生产写权限及fail-closed强制接入，F本周只读。全部R模型完成前不启动统一分类、模型熔炼或个人决策产品开发。
