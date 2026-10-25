# MKT022：CSS v7.2.0 ACR 的 HTTP PUT 写入、授权及目标语义校验链

date: 2026-10-25 (UTC+08)
track: commercial_market
status: COMPLETE_BOUNDED_FIXED_SOURCE_WRITE_PATH_AUDIT
preflight_main_head: a1f65a97a5f11d78ebde334eeaddf67e8ead96d6
prior: MKT017 至 MKT021，特别是 MKT021 的 ACR acp:resource 目标错配待验证
scope: 固定 CommunitySolidServer/CommunitySolidServer v7.2.0 官方源码、配置和上游 HTTP 测试的只读审查；未运行服务或测试，未接入真实 Pod 或用户数据。

## 1. 本轮新增的技术事实

**MKT022-F1 [FIXED_SOURCE_AND_CONFIGURATION]：ACR 与普通 .meta 是不同资源类别，PUT 处理器没有统一禁止写入 .acr。**
`config/ldp/handler/components/operation-handler.json` 为 PutOperationHandler 注入 `MetadataStrategy`；`config/util/auxiliary/strategies/meta.json` 仅匹配 `.meta`，`config/util/auxiliary/strategies/acr.json` 的 `AcrStrategy` 匹配 `.acr`。PutOperationHandler.ts 仅在 `metadataStrategy.isAuxiliaryIdentifier(operation.target)` 时拒绝 PUT，随后调用 ResourceStore.setRepresentation。因此在已审 ACP 配置中，.acr 不因上述 metadata PUT 禁令被拒。该结论仍受授权、后续存储校验与实际运行配置约束。

**MKT022-F2 [FIXED_SOURCE_AND_UPSTREAM_HTTP_TEST]：具有目标资源 Control 权限时，服务器存在 HTTP PUT 写入 ACR 的明确测试路径。**
`config/ldp/authorization/acp.json` 将 `.acr` 路由至 LdpHandler；`AuthAuxiliaryReader.ts` 将目标资源的 Control 权限映射为 ACR 的读写权限。`test/integration/AcpServer.test.ts` 的 `requires control permissions to access ACRs` 测试先确认未获授权的 PUT 返回401，授予公开 Control 后 PUT `.acr` 预期返回205，后续根容器 GET 预期200。该测试直接证明上游测试设计包含授权后 ACR HTTP PUT 成功路径；本轮没有独立执行 Jest，不应将测试预期冒充本轮观测。

**MKT022-F3 [FIXED_SOURCE]：写入存储层会调用 ACR 校验器，其已读实现验证 RDF 语法而未实施资源归属的语义绑定。**
`config/util/auxiliary/acr.json` 把 `AcrStrategy` 与 `MetadataStrategy` 放入 `RoutingAuxiliaryStrategy`；`RoutingAuxiliaryStrategy.validate` 将 `.acr` 转给 `AcrStrategy`。`DataAccessorBasedStore.writeData` 第482至485行调用 `auxiliaryStrategy.validate(representation)`。`ComposedAuxiliaryStrategy.validate` 将 representation.metadata.identifier 传给 `RdfValidator`。RdfValidator.ts 仅转换成 INTERNAL_QUADS 并读尽数据流以检查可解析性；没有比较 `acp:resource` 与 `.acr` 对应的资源 URL。已审链路未发现目标一致性校验，尚未排除未读中间件、定制部署或其他处理器。

**MKT022-F4 [FIXED_SOURCE_INFERENCE]：目标错配可能进入写入侧，但实际接收结果仍需合成 HTTP 负对照。**
MKT021 已确认 AcpReader 以 `iri === target.path` 决定直接 accessControl 与祖先 memberAccessControl 的选择。本轮证实 .acr 的 HTTP PUT 路径存在，并找到写入侧 RDF 语法校验调用。若具有 Control 权限的请求能保存有效 Turtle、却声明错误 `acp:resource`，则已读求值逻辑可能改变有效策略集合。这是条件性静态推断。**不能宣称真实漏洞、未授权攻击、实际绕过或任何已执行 HTTP 错配成功。** Control 权限是前提；授权者自身错误配置的风险与外部攻击应分别评估。

## 2. 后续独立合成验证协议候选

固定 v7.2.0、明确 ACP 预设、单独的内存和文件后端、合成用户与数据；先确认请求者对目标资源的 Control，记录同一凭据和相同父容器授权。对比以下结果，保存 HTTP 状态、读取回来的 ACR 内容、授权日志和 GET 权限：
1. ACR 声明正确目标，子资源 deny Read，父容器 member allow Read。
2. 仅将 ACR 的 `acp:resource` 改成父容器，其他字段不变；记录 PUT 是否拒绝及 GET 是否变化。
3. 在未获得 Control 时提交上述两个文件，要求拒绝写入。
4. Turtle 语法损坏时要求拒绝；语法合法但目标错配时确认是否有语义校验。
5. 同一 ACR 多个 `acp:resource` 与祖先权限冲突。
6. 对内存和文件后端分别重跑，并检查新请求与缓存失效。

以上均为**尚未执行的候选测试**。不能对真实个人 Pod、第三方服务或生产环境发起测试；若无法确认完全免费环境，则只保留离线设计和源码审查。

## 3. 心理史学候选方法映射

输入：目标资源 URL、ACR 路径、RDF acp:resource、WebID、clientId、issuer、祖先关系、请求模式。
状态：权限图、直接策略与成员继承策略、请求前后授权版本。
算法：先授权 Control 写入，再对 ACR 做 RDF 校验与保存；读侧从目标及祖先收集策略、按目标声明选择策略、计算 allow/deny。
目标：敏感领域数据的用途隔离与可验证撤权；不引入单一人生效用权重。
反馈与修正：未来应比较授权修改前后的完整访问矩阵，失败则保留原权限和可解释错误；尚无实测自我修正。
隐私：候选校验 ACR 实际所属资源与声明目标一致，并记录继承权限、客户端身份和缓存状态。
解释性：候选输出实际读取的 ACR、声明目标、命中策略、允许或拒绝原因；CSS 本身未验证提供用户可读解释。
费用：开源源码和公开规范免费阅读，本轮无部署、收费 API 或 CI。
局限：没有运行发行程序，未检查所有中间件，也没有验证第三方数据副本的撤销传播。MARKET E1 源码与上游测试设计证据；独立执行0，真人决策改善实证0。

## 4. E 当日治理检查与新增风险登记

2026-10-25 已有 E002 每日实质审计与 E003 R136 冻结负对照事件登记。本轮核查 main 最新提交、MKT001 至 MKT021、E002/E003、F001 及新 R145/R146 和 B 证据分类记录，不重复创建 E004，也未修改 R 系列、原始239索引、冻结协议或其他研究轨。

E 新增发现：
* B 轨 `B_R074_R075_EVIDENCE_TAXONOMY_HUMAN_TRANSFER_VS_HISTORY_2026-10-25.md` 发现 R074/R075 旧状态中的 E3 指独立真人实验跨研究迁移；当前统一口径 E3 指真实历史。两者应在新报告映射为 E2_EXTERNAL_HUMAN_EXPERIMENT_TRANSFER，保留旧标签以追溯。此为**证据分类冲突已登记**，不是新增历史 E3，也未擅改原冻结 JSON。
* R145 事前冻结提交 debede2a506fcd58ab848db336b16b946a7e7b4b，随后 JS 精确 Gram 与独立 Python 完整 KKT 复核12配置、192排列。R146 事前冻结提交18420b893e8137d0923ab3889dd3e3f32fa0f658，随后 JS 和独立 Python 对1171个人工经济作精确审计。两者仅内部 E1，新增方法远端 CI 均为 NOT_RUN；历史 CI 不覆盖新程序。
* R146 报告明确 `majority_pairwise_comparisons=516411` 为候选配对槽位上限，原 JS 存在提前终止，不能宣称全部配对实际执行；`budget_identity_world_grid_checks=5855` 采用同一表达式两份拷贝，独立财政检查由 Python 的24591项逐人账簿提供。该局限保留在科学报告中，未修改原始程序。
* A 轨 Andreoni/Miller 1993 的公开镜像已验证2800条真人行动与配对，但20个10轮区块缺少独立受试者场次证据；不能计为 R073 新独立 LOSO 验收，原始数据再分发许可亦未核实。
* original239 v7.8 仍记录239项、154项逐项证据待核，内部 schema/date 仍滞后。R136 冻结负对照历史失败保留。全仓冻结哈希和 GitHub 账单未做全面核验。未核验的新提交不得宣称 CI 成功。

## 5. F 本周状态与费用

F001（2026-W43）已完成，主题为人类否决权、最小采集与解释；本轮避免重复专题。F002 待下一周研究撤权、缓存、衍生数据及备份生命周期。本轮候选风险：拥有 Control 的合法管理者可因 ACR 目标错配造成意外权限变化，需在未来安全设计中提供语义校验和撤权后再读测试。仅原则性知识储备，不接入真实敏感数据，不提前开发个人决策产品。

研究顺序保持：完整 R 系列、系统归纳、最后模型熔炼。无产品或论文购买、注册收费服务、计费 API、付费 CI、云服务器/GPU、额外订阅；本轮主动新增费用0。账户整体账单和免费额度未独立核验。

next_action: MKT023 在固定版本中追踪 ACR HTTP PUT 的授权请求模式提取与请求级缓存边界；若无法获得新增证据，转向 Exist 的 OAuth 撤销和 ProjectionLab 的情景参数敏感性。E 下次检查 R074/R075 证据分类映射是否在新报告中正确采用，F 下周 F002。

## 6. 固定非中文原始来源

S1 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/config/ldp/handler/components/operation-handler.json
S2 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/config/util/auxiliary/strategies/meta.json
S3 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/config/util/auxiliary/strategies/acr.json
S4 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/config/util/auxiliary/acr.json
S5 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/config/ldp/authorization/acp.json
S6 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/http/ldp/PutOperationHandler.ts
S7 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/authorization/AuthAuxiliaryReader.ts
S8 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/storage/DataAccessorBasedStore.ts
S9 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/http/auxiliary/RoutingAuxiliaryStrategy.ts
S10 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/http/auxiliary/ComposedAuxiliaryStrategy.ts
S11 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/http/auxiliary/RdfValidator.ts
S12 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/integration/AcpServer.test.ts
S13 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/authorization/AcpReader.ts
S14 https://solid.github.io/authorization-panel/acp-specification/
S15 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R074_R075_EVIDENCE_TAXONOMY_HUMAN_TRANSFER_VS_HISTORY_2026-10-25.md
S16 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R145_DUAL_GRAM_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-25.md
S17 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R146_MEDIAN_TAX_INTEGER_GRID_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-25.md
S18 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/ANDREONI_MILLER_1993_HUMANLSTM_2800_ROW_PAIR_AND_SESSION_GATE_2026-10-25.md

commit_sha: 以 GitHub 写入后远端回读核验为准，不预填。
