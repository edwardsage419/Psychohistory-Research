# R275 等效机制分析（原239目录12-005，P0）

状态 **CLOSED_BOUNDED_E1_EQUIFINAL_PAIR_OBSERVATION_DISCRIMINATION**。三个机制IID_PAIR、COPY_PAIR、FLIP_PAIR都使四个A边缘序列完全公平且联合分布相同；仅观测A时等先验MAP平均正确率1/3。观察完整(A,B)成对关系时可识别同频率背后的不同机制，四pair有限样本的等先验MAP平均正确率**23/24**，IID真机制仍有1/8的错分概率。共三机制×256原pair源=768个完整人工原source配置（包含0质量占位行），正概率行288。

[冻结协议](../../protocols/R275_EQUIFINALITY_3_MECHANISMS_768_COMPLETE_PAIR_SOURCE_TYPES_PRESCORE_FREEZE_2026-10-23.md) · [标准库源码](r275_exact_equifinality.py) · [完整768原来源CSV](R275_ALL_768_ORIGINAL_EQUIFINALITY_PAIR_SOURCES.csv) · [原理论解析和来源风险结果JSON](R275_EXACT_EQUIFINALITY_RESULTS.json) · [SHA256机器来源凭证](R275_MACHINE_RECEIPT.json) · [正式科学报告](R275_SCIENTIFIC_REPORT_2026-10-23.md) · [机器正式有界验收](R275_FINAL_ACCEPTANCE_STATUS.json)。

[GitHub Actions run39903913659](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39903913659)：Python3.11、3.12各50真unittest全部通过共100项，第三独立源CSV逐source重建核对完成，三job completed/success，全部CSV/JSON/SHA机器永久归档main [commitd70cb4e5](https://github.com/edwardsage419/Psychohistory-Research/commit/d70cb4e542b47d3efe10c551a863408a2c31081e)。

科研证据仅E1人工数学，新增真人E2=0，历史E3=0，R073/PESEN v0.1仍冻结；下一原目录12-006 Model Identifiability（R276），继续按原R学习目录推进。
