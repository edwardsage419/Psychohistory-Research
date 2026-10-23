# R296 科学报告：02-001 Rescorla–Wagner 复合线索共享预测误差、阻断和解除阻断

日期2026-10-23 Asia/Taipei。原始239目录候选ID 02-001（P1），对应新独立研究R296。**仅正式结题有限人工数学E1，不包括原作者动物学习实验E2、真人学习复现或历史E3。** 原始目录与此前研究冻结协议均无改变。

## 原作者、方法及已有R系列的区别

Rescorla, R. A. & Wagner, A. R. (1972), *A Theory of Pavlovian Conditioning: Variations in the Effectiveness of Reinforcement and Nonreinforcement*, in Black & Prokasy (eds.), *Classical Conditioning II: Current Research and Theory*, pp.64–99，Appleton-Century-Crofts。[原作者 Allan Wagner 耶鲁官方发表记录](https://wagner.yale.edu/publications)与[原始章节扫描版](https://www.columbia.edu/~rk566/Session4/Theory%20of%20Pavlovian%20Conditioning.pdf)。核心机制是一起出现的线索共享复合结果预测误差，使已学到的A影响后加入B的可学余量。

R065等先前研究中存在强化学习或估值机制，但本轮只从原目录02-001逐项建立来源证明，**不重复归入原作者七模型的独立真人预测结果**，更不把该源级人工机制视为另一个人类独立实验。

[R296事前完整冻结协议](../../protocols/R296_RESCORLA_WAGNER_BLOCKING_UNBLOCKING_40_SOURCE_PRESCORE_FREEZE_2026-10-23.md)，GitHub[78e947a3](https://github.com/edwardsage419/Psychohistory-Research/commit/78e947a3de8dbeb209edc473ae74f98eb6937904)。在模型源码与结果写入前提交。

## 完全人工研究世界与数学机制

人工线索A和B的联结强度初始0，两种线索相同学习率α∈{1/4,1/2}，结果学习敏感度β=1。条件A-only预训练0或8次，每次奖励目标λ=1；然后AB复合线索获得奖励目标λ=1或2，追踪m=0、1、2、3、4各状态。

一共2×2×2=**8个人工世界**，每个五个m状态，**40条完整人工source行**，不是40名人或40次动物原实验。每个AB试次的Rescorla–Wagner更新：

ΔV_A=α(λ−V_A−V_B)，ΔV_B=α(λ−V_A−V_B)。

为了隔离预测误差共享的机械效应，另构造同试次独立误差负对照：ΔU_i=α(λ−U_i)，i=A,B；它不包含线索间的联结预测竞争，且本研究并未声称它是原作者采用的另一个成熟心理学模型。

令p=1−(1−α)^n_pre，任意m的解析精确解：

* RW_B=(λ−p)/2·[1−(1−2α)^m]；
* RW_A=p+RW_B；
* RW_A+RW_B=λ+(p−λ)·(1−2α)^m；
* 独立误差对照 IND_B=λ·[1−(1−α)^m]，与是否预训练A无关。

两套不同路径验证这些等式：正式程序逐次递推，同时独立解析计算；第三来源审计完全不导入正式程序，再逐次递推并计算闭式式子。

## 冻结的实验负对照与真实人工计算结果

| 学习率α | 预训练A | AB奖励λ | 4个复合试次后RW_B | 同条件独立误差IND_B |
|---|---:|---:|---:|---:|
| 1/4 | 0 | 1 | 15/32 | 175/256 |
| 1/4 | 8 | 1 | 98415/2097152 | 175/256 |
| 1/4 | 8 | 2 | 1081455/2097152 | 175/128 |
| 1/2 | 0 | 1 | 1/2 | 15/16 |
| 1/2 | 8 | 1 | **1/512** | 15/16 |
| 1/2 | 8 | 2 | **257/512** | 15/8 |

* **Blocking：** A单独预训练后，在AB复合条件中预测奖励的主要部分已由A解释，故B剩余增量更小。α=1/2时，A预训练8次后p=255/256，随后AB奖励1使B=1/512；无预训练时B=1/2，两种学习率均出现同方向差异。
* **Unblocking：** 在相同的8次A预训练后，把AB奖励目标从1提高到2重新引入更大预测误差，B在α=1/2时达到257/512。两种学习率均满足高奖励使B大于常规奖励。
* **独立误差负对照：** IND_B仅依赖自身AB接触和奖励，和先前A训练无关。α=1/2、λ=1、m=4时IND_B一律15/16；该负对照不呈现相同预训练阻断。
* **边界：** α=1/2使复合学习第一个AB试次后共享预测误差准确归零；后续试次不再改变RW联结。人工目标为2时负对照IND_B允许大于1，这只是强度模型数值，不能视为二元概率。

上述结果是研究者选择的人工参数和目标增强反例；真实条件反射、抑制、动物个体差异、试次间潜在遗忘和条件性行为表达均未被拟合或验证。本轮没有计算原始1972实验任何效应量，也不保证模型能解释所有已发表的blocking/unblocking实验。

## 源码、真实CI及科研验收

[主程序及211项实际模型单元测试](r296_exact_rescorla_wagner.py)；
[40条全部原人工模型状态CSV](R296_ALL_40_ORIGINAL_RW_CUE_BLOCKING_STATES.csv)；
[8世界所有训练节点与闭式对照结果](R296_EXACT_BLOCKING_UNBLOCKING_RESULTS.json)；
[原来源/结果SHA256凭证](R296_MACHINE_RECEIPT.json)；
[第三方独立40源和14项篡改检验](../catalogue_audit/independent_r296_source_audit.py)。

[GitHub Actions run39920891647](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39920891647)三job completed/success：Python3.11和3.12各211项主单测、14项独立审计通过；第三独立作业重建40原始状态、闭式与递推并核查SHA，源文件永久归档于[commit8133120b](https://github.com/edwardsage419/Psychohistory-Research/commit/8133120bc6b4270b13bc60ad472e4f643ec33ae8)。

正式结论：**CLOSED_BOUNDED_E1_ARTIFICIAL_R296_RW_CUE_COMPETITION**；真实人E2=0，真实动物E2=0，历史E3=0。R073与PESEN v0.1继续冻结；未完成全239候选逐项科学检验之前不开始统一分类与模型融合。
