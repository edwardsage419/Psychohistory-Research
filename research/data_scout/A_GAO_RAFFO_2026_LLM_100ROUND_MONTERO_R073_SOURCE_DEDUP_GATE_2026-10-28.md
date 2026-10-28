# A轨 2026年重复博弈论文真人基准来源去重与R073资格审计

日期：2026年10月28日。状态：PAPER_METADATA_AND_METHOD_VERIFIED；NEW_INDEPENDENT_HUMAN_DATA=NO；RAW_NEW_HUMAN_ROWS=0。

## 英文一手来源
Raina Gao与Tristan Raffo，2026年8月10日，*Modeling Human Behavior in the Prisoner's Dilemma with Large Language Models*，arXiv 2610.23860，https://arxiv.org/abs/2610.23860 。实际读取该公开论文摘要、方法3.1至3.3及结果4节。作者以五类语言模型代理模拟固定对手与轮换对手的100轮囚徒困境，和Montero-Porras等2022年真人实验比较。作者明确指出人类比较来自该2022年实验，模拟的100轮属于LLM代理输出。论文给出的真人合作率固定对手56.1%、轮换对手28.5%为引用基准，不能计为新采集的真人样本。

## 与项目已冻结真人来源交叉核验
项目 `research/data_scout/MONTERO_2022_R073_ORIGINAL_SOURCE_IDENTITY_HARD_EXCLUSION_2026-10-26.md` 已确认R073直接使用Montero-Porras等2022年12场、188名真人、100轮FP/SP原始实验，原作者论文DOI 10.1038/s41598-022-11654-2；公开Dryad入口 https://datadryad.org/dataset/doi:10.5061/dryad.37pvmcvmk 。2026年文章再次使用同一人类实验作对照，故无法构成R073第二独立真人实验。不能把模型代理模拟轨迹当作真人E2，也不能将引用人类合作率作为独立留出验证。

## 字段、身份、轮次、许可和获取
新论文的模型模拟单位是100轮LLM代理轨迹；真人基准来自既有Montero实验，原始人类身份、12场次、行为字段和许可应沿用原来源审核，不可另起新真人来源登记。本文未获取任何新真人逐行数据，未验证新模型模拟输出CSV字节、代理随机种子或复现实验环境，代码许可未核实。即使模拟结果可取得，证据类别仍属于模型模拟而非真实人类实验。

R073_DIRECT_NEW_EXTERNAL_E2=NO；R073_SOURCE_INDEPENDENCE=FAIL；A_REPLAY_READY_FOR_NEW_HUMAN=NO。仍需独立实验、双人逐轮行动、真实身份与场次、固定评分可迁移性及明确使用许可。没有访问非公开数据、购买服务或触发计费计算。
