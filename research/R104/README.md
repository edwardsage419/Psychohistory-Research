# R104：2024年独立PLOS公共品重复实验公开原数据第一手来源资格

日期：2026-10-17。**R104=IN_PROGRESS_ORIGINAL_PLOS_FILE_ROUTE_REJECTED**，尚无真实原CSV双重SHA成功，E1完整原文件认证未成立，真人E2评分0，PESEN v0.1 FROZEN。

作者Liu、Tsai、Chen、Cheng，2024年`PLOS ONE`论文DOI [10.1371/journal.pone.0299196](https://doi.org/10.1371/journal.pone.0299196)，原作者出版社配套[S1 Data CSV](https://doi.org/10.1371/journal.pone.0299196.s002)。论文公开描述**96名真人、八原实验场次、每场12名真人、4人互动小组及20轮固定组重复公共品博弈**，分别对照简化/详细反馈。它们是**论文设计描述**，本项目尚未对原CSV来源行动与人员结构独立核验。这是不同于R102和R103的新作者团队实验；预计可在严格原来源身份合格后研究前轮自己与同伴贡献和同等收缩安慰剂。

实际执行前独立[冻结Phase A出版社原CSV完整SHA两次重取和header-only来源协议](../../protocols/R104_PHASE_A_2024_PLOS_ONE_PUBLIC_GOODS_ORIGINAL_SUPPLEMENTARY_CSV_DOUBLE_SHA_HEADER_FREEZE_2026-10-17.md)，仅准官方网站`journals.plos.org/plosone/article/file`同一精确DOI附件路径，最多1MiB，仅CSV表头，零原贡献及人号应用读取。原PLOS公开资料尚未提供本项目认证的发表方MD5，因此项目双来源SHA只能证明出版方真实字节可重复，不能虚称出版方外部摘要一致性。12项纯合成来源及安全测试完成后，真正GitHub Actions官方请求触发**`R104_PLOS_ORIGINAL_URL_NOT_PINNED`严格来源URL安全阻断**，[第一次真实来源阴性收据](R104_PHASE_A_LIVE_CI_PLOS_2024_ORIGINAL_CSV_DOUBLE_SHA_HEADER_ONLY_RECEIPT.json)由GitHub Actions机器人永久提交[commit 03eb8fd1](https://github.com/edwardsage419/Psychohistory-Research/commit/03eb8fd1b52c66d5307641af681ed7d38f24bcbc)。此错误表明有URL未匹配既定出版社路径；真实跳转位置、是否跨域、源响应体为何均尚未独立判明，**不能直接断言PLOS数据不可访问、缺失或其内容有问题**。没有一条真人行为数据被读取或评分。

**当前结论：R104源出版网页与附件DOI公开存在，原文件完整E1未建立，真人评分E2=0。** 下一步骤限于另立预冻、零响应正文的确切重定向路径诊断；若无法严格认证出版方交付链，则有界终止转向另一更容易哈希认证的真人原数据集。不能以来源传输失败宣布心理历史模型阴性。


## 2026-10-18 正式撤销“新独立实验”候选资格

**最高优先级正式纠错**：[R104完整原始DOI重复审计及限定结题](R104_FINAL_DUPLICATE_OF_R099_CORRECTION_REPORT_2026-10-18.md) · [机读结题状态](R104_CURRENT_SOURCE_STATUS.json)。在已结题的[R099](../R099/README.md)中核验到了**与本R104完全相同的论文DOI和S1数据DOI**，原R099本来已经取得真来源43,467字节的SHA256、96真人、24四人组456个组轮LOOG真E2。此前本README的“新独立实验团队”表述已正式撤销。R104新增独立样本0，新增真人E2 0；不再重试此PLOS源下载。最早真实严格来源URL失败收据完整保留，不将R099原数据成绩复制成新的外部复现。**R104=CLOSED_DUPLICATE_OF_R099_NO_NEW_EXPERIMENT，PESEN v0.1 FROZEN。**
