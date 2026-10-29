# A轨公开真人数据侦察：Grujić 与 Lenaerts 2020 空间重复囚徒困境

日期：2026-10-29 UTC。目标键 (A,doi:10.5061/dryad.7fq25s8,2020-v1,source/identity/license/R073-gate)。去重：main现有R073、R077及ds007822数据审计和当轮交接均已读取，未发现该DOI的本轮A轨登记。只读调查，不下载非公开材料，不提交第三方原始数据。

## 一手证据

论文：Grujić J., Lenaerts T. (2020), *Do people imitate when making decisions? Evidence from a spatial Prisoner’s Dilemma experiment*, Royal Society Open Science 7:200618，DOI https://doi.org/10.1098/rsos.200618，全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC7428279/ 。论文方法确认：4×4周期方格网络，每场16名参与者，四邻居交互，9场独立实验会话、共144名参与者，每场50轮；有收益信息5场共80人，无收益信息4场共64人。决策在网络上互相依赖，不能把个人或邻居行为当独立实验。研究处理收益信息影响模仿行为的问题。

公开数据登记：Dryad DOI https://doi.org/10.5061/dryad.7fq25s8 ，2020-07-27公开。页面实际列出 `DataSet.csv`（215.22 KB）、`README_for_DataSet.txt`（1.41 KB）、两份英文实验说明PDF（各约2.14 MB），总文件约4.50 MB。登记页面描述为方格网络多人重复囚徒困境。

## 字段、来源和许可关口

论文确认时间单位为单轮、场次单位为16人网络、参与者嵌套在9场内。真实逐轮行动有公开CSV候选，尚未读取CSV行及README字段字典。Dryad下载链接尝试返回HTTP 403，因此本轮无法验证CSV实际列名、场次ID、参与者位置ID、行动缺失、收益记录、数据行数、文件hash或每场完整50轮。没有把论文推算的144×50=7200当作实际已读取记录。

论文正文使用CC BY 4.0。Dryad页面未在本轮成功提供该数据集的文件级再分发许可；不能由论文许可推定CSV许可。许可状态：DATA_REUSE_LICENSE_UNVERIFIED，禁止再分发原CSV。无需购买数据或注册付费账户。

## 复现准备判定

数据价值：真人行为、重复轮次、空间网络及信息处理对照，适合未来E2的网络模仿/群体动态检验。下一步应在免费可访问条件下读取README和CSV，核验 `session×participant×round` 唯一性、邻居拓扑、两种处理、缺失、时间排序及原始许可；以会话为主要依赖簇开展留出/重采样，避免泄漏。

R073冻结双人100轮直接迁移资格：NO。原因是本研究每场50轮、每人同时面对四邻居，实验结构与R073双人长轮次不同。不可修改R073模型或评分规则来追求兼容。新增正式真人E2预测=0，历史E3=0。

本轮状态：PRIMARY_PAPER_AND_DRYAD_FILE_MANIFEST_VERIFIED；RAW_CSV_READ_BLOCKED_403；FIELDS_LICENSE_AND_REPLAY_PENDING。
