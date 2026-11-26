# v0.8 自主决策引擎

## 本地运行与迁移

在 `platform/future_model` 使用 Python 3.12、Node.js 24 和仓库锁文件。现有工作台、本地 API、CLI 和移动 PWA 继续使用同一数学契约。新 Web 默认使用 v8，可用 `?workflow=v07`、`?workflow=v05` 和 `?workflow=v04` 打开对应入口。

```bash
bash scripts/install.sh
bash scripts/verify.sh
bash scripts/run.sh --data /tmp/psychohistory-v08-example serve --port 8765
```

在本机浏览器打开 `http://127.0.0.1:8765`，使用该数据目录的本地令牌。服务绑定环回。可以直接说出比较目的、方案和已知条件，核对系统复述的原文与约束，再查看已经计算的比较或局部结果。高级结构化输入可补充口径。结果保留推导、数值、时点和来源，选择与计划均为用户记录。

```bash
printf '%s\n' '{"operation":"capabilities","data":{}}' |
  bash scripts/run.sh --data /tmp/psychohistory-v08-example decision-v08
```

v8 JSON Lines 与 `/api/v8/decisions` 共用宿主。临时会话在关闭、过期或重启后需重新建立。跨决策使用已有记录的资源仍须单独授予用途权限。历史记录、签名归档和恢复继续走原生 v4/v5 入口，资源归档 1.2.0 使用支持该模式的版本读取。升级先在独立数据根验证，可保留经授权的同代归档及受控原数据根。回退至 v0.7 客户端或代码时需开启新对话，历史备份仍按原授权代次检查。直接替换含撤回记录的数据根或跨设备复制其授权文件超出已验证恢复路径。 [恢复规程](RECOVERY.md) · [v0.7 归档兼容说明](V07_WORKBENCH.md)

## 模块合同

| 模块 | 当前合同与依赖 | 扩展及授权 |
| --- | --- | --- |
| 语言与上下文 | `decision_language`、`decision_semantics`、`decision_parser_registry`。RawTurn 合同 1.0.0 使用原始 UTF-8 SHA-256 与从零开始的半开 Unicode 标量区间。语义候选记录时间、数量、单位、原文归属、共享守卫与修订线索 | 在受审的应用构造代码中用 `ParserRegistry.register(spec, parse)` 登记本地函数与精确版本。宿主校验候选坐标、文本、输入/输出上限。可并行启用新旧版本、停用与重新启用旧版。候选字段不会进入原生账本。 |
| 证据、知识与参数 | 本地知识合同 1.1.0，全文索引、源文件、方法边和许可策略版本。按需重算命中的 Git blob。评分绑定情景与口径声明身份。独立的事实缓存区分获取、撤回、核验和用途票据 | `PublicFactCache` 仅由受信宿主配置固定 HTTPS 只读来源和版本。缓存为内存态，默认没有活跃来源。候选限范围、时间、证据身份及授权后才可请求宿主核验；公开材料不含用户查询。生产自动参数注入等待准入。 |
| 原生求解与调度 | `DecisionRegistry`、`DecisionHubV05` 和现有 15 项方法。先校验输入并使用 C028 检查底线，再按适用性执行 Pareto、C029 等。知道的单项冲突和点值差可从同一确认投影计算 | 拟新增方法需通过稳定 `Method` 合同，填写版本、公式、来源、许可、输入输出、单位、验证条件、反例、基线、资源上限、复算及依赖。隔离登记使用 `CandidateRegistry`，保留 `NOT_ADMITTED`。只有受审的发布代码才能接到生产注册表。 `DecisionRegistry.for_release` 从完整档案按家族选择一个精确版本并检查来源，生成不可变发布快照。当前宿主仍固定 C028 1.0.0，依赖失效只阻断相关分支。更换及回退需重新装配并开启新会话。 |
| 联合情景、风险与预算 | `decision_composition` 合同 1.0.0 绑定共同世界、版本、单位、授权和证据代次，保留竞争解释、缺失域及签名检查点 | 可执行隔离复算限制世界规模、预处理和每次比较的预算。完成研究准入后仍需要原生参数映射、持久化恢复及资源验收。 [联合情景与复算](V08_COMPOSITION.md) |
| 计划与长期资源 | `decision_resources` 使用原有实际/预测现金、已反映余额、工时、任务及期限，v8 增加显式同做计划的按身份并集 | `joint_resources` 只读。 `recurring_benefit`、`goal_deadline_frontier` 提供有限合成候选分析。现有 `reuse_resources` 仅复用明确授权记录的共同资源。 |
| 反馈与候选评价 | 历史记录保留事前预测及事后观察。 `FeedbackLab` 冻结合成/公开开发评价名单，对照当前版本、固定基线及候选调整的损失和低估边界 | v8 API `feedback/freeze`、`observe`、`evaluate` 和 `rollback` 使用临时凭据，只接收固定模式的开发数据。回退销毁会话评价，生产模型及用户记录独立存储。 |
| 权限、存储与界面 | `ConversationHub`、已有 SQLite 及签名备份；Web、API、CLI 以及原生 Apple 客户端源工程；PWA 的已移植方法保持既有协议 | 数据按保存、资源复用和科研用途分开授权。跨设备同步、个人算法自动更新及用途权限迁移待独立审查。 |

新模块由源代码显式注册。部署时维护客户和引擎的兼容版本，新增字段采用兼容读法。破坏性语义变更升主合同，保留旧读档入口。对候选启用、停用及回退先运行隔离样例。不得从数据、下载或 API 请求加载待执行模块。解析和模拟适配器可以通过如下测试复算。演示方法只登记在独立测试创建的注册表中。

```bash
.venv/bin/python -m pytest -q tests/test_v08_extensions.py
PYTHONPATH=src .venv/bin/python scripts/v08_composition_replay.py
```

## v8 传输与收据

- `start` 可带一次性关联 `cancel_nonce`。每次启动由服务端签发独立 `session_id` 和 `session_instance`。 `cancel-start` 取消尚未发布的请求。客户端收到已失效的首答后，以该结果的实例和修订释放资源。网络中断导致首答始终未收到时，已经发布的临时会话在超时后清除。
- 后续变更、保存、资源查询及 `end` 均携带 `session_id`、`session_instance` 和当前 `revision`。退出界面可以调用 `discard`，服务端只允许释放同一实例，容许客户端持有该实例的最后一个已交付修订。v6/v7 保留初始标识回显，私有工作区最多保留 65,536 个一次性客户端标识散列，以拒绝跨重启重试相同标识。表满后仍可使用 v8。旧实现升级前的临时会话需要重新开始。这个表独立于历史授权和个人记录归档，不含对话原文。
- `result` 绑定实例、修订、授权代次、方法、原文、依赖及计算散列。 `partial_analysis` 单独给出 `DESCRIPTIVE_ONLY` 与 `authority=NONE`。它保持 `phase=CLARIFY`、`analysis=null`，不能为方案选择、保存、计划或学习提供资格。旧修订、授权撤回和复用资格变更抛弃旧结果。
- 当前运行是绑定环回、一个本地工作区的单进程宿主。跨设备授权和真机证据另行管理。工作区令牌、个人原文、备份和诊断记录保存在本地受控目录。

[工程验收](../reports/V08_ACCEPTANCE.md) · [公开语言对照](../reports/v08/PUBLIC_DEVELOPMENT.md) · [独立验收交接](V08_INDEPENDENT_HANDOFF.md) · [研究接入](V08_RESEARCH_INTEGRATION.md)
