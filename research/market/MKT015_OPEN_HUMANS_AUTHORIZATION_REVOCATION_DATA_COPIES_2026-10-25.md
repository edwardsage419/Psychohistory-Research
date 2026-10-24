# MKT015 Open Humans 项目级授权、撤回与数据副本生命周期审读

run_date: 2026-10-25（UTC+08）
track: commercial_market
subflow: product
status: COMPLETE_BOUNDED_OFFICIAL_DOCS_AND_ORIGINAL_PAPER_REVIEW
observed_main_head_before_write: 5ac566bc9809799889c5db4636d162a1a94171fb
scope: 公开非中文官方文档、数据使用政策、2019 年开放原始论文及公开 API 文档。仅做只读研究，没有账户注册、数据上传、API 调用、付费订阅、CI 或真实个人数据。

## 1. 与 MKT014 的实质差异

MKT014 研究 ActivityWatch Research Edition 最终编译产物的隐私保护来源。本轮转向 Open Humans 的项目级授权机制，重点研究授权撤销与数据删除的操作顺序、平台副本与外部副本责任边界。两项研究对象和证据不同，不重复之前的 Tauri 构建审计。

**MKT015-F1，官方技术文档支持：授权和项目上传文件删除是两个不同操作。**

Open Humans 提供 OAuth2 项目和 on-site 项目。项目请求特定来源的数据访问，用户通过项目授权后，项目可以通过 API 访问对应来源。成员默认使用项目专属随机标识，用户名另需请求授权；这只是降低直接身份关联的措施，不等于对高维健康、位置、遗传数据的匿名化证明。

用户可在连接管理页面撤回项目授权，文档明确撤回立即阻止后续共享、上传和消息权限。项目管理者的 member removal 也撤销继续访问的权限。然而 member removal **不会自动删除该项目此前上传到成员账户的数据**。官方建议项目如需清除自己上传的数据，应先执行文件删除，再移除成员。OAuth2 的删除接口支持按 file_id、文件名或 all_files 删除项目上传到成员账户的文件。已经由外部研究者下载的副本不属于该 API 的删除范围。

**MKT015-F2，官方政策支持：账户删除与备份清除存在时间差。**

数据使用政策写明，账户或文件删除会立即从当前账户数据库及关联文件中移除；受限存储中的安全备份会在 60 天后永久删除。政策允许某些既往公开内容继续显示，例如评论。政策同时明确第三方研究者对其自身数据处理承担责任，Open Humans 无法控制这些第三方如何保存、使用和删除数据。

这形成三种不同的撤销边界：
1. 撤销项目授权：停止项目未来经平台授权的读取、上传和消息操作。
2. 删除平台文件或账户：删除平台当前可用副本，备份有最长 60 天的政策周期。
3. 已复制到项目服务器、研究者本地、外部备份或公开下载的数据：须由对应接收方依据其承诺和适用规则另行处理；平台无法直接保证这些副本删除。

2019 年论文也区分成员退出项目与项目上传数据是否保留，且允许成员选择保留或删除部分上传数据。论文是平台设计与案例描述，不是删除有效性的独立渗透测试或长期决策收益实验。

**MKT015-F3，官方文档支持：授权范围与研究同意的职责分离。**

OAuth2 项目可按来源请求权限，用户名默认不共享，消息可使用项目内随机标识。官方要求 OAuth2 项目在自身网站或应用处理研究同意和使用条款，再转至 Open Humans 完成项目授权。对研究项目，扩大 20 人初始上限需要审核；涉及研究的项目审批要求 IRB 或等效伦理审查材料。不能把 OAuth 授权界面等同于完整研究知情同意，亦不能将通过社区审批推定为已验证的安全性。

## 2. 产品和方法观察矩阵

产品及组织：Open Humans，非营利个人数据管理与参与式研究平台，公开官方项目文档和 2019 年开放论文。

真实输入：项目可导入可穿戴设备、遗传数据、位置记录、连续血糖、社交或个人上传文件；具体来源受用户选择、上游导入项目与权限控制约束。本文未读取任何用户数据。

状态表达：成员账户下的数据文件、描述与标签元数据、来源项目、项目级成员随机 ID、用户授权的来源关系；并未见统一的人生状态向量或经验证的跨领域效用函数。

算法和接口：OAuth2 与 on-site 授权、项目级来源选择、项目 API 读取和上传、项目成员撤销、文件 ID/文件名/全部文件删除。公开 Python API 客户端支持相应调用。未审计服务器运行代码、访问控制单元测试或实际权限失效时间。

目标：支持参与者掌控个人数据汇集、授权和参与研究。平台的科学目标与个人长期决策优化目标不同。

反馈与自我修正：成员可查看共享关系、撤销或重新授权、删除账户及文件。授权变更提供治理反馈；未见官方公开的跨生活领域目标优化、概率预测校准、自动学习人生偏好或因果效果评价算法。

隐私权限：来源级授权、项目内随机 ID、用户可撤销项目权限、项目上传文件单独删除、备份最长 60 天、外部副本另由第三方负责。随机 ID 不消除重识别风险。

解释性：API 文档和数据使用政策使权限状态与删除流程可追踪。第三方下载后的用途、派生统计、衍生模型、研究发表成果与外部备份没有统一可审计的回收证明。

费用模式：官方联系页面宣称创建项目免费，OAuth2 初始 20 人上限，公开文档和论文可免费阅读。本项目只做文档研究，未注册、创建项目、触发 API 或支付任何费用。平台免费声明不能推定未来全部集成成本均为零。

产品局限：跨项目数据格式与测量误差、权限范围、跨主体数据治理、外部副本撤回、历史备份和衍生推断删除。尚无证据证明其提高个人长期决策质量。

## 3. 可检验的候选控制与风险

MKT015-R1 HIGH：项目撤权后，第三方先前下载的文件仍可留存。候选控制：按来源、接收方、文件身份和授权版本登记副本，撤回时向各接收方生成删除义务清单；仅有可核查回执才标记为确认清除。未来合成测试，未执行。

MKT015-R2 HIGH：先移除成员可能失去项目对原上传文件的清理权限。候选控制：事务性撤销状态机采用“暂停新访问、枚举项目文件、执行删除、验证结果、撤销项目成员、审计外部副本”顺序；任何失败显式留待处理，不自动宣称全部删除。该顺序是研究建议，尚未验证为官方所有场景的最佳做法。

MKT015-R3 HIGH：平台文件删除与 60 天备份保留并存。候选控制：分别记录 active_deleted_at、backup_expiry_policy、backup_purge_evidence、external_copy_status，用户界面明确时间差和未知。未运行。

MKT015-R4 HIGH：位置、遗传、健康时间序列可通过组合特征重识别，项目内随机 ID 不能作为匿名性充分条件。候选控制：默认用途隔离、细粒度来源权限、聚合与最小化、第三人数据排除；未来用纯合成数据检验跨源链接风险。未运行。

MKT015-R5 MEDIUM：授权范围变化需要成员重新授权。候选控制：权限版本固定，升级权限时重新提示并拒绝旧授权自动扩大；未来以合成令牌状态验证。未运行。

MKT015-R6 MEDIUM：OAuth2 项目研究同意与平台技术授权分离。候选控制：研究目的、用途、接收方、保留期、撤销限制和争议渠道分别记录；无法证明同意有效时停止数据流。未运行。

MKT015-R7 MEDIUM：外部项目可能生成衍生评分、图谱关系或模型参数。候选控制：原始文件、派生特征、缓存、模型输入、报告与不可撤销公开成果分层登记；不承诺不可实现的完整回收。未运行。

候选零费用合成测试：权限 A 与 B 分源访问、撤权后读取拒绝、先删文件再撤项目、反向顺序负对照、备份到期状态、外部副本无删除回执、权限扩大需再授权、匿名 ID 跨来源链接风险。均为 TESTS_PROPOSED_NOT_RUN。

## 4. 证据等级和科研边界

MARKET-E1：官方 OAuth2 features、member removal、data upload/delete、setup、data use policy、contact 页明确说明的机制与政策。
MARKET-PRIMARY-PAPER：2019 年 GigaScience 论文 DOI 10.1093/gigascience/giz076，平台设计、参与者控制及历史案例的原始描述。2019 年统计与当下产品规模不可混用。
MARKET-INFERENCE：基于上述机制提出的撤销状态机、权限版本控制和删除回执设计。
MARKET-UNVERIFIED：真实服务器撤权即时性、第三方删除履约率、备份实物清除、独立安全审计、长周期人生决策改善效果。

以上证据等级与 R 主线内部合成 E1、真人 E2、历史 E3 严格分开。平台权限文档不构成心理史学模型的预测验证。

## 5. E 当日治理增量

今日已有 `research/operations/E002_READONLY_PROJECT_AUDIT_2026-10-25.md`，本轮不重复创建 E003 或改写其他研究轨。

读取最新 main HEAD 为 `5ac566bc9809799889c5db4636d162a1a94171fb`，近期 TH018 已新增理论归档并更新索引；R134、R135 均先冻结第三方法协议再提交有限人工数学结果。R134 报告列出 81 组局部分类、11664 组入侵组合，明确新 CI 未执行、E2/E3 均为零；R135 报告列出 4096 规则、64 固定点和 2080 镜像轨道，明确未重跑原 ESS 全量扫描、新 CI 未执行。只读 GitHub Actions 查询 R134 报告提交 `166edefa757ccac4ebdce58d74057902b8fa26f8`、R135 报告提交 `872f5af1d259a28dde057b4b58b6bd7c8d348e4f` 均返回 0 个关联 run。此查询只覆盖指定 SHA，不能推断其他历史 run 不存在，也不能将本地跨语言一致性当成外部独立复现。

直接解析 original239 v7.8 JSON：`total_original_models=239`、`rows.length=239`、`provisional_itemwise_audit_open_count=154`；其 `schema` 字符串仍标记 v7.6，`date` 仍为 2026-10-24。版本元数据滞后问题继续开放。R134、R135 新增内部 E1 不自动改变 154 待审数量。没有独立逐行重算 R134、R135 或全仓冻结协议哈希，不能声称全仓科学验收或冻结完整性已核验。

## 6. F 本周专题状态

2026-W43 已有 `research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md`，完成本周人类否决与最小数据专题。避免重复写 F001。下一周 F002 研究授权撤回与数据生命周期，可直接复用本轮 Open Humans 官方机制作为案例，重点区分平台撤权、原始文件删除、第三方副本、衍生数据和备份 60 天周期。F002 尚未正式执行。未接入用户真实敏感数据或开发个人决策产品。

## 7. 并发、归档和费用

写入前复核 main HEAD、research/market 现存 MKT001 至 MKT014、research/operations 今日 E002、research/privacy_safety 本周 F001，确认目标 MKT015 路径尚不存在。仅向 market 独立新文件增量归档；若并发出现同名文件，不覆盖其他研究轨。提交后须回读 GitHub commit SHA 与文件 blob，确认实际远端状态。

本轮未注册服务、购买论文或产品、使用计费 API、云服务器/GPU、触发收费或免费 CI、接入个人敏感数据。主动新增费用为 0，整体账户账单及免费额度未独立核验。

研究顺序不变：先完成全部 R 系列，再系统归纳分类，最后模型熔炼。商业研究、E、F 均为候选知识储备，不修改冻结协议或预设唯一人生效用权重。

next_action: MKT016 研究 Open Humans 项目主访问令牌与用户级 OAuth2 token 的权限边界、外部副本删除责任，或比较 Solid Pods 的本地/用户控制与撤权可验证性。优先官方技术规范、固定源码及免费原始研究。

## 8. 来源（非中文，2026-10-25 访问）

S1 https://www.openhumans.org/direct-sharing/oauth2-features/
S2 https://www.openhumans.org/direct-sharing/oauth2-member-removal/
S3 https://www.openhumans.org/direct-sharing/oauth2-data-upload/
S4 https://www.openhumans.org/direct-sharing/oauth2-setup/
S5 https://www.openhumans.org/data-use/
S6 https://www.openhumans.org/contact-us/
S7 https://pmc.ncbi.nlm.nih.gov/articles/PMC6593360/
S8 https://doi.org/10.1093/gigascience/giz076
S9 https://github.com/OpenHumans/open-humans-api/blob/master/ohapi/api.py
S10 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/operations/E002_READONLY_PROJECT_AUDIT_2026-10-25.md
S11 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md
S12 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R134_THIRD_METHOD_EXACT_JACOBIAN_AND_INTERPOLATION_SCIENTIFIC_REPORT_2026-10-25.md
S13 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R135_BURNSIDE_MIRROR_ORBIT_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-25.md
S14 https://github.com/edwardsage419/Psychohistory-Research/blob/main/docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v7.8_2026-10-25.json
