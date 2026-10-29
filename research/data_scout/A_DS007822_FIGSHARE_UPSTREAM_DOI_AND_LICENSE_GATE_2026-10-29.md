# A轨公开真人数据：ds007822 原始 Figshare DOI 与授权链补充核验

日期：2026-10-29 UTC。目标键：(A,OpenNeuro ds007822 v1.0.0,upstream Figshare DOI and redistribution license). 先前已完成33份事件文本、11个三人组、33人×40轮共1320条行为核验；本轮没有重复计算或新增真人预测。

## 新增来源身份

正式英文论文：Kim H, Jun SC, Nam CS (2026), *A reproducible EEG hyperscanning dataset for triadic social decision-making during an iterated 3-player Prisoner's Dilemma*, Data in Brief 68:113064, DOI 10.1016/j.dib.2026.113064，2026-07-10线上发表。PubMed PMID 42541318，https://pubmed.ncbi.nlm.nih.gov/42541318/ 。该论文的 Databank accessions 明确列出 Figshare 原始数据 DOI **10.6084/m9.figshare.32197038**。论文公开数据入口为 OpenNeuro DOI **10.18112/openneuro.ds007822.v1.0.0**。Figshare 题名为 *EEG and Hyperscanning, triadic Prisoner's dilemma game*，链接 https://figshare.com/articles/dataset/EEG_and_Hyperscanning_triadic_Prisoner_s_dilemma_game/32197038 。

GitHub 官方数据镜像 OpenNeuroDatasets/ds007822：
* README Git blob 4bbc8c259406e8a1cce00c6549cba41ff556f2c8 明确11个三人组、33人、事件 TSV。
* dataset_description.json Git blob c6d51a07c3a5b3821b8ffabea51a502ea99835e4，License 字段为 CC0。
* 根 LICENSE Git blob 7cf9928dd50e0b154c7e5d09f91f16674dff64fc，原文为 “License information was not provided with the source files.”

上述两项许可元数据相互矛盾。论文正文的 CC BY 是论文许可，不能直接作为 Figshare 上游原始数据、行为记录及EEG文件的再分发授权。Figshare 页面本轮访问返回HTTP 403；其 API 未能获取元数据，未验证 Figshare 记录文件清单、文件级许可、权利人或是否与OpenNeuro字节相同。**许可状态仍为 UNRESOLVED**。第三方目录将 Figshare license 记作 null，不构成官方授权确认。

## 行为和复现适用性

先前核验的行为单位为每人每轮一次选择，参与者键保留组号及组内身份槽；时间单位为40轮，独立分组为11个三人组。该实验是三人博弈，R073 冻结要求双人100轮独立场次及原评分规则，直接复验资格为 NO。若将来开展三人模型迁移，须先冻结新协议并以组为划分单位，防止同一三人组跨训练与测试造成信息泄漏。

本轮不重新分发原始数据，不使用未公开私人信息，不进行任何真人E2预测或历史E3预测。数据研究结果为 PRIMARY_PAPER_FIGSHARE_DOI_LINK_VERIFIED，LICENSE_CONFLICT_OPEN，RAW_FIGSHARE_UNREAD，R073_DIRECT_REPLAY_NO。后续仅在免费公开渠道验证 Figshare 官方许可和源文件关系；无法验证则继续阻塞。
