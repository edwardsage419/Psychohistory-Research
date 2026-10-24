# MKT017 Community Solid Server v7.2.0 ACP 权限继承与客户端匹配源码审计

observed_at: 2026-10-25 (UTC+08)
track: commercial_market
status: COMPLETE_BOUNDED_FIXED_TAG_SOURCE_AND_TEST_REVIEW
observed_main_head_prewrite: 7b0b4735e4d436e7573ef5710aa4eb03b75e1022
upstream: CommunitySolidServer/CommunitySolidServer
fixed_tag: v7.2.0
fixed_tag_commit: b4fe28370bc297308fdf9329b6eb7901dde5395f
official_release_published_at: 2026-07-22T09:14:09Z
preflight: 已读取 main HEAD、market MKT001 至 MKT016 文件清单、MKT016 全文、E002/E003、F001、本日近期 R/TH/A 提交和当日工作登记。写入前再次检查 HEAD 与 market 目录，确认 MKT017 尚不存在。仅增量研究，不修改其他轨文件或索引。

## 1. 本轮真实新增机制与证据

MKT017-F1，IMPLEMENTATION-SOURCE：在 v7.2.0 固定源码 `src/authorization/AcpReader.ts` 第 73 至 100 行，权限计算对目标资源及全部祖先依次读取 ACR，收集有效策略后调用 `@solid/access-control-policy` 的 `allowAccessModes(policies, context)`。源码第 119 至 125 行对目标自身使用 `accessControl`，对祖先使用 `memberAccessControl`。**一个子资源存在独立 ACR，并不意味着祖先 memberAccessControl 不再参与该子资源的 ACP 权限计算。** 这与 WAC 源码第 153 至 176 行优先寻找最近有效 ACL 的算法构成重要实现差异。直接修改子资源的本地规则不能据此证明已撤销祖先授予的访问。实际撤权结果仍取决于所有有效 allow/deny 策略的求值；本轮未对运行服务器做请求实验。

MKT017-F2，IMPLEMENTATION-SOURCE + TEST-FIXTURE：`AcpReader.ts` 第 106 至 112 行将 WebID、clientId、issuer URL 组成上下文。固定单元测试 `AcpReader.test.ts` 第 179 至 203 行要求 agent、client、issuer 同时匹配，缺少这些凭据时无 read 权限，补齐时 read=true。该测试源文件是项目维护者的测试设计，**本轮仅审阅测试代码，未运行 Jest，也未验证实际部署或第三方客户端的安全性**。测试覆盖一个正反对照，不能推断令牌撤销传播或任意复杂策略均正确。

MKT017-F3，IMPLEMENTATION-SOURCE + TEST-FIXTURE：`AcpReader.test.ts` 第 90 至 145 行含继承及多 ACR 策略组合单测；`AcpServer.test.ts` 第 65 至 130 行含无 ACR 返回 401、授权后返回 200、继承读取成功、ACR 读写需要 control 权限的 HTTP 集成测试。存在测试用例并不等于当前环境运行成功。缺少 ACR 时 `AcpReader.ts` 第 150 至 159 行将 NotFound 转换为空 RDF 数据，最终是否拒绝由有效策略与 authorizer 决定；集成测试展示一组无 ACR 的拒绝实例。不可把该实例推广成所有错误配置均安全。

MKT017-F4，IMPLEMENTATION-SOURCE：`AcpUtil.ts` 第 34 至 57 行解析 agent、client、issuer、vc 及 allow、deny、allOf、anyOf、noneOf；最终策略求值委托外部 `@solid/access-control-policy` 包。本轮未审计该包的固定版本实现，因此不宣称已经独立验证 deny 优先级、冲突合并或所有 matcher 语义。 `AcpReader.ts` 第 54 至 61 行每次 handle 建立局部缓存，第 147 至 175 行单测检查重复 ResourceStore 读取次数；不代表跨请求的撤销缓存一致性已得到证明。

MKT017-F5，IMPLEMENTATION-SOURCE + CONFIG：固定 `config/ldp/authorization/acp.json` 显式启用 ACP reader，并在配置中列出 agent、client、issuer 属性。固定 `config/ldp/authorization/allow-all.json` 则明确无条件允许操作。部署配置必须作为权限审计对象。源代码可支持隔离能力，错误配置仍可能完全开放资源。

MKT017-F6，RELEASE-METADATA：固定 v7.2.0 Git tag 解析为 commit `b4fe28370bc297308fdf9329b6eb7901dde5395f`，官方 GitHub Release 日期为 2026-07-22。发布说明包括 TokenOwnershipValidator 信息泄露防护与安全说明文档更新。这是版本变更元数据；本轮未检查发行包字节、运行漏洞或独立安全报告，不能把修复公告视为全系统安全验收。

## 2. 产品观察矩阵

| 维度 | v7.2.0 可核查机制与限制 |
| --- | --- |
| 数据输入 | HTTP 请求中的资源路径、方法、认证 WebID、clientId、issuer；Pod 中 RDF/普通资源；本轮无真实个人数据 |
| 状态表示 | Pod 资源树、资源与祖先 ACR、ACP 策略、访问模式、请求凭据上下文 |
| 算法 | 对目标及祖先汇总 accessControl/memberAccessControl，再由 access-control-policy 计算允许模式 |
| 目标 | 按资源、身份和客户端限制读写及控制权限，支持应用数据隔离 |
| 反馈与自我修正 | 管理者更新 ACR 与授权规则；代码未显示个人目标学习、偏好自适应或人生策略优化 |
| 隐私权限 | 可按 clientId 和 WebID 组合匹配；继承规则与 allow-all 误配置构成需验证风险 |
| 可解释性 | 源码可追踪策略来源和上下文；实际拒绝原因、审计日志与可读解释未在本轮实测 |
| 费用模式 | 固定 package.json 为 MIT；仅免费公开源码审查，无运行服务或额外费用。云托管、维护和收费服务不在本轮范围 |
| 产品局限 | 无跨副本撤销保证、无备份删除验证、无独立长期个人决策效果研究；未运行服务器、Jest 或外部策略包 |
| 验证性 | 固定 tag、Git blob、单元和集成测试文件可供后续离线合成复验 |

## 3. 候选合成验证方案，均未执行

T01 同一 WebID，client A 获得资源 A 的 read，client B 无法读取 A；验证凭据是否携带可信 clientId。
T02 相同 WebID 和 client，issuer 由已授权改为未授权，预期不匹配策略；明确独立验证令牌认证层。
T03 父容器 memberAccessControl 授予 read，子资源 ACR 无该 allow，检查是否仍因祖先策略获权；对比 WAC 最近 ACL 行为。
T04 撤销父容器授权后，子资源的读权限应按新有效策略重算；同时检查祖先、组、公开规则及跨请求缓存。
T05 子资源显式 deny 与祖先 allow 冲突，检查固定外部策略包版本的实际求值，不预设测试结果。
T06 无 ACR、错误 ACR、无授权配置分别检查 HTTP 状态和审计日志，禁止将 401/403/500 混同。
T07 对 ACR 的 GET、PUT、DELETE 检查 control 权限与拒绝行为，包含匿名和有身份请求。
T08 配置由 ACP 变为 allow-all 或 WAC 时检测高风险权限扩张并拒绝迁移；保留原规则备份以供合成审计。

以上是未来安全与市场方法研究的候选测试，不能提前开发个人决策产品或接入用户真实敏感数据。

## 4. E 当日治理检查，限新增事实

E002 当日已完成跨轨只读审计，E003 已记录 R136 原冻结 q2/q3 负对照 FAILED_NONDISCRIMINATING。本轮直接读取其后新增的 `R136_CORRECTIVE_Q_ORDER_SCIENTIFIC_REPORT_2026-10-25.md`：报告称新冻结的纠正性边际检查对 1215 行逐行复核，810 行 q2≠q3 的故意错序均被拒绝，405 行 q2=q3 不可辨识；状态仅 PASS_CORRECTIVE_CONTROL_ONLY，原历史失败仍保留。完整 1215 行 CSV 的原始字节仍未由本轮取得，本轮也未独立重算该算法或检查新增 CI，不得宣称正式第三方法验收。

另读 `R137_CYCLE_DB_BIRTH_DEATH_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-25.md`：报告记录事前冻结后，环图 C5 至 C9 五个阈值独立出生死亡链精确复算，状态 PASS_BOUNDED_LOCAL_E1_THIRD_METHOD；明确新 CI NOT_RUN，未新增真人 E2 或历史 E3。A 数据侦察 `ANDREOZZI_2020_R079_R087_PRIOR_E2_SOURCE_DEDUP_2026-10-25.md` 确认 2020 真人数据已在 R079/R087 使用，不能作为新的独立 R073 外部复现实验，且三水平行动不适配原二元冻结评分。上述状态仅基于 GitHub 归档报告，未独立复跑。

original239 最新已核对记录 v7.8 的 provisional itemwise audit open=154；本轮未重新解析新版索引，也未减少队列。schema 内部版本滞后、R127 追溯补充、R136 原冻结控制失败仍为既有开放项。无全仓冻结协议哈希审计。E002/E003 已满足今日实质检查，本轮仅登记新增差异，不重复写 operations 文件。

## 5. F 本周专题、证据边界与费用

2026-W43 的 F001 已归档并完成“人工否决与最小数据”专题。本轮未重复创建 F002。新增候选风险是 ACP 的祖先授权可能使局部撤销无效，以及 WebID 与客户端身份应分别校验；归入下周 F002“授权撤回、衍生数据与备份生命周期”待办。未接入敏感数据或开发个人决策产品。

证据分级：MARKET-E1 官方固定版本源码、配置和测试文件；RELEASE-METADATA 官方版本日期；MARKET-INFERENCE 候选风险；MARKET-E2 独立执行复验=0，MARKET-E3 长期个人决策效果验证=0。项目 R 系列 E1/E2/E3 独立计量。没有购买产品或论文、注册收费服务、计费 API、收费 CI、云服务器/GPU、新订阅或真实敏感数据；主动新增费用为 0，账户整体账单及免费额度未独立核验。

研究顺序：先完成全部 R 系列，再统一归纳分类，最后模型熔炼。此处机制仅为候选知识储备，不改变冻结协议、不设定唯一人生效用权重。

next_action: MKT018 深读 `@solid/access-control-policy` 固定依赖版本的 allow/deny 冲突与 client matcher 求值测试，并对照 CSS v7.2.0 的 package lock；若免费公开源码无法取得，则转向 Exist API 授权撤销和数据生命周期研究。

## 6. 非中文公开原始来源

S1 https://github.com/CommunitySolidServer/CommunitySolidServer/releases/tag/v7.2.0
S2 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/authorization/AcpReader.ts
S3 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/authorization/AcpUtil.ts
S4 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/authorization/WebAclReader.ts
S5 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/unit/authorization/AcpReader.test.ts
S6 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/integration/AcpServer.test.ts
S7 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/integration/PermissionTable.test.ts
S8 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/config/ldp/authorization/acp.json
S9 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/config/ldp/authorization/allow-all.json
S10 https://communitysolidserver.github.io/CommunitySolidServer/7.x/architecture/features/protocol/authorization/
S11 https://communitysolidserver.github.io/CommunitySolidServer/7.x/usage/authorization-methods/
S12 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/operations/E003_R136_FROZEN_NEGATIVE_CONTROL_INCIDENT_DELTA_2026-10-25.md
