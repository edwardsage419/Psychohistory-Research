# R199 隐马尔可夫时间序列：完整可见预测、Viterbi及逐时隐后验解码

2026-10-21。原239目录P2/08-023 HMM Time Series。状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_HMM_SEQUENCE_DECODING**。

[原始计算前冻结协议](../../protocols/R199_HMM_24_WORLDS_2064_TRAINS_PRESCORE_FREEZE_2026-10-21.md)固定二元隐藏状态、二元噪声观测、六人工已知参数HMM：BASE(a3/4,r3/4)、LABEL_SWAPPED(a3/4,r1/4)、IID_HIDDEN(a1/2,r3/4)、SWITCH_HIDDEN(a1/4,r3/4)、WEAK_SIGNAL(a3/4,r5/8)、STRONG_SIGNAL(a3/4,r7/8)。隐藏初始公平1/2，轨迹长度L3/4、独立训练轨迹m1/2，共**24人工世界、2064完整有序原观测训练序列组合、196唯一可见拟合profile、144候选×可见序列隐藏后验配置**。前向PMF递推与所有潜在状态路径完整Fraction求和全等，前后向逐时隐后验与完整潜在路径状态边际全等，Viterbi max-product整条最可能路径与独立全部潜在路径穷举argmax逐路径全等；原训练likelihood直接逐轨迹相乘和Counter计数指数算法相等。训练只用可见完整序列似然六固定候选择优并用真正独立新序列全观测对数预测评分、仅给前缀预测末观测Brier，math.log/70位Decimal及两套Fraction Brier全一致。

**核心结果**：BASE和LABEL_SWAPPED完整可见观察分布每状态逐Fraction完全一样，所有隐藏状态posterior严格互补，故训练候选并列时按BASE优先，LABEL_SWAPPED作为工作候选从来没有选出；两真实源的所有可见未来分数相同，但人工真潜在标签评分相反。L4、m2源BASE与LABEL_SWAPPED新可见完整序列loss同≈2.791243、末观测Brier同≈0.252627，而工作选择器给出的人工真隐藏整条Viterbi标签正确率分别≈28.84%与**1.02%**。全部144种模型/可见序列解码中Viterbi全路径MAP与逐时边际MAP实际**54例不同**。准确预测可见数据不等于识别潜在类别的语义身份，真实人群没有真隐标签时不能把人工oracle评分冒充实证。

[正式科学报告](R199_SCIENTIFIC_REPORT_2026-10-21.md)、[24世界预测/人工真标签评分](R199_EXACT_RESULTS.json)、[2064完整原有序训练CSV](R199_ALL_2064_ORDERED_OBSERVED_TRAINING_SETS.csv)、[196精确完整拟合配置](R199_ALL_196_OBSERVABLE_FIT_PROFILES.json)、[144完整各时点隐后验/Viterbi路径](R199_ALL_144_OBSERVABLE_HIDDEN_DECODINGS.json)、[机器验收](R199_FINAL_MACHINE_ACCEPTANCE.json)、[原生40单测源码](r199_exact_hmm_sequence_decoding.py)、[原协议和全部源码/结果七文件ZIP](R199_Exact_24_HMM_Sequence_Worlds.zip)永久入库。[GitHub Actions39593984143](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39593984143)双Python各40项单元测试共80次、第三完整人工原样本与未来预测科研验收，三个job全success；[实际数据提交cc464dc4](https://github.com/edwardsage419/Psychohistory-Research/commit/cc464dc45c7b7583a4da091fc70ec9d108dfa0ef)。

原理：[Baum等1970](https://doi.org/10.1214/aoms/1177697196)、[Viterbi1967](https://doi.org/10.1109/TIT.1967.1054010)、[Rabiner1989](https://doi.org/10.1109/5.18626)。科研仅人工E1、E2/E3新增0、R073/PESEN v0.1保持冻结。下一 **R200 P1/08-024 Change Point Detection**。先完成全部R再分类和熔炼。
