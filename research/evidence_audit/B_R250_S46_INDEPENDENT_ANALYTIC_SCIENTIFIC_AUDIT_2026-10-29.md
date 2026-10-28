# B轨 R250 S46独立闭式Fraction科学审计
日期：2026-10-29。事前协议 `1c50aef1dd9068e6110e487bbfb8d53f9f1f82cc`。R轨读取原始576行CSV并按观察边分组。B轨 `research/evidence_audit/b_r250_s46_fraction_analytic_20261029.py` 完全独立使用链与三角的有限Bernoulli闭式公式，未调用R轨函数或原CSV。
实际本地Python命令行执行独立脚本，九世界解析结果如下：CHAIN_P_QUARTER: F0=15/256, F01=3/64, gain=3/256; CHAIN_P_HALF: F0=3/16, F01=1/8, gain=1/16; CHAIN_P_THREE_QUARTER: F0=63/256, F01=9/64, gain=27/256; TRIANGLE_P_ZERO: F0=0, F01=0, gain=0; TRIANGLE_P_QUARTER: F0=135/1024, F01=27/256, gain=27/1024; TRIANGLE_P_HALF: F0=1/4, F01=3/16, gain=1/16; TRIANGLE_P_THREE_QUARTER: F0=135/1024, F01=27/256, gain=27/1024; TRIANGLE_P_ONE: F0=0, F01=0, gain=0; TRIANGLE_STATIC_TRUE_GRAPH_REPORT_ALIAS: F0=1/4, F01=3/16, gain=1/16。
R轨已在隔离V8实际读取GitHub原CSV执行5787项确定性断言，0失败。B轨45项世界名、F0、F01、收益、全边支持数比较均一致，0失败。人为将三角p=1/2的收益改为999，比较器成功拒绝。精确概率恒等式检查不能代替真人样本外预测、概率校准、分场次重采样或独立外部复现。
泄漏边界：F01仅含观察Y01；Fall使用全部边并确定观察目标，因此零风险仅为确定性信息上界。将目标本身作为特征属于非法未来信息泄漏。伪报告世界的真实连通率0，观察目标率1/2，须分开报告。当前为项目内部不同算法及不同语言的程序性复核，外部独立团队复现0，E1证据。
待补：GitHub原CSV的完整Node.js命令行重跑与新增CI，均不能在无费用确认前擅自触发。无新费用。
