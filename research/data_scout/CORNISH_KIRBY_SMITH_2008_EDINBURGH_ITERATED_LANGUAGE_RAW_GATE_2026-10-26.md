# A 数据侦察：Cornish、Smith、Kirby 真人迭代学习实验原始数据资格门

日期：2026-10-26。状态：OFFICIAL_DATASET_LICENSE_CHECKSUM_VERIFIED / RAW_BYTES_PENDING / MODEL_TRANSFER_BLOCKED。

## 官方来源
爱丁堡大学 DataShare 官方原始数据： https://datashare.ed.ac.uk/items/97b12ae7-9808-4e35-812c-5a4b149f7eb0 ，DOI https://doi.org/10.7488/ds/1586 ，2016-12-14 发布。原研究 Kirby, Cornish & Smith (2008)，PNAS，DOI https://doi.org/10.1073/pnas.0707835105 。数据归档名称 `Artificial languages created through iterated learning experiments by Kirby, Cornish & Smith (2008) and Cornish (2011)`。

官方完整元数据： https://datashare.ed.ac.uk/items/97b12ae7-9808-4e35-812c-5a4b149f7eb0/full 。单文件 `CornishData.xlsx`，标称60.83KB，官方 MD5 `29257082f9e930a62f54b029ba9be98b`，元数据 `dc.rights` 明示 Creative Commons Attribution 4.0 International Public License。数据表包含 Cornish 博士论文表 1-A 至 1-D 和 III-A 至 III-D，对应2008年论文实验1和2。官方特别说明原论文补充材料 Table S7 行顺序有误，归档文件为应采用的修正版。

## 字段与时间单位资格
实验单位为真人迭代学习链中的人工语言及传承代次，来源为原研究实验表。**尚未读取工作簿内部表头和实际单元格**，链ID、参与者身份、每代词形、刺激编码、缺失记录、代次编号、独立实验链数量、重复观察与可用分组均未核验。不可据网页描述臆造字段或样本数。下载链接 https://datashare.ed.ac.uk/bitstreams/f7b63c16-654b-4b47-83bf-b8df0b1a117e/download 在当前网页读取工具因 XLSX 二进制格式不受支持，容器下载亦失败；原始文件 SHA256 尚未取得，官方 MD5 是来源元数据，尚未本地复核。

## 模型复现资格
该数据可优先支持真实人工语言代际传承的描述性 E2 审查。R175 冻结模型为二元潜在记忆、条件独立位翻转报告与后验抽样/MAP，真实实验是多词形人工语言学习，尚未证明其可按冻结变量与概率评分直接映射。不得为适配数据而事后更改 R175 原模型或 R073 冻结评分规则。下一步先获得原始工作簿、校验 MD5、检查 sheet 与链身份、构建独立链的预先划分和许可署名记录；若不能匹配则记录阻塞。无新增E2预测评分或E3历史验证。

## 费用与来源
官方英文机构站点，公开访问且标示 CC BY 4.0，无需购买或付费注册。本轮未产生数据购买或计费API费用，账户账单未核验。
