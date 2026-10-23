# R307 科学报告：少数派一致性、私人信念与公开顺从的人工有限模型

日期2026-10-23 Asia/Taipei。原始239目录**03-016 Minority Influence Models**（P1）。形式验收 **CLOSED_BOUNDED_E1_ARTIFICIAL_R307_MINORITY_PRIVATE_PUBLIC_BAYES**，仅证明**项目发明的**有限数学机制可复算，不是1969年真实蓝绿知觉实验的复现，也不是1994元分析97项实验效应量的新估计。

## 一手文献与先前研究去重

Moscovici, S., Lage, E. & Naffrechoux, M. (1969), *Influence of a consistent minority on the responses of a majority in a color perception task*, Sociometry 32(4):365–380, DOI https://doi.org/10.2307/2786541；[PubMed馆藏](https://pubmed.ncbi.nlm.nih.gov/5373094/)。原作者研究真实参与者面对被少数人一致或不一致命名颜色时的反应。Wood, W., Lundgren, S., Ouellette, J. A., Busceme, S. & Blackstone, T. (1994), *Minority influence: a meta-analytic review of social influence processes*, Psychological Bulletin 115(3):323–345, DOI https://doi.org/10.1037/0033-2909.115.3.323。其对**97项实验**的元分析报告少数派影响在私人/间接测量较明显，并将少数派行为一致性作为重要调节。上述是真人原作与综合文献，**本研究没有原文的逐被试知觉CSV、原实验参数、可复核随机分配或97个实验的完整独立重算**。

之前R115 Informational Social Influence 已独立研究Bayesian action cascade，R116 Normative Social Influence 已研究公开/匿名表达，不可将相近“规范/信息”概念当作R307又获得新人群E2。R307单独构造**少数派行动的一致性/可信度证据门**和**数字多数压抑公开表达**的组合对照；其新算式不是Moscovici/Wood的作者模型。R303模仿学习、R304社会身份分配、R305自我分类及R306群体极化均各自保留原范围。

## 源冻结与人工演算全集

[事前研究协议](../../protocols/R307_MINORITY_INFLUENCE_CONSISTENCY_PRIVATE_PUBLIC_864_SOURCE_PRESCORE_FREEZE_2026-10-23.md)在源码和原结果生成前冻结，提交[4f74448e](https://github.com/edwardsage419/Psychohistory-Research/commit/4f74448e261ac61c65cd60926a056d6916a84e34)。

六个人工角色组成一组，少数派人数m∈{1,2}，其余为多数派（没有真人/动物）。先验少数观点受认可的假设概率p0∈{1/4,1/2}，重复证据曝光次数t∈{0,1,2,3}，少数派行为一致性c∈{0,1/2,1}、来源可信度k∈{0,1/2,1}和公开规范压力n∈{0,1/2,1}。每人工世界有独立的PRIVATE_BELIEF与PUBLIC_EXPRESSION两个观测渠道，构成**2×4×3×3×3×2=432个假设世界，864条完整人工source**。它们不是864名受试者、真实社交互动事件或历史时间序列。

自造贝叶斯证据强度L=1+c*k，先验赔率O0=p0/(1−p0)，经过t份条件独立、一样的假想少数派证据后的赔率Ot=O0*L^t；PRIVATE概率b=Ot/(1+Ot)。公开表达另设一个**自造规范保留率**z=1−n*(6−m)/6，PUBLIC概率e=p0+z*(b−p0)。每行保存完整贝叶斯逐步后验路径、两类渠道概率、证据强度、成员数、公开压抑值和偏离先验数值，所有分数使用Python Fraction精确运算。

这一构造没有任何实证强度校准，且规范压力被人为定义为影响公开表达但不影响私人状态。因而“私人概率较高而公开概率较低”是在规定函数下的**代数结果**，不能独立证明Wood1994的真人发现。

## 冻结正例、负对照和无法辨识参数的反例

当p0=1/4、t=3、c=k=1时，原先赔率1/3连续乘2三次，得Ot=8/3，PRIVATE概率**8/11**。同一假设条件但满规范压力n=1且m=2/6（其余4/6多数派）时，PUBLIC概率**9/22**；若只有m=1/6（其余5/6多数派），PUBLIC概率**29/88**，两者私人信念完全相同、公开表达有所不同。取消规范压力n=0时PUBLIC与PRIVATE都等于8/11。

对于同一先验，t=3，(c,k)=(1/2,1)与(c,k)=(1,1/2)的逐信号赔率倍率都是3/2，PRIVATE都得到**9/17**，在相同n、m下PUBLIC也完全相同。这是一个明确的**不可辨识性反例**：最终公开或私有选择概率本身无法把一致性效应从可信度效应拆开。真实研究须使用独立操纵/测量及未被混淆的指标，不能在这个有限玩具模型的可重复结果上虚报两个心理参数被分别验证。

不提供少数证据t=0，或c=0、k=0时，L=1，私人和公开都保持先验，不会凭空出现影响；n=0时两渠道完全一致。所有人工世界PRIVATE≥PUBLIC≥p0，并非关于所有现实少数派与公众观点的定律。p0=1/2且c=k=1、t=3时人工PRIVATE 8/9，只是合成分数，不能解释为真人改变态度的成功率。

## 可复现性与验收

[原生Fraction模型及2607项实际测试](r307_exact_minority_consistency_private_public.py)、[864原source CSV](R307_ALL_864_ORIGINAL_MINORITY_PRIVATE_PUBLIC_SOURCES.csv)、[432个世界全后验JSON](R307_EXACT_MINORITY_INFLUENCE_RESULTS.json)、[全源及结果SHA256机器凭证](R307_MACHINE_RECEIPT.json)、[完全不导入生产模块的逐步归一化Bayes独立复算和18项篡改测试](../catalogue_audit/independent_r307_source_audit.py)已永久归档。主程序计算赔率幂；第三方路径逐次构造归一化二元贝叶斯更新与公开保留因子，再逐source检查状态、完整路径、CSV、JSON和SHA。独立审计拒绝丢行、重复、伪造c、公开渠道、后验、初值和证据层级等。

[真实CI39953705822](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39953705822) **三个jobs completed/success**：Python3.11/3.12分别执行2607个主unittests和18项独立篡改审计；第三job重新生成原始864条人工source和全部结果，审计成功并永久提交main[归档commit d4ebc9cb](https://github.com/edwardsage419/Psychohistory-Research/commit/d4ebc9cbbffe550a61aa2d602fc3bceb79fb4850)。CSV SHA256 **77fdaadebbd80166746c9ef02b659482b929c33918982da3849827068a2302f9**，结果JSON SHA256 **f30bd38ab8fbcb168744ffe2c0c18c4f3c333d3add218d7d9040c46e9a95b7f4**。

R307仅有界人工E1；未计算实际个体行为、1994发表实验综合量或跨实验预测，更未得到社会变革和长期历史事件概率。原R073、PESEN v0.1协议继续冻结；239原模型主线仍在进行，整体分类与模型熔炼仍未开始。
