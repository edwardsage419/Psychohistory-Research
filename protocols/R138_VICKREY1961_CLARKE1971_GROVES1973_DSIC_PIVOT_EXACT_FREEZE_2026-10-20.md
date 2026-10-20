# R138 事前冻结：Vickrey 1961、Clarke 1971、Groves 1973的真报激励、VCG与预算边界
日期：2026-10-20。既定目录 P2 05-014 Mechanism Design。本协议在R138源码和正式枚举编写前创建。

## 一手文献身份与实际阅读
Vickrey (1961), Counterspeculation, Auctions, and Competitive Sealed Tenders, Journal of Finance 16(1):8–37, DOI 10.1111/j.1540-6261.1961.tb02789.x；原刊 https://cramton.umd.edu/market-design-papers/vickrey-counterspeculation-auctions-and-competitive-sealed-tenders.pdf ，直接可视核阅印刷20–21页(PDF index13–14)§III最高报价得标、次高价付款和无串通假设。
Clarke (1971), Multipart Pricing of Public Goods, Public Choice 11:17–33, DOI 10.1007/BF01726210；原刊 https://ranger.uta.edu/~weems/NOTES6319/PAPERSTWO/clarke.pdf ，直接核阅印刷17页(PDF index1)需求揭示与多部定价。以下公共项目二元pivot是项目新建的Clarke-Groves离散特例，未声称复现原连续公共品全部公式。
Groves (1973), Incentives in Teams, Econometrica 41:617–631, DOI 10.2307/1914085，原刊 https://ranger.uta.edu/~weems/NOTES6319/PAPERSTWO/groves.pdf ，直接核阅印刷624页(PDF index8)Eq3.2–3.4其他主体效用的补偿项；以下简单VCG不是该论文完整随机团队模型原程序。

## 原定有限验证全集
A. 单物品三人次价密封标，估值和报告均为{0,1,2,3,4}，报价最高者得标，平局最小索引胜，赢家支付次高报价，输家0；完整125个真值档案×3主体×5单侧报价=1875次如实报告弱占优检验；并列最优不误称严格占优。对照首价支付自己报价，真实(4,1,0)首价真报4得0，偏报2得2，只证明这一具体反例。
B. 三人，两件异质商品A/B，每人最多得一件（unit-demand），每件至多一人，包含全空、6种单件、6种双件，共13种合法配置；每人私值二元坐标取{0,1,2}²，共9种类型。按福利最大配置，以固定字典序处理平局；pivot支付=无本人时其他人最大福利−当选配置其他人福利。严格枚举729真值档案×3人×9偏报=19683次；真报弱占优、真实福利最优、非负付款、真实个人理性与支付不必等于单物品第二高价单独核查。
C. 三人不可排他二元公共项目，成本5，每人价值∈{0,...,5}，总报告值≥5时建造，平局建造；若建造，税_i=max(0,5−∑其他人的报告)，否则0；真实效用=真实价值*建造−税_i。216档案×3人×6偏报=3888次弱占优检验。例(5,5,5)建造税款全0，预算余额−5；(2,2,2)各税1，预算余额−2。配置效率、私人激励相容、预算平衡必须三门独立。无界报告、同谋、非拟线性和动态社会行为不在本期验证。
D. 对照非pivot收费：建造时每人按自己报告值付税；真实(5,5,5)中首人真报5效用0，偏报0在其他人报告不变时仍建造，私人效用5。只证实该指定收费法不满足DSIC，不对任何其他机制泛化。

## 科研和机器门限
Python标准库整数与Fraction严算，不以玩具配置冒充真人。分开两种机制独立验证路径：直算用户真实净效用及由总福利差导出的pivot价格。源码/测试/输出/科学报告SHA256并随研究文件版本化。必须实际运行GitHub Actions Python3.11和3.12全部测试和全域复算才能签署远端合格。
E2新增真人0，E3新增历史概率0。原R073与PESEN v0.1保持冻结。全R模型学习结束后再统一分类，最后熔炼。
