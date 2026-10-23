# 心理史学 R278—R280：模型平均、预测校准、严格适当Brier评分，连续三项原目录正式E1研究验收索引

日期2026-10-23 Asia/Taipei。原239候选目录严格接续12-008 Model Averaging and Ensembles（R278，P2）、12-009 Forecast Calibration（R279，P1）、12-010 Brier Score（R280，P1）。三项均先行冻结，后完成全原source穷举、独立数学解析、Python3.11及3.12真实unittest、GitHub Actions第三独立来源CSV与SHA256复核、机器人永久提交原始CSV/结果JSON/哈希、科学正式报告和机器验收。科研仅有界人工E1，新增真人E2=0、真实历史E3=0；原R073与PESEN v0.1未变。

## R278 模型平均与集成（12-008）
[事前冻结](../protocols/R278_BAYES_MODEL_AVERAGING_12_WORLDS_768_COMPLETE_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [完整研究及执行源码](../research/R278/README.md) · [正式科学报告](../research/R278/R278_SCIENTIFIC_REPORT_2026-10-23.md) · [正式机器验收](../research/R278/R278_FINAL_ACCEPTANCE_STATUS.json) · [GitHub最终run39904644080](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39904644080) · [完整原source永久归档0f39a4a7](https://github.com/edwardsage419/Psychohistory-Research/commit/0f39a4a753aa47bc4484b9de429da12a316196cb)。

三真p×四冻结报告政策＝12人工world，每world四训练bit和两独立测试bit的全部64原source，**768个带policy标签的完整人工原来源配置**。两点候选q=1/4、3/4，HARD_SELECT在K=2似然相等时预定选择低q，BAYES_AVERAGE以等先验更新两点权重；FIXED_HALF和TRUTH_ORACLE理论基准。真p=1/4时HARD_SELECT未来Brier205/1024低于BMA 87/410；真p=3/4时BMA 87/410低于HARD_SELECT259/1024；真p=1/2时BMA46637/168100优于HARD_SELECT5/16，但仍输固定半概率1/4。全source穷举与独立K~Binomial(4,p)未来损失公式相同，不能据此宣称BMA无条件普遍更好。双Python各108真测试，总216项全部通过，三个CI作业success。

## R279 预测校准与Murphy可靠性-分辨力-不确定性（12-009）
[先行冻结](../protocols/R279_FORECAST_CALIBRATION_9_WORLDS_144_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [原source和完整执行程序](../research/R279/README.md) · [科学报告](../research/R279/R279_SCIENTIFIC_REPORT_2026-10-23.md) · [正式机器验收](../research/R279/R279_FINAL_ACCEPTANCE_STATUS.json) · [首次失败run39904785939](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39904785939) · [修复后最终全成功run39904942557](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39904942557) · [永久source归档1f7275b3](https://github.com/edwardsage419/Psychohistory-Research/commit/1f7275b346824e5b235a9fcdf59bd10d40028d6c)。

两个真率不同的人工组各有两次二元观测，三冻结真实概率对×三预测概率政策＝九人工world，各16原source，**144原source完整类型，其中99正概率**。在两个群体真率为1/4、3/4时，所有人统一报q=1/2仍是总体完全校准（REL=0），但因只有同一个预测bucket而RES=0，Brier=1/4；正确分组报1/4、3/4则REL=0、RES=1/16、Brier=3/16。全部九世界population Brier=REL−RES+UNC由真实总体条件概率分桶并与全source加权严格一致；不能说有限一次样本的经验校准已测为0。**执行修复史保留**：首轮因多行assert语法错误失败，仅修正语法后重跑双Python各84真测试，共168成功，第三来源机器审计及永久机器人归档均成功。第一次失败绝不被计为成功CI。

## R280 Brier评分严格适当性与样本偶然误选（12-010）
[事前冻结](../protocols/R280_BRIER_STRICT_PROPRIETY_9_WORLDS_144_ORDERED_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [全源码和144原source](../research/R280/README.md) · [正式科研报告](../research/R280/R280_SCIENTIFIC_REPORT_2026-10-23.md) · [正式机器验收](../research/R280/R280_FINAL_ACCEPTANCE_STATUS.json) · [GitHub run39905121175](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39905121175) · [全原来源机器人归档6d94abb6](https://github.com/edwardsage419/Psychohistory-Research/commit/6d94abb697633a44b12db4db587d38c27fce11c9)。

三真p×三事先固定q＝九人工world，每world四独立Bernoulli的全部16有序原source，共**144个人工完整source类型**。严格适当性真值E[(Y−q)^2]=p(1−p)+(q−p)^2；真q=p最小化期望风险，但**不能保证每条有限样本q=p得分一定最好**。例如真p=1/2而错误报告q=1/4，其总体真实风险5/16高于真p的1/4，但只有四次观测时错误q的样本Brier更低概率为5/16。完整原source对评分胜负及同分概率的质量积分严格等于独立的K~Binomial(4,p)解析分类。双Python各83真实unittest共166通过，三job success，全部原source与SHA永久归档。

## 三项统一验收核算与边界
三项合计**30个人工固定world**（12+9+9），**1056个带world/policy标签的完整人工原source**（768+144+144；不同world共享来源而且R279含零质量配置，不能等同真人受试数）；Python双版本真实测试216+168+166=**550次均通过**；三个**最终成功**CI工作流分别3job，合计9个completed/success CI job。另R279首次**失败**CI run单独保留并准确标识，未将其记入九成功作业。每项均有研究协议冻结提交、来源完整CSV/分析JSON、机器SHA256凭证、科学报告与正式机读有界验收。实验仅证明有限数学空间严格概率机制及数据分割下的一些可复验事实，没有新增真实真人E2/历史E3、也没有跨实验R073的新独立预测效果。R073和PESEN v0.1均冻结。

原239候选目录下一项确认**12-011 Logarithmic Score（P1，拟R281）**，其后12-012 Open Reproducible Workflow and ODD。继续按用户确认的主线：先完成全部原R系列研究，再统一归纳分类，最后原创模型熔炼；个人辅助决策系统继续暂缓。
