# R279 预测校准：九个分组概率世界、144完整有序原source，Brier可靠性／分辨力／不确定性；先冻结

日期2026-10-23 Asia/Taipei。原239目录12-009 Forecast Calibration（P1），研究R279。第一来源：Murphy (1973), *A New Vector Partition of the Probability Score*, Journal of Applied Meteorology 12(4):595–600, DOI https://doi.org/10.1175/1520-0450(1973)012%3C0595:ANVPOT%3E2.0.CO;2；Gneiting & Raftery (2007), *Strictly Proper Scoring Rules, Prediction, and Estimation*, DOI https://doi.org/10.1198/016214506000001437。R279是自建完整有限来源的事前数学例子，无原作者数据实证复现。

## 三冻结人工概率世界
有两个人为已知组L和H，各有两个互相独立的二元结果，总共四个有序bit L1,L2,H1,H2。每组的真发生率分别(theta_L,theta_H)，固定三个世界：
* CALIBRATED_RATE=(1/4,3/4)；
* DETERMINISTIC_GROUP=(0,1)；
* INVERTED_RATE=(3/4,1/4)。
六? **实际样本是4bit，完整原空间是2^4=16种有序配置/world-policy**，绝不记成6bit。各source概率质量theta_L^kL(1-theta_L)^(2-kL)*theta_H^kH(1-theta_H)^(2-kH)，指数零时约定0^0=1。每个世界的两个组对总体的观测权重均1/2，因此总体结果概率永远1/2。
三个冻结报概率政策，在观测前完成固定，无预测再训练：
* ORIGINAL_BUCKETS：对L报q=1/4，对H报q=3/4；
* FLAT_HALF：对L和H一律报q=1/2（合并成**同一唯一forecast bucket**）；
* REVERSED_BUCKETS：对L报q=3/4，对H报q=1/4。
三个真概率世界×三政策＝9个人工world，每world16个完整有序原来源，共**144条带world/policy ID的完整人工source类型**。DETERMINISTIC_GROUP中每policy只有一个正概率配置（L00,H11），其他15条保留原概率0的形式占位，因此合计9world正质量类型为3×(16+1+16)=**99**，不能将144理解成144次独立观测。

## 冻结可靠性、分辨力及不确定性定义
用真实设计概率、不使用单次sample中观测到的经验组频率，定义按**预测概率值分桶**得到的总体population Murphy分解：
UNC=pbar(1−pbar)，pbar为所有行的真实基础率=1/2，故UNC=1/4；
REL=Σ_forecast-bins w_q (q−theta_true_given_forecast_q)^2；
RES=Σ_forecast-bins w_q (theta_true_given_forecast_q−pbar)^2；
Brier_expected=REL−RES+UNC；
其中每个bucket权重为落入该q的行数占四行比例，真实conditional rate为该bucket所覆盖组的theta按行权重加权平均。特别FLAT_HALF只有一个q=1/2的bucket，合并L和H的真实率后刚好1/2，因此REL=0、RES=0，即**完全population校准但零分辨力**。对于非flat政策有两个各权重1/2的桶。
在给定同一个真DGP下，可以比较分桶政策的期望Brier与REL/RES/UNC，不得将两个不同DGP的Brier直接当同一经验预测模型的排名。

## 冻结九世界全解析真值
| 真世界 | 策略 | REL | RES | UNC | 期望Brier |
|---|---|---:|---:|---:|---:|
|CALIBRATED_RATE|ORIGINAL_BUCKETS|0|1/16|1/4|3/16|
|CALIBRATED_RATE|FLAT_HALF|0|0|1/4|1/4|
|CALIBRATED_RATE|REVERSED_BUCKETS|1/4|1/16|1/4|7/16|
|DETERMINISTIC_GROUP|ORIGINAL_BUCKETS|1/16|1/4|1/4|1/16|
|DETERMINISTIC_GROUP|FLAT_HALF|0|0|1/4|1/4|
|DETERMINISTIC_GROUP|REVERSED_BUCKETS|9/16|1/4|1/4|9/16|
|INVERTED_RATE|ORIGINAL_BUCKETS|1/4|1/16|1/4|7/16|
|INVERTED_RATE|FLAT_HALF|0|0|1/4|1/4|
|INVERTED_RATE|REVERSED_BUCKETS|0|1/16|1/4|3/16|

两个分组政策的分辨力由真实theta生成；FLAT_HALF在全部三个世界均REL=0但Brier=1/4，若正确利用组信息，在CALIBRATED_RATE世界ORIGINAL_BUCKETS可做到3/16，在INVERTED_RATE世界REVERSED_BUCKETS也可做到3/16。因而“population可靠性为0”并不单独证明预测模型有效、可区分风险或具有实际应用价值。特别DETERMINISTIC_GROUP原policy有非零校准偏差REL=1/16但低风险Brier=1/16，优于REL=0的FLAT_HALF，这是同一世界中分辨力发挥作用的例子。

路线A完整穷尽全部144个四bit原source，保留每行group标签、固定forecast q、真theta、完整source质量和逐行Brier，按真DGP来源Fraction汇总每world真实期望Brier。
路线B不使用有序source表，直接按两群体真率计算Brier均值和上述REL、RES、UNC三项固定真实条件频率桶，验证所有九world总式完全一致。必须避免将基于有限一次source的经验可靠性分解和本研究的**population级分解**混为一谈。
路线C独立GitHub第三作业重读完整144 CSV包括45个零概率占位source，逐行重算四bit来源概率、四个预测、四项loss、9期望Brier及分桶REL/RES/UNC，核验CSV/JSON SHA256；需双Python3.11/3.12各至少45真实unittest、第三完整源审计及机器人永久提交所有文件后，三job全部completed/success方正式有界E1结题。

新增真人E2=0、真实历史E3=0，R073与PESEN v0.1继续冻结；下一原目录12-010 Brier Score（拟R280），原R全部完成后再统一归纳、分类、熔炼。
