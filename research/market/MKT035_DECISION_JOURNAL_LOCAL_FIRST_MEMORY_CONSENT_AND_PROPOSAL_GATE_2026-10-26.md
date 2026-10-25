# MKT035 Decision Journal 本地优先决策记忆、在线授权与自动记忆采纳机制审查

run_date: 2026-10-26 Asia/Singapore
track: market
subflow: product
status: COMPLETE_BOUNDED_FIXED_SOURCE_AUDIT
observed_main_head: bf44b3d595482eef9aacd6d322a521a5108d41ac
output_path: research/market/MKT035_DECISION_JOURNAL_LOCAL_FIRST_MEMORY_CONSENT_AND_PROPOSAL_GATE_2026-10-26.md
upstream_repo: sinameraji/decision-journal-electron
upstream_fixed_commit: 95269a7db776ce74165c811b9195feed17049b3d
ci_status: NOT_RUN
billing_checked: 本轮只读公开 GitHub 源码和标准，使用轻量本地人工合成逻辑；主动新增费用零，账户账单未核验
commit_sha: 写入后以远端 SHA 回读为准

## 1. 去重与选题
读取 main 最新 HEAD、MKT001 至 MKT034 目录、MKT034 正文、E004、F002、原始239 v7.8 和项目工作流 v2。此前研究过 Dcider、ARDA、OpenDecision 的评分、校准、偏离和注入，本轮转向真实存在的免费开源个人决策日志软件 Decision Journal，深读固定源码的「记忆提取及授权门控」。另检索 Decision Ledger 与其他 decision-journal 项目，因名称重复和产品定位差异，本轮不将它们混成同一产品。

## 2. 产品实际输入、状态、算法、反馈
官方 README 记录：macOS 本地决策日志，输入标题、问题背景、候选选项、预期结果、复查日期、主观置信度和心理状态；事后填写真实结果、教训和复盘。SQLite/SQLCipher 本地加密保存，支持搜索、分析、加密备份和恢复。Ollama 用于可选本地聊天，Whisper 用于可选本地语音转录。源码 MIT 许可，README 声称不需要账户或产品订阅。macOS 11+，不是跨平台实测。
源码 memory/queue.ts：启用记忆功能要求同时开启在线 AI、配置用户自己的 OpenRouter key 和提取模型。保存决策后进入异步提取队列；处理前检查 consentGeneration、决策版本、排除状态和模型；提取请求 enforceZdr=true；写入前再次检查 vaultGeneration、授权版本和原决策版本。src/main/ai/openrouterClient.ts 对该路径附加 zdr:true、data_collection:deny。普通手动在线聊天允许用户明确同意使用没有 ZDR 路由的模型，故其风险边界与自动提取不同。
记忆状态有 pending、approved、rejected、stale，来源记录保留 decision_id、field、excerpt、revision。用户修改原决策后旧来源派生项可标 stale；删除决策后无其他来源的派生项会被清除。拒绝提案写入 suppression，避免同一断言在下次编辑后重复出现。forgetAll 删除 memory_items、memory_suppressions、memory_jobs 并关闭记忆开关；不会自动删除原始决策、聊天记录、外部接收方已收到的内容。关闭记忆开关只停止队列及取消任务，已批准记忆仍存在，需明确使用忘记操作。
该产品目标是决策记录、复盘、个人判断回顾及可选 AI 记忆。源码中没有找到可证明真实人生收益预测、因果推断、多目标最优权重或自动根据事后结果重训练的独立测试。本轮不运行应用或真实模型。

## 3. 新发现：文档「每条建议须批准」与源码的自动采纳范围存在差异
README 的 Memory 介绍称建议在用户批准前不会被使用。固定源码 src/main/memory/store.ts 的 initialStateFor(kind) 明确：tentative 为 pending，explicit 与 self-described 为 approved。src/main/memory/validate.ts 验证摘录是否出现在原决策的字段、类别、长度、数量、抑制规则；并没有验证生成 statement 在语义上是否被 excerpt 蕴含。因而来源原文存在与长期命题可靠是两个不同性质。当前代码允许通过校验的 explicit 或 self-described 类型在插入时自动进入 approved。作者注释解释这是为了减少对用户已明确陈述内容的重复确认。该机制属于可见设计选择，尚未证明为真实安全漏洞或发生过错误归因。
本轮做了四个不含个人资料的独立合成状态例子：同样摘录「I might resign if conditions worsen」，模型若输出「I will resign next month」并自标 explicit，抽象校验满足摘录存在性而进入 approved；标 tentative 且附问题则 pending；tentative 缺问题被拒；另一个 self-described 命题可进入 approved。四项人工断言符合代码中的局部门控逻辑。该例只证明局部规则不能替代语义蕴含检查，不代表真实模型会输出该错误断言，也未实际执行 Electron 应用或生产 validator。

## 4. 隐私、授权、费用与局限
本地数据及加密属于 README 和代码支持的架构主张，未执行渗透测试、加密正确性审计或网络抓包。网络默认拒绝出站，官方 README 列出应用更新检查、更新下载、Whisper 模型下载、用户主动启用在线 AI 等例外。在线 AI 的 ZDR 路由属于代码参数及第三方供应商政策约束，不等同于对远端实际删除的独立验证。撤销授权使新请求停用、在途结果失效，但已经发送的内容无法召回。可选在线 AI 需用户自己的 API key，可能计费，**本项目禁止启用**。本轮只读免费源码，没有安装产品、下载模型或配置 key。
缺少可公开核验的真实用户长期决策改善实验、系统性安全测量、数据恢复后旧授权是否绝对无法再启用的独立测试；无证据推断该产品达到个人量化、数字孪生或长期多目标优化的科学标准。跨文化适用、Mac 以外设备支持和实际删除可验证性仍待查。

## 5. 来源与证据分级
SOURCE_CODE_MARKET_E1：固定提交的 memory/store.ts、queue.ts、validate.ts、ai/settings.ts、ai/openrouterClient.ts、ipc.ts；证实上述代码分支与状态。
AUTHOR_DOC_MARKET_E1：固定版本 README 的本地优先、加密、收费与隐私声明；尚无独立产品运行验证。
SYNTHETIC_LOGIC_MARKET_E1：四个抽象状态断言，验证局部规则，不验证实际服务器或人类表现。
MARKETING_E0：关于「私人、安全、改善判断」的宽泛效果性主张，均不自动上升为科研结论。
E2 HUMAN=0；E3 HISTORICAL=0；INDEPENDENT_REAL_DEPLOYMENT=0。

## 6. 候选方法与下一轮
MKT035-C1：未来对记忆分离「逐字摘录存在」「模型命题语义蕴含」「用户批准」三个不同门槛，重大长期偏好不应因模型自标 explicit 就被不可见采纳。
MKT035-C2：将原决策、推断记忆、外部发送副本、聊天历史、备份、缓存分开撤销和删除，展示每层结果与未知。
MKT035-C3：决策记录、事前概率、事后结果、结果归因、后悔程度和偏好变化分开存储，不能用事后结果自动判定先前选择非理性。
MKT035-C4：本地模型和在线模型权限分开，在线模型必须用户明确另行授权；本项目禁止计费 API。
MKT035-C5：候选控制只储备，不开发个人决策产品、不改变冻结 R073 或 PESEN、不预设唯一人生效用权重。

E 2026-10-26：E004 已归档只读日检。新增 R165 E1 证据已核冻结先于执行、原始 blob 一致；CI 未验证；R136 原冻结失败、original239 154 项待审仍开放。
F 2026-W44：F002 已归档授权撤销、衍生数据、备份生命周期专题，未接入真实敏感数据。

下一轮 MKT036：针对 Decision Journal 的备份恢复、权限代际重置与记忆旧状态重新出现问题，检查源码及可执行单测；如无新增机制，转向 Decision Ledger 固定仓库的决策结果反馈。继续优先完成全部 R 系列、之后分类、最后熔炼。

## 7. 非中文原始来源
1. https://github.com/sinameraji/decision-journal-electron/tree/95269a7db776ce74165c811b9195feed17049b3d
2. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/README.md
3. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/src/main/memory/store.ts
4. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/src/main/memory/validate.ts
5. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/src/main/memory/queue.ts
6. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/src/main/ai/openrouterClient.ts
7. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/src/main/ai/settings.ts
8. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/src/main/ipc.ts
9. https://csrc.nist.gov/pubs/sp/800/88/r2/final
