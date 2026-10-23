# R282 科学报告：ODD七要素与更新时序对模型复现的影响

日期：2026-10-23 Asia/Taipei。原239目录12-012 Open Reproducible Workflow and ODD，研究R282。结题限人工模拟E1。

## 理论来源、研究设计
Grimm et al. (2020), *The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism*, JASSS 23(2)7, DOI https://doi.org/10.18564/jasss.4259。Grimm et al. (2010), *The ODD protocol: A review and first update*, Ecological Modelling 221:2760–2768, DOI https://doi.org/10.1016/j.ecolmodel.2010.08.019。自建二智能体二元XOR模型，仅验证规范描述、执行可复现性和日程反例，不复现上述作者的任何经验模型。

[事前冻结协议](../../protocols/R282_ODD_SEVEN_ELEMENT_3_SCHEDULE_192_COMPLETE_SOURCE_PRESCORE_FREEZE_2026-10-23.md)，独立冻结提交[5447354b](https://github.com/edwardsage419/Psychohistory-Research/commit/5447354be84992df49810b59cd258405851d2eb9)。[完整七要素ODD2020模型说明](R282_ODD2020_SEVEN_ELEMENT_MODEL_DESCRIPTION.md)涵盖Purpose and patterns、Entities state variables and scales、Process overview and scheduling、Design concepts、Initialization、Input data、Submodels。每policy有相同64种完整六bit来源`a0,b0,eA0,eB0,eA1,eB1`，初始与四扰动分别公平独立，全来源权重1/64。三日程SYNC、A_THEN_B、B_THEN_A产生**192个带日程标签的来源类型**；64个source索引是完整枚举键，不是伪随机seed，也不是64次真实社会实验。

SYNC每期双方读取旧状态，A_THEN_B后者读取更新后的A，B_THEN_A后者读取更新后的B，更新规则均为读对方bit并XOR自己的扰动。每source记录完整t0/t1/t2双agent轨迹。来源穷举、独立闭式XOR代数、不导入主模拟源码的GitHub Actions第三job逐来源重算均严格一致。

|比较|精确来源数量|
|---|---:|
|每政策t2四种终态|每类16/64|
|SYNC与A_THEN_B的t1不同|32/64|
|SYNC与A_THEN_B的t2不同|48/64|
|SYNC与B_THEN_A的t1不同|32/64|
|SYNC与B_THEN_A的t2不同|48/64|
|A_THEN_B与B_THEN_A的t2不同|48/64|

因此，即使汇总最终状态概率完全一样，同来源反事实更新序列仍明显有别，必须报告准确activation schedule、输入stream、更新时间、顺序和原source映射。ODD机器门槛还验证七标准标题是否齐全，缺失或重复会被拒绝，但这不是外部标准机构对文档质量的认证。

[完整执行源码](r282_exact_odd_replay.py) · [192原source时序CSV](R282_ALL_192_ORIGINAL_ODD_SCHEDULE_SOURCES.csv) · [精确分析JSON](R282_EXACT_ODD_REPLAY_RESULTS.json) · [CSV/JSON/ODD全文SHA256机器凭证](R282_MACHINE_RECEIPT.json)。

[GitHub Actions run39906210132](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39906210132)三job全部completed/success。Python3.11与3.12各114实际unit tests，总228项通过；独立第三来源审核包括全部192行原source、两轮轨迹、文档七项与哈希，机器人永久归档[commit 0933b552](https://github.com/edwardsage419/Psychohistory-Research/commit/0933b552515950afb016fa647cf1c16d0d7c89fc)。

原CSV SHA256 `5242816a6f0fdbe099b77bf68e8828b7c0da8a91027aa16d1cf13d8c8fd30bed`；结果JSON SHA256 `488ab3f0ac5fa6de5c5d2bcea750b98c51deb4ca585e0a1541368325270d5fa9`；ODD全文SHA256 `32e1b5757f29dc66b22573c92bf46b7c0ad2b46bc1cdb01eb609309b11fb2890`。

没有新增真实人类E2或历史E3证据，R073与PESEN v0.1仍冻结。下一原239目录12-013 Systematic Review and Meta Analysis（拟R283），后续R系列完成后统一归纳分类，最后模型熔炼。
