# MKT020 CSS v7.2.0 ACP 权限测试覆盖与 ACR 目标身份审读

date: 2026-10-25 (UTC+08)
track: commercial_market
status: COMPLETE_BOUNDED_UPSTREAM_SOURCE_TEST_AUDIT
preflight_main_head: 701f1a666bebc517b923729424514cfb20bb74a2
upstream: CommunitySolidServer/CommunitySolidServer tag v7.2.0
scope: 接续 MKT019，固定版本公开英文源码和测试文件，只读审查，零新增费用。本文的 E、F 段仅登记当日和本周状态，保持各轨独立。

## 1. 新增事实及证据层级

MKT020-F1 [UPSTREAM_FIXED_TREE]：GitHub v7.2.0 递归树对象 b4fe28370bc297308fdf9329b6eb7901dde5395f 返回 truncated=false、1628 个路径条目。发现与 ACP 直接相关的测试包括 test/unit/authorization/AcpReader.test.ts、AcpUtil.test.ts、test/integration/AcpServer.test.ts、PermissionTable.test.ts 和 test/util/AcpHelper.ts。已读取这些固定版本文件以及 AcpReader.ts、AcpUtil.ts 的源码。此项说明候选文件发现范围，不能据此声称全仓每个测试均已逐行检查。

MKT020-F2 [UPSTREAM_FIXED_TEST]：PermissionTable.test.ts Git blob dd83e9d6dbf8717427235bc903109b3f8dae2b18 包含 51 个 HTTP 方法与权限组合行，并以 ACP 内存和文件存储两种配置运行相同表格。表中有 GET C/R、父容器 Read、子资源 Write、预期 401 的行，覆盖“父子允许模式不一致时没有 Read”的情形。ACP 配置辅助函数 setAcpPermissions 仅设置 allow 字段，没有设置 deny 字段；这 51 行无法证明显式 acp:deny 覆盖祖先 acp:allow 的组合行为。每行针对目标存在与不存在各有测试声明，属于测试设计，未独立执行。

MKT020-F3 [UPSTREAM_FIXED_TEST]：AcpUtil.test.ts Git blob 135f157c87548376c77a22b253f0ea6f59f56f49 第 27 至 31 行构造 allow Read/Append、deny Write 的 RDF 数据，第 65 行验证 getPolicy 正确解析 deny Write。它是“拒绝策略解析”的直接测试证据，尚未覆盖最终权限计算或 HTTP 结果。此前 MKT019 对两份测试文件的否定观察因此需限定为“没有显式拒绝的 HTTP/继承冲突验证”，不能概括为 CSS 完全没有 deny 测试。

MKT020-F4 [UPSTREAM_FIXED_TEST_SETUP_DIAGNOSTIC]：AcpServer.test.ts Git blob 09d330aa2b695eefd9df94207e69bb062c535bf0 的继承测试第 82 至 101 行：父容器 memberPolicies 允许 Read；测试随后调用 setAcp(target, createAcr({resource: baseUrl, policies: allow Write}))；最后 GET target 期望 200。AcpHelper.ts Git blob 7dcd7bf04f966c1a80d52245eca2de9dfaa67444 的 createAcr 将 resource 作为 ACR 的 acp:resource；setAcp(id,...) 仅将文档写到 id.acr。AcpUtil.ts Git blob 41c8f8fc20d056d2654354e7fb7b6c0f08d03d90 依据 RDF acp:resource 值生成受控资源 iri。AcpReader.ts Git blob b1be9fe053bd4421eb1dcf4717af7d8757365a65 根据 iri===target.path 选择 accessControl，否则选择 memberAccessControl。因此此测试中的子 ACR 明示 resource=baseUrl，与 target 不同；其 allow Write 的 accessControl 在当前读取逻辑下不能作为 target 的直接授权。GET 200 已由父容器继承 Read 足以解释。该用例对“父容器 Read 加子资源 Write 的同时生效”鉴别力不足。这是测试夹具与断言的静态审计结论，未运行 HTTP 测试，未认定真实产品安全漏洞。

MKT020-F5 [UPSTREAM_FIXED_UNIT_AND_DRAFT]：AcpReader.test.ts Git blob e8fa66d6ae172efa4420fe7949f06fe47e6ee2ca 在“combines all relevant ACRs”用例中正确将子资源 acp:resource 指向子目标，并测试祖先 Read 与直接 Append 合并；没有显式 deny。Solid ACP Editor's Draft 2022-09-29 第 6.2 和 6.3 节规定资源直接策略与祖先成员策略均为有效策略，满足的 deny 优先于 allow。该草案是规范设计参考，不能自动证明 CSS 实现符合规范。上游 ACP v0.1.3 的 deny 单测已在 MKT018 阅读，独立执行为 0。

## 2. 对未来个人决策系统的候选方法

| 维度 | 可见机制 | 限制 |
| --- | --- | --- |
| 数据输入 | HTTP 请求目标、用户 WebID、clientId、issuer、ACR RDF 策略 | 本轮无真实用户数据或账号 |
| 状态表达 | 父容器与子资源 ACR，allow/deny 集合，策略目标 iri | 未表达人的偏好、健康状态或人生目标 |
| 算法 | 按 acp:resource 匹配直接策略，汇集祖先 memberAccessControl，再调用 ACP 求值 | HTTP 显式拒绝组合未独立验证 |
| 目标 | 资源与应用级访问隔离，降低越权读取 | 没有生活多目标优化算法 |
| 反馈与自我修正 | 修改授权文件后可以重新求值 | 没有自动学习，缓存与令牌传播未测 |
| 隐私权限 | deny 与祖先授权冲突需要端到端验证；错误目标 IRI 可使预期子策略不生效 | 无法保证第三方副本、备份及衍生数据删除 |
| 解释性 | RDF 策略、目标标识、访问结果均可记录并复算 | 未证明产品提供用户可读解释 |
| 费用 | 官方源码和草案可免费读取 | 未部署服务器、下载收费产品或使用付费 CI |
| 可验证性 | 固定 Git blob、51 行权限表、精确代码路径 | 没有独立 HTTP 测试、生产部署测试或决策效果证据 |

## 3. 候选合成负对照及风险

T01：父容器 memberAccessControl allow Read，子资源 ACR 的 acp:resource 精确指向子资源，accessControl deny Read，使用同一匿名上下文发起 GET；规范预期拒绝。分别测试内存与文件存储，记录实际 HTTP 码、求值策略和日志。

T02：保持父容器 allow Read，将子资源改为仅 allow Write；GET 预期可由祖先授权通过。此项与 T01 联合区分“没有子级允许”与“子级明确拒绝”。

T03：将 T01 的子 ACR acp:resource 错误设为父容器 URL，比较 GET 与正确目标版本；以此测试 ACR 目标标识错误是否使 deny 失效。静态源码预测两者可能不同，实际行为未验证。

T04：同一资源匹配的两个策略分别 allow Read 与 deny Read；调换策略顺序，要求结果保持拒绝。再添加不同 clientId、缺失 clientId 的负对照。

T05：允许后撤销；对新请求、已有会话、缓存、已下载副本和衍生统计分别登记可撤销范围。权限拒绝不能当作已删除历史副本的证据。

风险 R1：测试成功状态可能被过度归因到实际未参与决策的子资源策略。R2：只检查无 allow 的拒绝行为，会漏掉显式 deny 对祖先 allow 的覆盖错误。R3：ACR 的保存位置与 acp:resource 声明目标不一致时，策略作用范围可能偏离预期。以上均为候选测试风险，无已确认安全漏洞。

## 4. E 当日治理增量（只读）

2026-10-25 已有 E002 跨轨实质审计与 E003 R136 冻结负对照事件登记。本轮核查当前 main HEAD、market MKT001 至 MKT019、E002/E003、F001 和后续 R141/R142 增量，未重复创建 E004。

R141 冻结提交 fef647da28c94c091a7b85ed8a4be03f7d1511c8 在结果提交前。最新科学报告 Git blob 6e5065aeacb14b88e43f0e963c0cf9377b72fb3b 声称 24 个离散场景共 213096 档案、3331944 次实际 JS 单侧偏离比较，并有 Python Fraction 独立组合复核；新 CI 明示 NOT_RUN。报告区分 JS 实际遍历和 Python 理论机会数。未在本轮重跑 3331944 次计算，E1 为内部有界数学证据。

R142 冻结提交 ca64385e9a93d111a11b723e916528db11ddd5e0 在源码和结果提交前。最新报告 Git blob 8f2fa36e2e7543333b2f62160c4062f3bf2543f4 记录 25 个精确 2×2 收益矩阵，κ=1 时纯 BNE=8、κ=99/100 和 101/100 时各为4，两种内部算法一致；新 CI 明示 NOT_RUN。仅限 h=0 完全信息 E1，未验证 h1/h2、真实 E2 或历史 E3。

R140 新方法归档仍可见 Node 128 行收据；在本轮 research/validation 目录列表未见同名 Python 完整结果 JSON，维持既有归档覆盖待办。original239 最近已审计 v7.8 的 154 条逐项审计待办，未重新读取最新版索引，不擅自宣称数量发生变化。R136 历史负对照失败仍开放。未扫描全仓冻结哈希、未将 [skip ci] 提交当成 CI 成功、未核验账户账单与免费额度。没有修改其他轨结果、冻结协议或索引。

## 5. F 本周状态

2026-W43 已有 F001（人类否决权、解释、最小采集）归档，今日不重复生成 F002。为下一周候选专题登记：授权撤回时需同时核验 acp:resource 身份、祖先有效策略、客户端身份、旧令牌、缓存及衍生副本；区分“拒绝未来访问”和“删除既往数据”。仅方法储备，无真实敏感数据和个人决策产品开发。

## 6. 证据、成本、归档与下一步

MARKET E1：固定 Git tree、固定 Git blob 源码及测试设计、Solid 社区 Editor's Draft。MARKET E2 独立软件执行=0，MARKET E3 长期人生决策效果=0。规范声明、上游测试源码、独立验证和推断分别标记，不能以官方文档替代实测。

本轮只使用公开非中文来源及现有连接，未购买论文或产品、注册收费服务、调用计费 API、租用云服务器/GPU、主动运行 CI、接入敏感数据。主动新增费用 0；账户账单和 GitHub 免费额度未核验。核心研究顺序保持完整 R 系列、系统归纳分类、最后模型熔炼。

next_action: MKT021 继续核查 CSS v7.2.0 ACP 的资源目标身份约束与测试夹具；优先研究 acp:resource 错配时的校验路径和拒绝语义，形成可独立运行且零费用的合成负对照。若现有证据不足，转向 Exist OAuth 撤权及 ProjectionLab 情景假设审查。

## 7. 原始非中文来源

S1 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/integration/PermissionTable.test.ts
S2 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/integration/AcpServer.test.ts
S3 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/unit/authorization/AcpUtil.test.ts
S4 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/unit/authorization/AcpReader.test.ts
S5 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/util/AcpHelper.ts
S6 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/authorization/AcpReader.ts
S7 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/authorization/AcpUtil.ts
S8 https://solid.github.io/authorization-panel/acp-specification/
S9 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R141_COMBINATORIAL_KKT_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-25.md
S10 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R142_H0_KAPPA_TIE_SENSITIVITY_SCIENTIFIC_REPORT_2026-10-25.md

commit_sha: 写入后核验远端 SHA，不预填。
