# R271 预注册与注册报告的选择性分析方法学（12-001，P0）

科研状态：**CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_PREREGISTRATION_FAMILYWISE_SELECTION**。冻结alpha=1/8与独立公平二元H0、每候选四bit单侧Binomial检验、家族检验数m=1/2/3、三个报告规则。九人工world全source共**13104种policy标签配置**，原始互异bit配置共4368种，不是真实研究样本。

[预先冻结协议](../../protocols/R271_PREREGISTRATION_9_DECISION_WORLDS_13104_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [完整标准库源程序](r271_exact_preregistration_familywise.py) · [13104完整原数据源与选择结果CSV](R271_ALL_13104_ORIGINAL_NULL_POLICY_SOURCE_TYPES.csv) · [完整九world拒绝概率JSON](R271_EXACT_NULL_REPORTING_RESULTS.json) · [SHA256机器证据](R271_MACHINE_RECEIPT.json) · [正式科学报告](R271_SCIENTIFIC_REPORT_2026-10-23.md) · [正式有界验收](R271_FINAL_ACCEPTANCE_STATUS.json)。

固定第一个检验的H0下阳性报告概率1/16；未校正m=3事后择优的家族报告概率721/4096≈17.6%，大于alpha=1/8；三检验Bonferroni校正因离散raw p最小1/16大于1/24而全部不拒绝。结论只适用于冻结的数学模型，**未实施任何真实研究预注册、注册报告同行审阅或人类E2实验**。

[最终GitHub Actions run39902734610](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39902734610)：Python3.11/3.12分别82项真unittest全部通过共164，第三完整来源审计成功，三job completed/success。原CSV、结果JSON及SHA全部永久归档[3d99415b](https://github.com/edwardsage419/Psychohistory-Research/commit/3d99415bfe7da4449462c42da8d8ecafb83a9d88)。

新增真人E2及真实历史E3都为0，R073/PESEN v0.1冻结。下一原目录12-002 Out of Sample Prediction（P0，拟R272）；全部原R模型完成后再分类与熔炼。
