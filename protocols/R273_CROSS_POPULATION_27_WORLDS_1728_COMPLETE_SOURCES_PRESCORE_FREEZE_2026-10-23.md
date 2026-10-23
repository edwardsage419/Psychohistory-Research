# R273 跨群体验证：27个人工独立群体转移世界、1728条完整训练与目标来源；事前冻结

日期2026-10-23 Asia/Taipei。原239候选目录12-003 Cross Population Validation（P0），研究编号R273。理论背景Yarkoni (2022), *The generalizability crisis*, Behavioral and Brain Sciences 45:e1, DOI https://doi.org/10.1017/S0140525X20001685（2020年先行在线）；作为竞争观点，Lakens, Tunç & Tunç (2022), *There is no generalizability crisis*, Behavioral and Brain Sciences 45:e25, DOI https://doi.org/10.1017/S0140525X21000340。两者观点有分歧，本研究仅做可检验数学转移案例，不以此裁定争议。Bareinboim & Pearl (2016), *Causal inference and the data-fusion problem*, PNAS 113(27):7345–7352, DOI https://doi.org/10.1073/pnas.1510507113，讨论因果迁移更严格的问题；R273不做因果迁移识别或干预效果估计。

## 有限源生成过程和预定义群体
源群体A成功率p_A∈{1/4,1/2,3/4}，目标群体B成功率p_B∈同集合，两群体的分布可以不同。先从群体A独立抽取四个训练Bernoulli(p_A) bit；之后群体B独立抽取两个真正未见测试Bernoulli(p_B) bit。全部六bit有序原source概率质量p_A^K(1-p_A)^(4−K) × p_B^J(1−p_B)^(2−J)；两群体原来源互相独立。每对(p_A,p_B)均有64种完整原source类型。

三冻结预测器：
* SOURCE_ORACLE：q=p_A，要求知道生成过程的源概率；用来界定源分布已知的基线，真实应用中通常不可直接访问。
* SOURCE_LAPLACE：只看A四个训练bit，q=(K+1)/6；先验Beta(1,1)冻结，绝不查看B两个测试标签。
* TARGET_ORACLE：q=p_B，使用外部知道的真实目标概率；只作**不可实施的理论风险下界**，不应当做从A训练可实施的模型。没有目标群体标签用于调参或实现该oracle。

3×3种群体概率组合 ×3预测器=27个冻结人工world，每world64条有序原source，合计**1728个带模型标签的完整人工来源类型**；对同一(p_A,p_B)三个模型重复使用原六bit设计空间，严禁把1728解释成1728位真人或独立人类群体。完整CSV保存世界、两个p、模型、全部六bit、训练A四bit、目标B两bit、两个成功数、原概率、训练后冻结q、A训练每行Brier、B独立测试每行Brier及平均。

## 事前冻结数学公式与方向案例
对任意真源a和真目标b，设基础目标不可约Brier为b(1−b)，训练成功次数K∼Binomial(4,a)。定义目标risk为E_{K,Y_B}[(Y_B−q(K))²]。三个完整封闭解析真值：
* SOURCE_ORACLE: `b(1-b)+(a-b)^2`。
* TARGET_ORACLE: `b(1-b)`。
* SOURCE_LAPLACE: `b(1-b)+a(1-a)/9+((4a+1)/6-b)^2`，将q训练波动与系统迁移偏差分离。
固定同域a=b=1/4时：SOURCE_ORACLE=TARGET_ORACLE=3/16，SOURCE_LAPLACE=31/144。
固定反向迁移a=1/4,b=3/4（及a=3/4,b=1/4）：SOURCE_ORACLE=7/16，TARGET_ORACLE=3/16，SOURCE_LAPLACE=55/144。仅源群体来源即使观测完美，也不保证目标预测校准。
固定反向迁移a=1/4,b=1/2：SOURCE_ORACLE=5/16，TARGET_ORACLE=1/4，SOURCE_LAPLACE=43/144。
所有27种组合的真实目标风险必须由完整1728原source严格积分复算且逐Fraction匹配上述式子；同时记录每source训练四bit的平均Brier、目标群体二bit平均Brier，及目标q与p_B的系统偏差。

要严格保留TARGET_ORACLE需要目标总体真率作为输入，而该真率未提供给可部署预测器。SOURCE_ORACLE也知道源真率，不能混淆为真实source fitted estimator。样本生成模型假设群体差异只体现在Bernoulli成功率，**不能代表人群心理、文化、制度、测量不变性或因果跨群体可迁移性**。

## 独立路线与验收
路线A完全穷举全部27world每个64源，模型冻结q由A训练或事前oracle给定，B测试bit只参与最终测试评分；正确原质量Fraction归一，计算每world真实来源目标Brier平均及训练内Brier。
路线B不读取有序source或独立测试值，仅以Binomial(4,a)训练K解析概率及B目标p_B计算目标期望风险，逐worldFraction与A完全相同；source Laplace前两阶矩用独立公式核对。
路线C第三GitHub Actions重新读取全部CSV直接重建每个原bit、双域source质量、两套逐行Brier及目标期望，独立验算27world的解析风险与源SHA256。
冻结协议先GitHub提交，再执行双Python3.11与3.12各≥45真实单元测试、第三独立来源审计、全部1728原source及结果JSON和SHA256机器人永久归档、三job completed/success以后才可有界E1结题。

新增真人E2=0、历史E3=0，R073和PESEN v0.1不变，暂不统一模型分类熔炼。下一原候选目录12-004 Temporal Holdout Validation（拟R274）。
