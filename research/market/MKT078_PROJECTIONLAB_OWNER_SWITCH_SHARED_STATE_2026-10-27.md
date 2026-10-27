# MKT078 ProjectionLab 个人与伴侣模式切换的财务状态归属及跨计划残留

日期：2026-10-27（Asia/Singapore）。轨道：market。状态：COMPLETE_BOUNDED_VENDOR_DOCUMENTATION_AND_SYNTHETIC_CONTRACT。主动新增费用：0。CI：NOT_RUN。

## 1. 预检、去重与研究问题
预检main HEAD为3d55bd86d39058db8aa7aefe6a040aa44599c332，market至MKT077，operations至E046，F002本周专题，最新R215-S11及B轨审计。MKT002/MKT027/MKT028讨论模拟采样与支出；MKT044研究动态与固定计划的时间归因；MKT045研究进度点的历史编辑。此次专门研究2026-09-29官方公开的「从伴侣模式切回个人模式」状态清理语义，以及2026-09-08 Current Finances 的跨计划继承边界。未复用既有合成反例。

## 2. 英文官方来源及已明确支持的机制
S1：ProjectionLab官方帮助《Switching Between Individual and Couple Planning》，2026-09-29，https://projectionlab.com/help/switching-between-individual-and-couple-planning 。从Couple切回Individual后，原伴侣独有账户及双方共同账户仍保留余额，但Owner字段清空；这些余额仍计入净资产等总量，直到用户手动处理。伴侣工资、社保等收入流仍保留于计划，需要用户逐项删除。伴侣Medicare支出则自动移除。反向从个人切为伴侣时，需检查账户归属。
S2：官方《How to Update Current Finances》，2026-09-08，https://projectionlab.com/help/update-current-finances 。Current Finances不是某个计划，标准计划从中同步账户余额及删除；具有自定义起始条件的计划不继承这些更新。余额更改可自动生成Progress Point。
S3：官方《How do I update account balances and check progress over time?》，2026-06-16，https://projectionlab.com/help/update-account-balances 。用户可编辑、复制和删除进度点；没有公开完整事件日志的可回放保证。
S4：官方《Security》，2026-08-12，https://projectionlab.com/security 。厂商声称Firestore存储、TLS、静态加密、MFA、可导出及删除。SOC2 aligned属于厂商控制表述；云供应商认证不等于产品本身认证。
S5：官方价格 https://projectionlab.com/pricing ，2026-10-27读取。Basic $0/年，Premium $129/年，Pro $549/年。Multiple Plans、Compare、What If和Downloadable Reports列在Premium。项目未注册免费账户，也未启用付费功能。

## 3. 新增机制及人工状态机
官方明确的状态转换是：规划身份Couple→Individual，伴侣及共同账户Owner清空但余额保留，伴侣收入不自动移除，伴侣Medicare自动移除。模式切换与经济归属清算具有不同的操作范围。可能出现净资产、收入及支出清理不对称的过渡状态；厂商文档没有声称系统自动完成所有关系财务分割。

人工合成数据：本人账户80000、伴侣账户50000、共同账户100000；伴侣工资60000/年、伴侣社保24000/年、本人收入30000/年；伴侣Medicare人工6000/年。切回个人模式后模拟官方所述规则，净资产仍为230000，其中150000处于Owner空白；伴侣收入84000/年仍在计划，Medicare移除。若研究者定义仅本人独有资产为80000，未清理总量与此人工口径相差150000。共同账户实际权益划分未知，不能把150000解释为真实多计金额或厂商财务错误。

对照一个标准计划与一个自定义起点170000的计划：删除Current Finances中共同账户后，人工标准计划继承的资产和变为130000，自定义起点仍170000。该演示只覆盖文档的继承契约，没有运行厂商财务引擎、税务算法、实际同步或多计划权限。

离线Node.js标准库脚本 research/market/mkt078_projectionlab_owner_switch_synthetic_20261027.js 已执行33项断言，失败0。包含Owner清空、余额保留、收入残留、Medicare清理、标准与自定义起点差异、源数据不变。脚本没有真实个人信息、网络请求、令牌或付费依赖。

## 4. 产品机制矩阵
真实输入：用户录入账户余额、账户Owner、伴侣身份、工资、社保、Medicare与其他现金流，可选插件同步。
状态表达：Current Finances共享账户及Owner、个人/伴侣模式、标准计划和自定义起点、计划内收入支出、Progress Point。
算法：模式切换下不同字段的保留/清空/删除规则有官方文档；完整预测税务和账户模拟代码未核验。
目标：由用户设定财务目标及情景，计划比较依赖当前账户与现金流口径。未提供统一人生效用权重。
反馈与修正：用户可手动审阅空Owner账户、删除伴侣收入、修改余额并观察进度；文档未证明会自动发现全部归属矛盾或执行统计误差校准。
隐私权限：共同资产及伴侣收入涉及第三人数据；账户Owner字段为空并不证明数据已删除或撤销处理授权。厂商云端安全为自述，未独立测试。
解释性：官方帮助给出字段级迁移规则；未证明自动生成可追溯的模式切换事件链、用户确认差异清单及历史评分版本。
费用：Basic免费，Premium和Pro收费；本项目仅免费阅读。
局限：人工金额不是真实用户，真实家庭产权/税务规则依赖法域，模式切换的因果效果、真实产品回归测试和用户长期决策收益均未验证。

## 5. 候选知识储备及风险
MKT078-C1：未来模型若支持关系状态切换，须分别核对规划身份、资产权益、账户归属、收入归属、费用归属、第三人授权及各计划起点；Owner=null应进入待核队列。
MKT078-C2：每个共享状态变更生成受影响计划清单和输入差异，区分同步计划与自定义起点，并保留原始版本及人工批准。
MKT078-C3：共同账户不得因模式切换而自动断定所有权，提供未知/争议状态及人工决定权；不预设任何个人效用权重。
MKT078-C4：对伴侣资料的撤销、保留、清除及派生预测失效使用F002的来源依赖和生命周期候选控制，保留外部副本未知状态。
风险R1 HIGH：规划身份已改变但旧资产及伴侣收入仍影响未来预测。R2 MEDIUM：标准计划与自定义起点受更新影响不同，跨计划结果可失去可比性。R3 HIGH：第三人财务信息的处理目的和权限状态未随身份切换重新核对。均为条件性研究风险，未声称厂商存在漏洞。

证据等级：VENDOR_DOCUMENTED，SYNTHETIC_CONTRACT_33_ASSERTIONS，UNVERIFIED_PRODUCT_RUNTIME。归档等级MARKET E1；无新增真人E2、历史E3或独立长期效果。F002已完成2026-W44，本轮只登记后续候选，不重复立项F003。

## 6. 下一项
MKT079优先核对ProjectionLab官方个人/伴侣转换的收入残留与Owner空白是否存在公开回归测试或变更日志；若无，转向ARDA或Dcider的目标状态及人工确认机制。绝对零新增费用。
