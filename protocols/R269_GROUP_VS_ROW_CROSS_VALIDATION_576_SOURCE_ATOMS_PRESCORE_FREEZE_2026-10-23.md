# R269 交叉验证：六组双重复的576完整人工源、逐行与整组留出Brier比较；事前冻结

日期：2026-10-23 Asia/Taipei。原239目录 `11-029 Cross Validation`，P0。研究编号R269。第一来源：Roberts et al. (2017), "Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure", Ecography 40:913–929, DOI https://doi.org/10.1111/ecog.02881；Arlot & Celisse (2010), "A survey of cross-validation procedures for model selection", Statistics Surveys 4:40–79, DOI https://doi.org/10.1214/09-SS054 。实现定义参见scikit-learn的LeaveOneGroupOut https://scikit-learn.org/stable/modules/cross_validation.html 。该文献用于限定外推风险；本实验是自行设计的有限人工概率模型，不声称复现原文章实证数据。

## 冻结生成模型和样本空间
六个相互独立的潜在组标签Z_g~Bernoulli(p)，g=0,...,5，每组恰有两个重复行，y_{g,0}=y_{g,1}=Z_g，共12行。p∈{1/4,1/2,3/4}三个冻结真实生成概率，观测重复行具有同组完美相关。样本单位有两层：仅六个潜在独立组，12行不独立。每个p的六bit Z向量有2^6=64种完整原概率空间原子，精确质量p^K(1-p)^(6-K)，K=sum_g Z_g。

三个冻结预测器：
* GROUP_ID_MEMORIZER：训练时记住出现过的group_id对应y（训练中同组重复y严格一致）；预测未知group_id时返回1/2。无其他特征。
* GLOBAL_LAPLACE：训练所有行阳性总数C，返回(C+1)/(N_train+2)，从头拟合；保留所有重复行，不对数据进行静默去重。
* CONSTANT_HALF：所有情况下返回1/2。

九个冻结world恰为三个p×三个预测器；每world完整64条原Z source，合计**576条完整人工模型来源配置**，其中跨同p预测器共享相同64个潜在来源，绝不能称为576个独立人类实验。每条source记录世界、p、模型、六bit组标签向量、精确来源概率、12行构造及两种交叉验证的12个逐行预测概率和Brier、每source平均Brier。

## 两个严格不同的验证协议
LOOR（leave-one-observation-out）逐行留一：12折，每折只删除一个行(i)，训练剩余11行。对于被留行，其同组复制行仍在训练中，group_id泄漏，因此不满足任何新组预测要求。
LOGO（leave-one-group-out）逐组留一：6折，每折完整删除一个group_id对应的两行，训练剩余10行，评估该组2个重复行。所有验证折训练与测试集合的组交集必须严格为空，且所有训练拟合仅使用训练行。两方案对每个source的12条行各预测恰好一次，按行Brier平均；因为每组六行大小均一，该结果也等于按组平均。不能以LOOR的0误差宣称未来未见组表现0误差。

## 事前锁定的数学真值
GROUP_ID_MEMORIZER：LOOR全部source Brier=0；LOGO全部source Brier=1/4（未见组回退1/2），对任意p恒成立。
CONSTANT_HALF：LOOR和LOGO的Brier全部source均为1/4。
GLOBAL_LAPLACE：任意目标组标签B∈{0,1}，其余5组的成功数S~Binomial(5,p)，S独立于B。LOOR在目标行训练源有11行，其中本组另一行仍存在，故q_row=(2S+B+1)/13；LOGO训练10行且排除目标整组，q_group=(2S+1)/12。两种Brier误差的分子分别化为B=0时(2S+1)^2、B=1时(11−2S)^2。解析共用期望分子 1+160p(1−p)。因此
```text
E[LOOR Brier global Laplace]=(1+160p(1-p))/169
E[LOGO Brier global Laplace]=(1+160p(1-p))/144
```
当p=1/4或3/4时分子31，故前者31/169，后者31/144；当p=1/2时分子41，故前者41/169，后者41/144。所有世界必须由穷举精确有理数重建以上9对均值，且各world来源质量恰一。验证方案不同意味着训练样本量不同；全球平滑器的乐观差距既包含同组复制残留也包含训练量的变化，不得把两者用本实验强行拆分为唯一因果效应。

模型间比较：逐行LOOR下GROUP_ID_MEMORIZER预期Brier严格0，胜过另外两模型；整组LOGO下当p=1/4和3/4，GLOBAL_LAPLACE为31/144<1/4，胜过另外两模型；当p=1/2，CONSTANT_HALF和GROUP_ID_MEMORIZER都为1/4，GLOBAL_LAPLACE为41/144>1/4，故至少没有唯一的群体预测优胜者。以上是**对完整设计来源空间的期望分数**比较，不是对一条真实观测source进行选择后重测，也不是人类行为预测的验证结论。

## 三路线、可复算与结题边界
路线A：按事前训练/测试索引逐source实际重新拟合各模型，严格分割12折LOOR与6折LOGO，保存每row的原始预测和loss，再用精确Fraction按原source设计概率积分。
路线B：不调用折叠拟合器、不依赖路线A保存的原source，把B独立Bernoulli(p)、S独立Binomial(5,p)代入冻结解析表达式，独立恢复每model和protocol的期望Brier（MEMORIZER/CONSTANT为0或1/4）。
路线C：单独审计每source的组分割不交叉、12行预测计数恰好一次、训练中同组复制是否出现、原来源质量与源CSV/SHA256机器一致性。
须先提交本协议，后建立Python3.11/3.12各≥45实际测试，独立第三job复核原source CSV、所有原始预测和设计概率、永久机器人commit全部原CSV和结果JSON/SHA256，三job completed/success以后方可正式有界E1结题。新真人E2=0，真实历史E3=0；R073、PESEN v0.1冻结；原R系列完成前不进行整体模型熔炼。原目录下一项核实为11-030 Posterior Predictive Checks，拟R270。
