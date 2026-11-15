# 自动持久化与灾难恢复（Gate 11）

## 三种状态不可混淆

1. 代码提交后必须 push 独立工程分支，并用 `git ls-remote origin refs/heads/feat/psychohistory-platform-v0.1` 与 `git rev-parse HEAD` 核对完整 SHA。不得以本地 commit 代替远端保存成功。
2. 已发布 Codex 环境恢复基础依赖，不保证上一次任务的进程、SQLite、未提交文件或临时目录存在。新任务按 GitHub 实际 SHA 检出，再执行版本化安装器和测试。
3. SQLite 与内容寻址文件通过一致性备份恢复；它们不是 GitHub 中的长期敏感数据库。只允许公开的合成产物可以单独入 Git。受限/大型资料的外部安全持久化未获授权，状态 BLOCKED。

## 一致性备份

先结束活动任务并停止 Web。使用新目录名（绝不覆盖旧备份）：

```bash
bash scripts/run.sh --data /workspace/psychohistory-data backup /workspace/psychohistory-backup-001
bash scripts/run.sh --data /workspace/psychohistory-restored restore /workspace/psychohistory-backup-001
```

`sqlite3.Connection.backup` 生成一致数据库；全部对象、审计日志和 SHA-256 清单一起保存。恢复按 256 KiB 块流式复制，不把整个档案载入内存；逐文件核验清单、对象身份、SQLite integrity_check、schema_version 和运行产物引用，然后从暂存目录原子迁移到**全新**数据根。令牌、staging、锁文件不进入备份。哈希可检测意外损坏；对能同时篡改清单和数据的恶意写入者，不宣称提供数字签名级身份认证。

恢复后生成新令牌。回滚时切换到恢复的新根，保留旧根及其全部失败/取消日志；恢复不覆盖现有数据根，不抹去真实失败。

## 从远端全新重建

`examples/synthetic-result.json` 是 seed=123、6 轮、16 人、delta=0.2 的合成科研载荷，不含令牌或私人数据。运行：

```bash
python scripts/disaster_recovery.py \
  --expected-sha FULL_REMOTE_SHA \
  --work-dir /tmp/psychohistory-new-recovery \
  --report /tmp/psychohistory-recovery-receipt.json
```

目录必须不存在。工具从 GitHub 浅克隆工程分支，核验 SHA，新建 venv、按 Python 锁安装、npm ci 与构建、完整测试，运行实验并与提交样例逐字段比较，再备份 SQLite/产物、恢复到新根并重取同一运行结果。实际命令、退出码、错误和日志哈希均保留。命令失败不会生成 PASS；失败的工作目录保留用于诊断。

## 额度中断时

只提交作用域内已经检查、可公开的代码/配置/文档/合成产物，推送并核验 SHA，记录尚未完成的门槛和失败。不得上传 token、数据库、私人/限制数据或虚构成功。额度恢复后读取最新远端分支、reports/PROGRESS.md 和真实失败记录继续，不重新启动研究队列。
