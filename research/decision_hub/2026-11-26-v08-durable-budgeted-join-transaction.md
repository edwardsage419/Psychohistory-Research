# v0.8 联合情景持久续算：预约预算、单次执行权及原子发布
2026-11-26。RESEARCH_CANDIDATE / SQLITE_TRANSACTION_EXECUTED / FIXED_FUNCTION_SLICE_EXECUTED / SYNTHETIC_DEVELOPMENT / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。手动科研增量，非生产修复或独立验收。
## 1. 基线、去重及新候选
起始main 82803894d9adf4a2a8bd7b8ff4ceaf4ba58da430；核对18近期提交、15开放PR、v3.2及同步规程前22行、唯一产品交接前22行blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、前轮有界数值及共享参数报告7821b0afe42fc77ead90693f40a79ff7b6af54c7、预算续算报告d4a85f1e92744d1179f76a47cf56926d17b18cf3、账本规划R101报告907f12081ddce7bb752ae498bcf21f4b4b218a60前22行。检索transaction/checkpoint/nonanticipation/information partition/idempotent/adaptive policy/feedback planning/robust longitudinal/observation/revision-safe等。R107计算发布事务（commit 2f0c17a303bde8ef3e9711a08fcbbbaa8d5e78ec）已有有限事件交错、修订与重放状态模拟；R43已有部分观察支持，R99/R101已有长期规划及账本，近期联合域已有预算续算。本轮新增真实SQLite文件事务、进程异常退出、并发预约与执行权、持久预算及旧任务隔离，不重复声称发明DP、联合情景算法或独立新样本。全库去重有限。
新发现Draft #63 v0.8已存在，固定head 734686980b19da9291bdd08b67d4e2519c011acf，base为本轮起始main，open/draft/unmerged，167个变更文件，作者报告696 Python测试及11子测试、84移动、4 Node、5 Linux Swift XCTest。公开开发主体1/4、数值单位7/23、条件0/5、账本修订0/10；仍未达G02完整门。实际读固定head V08_ACCEPTANCE.md blob da628bfb5ceb29a9858076222db8d7407e478e84、V08_ENGINE.md 6e0cbce22236b0f9d3b7f82e7217936959e2892c、V08_RESEARCH_INTEGRATION.md dc1cd0973bf138e076530935b0317bac63c4d86e、V08_INDEPENDENT_HANDOFF.md b0a70c4634693a916febc82ecddd39031b33bd33、V08_COMPOSITION.md a602867cb0ff640f3c585d6bb46890a27a6567bc。开发方自报工程成果不等于本轮重跑或独立验收。持久续算、实体设备、完整手机离线引擎、真实用户、实时事实和独立留出仍开放。选择持久续算是为填补该候选明确缺口；不修改原先完整版本目标，不派发零碎Codex任务。
## 2. 固定函数真实调用及研究合同
读取固定head platform/future_model/src/psychohistory/decision_composition.py 全文，Git blob aea376e8c94a4959bee1afd5e8a6b8c785060d42；contracts.py canonical相关源码blob 143b3d588258bac3f081c593b2ebf6ea8bdcee0a。实际本地转录从def _canonical到def advance_join之前函数块2349字符（FNV-1a32 4be388ee）、advance_join函数块3610字符（ea634c3d），与连接器所读固定片段长度及FNV一致。FNV仅转录诊断，非密码学身份或完整Git blob复算。真实调用这两个原函数块及原canonical；采用人工dataclass范围和端口夹具、转录Pydantic检查点模型；夹具省略原范围purpose字段，未运行完整上游Pydantic端口、宿主、原生API、CLI或Web。不能证明生产传输兼容。阈值为非负整数或无有限阈值None，缺少证据用missing端口省略；收益为非负整数。联合世界是人工共同情景，非概率。原advance_join的纯函数签名检查允许同一个合法检查点反复计算（本轮复现同一检查点两次得到相同结果）；这符合隔离纯函数的可复算性质，不是已证实生产漏洞。持久宿主负责控制重复执行及发布。
本轮研究选择单个逻辑run、最多一个在途任务、SQLite文件数据库、WAL、synchronous=FULL、BEGIN IMMEDIATE；trusted host在本地提供有效来源/范围/计划、密钥及工作票据。数据库run记录当前授权、单调代次、计划摘要、总额度、已预约额度、已提交游标、检查点、当前结果及活动操作ID；ops以(run,op)为唯一键，保存代次、计划摘要、cap、预约量、起始游标和状态。未提供外部不可信调用者的身份认证或工作票据验签，不允许把夹具传入真实个人记录。原签名密钥为临时测试密钥，不入库；真实跨重启密钥管理待验证。
## 3. 持久事务算法与不变量
A 预约事务：原子核对当前授权、代次、计划摘要；已存在同ID且合同相同只返回REPLAY_状态，合同不同ID_CONFLICT；已有在途任务BUSY。实际预约量a=min(cap,total-spent,job_count-cursor)。无额度返回LIMIT，无剩余工作返回COMPLETE；正预约量同时插入RESERVED操作、扣除a额度并绑定活动操作。初始检查点和结果以预算0产生。预约不可因执行失败或确认死进程而退款；此为保守算术比较工作量策略，不是用户货币或设备能耗。
B 执行权事务：必须在运算前将唯一活动操作从RESERVED原子变为RUNNING。若重复票据、已撤权、旧代次、计划摘要或游标不匹配，拒绝。只有取得执行权的可信工作线程调用原advance_join，严格使用预约额度和服务器内部检查点；客户端不得提交任意计算结果。初版发现重复publish调用在拒绝前仍执行数学计算，本轮实际修正并全量重跑；初版结果单独保留，不合并计数。
C 发布事务：完成后重新核对同一run、活动操作、授权、代次、计划摘要、起始游标、预约量及RUNNING状态；只在一个事务内提交新游标、签名检查点、研究输出、清除活动操作及COMMITTED状态。旧任务或重复提交不能替换当前结果。所有原输出authority NONE；不授予行动、保存、训练或正式建议权限。计算、发布与实际观察仍分开。
D 异常及修订：受信宿主确认工作者已经终止后才ABANDONED，不自动以超时作为死亡证明；已用预约量不退回。授权、来源或范围改变，递增代次、取消旧活动操作、清空旧游标/结果；若当前有权，重建零预算结果；同一run已消费的总预约额保持不减，重新授权也不能复用旧ID。任何已完成旧任务在新代次下不具当前性。修订和撤权不能保证在途CPU立即停止；本轮只保证旧发布被阻断。
不变量：spent=sum(all op amounts)且0≤cursor≤spent≤total；RESERVED或RUNNING至多一个且与active一致；当前代次cursor等于该代次COMMITTED金额之和；撤权状态无当前结果或检查点。事务提交后旧请求不能重复预约、重复取得执行权或重复发布。假设数据库事务及受信工作进程正常工作、文件不被外部替换；不证明整个磁盘回退、防密钥窃取、备份恢复、恶意宿主、任意崩溃或分布式一致性。
## 4. 实验与实际结果
Python 3.13.5、Pydantic 2.13.5、SQLite 3.46.1，本地Linux工具容器。实际使用临时SQLite文件、真实独立连接及事务；无网络、个人数据、训练、费用或生产运行。合成开发输入为ChatGPT辅助原创，同一研究者的直接逐世界枚举参照，不是独立科学验收。
64种三世界阈值序列（0/2/None/missing）×27种收益序列（0/3/missing）×5预算（0至4）×3执行策略（正常、首次预约放弃、重复预约及重复发布）=25920个配置。每一前缀直接逐世界核验pass/fail/missing/not_calculated分区、计数界及最终已知域覆盖；每一提交再次核对原函数片段输出。注意所有已知任务完成仍可能缺失证据，不宣称全域完整。
最终实测：
```json
{
  "abandoned_reservations": 6048,
  "committed_steps": 20982,
  "completed_all_known": 17262,
  "concurrent_claim_controls": 24,
  "configurations": 25920,
  "crash_controls": 3,
  "legacy_duplicate_accepts": 1,
  "limited": 8658,
  "missing_coverage": 15876,
  "other_controls": 32,
  "prefix_checks": 52950,
  "replay_rejections": 12576,
  "source_slice_replay_checks": 20982,
  "stale_rejections": 64,
  "thread_controls": 48
}
```
三项真实子进程os._exit控制：预约已提交但运算未开始、发布事务已写入但未提交、发布事务已提交但响应未返回。重开数据库均正确保留预约额度，未提交结果不露出，已提交结果不重复发布；弃用任务经宿主确认死亡后允许新ID在剩余预算内续算。非硬件断电或文件系统灾难试验。48组两个线程同时预约（同ID和不同ID各24），24组相同票据的并发执行权争夺，均只一个获权。初版约30秒，修正全量约34秒，包含测试SQLite写入、参照及大量夹具构造，非产品延迟或设备性能。
另运行72组受控真实线程交错，旧任务取得执行权后暂停，插入修订、撤权或撤权再授权（各24），然后允许旧计算继续并尝试提交。修订及重新授权分支先提交新结果；旧发布72/72拒绝，新结果48/48保持，撤权48/48当前结果不可见（其中24后续重新授权）；这不证明撤权后CPU被实时取消。签名检查点四类字段篡改4/4拒绝，范围/收益/阈值变更3/3拒绝。仅一个研究者设定的同步顺序，不是现实竞态概率。
```json
{"interleavings":72,"rejected_inflight":72,"new_current_preserved":48,"revoked_hidden":48,"checkpoint_tamper_rejected":4,"changed_plan_rejected":3}
```
## 5. 复算资产及发布边界
完整本地会话研究包 psychohistory_durable_join_research_2026-11-26.zip，8文件，ZIP校验通过，SHA256 457382d394d11d5ad540acd7560cd1755f66789d9872c48ad691e259d1b2d362。包内native_slice.py、research.py、interleave.py、initial_results.json、results.json、interleave_results.json、README.md及SHA256SUMS。7个受校验文件全部通过。运行 python research.py 和 python interleave.py；需要已有Python与Pydantic环境。首轮及修正版结果分别保留。after_claim同步钩子在修正版全量运行后增加，默认None不改变主流程，用于72组受控线程实验。核心脚本SHA256：native_slice.py a62e2a56165e95c1777d0f049b5675dee23bcdb4dec1b8fe5f6752057c59d2c6；research.py b18e5bd175f9a9e69a0dd4e50af6e8d6d9aedd0393969305539605242e1ceee1；interleave.py 1762219ac947bc890035de6f9509be213da9aa5ee7e1774e8490cda2630cea39，以包内清单为准。完整ZIP在研究会话提供；本报告同步GitHub，不声称ZIP或全部本地脚本已上传到仓库。
核心发布过程（SQL及状态逻辑摘录，需上面完整复算代码运行，并非可直接替换生产实现）：
```python
# reservation, claim and commit are three durable transactions;
# reserve and claim recheck trusted current scope under BEGIN IMMEDIATE.
# active ticket must match run, op, epoch, digest, cursor, amount.
with store.tx():
    # validate reservation and current authorization
    # atomically transition exactly one RESERVED -> RUNNING
    store.db.execute("UPDATE ops SET status='RUNNING' WHERE run=? AND op=?",(ticket["run"],ticket["op"]))
result = advance_join(plan, plan.scope, ticket["amount"], signing_key=key, checkpoint=ticket["cp"])
with store.tx():
    # validate current scope and active RUNNING reservation again
    # atomically publish checkpoint/result AND consume operation
    # stale / replay branch performs no write
    pass
```
实际实验中全部上述核验、状态条件、更新与异常退出测试均由research.py执行；摘录不应作为生产实现，省略的条件不可删除。
## 6. 对下一版本接口及研发建议
复用v0.8 CompositionScope、GroupedPort、_JoinPlan、签名检查点及ActiveMethodManifest，不新建重复联合域模型。新增候选宿主DurableCalculationRun、BudgetReservation、WorkerClaim、PublicationTransaction接口，以可信作用域、预算策略、版本、来源、授权代次及操作身份绑定。操作ID、结果、日志保留与删除、授权隔离须受产品隐私规则约束。单次执行权及提交不等同完整用户任务预算；本实验只计组对谓词预约，未计数据库、准备、签名、输出、CPU、内存或电量。还需全请求真实预算、物理设备、恢复事务、备份回退保护、真实授权、实时取消、真实来源及原生入口、联合规划及独立留出。在前述条件未完成前保持隔离研究用途。当前不声称DP或完整长期计划正式接入；下一轮主线优先解决v0.8明确未过的条件、角色、数值时域及修订图与实际账本连接。模型轨负责科学接口；产品轨维护唯一交接及权限/交互；独立轨保管未见样本并复核实际代码及设备；不擅自修改任务或新增Codex工作。R073、PESEN、冻结协议及历史证据等级不变。未修改生产代码、PR或触发主动CI、训练、合并、部署、费用。
