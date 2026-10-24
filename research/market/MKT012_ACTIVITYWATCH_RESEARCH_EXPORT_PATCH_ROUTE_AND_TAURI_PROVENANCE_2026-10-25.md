# MKT012 ActivityWatch Research Edition 导出补丁、接口覆盖与 Tauri 构建来源审计

run_date: 2026-10-25（UTC+08）
track: commercial_market
subflow: product
status: COMPLETE_BOUNDED_PINNED_STATIC_SOURCE_AUDIT
observed_main_head_before_write: c418841e9ff2d6b24fe1bf790b8144c7bceb5304
preflight: 先读取 main、market MKT001 至 MKT011、E002、F001、本日 R130/TH015 提交、original239 v7.8 与 Actions。写前再次检查 main 和目标路径。本轮仅新增 market 独立报告。
scope: 非中文官方文档、ActivityWatch 固定 v0.14.0b5-research 发布源码、其 Git 子模块及 Tauri 锁定依赖。只读静态审查，未安装发行二进制、运行原软件、触发 CI 或使用真实用户数据。

## 1. 对 MKT011 待澄清问题的实质进展

### 1.1 找到发布流程中的研究版专用导出补丁

MKT011 直接读取的 aw-server-rust 固定子模块 d2e7b803d6d788e461c38da45ce19feaca9513ff 的 `aw-server/src/endpoints/export.rs` 没有研究版过滤。这是**未打补丁的上游子模块**，不能据此认定 Research Edition 的发行包缺少导出保护。

本轮在同一个固定发布 tag `v0.14.0b5-research`（发布于 2026-09-09）中直接发现：
1. `scripts/patch_research_edition_export.py`（blob `2f5cb35d85fb245ed48cea6a887898df64ee7350`）会复制研究版 Rust sanitizer 模块，并将调用插入总导出与单 bucket JSON 导出两个端点，缺失预期插入点时构建脚本失败。
2. `scripts/research_edition/export_sanitize.rs`（blob `803025a4d12c572aaa2148d3c5743196745b0f5d`）实现过滤与身份重写。存在单元测试，但本项目未执行测试。
3. 固定 tag 的 `.github/workflows/release.yml`（blob `1c2bbab02dcee45213aafc6f950c1e19b3861ba0`）在 Qt、manylinux Qt 和 Tauri 构建路径中均调用上述补丁脚本。Qt 路径还明确在研究版配置修改后重新构建 aw-server-rust。

**修订 MKT011 的未决项：** 研究版导出保护具有明确的发布期补丁来源；先前只读未打补丁 Rust 文件的证据不足以判断发布包的行为。此项由“未找到实现”更新为“已找到源码实现，发行物对应关系与覆盖范围仍需验证”。保留原始 MKT011 文件，不追溯改写。

### 1.2 补丁确实覆盖的接口与字段

固定 `patch_research_edition_export.py` 在两个位置插入 `sanitize_buckets_export`：
* `GET /api/0/export`，全 bucket JSON；
* `GET /api/0/buckets/<bucket_id>/export`，单 bucket JSON。

`export_sanitize.rs` 逐事件拒绝任何顶层 `data.url` 字段；仅当 bucket type 为 `currentwindow` 时，拒绝不属于固定研究类别白名单的字符串 `data.title`。若检查失败，导出端点返回 Conflict。它重写导出映射 key、bucket.id 与 bucket.hostname 为 `research-participant`，且遇到重写身份冲突时拒绝导出。固定测试包含原始 URL、未过滤标题、双主机冲突、保留应用名称和允许研究类别标题。

边界：对非 currentwindow bucket 的 `data.title` 没有同等拒绝逻辑；对 `data` 中其他字段及 bucket.data 元数据没有一般敏感字段白名单。原始应用名被明确允许。因而该 sanitizer 属于**特定字段的拒绝规则和部分主机身份重写**，不能直接推定所有事件和元数据已匿名化。

### 1.3 UI CSV 和 REST 事件读取仍属不同路径

固定 `aw-server-rust` 的 `aw-server/src/endpoints/mod.rs` 将 `/api/0/export` 与 `/api/0/buckets/<id>/export` 映射到上述可补丁的端点，同时提供 `/api/0/buckets/<id>/events` 原始事件读取路由。研究版补丁脚本只修改两个 JSON 导出端点。

由固定 aw-server-rust 子模块指向的 `aw-webui` 提交 `13a9428ef854f357bbf2aa9e09ad04ded811c000` 中，`src/views/Buckets.vue` 的“Export all buckets as JSON”按钮调用 `/0/export`，单 bucket JSON 调用 `/0/buckets/<id>/export`，CSV 导出通过 `getBucketWithEvents` 读取事件再转 CSV；该页面的这些导出方法未见研究版专用敏感字段检查。服务器事件读取路由也未见与 JSON sanitizer 相同的检查。

**新风险登记 MKT012-R1：** 研究版 JSON 导出拒绝机制不能自动外推至 UI CSV、原始事件 REST 读取或额外 watcher 的其他读取路径。需受控合成测试确定不同路径的实际数据和授权边界。此为固定源码静态可见的覆盖差异，尚未独立确认发行二进制的可观察结果，不作已证实漏洞或攻击可利用性结论。

### 1.4 Tauri 发行构建依赖存在需要独立闭合的来源差异

研究版发布页确实提供 Tauri Research Edition 的 Windows、macOS、Linux 安装资产。固定 `ActivityWatch/aw-tauri` 子模块 `924150c5923bdf1d35a83f4ef3fa23be6f2924a6` 的 `src-tauri/Cargo.toml` 将 `aw-server` 与 `aw-datastore` 声明为远程 `aw-server-rust.git` 的 git 依赖，`src-tauri/Cargo.lock` 锁定至 **未打研究版补丁的** `d2e7b803d6d788e461c38da45ce19feaca9513ff`。本轮读取的 `aw-tauri` Makefile 使用 `npm run tauri build`。发布 workflow 虽然先修改顶层 `aw-server-rust` checkout，随后构建 Tauri，现有固定文件没有显示将 Tauri 的 git 依赖切换到该本地已打补丁 checkout 的明确步骤。

**新风险登记 MKT012-R2：** Qt 与 Tauri 发行物是否都链接研究版 sanitizer 尚未闭合。需要核对 release job 中 Cargo 依赖解析日志、编译后符号或发行二进制的合成数据导出行为。源码静态差异足以提出高优先级构建来源审计问题，**尚不足以断言实际 Tauri 发行包缺失过滤**。不得用 workflow 中存在补丁步骤代替二进制验证。

### 1.5 身份验证、数据输入与功能定位

固定 Rust `apikey.rs` 与 `config.rs` 表明 API Bearer key 是可选项，默认未启用；默认监听地址为 127.0.0.1。研究版配置将默认端口改为 5667。由此可区分网络暴露、同机进程访问、watcher 写入、导出与研究参与者主动上传。无证据表明系统默认向研究方实时传输数据。

输入为窗口、浏览器及 AFK 事件，额外 watcher 可写其他 bucket；状态为本地事件、时间戳、时长、类别与应用名；算法为研究类别映射、字段剔除和 JSON 导出检查；反馈为时间分布与数据导出。该产品未公开用于人生多目标效用优化、长期预测校准或决策自我修正的机制。解释性来自公开映射与可检查的事件字段。Research Edition 是免费开源预发布研究工具；未购买商业服务、运行本地构建或启用收费资源。

## 2. 未来合成验收建议，全部 NOT_RUN

* AW-E01：同一组完全虚构的混合 bucket，在 Qt 和 Tauri 固定研究版发行物上分别请求全量 JSON、单 bucket JSON、CSV 和 events API，逐路径记录是否拒绝、字段差异及状态码。
* AW-E02：为非 currentwindow bucket 构造只含敏感 title、无 url 的事件，确认 JSON sanitizer 的覆盖边界。
* AW-E03：构造嵌套元数据、应用名、设备名和两个不同主机 bucket，验证哪些身份字段被重写以及冲突是否拒绝。
* AW-E04：核验研究版发行物编译来源，绑定 tag、workflow run、Cargo.lock、Cargo 实际解析依赖和最终二进制散列。
* AW-E05：在无真实个人数据的本地受控环境下验证 API key 开关、watcher 白名单、撤销后停止采集、已导出副本及衍生统计的删除传播。
* AW-E06：建立每种导出路径的字段级 schema 和研究许可检查，不将“JSON 导出已过滤”外推为“所有数据访问已过滤”。

这些是未来方法储备，不执行产品开发、不接入用户数据、不更改任何 R 系列冻结协议。

## 3. E 当日治理增量与 F 本周去重

E：`research/operations/E002_READONLY_PROJECT_AUDIT_2026-10-25.md` 已完成当日实质审计，本轮仅核对其后 R 主线增量。main 最新已读 HEAD 为 `c418841e9ff2d6b24fe1bf790b8144c7bceb5304`。R127/R128/R129 的冻结第三方法 CI run `40113226398` 显示 completed/success；归档报告保留 R127 原始 CSV 缺行标志的历史协议差异，R128/R129 限定 E1 已接受。R130 独立精确 resolvent run `40113779564` 显示 completed/success，Python 3.11 与 3.12 两项任务的“Frozen independent exact matrix resolvent”和“Unmodified R130 original 65 tests”步骤均 success；其 175 行、350 个数值比较仅支持项目内部有限 E1。Original239 v7.8 JSON 已直接解析，`rows.length=239`、`provisional_itemwise_audit_open_count=154`；该值相较 E002 当时的 v7.6 的 157 减少 3。v7.8 的 `schema` 字符串仍标识 v7.6、`date` 字段仍是 2026-10-24，属于待由 R 轨判断的元数据版本漂移风险；E 不改写索引。未执行全仓冻结协议字节哈希扫描，不宣称 R073/PESEN 已获本轮全仓哈希验证。无新的真人 E2、历史 E3 验证。

F：2026-W43 已存在 `F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md`，本轮不重复建立 F 文件。将“采集时过滤与导出时过滤分离”“JSON 与 CSV/REST 覆盖差异”“Tauri 与 Qt 构建来源一致性”登记为 F002 研究候选，结合本地优先、撤销授权、衍生数据和备份删除。尚无真实敏感数据或安全控制效果实验。

## 4. 证据、限制、费用和后续

MARKET-E1-OFFICIAL：ActivityWatch 官方 Research Edition、导出与安全文档，以及固定 release 元数据，支持公开功能与限制。
MARKET-SOURCE-STATIC：固定 Git tag 的构建脚本、sanitizer、测试源码、Git 子模块、aw-webui、aw-tauri Cargo.toml/Cargo.lock 及 Rust 路由已直接读取。此等级仅为源码结构和构建配置核对，**不代表独立运行验证或真实用户效果证据**。
MARKET-UNVERIFIED：发行二进制是否执行 sanitizer、Tauri Cargo 依赖实际编译来源、各导出路径实际拒绝行为、身份字段完整匿名化、真实安全风险及个人决策效果。R 科研 E1/E2/E3 与市场资料等级分开。
费用：只读 GitHub 连接器、公开免费文档，无付费 API、订阅、购买、云服务器、GPU、CI 启动或真实个人数据。主动新增费用 0；整体账单及免费额度未独立核验。
归档：仅本文件增量写入，提交后须远端核验 SHA；E/F 不改写。
next_action: MKT013 优先审查 ActivityWatch Research Edition Tauri 的 Cargo 依赖来源与实际发行构建证明；若缺少可读公开构建日志，则转向 Open Humans 的个人数据授权与撤销机制。E 下一次复核 v7.8 元数据漂移和 R130 CI 归档，F 下一周开展 F002 数据生命周期专题。

## 5. 固定来源

S1 https://docs.activitywatch.net/en/latest/research/research-edition.html
S2 https://docs.activitywatch.net/en/latest/features/exporting-data.html
S3 https://github.com/ActivityWatch/activitywatch/releases/tag/v0.14.0b5-research
S4 https://github.com/ActivityWatch/activitywatch/blob/v0.14.0b5-research/scripts/patch_research_edition_export.py
S5 https://github.com/ActivityWatch/activitywatch/blob/v0.14.0b5-research/scripts/research_edition/export_sanitize.rs
S6 https://github.com/ActivityWatch/activitywatch/blob/v0.14.0b5-research/scripts/tests/test_patch_research_edition_export.py
S7 https://github.com/ActivityWatch/activitywatch/blob/v0.14.0b5-research/.github/workflows/release.yml
S8 https://github.com/ActivityWatch/aw-server-rust/blob/d2e7b803d6d788e461c38da45ce19feaca9513ff/aw-server/src/endpoints/mod.rs
S9 https://github.com/ActivityWatch/aw-server-rust/blob/d2e7b803d6d788e461c38da45ce19feaca9513ff/aw-server/src/endpoints/bucket.rs
S10 https://github.com/ActivityWatch/aw-webui/blob/13a9428ef854f357bbf2aa9e09ad04ded811c000/src/views/Buckets.vue
S11 https://github.com/ActivityWatch/aw-webui/blob/13a9428ef854f357bbf2aa9e09ad04ded811c000/src/stores/buckets.ts
S12 https://github.com/ActivityWatch/aw-tauri/blob/924150c5923bdf1d35a83f4ef3fa23be6f2924a6/src-tauri/Cargo.toml
S13 https://github.com/ActivityWatch/aw-tauri/blob/924150c5923bdf1d35a83f4ef3fa23be6f2924a6/src-tauri/Cargo.lock
S14 https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40113779564
S15 https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40113226398
