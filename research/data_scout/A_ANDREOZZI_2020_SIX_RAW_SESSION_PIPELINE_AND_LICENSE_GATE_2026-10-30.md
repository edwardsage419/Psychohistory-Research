# A轨：Andreozzi 2020 六场原始会话到 CSV 的公开复现链审计

日期：2026-10-30 UTC。来源：seyhunsaral/stabilitycondcoop 英文公开仓库，论文 Scientific Reports (2020), DOI 10.1038/s41598-020-70681-z。实际读取 README.md Git blob 3292568ac99ec45c22ebcf009fa929028e07608a、LICENSE blob a7d26c9987564e97e270547d50707d7093ada753、code/process_raw_data.R blob 522efd459f574ccaef3d9ce1dd2b086ffb70370e；实际读取 data/rawdata 和 data/csv 的 GitHub 文件目录元数据。

六个原始实验会话 XLS 文件均在仓库公开，按目录记录：
* 170516_1052.xls，528062字节，blob 904c6aae4；
* 170516_1335.xls，525700字节，blob 1f2b7b71c；
* 170518_1001.xls，536711字节，blob 8bfc8749c；
* 170518_1343.xls，487756字节，blob 16dc7c947；
* 171120_1317.xls，571055字节，blob e9f200cb5；
* 171120_1546.xls，571055字节，blob 025eb3080。

以上大小和 blob 为目录只读结果，未解析 XLS 原始字节；末两文件大小应以远端目录为准，若需精确复算须再逐一核验。公开清洗结果包括 subjects.csv（blob bd4c1550002621bee7dfb50e0d15d317764d1ea9）、quest.csv 和 decbehav.csv。

作者处理程序通过 zTree::zTreeTables 读取 globals、subjects、DECBEHAV 三张表。处理时对每个会话从 globals 第2行的 Treatment.1 提取处理标签，按文件遍历序号赋 Session。筛除原始 Period<5 的四个练习期，再将 period 减4，构造 treatment/session/subject 复合身份，按主体计算滞后字段，写出 CSV 和 RDS。

新增复现门：原始 XLS 读取、zTree 包及旧 tidyverse 版本兼容、globals 第2行 Treatment.1 的存在与值、文件排序与 Session 分配，以及原始到清洗 CSV 的字节或行级重建均需要实际运行后才能 PASS。滞后字段使用 order_by=subject_unq，组内常量，实际时间排序依赖上游行顺序。此前记录的 813/1206 个 wide_o 历史字段错位保持开放；静态代码检查无法断言论文主结果失效。

许可：作者 README 明确 data/ 使用 CC BY 4.0，code/ 和 ztree/ 使用 MIT；本轮只引用公开来源及元数据，没有重新分发第三方原始记录。单位：六个实验会话，参与者和逐轮配对需依赖此前已经审计的 subjects.csv，六场会话不可视为1340个独立样本。数据可获得性：仓库目录可访问，二进制原始解析 NOT_RUN。R073 100轮独立双人实验资格：NO。新增 E2 预测=0。

状态：PARTIAL，已确认六场原始来源清单与清洗代码的输入输出链，尚未执行完整原始数据重建。下一步在可用开源 R/zTree 环境下复算原始表及比较清洗输出，避免新费用。
