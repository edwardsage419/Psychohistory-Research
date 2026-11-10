# R127 CI 日志尾随 OK 错误接受：独立负例审计

审计范围：R127 历史工作流日志解析器，独立于此前已登记的 Python -O assert 失效缺陷。
目标工作流：.github/workflows/r127-van-huyck-1990-coordination-source-table-60-tests.yml
审计时目标 Git blob：4b22f653dc7516bb31ead23e45dcf7f62261d79d
审计起点 main：754fb01700c7200b3a337e2dfe71bbd2e7e92266
科研证据等级：验收工具完整性反例；无新增 E1/E2/E3 科研证据。

## 可执行反例与结果

现有解析器的两个条件是 `re.findall(r'Ran (\\d+) tests? in', log)==['60']` 和 `re.search(r'\\nOK\\s*$', log)`，通过 Python assert 执行。

输入：
```text
Ran 60 tests in 0.1s
FAILED (failures=1)
OK
```

在独立 Python 进程执行相同两个断言时，普通模式退出码 0，优化模式退出码 0。日志中明确包含 FAILED，尾随伪造 OK 却使两个条件同时成立。这一问题独立于 -O 的断言删除。控制组 `Ran 60 tests in 0.1s\nOK\n` 通过，`Ran 59 tests in 0.1s\nOK\n` 在普通模式被拒绝。

## 边界

反例只证明日志解析器会错误接受被篡改的文本。完整生产工作流的测试命令使用 `set -euo pipefail`，原生 unittest 失败通常使步骤直接失败。尚未证明真实生产 CI 可以在原生测试失败时成功通过。历史成功运行及数学结果不因此自动失效。

## 最小修复建议与独立控制

由 R 主线拥有工作流修复。使用显式异常或退出检查替代 assert，并且明确拒绝日志中任何以 `FAILED`、`ERROR` 或 `FAIL` 开头的行；限定恰好一条 `Ran 60 tests in ...` 汇总行以及独立 `OK` 行。独立验证在 Python 普通与 -O 模式下均得到：正常日志退出 0，59 项退出 1，含 FAILED 且尾随 OK 的伪造日志退出 1。该建议仍需在原工作流上实施和验证。

本审计只新增独立审计文档，不修改模型、冻结协议、R 主线工作流、CI 或历史收据。未触发 Actions，未购买数据或计算资源。正式原始目录 05-003 保持待核，R127 保持 CLOSED_BOUNDED。
