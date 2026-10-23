# R272 正式科学报告：训练损失与独立样本预测风险的严格分离

日期：2026-10-23 Asia/Taipei。原239目录12-002 Out of Sample Prediction（P0）。研究R272。科学级别E1，仅人工六bit有限模型概率空间。

## 第一来源与研究问题

Gneiting & Raftery (2007), *Strictly Proper Scoring Rules, Prediction, and Estimation*, JASA 102(477):359–378, DOI https://doi.org/10.1198/016214506000001437；Cawley & Talbot (2010), *On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation*, JMLR 11:2079–2107, https://jmlr.csail.mit.edu/papers/volume11/cawley10a/cawley10a.pdf 。以上构成预测评分和模型选择偏差的理论参照。此R项实现的是自行构造的精确有限人工样本空间，未逐字节复现上述论文数据、实际算法或真实样本泛化风险。

## 冻结来源与三种预测模型

[先冻结协议](../../protocols/R272_OUT_OF_SAMPLE_9_BERNOULLI_WORLDS_576_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md)，先行SHA commit [52f84dbf](https://github.com/edwardsage419/Psychohistory-Research/commit/52f84dbfbe8563cf5c9a491e67d5e320223e0a56)。三种真实人工Bernoulli p=1/4、1/2、3/4；每source前4bit专属训练、后2bit专属测试，两集合完全独立同p分布；六bit全部2^6=64种有序source原子以p^(总1)(1-p)^(总0)精确Fraction加权。对比三个模型：常数半概率q=1/2，训练四bit MLE q=K/4，事先固定Beta(1,1) Laplace平滑q=(K+1)/6。3p×3模型=九人工world，合计**576种模型标识的完整source类型**，同p下三模型来源共享，绝不能视为576个独立实验或受试。

针对每source先冻结训练预测q，然后在4训练bit和2条**未被使用的独立测试bit**分别计算逐bit Brier (y−q)^2，所有原bit、每行误差、原概率以及预测q均保存CSV。测试bit从不进入q的训练计算。

## 两路独立精确结果

路线A按全部576原source逐个重新拟合训练端q和测试端评分，以准确source质量加权得到训练与测试的设计期望。路线B**不读取任何有序source或测试bit**，仅利用K_train∼Binomial(4,p)的解析质量，对训练平均Brier和真实未来风险p(1−q)^2+(1−p)q^2单独积分。九world训练和未来两项全部严格Fraction一致。第三来源CSV的GitHub CI重新解析全部原bit、source质量、训练概率、逐行train/test Brier以及边界log损失标记与SHA256。

|真实生成p|模型|E训练Brier|E独立测试Brier|E测试减训练|
|---|---|---:|---:|---:|
|1/4|CONSTANT_HALF|1/4|1/4|0|
|1/4|TRAIN_MLE|9/64|15/64|3/32|
|1/4|LAPLACE_BETA11|11/72|31/144|1/16|
|1/2|CONSTANT_HALF|1/4|1/4|0|
|1/2|TRAIN_MLE|3/16|5/16|1/8|
|1/2|LAPLACE_BETA11|7/36|5/18|1/12|
|3/4|CONSTANT_HALF|1/4|1/4|0|
|3/4|TRAIN_MLE|9/64|15/64|3/32|
|3/4|LAPLACE_BETA11|11/72|31/144|1/16|

MLE对固定训练bit的经验Brier最优（与其他模型可能并列），但当p=1/2时，其未来独立风险为5/16，高于半概率常数模型1/4，也高于Laplace的5/18。p=1/4/3/4时Laplace未来风险31/144，优于MLE的15/64。结果明确表明在本人工设计下不能用训练端拟合优度替代独立未来概率预测评价。

若MLE训练得到q=0/1，但后两独立测试bit至少出现一次与极端值矛盾，原始负对数损失出现+∞；该事件p=1/4或3/4真实概率291/2048，p=1/2概率3/32。此研究没有对原q进行人为下截或对∞进行有限数替代；因此MLE该未截尾预测的**样本外期望对数损失无穷**，尽管其Brier始终有界。两种严格评分应区分评价目标与极端概率风险。

## 执行记录与受限证据
[运行源码](r272_exact_train_test_prediction.py) · [全部576训练与留出原source CSV](R272_ALL_576_ORIGINAL_TRAIN_AND_TEST_SOURCES.csv) · [九world精确训练/测试Brier与无限log风险JSON](R272_EXACT_RESULTS.json) · [SHA256机器凭证](R272_MACHINE_RECEIPT.json) · [GitHub Actions run39903106107](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39903106107)。Python3.11及3.12各83项真测试通过，共166项，第三独立原source重建和机器人永久归档均success，完整三job success；原source永久提交[dd4995e8](https://github.com/edwardsage419/Psychohistory-Research/commit/dd4995e82cd62cc35c493b79f3525854c06a7eab)。

原CSV SHA256 `dc40ed773491817caf242ba6416e1bdf98ef2f1a2cd05e1956bdf5aec5801663`；结果JSON SHA256 `f891df1c4640c2f49a457c436bc043f6bc08b768ac92594050e7e08061495a40`。

研究没有使用真实真人样本和历史序列，没有独立跨实验或跨时期预测证据，新增E2=0、E3=0；不解除R073与PESEN v0.1的冻结。原239目录下一项12-003 Cross Population Validation（P0，拟R273）。仍先完成全部原R学习，再统一归纳分类，最后熔炼。
