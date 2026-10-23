# R275 正式科学报告：相同观察边缘与不同成对机制

日期2026-10-23 Asia/Taipei。原239候选目录12-005 Equifinality Analysis（P0）。研究编号R275，科研证据仅人工有限E1，无实际受试数据。

## 理论来源
von Bertalanffy (1968), General System Theory 中的等效终态概念，https://www.panarchy.org/vonbertalanffy/systems.1968.html 。Ruddell et al. (2019), *Information Theory for Model Diagnostics: Structural Error is Indicated by Trade-Off Between Functional and Predictive Performance*, DOI https://doi.org/10.1029/2018WR023692 ，讨论不同机制可拟合相似预测模式时的模型审计风险。参数观测等价的正式统计定义参考 *Linking Item Response Model Parameters* https://pmc.ncbi.nlm.nih.gov/articles/PMC4978781/ 。该项是原创有限人工机制反例，未复用任何作者数据。

## 事前冻结的三种人工生成机制
[先行冻结协议](../../protocols/R275_EQUIFINALITY_3_MECHANISMS_768_COMPLETE_PAIR_SOURCE_TYPES_PRESCORE_FREEZE_2026-10-23.md)，独立提交[c29ff305](https://github.com/edwardsage419/Psychohistory-Research/commit/c29ff305375f8510137f3a50bf20005fd695768d)。每个数据source含四个有序二元对(Ai,Bi)，i=1到4，每个Ai独立公平Bernoulli(1/2)。
1. IID_PAIR：每个B与A独立Bernoulli(1/2)，四种pair(00,01,10,11)各1/4。
2. COPY_PAIR：B=A，pair只能00或11，且各1/2。
3. FLIP_PAIR：B=1−A，pair只能01或10，且各1/2。

三机制下只观察完整四比特A向量的**联合分布完全一样**：16种A向量每种严格质量1/16。只看任何A统计量，无论观察多少这种独立pair的A边缘样本，均不能在这三机制之间作出辨别。因而“个体观测特征完全相同”并不等于“相同的群体机制”。

## 两种明确冻结观测设计
PARTIAL_A_ONLY只观察Ai，对三机制等先验1/3，三种likelihood都是1/16；MAP并列预先选择IID_PAIR，三机制条件识别正确率依次1、0、0，事前等权平均1/3。这一正确率对IID机制的偏斜完全来自**并列处置规则**，不是IID有更高观测支持。

FULL_AB_PAIR观察四个完整成对关系，IID对任意8bit原source似然1/256；全四对相等时COPY似然1/16，其余0；全四对反向时FLIP似然1/16，其余0；混合关系时只有IID非零。完整配对观察下，对IID真机制的MAP错误恰为全部4pair相等或全部4pair反向两相斥事件，每个条件概率(1/2)^4，故IID条件正确率7/8；真COPY或真FLIP各必被识别，条件正确率1；三真机制先验等权整体正确率(7/8+1+1)/3=**23/24**。全相等观察对COPY后验16/17，对IID后验1/17；全反观察FLIP后验16/17、IID后验1/17；混合关系时IID后验为1。**统计可辨识与有限样本百分之百分类是不同命题**。

## 全来源穷举、解析核验与机器CI
对每机制全部4^4=256完整有序pair源进行枚举，三机制共**768个带模型标识原source类型**，包含不可能源的0质量行，非零质量数依次256、16、16，共288。每条CSV逐项保存A投影、四pair相等次数、来源真实质量、两种观测设计分别对三模型的似然、后验、MAP选择及正确性。路线B无需原source枚举，仅用边缘公平分布、四次相等或相反事件概率与支持集合得到正确率1/3与23/24；原source加权与解析结论严格一致。

GitHub Actions第三job独立逐条重建全部768原source，复核包括零概率source在内的全部似然、后验、MAP分类、每机制source质量和A四bit边缘分布，每个CSV/JSON SHA256与机器人归档收据一致。[CI run39903913659](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39903913659)三个作业completed/success，Python3.11与3.12各50项真测试通过共100项，独立来源审计通过；机器人永久归档[提交d70cb4e5](https://github.com/edwardsage419/Psychohistory-Research/commit/d70cb4e542b47d3efe10c551a863408a2c31081e)。

[程序](r275_exact_equifinality.py) · [全部768原source CSV](R275_ALL_768_ORIGINAL_EQUIFINALITY_PAIR_SOURCES.csv) · [精确结果JSON](R275_EXACT_EQUIFINALITY_RESULTS.json) · [机器来源SHA凭证](R275_MACHINE_RECEIPT.json)。
源CSV SHA256 `2112c0104d2acc49e25e33cc34ac10f38729f259083a7a4b68f1b1f914c538cc`；结果JSON SHA256 `8a92ed16d3f230a3a035199dc0f035672f997a2694dfbe5c9ac46a469484079f`。

## 研究边界与后续
本项同源观测差异来自数学设定的配对复制或反转，没有加入真实社会心理、网络、制度、历史机制，更没有因果认知的独立测量。实验样本单位是模拟四pair配置，不是受试人。新增真人E2=0、真实历史E3=0；R073及PESEN v0.1维持冻结。下一候选原目录12-006 Model Identifiability（P0，拟R276）。遵守先研究所有原R、再统一归纳分类、最后熔炼。
