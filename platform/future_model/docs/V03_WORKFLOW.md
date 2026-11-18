# v0.3 机制实验

通过中文控制台的「机制实验」页登记并核验正式来源，选择模型版本，提交参数，再批准一次合成执行。完成后可查看轨迹、数值诊断、R132/R123 来源 blob、源码指纹和不可变快照。历史支持按 ID 读取。选择「从快照分支」会从所选实验的最后状态和时间继续。分支保存父快照哈希并要求单独批准。

## 数学契约

| 模型 | 方法 | 时间 | 状态与评价 |
| --- | --- | --- | --- |
| `r123-degroot@1.0.0` | 固定行随机矩阵的同步加权平均 | 整数轮 | 两个标量意见，精确有理数，用间距递推独立核验 |
| `r132-replicator@1.0.0` | Taylor–Jonker Eq.3 世代映射，联验 Eq.4 增量 | 整数世代 | 两项或三项策略份额，精确有理数 |
| `r132-replicator@1.0.0` | 对 Eq.2 的显式 Euler 或四阶 RK4 | 有理数观测时间 | 两项或三项策略份额，固定 42 位 Decimal 运算和可查询误差 |

Eq.2 的向量场为 `x[i] * ((A x)[i] - xᵀAx)`。Eq.3 的下一世代是 `x[i] * (1 + (A x)[i]) / (1 + xᵀAx)`，需要每个策略的出生倍数非负且总体分母为正。Eq.4 的增量是 Eq.2 向量场除以该分母。Euler 和 RK4 路径均显式验证各自的单纯形，越界会留下真实错误。Hawk–Dove 大步长案例的计算零值原样保留，并显示 `FALSE_EXTINCTION` 与连续参考值。Logistic 用闭式参考解，Stag–Hare 和 Hawk–Dove 用分离变量积分反演。零和 RPS 的乘积漂移在轨迹诊断中记录。适用范围限于受信任内置模型和有限合成参数。 [Taylor 与 Jonker 1978](https://doi.org/10.1016/0025-5564(78)90077-9)

可比较的两条轨迹须使用同一模型版本、正式来源、同一个精确起点、相同收益矩阵或意见权重，以及同一时钟和观测网格。比较结果给出各观测点及全程的最大坐标绝对误差，并保留两端的数值诊断。它们可以来自不同允许的积分算法。预测 Brier 和 Log Loss 继续由 v0.2 的冻结预测协议提供。轨迹工件使用 `SYNTHETIC_ONLY`，实证状态保持 `UNKNOWN`。 [v0.2 数学与预测口径](MATHEMATICS_V02.md)

## CLI 和 API

以下命令在 `platform/future_model` 中运行。令牌、数据库及备份留在独立本地目录。

```bash
DATA="/workspace/psychohistory-v03-data"
bash scripts/run.sh --data "$DATA" research register R132
bash scripts/run.sh --data "$DATA" mechanism models
bash scripts/run.sh --data "$DATA" mechanism submit r132-replicator 1.0.0 SOURCE_ID \
  --parameters '{"initial":["1/2","1/2"],"payoff":[["-2","2"],["0","1"]],"method":"euler","steps":1,"step_size":"4"}'
bash scripts/run.sh --data "$DATA" mechanism approve RUN_ID
bash scripts/run.sh --data "$DATA" mechanism result RUN_ID
bash scripts/run.sh --data "$DATA" mechanism compare RUN_A RUN_B
```

`method=eq3` 使用整数 `steps` 且省略 `step_size`。R123 提交使用 `opinions`、`weights`、`steps`。可选 `--branch-from RUN_ID` 继续同一来源和策略维度的完成快照，初值参数保留原声明。 CLI 的 `mechanism experiments`、`status`、`result` 和 `compare` 可查询历史。写入命令遵循已有单调度器互斥。

JSON API 位于 `/api/v3`，包括 `GET /models`、`GET/POST /experiments`、`GET /experiments/{id}`、`POST /experiments/{id}/approve`、`POST /experiments/{id}/cancel`、`GET /experiments/{id}/result` 和 `POST /compare`。来源登记和验证仍使用 `/api/v2/sources`。POST 运行参数为 `model_id`、`model_version`、`source_id`、`parameters` 和可选的 `branch_from`。比较参数为 `left`、`right` 和可选 `metric=trajectory`。所有 v3 请求使用同源带令牌访问。

## 生命周期、存储与恢复

Linux worker 使用独立 POSIX 会话及进程组、RLIMIT_CPU、RLIMIT_AS、内核父进程死亡信号和 PPID 监测。macOS worker 使用独立会话及进程组、RLIMIT_CPU 和 PPID 监测，内存限额标记 `NOT_ENFORCED`。取消与墙钟超时只向已核实的受控进程发送终止信号。隔离针对内置、受信任的模型。调度器发布轨迹前校验输入身份、时间语义、快照与数值内容，并用同一确定性内核执行一次有界复算。该发布检查和独立解析核验各自提供不同证据。

SQLite 是来源登记、运行状态和审计事件的事务权威。旧 JSONL 初次打开时导入，保留有界镜像供查阅。备份从同一个 SQLite 快照生成审计日志。已知旧版未处理的日志尾部须保留至人工修复，备份会拒绝漏收的快照。对象内容同步后用不覆盖链接发布并同步对象目录。备份和恢复仅向新目录发布，使用排他目录改名和目录同步。经进程强杀或退出注入测试的保证限定于所测文件系统和故障窗口。真实突然断电为 `NOT_RUN`。

升级时先关闭旧服务并备份。v0.1 和 v0.2 的旧成果在 v0.3 各自的端点读取，原身份和留出预留保留。已过期的源代码执行身份仍会阻止批准旧协议重新执行。查看旧运行时应使用它的原版本状态查询和产物读取命令。 [灾难恢复步骤](RECOVERY.md)
