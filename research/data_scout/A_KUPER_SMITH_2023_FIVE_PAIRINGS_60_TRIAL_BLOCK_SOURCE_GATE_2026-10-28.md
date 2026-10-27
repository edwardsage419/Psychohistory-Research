# A轨 Kuper-Smith与Korn真人实验配对日程来源级核验

日期2026-10-28。英文一手作者仓库 https://github.com/dnhi-lab/losses_gains_2x2 。本次实际读取作者固定源码，未下载或归档参与者级CSV，未重做真人行为评分。此前本项目已在2026-10-26归档该数据的33702行逐行来源审计（`research/data_scout/KUPER_SMITH_KORN_V2_TAG_ZENODO_R073_COMPATIBILITY_AUDIT_2026-10-26.md`）；本次只增加配对日程的独立源码验证，不把既有33702行记作新增记录。

## 五份直接读取的源码

1. `materials/data_collection_iterated/defStudy.m` Git blob `1bc7f0ab4b3c83136db277475aa85c7840b403a`，多人模式20个不同收益矩阵、每矩阵重复3轮，给出5种六人完全匹配。
2. `materials/data_collection_iterated/playTheGame.m` Git blob `c985af146613aef8bfc9d0563fe0f1f5554e1376`，每个区块遍历20矩阵×3轮，记录对手ID。
3. `materials/data_collection_iterated/defBasics.m` Git blob `356666d810d212afb86f6e22faf426f3ca53b976`，区块编号和配对方案由人工输入，实际执行顺序需要真实数据确认。
4. `analysis/format_data_Exp_1_2_3.m` Git blob `6965e66ac05ec67b519f0674a708fcdcef917785`，5个区块、全局300试次，实验1对手ID显式NaN；前次自己及对手行动只在全局300轮身份边界重置，不按60轮区块重置。
5. `analysis/exclude_participants_iterated.m` Git blob `0188f3d6f7d7c3a803c9a6a8f95ef83af0355e27`，跨实验重复参与者ID135、231、255、246被手工排除第二次参加，另有无效反应过滤。

独立静态程序 `research/data_scout/a_kuper_pairing_source_static_gate_20261028.js` 直接验证：20矩阵×3轮=每区块60次；5种六人配对方案各含3对，合计覆盖15个不重复的无序配对，恰好构成六人完全图的一次分解。作者源码内配对输入为人工选择，因此实际五个区块是否严格使用全部五种不同方案仍待真实行级检查。每个固定收益矩阵在单区块内连续重复3次，跨矩阵收益条件变化；把全局300次当成单一固定对手、固定收益的300轮重复博弈会产生错误的风险集和历史反馈定义。

## R073准入及数据治理

R073冻结协议要求原Montero来源的FP/SP两处理、每处理6个独立场次、每人100轮、t3..100的18424个共同目标、七个模型、alpha=20和同处理5场训练留1场评分。Kuper候选的六人分组、每区块60次、五种配对方案、20种收益矩阵及300次全局试次与该冻结宇宙无法直接映射。**直接原R073零改动复评分状态继续为BLOCKED**，即使能够获取全部CSV也不能将其标作R073同口径独立复验。未来可另立先冻结的真人E2协议，但必须保留来源独立性、对手切换、时间可用性、许可和跨实验身份去重检查。

作者仓库根MIT文本适用范围写为Software与documentation；原始真人数据的独立再分发授权仍需单独确认。公开作者源码可读，当前本轮没有新增原始行为数据行级核验。新增E2=0，费用0，未访问私人数据。
