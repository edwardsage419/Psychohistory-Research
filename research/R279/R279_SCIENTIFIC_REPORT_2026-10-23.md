# R279 正式科学报告：校准为零不代表有风险分辨力

日期2026-10-23 Asia/Taipei。原239模型目录12-009 Forecast Calibration（P1）；状态：**有界人工数学E1**。

## 原始文献与方法边界
Murphy (1973), *A New Vector Partition of the Probability Score*, Journal of Applied Meteorology 12(4):595–600，DOI https://doi.org/10.1175/1520-0450(1973)012%3C0595:ANVPOT%3E2.0.CO;2；Gneiting & Raftery (2007), *Strictly Proper Scoring Rules, Prediction, and Estimation*, DOI https://doi.org/10.1198/016214506000001437 。R279采用自建二元组发生率的精确来源数学空间，不声称复现上述文献实证案例。

## 冻结设计与全部source
[事前完整冻结协议](../../protocols/R279_FORECAST_CALIBRATION_9_WORLDS_144_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md)，冻结GitHub提交[acb48cd4](https://github.com/edwardsage419/Psychohistory-Research/commit/acb48cd4e0640ac36c56d9bfdfa2fc111c720d11)。两个事前明确人工L和H组各2条Bernoulli观察，总计4bit/原source，三冻结真实世界：(theta_L,theta_H)=(1/4,3/4)、(0,1)、(3/4,1/4)。三预测政策ORIGINAL_BUCKETS分别报(1/4,3/4)，FLAT_HALF对两组都报1/2，REVERSED_BUCKETS反向报(3/4,1/4)。各world所有2^4=16有序原source完整保留且source联合质量精确，三真率×三预测政策共9world，**144个模型/世界标识的人工完整来源类型**；真概率(0,1)的每world有15个零质量source占位，全部9world共**99种正质量原source配置**。同一真机制的三政策共用原观察配置，不是144份独立真人数据。

## 双路线来源与真正总体分解
路线A逐source完整保存L1/L2/H1/H2四bit、每个真实分组、每行预测概率、来源质量、逐行Brier和每source平均，来源概率Fraction加权计算每world期望评分。
路线B完全不读取原source，按**真实总体条件概率**以预测概率值q分桶，定义：
```text
p_bar = (theta_L+theta_H)/2 = 1/2
UNC = p_bar*(1-p_bar)
REL = sum_bin(weight_bin * (q_bin - theta_given_bin)^2)
RES = sum_bin(weight_bin * (theta_given_bin - p_bar)^2)
E[Brier] = REL - RES + UNC
```
两种组预测q不同则有两个各1/2权重预测桶；FLAT_HALF所有四行q=1/2，**只能形成一个预报概率桶**，其真条件均值(θL+θH)/2=1/2，故REL=0、RES=0。该分解严格限于总体真概率的预期Brier，不是单一次有限样本的经验校准分解。

## 九个人工世界精确验收结果

|真实机制|预测器|REL可靠性误差|RES分辨力|UNC不确定性|E[Brier]|
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

在CALIBRATED_RATE真世界，FLAT_HALF虽然总体REL=0，但其Brier=1/4，逊于正确分组ORIGINAL_BUCKETS的3/16；在DETERMINISTIC_GROUP真世界，完全平坦预测仍REL=0，但ORIGINAL_BUCKETS尽管REL=1/16，因RES=1/4而获得更低Brier=1/16。因此校准度量必须与分辨力/锐度及真正独立预测评分一起考虑。不能仅凭某次经验样本中小的校准误差确定某模型对历史事件有预测力。

## 真实GitHub执行和首次失败保留
标准库[源程序](r279_exact_forecast_calibration.py) · [全部144原source CSV](R279_ALL_144_ORIGINAL_FORECAST_CALIBRATION_SOURCES.csv) · [完整九世界解析结果JSON](R279_EXACT_RESULTS.json) · [SHA256机器凭证](R279_MACHINE_RECEIPT.json)。
首次workflow [run39904785939](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39904785939) 因Python multiline assert断行语法错误失败，留下正式失败记录。随后仅修正可执行断行语法，[fix commit40fa945d](https://github.com/edwardsage419/Psychohistory-Research/commit/40fa945d0273b085279576f52b5abd0e3d24c284)，保留既定冻结协议、模型定义及真值不动。[最终GitHub Actions run39904942557](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39904942557)三个job全部completed/success，Python3.11、3.12各84真实unittest通过，共168项，第三独立144原source逐行重算及population Murphy分解审计成功，机器人已永久提交全部CSV/JSON/SHA到main [archive1f7275b3](https://github.com/edwardsage419/Psychohistory-Research/commit/1f7275b346824e5b235a9fcdf59bd10d40028d6c)。

原CSV SHA256 `c2c64e3a2bb4c5b1248663301ac50528e3762776ea3d4ef5ff2eeddf342edab0`；结果JSON SHA256 `985764e4205d5673a0e2c7ca33f8e5589252ff6a5b5de39b617912773700da7f`。

所有统计数字来自真实完整人工E1，新增真人E2=0、真实历史E3=0，R073/PESEN v0.1不变。下一原目录12-010 Brier Score（R280，P1），全部原R研究完成后才统一归纳、分类与熔炼。
