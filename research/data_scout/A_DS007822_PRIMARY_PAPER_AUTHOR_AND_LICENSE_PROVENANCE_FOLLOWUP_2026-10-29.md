# A 轨：OpenNeuro ds007822 原始论文、作者和许可溯源补充

UTC 日期 2026-10-29。目标键：(A,ds007822,v1.0.0,原始论文及许可冲突)。在既有 A 轨 33 份决策事件 TSV / 1320 行核验基础上，仅核查新的外部来源及作者对应关系；不重复声称本轮又执行 1320 行逐行审计。

## 本轮实际读取的新增一手证据
1. PubMed PMID 42541318，2026-07-10 在线发表：Kim H、Jun SC、Nam CS，*A reproducible EEG hyperscanning dataset for triadic social decision-making during an iterated 3-player Prisoner's Dilemma*，Data in Brief 68:113064，DOI https://doi.org/10.1016/j.dib.2026.113064；https://pubmed.ncbi.nlm.nih.gov/42541318/ 。摘要明确 11 个三人组、33 人、每人 40 个决策轮次、逐轮合作/背叛行为标记，数据存放于 OpenNeuro。
2. 论文全文索引明确给出数据集 DOI https://doi.org/10.18112/openneuro.ds007822.v1.0.0 ，还指向 Figshare 原始数据 DOI https://doi.org/10.6084/m9.figshare.32197038 。Figshare 原始文件和其许可证未在本轮逐个读取，不据此判定所有上游文件可再分发。
3. GitHub 官方镜像 https://github.com/OpenNeuroDatasets/ds007822 ：本轮 GitHub 连接器实际读取固定 main 的 dataset_description.json blob c6d51a07c3a5b3821b8ffabea51a502ea99835e4，声明 Authors=["n/a"]、License="CC0"、数据 DOI 同上；LICENSE blob 7cf9928dd50e0b154c7e5d09f91f16674dff64fc 的原文指出来源文件未提供许可信息。README blob 4bbc8c259406e8a1cce00c6549cba41ff556f2c8 描述 11 三人组、33 人和三个 EEG 任务。
4. 论文全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC13427532/ 以 CC BY 发布论文正文。该许可适用于论文内容，不能自动替代 OpenNeuro 数据文件或 Figshare 原始记录的具体授权。

## 可复现性与证据门槛
本轮新增证据使数据来源与 2026 年 Kim/Jun/Nam 论文之间的对应关系达到 STRONG_PAPER_DATASET_DOI_MATCH；公开仓库 Authors=n/a 的元数据缺口可通过论文引文补充作者归属，但仓库元数据仍需由数据维护者正式修正。许可仍为 CONFLICT_OPEN：数据集元数据 CC0 与根 LICENSE 缺来源许可声明并存。未获清晰授权前，仅保存来源指针、字段摘要和审计，不重新分发原始 EEG、问卷或事件文件。

时间单位为每人 40 次三人同时互动，个体标识为组内匿名槽位。组层统计独立单位最多为 11 个三人组，33 人和 1320 次行为均不能充当 1320 个独立实验场次。原始实验方法已由论文补充，但逐轮时间戳、组内同步、条件分配和缺失机制尚需对原文件逐字段复核。R073 冻结双人 100 轮结构直接复验资格 NO；可在另立事前协议后作为 E2 三人行为研究候选。新增 E2 正式预测 0，E3 历史预测 0。

## 复现准备结果与后续
来源论文识别：PASS；研究者与出版日期：PASS；数据 DOI 对应：PASS；本轮原始文件重新获取与逐行核验：NOT_RUN（沿用此前归档的33文件审计）；文件级许可与上游再分发权：OPEN；独立三人组数量：11（论文声明与既有字段审计一致）；R073 直接资格：NO。下一步优先确认 Figshare 原始文件的发布者及授权声明，并向仓库维护者核对 License 字段；禁止自行修改第三方元数据或访问私人数据。
