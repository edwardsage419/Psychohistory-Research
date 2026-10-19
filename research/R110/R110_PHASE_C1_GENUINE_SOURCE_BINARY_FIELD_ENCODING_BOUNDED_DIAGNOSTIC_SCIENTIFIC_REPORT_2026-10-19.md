# R110 C1：2015 UCL 原始来源行为编码与资格失败诊断（正式有界报告）

日期：2026-10-19（Asia/Taipei）
来源研究：Bone, Wallace, Bshary, Raihani (2015), PLOS ONE, doi:10.1371/journal.pone.0117183。
原附件：https://doi.org/10.1371/journal.pone.0117183.s001
官方方法说明：https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0117183

## 预冻结与原始结果

C1预冻结：protocols/R110_PHASE_C1_ORIGINAL_UCL_BINARY_AND_ELIGIBILITY_DIAGNOSTIC_SOURCE_ONLY_FREEZE_2026-10-19.md；旧C0失败收据保持不变。真实运行：GitHub Actions https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39222228439 ，两个jobs均success，按先13项纯合成后原始来源的顺序运行，机器输出 research/R110/R110_PHASE_C1_LIVE_CI_2015_UCL_ORIGINAL_SOURCE_ANONYMOUS_ELIGIBILITY_OR_FAILURE.json 已自动归档。原始全文固定SHA256=ea70b0f3d98075f9d3e4401becfcdec8f6bdb5cae00c4dad63a697f9b61d7b5f。验证的来源宇宙为120位真实匿名ID、每人两游戏各50轮，合计12000原行；两游戏每类6000行。

严格沿用冻结C0的二元接受集 {0,1,0.0,1.0}（容许外侧空白），源 Player cooperated 全部12000行为非空、非数值文字；源 Partner coop prev 同样全部12000行为非空、非数值文字。源 Partner opt out prev 其中接受0有10454行、接受1有1306行、其他非空文字240行。依C0互斥排除顺序，首轮240行、之后11760行全部在原本人合作行动二元编码门排除，剩余其它排除原因均零；合格预测目标0、合格人物0、合格游戏类别0。所有计数之和12000，未发布任何原始编码词、人号、逐行原行动。

**科学解释**：C0是原源动作编码与预冻结数值解析合同不匹配导致合法目标门失败。它既不是经过竞争模型评分的阴性结果，也不构成正面模型验证。C0原失败状态保持 R110_C0_PRE_FROZEN_REAL_800_TARGET_40_ACTOR_2_GAME_GATE_FAIL，真实M0至M4 Brier评分条目数为0，未产生可报告的真实Brier数值。C1本身也没有执行预测评分。

## 出版方独立字段说明与下一局部研究门

原PLOS论文同页 S1 Supporting Information明确说明：Partner coop prev 用 yes 表示上一轮伙伴合作，用 no 表示上一轮伙伴背叛；S1也解释多项行为派生字段的0/1含义。论文Table 4解释二元玩家合作的分析语义，但本轮尚未实证确认发布CSV Player cooperated 字段具体文字是否同样为yes/no。论文语义与精确原CSV单元编码必须区分。后续只可另冻**C2无预测的精确作者字典匹配审核**，对三行为字段计数 exact yes/no（含外侧空白及大小写是否允许需先锁定）。如果存在任何未覆盖文字，仅作未知状态并停止重编码。不得因C1 0目标而修改、覆盖C0模型和阈值；任何新解码模型评价都需另立C3协议，在观察可评分结果前冻结，标为独立扩展研究，不能追认C0通过。

## 限制

没有原始实际同伴人物ID，也没有真正实验室session列。作者上一轮伙伴信号不能冒充独立重建的本人对手历史。即使以后成功解析动作，不能称R073完整冻结模型的精确跨场次复验、因果社会学习或日历前瞻。

PESEN v0.1与R073继续冻结。R105真实多人同权收缩阴性与R106真实双人同权伙伴正向并列保留。
