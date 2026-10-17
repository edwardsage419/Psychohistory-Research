# R085：四人不对称公共品博弈原作者来源身份与MATLAB模式资格（有界结题）

日期2026-10-17。**行政研究结题 `CLOSED_BOUNDED`；真正四人贡献行为 E2=`BLOCKED / NOT_ESTABLISHED`；PESEN v0.1仍FROZEN。**

本阶段有意转向2025年原作者 [Wang、Hilbe、Zhang 官方Zenodo v2](https://zenodo.org/records/16918146) 双实验（四人线性、四人阈值公共品）。文献介绍三种平等/不对称配置FE/AI/MI，各20轮、两session且人群在session间重新分组；但这些人数与设计均为公开原作者描述，R085没有成功运行任何真实贡献率指标。

**数据来源成功和科研实证失败必须区分：** 已在新数据读取前冻结[Phase A原始文件与方法协议](../../protocols/R085_AUTHOR_ASYMMETRIC_FOUR_PERSON_PGG_SOURCE_AND_SCHEMAS_FREEZE_2026-10-17.md)，固定两件官方 `.mat` 文件及其出版方MD5；[原始真实CI run 39002422986](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39002422986)实取两件官方字节并逐一通过MD5源身份检查，纯合成24项通过，但 scipy.io.whosmat 原MAT结构读取失败，真实本人/组/轮字段不得推断。

失败以后，再先冻结[Phase B单独格式协议](../../protocols/R085_PHASE_B_ORIGINAL_MAT_FORMAT_NONBEHAVIORAL_INSPECTION_FREEZE_2026-10-17.md)；[第二来源实跑39002668337](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39002668337)合计34项synthetic全过，两件均属MATLAB5开头、但严格结构解析再度失败。既有初次失败与本次失败全部留档。 [第三次独立相同源重读并永久安全失败归档39002819018](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39002819018)也通过34项synthetic及逐字节检验，永久提交[匿名原作者MD5/真实MAT失败收据](R085_ORIGINAL_AUTHOR_TWO_MAT_VERIFIED_MD5_BUT_STRUCTURE_FAIL_SOURCE_RECEIPT.json)，**1123字节、SHA256 `282d3beb52b30ad938cf0e89247a2316a2c40d118a51712543a42c9fd6a3bae8`**。以上CI的success指失败被准确、安全、可重复地记录，绝非真人科学实证通过。

[完整A01–A06科学报告与适用范围](R085_ZENODO_ORIGINAL_FOUR_PERSON_PGG_AUTHOR_MD5_SCHEMA_SOURCE_GATE_REPORT_2026-10-17.md) · [机读正式验收](R085_FINAL_ACCEPTANCE_STATUS.json) · [Phase A原始来源脚本](r085_zenodo_original_four_person_mat_source_gate.py) · [Phase B格式重试脚本](r085_phase_b_mat_real_source_type_only.py) 与24+10项合成测试。原作者原始文件、个人贡献数组、身份及任何行都没有再发布至项目仓库；**真实参与者行读取0、真实合作变化评估0、因果效果未识别**。不能因此推论两件原始文件永久损坏或2025年研究不可靠。后续优先另立R086研究同一来源的两人Excel独立样本，或换其他原作者可解析数据，避免四人MAT资格门无限占用研究资源。
