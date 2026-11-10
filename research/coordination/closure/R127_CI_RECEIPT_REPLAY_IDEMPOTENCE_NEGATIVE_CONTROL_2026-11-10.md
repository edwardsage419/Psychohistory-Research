# R127 CI 收据重复执行幂等性独立负控（2026-11-10）

track: independent R closure audit
starting_main: 5158c2ad420a26e8015e53e9b765ca7d5e601791
scope: workflow publish step only; no R127 scientific result changes
workflow_blob: 4b22f653dc7516bb31ead23e45dcf7f62261d79d
status: VERIFIED_LOCAL_GIT_COUNTEREXAMPLE; PRODUCTION_RERUN_NOT_EXECUTED
evidence_grade: engineering validation only; E1/E2/E3 increment zero

## 来源与精确缺口

现有 `.github/workflows/r127-van-huyck-1990-coordination-source-table-60-tests.yml` 在生成收据后无条件执行 `git add <receipt>`、`git commit -m ...`、`git pull --rebase origin main` 和 `git push origin HEAD:main`。当收据文件已经存在且字节相同，`git commit` 返回非零，Shell `set -euo pipefail` 导致 publish step 失败。这属于重复运行时的发布幂等性缺口；与已归档的 assert 优化模式及 trailing OK 检查器问题分开去重。

## 可执行负控及结果

在隔离临时目录运行（未触碰真实仓库）：

```bash
d=$(mktemp -d)
cd "$d"
git init -q
git config user.email audit@example.org
git config user.name audit
printf 'fixed\n' > receipt.json
git add receipt.json
git commit -qm initial
git add receipt.json
git commit -m 'results receipt replay'
printf 'exit=%s\n' "$?"
```

本轮实际运行结果：`exit=1`，Git提示 `nothing added to commit`。因此在完全相同的收据重放情况下，当前发布步骤无法自然返回成功。实际生产重复执行还可能受运行时间、并发主线提交及结果字段影响，本轮未重跑Actions，不能断言历史生产作业曾因此失败。

## 影响和交接

分类为P2工程可靠性问题，优先级低于R127已确认的两个P0候选验收检查器缺陷。建议R主线在修复工作流时使用 `git diff --cached --quiet` 判断收据是否改变；无变化时明确记录 no-op success，有变化时正常提交。应保留 `git pull --rebase` 的并发冲突失败语义，并在发布前检查源提交身份。不得以无变化成功替代科学证据验收。

本轮正式关闭itemwise 0；R127仍为CLOSED_BOUNDED，05-003继续待核。CI NOT_RUN；未使用新增付费服务；账户账单未核验。冻结协议未变。
