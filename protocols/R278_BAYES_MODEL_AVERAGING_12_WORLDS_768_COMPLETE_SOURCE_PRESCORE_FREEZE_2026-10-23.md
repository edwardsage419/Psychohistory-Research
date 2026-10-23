# R278 模型平均与集成：十二个人工模型选择世界、768完整原source；事前冻结
日期2026-10-23 Asia/Taipei。原239目录12-008 Model Averaging and Ensembles（P2），研究R278。
第一来源：Hoeting, Madigan, Raftery & Volinsky (1999), *Bayesian Model Averaging: A Tutorial*, Statistical Science 14(4):382–417, DOI https://doi.org/10.1214/ss/1009212519；原论文 https://sites.stat.washington.edu/www/research/online/hoeting1999.pdf 。Gneiting & Raftery (2007), *Strictly Proper Scoring Rules, Prediction, and Estimation*, JASA 102(477):359–378, DOI https://doi.org/10.1198/016214506000001437 ，原论文 https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf 。本研究是自建完整有限随机空间，而非复现作者的经验案例。

## 冻结来源、预测器及评分
真生成Bernoulli p∈{1/4,1/2,3/4}，每世界训练4个互相独立bit X1…X4、未来测试2个从未用于训练的bit Y1/Y2；所有原始6bit互相独立同p。每真p的完整有序原source空间有2^6=64种，其精确质量p^(K+J)*(1−p)^(6−K−J)，K训练成功数、J测试成功数。
模型候选族事前固定两种点分布q_low=1/4、q_high=3/4，且Bayes先验模型权重各1/2。冻结四个预测政策：
1 HARD_SELECT：根据训练4bit的likelihood L_low=(1/4)^K*(3/4)^(4−K)，L_high=(3/4)^K*(1/4)^(4−K)选择似然较大者；K=2发生相等时**事前固定选择q_low**；未来两个bit都按所选单模型概率预测。
2 BAYES_AVERAGE：按等模型先验更新权重w_low=L_low/(L_low+L_high)，w_high=1−w_low，未来单bit混合预测q=(w_low/4)+(3*w_high/4)。完整预测分布若同时预测两条Y不独立，本实验只评分**单bit边缘Brier平均**，不声称两个bit的独立联合预测。
3 FIXED_HALF：所有训练和测试预测q=1/2，可部署稳定基线。
4 TRUTH_ORACLE：q=p，依赖实验设计者知道的真p，**只作不可部署的理论风险下界，不是现实中可从X训练的估计器**。
3p×4预测政策=12个人工world；每world全部64原配置，共**768种带policy标识完整人工源类型**，而同p四政策共享完全相同的64原bit源，不可说768个独立实验。

对每source存训练4bit、测试2bit、K、J、原概率、训练得到的低候选Bayes权重和最终预测q、训练与测试每行Brier及平均、该policy是否依赖不可访问真p、是否在模型选择中发生K=2平手。测试两个Y只在预测冻结后评分；严禁使用Y进行policy选择或权重调优。

## 三层冻结精确预期
路线A枚举12world×64有序source，真实构造训练模型likelihood、预测q、逐行训练/独立测试Brier，并以原概率Fraction积分计算每world的训练平均及未来两bit平均Brier。
路线B**不调用来源枚举、不接触任何测试标签**，使用K∼Binomial(4,p)五种类解析质量 w_k=C(4,k)p^k(1−p)^(4−k) 和p对未来的单bit风险 p(1−q)^2+(1−p)q²，单独推导12项独立预测期望。训练期解析损失为[K(1−q)^2+(4−K)q²]/4。冻结实际结果：
|真实p|HARD_SELECT(train,test)|BAYES_AVERAGE(train,test)|FIXED_HALF(train,test)|TRUTH_ORACLE(train,test)|
|1/4|(89/512,205/1024)|(267/1640,87/410)|(1/4,1/4)|(3/16,3/16)|
|1/2|(7/32,5/16)|(33107/168100,46637/168100)|(1/4,1/4)|(1/4,1/4)|
|3/4|(89/512,259/1024)|(267/1640,87/410)|(1/4,1/4)|(3/16,3/16)|

特定观察K=0,1,2,3,4的BAYES_AVERAGE预测依次为21/82、3/10、1/2、7/10、61/82。HARD_SELECT采用平手偏向低p候选，造成真p=3/4与p=1/4的风险非对称，不能误称硬选择镜像对称。p=1/2真值未在候选族中，BAYES_AVERAGE测试风险46637/168100略优于HARD_SELECT的5/16，却仍差于FIXED_HALF的1/4。p=1/4时硬选择未来风险205/1024优于BMA的87/410，而p=3/4时BMA 87/410优于硬选择259/1024。故不能声称“模型平均在任何数据生成情境下都胜过选择单模型”；其好坏依真DGP、先验及平手规则而变。

路线C单独GitHub Actions审计全部768原source CSV、六bit训练/测试分隔、来源质量、独立重算训练似然和模型权重、训练及测试每bit Brier、12项平均风险、各文件SHA256。只在三job全部completed/success且真实Python3.11/3.12各≥45项unittest通过、完整原CSV+结果JSON+SHA256收据均由机器人永久GitHub main归档之后，允许有界E1结题。

目前没有真人E2、历史E3、真正外部样本；R073/PESEN v0.1保持冻结。下一原目录12-009 Forecast Calibration（拟R279）。先完成原R系列后统一分类归纳，最后熔炼。
