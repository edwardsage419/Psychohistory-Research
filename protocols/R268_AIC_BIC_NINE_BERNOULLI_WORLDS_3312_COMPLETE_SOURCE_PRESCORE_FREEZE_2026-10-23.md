# R268 AIC与BIC：九个人工Bernoulli数据世界、3312完整数据来源、有限惩罚逆转；计算前冻结

日期：2026-10-23 Asia/Taipei。原239目录11-028 AIC and BIC（P1），研究编号R268。第一文献Akaike (1974), A New Look at the Statistical Model Identification, IEEE TAC 19(6):716-723，https://doi.org/10.1109/TAC.1974.1100705 。第二文献Schwarz (1978), Estimating the Dimension of a Model, Annals of Statistics 6(2):461–464，https://doi.org/10.1214/aos/1176344136 。研究只验证**冻结的有限Bernoulli一参数MLE与零参数固定模型**及AIC/BIC公式，不重复原论文数据、先验模型边际似然或一般预测误差界。

## 九世界与两个候选模型
真数据生成机制：n个独立Bernoulli(p_true)的有序观测y1,...,yn，p_true∈{1/5,1/2,4/5}，n∈{4,6,10}，3×3恰九世界；各世界完整2^n个有序0/1原source，来源准确质量p_true^K(1-p_true)^(n-K)。九世界全原source数3×(2^4+2^6+2^10)=**3312**。所有y序列都是人工随机来源全集类型，不是3312条真人样本。

比较两个冻结候选模型：
* M0_FIXED: 固定Bernoulli成功率q0=1/5，免费参数个数k_model=0，无拟合；最大对数似然LL0=K ln(1/5)+(n-K)ln(4/5)。
* M1_FITTED: 独立Bernoulli成功率q未知并在给定当前source后拟合，MLE qhat=K/n，可调参数个数k_model=1；LL1=K ln(qhat)+(n-K)ln(1-qhat)，K=0/n时按0 log 0的连续延拓值0处理（恰好所有当前观测的最大对数似然0）。

固定同一观测来源与同一似然约定计算AIC=-2LL+2*k_model、BIC=-2LL+k_model*ln(n)。两候选的参数计数采用模型结构而不是拟合是否碰到边界来定，不允许BIC任意附加先验或把n改成九world总source个数。以**严格低分选中模型**，若恰好打平优先M0，浮点误差不得伪造严格平局。记录每source的n、p_true、原y序列、K、来源质量、两候选LL/AIC/BIC差及各自选中模型。不可按事后结果更换模型、候选参数个数或成功率。

## 数学独立验算与准确概率
路线A遍历全部3312原有序y source，以精确有理原概率为权重记录每世界AIC与BIC选择、选择不一致概率、各来源K频数。路线B不使用来源序列或其直方图，仅对每个(n,p_true)以Binomial(n,p_true)的n+1个独立解析质量C(n,K)p^K(1-p)^(n-K)，从直接**对数似然比**公式验算选择规则并得每世界两准则选M1概率及分歧概率；两条路线所有世界的三项选择概率逐Fraction相等，逐K模型决策一致。

AIC对M1的阈值：2(LL1−LL0)>2，BIC对M1的阈值：2(LL1−LL0)>ln n。n=4与6时ln n<2，BIC比AIC惩罚更轻；n=10时ln n>2，BIC比AIC惩罚更重。由冻结q0=1/5：
* n=4时两准则分歧只发生在K∈{0,2}，且**AIC选M0、BIC选M1**；
* n=6时各K两准则均同选；
* n=10时分歧只发生在K=4，且**AIC选M1、BIC选M0**。
三种p_true在n4的分歧概率依p_true 1/5、1/2、4/5顺序分别为352/625、7/16、97/625；在n6全为0；在n10分别172032/1953125、105/512、10752/1953125。所有分歧原子由完整源独立加权核对。

## 风险和结题约束
样本内MLE qhat在极端K=0或n时为0或1，而各p_true严格在(0,1)：如果下一条独立观测出现相反结果，plug-in模型给出零概率、负对数预测损失为+∞，因此**本研究不可以根据样本内AIC/BIC胜负声称严格更好零样本外预测**，也不据此给出AIC/BIC总体优劣排序。AIC/BIC都是近似选择准则，真实信息损失/模型后验概率需要其他检验条件。

须先提交冻结协议，后提交可运行标准库程序；Python3.11及3.12各≥45真单测，第三独立来源CSV审计，全部3312完整原source、世界级结果JSON与SHA256机读凭证永久GitHub归档，三job完整success后方可有界E1结题。新增真人E2=0、历史E3=0，R073/PESEN v0.1继续冻结。完成原R系列全部学习后方进入统一分类与熔炼，下一R269依原目录再核实。
