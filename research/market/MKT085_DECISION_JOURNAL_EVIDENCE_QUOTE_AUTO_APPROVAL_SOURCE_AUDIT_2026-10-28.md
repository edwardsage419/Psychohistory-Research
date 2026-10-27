# MKT085 开源 Decision Journal 的证据引用、自动批准与决策记忆风险
日期：2026-10-28（Asia/Singapore）。轨道：market。状态：BOUNDED_SOURCE_AUDIT。主动新增费用0。

## 来源固定与新机制
上游英文开源项目 https://github.com/sinameraji/decision-journal-electron ，main固定提交 `95269a7db776ce74165c811b9195feed17049b3d`。固定源码：
* `src/main/memory/validate.ts` Git blob `83c38fb843515353fd301ccf53c12090d7bc8198`
* `src/main/memory/store.ts` Git blob `a9b871cb01b08c26bc43956fb82c946e1eac6efb`
* `src/main/memory/context.ts` Git blob `5e237d817bbb034318f1dc2a4764eb60ba556390`
* `src/main/memory/__tests__/validate.test.ts` Git blob `dc34e5163c74628bf6a7f38130bbc79f8b1b961a`
* `README.md` Git blob `409106114511eddbd1039899af17c0cc57eec216`

本轮独立于MKT084的Shadow OS官方文档研究，直接读取另一开源产品的源代码及测试。产品将决策、候选选项、预测、复盘、信心与心理状态存于本地加密SQLite。可选本地Ollama对话；可选OpenRouter在线AI和独立的AI记忆开关。在线记忆提取使用外部模型，需要用户启用；项目明确披露自备API密钥可能收费，因此本轮不注册、不启用、不测试该功能。用户可编辑/删除记忆，决策修改会触发旧证据过期机制。默认离线、备份恢复、权限和撤销均为README与部分源码支持，完整安装包的网络行为尚未动态验证。该产品针对macOS，非通用跨平台部署保证。

## 可复核的条件性风险
`validate.ts` 对模型生成的 `statement` 仅校验非空、长度、类别、kind、重复和引用片段是否存在于决策某个字段；引用匹配为规范化后的子串包含关系。它没有校验statement的语义是否由excerpt蕴含。`store.ts` 的 `initialStateFor` 将 `explicit` 与 `self-described` 直接设为 `approved`，仅 `tentative` 为 `pending`；上游测试明确断言这一行为。`context.ts` 可选对话记忆上下文读取approved项。

合成反例：决策原文 `I do not want to quit my job now.`；引用 `do not want to quit my job now` 在原文中真实存在；假设模型错误输出 `I want to quit my job now.`，标记 `kind=explicit`。源码的引用存在性检查能够通过，错误statement可进入approved。该反例证明“引用片段存在”不足以保证“陈述含义被引用支持”；未实际调用上游模型，也未运行完整Electron应用，真实发生率与用户伤害未知。

README当前文字称记忆提议都展示来源、未经用户批准不会被使用，与上述 `explicit/self-described` 自动批准实现存在文档范围差异。即使提取和对话记忆均需单独开启，自动批准状态仍需清楚向用户披露。不能据此认定真实数据泄露或违法。源代码的 `renderApprovedMemories` 文本还将approved集合描述为用户已审阅保留，可能使下游模型过度信任自动批准项。

## 离线验证与产品矩阵
独立零依赖Node脚本 `research/market/mkt085_memory_quote_entailment_contract_20261028.js` 固定检查五份上游文本关键源码片段与人工否定反例，17项断言通过。此脚本属于源码合同与逻辑反例，不冒充完整应用运行。上游项目已有测试证明自动批准，未发现可证明语义蕴含的独立验证器；全库测试覆盖未穷尽。

输入：原始决策、选项、期望结果、回顾、用户可选AI记忆。状态：decision、review、memory proposal、approved/pending/stale、source revision。算法：本地子串来源验证、模型提取、类别与证据kind、撤销/重验。目标：记录、复盘和决策记忆。反馈：事后复盘、用户纠错、旧来源失效。解释性：引用来源与模型版本，语义正确性未获保证。隐私：本地默认、可选外发、单独记忆开关。费用：仓库package.json声明MIT且README声明免费本地使用；固定根目录未见LICENSE文件，复制许可文本前应单独核验；可选OpenRouter请求可能收费，本项目绝不启用。可验证性：固定源码E1，生产应用/长期效果未验证。

相对Shadow OS，Decision Journal的可见增量是可审查的记忆状态机与来源引用校验。两者都未提供经外部验证的长期人生决策改进证据。对未来项目仅保留候选方法，不启动个人产品开发、不固定人生效用权重。

## 证据等级与后续
MARKET E1 SOURCE_VERIFIED：固定Git blob、自动批准、子串匹配和上下文选取。MARKET E1 SYNTHETIC_LOGICAL_COUNTEREXAMPLE：17项离线断言。实际模型错误输出概率、运行时完整安全性、用户效能：UNKNOWN。相关F003独立研究见 `research/privacy_safety/F003_EVIDENCE_ENTAILMENT_AND_MEMORY_CONTESTABILITY_2026-W44.md`。

下一市场题：检查该产品编辑决策后的多来源记忆失效逻辑及已有测试，关注一个来源修订后其他来源是否仍可独立支持记忆。零新增费用。
