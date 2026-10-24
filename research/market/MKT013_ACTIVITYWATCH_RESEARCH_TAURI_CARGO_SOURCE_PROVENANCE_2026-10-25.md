# MKT013 ActivityWatch Research Edition Tauri 构建依赖来源与隐私补丁覆盖审计

run_date: 2026-10-25（UTC+08）
track: commercial_market
subflow: product
status: COMPLETE_BOUNDED_PINNED_SOURCE_AND_BUILD_GRAPH_AUDIT
observed_main_head_before_write: 2f3ac610e4513a74f8e42f08ecfe4dcdd27324a6
preflight: 已读 main、market MKT001 至 MKT012、E002、F001、R131 最新协议和研究报告、当日 data_scout 与 original239 v7.8。写前再次检查 HEAD、market、operations、privacy_safety；目标路径未存在。
scope: 仅英文公开官方文档、上游固定 tag 的源码、Cargo 官方规范和本项目 GitHub 只读记录。没有下载或运行发行二进制、安装软件、执行 CI、使用真实用户数据或付费服务。

## 1. 本轮真实新增机制发现

### MKT013-F1：Tauri 嵌入服务器来自 Git 依赖，来源与本地研究补丁是两条不同路径

固定发行 tag 为 ActivityWatch/activitywatch `v0.14.0b5-research`，官方发布于 2026-09-09 12:21:58 UTC，指向提交 `ac70c60f8caaa0634641836669ee9f04e6ff5036`。该 release 的资产清单包含 Windows、macOS、Linux 的 Tauri Research Edition 发行文件；仅证明发行资产存在。

固定 `ActivityWatch/aw-tauri` 子模块 `924150c5923bdf1d35a83f4ef3fa23be6f2924a6` 中：
1. `src-tauri/src/lib.rs` 明确导入 `aw_server`，并调用 `aw_server::endpoints::ServerState` 和 `aw_server::config::create_config`，说明 Tauri 服务器接口来自编译进应用的 Rust crate。
2. `src-tauri/Cargo.toml` 把 `aw-server`、`aw-datastore` 声明为 `https://github.com/ActivityWatch/aw-server-rust.git` 的 `branch=master` Git 依赖，没有在此清单中声明指向顶层 `aw-server-rust/` 的本地 path 依赖或 `[patch]` 替换。
3. `src-tauri/Cargo.lock` 对 `aw-server`、`aw-datastore` 等锁定 Git 修订 `d2e7b803d6d788e461c38da45ce19feaca9513ff`。该固定原始 Rust `export.rs` 未含 Research Edition 的 `RESEARCH_EDITION_EXPORT_SANITIZE` 插入标志。

Cargo 官方文档明确 Git 依赖按远程仓库解析，并将选定修订锁定于 `Cargo.lock`；要将 Git 依赖改为本地修改版，需显式配置可生效的 `[patch]` 等覆盖。单独修改旁边的 Git 子模块工作树不会自动改变另一个 Cargo 工作区的 Git 依赖。

### MKT013-F2：发布流程在本地补丁后重建 Tauri，但现有可读步骤没有闭合 crate 来源

固定 tag 的 `.github/workflows/release.yml` 在 `build-tauri` 中：
1. 先运行 `scripts/check_tauri_server.py "$VERSION_NO_V"`；
2. Research Edition 时执行 `scripts/patch_research_edition_export.py`，修改顶层 `aw-server-rust/aw-server/src/endpoints` 下的 Rust 源文件；
3. 执行 `make build`，在 `TAURI_BUILD=true` 时，顶层 Makefile 对 `aw-server-rust` 只执行 `aw-sync` 构建，`aw-tauri` 则执行自身 `npm run tauri build`；
4. 随后执行研究版 profile identity 补丁，并再次运行 `make --directory=aw-tauri build`。

`scripts/check_tauri_server.py` 的实际检查对象为：Tauri 锁定的 aw-server Git 修订、顶层服务器子模块 HEAD、两者的版本与发布主次版本是否一致。它没有检查 sanitizer 插入标志是否存在于 Cargo 实际编译的 crate 中。其成功输出“same revision”仅证明修订一致，不能证明未提交的本地补丁被嵌入 Tauri。

`aw-tauri/Makefile` 的构建命令是 `npm run tauri build`。本轮审读的固定 workflow、顶层 Makefile、aw-tauri Cargo.toml 与 Cargo.lock 中，未见显式将 Cargo 的 Git 依赖重定向到打过补丁的顶层工作树的步骤。

**可验证的静态结论：** 已确认 Tauri 的锁定 Git 依赖来源与 Research Edition 在顶层工作树实施的补丁来源不同；现有发布脚本的“补丁步骤成功”及“修订一致”检查均不足以证明最终 Tauri 内嵌服务器含导出 sanitizer。

**仍未验证：** 实际发行包是否存在绕过导出过滤的行为、是否有未读到的环境覆盖或 Cargo 配置、发布时的完整依赖解析、编译缓存来源、二进制符号与 REST 行为。不得将此静态审计写成已证实的安全漏洞。

### MKT013-F3：安全控制与可验证性

该产品的数据输入仍为本地窗口、浏览器和 AFK 事件，允许其他 watcher 写入额外 bucket。状态为带时间戳、时长、应用名及类别的本地事件。算法包含采集端字段过滤、分类映射、特定 JSON 导出字段拒绝规则。用户反馈为活动时间分布与导出数据；未发现人生多目标效用权重、长期情景预测校准或个体决策结果自我修正的公开实现。

权限与隐私：采集时过滤、导出时过滤、REST/CSV 读取和编译产物来源须分别验证；研究版端口与 profile 隔离不等同于每个访问路径已安全过滤。源码可审计性较高，实际发行行为和独立安全审计仍未闭合。

费用：官方免费开源版本可供阅读和未来离线合成测试。本轮未使用商业服务；未来任何测试只允许现有设备、无收费的软件与公开资料，免费额度不能确认时仅继续源码审读。

## 2. 风险登记与未来合成验收，全部 NOT_RUN

MKT013-R1 HIGH：Tauri Git 锁定依赖可能未包含 Research Edition 本地导出补丁。候选验收：固定 release tag、Cargo.lock、Cargo 实际依赖路径、构建日志与发行二进制散列，证明最终嵌入的 aw-server 具有 sanitizer。
MKT013-R2 HIGH：`check_tauri_server.py` 仅比较提交修订，可能对工作树未提交的安全补丁产生来源一致性的假阳性。候选验收：在纯合成仓库中分别构造“相同 SHA、不同工作树补丁”及“明确 Cargo path override”，检查 provenance gate 能否区分。
MKT013-R3 HIGH：JSON、CSV、REST 读取路径存在前述 MKT012 静态覆盖差异。候选验收：同一批虚构事件经不同接口读取，在 Qt 和 Tauri 研究发行物上分别验证拒绝行为。
MKT013-R4 MEDIUM：发布资产存在不代表源码补丁进入最终二进制。候选验收：官方构建证明、可复现构建或受控离线行为测试；缺少证明时保持 UNVERIFIED。

所有候选控制均为未来方法储备，不接入真实个人敏感数据，不提前开发个人决策产品，不改动 R 系列冻结协议。

## 3. E 每日治理与 F 每周专题登记

E：今日已存在 `research/operations/E002_READONLY_PROJECT_AUDIT_2026-10-25.md`，不重复生成当日审计。本轮增量只读核查 2026-10-25 后续提交：R131 在先冻结协议后新增独立吸收链精确算法、84 行数据与有界 E1 报告；原始报告明确新 JavaScript 算法仅本地执行，旧 R131 CI run `39360828291` 不能作为本次新方法的 CI 验收。新增真人 E2=0，历史 E3=0。另有 2022 年 noisy public-goods game Dryad 数据集筛选记录，官方 CSV/README 下载 HTTP 403，行级字段与独立 session 尚未验证，R073 冻结评分规则不可直接迁移。original239 v7.8 JSON 已读取，`rows.length=239`、`provisional_itemwise_audit_open_count=154`，但 `schema` 内部版本仍为 v7.6、`date` 仍为 2026-10-24，元数据漂移继续待 R 轨审阅。未进行全仓冻结协议哈希扫描，未对所有新提交逐一核验 CI；不能推断已完成科学验收。只读 E 检查，无 E 文件写入。

F：2026-W43 已存在 `research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md`，本轮不重复创建。本轮为下一周 F002 记录新风险：同一发行包内不同数据访问路径的权限一致性，以及源代码补丁与实际编译产物之间的隐私控制可追溯性。下周继续本地优先、撤销授权、衍生数据和备份删除专题；未执行 F002 或接入真实敏感数据。

## 4. 来源等级、限制、归档与下一项任务

MARKET-E1-OFFICIAL：ActivityWatch 官方发行页、固定 release 工作流、官方 Cargo 依赖规范。
MARKET-SOURCE-STATIC：固定 aw-tauri 的 Cargo.toml、Cargo.lock、lib.rs、Makefile，固定顶层 Makefile、check_tauri_server.py、导出补丁源码的直接审读。
MARKET-INFERENCE：在已读构建图中缺少本地依赖重定向，推断补丁可能未进入 Tauri 内嵌服务器，属于需验证的构建风险。
MARKET-UNVERIFIED：完整发行二进制内容、Cargo 构建实际解析路径、Qt/Tauri 行为差异、真实安全影响及人生决策效果。
科研 E1/E2/E3 与市场来源等级严格分开。

归档：本报告为独立新增 market 文件，写前已检查 main HEAD、market、operations 和 privacy_safety 目录，目标路径不存在。提交后须远端回读核验 SHA。未修改其他轨文件、冻结协议或索引。
费用：仅公开免费 GitHub 连接器与 Cargo 官方文档，无新增购买、订阅、计费 API、CI、服务器、GPU 或敏感数据接入。主动新增费用 0，账户实际账单及 GitHub 免费额度未独立核验。
next_action: MKT014 优先查找研究版 tag 对应的公开构建日志或可复现来源证明，无法获得时转向 Open Humans 的个人数据授权与撤销机制。E 后续检查 R131 新 CI 声称及 original239 版本漂移，F 下周正式开展 F002。

## 5. 固定来源

S1 https://github.com/ActivityWatch/activitywatch/releases/tag/v0.14.0b5-research
S2 https://github.com/ActivityWatch/activitywatch/blob/v0.14.0b5-research/.github/workflows/release.yml
S3 https://github.com/ActivityWatch/activitywatch/blob/v0.14.0b5-research/scripts/patch_research_edition_export.py
S4 https://github.com/ActivityWatch/activitywatch/blob/v0.14.0b5-research/scripts/check_tauri_server.py
S5 https://github.com/ActivityWatch/activitywatch/blob/v0.14.0b5-research/Makefile
S6 https://github.com/ActivityWatch/aw-tauri/blob/924150c5923bdf1d35a83f4ef3fa23be6f2924a6/src-tauri/Cargo.toml
S7 https://github.com/ActivityWatch/aw-tauri/blob/924150c5923bdf1d35a83f4ef3fa23be6f2924a6/src-tauri/Cargo.lock
S8 https://github.com/ActivityWatch/aw-tauri/blob/924150c5923bdf1d35a83f4ef3fa23be6f2924a6/src-tauri/src/lib.rs
S9 https://github.com/ActivityWatch/aw-tauri/blob/924150c5923bdf1d35a83f4ef3fa23be6f2924a6/Makefile
S10 https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html
S11 https://doc.rust-lang.org/cargo/reference/overriding-dependencies.html
S12 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R131_INDEPENDENT_ABSORBING_CHAIN_SCIENTIFIC_REPORT_2026-10-25.md
S13 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/NOISY_PGG_2022_DRYAD_PUBLIC_HUMAN_GROUP_GAME_TRIAGE_2026-10-25.md
