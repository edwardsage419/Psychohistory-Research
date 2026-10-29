# F009 第2阶段：跨设备删除确认、忽略删除与版本归档风险

日期：2026-10-30 Asia/Singapore，2026-W44。目标键：(privacy_safety,F009,phase2,replica-ack-ignore-delete-archive-retry)。状态：COMPLETE_PHASE2_STATIC_AND_SYNTHETIC。延续F009第一阶段，F008 Keyhive撤销专题保持IN_PROGRESS；本轮不重复其静态水位结论。

## 1. 英文官方资料新核验

Syncthing官方删除配置：https://docs.syncthing.net/advanced/folder-ignoredelete.html 。其ignoreDelete高级选项会忽略传入删除索引，官方明确警告一般应保持false。官方示例指出，Alice删除文件后Bob若忽略删除，Bob可保留该文件；Bob后来修改文件又可能把更新传播回Alice。由此不能仅凭“删除消息已经发送”认定所有副本擦除。此行为是官方技术文档支持的机制描述，本轮没有运行Syncthing验证。

Syncthing官方版本归档：https://docs.syncthing.net/users/versioning.html 。默认不启用旧版本保留；启用后，**从其他设备接收到的删除或替换**可把旧内容移入.stversions，保留策略可按天数/数量设置，某些配置值0表示不自动清理。源设备的本地直接修改不会自动产生同样的Syncthing归档。删除活跃文件、清理.stversions、外部备份到期是不同事件。

Syncthing配置说明：https://docs.syncthing.net/users/config 。receiveonly模式不向其他设备传播本地更改；实际删除语义依文件夹类型、ignoreDelete及版本归档配置而异。ActivityWatch官方同步指南：https://docs.activitywatch.net/en/latest/syncing.html 另明确其应用层当前不传播删除。两项目不能混同为同一种同步协议或共同安全保证。

以上均属官方文档支持的功能边界，未取得独立安全审计、真实设备擦除证明或跨服务商备份到期凭证。免费开源文档审查无新增成本。

## 2. 三设备有限人工故障模型

归档源码：research/privacy_safety/f009_replica_delete_retry_synthetic_20261030.js。设备A/B/C最初各有虚构记录x，B离线；A发布删除epoch2，C收到并归档旧副本。状态依次为：

1. A与C活跃记录删除，B仍离线且保留旧记录：PENDING_REPLICA。
2. B重连，旧epoch1写入被人工策略拒绝；B确认删除，但C仍有归档副本：PENDING_ARCHIVE。
3. C的归档被人工设定为清除后：MODEL_ACK_COMPLETE，仅表示该有限模型内三个设备已确认，无真实物理擦除证明。
4. 独立反例：C配置忽略删除，仍保留活跃记录，总体状态PENDING_REPLICA。

隔离V8实际运行9项状态断言、3项非法输入拒绝PASS。模型自行定义版本号、确认及归档状态；没有调用Syncthing、ActivityWatch或实际操作系统同步接口。模型成功不能证明现实产品满足GDPR等法律删除义务。

## 3. 候选控制与风险记录

建议未来在明确授权范围内，最小化记录目的和副本，单独保存tombstone_epoch、replica_last_ack_epoch、replica_online_state、archive_present、backup_expiry、delete_retry_count、unknown_replica_count。任何设备离线、拒绝删除、归档未清理或备份未到期时显示PENDING，禁止将单设备删除反馈写成全局完成。

需要对恢复连接后的旧版本回放、双向同步的冲突副本、忽略删除设置、外部同步目录和备份策略分别测试。若记录属于高度敏感信息，应优先避免不必要的跨设备复制；人工确认高风险共享，提供授权撤销、申诉和可理解的删除进度。保留最小审计元数据，避免删除审计本身长期暴露身份。不得将任何固定效用权重强加于未来个人决策模型。

证据：官方技术文档 + 人工E1故障模型。实际产品同步运行、加密擦除、远端服务商确认、真实敏感数据处理均NOT_RUN。新增真人E2预测0、E3为0、外部安全审计0。零新增费用，账单和免费额度NOT_VERIFIED。下一F009阶段优先研究墓碑版本冲突与备份到期可核验证据；F008仅在上游发生实质变化时继续。
