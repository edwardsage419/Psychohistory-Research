# R105 Phase A：2024独立真实在线公共资源困境原CSV首源完整MD5与表头（先冻）

日期 2026-10-18。状态：FROZEN_BEFORE_AUTHENTICATED_FILE_SOURCE_OR_BEHAVIOR. PESEN v0.1 FROZEN.

## 项目全库来源查重

本项研究在建项前逐字节检查既有主要来源 R047 InequalityCPR、R095 Chapman Friend/Foe、R096 Montero-Porras 2022 fixed/random dyadic PD、R099 Liu 2024 PLOS S1 Data、R100/R098 Wang 2025 16918146、R101 Stallen 2023 DataverseNL、R102 Antonioni 2025 Zenodo 17610157、R103 Poncela-Casasnovas 2016 Zenodo 1127154及R104对R099的重复勘误。选定的新出版源 DOI **10.5281/zenodo.10818840** 与已有这些数据归档的DOI不同；论文实验、招募渠道和实验任务也与R096论文/数据不同。作者Eladio Montero-Porras与R096有重合，必须注明：**是新实验，不是完全无共同作者的新团队**。另有[较早Zenodo版本10228658](https://zenodo.org/records/10228658)描述类似数据：同一科学实验的版本，禁止把不同Zenodo版本误作不同真人复制。

## 只允许的官方原数据及已出版事实

Eladio Montero-Porras等，*Defaults: a double-edged sword in governing common resources*，正式[Zenodo原研究材料 10818840](https://zenodo.org/records/10818840)，真实在线Prolific四人共同资源困境（CPR），10轮；处理Control（出版描述n=100）、Pro-social（n=156）、Self-serving（n=156）；出版方说明完整参与者均属于完成10轮且所在原组无中途退出者。作者2024年3月14日归档，原始长表**`data_long_format.csv`**，Zenodo公开文件摘要 **MD5 `a3afbb4e52179a0e1d8b1b533f076cc9`**，标注文件约1.1MB。每人10行；档案介绍可能包含个人的逐回合提取、组总提取、处理组别等，但真正头字段未由本项目独立核验。不得把“412人/103组×10轮”当作真实来源已确认，也不得假设有不同实验室session标记；从已发布设计看属于线上同实验多个组，分组留出和人历史资格需要后续冻结的真实原字段审核。并不适用将逐组样本当作互相独立招募实验。

## 来源A冻结验收

仅GET固定首源`https://zenodo.org/records/10818840/files/data_long_format.csv?download=1`；严格HTTPS `zenodo.org` 域、精确路径与唯一 `download=1` 查询，重定向也必须满足同一来源。最大原文件2MiB，原出版方MD5必须与`a3afbb4e52179a0e1d8b1b533f076cc9` **整个原字节**一致，原文件SHA256由本项目另算并保留；严禁MD5不吻合时接受体量/表头或猜镜像。仅用应用CSV reader读取源**首个header行**，列数限定3..150、每列唯一可打印UTF8，若出现不可安全公开的列名则记录固定异常、不输出；物理行数用换行计数支持缺最后LF，**不解析原任何参与者ID、组号、轮号、数额、默选值、SVO或人口信息**。输出作者DOI、官方全MD5匹配、文件字节数、项目SHA256、来源真实列数、匿名物理数据行数、零行为和零模型结果。首次真实读取前必须先通过合成 URL、MD5、UTF8 header、无末换行、双重列名、无个体泄露测试。

CI独立归档`research/R105/R105_PHASE_A_LIVE_CI_FIRSTPARTY_2024_CPR_LONG_CSV_MD5_HEADER_RECEIPT.json`，包括真实负结果。A成功只代表原始文件E1，不能推出原人/组身份资格、同伴独立增益、任何因果或新E2。后续B非行为键核验成功后，**先冻结同等历史权重收缩基线和破坏组间配对的负对照**再读原提取额；不使用当前轮其他人投入作为未来特征。PESEN v0.1 FROZEN。
