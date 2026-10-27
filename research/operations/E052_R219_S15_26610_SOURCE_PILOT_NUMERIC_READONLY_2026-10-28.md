# E052 R219 S15 原始来源与pilot条件矩第三路线治理审计

日期：2026年10月28日（Asia/Singapore）。轨道 operations。性质：只读治理与数值独立复算。状态 SOURCE_LEVEL_NUMERIC_PASS。新增CI NOT_RUN。主动新增费用0。

## 起点与冻结范围

开始读取 main HEAD、MKT082、E051、F002、R219 S15冻结协议及正式收据、B轨审计、最新R221 S17协议和A轨数据准入。原R219六个人工世界与原239条目09-010保持原状态。

冻结协议 `protocols/R219_S15_INDEPENDENT_PILOT_PROPENSITY_PRESCORE_FREEZE_2026-10-27.md` 当前Git blob `061b8a35d576deee66b920073280cea481a1949d`，其冻结提交 `b32f8c39948c108d7daa502f5c23d9a2143c9225` 在S15正式计算前。原始CSV `research/R219/R219_ALL_1281_ORIGINAL_TREATMENT_ASSIGNMENT_SOURCES.csv` 当前Git blob `fa14af5a46694c6cc23717f8e9ee9fa2acb9501d`，与冻结协议声明一致。S15正式收据 `research/validation/R219_S15_INDEPENDENT_PILOT_12_CONDITION_EXACT_RECEIPT_2026-10-27.json` blob `a91efbfcc5dfe03f7f9cb5df25bb291b7ff6a793`。

## 本轮独立执行

使用 `research/operations/e052_r219_s15_source_pilot_numeric_20261028.js`，只依赖Node标准库。程序独立读取1281行原始人工赋值来源及正式S15 JSON。对每行核查八个Z、Y观察值与潜在结果对应、完整赋值位掩码、Bernoulli赋值概率、人工ATE及世界概率质量；重新从四个pilot位置的真赋值概率构造16种pilot概率，并从预定平滑公式求e_hat。再用逐单位独立Bernoulli条件矩和全方差公式复算160个有支持pilot条件的均值、方差和MSE，32个无原始共同支持pilot条件保持null。复核12项世界与平滑强度汇总及原公共已知倾向基线。

实际执行 **26610项数值与结构检查，失败0**。原始来源1281行，世界6个，支持pilot条件160个，阻塞pilot条件32个，有效pilot与未来赋值组合槽40960个。比较容差为相对 `1e-9`，属于数值复算，不能标记为严格有理数逐字段一致。R原程序使用逐赋值有理数枚举，B原程序使用Bernoulli条件矩。本轮额外逐行检查原CSV一致性，条件矩公式与B轨存在数学同源性，因此是第三个程序检查路线，不构成完全独立科学证据。

重要结果保留：CORRECT_X人工世界α=1时pilot未来MSE=575/128，已知公共倾向基线=17/6；WEAK_OVERLAP世界α=1时MSE=833717/524288，基线=257/30，伴随估计偏差；POSITIVITY_FAILURE世界所有平滑仍拒绝数值因果估计。这些均限于人工E1。

## E轨跨任务治理

最新R221 S17冻结协议当前blob `53d60b205e1bc9e4e17f8e39ebaf09453356f24f`。GitHub提交显示新增1/8、3/8误分类率的冻结协议于2026年10月27日15:41:32 UTC提交 `e6e892d639b06342b87129d622b574c888d5faed`；正式结果于15:44:20 UTC提交 `1c7c74af582e9cdcf9c329519c2281216ae2dcfc`，15:45:06 UTC另有收据排序及字段补齐提交 `b67ec418f4e9d2fbe0b00149066ea89519bc5ea6`。协议明确0、1/4、1/2属于提交前探索，不可称全五率预注册。R221 S17原R/B内部人工E1核验保留，不能升为E2或E3。对正式结果提交查询GitHub Actions head_sha返回total_count=0，CI不宣称成功。

R073冻结双人100轮协议仍没有因A轨三人40轮OpenNeuro数据而新增合格评分；A轨许可冲突继续阻塞。R074、R075、R077已有三个不同真人实验的内部E2评估继续保留。R136、R181、R214 S10旧问题开放。原R/B/A/TH研究、协议、共享索引未改动；没有对仓库未检验部分作全覆盖通过宣称。

## F本周及费用

2026年第44周F002已完成，当前目录只有F001和F002。本轮不重复新建F专题。F003计划下周研究错误偏好归因、派生记忆证据及人工纠错。MKT083的无偏好状态被强行拟合列入F轨候选风险。没有访问真实个人敏感数据。

本轮只使用已连接GitHub读取、公开英文官方文档、现成离线计算。没有启动CI、使用收费API、购买服务或租用计算资源。GitHub整体账单和免费额度未独立核验。下一E053优先核查R220 S16独立pilot两种nuisance估计的冻结负对照，及R221 S17最新修正收据的一致性。
