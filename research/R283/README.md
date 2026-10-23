# R283 人工三研究系统汇总方法（12-013，P1）

**CLOSED_BOUNDED_E1**：完整模拟研究登记册S1/S2/S3，三世界各64个完整六bit原source，合计192个全人工来源；不是从真实已发表论文搜集数据的系统综述或元分析。理论依据PRISMA 2020报告透明度及Higgins et al. 2003异质性研究。

[事前冻结协议](../../protocols/R283_THREE_STUDY_FIXED_EFFECT_SYNTHESIS_192_COMPLETE_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [可执行标准库程序](r283_exact_meta.py) · [全部192原研究source CSV](R283_ALL_192_ORIGINAL_THREE_STUDY_META_SOURCES.csv) · [三个情境精确分析JSON](R283_EXACT_META_RESULTS.json) · [SHA256凭证](R283_MACHINE_RECEIPT.json) · [科学报告](R283_SCIENTIFIC_REPORT_2026-10-23.md) · [机器正式验收](R283_FINAL_ACCEPTANCE_STATUS.json)。

真同质世界全纳入加权效应1/2、E[Q]=2，但只报告最有利研究的期望效应469/512；异质性正负抵消世界，全纳入真加权效应0，而事后最大研究的期望效应175/256。权重需要不可真实观测的人工真方差，故不是实际论文统计量。

首次[失败CI run39906498127](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39906498127)第三独立审计解包失误，保留记录；修正后[成功run39906571655](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39906571655)三job success，双Python3.11/3.12各99项真测试共198通过，全来源机器人永久归档[6b4f0e1a](https://github.com/edwardsage419/Psychohistory-Research/commit/6b4f0e1adb42484eaa55c5eebf08ee47f9421e13)。

科研只限人工E1，新增真人E2=0、历史E3=0，R073及PESEN v0.1继续冻结。下一原目录R284发表偏差。
