# F009 第三十五阶段：多设备乱序撤销与旧备份恢复
UTC 2026-10-31T08:19Z，2026-W44。目标键 (privacy_safety,F009,phase35,out_of_order_revocation_replica_restore)。纯候选原则与虚构状态机，不接入个人敏感数据、真实设备、证书或付费服务。

原始标准：RFC 5280规定证书撤销列表thisUpdate、nextUpdate及撤销日期；RFC 9162定义追加式Merkle日志一致性证明并讨论不一致视图风险。两者不直接规定个人决策授权，此处把撤销顺序、日志持续性和独立信任锚点作为未来候选控制。

建立三条虚构事件：epoch1 GRANT、epoch2 REVOKE、epoch3 GRANT（第三条明确假定经合法重新授权）。三个虚构设备各收到三条事件的六种顺序，穷举6^3=216种交付组合、648个设备最终状态。候选模型保存按epoch索引的事件，要求无缺口、parent前驱连续、同epoch冲突进入UNKNOWN。全部216组完整链最终进入REVIEW，程序在原生Python普通及-O模式各执行659项断言，全部PASS。REVIEW仅代表可以进入人工审查，绝非自动授权。

单独反例：旧授权在撤销后重放，宽松last-arrival-wins缓存可错误返回REVIEW；候选顺序模型保持REJECT。先收到epoch1和epoch3而缺epoch2时返回UNKNOWN，补齐后才可审查。相同epoch冲突或parent断裂返回UNKNOWN。独立可信高水位为3时恢复只有epoch1的旧备份返回UNKNOWN；可信高水位丢失也返回UNKNOWN。将高水位错误重置为0的反例仍可能将旧备份错误送入REVIEW，说明可信锚点本身不能从回退的备份中恢复。

候选控制：本地最小化保存事件epoch、撤销版本、签发主体、前驱证明、设备已见高水位和争议状态；高影响操作要求最新可信授权与撤销状态已确认。离线、冲突、缺前驱、可信锚点丢失时暂停自动执行并保留人工申诉。事件日志需跨备份保护，防止旧快照覆盖已见撤销。若采用透明日志，须另行验证真实签名、独立日志根和一致性证明。

限制：脚本使用字符串token模拟事件，没有签名、真实时间、证书路径验证、密码学哈希或多设备联网；216种状态只是人工排列数，不代表现实风险概率。真实再授权合法性、删除生效范围、跨文化公平与用户权利仍待独立研究。新增E2=0、E3=0，零新增费用。

来源：https://www.rfc-editor.org/rfc/rfc5280.html
https://www.rfc-editor.org/rfc/rfc9162.html
可复算程序 research/privacy_safety/f009_phase35_out_of_order_revocation_20261031.py。
下一项phase36：离线设备合并冲突时授权签发主体变更、跨根轮换及撤销证据缺失的安全恢复。
