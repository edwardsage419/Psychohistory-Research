# 心理史学原始239目录：R295习惯/R296 Rescorla–Wagner 有限数学研究与v1.0档案核验

日期：2026-10-23 Asia/Taipei。性质：科学分级严格受限的两个新E1研究包与原239候选逐行来源目录更新。既定主线为：全部R系列先研究与检验，结束后分类，最后才熔炼原创心理史学模型。**整体239科学结题NOT_ESTABLISHED**。

## 两项正式限定研究

| 项目与对应候选 | 事前协议冻结提交 | 完整原人工source | Python 3.11/3.12各主模型单测 | 本体三job CI |
|---|---|---:|---:|---|
| R295 Habit Formation / 01-019 P1 | [638948a4](https://github.com/edwardsage419/Psychohistory-Research/commit/638948a4fb2fdcc370dbbc2c2f9f634f4d61a57b) | 180 | 731 + 731 | [39920355215](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39920355215) SUCCESS |
| R296 Rescorla Wagner Learning Rule / 02-001 P1 | [78e947a3](https://github.com/edwardsage419/Psychohistory-Research/commit/78e947a3de8dbeb209edc473ae74f98eb6937904) | 40 | 211 + 211 | [39920891647](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39920891647) SUCCESS |

这两个测试都是研究者定义并穷举的人工配置，不是真人/动物观测；两个实验共**220条独立人工源状态**，双Python本体**1884次实际单测成功**。两项另有完全不导入正式主程序的原来源审计各14个逆向测试，分别在双Python与第三CI job重算，并将源CSV、计算结果JSON与SHA256永久归档，核心算法经独立解释与解析式交叉检查。

### R295结果与证据等级

[完整R295科学报告](../research/R295/R295_SCIENTIFIC_REPORT_2026-10-23.md)、[独立原来源审计](../research/catalogue_audit/independent_r295_source_audit.py)和[正式机读验收](../research/R295/R295_FINAL_ACCEPTANCE_STATUS.json)。文献锚Dickinson (1985) *Actions and habits*、Wood & Neal (2007) DOI https://doi.org/10.1037/0033-295X.114.4.843、Lally et al. (2010) DOI https://doi.org/10.1002/ejsp.674。冻结人工情境习惯强度H_n=1−(1−α)^n和混合行动得分U_A=(1−λ)V+λ·cue·H_n。90组同参数奖赏贬值配对中：完全目标导向30/30敏感，半习惯8/30，完全习惯0/30。训练α1/2四次得H=15/16；仅习惯情境匹配时贬值后仍选A，切换情境后选B。**模型中设定的λ和这些比率没有接受人类自动性测量或原作者原始数据验证。** E1-only；新E2/E3=0。

### R296结果与证据等级

[完整R296科学报告](../research/R296/R296_SCIENTIFIC_REPORT_2026-10-23.md)、[独立原来源审计](../research/catalogue_audit/independent_r296_source_audit.py)和[正式机读验收](../research/R296/R296_FINAL_ACCEPTANCE_STATUS.json)。原作者Rescorla & Wagner (1972) *A Theory of Pavlovian Conditioning*, 原作者[耶鲁大学官方出版列表](https://wagner.yale.edu/publications)，页64–99。RW模型的共享复合预测误差ΔV_i=α(λ−ΣV)给出人工阻断/解除阻断。8个人工世界，40条完整训练状态；α1/2时，A已预训练8次后AB强化4次，B最终强度1/512；没有A预训练则1/2；奖励增强为2时257/512。各线索独立误差的人工竞争对照B=15/16且不受A先前训练影响。**这证明所列离散数值方程产生这些人工机制，不代表原文动物实验得到相同数值，也未建立真实条件学习效应大小。** E1-only；新动物/真人E2=0，历史E3=0。

## 原239目录来源严格变更

| 项目 | v0.8（R294后） | v0.9（R295后） | v1.0（R296后） |
|---|---:|---:|---:|
| 原模型主R来源关联 | 182 | 183 | **184** |
| 共享早期范围数学关联（不可双计） | 3 | 3 | **3** |
| 早期范围有限关联（非主R） | 5 | 5 | **5** |
| 现有核对材料无逐条关系 | 49 | 48 | **47** |
| 主R关系尚待确认 | 54 | 53 | **52** |
| 原始候选模型总数 | 239 | 239 | **239** |

[完整239项v1.0证据索引](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.0_2026-10-23.json)从[v0.9](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.9_2026-10-23.json)仅变更02-001一行；v0.9从v0.8仅变更01-019一行。所有238/237其他候选项目原来源字段不变；239个原始模型唯一ID、顺序、优先级不变。**184是已核验主研究来源指向数，不等于184项论文的独立真实实证复现，也不代表184个模型都有广泛预测效力。**

[当前未核52项P1/P2目录队列](ORIGINAL_239_PENDING_52_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)：P1 **25**，P2 **27**。未建立关联仍需调查历史研究档案，不能解释为科学否证或从未研究。下一个原目录 P1 **02-003 Q Learning**。

目录级独立代码与真实CI：
* [R295 v0.9原239一行核验程序](../research/catalogue_audit/verify_p1_r295_crosswalk_v0_9.py)、[run39920555825](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39920555825)三个成功作业；
* [R296 v1.0原239一行核验程序](../research/catalogue_audit/verify_p1_r296_crosswalk_v1_0.py)、[run39921236962](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39921236962)三个成功作业。

总计4个研究/目录CI工作流、**12个成功作业**；每项目录元数据审计用Python3.11/3.12并在第三job独立验证原始行映射、源文件SHA、E2/E3不升格。源级档案与实际科学证据等级始终分开。

## 继续推进要求

R297应先核查旧R系列中Q-learning是否已有可重复使用的原作者代码、具体任务和真人独立预测评估，避免重做相同机制；再为原始02-003追加被明确限定的独立审计。若仅能构造人工数学，则依同一标准冻结事前协议、对照竞争模型、列明可检验的负对照与E2/E3=0。R073/PESEN v0.1仍然冻结；分类/熔炼和个人辅助决策系统暂缓。
