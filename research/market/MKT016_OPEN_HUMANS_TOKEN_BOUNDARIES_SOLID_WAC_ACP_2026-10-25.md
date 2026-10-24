# MKT016 Open Humans 主令牌与 Solid Pods WAC/ACP 访问控制对照

date: 2026-10-25 (UTC+08)
track: commercial_market
status: COMPLETE_BOUNDED_OFFICIAL_DOC_AND_SPEC_REVIEW
observed_main_head_before_write: 932d546eb651f1ab00e5990dc9dd267f5d891897
preflight: 已读 main 最新 HEAD、MKT001 至 MKT015、E001/E002/E003、F001 与当日研究登记。研究焦点是 MKT015 尚未展开的令牌权限范围及 Solid 资源访问控制。无账户注册、真实令牌、敏感数据或软件部署。

## 1. 新增事实及证据等级

MKT016-F1，MARKET-E1，Open Humans 官方 OAuth2 data access 文档：用户级 access token 可经 /api/direct-sharing/project/exchange-member/ 获取本成员项目 ID 和授权文件信息；项目 master access token 可结合 project_member_id 访问项目成员数据，还能经 /api/direct-sharing/project/members/ 枚举项目成员及文件。官方说明 master token 可访问分享给该项目的私有数据、发送消息和上传文件，并建议 OAuth2 项目尽量使用用户专属端点。主令牌泄露会扩大多个成员的数据暴露面，属于基于权限文档的风险推断，尚未测试服务器。

MKT016-F2，MARKET-E1，Open Humans 官方 OAuth2 setup：授权码换取 access_token、refresh_token、expires_in，refresh_token 可换新令牌。成员可撤销项目授权，扩大请求权限需重新授权。文档不足以证明所有缓存、刷新令牌与外部副本在撤权后同时删除。官方将 master token 视为项目密码，明确禁止放进 Git 仓库，疑似泄露需联系支持重置；其上传接口允许 Authorization header。候选建议是避免在 URL 查询串、日志、共享文件中暴露令牌，优先最小权限用户令牌。未审计实际日志。

MKT016-F3，SPEC-PRIMARY，Solid WAC 1.0.0 社区报告，2024-05-12：以资源 ACL 表达 acl:Read、acl:Write、acl:Append、acl:Control；无独立 ACL 表示的子资源可继承最近容器的有效 ACL。撤权须检查显式 ACL、上级继承、组与公开权限。该报告并非 W3C 正式标准，实际部署是否正确执行尚未验证。

MKT016-F4，SPEC-PRIMARY，Solid ACP 社区草案：Policy 支持 acp:allow、acp:deny、allOf、anyOf、noneOf，并能以 agent、client、issuer 等属性匹配。与只按用户 WebID 表达的 WAC 权限相比，ACP 可约束客户端身份。Solid-OIDC 负责身份认证，身份成立并不自动代表对某个资源拥有读取授权。

MKT016-F5，IMPLEMENTER-E1，Community Solid Server v7 官方授权方法说明：WAC 模式下多个应用使用同一获授权 WebID，恶意应用可能访问原本供其他应用使用的数据；ACP 可限制具体客户端。v7 配置生成器允许 WAC、ACP 或关闭授权，关闭授权将使全部资源可读写。既有 WAC 服务器迁移到 ACP 必须更换相应授权资源，不能认为格式直接兼容。这是本轮最重要的新增可核查产品实现差异。

MKT016-F6，IMPLEMENTER-E1，Community Solid Server 官方功能与 LICENSE：支持 RDF/普通二进制资源、文件系统/内存/SPARQL 等存储选项；内存数据可能在重启后消失；源码采用 MIT 许可证。现有设备上的本地开源研究无需购买软件，但云托管、运维、网络暴露和额外设备均可能产生费用，当前禁止部署付费方案。

## 2. 统一产品观察矩阵

| 维度 | Open Humans | Solid / Community Solid Server |
| --- | --- | --- |
| 输入 | 用户授权来源文件、项目上传数据、标签 | RDF/HTTP 资源与二进制文件，视应用而定 |
| 状态表达 | 项目、成员 ID、来源权限、文件元数据 | Pod 资源树、ACL/ACP、WebID、client/issuer |
| 算法 | OAuth2 授权码与刷新、成员枚举、项目/用户级令牌 | WAC 有效 ACL 查找、ACP matcher、Solid-OIDC |
| 目标 | 参与者个人数据控制和研究授权 | 跨应用数据互操作和资源访问控制 |
| 反馈与修正 | 撤权、重新授权、项目移除、文件删除 | 修改访问策略、拒绝请求、迁移授权规则 |
| 隐私 | 主令牌跨成员权限；外部下载副本无法自动回收 | WAC 同身份跨应用权限风险；ACP 客户端隔离；ACL 继承风险 |
| 解释性 | API 和授权范围可审查；缓存与外部副本未知 | 规则可检查；多级继承与策略组合提高审计难度 |
| 费用 | 官方声明建项目免费，初始 20 人上限 | MIT 开源，现有设备可本地运行；额外托管费用未获零费用保证 |
| 局限 | 未验证撤权传播时延和真实外部删除 | 未运行服务器、未独立测试权限迁移与备份清理 |

两者都没有公开证明长期个人决策改善的独立试验，也未提供已验证的统一人生效用权重、跨领域因果模型或长期优化算法。

## 3. 风险与零新增费用候选测试

R1 HIGH，master token 的项目范围暴露。候选控制：最小权限、用户级令牌优先、隔离日志与凭证。合成测试：用户 A 令牌不能访问 B 数据。
R2 HIGH，WebID 身份授权被误当作客户端授权。候选控制：需要应用隔离时研究 ACP client matcher。合成测试：同一 WebID 的两个应用只能访问各自获授权资源。
R3 HIGH，父容器 ACL 继承导致撤权遗漏。候选控制：有效权限计算覆盖上级容器、组及公开规则。合成测试：删除局部规则后验证继承权限。
R4 HIGH，令牌失效不能回收已下载文件及派生统计。候选控制：分层副本登记与第三方删除回执。合成测试：撤权后读取拒绝，外部副本标 UNKNOWN。
R5 MEDIUM，CSS 误配置为关闭授权或 WAC/ACP 迁移不兼容。候选控制：拒绝无授权配置，迁移前后回归检查。
R6 MEDIUM，URL 查询串令牌泄露。候选控制：Authorization header、日志脱敏、令牌轮换。
R7 MEDIUM，规范草案与产品实测混用。候选控制：记录规范版本、服务器版本、测试环境与实际复现证据。

以上七项均为 TESTS_PROPOSED_NOT_RUN；不开发个人决策产品，不接入用户真实敏感数据，不改变任何冻结协议。

## 4. E 与 F 独立工作流状态

2026-10-25 E002 已完成每日跨轨实质审计。其后 R136 出现事前冻结 q2/q3 错序负对照 FAILED_NONDISCRIMINATING，已在独立 E003 增量只读审计登记。本轮额外用 Fraction 检查 R136 报告中的两组精确收益见证，二者 ZD 残差均为零，印证负对照无法鉴别排序错误；未重跑完整 1215 行。R136 CSV 尚未上传，查询新报告提交的关联 CI 为零，不能宣称新 CI 验收。original239 v7.8 仍有 154 项待逐项审计；schema 内部版本仍为 v7.6。A 的空间重复博弈 Dryad 数据仍有 403 下载阻塞，未产生 E2。

2026-W43 F001 已完成“人工否决与最小数据”专题。本轮新增 F002 候选案例：身份与应用授权分离、继承权限撤回、令牌吊销和衍生数据生命周期。F002 尚未正式执行，本周不重复创建。

## 5. 科研证据、费用与下一轮

MARKET-E1 为官方技术文档与实现者说明；SPEC-PRIMARY 为社区规范草案；MARKET-INFERENCE 为候选风险；MARKET-E2 独立实测为零，MARKET-E3 长期决策效果验证为零。与 R 系列 E1/E2/E3 严格分开。

本轮仅使用公开非中文文档、现有 ChatGPT 和 GitHub 权益；没有注册、购买、计费 API、收费 CI、云服务、GPU、额外订阅或真实个人数据。主动新增费用 0；未核验账户整体账单或免费额度。

next_action: MKT017 深读 Community Solid Server v7 的 WAC/ACP 配置、客户端匹配、ACL 继承与撤权测试源码及更新日志，验证实现与文档的一致性。若无新增可核查内容，转向 Exist API 数据授权撤销或 ProjectionLab 情景模拟输入假设。先完成全部 R 系列，再归纳分类，最后熔炼。

## 6. 非中文公开来源（2026-10-25 审读）

S1 https://www.openhumans.org/direct-sharing/oauth2-data-access/
S2 https://www.openhumans.org/direct-sharing/on-site-data-access/
S3 https://www.openhumans.org/direct-sharing/oauth2-setup/
S4 https://www.openhumans.org/direct-sharing/oauth2-member-removal/
S5 https://www.openhumans.org/direct-sharing/oauth2-data-upload/
S6 https://solidproject.org/TR/wac
S7 https://solidproject.org/TR/acp
S8 https://solidproject.org/TR/oidc
S9 https://communitysolidserver.github.io/CommunitySolidServer/7.x/usage/authorization-methods/
S10 https://communitysolidserver.github.io/configuration-generator/v7/
S11 https://communitysolidserver.github.io/CommunitySolidServer/7.x/features/
S12 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/main/LICENSE.md
S13 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/operations/E003_R136_FROZEN_NEGATIVE_CONTROL_INCIDENT_DELTA_2026-10-25.md
