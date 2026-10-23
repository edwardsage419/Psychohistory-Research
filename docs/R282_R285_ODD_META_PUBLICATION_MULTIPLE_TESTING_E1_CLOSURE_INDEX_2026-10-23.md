# 心理史学R282—R285：ODD开放复现、系统综述模拟、发表选择与多重比较，四项连续有界研究归档

日期2026-10-23 Asia/Taipei。原239研究目录最后四项12-012至12-015依序完成：R282 Open Reproducible Workflow and ODD（P0）、R283 Systematic Review and Meta Analysis（P1）、R284 Publication Bias Diagnostics（P1）、R285 Multiple Testing Correction（P1）。每项事前冻结研究协议，在人工完整原概率空间执行标准库程序、原来源精确穷举与独立数学路线、Python3.11及3.12真单测、GitHub Actions第三独立来源审计、完整原CSV/结果JSON/SHA256永久机器人入库，之后归档科研报告和有界验收。

## R282 ODD2020七要素与执行时序复现
[事前冻结](../protocols/R282_ODD_SEVEN_ELEMENT_3_SCHEDULE_192_COMPLETE_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [独立七要素文档和全研究入口](../research/R282/README.md) · [科学报告](../research/R282/R282_SCIENTIFIC_REPORT_2026-10-23.md) · [机读正式验收](../research/R282/R282_FINAL_ACCEPTANCE_STATUS.json) · [CI run39906210132](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39906210132) · [原来源永久归档0933b552](https://github.com/edwardsage419/Psychohistory-Research/commit/0933b552515950afb016fa647cf1c16d0d7c89fc)。

两agent、两轮固定6bit原输入，三不同更新日程各完整64种来源，共**192个带日程标识人工来源类型**。三种调度t2最终群体分布完全相同，但同一原来源下的SYNC与两个顺序日程t2状态有48/64不同；执行顺序必须明确归档才能真正同源复现。七标准ODD2020部分、零实证数据/零PRNG声明、完整轨迹、独立闭式位公式以及负向缺失章节测试全核验。两个Python版本各114项真正unittest，**共228通过**，三CI job success。内部ODD七标题审查不等于出版物标准第三方认证；实际人工E1，无真实E2或历史E3。

## R283 全纳入人工研究汇总与选择性择优
[事前冻结](../protocols/R283_THREE_STUDY_FIXED_EFFECT_SYNTHESIS_192_COMPLETE_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [原来源与执行入口](../research/R283/README.md) · [科学报告](../research/R283/R283_SCIENTIFIC_REPORT_2026-10-23.md) · [正式机器验收](../research/R283/R283_FINAL_ACCEPTANCE_STATUS.json) · [最终CI run39906571655](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39906571655) · [来源永久归档6b4f0e1a](https://github.com/edwardsage419/Psychohistory-Research/commit/6b4f0e1adb42484eaa55c5eebf08ee47f9421e13)。

三个虚构study每项只有1个处理与1个对照bit，三真实DGP×每world64个原source，共**192个人工来源类型**。采用已知人工真DGP方差的oracle逆方差权重，完整纳入全S1/S2/S3，并用Cochran Q和错误的只挑最大study效应作比较。真正同质世界全部汇总真效应1/2，posthoc只报最大study均值469/512；异质世界正负抵消全部真汇总为0，但挑最大study均值175/256。全来源与独立3³=27研究风险差组合及E[Q]闭式完全一致。没有真实文献检索与系统综述，不能当真实元分析结论。Python双版本各99项真测试共**198通过**，三job最终success。首次[CI失败run39906498127](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39906498127)因第三独立审计的zip参数遗漏，修复后原协议和数学未变；失败历史保留不计为成功。

## R284 选择性发表及完整人工登记册
[先行冻结](../protocols/R284_PUBLICATION_SELECTION_3_POLICIES_768_COMPLETE_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [完整原来源执行器](../research/R284/README.md) · [科学报告](../research/R284/R284_SCIENTIFIC_REPORT_2026-10-23.md) · [正式机器验收](../research/R284/R284_FINAL_ACCEPTANCE_STATUS.json) · [CI run39906691468](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39906691468) · [原来源机器人提交dfd95dcc](https://github.com/edwardsage419/Psychohistory-Research/commit/dfd95dcc386a6b0c83e87689b708f83df9de13d4)。

四个虚构study各一条公平结果Y与一条公平披露bit R，三披露政策完整共享256原source，共**768个人工来源类型**。四研究真实登记册平均阳性率1/2：完整公开条件阳性率1/2、只公开阳性1、偏好公开阳性2/3；完全无公开的来源概率分别0、1/16、1/256，均明确记录NULL，禁止偷偷删掉。全来源与独立单研究概率计算一致，双Python各100测试共**200通过**，三job success。人工已知选择机制不是现实已发表文献所存在发表偏差程度的实证检测。

## R285 Holm和BH两种错误控制目标
[事前冻结](../protocols/R285_TWO_HYPOTHESIS_HOLM_BH_2304_COMPLETE_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [完整源码与原source](../research/R285/README.md) · [科研报告](../research/R285/R285_SCIENTIFIC_REPORT_2026-10-23.md) · [正式机读验收](../research/R285/R285_FINAL_ACCEPTANCE_STATUS.json) · [成功run39906881178](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39906881178) · [机器人永久原数据归档41643378](https://github.com/edwardsage419/Psychohistory-Research/commit/41643378604f670fc72234ab608965422c2f4e60)。

两独立假设各四bit，三真原假设组合×未校正/Holm/BH三政策，共**9人工world×每world256原source=2304完整原配置**。冻结仅作数学对比的α=1/2（非现实研究推荐阈值）下，BOTH_NULL未校正FWER135/256，Holm31/256，BH47/256；其中真假设全部成立时FDR=FWER。ONE_SIGNAL与BOTH_SIGNAL各有预冻结的错误发现/真发现准确质量，完整原source和独立5×5二项类别逐Fraction相同。两Python版本各80真测试，**共160成功**，三job success。不能把有限人工例子的数值当作所有依赖和alpha下的普遍统计检验定理。

## 四项研究汇总与目录边界
|项目|R282|R283|R284|R285|合计|
|---|---:|---:|---:|---:|---:|
|人工世界或政策机制|3|3|3|9|**18**|
|带模型标签完整人工source|192|192|768|2304|**3456**|
|双Python真测试通过|228|198|200|160|**786**|
|最终成功CI jobs|3|3|3|3|**12**|

四项每个均有事前冻结commit、完整来源CSV、解析结果、机器SHA256凭证、科研报告、正式验收及第三GitHub Actions独立来源审计，全部最终三job completed/success；另R283历史首次失败CI如实留存，不混计成成功。3456是共享原空间且包含政策重复的**人工有标签来源配置**，不等于独立实验数，更非真人观察。全部科研证据仅人工E1，本轮新增真人E2=0、历史E3=0，R073和PESEN v0.1冻结。

**重要：原239目录最后一项R285的完成不能等于239原目录全部模型已实证结题。** 全系列需要随后以唯一`docs/MODEL_CANDIDATE_CATALOG_v0.1.json`和R208/R209历史目录映射勘误为基准，逐原条目审计实际映射、存在性、源码、正式验收和证据边界，之后才能考虑统一归纳分类、最后模型熔炼。
