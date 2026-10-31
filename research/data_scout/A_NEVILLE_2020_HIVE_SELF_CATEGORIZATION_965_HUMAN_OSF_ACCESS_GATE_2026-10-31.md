# A 数据侦察：Neville et al. 2020 The Hive 社会分类与行为模仿

日期 2026-10-31 UTC。轨 A。状态 **PUBLISHED_DESIGN_VERIFIED / RAW_DATA_BLOCKED**。未使用私人资料、未获取原始数据。

## 来源与可核验实验设计

原始论文：Neville, Drury, Reicher, Choudhury, Stott, Ball & Richardson (2020), *Self-categorization as a basis of behavioural mimicry: experiments in The Hive*, PLOS ONE 15(10) e0241227, [DOI](https://doi.org/10.1371/journal.pone.0241227), [PMC全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC7598449/)。

[University of St Andrews官方数据登记](https://research-portal.st-andrews.ac.uk/en/datasets/self-categorization-as-a-basis-of-behavioural-mimicry-experiments/)确认2020年 OSF 数据登记及公开查看入口：[OSF kjt4u](https://osf.io/kjt4u/?view_only=4a871bdea56a4f4e829c1bd651c5b97d)。论文数据可用性声明指向同一地址。

论文方法确认：英国科学博物馆六周招募共1139人，排除未满10岁及未完成者后分析965人。每次现场实验4至12人，组大小中位数7。随机分配红蓝类别，实验包含 Maze、Rather 和 Fidget 三种行为任务，观察人类对事先编程的群体色点运动的模仿。群体、会话、受试者及任务是不同层级；同场多人及同一人的多次动作存在相关性，不能把位置或动作当成独立受试者。原文实验时长约10分钟；不能由此推断每个数据文件的逐行时间单位。部分参与者年龄10至17岁，原始数据再使用须注意年龄及隐私保护。

## 本轮真实访问与复现准备门

1. 原始英文论文全文及大学数据登记已实读，论文使用CC BY许可。
2. OSF公开查看入口本轮访问返回HTTP 403。没有取得目录、文件名、CSV字段、受试者ID、会话ID、时间戳、原始位置序列、缺失编码、文件摘要或文件级许可证。
3. **数据许可待核**：论文CC BY不能自动外推为OSF所有文件可再分发。禁止上传原始受试者数据。
4. 未来若能合法取得公开文件，应先验证字段是否包含随机类别、任务、会话、匿名受试者、动作/位置及时间顺序，审查同场聚类、反复测量、缺失和年龄隐私。预先冻结按会话留出的E2检验及简单基线，避免同场或同一受试者泄漏。
5. 此实验与R305 S101项目自行规定的四对象MC分类分数没有一一对应的可观测参数。可以作为社会类别对模仿行为影响的独立实证候选，不能直接认定验证R305评分方程。
6. **R073排除**：该研究是多人群体模仿任务，含编程模拟点，不具备冻结的百轮真人双人重复博弈行动结构。R073模型与评分规则未修改。

数据状态：SOURCE_VERIFIED, DESIGN_VERIFIED, RAW_FILE_NOT_ACQUIRED, FIELD_SCHEMA_UNKNOWN, FILE_LICENSE_UNKNOWN, INDEPENDENT_SESSION_PAPER_ONLY, E2_NOT_RUN, R073_INELIGIBLE。无新增费用。
