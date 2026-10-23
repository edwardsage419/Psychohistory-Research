# R276 正式科学报告：产品参数的结构性不可辨识与增加观测通道的恢复

日期2026-10-23 Asia/Taipei。原239目录12-006 Model Identifiability（P0）。研究R276，证据等级E1有限人工参数实验，无真实人类或历史数据。

## 文献依据
Rothenberg, T.J. (1971), *Identification in Parametric Models*, Econometrica 39(3):577–591，DOI https://doi.org/10.2307/1913267，原文 https://pages.stern.nyu.edu/~dbackus/Identification/id/Rothenberg_id_Econometrica_71.pdf 。该文从参数统计模型的概率分布是否能够区分参数出发，讨论辨识与信息矩阵条件。R276使用自行设计的三个有限参数点反例，没有复现原作者真实数据。

## 原始冻结协议与结构定义
[冻结协议](../../protocols/R276_STRUCTURAL_IDENTIFIABILITY_192_SOURCE_ATOMS_THREE_PRODUCT_PARAMS_PRESCORE_FREEZE_2026-10-23.md)，先行commit[58e192c5](https://github.com/edwardsage419/Psychohistory-Research/commit/58e192c523cc87b4fd4f6b9758af118d620a1951)。参数点PARAM_A=(1/2,1/2)、PARAM_B=(1/4,1)、PARAM_C=(1,1/4)。三个参数点乘积q=θ1θ2均为1/4。每个source包含四条独立Y∼Bernoulli(q)，另有与Y独立的两条Z∼Bernoulli(θ1)。每真参数全2^6=64个有序原source类型，三个参数共**192个完整原source**，包括C模型Z非11时质量0的配置；正质量数64+64+16=144。零质量source只是完整原空间保留占位，并不构成真实实验数据。

## 冻结观测方案与准确概率
OBSERVE_Y_ONLY只读取四条Y。三个候选参数的任何四bit Y联合概率均为(1/4)^K(3/4)^(4−K)，因此完整观测分布严格相同，不能通过增加同机制下更多Y样本解决θ1与θ2的区分。等候选先验与预冻结MAP并列选择PARAM_A，三真参数条件正确率依次1、0、0，等权平均**1/3**。该不对称结果来自tie-break，不代表A参数受到更大观测支持。

OBSERVE_Y_AND_Z另外读取两条Z。Z=00时参数A、B、C似然比例1/4:9/16:0，模型后验为4/13、9/13、0，MAP选B；Z=01/10时后验4/7、3/7、0，选A；Z=11时后验4/21、1/21、16/21，选C。Y的likelihood作为公共正因子完全抵消，不影响分类。于是三真参数的条件MAP正确率分别为：
* A：观察混合Z=01/10的概率1/2；
* B：观察Z=00的概率9/16；
* C：必观察Z=11，概率1。
等候选真模型先验平均=(1/2+9/16+1)/3=**11/16**。

增加Z之后三个**离散候选**的联合数据分布彼此不同，因此在这些固定参数点上实现分布层面可辨识，但两条Z有限样本的Bayes分类准确率仍不等于1。实验结论不涵盖θ的二维连续开集是否可辨识，也不提供真实数据参数区间。

## 三条独立精确复算路径
路线A对每真参数全部64有序六bit源执行真实似然计算、三候选后验、冻结MAP及来源概率加权，保存所有原Y/Z比特、来源质量、两通道likelihood、posteriors、MAP选择和每source判定。
路线B完全不调用路线A来源，使用独立的Y∼Bernoulli(1/4)四bit分布和Z的两次Bernoulli(θ1)计数分类，推导全部边缘以及1/3与11/16。全部来源期望与路线B精确Fraction相同。
路线C GitHub Actions第三job另外编写完整CSV审计，逐条重建原source、各候选参数的概率质量、两种likelihood、后验分数与MAP，验证Y边缘完全等价、支持零质量计数、准确source SHA256与结果哈希。

[GitHub Actions run39904079585](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39904079585)三个job completed/success，Python3.11与3.12各50项真实unittest通过，共100项。原CSV及机读结果由机器人永久归档commit[e32a4a4f](https://github.com/edwardsage419/Psychohistory-Research/commit/e32a4a4fb38ee90eea6ab7670eadf54ff3bbdbad)。

[可运行源码](r276_exact_structural_identifiability.py) · [全部192有序source CSV](R276_ALL_192_ORIGINAL_IDENTIFIABILITY_PARAMETER_SOURCES.csv) · [解析结果与三世界JSON](R276_EXACT_RESULTS.json) · [机器SHA凭证](R276_MACHINE_RECEIPT.json)。
完整CSV SHA256 `9507c95f36edf47dcb5936cb877f9883346df33bad1031487fe9d6bed230f490`，结果JSON SHA256 `61de22a8576178c546523280f3bb83be514951d7d1df71bff7a612ddb2d92d0f`。

## 科研边界与主线
只有E1人工离散模型，可辨识性命题不等于真实历史群体因果识别。新增真人E2=0、真实历史E3=0；未更新R073/PESEN v0.1。下一原目录12-007 Model Misspecification Checks（P0，拟R277），原R全部完成之后再统一归纳分类和原创模型熔炼。
