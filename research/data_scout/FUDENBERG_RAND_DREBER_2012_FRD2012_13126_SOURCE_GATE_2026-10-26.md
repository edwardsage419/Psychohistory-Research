# A轨：Fudenberg、Rand、Dreber 2012真人重复博弈数据的原始来源与字段资格登记

日期：2026-10-26。状态：PRIMARY_PUBLIC_ARCHIVE_AND_DERIVED_SCHEMA_VERIFIED / RAW_BINARY_NOT_DECODED / R073_DIRECT_FROZEN_TRANSFER_BLOCKED。与此前已登记的Nay、Vorobeychik 2016复合NV_games区分，严禁把其FR子来源重复计为新独立实验。

## 来源及可获得性

一手论文：Fudenberg, Rand and Dreber (2012), *Slow to Anger and Fast to Forgive: Cooperation in an Uncertain World*, American Economic Review 102(2):720–749, DOI https://doi.org/10.1257/aer.102.2.720 。论文明确讨论重复囚徒困境与实施动作噪声。原作者复制包公开索引 https://www.openicpsr.org/openicpsr/project/112512/version/V1/view ，记录2019-10-11归档，项目 DOI https://doi.org/10.3886/E112512V1 。本轮该网页进一步访问出现403，因此原包具体文件字段及许可证尚未读取。

可复核衍生数据来源：作者之外的公开R包 https://github.com/fdvorak/stratEst ，本轮固定master提交 `c05aae64eadc8f5e2bbf8b98b14b884f5b393be7`。实际通过GitHub原生目录接口核验 `data/FRD2012.rda` Git blob `6b196ca1624081850b41dc2084c762257d59dd8f`，26,923字节；通过GitHub原生文件接口读取 `man/FRD2012.Rd`。衍生R二进制在本轮GitHub读取接口触发UnicodeDecodeError，**未取得完整行数据，也未完成真实行数复算**。

## 已实际核验的文档字段

包作者正式字段说明声明13,126条真人逐回合决策、9列：`treatment`（六个处理），`id`（参与者），`game`（supergame），`period`（supergame内回合），`choice`（当期合作/背叛），`last.choice`（前回合自身动作），`last.other`（前回合对手动作），`bc`（收益比），`error`（噪声）。上述行数和字段为**文档声明**，尚未经过本项目逐行实读。该数据提供了R073独立来源所需要的多次博弈、时间与个人身份信息，但没有在九列中明确提供当前对手ID、实验场次ID或当前对手动作；`game`与`id`的组合是否能构造独立留出场次仍需核验。实施噪声意味着还须区分意图行动、实现行动及实际可见反馈的时间顺序。

同一研究已作为Nay/Vorobeychik 2016 `NV_games`复合数据的FR成分出现。其衍生汇总不能视作新的独立实验，也不能在训练集包含FR成分时再次将FRD2012作为独立测试集。

## 许可、R073资格与后续操作

stratEst包公开软件许可为GPL-3，无法直接证明2012年原作者真人数据的全部再分发权限。openICPSR的项目级许可证尚未读取。无需付费注册的数据可用性仍待原始压缩包或R包原始字节实读确认。下一步应在无费用前提下读取固定RDA字节、逐行核验(id,game,period)唯一性、回合断点、历史字段、噪声动作语义和训练测试来源重叠；核实原作者许可证及实验场次标识。

R073冻结的FP/SP两处理、12独立场次、100轮和98评分目标与FRD2012六处理、变长supergame结构不同，直接迁移资格为BLOCKED。任何新的真人E2评分必须另行事前冻结不同协议，明确原R073评分不可冒充同口径复现。新增E2=0、E3=0，R073与PESEN v0.1保持冻结。没有购买、收费API、注册或读取私人数据。
