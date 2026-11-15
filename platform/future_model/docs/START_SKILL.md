# 工程任务恢复入口

1. 每个 Codex Cloud 任务已隔离，不创建额外 Git worktree，除非用户明确要求。先读取当前任务授权、适用 AGENTS.md 和 reports/PROGRESS.md，检查工作区及 GitHub 真实分支 SHA，保留已有变更。
2. 基础环境 Psychohistory-Platform 提供 Python 3.12/Node 24。从仓库的明确已推送 SHA 恢复 platform/future_model，执行 `bash scripts/install.sh` 和 `bash scripts/verify.sh`，不得依赖上一任务的临时文件或 SQLite。
3. 调研阶段的环境 Start skill “不得开发/提交”已被本次明确工程授权覆盖；仍不得合并、部署、改冻协议或增费。不修改环境发布版本，不自动 Publish。
4. 数据根默认 /workspace/psychohistory-data，独立于仓库。`bash scripts/run.sh --data /workspace/psychohistory-data serve --port 8765`，只监听 127.0.0.1。令牌存数据根 token 文件，不写入 Git、日志或截图；页面内存认证。
5. 未完成任务按真实 SQLite 状态处理；历史 RUNNING 在无所属 worker 重启时记录 FAILED，不能冒充恢复执行成功。提交身份与当前代码/环境不符会 BLOCKED，需在正确版本执行或新建运行并重新批准，不重写旧身份。
6. 优先完成已有工程，不重跑研究线程。冻结 R073/PESEN 和其他协议；只读登记不是执行准入；合成结果不是科学预测或因果验证。
7. 每个合理工程检查点使用 [skip ci] 提交，仅推送独立工程分支并核验远端 SHA。受限/大型资料 BLOCKED。不能依赖任务 VM 作为唯一副本；按 docs/RECOVERY.md 备份与恢复。
8. GitHub API 需要当前运行实例允许 api.github.com。源配置草稿保存不等于当前实例已应用；以 environment_status 与实际请求为准。不要索取/打印原始 token。仍受阻则保存全部独立工作并明确标记 PR BLOCKED，不虚构 PR。

PR #40 审查后：CLI 的 runs/status/result/discover 只访问 Store，不启动调度器，可与 Web owner 并存；其他离线命令保持排他 owner。approve/demo 只执行显式目标，不调度邻近已批准任务。Web 控制台单独加载全部活动任务并提供 50 条历史分页；源代码/环境身份仍必须精确锁定。
