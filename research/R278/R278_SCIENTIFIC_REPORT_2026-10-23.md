# R278 正式研究报告：固定模型平均、硬模型选择与独立测试评分

日期2026-10-23 Asia/Taipei。原239目录12-008 Model Averaging and Ensembles（P2），对应R278。状态：有界人工数学E1。

## 原始文献与限定目标
Hoeting, Madigan, Raftery & Volinsky (1999), *Bayesian Model Averaging: A Tutorial*, Statistical Science 14(4):382–417，DOI https://doi.org/10.1214/ss/1009212519，原文 https://sites.stat.washington.edu/www/research/online/hoeting1999.pdf。Gneiting & Raftery (2007), *Strictly Proper Scoring Rules, Prediction, and Estimation*, JASA 102(477):359–378，DOI https://doi.org/10.1198/016214506000001437，原文 https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf。本次独立构造有限二元预测实验，未声称原作者真实实验复现或现实模型平均优势。

## 事前冻结与完整原source
[冻结协议](../../protocols/R278_BAYES_MODEL_AVERAGING_12_WORLDS_768_COMPLETE_SOURCE_PRESCORE_FREEZE_2026-10-23.md)，先行GitHub commit [eb1c8df3](https://github.com/edwardsage419/Psychohistory-Research/commit/eb1c8df38349c36ed10d7a2103969818b14d7500)。三个真实生成p∈{1/4,1/2,3/4}，每source完整四训练bit和两条真正独立测试bit，原source有2^6=64有序配置/世界，真实概率p^总成功数(1−p)^总失败数。

四种预定义政策：HARD_SELECT根据训练四bit的q=1/4或3/4候选likelihood选择其一，K=2证据平手时固定选择q=1/4；BAYES_AVERAGE对两个候选按等先验模型后验权重加权预测**单bit边缘概率**；FIXED_HALF固定1/2；TRUTH_ORACLE为无法由训练数据获取的理论真率p，仅作不可部署基准。共三p×四政策＝12world，**768个带模型ID的完整人工原source类型**，同p的四模型重复共享64个原六bit配置，绝不等于768个独立真实实验。每source逐行训练/独立测试Brier、两候选模型后验权重、实际预测q、tie-break和oracle标记均保存原CSV。两个未来Y由同一模型参数混合时其联合预测可能有依赖，当前只评价单bit边缘Brier，不宣称多bit联合独立模型已通过检验。

## 两路独立复算的完整冻结结果
路线A遍历全部768有序原source，严格按已知四训练bit拟合固定政策，再逐两个未参与训练的测试bit评分和有理source质量加权。
路线B不使用来源枚举器或测试bit，直接以K_train∼Binomial(4,p)五类别、真实未来p及每个k预定义q(k)计算：
`Etrain = Σ_k Pr(K=k)[k(1−q)^2+(4−k)q²]/4`；
`Efuture = Σ_k Pr(K=k)[p(1−q)^2+(1−p)q²]`。
两路线十二世界的训练与独立未来风险均逐Fraction完全一致。第三独立GitHub Actions审计直接逐条重读原CSV，复原训练似然、低概率模型后验权重、每bit训练/测试Brier、来源概率和十二组解析分数，再核查源CSV及结果JSON SHA256。

|真实p|模型|期望训练Brier|期望独立未来Brier|
|---|---|---:|---:|
|1/4|HARD_SELECT|89/512|205/1024|
|1/4|BAYES_AVERAGE|267/1640|87/410|
|1/4|FIXED_HALF|1/4|1/4|
|1/4|TRUTH_ORACLE|3/16|3/16|
|1/2|HARD_SELECT|7/32|5/16|
|1/2|BAYES_AVERAGE|33107/168100|46637/168100|
|1/2|FIXED_HALF|1/4|1/4|
|1/2|TRUTH_ORACLE|1/4|1/4|
|3/4|HARD_SELECT|89/512|259/1024|
|3/4|BAYES_AVERAGE|267/1640|87/410|
|3/4|FIXED_HALF|1/4|1/4|
|3/4|TRUTH_ORACLE|3/16|3/16|

模型后验平均五种训练计数K=0至4的预测分别是21/82、3/10、1/2、7/10、61/82。硬选择在K=2固定偏向低p使两端p=1/4与p=3/4风险出现非对称：p=1/4时硬选择未来205/1024优于模型平均87/410；p=3/4时模型平均87/410优于硬选择259/1024；真实p=1/2未进入两个模型候选家族时，模型平均46637/168100优于硬选择5/16，但仍差于固定半概率1/4。故本模型不支持“贝叶斯平均必定比选择单一模型表现好”这一无条件断言。来源全为人工、三真生成率人工固定。

## 真正执行证据与适用边界
[完整标准库源码](r278_exact_bayesian_model_averaging.py) · [768原source、候选权重和逐行评分CSV](R278_ALL_768_ORIGINAL_MODEL_AVERAGING_SOURCES.csv) · [完整十二世界数学结果JSON](R278_EXACT_RESULTS.json) · [来源SHA256机器凭证](R278_MACHINE_RECEIPT.json)。
[GitHub Actions run39904644080](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39904644080)三个job completed/success；Python3.11/3.12各108真unittest，共216项通过，第三完整来源逐行审计及机器人永久归档成功。全原source永久提交[0f39a4a7](https://github.com/edwardsage419/Psychohistory-Research/commit/0f39a4a753aa47bc4484b9de429da12a316196cb)。
源CSV SHA256 `e0cd62f93b7a0ff54d1c5266d3fa7cacfeba2a87109a3f8659356b804201b93d`；结果JSON SHA256 `8099d8f2e37a33b922fc466e5ba4033d26eff280c52a2604b01f8c40147ba166`。

新增真实人类E2=0、真实历史E3=0，没有取得R073模型跨实验复现，R073及PESEN v0.1冻结。下一原目录12-009 Forecast Calibration（R279，P1），原R全部完成后再统一归纳分类，最后模型熔炼。
