# MKT021：CSS v7.2.0 ACR 目标绑定、RDF 校验边界与负对照设计

date: 2026-10-25 (UTC+08)
track: commercial_market
status: COMPLETE_BOUNDED_FIXED_SOURCE_AUDIT
preflight_main_head: f9d4b45b1952761cde9c03f29d92cd341d4e3943
prior: MKT017–MKT020，尤其 MKT020 的子资源 ACR 目标身份测试夹具问题
scope: 固定 CommunitySolidServer/CommunitySolidServer v7.2.0，源码、测试、配置、ACP Editor's Draft 只读审查；无真实用户数据、安装运行或计费行为。

## 1. 本轮新增的可复核机制事实

**MKT021-F1 [FIXED_SOURCE]：ACR 文件位置与 acp:resource 声明分别进入求值链，当前读取函数以声明 IRI 决定采用直接策略还是成员策略。**

固定源码 AcpReader.ts 的 extractPermissions 首先沿目标及全部祖先标识逐一读取对应的 .acr 文档；readAcrData 使用 acrStrategy.getAuxiliaryIdentifier(identifier) 定位文件。AcpUtil.ts 的 getAccessControlledResources 从该 RDF 文档枚举所有 acp:resource 三元组，产生独立的受控资源 iri。AcpReader.ts 的 getEffectivePolicies 只检查 `iri === target.path`：相等时取 accessControl；不等时取 memberAccessControl。该函数没有把 iri 与当前正在读取的 ACR 所属 identifier 再作相等或祖先关系验证。若 ACR 内 acp:resource 错指其他资源，策略选择会随之改变。这里确认的是固定代码的分支条件；未证明生产 HTTP 可写入此类文档，也未证明存在真实越权。

**MKT021-F2 [FIXED_CONFIGURATION_AND_SOURCE]：已审 ACP ACR 配置使用 RDF 语法校验，尚未看到 acp:resource 与实际 .acr 所属资源的语义绑定校验。**

config/util/auxiliary/strategies/acr.json 为 AcrStrategy 配置 RdfValidator，并将后缀设为 .acr。RdfValidator.ts 调用 RepresentationConverter 将内容转换为 INTERNAL_QUADS，读尽流以确保 RDF 可解析；其 handle 代码没有读取 acp:resource 并对照 identifier。RdfValidator.test.ts 验证转换成功、转换失败与内部四元组格式直通，没有目标身份约束断言。config/ldp/authorization/readers/acp.json 将 AcpReader 接到该策略。结论限定于已读配置和校验函数；整个写入管线是否还有额外语义约束尚未完成穷尽审查。

**MKT021-F3 [FIXED_TEST]：现有继承测试的错配确实降低了直接子策略的鉴别力。**

AcpServer.test.ts 的继承用例向 target.acr 写入 createAcr({resource: baseUrl, policies: [allow Write]})，虽然目标资源是 target。AcpHelper.ts 的 createAcr 将 resource 原样写成 acp:resource，setAcp 则将文档写入目标的 .acr。按 F1 的读取条件，这一 allow Write 不能作为 target 的直接 accessControl；父容器 member allow Read 足以解释最终 GET 200。AcpReader.test.ts 的正确组合用例则明确让子 ACR 的 acp:resource 指向子目标，证实夹具的差异。两项都属于上游测试源码审读，本轮没有执行 Jest 或 HTTP 测试。

**MKT021-F4 [PRIMARY_DRAFT]：ACP 2022-09-29 Editor's Draft 第 4.1、6.2、6.3 节将直接策略绑定于资源自身的 ACR，将继承成员策略绑定于祖先 ACR，并规定满足的 deny 覆盖 allow。**

草案属于持续修订的社区规范参考。它支持将 ACR 目标身份错配作为应测风险，不自动证明 CSS 实现不合规，也不能代替真实请求测试。

## 2. 最小合成负对照矩阵（待实际执行）

假设目标 /foo，父容器 /，匿名上下文，父 ACR 声明 acp:resource=/ 且 memberAccessControl 允许 Read，测试固定在相同凭据、相同服务器配置和相同存储后端下进行。

| ID | 子文件 /foo.acr 内的声明和策略 | 按已读源码的有限静态预期 | 独立验证 |
| --- | --- | --- | --- |
| T01 | acp:resource=/foo；accessControl deny Read | 祖先 allow Read 与子 deny Read 同时有效，底层 deny 优先，GET 应拒绝 | 未运行 |
| T02 | acp:resource=/；accessControl deny Read | 子策略因 iri!=target 被跳过；父 allow Read 可能使 GET 通过 | 未运行 |
| T03 | acp:resource=/；memberAccessControl allow Read；父 ACR 无允许 | 子文件中的成员策略可能被误选为 /foo 的有效策略 | 未运行 |
| T04 | acp:resource=/foo；accessControl allow Write；父 member allow Read | GET 应受祖先 Read 允许；直接 Write 仅贡献写权限 | 未运行 |
| T05 | 一份 ACR 包含两条 acp:resource，其中一条指向 /foo，另一条指向无关 URL | 读取器会枚举两个声明，需检查策略重复与不相关成员策略污染 | 未运行 |
| T06 | T01 与 T02 在内存和文件后端、经真实 HTTP PUT 写入后重复 | 区分读侧静态行为与写侧验证是否拒绝错误声明 | 未运行 |

T01 至 T05 是源码分支推导的候选预期，**不是已观测的 HTTP 结果**。尤其 T02/T03 的风险取决于写入权限、实际存储验证、身份校验和是否可提交此类 ACR；当前不能认定为安全漏洞。若写入阶段拒绝错配 ACR，应登记为安全边界成功，不能把读侧静态条件等同实际漏洞。测试只能在离线合成数据和免费环境执行，严禁接入真实个人 Pod。

## 3. 对未来心理史学决策系统的候选知识映射

| 维度 | 具体机制及候选借鉴 | 限制 |
| --- | --- | --- |
| 输入 | 请求目标 URL、WebID、clientId、issuer、RDF 授权资源、祖先容器关系 | 没有任何真实健康、财务或关系数据 |
| 状态表达 | 每资源 ACR、策略 allow/deny、继承关系、声明资源 IRI | 不表达人生状态和偏好 |
| 算法 | 先定位 .acr 文件，再解析 acp:resource 和策略，合并有效策略后求值 | 当前仅源码审读，未执行上游算法 |
| 目标 | 数据来源与应用权限隔离；撤权可解释和可复核 | 无人生目标优化或效用权重 |
| 反馈与自我修正 | 授权文件更新后重新求值的设计；候选记录变更前后差异 | 缓存、令牌和副本撤销未测试，无自动学习 |
| 隐私与权限 | 候选要求：校验授权文档实际归属与声明目标一致；对祖先继承和显式拒绝设负对照 | 第三方已下载副本与衍生统计无法由 GET 拒绝自动清除 |
| 解释性 | 每次决定记录实际读取的 ACR 路径、声明目标、命中策略及最终结果 | 当前没有证明终端用户可见解释 |
| 费用 | v7.2.0 package.json 声明 MIT，固定公开源码免费阅读 | 自建部署有设备运维成本，本轮未部署或注册服务 |
| 可验证性 | 固定源码、配置、单测与六项合成测试矩阵 | MARKET 独立运行=0，真人长期决策效果=0 |

## 4. E 当日治理检查（只读，避免重复归档）

2026-10-25 已有 E002 当日跨轨实质审计与 E003 R136 冻结负对照事件审计。本轮核查 main 最近提交、market MKT001–MKT020、E002/E003、F001、R143/R144 新报告及 original239 v7.8，未重复创建 E004，未修改其他研究轨或索引。

R143：事前冻结 a92d93018ce1816c947d216610935b506e001b9a，独立 B 冻结 b21936d7746311860fa208a0a922f62b96de2ba6；新增九个人工机制世界的 Cramer、路径树与前向递推内部复核。九组完整 CSV 已归档，完整 JSON 报告注明本地生成、未上传。新增程序 CI=NOT_RUN；只能称有界内部 E1。

R144：事前冻结 342db052ba928564b8d421426d1daa6505a388b1，结果提交在后。位编码方法穷举7776条人工历史和38880个配对反事实，机器 JSON 与源码已在仓库。报告记录终点响应签名类别 7298/365/96/17，属于内部人工状态机 E1，非真实历史 E3。针对最新科学报告提交 9e696eb9e200da02f1df244098122c19e08e2b66 查询 GitHub Actions，total_count=0，不能将旧 CI 视为本次新算法验收。

原始239项交叉索引最新文件 v7.8 仍报告 total_original_models=239，待逐项证据审计154，内部 schema/date 字段仍滞后至 v7.6/2026-10-24。R136 冻结负对照失败的历史记录继续开放。A 轨 DFS2020 已登记派生 input 与同回合 choice 的目标泄漏风险，二进制原始行仍未读取；不能计作 R073 新独立 E2。最新理论轨 TH024 提交可见，未审全文。没有检查所有冻结文件哈希或 GitHub 账单，未推断未核验提交/CI 已完成。各轨研究文件、索引及冻结协议均保持原样。

## 5. F 本周专题状态

2026-W43 的 F001 人类否决权、解释、最小采集已归档；本轮不重复立项。F002 计划研究撤权和数据生命周期，增加本轮具体风险：撤权时同时检查授权文档的实际位置、acp:resource 声明、祖先策略、客户端身份、缓存和历史副本。拒绝未来访问与删除既往数据分别记录。仅候选原则，无真实敏感数据、无个人决策产品开发。

## 6. 证据边界、阻塞与下一项研究

证据：MARKET E1 为固定上游源码、配置、测试文本与 ACP Editor's Draft；MARKET 独立运行=0，真实个人决策改善实证=0。MKT021 新增的是目标绑定及语法验证边界的源码路径证据。风险等级：需合成测试的候选权限风险。营销资料、规范草案、代码、测试设计、实际执行和推测严格区分。

本轮未购买论文或产品、注册收费服务、使用计费 API、启动收费 CI、租服务器/GPU 或接入个人数据；主动新增费用 0。账户账单与免费额度未独立核验。研究顺序仍为完整 R 系列、系统归纳、最后模型熔炼；市场/E/F 都仅作为知识储备。

next_action: MKT022 优先追踪 CSS v7.2.0 ACR 的真实 HTTP 写入验证管线与可拒绝的 acp:resource 错配；如证据仍不足，转向 Exist OAuth 撤销和 ProjectionLab 情景参数来源与敏感性。F002 下周按独立路径研究授权撤销与数据生命周期。

## 7. 原始非中文来源

S1 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/authorization/AcpReader.ts
S2 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/authorization/AcpUtil.ts
S3 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/http/auxiliary/RdfValidator.ts
S4 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/config/util/auxiliary/strategies/acr.json
S5 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/config/ldp/authorization/readers/acp.json
S6 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/integration/AcpServer.test.ts
S7 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/unit/authorization/AcpReader.test.ts
S8 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/util/AcpHelper.ts
S9 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/unit/http/auxiliary/RdfValidator.test.ts
S10 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/package.json
S11 https://solid.github.io/authorization-panel/acp-specification/
S12 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R143_ARRIVAL_TIE_BIAS_CRAMER_PATH_ENUM_SCIENTIFIC_REPORT_2026-10-25.md
S13 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R144_BITPACKED_ONE_STEP_RESPONSE_IDENTIFIABILITY_SCIENTIFIC_REPORT_2026-10-25.md

commit_sha: 待 GitHub 写入后核验；不预填。
