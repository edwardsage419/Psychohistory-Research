# R092 发布数据格式与研究接纳限制报告（2026-10-17）

**状态：R092=CLOSED_SOURCE_FORMAT_BLOCKED，源身份已核验（E1），真实个人行为/群体轮次表尚未接纳，独立跨作者预测E2=NOT_ESTABLISHED，实验前瞻E3=NOT_ESTABLISHED。PESEN v0.1=FROZEN。**

## 研究独立来源及当前科学边界

作者 Wang, Xiaomin / Hilbe, Christian / Zhang, Boyu；公开2025-08-21 Zenodo v2 固定 record 16918146，DOI [10.5281/zenodo.16918146](https://zenodo.org/records/16918146)。选定不同原作者阈值公共品四人组的 `ThresholdPGG_4P_ExperimentalData.mat`，出版方文件MD5 `6036f73c2f758ab3aeed6dcf4f74585b`，实际固定长度 **17,159 bytes**，整文件SHA256 `76b02d921d02ad652cb952a71173e84b206135e4deb7bfc6235b9387738a6b05`。独立首方来源确认成功。

数据集出版方描述该**文件**含FE平等N=76、AI对齐不平等N=100、MI错位不平等N=100，共276名原始真人；每人两个20轮实验场次，第二场重新配组且同一原受试者再次参与。源描述指列`Treatment,Session,GroupID,PlayerID,GlobalPlayerID,Round,Contribution`，但**并没有在当前程序从真实MAT内部核验这些字段结构**。若可正确读入时，理论上期望138个group-session单位、552名次人-session、11040个行为机会；**此处仅预先发表的设计预期，不得当作实际已读取的记录数。** 原始贡献数值是连续贡献，不是与R089完全同定义的二元global投资票数。

## 三份隔离、分别在原件下载前冻结的原始格式检验与失败保留

1. [Phase A来源格式冻结](../../protocols/R092_WANG_HILBE_ZHANG_2025_ASYMMETRIC_THRESHOLD_4P_ORIGINAL_ZENODO_MAT_SOURCE_FREEZE_2026-10-17.md)，commit `16aa141e3e28bf568dba06917542bd297f402f6c`，先执行19项纯synthetic。原CI [39016848341](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39016848341)首次synthetic中，截断MAT原件抛出MatReadError异常未被捕获，失败发生于访问真人原件前；只补充`MatReadError` fail closed，不修改任何模型，合成19全通过的[CI39016888560](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39016888560)真实首方源经完整MD5证实，但`scipy.io.whosmat`返回`R092_UNSUPPORTED_ORIGINAL_MAT_STRUCTURE`，实证评分0。
2. [Phase A2仅HDF5变量结构冻结](../../protocols/R092_PHASE_A2_ORIGINAL_PUBLISHER_MATLAB_V73_HDF5_METADATA_ONLY_FREEZE_2026-10-17.md) commit `cf6eaca85a74ed70aaf291e5e1f8fae2520c3745`。原CI [39017000035](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39017000035)34项synthetic全部通过，真人来源MD5已通过，但不符合预设HDF5签名（offset0及512），**严格失败** `R092A2_NOT_SUPPORTED_PINNED_HDF5_OR_MAT_V73_FORMAT`，没有读或推断任何作者人类合作数据。
3. [Phase A3有限文件类型信号冻结](../../protocols/R092_PHASE_A3_ORIGINAL_THRESHOLD_MAT_RESTRICTED_FILE_SIGNATURE_DIAGNOSTIC_FREEZE_2026-10-17.md) commit `6b9a1741e4b80e3133b8fafcb617dc546a06e30a`。原CI [39017117283](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39017117283) 47项源哈希/安全头/隐私synthetic全部PASS、真人原件再次固定MD5与原文件SHA通过，结果表明 `MATLAB 5.0 MAT-file` 文件头识别，**不是MATLAB 7.3/HDF5**。但`scipy.io.whosmat`对该作者真实文件返回`TypeError`而不是可用的变量结构，因此源行为表仍不可读取、不可评分。有限安全收据只包含文件头格式信号，**不含原始二进制字节和任何作者记录的字段值**。

已获证实的是：下载端来源真实性、版本固定及严格预先来源处理、可重演的两次技术不兼容/拒绝；**没有证实**：原件内GroupID×Session稳定组成、20期无缺失真人行为、真实贡献值范围、M0/M1/M2预测收益、以及R089跨实验同二元目标复现。MATLAB 5格式的识别不能取代变量解析；`TypeError`也不能推断作者数据文件“已损坏”。未来可在另一已冻结程序中评估Octave/兼容MATLAB读取器，但不得在当前缺乏数据资格情况下继续计算所谓真实预测。

## 完成状态与统一标准

A01 独立原作者备选题及前测计划**PASS_SOURCE_SCOPE**；A02官方原始MD5+全SHA身份**PASS_AUTHENTICITY**；A03真实行为模型与实验适应性**BLOCKED_UNREADABLE_SOURCE_FIELDS**；A04所有原格式失败和不兼容**PASS_NEGATIVE_EVIDENCE_RETENTION**；A05不把E1/source格式等同E2/E3**PASS_EVIDENCE_BOUNDARIES**；A06研究冻结、完整来源程序、47synthetic校验和永久Git报告**PASS_SOURCE_ARCHIVE**。因此严格不能在该阶段写“统一标准A01–A06全部PASS”或宣称实证完成。

**R092正式状态=SOURCE_FORMAT_BLOCKED_CLOSED；E1来源认证成功、E2/E3未成立；PESEN v0.1继续FROZEN。** 下一步R093优先别的可直接读取且公布二元全体公共品原始逐轮行动的独立真人实验，或在独立冻结的MATLAB 5专用源解码中重新尝试R092，前提是不能为了符合预期修改冻结的M0/M1/M2比较。
