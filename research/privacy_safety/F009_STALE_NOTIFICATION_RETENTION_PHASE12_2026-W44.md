# F009 第十二阶段：废弃通知渠道、保留期限与恢复救济
日期：2026-10-30 UTC，2026-W44。目标键：(privacy_safety,F009,phase12,stale-notification-channel-retention-and-recovery)。状态：COMPLETE_BOUNDED_STANDARD_PLUS_ARTIFICIAL_E1。

## 标准与风险边界
NIST SP 800-63B-4 https://pages.nist.gov/800-63-4/sp800-63b.html 要求支持至少两个通知地址，账户恢复触发通知，通知应发送至适用地址并提供否认事件的求助方式。NIST没有规定旧地址必须保存30天，也不等于消息实际送达。英国ICO存储期限指南 https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/ 要求根据用途证明保留期限，定期审查并删除不再必要的个人信息；其指南目前标注因英国法律变化正在审阅。ICO研究例外 https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/the-research-provisions/principles-and-grounds-for-processing/ 强调仅为研究目的保留的数据不能自动转作影响具体个人的决策用途。

人工攻击边界：已废弃邮箱可能转让给他人；为防恢复攻击而无限保存并持续发送旧邮箱，会造成个人隐私泄露。若立刻删除所有旧地址又没有新的已验证地址，合法用户可能失去恢复事件通知与救济路径。候选处理将地址状态分为ACTIVE、STALE、COMPROMISED；旧地址过期、用户要求删除或确认泄露时停止旧地址发送，并根据合法保留事由清理；没有可信通知路径则标记待人工复核及限制高风险动作。不可将邮件已发视为本人已收。

## 人工实验
源码 research/privacy_safety/f009_stale_channel_retention_phase12_20261030.js；Node.js 22.16.0本地执行24项断言通过，其中5项非法输入正确拒绝。候选示例以30天为本地假设保留期限，测试第29天与第30天边界、已废弃地址、泄露地址、删除请求、法律保留标志、申诉、无有效通知渠道、重复恢复方式及最小审计字段。恢复仅以人工布尔变量模拟，完全没有真实身份核验、通知发送、密码学、送达或账户。模型只表示受限候选政策，无法据此声称符合任何特定AAL；法律保留不代表自动获准发送到已废弃地址。审计收据仅包含事件类型、路由数量与是否清理旧渠道，仍可能因账户关联而属于个人数据，需要目的与期限约束。

STANDARD为官方英文标准及监管指南；ARTIFICIAL_E1为内部24项人工状态机测试；候选政策有效性、合法适用期限与跨司法辖区合规均UNKNOWN。新增真人E2=0，历史E3=0。没有真实敏感数据、账户、通知服务、付费API、云算力或Actions，账单未独立核验。下一phase13：研究多渠道送达证明缺失、被转让地址误投递及人工申诉的隐私和可用性权衡。
