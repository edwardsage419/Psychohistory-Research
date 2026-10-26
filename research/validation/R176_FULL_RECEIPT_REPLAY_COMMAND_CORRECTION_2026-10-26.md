# R176补档报告复跑命令路径更正

日期：2026-10-26。更正范围仅限 `R176_FULL_RECEIPT_ARCHIVE_CLOSURE_AND_STATIC_CHECK_2026-10-26.md` 末段的B程序文件名。该报告暂写 `r176_b_path_mass_20261026.py` 并注明待核实。已重新读取原B科学报告 `research/evidence_audit/B_R176_PATH_MASS_IDENTITY_SCIENTIFIC_AUDIT_2026-10-26.md`，其实际记录的脚本路径为 `research/evidence_audit/r176_b_path_mass_identity_20261026.py`。

正确运行顺序：

```sh
python research/validation/r176_institution_observability_20261026.py
python research/evidence_audit/r176_b_path_mass_identity_20261026.py
```

原始60487字节完整JSON已经在 `research/validation/r176_institution_observability_receipt_20261026.json` 单独归档。此更正没有重新执行B脚本或GitHub Actions，不更改科学结果、源文件或冻结协议。