# R272 P0：只读审计 CI 的来源触发覆盖、Actions 固定身份与主分支保护准入

日期：2026-11-17 UTC。继续 R272 original239/12-002 的既有 PR #51，针对生产准入的可验证工程约束作增量审计。**冻结 R272 科学结果、原三 job 验收历史、原生产工作流和 main 设置均未修改。**

## 1. 当前可证实的 GitHub 状态

本轮开始 `main` 为 `073496bed7b0e1ab0bafef7739fc02f8a4a004c4`。从 GitHub REST 读取：

* 仓库 `edwardsage419/Psychohistory-Research` 是公开仓库，default branch `main`。
* `GET /branches/main` 返回 `protected:false`。
* `GET /rulesets` 返回空数组。
* 原生产工作流 `.github/workflows/r272-exact-train-test-oos-e1.yml` 的 Git blob 为 `3132b08cf4ee64b55f5112d2249894ea0ec9d42d`，其仍使用优化可跳过的 Python assert、先 --emit 后检查、`contents:write` 与自动推送 `main` 的旧流程。没有更新该文件。
* PR #51 是 `Draft`、可合并状态 `clean`，但上述旧生产风险未因此闭合。

GitHub 官方文档确认 GitHub Free 公共仓库可免费启用分支保护及必要状态检查。文档：https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches 。本轮**没有更改** GitHub 分支保护，亦未访问账户实际账单。

## 2. 发现的额外 CI 触发缺口

上一版仅在审计工作流自身或新增第三来源复算文件变更时触发。旧原生 R272 模型、冻结协议、归档 CSV/JSON、机器收据、旧 wrapper/negative suite、隔离 v2 等源文件改变时，若该次提交没有同时改工作流或第三来源文件，GitHub 可跳过此审计运行。

在未强制状态检查时，这意味着某些修改无法取得对应的 R272 最新审计结果。将这一类路径过滤工作流直接指定为**全仓库必需状态检查**则会产生另一个问题：GitHub 官方文档明确说明，若 PR 因路径过滤而不启动 workflow，其所需状态检查将保持 `Pending`，可以阻塞与 R272 无关的研究 PR。原文：https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax 及 https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks 。

因此，当前版本即使补全路径，仍应保持为**限定范围只读审计工具**。必须在另一个 owner 批准的独立全仓库保护方案准备好之前，避免将其路径过滤 jobs 直接列为 main 的全局必需项。

## 3. 本轮真正实施的补丁

只改同一 PR #51 的 `.github/workflows/r272-full-checkout-unadopted-candidate-20261117.yml`，前次 Git blob `7e8186bcf2499c49a50abccfab66e802102d38d4`，新 Git blob `70931c3b3bd8c1eb66967ae51308d8350af0b63c`。

* `push.paths` 和 `pull_request.paths` 各有**完全相同的 13 个实际受审文件路径**：包括审计工作流本身、旧生产 workflow、旧单入口、wrapper、负向套件、归档 checker ZIP、隔离 v2、独立第三来源、原科研生成器、旧来源 CSV/结果 JSON/收据和冻结协议。逐项远端回读确认。
* 将三个 `actions/checkout` 从可移动 `v4` 换成固定 Git 提交 `34e114876b0b11c390a56381ad16ebd13914f8d5`（当时 GitHub tag `v4.3.1` 的 commit）；三个 `actions/setup-python` 固定为 `a26af69be951a213d495a4c3e4e4022e16d87065`（当时 `v5.6.0` 的 commit）。上述 SHA 均实际由 GitHub 官方仓库 tags API 查询，而非推测。
* 安全回归 job 末尾新增原正式 R272 生产工作流的完整 Git blob SHA1 检查，要求精确等于 `3132b08cf4ee64b55f5112d2249894ea0ec9d42d`。任何对这份旧生产入口的改动都令**该审计候选**失效并要求重新审议，禁止无声把科学验收已通过等同于生产接入已获授权。
* 保留 `permissions: contents: read` 和 `persist-credentials: false`，未启动新付费服务，未给真实 production 凭证新增写权限。

## 4. 实际 GitHub CI

原生 run：https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44043516100

* Run `44043516100`，workflow 触发提交 `72c67d846e7bee8f15f14e5a9f877d7bc71031fd`，`completed / success`。
* GitHub 原生实际 job `133903524212`，Python 3.11 完整冻结数学及隔离 v2，success。
* Job `133903524648`，Python 3.12 完整冻结数学及隔离 v2，success。
* Job `133903978212`，独立第三来源 576 条冻结人工记录、九世界及三种优化模式、有害来源拒绝，success。
* Job `133903524832`，导入路径旧候选假 PASS 复现、v2 阻断、旧生产工作流身份锁定，success。

GitHub 日志另核验：

```
R272_LEGACY_PRODUCTION_IDENTITY_UNCHANGED
R272_UNPINNED_SIBLING_IMPORTS_CAUSE_FULL_FALSE_ACCEPTANCE
R272_QUARANTINED_V2_BLOCKS_TWO_MODULE_INJECTION
R272_QUARANTINED_V2_REAL_CHECKOUT_3_MODES_PASS
R272_FROZEN_THIRD_SOURCE_576_ROWS_9_WORLDS_PASS
R272_THIRD_SOURCE_ALL_THREE_PYTHON_MODES_IDENTICAL
R272_FROZEN_THIRD_SOURCE_SHA256_NEGATIVE_REJECTED
```

这里的三个科学 job 与一个安全 job 都在**只读工程审计 workflow**中完成。它们不能自动替代 2026-10-23 原冻结协议要求的历史科研验收工作流及其证据身份。

## 5. 可供 owner 另行选择的零新增订阅生产方案

生产迁移包含两项彼此独立、尚未获批的决定。

**A. GitHub 主分支权限治理（未执行）**

公开仓库 GitHub Free 支持基本分支保护。若采用，`main` 应要求经 PR 合并、禁止强制推送及删除，并要求一个**不受路径过滤跳过影响**的稳定唯一状态检查。实际启用、规则例外和管理员 bypass 权限由 owner 决定。

**B. R272 安全科研校验生产迁移（未执行）**

把现有只读隔离 v2 和第三来源审计整合为冻结要求的 3 项科研 job，加安全回归。先在独立候选上测试对真实 R272 改动会运行完整复验，对其他学科文档变动正常放行的策略。为避免一次 unrelated theory PR 重跑六组数学研究，可设计一个不设路径过滤的**轻量必需汇总 job**：其总是产生明确结果，仅在确实涉及 R272 源身份或工作流的 PR 中请求完整科研校验；依赖 job 失败、取消或未运行时必须显式给出拒绝，不能因 `skipped` 被误判为成功。现有已审计 workflow 可以继续保持路径限定、非必需。整个迁移需要保证冻结协议原三项 CI job 验收语义且不重写历史收据。

这一方案只是工程设计候选。没有新增、启用任何新全仓库持续 CI 任务；没有触发私有/计费 runner。创建 GitHub required checks 或修改工作流生产写权限仍需要 owner 明确授权。

## 6. 科研状态

`COMPLETE_BOUNDED_ENGINEERING`：13路径覆盖、六个固定 action SHA、旧生产字节门槛、原生四 job 真实 success 及第三来源严格复验。

`OPEN_PRODUCTION_ADMISSION`：`main` 未设置分支保护、正式旧生产 workflow 未替换、required status 设计尚未部署、生产实际写权限及并发审计未运行。

`UNCHANGED`：R272 原 E1 受限科研结题、原 P0/12-002 待核、R073、PESEN v0.1、原154项待核队列及所有冻结协议。新增真人 E2=0，历史 E3=0，外部科学团队独立复现=NOT_RUN。新增计费服务=0，账户账单未读。
