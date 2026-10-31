# A轨公开真人文化传递数据核验：Martin 2016 ReShare 851840

日期：2026-10-31 UTC。目标键：(A,UKDA_851840,2016_public_record,seven_generation_cultural_chain_source_and_R073_gate)。本轮仅公开英文来源；没有获取私人记录、购买数据或注册账户。

## 官方来源与实查

UK Data Archive ReShare 官方目录：https://reshare.ukdataservice.ac.uk/851840/ 。DOI：https://doi.org/10.5255/UKDA-SN-851840 。题名 The formation of stereotypes through cumulative cultural transmission, experimental data。数据采集 2011-10-03 至 2014-04-30，公开登记日期 2015-06-30，最后更新 2016-05-24。研究机构 University of Aberdeen；实验在个人电脑上完成。

官方说明：受试者为大学本科生，每人作为文化传递链中的一代，连续七代；前一代记忆的社会目标特征作为下一代学习材料。主要结果测量为任务准确度与反应结构。这里的时间单位是实验代际/链内顺序，不能视为每个人的连续七次互动。

## 文件级核验

官方页面明确列出 `ESI0106881_Data_Archive.sav`，SPSS二进制格式，25kB，公开访问标记为 Anyone。另有 `Description_of_ESI0106881_Data_Archive.docx`，154kB，`ReadMe.txt`，4kB。说明文档和README列出 UK Data Service End User Licence；数据 SAV 的 License 栏为空，不能自行推断与文档许可相同。访问详情：https://reshare.ukdataservice.ac.uk/851840/ 。

本轮尝试通过公开页面访问 SAV 和 README，网页工具分别返回不支持二进制内容类型及Unicode解码错误。没有实际读入SAV字节。因此：实际字段名、样本行数、链ID、代次ID、每代行为条目、匿名身份编码、文件SHA256均为 NOT_VERIFIED。目录记录只能证明文件列示和标记公开，不能证明逐行复现可行。没有把真人数据复制入本仓库。

## 适用性与阻塞

R313候选：存在真实人类跨代信息传递、潜在链级独立单位，适合未来有限文化传递E2设计。与R313三节点空间邻居复制核存在结构差异；缺少已核验的两项二值特征和逐步有向邻居复制字段，直接模型评分 BLOCKED_BY_MEASUREMENT_MAPPING。

R073候选：实验为七代记忆传递，非同一真人双人囚徒困境的百轮行动序列，`R073_ELIGIBILITY=HARD_NO_BY_TASK_AND_TIME_UNIT`。不得将链内七代或研究年份误作百轮。

复现准备结果：`SOURCE_AND_OPEN_FILE_METADATA_VERIFIED`；`RAW_SCHEMA=BLOCKED`；`LICENSE_FOR_DATA_SAV=UNRESOLVED`；`R313_E2=NOT_RUN`；`R073_E2=NOT_RUN`。下一步仅在免费且合法的方式获取原始SAV及英文说明后检查变量、链ID和七代依赖，按链而非逐行分组；先做隐私和许可审核，再考虑独立样本评估。

不触发计费API、云算力、GitHub Actions或付费注册。
