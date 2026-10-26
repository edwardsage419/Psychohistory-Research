# MKT063 sqlite-history-json 原地历史恢复后的触发器丢失与审计分叉

日期：2026-10-27（Asia/Singapore）。轨道：market。状态：COMPLETE_BOUNDED_SOURCE_SQLITE_SYNTHETIC_E1。主动新增费用：0。

## 1. 去重、固定来源与范围

已读取main的MKT001至MKT062文件目录、MKT062正文、E031和本周F002。MKT062研究显式disable_tracking后重新启用导致的空档。本轮转向**没有显式停用审计**、直接使用restore(swap=True)的独立机制，避免重复。研究对象为Simon Willison的开源sqlite-history-json，固定仓库提交 `53e66b2791a1ccc2efd19c1e24de9fd5afcc343b`，Python库0.4，Apache-2.0，无运行时第三方依赖。

固定英文一手源码：
* https://github.com/simonw/sqlite-history-json/blob/53e66b2791a1ccc2efd19c1e24de9fd5afcc343b/sqlite_history_json/core.py ，Git blob `a83469cb6ef55b1b18921a0a92edad490a6b8afc`。
* https://github.com/simonw/sqlite-history-json/blob/53e66b2791a1ccc2efd19c1e24de9fd5afcc343b/tests/test_sqlite_history_json.py ，Git blob `af5e0cb24f9736d00c4e5a79ad755453f7080674`。
* https://github.com/simonw/sqlite-history-json/blob/53e66b2791a1ccc2efd19c1e24de9fd5afcc343b/README.md 。
* SQLite官方触发器机制：https://www.sqlite.org/lang_createtrigger.html 。

## 2. 新发现：restore(swap=True)完成后审计触发器可能消失

固定源码`restore()`第443至577行：先按审计事件重建`_tmp_restore_{table}`，在`swap=True`分支中依次执行`ALTER TABLE [table] RENAME TO [_tmp_old_{table}]`、`ALTER TABLE [_tmp_restore_{table}] RENAME TO [table]`、`DROP TABLE [_tmp_old_{table}]`。该分支没有重新调用`enable_tracking()`或重新建立审计触发器。

SQLite触发器附着于表对象。原业务表改名后，其INSERT、UPDATE、DELETE触发器随旧表对象移动；旧表被DROP时触发器随之删除。新恢复表原先未安装审计触发器。由源码和SQLite DDL语义推出：**原地恢复成功返回后，新的业务写入可能不再进入审计历史**。这不同于MKT062的显式停用。

固定测试文件的`test_restore_swap`与`test_restore_swap_replaces_original`（约738至765行）核对恢复后的行值，未继续核对触发器数量或恢复后写入的审计增量。仅据现有测试覆盖判断存在回归测试空白，不能断言上游没有其他保护或生产事故。

## 3. 独立SQLite实验，19项通过

本轮在现成执行环境用Python标准库sqlite3、SQLite 3.46.1、纯内存人工表独立执行。**没有下载或直接运行上游Python包**。审计触发器使用与上游相同的三操作模式，UPDATE仅记录变化列；恢复时的三步DDL与固定源码一致。19项合成断言通过，0失败。

实验序列：
1. 建立items及_history_json_items，安装3个触发器；写入id=1/name=A/qty=1，再更新name=B。初始审计2条且回放与当前表一致。
2. 建立`_tmp_restore_items`，填入早期状态A；执行上游swap分支的两次ALTER TABLE及一次DROP TABLE。第一次改名后3个触发器均指向`_tmp_old_items`；最终新items表中为A，但审计触发器数量从3降至0，旧审计仍保留2条。
3. 将恢复后的items.name改成C，SQL写入成功，审计条数仍为2，历史回放返回B，当前为C。
4. 再次建立触发器并将qty改为9。新增一条仅包含qty的审计UPDATE，回放成为name=B/qty=9，实际为name=C/qty=9。重新启用并未自动弥补此前缺口。
5. 负对照：另一个人工数据库使用不替换原表的恢复方式，原表3个触发器继续存在，后续UPDATE会正常增加审计事件。4项负对照均通过。

断言覆盖：触发器初始存在、旧表改名后绑定、恢复状态、DROP后触发器消失、历史行保留、恢复后写入漏记、回放偏离、重新启用后局部更新仍偏离、未出现恢复分支身份标记、非swap负对照。结果证明固定SQL分支的条件性风险，未证明上游包的所有调用路径或实际生产事故。

## 4. 未来个人决策模型候选映射

真实数据输入候选：业务对象ID、审计事件ID、快照来源版本、恢复操作ID、审计触发器配置、事务边界、权限与来源身份。状态候选：TRACKING_VERIFIED、RESTORE_PENDING、RESTORE_APPLIED_UNVERIFIED、AUDIT_TRIGGER_MISSING、HISTORY_DIVERGED、REBASELINE_REQUIRED。原地恢复后的每次新写入都应具备可检验的事件连续性证明。

候选方法：恢复前保存审计高水位与源表schema，恢复后验证触发器及新旧表对象身份，执行可回滚的人工写入负对照，核对审计增量，记录历史分叉和重建基线身份；恢复版本应明确区分历史分支，不把旧时间线与新时间线无条件串接。这里仅提出原则性设计，未开发个人决策产品。

目标与反馈：恢复后可审计写入比例、事件缺失数量、最后可信快照、历史回放与当前状态差异、人工恢复审批状态。发现触发器缺失或回放分叉时，暂停历史评分及自动推断并提示人工检查。解释输出必须列出审计可见性边界，禁止声称完整恢复已获验证。

隐私：审计保留旧敏感值与撤销授权的关系沿用F002生命周期约束。修复触发器时也要避免重复持久化已撤销的原文。权限和用户撤销操作应优先于历史分析完整性；任何不可删审计证据只能保留必要的非敏感元信息。

费用与商业模式：此开源库可在现有设备用免费SQLite审阅。项目无新增购买、API、GPU、云服务或收费CI。无直接面向个人的人生规划收费产品，也无可验证的个人决策收益，不能以技术机制代替市场效果。

## 5. 证据分级、风险与下一步

MARKET E1：固定一手源码与上游测试覆盖支持风险定位；独立SQLite合成实验19/19支持DDL触发器丢失与历史分叉。UPSTREAM_PACKAGE_EXECUTION=NO；PRODUCTION_INCIDENT=NOT_VERIFIED；EXTERNAL_REPLICATION=NO；PERSONAL_DECISION_OUTCOME=NOT_VERIFIED。

MKT063-R1 HIGH：原地历史恢复后审计触发器缺失，后续写入静默漏记。
MKT063-R2 HIGH：恢复前后的不同历史分支未明确标记，导致回放或效用评分误读。
MKT063-R3 MEDIUM：现有swap测试只检查恢复结果值，未覆盖恢复后写入连续性。

下一轮MKT064优先检查另一个开源事件账本的恢复分支、触发器存活测试与版本化回放，形成跨项目对照。E轨当日全轨实质检查已由E028完成，本轮另开展R197第三方法审计。F轨本周F002已完成，不重复立项。三个研究维度均为候选知识储备；先完整R系列、后归纳、最后熔炼，所有冻结协议保持不变。
