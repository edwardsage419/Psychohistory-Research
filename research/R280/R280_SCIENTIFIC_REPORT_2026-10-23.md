# R280 正式科学报告：Brier严格适当性与有限样本中的错误模型偶然胜出

日期2026-10-23 Asia/Taipei。原239模型目录12-010 Brier Score（P1），研究R280。有界人工E1数学证据，未使用任何真实受试/历史事件数据。

## 原始理论来源与任务边界
Brier, G.W. (1950), *Verification of forecasts expressed in terms of probability*, Monthly Weather Review 78(1):1–3，DOI https://doi.org/10.1175/1520-0493(1950)078%3C0001:VOFEIT%3E2.0.CO;2。Gneiting & Raftery (2007), *Strictly Proper Scoring Rules, Prediction, and Estimation*, JASA 102(477):359–378，DOI https://doi.org/10.1198/016214506000001437，原作者文本 https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf 。二元Brier是典型严格适当概率评分，具体Brier loss(q,y)=(q−y)^2。该研究以独立有限四bit人工数据重检其期望最优性，并量化一次小样本错误预测报告偶然优于真概率报告的机会；没有声称原创适当性定理或复现原论文实际经验结果。

## 来源设计与预先冻结
[事前冻结协议](../../protocols/R280_BRIER_STRICT_PROPRIETY_9_WORLDS_144_ORDERED_SOURCE_PRESCORE_FREEZE_2026-10-23.md)，独立事前GitHub commit[b21848cd](https://github.com/edwardsage419/Psychohistory-Research/commit/b21848cd58d9f9d581ce79c685467c49c32a6897)。三个真数据生成率p=1/4、1/2、3/4；三种不看结果事前冻结的报告q=1/4、1/2、3/4，合计9人工world。每source四个相互独立同p Bernoulli结果，2^4=16个有序原source且原质量p^K(1−p)^(4−K)，世界标签合计**144个完整人工原source配置**，同p的三个q重复使用同一原原子空间，不是144个真人实验。

每source保存四个原bit、真实概率p、报告概率q、四个逐bit Brier、以真p报告的四个oracle损失、样本均分及其差、错误固定q在该source严格优于真p报告的标记和并列标记。比较前q已冻结，没有用四bit数据拟合q，基于四bit后再选择更好的模型不能算独立预测。

## 双数学路线及真正验收值
路线A完整穷举全部144有序原source逐bit评分并按原质量Fraction加权，统计九world的总体期望损失、超额后悔值regret、样本错误q偶然得分更低概率和同分概率。
路线B不读取原source枚举器，仅用K∼Binomial(4,p)五个类别的组合概率，独立计算四次二元Brier均分的胜负与并列情况，并用平方展开证明：
```text
E[(Y-q)^2 | p]=p(1-q)^2+(1-p)q^2=p(1-p)+(q-p)^2
E[score(q)-score(p)]=(q-p)^2 >= 0
```
因此在冻结三真率中只有q=p能得到最低期望Brier，但这个结论与某次四bit样本的胜负不同。九world来源完整积分与独立二项式解析全部Fraction相同。

|真p|报告q|期望Brier|期望超额regret|P(q样本优于p)|P(同分)|
|---|---|---:|---:|---:|---:|
|1/4|1/4|3/16|0|0|1|
|1/4|1/2|1/4|1/16|67/256|0|
|1/4|3/4|7/16|1/4|13/256|27/128|
|1/2|1/4|5/16|1/16|5/16|0|
|1/2|1/2|1/4|0|0|1|
|1/2|3/4|5/16|1/16|5/16|0|
|3/4|1/4|7/16|1/4|13/256|27/128|
|3/4|1/2|1/4|1/16|67/256|0|
|3/4|3/4|3/16|0|0|1|

在真p=1/2下，报告q=1/4的总体风险5/16劣于真实p的1/4，但四条测试数据中有5/16真概率质量使其样本评分反而更低。真p=1/4、报告3/4时，四次中K=2可能造成两种模型评分相等，质量27/128。不能以一次有限来源结果或未经校正的事后模型比较等同于独立泛化优势。

## 真实来源与GitHub执行证据
[标准库完整程序](r280_exact_brier_strict_propriety.py) · [全部144原来源及两组逐行Brier CSV](R280_ALL_144_ORIGINAL_BRIER_SCORING_SOURCES.csv) · [九世界独立解析结果JSON](R280_EXACT_RESULTS.json) · [机器SHA256源凭证](R280_MACHINE_RECEIPT.json)。
[正式GitHub CI run39905121175](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39905121175)三job completed/success；Python3.11/3.12各83项真实unittest完成，共166项通过。第三独立来源CSV审计确实重新建立完整四bit原空间、源质量、四行q与p损失、九world均值与各五个K计数类别的错误样本胜出概率及源SHA256。机器人将全部CSV/JSON及SHA收据永久main归档[commit6d94abb6](https://github.com/edwardsage419/Psychohistory-Research/commit/6d94abb697633a44b12db4db587d38c27fce11c9)。

原source SHA256 `c34b7bb792a1df59d529b5b5ed86fd1303e724191fb53e0077b73453e3ad3d9b`；结果JSON SHA256 `a1fbc582436208be7611f48238b31c14b74325ca75eaddcd77abe7bbecb9b0a1`。

科研结论仅人工E1，新增真实人类E2=0、真实历史E3=0，原R073与PESEN v0.1冻结。下一原目录12-011 Logarithmic Score（拟R281），原R系列全部研究完成后才统一归纳分类，最后熔炼。
