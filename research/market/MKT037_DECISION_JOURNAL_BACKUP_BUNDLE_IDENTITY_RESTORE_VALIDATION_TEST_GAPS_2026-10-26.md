# MKT037 Decision Journal 备份成套身份、恢复校验及自动化测试覆盖审计

run_date: 2026-10-26 Asia/Singapore
track: market
subflow: product
status: COMPLETE_BOUNDED_SOURCE_AUDIT_AND_SYNTHETIC_SQLITE_CHECK
observed_main_head_before_write: 6d53c78ccb9ec2b1320c9bb329e2c3d9fe2919df
upstream_repo: sinameraji/decision-journal-electron
upstream_fixed_commit: 95269a7db776ce74165c811b9195feed17049b3d
remote_ci: NOT_RUN_BY_THIS_RESEARCH
cost: 免费公开英文源码、SQLite 原始技术文档、Python 标准库合成检查；主动新增费用 0，整体账单和免费额度未独立核验

## 1. 去重和研究对象

已读取当前 GitHub main HEAD、market MKT001 至 MKT036、E004/E005、F002 及本轮新增 R167、R073 至 R077 来源纠正记录。MKT035 研究长期记忆授权，MKT036 研究 WAL 单文件复制与旧记忆恢复。本轮聚焦此前未单独审查的 **备份成套身份验证、恢复前数据库有效性、恢复失败回滚边界及实际测试覆盖**。固定上游 main 与前一轮相同，故“新增”指本项目新增的机制审查和合成负对照，不宣称软件新发布修复。

## 2. 产品输入、状态、目标与运行边界

产品记录用户决策、候选方案、主观预期、事后结果、复查日期、可选 AI 记忆。持久状态为本地加密 SQLCipher 数据库及独立 vault.json，备份导出两者；本地模型和可选外部模型有不同授权状态。源码无本轮可验证的长期决策预测改善、人生效用最优化或自动校准证据。package.json 版本 0.11.0、license 字段 MIT，README 声称离线本地使用不需订阅；可选 OpenRouter API 可能计费，本项目未启用、未注册。

## 3. 主要新增发现：PIN 验证、数据库完整性与备份身份是三项不同的检查

固定源码 src/main/ipc.ts:
* 1126 至 1156 行：vault:export 写 vault.json，随后 fs.copyFile 决策数据库到 decisions.db；当前路径没有发现成套 manifest、数据库哈希绑定、写入后 reopen/integrity_check 或独立快照校验。
* 1174 至 1216 行：vault:import 先检查两个文件存在，再用 portable vault 和 PIN 解锁，然后复制数据库并 hydrateDb；没有在复制前独立验证数据库字节属于同一套备份。
* 1220 至 1290 行：vault:replace-from-backup 首先验证 vault.json 与 PIN，随后 teardownSession、将现有 vault/db 重命名为 .replaced、删除 db-wal/db-shm，再复制新 db 并尝试 hydrateDb；失败时尽力回滚旧 vault/db。恢复路径有授权撤销和代际控制，但源码未见恢复前成套文件的哈希绑定或完整数据库可读性预检。

因此，正确 PIN 只能说明 portable vault 解锁条件通过，不能单独证明配套 decisions.db 与该 vault 匹配、未损坏、内容属于用户选定的备份版本。数据库本身可被 SQLite integrity_check 判为 ok，也不能证明它属于正确的备份。具体加密数据库失败形态仍需 SQLCipher 真实应用验证；没有证据表明实际用户遭遇数据损坏或越权访问。

SQLite 官方 PRAGMA integrity_check 主要检查数据库内部结构及约束，不验证外部文件配对或备份版本身份。Online Backup API 可以提供活动数据库的一致快照，但仍需另行处理成套身份、授权状态和恢复版本。

## 4. 自动化测试覆盖边界

直接枚举固定提交的 Git tree：src/main/ai/__tests__、src/main/memory/__tests__、src/main/rolemodels/__tests__、src/renderer/routes/__tests__ 存在。没有发现文件路径名称含 backup/restore 的测试。检查 src/renderer/routes/__tests__/decisionDraft.test.ts，其覆盖草稿解析、缺字段、非法 JSON 等；src/main/memory/__tests__/validate.test.ts 覆盖来源摘录和记忆初始批准状态。**这些测试不等于备份/恢复端到端测试。** 路径枚举与所读测试内容不足以证明仓库所有隐藏测试均不存在，也未执行 vitest、Electron 或 SQLCipher。

上游 CHANGELOG v0.10.0（2026-09-09）将 Backup vault 入口增加到 Settings；v0.11.0（2026-09-09）增加决策草稿自动保存。未找到在固定 main 中针对本轮备份成套身份问题的明确修复提交。此结论只覆盖已读取的固定源码、测试树和更新日志。

## 5. 独立合成检查：结构有效但备份配对错误

使用 Python 3 标准库 sqlite3、hashlib、tempfile，在临时目录构造两份不同内容的未加密人工 SQLite 数据库 A/B，以及损坏的第三份数据库 C。以 A 的 SHA256 作为人工 manifest 的预期哈希，逐一验证 integrity_check 与 manifest 匹配情况。实际执行结果：

```json
{
  "matched": {"integrity": "ok", "rows": 1, "matches_manifest": true},
  "swapped_valid_db": {"integrity": "ok", "rows": 1, "matches_manifest": false},
  "corrupt_db": {"integrity": "ERROR", "rows": null, "matches_manifest": false}
}
```

三个断言均满足：结构正常且身份匹配；结构正常但身份不匹配；损坏且身份不匹配。这是**未加密人工 SQLite 的逻辑负对照**，未运行 Decision Journal、未测试 PIN、SQLCipher、Electron、用户数据或实际备份替换。它表明“能打开”与“属于预期版本”需要分别检查。人工 manifest 是本轮建议的检测器，不能误称为产品已实现的功能。

可复算示例：
```python
import sqlite3, tempfile, pathlib, hashlib, json
with tempfile.TemporaryDirectory() as td:
    root = pathlib.Path(td)
    def make(name, value):
        p = root / (name + ".db")
        with sqlite3.connect(p) as db:
            db.execute("CREATE TABLE records(id INTEGER PRIMARY KEY, value TEXT)")
            db.execute("INSERT INTO records(value) VALUES (?)", (value,))
            db.commit()
        return p
    a, b = make("a", "decision-A"), make("b", "decision-B")
    expected = hashlib.sha256(a.read_bytes()).hexdigest()
    corrupt = root / "corrupt.db"
    corrupt.write_bytes(b"not-a-sqlite-database")
    result = {}
    for name, p in [("matched", a), ("swapped_valid_db", b), ("corrupt_db", corrupt)]:
        try:
            with sqlite3.connect(f"file:{p}?mode=ro", uri=True) as db:
                integrity = db.execute("PRAGMA integrity_check").fetchone()[0]
                rows = db.execute("SELECT count(*) FROM records").fetchone()[0]
        except sqlite3.DatabaseError:
            integrity, rows = "ERROR", None
        result[name] = {"integrity": integrity, "rows": rows,
                        "matches_manifest": hashlib.sha256(p.read_bytes()).hexdigest() == expected}
    assert result["matched"] == {"integrity": "ok", "rows": 1, "matches_manifest": True}
    assert result["swapped_valid_db"] == {"integrity": "ok", "rows": 1, "matches_manifest": False}
    assert result["corrupt_db"] == {"integrity": "ERROR", "rows": None, "matches_manifest": False}
    print(json.dumps(result))
```

## 6. 候选控制、风险及科学证据

MKT037-C1：未来备份输出需绑定唯一备份 ID、版本、创建时间、数据库和 vault 的校验摘要，并在实际恢复前校验。摘要需要可信保护，单纯未认证哈希不防恶意替换。
MKT037-C2：恢复前在隔离环境验证可解锁、SQLCipher 兼容性、数据库完整性、关键表存在及版本匹配，再触碰当前数据；恢复后做可读性和关键记录核验。
MKT037-C3：失败回滚必须明确区分旧数据文件恢复、旧会话可重新打开、WAL 一致性、已撤销权限继续有效与用户界面状态；失败不等于已安全回滚。
MKT037-C4：增加仅用人工数据的备份、恢复、同日覆盖、跨备份文件替换、损坏数据库、断电中断、旧记忆复活等端到端负对照。未来安全工程候选，当前不提前开发个人决策产品。
MKT037-C5：数据生命周期与授权仍由 F002 候选控制研究；不修改 R 系列协议、不预设唯一人生效用权重。

SOURCE_CODE_MARKET_E1：固定上游源码与测试树；
AUTHOR_DOC_MARKET_E1：CHANGELOG/package.json；
PRIMARY_TECHNICAL_REFERENCE：SQLite PRAGMA/Backup 官方英文文档；
INDEPENDENT_SYNTHETIC_E1：三种人工数据库逻辑检查；
REAL_PRODUCT_RESTORE_TEST=0；REAL_USER_LONG_TERM_BENEFIT=0；E2 HUMAN=0；E3 HISTORICAL=0；CI=NOT_RUN。
潜在故障是有界风险记录，不代表已证实真实产品事故。

## 7. E/F 状态及下一轮

E：2026-10-26 E004/E005 已归档。本轮只读复核 R167 72 个合成世界、B 轨独立直接权重计算，均为内部 E1；另发现 E005 的“R073 缺第二独立真人实验”表述已被 A 轨后续来源登记纠正：R074、R075、R077 分别为第二、第三、第四项原始真人实验，R076 为重复来源；旧 E3 字段与当前 E3=历史证据口径冲突。具体证据差量另记 E006，不覆盖 E005。
F：2026-W44 F002 已完成授权撤销、衍生数据和备份生命周期专题，本轮仅追加案例，不重复立项。

下一轮 MKT038：优先审查其他本地决策日志系统的版本化偏好、事前概率与事后结果追踪；也可针对 Decision Journal 的 draft 恢复版本冲突和记忆来源失效进行不同于备份主题的源码审查。

## 8. 非中文原始来源

1. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/src/main/ipc.ts
2. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/src/main/db/drafts.ts
3. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/src/renderer/routes/__tests__/decisionDraft.test.ts
4. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/src/main/memory/__tests__/validate.test.ts
5. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/CHANGELOG.md
6. https://github.com/sinameraji/decision-journal-electron/blob/95269a7db776ce74165c811b9195feed17049b3d/package.json
7. https://www.sqlite.org/pragma.html
8. https://www.sqlite.org/backup.html
