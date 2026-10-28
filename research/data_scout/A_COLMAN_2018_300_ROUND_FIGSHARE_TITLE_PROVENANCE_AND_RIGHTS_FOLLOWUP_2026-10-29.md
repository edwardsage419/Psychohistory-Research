# A轨 Colman等2018年300轮真人重复囚徒困境：论文与数据登记标题一致性追踪

日期：2026-10-29。性质：既有候选来源的新增元数据交叉核验。原有A轨 `COLMAN_PULFORD_KROCKOW_2018_300_ROUND_PD_FIGSHARE_PRIMARY_METADATA_AND_LICENSE_GATE_2026-10-27.md` 和 `COLMAN_2018_FIGSHARE_ZIP_ENDPOINT_LICENSE_FOLLOWUP_2026-10-27.md` 保留，不重复声称新实验或新原始数据。

## 本轮实读英文一手来源
1. University of Leicester Figshare: https://figshare.le.ac.uk/articles/dataset/Repeated_Prisoner_s_Dilemma_Dataset/10194938 。数据登记发布于2017-09-14，作者A. M. Colman、Briony D. Pulford、E. M. Krockow，下载总大小185.25 KB，Licence字段明确为All Rights Reserved。数据说明将关联论文题目写作 `Persistent Cooperation and Gender Differences in the Prisoner’s Dilemma: A Conceptual Replication`。
2. PubMed PMID 29727770: https://pubmed.ncbi.nlm.nih.gov/29727770/ 。正式论文发表于2018年，题目 `Persistent cooperation and gender differences in repeated Prisoner's Dilemma games: Some things never change`，DOI 10.1016/j.actpsy.2018.04.014，作者三人相同，摘要明确300轮不间断真人双人重复博弈。

## 新增来源风险与核验结论
本轮明确记录数据页说明的论文题目与正式发表题目**文字不一致**。作者相同、研究主题和时间顺序相容，数据页仍可能指向同一研究的预发表标题；但Figshare可见页面没有直接显示正式论文DOI，当前缺少数据文件内部的正式论文映射字段。身份关系标记 `PROBABLE_SAME_STUDY_BUT_DOI_LINK_UNVERIFIED`，避免以标题近似替代数据版本证明。

原Figshare公开入口只列出185.25 KB的ZIP总下载量，未能实读二进制内部文件名、字段、参与者/配对ID、独立场次、轮次完整性、缺失值及文件哈希。300轮来自正式论文摘要，不等于已经取得300轮逐行数据。文件层级All Rights Reserved未授予再分发权，不把真人原始数据复制到本仓库。无私人数据访问，无账户注册，无购买。

## R073独立复验硬门槛
原R073冻结协议使用Montero 2022的FP6/SP6共12独立场次、100轮和特定留出评分规则。Colman实验300轮，缺少可验证的场次身份及同口径处理结构。禁止在查看结果后选择100轮窗口、改变七模型、平滑参数或训练折以声称R073原协议直接复验。

`SOURCE_METADATA_CROSSCHECKED; DATA_PAPER_TITLE_DISCREPANCY_OPEN; RAW_UNREAD; LICENSE_RESTRICTED; DIRECT_R073_REPLAY_NO`。

下一步需要合法取得ZIP字节和README，核对实际字段、正式论文DOI映射及许可范围，再决定是否在新的事前冻结协议下开展单独标注的E2预测。新增E2=0，E3=0，外部独立复现=0。新增费用0。