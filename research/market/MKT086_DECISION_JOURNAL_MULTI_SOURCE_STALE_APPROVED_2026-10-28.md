# MKT086 Decision Journal 多来源记忆的过期证据继续获批风险

日期：2026年10月28日（Asia/Singapore）。轨道：market。性质：固定源码审查与最小SQLite重演。新增主动费用：0。

## 固定来源和研究问题

英文开源仓库 https://github.com/sinameraji/decision-journal-electron ，固定 main 提交 `95269a7db776ce74165c811b9195feed17049b3d`。本次直接读取：
* `src/main/memory/store.ts` Git blob `a9b871cb01b08c26bc43956fb82c946e1eac6efb`；
* `src/main/memory/context.ts` Git blob `5e237d817bbb034318f1dc2a4764eb60ba556390`；
* `src/main/ipc.ts` 的决策更新、复盘、删除与记忆失效调用；
* `src/main/db/open.ts` 的 memory_sources revision、decision_id、item_id schema。

MKT085已审计单条引文存在性与自动批准。本轮只研究新问题：一条已批准记忆由两个不同决策来源共同支持，随后两个决策依次编辑，过期来源是否可能互相充当有效证据。

## 代码合同与条件性反例

`invalidateForDecision(db, decisionId, newRevision)` 首先找到当前被编辑决策的旧版本来源。随后用下列条件判断是否还有其他来源：

`WHERE item_id = ? AND NOT (decision_id = ? AND revision < ?) LIMIT 1`

这个条件排除了本次编辑的旧来源，但对其他决策来源没有检查其各自当前 revision。函数一旦找到任何其他来源便跳过将记忆标记为 stale。聊天上下文 `renderApprovedMemories` 仅按 approved 状态选择记忆，没有额外逐来源新鲜度校验。

人工时序：记忆 M 初始 approved，来源 A(revision=1)、B(revision=1)；A 编辑为 revision=2，旧A被排除，B仍有效，M保持approved；B随后编辑为 revision=2，旧B被排除，旧A在SQL中被当作另一条来源，M仍保持approved。此时A、B都没有与当前版本相同的来源，M仍可进入获批记忆上下文。

`insertProposals` 还有 `SELECT 1 FROM memory_sources WHERE item_id = ? AND decision_id = ? LIMIT 1`，按决策ID去重，没有按revision判断。若后续模型对同一statement再次提议，旧来源行可使新revision来源被跳过。这是额外的条件性持久化风险。

## 复算与边界

零依赖标准库脚本 `research/market/mkt086_multisource_invalidation_sqlite_20261028.py` 使用固定源码相同的三条关键SQL谓词，在内存SQLite重演单来源、仍有一个有效来源、两个来源依次编辑、反序编辑、用户亲自写入记忆豁免，以及旧来源去重。实际运行17项断言，17 PASS，0 FAIL。核心反例在两个编辑顺序均成立。

本次复现的是固定SQL条件的局部状态行为。未启动完整Electron应用、未连接真实数据库、未触发模型、未访问用户真实数据；实际运行时的其他防护与真实发生率未知。不能声称用户已经遭受损害。

## 产品机制记录

输入：个人决策、复盘、记忆提议、来源决策ID与内容revision。状态：pending、approved、stale、来源行、提取队列。算法：来源引用存在性验证、按statement归并、按决策ID去重、编辑时失效。目标：让已批准记忆为未来决策对话提供上下文。反馈：决策编辑、复盘、用户手动更正和拒绝；跨来源版本新鲜度存在上述缺口。解释性：展示来源文字，但来源revision未在聊天前全部复验。隐私：本地加密存储为默认；在线AI和自动记忆是独立可选开关，外部处理依赖第三方。费用：本地源码可免费审查；OpenRouter在线API可能计费，本项目没有注册、启用或调用。局限：真实应用的全路径安全与长期决策改善均未独立验证。

## 候选控制和证据等级

未来方法候选：逐个来源比对其对应决策的当前revision；只有至少一个有效来源才能保持approved；同一决策的新revision可重新挂接来源；来源全失效后阻止聊天上下文继续引用；记录用户明确确认和模型自动批准的区别。对来源更新采用事务化处理和回归测试。以上均为未采纳候选控制，不提前开发个人决策产品。

MARKET E1 SOURCE_VERIFIED：固定源码SQL和状态选择逻辑。
MARKET E1 SYNTHETIC_SQLITE：17项局部SQLite断言。
UNKNOWN：完整应用、用户影响、真实发生率、跨平台运行。
下一轮市场：检查上游是否已有针对该多来源失效的回归测试、issue或后续修复；若没有新增证据，转向另一开源偏好学习实现。保持先完成全部R系列、后统一分类、最后熔炼。