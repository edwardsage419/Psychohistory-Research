# A子流程：V-Dem v16时间单位与公开获取路径补充核验

日期：2026-10-26。继承 `research/data_scout/VDEM_V16_2026_COUNTRY_YEAR_INSTITUTION_HISTORY_SOURCE_GATE_2026-10-26.md` 已登记的官方来源，避免重复登记为另一独立数据集。状态：SOURCE_TIME_UNIT_AND_FORM_GATE_VERIFIED / RAW_BYTES_PENDING。

官方英文页面 https://www.v-dem.net/data/the-v-dem-dataset/ 及官方版本档案 https://www.v-dem.net/data/dataset-archive/ 在本轮重新核验：v16于2026年3月发布。Country-Year Full+Others为531指标、251指数及62项外部指标；Country-Date含531指标与95指数；Coder-Level为273指标。Country-Year、Country-Date、Coder-Level是同一发布体系的不同观测单位，不能把三个文件误计为三个独立历史实验。Country-Date的具体日期粒度、原始日期列名仍待实际数据核验。

官方Country-Year Core v16下载表单 https://v-dem.net/data/the-v-dem-dataset/country-year-v-dem-core-v16/ 要求电子邮箱、隐私处理同意等字段。本项目未填写任何个人信息或注册账户。官方免费GitHub `vdeminstitute/vdemdata` 提供v16 RData替代路径，前一轮已经核验其Git blob `5a472621427337cebf032a9c4e397e0bedd57aea`，但本环境容器外网DNS不可用，GitHub连接器不提供该大型二进制文件的原始行读取。此次没有获取新原始字节，不能声称验证列名、国家数、时间范围、缺失或观测者身份。

许可继续按V-Dem官方FAQ的CC BY-SA 4.0记录，需署名并对衍生发布遵守相同方式共享；R软件包许可证与数据许可证分开。官方明确不建议直接跨版本比较绝对指数，历史评分会随编码员、覆盖范围及测量模型更新而修订。若将v16回填历史年份用于当年事前预测，可能引入事后修订信息，必须冻结版本及当时可得性。国家年度留出应按国家分组或严格时间前推，并核查相邻年份和同国测量依赖。不能用Country-Year指数替代R176四主体微观行动、也不能用于R073二元重复博弈评分。

当前复现准备结果：数据来源、许可、候选观察单位与下载障碍已记录；实际原始字段、逐行数据、哈希、可复现的历史标签与事前时间切分均OPEN。新增E2真人预测=0、E3历史预测=0；R主线优先，A数据下载顺延。所有来源为英文官方网页及官方GitHub。