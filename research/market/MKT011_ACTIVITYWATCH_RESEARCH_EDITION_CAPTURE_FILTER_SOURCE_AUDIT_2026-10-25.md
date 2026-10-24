# MKT011 ActivityWatch Research Edition 采集前过滤源码与导出边界审计

run_date: 2026-10-25（Asia/Shanghai）
track: commercial_market
subflow: product
status: COMPLETE_BOUNDED_PINNED_SOURCE_AUDIT
observed_main_head_before_write: c1c9c2ea9dc548ced1161afdb3f449c3c0d6c26e
scope: 非中文官方技术文档、2026-09 Research Edition 固定发布版源码、测试源码、发布元数据与当前主分支差异。只读审计，没有安装软件、接入个人活动数据、运行原软件或发起新 CI。
preflight: 已读取 MKT001 至 MKT010 目录、MKT010 正文、E001/E002、F001、original239 v7.6 和最近 R127/R128/R129 提交；本轮路径写前不存在。

## 1. 本轮真实新增研究增量

### 1.1 固定发布版本与源码绑定
ActivityWatch Research Edition 文档（2026-09-30 复审）将当前研究桌面构建固定为 `v0.14.0b5-research`，适用于 Windows、macOS、Linux，Android 的相同过滤尚未发布，iOS 无相应原生应用。通过 GitHub release 元数据核对该 tag 于 2026-09-09T12:21:58Z 发布，含独立 research 构建资产。此研究版为 prerelease，不能将 2026-10-10 的普通稳定版 v0.14.1 等同为 Research Edition 的验证版本。

直接读取超仓库 `ActivityWatch/activitywatch` 的固定 tag Git tree `ac70c60f8caaa0634641836669ee9f04e6ff5036`，确认：
* `aw-watcher-window` 子模块固定提交 `abd69a6b6a56a80df3d9971ca152f84fc23e7340`；
* `aw-server-rust` 子模块固定提交 `d2e7b803d6d788e461c38da45ce19feaca9513ff`。
本轮直接读取这两个固定提交中的 Python 过滤代码、测试文件和 Rust export endpoint；没有用当前 master 的新代码冒充 2026-09 的发布构建。

### 1.2 数据输入、状态表示和采集前变换
固定 `aw_watcher_window/research_filter.py`（Git blob `756ffe8a569966b4d701e781101633875b69406a`）公开 `transform(window, category_map, app_category_map)`。输入为窗口的 app、title、可选 URL 和 incognito 字段。浏览器识别采用固定名称集合及不区分大小写的完全匹配；已识别浏览器优先对 URL 进行子串类别匹配，URL 无命中时再用标题。匹配多项时最长模式优先，等长时映射先出现者优先。无匹配写 `excluded`。浏览器输出保留 app 和类别化 title，丢弃原 URL；incognito 标志仍可能保留。非浏览器默认丢弃 title 和 URL，但保留原 app 名称；若配置非空 `research_app_category_map`，则以类别替换原 app，未匹配写 `Excluded`。

固定 `aw_watcher_window/main.py`（Git blob `9d20740b0523cdd4c8aa789da10a2886070f5d23`）显示非 Swift 路径在 `client.heartbeat(..., queued=True)` 前调用 `transform_window`，研究模式下调用上述 `research_transform`。macOS Swift 路径使用单独参数传入 category maps；本轮未逐行审计 Swift 二进制构建，跨平台一致性仍待实测。源码和上游测试 `tests/test_research_filter.py`（Git blob `c6b7fa7af03fc549aaf1ef67005b8f02231a7977`）包含 URL 优先、最长匹配、标题和 URL 删除、原 app 名保留、可选 app 类别映射等测试用例。**这些是静态源码与测试断言的可见事实；本项目没有运行上游测试，也没有审计打包二进制。**

原始状态为窗口事件和 AFK 事件；研究状态为时间戳、时长、应用名或应用类别、浏览器活动类别。官方描述研究版使用本地数据库与端口 5667，与普通版端口 5600、应用标识和数据目录隔离；没有默认实时上传。研究参与者可手动导出 JSON 并自行上传给研究团队。导出前后数据字段和风险边界须分别审计。

### 1.3 可验证的隐私缺口与版本差异
A. 研究版默认保留 app 名称。软件名可能揭示工作单位、健康活动、个人身份或小众兴趣，因而“标题和 URL 被删除”不能推出整个记录匿名。可选 app 类别映射能进一步降低此类风险；配置必须由研究方提供，且类别本身仍可能具有敏感含义。

B. 浏览器名称集合为静态列表，未知或新出现的浏览器可能进入非浏览器路径，导致类别缺失。固定源码中的非浏览器路径仍丢弃 title 和 URL；该边界属于测量遗漏及潜在应用身份泄露，不能无证据断言 URL 已经泄露。

C. 过滤仅覆盖内置 `aw-watcher-window`。官方文档明确指出外加 `aw-watcher-web` 或其他 watcher 向研究端口 5667 写入时，可把原始 URL 和标题写入同一服务器及导出集合。官方建议研究参与者不要连接额外 watcher。该风险来自上游明确披露，未进行攻击或渗透测试。

D. 固定 `aw-server-rust/aw-server/src/endpoints/export.rs`（Git blob `4b7653d8bf3d5eeb98414b1c25276ff3fcf227e9`）的 `buckets_export` 实现遍历 datastore 全部 buckets，并将各 bucket 的全部事件加入导出，没有在该函数内看到针对研究模式或敏感字段的显式过滤条件。官方 Research Edition 文档同时声称研究导出遇到既有未过滤事件会拒绝执行（fail closed）。**两者在审计层面形成待澄清的保护范围问题**：可能由前端或其他层执行校验；仅凭该 Rust 函数不能认定用户界面导出一定绕过校验，也不能推定 API 层已经提供同等保护。需要固定版路由、前端、端口与端到端合成验证。不得将此项标记为已证实漏洞。

E. 当前 `aw-watcher-window` master 新增 `privacy_filter.py` 和 `main.py` 对应调用；2026-09 固定 research 子模块的 `main.py` 没有这些导入。普通版近期“自定义预入库过滤”能力与固定 Research Edition b5 的能力必须分别标注，不能把新 master 功能追溯给旧发布版。

### 1.4 目标、反馈、解释、权限与费用
此工具的直接目标是收集活动时间和研究类别统计，反馈为类别时间分布及导出数据；没有公开的长期人生效用函数、多目标权重优化、动态基准线、因果推断或长期决策自我修正机制。可解释性来自公开映射规则、最长匹配、来源 watcher 与事件时间，分类错误可通过研究方更新映射及未来新采集处理；已入库旧事件是否重分类需单独验证。

本地存储与独立端口降低了常规与研究档案混用的机会，但本地 API 的默认鉴权、第三方 watcher、外部手动上传和本地备份仍是不同的权限边界。用户或研究方需要分别控制采集、数据检查、导出、分享和删除。

官方项目基础软件免费开源，MPL-2.0；发行说明提及可选 AW Pro 赞助订阅，本研究没有使用。研究版无需另付产品费才能阅读源码或文档，部署和研究参与者运营成本未作独立评估。本项目未购买、安装、注册、租用服务器、使用计费 API 或付费 CI。

## 2. 心理史学候选方法及未来可检验合成测试（全部 NOT_RUN）

* AW-R01：固定 b5 子模块，对已知浏览器、未知浏览器、空类别映射、URL 与标题冲突、等长/最长模式进行逐字段输入输出核对。
* AW-R02：对非浏览器 app 使用原名、非空 app 类别映射、未知 app、敏感 app 名，核对入库字段及测量覆盖率变化。
* AW-R03：针对 incognito、URL 中查询参数、文件路径、应用名、类别名设计假数据，检查所有 watcher 与日志的入库前暴露边界。
* AW-R04：分别通过研究版 dashboard 导出与允许的本地 REST 导出路径，在已有未过滤旧事件、外加 watcher、混合 bucket 下核对 fail-closed 范围；此为未来受控合成验证，不运行真实参与者数据。
* AW-R05：核对独立 profile、端口 5667 与 5600、不同安装顺序、标准版与研究版共存时的读取权限和数据隔离。
* AW-R06：对相同合成事件分别统计原始秒级窗口、AFK 过滤后的类别时间和日级汇总，记录规则版本、缺失、重叠与时区处理；不把设备使用时间当作生活质量。
* AW-R07：撤销授权后分别测试采集停止、数据库残留、导出副本、历史备份、派生类别统计和 AI payload；删除完成必须逐副本证明。
* AW-R08：对研究分类器建立误分类矩阵和敏感性分析，量化 app 类别映射的隐私收益与信息损失；只用匿名合成事件。

候选控制：入库前最小化优先；按 watcher 白名单隔离数据源；导出前逐 bucket 审查；明确标记“原始字段从未保存”与“导出时才删除”；记录分类规则版本、授权范围、被撤销的派生记录；支持无法比较或拒绝评分。全部是未来方法储备，不能提前开发个人决策产品或改动 R073、PESEN v0.1 及其他冻结协议。

## 3. E 与 F 去重状态

E：本日 `research/operations/E002_READONLY_PROJECT_AUDIT_2026-10-25.md` 已完成独立实质审计，覆盖 R129 有限内部 E1 的 JS/Python 两实现归档、R127 追溯行标志补充、original239 v7.6 的 157 项待逐项审计、TH014/C002 当日归档和 README 导航问题。MKT011 仅引用，不代替 E 改写 R 索引或证据。

F：2026-W43 已有 `F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md`，本轮不重复开题。F002 候选新增“采集前过滤、导出前检查和外加 watcher 绕过”三者的可证明边界，连同撤销授权与衍生数据删除在下周研究。无真实敏感数据。

## 4. 证据分级与阻塞

* MARKET-E1-OFFICIAL：Research Edition 文档、参与者说明、2026-10 发布博客、官方安全与同步文档，支持上游明确说明的机制及限制。
* MARKET-E2-SOURCE-INSPECTION：固定 Git tag、两个子模块提交、三个过滤相关 Git blobs 和 Rust export 函数经 GitHub 连接器直接读取。此等级表示代码结构与版本绑定已核对，**不是独立运行验证，也不是 MARKET-E2 的真实用户效果验证**。按商业基线严格的 E2 定义，独立效果证据仍为 0。
* MARKET-NOT-VERIFIED：发布二进制字节对应、macOS Swift 路径行为、REST 与 UI 导出保护一致性、额外 watcher 导出时是否被拒绝、跨平台测量准确率、真实隐私风险量化和人生决策效果。
* R 科研 E1/E2/E3 与市场证据分类完全分离；无本轮新真人或历史证据。

Sources:
S1 https://docs.activitywatch.net/en/latest/research/research-edition.html
S2 https://docs.activitywatch.net/en/latest/research/participant-instructions.html
S3 https://activitywatch.net/blog/activitywatch-research-edition/
S4 https://github.com/ActivityWatch/activitywatch/releases/tag/v0.14.0b5-research
S5 https://github.com/ActivityWatch/activitywatch/tree/v0.14.0b5-research
S6 https://github.com/ActivityWatch/aw-watcher-window/blob/abd69a6b6a56a80df3d9971ca152f84fc23e7340/aw_watcher_window/research_filter.py
S7 https://github.com/ActivityWatch/aw-watcher-window/blob/abd69a6b6a56a80df3d9971ca152f84fc23e7340/aw_watcher_window/main.py
S8 https://github.com/ActivityWatch/aw-watcher-window/blob/abd69a6b6a56a80df3d9971ca152f84fc23e7340/tests/test_research_filter.py
S9 https://github.com/ActivityWatch/aw-server-rust/blob/d2e7b803d6d788e461c38da45ce19feaca9513ff/aw-server/src/endpoints/export.rs
S10 https://github.com/ActivityWatch/aw-watcher-window/blob/master/aw_watcher_window/privacy_filter.py
S11 https://docs.activitywatch.net/en/latest/security.html

work_performed: 固定发行版与两个子模块 Git tree 核验；逐文件审读 Python 分类器、调用路径、上游测试与 Rust 导出函数；登记 5 类边界和 8 项未执行合成测试；E/F 去重。
ci_status: NOT_RUN
billing_checked: 主动新增费用 0，未查整体账单或免费额度。
blockers: 尚无真实发行构建运行、上游测试本地执行、UI/REST 端到端导出核验或独立效果评价。
next_action: MKT012 优先固定 ActivityWatch Research Edition 的前端导出校验代码与 REST 路由，判定 fail-closed 实际覆盖范围；若源码访问受限则改审 Open Humans 的个人数据授权与撤销。E 次日复核 R129 CI 与 original239 口径，F 下周专题研究删除与导出边界。
