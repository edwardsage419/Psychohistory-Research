# R116：规范性社会影响——社会地位压力与信息性社会影响的数学区分

日期：2026-10-19（Asia/Taipei）。原有239候选目录 P0 03-005 Normative Social Influence，研究编号R116。**LEARNING_COMPLETE_BOUNDED_PRIMARY_SOURCES_AND_STATUS_INFORMATION_IDENTIFIABILITY；仅第一手文献和自定义数学反例的限定学习已验收，真人E2=0；PESEN v0.1及R073冻结。** 此状态不代表整个规范性社会影响理论被验证，更不意味着心理史学模型已经开始熔炼。

### 原学术来源

* [Solomon Asch (1955) 原刊《Opinions and Social Pressure》](https://doi.org/10.1038/scientificamerican1155-31)，[MIT高校原印刷PDF副本](https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Influence_Compliance/required_readings/1Asch_1955_Opinions_and_social_pressure.pdf)：核阅原文第3–4页，作者记录123名受试者、相关错误多数试次选择中的36.8%跟随；本项目没有原始逐人判断数据，不将此群体汇总百分比称为项目E2复现。
* [Deutsch & Gerard (1955) 信息性和规范性社会影响的原创实验论文](https://doi.org/10.1037/h0046408)：核对官方[PubMed](https://pubmed.ncbi.nlm.nih.gov/13286010/)与可获得的出版方预览，未取得原始行为数据、未重新估计两种原因的效应。
* [Bernheim (1994) 《A Theory of Conformity》](https://doi.org/10.1086/261957)：阅读[原刊全文副本](https://www.haverford.edu/sites/default/files/Bernheim1994.pdf)第841–844页及[作者本人论述](https://bernheim.people.stanford.edu/publications/theory-conformity)。在该真实理论中社会地位通过他人对偏好类型的推断间接受行动影响，处罚是均衡内生；**本项目的外生固定地位成本toy不属于Bernheim原方程/原均衡的重现**。

### 真正可复算的数学机制与主要结论

事先冻结精确Fraction有理参数：自己的私人信号倾向选择0，私信可靠度3/5、初始Pr(V=1)=2/5；群体同向报告选择1且视为单条条件独立的消息。强信息可靠度3/4，Bayes更新后主观Pr(V=1)=2/3；弱信息可靠度11/20则主观Pr(V=1)=22/49。公众可归因的表达且与可见群体不一致时，外生惩罚收益1/4；本人原选项0的客观内在期望优势为1/5，故只有当成本严格高于1/5才会因压力改选1，等于门槛时按预冻规则选择0。

四个原冻结toy在“未见群体匿名／未见群体公开／见群体匿名／见群体公开”的选择1格为：
* NO_INFLUENCE：0/0/0/0
* NORMATIVE_ONLY：0/0/0/1
* INFORMATIONAL_ONLY：0/0/1/1
* BOTH：0/0/1/1

公开跟随群体的相同行动，在纯规范压力toy下背后的私人Pr(V=1)=2/5，在纯信息toy下为2/3；强消息下信息toy与两通道toy甚至在完整四格行动上都不能区分，单纯增加匿名条件**并不能保证全面识别压力效应**。减弱单条消息可靠度后，纯信息toy在公开条件也保持私人行动0，两通道toy却因地位损失仍公开选1；此分离仅针对合成假设，不等于真实干预或心理因果识别。

**来源和计算必须区分**：代码实现的是研究者外加固定声誉成本，不能当成Asch受试者的真实动机分解、Bernheim内生均衡重现或Deutsch–Gerard两类社会影响的实际效应量。信号条件独立是模型输入假设，不允许把相同来源的多位人物意见自动当独立证据。正确采集原私人判断、信息来源、公共/私人表达条件、可见性及其分配才能进一步进行真E2。

### 研究档案与真正机器执行

[GitHub Actions run 39242176948](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39242176948) **success：48项独立合成/数学测试通过、失败0**；机器记录中源代码、测试与报告SHA256，以及四机制2×2/弱信息反例结果，已由Actions机器人提交并由GitHub文件接口回读。

* [事先冻结协议](../../protocols/R116_NORMATIVE_SOCIAL_INFLUENCE_PRIVATE_PUBLIC_STATUS_VS_INFORMATION_SOURCE_FREEZE_2026-10-19.md)
* [第一手文献、数学结构及科研限制正式报告](R116_ASCH_BERNHEIM_PUBLIC_NORMATIVE_VS_INFORMATIONAL_MECHANISM_SCIENTIFIC_REPORT_2026-10-19.md)
* [精确Fraction概率及双通道实验实现](r116_normative_public_status_vs_informational_cue_exact.py)
* [48项严格单元测试](test_r116_normative_public_status_vs_informational_cue_exact.py)
* [实际CI与研究源码SHA验收收据](R116_PHASE_A_48_SYNTHETIC_PUBLIC_STATUS_INFO_CI_ACCEPTANCE.json)
* [正式科研验收](R116_FINAL_ACCEPTANCE_STATUS.json)

复算指令：`PYTHONPATH=research/R116 python -m unittest -v research/R116/test_r116_normative_public_status_vs_informational_cue_exact.py`，仅标准库、没有外部原始人类行为文件。下一步继续原既定R模型学习，所有模型完成后才统一分类和熔炼。R073与PESEN v0.1保持冻结。
