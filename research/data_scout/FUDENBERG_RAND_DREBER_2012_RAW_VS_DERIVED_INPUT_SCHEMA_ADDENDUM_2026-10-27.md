# A轨：FRD2012原始9列与派生10列的时间字段资格补充

日期：2026-10-27。状态：SOURCE_DOCUMENTATION_VERIFIED / RAW_BINARY_BLOCKED / LICENSE_PENDING / R073_DIRECT_FROZEN_TRANSFER_BLOCKED。承接research/data_scout/FUDENBERG_RAND_DREBER_2012_FRD2012_13126_SOURCE_GATE_2026-10-26.md。来源归属仍为Fudenberg、Rand、Dreber 2012同一真人实验，已出现在Nay/Vorobeychik复合数据的FR子集，不增加独立实验计数。

## 新核验

英文CRAN stratEst包当前参考手册明确区分原始FRD2012数据框9列与经stratEst.data变换后的data.FRD2012数据框10列。原始9列为treatment,id,game,period,choice,last.choice,last.other,bc,error。衍生10列额外增加input，取前回合自身与对手动作组合cc,cd,dc,dd；每一supergame第一回合input=NA。两者文档均声明13126行，仍是包文档声明而非本项目逐行实读。

原始文档：https://stat.ethz.ch/CRAN/web/packages/stratEst/refman/stratEst.html
派生字段说明：https://search.r-project.org/CRAN/refmans/stratEst/html/data.FRD2012.html
包手册及示例：https://cran.r-universe.dev/stratEst/doc/manual.html
原作者论文：https://doi.org/10.1257/aer.102.2.720
原始归档：https://www.openicpsr.org/openicpsr/project/112512/version/V1/view
此前固定衍生仓库Git提交c05aae64eadc8f5e2bbf8b98b14b884f5b393be7，data/FRD2012.rda blob 6b196ca1624081850b41dc2084c762257d59dd8f。

## 时间、许可和复现准备

input是历史行为的派生编码，不能当作新增独立测量变量。period是supergame内部回合，不能跨game使用前回合input。last.other为上一回合对手动作，当前对手身份ID、完整场次ID仍未在9列中提供。实施噪声可能要求进一步区分意图、实施和可见反馈，必须读取原作者说明及原始行数据才能确定。stratEst软件GPL-3许可不能自动证明真人行为原始数据的再分发许可。

本轮尝试GitHub公开原始RDA字节接口，但二进制响应不符合文本连接器限制，未解码26,923字节RDA。13126行尚未实数核验；没有下载、保存或再分发第三方真人原始数据。下一步：通过免费合法的二进制读取途径核验原始数据行、键(id,game,period)、回合边界、噪声语义和来源去重；核实openICPSR数据许可。R073原冻结FP/SP、100轮、12场和98评分目标与该六处理、变长supergame结构不一致，直接迁移BLOCKED。新增真人E2预测评分0，历史E3评分0，无新增费用。
