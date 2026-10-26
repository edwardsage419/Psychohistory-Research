# R176完整精确收据补档与静态一致性检查

日期：2026-10-26。目标：关闭E015-01指出的原始收据Git归档缺口，不改变R176任何冻结模型、参数或原研究结论。

原始完整文件由先前R176计算在本地生成：`r176_institution_observability_receipt_20261026.json`，60487字节、1907行、48对人工世界，原始SHA256 `a7c45ab4637a49cbf80958e3deade64e8cd3be0a758edfeaf44b5fc95933aa0a`。本轮在容器对原始字节重新计算SHA256与此前摘要记录严格相同，之后通过当前会话附件原始文本逐行无损重建。新文件路径：`research/validation/r176_institution_observability_receipt_20261026.json`。GitHub远端回读60487字节与本轮上传内容逐字节一致，Git blob `bb9b4d604575478846f40120dde3b1fdbed2d6fc`。原摘要收据仍保持原样，其历史字段 `full_receipt_archived=false` 反映当时状态，不得静默修改；本文件记录之后的状态转移。

独立静态核验完整48行，每行13期joint_tv及count_tv，总计1248个精确有理数单元。24组退出率0在13期均为零；24组退出率1/4在第2期joint首次非零、第3期count首次非零；全部624个时点满足 `0<=TV_count<=TV_joint<=1`；与原摘要的t2、t3、t12四组最小最大值共8个极值严格一致。异常0。此检查读取已经归档的数值，**没有重新运行R176全状态转移程序**，所以不能替代第三条算法对t4..t12的独立逐格复算。外部复现0。

本轮完成原始数据归档完整性修复。E015-01可以标记为CLOSED_ARCHIVE_BYTES_VERIFIED，E015-02后期第三路径复算仍OPEN。R176原有E1验收不变；E2/E3新增0，R073/PESEN v0.1继续冻结。复跑依赖链：先执行 `python research/validation/r176_institution_observability_20261026.py` 可重生成同名完整JSON，再执行 `python research/evidence_audit/r176_b_path_mass_20261026.py`（实际B脚本路径请按仓库中已归档名称核实）；现在静态归档已提供原始B输入字节。未运行远端CI。