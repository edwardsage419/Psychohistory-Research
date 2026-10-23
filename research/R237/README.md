# R237 主题模型（10-011）：九有限collapsed LDA世界、1944完整主题—词序列来源

日期2026-10-23。原始239目录 `10-011 Topic Models` P2。科学状态 `CLOSED_BOUNDED_E1_FINITE_ARTIFICIAL_COLLAPSED_LDA_IDENTIFICATION`。

[事前冻结协议](../../protocols/R237_TOPIC_MODELS_9_COLLAPSED_LDA_WORLDS_1944_ORIGINAL_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [完整科学报告](R237_SCIENTIFIC_REPORT_2026-10-23.md) · [1944完整原人工topic-word来源](R237_ALL_1944_ORIGINAL_LATENT_TOPIC_WORD_ATOMS.csv) · [原生Fraction计算源码](r237_exact_collapsed_lda.py) · [9世界联合词分布/共现/潜在后验](R237_EXACT_RESULTS.json) · [SHA256机读原档凭证](R237_FINAL_MACHINE_ACCEPTANCE.json) · [正式科学验收](R237_FINAL_ACCEPTANCE_STATUS.json)。

主要结果：BASE与交换两个主题标签的LABEL_SWAP_ALIAS具有完全相同全部27个可见三词有序文档概率，但真正隐藏主题编号被互换；当两主题词分布完全重复，Dirichlet先验从(1,1)改为(3,1)也不改变任何可观察文档概率，却改变隐主题归属概率。BASE、ALPHA_CONCENTRATED、ALPHA_SPARSE的词0边际都1/3，同文档内两个词0指示协方差分别1/108、1/324、1/54，说明仅词频不足以恢复文档内依赖。核验每个原源theta collapsed法、独立Pólya urn法、解析Dirichlet协方差和全完整观察分布。

[GitHub Actions run39885530463](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39885530463)三个job success，Python3.11和3.12各96真实单测，共192次通过。完整1944原来源及精确计算结果机器人永久归档[a718dd9c](https://github.com/edwardsage419/Psychohistory-Research/commit/a718dd9cfb82b461f9e77f73524c264327451ed0)。

全部为三词、两主题的人工E1，不曾拟合真实历史文档主题、文本含义或样本外语言概率，新增真人E2=0、历史E3=0。R073与PESEN v0.1冻结。下一真实239目录 `10-012 Historical Text Embeddings`（R238）。研究顺序继续原R全部完成后统一归纳分类，最后熔炼。
