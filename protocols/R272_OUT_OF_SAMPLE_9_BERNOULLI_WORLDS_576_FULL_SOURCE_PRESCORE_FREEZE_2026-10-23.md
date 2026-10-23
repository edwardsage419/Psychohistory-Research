# R272 样本外预测：九人工Bernoulli世界、576完整训练及独立测试原source；事前冻结

日期2026-10-23 Asia/Taipei。原239目录12-002 Out of Sample Prediction（P0），项目R272。原理论文献Gneiting & Raftery (2007), *Strictly Proper Scoring Rules, Prediction, and Estimation*, JASA 102(477):359–378, DOI https://doi.org/10.1198/016214506000001437；Cawley & Talbot (2010), *On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation*, JMLR 11:2079–2107，原作者文档 https://jmlr.csail.mit.edu/papers/volume11/cawley10a/cawley10a.pdf 。本项建立原创有限人工例子，不宣称复现上述作者数据、模型选择过程或其真实泛化研究结论。

## 生成设计、严格留出与原source

三种真实Bernoulli数据机制p∈{1/4,1/2,3/4}，每world有四个事前训练bit X1到X4及与训练严格独立的两个测试bit Y1/Y2，所有六bit互相独立且来自同一p，组成完整2^6=64种有序原source，准确原概率质量p^(Ktrain+Ktest)(1-p)^(6-Ktrain-Ktest)。测试标签必须只用于事后评分，严禁以其修改模型与超参数。三个冻结预测器（事前规则）：
* CONSTANT_HALF：无训练，q=1/2；
* TRAIN_MLE：由前四个训练bit拟合 q=Ktrain/4，允许q=0或q=1边界；
* LAPLACE_BETA11：由四个训练bit与固定Beta(1,1)先验得到q=(Ktrain+1)/6。

每p×三个模型形成九个人工world，来源类型计64×9=**576条带模型标识的完整原source**。相同p下三模型使用同一64原bit空间，不能将其误作576名独立人类受试。每source CSV原样保留六bit训练/测试分割、训练4bit、测试2bit、train K及test K、source精确质量、训练固定预测q、四次训练逐行Brier与均分、两个测试逐行Brier与均分，以及未经截尾q对应的log-loss是否存在+∞（当q=0预测到1，或q=1预测到0）。

## 冻结精确目标
在全部source概率空间上求训练均分Brier及**真正独立测试均分Brier**的设计期望；另独立计算条件于train K的未来真风险p(1−q)^2+(1−p)q²，使用Binomial(4,p)解析分布取期望。两个test bit只决定已经冻结的预测器评分，无论测试结果怎样，q必须相同。

下表为每p固定三模型的预计算闭式目标（前者训练均分Brier，后者未来两bit均分Brier）：
|真p|CONSTANT_HALF|TRAIN_MLE|LAPLACE_BETA11|
|---|---|---|---|
|1/4|(1/4,1/4)|(9/64,15/64)|(11/72,31/144)|
|1/2|(1/4,1/4)|(3/16,5/16)|(7/36,5/18)|
|3/4|(1/4,1/4)|(9/64,15/64)|(11/72,31/144)|

来源均值应严格Fraction相同。TRAIN_MLE训练期最优或与其它模型打平，但在p=1/2独立测试上最差，future Brier 5/16，大于LAPLACE的5/18和CONSTANT_HALF的1/4。p=1/4或3/4时LAPLACE future Brier 31/144，比TRAIN_MLE 15/64更小。模型排名根据真实p与冻结分布改变，不能不经验证宣称一种预测器总优。

独立测试对数风险的特殊界限：当TRAIN_MLE得到q∈{0,1}而两个未来测试bit出现与极端q矛盾的至少一个结果，按未经截断真实log(0)对数损失为+∞。冻结全原source中出现该事件的真实概率
`(1-p)^4*[1-(1-p)^2]+p^4*[1-p^2]`，p=1/4或3/4为291/2048；p=1/2为3/32。只报告极端失败事件概率，未将∞强行转换为有限数，也未将训练期0-loss视作未来稳健预测。

## 三路线和验收
路线A完整遍历九world各64个六bit原source，真正训练集内拟合q并在**完全独立的两个测试bit**逐个评分，所有逐行score保存在CSV，质量加权得每项训练和独立测试设计平均。
路线B不调用source_rows与任何测试bit枚举，仅按Binomial(4,p)成功次数解析积分冻结三预测器，得到解析训练期Brier与独立未来风险；另外用四次训练全0/全1概率×独立二bit反向事件推导精确+∞风险质量。
路线C第三GitHub Actions job不依赖源码计算输出内部对象，重新解析全部576原CSV、断言六bit完整来源、质量、训练/测试隔离、逐行Brier/分数、原极端log-loss失败标志和所有结果SHA256。
先将本协议提交main且保留冻结SHA；之后实现无第三方依赖源码、Python3.11/3.12各≥45真单测、第三来源审计、完整CSV与结果JSON/SHA256机器永久归档、三job全部completed/success方可E1有界结题。

不能将期望future风险视为真实外部数据集评估或个人历史预测性能；没有真实人类E2、真实历史E3，不更新R073/PESEN v0.1，暂缓模型统一归纳与熔炼。原239目录下一项为12-003 Cross Population Validation（拟R273），待结束后原目录顺序继续。
