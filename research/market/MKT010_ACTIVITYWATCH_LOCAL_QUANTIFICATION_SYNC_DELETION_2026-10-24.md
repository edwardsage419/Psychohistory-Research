# MKT010 ActivityWatch 本地量化、跨设备同步与删除传播机制审查

run_date: 2026-10-24（Asia/Shanghai）
track: commercial_market
subflow: product
status: COMPLETE_BOUNDED_PRIMARY_DOCUMENT_REVIEW
observed_head_before_write: 6431ae1d07877553c8fd7882c2b49aaed870e176
preflight: 读取 main HEAD、market MKT001 至 MKT009 目录、MKT009 正文、E001、F001、工作流规范、R127 追加独立审计、R128 新报告和 original239 v7.6；写前确认本路径不存在。仅查看非中文官方页面、上游 GitHub release 和已有研究档案。未安装产品、接入个人活动数据、执行付费服务或触发 CI。

## 1. 本轮可证实的产品增量

### 1.1 发布版本与真实输入
ActivityWatch 官方于 2026-10-06 发布 v0.14.0；上游 GitHub releases/latest 的最新稳定 tag 在本轮为 v0.14.1，发布时间 2026-10-10T19:18:45Z（S1、S2）。这是上游版本记录，不代表本项目安装或运行。

数据源包括前台应用及窗口标题、浏览器标签（可选扩展）、离开键盘 AFK 观测、可扩展 watcher。公开数据模型将观测按 watcher 与主机划为 bucket，每个事件含 ISO8601 时间戳、秒数 duration 和依事件类型而定的 JSON data。浏览器事件类型可能含 URL、标题、incognito 标志；窗口事件可能含应用和标题。时间戳按 UTC 存储，原始 offset 被丢弃。心跳机制合并相邻同内容事件以减少存储和 IO（S3）。这类数据是设备活动代理变量，不能直接当作人的注意力、生产率、幸福感或人生目标达成量。

### 1.2 状态、算法与反馈
原始 bucket 事件与 canonical events 是两层不同表示。canonical 查询组合窗口和 AFK 事件、按规则分类、处理多设备事件；原始事件不自动包含 AFK 过滤或分类。分类由规则及类别层级产生，用户可修改规则、观察时间分布（S4、S5）。产品主要提供行为记录与描述性反馈；没有发现公开的长期人生效用函数、因果识别、目标最优化或真实生活改善独立预测评价。不能将设备活动小时数等同于生活质量。

### 1.3 2026-10 新增同步机制与明确的删除缺口
v0.14.0 支持 opt-in 的 aw-sync。每台设备把数据写入本机同步目录自己的子目录，跨设备文件传输由用户选用的工具承担，接收端以只读方式读取并导入为 synced-from buckets。Android 当前只推送，桌面后台默认只推送，设置后可拉取；每台设备会持有其他设备数据副本。上游官方明确说明：**删除事件不会跨设备同步，设置也不会同步，接收端本地修改可能在后续同步中丢失**（S6、S7）。因此删除源设备记录不足以证明其余设备、同步目录、第三方云盘和导出文件均已清除。

同步传输目的地由所选工具决定。使用 Dropbox/Google Drive 等云同步时，数据副本会进入相应第三方服务器；官网 FAQ 中“数据不会上传到云”的简述需要结合此可选功能限定理解。该观察是官方文档的明确边界，并非本轮发现的独立漏洞。

### 1.4 隐私、API 与加密的边界
官方 Security 文档明确承认尚无独立安全审计。默认本地 API 无身份验证，能够访问该本地服务的进程可能读取、写入或删除数据；aw-server-rust 支持可选 API key，经典 Python server 不支持。API key 不保护数据库静态文件，也不使远程明文 HTTP 服务自动安全。SQLCipher 静态加密仅在自行编译并开启 Cargo encryption 特性时可用，普通发行包不包含该功能（S8）。v0.14.0 发布说明称可在入库前过滤敏感窗口标题，并限制 Firefox 扩展可访问的 API 端点；文档中旧的 Filtering data 页面仍将总体过滤功能标记为 planned，存在文档版本口径差异，后续应核实具体过滤规则与覆盖 watcher（S1、S8、S9）。

### 1.5 导出、AI 边界、费用
官方 Raw Data 页面允许按 bucket 或全部 JSON 导出，REST API 也有 export 路径。官方建议 AI 使用前先在本地按类别、应用及有限时间范围聚合，删减窗口标题、完整 URL、文件名等字段，检查实际发送内容；不能直接把原始事件历史默认交给外部模型（S10、S11）。Research Edition 文档描述预入库丢弃浏览器 URL 和窗口标题的专门研究构建，但该承诺只覆盖其指定 window watcher，额外 watcher 可重新引入敏感数据，桌面构建仍为 prerelease（S12）。

官网声明免费、开源、MPL-2.0、无强制付费档位；可以选择第三方同步工具，其费用及隐私政策需独立评估。本轮未注册、安装或使用任何同步服务（S13）。

## 2. 与 Exist 的可核查对照及候选方法

Exist 侧重汇集日级个人属性并计算跨属性相关性，缺失值处理与相关检验在 MKT003 中已登记。ActivityWatch 侧重秒级设备事件、可复核的 AFK 过滤、规则分类和本地原始数据导出。两者输入粒度与数据语义不同。候选研究问题是：以匿名合成设备事件为输入，分别输出原始观察、经过 AFK 过滤的类别时间、日级汇总和带缺失标志的统计序列，并对每层保留变换版本与来源。任何相关关系仍需独立样本外预测检验，不能从活动时长推断因果。

建议未来合成验证矩阵，均 NOT_RUN：
1. AW01：跨午夜、跨时区与 UTC offset 丢弃后，日级汇总是否稳定且有明确本地时区政策。
2. AW02：AFK 与窗口事件交叉时，原始累计时长与 canonical 活动时长是否被正确区分。
3. AW03：重复心跳与重叠设备时间，是否重复计时；多设备合并策略需明示。
4. AW04：删除源设备事件后，远端镜像与导出副本是否继续可读；未同步删除应触发风险告警而非“已彻底删除”。
5. AW05：第三方云同步、未认证本地 API、数据库明文与可选 SQLCipher 构建分别做威胁边界测试。
6. AW06：过滤前后的敏感窗口标题、URL 与其他 watcher 事件是否泄露，特别检查 Research Edition 额外 watcher 情形。
7. AW07：聚合后的 AI 输入仅含许可字段，并记录被发送 payload、用途、授权版本及撤销状态。

## 3. E 当日治理增量（只读）
E001（2026-10-24）已经完成实质每日审计，故本轮未重复新建 E 报告。最新 main 初始 HEAD 为 6431ae1d07877553c8fd7882c2b49aaed870e176；最近理论 TH013 已索引，R128 新增冻结协议、42 例精确构造数据、独立脚本与有界报告。直接读取 R128 报告，其状态为 BOUNDED_INTERNAL_E1_COMPUTATION_PASS / NEW_CI_NOT_VERIFIED / NO_GLOBAL_QUEUE_DECREMENT，不能标为真人 E2 或历史 E3。

直接读取 original239 v7.6 JSON：total_original_models=239，provisional_itemwise_audit_open_count=157。R127 后续独立 JavaScript 审计发现冻结协议要求逐行 exact comparison flag，而已归档 CSV 表头缺该字段，记为 PROTOCOL_ARCHIVE_NONCONFORMANCE。该审计文档因 commit-run 查询返回空列表而标 CI_VERIFICATION_PENDING。**本轮使用不同的 GitHub REST 直接查询，核实 R127 run 40099180033，head_sha=d58f71bceacc08fba2ae8b0ce478dc51e54900e3，completed/success，两个 Python 3.11 与 3.12 job 均 success，独立 payoff/tamper 和原有60项测试步骤均显示 success。** 这更新了 CI 可核验状态，不能消除 CSV 归档与冻结协议不符，也不能自动批准 R127 科研验收或将 157 减一。未重新运行原始代码或逐行复算 CI 日志，未对所有冻结文件做哈希巡检。

已知 README 导航滞后及跨轨同步风险继续 OPEN。没有改动 R、TH、A/B、C/D、original239 或冻结协议。费用方面未触发任何 CI，不能由历史 CI 状态推断账户账单。

## 4. F 本周专题状态
F001（2026-W43）已在 research/privacy_safety/ 归档，本轮避免重复。F002 候选问题得到明确上游案例：ActivityWatch v0.14.0 的事件删除不传播；同步工具可能在第三方云保留副本；未认证本地 API 和普通发行包未启用静态加密；Research Edition 只过滤特定 watcher。建议下周 F002 将授权撤回、原始记录删除、派生统计失效、同步副本清理、历史备份清理与 AI payload 撤销分别建模。没有实际接入真实个人数据或提前开发产品。

## 5. 证据等级与执行记录
evidence_scope:
* MARKET-E1-OFFICIAL: 官方 release、同步、数据模型、导出、安全、Research Edition 文档，可支持上游宣称和已公开限制。
* MARKET-E2-REPOSITORY-METADATA: GitHub 官方 v0.14.1 release tag 和日期已通过连接器直接查询；未审计发布构建或复现源码。
* MARKET-NOT-VERIFIED: 跨设备删除实测、隐私过滤实际覆盖率、性能、因果/决策效果、第三方独立安全审计均无本轮实证。
* R 科研 E1/E2/E3 与 MARKET 证据完全分离。

source_links:
S1 https://activitywatch.net/blog/activitywatch-v0-14-0/
S2 https://github.com/ActivityWatch/activitywatch/releases/tag/v0.14.1
S3 https://docs.activitywatch.net/en/latest/buckets-and-events.html
S4 https://docs.activitywatch.net/en/latest/examples/working-with-data.html
S5 https://docs.activitywatch.net/en/latest/features/categorization.html
S6 https://docs.activitywatch.net/en/latest/syncing.html
S7 https://activitywatch.net/blog/syncing-your-activitywatch-devices/
S8 https://docs.activitywatch.net/en/latest/security.html
S9 https://docs.activitywatch.net/en/latest/features/filtering-data.html
S10 https://docs.activitywatch.net/en/latest/features/exporting-data.html
S11 https://docs.activitywatch.net/en/latest/examples/agents-and-ai.html
S12 https://docs.activitywatch.net/en/latest/research/research-edition.html
S13 https://activitywatch.net/
E1 https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40099180033
E2 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R127_JS_INDEPENDENT_CSV_REPLAY_AND_PROTOCOL_GAP_2026-10-24.md
E3 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R128_FRECHET_JOINT_BOUNDS_SCIENTIFIC_REPORT_2026-10-24.md

work_performed: 实读上游 2026-10 发布说明、同步设计、数据模型、API/安全、导出、AI 使用、Research Edition，核实最新稳定 release tag；形成 7 项未执行的合成验收测试；完成 E/F 去重与 R127 CI 状态补充核验。
output_paths: research/market/MKT010_ACTIVITYWATCH_LOCAL_QUANTIFICATION_SYNC_DELETION_2026-10-24.md
commit_sha: 以 GitHub 实际提交及回读为准，文件内不预填。
ci_status: 本轮 NOT_RUN；只读核实既有 R127 CI run。
billing_checked: 无购买、无注册、无新增订阅、无付费 API、无云算力、无主动 CI，主动新增费用 0；账户整体账单和免费 CI 余额未独立读取。
blockers: 未运行 ActivityWatch、未取得跨设备实验、未核验发布构建的加密与过滤行为；E/F 继续作为现有定时任务的独立子职能，不声称拥有独立调度器。
next_action: MKT011 优先审查 ActivityWatch Research Edition 预入库数据最小化的源码/发布版本证据与额外 watcher 绕过边界，或者对照 Open Humans 的数据授权与撤销机制。E 次日核查 R127 归档协议缺口是否被正式解决，R128 是否出现可验证 CI；F 下周研究跨设备删除与衍生数据撤销。R 系列先完成，再统一分类，最后模型熔炼。
