# F002 授权撤销、衍生数据、缓存与备份的全生命周期安全方法

research_week: 2026-W44 (2026-10-26 至 2026-11-01)
run_date: 2026-10-26 Asia/Singapore
track: privacy_safety
subflow: F
status: COMPLETE_BOUNDED_STANDARDS_AND_SOURCE_METHOD_REVIEW
observed_main_head: 22d6617098a7b6a914c21bf5320d313949656a23
output_path: research/privacy_safety/F002_CONSENT_REVOCATION_DERIVED_DATA_BACKUP_LIFECYCLE_2026-W44.md
ci_status: NOT_RUN
billing_checked: 公开英文标准与免费源码审阅，主动新增费用零；整体账单未核验
commit_sha: 远端写入后核验

## 1. 去重与资料等级
读取本周前一周 F001 和 market MKT025 至 MKT034 的权限及生命周期候选风险。F001 已涵盖人类否决和最小采集，本周集中研究授权撤销后的缓存、衍生记忆、备份、外部接收者。只使用非中文网站。
原始规范：
1. NIST Privacy Framework 1.0（2020-01，现行已核正式版本）：Control-P 中 CT.PO-P1 处理授权及撤销，CT.PO-P2 数据审阅/传输/变更/删除，CT.PO-P4 生命周期，CT.DM-P4 可删除、CT.DM-P5 按政策销毁、CT.DM-P7 随数据传递处理权限。自愿性框架，属于规范指导，不是效果实验。https://www.nist.gov/privacy-framework/privacy-framework
2. NIST Privacy Framework 1.1 初始公开草案（2025-04-14），截至本次官方页面仍显示草案及最终版 Coming soon。仅作为更新观察，不能当作已定稿的 v1.1 规范。https://csrc.nist.gov/pubs/cswp/40/nist-privacy-framework-11/ipd
3. NIST SP 800-88 Rev.2，2025-09-26 正式版，针对存储介质清理与加密擦除的程序和核验要求；其适用边界为存储介质清理，不能推导已经发往外部模型提供商的数据可撤回。https://csrc.nist.gov/pubs/sp/800/88/r2/final
4. 欧洲数据保护委员会 EDPB 对 GDPR 数据主体权利的官方解释：撤回同意可能触发删除请求，需考虑适用法律基础、有限例外和第三方接收者通知。该监管指南的义务仅在适用法域和事实成立时判断，不能作为全球统一法律。https://www.edpb.europa.eu/sme/be-compliant/respect-individuals-rights_en
5. 可检查的工程样本：Decision Journal 固定 GitHub commit 95269a7db776ce74165c811b9195feed17049b3d，src/main/ai/settings.ts、src/main/memory/queue.ts、store.ts。仅作源码机制案例，不作为符合规范的认证。https://github.com/sinameraji/decision-journal-electron/tree/95269a7db776ce74165c811b9195feed17049b3d

## 2. 候选状态机与范围
建议未来研究先把每项数据标记为 SOURCE、LOCAL_COPY、DERIVED_ITEM、CACHE、BACKUP、EXTERNAL_COPY 六类，并分别维护处理目的、来源、权限、创建时间、依赖关系、保留期限和可删除证明。每个来源权限的状态为 AUTHORIZED、REVOKED、DELETION_REQUESTED、LOCAL_ERASURE_VERIFIED、EXTERNAL_STATUS_UNKNOWN 或 EXTERNAL_ERASURE_CONFIRMED。各类副本状态可不同，禁止以一个布尔值「已删除」覆盖所有对象。

候选撤销步骤：停止新读取和后台任务；将在途响应作废；切断新的派生处理；标记依赖旧来源的记忆为失效待复核；按范围处理本地原始值、衍生项、索引、日志和导出副本；核查备份的恢复后再删除策略；如适用向外部接收方提出请求并记录回应；向用户呈现仍未知的外部副本状态。撤销读取、撤销未来处理、删除本地副本、删除历史备份、外部服务完成删除须分别报告。

## 3. 固定源码样本的具体发现
Decision Journal 的 memory/queue.ts 在请求前后检查 consentGeneration 和 vaultGeneration，失效响应不入库；memory/store.ts 的 forgetAll 删除 memory_items、memory_suppressions、memory_jobs 并关闭记忆开关；原始决策与已保存聊天并不在 forgetAll 的删除范围。memory:set-enabled(false) 停止队列并取消任务，但没有在该处理分支中删除既有 memory_items。其 README 明确已发往外部服务的数据无法召回。工程层面这是一组不同的操作语义。
需要注意 memory/store.ts 中明确对 explicit 与 self-described 提案自动设置 approved，tentative 才 pending；原始摘录存在性检查并不直接证明模型所生成的整句命题在语义上成立。此风险与授权生命周期相邻，留待未来「派生记忆证据与人工纠错」专题单独实测。

## 4. 原则性候选控制
F002-C1：撤销是版本化事件，记录权限代数和 consent generation；旧 generation 产生的写入拒绝，避免在途响应回写。
F002-C2：所有衍生项必须带来源 ID、原文版本、提取模型和提示版本；来源被撤销、编辑或删除后执行失效传播与重新授权审查。
F002-C3：设置撤销处理的「不可确定」结果类型。外部服务已收到内容时，只报告已发送、请求删除、第三方已确认或无法核实，不承诺远端彻底清除。
F002-C4：本地备份和导出副本建立可核对的清单与恢复隔离。恢复旧备份时不得静默复活已撤销授权或重新启用外部上传。
F002-C5：最小保留审计记录，只保留动作时间、类别、结果与证据标识；避免把被删除的敏感原文再写入不可删审计日志。
F002-C6：加密、删除文件、介质加密擦除和第三方删除属于不同技术声明，任何安全结论均需要具体方法和验证范围。
F002-C7：涉及健康、财务、关系及第三人资料时，默认本地处理、分区隔离、单独目的授权；未来不设统一效用权重，保持人工最终控制。

## 5. 风险记录与未来验证
F002-R1 HIGH：仅关闭授权仍保留衍生画像；需要派生链追踪和可撤销性测试。
F002-R2 HIGH：备份恢复复活旧权限或旧敏感记录；需要恢复后拒绝旧 generation 的合成测试。
F002-R3 HIGH：第三方已接收内容却误显示「已彻底删除」；需要多状态证据报告。
F002-R4 MEDIUM：删除索引却保留聊天或截图；需要按副本类型分别核查。
F002-R5 MEDIUM：错误提取的「明示偏好」自动进入长期记忆；需要语义证据和人工纠错测试。
F002-R6 MEDIUM：不可删日志二次保存敏感内容；需要日志最小化与清理政策。

未来只可在人工合成状态机上进行「撤销中途完成」「重复撤销」「旧备份恢复」「共享衍生来源删除」「第三方未确认」负对照。不得输入真实用户数据、调用收费模型、租用云资源或提前开发产品。标准指导等级为 NORMATIVE_PRIMARY，源码为 SOURCE_CODE_INSPECTION，控制清单为 DESIGN_CANDIDATE；真实安全效果、外部独立实测和个人长期收益均为 NOT_VERIFIED。

## 6. 下一周
F003 候选主题：派生记忆的证据语义、错误偏好归因、申诉与人工纠错，优先公开原始研究和可复核开源测试。与 R 系列科研主线分离，不改变冻结协议。R 全系列完成后再归纳、最后熔炼。
