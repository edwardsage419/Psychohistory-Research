# MKT018 Solid ACP v0.1.3 权限冲突与客户端匹配的固定源码及测试审读

date: 2026-10-25 (UTC+08)
track: commercial_market
status: COMPLETE_BOUNDED_FIXED_TAG_SOURCE_AND_TEST_AUDIT
prewrite_main_head: a927679035ee7eea3b6b2acc9c662e8a74e33386
upstream_package: @solid/access-control-policy
upstream_repository: solid-contrib/access-control-policy (原 solid/access-control-policy，GitHub 仓库 ID 441172941)
fixed_tag: v0.1.3
fixed_tag_ref_object_sha: b1bfdbc112724cccd5beaa9bd663bedefa16446e
package_json_blob_sha: c2206abf641163cc85b02a196f50c08c12550de2
scope: MKT017 未完成的外部 ACP 求值器审计。仅阅读公开非中文原始源码、固定单元测试和规范；无服务器部署、账户注册、个人数据或付费 API。

## 1. 研究增量及可复核证据

MKT018-F1，FIXED_IMPLEMENTATION_SOURCE：Community Solid Server v7.2.0 的 package.json 将 @solid/access-control-policy 声明为 ^0.1.3，CSS 的 AcpReader.ts 将资源及祖先有效策略交给 allowAccessModes。直接读取外部包 v0.1.3 的 package.json，确认其版本 0.1.3、MIT 许可证。CSS 的 package-lock.json 文件存在且 Git blob 为 62ab7a2bdffdea60df3c1aff31f8eae9e08424af，但本轮因内容过大无法获取并解析，故 **不能声称已核验 CSS 实际锁定版本或已执行的 npm 依赖字节**。^0.1.3 是声明的语义版本范围，固定 v0.1.3 是本轮源码审查对象。

MKT018-F2，FIXED_IMPLEMENTATION_SOURCE + TEST_FIXTURE：固定 `src/algorithm/allow_access_modes.ts` Git blob 21d6f0c746dff4ff39d2c8e4b63f3efa2e2c0698 将满足条件的策略分别累积 allow 与 deny，最后从 allow 集合删除 deny 集合中的每一种访问模式。**同一模式的有效 deny 优先于有效 allow，策略遍历顺序不影响集合结果。** 固定 `allow_access_modes.test.ts` Git blob 2ce6f9339d6e47df81363c3dded846016ef0e8e3 包含同策略冲突、跨策略冲突、反转顺序及不同模式组合测试。此结论已经获得源码和测试用例双重支持；测试本轮未运行。Solid ACP 社区规范 6.3 同样描述 deny overrules allow，但规范符合性与发行程序实测尚未独立验证。

MKT018-F3，FIXED_IMPLEMENTATION_SOURCE + TEST_FIXTURE：固定 `src/algorithm/apply_policy.ts` Git blob b77d2653eb845a214bcb0a8769b68e62b070af18 要求 allOf 或 anyOf 至少存在一项匹配条件。allOf 的全部 matcher 需满足，anyOf 至少一个需满足，noneOf 任意命中则使该策略不适用。**只有 noneOf 而无 allOf/anyOf 的策略永不适用，不能把 noneOf 当成独立的禁止授权机制。** 对应 `apply_policy.test.ts` Git blob 58ae0ad611814a63fc33b237a8923d30f1b41f7d 包含 noneOf-only 返回 false 的测试。风险案例：将“禁止客户端 B”仅写为 noneOf，预期的拒绝策略可能根本没有生效。此为源码语义推论，未证明 CSS 对错误规则的运行响应。

MKT018-F4，FIXED_IMPLEMENTATION_SOURCE + TEST_FIXTURE：固定 `src/algorithm/match.ts` Git blob c6ad7d8087012816c9c5eee1a56e40d3111c1bdd 要求 matcher 至少有一种属性，且每种已声明的属性类别都必须匹配请求上下文。单个类别内允许多值之一命中。agent、client、issuer、vc 四类属性合取；仅 agent 匹配不足以绕过 client/issuer 的限定。测试 `match.test.ts` Git blob 68866491ef4667cbc01c3f7366ce2659fabababc 覆盖一个属性不匹配和全部匹配。

MKT018-F5，FIXED_IMPLEMENTATION_SOURCE + TEST_FIXTURE：固定 `src/algorithm/match_client.ts` Git blob 43f7ca1275b3730535072eee48eb2766bba73fff 中，普通 client IRI 要求 context.client 存在且相等；**ACP.PublicClient 为通配匹配，即使请求没有提供 clientId 仍会命中。** `match_client.test.ts` Git blob 7ee7cb05c58cb51c885489cffc9f42b810ca4fdc 明确测试空 context 对 PublicClient 返回 true。此机制可以表达公共客户端策略，若误用于敏感资源，会扩大访问范围。需要同时检查实际认证层是否可信地提供 clientId。

MKT018-F6，FIXED_IMPLEMENTATION_SOURCE：`match_agent.ts` 支持 PublicAgent、AuthenticatedAgent、CreatorAgent、OwnerAgent 与精确 agent IRI；`match_issuer.ts` 要求 context.issuer 存在并精确匹配。此为已阅读的固定源码语义，不能直接推断任意服务器已实现可靠认证或拥有者身份校验。

## 2. 产品与研究方法矩阵

| 维度 | 已观察机制 | 验证边界 |
| --- | --- | --- |
| 数据输入 | CSS HTTP 请求中的资源、WebID、clientId、issuer，ACP 的策略与 matcher | 未接入任何真实个人数据 |
| 状态表达 | 资源及祖先 ACR，allow/deny 模式集合，allOf/anyOf/noneOf 和上下文属性 | 实际 CSS package-lock 解析未完成 |
| 算法 | 有效策略集合求值，deny 覆盖 allow，matcher 逐类别合取 | 固定 v0.1.3 源码已读，Jest 未运行 |
| 目标 | 资源级访问控制及应用隔离 | 无人生目标优化或偏好学习 |
| 反馈与自我修正 | 管理者可更新 ACR 并重新请求；算法本身不自学习 | 撤权后的缓存、令牌、备份与外部副本未测 |
| 隐私权限 | client 精确匹配及 PublicClient 通配；祖先规则和 deny 优先级 | 认证来源和实际 HTTP 结果未测 |
| 解释性 | 可列出贡献权限的有效策略、匹配属性及冲突模式 | 未验证实际服务器是否生成可审计解释 |
| 费用 | v0.1.3 MIT 开源源码可免费审读；本轮零新增操作费用 | 云托管、额外计算和计费 CI 均禁止 |
| 局限 | 仅授权决策组件；无删除传播、备份清理、长期人生决策效果证据 | 无发行二进制、跨版本兼容及独立安全审计 |

## 3. 候选合成验证及优先风险

T01 父容器 allow Read，子资源 deny Read，匹配同一请求时应拒绝 Read；反转策略输入顺序，结果应相同。
T02 同策略 allow Read 和 deny Read，应拒绝 Read；允许 Write 而 deny Read 时应只保留 Write。
T03 仅有 noneOf 的 deny 策略应判不适用，另加 allOf 或 anyOf 后重新求值，防止误认为 noneOf 自带禁止效力。
T04 同一 WebID 的两个不同 clientId 仅一个匹配授权，且缺少 clientId 不应匹配普通客户端规则。
T05 配置 PublicClient 时即使请求未提供 clientId 也会匹配；需检查上层身份认证及资源分类是否允许此通配。
T06 matcher 同时限制 agent、client、issuer，故意更改任意一个字段，确认不会通过。
T07 父容器 allow、子资源 deny 及多级祖先组合；撤销任一规则后重复请求，检查跨请求缓存和旧令牌。
T08 锁定 CSS 实际安装依赖版本及 npm tarball 哈希，独立运行固定版本单元测试，再运行本地无敏感数据的 HTTP 负对照。仅在确认完全免费且不会启动计费 CI 时考虑执行。

以上均为 PROPOSED_NOT_EXECUTED；本轮没有声称执行测试、真实漏洞、认证绕过或第三方独立安全验证。

## 4. E 当日只读协调与质量核对

已在研究开始和写入前读取 GitHub main HEAD、market MKT001 至 MKT017、operations E001/E002/E003、privacy_safety F001 与今日 R/TH/A 新增提交。2026-10-25 的 E002 已完成每日实质跨轨审计，E003 已完成 R136 负对照事故增量审计，因此本轮不创建重复 E004。R136 历史冻结负对照失败记录继续保留。

本轮额外读取 R138 第三方法报告及后续精确 Git blob 本地重放补充收据。新收据称 GitHub 原样 Python 文件本地执行、输出与此前计算逐字节一致；**这是项目归档的内部重放声明，本轮未独立重跑，且新远端 CI 仍为 NOT_RUN**。R139 新第三方法报告称 17 个最佳反应情形、729 个有序配置、17496 项偏离检查与预冻结负对照通过，GitHub 精确源码重放；本轮仅核对归档文本，未独立重算或核验新 CI。R138/R139 新增真人 E2=0、历史 E3=0，不能重复降低 original239 v7.8 记录的 154 项待逐项审计队列。v7.8 JSON 内 schema/date 仍显示 v7.6/2026-10-24，属已有元数据滞后问题；未修改索引。最新 TH021 已提交，不由本轨改写。未进行全仓冻结文件哈希审计、账单核对或免费额度审计，不能宣称其已完成。

## 5. F 本周专题状态

2026-W43 的 F001 人类否决权、解释与数据最小化专题已正式归档。本轮没有重复创建 F002。新增 F002 候选风险为：误用 PublicClient 通配、noneOf-only 禁止规则失效、祖先授权与子资源 deny 的组合、撤权后的跨请求缓存及外部副本。F002 应按下周专题“授权撤回与衍生数据生命周期”研究，且不得接入真实敏感数据、开发个人决策产品或提前设定唯一人生效用权重。

## 6. 证据等级、归档限制及下一步

MARKET-E1：固定 v0.1.3 官方上游源码、单元测试源码及 CSS v7.2.0 package.json。
SPEC-PRIMARY：Solid ACP 社区规范；其规范性要求不自动等于软件符合性。
MARKET-INFERENCE：错误配置风险与未来合成测试。
MARKET-E2 独立执行验证：0；MARKET-E3 长期个人决策改善证据：0。以上与 R 系列科研 E1/E2/E3 分开。

本轮未购买论文或产品、未注册收费服务、未调用计费 API、未启动收费 CI、未部署云服务器/GPU、未接入真实敏感数据。主动新增费用 0；GitHub 账户账单及免费额度未核验。

next_action: MKT019 优先在免费条件下获取 CSS v7.2.0 package-lock 的确切 @solid/access-control-policy 解析版本，并检查实际服务器 ACP deny 与父容器 allow 的合成测试覆盖。若仍无法取得完整锁文件，转向 Exist 数据授权撤回及 ProjectionLab 情景参数可解释性研究，不为锁文件下载购买任何服务。

项目顺序保持先完成全部 R 系列，再系统归纳分类，最后模型熔炼。商业、治理、安全均为候选知识储备。

## 7. 非中文原始资料与固定来源

S1 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/package.json
S2 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/authorization/AcpReader.ts
S3 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/package-lock.json
S4 https://github.com/solid-contrib/access-control-policy/tree/v0.1.3
S5 https://github.com/solid-contrib/access-control-policy/blob/v0.1.3/src/algorithm/allow_access_modes.ts
S6 https://github.com/solid-contrib/access-control-policy/blob/v0.1.3/src/algorithm/apply_policy.ts
S7 https://github.com/solid-contrib/access-control-policy/blob/v0.1.3/src/algorithm/match.ts
S8 https://github.com/solid-contrib/access-control-policy/blob/v0.1.3/src/algorithm/match_client.ts
S9 https://github.com/solid-contrib/access-control-policy/blob/v0.1.3/test/unit/algorithm/allow_access_modes.test.ts
S10 https://github.com/solid-contrib/access-control-policy/blob/v0.1.3/test/unit/algorithm/apply_policy.test.ts
S11 https://github.com/solid-contrib/access-control-policy/blob/v0.1.3/test/unit/algorithm/match_client.test.ts
S12 https://solid.github.io/authorization-panel/acp-specification/
S13 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/operations/E003_R136_FROZEN_NEGATIVE_CONTROL_INCIDENT_DELTA_2026-10-25.md
S14 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md

commit_sha: 写入后以远端核验为准。
