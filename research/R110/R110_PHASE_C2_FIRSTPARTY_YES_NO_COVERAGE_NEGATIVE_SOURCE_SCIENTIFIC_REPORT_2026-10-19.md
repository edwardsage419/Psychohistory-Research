# R110 C2：2015 UCL 原始合作动作 yes/no 编码覆盖审核（正式限定研究结题）

日期：2026-10-19（Asia/Taipei）
学术出处：Bone JE, Wallace B, Bshary R, Raihani NJ (2015), PLOS ONE, https://doi.org/10.1371/journal.pone.0117183
原 S1 发布附件：https://doi.org/10.1371/journal.pone.0117183.s001
冻结先于本轮真实编码审阅：protocols/R110_PHASE_C2_2015_UCL_ORIGINAL_AUTHOR_YES_NO_WORD_CODEBOOK_SOURCE_ONLY_PRESCORE_FREEZE_2026-10-19.md
真实CI：https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39222908506
机读原始匿名证据：research/R110/R110_PHASE_C2_LIVE_CI_ORIGINAL_2015_UCL_AUTHOR_YES_NO_WORD_SCHEMA_OR_FAILURE.json

## 1. 真正结果

8项不取真人数据的合成测试通过之后，原GitHub Actions从已冻结合法的出版方交付路线取得真实原文件，调用同一B1真原人/游戏/轮结构与原始全文件 SHA256=ea70b0f3d98075f9d3e4401becfcdec8f6bdb5cae00c4dad63a697f9b61d7b5f。两个CI jobs 均为 success，成功表示程序审计和归档完成，不表示来源编码全通过。

C2预设的合作词典：仅ASCII首尾空白裁剪与大小写折叠后的 yes=1、no=0；其余源字面不能推测。12,000个原来源行中：

| 原始合作列 | yes | no | 其它非空字词 | 空白 | 合计 |
|---|---:|---:|---:|---:|---:|
| Player cooperated（本人合作） | 7,437 | 2,173 | 2,390 | 0 | 12,000 |
| Partner coop prev（作者记录的前轮伙伴合作信号） | 7,606 | 4,154 | 240 | 0 | 12,000 |

源Partner opt out prev仍按原C0数值接受集检查：10,454条为0、1,306条为1、240条无法解码。没有读取或发布任何不认识的原始文字，不判断其含义。两游戏各6,000行，具体按匿名处理类别机器收据保留；C2已验证 yes/no 词存在于真实原来源，但**原始两个合作字段均非100%覆盖**。来源词典门真实结论：C2_UNMAPPED_SOURCE_TEXT_REQUIRES_CODEBOOK。

## 2. 科学结论

2015 PLOS原论文S1说明作者伙伴上轮字段的 yes/no 含义；这为已匹配 yes/no 项提供出版方第一手语义，但不能使另外2390条本人记录和240条伙伴信号自动合法。特别是后者240与原120人×两局的首次回合数恰好相等，尚无逐原回合交叉诊断证明未知文字都在首轮，不能将该数值巧合转换为已证实的码本。本人未知2390条是否属于退出、破产、未出席或其它状态亦尚不可确认。

原C0接受的是0/1数值源字面，已作为独立历史失败锁定；C1和C2属于后续来源诊断，不追溯更改C0筛选和模型目标。此前原C0模型五项同目标实际真人Brier评分条目数为**0**，不是任何模型 Brier 值为0。R110的原S1完整来源E1通过、真实120人身份基本结构通过，确切真实伙伴人号与原场次号没有独立核验，因此即使以后码本可得，也不能自动称为真实实验室LOSO或严格R073跨来源复现。

## 3. 有界结束与重新开放条件

本轮对未知源词停止猜测，保留C1、C2全部实名去除的真实机读失败证据。**R110=CLOSED_BOUNDED_E1_ORIGINAL_BEHAVIOR_TEXT_CODEBOOK_UNMAPPED；学习状态 LEARNING_PARTIAL_SOURCE_BLOCKED；真人E2预测=0，PESEN v0.1及R073保持冻结。** 若未来从作者/出版方获取对未匹配原词的完整、唯一、精确对应说明，并能合法区别退出/破产的目标资格，可另行冻结新版本模型与退出逻辑，在看任何预测分数前独立审阅；不更改C0。否则推进既定R系列其他研究。
