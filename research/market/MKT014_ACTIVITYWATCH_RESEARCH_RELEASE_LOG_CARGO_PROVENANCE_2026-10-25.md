# MKT014 ActivityWatch Research Edition 公开发行日志与 Tauri 依赖来源实证审读

run_date: 2026-10-25（UTC+08）
track: commercial_market
subflow: product
status: COMPLETE_BOUNDED_PUBLIC_RELEASE_LOG_AUDIT
prewrite_main_head: 45b7aa40c5ff5c716e9c438f6b11974bba0d9468
scope: 公开非中文官方 GitHub 发布元数据、既有 GitHub Actions 历史运行日志、固定源码和项目研究记录。未下载或执行二进制、未触发新 CI、未使用真实个人数据、未新增费用。

## 1. 相对 MKT013 的真实增量

MKT013 已静态确认 Research Edition 顶层本地 Rust 工作树补丁与 aw-tauri Cargo Git 依赖来源分离，但当时缺少实际构建日志。本轮找到上游固定 tag `v0.14.0b5-research`（顶层提交 `ac70c60f8caaa0634641836669ee9f04e6ff5036`）的公开 Release workflow run `34330645727`。该 run 于 2026-09-09 执行，状态 `completed/success`，`run_attempt=3`；Linux Tauri 构建 job `102436937495` 为 `success`。只读取历史日志，没有启动工作流。

**MKT014-F1，直接日志证据：同一 Linux Tauri 构建 job 出现两套 aw-server 来源。**

1. 08:57:29 UTC：日志显示执行 `python3 scripts/patch_research_edition_export.py`，并输出 `Patched Research Edition export sanitizer under /home/runner/work/activitywatch/activitywatch/aw-server-rust`。这证明本地工作树补丁步骤执行并报告成功。
2. 09:02:16 UTC：本地构建输出 `Compiling aw-server v0.14.0-beta.5-research (/home/runner/work/activitywatch/activitywatch/aw-server-rust/aw-server)`。该日志发生于顶层 Rust 工作区构建阶段。
3. 09:04:51 UTC：Tauri 构建输出 `Updating git repository https://github.com/ActivityWatch/aw-server-rust.git`。
4. 09:08:52 UTC：Tauri 依赖编译输出 `Compiling aw-server v0.14.0 (https://github.com/ActivityWatch/aw-server-rust.git?branch=master#d2e7b803)`。该路径是远端固定 Git 修订，与本地研究版 `v0.14.0-beta.5-research` 构建来源不同。
5. 09:19:59 UTC：研究版 profile identity 补丁后再次执行 `make --directory=aw-tauri build`；09:20:54 UTC 的 Tauri 构建完成。所审日志未显示把远端 aw-server crate 改为已补丁本地 crate 的步骤。

**有界结论：** 公开 Linux 发行构建日志已经直接确认，Tauri 编译阶段所用 `aw-server` crate 来源为远端 `#d2e7b803`，顶层研究版补丁位于另一个本地源码树。固定 `#d2e7b803` 的原始 `export.rs` 未包含研究版专用 `RESEARCH_EDITION_EXPORT_SANITIZE` 标志（MKT011 至 MKT013 固定源码审读）。因此“补丁步骤成功”与“最终 Tauri 使用已打补丁的服务器源码”不能划等号；对 Linux 这一公开构建路径，已有强于静态推断的依赖来源反证。

**仍然未验证：** 未对发布二进制进行字节或行为检查，未对真实导出 JSON、CSV、REST 路径执行测试，未独立证明某个已发布安装包存在可利用的隐私漏洞。其他平台的构建日志虽有成功步骤，未逐行做相同的依赖来源分析。不得宣称所有版本或所有平台已证实存在安全问题。

**MKT014-F2，历史 CI 与资产元数据的证据边界。**

固定 run `34330645727` 的 Linux Tauri job、研究版补丁/打包 smoke job `102436937107` 都显示 success；前者的 `Patch research edition export hostname sanitizer`、`Build`、`Rebuild aw-tauri with research defaults` 均成功。这些状态证明相应步骤执行成功，不会自动验证最终 crate 内的隐私过滤。

GitHub release `v0.14.0b5-research` 发布于 2026-09-09 12:21:58 UTC，列出 Tauri Linux x86_64 AppImage、deb、zip 等资产及 SHA256 digest。例如 Linux x86_64 AppImage digest 为 `sha256:3c8d56baf4560e52b3d020fb436f86e02b6fec05c3eb916997c2558c402686c6`。本轮只核实 GitHub 发布元数据，未下载资产计算本地 hash。资产 digest 证明可进行未来的文件身份验证，不能证明其安全行为。

## 2. 产品机制与心理史学候选方法

产品输入：窗口应用名与标题、浏览器活动、AFK、额外 watcher 的本地事件。
状态表达：时间戳、持续时间、bucket、设备及活动类别；聚合为个人时间分配。
算法：采集端分类及字段过滤、研究版导出 sanitizer 脚本、Rust 数据存储及查询；本轮重点为源码到最终构建产物的可追溯性。
目标与反馈：时间使用观察及分类反馈；未取得可验证的人生效用权重、长期多目标优化、独立决策改善或预测校准证据。
隐私权限：研究版采集端过滤、本地数据库、JSON/CSV/REST 多访问路径以及 Tauri 内嵌服务器必须分别验收。
解释性：公开源码、Cargo 锁文件、构建日志与资产 SHA256 可为来源审计提供线索，仍缺最终二进制中的补丁闭合证明。
费用：公开免费开源技术资料；未购买、部署或注册任何新服务。不得把可选商业订阅纳入项目支出。
局限：本次审读是单一固定版本的单一 Linux 构建日志及公开元数据；不推断一般软件安全性或个人决策有效性。

候选研究方法：未来任何隐私保护模块应将“源码检查、构建依赖实际解析、发行物哈希、真实接口合成行为测试”列为不同的可验证关口。只作为未来知识储备，不提前开发个人决策产品，不更改 R 冻结协议。

## 3. 待验证风险与零成本候选测试

MKT014-R1 HIGH：顶层研究版本地 sanitizer 与 Tauri 内嵌服务器 Git crate 来源不一致。未来以纯虚构事件在固定发行物上测试 JSON/CSV/REST 行为，确认各路径过滤结果。状态 NOT_RUN。
MKT014-R2 HIGH：研究版 smoke job 的 `--check` 和构建成功不能代表最终 crate 含补丁。未来检查 `cargo metadata`、编译器 dep-info 与最终二进制身份，禁止仅凭 step success 结题。状态 NOT_RUN。
MKT014-R3 MEDIUM：不同平台发行物可能采用不同构建来源。未来分别复查 Windows/macOS 日志及产物哈希。状态 NOT_RUN。
MKT014-R4 MEDIUM：额外 watcher、历史数据、CSV 与 REST 可能形成跨路径数据暴露。未来需按入口和出口分别设计合成最小化与拒绝导出测试。状态 NOT_RUN。
MKT014-R5 MEDIUM：发布 SHA256 元数据未经本地下载重算，文件身份未独立验证。状态 NOT_RUN。

## 4. E 当日治理检查，F 本周专题状态

E：今日已存在 `research/operations/E002_READONLY_PROJECT_AUDIT_2026-10-25.md`，本轮仅增量只读检查。GitHub main HEAD 在写前为 `45b7aa40c5ff5c716e9c438f6b11974bba0d9468`；其后近期可见 TH017 索引顺序补充、R131/R132/R133 有限数学 CI 研究。直接读取 R133 增量报告、Actions run `40122771095` 及 job `120957709958` 的日志，确认 job success、`checked_games=625`、`crossmodel_class_matches=625`、`R133_frozen_status_verified=true`、`R133_625_EXACT_BRIDGE_PASS`。这仅是内部合成二策略 E1 交叉方法一致性，不等于原刊独立复现、真人 E2 或历史 E3。R133 现有报告也明确未重跑原 ZIP 中的 36 项旧测试。最新 original239 v7.8 文件直接读取：`total_original_models=239`、`rows.length=239`、`provisional_itemwise_audit_open_count=154`；其 `schema` 内部字符串仍写 v7.6，`date` 仍写 2026-10-24，元数据漂移未修。未执行全仓冻结协议字节哈希审计，也未独立复算625行数学；不能声称全仓验收通过。未改写 R、TH、索引或其他轨文件。

F：2026-W43 已有 `research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md`，本轮不重复 F 专题。为下周 F002 候选增加“构建来源与最终安全控制一致性”、“撤销授权后不同导出/读取路径的权限一致性”；F002 尚未正式执行。没有接入真实个人敏感数据。

## 5. 证据等级、费用、归档与下一项研究

MARKET-E1-OFFICIAL：固定 release tag、发布资产 digest、GitHub Actions run/job 记录。
MARKET-SOURCE-EXECUTION-LOG：上游真实历史构建日志，直接打印补丁执行、本地 crate 构建及 Tauri Git crate 构建来源；强于静态源码推测，仍未验证发行物行为。
MARKET-INFERENCE：根据固定源码与日志推断 Tauri 内嵌服务器可能缺少研究版专用导出补丁。
MARKET-UNVERIFIED：真实发行物中可调用的接口行为、二进制包含的 sanitizer、跨平台覆盖、独立安全审计、长期个人决策效果。
以上 MARKET 证据标签不得混同科研 R 系列 E1/E2/E3。

本轮只读公开非中文来源，未启动 GitHub Actions 或其他 CI、未下载二进制、未使用付费 API、云算力、收费订阅、真实敏感数据。主动新增费用为零；账户账单及 GitHub 免费权益额度未独立核验。

preflight: 已读取 main HEAD、market 既有 MKT001 至 MKT013、operations E002、privacy_safety F001，写前重新核查 HEAD 和目标路径，目标文件不存在；仅新增 market 独立路径。提交后须回读核验 SHA，若并发冲突则停止覆盖。

next_action: MKT015 转向 Open Humans 的项目级数据授权、即时撤权、项目副本删除、备份生命周期与第三方数据处理责任，优先官方技术文档和 2019 年原始研究论文。继续维持 R 系列先完整学习，再系统归纳分类，最后模型熔炼的顺序。

## 6. 可核查来源

S1 https://github.com/ActivityWatch/activitywatch/actions/runs/34330645727
S2 https://github.com/ActivityWatch/activitywatch/actions/runs/34330645727/job/102436937495
S3 https://github.com/ActivityWatch/activitywatch/actions/runs/34330645727/job/102436937107
S4 https://github.com/ActivityWatch/activitywatch/releases/tag/v0.14.0b5-research
S5 https://github.com/ActivityWatch/activitywatch/blob/v0.14.0b5-research/scripts/patch_research_edition_export.py
S6 https://github.com/ActivityWatch/aw-tauri/blob/924150c5923bdf1d35a83f4ef3fa23be6f2924a6/src-tauri/Cargo.lock
S7 https://github.com/ActivityWatch/aw-server-rust/blob/d2e7b803d6d788e461c38da45ce19feaca9513ff/aw-server/src/endpoints/export.rs
S8 https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40122771095
S9 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R133_ESS_R132_625_CROSSMODEL_EXACT_CI_SCIENTIFIC_REPORT_2026-10-25.md
S10 https://github.com/edwardsage419/Psychohistory-Research/blob/main/docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v7.8_2026-10-25.json
