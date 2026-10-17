# R097：2017 Mao 等人长期重复囚徒困境独立来源筛选（E0来源访问阻断）

2026-10-17。**R097当前实验候选 = `SOURCE_ACCESS_BLOCKED_BOUNDED`，本次完成来源筛选和失败证据归档，不是新的真人预测模型E2/正式科研结题。** 论文作者 Andrew Mao、Lili Dworkin、Siddharth Suri、Duncan J. Watts，[*Resilient cooperators stabilize long-run cooperation in the finitely repeated Prisoner's Dilemma*](https://doi.org/10.1038/ncomms13800)，*Nature Communications* 8:13800 (2017)，原论文报告94名受试者20个工作日、每日20次十轮重复双人博弈，数据官方位于[OSF 64z8u](https://osf.io/64z8u/)，[原实验软件GitHub](https://github.com/TurkServer/long-run-cooperation)。

**独立性和数据资格**：真实原研究团队与R096不同，但**相同被试跨多日重复参与**，20日≠20个独立新招募参与者样本，400局也≠400独立实验室群体。在可计算的原始逐人日×局×轮×对手记录被实际核验之前，不能冻结真实场次留出训练集、行动编码或推断历史学习机制。

[最先冻结的Phase A来源资格协议](../../protocols/R097_MAO_DWORKIN_SURI_WATTS_2017_LONG_RUN_20_DAYS_ORIGINAL_OSF_SOURCE_ACCESS_GATE_2026-10-17.md) → [23项OSF来源主机、节点、隐私纯synthetic全PASS且实际两项官方目录访问503的CI39024639047](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39024639047)：`https://api.osf.io/v2/nodes/64z8u/` **HTTP503**；`https://api.osf.io/v2/nodes/64z8u/files/osfstorage/?page%5Bsize%5D=100` **HTTP503**。所以 **原实验确切行为数据源未获取**，SHA/MD5身份/真实人轮、真合作二元次序、实对手、跨日独立性均未建立；真实M0/M1/M2模型计分**0**，不是负面实验预测结果。

[正式科学边界/原始访问失败审计](R097_INDEPENDENT_2017_MAO_LONG_RUN_PD_OSF_E0_SOURCE_ACCESS_NEGATIVE_SCIENTIFIC_REPORT_2026-10-17.md) · [机读来源不可用证据JSON](R097_MAO_2017_94_HUMANS_20DAY_OSF_ORIGINAL_SOURCE_ACCESS_E0_RECEIPT_2026-10-17.json) · [可复查OSF来源权限验证源码](r097_mao_2017_long_run_osf_original_20day_metadata_access_gate.py) · [23项纯合成安全测试](test_r097_mao_2017_long_run_osf_original_20day_metadata_access_gate.py)。不上传原始行为数据、不编造样本数字或来源哈希。实验代码Git树已核验存在，但它不是人类微观数据证据。

**已成立的R095八场次全部M1阴性、R096十二场次FP固定伙伴正/随机伙伴正负混合依旧有效**；R097的来源访问失败不会改变它们。下一阶段R098继续寻找真正可下载原数据、拥有独立session与对手历史的不同实验团队，按源认证→源身份审核→模型先冻结→源真人实跑→完整重新下载复算的科研链推进。PESEN v0.1 保持FROZEN。
