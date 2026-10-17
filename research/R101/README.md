# R101：2023年另一独立团队的真人逐轮选择伙伴公共品实验原始来源筛选

2026-10-17。**当前 Phase A：真实第一手DataverseNL目录元数据审核运行中，原始行为源字节/人物与对手身份/独立场次均尚未证实，实际真人模型新得分0。PESEN v0.1=FROZEN。**

独立作者 Stallen、Snijder、Gross、Hilbert、De Dreu 的2023年[*Nature Communications*原论文](https://doi.org/10.1038/s41467-023-42128-2)报告336名真人、八人群体、每轮双人配对、由系统分配或选择伙伴条件。论文公开数据位置[OSF CASQZ](https://doi.org/10.17605/OSF.IO/CASQZ)，另一作者机构UvA报告正式同论文数据集[DataverseNL DOI 10.34894/EYFM5L](https://doi.org/10.34894/EYFM5L)。**这些是论文和机构公开索引的出处事实，不等于本项目已独立读取任一个原始真人行为文件。**

优先真正DataverseNL以避开R097另一OSF数据源原API503的重试损耗。[Phase A官方来源元数据冻结](../../protocols/R101_PHASE_A_STALLEN_2023_DATAVERSENL_OFFICIAL_METADATA_ONLY_GATE_FREEZE_2026-10-17.md)只允许精确官方 `dataverse.nl` DOI API的文件目录，不访问任何actor/partner/round值。[纯标准库官方目录审计](r101_stallen_2023_original_DataverseNL_official_metadata_only.py)、15项纯synthetic和[GitHub工作流](../../.github/workflows/r101-2023-Stallen-DataverseNL-author-metadata-source-only.yml)均已经上传GitHub；真实来源成功或失败必须另将匿名机读收据归档。若目录确实开放，先固定官方fileID/文件大小/MD5与精确路径，再逐步验证Source actor/opponent/round/session独立性。

研究目标：检验个人历史之外当前及过往对手行动是否对下一轮选择仍提供**新增、独立留出预测价值**。R100已正式E1身份不能重建限定结题，不能带入R101的训练样本；R095阴性、R096固定与换伴异质、R099四人组历史正向仍并列保留。R073及PESEN模型保持既有冻结，不能因新样本结果事后选参。
