# R071 真人公共物品惩罚实验数据：来源可追溯但 E2 未达标

日期：2026-10-16。证据等级：**真实论文元数据核查＋一次实际来源获取失败，尚不是 E2 原始数据复验**。本报告所述 384/320 人等公开数字是作者/发布者报告，不是本项目运行真人数据复现。R071 合成 E1 成功不能让 E2 自动通过。

## A：Dryad 真正匹配主题的随机惩罚来源

[Smerlak, Salahshour & Oberhauser (2022), *The cost of noise: Stochastic punishment falls short of sustaining cooperation in social dilemma experiments*](https://doi.org/10.1371/journal.pone.0263028)；[官方 Dryad DOI 10.5061/dryad.n02v6wx03](https://doi.org/10.5061/dryad.n02v6wx03)。数据页列出 `noisy-PGG.csv`（约 1.30MB）和 `README-noisy-PGG.pdf`，论文/发布者说明 2021 年线上真人公共物品博弈 **384人、96个四人小组**完成；分析排除非应答后 **320人、80个四人小组**，control/low/medium/high噪音条件分别为21/20/20/19组。这些数字只是公开出版元数据；**该文件没有被 R071 的程序独立读取**。

[严格来源门协议](../../protocols/R071_E2_DRYAD_PGG_NOISE_SOURCE_APPLICABILITY_2026-10-16.md) 于首次访问原始 CSV 字节之前冻结，规定只读原件 SHA256、CSV 列头、行数和匿名字段类别，不允许输出个体记录或拟合。执行 [GitHub Actions run 38891213930](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38891213930)，**11项**合成 CSV 安全/泄露/列数测试成功，但官方文件链接访问产生 `HTTPError`，真实来源作业 **FAIL**。结果为 `SOURCE_UNRESOLVED`，原件 SHA256、字节总数、真实列头、实际人/组数均 `UNKNOWN`，不能使用发布页面数字替代。匿名失败凭据 [R071_E2_DRYAD_SOURCE_ATTEMPT_RESULTS.json](R071_E2_DRYAD_SOURCE_ATTEMPT_RESULTS.json)，短期 CI 匿名工件 `12041492420`，源 SHA 未建立；未从任何其他镜像悄然切换以制造成功。

这个候选**即使未来可以合法下载**，也无法直接作为当前 R071 五人、二元贡献、固定 P 角色与确定性罚款制度的逐人校准：作者实验为**四人**、随机处罚噪音处理，需恢复完整实验成本合约、身份编码与处罚对象、个人连续贡献、前日信念代理才可修订模型与预注册对照。

## B：已证真实原始来源仍不满足当前模型

旧 [R067/R047 的公共资源数据适用性正式报告](../R067/R067_E2_R047_APPLICABILITY_RESULTS.json) 固定作者仓库 `lrdegeest/InequalityCPR` 的提交 `1142b0915a0a46e72264358378b3535948f6b2b4`，原数据 Git blob `73c02176bc9e060af987149594a85f9f7b591230`。该数据是 32 个**四人小组**、128 名被试的公共池资源**多水平提取**实验，而不是 R071 的 5 人、每人只能做0/1贡献、独立明确执行制裁人 P 的相同实验。虽已通过旧项目“原始数据来源真伪”验证，但**从未被 R071 再用一次二元映射重算或合法校准**，因此应保留 `BLOCKED_MODEL_MISMATCH`。

## C：其它公开目录，只建立候选清单而不伪称已读取

- [Dryad：Herrmann、Thöni 与 Gächter《Antisocial punishment across societies》](https://doi.org/10.5061/dryad.87301) 在官方元数据描述有 **16 个样本来源群体**、反社会惩罚、公开 ZIP 数据及分析代码，相关原始论文 DOI `10.1126/science.1153808`。本轮没有读取 ZIP，也不把不同样本来源与 R071 纯规范参数设为直接一一对应。
- [Zenodo：Burton-Chellew、El Mouden、West《Conditional cooperation and confusion in public-goods experiments》](https://zenodo.org/records/4947771) 提供约66 KB 的 xlsx 数据，特别强调**表面条件合作可能与误解收益规则混杂**，适合作为将来判断 N 的规范动机时的竞争解释；**本轮没有读取/解析 xlsx**，也没有证明个体的规范心理。

## D：未来严格 E2 门

优先恢复至少一个合法来源的原始字节 hash+权限：每条真实贡献/处罚的单位、支付方式、组人数、制度对照、处罚对象/执行成本、策略与信念/预期（如果观察不到，应主动标为不可识别）。冻结与真实任务相容的新模型、机构/小组级留出、竞争基线与预测损失。若无法测量“条件规范”和对“被处罚的反事实预期”，仅估计贡献率关联不能检验本研究 N 的两个认知条件，更不能仅凭惩罚有效推论规范传承机制。

`R071_E1_SYNTHETIC=PASS`；
`R071_E2_DRYAD_SOURCE_BYTES=NOT_RECOVERED`；
`R071_E2_R047_DIRECT_EQUIVALENCE=BLOCKED_MODEL_MISMATCH`；
`R071_REAL_PUNISHMENT_AND_NORM_MECHANISM=NOT_ESTABLISHED`；
`R071_E3=OPEN`；
`PESEN_v0.1=FROZEN`。
