# R284 科学报告：结果依赖披露如何偏移已发表研究的阳性比例

日期2026-10-23 Asia/Taipei。原239目录12-014 Publication Bias Diagnostics（P1）。首要理论来源：Sterne, Egger & Smith (2001), *Investigating and dealing with publication and other biases in meta-analysis*, BMJ 323:101–105, DOI https://doi.org/10.1136/bmj.323.7304.101；Egger et al. (1997), *Bias in meta-analysis detected by a simple, graphical test*, BMJ 315:629–634, DOI https://doi.org/10.1136/bmj.315.7109.629 。本研究不复现任何实际已发表研究、未访问文献数据库、并非实际发表偏差估计或Egger回归验证。

[冻结协议](../../protocols/R284_PUBLICATION_SELECTION_3_POLICIES_768_COMPLETE_SOURCE_PRESCORE_FREEZE_2026-10-23.md) GitHub先行提交[0a6eccd2](https://github.com/edwardsage419/Psychohistory-Research/commit/0a6eccd270565c9a5a15a577f2dec1d1d4c7e3cb)。四个人工study的真结果Y_i~Bernoulli(1/2)，四枚单独披露bit R_i~Bernoulli(1/2)彼此独立，合计8bit所有256原有序source；三冻结政策共享相同256原bit空间，合计**768种带政策标签人工原source**，各来源质量均1/256。策略COMPLETE_REGISTRY永不删研究；POSITIVE_ONLY仅公开阳性；POSITIVE_PREFERRED阳性永公开、阴性在R_i=1时公开。完整原source CSV记录全研究结果、披露噪声、研究纳入位、公布数、公布阳性数、公开平均及“没有研究公开”标志；所有无公开情况明确保留NULL，禁止替换0、删除来源导致条件分母改变。

|人工披露机制|单study发表概率|期望公开study数|完全无公开概率|至少公开一项时，公布阳性率期望|
|---|---:|---:|---:|---:|
|COMPLETE_REGISTRY|1|4|0|1/2|
|POSITIVE_ONLY|1/2|2|1/16|1|
|POSITIVE_PREFERRED|3/4|3|1/256|2/3|

路线A完整枚举三policy×256源，用真实source质量分别计不公布的概率和已公布条件比例的分子、分母，再计算条件期望。路线B不调用来源枚举，仅凭单研究联合三类别“发表阳性1/2、发表阴性1/4、不发表阴性1/4”计算POSITIVE_PREFERRED条件发表阳性率2/3及不发表四研究概率(1/4)^4=1/256，其他政策相应独立类别公式全部匹配。第三GitHub Actions作业单独逐CSV重建所有8bit、出版掩码和完整条件比率、精确质量与SHA256，不导入研究源码。

所有单次研究原阳性率仍是1/2，改变的是可观测研究的选择机制。因为不知道现实论文的全注册研究表和选择概率，**只看公开研究通常无法直接识别其完整数据源的被选择程度**；本报告的已知披露规则属于设计者设定，并不是现实发表机制的实证发现。

[GitHub Actions run39906691468](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39906691468)三个job completed/success，Python3.11与3.12各100真实unittest，共200项通过；原CSV、结果JSON和SHA256机器凭证由机器人永久归档main提交[dfd95dcc](https://github.com/edwardsage419/Psychohistory-Research/commit/dfd95dcc386a6b0c83e87689b708f83df9de13d4)。

[可运行程序](r284_exact_publication_selection.py) · [全部768原source CSV](R284_ALL_768_ORIGINAL_PUBLICATION_SOURCES.csv) · [全部政策精确结果JSON](R284_EXACT_RESULTS.json) · [机器SHA256来源凭证](R284_MACHINE_RECEIPT.json)。CSV SHA256 `a7843584dff18a5f6027ad2a29ef98b919474f2ac54c18288c8466167da7d1ff`；结果JSON `39e6654a58ec531c48691a28eb888f0be7bec1cf8f4a44cfdb490de44b9e615d`。

全部只有人工E1，新增真人E2、真实历史E3均0，R073及PESEN v0.1不变；下一原目录12-015 Multiple Testing Correction（R285）。
