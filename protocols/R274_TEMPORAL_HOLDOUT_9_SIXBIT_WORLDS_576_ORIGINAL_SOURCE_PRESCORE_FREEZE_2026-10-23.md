# R274 跨时期留出：九个人工时间分布世界、576个完整原source、历史合法预测与未来信息泄漏；先行冻结

日期2026-10-23 Asia/Taipei。原239目录12-004 Temporal Holdout Validation（P0），R274。研究背景Roberts et al. (2017), *Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure*, Ecography 40:913–929, DOI https://doi.org/10.1111/ecog.02881；Cerqueira, Torgo & Mozetič (2020), *Evaluating time series forecasting models: an empirical study on performance estimation methods*, Machine Learning 109:1997–2028, DOI https://doi.org/10.1007/s10994-020-05910-7 。本研究并未复现上述作者的时间序列数据、原模型或真实预测结果，仅完整求解三个冻结人工二元时间机制。

## 冻结的时间先后与9个人工world
先验时间t=1,...,4作为训练期：X1...X4相互独立Bernoulli(a)。未来时间t=5,6作为评估期：Y5,Y6相互独立Bernoulli(b)，与所有旧记录独立。三个时间机制：
1 STABLE_HALF：a=1/2、b=1/2；
2 RISING_RATE：a=1/4、b=3/4；
3 FALLING_RATE：a=3/4、b=1/4。
每个机制有完整2^6=64种有序来源序列，原联合概率质量a^K(1-a)^(4-K)*b^J(1-b)^(2-J)，K=sum(X)、J=sum(Y)。三机制×三冻结模型=9人工world，**576条带模型ID的完整来源类型**，相同机制跨模型重复使用完全相同的原二元配置，不能理解为576个独立真实历史事件。

三模型：
* PAST_ONLY_LAPLACE（合法事前预测）：在t=4时只用已见K，q=(K+1)/6，对t=5,6的两次预测相同。
* HINDSIGHT_POOLED（非法未来泄漏反例）：在评价了未来Y后回头把前6个bit放进同一训练中，q=(K+J+1)/8，然后又以同一Y5,Y6评分；q因依赖J而在预测截止点无法生成，禁止当作真正的样本外模型。
* PRECOMMITTED_HALF（合法事前基线）：所有时期q=1/2。
每source必须存原前四bit、后两bit、源质量、冻结模型名、报告q、两个未来逐行Brier、未来两行平均，以及future_label_used_in_fitting的机器真假。对于同一旧四bit变更未来两bit，非法模型q会变化，另外两个冻结合法模型q必须不变。

## 预先锁定的确切期望风险
三个机制×三个模型的设计概率加权未来两期平均Brier必须逐Fraction等于下面9个真值：
|机制|PAST_ONLY_LAPLACE|HINDSIGHT_POOLED|PRECOMMITTED_HALF|
|---|---:|---:|---:|
|STABLE_HALF|5/18|27/128|1/4|
|RISING_RATE|55/144|131/512|1/4|
|FALLING_RATE|55/144|131/512|1/4|

以上HINDSIGHT_POOLED的损失是**非法地利用评分标签重新拟合之后的同一数据拟合评分**，即使数值较小，也不能称为“样本外预测优于其他方案”。在STABLE_HALF下未来泄漏模型报告27/128小于PRECOMMITTED_HALF的1/4；这种好成绩恰来自提前看到了验证标签而无可部署意义。对RISING_RATE和FALLING_RATE，合法PAST_ONLY_LAPLACE的未来风险55/144，明显高于PRECOMMITTED_HALF的1/4，说明结构性时变下旧时期预测器可能不及简单基线；仅在三种人工设定下成立。

## 真正独立复算路线
路线A逐world枚举全部64个原有序source，按照冻结三套训练政策输出q及后期两行Brier，正确来源概率Fraction积分九种评分，记录未来泄漏标志。
路线B绝不调用路线A原source枚举：先独立按K∼Binomial(4,a), J∼Binomial(2,b)的联合分布共5×3=15个(K,J)类别计算期望未来损失 `[J(1-q)^2+(2-J)q²]/2`，逐Fraction验证九项目标。尤其过去合法q完全不含J，非法模型q=(K+J+1)/8确实使用J且不能采用未来独立风险闭式取代泄漏的条件式。
路线C第三GitHub Actions独立审计CSV的576完整源、多项原概率、训练/未来来源截断、各模型q、逐行测试分数和非法模型标记、SHA256、九世界全源风险；还需检查同一训练历史换用不同未来序列时各合法预测器输出相同而hindsight输出变化。

冻结协议先于模型代码永久提交。必须Python3.11/3.12各≥45真单测、第三独立真实原source审核、全部CSV及JSON与SHA256机器人永久归档、三job completed/success以后方可科学有界E1结题。无真实时间序列、无真人E2、历史E3、外部回测或PESEN更新；R073/PESEN v0.1保持冻结。下一原目录12-005 Equifinality Analysis（拟R275）。遵守先全R学习后统一归纳分类最后熔炼。
