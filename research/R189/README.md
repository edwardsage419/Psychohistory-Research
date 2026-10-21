# R189 多层广义线性模型：24个人工离散随机截距Logit世界

日期：2026-10-21，原目录P1/08-013 Multilevel Generalized Linear Models。科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_DISCRETE_GLMM**。

[事前冻结协议](../../protocols/R189_DISCRETE_GLMM_24_WORLDS_8472_TABLES_PRESCORE_FREEZE_2026-10-21.md)先于评分入库，设定两组解释条件x∈{0,1}、各两个彼此独立群组、每群组n=2/4次潜在二元事件。每群组共用等概率双点随机截距赔率倍数h或1/h，参数2种基准赔率×3种组别倍率×2种随机截距强度×2种n，共**24人工世界**，完整列举**8472组人工四群组训练计数表**与精确原始概率，另有**261种唯一无序拟合profile**。用严格嵌套的12候选无随机效应模型和36候选双点随机效应模型，在每群组完整计数PMF边际似然上以Fraction择优。源PMF通过组合公式及两套独立逐事件DP完全一致，全部候选likelihood用原有序群组与聚合直方图独立Fraction一致。两个模型在**完全独立的新群组**测试计数分布上用math.log和Decimal.ln两套独立实现验收真实来源加权logloss。

**固定反例：** o=1/3,t=3,h=3时，单次x0边际p=3/10、x1边际p=1/2，真正组条件赔率倍率为3，但总体边际赔率比仅7/3；同群x0任两事件协方差为1/25，n2群组两次成功的真实概率13/100，错误将两事件按p=3/10独立相乘得9/100。完整训练样本全概率加权的新群组测试logloss在n2时POOLED 1.295317、GLMM 1.260859；n4时POOLED 1.987992、GLMM 1.918470。真实h=1世界也有GLMM更差的案例，训练更高自由度不会保证全部来源的外部预测改进。

[正式科研报告](R189_SCIENTIFIC_REPORT_2026-10-21.md)、[24世界完整输出JSON](R189_EXACT_RESULTS.json)、[8472条原始训练计数CSV](R189_ALL_8472_ORDERED_CLUSTER_TRAINING_TABLES.csv)、[261种完整概率拟合profile](R189_ALL_261_CLUSTER_FIT_PROFILES.json)、[正式机器验收](R189_FINAL_MACHINE_ACCEPTANCE.json)、[原生源码与30项测试](r189_exact_discrete_logit_glmm.py)、[完整六文件ZIP](R189_Exact_Two_Point_GLMM_24_Worlds.zip)均已正式归档。[GitHub Actions39571031157](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39571031157)双Python各30单测、共60次通过和完整结果归档三个job全success，[永久结果提交583d671](https://github.com/edwardsage419/Psychohistory-Research/commit/583d671af309be7b7ba64ddb54c252cc01b2e93f)。

一手背景来源：[Breslow/Clayton1993](https://doi.org/10.1080/01621459.1993.10594284)、[Neuhaus/Kalbfleisch/Hauck1991](https://doi.org/10.2307/1403572)。这是**有限离散随机截距混合模型**，不称为高斯GLMM估计，且无新增真人E2或历史E3。R073及PESEN v0.1冻结。下一 **R190 P1/08-014 Generalized Additive Models**，完成既定全部R后才统一归纳分类，最后熔炼。
