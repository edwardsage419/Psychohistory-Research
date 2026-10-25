# MKT019 CSS v7.2.0 锁定 ACP 版本与祖先允许、子资源拒绝测试覆盖审计

date: 2026-10-25 (UTC+08)
track: commercial_market
status: COMPLETE_BOUNDED_FIXED_BLOB_AND_TEST_REVIEW
preflight_main_head: e600325f8b83550dedb3944b4789b8a372f80c74
upstream: CommunitySolidServer/CommunitySolidServer v7.2.0
upstream_package_lock_git_blob: 62ab7a2bdffdea60df3c1aff31f8eae9e08424af
scope: 延续 MKT018 的精确依赖版本缺口和 CSS 权限组合测试审读。公开非中文源码与技术文档，零新增费用，无实际个人数据。

## 1. 本轮真实新增证据

MKT019-F1 [UPSTREAM_FIXED_LOCKFILE]：通过 GitHub Git blob 只读接口取得 CSS v7.2.0 原始 package-lock.json（返回文本约 1,275,284 字符），成功解析 JSON。lockfileVersion=2；packages["node_modules/@solid/access-control-policy"] 的 version 精确为 **0.1.3**，resolved 为 https://registry.npmjs.org/@solid/access-control-policy/-/access-control-policy-0.1.3.tgz，integrity 为 `sha512-LTxfN8N5hNBNYfuwJr0nyfxlp2P0+GeK+biCa1FQgIqska3wXpTgYaxjVgsw27mKx4N1FOlaGwG+nXdLnl9ykg==`。顶层声明仍为 `^0.1.3`，锁文件旧格式兼容段 dependencies["@solid/access-control-policy"] 同样指向 0.1.3 和同一完整性摘要。故 MKT018 的“实际锁定版本未核实”已在**仓库锁文件层面**闭合。没有下载 npm tarball、运行 npm ci、验证 tarball 实际字节或检查部署实例；不能把锁文件元数据等同于实际生产安装和安全审计。

MKT019-F2 [UPSTREAM_FIXED_TEST_SOURCE]：固定 v7.2.0 的 `test/unit/authorization/AcpReader.test.ts`（Git blob e8fa66d6ae172efa4420fe7949f06fe47e6ee2ca）含父容器 memberAccessControl 允许 Read 的继承测试（90 至 110 行），以及父容器 Read 与子资源 Append 权限组合测试（112 行起）。本轮检索该完整文件，没有找到 `acp:deny` 条件。该文件证明祖先授权聚合存在测试，**不构成祖先 allow Read 与子资源 deny Read 冲突的直接测试证据**。

MKT019-F3 [UPSTREAM_FIXED_TEST_SOURCE]：固定 `test/integration/AcpServer.test.ts`（Git blob 09d330aa2b695eefd9df94207e69bb062c535bf0）第 65 至 68 行验证缺 ACR 返回 401；70 至 80 行验证获允许返回 200；82 至 101 行验证父容器 memberPolicies allow Read 与子资源 allow Write 的组合；103 至 131 行验证控制权限对 ACR 读写的限制。该文件同样未出现 deny 测试。**仅确认这两份已读测试文件的覆盖缺口，不声称 CSS 全部测试套件缺少 deny 场景**。上游 `@solid/access-control-policy` v0.1.3 自身已有 deny 覆盖 allow 的单元测试，详见 MKT018。

MKT019-F4 [UPSTREAM_FIXED_IMPLEMENTATION_SOURCE]：固定 `src/authorization/AcpReader.ts`（Git blob b1be9fe053bd4421eb1dcf4717af7d8757365a65）第 82 行起收集目标及祖先策略，第 123 行起对目标使用 accessControl、对祖先使用 memberAccessControl，第 133 行起逐级向根遍历。依赖锁定与源码审读共同支持“CSS v7.2.0 按预期引用已审读的 ACP v0.1.3 语义”的源码层判断。发行程序和 HTTP 实际行为仍需独立执行。

MKT019-F5 [PRIMARY_PACKAGE_DOCUMENTATION]：npm 官方 package-lock 规范明确 `packages` 下记录安装解析版本、resolved 和 integrity；完整性字段表示预期包字节摘要。其存在不自动证明实际执行环境的依赖字节已验签，也不验证服务器授权行为。

## 2. 产品机制与未来方法映射

| 维度 | 本轮证据支持的机制 | 明确限制 |
| --- | --- | --- |
| 真实数据输入 | HTTP 资源请求、用户 WebID、clientId、issuer、ACR 权限声明 | 本轮只读源码，无真实用户或测试账户 |
| 状态表达 | 资源及祖先 ACR、accessControl/memberAccessControl、allow/deny 模式集合、匹配上下文 | 不表示个人偏好、人生目标或状态转移 |
| 算法 | CSS 聚合祖先策略；锁定的 ACP 0.1.3 对有效同模式 deny 优先 | HTTP 组合结果尚未独立运行 |
| 目标 | 细粒度资源访问控制和跨客户端权限隔离 | 不包含多目标人生优化 |
| 反馈与自我修正 | 管理者可以更改 ACR 并重新发起请求 | 不具备自主学习；缓存和令牌撤销传播未测 |
| 隐私权限 | 同 WebID 不同 clientId 可分别匹配，祖先与子资源规则可能共同影响授权 | 外部副本、备份、衍生数据删除不受该组件保证 |
| 解释性 | 固定规则及输入可被枚举并推导访问决定 | 未证明产品向用户展示可复算权限解释 |
| 费用 | 源码 MIT 开放，现有公开资料免费审读 | 不购买服务、部署云资源或启用收费 CI |
| 可验证性 | 锁文件版本、固定源码和上游测试可复核 | 未执行独立 HTTP、npm 安装或发行程序测试 |

## 3. 候选合成验证与风险

T01：父容器 memberAccessControl allow Read，子资源 accessControl deny Read，匹配同一匿名请求，应验证最终拒绝；调换 ACR 更新顺序再次验证。

T02：子资源仅有 allow Write，祖先 allow Read，分别请求 GET 和 PUT，记录实际状态码及生效策略。

T03：用户 WebID 相同、clientId 分别为 A 与 B；只给 A 授权，B 与缺 clientId 均须检查拒绝结果。另检查 PublicClient 通配的预期影响。

T04：先允许再撤销；新旧请求、缓存、旧令牌、同步副本分别检查。权限撤销不代表已下载数据消失。

T05：在离线且确定无新增费用的环境中，按锁文件执行 npm ci，记录实际安装版本及 tarball 完整性，再运行固定 ACP 单元测试与 CSS HTTP 负对照；本轮均为 PROPOSED_NOT_EXECUTED。

风险 R1：只审查上游 ACP deny 单测可能漏掉 CSS 祖先与子资源整合错误。R2：仅依赖 semver 声明会误认安装版本。R3：锁文件摘要无法替代运行环境与二进制来源验证。以上为测试必要性推论，不代表已发现漏洞。

## 4. E 当日科研治理增量

已读取 main HEAD、market MKT001 至 MKT018、operations E001/E002/E003、privacy_safety F001、今日新增 R140 及 original239 v7.8。E002 已完成 2026-10-25 实质每日审计，E003 已记录 R136 冻结负对照失败，因此本轮只记录新增问题，避免另建重复 E 文件。

R140 新第三方法先冻结协议，提交 `1968c0a5756c15de2a6e3b257aaccc95cd202ba4`，随后归档 Python、Node 和 128 制度结果。科学报告称两种语言逐制度一致，128 制度、1136 档案、4584 偏离、6 等价类、2272 等价配对。报告明确这属于自建有限人工 E1，新增真人 E2=0、历史 E3=0。R140 完整 Python 结果 JSON 据报告仅在本地生成，仓库 research/validation 列表未见该同名文件；Node 完整行收据已在仓库。此为**可复算产物归档覆盖差异**，由 R 主线自行决定是否补齐。对 R140 报告提交 `2bc44c29706076b83c10446fdc2f065df1183c4a` 按 head_sha 查询 Actions 返回 0，不能借用旧 R140 CI 证明新程序通过。原始 239 项 v7.8 仍有 154 条逐项证据审计待办，schema/date 仍保留 v7.6/2026-10-24 内部元数据；未改写。R136 历史失败继续开放。没有进行全仓冻结哈希检查、实际账户账单审计或 GitHub 免费额度核验。各轨新提交的存在与科研验收严格区分。

## 5. F 本周状态

2026-W43 F001 已归档，内容为人类否决权、解释和最小数据原则；本轮未重复启动 F002。为下一周 F002 登记：授权拒绝应同时检查祖先策略和客户端身份；撤权后需分别管理本地原始文件、缓存、令牌、衍生统计、备份和第三方副本。仅候选控制，无真实敏感数据、无产品开发。

## 6. 证据、归档与后续

MARKET E1：固定 Git blob 锁文件、CSS v7.2.0 固定源码与测试文本、npm 官方格式说明。MARKET E2 独立执行验证=0；MARKET E3 个人长期决策效果=0。上游测试源码已阅读，未执行。独立科研 E1/E2/E3 与商业证据等级不得混用。

本轮没有购买、注册付费服务、调用计费 API、启动 CI、部署服务器/GPU 或接入真实敏感数据。主动新增费用 0，账单与免费额度未核验。仅新增 research/market 独立路径，不修改 R、E、F、索引或冻结协议。

next_action: MKT020 审查 CSS v7.2.0 其他 ACP 测试文件是否覆盖祖先 allow 与子资源 deny 冲突，优先静态审读；若无法在零新增费用条件下验证，转向 Exist 的 OAuth 撤权及 ProjectionLab 情景假设透明性研究。E 下一次只检查 R140 新程序产物及真实 CI 是否补齐。F002 进入下一周后再进行授权撤回与衍生数据生命周期专题。

## 7. 可核验非中文来源

S1 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/package-lock.json
S2 https://api.github.com/repos/CommunitySolidServer/CommunitySolidServer/git/blobs/62ab7a2bdffdea60df3c1aff31f8eae9e08424af
S3 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/unit/authorization/AcpReader.test.ts
S4 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/integration/AcpServer.test.ts
S5 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/authorization/AcpReader.ts
S6 https://github.com/solid-contrib/access-control-policy/blob/v0.1.3/src/algorithm/allow_access_modes.ts
S7 https://docs.npmjs.com/files/package-lock.json/
S8 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R140_EFFECTIVE_RULE_GRAPH_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-25.md
S9 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md

commit_sha: 以写入后远端 SHA 核验为准。
