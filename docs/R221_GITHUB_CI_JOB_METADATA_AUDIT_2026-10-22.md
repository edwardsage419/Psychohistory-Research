# R221 GitHub Actions作业状态与真实运行日志分歧：独立复核记录

复核日期：2026-10-22。本报告仅记录CI元数据与实际运行日志，不改变R221六SCM任何冻结协议、数学数据、结论、来源SHA或已归档正式验收，也不擅自声称队列字段已修复。

证据源：GitHub Actions [run39784385018](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39784385018)，整体status=completed、conclusion=success。

实查 `GET /repos/edwardsage419/Psychohistory-Research/actions/runs/39784385018/jobs`：

| GitHub作业 | 真实Job ID | jobs接口状态 | jobs接口结论 | 真实日志 |
|---|---:|---|---|---|
| Python3.11测试 | 119843571961 | queued | null | Ran 39 tests，OK |
| Python3.12测试 | 119843571405 | completed | success | Ran 39 tests，OK |
| 完整原来源归档 | 119843651457 | completed | success | 结果永久归档 |

经 GitHub connector 实际读取上述两Python的逐作业独立执行日志，二者均显示真实单测39项和最终OK，合计78次测试执行；3.11作业日志有真实运行时间戳2026-10-22 13:09:33 UTC，与同一API继续显示queued/null不一致。**此分歧属于可查询作业元数据一致性缺口，现已如实记录；不臆断GitHub内部具体成因**。

科研层面，R221有限合成SCM因果中介的精确计算由程序、永久归档的48条来源和两个版本的实际测试日志支持。CI总任务成功与两份日志通过不允许改写3.11真实jobs字段，也不能作为真实E2或E3证据。需要日后复验接口时保存新时间戳和真实job字段；未来如果GitHub显示已纠正，应补一条新日期状态记录而不覆盖本文件。

保持R221 [原最终机器验收](../research/R221/R221_FINAL_ACCEPTANCE_STATUS.json)中的异常说明，R073与PESEN v0.1仍冻结。
