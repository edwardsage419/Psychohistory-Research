# R085 正式科学报告：不对称四人公共物品博弈的原作者二文件SHA/MD5与MAT资格审计

2026-10-17。限定结题：来源身份可以由官方MD5严格校验，但**实际MATLAB格式无法经SciPy结构解析**，因此R085真人原始行动 E2 **没有成立**。本项为原作者数据资格审计（E0发表来源、E1纯合成和真实原始文件完整性证据），不能称为真实贡献率科学结果。

## A01 研究对象与原作者完整材料

原作者 Wang, Xiaomin; Hilbe, Christian; Zhang, Boyu，2025年8月21日 Zenodo v2官方记录 [10.5281/zenodo.16918146](https://zenodo.org/records/16918146)，标题 *Dataset and computer code for The dynamics of cooperation in asymmetric public goods games*。原作者公开说明分两种四人公共品实验制度（线性与阈值），每种三种处理FE平等、AI优势对齐、MI优势错配，各20轮和两个session。作者陈述线性四人FE100、AI104、MI108名不同真人；阈值四人FE76、AI100、MI100名不同真人。注意同一个人可在两个session重新分组，且GlobalPlayerID在session间重新分配；上述人数与原始字段**未经本研究重新抽样验证**，仍是作者公开元数据。

限定源合同先于第一次真实字节：
[Phase A 原始数据身份/结构冻结](../../protocols/R085_AUTHOR_ASYMMETRIC_FOUR_PERSON_PGG_SOURCE_AND_SCHEMAS_FREEZE_2026-10-17.md)，commit `d0598f2cb360175c5d5b8d80dacba70f4d1c8a13`，指定官方Zenodo v2固定记录两个二进制文件名与作者网页MD5及scipy whosmat读取资格。任何R085真实行为评估只有在源字节及schema通过后才能冻结另行执行。

## A02 官方原始二进制身份

* `LinearPGG_4P_ExperimentalData.mat`，网页公开MD5 `42153952f8e6614d09c2d903fd97af62`；
* `ThresholdPGG_4P_ExperimentalData.mat`，网页公开MD5 `6036f73c2f758ab3aeed6dcf4f74585b`。

2026-10-17 GitHub Actions实际从两个官方固定Zenodo文件URL分别取回源文件：若源文件内容MD5与上列官方原始页面完全不符，程序会直接抛出`R085_ZENODO_AUTHOR_MD5_MISMATCH`、不执行读取器。现实两件在此阶段均越过MD5检查，到达MAT结构解析才失败。此事实**只证明发布方给定MD5一致下的原始内容身份**，并不能证明已能够按照原作者说明重构真实人/组/轮。

## A03 源结构读取失败与独立受控重试

第一次冻结之后，提交[MAT5原始读取脚本](r085_zenodo_original_four_person_mat_source_gate.py)、[24项合成来源检查](test_r085_zenodo_original_four_person_mat_source_gate.py)、[首次真实执行CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39002422986)。两个CI job均success，24项合成通过。两个真实文件均在MD5核验后经 scipy 1.14.1 `whosmat` 报出`R085_SCIPY_MAT_SCHEMA_OR_VERSION_UNSUPPORTED`；来源总门明确FAIL_CLOSED_NO_REAL_HUMAN_SCORE。**CI执行success是失败收据生成成功，不是科学数据读入成功。**

第一次真实失败之后，先冻结[Phase B格式辨识新协议](../../protocols/R085_PHASE_B_ORIGINAL_MAT_FORMAT_NONBEHAVIORAL_INSPECTION_FREEZE_2026-10-17.md)，commit `fe426cc63c0a2a5389877fc9e7a129e36c70219c`，不删除或更改原始Phase A代码、不调整源MD5，只允许检查MATLAB5/HDF5魔数、顶层key和变量shape，**不读真人结果矩阵**。再提交[Phase B程序](r085_phase_b_mat_real_source_type_only.py)与[10项新合成检查](test_r085_phase_b_original_mat_metadata_only.py)。[Phase B真来源工作流39002668337](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39002668337)合计34项合成全过，真实二源判别为MATLAB5头、仍然两个`R085_PUBLISHED_FILE_MAT5_WHOSMAT_FAILED`，失败源资格不动。

[Phase C来源身份安全失败收据独立重复运行](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39002819018)以同一真实源码、严格相同作者MD5与34项合成检查再次运行，并要求安全失败匿名收据与Phase B第一次来源收据**精确1123字节、SHA256 `282d3beb52b30ad938cf0e89247a2316a2c40d118a51712543a42c9fd6a3bae8`**完全一致才允许自动存永久Git： [来源失败匿名记录](R085_ORIGINAL_AUTHOR_TWO_MAT_VERIFIED_MD5_BUT_STRUCTURE_FAIL_SOURCE_RECEIPT.json)。记录仅含源文件名、发布方MD5、失败类、程序状态；源码对真实文件内容不输出数组元素、参与者或原始 .mat。

**R085实际读取人类行为数组0次；真实四人贡献指标0个；已重算实验人数0；独立外部E3 0次。** 不可以从纯合成和真实MD5核验推导出任何不对称处理会增减合作的现实结论。

## A04 负结果、科学边界及下一步

记录的两种原始文件均通过作者MD5，但以本项目冻结的标准scipy MAT5解析技术均失败；未获得真实源顶层变量name/shape，不具备后续估计分母基础。不能推断文件本身永久损坏、所有MATLAB解析器不能用、原作者数据不存在或真实实验数据错误。另一数据结构解析需要独立有限新研究，应记录本次方法未成功而非回填成功。

同一作者原Zenodo记录的两人博弈源Excel文件（线性与阈值）在其网页有单独公开MD5和明确按四行表达两人合作20轮及两个交替角色session的说明；若进一步研究，应**另立R086**在评分前独立冻结这两人样本和其Excel字段/角色映射及独立原文件MD5，不擅自当作本四人数据的修复。也可选GitHub其他独立作者数据。任何跨FE/AI/MI对比若处理分配和人组身份未独立证实不能声称资源不对称的因果效应。

## A01–A06 有界验收

A01限定对象及四人实验来源问题PASS；
A02官方二份原始MD5身份核验PASS，但可解释内部格式仍OPEN；
A03合成24+10、真实格式失败执行及独立重放PASS，**真实行为复算E2 = OPEN**；
A04所有真实失败/阴性永久保留PASS；
A05没有编造真实真人效应/因果/历史验证PASS；
A06协议、原源码、合成、真实失败收据、独立归档、正式报告与GitHub主分支索引在最终核验后PASS。

**限定项目档案状态 `CLOSED_BOUNDED`（仅数据资格审计），原始真人行为研究仍 `SOURCE_SCHEMA_BLOCKED`，不是实证科学E2验收；PESEN v0.1 `FROZEN`。**
