# A 子流程：Grujić 与 Lenaerts 2020 空间重复囚徒困境数据初筛

日期：2026-10-25。登记性质：公开来源核实及下载阻塞。**没有取得逐行原始数据，没有启动 R073 评分。**

## 已核实的英文公开来源
1. 论文：Grujić J. and Lenaerts T. (2020), *Do people imitate when making decisions? Evidence from a spatial Prisoner's Dilemma experiment*, *Royal Society Open Science* 7:200618, DOI 10.1098/rsos.200618；PubMed PMID 32874651。
2. 官方数据：Dryad DOI 10.5061/dryad.7fq25s8，公开版本日期 2020-07-27。网页列出 `DataSet.csv`（215.22 KB）、`README_for_DataSet.txt`（1.41 KB）和两份英文实验说明 PDF（各约 2.14 MB）。整套版本标示 4.50 MB。
3. 数据集网页明确说明：方格网络上的重复多人囚徒困境实验；两种处理分别提供或不提供收益差异信息。存在真人互动、重复行为及网络位置的研究潜力。

来源 URL：
* https://datadryad.org/dataset/doi:10.5061/dryad.7fq25s8
* https://doi.org/10.1098/rsos.200618
* https://pubmed.ncbi.nlm.nih.gov/32874651/

## 实际访问测试
在本轮使用公开网页下载入口实际请求 README（file_stream/296894）和原始 CSV（file_stream/296893），均返回 HTTP 403 Forbidden。可验证文件名称与公布大小，**不能验证**原始 CSV 行数、字段、时间单位、参与者标识、邻居身份、各场次划分、逐回合行为及许可的精确授权文本。

## 复现准备与适用性
优先级：A 子流程网络互动真人 E2 候选，`ACCESS_BLOCKED_403`。原实验为多人方格网络，不能直接当作 R073 双人固定协议的独立复验样本。若未来可取得文件，须先检查是否与已归档 R 系列来源重叠，确认原始行动及滞后时间语义、身份与场次隔离、网络边及数据许可；不得将其重新编码为双人数据以便迎合冻结模型。

真实 E2 新评分：0。真实 E3：0。新增费用：0。未购买或注册账户，未获取任何私人数据。
