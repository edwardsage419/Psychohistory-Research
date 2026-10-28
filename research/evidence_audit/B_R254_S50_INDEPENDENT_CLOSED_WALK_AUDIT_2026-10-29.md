# B轨：R254 S50签名三角图独立闭游走与轨道复算

日期：2026-10-29。审核目标为[先行冻结S50协议](../../protocols/R254_S50_SIGNED_ODD_WALKS_PAIRED_SOURCE_PRESCORE_FREEZE_2026-10-29.md)，冻结提交 `864438580f388aeacb8dc545bf692bc99b2faa89`。原R254人工E1模型和原始正式验收均保持不变。

## 两种独立数学计算路线

R轨 [r254_s50_paired_signed_trace_20261029.py](../validation/r254_s50_paired_signed_trace_20261029.py) 从六bit构造每条边阈值，计算3×3矩阵乘积的trace和递推 `x_{n+1}=Ax_n`，覆盖512个外生配对及n=0..3。

B轨 [b_r254_s50_independent_closed_walk_oracle_20261029.py](b_r254_s50_independent_closed_walk_oracle_20261029.py) 通过顶点walk的乘积求和计算每个状态坐标 `sum_paths prod(edge weights)×seed[end]`，并枚举全部闭合walk直接计算 `tr(A²),tr(A³),tr(A⁴)`。B轨没有导入R轨脚本、调用R轨矩阵乘法或读取其内部状态。独立对每个六bit源验证 `tr(A³)=6abc`，随后和R轨的机读收据比较。

## 实际执行

在本地Python命令行先运行R轨生成 [精确收据](../validation/R254_S50_PAIRED_SIGNED_TRACE_RECEIPT_2026-10-29.json)，再运行B轨。B轨重新计算512对×4时点×3坐标×2符号世界 = **12288个状态坐标**，与R轨在7个汇总字段上的精确结果一致，字段包括三阶迹不相等配对数、偶次迹配对一致数、四时点向量不等数、三个谱迹期望和边mask计数。全部比较通过。

执行一次负例：将收据中的n=3不等配对数从200人为改为999，B轨比较器确实抛出不一致并拒绝该伪造结果。独立分析同时确认n=1差异条件概率 `(1/2)×(3/4)=3/8`，与R轨192/512相符。

## 证据边界和后续缺口

状态：`INTERNAL_INDEPENDENT_WALK_ORACLE_PASS`。属于同一项目内不同数学算法的程序性复核，**外部研究团队独立复现为0**。所有输入为冻结E1人工外生bit及seed组合。原R254完整18432行CSV只读核对了远端blob和正式报告SHA元数据，未能在本轮取得完整CSV字节并重新逐行比对；这一验证缺口仍为OPEN。没有真实独立样本、经验样本外预测、概率校准、重采样置信区间或现实因果识别。没有将四时点当作独立观测，也没有将原R254的历史成功CI视为本轮S50新增代码的CI通过。R073及PESEN v0.1继续冻结。
