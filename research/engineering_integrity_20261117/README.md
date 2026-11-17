# R 系列完整性工程交付

以 [REPORT.md](REPORT.md) 为整体报告。R132 原始13条件已加固，历史收据/协议不变；新增证明仅为本地工程复验。九个PR可按限定范围归档，生产/科学准入与冻结审批保持独立。所有真实失败与当前源码身份可追溯。

- R132：R132_TEST_MATRIX.json、logs/r132-*、final-integrity-review.md
- R275：r275_archive_gate_v2.py、test_r275_archive_gate_v2.py、logs/r275-v2-*；旧入口仍禁止生产使用
- 九PR：PR_HEADS.json、pr-dependencies-report.md、pr-native-report.md、combined-verification/
- 原失败证据：logs/r132-red.log、logs/r132-cache-red.log、r275-original-reproduction/
- 原历史文件逐字节保护：IMMUTABLE_R132_FILES.json

不合并、不部署、不启用工作流、不启动新的科研主线。
