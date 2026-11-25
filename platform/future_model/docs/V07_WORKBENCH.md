# v0.7 自主决策工作台

使用 Python 3.12、Node.js 24 LTS、npm 和 Git。从仓库的 `platform/future_model/` 运行：

```bash
bash scripts/install.sh
bash scripts/verify.sh
bash scripts/run.sh --data /tmp/psychohistory-v07-demo serve --port 8765
```

建议将 `--data` 指向仓库外由自己控制的规范化目录；上述路径供启动示例。打开 `http://127.0.0.1:8765`，用数据目录下 `token` 文件中的令牌连接。服务只绑定环回地址，浏览器令牌只留在本页内存。发布和远端部署另行授权。

## 使用

- 用中文写出要比较的方案和已知事实。系统先给可支持的局部信息与优先追问。确认真实选项、原文依据和底线后，才运行比较。转述、承诺、估计、否定和适用条件需要各自核对。不认识的输入显示为待核实或保留在原文，有限规则覆盖详见验收报告。
- 可以这样输入「房租和停车费合计每月最多3000元。A：每月房租2600元，停车费每月500元。B：每月房租2600元，停车费每月300元。」核对后会得到合计与底线，缺少币种、周期或具体金额时可补一句同口径的资料。
- 情景比较示例「我该选『方案甲』，还是『方案乙』？情景平常：方案甲得10分，方案乙得6分。情景变动：方案甲得0分，方案乙得7分。都比较未来30天，分差可比较，分数越高越好。」确认后可展开原生 C029 后悔值表。条件和分数属于用户提供的情景假设。
- 「共同资源与进度」接受可选的结构化快照。选择需要共同占用现金或工时的事项时，核对当天实际余额或账本、过去流入流出、未来费用、每日剩余可用分钟、共享旧任务和进度。金额使用小数文本，跨方案的键使用工作台显示的方案标识。可拆分分钟进入已有期限和容量模型；连续块、口径不全或时点失效时返回未知。账本实际到账与预测分列，已反映在余额的交易不再入账。工作台显示公式来源与统一修订。
- 「本地知识与待补资料」展示语料的出处、版本、适用边界及补证计划。全文匹配仅提供研究参考。产品当前使用本地知识库与严格的公开事实隔离协议，联网事实更新未启用。
- 默认会话临时。可以在「本地记录与隐私」单独授权保存、导出、恢复、记录实际行动和观察，或删除记录及撤回保存授权。跨会话资源复用为额外的 API 授权，仅可引用当前已保存版本的共同资源。撤回或覆盖版本使旧授权失效。选择和计划不会替用户执行。

## API 和 CLI

保留 `/api/v4/decisions`、`/api/v5/decisions` 和 `?workflow=v04`、`?workflow=v05`。旧 `/api/v6/decisions` 由当前自主服务承接。新入口 `/api/v7/decisions` 的 POST 会话操作包括 `start`、`turn`、`confirm`、`analyze`、`update_resources`、`reuse_resources`、`select`、`plan`、`save` 与 `end`。会话修改使用服务端会话和当前 revision。浏览器可用客户端预生成会话标识在首次响应前取消；会话与取消记录有时限。

GET `/status`、`/models` 和 `/capabilities` 提供版本、方法和跨端范围。POST `/knowledge` 接受 `{"query":"C028 interval hard constraint","limit":5}`，`/knowledge/discover` 提供明确任务口径的补证计划，GET `/knowledge/report` 提供每项字节核验，GET `/research-candidates` 返回隔离登记。POST `/resource-grant`、`/resource-revoke`、`/resource-replay` 与保存授权、已存决策标识关联。所有个人决策 API 需要本地 bearer。正文详情报告中的虚构输入可直接重放。

```bash
printf '%s\n' '{"operation":"status","data":{}}' '{"operation":"capabilities","data":{}}' |
  bash scripts/run.sh --data /tmp/psychohistory-v07-example decision-v07
.venv/bin/python scripts/v07_offline_check.py
PYTHONPATH=src .venv/bin/python -m psychohistory.decision_knowledge report
```

CLI `decision-v06` 保留为同一路径的别名。旧 `use_local_model=true` 在自主路径上返回退役通知。历史来源标记保留。应用无需 AI 服务、模型权重或模型环境变量。

## 迁移与回退

候选复用了 #61 的对话、自带数学界面、记录和移动端。v0.7 已有的 v0.4/v0.5 记录及备份使用原校验路径。带资源预测的归档使用 1.2.0，必须用支持该模式的版本复算或恢复；旧软件不会静默降级读入资源预测。切换前保留当前授权代次的已签名备份及完整受控数据根，先用独立数据目录验证。在撤回之后恢复数据仍受原授权代次约束。详细操作见 [恢复规程](RECOVERY.md) 及 [验收记录](../reports/V07_ACCEPTANCE.md)。

手机 PWA 的本地范围、共享数学接口和已验证升级边界见 [移动版验收](../../mobile/docs/V07_MOBILE_ACCEPTANCE.md)。v0.6 文档和报告按历史版本查看。
