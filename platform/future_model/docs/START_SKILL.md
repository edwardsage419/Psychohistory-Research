# Codex Cloud 安装与启动规程

适用于现有 `Psychohistory-Platform` 环境及通过该环境启动的任务。仓库为 `edwardsage419/Psychohistory-Research`，代码工作目录为 `platform/future_model/`。从任务指定的已推送版本工作；未指定时以可核实的 `main` 为准备基线。启动前阅读根目录 [AGENTS.md](../../../AGENTS.md) 和 [项目规程 v3.2](../../../docs/PROJECT_WORKFLOW_REQUIREMENTS_V3_2_2026-11-25.md)。自主认知与长期个人决策系统是主线，本规程用于环境准备和任务恢复。

## v3.2 环境边界

保持现有环境名称、仓库、共享范围与普通工程工具链。取消Qwen/Ollama及其他第三方AI推理、预训练权重下载、微调和专项评价；不配置相关模型服务地址或密钥，不将其作为安装、启动、测试或验收前提。历史资产按原版本保留；不在环境准备阶段删除代码或修改历史结果。自主引擎未完成的能力如实标记，不自动调用外部模型降级。保留Python 3.12、Node.js 24 LTS、npm、Git及锁定依赖，不因长期方向改变而擅自更换已验证的工具链。

云端设置页面的修改需要实际有权访问；本仓库文件更新仅改变检出后的启动规程，不证明云端保存或发布配置已经改变。设置页应检查是否有旧模型安装步骤、模型环境变量或服务配置，仅移除经确认的旧模型专用设置，保留无关环境变量和密钥。安装网络仅允许所需免费包仓库及现有授权来源；运行验证默认断开外部网络，确需公开证据获取时按任务最小授权执行。不得新增费用、扩大共享或权限。自主运行测试须记录真实退出状态；下述脚本是现有基线回归，尚不证明完整自主语言能力。云端Linux验收与Mac/iPhone真机验收分别报告。

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
