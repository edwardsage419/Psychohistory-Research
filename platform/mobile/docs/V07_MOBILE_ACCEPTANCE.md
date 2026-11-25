# v0.7 候选 B12 · 移动端工程验收

日期 2026-11-25。实际工作树起点为 main `6e44ecf50e9e8de0d8a3eb76766cd0d3bf44ab9c`，移动资产取自 Draft PR #61 `4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e`。执行环境为 Linux x86_64，Python 3.12.14、Node.js 24.22.1、npm 11.9.0、Chromium 156.0.8078.79 和 Playwright 1.62.1。初始默认沙箱阻止绑定回环端口，启用测试命令所需网络能力后仅在 `127.0.0.1` 运行 API 和浏览器用例。

## 跨端契约和可用范围

同一能力清单由桌面认证 API、CLI 以及移动构建公开清单提供。标识为 `psychohistory.cross-end-capabilities.v1`，平台候选版本为 `0.7.0`，移动包版本为 `0.3.0`。构建校验源 JSON、生成模块与 `package.json` 一致。移动运行时在载入时对照状态 schema、已装载方法及版本，结果分别标记平台版本、移动版本、状态版本和方法版本。 [跨端能力清单](../src/platform-capabilities.json)

| 范围 | 本轮结果 |
| --- | --- |
| 共享数据 | `DecisionStateV05` `0.5.0`。手动粘贴或读取状态 JSON 后，计算须由接收者重新确认。浏览器实测即使来源标明已确认，也进入待确认状态。实际拒绝 v0.7 状态版本和会话封装，拒绝后保留原草稿。 |
| 共享计算 | 11 个 v0.5.0 方法，方法版本均为 `1.0.0`。离线 JS 有各方法的本机实现，合成参照与原生 Python 复算。四个区间信息价值方法在手机仍为 `UNSUPPORTED`。 |
| 手机独立运行 | 离线确定性候选引导、用户确认和编辑、支持的方法计算、情景表和区间图、授权保存、复盘、加密导出和当前授权账本内恢复。第三方模型入口已标为退役。 |
| 桌面 v0.7 | 本地 API、CLI 和 Web 工作流。v0.7 会话、知识索引、长期共享资源和凭据的手机运行尚未实现。 |
| 私有数据 | 加密备份仍保有原安装与授权代次边界。Mac 辅助计算桥接、安全同步和跨端加密档案迁移未实现。 |

## 实测证据

| 检查 | 结果 |
| --- | --- |
| Node 构建、生成契约校验和套件 | PASS。构建清单及公开资源校验通过。84 项通过、0 失败、0 跳过，含真实 Chromium 测试的缓存损坏、原子更新、逐出恢复、IndexedDB、WebCrypto 和授权竞争。故意改变能力清单里的方法版本后，构建报错并保留上次发布。 |
| Python、Node、离线 Chromium 对照 | PASS。25/25 Python↔Node、25/25 Python↔离线 Chromium。逐例核对输入哈希、状态及方法版本、时点范围、方法准入和所选数值场。安装服务器关闭且回环连接被拒绝后，浏览器从 Service Worker 重载，再运行全部对照。 |
| 跨端能力接口 | PASS。真实 `decision-v07` CLI 的 `capabilities` 操作与源清单逐值一致。真实回环 API `GET /api/v7/decisions/capabilities` 匿名请求返回 401，经本机令牌认证返回 200，内容与同一清单逐值一致。 |
| Chromium 离线工作台 | PASS。390 × 844 移动视口，安装源停止后验证离线重载。虚构职业的最坏后悔值随情景编辑由 4 降到 1，学习方案由 0.3 改为 0.9 后与 0.7 的对照支配关系反转，虚构居住费用 1700 在约束上限由 1600 调到 1800 后从不通过变为通过。另验证候选确认、底线修订和严格的格式拒绝。 |
| 历史升级与隐私 | PASS。实际用 PR #61 静态包 v0.2 在浏览器中创建虚构加密记录并导出，加密记录在同源升级至 v0.3 后成功解锁，其当前代次的旧备份可恢复。候选独立测试另验证后台会话清理、复盘的未选方案保持 `NOT_OBSERVED`、跨标签锁定与撤回、旧备份拒绝。虚构私有标记未进入应用请求、URL、控制台、Web Storage 或备份明文。 |
| 实体 Mac、iPhone、分发 | **BLOCKED / NOT_RUN**。没有可操作实体设备。实际安装、主屏幕飞行模式冷启动、VoiceOver、设备间认证/撤回和分发均未执行。本轮未运行 WebKit。 |
| 独立验收与真实效果 | **NOT_RUN**。本轮使用公开开发场景和虚构数据。 |

候选静态包有 25 项公开资源，另含发布清单和 Service Worker。清单 SHA-256 为 `92879617bdcc59fa76f66357a7d68b2580aa00b12efe7af228efe9f01aeb5da6`。原版 v0.2 清单 SHA-256 为 `d4ef32fd30ec99f9e8a4fdcfe6bf59e187975123df4e9339fcb115e3c4c3969f`。跨端 JSON 的 SHA-256 为 `a130e25e92871546a63cd12662ae1dc53df8f038a3d83fe37ac8f1845fbb530e`。

## 复现

以下命令从仓库根目录运行，使用已安装的 Python 3.12 环境和现有锁文件。需要本机 Chromium 以及 Playwright，`PLAYWRIGHT_MODULE` 指向已有的 `index.mjs`，`CHROMIUM_BIN` 指向浏览器。可以省略 `MOBILE_LEGACY_DIST` 仅测试当前包。

```sh
legacy_root=$(mktemp -d)
git archive 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e platform/mobile | tar -x -C "$legacy_root"
(cd "$legacy_root/platform/mobile" && npm run build)
cd platform/mobile
npm run build
CHROMIUM_BIN=/usr/bin/chromium npm test
python scripts/export-contract.py --check
MOBILE_PARITY_BROWSER=chromium CHROMIUM_BIN=/usr/bin/chromium python scripts/verify-parity.py
MOBILE_LEGACY_DIST="$legacy_root/platform/mobile/dist" MOBILE_BROWSER=chromium \
  CHROMIUM_BIN=/usr/bin/chromium node tests/workbench.browser.mjs
```

桌面命令从仓库根目录运行，使用临时数据目录执行 `python -m psychohistory.cli --data <目录> decision-v07`，在标准输入传入 `{"operation":"capabilities","data":{}}`。回环 API 使用 `python -m psychohistory.cli --data <目录> serve --port 0` 启动，从本机 `token` 文件获取令牌。可在现有套件中逐例查看工程输入和断言。 [数学参照](../scripts/verify-parity.py) · [浏览器工作台](../tests/workbench.browser.mjs)
