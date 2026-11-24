# Psychohistory Mobile v0.1 验收记录

截至 2026-11-21（北京时间）。开发固定起点为 v0.5 合并提交 `0e574a7c7077824bb700d5fa9c5654e39348fe79`，由 Draft PR #59 的样机 `daa3af9bc7385cd65e49db4687b1b39f47607d00` 续做。验收范围来自 [Issue #58](https://github.com/edwardsage419/Psychohistory-Research/issues/58)。真机发布门槛为 **BLOCKED**，物理 iPhone 测试为 **NOT_RUN**。

## 能力与边界

| 能力 | Mobile v0.1 范围 |
| --- | --- |
| 问题和规划 | 自由文本、候选原文片段、用户确认、按证据和可行性优先追问、合成情景、结构化编辑。确定性处理，另有完整状态 JSON 入口。 |
| C028、可比性、Pareto | 版本 `1.0.0`，区间、严格不等式、单位、有效时段、证据缺口，及当前可用方案的显示。 |
| C029、C030、C031 | 版本 `1.0.0`，点值及区间后悔、最坏效用和中点基线、精度阈值。依赖未知时外界仍保持外界。 |
| 权重敏感性及 C034 | 版本 `1.0.0`，经确认的权重边界、量尺和依赖，含阈值、见证和局限。 |
| `voi_point` | 版本 `1.0.0`，有限状态、信号、行动集合、条件性净值，以及忽略信号和完美信息基线。 |
| `timing_actions`、`timing_investigation` | 版本 `1.0.0`，有来源的时间起点、严格期限、等待及切换损失、依赖的调查时长与信号、正概率无行动时的 UNKNOWN。 |
| 四种区间信息价值方法 | `voi_oracle_bounds`、`voi_fixed_policy`、`voi_maximin`、`voi_randomized_certificate` 显示 `UNSUPPORTED`。各自继续保留 v0.5 桌面版本和候选地位。 |
| 隐私及状态 | 用户授权后可用 WebCrypto 和 IndexedDB 保持加密历史，支持删除、撤回和当前授权代次内恢复。桌面签名备份及旧样机备份无法在移动账本下验证。 |
| 外部功能 | 个人资料同步、外部检索、外部推理、行动代理、跨设备恢复、后台截止提醒、真实因果预测及个人效果研究列为未实现或未验证。 |

R073、PESEN v0.1 及其他冻结记录继续使用原科研协议。合成参照只能说明实现与约定的数学规则相符。提交的开发案例和代码审查算例都已见，独立科研留出、真实个人效果和外部科学验证均为 **NOT_RUN**。

## 工程验收证据

| Issue #58 条目 | 实测范围 | 结果 |
| --- | --- | --- |
| A · 浏览器工程复演 | Chromium 156.0.8078.79，390 px。关闭本地静态服务器后重新加载，完成虚构职业、学习投资和居住决策。核对交互图和数据表、改参重算、离线解锁与复盘。 | PASS |
| B · 跨语言数值与准入 | 25 组共享合成案例分别比较 Python 3.12、Node 24 和实际静态包内的 Chromium。逐项核查 canonical 输入摘要、严格硬约束和单位、候选集合、C029–C031、C034、信号后验与行动、调查成本反转、到期等号及近边界。 | PASS，每个 JavaScript 环境 25/25 |
| C · 授权记录 | 实际 IndexedDB 和 WebCrypto。关闭页面后解锁；未授权时不创建库；旧记录、跨标签并发写入、撤回、损坏或已失授权账本均按指定规则处理。 | PASS |
| D · 故障和隐私 | 实际 Chromium 验证被拦截的安装更新、缓存损坏、保留前版、缓存逐出和可用后的修复。口令错误、密文篡改、旧备份、撤回竞态、浏览器后退和多标签清理负例通过。合成输入未进入应用请求、URL 或控制台。 | PASS |
| E · 实体 iPhone | Safari 添加主屏幕、关闭 Mac、飞行模式冷启动并完成三类独立案例。 | **BLOCKED / NOT_RUN** |

合成的有限调查参照将全部四个信号策略独立枚举。忽略信号的立即行动基线为 `6`，有信息时为 `6.9`，成本 `0.5` 时净值为 `+0.4`，成本 `0.9` 时为零，再提高即反转。另有共同到达时长边际的三组条件分布。依赖结构不同，净值分别为 `+0.76`、`-0.50`，条件分解的独立对照为 `-0.05`。这些工程结果只涵盖声明的合成输入。比较 C030 的中点假设与区间边界时，未声明联合矩形的结论保留外界标记。C031 的严格阈值案例在 `0.75` 上有导致并列的见证。

移动端本地 `npm test` 为 **66 通过、0 失败、0 跳过**，其中有真实 Chromium 子测试。另运行独立的三个工作台浏览器流程和模型对照。固定桌面基线运行 **400 项 pytest、11 个子测试**，TypeScript/Vite、标准库核心、v0.1 至 v0.5 浏览器工作流和历史 v0.4 备份恢复通过。桌面既有 Starlette/httpx 弃用提示出现一次。

本地 WebKit 下载被研发环境的域名策略拒绝。托管验证使用公开仓库既有免费标准运行器，Ubuntu 运行 Chromium，macOS 增加 WebKit 并保留 Chromium 负向测试。按报告对应 Draft HEAD 查阅实际托管结果。 [GitHub Actions](https://github.com/edwardsage419/Psychohistory-Research/actions/workflows/psychohistory-mobile-v01.yml)

### 首轮托管失败与修复

初版 Ubuntu 的浏览器用例把浏览器的在线提示当作离线证据，托管 Chromium 仍报告在线。现直接验证回环服务器端口无法连接，并要求重载响应来自 Service Worker。初版 macOS 在通过符号链接访问临时目录时，构建入口误以为自己仅被导入，造成测试包缺失。现用真实路径识别命令行入口，符号链接复现已由失败转为通过。 [首轮运行](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44866328901)

第二轮 Ubuntu 全通过，macOS 已通过构建、测试、Python/Node 及 WebKit 数值对照。Playwright 强制切换 WebKit 网络状态后，页面重载返回浏览器内部错误。完整浏览器流程统一使用关闭真实回环端口来切断安装源，继续逐次核对重载响应的 Service Worker 来源。 [第二轮运行](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44866621879)

### 另行设计的合成浏览器复核

复核方在阅读工程和测试案例前固定了三组新输入及预期，设计文件 SHA-256 为 `d00edc89906b72308e11ad63bc0ba93c7e388062c0b8ef02e172a0736597f944`。在固定实现 `55611006b2973be11dee19283395042a5035b94b` 的 Chromium 静态包中，安装源关闭后从 Service Worker 重载。职业案例严格大于 30% 的条件在等号失败、40% 通过。学习案例修改概率使净值从 40 降到 25，基线为 30 和 20，概率依据缺失时拒绝调查计算。居住案例保持待证与拒绝分离，确认行动可用性后结果由 48 变为 54，再撤回该条件时回复 48。三组均通过，未观察到页面脚本异常。后续修改涉及构建入口和测试，移动运行时模型及界面源码相同。此记录属于会话内另行设计的工程复核，独立科研留出与真实设备门槛的状态见上文。

### 可复现命令

```sh
cd platform/mobile
npm run build
npm test
python scripts/export-contract.py --check
python scripts/verify-parity.py
MOBILE_PARITY_BROWSER=chromium python scripts/verify-parity.py
MOBILE_BROWSER=chromium node tests/workbench.browser.mjs
```

浏览器命令使用 Playwright 1.62.1，支持通过 `PLAYWRIGHT_MODULE` 指向既有工具的 `index.mjs`，通过 `CHROMIUM_BIN` 指向系统 Chromium。已安装 Playwright WebKit 时，将浏览器参数改为 `webkit`。本次静态包包括 26 个公开文件。清单 SHA-256 为 `c636d56cd69af27407b7636f758c9daab63dacdd6bf9f738290c52e787afccbb`，ZIP SHA-256 为 `f02d7925f8ef2bd2d50db960de0c46cedde34a553d138436b1cbd9734158f8cc`。发布前并行 main 已读回 `930f35c38cc820cc18d7ff4363ab92654b165529`，上游新增研究与交接记录不触及本次的移动端或桌面接口文件。

## 真机验收记录

| 项目 | 要记录的证据 | 当前状态 |
| --- | --- | --- |
| 安装 | iPhone 机型、iOS 和 Safari 版本、可信 HTTPS 来源、应用版本、主屏幕启动 | NOT_RUN |
| 冷启动 | 关闭 Mac，关闭 Wi-Fi 和蜂窝网络，从已结束进程的主屏幕图标重新启动 | NOT_RUN |
| 三类开放任务 | 事先由独立验收方提供虚构职业、学习投资和生活规划案例，执行澄清、计算、看图、改参重算及复盘 | NOT_RUN |
| 隐私及生命周期 | 杀 App 后解锁、未授权草稿、恢复拒绝、升级/回退、逐出和多标签状态 | NOT_RUN |
| 可用性 | 安全区域、横竖屏、大字体、VoiceOver 读出顺序及触控操作 | NOT_RUN |

本任务环境无可操作的物理 iPhone 和其已受信的专用安装源。Chromium 移动尺寸、浏览器断网及 macOS WebKit 都是工程证据。它们无法提供 iOS 主屏幕启动和系统存储逐出的实测结果。

## v0.6 集成增量 · Mobile v0.2

2026-11-24，在平台 v0.6 工作树取用 Draft PR #59 的 `fac395751d0429d2a3f3234672a60f2c715676ad` 移动包。保持原计算算子、v0.5 生成契约、缓存策略与加密账本。新增离线对话使用 v0.6 的摘要、待核对候选、用户确认与明确更正状态。可接受的词句和字段是桌面解释器的有限子集。

| 工程检查 | 本轮实测 |
| --- | --- |
| 静态构建与缓存 | Node 24.22.1 构建通过，公开包修订 `d4ef32fd30ec99f9e8a4fdcfe6bf59e187975123df4e9339fcb115e3c4c3969f`。构建产物在 Git 忽略范围。 |
| 移动套件 | 81 项通过、0 失败、0 跳过，含 10 项对话单测，以及真实 Chromium 中的 IndexedDB、WebCrypto、缓存原子更新和逐出恢复。 |
| 共享契约及数值 | 生成契约校验通过。25/25 Python 与 Node、25/25 Python 与 Chromium 的共享 v0.5 数值和准入案例通过。 |
| v0.6 对话语义抽查 | 6/6 合成文本的领域、方案原文和数字候选角色、指标、主体、数值、单位、原文来源与 Python 解释器一致。 |
| 离线工作台 | Chromium 156.0.8078.79 移动视口下关闭实际预览端口，由 Service Worker 冷重载。通过对话候选确认、底线修订、职业、学习与居住案例，以及重算、加密历史、观察、恢复、两标签锁定与撤回。虚构私有标记未进入请求、URL、Web Storage、备份明文或控制台。 |
| WebKit 与实体设备 | 托管 macOS 15 ARM64 的 WebKit 通过 25/25 契约用例、离线重载、加密历史、观察、恢复、两标签锁定及撤回。实体 iPhone 主屏幕冷启动、iOS VoiceOver 和用户 Mac 模型均为 NOT_RUN。当前移动包无 Mac 私有代理。 [托管复验](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/45298601033/job/138125596759) |

计算沿用共享 v0.5 输入口径。Mac 可选模型默认关闭，iPhone 需要经用户连接并授权的受支持私有桥接才能访问 Mac 服务；此移动静态包只运行设备内的离线引导与计算。私人 HTTPS 安装用于提供静态文件。真实设备与用户效果的发布门槛仍待验收。

```sh
npm run build
CHROMIUM_BIN=/usr/bin/chromium npm test
python scripts/export-contract.py --check
MOBILE_PARITY_BROWSER=chromium CHROMIUM_BIN=/usr/bin/chromium python scripts/verify-parity.py
MOBILE_BROWSER=chromium CHROMIUM_BIN=/usr/bin/chromium node tests/workbench.browser.mjs
```

通过 `PLAYWRIGHT_MODULE` 指定已安装 Playwright 的 `index.mjs`。上述服务只绑定本机回环地址。
