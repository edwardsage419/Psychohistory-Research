# Codex Cloud 安装与启动规程

适用于现有 `Psychohistory-Platform` 环境及通过该环境启动的任务。仓库为 `edwardsage419/Psychohistory-Research`，代码工作目录为 `platform/future_model/`。从任务指定的已推送版本工作；未指定时以可核实的 `main` 为准备基线。启动前阅读根目录 [AGENTS.md](../../../AGENTS.md) 和 [项目规程 v3.1](../../../docs/PROJECT_WORKFLOW_REQUIREMENTS_V3_1_2026-11-20.md)。个人决策系统是主线，本规程用于环境准备和任务恢复。

## Install script

使用 Python 3.12、Node.js 24 LTS、npm 和 Git。以下命令从仓库检出目录执行，复用现有锁文件和安装入口。

```bash
set -euo pipefail
repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root/platform/future_model"
bash scripts/install.sh
bash scripts/verify.sh
```

环境的存取与共享沿用现有授权和最小网络范围。安装只需现有开源依赖及其包仓库。仓库或 PR 操作需要 GitHub 时，按任务已有受控连接及环境域名策略处理。使用前核对当前实例的实际状态和具体请求结果。保持已有锁文件，费用、授权或依赖校验不明确时报告阻塞。

## Start skill

1. 打开任务实际检出的项目根目录，核对 Git 提交、工作区、环境和已授权任务范围。保存用户或并发改动。检出与远端版本有差异时先判断任务是在恢复还是开始新版本。
2. 核对 Python、Node 和准备好的依赖。有新鲜验证需要时在 `platform/future_model/` 执行 `bash scripts/verify.sh`，记录真实退出状态。只有任务需要界面或接口时才启动服务。预览使用独立的合成测试数据根：

   ```bash
   cd "$(git rev-parse --show-toplevel)/platform/future_model"
   bash scripts/run.sh --data /workspace/psychohistory-data serve --port 8765
   ```

   从同一实例访问 `http://127.0.0.1:8765/api/v1/health` 检查就绪，核对既有进程后再尝试启动另一个实例。保持环回监听。令牌留在数据根的 `token` 文件，避免进入 Git、聊天、日志或截图。
3. 云环境准备与共享的设置页面负责保存和发布未来任务使用的配置。发布后核对新任务的实际版本；续接任务保留自己的工作文件与运行状态。任务不以旧 VM、临时 SQLite 或未备份文件为唯一副本。需要恢复时依 [恢复规程](RECOVERY.md) 操作。
4. 历史 `RUNNING` 无所属 worker 的记录按真实状态恢复为失败。审批身份与当前代码或环境不符时保留阻塞状态，使用匹配版本或另起合规运行。CLI 的 `runs`、`status`、`result`、`discover` 可与 Web owner 并存，离线维护命令遵循现有排他规则。
5. 环境准备和启动验证使用虚构或有权公开的数据。既有合成研究模式和历史结果仅作为工程及研究资产，冻结协议和科学证据等级按原规程处理。版本开发在收到用户的明确任务后开始。
