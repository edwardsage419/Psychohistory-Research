# R283 科学报告：人工完整登记册、固定效应与选择性报告的精确风险

日期2026-10-23 Asia/Taipei，原239目录12-013 Systematic Review and Meta Analysis（P1）。理论来源Page et al. (2021), *PRISMA 2020 Statement*, BMJ 372:n71, DOI https://doi.org/10.1136/bmj.n71；Higgins et al. (2003), *Measuring inconsistency in meta-analyses*, BMJ 327:557–560, DOI https://doi.org/10.1136/bmj.327.7414.557。

**此项不是系统检索、系统综述或真实论文元分析。** 仅为理解三个虚构study的完整纳入及模型异质性而设计的人工E1概率空间。全部S1、S2、S3恰各有一个处理bit和一个对照bit，原source共2^6=64种/世界，三人工生成情境合计**192个来源标签配置**，全部概率大于零。来源顺序T1C1T2C2T3C3、每条真数据机制、三个study风险差、全研究固定效应汇总及Q统计全部按原位存档。

[先行冻结协议](../../protocols/R283_THREE_STUDY_FIXED_EFFECT_SYNTHESIS_192_COMPLETE_SOURCE_PRESCORE_FREEZE_2026-10-23.md)，冻结提交[310b1343](https://github.com/edwardsage419/Psychohistory-Research/commit/310b134383db1b08b66750d12d7229005426b439)。不依据结果筛选study。每study假设设计者提前知道真处理/对照率，设置理想化oracle方差v=pT(1−pT)+pC(1−pC)及权重w=1/v；现实单处理单对照试验不能从样本直接可靠估计这样的方差，故**不能将该oracle权重当成真实研究可获得的标准误**。全纳入汇总D=Σw d/Σw；异质性Q=Σw(d−D)^2；错误的选择性策略只报告MAX(d1,d2,d3)。

|人工情境|真加权效应|合成估计方差|E[Q]|事后最大研究效应期望|
|---|---:|---:|---:|---:|
|HOMOGENEOUS|1/2|1/8|2|469/512|
|BALANCED_HETEROGENEITY|0|3/22|10/3|175/256|
|ONE_REVERSAL|1/6|1/8|34/9|419/512|

路线A完整原六bit穷举、source真概率Fraction加权计算E[D]、Var(D)、E[Q]、E[max d]；路线B不读取原source，以三研究独立风险差d∈{-1,0,+1}的**3³=27个分类组合**解析计算max风险，并通过独立噪声分解给出E[Q]=2+Σw(δ_i−δbar_w)^2。两路三个世界全部精确一致。第三GitHub Actions独立审计从原CSV逐study重算研究ID、风险差、oracle权重、Q、全部192原概率以及结果SHA256。

首次[CI run39906498127](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39906498127)双Python通过但第三审计脚本一行zip解包错误失败；[修正commit638f8e6b](https://github.com/edwardsage419/Psychohistory-Research/commit/638f8e6bd7d10e6a1c204d92661b3aa060cb6752)只修独立核验，不改变冻结设计。最终[成功CI run39906571655](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39906571655)：Python3.11及3.12各99真单元测试，共198通过，第三审计和机器人归档成功，三job completed/success。全部原source永久归档[commit6b4f0e1a](https://github.com/edwardsage419/Psychohistory-Research/commit/6b4f0e1adb42484eaa55c5eebf08ee47f9421e13)。

[Python源码](r283_exact_meta.py) · [全部192原source CSV](R283_ALL_192_ORIGINAL_THREE_STUDY_META_SOURCES.csv) · [独立解析结果JSON](R283_EXACT_META_RESULTS.json) · [机器SHA收据](R283_MACHINE_RECEIPT.json)。原CSV SHA256 `3afd2738cb786e384f740a4845a0c91464024acfb06dd3e3c31cf669bd9d80ee`，结果JSON SHA256 `5beb10413cfbfd169406f0c7359896c842e7d6dbc12211fec9b763244182f0a9`。

该人工例子显示完整纳入和结果导向择优的差异，不证明现实研究的异质性或真实元分析结论。新真人E2=0、真实历史E3=0，R073/PESEN v0.1冻结。下一原目录12-014 Publication Bias Diagnostics（R284）。
