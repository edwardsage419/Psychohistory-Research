# R273 正式科学报告：跨群体Bernoulli分布转移的独立测试风险与oracle边界

日期：2026-10-23 Asia/Taipei。原239候选目录12-003 Cross Population Validation（P0）。研究R273。结题性质：有限人工E1数学复算，不含真实人类或历史外部预测证据。

## 理论来源及边界
Yarkoni, T. (2022), *The generalizability crisis*, Behavioral and Brain Sciences 45:e1, DOI https://doi.org/10.1017/S0140525X20001685（2020年12月在线）；Lakens, D., Tunç, D.U., & Tunç, M.N. (2022), *There is no generalizability crisis*, Behavioral and Brain Sciences 45:e25, DOI https://doi.org/10.1017/S0140525X21000340。这两篇对心理学可推广性危机的判断有争论，R273不裁定学术争议，只实现一个条件明确的数学模型。Bareinboim, E. & Pearl, J. (2016), *Causal inference and the data-fusion problem*, PNAS 113:7345–7352, DOI https://doi.org/10.1073/pnas.1510507113。此处比较**概率预测跨群体转移**，没有进行因果迁移或识别实验。

## 先行冻结与全部原始来源
[事前冻结协议](../../protocols/R273_CROSS_POPULATION_27_WORLDS_1728_COMPLETE_SOURCES_PRESCORE_FREEZE_2026-10-23.md)，独立提交[91abafba](https://github.com/edwardsage419/Psychohistory-Research/commit/91abafbaf627dbf67f86208a82008a5be419e507)。源群体A四个训练bit来自Bernoulli(a)，目标群体B两个真正独立测试bit来自Bernoulli(b)，a,b∈{1/4,1/2,3/4}。a和b可能不同；每对完整2^6=64个有序独立原source配置，精确原质量a^K(1−a)^(4−K) b^J(1−b)^(2−J)。

3源p×3目标p×3固定预测器＝27世界，合计**1728带模型标识完整人工source类型**。同样(a,b)原随机源在三个模型间重复使用，绝不等于1728名真人或独立群体。

预测器SOURCE_ORACLE只使用假定已知的源真率a，TARGET_ORACLE知道不可事前取得的目标真率b，SOURCE_LAPLACE只使用源群体四个训练bit K，q=(K+1)/6。两种oracle只用来界定理论基线，不能称为仅从A观测中可部署的拟合预测器。B的两个测试标签从未用于SOURCE_LAPLACE的训练或决策。

## 两条独立风险推导及第三来源复核
路线A完整枚举27世界×每world64原有序source，逐条固定训练q、源训练四行Brier、目标二行Brier，并以正确联合来源质量Fraction平均。
路线B绝不调用路线A原source枚举或测试标签，采用K∼Binomial(4,a)和目标风险b(1−b)+(q−b)^2的解析式：

```text
SOURCE_ORACLE:  b(1-b) + (a-b)^2
TARGET_ORACLE:  b(1-b)
SOURCE_LAPLACE: b(1-b) + a(1-a)/9 + ((4a+1)/6-b)^2
```

第三路线GitHub Actions从完整CSV逐行独立重建原两群体二元数据、来源联合概率、三个模型的固定q、所有六行Brier与源质量以及源SHA256。27个world全部目标风险、训练风险及预测偏差与独立解析公式严格有理一致。

## 代表性条件与明确预测转移风险

|源真率a|目标真率b|SOURCE_ORACLE测试Brier|SOURCE_LAPLACE测试Brier|TARGET_ORACLE测试Brier|
|---|---|---:|---:|---:|
|1/4|1/4|3/16|31/144|3/16|
|1/4|1/2|5/16|43/144|1/4|
|1/4|3/4|7/16|55/144|3/16|
|1/2|1/2|1/4|5/18|1/4|
|3/4|1/4|7/16|55/144|3/16|

在p源=1/4、p目标=3/4的人工迁移中，SOURCE_ORACLE即使完美知道源生成率，目标Brier仍为7/16，对比不具备部署可行性的目标真率下界3/16有显著额外损失。SOURCE_LAPLACE的目标风险55/144介于二者之间，展示向1/2平滑可在此项分布转移中降低错误概率暴露，但同源同目标时它又有估计方差代价：31/144大于源与目标都已知的3/16。不能由一例推断Laplace对所有跨人口/文化/制度转移都胜出。

本人工样本只改变总体Bernoulli成功率，没有任何协变量、测量等值性、对抗行为、文化构念、人群抽样选择机制或真实历史漂移数据，因此无法从本次完成证明社会心理机制的真实可迁移性。

## 真实机器核验
[完整可运行数学程序](r273_exact_cross_population_prediction.py) · [1728个原source与逐行Brier](R273_ALL_1728_ORIGINAL_CROSS_POPULATION_SOURCES.csv) · [27世界所有目标风险和偏差JSON](R273_EXACT_CROSS_POPULATION_RESULTS.json) · [SHA256凭证](R273_MACHINE_RECEIPT.json)。[GitHub Actions run39903300167](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39903300167)，Python3.11及3.12各172项真实单测通过，共344项；第三来源逐行重算与归档job成功，全部三job completed/success。

机器人将全部原CSV/结果JSON/机器SHA永久归档main：[1d57f507](https://github.com/edwardsage419/Psychohistory-Research/commit/1d57f5078d172d1feb4b6a07a68e8732c102edf6)。完整原CSV SHA256 `b4f417d0b218fd1aaa9082ab7a49e52675df59af9fd80841e74888b31dcd6d52`，结果JSON SHA256 `1f1e35d20ddd486bb7d71c65cea96e9590912268c93f17ad1ec99b7f6ac463b8`。

## E1证据与后续
本项没有新增真人E2或真实历史E3，未解除R073或PESEN v0.1冻结，也未实施跨实验外部复现。下一原目录12-004 Temporal Holdout Validation（P0，拟R274）。原R系列完成之后才统一归纳分类并熔炼原创模型。
