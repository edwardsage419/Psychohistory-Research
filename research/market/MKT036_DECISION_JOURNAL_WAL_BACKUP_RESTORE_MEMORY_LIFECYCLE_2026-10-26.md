# MKT036 Decision Journal WAL 备份一致性、旧记忆恢复与授权代际边界

run_date: 2026-10-26 Asia/Singapore
track: market
subflow: product
status: COMPLETE_BOUNDED_FIXED_SOURCE_AND_INDEPENDENT_SQLITE_SYNTHETIC
observed_main_head_before_write: 735e551307df712f0dfbb0be4f4e809b0000b197
upstream_repo: sinameraji/decision-journal-electron
upstream_fixed_commit: 95269a7db776ce74165c811b9195feed17049b3d
ci_status: NOT_RUN
billing: 本轮仅免费公开源码、SQLite 官方英文文档和 Python 标准库本地人工测试，主动新增费用零；账户整体账单未独立核验

## 1. 去重与范围

已读取 main 最新 HEAD、MKT001 至 MKT035 目录、MKT035、E004、F002、本日 R166 新报告及 A 数据侦察新记录。MKT035 已讨论记忆提案批准、队列授权检查和 forgetAll。本轮新增审查 **备份创建的一致性** 与 **旧备份恢复对已批准记忆的影响**，避免重复记账。固定源码版本未更新；这里的“新增”指本项目首次完成的机制审计及独立合成反例，不宣称产品刚发布新功能。

## 2. 实际数据、状态、算法、反馈、费用

Decision Journal 接受用户输入的决策背景、选项、预期结果、复查日期、主观信心及事后复盘；本地 SQLCipher 数据库保存决策、会话、记忆提案、来源与记忆队列。记忆包含 approved/pending/rejected/stale，数据恢复与在线 AI 授权分别管理。软件旨在支持长期决策记录与回顾；没有在本轮取得可证实长期个人收益改善、跨情境最优权重、概率校准或真实因果效果的独立证据。README 宣称本地优先；package.json 标记 MIT、免费本地使用，可选在线 AI 需要自备 OpenRouter key，可能计费，本项目未启用。固定提交下单独读取 LICENSE 路径返回 404，许可证文件完整性未独立核实。

## 3. 新增主要发现：WAL 模式与单文件备份路径存在不一致风险

固定源码 src/main/db/open.ts 第 538 至 570 行对已打开的加密数据库设置 `journal_mode = WAL`。src/main/ipc.ts 第 1125 至 1152 行在会话仍打开时导出便携 vault.json，随后执行 `fs.copyFile(dbPath(), join(destDir, 'decisions.db'))`，未在该导出路径看到 SQLite backup API、明确 checkpoint、数据库关闭或复制 WAL 文件。

SQLite 官方 WAL 说明：已提交事务可以暂存在独立的 WAL 文件，直到 checkpoint 才进入主数据库文件。只复制主数据库文件可能漏掉已提交事务，部分状态下也可能产生不可用快照。SQLite 官方建议使用 Online Backup API 或 VACUUM INTO 制作活动数据库的一致快照。由于该应用使用 SQLCipher 扩展，最终可用方案还需兼容其加密设置与备份验证。**此处为源码和 SQLite 机制共同支持的具体风险，尚未在该 Electron 应用真实环境复现。**

本轮用 Python 标准库 sqlite3 在临时目录创建**无敏感数据、未加密的人工 WAL 数据库**，关闭自动 checkpoint，明确 checkpoint 基线后提交 3 行；保持源连接打开，仅复制主 .db 文件；另用 sqlite3 backup API 生成快照。实际结果：
```json
{"journal_mode":"wal","live_rows":3,"file_only_copy_rows":0,"sqlite_backup_rows":3,"wal_size":4152,"assertions":[true,true,true]}
```
此例直接证明 SQLite 文件单独复制的失真可达成，未证明用户实际已丢失数据，未测试 SQLCipher 或 Electron 的文件系统时序。

可独立复算的 Python 3 标准库示例：
```python
import sqlite3, tempfile, shutil
from pathlib import Path

with tempfile.TemporaryDirectory() as d:
    src, copied, safe = [Path(d) / name for name in ("source.db", "copied.db", "safe.db")]
    db = sqlite3.connect(src)
    assert db.execute("PRAGMA journal_mode=WAL").fetchone()[0] == "wal"
    db.execute("PRAGMA wal_autocheckpoint=0")
    db.execute("CREATE TABLE t(id INTEGER PRIMARY KEY, val TEXT)")
    db.commit()
    db.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    db.executemany("INSERT INTO t(val) VALUES (?)", [("a",), ("b",), ("c",)])
    db.commit()
    live = db.execute("SELECT count(*) FROM t").fetchone()[0]
    shutil.copyfile(src, copied)
    with sqlite3.connect(copied) as cp:
        copied_count = cp.execute("SELECT count(*) FROM t").fetchone()[0]
    dest = sqlite3.connect(safe)
    db.backup(dest)
    safe_count = dest.execute("SELECT count(*) FROM t").fetchone()[0]
    dest.close()
    db.close()
    print(live, copied_count, safe_count)
    assert (live, copied_count, safe_count) == (3, 0, 3)
```

## 4. 第二发现：备份恢复关闭在线授权，但可恢复旧记忆状态

src/main/ipc.ts 第 1174 至 1210 行与 1220 至 1289 行分别执行新导入和替换恢复，复制旧 `decisions.db` 后调用 `hydrateDb`，然后 `revokeOnlineConsent()` 和 `clearCatalog()`。src/main/ai/settings.ts 将在线授权存储在数据库外的 `online-ai.json`，撤销时把 enabled 置 false、consentGeneration 加一。src/main/ipc.ts 的 vaultGeneration 随锁定、解锁和恢复增加；memory/queue.ts 对在途结果进行代际和授权检查。

与此同时，src/main/memory/store.ts 第 1 至 46 行表明记忆及 memory_enabled 存储在数据库中，且已批准记忆与数据库一起备份。恢复流程没有看到删除 memory_items 或把恢复后的 memory_enabled 强制置 false 的操作。因此，**旧备份中仍保存的已批准记忆可能在恢复后重新出现**。恢复后的在线 AI 为关闭状态，不能将旧记忆出现等同于恢复后立即对外发送数据。旧记忆是否会重新进入具体聊天上下文、旧任务跨设备代际碰撞及恢复失败回滚行为均需专门应用测试。

额外注意：backupFolderName 只包含日期，同一天同一目录再次导出会命中相同文件夹；mkdir recursive、writeFile 与 copyFile 在当前路径没有防止覆盖既有备份的独立检查。这是源码支持的潜在版本覆盖风险，未在应用中实测。

## 5. 证据等级、局限和候选控制

SOURCE_CODE_MARKET_E1：固定提交的 ipc.ts、db/open.ts、memory/store.ts、memory/queue.ts、ai/settings.ts 与 package.json。
PRIMARY_TECHNICAL_STANDARD：SQLite 官方 WAL、Online Backup API；规范技术事实，不能代替产品运行测试。
INDEPENDENT_SYNTHETIC_E1：本地未加密 SQLite 反例，三项断言通过；不代表真实 SQLCipher 备份已失败。
AUTHOR_CLAIM_E0：产品 README 的私密、安全和长期判断改善表述，尚未由独立真实用户实验确认。
E2 HUMAN=0；E3 HISTORICAL=0；INDEPENDENT_REAL_PRODUCT_RUN=0；REMOTE_CI=NOT_RUN。

MKT036-C1：未来本地优先决策记录方案需要使用支持事务一致性的备份接口，并在恢复后执行行数、关键记录、版本与完整性检查。
MKT036-C2：备份应包含时间与不可变唯一标识，避免同日同目录静默覆盖；应报告实际捕获的数据边界。
MKT036-C3：备份恢复后的在线授权、记忆启用、历史批准记忆及旧导出副本应分别呈现状态；对已撤销来源的派生记忆做来源失效审查。
MKT036-C4：长期个人偏好与记忆不应在恢复旧版本后自动被当作当前有效判断。用户可查看、否决、纠正。
MKT036-C5：上述均为未来候选控制，不修改 R073、PESEN、R 系列冻结协议，不开发个人决策产品，不预设唯一人生效用权重。

## 6. E 与 F 状态及后续

E 2026-10-26：E004 已完成当日正式只读检查。本轮只读追加检查 R166：原冻结条件数误写 56，首次执行失败，事后公开更正为 28；后续两条 JS 精确方法复核，属于有修订记录的内部 E1，未见指定提交关联 Actions。A 轨排除了 Montero 2022 作为 R073 第二独立实验候选。详细差量另存 E005，不改写 R 轨成果。
F 2026-W44：F002 已完成授权撤销与备份生命周期专题，本轮将“备份事务一致性”和“旧记忆复活”登记为新案例，避免同周重复专题。

下一轮 MKT037：优先寻找 Decision Journal 的备份/恢复自动化测试、加密数据库快照验证及项目 issue 修复记录。若无法获得新证据，转向其他本地优先决策日志工具的事后结果反馈与版本化偏好机制。

## 7. 非中文原始来源

1. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/src/main/ipc.ts
2. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/src/main/db/open.ts
3. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/src/main/memory/store.ts
4. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/src/main/memory/queue.ts
5. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/src/main/ai/settings.ts
6. https://www.sqlite.org/wal.html
7. https://www.sqlite.org/backup.html
8. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/package.json
