# R088：171个真实六人多层级公共品群体的20轮合作锐界（正式E2）

日期2026-10-17。**R088=CLOSED_BOUNDED，限定真实原作者E2已通过、A01至A06全部限定PASS、PESEN v0.1保持FROZEN。**

来源 Pilgrim, Stewart & Raihani (2025-online / 2026-volume), *Social identity and cooperation co-evolve in a multilevel public goods game*, *Scientific Reports* 16:1610, [DOI 10.1038/s41598-025-30979-2](https://doi.org/10.1038/s41598-025-30979-2)。原作者 [chasmani/PUBLIC_social_identity_and_cooperation](https://github.com/chasmani/PUBLIC_social_identity_and_cooperation) 固定commit `8ce2c0cac4784485232aa96295f48ff147290b05`。该仓库经作者既定排除规则形成的6人完整组 `analysis/data/data_full_groups.csv` **2,270,643字节**、Git blob `f902865203bdb465a505869b593eca432831b2fa`，原作者两份源R分析排除/合作脚本均做了原始blob字节核验。数据包含171完整六人组×20轮，3条件每种57组，各组有两个三人子组，1,026原受试者对应20,520人轮应有行动。

科学过程严格保留失败：
1. [评分前Phase A协议](../../protocols/R088_SIX_PERSON_MULTILEVEL_PUBLIC_GOODS_171_GROUP_ORIGINAL_SOURCE_E2_FREEZE_2026-10-17.md)，commit `1f84bf430e4bb3c4aff8bf25eb90ba54e008df24`。 [首次CI39011042473](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39011042473)：35synthetic PASS、真实来源**失败**，因实际行动有缺失而不能按“每人全20轮必有回应”计分。
2. [新增受限Phase B源字段诊断协议](../../protocols/R088_PHASE_B_ORIGINAL_ACTION_FIELD_DIAGNOSTIC_FREEZE_2026-10-17.md)，commit `93008fb66516af9930c5a79d4a162fa744fa0a5b`。[来源实跑CI39011243425](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39011243425) 52synthetic PASS，发现**20,456份真实明确行动，64空行动**，按条件为GlobalOnly19、Balanced26、GlobalBoost19，其中第一轮29空、最后一轮0空，不擅自删除群组或当作self。
3. [新Phase C缺失锐界评分前冻结](../../protocols/R088_PHASE_C_ORIGINAL171_MISSING_ACTION_SHARP_INTERVAL_SOURCE_FREEZE_2026-10-17.md) commit `b8f819e806a5dc39c10f5c0de13c9f613145dae3`。[首轮真实171组极值计分CI39011509370](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39011509370)，81项synthetic PASS，并验证完整3件原作者源blob；[第二次完整原始数据独立取回、81synthetic重跑、匿名精确结果归档CI39011582787](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39011582787)成功，两份原始安全结果**各自逐字节与前次SHA完全一致**，永久存档。

**E2真实原作者全球投资/全球达标比例锐界（非置信区间）**：

| 57组/条件 | 六人全球投资率 | 四人及以上全球达标group-round比率 | 第一轮→第20轮全球投资率变化 |
|---|---|---|---|
| GlobalOnly | 67.9532%—68.2310% | 71.3158%—71.5789% | −27.1930至−24.8538百分点 |
| Balanced | 44.6199%—45.0000% | 42.9825%—43.5088% | −26.6082至−24.2690百分点 |
| GlobalBoost | 60.6287%—60.9064% | 64.3860%—64.5614% | −21.0526至−17.2515百分点 |

任意合法补全64个真实缺失行动，GlobalOnly-Balanced依然 **+22.9532至+23.6111百分点**，GlobalBoost-Balanced仍 **+15.6287至+16.2865**，GlobalBoost-GlobalOnly **−7.6023至−7.0468**。与此同时各条件组内初末变化必为负，完整组六人样本中GlobalOnly至少41组、Balanced至少37组、GlobalBoost至少35组保证衰退，仍分别有至少1/11/9组保证上升；不将含缺失的不确定群组当成稳定不变。

[完整正式科研报告](R088_ORIGINAL_171_MULTILEVEL_PUBLIC_GOODS_GLOBAL_SHARP_E2_SCIENTIFIC_REPORT_2026-10-17.md) · [匿名全部3420组轮三条件群体上下界E2正式JSON](R088_ORIGINAL171_GLOBAL_COOPERATION_64_MISSING_SHARP_BOUNDS_E2_RESULTS.json) **65,424字节**、SHA256 `2b0f76fa8f7d1a42d2f91508c4acf52c0a7c0fc9523801ec1d9759559d8fb67e`、Git blob `1b97419451e6124d7d7449bdb87f743905f43789` · [真实空值源诊断收据](R088_ORIGINAL20520_ACTION_LABEL_MISSINGNESS_E1_SOURCE_RECEIPT.json) **2144字节** SHA256 `b52f6313f40beecdb761c5bb9b6013b318700c2e1c2f8f4d0a7682efee5edf18` · [A01-A06机读验收](R088_FINAL_ACCEPTANCE_STATUS.json) · [Phase C可执行源码](r088_phase_c_original171_missing_sharp_bounds_E2.py)、[全部81项分三阶段合成tests](test_r088_phase_c_original171_missing_sharp_bounds_E2.py)。

**科研证据界限：**从作者已筛选的完整组六人样本回顾性计算，在不确定64个具体行动下上述全球合作比例次序是缺失稳健的；不包含原作者招募后排除人员，不具备所有招募者一般化或独立再抽样置信区间；尚未在同一实验验证社会身份心理因果/局部公共品达标/制度政策因果；既有作者首次发表的结论不能作为本项目新E3，更不能推到历史社会演化。R088有界结题，不在此171组上无限修改模型。PESEN v0.1继续冻结。
