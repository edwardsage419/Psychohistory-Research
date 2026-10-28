# F007 历史备份删除证明与数据生命周期证据分层（第一阶段）

日期：2026-10-29，第44周。状态：IN_PROGRESS_UNADOPTED。与已完成F006的代理权限及派生记忆撤销专题分离。本轮仅公开规范研究，没有真实个人数据、删除命令、密钥销毁或产品实现。费用0。

## 新增来源

S1 NIST SP 800-88 Rev.2最终版（2025-09-26）https://csrc.nist.gov/pubs/sp/800/88/r2/final ，官方说明媒体清除应按信息敏感性、清除方法及验证程序管理；相较2014版，2025年修订强化组织化清除计划、密码擦除及供应商可信度。S2 NIST正式公告 https://www.nist.gov/news-events/news/2025/09/guidelines-media-sanitization-nist-publishes-sp-800-88r2 ，明确Rev.2替代Rev.1及关键更新。S3 英国ICO存储限制指导 https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/ ，说明离线副本仍可能属于个人数据处理，适当删除应覆盖备份。S4 ICO删除审计指导 https://ico.org.uk/for-organisations/advice-and-services/audits/data-protection-audit-framework/toolkits/records-management/disposal-and-deletion/ ，要求按保留计划删除并记录失败。S5 ICO权利审计 https://ico.org.uk/for-organisations/advice-and-services/audits/data-protection-audit-framework/toolkits/accountability/information-rights/ ，提及备份与外部接收方。ICO材料注明受2025年法律变化影响可能更新，不能将本研究当作针对某个法域的法律意见。

## 研究新增量

建立六种独立证据状态的候选分类：①删除请求登记；②阻止未来读取或推理使用；③主数据库逻辑删除；④缓存及派生索引清理；⑤备份副本清理或到期隔离；⑥媒介清除或密钥失效的验证。任何一项成功都不自动推出其余项目完成。密钥销毁需要核验密钥作用范围、残余副本及可恢复性；删除日志、API成功响应和媒体清除验证应分别登记。

人工风险链：某原始偏好P从主数据库删除，索引I仍可检索，备份B仍可恢复。将P标为DELETED会误导用户；更审慎的状态是ACTIVE_USE_BLOCKED、INDEX_PENDING、BACKUP_PENDING、MEDIA_ERASURE_UNVERIFIED。上述只是候选审计状态，不代表已运行任何系统。

## 候选控制及待证

C1 每份数据保留来源、用途、授权范围和保留期限。C2 撤销授权后立即阻止继续参与建议，另列物理删除进度。C3 备份恢复路径必须考虑已撤销数据再次进入活动系统的风险。C4 区分逻辑删除、备份到期、密码擦除、介质清除和可恢复性测试。C5 删除失败形成问题记录并允许人工申诉。C6 不以单个成功标志声称“完全删除”。全部UNADOPTED，未证明任何删除完整性。

下一阶段核对restic快照与密钥分离的公开文档，设计不涉及真实数据的可复算状态机反例；只有证据充分时才标记F007专题完成。本周F006已完成，F007当前为额外增量。
