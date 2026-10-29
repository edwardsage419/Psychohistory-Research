# A轨：Grujić与Lenaerts 2020 Dryad 数据授权政策及原始文件访问复核

UTC日期：2026-10-29。目标键：(A,doi:10.5061/dryad.7fq25s8,2020,license-and-raw-access)。承接已归档 `A_GRUJIC_LENAERTS_2020_DRYAD_SPATIAL_PD_50ROUND_SOURCE_GATE_2026-10-29.md`，仅记录本次新增证据，不重复声明已取得CSV。

## 本轮实际核验的英文一手来源

1. Dryad正式数据页 https://datadryad.org/dataset/doi:10.5061/dryad.7fq25s8 ，2020-07-27发表。公开登记四份文件：DataSet.csv 215.22 KB；README_for_DataSet.txt 1.41 KB；两份英文实验说明PDF各约2.14 MB。原论文链接 https://doi.org/10.1098/rsos.200618 。
2. Dryad机构正式政策 https://datadryad.org/mission 明确Dryad发布研究数据采用CC0；正式文件要求 https://datadryad.org/help/requirements/files 规定不接收与CC0冲突的数据许可，要求人类受试者数据适当去标识化。
3. 原论文 https://pmc.ncbi.nlm.nih.gov/articles/PMC7428279/ 公开声明数据在上述Dryad归档；此前已核验九个实验会话、144名参与者、每场16人、50轮的多人空间重复囚徒困境设计。
4. 本轮直接点击Dryad页面的README_for_DataSet.txt下载入口，目标 `https://datadryad.org/downloads/file_stream/296894` 返回HTTP 403。公开REST元数据URL `https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.7fq25s8` 在当前网页工具不可访问。

## 字段与复现门槛

真实CSV仍未成功读取，因此字段名、逐轮时间单位、原始记录行数、会话ID、匿名参与者ID、固定邻接关系、数据缺失及可复算的逐人行动记录均为NOT_VERIFIED。按论文设计推算的144×50=7200人轮次仅是理论最大完整计数，不得当作实际CSV行数。

Dryad平台级CC0发布政策提供了积极的授权证据；本轮尚未取得该特定版本的官方API license字段或原始文件头，因此记录为 `PLATFORM_CC0_POLICY_CONFIRMED_DATASET_LICENSE_METADATA_UNREAD`。不分发任何原始数据。

R073冻结的双人100轮直接复验条件：NO，因50轮且多人空间网络；可用于未来单独冻结的网络模仿机制E2研究，需先确认场次、邻居、反馈与留出划分，禁止事后调参。真实E2预测新增0，E3新增0。

## 后续

优先通过公开免费渠道重试原始README及CSV或Dryad官方只读元数据，取得字段字典和版本许可字段；成功后按session划分独立留出，保留人和网络内相关性。若仍HTTP403，仅维持来源登记与阻塞状态，不凭论文摘要伪造记录。
