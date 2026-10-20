# R150：人口转变模型 — 双粗率错位下降与人口总量观测的识别边界

日期：2026-10-20。既定候选目录 **P1 / 06-008 Demographic Transition Models**。

直接核验原作者出版社出版记录和论文摘要：
- Thompson (1929) *Population*, AJS 34(6):959–975, [DOI 10.1086/214874](https://doi.org/10.1086/214874)；出版社原始摘要包含A/B/C三类出生、死亡率下降模式；
- Davis (1945) *The World Demographic Transition*, ANNALS 237:1–11, [DOI 10.1177/000271624523700102](https://doi.org/10.1177/000271624523700102)，原论文出版信息及标题核实，但访问限制使本期没有全文逐页阅读；
- Lee (2003) *The Demographic Transition: Three Centuries of Fundamental Change*, JEP 17(4):167–190 [DOI 10.1257/089533003772034943](https://doi.org/10.1257/089533003772034943)，AEA原刊摘要核实死亡率先下降、出生率后下降和短期人口增长加速的典型叙述。

**所有模型数字与程序均为项目自行设定E1理论实验，不是原作者公布的公式或国家人口预测。**

从1000人口、出生粗率1/5到1/20、死亡粗率1/5到1/20，年度时间转换点各取0..8（9×9），再比较无额外冲击、t4额外死亡率1/10、t4净移入率1/10三类场景，**243个十二期完整生命统计账本**。逐年独立记录人口存量、出生/死亡/净移入流及率；两种独立乘积算法检查终点。全部111项本地真实unittest已通过。

无冲击时36种死亡率先降的人口增长，36种出生率先降的人口收缩，9种同时降稳定；(td2,tb6)P12=279841/160，倒序(td6,tb2)P12=83521/160，相同最终粗率但不同最终存量。只观察人口总数不能区分(b=d=1/5)与(b=d=1/20)两种不同出生/死亡规模。同类结论是简单存量人口会计的数学性质，不是现实预测准确性或人口惯性的年龄队列证据。

正式文件：[事前冻结协议](../../protocols/R150_THOMPSON1929_DAVIS1945_LEE2003_DEMOGRAPHIC_TRANSITION_EXACT_TIMING_PRESCORE_FREEZE_2026-10-20.md)（commit `795ceea8`）｜[科学报告](R150_PRIMARY_THEORY_AND_243_EXACT_VITAL_RATE_HISTORIES_SCIENTIFIC_REPORT_2026-10-20.md)｜[含全部程序、111项单测和243个完整原JSON结果的ZIP](R150_Thompson_Davis_Lee_Demographic_111_Tests_243_Models.zip)｜[验收状态](R150_FINAL_ACCEPTANCE_STATUS.json)｜[真实远端CI](../../.github/workflows/r150-demographic-transition-111-tests.yml)。

ZIP标准Python zipfile可解压：`python -m zipfile -e R150_Thompson_Davis_Lee_Demographic_111_Tests_243_Models.zip out`；out下 `python -m unittest -q test_r150_demographic_transition_exact.py`，`python r150_demographic_transition_exact.py > replay.json`。LZMA压缩但无需第三方依赖。R151才是Age Structured Population Models，**年龄结构与实际人口惯性不能从R150一项单一总人口状态获得**。

新增E2真人独立预测=0，E3真实历史预测=0，R073/PESEN v0.1继续冻结。研究顺序维持先结束全部既定R，再统一归纳分类，最后熔炼。
