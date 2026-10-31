# TH171 Smartcards第7地区结构性缺失、GP代理误分类与跨地区填补识别边界

研究日期及非中文原始来源检索日期：2026-10-31（Asia/Singapore）。
track: theory；status: THEORY_NOTE_BOUNDED。
target_key: (theory,ATANDA2019_A8_A9_DISTRICT7_GP_CARD_STATUS,TH171-theory-v1,structural_missingness_proxy_measurement_and_donor_transport)。
本轮承接TH170，属非盲态互补公开表格审计。仅使用已发表汇总计数与人工有理数推导，未接入个人资料、未下载原始受益人记录、未运行Stata、未建立真实因果效应。

## 一、来源、版本、直接阅读范围

S1 [A，原始第三方复现报告全文的指定部分，直接核对第3节脚注4、表A8完整第22至23页、表A9第24至25页、B1第26页] Atanda, Akinwande A. (2019-03; PDF封面2019、建议引文2018). *Biometric Smartcards and payment disbursement: a replication study of a state capacity-building experiment in India*. 3ie Replication Paper 23. DOI:10.23846/RPS0023。https://www.3ieimpact.org/sites/default/files/2019-06/RPS23_Biometric_Smartcards_and_payment_disbursement_India_3.pdf 。另有2019正式期刊版 DOI:10.1080/19439342.2019.1646782；本轮汇总数字只归于3ie PDF，不假定期刊版逐表一致。
S2 [A，作者公开原刊PDF第846页引言与第849页第4节案例，直接查看2页，其他章节未完整审读] Gelman, Andrew; King, Gary; Liu, Chuanhai (1998). *Not Asked and Not Answered: Multiple Imputation for Multiple Surveys*. Journal of the American Statistical Association 93(443):846–857. DOI:10.1080/01621459.1998.10473737；作者公开全文 https://gking.harvard.edu/files/not.pdf 。哈佛归档网页年份标为1999，原刊封面明确1998-09，保留书目版本差异。
S3 [A，作者公开2019年预印本v1第1至2.4节，直接审读识别限制、donor-based定义与非单调缺失] Chen, Yen-Chi; Sadinle, Mauricio (2019-04-24). *Nonparametric Pattern-Mixture Models for Inference with Missing Data*. arXiv:1904.11085v1. https://arxiv.org/pdf/1904.11085 。本轮未核对正式发表版，也未执行作者估计器。
S4 [B，同行评审原刊摘要] Molenberghs, Geert; Michiels, B.; Kenward, Michael G.; Diggle, Peter J. (1998). *Monotone missing data and pattern-mixture models*. Statistica Neerlandica 52(2):153–161. DOI:10.1111/1467-9574.00075。https://research.lancaster-university.uk/en/publications/monotone-missing-data-and-pattern-mixture-models/ 。
S5 [B，大学正式书目与摘要] Aßmann, Christian; Würbach, Ariane; Goßmann, Solange; Geißler, Ferdinand; Bela, Anika (2015). *Nonparametric multiple imputation for questionnaires with individual skip patterns and constraints*. Sociological Methods & Research. DOI:10.1177/0049124115610346。https://fis.uni-bamberg.de/entities/publication/e1a7b929-3aea-4aaf-8ac2-625fb85a336f 。仅摘要，跳题修复为候选方法。
检索日均为2026-10-31，未使用中文网站或付费论文。

## 二、直接核对公开A8/A9三重联合计数

3ie表格的“Carded GP”是村级支付系统转换状态，“Have Smartcard”是个人是否持卡字段。两者属于不同统计单位和处理版本。

| 项目、处理组内部GP类别 | 个人有卡 | 个人无卡 | 个人状态缺失 | 合计 |
| --- | ---: | ---: | ---: | ---: |
| NREGS，GP已转卡 | 1724 | 1181 | 2273 | 5178 |
| NREGS，GP未转卡 | 290 | 971 | 1080 | 2341 |
| SSP，GP已转卡 | 774 | 411 | 682 | 1867 |
| SSP，GP未转卡 | 213 | 393 | 277 | 883 |

NREGS处理组总数5178+2341=7519，已观察有卡2014、无卡2152、缺失3353，逐项与表A8吻合。SSP处理组1867+883=2750，有卡987、无卡804、缺失959，逐项与表A9吻合。

第7地区（公开表ID491）NREGS：1425名个人的持卡状态全部缺失，处理1037名均属于已转卡GP，对照388名属于未转卡GP。SSP：处理398人均在已转卡GP，只有2人明确有卡、396人缺失；对照159人在未转卡GP，持卡状态全部缺失。公开表未说明该地区究竟未询问、跳题、拒答、丢失数据或数据合并失败，不能认定缺失机制。

## 三、精确有理数审计与识别范围

若二元个人持卡状态的缺失值可任取0或1，则任一公开样本格子的持卡率尖锐描述界为 [已知有卡/N,(已知有卡+缺失)/N]。这些端点可分别将所有缺失赋0或赋1达到，不包含统计抽样误差。

| 项目 | 已转卡GP个人持卡率界 | 未转卡GP个人持卡率界 | 两类GP持卡率描述差界 |
| --- | --- | --- | --- |
| NREGS处理组 | 33.2947%至77.1920% | 12.3879%至58.5220% | 负25.2273至正64.8041个百分点 |
| SSP处理组 | 41.4569%至77.9861% | 24.1223%至55.4926% | 负14.0358至正53.8638个百分点 |

NREGS已转卡GP中至少1181人明确没有个人Smartcard，未转卡GP中至少290人明确有卡；SSP相应人数为411与213。故“GP已转卡=个人有卡”的确定性映射被公开观测直接否定。

若将第7地区从已转卡GP样本排除，NREGS剩余4141人（1724有卡、1181无卡、1236缺失），其持卡率界为41.6325%至71.4803%；SSP剩余1469人（772有卡、411无卡、286缺失），其界为52.5528%至72.0218%。排除地区改变了目标总体，不能据此宣称原总体缺失问题已解决。

第7地区内部NREGS处理组持卡率可从0到1，对照组也可从0到1，处理减对照的描述差可从负1到正1。SSP处理组持卡率界为[2/398,1]，对照[0,1]，组差界为[2/398-1,1]。两种缺失补全世界可保留完全相同的全部已发表记录及GP转换状态，却产生不同的真实个人持卡比例。

## 四、十二项条件性命题、竞争解释及反例

TH171-01 [S1] GP转换是行政层处理状态，个人持卡是个体层测量；已知GP转换不能逐人确定个人状态。反例：已转卡GP内1181名NREGS个人明确无卡。
TH171-02 [S1] GP未转卡也不能逐人判为无卡。反例：处理组未转卡GP内290名NREGS个人明确有卡。
TH171-03 [S1] 第7地区NREGS个人持卡观测概率为0，任何仅在该地区内部训练的有监督填补缺少标签支持；该观察是有限表格层的零支持，不等同于全人口必然零概率。
TH171-04 [S1] 第7地区SSP只有2个已知有卡记录，无法据此判断所有缺失者都持卡；该组条件支持极弱。
TH171-05 [S1，精确推导] 处理组GP类别持卡率差的无假设描述界均跨零；GP转换与个人持卡的方向关联在已发表汇总层面无法确定。
TH171-06 [S1，人工构造] 第7地区NREGS全部缺失赋0与赋1形成两个与公开表完全相容的世界；行政GP状态固定，个人真实采用率可截然不同。
TH171-07 [S2] Gelman/King/Liu的跨调查层级填补把“未问”与“未答”纳入建模，使用跨调查信息与权重；迁移到跨地区须另行验证问卷语义、权重及可运输性。作者研究对象是民意调查，不是Smartcards。
TH171-08 [S3] Chen/Sadinle区分可从观测分布恢复的部分与依赖识别限制的缺失分布；选择donor地区等同于引入跨地区条件分布假设，不能称为数据自身的证明。
TH171-09 [S3,S4] Complete-case、available-case、neighboring-case属于不同的识别限制；在第7地区完全缺乏NREGS标签时，使用其他地区的donor还需正支持及可运输假设。
TH171-10 [S5] 问卷跳题可能导致结构性缺失，变量在某些人群甚至可能不适用；填补前需先恢复问卷流程、适用人群及代码字典。
TH171-11 [S1] 第7地区处理组GP已转卡与个人状态全缺失可同时成立；这并未证明个人卡已发放、个人已实际使用，亦未证明行政GP指标错误。
TH171-12 [S1,S2,S3] 随机化分配的政策ITT、GP层转换、个人持卡率与个人使用率分别需要不同估计对象；用非随机持卡状态分组评价政策仍有采用选择与缺失偏差。

竞争解释：A问卷未包含该地区模块；B跳题规则或程序版本差异；C真实不回答；D数据拼接键失败；E公开报表转换/重编码。A至E均是待检验假说，现有表格不能识别。跨地区层级填补与完全保守界限属于不同方法路线，前者更精细但增加模型依赖，后者较宽但保持已刊数据逻辑覆盖。

## 五、四层连接、价值边界与验证清单

个体层：持卡、实际刷指纹、领取支付、被问及与拒答须分开。群体层：GP转换、地区同伴传播、服务点可达性可能共同影响实际使用和报告。制度层：问卷版本、行政GP编码、抽样权重、受益人主键及缺失值重编码决定观测机制。历史层：2010至2012实验执行、2014与2016论文样本变更、2019复现报告形成不同数据版本，跨期比较须固定字段定义。

验证次序：1合法取得README/问卷模块/变量字典，恢复地区7是否被问；2核对b17_useSmartcard、b26_1_swipeFingerprints与Have Smartcard是否同变量及缺失码；3核对GP行政指标的观察日期与个人持卡/使用时间；4先在有标签地区做预注册遮蔽检验，再审查向地区7运输所需的条件独立与正支持；5分别报告无假设界、假设敏感性与模型依赖的填补值；6取得合法原始字节后才可进行真实Stata复算及聚类推断。

科学状态：公开表格精确算术与理论边界，未完成真实微观复算、真实因果识别、独立历史留出或前瞻预测。R系列E1/E2/E3新增均为0。数学脚本：theory/th171_joint_proxy_bounds_20261031.py。C008满足2026-10-31，D002满足2026-W44，均只读不重复。

下一理论专题TH172：行政数据代理指标、制度执行版本与跨群体测量等值性的原始理论比较，避免连续仅围绕同一实验重复审计；如合法恢复Smartcards问卷字典，另立独立来源核验任务。
