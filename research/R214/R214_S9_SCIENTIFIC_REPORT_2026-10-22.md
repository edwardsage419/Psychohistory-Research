# R214-S9 九世界离散断点设计独立补充研究结题报告

日期：2026-10-22。真实239目录 **09-005 Regression Discontinuity Design** 的**第三条独立研究分支**。原R214主研究12世界、192原噪声来源及R214-S2七世界、7168来源维持原样；本研究单独标记 **CLOSED_BOUNDED_E1_ARTIFICIAL_NINE_WORLD_RDD_SUPPLEMENT**，不新增原239目录条目。

## 计算前协议及方法依据

本次完全执行原已冻结的 [9世界576来源36外推协议](../../protocols/R214_RDD_9_WORLDS_576_ORIGINAL_SOURCES_36_LOCAL_EXTRAPOLATIONS_PRESCORE_FREEZE_2026-10-22.md)。该原协议独立于 R214 主研究与 S2，先于本次 Python 程序创建。本次不事后重设九个生成机制、R网格、U/E分布、四固定跨度或因果目标。

主要方法背景：Imbens and Lemieux (2008), *Regression discontinuity designs: a guide to practice*，DOI https://doi.org/10.1016/j.jeconom.2007.05.001；Lee and Lemieux (2010), *Regression Discontinuity Designs in Economics*，DOI https://doi.org/10.1257/jel.48.2.281。引用只证明方法依据，**本项目没有复现上述论文真实经验样本、最优带宽、密度检验或抽样方差**。

固定16个非零R位置 ±1/8 至 ±8/8；D=1{R≥0}；U为二元潜在基线类别（仅本预设“U可观测调整”特例把U当作数据），E为独立等概率±1，结果扰动E/4。九世界每世界16R×2U×2E=64条互斥人工原来源，合计576条；每世界源概率严格求和1。全部固定R位置距阈值至少1/8，**没有无限趋近阈值的实际观察支持**。

每世界4个h∈{1/8,1/4,3/8,1/2}，使用实际观测位置 ±h、±2h：最近距离局部常数差、左右两点线性截距之差、在U两类均有正支持时按共同P(U)=1/2标准化的条件线性差。合计36个“世界×跨度”比较；三个估计器各有36个数值。左右线性截距既经独立正常方程，也经2μ(h)−μ(2h)的Fraction恒等式检验。观察估计只用R、D、实际Y及声明可观测的U类别和来源概率；隐藏Y0/Y1仅用于计算真实oracle效果和误差。

## 完整来源结果

| 原人工世界 | 真τ(0) | h=1/8局部线性 | h=1/2局部线性 | 诊断 |
|---|---:|---:|---:|---|
| LINEAR_CONSTANT | 2 | 2 | 2 | 线性规格匹配 |
| LINEAR_EFFECT_SLOPE | 2 | 2 | 2 | 处理异质线性斜率 |
| COMMON_CURVATURE | 2 | 2 | 2 | 双侧相同二次曲率抵消 |
| DIFFERENTIAL_CURVATURE | 2 | 31/16 | 1 | 有限点外推偏差−4h² |
| BASELINE_JUMP | 2 | 3 | 3 | 未处理基线跳跃，偏差+1 |
| SORTED_LATENT_TYPE | 2 | 3 | 3 | 潜在类别选择偏差+1；可观测U标准化后为2 |
| DENSITY_JUMP_ONLY | 2 | 2 | 2 | 正/负R单点质量比3:1，仍无估计偏差 |
| PLACEBO_JUMP_NO_TREATMENT | 0 | 1 | 1 | 真实无处理效应，观察跳跃1 |
| TREATED_SIDE_CURVATURE | 2 | 63/32 | 3/2 | 单侧曲率造成偏差−2h² |

关键数学对比：离散R的有限两点线性外推即使在潜在Y0连续时，也可能偏离真实阈值因果目标。真实Y0突跳会让观察跳跃与处理效果混淆；固定可观察U且两侧都有支持时，标准化可消除本人工SORTED_LATENT_TYPE案例的组成偏差；不能推广到现实未测量的潜在类型。DENSITY_JUMP_ONLY中的R质量跳跃不必然构成未处理结果连续性失效，密度诊断不能代替机制识别。

## CI、来源复现与归档

* 程序：[r214_exact_nine_world_rdd.py](r214_exact_nine_world_rdd.py)。
* 全部原来源：[576条CSV](R214_S9_ALL_576_ORIGINAL_RDD_SOURCES.csv)。
* 全部外推：[36组CSV](R214_S9_ALL_36_LOCAL_EXTRAPOLATIONS.csv)。
* [完整九世界结果JSON](R214_S9_EXACT_RESULTS.json) 与 [机器SHA验收](R214_S9_FINAL_MACHINE_ACCEPTANCE.json)。
* [GitHub Actions run39786552882](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39786552882) 实际结束为 success；Python3.11与3.12各48单测通过，合计96测试执行；原来源生成及独立摘要复核的归档job也completed/success。
* 机器人真实主分支原CSV/JSON提交：[3b73602f](https://github.com/edwardsage419/Psychohistory-Research/commit/3b73602f026f85ef469b6e4f7eeee76340d80330)。三文件SHA256均已记录在机器验收JSON。此前R214主研究、R214-S2和R215结果没有覆写。

**科学边界**：全部是人工精确来源E1，新增真人E2=0，真实历史E3=0。不估计真实密度操纵、抽样噪声方差、带宽选择不确定性、估计极限、实际人类行为的外推或真实历史因果效应。R073和PESEN v0.1仍冻结。

原冻结“九世界576来源36外推”工作项现有独立执行证据及正式有界结题，与R214主研究和S2三个不同设计明确分离。后续继续原239目录中尚未完成的R项，之后统一分类，最后熔炼。
