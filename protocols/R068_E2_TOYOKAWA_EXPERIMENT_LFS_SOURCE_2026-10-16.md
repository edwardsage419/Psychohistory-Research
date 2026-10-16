# R068：2022 人类社会学习实验的固定 Git LFS 来源与可识别性审计

日期：2026-10-16。**首次下载作者完整 LFS 数据对象之前冻结**。本协议只是 E2 原始数据结构、来源与认知学习规则可识别性检验，严禁在此关拟合 R068 的三人多数公式或 success-bias 强度。

## 文献与固定来源

Toyokawa, W. & Gaissmaier, W. (2022), *Conformist social learning leads to self-organised prevention against adverse bias in risky decision making*, eLife 11:e75308，[论文](https://pmc.ncbi.nlm.nih.gov/articles/PMC9090329/)。作者公开完整分析代码仓库 `WataruToyokawa/ToyokawaGaissmaier2021`，固定 `main` commit `6fca0b26c33af3a5b3c415719fa3df0dced15149`（论文引用 SWH 相同 commit）。仓库的 Git LFS 文件**不是** Git blob 本体；源完整性必须同时固定 Git LFS pointer 文本 Git SHA 和 LFS payload SHA256/字节数。

选定两个实验行为文件：
- `experimentalAnalysis/allBehaviour1022_group.csv`，pointer Git blob `fc3d579f02f248b4a62b24a545f596ecd703b754`；LFS `sha256:b01af9eb32945c57b6a9528c2f7e291e955819c1df799cfc942708473cd4ceb3`，预期 4,144,197 bytes；
- `experimentalAnalysis/allBehaviour1022_indiv.csv`，pointer Git blob `d260e6b6858d29dfe11215c9543ea97d98a07282`；LFS `sha256:06ddbf5dbe64893f841ef6801c6e1e00553869eb774ee05740b8cf0d1f6801c1`，预期 2,306,541 bytes。

## 事先定义的验收门

1. 真实 CI 使用 `git init` + `git fetch origin <固定 commit>`+ `git checkout --detach FETCH_HEAD`，`git lfs pull --include` 精确上述两个文件，不下载其它 LFS 原始数据。首先用 `git rev-parse HEAD` 强制校验固定 commit，`git cat-file -p HEAD:<文件>` 检查精确 pointer 和 oid/size，然后检查 payload sha256/字节数。若服务器拒绝 LFS 或仅返回 pointer，标 `NETWORK_OR_LFS_DATA_UNRESOLVED`，**不**把 pointer 当真实行。
2. 仅对确实已经获取的 UTF-8 CSV 进行严格 `csv.reader` 完整表格解析，输出字段名（仅 ASCII 字母/数字/下划线/点/短横线安全白名单）、行数、列数、重复字段/形状错误数、总体空值统计、字段名可能涉及的 `subject/group/round/trial/choice/social/frequency/reward/payoff` 字面候选。**不能输出任何个体值、结果轨迹、各实验组的小组统计或原始 ID。**
3. 总行数限制 250,000、列数 400、每文件最多 8 MB，UTF8 无法解码、字段无效或行宽不一致 fail closed。强制 exact two-file source and pinned SHA; 一份无法获得，则总状态 `SOURCE_UNRESOLVED`，不可仅拿另一份称全部通过。
4. 依据**来源目录与字段名**只能判断“有可研究的候选列”；只有实读作者代码对每个字段定义，确认学习者选择、观察到的示范者局部频率、示范者获得奖励、是否观察到三位独立示范者及选择时序，才能开始下一轮行为映射。没有看到这些条件不代表实验失败，只代表 **R068 的特定最小三人从众/成功权重模型不具备直接验证资格**。
5. GitHub 输出只包括元数据与哈希；源个人记录临时保存在 Actions runner，作业末尾删除，不将作者可能有版权/同意限制的个体 CSV 再发行。来源无显式 LICENSE；**公共可读 ≠ 无限制再分发授权**。当前只审计，不把作者数据转售/公开。
6. 运行 10+ 合成 fail-closed 测试（hash 不符、Git pointer 被误认为 payload、列重复、行宽、缺项、非 UTF8、匿名头部保护、大小限制、来源版本变化）；CI 真实运行成功和科学可识别性判断分开报告。

**目标：** 若来源通过，则 `SOURCE_SHA_AND_SCHEMA_PASS`，仍 `E2_MODEL_IDENTIFICATION=OPEN`。R068 E1 合成概率继续 FROZEN；PESEN v0.1 FROZEN。

`R068_TOYOKAWA_LFS_SOURCE_PROTOCOL=FROZEN`
`R068_REAL_MODEL_FIT=NOT_AUTHORIZED`
`PESEN_v0.1=FROZEN`
