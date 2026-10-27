# A轨 Fudenberg与Pathak公开真人公共物品博弈数据来源与R073资格审计

日期：2026-10-28（Asia/Singapore）。新登记来源：[MIT Blueprint Labs的unobserved_punishment公开复现仓库](https://github.com/MIT-Blueprint-Labs/unobserved_punishment)，固定Git提交 `f8d3760c954a8757ab16ac5c2f7a1c69d2517898`。README称研究为“Unobserved Punishment Supports Cooperation”，作者Drew Fudenberg、Parag A. Pathak；复现说明由Vendela Norman于2022-05-03整理。

## 实际取得与来源身份
实际通过GitHub公开内容读取 `clean_data/unobserved_dataset.csv` 全部177144字节，Git blob `f5767dd72928b16eaa30c8cc67af15b17ad25d4c`，同时读取 `Readme.txt`、`code/clean.sas`、`code/tables.do` 与一份 `raw_data/attend042707/data_main.TXT` 的内容。仓库包含六个实验场次的原始阶段文件、清洗SAS程序、Stata表格与图表复现代码，能够直接获取公开清洗CSV。复现说明特别指出论文Table 4第5列与复现包产生的估计不一致，需在未来正式复现中独立记录这一差异。

## 行为记录结构的实际验证
CSV共有28列、2400条参与者逐轮记录、六个session（C1、C2、T1、T2、T3、T4），构成132个session×subject身份组合。各场次结构如下：

| session | 参与者身份组合 | 每人轮次 | 行为行数 |
| --- | ---: | ---: | ---: |
| C1 | 24 | 10 | 240 |
| C2 | 20 | 20 | 400 |
| T1 | 24 | 20 | 480 |
| T2 | 24 | 20 | 480 |
| T3 | 20 | 20 | 400 |
| T4 | 20 | 20 | 400 |

总计110个session×period时间单元、600个session×period×group四人小组单元。全部600个小组单元恰有4条参与者记录。每条记录的opp1、opp2、opp3与同session、同period、同group的其他三人身份完全一致，2400条配对集合比较失败0。重复session×subject×period键0，轮次缺口0，空字段记录0，贡献值超出0至20的记录0。132个身份组合在研究期间均发生小组标签变更。额外逐行检查发现132个身份组合的实际三人对手集合均发生变化，2268次连续个人轮次转换中2268次对手集合有变化；后续任何历史行为特征必须按照真实对手ID与时间顺序建立，不能默认固定伙伴。

变量包括period、subject、group、contrib、三个对手ID及其贡献、三个惩罚选择、session、base、set与mod_period。原SAS清洗脚本显示`punish`是该轮对他人实施非零惩罚的计数（0至3），`you_punished`是其二值指标；`set`按1至10轮与11至20轮分段。不得把`punish`误读为随机处理组别，也不得跨session直接合并subject数值ID。132个session×subject身份组合的跨场次真实个人去重尚未核验。

## 许可、独立性与可复现性
仓库顶层文件清单未发现LICENSE文件，README也未给出清洗行为数据的明确独立再分发许可。当前仅引用来源、文件blob、聚合结构及本项目自编审计代码，不复制参与者级数据进项目仓库。公开读取无需付费、注册或访问私人资料。原研究的完整统计复现仍需核验SAS/Stata版本、论文差异、场次间独立性及小组重配规则。项目内[离线审计脚本](a_fudenberg_pathak_unobserved_punishment_source_gate_20261028.js)接受本地原CSV，要求Git blob身份匹配，输出聚合统计；[机器收据](A_FUDENBERG_PATHAK_PUBLIC_PGG_2400_ROW_SOURCE_RECEIPT_2026-10-28.json)保留本轮结构核验。

**R073直接复评分资格=NO**：此数据为四人公共物品博弈，单人10或20轮且每轮对手集合变化，与R073冻结的双人100轮囚徒困境、FP/SP分层及按独立实验场次留出评分规则不同。它适合在未来另立事前冻结的真人E2网络合作/公共物品研究，必须先确认许可、分组重配、有效独立单位与按时间的历史特征。当前新增正式真人E2预测0、历史E3预测0。不得为了适配数据而调整R073冻结规则。
