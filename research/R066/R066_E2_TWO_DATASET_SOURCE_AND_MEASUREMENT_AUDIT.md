# R066：两套真实来源的测量完整性审计与经验研究关口

日期：2026-10-16。结论：**两个公开来源的文件完整性已由真实 GitHub Actions 验证；它们都尚不足以直接估计并比较三个经典意见动力学模型的社会影响参数。** R066 继续 ACTIVE，三模型经验预测结论保持 OPEN。

## 一、事先冻结并确实执行的检查

本轮运行前先提交了 [双来源审计协议](../../protocols/R066_E2_TWO_DATASET_MEASUREMENT_AUDIT_2026-10-16.md)，commit `4b8f1ada0568d66b8da54adb5605777803fde127`。运行代码 [r066_e2_measurement_source_audit.py](r066_e2_measurement_source_audit.py) 和 13 项 [合成反例测试](test_r066_e2_measurement_source_audit.py) 先独立提交。

[GitHub Actions run 38861027481](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38861027481) `completed/success`，两个作业均 success（真实来源 116843100304、合成测试 116843100521；Ran 13 tests / OK）。实际通过原作者固定提交下载 5 个原始文件，核验准确 Git blob SHA1 和字节数，解压/解码、逐行列检查并生成仅包含匿名聚合数据的 artifact `12029108180`。机器读取结果永久归档 [R066_E2_TWO_CANDIDATE_RESULTS.json](R066_E2_TWO_CANDIDATE_RESULTS.json)。个人 ID、原始评论、逐人意见时间序列和帖文永久链接均未提交到本研究 GitHub。

## 二、候选 A：Monti 2020 Reddit 社会互动痕迹

原作者 [corradomonti/learnable-opinion-dynamics](https://github.com/corradomonti/learnable-opinion-dynamics)，固定提交 `5d31ba59e716e5bde85e4c56b9cdacc3920aaaf6`。四个来源压缩文件全部字节哈希校验 PASS。

| 数据文件 | 真实行数 | 字段结构 |
|---|---:|---|
| edges_user.tsv.bz2 | 90,772 | 月份、被回复者、回复者、次数 |
| edges_feature.tsv.bz2 | 144,677 | 月份、用户、社区、次数 |
| feature_scores.tsv.bz2 | 144,677 | 用户、社区、月份、正/负分及对应帖子数 |
| interaction_scores.tsv.bz2 | 139,529 | 日期、回复双方、评分及帖子关系字段 |

四表合计 **519,655 条数据行**，不是 519,655 个独立受试者。两份 edge 文件均覆盖 **2008-01 至 2017-12，共 120 个月**；用户回复边表的权重和为 139,529 次，用户参与社区的权重和为 4,226,515 次。其他文件可能有帖子链接或用户字段，但研究仓库没有重新分发其原始内容。

**测量门：`BLOCKED_MEASUREMENT`。** 表格明确记录互动、社区参与、正负帖子评分。没有逐人直接意见自评量表，更没有可直接用于三个确定性连续意见状态模型的真实 `x_i(t)` 标签。这里的作者论文可以从社会痕迹推断*潜在*意见，但那是附加生成式测量模型与假设，不能自动当作 DeGroot/FJ/HK 的已观测状态。因此这个数据源适合未来探讨「隐变量观测层如何融合网络模型」，不适合当前零假设下直接比较三模型行为预测。

## 三、候选 B：Okawa–Iwata 2022 人工标注的帖子级意见

原作者 [mayaokawa/opinion_dynamics](https://github.com/mayaokawa/opinion_dynamics)，固定提交 `32441421a9a012acc64b206f73a2b6525580e3ce`。`working/posts_final_sample_twitter_Abortion.tsv` 的真实 blob `2a88788f32496a8ebe45293ecf95eaf516876df6`，279,372 字节，逐字节与来源记录一致。

原始列名：`user_id, opinion, time`。真实解析取得：

| 匿名源结构统计 | 结果 |
|---|---:|
| 已标注发文行数 | 9,944 |
| 文件内不同 `user_id` 值 | 300 |
| 至少两个不同时间点出现的 `user_id` 值 | 300 |
| 不同归一化时间点 | 9,942 |
| 时间最小值、最大值 | 0、1 |
| 观点类别 0 / 1 / 2 / 3 | 3,700 / 2,995 / 1,862 / 1,387 |

**重要原始说明差异：** 作者 README 描述该样本包含「100 名最活跃用户」，实际固定文件出现 **300 个不同的 `user_id` 值**。本阶段只能确认文件标识数量，无法据此判断 300 值是否代表 300 个彼此独立的真实人或 README 过时。保持 `README_SAMPLE_SIZE_DISCREPANCY=OPEN`，不得选用 100 或 300 作为已证实的受试者人数。不能用数字标签 0–3 的线性重标度自行定义真实人的连续潜在态度差异。

**测量门：`BLOCKED_MISSING_NETWORK_AND_LATENT_MEASUREMENT`。** 有重复的帖子级人工标注类别与时间，却没有与同批参与者关联的真实社交影响边 W；样本意见标签也不是经验证的连续个体意见量表。虽然这组数据较适合以后测试不同的**时间序列意见观测映射**，但目前不能将人工贴文分类当作 DeGroot/FJ/HK 的已识别社会机制。未经协议，不以所有用户的平均网络代替真实可观测交互网络。

## 四、第三候选：Larson–Lewis 2026 纵向调查与村庄社交网络

进一步检索发现 Jennifer M. Larson 与 Janet I. Lewis 的 *Networks shape political attitude change*，2026-08-10 在线发表于 *Network Science*，DOI `10.1017/nws.2026.10038`。作者报告来自 **16 个乌干达村庄**的基线/两三周后个人态度调查、社会关系网络，以及部分受试者的随机干预处理。这种同一个体重复态度量表加可测网络的设计在测量层面更适合 R066 的模型判别，但还需核对每个变量、时间离散程度、干预如何作为外生冲击进入模型，以及作者数据许可和隐私边界。

论文 Data availability statement 指向 Harvard Dataverse DOI `10.7910/DVN/RAHSVM`。**本轮没有成功取得 Dataverse 数据记录、版本号、任何原始文件或实际数据 schema**，所以该来源状态仅为 `METADATA_CANDIDATE`，远未达到 E2。不得声称已成功读取或验证第三候选数据。下一工作应优先核实 DOI 访问和许可、字段与样本匿名性，必要时选择替代的带真实网络和重复意见量表的数据。

论文入口：https://doi.org/10.1017/nws.2026.10038

## 五、结论与新模型研究计划

- `R066_E1_THREE_MODEL_MECHANISMS=PASS`：此前三模型合成运算和 25 项测试已验证。
- `R066_E2_TWO_SOURCE_INTEGRITY=PASS`：真实原始 5 文件、全部结构行、13 项边界测试成功。
- `R066_EMPIRICAL_THREE_MODEL_DISCRIMINATION=BLOCKED_MEASUREMENT`：来源完整性不自动升级为模型解释力的证据。
- `R066_NEW_NETWORK_AND_REPEATED_ATTITUDE_SURVEY_DATA=OPEN`：第三候选的数据实际访问和法律/隐私检查未完成。
- `R066_EXTERNAL_E3=OPEN`，`PESEN_v0.1=FROZEN`。

若第三候选不可获得，应扩大搜寻「同一受试者多时间点态度量表＋真实关系网络」的历史或社会实验数据。在没有 E2 模型可辨识条件时，不启动消耗计算资源的伪经验三模型优劣排名。下一阶段可以独立研究测量误差与潜在社会机制的关系，保留与 R065 的个体认知机制对接可能性。
