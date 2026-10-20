# R149 增量补充研究：结构化理论双向回写、共同冲击及资源支持

该独立模型的计算前协议于 `70b4bcf48ca698a525de0d8d110403f843d84bf5` 入库，早于所有计算及源码归档：[结构化理论24模型事前冻结协议](../../protocols/R149_GIDDENS1984_SEWELL1992_STRUCTURATION_RECURSIVE_AGENCY_STRUCTURE_PRESCORE_FREEZE_2026-10-20.md)。与同阶段[41项测试主线](README.md)明确区分：本增量采用**24组不同的有限人工状态机**，不把其结果与另一个模型的第8期统计量相加、也不取代41项主线。

本模型有两名行动者、结构状态0–4、六个年度、资源开关0/1、共同冲击概率0或1/2、结构反馈开关0/1、初态0/2/4。24=2×2×2×3种固定参数；每一情景下每年的两人A行动概率在同一期共同冲击Z给定后条件独立：P(A0=1|s,Z)=(1+s+resource+Z)/8，P(A1=1|s,Z)=(2+s+Z)/8。共同资源及结构约束决定行动概率，随后当期2人共同实践数量更新下年结构；关闭回写则结构保持不变。原创结构化理论示范，并非Giddens或Sewell原著数学公式。

精确Fraction穷举结果：条件独立的两行动者即使没有直接模仿，也会因为共同年冲击呈现当期采纳协方差 **1/256**。两种同样行动多重集合却顺序不同的历史：从结构0出发，先均A再均B到终态0，先均B再均A到终态1，体现边界与时序交互。对于冲击概率1/2的各12场景，额外穷举每期64条冲击序列并精确核对与前向概率分布和期望行动总量吻合。

完整 [77个原生Python unittest及全部结果JSON可复算ZIP](R149_Giddens_Sewell_Structuration_77_Tests.zip)，原文件SHA256 `f1c042fd39182326a09be53f74f7b295fe83cad27b5c8cff8df7d1126695aee6`，ZIP Git blob `c4172127ce15c6ba4bf5c24b580e791ecdf0f04c`。原程序SHA256 `60a79eff858ae8299557cdf467d73c05e15e257f3ec62b9129e5e11d6e3a2f36`，测试 `4f5dcb5e24825d893a73de5fcf671868f1d38de9392dc61750891fc69bc1ec52`，原结果 `50477e084b04a2b72422d73f7ce1fda535cad9819ffc6456f818ef5219c62cdb`。使用 `python -m zipfile -e R149_Giddens_Sewell_Structuration_77_Tests.zip out` 解压，在独立目录运行 `python -m unittest -q test_r149_structuration_exact.py` 和 `python r149_structuration_exact.py > replay.json`。**须真实双Python GitHub CI通过之后标记正式验收。**

仅项目自建理论 E1，未读取原作者连续历史数据、没有新的真人外部验证E2或历史预测E3。
