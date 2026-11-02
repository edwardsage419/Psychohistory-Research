# TH212 1912年孟买鼠疫逐年原始统计与1908年Table III影像审计补记

track: theory
subflow: original-primary-audit
run_date_utc: 2026-11-02
target_key: (theory,BombayPlagueCommission1908+1912,1908-published-scan+1912-published-scan,rat-species-sampling-denominator-and-temperature-chamber-table-identity)
status: COMPLETE_BOUNDED_PRIMARY_IMAGE; PARTIAL_HISTORICAL_IDENTIFICATION; NOT_RUN_HISTORICAL_REESTIMATION
observed_head_before_write: f8efb53c8fec78727f23519b68756ab1d8b172c7

## 原著、版本及实际阅读范围

1. Advisory Committee appointed by the Secretary of State for India (1908), “XXXI. On the seasonal prevalence of plague in India,” *Journal of Hygiene* 8(2):266–301, DOI 10.1017/S0022172400003314。原刊印刷p283 Table III及实验方法、p284 Table IV直接阅读；p283原刊页面影像由NIH PMC直接打开并目视核验。原刊PDF: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/A4CF58A9FFFF07650E1D8DD2E9ECD2A2/S0022172400003314a.pdf/xxxi_on_the_seasonal_prevalence_of_plague_in_india.pdf ; 原始影像页 https://pmc.ncbi.nlm.nih.gov/articles/PMC2167146/?page=18 。本轮未重读该篇全文。
2. Advisory Committee appointed by the Secretary of State for India (1912), “XLIX. Statistics of the occurrence of plague in man and rats in Bombay, 1907–11,” *Journal of Hygiene* 12(Suppl):221–226, PMCID PMC2167442, PMID 20474511。直接目视核验正式原刊扫描pp221–226六页，尤其pp222–226五个逐年统计表。https://pmc.ncbi.nlm.nih.gov/articles/PMC2167442/ 。1912原刊此篇无可核验的个人署名，沿用机构署名；未找到可确认DOI，使用稳定PMCID和PMID。
3. 原始统计为殖民时期调查记录。1912作者在p221称人类鼠疫数据来自市卫生部门，鼠数据来自市实验室，并明确鼠采集/检验部分周中断一两日，已对鼠数字作校正。不能假定五年为相同采样强度或同一城市鼠总体的随机样本。

## 原刊Table III的影像闭合与竞争解释

1908 p283 July–August 1906温度室同时试验，正式原刊影像逐行显示：
| 受试动物 | 室温80–83°F成功/总数 | 冷室70°F成功/总数 | 原刊成功率百分数 |
| --- | ---: | ---: | --- |
| Bombay rats | 5/29 | 13/46 | 17% 与28% |
| Ship rats | 8/25 | 18/27 | 32% 与66% |
| Guinea-pigs | 4/8 | 15/15 | 50% 与100% |

上述为不同动物组、不同样本量的实验成功比例，不能合并为单一实验的处理效应。p283明示冷室封闭并在地面铺石灰以吸收二氧化碳、保持相对干燥，温度与环境条件并未完全独立变化。不能把观察差异解释成已经识别的温度单独因果效应。1908 p284另有Jan–Feb 1907的25组对25组豚鼠热室实验（21/25与8/25），属于不同季节和实验安排，不能当成Table III的重复测量。

## 1912年五张年度原始表的年度总计

下表直接从正式原刊印刷pp222–226的每页底行和页眉抄录；单位为表列年度人类鼠疫死亡数、两种鼠类检出感染数及全年检验鼠只数，未复算每个半月行。

| 年份 | 全部检验鼠只数 | 人类鼠疫死亡数 | 感染 M. rattus 表列数 | 感染 M. decumanus 表列数 | 原刊页 |
| --- | ---: | ---: | ---: | ---: | --- |
| 1907 | 107875 | 6455 | 4553 | 14803 | 222 |
| 1908 | 110512 | 5441 | 2789 | 13512 | 223 |
| 1909 | 91540 | 5207 | 2277 | 9645 | 224 |
| 1910 | 119456 | 3661 | 2936 | 10851 | 225 |
| 1911 | 134401 | 3992 | 2436 | 11803 | 226 |

### 新增识别发现

**A. 年度感染鼠绝对数上升不等于鼠类感染率上升。**1909至1910年，表列感染M. rattus数量2277→2936，上升659/2277≈28.94%；全部检验鼠只数91540→119456，上升27916/91540≈30.50%。把感染M. rattus表列数除以全部检验鼠数，仅作为混合物种且受采样影响的代理比值，分别约24.87/1000和24.58/1000，反而略降。两种统计趋势不同。由于没有各年、各半月、各物种被检验总数及采样设计，不能据此计算M. rattus物种内感染率或估计真实鼠群流行率。1912作者还对部分鼠数字作过停采日校正。上述代理比值不应作为严谨阳性率。

**B. 人类死亡与鼠感染绝对数亦不可直接一一映射。**同一1909→1910年人类死亡5207→3661，下降1546/5207≈29.69%，M. rattus表列感染数却上升。调查覆盖、季节、物种、死亡报告、传播时滞、其他环境与制度因素均可造成差异。这只是原始统计口径与简单同向解释的冲突，尚无因果机制判定。

**C. 原刊“percentage above or below mean for year”列是相对年度均值的偏差。**它和每半月感染鼠占比、病例死亡率、或人口发病率均不同。对跨年或跨物种机制比较，应先恢复同口径计数、对应检验数、样本抽取/停采修正及观测期。

**D. 原刊p221明确提出M. decumanus流行稍早于M. rattus、人类流行随后发生的描述。**这是当时调查者基于季节图表的观察性时间顺序，不能据此确认物种间传染路径或单独识别季节因果。此项原作者解释与纯易感者耗竭、气候对跳蚤传染力、鼠群更替、采样偏差等竞争机制继续并存。

## 检查、边界及未读

本轮Python标准库Fraction按人工转录的指定表格总数和Table III分组计数执行13项精确算术/逻辑断言，13 PASS，0 FAIL；包含两个年度分子分母变化方向、三个Table III冷/热比较及p284 21/25与8/25差13/25。它只验证已输入数字的算术，不证明手工抄录每格均无误。

已直接核验原始扫描p221–226及p283；1908 p284本轮使用正式原刊PDF文字层，历史记录中已读。1912逐半月行、各物种检验分母、样本采集地点、校正算法、原始实验记录及1908实验分配方式未复核。1907至1911原始鼠只级记录、独立数据复算、真实因果估计、样本外预测、R系列E1/E2/E3及MARKET升级全部NOT_RUN。未下载或向公开仓库上传受版权限制的原始扫描。

与既有TH212的独立增量：1908 Table III原始图像实际闭合；1912五年原始统计表及原作者采样中断校正说明首次直接阅读；提出1909/1910感染鼠数与检验总数的分母竞争反例。沿用TH212，不新建TH编号、不融合模型。

C010 COMPLETE 2026-11-02，只读。D003 COMPLETE 2026-W45（2026-11-02），只读。R073及PESEN v0.1冻结，R272 P0仍开放，E1/E2/E3与MARKET未升级。CI未主动触发，费用新增操作0；账户计费与免费额度NOT_VERIFIED。

下一步：转向本周覆盖不足的另一独立学科原著；TH212如再开展历史复算，先寻找按物种及半月分开的检验总数、停采修正和明确的时间/地点口径。先全部R，再统一分类，最后有条件熔炼。
