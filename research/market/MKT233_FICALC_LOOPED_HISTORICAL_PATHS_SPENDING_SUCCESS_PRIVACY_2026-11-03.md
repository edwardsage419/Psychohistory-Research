# MKT233: FI Calc 历史循环路径、支出成功定义及分享链接隐私审查

track: market
subflow: commercial_product_mechanism_and_external_validity
run_date_utc: 2026-11-02T23:24Z
local_date: 2026-11-03 Asia/Singapore
target_key: (market,FI-Calc,current-public-docs-2026-11-03,looped-history-vs-actual-history+spending-success-definition+shared-url-data)
baseline_main: 1c3c3dc18bf66f1864178a25ec1bb975a8821e20
status: COMPLETE_BOUNDED_PRIMARY_DOCUMENTATION_AND_LOCAL_SYNTHETIC_ARITHMETIC
evidence_grade: MARKET-E1_OFFICIAL_DOCUMENTATION
independent_peer_reviewed_context: 2003 Cooley/Hubbard/Walz abstract only; NOT product validation
production_source_audit: NOT_RUN
production_simulation_execution: NOT_RUN
real_user_decision_improvement: NOT_VERIFIED
participant_data: NOT_ACCESSED
new_R_E2_E3: 0
CI: NOT_RUN
account_billing_and_free_Actions_quota: NOT_VERIFIED
paid_operations: NONE

## 1. 去重与研究问题

先核对 main、MKT232、E168、F010、R/B 最新 R257 S53 交接、理论 TH218 交接、原239 队列和交叉索引、开放 PR。MKT232 已审计旧版 cFIREsim 的 145 年/116 个完整30年窗口及其旧源码版本断层。市场既有 MKT200–202 已登记退休计算器随机试验，不能作为 FI Calc 产品专属因果效果。本轮目标是**现行 FI Calc 官方明确允许的循环历史序列**及其成功判据与输入数据暴露，避免重复旧版 cFIREsim 研究或将不同产品效果混为一谈。

## 2. 真实产品机制、费用与可复核范围

官方 https://ficalc.app/about 声明 FI Calc 免费、接受自愿捐助，提供历史回测工具，明确不提供投资建议。官方 https://ficalc.app/docs/configuration/historical-data 明确采用 1871–2024 年度历史数据，可限制起止年份，默认使用所有可用年份。输入包括退休期限、初始组合、股票/债券/现金、年度提款策略、额外支出与收入。官方 https://ficalc.app/docs/withdrawal-strategies/ 列举 Constant Dollar、VPW、Guyton-Klinger、95% Rule、CAPE-based 等策略；各策略的年度反馈规则有公开文字说明。用户可调整假设并比较各历史路径，查看资产、可用支出、历史回报，导出 CSV/Excel。

官方 https://ficalc.app/docs/usage-guides/export-columns 描述输出的79个固定年度列及可扩展收入/支出列，并明示年初发生收入与支出、期末应用投资增长、费用与再平衡。该文档区分“资金耗尽”和“无法满足请求支出”；其 **Simulation Successful?** 以整个模拟期限内请求支出是否得到满足为准。账户耗尽后仍可能由其他收入覆盖支出。跨产品比较成功率前必须统一失败定义，不能把该判据直接视为 cFIREsim 旧版“任一年资产小于零”判据。

目前取得的是生产产品官方方法、导出字段和隐私文档。没有获取 FI Calc 生产算法固定源码、部署版本身份、真实完整 CSV 输出，也没有执行线上计算器。因此具体生产成功率、源码与文档一致性均 NOT_VERIFIED。官方没有披露经过独立前瞻校准的个人未来成功概率。

## 3. 循环历史路径的可复核数值影响

官方 https://ficalc.app/docs/configuration/historical-data 明确：启用“Loop historical data”时，模拟达到所选历史数据末年后，从首年继续；可在设置中关闭。官方特别提示，最近年份接最早年份是**模型构造的序列**，并非真实连续历史。官方文档描述该设置可关闭；本轮未运行UI确认当前生产默认开关的实际状态。

使用官方列出的1871至2024共154个年度键，假设每个起始年份均构造30年路径，纯整数年份的本地 Python 标准库枚举与断言得到：

| 路径类型 | 数量 | 计算 |
| --- | ---: | --- |
| 不跨末端、完整30年历史窗口 | 125 | 154−30＋1 |
| 允许末端回绕的30年起点路径 | 154 | 每个年度各作为起点 |
| 需要跨越2024→1871接缝的路径 | 29 | 154−125 |
| 回绕路径占所有循环路径 | 18.8312% | 29/154 |
| 相邻30年路径共享年份 | 29/30 | 96.6667% |

首个跨缝起点1996，序列1996…2024→1871；最后一个跨缝起点2024，序列2024→1871…1899。以上为**条件算术**，仅适用于所述154年、30年、每年一个起点的路径构造。它不代表从 FI Calc 线上导出的实际路径计数，也不证明默认设置、内部排除规则或资产模拟执行结果。若生产软件采用其他过滤或设置，实际数量可不同。

研究解释：循环模拟使不同期限拥有相近数量的起始场景，但部分场景含人为历史接缝。即使未循环，相邻30年窗口也高度相关。不能把154条路径当作154个独立、同分布的未来退休实验，也不能把历史成功比例自动提升为个人未来成功概率。比较两种配置的成功率，需要先固定输入、年份区间、失败定义、路径长度和循环开关。

独立学术背景：Cooley, Hubbard & Walz (2003), *A Comparative Analysis of Retirement Portfolio Success Rates*, Financial Services Review 12(2):115–128, DOI 10.61190/fsr.v12i2.4759，期刊免费英文摘要明确比较重叠历史时期与 Monte Carlo，在某些条件下结果差异很大。仅核对了摘要，没有逐格审阅全文或复算其数值；该研究也未直接检验 FI Calc。https://openjournals.libs.uga.edu/fsr/article/view/4759

## 4. F本周安全专题的关联增量，未新增F编号

官方 https://ficalc.app/privacy （本轮2026-11-03读取）声明计算器输入在浏览器处理；如创建账户，账户信息及保存的计算会存储；分享URL可能包含输入，并被托管商、站点服务和链接接收者获得；Google Analytics 接收包括页面URL在内的使用信息，因此可能接收编码在URL中的计算参数。**浏览器内计算不等于所有输入及元数据均不离开浏览器。** 这是官方政策披露，实际网络流量、第三方接收、删除及撤销范围均未实测。F010 2026-W45已完成，保持 COMPLETE；本轮仅向未来隐私评估提供具体风险例子。

## 5. E治理只读检查与证据边界

2026-11-03已有E168实质审计，本轮不重复新增E编号。当前 main 基线1c3c3dc18bf66f1864178a25ec1bb975a8821e20，比MKT232提交769e3fd87af5e5226e9c0942b3efac83031a6612新增4提交，涉及R/B R257 S53独立几何验证与理论TH218。R/B最新报告记载8个凸世界的232项精确比较一致、7项篡改拒绝；其历史盲态顺序FAIL仍在，完整科学验收PARTIAL，R E2/E3新增0；不能将此提升为R正式闭合。

本轮直接查GitHub开放PR列表，#1–#12均为open Draft；#3、#8、#9均未合并。#3相对本轮main diverged（main独有1230提交、PR独有1提交）；PR #8/#9历史收据身份依赖未解决。原239队列Git blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，crosswalk blob 36f24235901172642c46853298aebb421f1a3552，均与E168一致，文件级净减少0；154/P0 27/P1 82/P2 45为该文件既有计数，本轮未重新逐行复核。

R272现行生产YAML blob 3132b08cf4ee64b55f5112d2249894ea0ec9d42d，仍具有contents:write、--emit先于内联assert检查和自动git push路径，且未见强制调用新单入口；P0保持OPEN。R333–R340生产强制调用未取得新的闭合证据。未改写生产工作流、冻结协议、共享索引或PR；R073和PESEN v0.1保持冻结。

## 6. 科学等级、费用、下一步

MARKET-E1：官方现行公开产品文档、隐私政策和可导出字段。LOCAL_SYNTHETIC_ARITHMETIC：154年、125个完整窗口、29个跨缝窗口、154个循环起点的条件整数枚举。MARKET-E2/E3（FI Calc产品专属真人决策改善/长期净福利）：NOT_VERIFIED。R E1/E2/E3新增：0。没有真实个人数据、登录、购买、付费API、云/GPU或Actions调度。GitHub账户账单与Actions免费额度未验证，故CI保持NOT_RUN。

next_action: 若有可公开验证的现行生产版本或免费可导出样本，比较固定参数下循环开关的实际输出与支出成功定义，并保存完整来源版本。优先转向能观测真实用户损失、错误避免或长期决策改善的产品，避免继续以历史模拟器窗口计数制造新编号。E等待R272真实完整checkout、权限与强制验收接入的R主线owner审查；F本周只读。
