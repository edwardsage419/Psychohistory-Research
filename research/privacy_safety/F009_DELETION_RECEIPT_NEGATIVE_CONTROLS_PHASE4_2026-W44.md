# F009 第四阶段：跨设备删除证据清单与失败注入

日期：2026-10-30 UTC，2026-W44。目标键：(privacy_safety,F009,phase4,deletion-receipt-fail-closed-negative-controls)。状态：COMPLETE_PHASE4_ARTIFICIAL_E1。仅为未来个人决策模型储备原则性隐私控制，未接入真实敏感数据，未开发产品。

## 官方资料边界

Syncthing 官方 https://docs.syncthing.net/users/versioning.html 说明远端删除或替换可能在接收设备的 .stversions 保存历史版本；cleanoutDays=0、maxAge=0 等配置可导致历史版本长期保留，且版本保留策略按设备/文件夹配置。

restic 官方 https://restic.readthedocs.io/en/v0.17.0/060_forget.html 说明 forget 移除快照引用，prune 回收仅由已移除快照引用的数据；其他快照仍引用的数据会保留。其 check 命令用于仓库结构完整性检查，不能替代跨设备物理擦除证明。以上是官方文档支持的机制，本轮没有运行两种软件。

## 候选证据合同

人工删除记录需要包含 deletion_epoch、预期设备集合、每设备确认 epoch 与来源校验状态、未知副本数、外部云副本状态、历史版本清理收据、备份引用数、prune 完成及收据 epoch、法律保留标志。所有字段属于候选设计，尚无真实系统证明其可完全采集。

归档程序 research/privacy_safety/f009_deletion_receipt_negative_controls_20261030.js 定义 fail-closed 的人工状态：
* UNKNOWN_REPLICA、UNKNOWN_DEVICE_RECEIPT、UNKNOWN_ARCHIVE_RECEIPT、UNKNOWN_PRUNE_RECEIPT 表示缺乏可信完整证据。
* PENDING_REPLICA、PENDING_ARCHIVE、PENDING_BACKUP_REFERENCE、PENDING_PRUNE、PENDING_LEGAL_HOLD 表示具体阻塞。
* MODEL_SCOPE_COMPLETE 只表示本人工合同的字段检查完成，严格不能解释为物理擦除、第三方副本清除、法律合规或生产环境安全证明。

## 实际运行及负控制

首次在隔离 V8 执行预写测试时，负数备份引用计数未按预期抛错，测试失败，程序**未写入远端**。随后在输入验证中显式拒绝负引用，重跑全部检查成功，再将修订版源码写入 GitHub。保留失败事实，不将首次失败记录为 PASS。

最终在隔离 V8 执行：1项正控制 MODEL_SCOPE_COMPLETE、12项故障负控制均拒绝完成、5项非法输入均抛错。负控制分别为离线旧epoch、未知设备、未知云副本、设备收据缺失、未验证确认、历史归档未清、归档收据过期、备份共享引用、prune中断、prune收据过期、法律保留及备份清单缺失。人工状态机不访问实际设备或备份。

现有实现只验证布尔 verified 字段，未实现签名真实性、设备枚举完整性、收据撤销、时钟可信性、密钥擦除、数据生命周期自动执行及第三方服务商证据。生产使用必须独立建立这些能力并进行故障注入与安全审计。

## 研究等级及后续

E1 人工程序性检查，NONBLIND；真人安全 E2 实验0、独立 E3 0、外部安全审计0。F009本周专题已完成四个有界阶段，F008上游撤销问题继续开放，避免无新增信息重复汇报。费用为0，本轮未注册服务、未运行收费CI、未使用用户数据；GitHub账单/免费额度 NOT_VERIFIED。

下一F009第五阶段：研究删除请求与不可删除审计证据的最小化冲突，候选方案仅保存不可逆摘要、请求epoch、保留依据与过期时间，并用人工反例验证恢复历史版本后的撤销状态。需先检查本周其他轨是否已研究相同问题。
