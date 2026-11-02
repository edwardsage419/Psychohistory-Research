# MKT225 秘鲁财务日记应用现场随机试验：知识改善、储蓄无显著变化与信用使用增加

track: market
subflow: commercial_product_research + E_readonly_coordination + F_weekly_readonly
run_date_utc: 2026-11-02
local_date: 2026-11-02 Asia/Singapore
target_key: (market,Peru-financial-diaries-research-app,Frisancho-Herrera-Prina-2023-IZA16304,objective-credit-vs-saving-null-and-human-assisted-compliance)
observed_main_before_write: 96e23f3751e7a7c85d5cd81a032f8490ae9cad73
status: COMPLETE_BOUNDED_PRIMARY_FULLTEXT_REVIEW
market_evidence_grade: MARKET-E2_DIRECT_CLUSTER_RANDOMIZED_BUNDLED_INTERVENTION
market_evidence_scope: entire intervention bundle, not isolated app or personalized algorithm
original_participant_data_reanalysis: NOT_RUN
independent_native_app_execution: NOT_RUN
long_term_net_wealth_or_welfare: NOT_VERIFIED
new_R_E2_E3: 0
E_daily: E167_ALREADY_COMPLETE; THIS_RUN_READ_ONLY_INCREMENTAL
F_weekly: F010_ALREADY_COMPLETE; THIS_RUN_READ_ONLY
CI: NOT_RUN
billing_checked: ACCOUNT_BILLING_AND_FREE_QUOTA_NOT_VERIFIED
paid_actions: NONE
sensitive_personal_data: NOT_ACCESSED

## 研究问题与去重

MKT222至MKT224已覆盖未来自我图像和对话干预，本轮转向不同机制：连续自我记录加个性化反馈是否真正改善客观财务行为。此前MKT218涉及储蓄目标功能，MKT201涉及退休计算器；本研究的关键独有识别点是人工辅助录入、真实信用局行政数据、储蓄零结果和执行成本。该应用是2018至2019年真实运行的研究干预原型。当前是否作为独立商业产品对外提供、软件许可、开源源码及商业定价均未确认，不能宣称其为可购买现行产品。

## 直接阅读的免费原始资料

Frisancho, Veronica; Herrera, Alejandro; Prina, Silvia (2023). Can a Mobile-App-Based Behavioral Intervention Teach Financial Skills to Youth? Experimental Evidence from a Financial Diaries Study. IZA Discussion Paper 16304, July 2023, 56页英文全文：https://docs.iza.org/dp16304.pdf 。论文由 IZA 页面标记为2023年 Journal of Economic Behavior & Organization 214, 595至614的发表研究：https://www.iza.org/publications/dp/16304/can-a-mobile-app-based-behavioral-intervention-teach-financial-skills-to-youth-experimental-evidence-from-a-financial-diaries-study 。访问日2026-11-02。

本轮实际阅读原始PDF摘要、实验设计2.1至2.4、识别3、结果4及讨论5的文本。具体结果取自原文正文对Table 2、Table 3、Table 4、Table 5及附录的解释。未取得原始受试者数据或代码，未复算回归，未把作者表格解读称为独立重估。2023年发表版排印全文的所有表格未逐项核对，以下数值以公开IZA工作论文版本为准。

## 产品输入、状态、反馈及实际使用

处理组应用允许用户逐笔记录现金流，先选择收入、支出或金融工具，再选择收入来源、消费类别、存款、取款、借出、借入及偿还等子类。每笔记录包含金额、交易日期、录入时间。处理组在27周内产生17,204条财务交易记录。需要网络上传数据至研究服务器，日常离线录入可行。产品没有披露基于机器学习的个人收益预测算法，研究没有实施大语言模型建议。

处理组同时接受每两周一次的人工上门核账与补录，以及短信提供两周收支和储蓄摘要、继续记录提醒、下次上门安排。第四个月另发送一次消费类别饼图。对照组使用外观类似的饮食记录应用，收到提醒及一次初始安装访问。两组都得到每月约1美元手机流量奖励并有抽奖机会。因此随机分配识别的是整套财务日记、持续人工接触与个性化短信组合的效果，无法将效果单独归因于软件、自我监测、短信或人工帮助。

实验于2018年12月9日至2019年6月16日进行，27周。秘鲁Piura地区47所学校的390名毕业前学生参与，学校层面分层随机，处理组203人，对照组187人；982名符合智能手机条件的候选者中招募390人，存在招募及地域外推限制。财务知识与自报行为在干预结束约两个月后测量，信用局记录在2019年8月及2020年2月取得。

执行保真度是本轮重要发现。处理组第一个月约79%参与记录，后五个月约66%；研究后期多数交易由上门调查员录入。论文报告停止访问及激励后，处理组约60%自报每月至少继续使用四次。参与和记录完整性不能直接等同于用户自主持续录入能力。信用局的客观记录可帮助区分自报偏差。

## 随机试验结果与界限

作者报告的ITT估计：财务知识测验提高0.09个标准差；市场价格认知提高约0.32个标准差。预算行为、购物策略、是否储蓄及储蓄存款额均未确认显著改善。财务知识改善属于测验指标，不可直接作为财务福利改善。

信用结果：干预结束附近有未偿债务的概率提高约1.2个百分点。八个月后该概率差异方向相同，论文报告p约0.11，不能宣称持续的显著二元效果。八个月后未偿债务规模作者报告提高约16%，借贷机构数量增加。逾期借款概率与债务收入比没有确认显著变化。信用使用增加可能意味着获得正规金融服务的机会增加，也可能意味着负债暴露上升；未发现逾期差异不能证明不存在财务损害，亦不能证明借贷产生生产性收益。

作者报告先前没有接受学校财务教育者的财务知识改善约0.21个标准差，但两类人群之间的正式交互差异未能拒绝相等假设。应避免把组内显著与组间差异混淆。研究使用多重结果的sharpened FDR q值处理，同时包含TOT/LATE的工具变量估计；后者依赖额外识别假设，不能替代随机ITT。原始数据和完整预注册历史均未独立核查。

成本与可扩展性：论文Table 1正文报告，相对于对照饮食记录应用，处理干预的27周人均增量成本约185.3美元，约45%的处理实施总成本来自调查员工资与差旅。此为实验实施成本，不是应用售价。作者提出将来可能以其他方式减少人工成本，低成本替代方案尚未被这项试验证实有效。

## 对心理史学商业方法储备的具体含义

第一，未来个人量化系统须分离用户本人输入、人工代录、自动导入与回填的来源。完整交易日记可能掩盖自主参与度下降。

第二，未来评价需同时记录信息理解、真实行为、债务或其他副作用和长期净福利。不能以记录次数、测验提高、用户主观满意度代替净收益。

第三，存在人力支持时，必须单独记录实际交付成本及效果归因。纯软件复制研究中的组合效果需要新的随机实验。

第四，长期目标偏离控制应保留多目标冲突，尤其储蓄目标与信用使用、消费和流动性之间的权衡。本研究没有估计普适的最优目标权重。

证据等级为 MARKET-E2，仅限该历史随机组合干预。真实商业软件算法、跨国家长期复现、持续自主使用、客观净财富及总体人生福利均 UNKNOWN 或 NOT_VERIFIED。本研究不升级任何 R 系列 E1/E2/E3。

## E 只读科研治理检查

本地2026-11-02已有 E167 实质治理审计，本轮没有重复创建E编号或重复B数学验证。读取R272最新研究报告 R272_P0_EARLY_SUCCESS_BYPASS_IDENTITY_AUDIT_20261102T1444Z.md：候选强制工作流检查器只检查命令字面存在，无法保证命令实际可达。R/B在重构本地夹具中发现3/3 early exit变异被旧检查器错误接受，独立精确身份门拒绝3/3。原生产工作流仍未采用候选，完整真实checkout与Actions false-green测试未运行。R272 P0保持OPEN。该问题已由R/B直接登记，不重复提交同类P0通知或擅自修改工作流。

R333至R340组合门在最近R轨交接中为PARTIAL_P0_OPEN，真实完整checkout执行NOT_RUN，生产强制接入NOT_ESTABLISHED。R073与PESEN v0.1冻结保持。理论轨最新TH212交接只证明历史表格及精确算术，不能升级历史因果或R E3。

本轮重新读取GitHub pulls集合，12个open PR全部Draft，未合并；最近更新时间均为2026-10-29。PR #3 R257 S53严格门相对基线main diverged，main独有1189提交，PR独有1提交，来源身份与历史盲态仍待验收。PR #8和#9历史字节身份与排序依赖仍需分别审查。没有自动合并权限。

original239待核队列 Git blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f；crosswalk Git blob 36f24235901172642c46853298aebb421f1a3552，与上一轮相同。上次直接逐行核对为154项，P0 27、P1 82、P2 45；本轮依blob身份判断文件级净变化0，未重新逐行统计，也没有正式关闭任何项目。

## F 本周安全状态

2026 W45的F010已完成，本轮仅只读确认。此次研究涉及未成年人、家长同意、逐笔财务数据、调查员访问及信用局身份匹配，提示未来个人决策产品必须区分研究授权、数据录入代理、第三方信用数据处理和撤销范围。原始研究中真实数据的安全部署、删除完成和个人隐私合规没有在本轮独立审计。没有读取任何个人健康、财务或关系资料，没有新增F编号或实际安全测试。

## GitHub、CI与费用

写入前main 96e23f3751e7a7c85d5cd81a032f8490ae9cad73，已核对目标文件原先不存在。该HEAD的check runs和Actions runs查询均返回0；这不证明历史CI从未执行。没有触发任何Actions、购买论文、调用付费API或开通服务。GitHub账户真实账单和免费额度NOT_VERIFIED，故不启动可能计费CI。GitHub提交与远端回读结果需以实际写入后核验为准。

next_action: 商业轨优先寻找独立、纯软件条件下的预算记录随机试验，或比较该组合实验与已有Gimme5真实储蓄目标实验的行为终点及实施成本。E等待R272可达性检查、真实原生验收和R333至R340生产强制接入证据。F本周只读，R系列最高优先级与既定研究阶段次序不变。
