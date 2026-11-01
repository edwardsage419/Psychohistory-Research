# MKT210: DecisionTwin 公开源码中的决策翻转、置信度与许可边界

track: market
subflow: 真实个人决策产品机制与可验证性
run_date_utc: 2026-11-01
local_date: 2026-11-02 Asia/Singapore
target_key: (market,DecisionTwin,SEJUNK/DecisionTwin@b83c18d91d4edcc11123f7b7839fc8f428753cc1,local-flip-confidence-heuristic-license-evidence)
baseline_main: 8ea62f122651666628c5100893e791ebf1791f32
status: COMPLETE_BOUNDED_STATIC_SOURCE_AUDIT
evidence: MARKET-E1_DIRECT_PUBLIC_SOURCE_INSPECTION; MARKET-E2/E3_PRODUCT_OUTCOME_NOT_VERIFIED
runtime_test: NOT_RUN
synthetic_counterexample: STATIC_ALGEBRA_ONLY
live_ai_call: NOT_RUN
paid_api_or_hosted_service: NOT_USED
sensitive_personal_data: NOT_ACCESSED
new_R_E2_E3: 0
CI: NOT_RUN
billing: NOT_VERIFIED

## 研究对象与公开源码身份

研究对象是2026年8月9日建立的公开个人决策模拟器 DecisionTwin，作者仓库 https://github.com/SEJUNK/DecisionTwin ，固定 main commit `b83c18d91d4edcc11123f7b7839fc8f428753cc1`。只读核对 README、TECHNICAL_ARCHITECTURE.md、src/lib/decision.ts、src/lib/decision.test.ts、src/App.tsx、backend/app/schemas.py、backend/app/services/decision_service.py 和示例数据。

产品输入是二选一问题、2至10项因素、每项1至10的重要性权重及可选自由文本背景。服务端通过 OpenAI 或 Azure OpenAI 的结构化输出产生每项因素对两个选项的评分和线性情景参数。浏览器内的 What If 计算对两个变量 monthlyCost 和 commuteTime 进行本地确定性重算。该产品目前只有两个显式可调模拟变量，未证实可泛化为任意多维人生情景。示例背景包含收入和储蓄信息，真实私人数据无需在研究阶段输入。

仓库 README 明确说明没有 LICENSE 文件，属于个人项目，默认保留作者权利。代码公开可读不等于已获得再分发、修改或商业使用许可。服务端真实生成需要外部 AI API 凭证，本项目零新增费用规则下不调用、不部署、不复制第三方代码。

## 静态源码发现一：分数和置信度不是预测校准

`calculateDecision` 对因素分数做加权平均，乘10后四舍五入形成0至100的选项分数；平分时默认选A。所谓本地 confidence 由两项分数的绝对差乘3再加58，最后限制在54至92之间。该数值是工程启发式，无公开真实决策结果、预测正确率、可靠性图或概率校准依据。分数差为0时也显示58%的confidence。

`ResultsScreen` 优先显示 AI 输出的 recommendation 和 confidence；两个选项的数值评分却来自本地 `calculateDecision`。当AI给出的推荐与本地加权赢家不一致时，当前所读前端片段没有显示一致性阻断。后续 `SummaryScreen` 改用本地 winner 和本地 confidence。由此，同一输入在不同页面可能显示不同来源的推荐与置信度。源码阅读证明存在来源切换，尚未用实际UI执行证明用户可触发该冲突。

服务端 `DecisionService` 验证 AI 推荐必须属于提交的两个选项，验证每项因素存在，未检查 AI 推荐与前端本地加权赢家相等。这是具体的未覆盖一致性约束，不表示实际已有错误用户案例。

## 静态源码发现二：翻转阈值的扫描域固定

`findFlipCost` 总是从5000到30000以500为间隔扫描，并把第一个与当前赢家不同的成本值作为翻转点；扫描范围没有读取AI返回的 monthlyCost min/max/step。模型本身允许不同的合法范围。

构造一个仅用于静态推理的合法两因素模型：成本变量 min=40000、max=60000、step=5000、default=50000；成本因素初始两个选项都为5，A每步增加1，B每步减少1；第二因素两个选项都为5且不随变量改变。两因素等权重。默认成本50000时两个选项平分，规则选择A；合法成本40000时B获胜。扫描器从5000开始，其传入值被另一个函数截断至40000，因此第一步就可能返回5000作为翻转点。5000位于声明的合法成本范围之外。该反例直接由源码条件与算术推出，没有执行第三方程序，也没有证实生产环境真实AI会返回此特定模型。

另外，`describeDecisionFlip` 将移动幅度占变量范围的比例最大者称为驱动变量，未使用各变量对选项分差的实际边际贡献。因此较大的无效移动也可能被命名为翻转原因。SummaryScreen 还以与flipCost距离是否小于4500作为最敏感因素的启发式判断；这不是经验证的敏感性分析。

## 现有测试、证据等级及产品对照

仓库有手算预期值的 Vitest 测试，涵盖默认模型、边界、NaN、两变量变化和已知翻转；本轮实际只读测试文件，未运行 Node、Python、联网服务或真实AI。现有测试的可见用例未覆盖上述跨页面AI与本地赢家一致性、动态成本范围阈值、置信度校准和驱动因素归因。测试覆盖判断仅限所读文件。

相对 Dcider 的未披露权重评分，DecisionTwin提供可检查的本地算术与因素加权机制，且提供用户可调的反事实界面。相对 ProjectionLab 的财务情景概率，它的confidence并无可确认的概率解释。相对 Beeminder 的真实目标轨迹，它没有已验证的行为反馈闭环或实际人生改善评价。该产品的直接真人随机试验、长期决策改善和跨文化公平证据均未发现，不能将源码可复算等同于结果真实有效。

证据分类为 MARKET-E1 公开实现静态核对。没有新MARKET-E2/E3真实效果证据，也不改变R系列的E1/E2/E3。

## E只读治理与F本周状态

本地2026-11-02的E167已完成实质治理审计，本轮只做增量只读核对。当前main `8ea62f122651666628c5100893e791ebf1791f32` 相对MKT209提交 `8a88b82d23c1d15843840ce0d622ca3749ee1837` 前进6个提交，内容为R257 S53独立几何投影E1、非凸世界审计、TH205及交接。R257 S53历史盲态顺序FAIL、正式验收PARTIAL；R333至R340组合门的完整原生执行和八份工作流强制接入仍开放。original239待核队列 blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`、crosswalk blob `36f24235901172642c46853298aebb421f1a3552` 未变化，文件级净关闭0。154项及P0=27/P1=82/P2=45为该固定blob对应的队列快照。

本轮重新读取GitHub pulls集合，12个open PR均为draft，merged_at为空。PR #1旧比较器错误接受和PR #3严格数学门候选仍未合并。PR #3相对本轮main的比较结果是main独有1120提交、PR独有1提交，来源认证和历史盲态仍待独立审查。此处的版本差异本身不能证明合并冲突。没有自动合并、重写冻结协议、修改R/B文件或替代B数学复算。

F010在2026-W45已经COMPLETE，本轮只记录可供未来审查的风险：未经校准的百分比confidence可能引发自动化偏见；不同页面结果来源不一致会损害知情决定；发送可选背景到云端AI需明确授权和最小化输入。未新建F编号，未执行安全部署或读取个人敏感数据。

## 下一步及成本

市场优先查找真实产品的外部独立使用结果，或进一步审阅其他开放实现中可证明的阈值与建议一致性机制。DecisionTwin仅可继续公开只读研究；若未来涉及复用源码，应先取得明确许可。E优先R333至R340完整原生组合门与强制接入，R257 S53历史盲态失败独立处理。F本周只读。GitHub Actions没有主动触发；账户账单与免费额度仍未独立核验。R073及PESEN v0.1继续冻结，个人决策产品正式开发仍暂停。

## 原始公开来源

https://github.com/SEJUNK/DecisionTwin/tree/b83c18d91d4edcc11123f7b7839fc8f428753cc1
https://github.com/SEJUNK/DecisionTwin/blob/b83c18d91d4edcc11123f7b7839fc8f428753cc1/src/lib/decision.ts
https://github.com/SEJUNK/DecisionTwin/blob/b83c18d91d4edcc11123f7b7839fc8f428753cc1/src/App.tsx
https://github.com/SEJUNK/DecisionTwin/blob/b83c18d91d4edcc11123f7b7839fc8f428753cc1/src/lib/decision.test.ts
https://github.com/SEJUNK/DecisionTwin/blob/b83c18d91d4edcc11123f7b7839fc8f428753cc1/backend/app/services/decision_service.py
https://github.com/SEJUNK/DecisionTwin/blob/b83c18d91d4edcc11123f7b7839fc8f428753cc1/README.md
