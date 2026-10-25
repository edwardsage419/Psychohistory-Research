# MKT023：CSS v7.2.0 ACP 请求模式、授权缓存身份与权限更新可见性

date: 2026-10-25 (UTC+08)
track: commercial_market
status: COMPLETE_BOUNDED_FIXED_SOURCE_AND_UPSTREAM_TEST_AUDIT
preflight_main_head: ae7a755183e5daf48d55bd5a0e34d4bc4ba69a41
prior: MKT017 至 MKT022，特别是 MKT022 的 ACR HTTP PUT 授权与写入验证路径
scope: CommunitySolidServer/CommunitySolidServer 固定 v7.2.0 的源码、配置、单元测试、HTTP 集成测试；未安装服务器、运行上游测试或接入真实 Pod。

## 1. 新增机制事实及证据边界

### MKT023-F1：ACR PUT 的请求模式先按资源存在性提取，再映射为原资源 Control

[FIXED_SOURCE] MethodModesExtractor.handle 对已存在资源的 PUT 请求要求 write；新资源的 PUT 要求 append 与 create；GET/HEAD 要求 read。AuthAuxiliaryReader.findAuth 将针对 .acr 的权限查询转换为对应 subject 的 control 请求。interpretControl 在 subject control 为真时将授权文件上的 read、append、write、control 设为真。ParentContainerReader 另外根据父容器 append 计算 create。PermissionBasedAuthorizer 逐个检查所有 requestedModes，缺少任何必需模式均拒绝。因而合法 ACR 管理需要相关 Control 权限，是否允许新建还取决于创建和父容器权限路径。Control 是授权文档管理权限，不自动表示 subject 内容本身可读。

该结论来自固定代码的调用和分支结构。未独立执行全链 HTTP，不能将其扩大为所有部署配置的实测结果。

### MKT023-F2：AcpReader 的 ACR 数据去重缓存在一次 handle 调用内创建

[FIXED_SOURCE_AND_UPSTREAM_UNIT_TEST] AcpReader.handle 每次调用都执行 new IdentifierMap<IAccessControlledResource[]>，随后为本次 requestedModes 中各 target 传入同一个 resourceCache。重复祖先 ACR 读取通过 getDefault 去重。AcpReader.test.ts 的三个相关资源测试预期 acrStore.getRepresentation 总共调用三次，分别对应根、父和子，证实测试设计针对单次批量授权求值去重。此处未发现 AcpReader 自身的跨 handle 持久 ACR 缓存。

### MKT023-F3：外层 PermissionReader 另有 WeakMap 对象身份缓存，不能与 F2 混同

[FIXED_CONFIGURATION_AND_SOURCE_AND_UPSTREAM_UNIT_TEST] config/ldp/authorization/readers/default.json 将 PermissionReader 包装为 CachedHandler，缓存键为 credentials 与 requestedModes。CachedHandler.ts 使用嵌套 WeakMap，命中条件为这两个对象的引用身份相同，而非字段值相等；代码未设置基于 ACR PUT 的主动失效通知、TTL 或资源版本键。CachedHandler.test.ts 明确验证相同输入对象只调用一次 source，不同对象即使字段相同仍会重新调用；指定 fields 时复制外层对象但复用字段对象会命中缓存。

AuthorizingHttpHandler.handle 每次从 request 提取 credentials、从 operation 提取 requestedModes，再调用 permissionReader。正常独立 HTTP 请求通常有不同 request/operation 对象；是否出现跨请求复用同一 credentials 和 requestedModes 引用，需要检查实际运行上下文。故此处只能确认“对象身份缓存及无显式写后失效路径”，不能断言正常新请求使用陈旧权限，也不能保证所有自定义集成场景都即时刷新。

### MKT023-F4：已有上游 HTTP 测试覆盖一次授权增加后的新 GET，撤权负对照仍缺失

[UPSTREAM_TEST_DESIGN] AcpServer.test.ts 的 requires control permissions to access ACRs 用例依次要求：未授权 GET .acr 返回401；未授权 PUT .acr 返回401；测试夹具授予公开 Control 后 GET .acr 返回200；授权后的 PUT .acr 返回205；随后 GET 根容器返回200。最后一步表明上游测试设计确实检查 PUT 改变授权后的后续访问可见性。这是正向授权增加场景。当前审读的 AcpServer.test.ts 和 AcpReader.test.ts 没有直接覆盖“先允许 Read，撤回 Read，下一次 GET 必须拒绝”的反向路径；这一判断仅限于两份已读测试文件，不能称整个仓库完全缺少相关测试。

本轮未运行 Jest、真实 HTTP 请求或安装依赖。上游测试预期不是本轮执行观察；权限刷新和缓存行为的安全结论仍待独立合成验证。

## 2. 后续合成测试矩阵（全部未运行）

T01 授予公开 Read，随后撤销；在相同服务器进程内使用新 HTTP 请求验证第二次 GET 被拒，分别检查匿名、WebID、clientId、issuer。
T02 授予 Control 后 PUT 正确 ACR，再撤销 Read；比较授权文件回读、GET 结果和审计日志，确保写入成功与授权效果分开判定。
T03 保留相同 credentials 对象及 requestedModes 对象直接调用 CachedHandler，修改后端模拟权限；对照更换对象身份的调用，量化缓存命中边界。这是纯单元合成测试，不代表真实 HTTP 攻击。
T04 子资源显式 deny Read 与父容器 member allow Read 的正确目标 ACR，对照错误 acp:resource 目标声明，先验证 PUT 是否接收，再检查撤权后 GET。
T05 分别在内存和文件后端执行授权增加、撤销、重新授予；禁止复用真实个人账户、第三方 Pod 或敏感数据。
T06 逐次改变 clientId、WebID、issuer，检查身份隔离和未授权写入拒绝；并记录响应状态、授权版本、缓存键身份及实际 ACR 路径。

所有测试须在本地且确认零新增费用的合成环境运行。若无法确保依赖、设备和环境不收费，则保留测试设计，不启动 CI 或云计算。

## 3. 对心理史学未来个人决策系统的候选方法映射

| 维度 | 机制与候选借鉴 | 未验证边界 |
| --- | --- | --- |
| 数据输入 | 请求方法、目标 URL、WebID、clientId、issuer、ACR RDF、父容器关系、资源存在性 | 无真实健康、财务、关系数据 |
| 状态表示 | 请求的 read/write/append/create 模式、Control、权限策略版本、对象身份缓存 | 无个人偏好或人生状态建模 |
| 算法 | 请求模式提取、ACR 到 subject Control 映射、ACP allow/deny 求值、权限对象身份缓存 | 未独立执行上游实现 |
| 目标 | 细粒度数据隔离、合法撤权、授权状态可追溯 | 不预设唯一效用函数 |
| 反馈与自我修正 | 候选记录 PUT 前后策略、重读权限矩阵、发现撤权失败即报告阻塞 | 没有证实 CSS 自带自动修正机制 |
| 隐私权限 | 候选控制为撤权后新请求复核、缓存键与版本审计、客户端身份隔离、父子策略负对照 | 已下载第三方副本和衍生数据需另行管理 |
| 解释性 | 候选记录请求模式、目标、授权来源、命中策略、缓存状态、最终拒绝原因 | 未证明 CSS 向最终用户提供完整解释 |
| 费用 | 固定公开 MIT 开源源码与文档可免费审读 | 未部署，运维和账单未核验 |
| 可验证性 | 固定源码、配置、单元测试、HTTP 测试及六项合成协议 | MARKET 独立执行=0；个人决策效果实证=0 |

## 4. E 当日治理增量（只读）

已核对 2026-10-25 的 E002 正式每日审计和 E003 R136 事件审计，避免重复创建 E004。读取 main 最近提交、MKT022、F001、R147 新冻结协议及科学报告、B 独立审计和 A 数据源登记。

R147 新扩展先于执行冻结，冻结提交 5144933bdee0762e6f3223850222827b0fc85036，随后 JS 精确枚举 128 与 512 个人工世界；八个观测联合分布格子完全相同，两个结构因果模型的 do(A) 效应分别为0和1/4。B 使用 Python Fraction 在本地独立符号计算，报告11项检查通过，属于同项目不同算法的内部 E1。科学报告提交 a6766a341a706e844faf9f6fdd9e35383010b648 和 B 增量提交 9f45d7383a23081947c7e30f8a46455dfcfeac78 的 Actions head_sha 查询各返回 total_count=0。旧 R147 CI 不能为新实验背书。没有独立执行全套代码、核验冻结文件全仓哈希，也没有历史 E3 或真人 E2 新数据。

A 轨 Montero 2022 官方记录列出12场真人重复囚徒困境、188名参与者，固定配对六场92人，洗牌配对六场96人；官方 CSV/README 下载 HTTP403，行级字段、会话身份及许可仍未核验。不得纳入 R073 冻结模型的独立 LOSO 评分，不能计作新 E2。

直接读取 original239 v7.8 JSON，total_original_models=239，provisional_itemwise_audit_open_count=154，rows=239。内部 schema/date 仍标示 v7.6/2026-10-24，属于元数据滞后。R136 历史负对照失败与 R074/R075 旧 E3 真人标签冲突保持开放；未擅改任何研究轨、索引或冻结协议。未核验仓库全部提交、全仓哈希或账单。

## 5. F 本周专题状态

2026-W43 已有 F001 人类否决权、解释与最小采集专题，故本轮不重复建立 F 文件。下周 F002 继续研究授权撤回、缓存、备份、第三方副本及衍生数据生命周期。本轮新增候选风险：同一权限对象引用复用可能保留旧判断，授权增加的测试成功不能证明撤权同样成功。需使用新的请求、变化后的身份及版本标识进行合成负对照。无真实敏感数据或个人决策产品开发。

## 6. 科学与费用边界

证据等级：MARKET FIXED_SOURCE、FIXED_CONFIGURATION、UPSTREAM_TEST_DESIGN、COMMUNITY_EDITOR_DRAFT。MKT023 新增的是请求模式与两层缓存身份机制的可复核源码事实，以及一次正向授权变更后的上游 HTTP 测试设计。尚无独立服务器运行、跨环境安全证明、个人长期决策改善证据。不能把缓存设计的潜在陈旧命中描述为已确认漏洞。

主动新增费用为零：未购买产品或论文、注册收费服务、调用计费 API、启用 CI、租云服务器/GPU、接入敏感数据或增加订阅。GitHub 免费额度和账户账单未独立核验。研究顺序仍为完成 R 系列、统一归纳分类、最后模型熔炼；本轨仅储备候选知识。

next_action: MKT024 优先检查固定版本 ACP 的撤销权限测试覆盖及授权后新请求的对象生命周期；若无新增证据，转向 Exist OAuth 撤销或 ProjectionLab 参数敏感性和解释性，保持产品覆盖广度。E 继续核查 R147 新 CI 与 R073 独立数据门槛；F002 下周启动。

## 7. 非中文原始资料

S1 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/authorization/permissions/MethodModesExtractor.ts
S2 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/authorization/AuthAuxiliaryReader.ts
S3 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/authorization/ParentContainerReader.ts
S4 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/authorization/PermissionBasedAuthorizer.ts
S5 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/authorization/AcpReader.ts
S6 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/config/ldp/authorization/readers/default.json
S7 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/util/handlers/CachedHandler.ts
S8 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/unit/util/handlers/CachedHandler.test.ts
S9 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/unit/authorization/AcpReader.test.ts
S10 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/integration/AcpServer.test.ts
S11 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/server/AuthorizingHttpHandler.ts
S12 https://communitysolidserver.github.io/CommunitySolidServer/7.x/usage/authorization-methods/
S13 https://solid.github.io/authorization-panel/acp-specification/
S14 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R147_POSITIVE_OVERLAP_OBSERVATIONAL_TWINS_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-25.md
S15 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R147_POSITIVE_OVERLAP_SYMBOLIC_INDEPENDENT_E1_AUDIT_2026-10-25.md
S16 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/MONTERO_2022_12_SESSION_FIXED_SHUFFLED_PD_SOURCE_GATE_2026-10-25.md
S17 https://github.com/edwardsage419/Psychohistory-Research/blob/main/docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v7.8_2026-10-25.json

commit_sha: 由 GitHub 提交返回并在远端回读后核验，文内不预填。
