# MKT087 Decision Journal 删除来源后保留过期记忆的回归边界
日期：2026-10-28（Asia/Singapore）。商业产品机制研究。零新增费用。

## 固定来源与增量
英文上游仓库 https://github.com/sinameraji/decision-journal-electron ，本轮重新核验 main HEAD 为 `95269a7db776ce74165c811b9195feed17049b3d`。 `src/main/memory/store.ts` Git blob `a9b871cb01b08c26bc43956fb82c946e1eac6efb`；`src/main/db/open.ts` blob `1cba2e3aa32aa7a2d6402d7d157577a4f4a59d40`；`src/main/ipc.ts` blob `66057de70e243b170031e6749aeb190e975654c3`。MKT086已检查双来源先后编辑。本轮新增研究双来源中一条已经过期，另一条随后被删除的场景，并检查上游回归测试覆盖。

## 关键代码与人工时序
`memory_sources.decision_id` 外键使用 `ON DELETE CASCADE`。决策删除的 IPC 调用 `deleteDecision` 后只调用 `pruneOrphanedItems`；后者仅删除没有任何 `memory_sources` 行的非用户原创记忆。该路径没有逐条检查剩余来源对应决策的当前 `updated_at`。

人工状态：记忆 M 为 approved，A和B均提供版本1的来源。编辑A到版本2时，B仍有效，M保持approved。随后删除B，外键级联移除B的来源。A的版本1来源仍存在，`pruneOrphanedItems` 将其视为非孤儿。此时A来源已过期、B来源已删除，M仍approved。反向顺序同样成立。全部删除后会正常清理记忆，单来源编辑也能正常标记stale。以上状态只在固定源码与所述操作顺序下成立。

标准库内存SQLite复算脚本 `research/market/mkt087_delete_stale_source_sqlite_20261028.py` 已实际运行25项断言，25 PASS，0 FAIL。正向与反向编辑删除序列、级联、剩余来源新鲜度、状态及两个正常对照均被检查。PASS说明人工反例与当前SQL条件一致，不能解释为安全属性通过。

## 上游回归测试及修复状态
当前main仍为MKT086固定提交。上游 `src/main/memory/__tests__/validate.test.ts` Git blob `dc34e5163c74628bf6a7f38130bbc79f8b1b961a` 包含引用校验测试，未包含 `invalidateForDecision`、`pruneOrphanedItems` 或删除来源的回归用例。GitHub代码搜索在当前默认分支仅找到上述两个函数的实现与IPC引用，未找到专门测试。此为可见源码和索引范围的覆盖缺口，不能断言仓库所有历史分支或未索引文件均没有测试。当前固定main未观察到相关修复；未检验真实安装包版本。

## 产品机制与证据边界
输入为用户决策、复盘、来源引用和修订时间；状态为approved、stale、pending、rejected及来源版本。算法为SQL失效、外键级联和孤儿清理。目标为保存经证据支持的长期决策记忆。反馈为编辑、删除、重提和人工纠正。解释性保留来源文本，但聊天引用前缺少逐来源版本复验。隐私方面产品声明本地加密存储，在线AI与自动记忆需分别启用。源码可免费审查；OpenRouter在线模型可能计费，本轮未注册、调用或购买。

MARKET E1 SOURCE_VERIFIED：固定源码、数据库外键、IPC删除流程、上游测试文件。
MARKET E1 SYNTHETIC_SQLITE：25项本地SQL局部重演。
UNKNOWN：完整Electron路径、实际用户发生率、模型推断与长期效果、安装包是否另有防护。
候选控制：在删除及编辑后以全部当前有效来源重新决定记忆状态；已批准记忆进入聊天前复验；为删除和编辑交错次序加入回归测试。仅作未来方法储备，不实施个人决策产品。
下一项市场研究：比较另一开源决策日志的不可变原始记录与事后反思分层机制，避免连续研究同一实现。