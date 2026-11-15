# Psychohistory Platform v0.1

中文科研控制台 + CLI + API，共享独立数学核心。当前仅运行两个**完全合成机制**：个体 Bernoulli 状态更新、双轮群体传播。研究目录只读登记，不能将运行或构建成功当作真实预测、因果识别或科学结题。

## 云端安装与启动

要求 Python 3.12、Node.js 24 LTS、npm、Git。Linux 已实测，GitHub 托管 macOS 15 Apple Silicon ARM64 已原生实测（53 项通过、1 项 Linux 专用跳过；浏览器 9 步和备份恢复成功），用户 M4 MacBook Air 实机仍 **NOT_RUN**；不要求个人电脑在线。所有命令从 `platform/future_model/` 执行。macOS 使用不含符号链接的规范化工作路径作为 `--data` 目录，避免直接使用经 `/var` 或 `/tmp` 符号链接的路径。详细记录见 [逐门验收](reports/ACCEPTANCE.md)。

```bash
bash scripts/install.sh
bash scripts/verify.sh
bash scripts/run.sh --data /workspace/psychohistory-data serve --port 8765
```

服务仅绑定 `127.0.0.1:8765`；Web 构建由同一服务提供。控制台令牌在 `/workspace/psychohistory-data/token`（权限 0600）。在自己的安全终端读取它并填入页面；不要把令牌粘入聊天、截图、日志或 GitHub。刷新页面后需重新输入。令牌不存于 localStorage。

页面操作：连接 → 实验工作台 → 设置种子/轮次/人口/情景参数 → 提交 → **批准合成执行** → 查看状态、日志、概率输出、双分支历史和版本。审批与证据页可登记默认 R233 真实科研收据；此举只读原文件，不执行研究代码，不修改证据等级。

用 Ctrl-C 关闭服务；会终止自己启动的 worker 并保存取消状态。不把任务 VM 当作永久服务器或永久数据库。开发前端可另开 `npm --prefix web run dev`，仅环回监听，API 同源代理至 8765；正式浏览器验收针对构建后的同源页面。

## CLI 与 API

```bash
bash scripts/run.sh --data /workspace/psychohistory-data demo --seed 123 --rounds 6 --population 16
bash scripts/run.sh --data /workspace/psychohistory-data discover research/R233/R233_FINAL_ACCEPTANCE_STATUS.json
bash scripts/run.sh --data /workspace/psychohistory-data runs
bash scripts/run.sh --data /workspace/psychohistory-data submit --seed 7
bash scripts/run.sh --data /workspace/psychohistory-data approve RUN_ID
bash scripts/run.sh --data /workspace/psychohistory-data status RUN_ID
bash scripts/run.sh --data /workspace/psychohistory-data result RUN_ID
bash scripts/run.sh --data /workspace/psychohistory-data cancel RUN_ID
```

`demo` 明确执行已批准的内置合成协议并等待结果；`submit` 保留 PENDING，需后续批准。使用 API 时传 `Authorization: Bearer <本地令牌>`，勿把带令牌的示例命令记入持久日志。

CLI 的 runs/status/result/discover 不启动调度器，可在 Web 运行时查询。submit/cancel/backup 等离线维护命令保留排他所有权且不执行邻近队列；approve/demo 只执行明确目标。Web 拥有调度器时，审批/取消应通过同源 API 或页面进行。CLI 批准后若结果为 FAILED/BLOCKED/CANCELED，返回非零退出码并保留真实结果。

控制台历史按 50 条分页，活动任务单独查询并始终可见；选中实验按 ID 独立读取，翻页不丢失结果。

API v1：`GET /health`（仅公开健康状态）、`GET /models`、`GET/POST /runs`、`GET /runs/active`、`GET /runs/{id}`、`POST /runs/{id}/approve`、`POST /runs/{id}/cancel`、`GET /runs/{id}/result`、`GET /assets`、`POST /assets/discover`，均位于 `/api/v1` 前缀。写请求为 JSON；除健康状态外全部要求令牌；无多用户账号体系。

## 验证与证据

- `bash scripts/verify.sh`：完整本工程 pytest、pip check、严格 TypeScript/Vite 构建、`python -S` 无第三方包核心运行。
- 在服务启动后运行 `python scripts/browser_check.py`：真实 Chromium 页面操作。需系统 Chromium，并在测试用 venv 执行 `python -m pip install --index-url https://pypi.org/simple -r requirements-browser.lock`；设置 `PH_TEST_DATA` 指向独立测试数据目录，勿用于个人数据。
- 本次自主审查与修复见 [PR #40 审查报告](reports/PR40_ENGINEERING_REVIEW.md)。
- [逐门验收](reports/ACCEPTANCE.md)、[进度账本](reports/PROGRESS.md)、[失败记录](reports/FAILURES.md)、[浏览器截图](reports/console.png)。以实际报告为准；未执行项目明确 NOT_RUN。

## 安装布局与持久化

`src/psychohistory/` 包含契约、插件、适配器、核心、状态、关系、科研来源、存储、调度和服务；`web/` 是可替换客户端。`requirements.lock` 锁定 Python 传递依赖，`web/package-lock.json` 锁定 npm 依赖与完整性。安装器保留 TLS 与包完整性验证，不使用付费 API、GPU 或外部数据库。

代码/文档/允许公开的小型合成样例通过独立 Git 分支持久化；SQLite/本地产物另行备份。**工作区本身不是持久性保证。** [灾难恢复说明](docs/RECOVERY.md)提供一致性备份、校验恢复、远端重建及软件回滚程序。受限或大型数据为 BLOCKED，不上传公开 GitHub。

## 科学与安全边界

R073、PESEN v0.1 及原冻结协议不变；没有全库分类、原创熔炼、真人社会预测或个人决策 App。`UNKNOWN` 保持未知，不强行转成概率；区间、模型分歧不自动平均。独立进程仅隔离受信任内置插件，**不是恶意代码安全沙箱**。

详见 [契约](docs/CONTRACTS.md)、[科学准入/安全](docs/SECURITY.md)、[版本与迁移](docs/VERSIONING.md)、[原始交接规范](docs/OWNER_SPEC.md)。当前用户任务的明确开发/分支/推送/PR授权优先于附件中历史“待批准”状态。合并、公开部署、费用调整仍需另行授权。
