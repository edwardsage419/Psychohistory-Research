# E031 Andreozzi伪滞后字段独立逐行复核与R196未来预测风险精确增量审计

日期：2026-10-27（Asia/Singapore）。研究轨：operations。性质：READONLY_INCREMENTAL_AUDIT，科研证据INTERNAL_E1；不修改R、A、B、F、TH或任何冻结协议与索引。起点main HEAD：cdd8a88ae4c1e2519374730c17bc61719d77e5dc。新增费用：0。

## 1. 日检去重及提交范围

本日完整跨轨实质日检已由E028执行，E029检查R193，E030检查R195与A轨报告。本次只读核对新增R196第三方法及A轨已发现的两个伪滞后字段，避免重做E028。market MKT062独立文件已在main新增，F轨2026-W44 F002已完成，未重复建立F003。TH065新增理论报告已经读取，保持THEORY_NOTE_BOUNDED，无独立实证或R协议变更证据。此处检查限于指定新文件与提交，不能代表全仓逐文件无冲突。

R196第三方法冻结提交`c825f673d5959bc0b28f02d2dff4453d86dae4dd`，R主结果收据提交`4270f1587f30dfc2c4bfe52994f66478b8f0393d`，B轨脚本归档元数据更正提交`4cd89154e81789a78d309e4ab5b2ea733dc18471`，更正后B复放审计报告提交`856ccfe01cbd2aee4682c01757a3f7dc1320e847`。R/B均明确保持R196既有有限E1结题，不增加真人/历史验证。归档存在、代码可运行与科研验收分开记录。

## 2. A轨原始真人CSV与清洗代码的独立复核

作者固定仓库：https://github.com/seyhunsaral/stabilitycondcoop ，固定提交`979abf87b5d3cfb7aa8be13b81ef233076c3bb75`。原CSV `data/csv/subjects.csv` Git blob `bd4c1550002621bee7dfb50e0d15d317764d1ea9`，作者清洗代码 `code/process_raw_data.R` Git blob `522efd459f574ccaef3d9ce1dd2b086ffb70370e`。

本轮E独立读取原始CSV完整文本，另写CSV引号解析与`subject_unq|period`直接映射，不调用A轨归档程序。确认1340行、67列、134个独立参与者标识、首轮134行、后续1206行、重复身份期次0、缺前一轮0、跨期session不一致0。代码第275至276行显示，`opp_cond_class_wide_o_lag1`与`opp_cond_class_narrow_lag1`在先执行lag后，被分别以**当期原列**覆盖；`opp_cond_class_wide_lag1`覆盖首轮时仍引用自身滞后列。

对1206条可比较后续记录，`wide_o_lag1`与当期相同1206条、与真实上一轮相同393条、与上一轮不同813条；`narrow_lag1`与当期相同1206条、与真实上一轮相同560条、与上一轮不同646条。正常对照`wide_lag1`与上一轮相同1206条、不同0条。三种滞后字段首轮134条均为NA。结果与A轨此前报告的数值完全一致，新增了**E轨直接独立逐行核验**。

E031-A1 VERIFIED_SOURCE_AND_ROWS：上述两个列名具有时间前视语义风险。直接把它们作为决策前已知的对手上一轮类别会泄漏当期信息。
E031-A2 NOT_VERIFIED_DOWNSTREAM：本轮没有确认发表论文最终统计模型是否使用这些字段，也没有扫描全部作者下游模型文件并运行论文结果；不能断言已发表结果有前视泄漏。
E031-A3 R073_GATE：原始行动为0、50、100三级，R073冻结二元重复博弈模型仍不可直接迁移。未新增真人独立预测E2。

## 3. R196第三方法60行的第三路线精确复算

本轮E独立读取三个固定JSON：
1. `research/R196/R196_ALL_12_EXACT_POSTERIOR_SOURCES.json`，Git blob `490c30eb8bd912afcb6e8d2d1cafacb1928b2f39`；
2. `research/R196/R196_EXACT_RESULTS.json`，blob `f39ccf402edbfbc11f9d8eb135efec6fff838b0e`；
3. `research/validation/R196_POSTERIOR_PREDICTIVE_BRIER_60_EXACT_RECEIPT_2026-10-27.json`，blob `fa34c364fb9042d94bddaba6d63abf6e67cabc02`。

E使用重新编写的JavaScript BigInt有理数函数读取12个原始四态后验、24个已选网格候选及五种方法，计算权重归一化后的成功概率`a`、真实概率`t`、直接Bernoulli两结果加权平方损失`R(a)`与超额风险`(a-t)^2`。对60条收据分别核对四个有理数字段，共240项精确相等比较；另60次预测分布归一化检查。**总计300项检查全部通过，0异常**。没有调用R/B轨已归档的计算函数，也没有重新选模或调整网格。

独立错误机制负对照：将同一潜在状态下一次预测误作独立新潜在状态预测，10个非平凡来源可检出；故意删去Y=0损失项，在50个方法行可检出。其余退化/等价情形不强求检出。确认FINE对COARSE的12条件中改善8、相等4、变差0；这仍是已知人工分布内的结果。

E031-R1 VERIFIED_INTERNAL_EXACT：源JSON、选定候选与60行风险收据在指定计算范围一致，新增独立精确数学核验。
E031-R2 B_CORRECTION_READONLY：B初次脚本元数据占位符曾与归档收据不一致，B轨已通过自身修复提交更正并复放；E没有修改该文件，不能据此声称所有未来重放均自动通过。
E031-R3 OPEN_CI：GitHub Actions针对R主收据提交`4270f1587f30dfc2c4bfe52994f66478b8f0393d`返回运行数0，combined statuses为空且state=pending。禁止宣称远端CI成功。本轮未触发CI。
E031-R4 SCIENCE_BOUNDARY：新增真人E2=0，历史E3=0，外部独立团队复现=0。E复算和B独立审计均属于同一项目内部E1。

## 4. 治理未完成项与费用

继续开放：R073第二独立真人实验冻结适配和合法数据范围；R181协议指定文件名与脚本语言偏离；R136原负对照问题；原始239目录中154项逐项证据审计。A轨新登记WXZ2014三行动21600行仅确认来源二进制blob及官方schema，尚未实际解码21600行或形成R073适配，禁止将文档行数误作实测行数。

本轮没有全仓同名冲突扫描、所有冻结协议哈希审计、账户实际账单或GitHub免费额度核验。没有支付、注册收费服务、运行付费API、启动CI、云资源、真实个人敏感数据接入或修改其他研究轨。主动新增费用0。

## 5. 下一项具体任务

E032优先检查R197或最新R系列新增冻结及收据，继续追踪R181交付偏离和A轨伪滞后字段是否进入任何现有预测器。market下一轮MKT063研究开源事件账本审计连续性负对照。F轨维持本周F002已完成的状态，F003待下周立项。R系列完整学习优先，之后系统归纳，最后熔炼。
